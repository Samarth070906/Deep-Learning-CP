import requests
import json

base_url = "http://localhost:8001"

print("1. FULL EXPLANATION FOR ROW 3")
res = requests.post(f"{base_url}/verify", json={
    "agent_response": "Color of GameStation X1 is White.",
    "context": {"unit": "", "visually_verifiable": True, "source_reliability": 0.8, "action_risk": 0.5}
})
print(json.dumps(res.json(), indent=2))

print("\n2. ERROR HANDLING PROOF")
res_err = requests.post(f"{base_url}/verify", json={
    "agent_response": "BlahBlahBlahNonsenseClaim123",
    "context": {}
})
print(f"Status Code: {res_err.status_code}")
print(f"Response: {res_err.text}")

print("\n3. HISTORY ENDPOINT PROOF")
res_hist = requests.get(f"{base_url}/history?limit=2")
print(f"Status Code: {res_hist.status_code}")
hist_data = res_hist.json()
print(f"Number of records returned: {len(hist_data)}")
for h in hist_data:
    print(f"ID: {h['id']}, Claim: {h['claim']}")
