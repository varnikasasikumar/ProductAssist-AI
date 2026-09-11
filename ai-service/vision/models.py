from typing import List, Optional
from pydantic import BaseModel, Field
from troubleshooting.models import TroubleshootingResponse

class VisionAnalysisResponse(BaseModel):
    detected_product: Optional[str] = Field(None, description="Detected product type (e.g. 'CNC Machine') or null if unreadable", example="CNC Machine")
    detected_model: Optional[str] = Field(None, description="Detected product model designation (e.g. 'CNC-X100') or null if unreadable", example="CNC-X100")
    detected_error_code: Optional[str] = Field(None, description="Detected display error code (e.g. 'E105') or null if unreadable", example="E105")
    visible_text: List[str] = Field(default_factory=list, description="List of visible text labels, display messages, or warning text read from the image")
    observed_issue: Optional[str] = Field(None, description="Objective visual observation of physical state or display warning", example="Coolant level low indicator light and error E105 visible on HMI screen")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score for the visual extraction (0.0 to 1.0)", example=0.95)
    notes: Optional[str] = Field(None, description="Analytical notes distinguishing visible observations from inferred possibilities", example="Clear view of HMI panel showing error E105 alarm.")

class VisionTroubleshootResponse(BaseModel):
    vision_analysis: VisionAnalysisResponse
    troubleshooting_session: TroubleshootingResponse
