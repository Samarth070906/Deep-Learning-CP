import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
import json
from pathlib import Path
from scipy.stats import pearsonr
from sklearn.metrics import mean_absolute_error
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
from trustagent.models.consistency_net.model import MultiModalConsistencyNet
from trustagent.models.trust_score_net.metadata_lookup import get_record_features
from trustagent.models.trust_score_net.numeric_parser import get_numeric_deviation

class TrustScoreNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    def forward(self, x):
        return self.net(x) * 100.0

def get_true_claim_and_unit(entity, attribute):
    from trustagent.data.generator.seed_data import data as seed_data
    for product in seed_data:
        if product["entity"] == entity:
            if attribute in product["attributes"]:
                attr = product["attributes"][attribute]
                unit_str = attr.get('unit', '')
                unit_display = f" {unit_str}" if unit_str else ""
                claim = f"{attribute.replace('_', ' ').title()} of {entity} is {attr['value']}{unit_display}."
                return claim, unit_str
    return None, None

def main():
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    data_path = Path("d:/Third Year/DL/CP/trustagent/data/generated/generated_records.json")
    with open(data_path, "r", encoding="utf-8") as f:
        records = json.load(f)
        
    random.seed(42)
    shuffled_records = list(records)
    random.shuffle(shuffled_records)
    split_idx = int(len(shuffled_records) * 0.8)
    ordered_records = shuffled_records[:split_idx] + shuffled_records[split_idx:]
    
    random.seed(seed)
    
    cache = torch.load("d:/Third Year/DL/CP/trustagent/data/generated/features.pt")
    all_x = torch.cat([cache['train_x'], cache['test_x']], dim=0)
    all_y = torch.cat([cache['train_y'], cache['test_y']], dim=0)
    
    cons_net = MultiModalConsistencyNet(input_dim=5, hidden_dim=64)
    cons_net.load_state_dict(torch.load("d:/Third Year/DL/CP/trustagent/models/consistency_net/checkpoint.pt"))
    cons_net.eval()
    
    with torch.no_grad():
        consistency_scores = cons_net(all_x).squeeze()
        
    evidence_availables = all_x[:, 4] 
    
    train_X = []
    train_Y = []
    
    for i in range(len(all_x)):
        c_score = consistency_scores[i].item()
        e_avail = evidence_availables[i].item()
        num_modalities = all_x[i, 2].item()
        modality_conf = max(all_x[i, 0].item(), all_x[i, 1].item())
        is_consistent = (all_y[i].item() == 1.0)
        
        if e_avail == 0.0: c_score = 0.0
        
        avg_conf = random.uniform(0.5, 1.0) if e_avail else 0.0
        r_id = ordered_records[i]["record_id"]
        rel, risk = get_record_features(r_id)
        
        record = ordered_records[i]
        claim_text, unit = get_true_claim_and_unit(record["entity"], record["attribute"])
        evidence_text = record["sources"]["text"]
        num_dev = get_numeric_deviation(claim_text, evidence_text, unit)
            
        # Updated target formula to fix single-modality SUPPORT capping
        if e_avail == 0.0:
            y = 50 - (risk * 40) + (rel * 10)
        elif num_modalities == 1.0 and modality_conf > 0.9:
            # Bypass consistency_score neutral cap! Use the strong modality's own signal.
            if is_consistent:
                y = modality_conf * 90 + (rel * 10) - (risk * 10)
            else:
                y = 10 + (rel * 5) - (risk * 15)
                if num_dev != -1.0 and num_dev > 0.05:
                    y -= 30 * min(num_dev / 0.2, 1.0)
        else:
            y = c_score * 70 + avg_conf * 10 + rel * 10 - risk * 10
            if num_dev != -1.0 and num_dev > 0.05:
                y -= 30 * min(num_dev / 0.2, 1.0) 
            if c_score < 0.3: y -= 20
            
        y = max(0.0, min(100.0, y))
        
        train_X.append([c_score, e_avail, avg_conf, rel, risk, num_dev])
        train_Y.append([y])
        
    train_X = torch.tensor(train_X, dtype=torch.float32)
    train_Y = torch.tensor(train_Y, dtype=torch.float32)
    
    model = TrustScoreNet()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    print(f"Training TrustScoreNet on {len(train_X)} records...")
    for epoch in range(300):
        optimizer.zero_grad()
        preds = model(train_X)
        loss = criterion(preds, train_Y)
        loss.backward()
        optimizer.step()
        
    ckpt_path = Path("d:/Third Year/DL/CP/trustagent/models/trust_score_net/checkpoint.pt")
    torch.save(model.state_dict(), ckpt_path)
    print("Saved checkpoint.")

if __name__ == "__main__":
    main()
