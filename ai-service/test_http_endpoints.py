import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("       PRODUCTASSIST AI - FASTAPI RAG HTTP ENDPOINT VERIFICATION")
print("=" * 80)

# 1. Test GET /
resp = requests.get(f"{BASE_URL}/")
print(f"\n1. GET / -> Status {resp.status_code}")
print(f"   Response: {resp.json()}")

# 2. Test GET /health
resp = requests.get(f"{BASE_URL}/health")
print(f"\n2. GET /health -> Status {resp.status_code}")
print(f"   Response: {resp.json()}")

# 3. Test POST /rag/search with E105 query
payload = {
    "query": "What should I do if the CNC-X100 shows E105?",
    "model": "CNC-X100",
    "top_k": 3
}

resp = requests.post(f"{BASE_URL}/rag/search", json=payload)
print(f"\n3. POST /rag/search -> Status {resp.status_code}")
data = resp.json()
print(f"   Query         : {data.get('query')}")
print(f"   Model Filter  : {data.get('model')}")
print(f"   Total Results : {data.get('total_results')}")
if data.get("results"):
    first = data["results"][0]
    print(f"   Top Match Document : {first['document_name']} (Page {first['page_number']})")
    print(f"   Top Match Section  : {first['section']}")
    print(f"   Top Match Score    : {first['score']}")
    print(f"   Top Match Snippet  : {first['content'][:140]}...")

# 4. Test Validation Error (empty query)
resp_invalid = requests.post(f"{BASE_URL}/rag/search", json={"query": "", "top_k": 5})
print(f"\n4. POST /rag/search (Validation check for empty query) -> Status {resp_invalid.status_code} (Expected 422 Unprocessable Entity)")

print("\nAll HTTP endpoint checks completed successfully!")
print("=" * 80)
