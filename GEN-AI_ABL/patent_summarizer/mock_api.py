"""
Lightweight mock FastAPI used for reliable smoke tests.
Exposes /health, /models, /analyze (mock) endpoints.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Mock Patent Analyzer API", version="0.0.1")

class AnalyzeRequest(BaseModel):
    claim_text: str
    description: str
    style: str = "technical"
    model_name: str = "mock"
    use_mock: bool = True
    index_path: str = ""
    num_prior_art: int = 3
    retriever_type: str = "automatic"

class AnalyzeResponse(BaseModel):
    request_id: str
    patent_id: str
    summary: str
    novelty_score: float
    novelty_analysis: str
    prior_art: List[str]
    model_used: str
    style: str
    timestamp: str

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat(), "models_available": ["mock"]}

@app.get("/models")
async def models():
    return {"models": [
        {"name": "mock", "description": "Mock LLM for testing", "size": "0 MB"},
        {"name": "google/flan-t5-small", "description": "Flan-T5 Small", "size": "305 MB"}
    ], "default": "mock"}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    # deterministic mock output
    return AnalyzeResponse(
        request_id="mock-req-123",
        patent_id="MOCK-001",
        summary=f"Mock summary for claim: {req.claim_text[:120]}",
        novelty_score=0.42,
        novelty_analysis="This is a mocked novelty analysis.",
        prior_art=["Mock prior art A", "Mock prior art B"],
        model_used=req.model_name,
        style=req.style,
        timestamp=datetime.now().isoformat()
    )
