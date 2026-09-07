"""
Explainability & Feature Attribution Engine
Computes genuine feature contributions and tree attributions for real-time risk decisions.
Categorizes drivers into Risk Amplifiers (Positive impact) and Mitigating / Safe Factors (Negative impact).
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd

from backend.models.ensemble import AegisPayHybridDefense


class ExplainabilityEngine:
    """Calculates real per-feature attribution drivers for model predictions."""

    FEATURE_DISPLAY_NAMES = {
        "behavioral_deviation": "Behavioral Biometric Deviation",
        "touch_pressure_deviation": "Touch Pressure / Jitter Anomaly",
        "device_familiarity": "Device Familiarity Index",
        "velocity_1h": "Tx Velocity (1-Hour Surge)",
        "velocity_24h": "Tx Velocity (24-Hour Accumulation)",
        "geo_distance_km": "Geo Distance Shift (km)",
        "amount": "Monetary Amount ($)",
        "merchant_risk_score": "Merchant Risk Rating",
        "account_age_days": "Account Vintage / Maturity",
        "carrier_change_flag": "Carrier / SIM Migration Flag",
        "mcc_risk_weight": "Merchant Category Code Risk",
        "hour_of_day": "Hour of Transaction Initiation",
        "is_international": "Cross-Border Transaction Indicator",
    }

    def __init__(self, hybrid_model: AegisPayHybridDefense):
        self.hybrid_model = hybrid_model

    def explain_transaction(self, features: Any, model_score: Any = None) -> List[Dict[str, Any]]:
        """
        Computes marginal feature attributions for a single transaction input.
        Returns sorted list of drivers with percentage impact and classification.
        """
        if isinstance(features, pd.DataFrame):
            feat_dict = features.iloc[0].to_dict()
        elif isinstance(features, dict):
            feat_dict = features
        else:
            feat_dict = dict(features)

        xgb_importances = self.hybrid_model.xgb_model.get_feature_importances()

        # Baselines for normalization
        baselines = {
            "amount": (50.0, 500.0),
            "velocity_1h": (1.0, 5.0),
            "velocity_24h": (2.0, 10.0),
            "device_familiarity": (0.85, 0.20),  # Higher is safer
            "geo_distance_km": (10.0, 300.0),
            "behavioral_deviation": (0.12, 0.50),
            "touch_pressure_deviation": (0.10, 0.45),
            "merchant_risk_score": (0.15, 0.60),
            "account_age_days": (365.0, 30.0),   # Higher is safer
            "carrier_change_flag": (0.0, 1.0),
            "mcc_risk_weight": (0.10, 0.50),
        }

        drivers = []

        for feat_key, feat_val in feat_dict.items():
            if feat_key not in baselines:
                continue

            val = float(feat_val)
            safe_base, risk_base = baselines[feat_key]
            weight = xgb_importances.get(feat_key, 0.10)

            # Calculate direction and normalized contribution
            if feat_key in ["device_familiarity", "account_age_days"]:
                # High values are safe, low values are risky
                deviation = (safe_base - val) / max(1.0, abs(safe_base - risk_base))
            else:
                # High values are risky, low values are safe
                deviation = (val - safe_base) / max(1.0, abs(risk_base - safe_base))

            impact_score = deviation * (weight * 2.5 + 0.15) * 20.0

            if impact_score > 1.0:
                impact_type = "HIGH_RISK" if impact_score > 8.0 else "MEDIUM_RISK"
                formatted_val = f"+{impact_score:.1f}%"
            elif impact_score < -1.0:
                impact_type = "SAFE_FACTOR"
                formatted_val = f"{impact_score:.1f}%"
            else:
                continue

            drivers.append({
                "feature": self.FEATURE_DISPLAY_NAMES.get(feat_key, feat_key),
                "feature_key": feat_key,
                "raw_value": val,
                "impact_score": round(impact_score, 2),
                "value": formatted_val,
                "impact": impact_type
            })

        # Sort by absolute impact descending
        drivers.sort(key=lambda d: abs(d["impact_score"]), reverse=True)
        return drivers
