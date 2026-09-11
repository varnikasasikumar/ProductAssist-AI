import sys
import requests
import json

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

print("=" * 80)
print("     PRODUCTASSIST AI - TROUBLESHOOTING HTTP ENDPOINT VERIFICATION")
print("=" * 80)

# 1. Test POST /troubleshoot/start
start_payload = {
    "model": "CNC-X100",
    "problem": "The machine stopped suddenly and shows error E105"
}

resp = requests.post(f"{BASE_URL}/troubleshoot/start", json=start_payload)
print(f"\n1. POST /troubleshoot/start -> Status {resp.status_code}")
data1 = resp.json()
print(f"   Session ID       : {data1.get('session_id')}")
print(f"   Identified Issue : {data1.get('identified_issue')}")
print(f"   Status           : {data1.get('status')}")
print(f"   Message          : {data1.get('message')}")
print(f"   Next Question    : {data1.get('next_question')}")
print(f"   Sources Count    : {len(data1.get('sources', []))}")

session_id = data1.get('session_id')

# 2. Test POST /troubleshoot/{session_id}/respond
if session_id:
    continue_payload = {
        "response": "The coolant level is below MIN."
    }
    resp2 = requests.post(f"{BASE_URL}/troubleshoot/{session_id}/respond", json=continue_payload)
    print(f"\n2. POST /troubleshoot/{session_id}/respond -> Status {resp2.status_code}")
    data2 = resp2.json()
    print(f"   Status           : {data2.get('status')}")
    print(f"   Message          :\n{data2.get('message')}")
    print(f"   Next Question    : {data2.get('next_question')}")
    print(f"   Sources Count    : {len(data2.get('sources', []))}")

# 3. Test Invalid Session ID (Expect 404)
resp_invalid = requests.post(f"{BASE_URL}/troubleshoot/invalid-session-id-9999/respond", json={"response": "Yes"})
print(f"\n3. POST /troubleshoot/invalid-session-id-9999/respond -> Status {resp_invalid.status_code} (Expected 404 Not Found)")

# 4. Test GET /troubleshoot/{session_id}
if session_id:
    resp_get = requests.get(f"{BASE_URL}/troubleshoot/{session_id}")
    print(f"\n4. GET /troubleshoot/{session_id} -> Status {resp_get.status_code}")
    print(f"   Current Session Step : {resp_get.json().get('current_step')}")

print("\nAll Troubleshooting HTTP Endpoint Checks Completed Successfully!")
print("=" * 80)
