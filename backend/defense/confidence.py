"""
AegisPay v2 - Confidence Estimation & Abstention Engine
Evaluates detector agreement and prediction uncertainty to trigger abstention / manual review.
"""

from typing import Dict, Any, List, Tuple
import numpy as np


class ConfidenceEstimator:
    """Estimates prediction confidence and manages the abstention channel."""

    def estimate_confidence(
        self,
        calibrated_fraud_prob: float,
        model_scores: Dict[str, float]
    ) -> Tuple[str, float, bool]:
        """
        Returns:
            confidence_level: HIGH, MEDIUM, LOW
            confidence_score: 0.0 to 1.0
            should_abstain: bool (True if uncertainty warrants human review)
        """
        # 1. Margin from decision boundary (distance from 0.50)
        margin = abs(calibrated_fraud_prob - 0.50) * 2.0  # 0.0 at 0.50, 1.0 at 0.0 or 1.0

        # 2. Inter-model agreement variance
        scores_arr = list(model_scores.values())
        var = float(np.var(scores_arr)) if len(scores_arr) > 1 else 0.0
        agreement_factor = max(0.0, 1.0 - (var * 4.0))

        # Composite confidence score
        confidence_score = float(np.clip(margin * 0.6 + agreement_factor * 0.4, 0.0, 1.0))

        if confidence_score >= 0.70:
            confidence_level = "HIGH"
            should_abstain = False
        elif confidence_score >= 0.40:
            confidence_level = "MEDIUM"
            should_abstain = False
        else:
            confidence_level = "LOW"
            should_abstain = True  # Ambiguous region -> Abstain to Review

        return confidence_level, round(confidence_score, 4), should_abstain


confidence_estimator = ConfidenceEstimator()
