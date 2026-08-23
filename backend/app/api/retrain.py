"""
Adversarial Retraining API
"""

from fastapi import APIRouter
import pandas as pd
import numpy as np

from backend.app.schemas.schemas import RetrainRequest
from backend.app.services.state_manager import system_state
from backend.evaluation.metrics import evaluate_model_performance
from backend.models.registry import global_registry

router = APIRouter(prefix="/adversarial", tags=["Retraining"])


@router.post("/retrain")
def execute_retraining(req: RetrainRequest):
    # 1. Generate base dataset
    legit_train = system_state.simulator.generate_legitimate_stream(600)
    attacks_train = system_state.generator.generate_scenarios(200, mutation_strength=0.4, difficulty="Moderate")
    attacks_known = [a for a in attacks_train if a.attack_family != "AI Adaptive Fraud"]
    all_train = legit_train + attacks_known
    np.random.shuffle(all_train)

    X_train = pd.DataFrame([t.to_feature_dict() for t in all_train])
    y_train = np.array([t.is_fraud for t in all_train])

    # 2. Run gap analysis to find evasion clusters
    adv_scenarios = system_state.generator.generate_scenarios(50, mutation_strength=0.7, difficulty="Hard")
    adv_known = [a for a in adv_scenarios if a.attack_family != "AI Adaptive Fraud"]
    df_adv = pd.DataFrame([s.to_feature_dict() for s in adv_known])

    active_model = system_state.get_active_defense()
    pred = active_model.predict(df_adv)
    prob = active_model.predict_proba(df_adv)[:, 1]

    gap_report = system_state.gap_analyzer.analyze_evasions(adv_known, pred, prob)

    # 3. Generate targeted counterexamples and train hardened model
    counterexamples = system_state.trainer.generate_targeted_counterexamples(
        gap_report["clusters"],
        n_samples=req.n_counterexamples
    )

    target_ver = req.target_version if req.target_version in ["v2.0", "v3.0"] else "v2.0"
    hardened_model = system_state.trainer.train_hardened_model(
        X_train, y_train, counterexamples, target_version=target_ver
    )

    # 4. Register and set active
    m_id = f"aegispay_{target_ver.replace('.', '_')}"
    global_registry.register(m_id, hardened_model)
    system_state.current_model_version = target_ver

    # 5. Evaluate on fresh test set
    legit_test = system_state.simulator.generate_legitimate_stream(200)
    attacks_test = system_state.generator.generate_scenarios(80, mutation_strength=0.5, difficulty="Hard")
    attacks_test_known = [a for a in attacks_test if a.attack_family != "AI Adaptive Fraud"]
    all_test = legit_test + attacks_test_known

    X_test = pd.DataFrame([t.to_feature_dict() for t in all_test])
    y_test = np.array([t.is_fraud for t in all_test])

    perf = evaluate_model_performance(hardened_model, X_test, y_test)

    return {
        "status": "success",
        "retrained_model_version": target_ver,
        "counterexamples_synthesized": len(counterexamples),
        "new_metrics": perf,
        "message": f"Successfully hardened model to {target_ver} using {len(counterexamples)} targeted counter-samples."
    }
