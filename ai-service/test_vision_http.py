import io
import sys
import requests
from PIL import Image

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def create_synthetic_jpeg_bytes() -> bytes:
    buf = io.BytesIO()
    img = Image.new("RGB", (200, 200), color="blue")
    img.save(buf, format="JPEG")
    return buf.getvalue()

def run_vision_http_tests():
    print("=" * 85)
    print("      PRODUCTASSIST AI - MULTIMODAL VISION HTTP ENDPOINT TEST SUITE")
    print("=" * 85)

    jpeg_bytes = create_synthetic_jpeg_bytes()

    # -------------------------------------------------------------------
    # 1. Test POST /vision/analyze (Valid Multipart Image Upload)
    # -------------------------------------------------------------------
    print("\n1. POST /vision/analyze (Valid Image Upload)")
    files = {"file": ("control_panel.jpg", jpeg_bytes, "image/jpeg")}
    resp = requests.post(f"{BASE_URL}/vision/analyze", files=files)
    
    print(f"   Status Code        : {resp.status_code}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    
    data = resp.json()
    print(f"   Detected Product   : {data.get('detected_product')}")
    print(f"   Detected Model     : {data.get('detected_model')}")
    print(f"   Detected Error     : {data.get('detected_error_code')}")
    print(f"   Confidence         : {data.get('confidence')}")
    print(f"   Observed Issue     : {data.get('observed_issue')}")
    print("   [PASS] /vision/analyze returned 200 OK with valid Vision response!")

    # -------------------------------------------------------------------
    # 2. Test POST /troubleshoot/start-with-image (Vision -> Troubleshooting)
    # -------------------------------------------------------------------
    print("\n2. POST /troubleshoot/start-with-image (Integrated Vision + Agentic Troubleshooting)")
    files_ts = {"file": ("hmi_display.jpg", jpeg_bytes, "image/jpeg")}
    resp_ts = requests.post(f"{BASE_URL}/troubleshoot/start-with-image", files=files_ts)
    
    print(f"   Status Code        : {resp_ts.status_code}")
    assert resp_ts.status_code == 200, f"Expected 200, got {resp_ts.status_code}: {resp_ts.text}"
    
    data_ts = resp_ts.json()
    v_info = data_ts.get("vision_analysis", {})
    t_info = data_ts.get("troubleshooting_session", {})
    
    print(f"   Vision Extracted   : Model '{v_info.get('detected_model')}' | Error '{v_info.get('detected_error_code')}'")
    print(f"   Troubleshooting ID : {t_info.get('session_id')}")
    print(f"   Session Status     : {t_info.get('status')}")
    print(f"   Identified Issue   : {t_info.get('identified_issue')}")
    print(f"   Initial Question   : {t_info.get('next_question')}")
    print(f"   Sources Count      : {len(t_info.get('sources', []))}")
    print("   [PASS] /troubleshoot/start-with-image returned 200 OK with integrated workflow!")

    # -------------------------------------------------------------------
    # 3. Test Invalid Image Upload (Unsupported Extension / Text File)
    # -------------------------------------------------------------------
    print("\n3. POST /vision/analyze (Invalid Text File Upload -> Expect 400 Bad Request)")
    invalid_files = {"file": ("script.txt", b"This is plain text, not an image.", "text/plain")}
    resp_inv = requests.post(f"{BASE_URL}/vision/analyze", files=invalid_files)
    
    print(f"   Status Code        : {resp_inv.status_code} (Expected 400)")
    assert resp_inv.status_code == 400, f"Expected 400, got {resp_inv.status_code}"
    print(f"   Error Detail       : {resp_inv.json().get('detail')}")
    print("   [PASS] Clean HTTP 400 Bad Request error returned for invalid upload!")

    print("\n" + "=" * 85)
    print("All Vision HTTP Endpoint Tests Completed Successfully!")
    print("=" * 85)

if __name__ == "__main__":
    run_vision_http_tests()
