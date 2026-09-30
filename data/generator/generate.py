#!/usr/bin/env python
"""Dataset generator entry point for TrustAgent.

Usage:
    python -m trustagent.data.generator.generate [--num-seeds N] [--output-dir DIR]

The script loads the seed product catalogue from ``seed_data.py``, generates
balanced CONSISTENT/CONTRADICTORY records for every attribute of every seed,
and writes the resulting JSON file to ``--output-dir``.

With the default 30-seed catalogue and 4 attributes per seed, the generator
produces 1,200 records (600 CONSISTENT + 600 CONTRADICTORY).
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

from .seed_data import data as seed_data
from .perturbation import generate_record, reset_id_counter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TrustAgent synthetic dataset generator")
    parser.add_argument(
        "--num-seeds",
        type=int,
        default=None,
        help="Number of seed products to use (default: all available seeds).",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="trustagent/data/generated",
        help="Directory where the generated JSON file will be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Select seeds
    if args.num_seeds is None:
        selected_seeds: List[Dict[str, Any]] = seed_data
    else:
        selected_seeds = seed_data[: args.num_seeds]

    if not selected_seeds:
        print("[ERROR] No seed records available.", file=sys.stderr)
        sys.exit(1)

    # Reset ID counter for deterministic record IDs
    reset_id_counter()

    all_records: List[Dict[str, Any]] = []
    for seed in selected_seeds:
        all_records.extend(generate_record(seed))

    # Stats
    total = len(all_records)
    consistent = sum(1 for r in all_records if r["label"] == "CONSISTENT")
    contradictory = total - consistent
    balance_pct = consistent / total * 100 if total else 0
    print(f"Generated {total} records: "
          f"{consistent} CONSISTENT ({balance_pct:.1f}%), "
          f"{contradictory} CONTRADICTORY ({100 - balance_pct:.1f}%)")

    # Validate schema keys
    required_keys = {
        "record_id", "entity", "attribute", "domain", "sources",
        "perturbed_field", "label", "num_sources_altered", "visually_verifiable"
    }
    for rec in all_records:
        missing = required_keys - rec.keys()
        if missing:
            print(f"[ERROR] Record {rec.get('record_id')} missing keys: {missing}",
                  file=sys.stderr)
            sys.exit(1)

    # Check ID uniqueness
    ids = [r["record_id"] for r in all_records]
    if len(ids) != len(set(ids)):
        dupes = [rid for rid in ids if ids.count(rid) > 1]
        print(f"[ERROR] Duplicate record IDs found: {set(dupes)}", file=sys.stderr)
        sys.exit(1)

    out_path = output_dir / "generated_records.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)
    print(f"Wrote generated dataset to {out_path}")


if __name__ == "__main__":
    main()
