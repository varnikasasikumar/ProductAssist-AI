import uuid
import time
from typing import Dict, Any, Optional, List

class TroubleshootingSession:
    """
    In-memory session state model for tracking multi-turn diagnostic workflows.
    Supported Statuses:
      - DIAGNOSING        : Collecting initial observations or isolating cause.
      - CORRECTIVE_ACTION : Root cause identified, corrective instructions provided.
      - VERIFYING         : Awaiting user confirmation that action resolved issue.
      - RESOLVED          : User verified machine operating normally / issue fixed.
      - ESCALATED         : Documentation insufficient or service technician needed.
    """
    def __init__(self, model: str, problem: str, product: str = "CNC Machine"):
        self.session_id = str(uuid.uuid4())
        self.product = product
        self.model = model
        self.problem = problem
        self.identified_issue: Optional[str] = None
        self.error_code: Optional[str] = None
        self.diagnostic_answers: List[Dict[str, str]] = []
        self.current_step: int = 1
        self.status: str = "DIAGNOSING"
        self.resolution: Optional[str] = None
        self.sources: List[Dict[str, Any]] = []
        self.created_at = time.time()
        self.updated_at = time.time()

    def add_diagnostic_answer(self, question: str, answer: str):
        self.diagnostic_answers.append({"question": question, "answer": answer})
        self.current_step += 1
        self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "product": self.product,
            "model": self.model,
            "problem": self.problem,
            "identified_issue": self.identified_issue,
            "error_code": self.error_code,
            "diagnostic_answers": self.diagnostic_answers,
            "current_step": self.current_step,
            "status": self.status,
            "resolution": self.resolution,
            "sources": self.sources,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class SessionStore:
    """
    In-memory thread-safe session store for hackathon MVP.
    Designed so persistent storage (e.g. Redis / PostgreSQL) can be swapped in later.
    """
    def __init__(self):
        self._sessions: Dict[str, TroubleshootingSession] = {}

    def create_session(self, model: str, problem: str, product: str = "CNC Machine") -> TroubleshootingSession:
        session = TroubleshootingSession(model=model, problem=problem, product=product)
        self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[TroubleshootingSession]:
        return self._sessions.get(session_id)

    def save_session(self, session: TroubleshootingSession):
        session.updated_at = time.time()
        self._sessions[session.session_id] = session

session_store = SessionStore()
