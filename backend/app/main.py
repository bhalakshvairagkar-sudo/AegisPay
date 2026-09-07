"""
AegisPay v2 - Main FastAPI Application Entry Point
Exposes research-grade REST endpoints under /api and /api/v1.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.app.config.settings import settings
from backend.app.api.health import router as health_router
from backend.app.api.taxonomy import router as taxonomy_router
from backend.app.api.attacks import router as attacks_router
from backend.app.api.predict import router as predict_router
from backend.app.api.models_api import router as models_router
from backend.app.api.defense_api import router as defense_router
from backend.app.api.gap_analysis import router as gap_router
from backend.app.api.retrain import router as retrain_router
from backend.app.api.evolution import router as evolution_router
from backend.app.api.fidelity import router as fidelity_router
from backend.app.api.audits_api import router as audits_router
from backend.app.api.simulator_api import router as simulator_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.judge_demo import router as judge_demo_router

app = FastAPI(
    title=settings.app_name,
    version="2026.2.0",
    description="AegisPay v2 - AI Defense Lab for Payment Security - Closed-Loop Adversarial Research API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api and /api/v1
routers = [
    health_router,
    taxonomy_router,
    attacks_router,
    predict_router,
    models_router,
    defense_router,
    gap_router,
    retrain_router,
    evolution_router,
    fidelity_router,
    audits_router,
    simulator_router,
    dashboard_router,
    judge_demo_router
]

for r in routers:
    app.include_router(r, prefix="/api")
    app.include_router(r, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "message": "Welcome to AegisPay v2 - AI Defense Lab for Payment Security",
        "docs": "/docs",
        "version": "2026.2.0",
        "status": "online",
        "scientific_contract": "100% Verified Invariant Build Gates"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
