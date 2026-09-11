# ProductAssist AI

### RAG and Agentic AI-Based Multimodal Assistance System for Product Operation, Troubleshooting, and Maintenance

ProductAssist AI is an AI-powered assistance system designed to help technicians operate, troubleshoot, and maintain industrial products using authorized technical documentation.

The system combines **Retrieval-Augmented Generation (RAG), Agentic AI, Multimodal Vision, and Voice Interaction** to provide context-aware, step-by-step troubleshooting assistance.

It can retrieve relevant information from product manuals and technical documents, analyze control-panel images to identify products and error codes, guide technicians through an interactive troubleshooting workflow, and provide grounded responses with source references.

## Key Features

- 📚 **RAG-based Knowledge Retrieval**  
  Retrieves relevant information from authorized product manuals and technical documentation to generate grounded responses with source references.

- 🤖 **Agentic Troubleshooting**  
  Provides interactive, multi-step troubleshooting through diagnostic questions, corrective actions, verification, resolution, or escalation.

- 👁️ **Multimodal Vision**  
  Analyzes uploaded product/control-panel images to identify information such as product models, error codes, and visible text.

- 🎤 **Voice Interaction**  
  Supports speech-to-text and text-to-speech interaction for hands-free assistance.

- 🏭 **Multi-Product Support**  
  Designed to support multiple products and models through model-specific knowledge retrieval.

- 📖 **Multi-Format Knowledge Base**  
  Supports product knowledge from formats such as PDF, DOCX, HTML, JSON, and CSV.

- 🛡️ **Safety-Aware Troubleshooting**  
  Preserves safety precautions and provides controlled troubleshooting guidance for maintenance scenarios.

- 🔎 **Source-Cited Responses**  
  Provides document, page, and section references so technicians can verify the information used to generate an answer.

- 🔄 **Continuous Knowledge Updates**  
  New or updated product documents can be processed, chunked, embedded, and added to the vector knowledge base without retraining the LLM.

## System Architecture

ProductAssist AI follows a layered architecture where the frontend, business backend, and AI service communicate through REST APIs.

```text
┌──────────────────────────────┐
│      React + TypeScript      │
│         Frontend             │
└──────────────┬───────────────┘
               │ REST API
               ▼
┌──────────────────────────────┐
│      Spring Boot + Java      │
│      Business Backend        │
│                              │
│   Products / Models /        │
│   Documents / Maintenance    │
└──────────────┬───────────────┘
               │ REST API
               ▼
┌──────────────────────────────┐
│       Python + FastAPI       │
│          AI Service          │
├──────────────────────────────┤
│                              │
│  RAG        Vision     Voice │
│   │           │          │   │
│   ▼           ▼          ▼   │
│ ChromaDB   Gemini     STT/TTS│
│   │                          │
│   ▼                          │
│ Embeddings + LLM             │
│                              │
│ Agentic Troubleshooting      │
│ Safety & Verification        │
└──────────────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
   ChromaDB         MySQL
 Knowledge Base   Application Data
```

### Main Components

Frontend — React + TypeScript + Vite

Provides the user interface for technicians.
Supports text, image, and voice interactions.
Displays troubleshooting steps, source citations, and visual guidance.

Backend — Java + Spring Boot

Provides application-facing REST APIs.
Manages structured product and maintenance data.
Communicates with the Python AI service.

AI Service — Python + FastAPI

Handles RAG, document processing, embeddings, vision, voice, and troubleshooting orchestration.
Provides AI APIs consumed by the Spring Boot backend.

ChromaDB

Stores document embeddings and metadata.
Performs semantic retrieval of relevant knowledge chunks.

MySQL

Stores structured application data such as products, product models, documents, and maintenance records.

``

## RAG Workflow

ProductAssist AI uses Retrieval-Augmented Generation (RAG) to provide answers grounded in authorized product documentation.

The workflow consists of the following stages:

1. **Document Ingestion**
   - Product manuals and technical documents are uploaded to the knowledge base.
   - Supported formats include PDF, DOCX, HTML, JSON, and CSV.

2. **Text Extraction**
   - Text is extracted from the uploaded documents.
   - PDF content is processed page by page to preserve document references.

3. **Structure-Aware Chunking**
   - Extracted content is divided into smaller meaningful chunks.
   - Chunk metadata includes document name, page, section, and chunk index.

4. **Embedding Generation**
   - Each chunk is converted into a numerical vector representation using an embedding model.

5. **Vector Storage**
   - Embeddings and their metadata are stored in ChromaDB.

6. **Semantic Retrieval**
   - When a technician asks a question, the query is converted into an embedding.
   - ChromaDB retrieves the most semantically relevant knowledge chunks.

7. **Grounded Response Generation**
   - Retrieved context is provided to the LLM.
   - The LLM generates an answer using only the authorized retrieved information.

8. **Source References**
   - The response includes references to the relevant document, page, or section so that technicians can verify the information.

### RAG Flow

```text
Product Documents
       │
       ▼
Text Extraction
       │
       ▼
Structure-Aware Chunking
       │
       ▼
Embedding Generation
       │
       ▼
     ChromaDB
       │
       │
User Query
       │
       ▼
Query Embedding
       │
       ▼
Semantic Retrieval
       │
       ▼
Relevant Knowledge
       │
       ▼
      LLM
       │
       ▼
Grounded Answer
       │
       ▼
Source References
```

## Agentic Troubleshooting Workflow

ProductAssist AI uses an agentic troubleshooting workflow to guide technicians through diagnosis, corrective actions, verification, and resolution.

Unlike a simple question-and-answer chatbot, the troubleshooting system maintains the current session state and determines the next step based on the technician's responses.

### Workflow

```text
Product / Error Identification
            │
            ▼
        Diagnosis
            │
            ▼
   Diagnostic Questions
            │
            ▼
     Decision / Analysis
            │
            ▼
    Corrective Action
            │
            ▼
        Verification
       ┌────┴────┐
       │         │
    Resolved   Failed
       │         │
       ▼         ▼
   Resolution  Escalation

Troubleshooting States

DIAGNOSING — Collects information and asks diagnostic questions.
CORRECTIVE_ACTION — Provides the appropriate corrective procedure.
VERIFYING — Checks whether the corrective action resolved the issue.
RESOLVED — Confirms successful resolution.
ESCALATED — Used when the issue cannot be safely resolved through the available workflow.
```

## Multimodal & Voice Assistance

ProductAssist AI extends traditional text-based assistance with image and voice interaction, enabling technicians to communicate with the system in more natural and practical ways.

### Vision-Based Assistance

Technicians can upload an image of a product control panel or equipment.

The vision pipeline can:

- Identify the product and model.
- Detect visible error codes and text.
- Analyze relevant visual information.
- Use the detected information to initiate the appropriate troubleshooting workflow.

For example:

```text
Control Panel Image
        │
        ▼
Multimodal Vision Model
        │
        ▼
Product + Model + Error Code
        │
        ▼
Troubleshooting Workflow
        │
        ▼
Step-by-Step Guidance
```

## Voice Assistance

The system supports voice interaction through:

Speech-to-Text (STT) — Converts technician speech into text.
AI Processing — Processes the transcribed request using the RAG and troubleshooting workflows.
Text-to-Speech (TTS) — Converts the generated response into spoken guidance.
Technician Speech
│
▼
Speech-to-Text
│
▼
AI / RAG / Agent
│
▼
Generated Response
│
▼
Text-to-Speech
│
▼
Spoken Guidance
``

## Technology Stack

| Layer             | Technologies                          |
| ----------------- | ------------------------------------- |
| Frontend          | React, TypeScript, Vite               |
| Backend           | Java, Spring Boot, Spring Data JPA    |
| AI Service        | Python, FastAPI                       |
| RAG Framework     | LangChain                             |
| Vector Database   | ChromaDB                              |
| Embeddings        | Sentence Transformers                 |
| LLM               | Gemini / Configurable LLM Provider    |
| Vision            | Multimodal Vision Model               |
| Speech-to-Text    | Gemini / Whisper-compatible providers |
| Text-to-Speech    | Browser TTS / API-based providers     |
| Database          | MySQL                                 |
| API Communication | REST APIs                             |
| Version Control   | Git, GitHub                           |

### Architecture Pattern

The project follows a **separated frontend, business backend, and AI-service architecture**:

- **React** handles the user interface and interaction.
- **Spring Boot** handles business logic, structured data, and application APIs.
- **FastAPI** provides AI-specific capabilities such as RAG, vision, voice, and troubleshooting orchestration.
- **MySQL** manages structured application data.
- **ChromaDB** manages vectorized knowledge for semantic retrieval.

## Project Structure

```text
ProductAssist-AI/
│
├── ProductAssist-Backend/
│   └── Spring Boot application
│       ├── Controllers
│       ├── Services
│       ├── Entities
│       ├── Repositories
│       └── AI Service Integration
│
├── ai-service/
│   └── Python FastAPI service
│       ├── RAG
│       ├── Troubleshooting
│       ├── Vision
│       ├── Voice
│       ├── Maintenance
│       └── API Endpoints
│
├── frontend/
│   └── React + TypeScript application
│       ├── Pages
│       ├── Components
│       ├── Services
│       └── Assets
│
├── knowledge-base/
│   └── Product knowledge and technical documentation
│       ├── Manuals
│       ├── Troubleshooting Guides
│       ├── Safety Documentation
│       ├── Specifications
│       └── Visual Assets
│
├── .gitignore
└── README.md
```

## Demo Scenario

The primary demonstration uses the **CNC-X100 CNC Machine** and a simulated **E105 Cooling System Fault**.

### Scenario

A technician encounters an E105 error and the machine stops operating.

The technician can:

1. Upload a control-panel image showing the E105 error.
2. The vision system identifies the product, model, and visible error code.
3. The system retrieves relevant troubleshooting and maintenance information using RAG.
4. The troubleshooting agent begins an interactive diagnostic workflow.
5. The technician answers diagnostic questions.
6. The system provides the appropriate corrective action with safety precautions.
7. The technician performs the recommended action.
8. The system enters the verification stage.
9. If the issue is resolved, the workflow reaches **RESOLVED**.
10. If the issue cannot be safely resolved, the workflow can be **ESCALATED**.

### Example

```text
CNC-X100
   │
   ▼
E105 Cooling System Fault
   │
   ▼
Vision Analysis
   │
   ▼
RAG Retrieval
   │
   ▼
Agentic Diagnosis
   │
   ▼
Corrective Action
   │
   ▼
Verification
   │
   ├──► Resolved
   │
   └──► Escalated
```

## Supported Products & Knowledge Base

ProductAssist AI is designed as a multi-product assistance platform rather than a system limited to a single machine.

### Demo Products

| Product Category   | Model        | Example Use Case                            |
| ------------------ | ------------ | ------------------------------------------- |
| CNC Machine        | CNC-X100     | Operation, troubleshooting, and maintenance |
| Industrial Printer | Printer-A200 | Error diagnosis and operational assistance  |
| HVAC System        | HVAC-C500    | Troubleshooting and maintenance guidance    |

The system uses model-specific knowledge so that retrieved information can be associated with the correct product and model.

### Knowledge Sources

The knowledge base can contain multiple types of product information:

- Operation manuals
- Installation guides
- Troubleshooting guides
- Maintenance manuals
- Service manuals
- Safety documentation
- Technical specifications
- Product-specific structured data
- Spare-parts information
- Visual diagrams and flowcharts
- Operator reference guides

Documents are processed into searchable knowledge chunks with metadata such as **document name, page, section, product, model, and version**.

This allows the system to retrieve information relevant to the selected product and troubleshooting context.

## Safety & Hallucination Control

ProductAssist AI is designed to provide controlled and grounded assistance for technical troubleshooting.

### Grounded Responses

The LLM is instructed to generate responses only from the authorized knowledge retrieved from the product knowledge base.

The system:

- Uses retrieved documentation as the primary source of truth.
- Provides source references for generated answers.
- Avoids inventing unsupported technical information.
- Returns an insufficient-information response when the required information is not available in the knowledge base.

### Safety-Aware Troubleshooting

Safety information is preserved during the troubleshooting process.

The system can:

- Present relevant safety warnings before maintenance actions.
- Prevent unsupported troubleshooting instructions.
- Use controlled workflow states for diagnostic and corrective procedures.
- Escalate issues when the available workflow cannot safely resolve the problem.

### Error Handling

The system also includes fallback mechanisms for cases such as:

- Insufficient knowledge in the knowledge base.
- Low-confidence vision results.
- AI service unavailability.
- Invalid or unsupported inputs.

Rather than assuming an answer, the system can request clarification or recommend escalation when reliable assistance cannot be provided.

> **Design principle:** The LLM provides intelligence and language understanding, while the application workflow, knowledge base, and safety controls govern how that intelligence is used.

## Future Enhancements

ProductAssist AI can be extended beyond the current prototype with additional capabilities such as:

- 🌐 **Real-Time Equipment Monitoring**  
  Integrate live machine telemetry and sensor data for proactive fault detection.

- 📱 **Mobile / Edge Assistance**  
  Extend the system to mobile or edge devices for technicians working directly on equipment.

- 🧠 **Advanced Predictive Maintenance**  
  Use historical maintenance data and equipment signals to predict potential failures before they occur.

- 🔄 **Automated Knowledge Versioning**  
  Improve document version management and automatically prioritize the latest approved product documentation.

- 🌍 **Multi-Language Assistance**  
  Support technicians across different regions with multilingual text and voice interaction.

- 📊 **Advanced Analytics**  
  Provide dashboards for recurring faults, maintenance trends, resolution times, and equipment reliability.

- 🔌 **Enterprise System Integration**  
  Integrate with existing enterprise systems such as service management, inventory, and maintenance platforms.

- 🤖 **More Specialized AI Agents**  
  Introduce specialized agents for maintenance planning, spare-parts recommendation, diagnostics, and service escalation.

## How to Run

ProductAssist AI consists of three main application services:

1. React frontend
2. Spring Boot backend
3. Python FastAPI AI service

### Prerequisites

Make sure the following are installed:

- Java
- Maven
- Python 3.11+
- Node.js and npm
- MySQL
- Git

### 1. Start the AI Service

```bash
cd ai-service

venv\Scripts\activate

uvicorn main:app --host 127.0.0.1 --port 8000
```

The AI service runs on:

http://127.0.0.1:8000

``

### 2. Start the Spring Boot Backend

Open the ProductAssist-Backend project in Eclipse or your preferred Java IDE and run the Spring Boot application.

The backend runs on:

http://localhost:8080
``

### 3. Start the React Frontend

cd frontend
npm install
npm run dev

The frontend is available at the Vite development URL shown in the terminal, typically:

http://localhost:5173
``

### Environment Configuration

API keys, database passwords, and other secrets should be configured through environment variables or local .env files.

Important: Never commit API keys, database passwords, .env files, virtual environments, node_modules, build artifacts, or local vector database files to GitHub.

## API Endpoints

The system exposes REST APIs across the Spring Boot backend and Python AI service.

### Spring Boot Backend

| Method | Endpoint                                          | Purpose                                |
| ------ | ------------------------------------------------- | -------------------------------------- |
| POST   | `/api/assistant/ask`                              | Ask a knowledge-based question         |
| POST   | `/api/assistant/troubleshoot/start`               | Start troubleshooting                  |
| POST   | `/api/assistant/troubleshoot/{sessionId}/respond` | Respond to a troubleshooting step      |
| GET    | `/api/assistant/troubleshoot/{sessionId}`         | Retrieve troubleshooting session state |
| POST   | `/api/assistant/vision/analyze`                   | Analyze an uploaded image              |
| POST   | `/api/assistant/troubleshoot/start-with-image`    | Start troubleshooting using an image   |
| POST   | `/api/assistant/voice/transcribe`                 | Convert speech to text                 |
| POST   | `/api/assistant/voice/synthesize`                 | Convert text to speech                 |
| POST   | `/api/assistant/voice/troubleshoot`               | Start troubleshooting using voice      |

### Python AI Service

| Method | Endpoint                                        | Purpose                                           |
| ------ | ----------------------------------------------- | ------------------------------------------------- |
| GET    | `/health`                                       | Check AI service health                           |
| POST   | `/rag/ask`                                      | Retrieve knowledge and generate a grounded answer |
| POST   | `/troubleshoot/start`                           | Start an agentic troubleshooting session          |
| POST   | `/troubleshoot/{session_id}/respond`            | Process a troubleshooting response                |
| GET    | `/troubleshoot/{session_id}`                    | Retrieve troubleshooting state                    |
| POST   | `/vision/analyze`                               | Analyze product/control-panel images              |
| POST   | `/troubleshoot/start-with-image`                | Start troubleshooting from image analysis         |
| POST   | `/voice/transcribe`                             | Perform speech-to-text                            |
| POST   | `/voice/synthesize`                             | Perform text-to-speech                            |
| POST   | `/troubleshoot/start-with-voice`                | Start troubleshooting from voice input            |
| POST   | `/troubleshoot/{session_id}/respond-with-voice` | Respond to troubleshooting using voice            |

The Spring Boot backend acts as the application-facing API layer and communicates with the Python AI service through REST APIs.

## Team & Contributions

ProductAssist AI was developed as a two-person team during a 24-hour hackathon.

### AI & Backend

- Python + FastAPI AI service
- RAG pipeline and vector knowledge retrieval
- Embedding generation and ChromaDB integration
- LLM integration and grounded answer generation
- Agentic troubleshooting workflow
- Multimodal vision analysis
- Speech-to-text and text-to-speech integration
- Spring Boot integration with the AI service

### Frontend & Application

- React + TypeScript frontend
- Dashboard and application UI
- Product and model management
- Assistant interface
- Image and voice interaction
- Troubleshooting workflow interface
- Maintenance history interface
- Knowledge base interface
- Integration with backend APIs

### Collaboration

Both team members worked together on:

- System architecture and problem analysis
- ProductAssist AI workflow design
- Hackathon implementation and integration
- Testing and debugging
- Final demonstration and presentation

## Project Status

ProductAssist AI was developed as a working prototype during a 24-hour hackathon.

The current implementation demonstrates:

- RAG-based technical knowledge retrieval
- Grounded AI responses with source references
- Agentic troubleshooting workflows
- Multimodal product and error identification
- Voice-based interaction
- Multi-format knowledge ingestion
- Safety-aware troubleshooting
- Product and maintenance management
- Frontend, backend, and AI-service integration

The architecture is designed to be extended with additional products, models, knowledge sources, AI capabilities, and enterprise integrations.

## Acknowledgements

This project was developed as part of a 24-hour intra-college hackathon.

We would like to thank the organizers, mentors, faculty members, and everyone who supported us throughout the hackathon.

---

⭐ If you find this project interesting, feel free to explore the repository and follow its development.

```

```
