import requests

base_url = "http://localhost:8001"

print("\n2. ERROR HANDLING PROOF (Malformed payload)")
# Missing 'context' key entirely, which is required by the Pydantic schema
res_err = requests.post(f"{base_url}/verify", json={
    "agent_response": "Some claim"
})
print(f"Status Code: {res_err.status_code}")
print(f"Response: {res_err.text}")
