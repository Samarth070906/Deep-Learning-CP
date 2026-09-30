import hashlib

SOURCE_REL_LOOKUP = {
    "official retailer listing": 0.9,
    "third-party marketplace": 0.6,
    "unverified/user-submitted": 0.3
}

ACTION_RISK_LOOKUP = {
    "display product info": 0.2,
    "recommend to user": 0.5,
    "auto-complete a purchase": 0.9
}

def get_record_metadata(record_id: str):
    h = int(hashlib.md5(record_id.encode()).hexdigest(), 16)
    source_cat = list(SOURCE_REL_LOOKUP.keys())[h % len(SOURCE_REL_LOOKUP)]
    action_cat = list(ACTION_RISK_LOOKUP.keys())[(h // len(SOURCE_REL_LOOKUP)) % len(ACTION_RISK_LOOKUP)]
    return source_cat, action_cat

def get_record_features(record_id: str):
    source_cat, action_cat = get_record_metadata(record_id)
    return SOURCE_REL_LOOKUP[source_cat], ACTION_RISK_LOOKUP[action_cat]
