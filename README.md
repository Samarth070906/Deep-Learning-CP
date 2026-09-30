# TrustAgent

Verification layer for autonomous AI agent outputs.

## Overview
- **Phase 1** – Scope lock (text + image only)
- **Phase 2** – Synthetic dataset generator (e-commerce domain)
- **Phase 3** – Retrieval with FAISS (DONE)
- **Phase 4** – Modality verifiers (DeBERTa, CLIP)
- **Phase 5** – MultiModalConsistencyNet (4-dim input: text_score, image_score, num_modalities_available, pairwise_disagreement_flag)
- **Phase 6** – TrustScoreNet
- **Phase 7** – Decision & explanation
- **Phase 8** – FastAPI backend + React/Vite UI

> **Note (Phase 2 review):** `doc_score` has been dropped from the
> MultiModalConsistencyNet input vector for MVP.  Documents are deferred.
> Stage 5 input is now 4-dim (was 5-dim with a sentinel-collision bug).

## Repository layout
```
trustagent/
├── data/
│   ├── generator/          # synthetic dataset generation scripts
│   ├── raw/                # scraped source records (gitignored)
│   └── generated/          # generated JSON records + embeddings + FAISS index
├── models/
│   ├── text_verifier/
│   ├── image_verifier/
│   ├── consistency_net/
│   └── trust_score_net/
├── retrieval/              # Phase 3: sentence-transformer embeddings + FAISS
│   ├── embed.py            # embedding function (cached to .npy)
│   ├── index.py            # FAISS IndexFlatIP build/save/load
│   ├── retrieve.py         # retrieve(claim_text, k=3) top-k function
│   └── test_retrieval.py   # sanity-check test (5/5 self-retrieval PASS)
├── pipeline/
├── backend/
├── frontend/
├── eval/
├── notebooks/
├── requirements.txt
└── README.md
```

