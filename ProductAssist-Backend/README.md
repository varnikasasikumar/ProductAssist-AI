# ProductAssist-Backend

Spring Boot REST API Backend for ProductAssist AI — an enterprise RAG and Agentic AI-based multimodal assistance platform for product operation, troubleshooting, maintenance, and technical support.

## Overview

The `ProductAssist-Backend` service acts as the core application backend, managing core domain data and proxying/orchestrating AI workflows by communicating directly with the Python FastAPI `ai-service`.

## Architecture & Integration

### Application-Facing Multimodal Assistant Flow
```
React (future)
   │
   ▼
[ AssistantController ] (/api/assistant/*)
   │
   ▼
[ AssistantService ]
   │
   ▼
[ AiServiceClient ] (RestTemplate)
   │
   ▼ (HTTP / REST)
[ Python AI Service ] (Port 8000)
   │
   ├── Vision (Multimodal Image Analysis)
   ├── RAG (ChromaDB Vector Retrieval)
   ├── Gemini (Grounded LLM Reasoning)
   └── Agentic Troubleshooting State Machine
```

```
[ Frontend / Client ]
         │
         ▼
[ Spring Boot Backend (Port 8080) ]
  ├── Assistant Application API (/api/assistant/*)
  │     ├── /api/assistant/ask
  │     ├── /api/assistant/troubleshoot/*
  │     ├── /api/assistant/vision/analyze
  │     └── /api/assistant/troubleshoot/start-with-image
  ├── Verification AI Endpoints (/api/ai/*)
  ├── Domain Controllers & Persistence
  └── AiServiceClient (RestTemplate)
         │
         ▼ (HTTP / REST)
[ Python AI Service (Port 8000) ]
  ├── ChromaDB Knowledge Base
  ├── Grounded Gemini RAG (/rag/*)
  ├── Agentic Troubleshooting (/troubleshoot/*)
  ├── Multimodal Vision Analyzer (/vision/*)
  └── Voice Interaction (STT / TTS) (/voice/*)
```

### Vision + RAG + Troubleshooting Synergy
* **Vision Analysis**: Inspects uploaded technician images (control panel display, HMI touchscreens, error labels, physical equipment) to extract visible product names, model numbers, error codes, and visual anomalies.
* **RAG Knowledge Base**: Uses detected visual findings (e.g. error code `E105`) to retrieve technical documentation, safety procedures, and diagnostic steps from ChromaDB.
* **Agentic Troubleshooting**: Seamlessly initializes an interactive diagnostic state machine (`DIAGNOSING` -> `CORRECTIVE_ACTION` -> `VERIFYING` -> `RESOLVED` / `ESCALATED`) pre-populated with visual analysis findings.

---

## Configuration

Set configuration properties in `src/main/resources/application.properties`:

```properties
# Python AI Service Integration Settings
ai.service.base-url=http://127.0.0.1:8000
ai.service.connect-timeout=5000
ai.service.read-timeout=30000
```

---

## Application API Endpoints (`/api/assistant`)

### 1. Grounded Q&A (`POST /api/assistant/ask`)
* **Request**:
  ```json
  {
    "query": "What should I do if the CNC-X100 shows E105?",
    "model": "CNC-X100",
    "top_k": 5
  }
  ```
* **Response**:
  ```json
  {
    "query": "What should I do if the CNC-X100 shows E105?",
    "model": "CNC-X100",
    "answer": "Check the coolant level in the reservoir tank. If low, refill to the MAX line.",
    "sources": [
      {
        "document_name": "troubleshooting-guide.pdf",
        "document_type": "TROUBLESHOOTING",
        "page_number": 1,
        "section": "E105 Cooling System Malfunction"
      }
    ]
  }
  ```

---

### 2. Start Agentic Troubleshooting (`POST /api/assistant/troubleshoot/start`)
* Initiates a multi-turn interactive troubleshooting session.
* **Request**:
  ```json
  {
    "product": "CNC Machine",
    "model": "CNC-X100",
    "problem": "The machine stopped suddenly and shows error E105"
  }
  ```
* **Response**:
  ```json
  {
    "session_id": "4110cb99-d109-4e18-80aa-e7b5dcc52ec5",
    "product": "CNC Machine",
    "model": "CNC-X100",
    "status": "DIAGNOSING",
    "identified_issue": "Error Code E105 - Cooling System Malfunction",
    "response": "Check the coolant sight glass on the reservoir tank. Is the coolant level above the MIN mark?",
    "resolution": null,
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

### 3. Continue Agentic Troubleshooting (`POST /api/assistant/troubleshoot/{sessionId}/respond`)
* Submits technician observations or answers for an active session.
* **Request**:
  ```json
  {
    "message": "The coolant level is below MIN mark on the reservoir."
  }
  ```
* **Response**:
  ```json
  {
    "session_id": "4110cb99-d109-4e18-80aa-e7b5dcc52ec5",
    "product": "CNC Machine",
    "model": "CNC-X100",
    "status": "CORRECTIVE_ACTION",
    "identified_issue": "Error Code E105 - Cooling System Malfunction - Low Coolant Level",
    "response": "Top up coolant emulsion to 80% level. After topping up, press RESET on the control panel to clear E105.",
    "resolution": null,
    "sources": []
  }
  ```

---

### 4. Inspect Troubleshooting Session (`GET /api/assistant/troubleshoot/{sessionId}`)
* Retrieves the current diagnostic state of a troubleshooting session.

---

### 5. Multimodal Vision Analysis (`POST /api/assistant/vision/analyze`)
* Upload an image (form-data field `file`) of a control panel screen, nameplate, or machine component to extract visual diagnostics.
* **Response**:
  ```json
  {
    "detected_product": "CNC Machine",
    "detected_model": "CNC-X100",
    "detected_error_code": "E105",
    "visible_text": ["ALARM E105", "COOLANT FLOW LOW"],
    "observed_issue": "Coolant flow low warning on touchscreen HMI panel",
    "confidence": 0.95,
    "notes": "HMI alarm display clearly visible"
  }
  ```

---

### 6. Start Troubleshooting With Image (`POST /api/assistant/troubleshoot/start-with-image`)
* Upload an image (form-data field `file`) to automatically analyze visual findings and initiate an interactive troubleshooting session in a single call.
* **Response**:
  ```json
  {
    "vision_analysis": {
      "detected_product": "CNC Machine",
      "detected_model": "CNC-X100",
      "detected_error_code": "E105",
      "visible_text": ["ALARM E105"],
      "observed_issue": "Coolant flow low warning",
      "confidence": 0.95,
      "notes": "Visual match"
    },
    "troubleshooting_session": {
      "session_id": "session-v123",
      "product": "CNC Machine",
      "model": "CNC-X100",
      "status": "DIAGNOSING",
      "identified_issue": "Error Code E105 - Cooling System Malfunction",
      "response": "Inspect coolant sight glass on reservoir tank. Is the coolant level above MIN?",
      "resolution": null,
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

## Verification Endpoints (`/api/ai`)

* **`GET /api/ai/health`**: Verifies Python AI service connectivity.
* **`POST /api/ai/rag/search`**: Search ChromaDB vector store directly.
* **`POST /api/ai/rag/ask`**: Grounded Q&A via verification controller.
* **`POST /api/ai/troubleshoot/start`**: Initialize interactive troubleshooting session.
* **`POST /api/ai/troubleshoot/{sessionId}/respond`**: Continue troubleshooting session.
* **`POST /api/ai/vision/analyze`**: Multimodal image analysis.
* **`POST /api/ai/voice/transcribe`**: STT audio transcription.
* **`POST /api/ai/voice/synthesize`**: TTS audio synthesis.

---

## Local Development & Startup Order

1. **Start Python AI Service** (Port 8000):
   ```bash
   cd ai-service
   python -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```
2. **Start Spring Boot Backend** (Port 8080):
   ```bash
   cd ProductAssist-Backend
   .\mvnw.cmd spring-boot:run
   ```

---

## Running Tests

Run the full test suite via Maven wrapper:
```bash
.\mvnw.cmd test
```
Tests include unit & web integration tests for `AssistantController`, `AssistantService`, `AiServiceClient`, and `AiVerificationController`.
