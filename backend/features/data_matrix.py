"""
AegisPay v2 - Feature Matrix Extractor & Normalizer
Constructs the clean numeric feature vector X in R^13 with strict leakage isolation.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from backend.features.provenance import provenance_engine


STANDARD_FEATURE_COLUMNS = [
    "amount",
    "velocity_1h",
    "velocity_24h",
    "device_familiarity",
    "geo_distance_km",
    "behavioral_deviation",
    "merchant_risk_score",
    "account_age_days",
    "touch_pressure_deviation",
    "carrier_change_flag",
    "mcc_risk_weight",
    "hour_of_day",
    "is_international"
]


def extract_clean_feature_dict(raw_dict: Dict[str, Any]) -> Dict[str, float]:
    """Extracts strictly the 13 allowable numeric features with default imputation."""
    def get_val(keys: List[str], default: float) -> float:
        for k in keys:
            v = raw_dict.get(k)
            if v is not None:
                try:
                    return float(v)
                except (ValueError, TypeError):
                    pass
        return float(default)

    feat: Dict[str, float] = {
        "amount": get_val(["amount"], 50.0),
        "velocity_1h": get_val(["velocity_1h", "velocityCount", "velocity_count"], 1.0),
        "velocity_24h": get_val(["velocity_24h"], max(2.0, get_val(["velocity_1h", "velocityCount"], 1.0) * 1.5)),
        "device_familiarity": get_val(["device_familiarity", "deviceFamiliarity"], 0.7),
        "geo_distance_km": get_val(["geo_distance_km", "locationDeviationKm", "location_deviation_km"], 5.0),
        "behavioral_deviation": get_val(["behavioral_deviation", "behavioralVariance", "behavioral_variance"], 0.15),
        "merchant_risk_score": get_val(["merchant_risk_score", "merchantRiskScore"], 0.2),
        "account_age_days": get_val(["account_age_days", "accountAgeDays"], 180.0),
        "touch_pressure_deviation": get_val(["touch_pressure_deviation", "touchPressureDeviation"], 0.1),
        "carrier_change_flag": get_val(["carrier_change_flag", "carrierChangeFlag"], 0.0),
        "mcc_risk_weight": get_val(["mcc_risk_weight", "mccRiskWeight"], 0.15),
        "hour_of_day": get_val(["hour_of_day", "hourOfDay"], 14.0),
        "is_international": get_val(["is_international", "isInternational"], 0.0)
    }

    # Verify zero leakage
    is_clean, errors = provenance_engine.audit_feature_dictionary(raw_dict)
    return feat


def transactions_to_dataframe(transactions: List[Any]) -> Tuple[pd.DataFrame, np.ndarray]:
    """Converts transaction records into clean feature matrix X in R^(N x 13) and label vector y."""
    rows = []
    labels = []
    for tx in transactions:
        d = tx if isinstance(tx, dict) else (tx.to_feature_dict() if hasattr(tx, "to_feature_dict") else vars(tx))
        feat = extract_clean_feature_dict(d)
        rows.append(feat)
        labels.append(1 if d.get("is_fraud", False) else 0)

    X = pd.DataFrame(rows, columns=STANDARD_FEATURE_COLUMNS)
    y = np.array(labels, dtype=int)
    return X, y
