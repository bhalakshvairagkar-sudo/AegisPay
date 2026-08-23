"""
Synthetic Data Fidelity API
"""

from fastapi import APIRouter
import pandas as pd

from backend.app.services.state_manager import system_state
from backend.evaluation.experiments import experiment_registry

router = APIRouter(prefix="/fidelity", tags=["Fidelity"])


@router.get("")
def get_fidelity_metrics():
    latest_exp = experiment_registry.get_latest()
    if latest_exp and latest_exp.get("fidelity_metrics"):
        return latest_exp["fidelity_metrics"]

    # Compute live on sample
    legit_sample = system_state.simulator.generate_legitimate_stream(300)
    df = pd.DataFrame([t.to_feature_dict() for t in legit_sample])
    return system_state.fidelity_engine.evaluate_fidelity(df)


@router.post("/compute")
def compute_fidelity_live(n_samples: int = 500):
    legit_sample = system_state.simulator.generate_legitimate_stream(n_samples)
    df = pd.DataFrame([t.to_feature_dict() for t in legit_sample])
    return system_state.fidelity_engine.evaluate_fidelity(df)
