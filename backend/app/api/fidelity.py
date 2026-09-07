"""
AegisPay v2 - Multi-Dimensional Fidelity Scorecard API Router
"""

from fastapi import APIRouter
import numpy as np

from backend.evaluation.fidelity import fidelity_engine


router = APIRouter(tags=["Data & Lifecycle Fidelity"])


@router.get("/fidelity")
@router.post("/fidelity/compute")
def get_fidelity_scorecard():
    # Generate representative sample of simulated transactions
    np.random.seed(42)
    sample_data = []
    for _ in range(300):
        sample_data.append({
            "amount": float(np.random.lognormal(3.8, 1.1)),
            "velocity_1h": float(np.random.poisson(1.5)),
            "device_familiarity": float(np.random.beta(5, 2)),
            "behavioral_deviation": float(np.random.beta(2, 5)),
            "hour_of_day": float(np.random.normal(14.0, 3.5)) % 24
        })

    return fidelity_engine.compute_scorecard(sample_data)
