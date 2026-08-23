"""
Gap Analysis & Evasion Clustering API
"""

from fastapi import APIRouter
import pandas as pd

from backend.app.services.state_manager import system_state
from backend.evaluation.experiments import experiment_registry

router = APIRouter(prefix="/gap-analysis", tags=["Gap Analysis"])


@router.post("")
def run_gap_analysis(n_attacks: int = 50, mutation_strength: float = 0.65):
    """
    Generates a fresh test batch, runs active defense, extracts false negatives, and clusters them.
    """
    scenarios = system_state.generator.generate_scenarios(
        count=n_attacks,
        family_filter="ALL",
        mutation_strength=mutation_strength,
        difficulty="Hard"
    )
    # Exclude holdout family
    scenarios_known = [s for s in scenarios if s.attack_family != "AI Adaptive Fraud"]

    df = pd.DataFrame([s.to_feature_dict() for s in scenarios_known])
    active_model = system_state.get_active_defense()

    pred = active_model.predict(df)
    prob = active_model.predict_proba(df)[:, 1]

    gap_report = system_state.gap_analyzer.analyze_evasions(scenarios_known, pred, prob)
    return gap_report


@router.get("/latest")
def get_latest_gap_analysis():
    # Run gap analysis on active model
    return run_gap_analysis(n_attacks=40, mutation_strength=0.60)
