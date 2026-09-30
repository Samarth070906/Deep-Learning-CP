#!/usr/bin/env python
"""Embedding utilities for TrustAgent evidence retrieval.

Uses sentence-transformers/all-MiniLM-L6-v2 to produce 384-dim L2-normalised
embeddings.  Embeddings for the generated dataset are computed once and cached
to ``<data_dir>/embeddings.npy`` alongside a JSON manifest that maps each
embedding row back to the original record_id.  Subsequent calls load from
cache unless ``force_recompute=True``.

Design note
-----------
The model's ``.encode()`` call already L2-normalises when we pass
``normalize_embeddings=True``.  Normalised vectors let us use FAISS
``IndexFlatIP`` so that inner-product == cosine similarity — simpler
scoring semantics than raw L2 distance.
"""

import json
import os
from pathlib import Path
from typing import List, Optional

import numpy as np

# Lazy-loaded to avoid heavy imports until actually needed
_model = None

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


def _get_model():
    """Return (and cache) the SentenceTransformer model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: List[str], batch_size: int = 64) -> np.ndarray:
    """Embed a list of strings and return an (N, 384) float32 array.

    Embeddings are L2-normalised so inner-product == cosine similarity.
    """
    model = _get_model()
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return embeddings.astype(np.float32)


def embed_query(text: str) -> np.ndarray:
    """Embed a single query string.  Returns shape (1, 384)."""
    return embed_texts([text])


# ---------------------------------------------------------------------------
# Dataset embedding cache
# ---------------------------------------------------------------------------

def _default_data_path() -> Path:
    """Resolve the default path to generated_records.json."""
    return Path(__file__).resolve().parent.parent / "data" / "generated" / "generated_records.json"


def _cache_dir(data_path: Path) -> Path:
    """Cache directory lives next to the dataset file."""
    return data_path.parent


def embed_dataset(
    data_path: Optional[str] = None,
    force_recompute: bool = False,
) -> tuple:
    """Embed every ``sources.text`` field in the generated dataset.

    Returns
    -------
    embeddings : np.ndarray, shape (N, 384)
        L2-normalised embeddings.
    records : list[dict]
        The full list of dataset records (same order as embeddings).
    """
    dp = Path(data_path) if data_path else _default_data_path()
    cache_dir = _cache_dir(dp)
    emb_path = cache_dir / "embeddings.npy"
    manifest_path = cache_dir / "embedding_manifest.json"

    # Load dataset
    with dp.open("r", encoding="utf-8") as f:
        records = json.load(f)

    # Check cache validity
    if (
        not force_recompute
        and emb_path.exists()
        and manifest_path.exists()
    ):
        cached_embs = np.load(str(emb_path))
        with manifest_path.open("r", encoding="utf-8") as f:
            manifest = json.load(f)
        # Validate length match
        if len(manifest) == len(records) and cached_embs.shape[0] == len(records):
            print(f"[embed] Loaded cached embeddings from {emb_path}  ({cached_embs.shape})")
            return cached_embs, records

    # Compute fresh embeddings
    texts = [rec["sources"]["text"] for rec in records]
    print(f"[embed] Embedding {len(texts)} source texts with {MODEL_NAME} ...")
    embeddings = embed_texts(texts)

    # Save cache
    np.save(str(emb_path), embeddings)
    manifest = [rec["record_id"] for rec in records]
    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"[embed] Cached embeddings ({embeddings.shape}) -> {emb_path}")

    return embeddings, records
