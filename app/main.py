from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import hashlib
import uuid

# Import your schemas and AI engine
from app.schemas import RTIClassificationRequest, RTIClassificationResponse, FirstAppealPathway
from app.ai_engine import rti_engine

# Import the database components
from app.database import engine, get_db
from app import models

# Auto-generate the SQLite tables on boot
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="RTI Escalation Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify", response_model=RTIClassificationResponse)
async def classify_rti(request: RTIClassificationRequest, db: Session = Depends(get_db)):
    try:
        # 1. Generate Privacy-Compliant Hash & ID
        input_hash = hashlib.sha256(request.text.encode()).hexdigest()
        transaction_id = str(uuid.uuid4())
        
        # 2. Run AI Inference
        res = rti_engine.predict(request.text, request.state_code)
        
        # 3. Create Database Audit Log
        db_log = models.RTIAuditLog(
            transaction_id=transaction_id,
            input_hash=input_hash,
            decision=res["decision"],
            top_department=res['predictions'][0]['department_id'],
            confidence_score=res['predictions'][0]['confidence_score'],
            escalation_reason=res.get("escalation_reason")
        )
        db.add(db_log)
        db.commit()
        
        # 4. Return API Response
        return RTIClassificationResponse(
            transaction_id=transaction_id,
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
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"status": "online", "message": "RTI Escalation Engine is running"}