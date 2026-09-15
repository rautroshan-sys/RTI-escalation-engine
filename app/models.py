from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime, timezone

class RTIAuditLog(Base):
    __tablename__ = "rti_audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    
    # Privacy-Compliant Log: Storing hash instead of raw PII text
    input_hash = Column(String, index=True)  
    
    decision = Column(String)  # 'AUTO_ROUTE' or 'ESCALATE'
    top_department = Column(String)
    confidence_score = Column(Float)
    escalation_reason = Column(String, nullable=True)
    
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))