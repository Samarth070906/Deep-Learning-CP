"""Perturbation utilities for TrustAgent synthetic dataset generation.

Generates CONSISTENT and CONTRADICTORY records from seed data.  Every
attribute of every seed product is processed (not randomly sampled), with
five consistent and five contradictory variants per attribute to maintain
exact 50/50 label balance.

Design
------
* **Consistent records** reuse the correct attribute value but vary the
  sentence phrasing via ``_CONSISTENT_TEMPLATES``.  All templates include
  the entity name so that embeddings are distinguishable across products
  even when the attribute type (e.g. "price") overlaps.

* **Contradictory records** perturb the numeric value with controlled
  magnitudes and alter one or two source modalities (text, image).
  Document perturbation is intentionally omitted for MVP (documents
  deferred per Phase 2 review).
"""

import copy
import random
from typing import Dict, Any, List

# ---------------------------------------------------------------------------
# Unique record-ID counter (deterministic within a single generation run)
# ---------------------------------------------------------------------------
_id_counter = 0


def _next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


def reset_id_counter() -> None:
    """Reset the counter (call at the start of each generation run)."""
    global _id_counter
    _id_counter = 0


# ---------------------------------------------------------------------------
# Text templates (all include {entity} for embedding distinctiveness)
# ---------------------------------------------------------------------------
_CONSISTENT_TEMPLATES = [
    "{attr_name} of the {entity} is {value} {unit}.",
    "The {entity}'s {attr_name} is {value} {unit}.",
    "{entity} offers {value} {unit} for {attr_name}.",
    "With a {attr_name} of {value} {unit}, the {entity} delivers.",
    "Rated at {value} {unit}, the {entity}'s {attr_name} impresses.",
]

_CONTRADICTORY_TEMPLATES = [
    "{attr_name} of the {entity} is {value} {unit}.",
    "The {entity}'s {attr_name} measures {value} {unit}.",
    "{entity} reports {value} {unit} for {attr_name}.",
    "According to tests, the {entity} has {attr_name} of {value} {unit}.",
    "Updated specs show the {entity}'s {attr_name} at {value} {unit}.",
]


# ---------------------------------------------------------------------------
# Numeric perturbation
# ---------------------------------------------------------------------------

def _perturb_value(value: str, magnitude: float = 0.10) -> str:
    """Perturb a value (numeric or string)."""
    try:
        num = float(value)
        sign = random.choice([-1, 1])
        delta = num * random.uniform(magnitude * 0.5, magnitude * 1.5) * sign
        new_val = round(num + delta, 2)
        # Guarantee the value actually changed
        if new_val == num:
            new_val = round(num * (1.0 + magnitude), 2)
        if new_val == int(new_val):
            return str(int(new_val))
        return str(new_val)
    except ValueError:
        colors = ["Midnight Black", "Silver", "Space Gray", "Crimson Red", "White", "Blue", "Neon Green", "Cyan", "Purple", "Rose Gold"]
        available = [c for c in colors if c.lower() not in value.lower()]
        return random.choice(available) if available else "Slate Gray"


# ---------------------------------------------------------------------------
# Single-attribute record generators
# ---------------------------------------------------------------------------

def _generate_consistent(seed: Dict, attr_key: str, template_idx: int = 0) -> Dict:
    """Generate a consistent record for a specific attribute using a template."""
    product = copy.deepcopy(seed)
    attr = product["attributes"][attr_key]
    t = _CONSISTENT_TEMPLATES[template_idx % len(_CONSISTENT_TEMPLATES)]
    attr_display = attr_key.replace("_", " ").title()
    attr["text"] = t.format(
        entity=product["entity"],
        attr_name=attr_display,
        value=attr["value"],
        unit=attr.get("unit", ""),
    )
    return product


def _generate_contradictory(
    seed: Dict, attr_key: str,
    sources_to_alter: List[str],
    magnitude: float = 0.10,
    template_idx: int = 0,
) -> Dict:
    """Generate a contradictory record by perturbing specified sources."""
    product = copy.deepcopy(seed)
    attr = product["attributes"][attr_key]
    new_value = _perturb_value(attr["value"], magnitude)
    attr_display = attr_key.replace("_", " ").title()

    if "text" in sources_to_alter:
        t = _CONTRADICTORY_TEMPLATES[template_idx % len(_CONTRADICTORY_TEMPLATES)]
        attr["text"] = t.format(
            entity=product["entity"],
            attr_name=attr_display,
            value=new_value,
            unit=attr.get("unit", ""),
        )

    if "image" in sources_to_alter and attr.get("image"):
        parts = attr["image"].split("/")
        attr["image"] = "/".join(parts[:-1] + [f"altered_{parts[-1]}"])

    attr["perturbed_value"] = new_value
    return product


# ---------------------------------------------------------------------------
# Schema converter
# ---------------------------------------------------------------------------

def _to_schema(
    product: Dict, attr_key: str,
    perturbed_field, label: str, num_altered: int,
) -> Dict[str, Any]:
    """Convert an internal product dict to the output JSON schema."""
    attr = product["attributes"][attr_key]
    sources = {
        "text": attr.get("text"),
        "image_path": attr.get("image"),
        "document_excerpt": attr.get("document"),
    }
    entity_slug = product["entity"].replace(" ", "_")
    return {
        "record_id": f"{entity_slug}_{attr_key}_{_next_id():05d}",
        "entity": product["entity"],
        "attribute": attr_key,
        "domain": product.get("domain", "unknown"),
        "sources": sources,
        "perturbed_field": perturbed_field,
        "label": label,
        "num_sources_altered": num_altered,
        "visually_verifiable": attr.get("visually_verifiable", False)
    }


# ---------------------------------------------------------------------------
# Per-attribute record generation (balanced: 5 CONSISTENT + 5 CONTRADICTORY)
# ---------------------------------------------------------------------------

def _generate_for_attribute(seed: Dict, attr_key: str) -> List[Dict[str, Any]]:
    """Generate 10 balanced records for one attribute of one product."""
    records: List[Dict[str, Any]] = []

    # 5 consistent records - different text templates, same correct value
    for i in range(5):
        c = _generate_consistent(seed, attr_key, template_idx=i)
        records.append(_to_schema(c, attr_key, None, "CONSISTENT", 0))

    # 5 contradictory records - varied perturbation strategies
    # (sources_to_alter, magnitude, template_idx)
    contra_configs = [
        (["text"],            0.08, 0),   # small text perturbation
        (["text"],            0.20, 1),   # medium text perturbation
        (["text"],            0.35, 2),   # large text perturbation
        (["image"],           0.10, 0),   # image-only alteration
        (["text", "image"],   0.15, 3),   # multi-source perturbation
    ]
    for sources, mag, tidx in contra_configs:
        d = _generate_contradictory(seed, attr_key, sources, mag, tidx)
        pfield = sources[0] if len(sources) == 1 else "multiple"
        records.append(_to_schema(d, attr_key, pfield, "CONTRADICTORY", len(sources)))

    return records


# ---------------------------------------------------------------------------
# Public API (used by generate.py)
# ---------------------------------------------------------------------------

def generate_record(seed: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate records for ALL attributes of a seed product.

    Returns a list of dicts matching the output schema, with exact 50/50
    CONSISTENT/CONTRADICTORY balance (5 of each per attribute).
    """
    records: List[Dict[str, Any]] = []
    for attr_key in seed["attributes"]:
        records.extend(_generate_for_attribute(seed, attr_key))
    return records
