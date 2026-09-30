#!/usr/bin/env python
"""Phase 3 sanity-check test for TrustAgent evidence retrieval.

Tests run on the FULL generated dataset:
  1. Self-retrieval:  10 randomly sampled claims (balanced labels) --
     does retrieve() surface the originating record in top-3?
  2. Cross-modal evidence check:  5 randomly sampled claims --
     does the retrieved record carry the correct ``image_path`` and
     ``document_excerpt`` alongside the matching text?

Usage:
    python -m trustagent.retrieval.test_retrieval
"""

import json
import random
import sys
from pathlib import Path
from typing import List, Dict, Any

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _load_records() -> List[Dict[str, Any]]:
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data" / "generated" / "generated_records.json"
    )
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _select_balanced_sample(records, n=10, seed=42):
    """Randomly sample *n* records with balanced label mix."""
    rng = random.Random(seed)
    consistent = [r for r in records if r["label"] == "CONSISTENT"]
    contradictory = [r for r in records if r["label"] == "CONTRADICTORY"]
    half = n // 2
    c_sample = rng.sample(consistent, min(half, len(consistent)))
    d_sample = rng.sample(contradictory, min(n - half, len(contradictory)))
    selected = c_sample + d_sample
    rng.shuffle(selected)
    return selected[:n]


# ---------------------------------------------------------------------------
# Main test
# ---------------------------------------------------------------------------

def main() -> None:
    from trustagent.retrieval.embed import embed_dataset
    from trustagent.retrieval.index import build_and_save
    from trustagent.retrieval.retrieve import retrieve, reset_cache

    records = _load_records()
    total = len(records)
    n_con = sum(1 for r in records if r["label"] == "CONSISTENT")
    n_ctr = total - n_con

    print("=" * 72)
    print("TrustAgent Phase 3 -- Retrieval Sanity Check (full-scale)")
    print("=" * 72)
    print(f"Dataset size : {total} records")
    print(f"Labels       : {n_con} CONSISTENT, {n_ctr} CONTRADICTORY")
    print()

    # Always rebuild embeddings + index over current data
    print("[test] Rebuilding embeddings and FAISS index ...")
    build_and_save(force_recompute=True)
    print()

    # ------------------------------------------------------------------
    # TEST 1: Self-retrieval (10 claims)
    # ------------------------------------------------------------------
    test_claims = _select_balanced_sample(records, n=10)
    k = 3
    hits = 0
    misses = []
    reset_cache()

    print(f"=== Self-retrieval test ({len(test_claims)} claims, top-{k}) ===")
    print()

    for i, rec in enumerate(test_claims, start=1):
        claim_text = rec["sources"]["text"]
        claim_id = rec["record_id"]
        claim_label = rec["label"]

        results = retrieve(claim_text, k=k)
        retrieved_ids = [r["record"]["record_id"] for r in results]
        self_hit = claim_id in retrieved_ids

        if self_hit:
            hits += 1
        else:
            misses.append(rec)

        status = ">> HIT" if self_hit else ">> MISS"
        print(f"-- Claim {i}/{len(test_claims)}  [{claim_label}]  {status} --")
        print(f"   record_id : {claim_id}")
        print(f"   claim     : \"{claim_text}\"")
        for r in results:
            marker = " <-- SELF" if r["record"]["record_id"] == claim_id else ""
            print(f"   #{r['rank']}  score={r['score']:.4f}  "
                  f"id={r['record']['record_id']}  "
                  f"label={r['record']['label']}{marker}")
        print()

    # Investigate misses
    if misses:
        print("--- Investigating misses ---")
        for rec in misses:
            claim_text = rec["sources"]["text"]
            # Get top-10 to see where the self-match actually ranked
            extended = retrieve(claim_text, k=min(20, total))
            self_rank = None
            for r in extended:
                if r["record"]["record_id"] == rec["record_id"]:
                    self_rank = r["rank"]
                    break
            if self_rank:
                print(f"  {rec['record_id']}: self-match at rank {self_rank} "
                      f"(out of top-{k} window)")
            else:
                print(f"  {rec['record_id']}: self-match NOT FOUND "
                      f"(possible duplicate text across records)")
            # Check if another record has identical text
            same_text = [r for r in records
                         if r["sources"]["text"] == claim_text
                         and r["record_id"] != rec["record_id"]]
            if same_text:
                print(f"    -> {len(same_text)} other record(s) share identical text:")
                for sr in same_text[:3]:
                    print(f"       {sr['record_id']} [{sr['label']}]")
        print()

    # ------------------------------------------------------------------
    # TEST 2: Cross-modal evidence check (5 claims)
    # ------------------------------------------------------------------
    cross_sample = _select_balanced_sample(records, n=5, seed=99)
    cross_pass = 0

    print(f"=== Cross-modal evidence check ({len(cross_sample)} claims) ===")
    print()

    for i, rec in enumerate(cross_sample, start=1):
        claim_text = rec["sources"]["text"]
        expected_img = rec["sources"]["image_path"]
        expected_doc = rec["sources"]["document_excerpt"]

        results = retrieve(claim_text, k=k)

        # Find self-match
        self_match = None
        for r in results:
            if r["record"]["record_id"] == rec["record_id"]:
                self_match = r["record"]
                break

        if self_match is None:
            print(f"  [{i}] SKIP -- self-match not in top-{k} for "
                  f"{rec['record_id']}")
            continue

        actual_img = self_match["sources"]["image_path"]
        actual_doc = self_match["sources"]["document_excerpt"]
        img_ok = (actual_img == expected_img)
        doc_ok = (actual_doc == expected_doc)

        if img_ok and doc_ok:
            cross_pass += 1
            print(f"  [{i}] PASS  {rec['record_id']}")
            print(f"        image_path       : {actual_img}")
            print(f"        document_excerpt : {actual_doc}")
        else:
            print(f"  [{i}] FAIL  {rec['record_id']}")
            if not img_ok:
                print(f"        image_path expected : {expected_img}")
                print(f"        image_path actual   : {actual_img}")
            if not doc_ok:
                print(f"        doc_excerpt expected : {expected_doc}")
                print(f"        doc_excerpt actual   : {actual_doc}")
    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 72)
    print(f"Self-retrieval  : {hits}/{len(test_claims)} claims in top-{k}")
    threshold = min(9, len(test_claims))
    retrieval_ok = hits >= threshold
    print(f"  Threshold (>={threshold}/{len(test_claims)}) : "
          f"{'PASS' if retrieval_ok else 'FAIL'}")
    print(f"Cross-modal     : {cross_pass}/{len(cross_sample)} records matched")
    cross_ok = cross_pass == len(cross_sample)
    print(f"  Full match    : {'PASS' if cross_ok else 'FAIL'}")
    print("=" * 72)

    if not retrieval_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
