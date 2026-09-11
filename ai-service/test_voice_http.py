import io
import sys
import wave
import math
import struct
import requests

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def create_synthetic_wav_bytes(duration_sec: float = 0.5, sample_rate: int = 16000) -> bytes:
    buf = io.BytesIO()
    total_samples = int(sample_rate * duration_sec)
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        frames = [struct.pack('<h', int(8000 * math.sin(2 * math.pi * 440 * (i / sample_rate)))) for i in range(total_samples)]
        w.writeframes(b''.join(frames))
    return buf.getvalue()

def run_voice_http_tests():
    print("=" * 85)
    print("       PRODUCTASSIST AI - VOICE INTERACTION HTTP ENDPOINT TEST SUITE")
    print("=" * 85)

    wav_bytes = create_synthetic_wav_bytes()

    # -------------------------------------------------------------------
    # 1. Test POST /voice/transcribe (Audio Upload -> STT)
    # -------------------------------------------------------------------
    print("\n1. POST /voice/transcribe (Valid Audio Upload -> STT)")
    files = {"file": ("technician_speech.wav", wav_bytes, "audio/wav")}
    resp = requests.post(f"{BASE_URL}/voice/transcribe", files=files)

    print(f"   Status Code        : {resp.status_code}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"

    data = resp.json()
    print(f"   Transcribed Text   : '{data.get('text')}'")
    print(f"   Language           : {data.get('language')}")
    print(f"   Confidence         : {data.get('confidence')}")
    print("   [PASS] /voice/transcribe returned 200 OK with valid STT transcription!")

    # -------------------------------------------------------------------
    # 2. Test POST /voice/synthesize (Text -> Speech Audio Stream)
    # -------------------------------------------------------------------
    print("\n2. POST /voice/synthesize (Text Input -> Audio Speech Stream)")
    synth_payload = {"text": "Please inspect the coolant intake screen inside the reservoir tank."}
    resp_synth = requests.post(f"{BASE_URL}/voice/synthesize", json=synth_payload)

    print(f"   Status Code        : {resp_synth.status_code}")
    assert resp_synth.status_code == 200, f"Expected 200, got {resp_synth.status_code}"

    content_type = resp_synth.headers.get("content-type")
    audio_len = len(resp_synth.content)
    print(f"   Content-Type       : {content_type}")
    print(f"   Audio Output Bytes : {audio_len} bytes")
    assert audio_len > 0, "Expected audio response body bytes"
    print("   [PASS] /voice/synthesize returned 200 OK with audio stream!")

    # -------------------------------------------------------------------
    # 3. Test POST /troubleshoot/start-with-voice (Voice -> Troubleshooting Start)
    # -------------------------------------------------------------------
    print("\n3. POST /troubleshoot/start-with-voice (Voice-Driven Troubleshooting Start)")
    files_ts = {"file": ("problem_speech.wav", wav_bytes, "audio/wav")}
    resp_ts = requests.post(f"{BASE_URL}/troubleshoot/start-with-voice", files=files_ts)

    print(f"   Status Code        : {resp_ts.status_code}")
    assert resp_ts.status_code == 200, f"Expected 200, got {resp_ts.status_code}: {resp_ts.text}"

    data_ts = resp_ts.json()
    stt_info = data_ts.get("transcription", {})
    session_info = data_ts.get("troubleshooting_session", {})
    session_id = session_info.get("session_id")

    print(f"   Transcribed Text   : '{stt_info.get('text')}'")
    print(f"   Session ID         : {session_id}")
    print(f"   Session Status     : {session_info.get('status')}")
    print(f"   Identified Issue   : {session_info.get('identified_issue')}")
    print(f"   Initial Question   : {session_info.get('next_question')}")
    print("   [PASS] /troubleshoot/start-with-voice returned 200 OK!")

    # -------------------------------------------------------------------
    # 4. Test POST /troubleshoot/{session_id}/respond-with-voice (Multi-Turn Voice)
    # -------------------------------------------------------------------
    if session_id:
        print("\n4. POST /troubleshoot/{session_id}/respond-with-voice (Multi-Turn Voice Response)")
        ans_wav = create_synthetic_wav_bytes(duration_sec=0.8)
        files_resp = {"file": ("answer_speech.wav", ans_wav, "audio/wav")}
        resp_voice_resp = requests.post(
            f"{BASE_URL}/troubleshoot/{session_id}/respond-with-voice",
            files=files_resp
        )

        print(f"   Status Code        : {resp_voice_resp.status_code}")
        assert resp_voice_resp.status_code == 200, f"Expected 200, got {resp_voice_resp.status_code}: {resp_voice_resp.text}"

        data_vr = resp_voice_resp.json()
        stt_ans = data_vr.get("transcription", {})
        sess_ans = data_vr.get("troubleshooting_session", {})
        b64_audio = data_vr.get("audio_base64", "")

        print(f"   Spoken Answer STT  : '{stt_ans.get('text')}'")
        print(f"   New Session Status : {sess_ans.get('status')}")
        print(f"   Agent Spoken Message: {sess_ans.get('message')[:100]}...")
        print(f"   TTS Response Audio : {len(b64_audio)} base64 chars ({data_vr.get('audio_mime_type')})")
        print("   [PASS] /troubleshoot/{session_id}/respond-with-voice returned 200 OK!")

    # -------------------------------------------------------------------
    # 5. Test Invalid Audio Upload (Text File Upload -> Expect 400 Bad Request)
    # -------------------------------------------------------------------
    print("\n5. POST /voice/transcribe (Invalid Text File Upload -> Expect 400 Bad Request)")
    invalid_files = {"file": ("notes.txt", b"This is plain text, not audio.", "text/plain")}
    resp_inv = requests.post(f"{BASE_URL}/voice/transcribe", files=invalid_files)

    print(f"   Status Code        : {resp_inv.status_code} (Expected 400)")
    assert resp_inv.status_code == 400, f"Expected 400, got {resp_inv.status_code}"
    print(f"   Error Detail       : {resp_inv.json().get('detail')}")
    print("   [PASS] Clean HTTP 400 Bad Request returned for invalid audio upload!")

    print("\n" + "=" * 85)
    print("All Voice Interaction HTTP Endpoint Checks Completed Successfully!")
    print("=" * 85)

if __name__ == "__main__":
    run_voice_http_tests()
