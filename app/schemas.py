from pydantic import BaseModel, Field
from typing import List, Optional

class RTIClassificationRequest(BaseModel):
    text: str = Field(...)
    state_code: Optional[str] = None

class DepartmentPrediction(BaseModel):
    department_id: str
    confidence_score: float

class FirstAppealPathway(BaseModel):
    appellate_authority: str
    statutory_timeline_days: int = 30
    draft_letter_template: str

class RTIClassificationResponse(BaseModel):
    transaction_id: str
    predictions: List[DepartmentPrediction]
    decision: str
    escalation_reason: Optional[str] = None
    appeal_pathway: Optional[FirstAppealPathway] = None