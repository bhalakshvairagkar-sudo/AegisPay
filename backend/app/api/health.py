"""
Health & Diagnostic Endpoints
"""

from fastapi import APIRouter
from backend.app.services.state_manager import system_state
from backend.evaluation.experiments import experiment_registry

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health():
    latest_exp = experiment_registry.get_latest()
    return {
        "status": "healthy",
        "service": "AegisPay Defense Lab API",
        "version": "2026.1",
        "active_model": system_state.current_model_version,
        "latest_experiment_id": latest_exp.get("experiment_id") if latest_exp else None,
        "closed_loop_engine": "ACTIVE",
    }
