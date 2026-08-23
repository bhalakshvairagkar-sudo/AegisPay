"""
Isolation Forest Unsupervised Anomaly Model
Trained strictly on legitimate cardholder behavioral streams (zero fraud label leakage).
Detects out-of-distribution biometric, velocity, and geographical anomalies.
"""

from typing import Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class IsolationForestAnomalyDetector:
    """Unsupervised Isolation Forest for behavioral anomaly scoring."""

    def __init__(self, n_estimators: int = 100, contamination: float = 0.05, seed: int = 42):
        self.name = "Isolation Forest (Unsupervised)"
        self.model_type = "Anomaly Detection"
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=seed,
            n_jobs=-1
        )
        self.is_fitted = False

    def fit(self, X_legit: pd.DataFrame):
        """Fits strictly on legitimate baseline feature vectors."""
        X_scaled = self.scaler.fit_transform(X_legit)
        self.model.fit(X_scaled)
        self.is_fitted = True
        return self

    def score_samples(self, X: pd.DataFrame) -> np.ndarray:
        """
        Returns normalized anomaly score in [0.0, 1.0].
        Higher score = more anomalous / out-of-distribution.
        """
        if not self.is_fitted:
            return np.full(len(X), 0.1)
        X_scaled = self.scaler.transform(X)
        # raw decision_function: lower is more anomalous (negative for outliers)
        raw_scores = self.model.decision_function(X_scaled)
        # Normalize to 0 (normal) to 1 (highly anomalous)
        # Typically raw scores lie in [-0.3, 0.3]
        norm_scores = 1.0 / (1.0 + np.exp(raw_scores * 8.0))
        return np.clip(norm_scores, 0.01, 0.99)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        scores = self.score_samples(X)
        return np.column_stack([1.0 - scores, scores])

    def predict(self, X: pd.DataFrame, threshold: float = 0.60) -> np.ndarray:
        scores = self.score_samples(X)
        return (scores >= threshold).astype(int)
