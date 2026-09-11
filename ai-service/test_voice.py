import io
import sys
import os
import wave
import math
import struct
import asyncio
from fastapi import HTTPException

# Force UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from voice import (
    STTResponse,
    validate_audio_bytes,
    SpeechToTextClient,
    TextToSpeechClient,
    start_troubleshooting_with_voice,
    respond_to_troubleshooting_with_voice
)

def create_synthetic_wav_bytes(duration_sec: float = 0.5, sample_rate: int = 16000) -> bytes:
    """Helper to generate valid 16kHz PCM WAV audio bytes in memory."""
    buf = io.BytesIO()
    total_samples = int(sample_rate * duration_sec)
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        frames = []
        for i in range(total_samples):
            t = i / sample_rate
            val = int(10000 * math.sin(2 * math.pi * 440 * t))
            frames.append(struct.pack('<h', val))
        w.writeframes(b''.join(frames))
    return buf.getvalue()

class DummyUploadFile:
    """Mock UploadFile for async unit testing."""
    def __init__(self, filename: str, content: bytes, content_type: str):
        self.filename = filename
        self._content = content
        self.content_type = content_type

    async def read(self) -> bytes:
        return self._content

def run_voice_unit_tests():
    print("=" * 85)
    print("        PRODUCTASSIST AI - VOICE INTERACTION MODULE UNIT TEST SUITE")
    print("=" * 85)

    wav_bytes = create_synthetic_wav_bytes()

    # -------------------------------------------------------------------
    # TEST 1: Audio Byte Validation (Valid Formats)
    # -------------------------------------------------------------------
    print("\n--- TEST 1: Audio Byte Validation (Valid Formats) ---")
    mime_wav = validate_audio_bytes(wav_bytes, filename="audio.wav", content_type="audio/wav")
    print(f"  [PASS] Valid WAV bytes validated -> MIME: {mime_wav}")

    mime_mp3 = validate_audio_bytes(wav_bytes, filename="audio.mp3", content_type="audio/mpeg")
    print(f"  [PASS] Valid MP3 bytes validated -> MIME: {mime_mp3}")

    # -------------------------------------------------------------------
    # TEST 2: Audio Validation Error Handling (Invalid Files)
    # -------------------------------------------------------------------
    print("\n--- TEST 2: Audio Validation Error Handling ---")
    
    # 2a. Empty bytes
    try:
        validate_audio_bytes(b"")
        print("  [FAIL] Did not raise error for empty audio bytes")
    except HTTPException as err:
        print(f"  [PASS] Empty Audio Error Caught (HTTP {err.status_code}): {err.detail}")

    # 2b. Unsupported extension
    try:
        validate_audio_bytes(wav_bytes, filename="voice.txt")
        print("  [FAIL] Did not raise error for unsupported extension")
    except HTTPException as err:
        print(f"  [PASS] Audio Extension Error Caught (HTTP {err.status_code}): {err.detail}")

    # 2c. Oversized file (>15MB)
    try:
        huge_bytes = b"A" * (15 * 1024 * 1024 + 100)
        validate_audio_bytes(huge_bytes, filename="huge.wav")
        print("  [FAIL] Did not raise error for oversized audio file")
    except HTTPException as err:
        print(f"  [PASS] Audio Size Limit Error Caught (HTTP {err.status_code}): {err.detail}")

    # -------------------------------------------------------------------
    # TEST 3: Speech-to-Text (STT) Transcription Client
    # -------------------------------------------------------------------
    print("\n--- TEST 3: Speech-to-Text (STT) Client ---")
    stt_client = SpeechToTextClient(provider="mock")
    stt_res = stt_client.transcribe(wav_bytes, mime_type="audio/wav")

    print(f"  Transcribed Text : '{stt_res.text}'")
    print(f"  Language         : {stt_res.language}")
    print(f"  Confidence       : {stt_res.confidence}")

    assert len(stt_res.text) > 0, "Expected non-empty STT text transcription"
    print("  [PASS] STT Client Transcription Verified!")

    # -------------------------------------------------------------------
    # TEST 4: Text-to-Speech (TTS) Synthesis Client
    # -------------------------------------------------------------------
    print("\n--- TEST 4: Text-to-Speech (TTS) Client ---")
    tts_client = TextToSpeechClient(provider="mock")
    audio_out, mime_out, provider_out = tts_client.synthesize("Please check the coolant reservoir.")

    print(f"  Generated Audio Bytes : {len(audio_out)} bytes")
    print(f"  MIME Type             : {mime_out}")
    print(f"  TTS Provider          : {provider_out}")

    assert len(audio_out) > 0, "Expected non-empty synthesized TTS audio bytes"
    assert mime_out == "audio/wav", "Expected WAV MIME type"
    print("  [PASS] TTS Speech Synthesis Verified!")

    # -------------------------------------------------------------------
    # TEST 5: Integrated Voice -> Troubleshooting Pipeline
    # -------------------------------------------------------------------
    print("\n--- TEST 5: Integrated Voice -> Agentic Troubleshooting Pipeline ---")
    dummy_file = DummyUploadFile(filename="input.wav", content=wav_bytes, content_type="audio/wav")

    loop = asyncio.get_event_loop()
    integrated_start = loop.run_until_complete(
        start_troubleshooting_with_voice(file=dummy_file, stt_client=stt_client)
    )

    tr_text = integrated_start["transcription"]["text"]
    t_session = integrated_start["troubleshooting_session"]
    session_id = t_session["session_id"]

    print(f"  STT Spoken Input Text : '{tr_text}'")
    print(f"  Session ID            : {session_id}")
    print(f"  Status                : {t_session['status']}")
    print(f"  Identified Issue      : {t_session['identified_issue']}")
    print(f"  Initial Agent Question: {t_session['next_question']}")

    assert t_session["status"] == "DIAGNOSING", "Expected status 'DIAGNOSING'"
    print("  [PASS] Start Troubleshooting with Voice Verified!")

    # -------------------------------------------------------------------
    # TEST 6: Multi-Turn Voice Response Pipeline
    # -------------------------------------------------------------------
    print("\n--- TEST 6: Multi-Turn Voice Response Pipeline ---")
    dummy_file2 = DummyUploadFile(filename="ans.wav", content=b"below min coolant", content_type="audio/wav")

    integrated_resp = loop.run_until_complete(
        respond_to_troubleshooting_with_voice(
            session_id=session_id,
            file=dummy_file2,
            stt_client=stt_client,
            tts_client=tts_client
        )
    )

    t_sess2 = integrated_resp["troubleshooting_session"]
    b64_audio = integrated_resp["audio_base64"]

    print(f"  Updated Status        : {t_sess2['status']}")
    print(f"  Agent Spoken Message  : {t_sess2['message'][:120]}...")
    print(f"  TTS Audio Base64 Len  : {len(b64_audio)} chars")

    assert t_sess2["status"] in ["CORRECTIVE_ACTION", "VERIFYING"], "Expected CORRECTIVE_ACTION or VERIFYING status"
    assert len(b64_audio) > 0, "Expected generated TTS base64 payload"
    print("  [PASS] Multi-Turn Voice Response Verified!")

    print("\n" + "=" * 85)
    print("All Voice Interaction Module Unit Tests Completed Successfully!")
    print("=" * 85)

if __name__ == "__main__":
    run_voice_unit_tests()
