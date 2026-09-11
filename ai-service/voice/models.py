from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from troubleshooting.models import TroubleshootingResponse

class STTResponse(BaseModel):
    text: str = Field(..., description="Transcribed spoken text from audio input", example="The machine stopped suddenly and shows error E105")
    language: str = Field("en", description="Detected language code (e.g. 'en')", example="en")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Speech recognition confidence score (0.0 to 1.0)", example=0.96)

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text string to synthesize into speech audio", example="Please check the coolant reservoir sight glass.")
    voice: Optional[str] = Field("alloy", description="Optional voice designation (e.g. 'alloy', 'echo', 'fable')", example="alloy")
    format: Optional[str] = Field("wav", description="Requested audio format ('wav' or 'mp3')", example="wav")

class TTSResponseMetadata(BaseModel):
    mime_type: str = Field(..., example="audio/wav")
    provider: str = Field(..., example="openai")
    text_length: int = Field(..., example=45)

class VoiceTroubleshootResponse(BaseModel):
    transcription: STTResponse
    troubleshooting_session: TroubleshootingResponse
