"""
Model Benchmark & Comparison API
"""

from fastapi import APIRouter
from typing import List

from backend.app.schemas.schemas import ModelBenchmarkItem
from backend.evaluation.experiments import experiment_registry
from backend.models.registry import global_registry

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("/comparison", response_model=List[ModelBenchmarkItem])
def get_model_benchmarks():
    latest_exp = experiment_registry.get_latest()
    if latest_exp and latest_exp.get("models_evaluated"):
        return [ModelBenchmarkItem(**m) for m in latest_exp["models_evaluated"]]

    # Return registered metadata or empty if not evaluated
    items = []
    for m_id, meta in global_registry.model_metadata.items():
        if "precision" in meta:
            items.append(ModelBenchmarkItem(**meta))
    return items
