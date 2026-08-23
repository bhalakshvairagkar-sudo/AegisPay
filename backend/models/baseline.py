"""
Baseline Fraud Detection Models
1. Rule-Based Static Heuristic Engine
2. Supervised Random Forest Classifier
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from backend.simulator.transactions import SyntheticTransaction


class RuleBasedClassifier:
    """Static payment risk heuristic rule engine."""

    def __init__(self):
        self.name = "Rule-Based Engine (Legacy)"
        self.model_type = "Static Rules"

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Evaluates heuristic rule violations returning binary probability vector."""
        probas = []
        for _, row in X.iterrows():
            score = 0.0
            if row.get("amount", 0) > 800.0:
                score += 0.35
            if row.get("velocity_1h", 0) >= 5:
                score += 0.40
            if row.get("device_familiarity", 1.0) < 0.20:
                score += 0.30
            if row.get("geo_distance_km", 0) > 500.0:
                score += 0.25
            if row.get("carrier_change_flag", 0) == 1:
                score += 0.30

            prob = min(0.99, max(0.01, score))
            probas.append([1.0 - prob, prob])
        return np.array(probas)

    def predict(self, X: pd.DataFrame, threshold: float = 0.50) -> np.ndarray:
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)


class RandomForestBaselineWrapper:
    """Supervised Random Forest Classifier Baseline."""

    def __init__(self, n_estimators: int = 100, max_depth: int = 10, seed: int = 42):
        self.name = "Random Forest Baseline"
        self.model_type = "Supervised ML"
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            class_weight="balanced",
            random_state=seed,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: np.ndarray):
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            # Fallback if not fitted
            return np.tile([0.9, 0.1], (len(X), 1))
        return self.model.predict_proba(X)

    def predict(self, X: pd.DataFrame, threshold: float = 0.50) -> np.ndarray:
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)
