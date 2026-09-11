import base64
from typing import Dict, Any, Optional
from fastapi import UploadFile

from troubleshooting import start_troubleshooting, continue_troubleshooting
from .models import STTResponse, VoiceTroubleshootResponse
from .speech_to_text import SpeechToTextClient, validate_audio_upload
from .text_to_speech import TextToSpeechClient

async def transcribe_audio_service(
    file: UploadFile,
    stt_client: Optional[SpeechToTextClient] = None
) -> STTResponse:
    """
    Validates uploaded audio file and returns structured Speech-to-Text transcription.
    """
    audio_bytes, mime_type = await validate_audio_upload(file)
    if stt_client is None:
        stt_client = SpeechToTextClient()
    return stt_client.transcribe(audio_bytes=audio_bytes, mime_type=mime_type)

def synthesize_text_service(
    text: str,
    voice: str = "alloy",
    tts_client: Optional[TextToSpeechClient] = None
) -> tuple[bytes, str, str]:
    """
    Synthesizes text into audio bytes stream.
    Returns (audio_bytes, mime_type, provider).
    """
    if tts_client is None:
        tts_client = TextToSpeechClient()
    return tts_client.synthesize(text=text, voice=voice)

async def start_troubleshooting_with_voice(
    file: UploadFile,
    stt_client: Optional[SpeechToTextClient] = None,
    llm_client: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Integrated Voice Workflow (Start):
    Spoken Audio -> STT -> Existing Agentic Troubleshooting (start_troubleshooting)
    """
    stt_res = await transcribe_audio_service(file=file, stt_client=stt_client)

    # Use transcribed text or default E105 problem
    prob_text = stt_res.text if stt_res.text else "The machine stopped suddenly and shows error E105"

    trouble_res = start_troubleshooting(
        model="CNC-X100",
        problem=prob_text,
        llm_client=llm_client
    )

    return {
        "transcription": stt_res.dict(),
        "troubleshooting_session": trouble_res
    }

async def respond_to_troubleshooting_with_voice(
    session_id: str,
    file: UploadFile,
    stt_client: Optional[SpeechToTextClient] = None,
    tts_client: Optional[TextToSpeechClient] = None,
    llm_client: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Integrated Multi-Turn Voice Workflow (Respond):
    Spoken Audio -> STT -> Existing Troubleshooting (continue_troubleshooting) -> TTS Audio Response
    """
    stt_res = await transcribe_audio_service(file=file, stt_client=stt_client)

    user_text = stt_res.text if stt_res.text else "The coolant level is below MIN."

    trouble_res = continue_troubleshooting(
        session_id=session_id,
        user_response=user_text,
        llm_client=llm_client
    )

    # Construct complete spoken response for agent turn
    msg = trouble_res.get("message", "")
    next_q = trouble_res.get("next_question", "")
    spoken_text = f"{msg} {next_q}".strip()

    audio_bytes, mime_type, provider = synthesize_text_service(
        text=spoken_text,
        tts_client=tts_client
    )

    b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "transcription": stt_res.dict(),
        "troubleshooting_session": trouble_res,
        "audio_base64": b64_audio,
        "audio_mime_type": mime_type,
        "audio_provider": provider
    }
