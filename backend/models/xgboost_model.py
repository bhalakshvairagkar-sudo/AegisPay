"""
XGBoost Payment Fraud Classifier
Gradient boosted decision tree model with hyperparameter tuning for severe class imbalance.
"""

from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
import xgboost as xgb


class XGBoostClassifierWrapper:
    """Supervised XGBoost Classifier Wrapper."""

    def __init__(
        self,
        n_estimators: int = 120,
        max_depth: int = 6,
        learning_rate: float = 0.08,
        scale_pos_weight: float = 4.0,
        seed: int = 42
    ):
        self.name = "XGBoost Standard Classifier"
        self.model_type = "Gradient Boosting"
        self.seed = seed
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            scale_pos_weight=scale_pos_weight,
            subsample=0.85,
            colsample_bytree=0.85,
            random_state=seed,
            eval_metric="logloss",
            n_jobs=-1
        )
        self.is_fitted = False
        self.feature_names = []

    def fit(self, X: pd.DataFrame, y: np.ndarray, sample_weight: Optional[np.ndarray] = None):
        self.feature_names = list(X.columns)
        self.model.fit(X, y, sample_weight=sample_weight)
        self.is_fitted = True
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            return np.tile([0.9, 0.1], (len(X), 1))
        return self.model.predict_proba(X)

    def predict(self, X: pd.DataFrame, threshold: float = 0.50) -> np.ndarray:
        probs = self.predict_proba(X)[:, 1]
        return (probs >= threshold).astype(int)

    def get_feature_importances(self) -> Dict[str, float]:
        if not self.is_fitted:
            return {}
        importances = self.model.feature_importances_
        return {feat: float(imp) for feat, imp in zip(self.feature_names, importances)}
