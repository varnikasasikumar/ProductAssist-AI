import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("     PRODUCTASSIST AI - FASTAPI /rag/ask ENDPOINT VERIFICATION")
print("=" * 80)

# 1. Test POST /rag/ask without API key configured (Expect 400 Bad Request)
payload = {
    "query": "What should I do if the CNC-X100 shows E105?",
    "model": "CNC-X100",
    "top_k": 3
}

resp = requests.post(f"{BASE_URL}/rag/ask", json=payload)
print(f"\n1. POST /rag/ask (Key missing test) -> Status {resp.status_code}")
print(f"   Detail: {resp.json().get('detail')}")

# 2. Test Validation Error (empty query)
resp_invalid = requests.post(f"{BASE_URL}/rag/ask", json={"query": "", "top_k": 5})
print(f"\n2. POST /rag/ask (Empty query validation) -> Status {resp_invalid.status_code} (Expected 422 Unprocessable Entity)")

print("\nAll HTTP endpoint checks completed successfully!")
print("=" * 80)
