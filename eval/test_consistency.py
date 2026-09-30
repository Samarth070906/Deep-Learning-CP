import json
import random
import os
import sys
import numpy as np
import os
import sys
from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

# Add trustagent to path if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from trustagent.models.text_verifier.verifier import verify_text
from trustagent.models.image_verifier.verifier import verify_image
from trustagent.data.generator.seed_data import data as seed_data
from trustagent.models.consistency_net.features import build_features
from trustagent.models.consistency_net.model import MultiModalConsistencyNet

def load_data():
    data_path = Path(__file__).resolve().parent.parent / "data" / "generated" / "generated_records.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_true_claim(entity, attribute):
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = f" {attr['unit']}" if attr.get("unit") else ""
                return f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_str}."
    return None

def extract_features(records, support_thresh=0.3594, contradict_thresh=0.3394):
    features = []
    labels = []
    print(f"Extracting features for {len(records)} records...")
    
    for i, record in enumerate(records):
        claim = get_true_claim(record["entity"], record["attribute"])
        if not claim: continue
            
        evidence_text = record["sources"]["text"]
        image_path = record["sources"]["image_path"]
        is_visual = record.get("visually_verifiable", False)
        
        # Text verify
        t_label, t_score = verify_text(claim, evidence_text)
        
        # Image verify
        if is_visual and image_path:
            i_label, i_score = verify_image(claim, image_path, support_thresh, contradict_thresh, is_visual)
        else:
            i_label, i_score = "NO_EVIDENCE", 0.0
            
        vec = build_features(t_label, t_score, i_label, i_score)
        
        features.append(vec)
        # Target: 1.0 for CONSISTENT, 0.0 for CONTRADICTORY
        label = 1.0 if record["label"] == "CONSISTENT" else 0.0
        labels.append([label])
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i+1}/{len(records)} records")
            
    return torch.tensor(features, dtype=torch.float32), torch.tensor(labels, dtype=torch.float32)

def train_and_evaluate():
    # Fixed random seeds for reproducibility
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    records = load_data()
    random.shuffle(records)
    
    split_idx = int(len(records) * 0.8)
    train_records = records[:split_idx]
    test_records = records[split_idx:]
    
    # Check if features are cached to save time during dev
    feat_cache = Path("d:/Third Year/DL/CP/trustagent/data/generated/features.pt")
    if feat_cache.exists():
        print("Loading cached features...")
        cache = torch.load(feat_cache)
        train_x, train_y = cache['train_x'], cache['train_y']
        test_x, test_y = cache['test_x'], cache['test_y']
    else:
        train_x, train_y = extract_features(train_records)
        test_x, test_y = extract_features(test_records)
        torch.save({'train_x': train_x, 'train_y': train_y, 'test_x': test_x, 'test_y': test_y}, feat_cache)
        
    print(f"Train size: {train_x.shape[0]}, Test size: {test_x.shape[0]}")
    
    # Train MLP
    model = MultiModalConsistencyNet(input_dim=5, hidden_dim=64)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.005)
    
    train_dataset = TensorDataset(train_x, train_y)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    epochs = 30
    model.train()
    print("Training ConsistencyNet...")
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            preds = model(batch_x)
            loss = criterion(preds, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        if (epoch+1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs} | Loss: {epoch_loss/len(train_loader):.4f}")
            
    # Save checkpoint
    checkpoint_path = Path("d:/Third Year/DL/CP/trustagent/models/consistency_net/checkpoint.pt")
    torch.save(model.state_dict(), checkpoint_path)
    print(f"Checkpoint saved to {checkpoint_path}")
            
    # Evaluate from SAVED checkpoint
    eval_model = MultiModalConsistencyNet(input_dim=5, hidden_dim=64)
    eval_model.load_state_dict(torch.load(checkpoint_path))
    eval_model.eval()
    with torch.no_grad():
        test_preds_probs = eval_model(test_x)
        test_preds = (test_preds_probs >= 0.5).float()
        
    # We want contradiction detection metrics.
    # Contradiction is class 0 (target 0.0). Let's treat CONTRADICTORY as the positive class for PR/F1.
    true_contradictions = (test_y == 0.0).float()
    pred_contradictions = (test_preds == 0.0).float()
    
    tp = (pred_contradictions * true_contradictions).sum().item()
    fp = (pred_contradictions * (1 - true_contradictions)).sum().item()
    fn = ((1 - pred_contradictions) * true_contradictions).sum().item()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("\n--- Contradiction Detection Metrics (Overall) ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Split evaluation
    # Extract num_modalities from test_x (it's the 3rd feature, index 2)
    num_mods = test_x[:, 2]
    mask_both = (num_mods == 2.0)
    mask_text_only = (num_mods == 1.0) & (test_x[:, 0] > 0.0) # has text score
    mask_image_only = (num_mods == 1.0) & (test_x[:, 1] > 0.0) # has image score
    mask_neither = (num_mods == 0.0)
    
    splits = [
        ("Both Modalities Present", mask_both), 
        ("Text-Only", mask_text_only),
        ("Image-Only", mask_image_only),
        ("Neither (NO_EVIDENCE)", mask_neither)
    ]
    
    for name, mask in splits:
        print(f"\n--- Metrics: {name} ({mask.sum().item()} samples) ---")
        if mask.sum().item() == 0:
            print("No samples in this split.")
            continue
            
        m_true = true_contradictions[mask]
        m_pred = pred_contradictions[mask]
        
        m_tp = (m_pred * m_true).sum().item()
        m_fp = (m_pred * (1 - m_true)).sum().item()
        m_fn = ((1 - m_pred) * m_true).sum().item()
        
        m_prec = m_tp / (m_tp + m_fp) if (m_tp + m_fp) > 0 else 0
        m_rec = m_tp / (m_tp + m_fn) if (m_tp + m_fn) > 0 else 0
        m_f1 = 2 * (m_prec * m_rec) / (m_prec + m_rec) if (m_prec + m_rec) > 0 else 0
        
        print(f"Precision: {m_prec:.4f}")
        print(f"Recall:    {m_rec:.4f}")
        print(f"F1-Score:  {m_f1:.4f}")
    
    # Calibration Curve (Binning predicted probabilities)
    print("\n--- Calibration Curve Data ---")
    # We output probability of CONSISTENT (1.0). Let's print bins.
    probs = test_preds_probs.squeeze().numpy()
    labels = test_y.squeeze().numpy()
    
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    for i in range(len(bins)-1):
        low, high = bins[i], bins[i+1]
        in_bin = (probs >= low) & (probs < high)
        if i == len(bins) - 2:
            in_bin = (probs >= low) & (probs <= high) # include 1.0
            
        count = in_bin.sum()
        if count > 0:
            true_prob = labels[in_bin].mean()
            pred_prob = probs[in_bin].mean()
            print(f"Bin [{low:.1f}, {high:.1f}]: count={count:3d}, avg_pred={pred_prob:.3f}, true_frac={true_prob:.3f}")
        else:
            print(f"Bin [{low:.1f}, {high:.1f}]: count=  0, no data")
            
    print("Phase 5 Evaluation Complete.")

if __name__ == "__main__":
    train_and_evaluate()
