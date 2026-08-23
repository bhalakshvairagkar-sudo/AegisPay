"""
Attack Generation & Simulation API
"""

from fastapi import APIRouter
import pandas as pd
import numpy as np

from backend.app.schemas.schemas import AttackGenerationRequest, AttackGenerationResponse, ScenarioOutput
from backend.app.services.state_manager import system_state

router = APIRouter(prefix="/attacks", tags=["Attacks"])


@router.post("/generate", response_model=AttackGenerationResponse)
def generate_attacks(req: AttackGenerationRequest):
    # 1. Generate real scenarios
    scenarios = system_state.generator.generate_scenarios(
        count=req.count,
        family_filter=req.family_filter,
        sophistication_target=req.sophistication,
        mutation_strength=req.mutation_strength,
        difficulty=req.difficulty
    )

    df = pd.DataFrame([s.to_feature_dict() for s in scenarios])

    # 2. Evaluate with actual models from registry
    v1_model = system_state.get_model("aegispay_v1")
    v2_model = system_state.get_model("aegispay_v2")
    v3_model = system_state.get_model("aegispay_v3")

    pred_v1 = v1_model.predict(df) if v1_model else np.zeros(len(df), dtype=int)
    pred_v2 = v2_model.predict(df) if v2_model else pred_v1
    pred_v3 = v3_model.predict(df) if v3_model else pred_v2

    eval_v1 = v1_model.evaluate_risk(df) if v1_model else []

    scenario_outputs = []
    for idx, s in enumerate(scenarios):
        det_v1 = bool(pred_v1[idx] == 1)
        det_v2 = bool(pred_v2[idx] == 1)
        det_v3 = bool(pred_v3[idx] == 1)
        risk_score = eval_v1[idx]["unified_risk_score"] if idx < len(eval_v1) else None

        # Format output object to match frontend interface
        scenario_outputs.append(ScenarioOutput(
            scenarioId=s.txn_id,
            attackId=s.attack_id,
            family=s.attack_family,
            name=s.attack_name,
            genAi=s.gen_ai,
            amount=s.amount,
            velocity=s.velocity_1h,
            deviceFam=s.device_familiarity,
            locationDev=s.geo_distance_km,
            bioVariance=s.behavioral_deviation,
            difficulty=s.difficulty,
            mutatedScore=round(s.behavioral_deviation * 10, 1),
            detected_v1=det_v1,
            detected_v2=det_v2,
            detected_v3=det_v3,
            evadedInV1=not det_v1,
            evadedInV3=not det_v3,
            riskScore=risk_score
        ))

    evasion_rate_v1 = round((sum(1 for s in scenario_outputs if s.evadedInV1) / max(1, len(scenario_outputs))) * 100.0, 1)
    evasion_rate_v3 = round((sum(1 for s in scenario_outputs if s.evadedInV3) / max(1, len(scenario_outputs))) * 100.0, 1)

    logs = [
        f"Initialized Red Team Adversarial Generator with seed {system_state.seed}.",
        f"Generated {len(scenarios)} synthetic payment scenarios across family: {req.family_filter}.",
        f"Applied mutation vector scale: {int(req.mutation_strength * 100)}%.",
        f"Evaluated scenarios against Blue Team models (v1.0 Evasion: {evasion_rate_v1}%, v3.0 Evasion: {evasion_rate_v3}%)."
    ]

    return AttackGenerationResponse(
        scenarios=scenario_outputs,
        logs=logs,
        total_generated=len(scenarios),
        evasion_rate_v1=evasion_rate_v1,
        evasion_rate_v3=evasion_rate_v3
    )
