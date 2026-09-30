from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from datetime import datetime
from backend.database import Base

class VerificationRecord(Base):
    __tablename__ = "verifications"
    id = Column(Integer, primary_key=True, index=True)
    claim = Column(String, index=True)
    context_data = Column(JSON)
    trust_score = Column(Float)
    decision = Column(String)
    explanation = Column(String)
    claims_output = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
