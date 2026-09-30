import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend import models, database
from trustagent.pipeline.run import run_pipeline

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="TrustAgent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class VerifyRequest(BaseModel):
    agent_response: str
    context: Dict[str, Any]

@app.post("/verify")
def verify_claim(req: VerifyRequest, db: Session = Depends(get_db)):
    try:
        result = run_pipeline(req.agent_response, req.context)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        record = models.VerificationRecord(
            claim=req.agent_response,
            context_data=req.context,
            trust_score=result["trust_score"],
            decision=result["decision"],
            explanation=result["explanation"],
            claims_output=result["claims"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/history")
def get_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    records = db.query(models.VerificationRecord).order_by(models.VerificationRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records
