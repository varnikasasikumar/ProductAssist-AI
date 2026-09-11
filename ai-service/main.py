from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, UploadFile, File, Response
from pydantic import BaseModel, Field

from rag import (
    retrieve_knowledge_chunks,
    generate_grounded_answer,
    LLMKeyMissingError,
    LLMProviderError
)
from troubleshooting import (
    session_store,
    StartTroubleshootingRequest,
    ContinueTroubleshootingRequest,
    TroubleshootingResponse,
    start_troubleshooting,
    continue_troubleshooting
)
from vision import (
    VisionAnalysisResponse,
    VisionTroubleshootResponse,
    validate_image_upload,
    analyze_product_image,
    analyze_and_start_troubleshooting
)
from voice import (
    STTResponse,
    TTSRequest,
    VoiceTroubleshootResponse,
    transcribe_audio_service,
    synthesize_text_service,
    start_troubleshooting_with_voice,
    respond_to_troubleshooting_with_voice
)

app = FastAPI(
    title="ProductAssist AI Service",
    description="Multimodal RAG and Agentic AI Assistance Platform for Product Operation, Troubleshooting, and Maintenance",
    version="1.0.0"
)

# Search API Schemas
class RAGSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query", example="What should I do if the CNC-X100 shows E105?")
    model: Optional[str] = Field(None, description="Optional model identifier for metadata filtering", example="CNC-X100")
    top_k: int = Field(5, ge=1, le=10, description="Number of top chunks to retrieve (1-10)", example=5)

class RAGSearchResultItem(BaseModel):
    content: str
    document_name: str
    document_type: str
    page_number: int
    section: str
    model: str
    product: str
    score: Optional[float] = None
    source_file: str

class RAGSearchResponse(BaseModel):
    query: str
    model: Optional[str] = None
    top_k: int
    total_results: int
    results: List[RAGSearchResultItem]

# Grounded Q&A Schemas
class RAGAskRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User's natural language question", example="What should I do if the CNC-X100 shows E105?")
    model: Optional[str] = Field(None, description="Optional model identifier, e.g., 'CNC-X100'", example="CNC-X100")
    top_k: int = Field(5, ge=1, le=10, description="Number of context chunks to retrieve (1-10)", example=5)

class SourceCitationItem(BaseModel):
    document_name: str
    document_type: str
    page_number: int
    section: str

class RAGAskResponse(BaseModel):
    query: str
    model: Optional[str] = None
    answer: str
    sources: List[SourceCitationItem]
    retrieved_chunks: int

# Health Endpoints
@app.get("/")
def read_root():
    return {
        "message": "ProductAssist AI Service is running",
        "service": "ProductAssist AI Service",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {
        "status": "UP"
    }

# RAG Endpoints
@app.post("/rag/search", response_model=RAGSearchResponse)
def search_rag_knowledge(request: RAGSearchRequest):
    """Perform vector search over product knowledge base."""
    try:
        results = retrieve_knowledge_chunks(
            query=request.query,
            model=request.model,
            top_k=request.top_k
        )
        return RAGSearchResponse(
            query=request.query,
            model=request.model,
            top_k=request.top_k,
            total_results=len(results),
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG search failed: {str(e)}")

@app.post("/rag/ask", response_model=RAGAskResponse)
def ask_rag_grounded_question(request: RAGAskRequest):
    """Generate grounded answer with citations using RAG context."""
    try:
        result = generate_grounded_answer(
            query=request.query,
            model=request.model,
            top_k=request.top_k
        )
        return RAGAskResponse(**result)
    except LLMKeyMissingError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except LLMProviderError as err:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(err)
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during RAG answer generation: {str(err)}"
        )

# Troubleshooting Endpoints
@app.post("/troubleshoot/start", response_model=TroubleshootingResponse)
def start_troubleshooting_session(request: StartTroubleshootingRequest):
    """Start an agentic troubleshooting session."""
    try:
        res = start_troubleshooting(model=request.model, problem=request.problem)
        return TroubleshootingResponse(**res)
    except LLMKeyMissingError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except LLMProviderError as err:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

@app.post("/troubleshoot/{session_id}/respond", response_model=TroubleshootingResponse)
def continue_troubleshooting_session(session_id: str, request: ContinueTroubleshootingRequest):
    """Continue active troubleshooting session with user feedback."""
    try:
        res = continue_troubleshooting(session_id=session_id, user_response=request.response)
        return TroubleshootingResponse(**res)
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except LLMKeyMissingError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except LLMProviderError as err:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

@app.get("/troubleshoot/{session_id}")
def get_troubleshooting_session_state(session_id: str):
    """Retrieve troubleshooting session state."""
    session = session_store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Troubleshooting session '{session_id}' not found.")
    return session.to_dict()

# Vision Endpoints
@app.post("/vision/analyze", response_model=VisionAnalysisResponse)
async def analyze_product_image_endpoint(file: UploadFile = File(...)):
    """Extract product metadata, text, and issues from image."""
    try:
        image_bytes, mime_type = await validate_image_upload(file)
        result = analyze_product_image(image_bytes=image_bytes, mime_type=mime_type)
        return result
    except HTTPException:
        raise
    except LLMKeyMissingError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except LLMProviderError as err:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Vision analysis failed: {str(err)}")

@app.post("/troubleshoot/start-with-image", response_model=VisionTroubleshootResponse)
async def start_troubleshooting_with_image_endpoint(file: UploadFile = File(...)):
    """Start troubleshooting session directly from uploaded image."""
    try:
        image_bytes, mime_type = await validate_image_upload(file)
        result = analyze_and_start_troubleshooting(image_bytes=image_bytes, mime_type=mime_type)
        return VisionTroubleshootResponse(**result)
    except HTTPException:
        raise
    except LLMKeyMissingError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    except LLMProviderError as err:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Vision troubleshooting initiation failed: {str(err)}")

# Voice Endpoints


@app.post("/voice/transcribe", response_model=STTResponse)
async def transcribe_voice_endpoint(file: UploadFile = File(...)):
    """
    Speech-to-Text Endpoint:
    Accepts an uploaded audio file and converts spoken technician audio to text.
    """
    try:
        return await transcribe_audio_service(file=file)
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Speech transcription failed: {str(err)}")

@app.post("/voice/synthesize")
def synthesize_voice_endpoint(request: TTSRequest):
    """
    Text-to-Speech Endpoint:
    Accepts text input and synthesizes speech audio response bytes.
    """
    try:
        audio_bytes, mime_type, provider = synthesize_text_service(text=request.text, voice=request.voice or "alloy")
        return Response(content=audio_bytes, media_type=mime_type)
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Speech synthesis failed: {str(err)}")

@app.post("/troubleshoot/start-with-voice", response_model=VoiceTroubleshootResponse)
async def start_troubleshooting_with_voice_endpoint(file: UploadFile = File(...)):
    """
    Voice-Driven Agentic Troubleshooting Start Endpoint:
    Accepts spoken technician audio, converts to text, and initiates an agentic troubleshooting session.
    """
    try:
        result = await start_troubleshooting_with_voice(file=file)
        return VoiceTroubleshootResponse(**result)
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Voice troubleshooting initiation failed: {str(err)}")

@app.post("/troubleshoot/{session_id}/respond-with-voice")
async def respond_to_troubleshooting_with_voice_endpoint(session_id: str, file: UploadFile = File(...)):
    """
    Multi-Turn Voice Troubleshooting Endpoint:
    Accepts technician audio observation for an active session, continues troubleshooting,
    and returns transcribed text, session state, and synthesized TTS response audio base64 payload.
    """
    try:
        result = await respond_to_troubleshooting_with_voice(session_id=session_id, file=file)
        return result
    except HTTPException:
        raise
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Voice troubleshooting continuation failed: {str(err)}")


