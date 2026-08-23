"""
Real-time Transaction Risk Inference & SHAP Explainability API
"""

from fastapi import APIRouter
import pandas as pd

from backend.app.schemas.schemas import TransactionInput, PredictionResponse, FeatureDriver
from backend.app.services.state_manager import system_state

router = APIRouter(tags=["Inference"])


@router.post("/predict", response_model=PredictionResponse)
def predict_transaction(txn: TransactionInput):
    # Normalize input fields
    features = {
        "amount": txn.amount,
        "velocity_1h": txn.velocityCount if txn.velocity_1h is None else txn.velocity_1h,
        "velocity_24h": txn.velocity_24h if txn.velocity_24h is not None else (txn.velocityCount * 2),
        "device_familiarity": txn.deviceFamiliarity if txn.device_familiarity is None else txn.device_familiarity,
        "geo_distance_km": txn.locationDeviationKm if txn.geo_distance_km is None else txn.geo_distance_km,
        "behavioral_deviation": txn.behavioralVariance if txn.behavioral_deviation is None else txn.behavioral_deviation,
        "merchant_risk_score": txn.merchantRiskScore if txn.merchant_risk_score is None else txn.merchant_risk_score,
        "account_age_days": txn.accountAgeDays if txn.account_age_days is None else txn.account_age_days,
        "touch_pressure_deviation": txn.touch_pressure_deviation or 0.20,
        "carrier_change_flag": txn.carrier_change_flag or 0,
        "mcc_risk_weight": txn.mcc_risk_weight or 0.20,
        "hour_of_day": txn.hour_of_day or 14,
        "is_international": txn.is_international or 0,
    }

    df = pd.DataFrame([features])
    active_model = system_state.get_active_defense()

    # 1. Real Risk Evaluation
    eval_res = active_model.evaluate_risk(df)[0]

    # 2. Real SHAP / Feature Attribution Explanations
    explainer = system_state.get_explainability_engine()
    shap_drivers_raw = explainer.explain_transaction(features)

    shap_drivers = [
        FeatureDriver(
            feature=d["feature"],
            feature_key=d["feature_key"],
            value=d["value"],
            impact=d["impact"],
            raw_value=d["raw_value"],
            impact_score=d["impact_score"]
        )
        for d in shap_drivers_raw
    ]

    return PredictionResponse(
        unifiedRiskScore=eval_res["unified_risk_score"],
        supervisedMlRisk=eval_res["supervised_ml_risk"],
        anomalyScore=eval_res["anomaly_score"],
        ruleRisk=eval_res["rule_risk"],
        behavioralVariance=eval_res["behavioral_variance"],
        decision=eval_res["decision"],
        decisionColor=eval_res["decision_color"],
        modelVersion=active_model.version,
        shapDrivers=shap_drivers,
        is_live_prediction=True
    )
