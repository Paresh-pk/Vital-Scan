from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import uuid

from app.models.schemas import ClinicalInput, AssessmentResponse
from app.core.ml_service import MLRiskEngine
from app.core.storage import LocalStorage

router = APIRouter()
storage = LocalStorage()

# Initialize ML Engine (Load logic once)
try:
    risk_engine = MLRiskEngine()
except Exception as e:
    print(f"WARNING: ML Engine failed to load: {e}")
    risk_engine = None

@router.post("/assess", response_model=AssessmentResponse)
async def assess_clinical_risk(input_data: ClinicalInput):
    """
    Perform population-level risk estimation using NHANES-trained models.
    """
    if not risk_engine:
        raise HTTPException(status_code=503, detail="Risk Engine not initialized. Models missing.")

    try:
        # 1. ML Inference
        risks = risk_engine.assess(input_data)
        
        # 2. Construct Response
        response = AssessmentResponse(
            assessment_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            risks=risks
        )
        
        # 3. Privacy-Preserving Store (Encrypted)
        storage.save_assessment(response)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
