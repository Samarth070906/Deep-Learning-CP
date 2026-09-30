#!/usr/bin/env python
"""Core retrieval function for TrustAgent.

``retrieve(claim_text, k=3)`` embeds the input claim and returns the top-k
most similar source records from the generated dataset, together with their
cosine-similarity scores.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import numpy as np

from .embed import embed_query, embed_dataset
from .index import load_index, build_and_save


# Module-level cache so repeated calls don't reload from disk
_index = None
_records = None


def _ensure_loaded(
    data_path: Optional[str] = None,
    index_path: Optional[str] = None,
) -> None:
    """Lazily load (or build) the FAISS index and the records list."""
    global _index, _records

    if _index is not None and _records is not None:
        return

    # Load records
    dp = Path(data_path) if data_path else (
        Path(__file__).resolve().parent.parent / "data" / "generated" / "generated_records.json"
    )
    with dp.open("r", encoding="utf-8") as f:
        _records = json.load(f)

    # Load or build index
    ip = Path(index_path) if index_path else (
        Path(__file__).resolve().parent.parent / "data" / "generated" / "faiss.index"
    )
    if ip.exists():
        _index = load_index(str(ip))
    else:
        print("[retrieve] Index not found -- building now ...")
        _, _ = embed_dataset(str(dp))           # ensure embeddings exist
        _index = build_and_save(str(dp), str(ip))


def retrieve(
    claim_text: str,
    k: int = 3,
    data_path: Optional[str] = None,
    index_path: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return the top-k most similar source records for an input claim.

    Parameters
    ----------
    claim_text : str
        The claim to search for evidence against.
    k : int
        Number of results to return (default 3).
    data_path : str, optional
        Path to generated_records.json.
    index_path : str, optional
        Path to faiss.index.

    Returns
    -------
    list[dict]
        Each dict contains:
        - ``record`` : the full dataset record (dict)
        - ``score``  : cosine similarity (float, 0–1)
        - ``rank``   : 1-based rank
    """
    _ensure_loaded(data_path, index_path)

    # Clamp k to available records
    effective_k = min(k, _index.ntotal)

    query_emb = embed_query(claim_text)                # shape (1, 384)
    scores, indices = _index.search(query_emb, effective_k)  # each shape (1, k)

    results = []
    for rank, (idx, score) in enumerate(zip(indices[0], scores[0]), start=1):
        if idx == -1:
            continue  # FAISS returns -1 for unfilled slots
        results.append({
            "record": _records[idx],
            "score": float(score),
            "rank": rank,
        })

    return results


def reset_cache() -> None:
    """Clear the module-level cache (useful for testing / re-loading data)."""
    global _index, _records
    _index = None
    _records = None
