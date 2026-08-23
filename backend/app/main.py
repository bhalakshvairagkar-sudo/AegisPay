"""
AegisPay Defense Lab - Main FastAPI Application Entry Point
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
from backend.app.api.gap_analysis import router as gap_router
from backend.app.api.retrain import router as retrain_router
from backend.app.api.evolution import router as evolution_router
from backend.app.api.fidelity import router as fidelity_router
from backend.app.api.dashboard import router as dashboard_router
from backend.app.api.judge_demo import router as judge_demo_router

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Adaptive Adversarial AI Lab for Payment Security - Research API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api
app.include_router(health_router, prefix="/api")
app.include_router(taxonomy_router, prefix="/api")
app.include_router(attacks_router, prefix="/api")
app.include_router(predict_router, prefix="/api")
app.include_router(models_router, prefix="/api")
app.include_router(gap_router, prefix="/api")
app.include_router(retrain_router, prefix="/api")
app.include_router(evolution_router, prefix="/api")
app.include_router(fidelity_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
app.include_router(judge_demo_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to AegisPay - AI Defense Lab for Payment Security",
        "docs": "/docs",
        "version": settings.version,
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
