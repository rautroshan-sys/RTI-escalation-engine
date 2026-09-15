# API Contracts & Pydantic Schemas

from pydantic import BaseModel, Field
from typing import Optional

class RTIClassificationRequest(BaseModel):
    text: str = Field(..., description="The raw text of the RTI application in English, Hindi, or Marathi.")
    state_code: Optional[str] = Field(None, description="Optional 2-letter state code (e.g., 'MH', 'DL').")

class DepartmentPrediction(BaseModel):
    department_id: str
    confidence_score: float

class FirstAppealPathway(BaseModel):
    appellate_authority: str
    statutory_timeline_days: int = 30
    draft_letter_template: str

class RTIClassificationResponse(BaseModel):
    transaction_id: str
    predictions: list[DepartmentPrediction] # Must contain exactly top 2
    decision: str # "AUTO_ROUTE" or "ESCALATE"
    escalation_reason: Optional[str] = None
    appeal_pathway: Optional[FirstAppealPathway] = None