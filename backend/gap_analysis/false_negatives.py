"""
AegisPay v2 - False Negative Extraction & Deduplication
Isolates undetected adversarial transactions (y=1, y_hat=0) and normalizes feature vectors.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class FalseNegativeExtractor:
    """Extracts and normalizes false negative evasions for downstream failure clustering."""

    def __init__(self):
        self.scaler = StandardScaler()

    def extract_false_negatives(
        self,
        X_df: pd.DataFrame,
        y_true: np.ndarray,
        y_pred_actions: List[str],  # ALLOW, FRICTION, REVIEW, BLOCK
        raw_scenarios: Optional[List[Any]] = None
    ) -> Tuple[pd.DataFrame, np.ndarray, List[Dict[str, Any]]]:
        """
        Extracts false negatives where y_true == 1 and predicted action in ['ALLOW', 'FRICTION'].
        """
        y = np.asarray(y_true, dtype=int)
        fn_indices = []

        for i, act in enumerate(y_pred_actions):
            if y[i] == 1 and act in ["ALLOW", "FRICTION"]:
                fn_indices.append(i)

        if not fn_indices:
            return pd.DataFrame(), np.array([]), []

        fn_df = X_df.iloc[fn_indices].copy().reset_index(drop=True)
        fn_norm = self.scaler.fit_transform(fn_df)

        raw_records = []
        if raw_scenarios:
            for idx in fn_indices:
                if idx < len(raw_scenarios):
                    raw_records.append(raw_scenarios[idx])

        return fn_df, fn_norm, raw_records


fn_extractor = FalseNegativeExtractor()
