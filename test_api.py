import requests
import time
import json

base_url = "http://localhost:8001"

scenarios = [
    {
        "name": "1. Exact Match (Single Modality SUPPORT)",
        "agent_response": "Price of GameStation X1 is 499 USD.",
        "context": {"unit": "USD", "visually_verifiable": False, "source_reliability": 0.9, "action_risk": 0.2}
    },
    {
        "name": "2. Minor Numeric Deviation (~8% - CONTRADICT)",
        "agent_response": "Price of GameStation X1 is 459 USD.",
        "context": {"unit": "USD", "visually_verifiable": False, "source_reliability": 0.5, "action_risk": 0.8}
    },
    {
        "name": "4. Categorical Contradiction (Cross-Modal Conflict)",
        "agent_response": "Color of GameStation X1 is White.",
        "context": {"unit": "", "visually_verifiable": True, "source_reliability": 0.8, "action_risk": 0.5}
    }
]

print("Testing via API...\n")

for s in scenarios:
    print(f"=== {s['name']} ===")
    res = requests.post(f"{base_url}/verify", json={
        "agent_response": s["agent_response"],
        "context": s["context"]
    })
    
    if res.status_code == 200:
        data = res.json()
        print(f"Decision: {data['decision']} (Trust Score: {data['trust_score']})")
        print(f"Explanation:\n{data['explanation']}")
    else:
        print(f"Error {res.status_code}: {res.text}")
    print("-" * 50)
    
print("\n=== Checking History endpoint ===")
res = requests.get(f"{base_url}/history")
if res.status_code == 200:
    history = res.json()
    print(f"Found {len(history)} records in history.")
    for h in history:
        print(f"ID: {h['id']}, Claim: {h['claim']}, Decision: {h['decision']}")
else:
    print("Error fetching history.")
