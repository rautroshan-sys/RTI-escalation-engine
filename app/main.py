from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from app.schemas import RTIClassificationRequest, RTIClassificationResponse, FirstAppealPathway
from app.ai_engine import rti_engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify", response_model=RTIClassificationResponse)
async def classify_rti(request: RTIClassificationRequest):
    try:
        res = rti_engine.predict(request.text, request.state_code)
        
        return RTIClassificationResponse(
            transaction_id=str(uuid.uuid4()),
            predictions=res["predictions"],
            decision=res["decision"],
            escalation_reason=res["escalation_reason"],
            appeal_pathway=FirstAppealPathway(
                appellate_authority=f"First Appellate Authority, {res['predictions'][0]['department_id']}",
                statutory_timeline_days=30,
                draft_letter_template="Pursuant to Section 6(3) and Section 19 of the RTI Act..."
            ) if res["decision"] == "ESCALATE" else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    