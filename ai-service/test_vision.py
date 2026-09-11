import io
import sys
import os
import json
from PIL import Image
from fastapi import HTTPException

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from rag.llm import LLMClient
from vision import (
    VisionAnalysisResponse,
    validate_image_bytes,
    analyze_product_image,
    analyze_and_start_troubleshooting
)

def create_synthetic_image_bytes(format: str = "JPEG", color: str = "red", size: tuple = (200, 200)) -> bytes:
    """Helper to generate valid in-memory image bytes using PIL."""
    buf = io.BytesIO()
    img = Image.new("RGB", size, color=color)
    img.save(buf, format=format)
    return buf.getvalue()

class MockVisionLLMClient(LLMClient):
    """Mock LLM client returning deterministic vision JSON responses."""
    def __init__(self, mode: str = "valid"):
        self.mode = mode
        self.provider = "mock"
        self.api_key = "mock-key"

    def generate_vision(self, system_prompt: str, user_prompt: str, image_bytes: bytes, mime_type: str = "image/jpeg", temperature: float = 0.1) -> str:
        if self.mode == "valid":
            return json.dumps({
                "detected_product": "CNC Machine",
                "detected_model": "CNC-X100",
                "detected_error_code": "E105",
                "visible_text": ["CNC-X100 CONTROL PANEL", "ALARM E105", "COOLANT FLOW LOW"],
                "observed_issue": "Display screen shows active E105 Cooling System Malfunction alarm.",
                "confidence": 0.95,
                "notes": "Clear view of HMI panel showing error E105."
            })
        elif self.mode == "unknown":
            return json.dumps({
                "detected_product": None,
                "detected_model": None,
                "detected_error_code": None,
                "visible_text": [],
                "observed_issue": None,
                "confidence": 0.20,
                "notes": "Image is blurry and unreadable. Cannot identify product or error code."
            })
        else:
            return "Invalid text response"

def run_vision_unit_tests():
    print("=" * 85)
    print("        PRODUCTASSIST AI - MULTIMODAL VISION UNIT TEST SUITE")
    print("=" * 85)

    # -------------------------------------------------------------------
    # TEST 1: Image Byte Validation (Valid Formats)
    # -------------------------------------------------------------------
    print("\n--- TEST 1: Image Byte Validation (Valid Formats) ---")
    jpeg_bytes = create_synthetic_image_bytes("JPEG")
    png_bytes = create_synthetic_image_bytes("PNG")
    
    mime_jpeg = validate_image_bytes(jpeg_bytes, filename="test.jpg")
    print(f"  [PASS] Valid JPEG bytes validated -> MIME: {mime_jpeg}")
    
    mime_png = validate_image_bytes(png_bytes, filename="test.png")
    print(f"  [PASS] Valid PNG bytes validated -> MIME: {mime_png}")

    # -------------------------------------------------------------------
    # TEST 2: Image Byte Validation Error Handling (Invalid Files)
    # -------------------------------------------------------------------
    print("\n--- TEST 2: Image Byte Validation Error Handling ---")
    
    # 2a. Empty bytes
    try:
        validate_image_bytes(b"")
        print("  [FAIL] Did not raise error for empty bytes")
    except HTTPException as err:
        print(f"  [PASS] Empty Bytes Error Caught (HTTP {err.status_code}): {err.detail}")

    # 2b. Corrupt bytes
    try:
        validate_image_bytes(b"NOT_AN_IMAGE_PAYLOAD_12345")
        print("  [FAIL] Did not raise error for corrupt image bytes")
    except HTTPException as err:
        print(f"  [PASS] Corrupt Image Error Caught (HTTP {err.status_code}): {err.detail}")

    # 2c. Unsupported extension
    try:
        validate_image_bytes(jpeg_bytes, filename="script.exe")
        print("  [FAIL] Did not raise error for unsupported extension")
    except HTTPException as err:
        print(f"  [PASS] Extension Error Caught (HTTP {err.status_code}): {err.detail}")

    # 2d. Oversized file (>10MB)
    try:
        huge_bytes = b"X" * (10 * 1024 * 1024 + 100)
        validate_image_bytes(huge_bytes, filename="huge.jpg")
        print("  [FAIL] Did not raise error for oversized image")
    except HTTPException as err:
        print(f"  [PASS] Size Limit Error Caught (HTTP {err.status_code}): {err.detail}")

    # -------------------------------------------------------------------
    # TEST 3: Structured Vision Analysis (Valid Image Detection)
    # -------------------------------------------------------------------
    print("\n--- TEST 3: Structured Vision Analysis (Valid Image Detection) ---")
    mock_valid_llm = MockVisionLLMClient(mode="valid")
    res_valid = analyze_product_image(jpeg_bytes, mime_type="image/jpeg", llm_client=mock_valid_llm)

    print(f"  Detected Product    : {res_valid.detected_product}")
    print(f"  Detected Model      : {res_valid.detected_model}")
    print(f"  Detected Error Code : {res_valid.detected_error_code}")
    print(f"  Confidence          : {res_valid.confidence}")
    print(f"  Observed Issue      : {res_valid.observed_issue}")
    print(f"  Visible Text Lines  : {len(res_valid.visible_text)}")

    assert res_valid.detected_model == "CNC-X100", "Expected detected_model 'CNC-X100'"
    assert res_valid.detected_error_code == "E105", "Expected detected_error_code 'E105'"
    print("  [PASS] Valid Vision Extraction Verified!")

    # -------------------------------------------------------------------
    # TEST 4: Structured Vision Analysis (Unreadable / Unknown Image)
    # -------------------------------------------------------------------
    print("\n--- TEST 4: Structured Vision Analysis (Unknown / Unreadable Image) ---")
    mock_unk_llm = MockVisionLLMClient(mode="unknown")
    res_unk = analyze_product_image(jpeg_bytes, mime_type="image/jpeg", llm_client=mock_unk_llm)

    print(f"  Detected Product    : {res_unk.detected_product}")
    print(f"  Detected Model      : {res_unk.detected_model}")
    print(f"  Detected Error Code : {res_unk.detected_error_code}")
    print(f"  Confidence          : {res_unk.confidence}")
    print(f"  Notes               : {res_unk.notes}")

    assert res_unk.detected_model is None, "Expected detected_model to be None for unreadable image"
    assert res_unk.detected_error_code is None, "Expected detected_error_code to be None for unreadable image"
    print("  [PASS] Non-hallucination Null Return Verified!")

    # -------------------------------------------------------------------
    # TEST 5: Vision + RAG + Troubleshooting Pipeline Integration
    # -------------------------------------------------------------------
    print("\n--- TEST 5: Integrated Vision -> RAG -> Agentic Troubleshooting Flow ---")
    integrated = analyze_and_start_troubleshooting(jpeg_bytes, mime_type="image/jpeg", llm_client=mock_valid_llm)

    v_part = integrated["vision_analysis"]
    t_part = integrated["troubleshooting_session"]

    print(f"  Vision Model Extracted  : {v_part['detected_model']}")
    print(f"  Vision Error Extracted  : {v_part['detected_error_code']}")
    print(f"  Troubleshooting Session : {t_part['session_id']}")
    print(f"  Troubleshooting Status  : {t_part['status']}")
    print(f"  Identified Issue        : {t_part['identified_issue']}")
    print(f"  Initial Agent Question  : {t_part['next_question']}")
    print(f"  RAG Sources Count       : {len(t_part['sources'])}")

    assert t_part["status"] == "DIAGNOSING", "Expected troubleshooting session status 'DIAGNOSING'"
    assert len(t_part["sources"]) > 0, "Expected RAG context sources attached to session"
    print("  [PASS] Integrated Vision -> RAG -> Troubleshooting Pipeline Verified!")

    print("\n" + "=" * 85)
    print("All Multimodal Vision Unit Tests Completed Successfully!")
    print("=" * 85)

if __name__ == "__main__":
    run_vision_unit_tests()
