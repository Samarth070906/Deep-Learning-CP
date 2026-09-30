#!/usr/bin/env python
"""FAISS index management for TrustAgent evidence retrieval.

Index type: ``IndexFlatIP`` (inner product on L2-normalised vectors).

Why IndexFlatIP over IndexFlatL2?
---------------------------------
``all-MiniLM-L6-v2`` embeddings are L2-normalised (unit length).  For unit
vectors the inner product equals cosine similarity, which is the standard
measure for semantic similarity.  Using IP means the raw FAISS scores
*are* cosine similarities (0–1 range, higher = more similar), making
downstream interpretation trivial.  ``IndexFlatL2`` would return squared
Euclidean distances where *lower* is better — workable but less intuitive,
and the conversion ``cos = 1 − d²/2`` adds noise from float precision.

Persistence
-----------
The index is written to / loaded from ``<data_dir>/faiss.index``.
"""

from pathlib import Path
from typing import Optional

import faiss
import numpy as np

from .embed import embed_dataset, EMBEDDING_DIM


def _default_index_path() -> Path:
    return Path(__file__).resolve().parent.parent / "data" / "generated" / "faiss.index"


def build_index(
    embeddings: np.ndarray,
    save_path: Optional[str] = None,
) -> faiss.IndexFlatIP:
    """Build and optionally persist a FAISS flat inner-product index.

    Parameters
    ----------
    embeddings : np.ndarray, shape (N, 384)
        Must be L2-normalised (guaranteed by embed module).
    save_path : str or None
        If given, write the index here; otherwise use the default location.

    Returns
    -------
    faiss.IndexFlatIP
    """
    dim = embeddings.shape[1]
    assert dim == EMBEDDING_DIM, f"Expected {EMBEDDING_DIM}-dim, got {dim}"

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    print(f"[index] Built IndexFlatIP with {index.ntotal} vectors (dim={dim})")

    sp = Path(save_path) if save_path else _default_index_path()
    sp.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(sp))
    print(f"[index] Saved index -> {sp}")

    return index


def load_index(index_path: Optional[str] = None) -> faiss.IndexFlatIP:
    """Load a previously saved FAISS index from disk."""
    ip = Path(index_path) if index_path else _default_index_path()
    if not ip.exists():
        raise FileNotFoundError(
            f"FAISS index not found at {ip}.  "
            "Run `build_index()` or `python -m trustagent.retrieval.index` first."
        )
    index = faiss.read_index(str(ip))
    print(f"[index] Loaded index ({index.ntotal} vectors) from {ip}")
    return index


def build_and_save(
    data_path: Optional[str] = None,
    index_path: Optional[str] = None,
    force_recompute: bool = False,
) -> faiss.IndexFlatIP:
    """Convenience: embed the dataset, build index, save, return index."""
    embeddings, _ = embed_dataset(data_path, force_recompute=force_recompute)
    return build_index(embeddings, save_path=index_path)


# Allow running as a standalone script:
#   python -m trustagent.retrieval.index
if __name__ == "__main__":
    build_and_save()
