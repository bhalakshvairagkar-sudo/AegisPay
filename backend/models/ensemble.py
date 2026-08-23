"""
AegisPay Hybrid Defense Ensemble
Combines:
1. Supervised XGBoost Gradient Boosted Classifier (Probability)
2. Unsupervised Isolation Forest (Anomaly Outlier Score)
3. Direct Behavioral Biometric Variance
4. Multi-Window Velocity Dynamics
5. Policy Decision Engine (ALLOW, STEP-UP 3DS, MANUAL REVIEW, BLOCK)
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd

from backend.models.xgboost_model import XGBoostClassifierWrapper
from backend.models.anomaly_model import IsolationForestAnomalyDetector
from backend.models.baseline import RuleBasedClassifier


class AegisPayHybridDefense:
    """Multi-layer hybrid payment fraud defense architecture."""

    def __init__(
        self,
        version: str = "v1.0",
        xgb_weight: float = 0.55,
        anomaly_weight: float = 0.25,
        rule_weight: float = 0.10,
        behavior_weight: float = 0.10,
        seed: int = 42
    ):
        self.version = version
        self.name = f"AegisPay Defense {version}"
        self.model_type = "Hybrid Adversarial Ensemble" if version != "v1.0" else "Hybrid Ensemble"
        self.seed = seed

        self.xgb_weight = xgb_weight
        self.anomaly_weight = anomaly_weight
        self.rule_weight = rule_weight
        self.behavior_weight = behavior_weight

        self.xgb_model = XGBoostClassifierWrapper(seed=seed)
        self.anomaly_model = IsolationForestAnomalyDetector(seed=seed)
        self.rule_model = RuleBasedClassifier()
        self.is_fitted = False

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray, sample_weight: Optional[np.ndarray] = None):
        """Fits supervised XGBoost on full labeled set and Isolation Forest on legitimate slice."""
        # Train XGBoost
        self.xgb_model.fit(X_train, y_train, sample_weight=sample_weight)

        # Train Isolation Forest on legitimate transactions only (zero fraud label leakage)
        legit_mask = (y_train == 0)
        X_legit = X_train[legit_mask]
        if len(X_legit) > 20:
            self.anomaly_model.fit(X_legit)
        else:
            self.anomaly_model.fit(X_train)

        self.is_fitted = True
        return self

    def evaluate_risk(self, X: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Calculates Unified Risk Score (0-100), sub-scores, and policy decision for each record.
        """
        results = []
        xgb_probs = self.xgb_model.predict_proba(X)[:, 1]
        anomaly_scores = self.anomaly_model.score_samples(X)
        rule_probs = self.rule_model.predict_proba(X)[:, 1]

        for idx, (_, row) in enumerate(X.iterrows()):
            xgb_p = float(xgb_probs[idx])
            anom_s = float(anomaly_scores[idx])
            rule_p = float(rule_probs[idx])
            bio_dev = float(row.get("behavioral_deviation", 0.1))
            touch_dev = float(row.get("touch_pressure_deviation", 0.1))
            combined_bio = (bio_dev + touch_dev) / 2.0

            # Compute combined unified score [0.0 - 1.0]
            raw_unified = (
                self.xgb_weight * xgb_p +
                self.anomaly_weight * anom_s +
                self.rule_weight * rule_p +
                self.behavior_weight * combined_bio
            )

            # Scale to 0 - 100 integer
            unified_risk = int(np.clip(round(raw_unified * 100), 1, 99))

            # Policy Action Classification
            if unified_risk >= 80:
                decision = "BLOCK"
                decision_color = "text-rose-400 bg-rose-950/50 border-rose-800"
            elif unified_risk >= 60:
                decision = "MANUAL REVIEW"
                decision_color = "text-amber-400 bg-amber-950/50 border-amber-800"
            elif unified_risk >= 30:
                decision = "STEP-UP 3DS VERIFY"
                decision_color = "text-cyan-400 bg-cyan-950/50 border-cyan-800"
            else:
                decision = "ALLOW"
                decision_color = "text-emerald-400 bg-emerald-950/50 border-emerald-800"

            results.append({
                "unified_risk_score": unified_risk,
                "supervised_ml_risk": round(xgb_p * 100, 1),
                "anomaly_score": round(anom_s, 3),
                "rule_risk": round(rule_p * 100, 1),
                "behavioral_variance": round(combined_bio, 3),
                "decision": decision,
                "decision_color": decision_color,
                "model_version": self.version
            })

        return results

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Returns unified fraud probability vector for standard metric evaluation."""
        evals = self.evaluate_risk(X)
        probs = [e["unified_risk_score"] / 100.0 for e in evals]
        return np.column_stack([1.0 - np.array(probs), probs])

    def predict(self, X: pd.DataFrame, threshold: float = 0.50) -> np.ndarray:
        """Returns binary classification decision (1 if fraud/block, 0 otherwise)."""
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)
