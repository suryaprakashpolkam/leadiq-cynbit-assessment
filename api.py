from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from lead_analyzer import analyze_inquiry
from ml_model import predict_readiness
from database import save_analysis, list_analyses, init_db

app = FastAPI(title="LeadIQ API", version="0.1.0", description="Lead inquiry extraction and readiness classification PoC")

class InquiryRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": "LeadIQ API"}

@app.post("/analyze")
def analyze(request: InquiryRequest):
    try:
        analysis, mode = analyze_inquiry(request.message)
        readiness = predict_readiness(analysis)
        record_id = save_analysis(request.message, analysis, readiness)
        return {
            "id": record_id,
            "extraction_mode": mode,
            "analysis": analysis.model_dump(),
            "readiness": readiness
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {type(exc).__name__}")

@app.get("/analyses")
def analyses(limit: int = 20):
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    return {"items": list_analyses(limit)}
