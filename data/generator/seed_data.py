"""Seed data for TrustAgent synthetic dataset generator.

Provides 30 diverse product definitions across six domains. Each product has
several attributes with realistic values.
"""

_TEMPLATES = [
    "The {entity} has a {attr} of {value} {unit}.",
    "{entity} features {value} {unit} for its {attr}.",
    "With {value} {unit} {attr}, the {entity} stands out in its class.",
    "The {attr} on the {entity} is rated at {value} {unit}.",
    "At {value} {unit}, the {entity}'s {attr} is competitive.",
    "{entity} delivers {value} {unit} of {attr}.",
    "Boasting {value} {unit} {attr}, the {entity} impresses reviewers.",
    "The {entity} ships with {value} {unit} {attr}.",
    "Independent tests confirm the {entity}'s {attr} at {value} {unit}.",
    "For {attr}, the {entity} offers {value} {unit}.",
]

_VISUAL_TEMPLATES = [
    "The {entity} is available in {value}.",
    "The color of the {entity} is {value}.",
    "{entity} features a stunning {value} finish.",
    "A beautiful {value} design defines the {entity}.",
    "The {entity} comes in {value}.",
]

def _make_attr(entity, attr_name, value, unit, slug, has_doc, template_idx, is_visual=False):
    """Build one attribute dict from compact parameters."""
    if is_visual:
        t = _VISUAL_TEMPLATES[template_idx % len(_VISUAL_TEMPLATES)]
        unit_str = "" # visual attributes like color usually don't have units
    else:
        t = _TEMPLATES[template_idx % len(_TEMPLATES)]
        unit_str = unit
        
    attr_display = attr_name.replace("_", " ")
    text = t.format(entity=entity, attr=attr_display, value=value, unit=unit_str).strip()
    return {
        "value": str(value),
        "unit": unit,
        "text": text,
        "image": f"images/{slug}_{attr_name}.jpg",
        "document": f"specs/{slug}_{attr_name}_spec.pdf" if has_doc else None,
        "visually_verifiable": is_visual
    }

_PRODUCTS = [
    ("SuperPhone X", "electronics", "superphone_x", [
        ("price", 799, "USD", False), ("battery_life", 24, "hours", False),
        ("weight", 187, "grams", False), ("color", "Midnight Black", "", True),
    ]),
    ("MegaTablet Pro", "electronics", "megatab_pro", [
        ("price", 1199, "USD", False), ("screen_size", 12.9, "inches", False),
        ("storage", 256, "GB", False), ("color", "Silver", "", True),
    ]),
    ("UltraLaptop Air", "electronics", "ultralaptop_air", [
        ("price", 1499, "USD", False), ("ram", 16, "GB", False),
        ("battery_life", 18, "hours", False), ("color", "Space Gray", "", True),
    ]),
    ("NoiseGuard Pro", "electronics", "noiseguard_pro", [
        ("price", 349, "USD", False), ("battery_life", 30, "hours", False),
        ("weight", 254, "grams", False), ("color", "Matte Black", "", True),
    ]),
    ("PixelLens Z7", "electronics", "pixellens_z7", [
        ("price", 2499, "USD", False), ("megapixels", 50.3, "MP", False),
        ("weight", 738, "grams", False), ("color", "Graphite", "", True),
    ]),
    ("FitBand Ultra", "electronics", "fitband_ultra", [
        ("price", 249, "USD", False), ("battery_life", 14, "days", False),
        ("weight", 36, "grams", False), ("color", "Crimson Red", "", True),
    ]),
    ("GameStation X1", "electronics", "gamestation_x1", [
        ("price", 499, "USD", False), ("storage", 1, "TB", False),
        ("power_draw", 200, "watts", False), ("color", "White", "", True),
    ]),
    ("StreamCast 4K", "electronics", "streamcast_4k", [
        ("price", 49, "USD", False), ("resolution", 4, "K", False),
        ("weight", 32, "grams", False), ("color", "Black", "", True),
    ]),
    ("SoundHub Max", "electronics", "soundhub_max", [
        ("price", 199, "USD", False), ("power_output", 60, "watts", False),
        ("weight", 1.2, "kg", False), ("color", "Charcoal", "", True),
    ]),
    ("DroneFlyer X5", "electronics", "droneflyer_x5", [
        ("price", 799, "USD", False), ("flight_time", 31, "minutes", False),
        ("range", 10, "km", False), ("color", "White", "", True),
    ]),
    ("PowerBank Mega", "electronics", "powerbank_mega", [
        ("price", 59, "USD", False), ("capacity", 26800, "mAh", False),
        ("weight", 450, "grams", False), ("color", "Blue", "", True),
    ]),
    ("ActionCam Hero8", "electronics", "actioncam_hero8", [
        ("price", 399, "USD", False), ("resolution", 5.3, "K", False),
        ("battery_life", 105, "minutes", False), ("color", "Black", "", True),
    ]),
    ("SmartPen Scribe", "electronics", "smartpen_scribe", [
        ("price", 129, "USD", False), ("pressure_levels", 8192, "levels", False),
        ("battery_life", 10, "hours", False), ("color", "Silver", "", True),
    ]),
    ("EcoSedan S", "automotive", "ecosedan_s", [
        ("price", 35900, "USD", False), ("range", 405, "miles", False),
        ("battery_capacity", 75, "kWh", False), ("color", "Pearl White", "", True),
    ]),
    ("TurboSUV GT", "automotive", "turbosuv_gt", [
        ("price", 62500, "USD", False), ("horsepower", 395, "hp", False),
        ("fuel_economy", 24, "mpg", False), ("color", "Racing Red", "", True),
    ]),
    ("ElectroCycle R1", "automotive", "electrocycle_r1", [
        ("price", 14990, "USD", False), ("range", 150, "miles", False),
        ("weight", 220, "kg", False), ("color", "Neon Green", "", True),
    ]),
    ("AeroRunner 5", "fashion", "aerorunner_5", [
        ("price", 179, "USD", False), ("weight", 235, "grams", False),
        ("drop", 10, "mm", False), ("color", "Cyan", "", True),
    ]),
    ("StormJacket Pro", "fashion", "stormjacket_pro", [
        ("price", 299, "USD", False), ("weight", 450, "grams", False),
        ("waterproof_rating", 20000, "mm", False), ("color", "Navy Blue", "", True),
    ]),
    ("ChronoLux 42", "fashion", "chronolux_42", [
        ("price", 5999, "USD", False), ("water_resistance", 300, "meters", False),
        ("case_diameter", 42, "mm", False), ("color", "Rose Gold", "", True),
    ]),
    ("RoboVac S9", "home", "robovac_s9", [
        ("price", 599, "USD", False), ("suction_power", 5000, "Pa", False),
        ("battery_life", 180, "minutes", False), ("color", "Black", "", True),
    ]),
    ("SmartFridge Plus", "home", "smartfridge_plus", [
        ("price", 2199, "USD", False), ("capacity", 28, "cu ft", False),
        ("energy_usage", 630, "kWh/yr", False), ("color", "Stainless Steel", "", True),
    ]),
    ("AirClean Max", "home", "airclean_max", [
        ("price", 449, "USD", False), ("coverage_area", 1500, "sq ft", False),
        ("noise_level", 24, "dB", False), ("color", "White", "", True),
    ]),
    ("BrewMaster 3000", "home", "brewmaster_3000", [
        ("price", 699, "USD", False), ("pressure", 15, "bars", False),
        ("tank_capacity", 2.5, "liters", False), ("color", "Silver", "", True),
    ]),
    ("DoorView HD", "home", "doorview_hd", [
        ("price", 199, "USD", False), ("resolution", 2, "K", False),
        ("field_of_view", 180, "degrees", False), ("color", "Black", "", True),
    ]),
    ("PulseTracker Pro", "health", "pulsetracker_pro", [
        ("price", 149, "USD", False), ("battery_life", 7, "days", False),
        ("heart_rate_accuracy", 98, "percent", False), ("color", "Black", "", True),
    ]),
    ("BalanceScale X", "health", "balancescale_x", [
        ("price", 79, "USD", False), ("weight_capacity", 180, "kg", False),
        ("accuracy", 50, "grams", False), ("color", "White", "", True),
    ]),
    ("ZenMat Premium", "health", "zenmat_premium", [
        ("price", 89, "USD", False), ("thickness", 6, "mm", False),
        ("weight", 2.5, "kg", False), ("color", "Purple", "", True),
    ]),
    ("CyclePro R3", "fitness", "cyclepro_r3", [
        ("price", 1999, "USD", False), ("resistance_levels", 100, "levels", False),
        ("flywheel_weight", 18, "kg", False), ("color", "Black", "", True),
    ]),
    ("CloudRack X8", "computing", "cloudrack_x8", [
        ("price", 8999, "USD", False), ("ram", 128, "GB", False),
        ("storage", 4, "TB", False), ("color", "Silver", "", True),
    ]),
    ("ViewMax QHD", "computing", "viewmax_qhd", [
        ("price", 699, "USD", False), ("refresh_rate", 165, "Hz", False),
        ("response_time", 1, "ms", False), ("color", "Black", "", True),
    ]),
]

def _build_data():
    result = []
    for prod_idx, (entity, domain, slug, attrs) in enumerate(_PRODUCTS):
        product = {"entity": entity, "domain": domain, "attributes": {}}
        for attr_idx, (attr_name, value, unit, is_visual) in enumerate(attrs):
            has_doc = (attr_idx % 3 != 2)
            tidx = prod_idx * len(attrs) + attr_idx
            product["attributes"][attr_name] = _make_attr(
                entity, attr_name, value, unit, slug, has_doc, tidx, is_visual
            )
        result.append(product)
    return result

data = _build_data()
__all__ = ["data"]
