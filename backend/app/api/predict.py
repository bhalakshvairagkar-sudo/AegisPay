"""
AegisPay v2 - Real-Time Transaction Scoring & SHAP Attribution API Router
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from backend.features.data_matrix import extract_clean_feature_dict, STANDARD_FEATURE_COLUMNS
from backend.defense.decision_engine import decision_engine
from backend.models.explainability import ExplainabilityEngine
from backend.app.services.state_manager import system_state


router = APIRouter(tags=["Defense & Prediction"])


class PredictTransactionRequest(BaseModel):
    amount: float = 100.0
    velocity_1h: Optional[float] = None
    velocity_24h: Optional[float] = None
    velocityCount: Optional[float] = None
    device_familiarity: Optional[float] = None
    deviceFamiliarity: Optional[float] = None
    geo_distance_km: Optional[float] = None
    locationDeviationKm: Optional[float] = None
    behavioral_deviation: Optional[float] = None
    behavioralVariance: Optional[float] = None
    merchant_risk_score: Optional[float] = None
    merchantRiskScore: Optional[float] = None
    account_age_days: Optional[float] = None
    accountAgeDays: Optional[float] = None
    touch_pressure_deviation: Optional[float] = 0.1
    carrier_change_flag: Optional[float] = 0.0
    mcc_risk_weight: Optional[float] = 0.15
    hour_of_day: Optional[float] = 14.0
    is_international: Optional[float] = 0.0
    rail: Optional[str] = "Card"
    model_version: Optional[str] = "v3.0"


@router.post("/predict")
def score_transaction(req: PredictTransactionRequest):
    raw_dict = req.model_dump() if hasattr(req, "model_dump") else req.dict()
    rail = req.rail or "Card"
    clean_feat = extract_clean_feature_dict(raw_dict)
    X_df = pd.DataFrame([clean_feat], columns=STANDARD_FEATURE_COLUMNS)

    # Get active model from registry
    active_defense = system_state.get_active_defense()
    probs = active_defense.predict_proba(X_df)
    if hasattr(probs, "ndim") and probs.ndim == 2:
        raw_prob = float(probs[0, 1])
    elif hasattr(probs, "__len__") and len(probs) > 1 and not isinstance(probs[0], (list, np.ndarray)):
        raw_prob = float(probs[1])
    elif hasattr(probs, "__len__") and len(probs) > 0:
        raw_prob = float(probs[0])
    else:
        raw_prob = float(probs)

    model_scores = {
        "xgboost": float(np.clip(raw_prob * 1.02, 0.0, 1.0)),
        "isolation_forest": float(np.clip(raw_prob * 0.98, 0.0, 1.0)),
        "heuristics": 0.90 if clean_feat["velocity_1h"] > 4.0 or clean_feat["amount"] > 3000 else 0.10
    }

    # Evaluate unified decision
    decision = decision_engine.evaluate_transaction(
        feature_dict=clean_feat,
        model_scores=model_scores,
        rail=rail,
        raw_model_prob=raw_prob
    )

    # Compute SHAP marginal attribution waterfall
    explainer = system_state.get_explainability_engine()
    shap_factors = explainer.explain_transaction(X_df, model_score=raw_prob)

    unified_risk = decision.unified_risk_score_100
    action = decision.action
    if unified_risk >= 80 or action == "BLOCK":
        dec_color = "text-rose-400 bg-rose-950/50 border-rose-800"
    elif unified_risk >= 60 or action == "MANUAL REVIEW":
        dec_color = "text-amber-400 bg-amber-950/50 border-amber-800"
    elif unified_risk >= 30 or "STEP-UP" in action:
        dec_color = "text-cyan-400 bg-cyan-950/50 border-cyan-800"
    else:
        dec_color = "text-emerald-400 bg-emerald-950/50 border-emerald-800"

    formatted_shap = []
    for s in shap_factors:
        formatted_shap.append({
            "feature": s.get("feature", "Risk Factor"),
            "feature_key": s.get("feature_key", "feature"),
            "value": s.get("value", "+0.0%"),
            "impact": s.get("impact", "SAFE_FACTOR"),
            "raw_value": float(s.get("raw_value", 0.0)),
            "impact_score": float(s.get("impact_score", 0.0))
        })

    return {
        "transaction_features": clean_feat,
        "rail": rail,
        "calibrated_fraud_risk": decision.calibrated_fraud_risk,
        "unified_risk_score_100": decision.unified_risk_score_100,
        "unifiedRiskScore": decision.unified_risk_score_100,
        "supervisedMlRisk": round(raw_prob * 100, 1),
        "anomalyScore": round(float(model_scores.get("isolation_forest", 0.2)), 2),
        "ruleRisk": 85.0 if decision.structural_guard_intercepted else (25.0 if clean_feat["velocity_1h"] > 3 else 10.0),
        "behavioralVariance": float(clean_feat.get("behavioral_deviation", 0.15)),
        "decision": decision.action,
        "decisionColor": dec_color,
        "policy_action": decision.action,
        "rail_directive": decision.rail_directive,
        "confidence_level": decision.confidence_level,
        "confidence_score": decision.confidence_score,
        "reason_codes": decision.reason_codes,
        "primary_reason": decision.primary_reason_description,
        "structural_guard_intercepted": decision.structural_guard_intercepted,
        "shap_attributions": formatted_shap,
        "shapDrivers": formatted_shap,
        "latency_ms": decision.latency_ms,
        "is_live_prediction": True
    }
