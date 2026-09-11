# ProductAssist AI - Python AI Service

This service provides the AI backend capabilities for ProductAssist AI, including RAG (Retrieval-Augmented Generation), grounded LLM answer generation, agentic multi-turn troubleshooting workflows, vector search, vision, speech processing, and maintenance intelligence.

---

## Getting Started

### 1. Create a Virtual Environment

Open PowerShell or Command Prompt in the `ai-service` directory and run:

```bash
python -m venv venv
```

### 2. Activate the Virtual Environment (Windows)

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

### 3. Environment Variable & LLM Configuration

Copy `.env.example` to `.env` and set your preferred LLM provider and API key:

```bash
cp .env.example .env
```

**Environment Variables**:
* `LLM_PROVIDER`: Provider name (`gemini` [default], `google`, `openai`, `local`)
* `LLM_MODEL`: Model name (default: `gemini-2.5-flash` or `gpt-4o-mini`)
* `GEMINI_API_KEY` / `LLM_API_KEY`: API Key for Google Gemini or OpenAI

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the FastAPI Server

Start the application with Uvicorn:

```bash
uvicorn main:app --reload
```

The service will be accessible at:
- **Root endpoint**: `http://127.0.0.1:8000/`
- **Health check**: `http://127.0.0.1:8000/health`
- **RAG Search endpoint**: `POST http://127.0.0.1:8000/rag/search`
- **Grounded Ask endpoint**: `POST http://127.0.0.1:8000/rag/ask`
- **Start Troubleshooting**: `POST http://127.0.0.1:8000/troubleshoot/start`
- **Continue Troubleshooting**: `POST http://127.0.0.1:8000/troubleshoot/{session_id}/respond`
- **Get Session State**: `GET http://127.0.0.1:8000/troubleshoot/{session_id}`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`

---

## Agentic Troubleshooting Architecture

```
User Problem Input
       │
       ▼
[POST /troubleshoot/start]
       │
       ▼
In-Memory Session Manager (session_store.py)
       │
       ▼
RAG Vector Retrieval (retrieve_knowledge_chunks + filter_and_rank_chunks)
       │
       ▼
Orchestrator Decision Agent (LLM + Structured Output)
 ├── ASK_QUESTION (Next diagnostic check -> DIAGNOSING)
 ├── PROVIDE_CORRECTIVE_ACTION (Root cause found -> CORRECTIVE_ACTION / VERIFYING)
 ├── RESOLVE (User confirmed resolution -> RESOLVED)
 └── ESCALATE (Technician escalation -> ESCALATED)
       │
       ▼
Safety Guardrail Layer (safety_layer.py - Enforces Power OFF & PPE warnings)
       │
       ▼
User Observation Response -> [POST /troubleshoot/{session_id}/respond] -> Verify -> Resolve
```

### What Agentic Troubleshooting Means

Rather than following a rigid hard-coded decision tree, the **Troubleshooting Orchestrator** uses LLM reasoning and ChromaDB RAG context to dynamically evaluate the current diagnostic session state, user observations, and authorized documentation. It determines the most effective next diagnostic question or corrective action while enforcing mandatory industrial safety precautions.

### State Transition Lifecycle

$$\text{DIAGNOSING} \longrightarrow \text{CORRECTIVE\_ACTION} \longrightarrow \text{VERIFYING} \longrightarrow \text{RESOLVED} \quad (\text{or } \text{ESCALATED})$$

* **DIAGNOSING**: Initial problem input or isolating root cause step-by-step.
* **CORRECTIVE_ACTION**: Root cause identified; grounded corrective instructions & safety warnings provided.
* **VERIFYING**: User requested to perform procedure and verify system operation/flow.
* **RESOLVED**: User confirmed corrective action completed and system restored to normal.
* **ESCALATED**: Problem not covered in authorized documentation or service technician required.

### In-Memory Session State

* **Model**: `TroubleshootingSession`
* **Attributes**: `session_id`, `product`, `model`, `problem`, `identified_issue`, `diagnostic_answers`, `current_step`, `status` (`DIAGNOSING`, `CORRECTIVE_ACTION`, `VERIFYING`, `RESOLVED`, `ESCALATED`), `resolution`, `sources`.
* **Storage**: In-memory `SessionStore` (thread-safe, designed for seamless replacement with Redis/PostgreSQL).

---

## Agentic Troubleshooting Endpoints

### 1. Start Session (`POST /troubleshoot/start`)

Initiates a multi-turn diagnostic workflow.

**Request**:
```json
{
  "model": "CNC-X100",
  "problem": "The machine stopped suddenly and shows error E105"
}
```

**Response**:
```json
{
  "session_id": "25f404c6-5098-47f5-ab6b-2c87e11872ec",
  "model": "CNC-X100",
  "identified_issue": "Error Code E105 - Cooling System Malfunction",
  "message": "The system has triggered Error Code E105, which indicates a cooling system malfunction caused by coolant flow dropping below 8.0 L/min or a tripped thermal overload relay Q4.\n\n⚠️ SAFETY PRECAUTION: Always turn OFF main electrical disconnect switch before opening electrical cabinet or servicing internal components.",
  "next_question": "Could you check the coolant reservoir and confirm if the coolant level is adequate or if it is below the minimum required level?",
  "status": "DIAGNOSING",
  "sources": [
    {
      "document_name": "troubleshooting-guide.pdf",
      "document_type": "TROUBLESHOOTING",
      "page_number": 1,
      "section": "Error Code E105 - Cooling System Malfunction"
    }
  ]
}
```

---

### 2. Continue Session (`POST /troubleshoot/{session_id}/respond`)

Submits user diagnostic observations and advances the workflow.

**Turn 2 Request (Root Cause Identified)**:
```json
{
  "response": "The coolant level is below MIN."
}
```

**Turn 2 Response (`CORRECTIVE_ACTION`)**:
```json
{
  "session_id": "25f404c6-5098-47f5-ab6b-2c87e11872ec",
  "model": "CNC-X100",
  "identified_issue": "Error Code E105 - Cooling System Malfunction",
  "message": "Root cause identified: Low coolant level.\n\nRECOMMENDED CORRECTIVE ACTIONS:\n1. Turn OFF main electrical power disconnect switch on rear cabinet.\n2. Top up coolant tank with 6% water-soluble synthetic coolant emulsion to 80% capacity.\n3. Inspect intake screen for sludge/chips and flush if needed.\n\n⚠️ SAFETY PRECAUTION: Always turn OFF main electrical disconnect switch before opening electrical cabinet or servicing internal components.",
  "next_question": "Please perform these corrective steps and restart the pump. Is the coolant flow restored and E105 cleared?",
  "status": "CORRECTIVE_ACTION",
  "sources": [
    {
      "document_name": "troubleshooting-guide.pdf",
      "document_type": "TROUBLESHOOTING",
      "page_number": 1,
      "section": "Error Code E105 - Cooling System Malfunction"
    }
  ]
}
```

**Turn 3 Request (Verification Confirmation)**:
```json
{
  "response": "I refilled the coolant and restarted the pump. Coolant flow is restored and E105 is cleared."
}
```

**Turn 3 Response (`RESOLVED`)**:
```json
{
  "session_id": "25f404c6-5098-47f5-ab6b-2c87e11872ec",
  "model": "CNC-X100",
  "identified_issue": "Error Code E105 - Cooling System Malfunction",
  "message": "Troubleshooting completed successfully. The cooling system is now operating normally and Error Code E105 is resolved.",
  "next_question": "",
  "status": "RESOLVED",
  "sources": [...]
}
```

---

### 3. Inspect Session State (`GET /troubleshoot/{session_id}`)

Returns complete in-memory session object for state inspection and audit.

---

## Multimodal Vision Issue Identification

```
Uploaded Control Panel / Product Image
                 │
                 ▼
     [POST /vision/analyze]
                 │
                 ▼
 Image Format & Byte Stream Validation (vision/vision_analyzer.py)
                 │
                 ▼
 Vision-Capable LLM API (Google Gemini / OpenAI Vision / Fallback)
                 │
                 ▼
 Structured Extraction (detected_product, detected_model, detected_error_code, visible_text)
                 │
                 ▼
  [POST /troubleshoot/start-with-image] -> Existing RAG Retrieval & Agentic Orchestrator
```

### Vision Module Architecture

Located under `ai-service/vision/`:
* **`vision_analyzer.py`**: Validates image upload formats (`JPEG`, `PNG`, `WEBP`), enforces file size limits (10 MB), calls multimodal LLM vision API, and extracts structured visual findings.
* **`models.py`**: Defines Pydantic response models (`VisionAnalysisResponse`, `VisionTroubleshootResponse`).
* **Non-Hallucination Guardrails**: Model is strictly instructed to return `null` for unreadable or non-visible parameters. Never invents error codes or internal component failures.

---

## Multimodal Vision Endpoints

### 1. Analyze Product Image (`POST /vision/analyze`)

Accepts multipart form-data image upload and returns structured visual analysis.

**Request**:
* Header: `Content-Type: multipart/form-data`
* Body: `file` (Image file: `.jpg`, `.jpeg`, `.png`, `.webp`)

**Response**:
```json
{
  "detected_product": "CNC Machine",
  "detected_model": "CNC-X100",
  "detected_error_code": "E105",
  "visible_text": [
    "CNC-X100 CONTROL PANEL",
    "ALARM E105 COOLING SYSTEM MALFUNCTION",
    "COOLANT FLOW: 4.2 L/MIN"
  ],
  "observed_issue": "Display screen shows active E105 Cooling System Malfunction alarm.",
  "confidence": 0.95,
  "notes": "Clear view of HMI panel showing error E105."
}
```

---

### 2. Integrated Vision Troubleshooting (`POST /troubleshoot/start-with-image`)

Accepts an uploaded image, extracts model and error code, and seamlessly initiates a multi-turn agentic troubleshooting session linked to ChromaDB RAG documentation.

**Request**:
* Header: `Content-Type: multipart/form-data`
* Body: `file` (Image file: `.jpg`, `.jpeg`, `.png`, `.webp`)

**Response**:
```json
{
  "vision_analysis": {
    "detected_product": "CNC Machine",
    "detected_model": "CNC-X100",
    "detected_error_code": "E105",
    "visible_text": ["CNC-X100 CONTROL PANEL", "ALARM E105"],
    "observed_issue": "HMI touchscreen displays error code E105",
    "confidence": 0.95,
    "notes": "Extracted visible HMI text and error code E105."
  },
  "troubleshooting_session": {
    "session_id": "c9f09e9f-6187-493f-b886-f16e670485fb",
    "model": "CNC-X100",
    "identified_issue": "Error Code E105 - Cooling System Malfunction",
    "message": "Error Code E105 indicates a Cooling System Malfunction...",
    "next_question": "Before continuing, please check the coolant reservoir sight glass. Is the coolant level below the MIN marking?",
    "status": "DIAGNOSING",
    "sources": [
      {
        "document_name": "troubleshooting-guide.pdf",
        "document_type": "TROUBLESHOOTING",
        "page_number": 1,
        "section": "Error Code E105 - Cooling System Malfunction"
      }
    ]
  }
}
```

---

## Voice Interaction Module

```
Technician Spoken Audio
          │
          ▼
   [POST /voice/transcribe]
          │
          ▼
Speech-to-Text Engine (voice/speech_to_text.py)
          │
          ▼
Transcribed Text -> Existing RAG & Agentic Troubleshooting Pipeline
          │
          ▼
  Agent Response Message & Diagnostic Question
          │
          ▼
Text-to-Speech Engine (voice/text_to_speech.py)
          │
          ▼
   [POST /voice/synthesize] -> Audio Response Stream (audio/wav or audio/mpeg)
```

### Voice Module Architecture

Located under `ai-service/voice/`:
* **`speech_to_text.py`**: Audio byte stream validation (`.wav`, `.mp3`, `.m4a`, `.ogg`, `.flac`, `.webm`), 15 MB file size limit, and provider-agnostic STT (`STT_PROVIDER=gemini|openai`).
* **`text_to_speech.py`**: Provider-agnostic TTS (`TTS_PROVIDER=openai|google`) with fallback binary PCM WAV audio synthesis.
* **`voice_service.py`**: Orchestrates voice transcription, synthesis, and multi-turn voice troubleshooting (`start_troubleshooting_with_voice` & `respond_to_troubleshooting_with_voice`).
* **`models.py`**: Defines Pydantic schemas (`STTResponse`, `TTSRequest`, `VoiceTroubleshootResponse`).
* **Safety Isolation**: Voice module strictly handles Audio $\leftrightarrow$ Text translation. All safety guardrail checks (`safety_layer.py`) and RAG retrieval remain enforced by the core troubleshooting orchestrator.

### Voice Environment Configuration

Configure `ai-service/.env` with your preferred voice provider settings:

```env
# Speech-to-Text (STT) Settings
STT_PROVIDER=gemini
STT_MODEL=gemini-1.5-flash
STT_API_KEY=your_stt_api_key_here

# Text-to-Speech (TTS) Settings
TTS_PROVIDER=openai
TTS_MODEL=tts-1
TTS_API_KEY=your_tts_api_key_here
```

---

## Voice Interaction Endpoints

### 1. Transcribe Audio (`POST /voice/transcribe`)

Converts uploaded technician audio into text.

**Request**:
* Header: `Content-Type: multipart/form-data`
* Body: `file` (Audio file: `.wav`, `.mp3`, `.m4a`, `.ogg`, `.flac`, `.webm`)

**Response**:
```json
{
  "text": "The machine stopped suddenly and shows error E105",
  "language": "en",
  "confidence": 0.95
}
```

---

### 2. Synthesize Speech Audio (`POST /voice/synthesize`)

Synthesizes text input into spoken audio stream.

**Request**:
```json
{
  "text": "Please check the coolant reservoir sight glass. Is the coolant level below the MIN marking?",
  "voice": "alloy",
  "format": "wav"
}
```

**Response**:
* Content-Type: `audio/wav` or `audio/mpeg`
* Body: Audio binary stream

---

### 3. Voice Troubleshooting Start (`POST /troubleshoot/start-with-voice`)

Initiates an agentic troubleshooting session from spoken technician audio.

**Request**:
* Header: `Content-Type: multipart/form-data`
* Body: `file` (Audio file)

**Response**:
```json
{
  "transcription": {
    "text": "The machine stopped suddenly and shows error E105",
    "language": "en",
    "confidence": 0.95
  },
  "troubleshooting_session": {
    "session_id": "4594710e-086c-49f8-aaec-bdc09d9efa99",
    "model": "CNC-X100",
    "identified_issue": "Error Code E105 - Cooling System Malfunction",
    "message": "Error Code E105 indicates a Cooling System Malfunction...",
    "next_question": "Before continuing, please check the coolant reservoir sight glass. Is the coolant level below the MIN marking?",
    "status": "DIAGNOSING",
    "sources": [...]
  }
}
```

---

### 4. Multi-Turn Voice Troubleshooting Respond (`POST /troubleshoot/{session_id}/respond-with-voice`)

Accepts spoken technician diagnostic observation, advances troubleshooting state, and returns transcribed text, session state, and synthesized TTS audio base64 payload.

**Request**:
* Header: `Content-Type: multipart/form-data`
* Body: `file` (Audio file: e.g. technician saying "The coolant level is below MIN.")

**Response**:
```json
{
  "transcription": {
    "text": "The coolant level is below MIN.",
    "language": "en",
    "confidence": 0.95
  },
  "troubleshooting_session": {
    "session_id": "4594710e-086c-49f8-aaec-bdc09d9efa99",
    "model": "CNC-X100",
    "identified_issue": "Error Code E105 - Cooling System Malfunction",
    "message": "Root cause identified: Low coolant level...",
    "next_question": "Please perform these corrective steps and restart the pump. Is the coolant flow restored and E105 cleared?",
    "status": "CORRECTIVE_ACTION",
    "sources": [...]
  },
  "audio_base64": "UklGRiQAAABXQVZFZm10...",
  "audio_mime_type": "audio/wav",
  "audio_provider": "fallback_pcm_synthesizer"
}
```

