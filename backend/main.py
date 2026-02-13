from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime
from pathlib import Path

# ---- import your existing engine modules ----
from utils import normalize_url, is_valid_url
from redirects import get_redirect_chain
from feature_engine import extract_features
from risk_model import calculate_risk
from llm_explainer import generate_threat_report

from backend.db import init_db, insert_scan, fetch_scans, delete_all

# ==========================================================
# FASTAPI INIT
# ==========================================================
app = FastAPI(title="Sentinel AI PRO API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# STARTUP
# ==========================================================
@app.on_event("startup")
def startup():
    init_db()

# ==========================================================
# MODELS
# ==========================================================
class ScanRequest(BaseModel):
    input: str
    generate_ai: bool = False

class ScanResponse(BaseModel):
    url: str
    final_url: str
    redirect_chain: List[str]
    score: int
    level: str
    category: str
    confidence: float
    reasons: List[str]
    features: Dict[str, Any]
    ai_report: Optional[str] = None
    scan_seconds: float

# ==========================================================
# API ROUTES (REGISTER THESE FIRST)
# ==========================================================

@app.post("/api/scan", response_model=ScanResponse)
def scan(req: ScanRequest):

    raw = (req.input or "").strip()
    if not raw:
        raise ValueError("Empty input")

    url = normalize_url(raw)

    if not is_valid_url(url):
        raise ValueError("Invalid URL")

    start_time = datetime.utcnow()

    # Accurate mode — always resolve redirects
    chain = get_redirect_chain(url)
    final_url = chain[-1] if chain else url

    features = extract_features(final_url)

    # Expecting: score, level, category, confidence, reasons
    score, level, category, confidence, reasons = calculate_risk(
        features, chain, url
    )

    ai_report = None
    if req.generate_ai:
        ai_report = generate_threat_report(
            url=url,
            final_url=final_url,
            score=score,
            level=level,
            reasons=reasons,
            features=features
        )

    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()

    # Save to DB
    insert_scan({
        "ts": end_time.isoformat() + "Z",
        "url": url,
        "final_url": final_url,
        "score": score,
        "level": level,
        "category": category,
        "confidence": confidence
    })

    return {
        "url": url,
        "final_url": final_url,
        "redirect_chain": chain,
        "score": score,
        "level": level,
        "category": category,
        "confidence": float(confidence),
        "reasons": reasons,
        "features": features,
        "ai_report": ai_report,
        "scan_seconds": duration
    }

@app.get("/api/history")
def history(limit: int = Query(200, ge=1, le=500)):
    return {"items": fetch_scans(limit)}

@app.post("/api/history/clear")
def clear_history():
    delete_all()
    return {"ok": True}

# ==========================================================
# MOUNT FRONTEND (MUST BE LAST)
# ==========================================================
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

