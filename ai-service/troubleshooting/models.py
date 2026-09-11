from typing import List, Optional
from pydantic import BaseModel, Field

class StartTroubleshootingRequest(BaseModel):
    model: str = Field(..., min_length=1, description="Product model designation, e.g., 'CNC-X100'", example="CNC-X100")
    problem: str = Field(..., min_length=1, description="Initial problem or error code statement", example="The machine stopped suddenly and shows error E105")

class ContinueTroubleshootingRequest(BaseModel):
    response: str = Field(..., min_length=1, description="User's diagnostic observation or answer", example="The coolant level is below MIN.")

class TroubleshootingSourceItem(BaseModel):
    document_name: str
    document_type: str
    page_number: int
    section: str

class TroubleshootingResponse(BaseModel):
    session_id: str
    model: str
    identified_issue: Optional[str] = None
    message: str
    next_question: Optional[str] = None
    status: str = Field(..., description="DIAGNOSING | CORRECTIVE_ACTION | VERIFYING | RESOLVED | ESCALATED")
    reasoning_summary: Optional[str] = None
    sources: List[TroubleshootingSourceItem]
