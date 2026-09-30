import requests
import json

base_url = "http://localhost:8001"

print("\n2. ERROR HANDLING PROOF")
res_err = requests.post(f"{base_url}/verify", json={
    "agent_response": "",
    "context": {}
})
print(f"Status Code: {res_err.status_code}")
print(f"Response: {res_err.text}")

