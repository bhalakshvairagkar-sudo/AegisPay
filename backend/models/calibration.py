"""
AegisPay v2 - Probability Calibration Engine
Applies Isotonic Regression and Platt Scaling to raw classifier outputs and evaluates Brier Score and ECE.
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression


class CalibrationEngine:
    """Calibrates raw classifier scores to output true empirical fraud-risk estimates."""

    def __init__(self, method: str = "isotonic"):
        self.method = method
        self.isotonic_calibrator: Optional[IsotonicRegression] = None
        self.platt_calibrator: Optional[LogisticRegression] = None
        self.is_fitted = False

    def fit(self, raw_scores: np.ndarray, y_true: np.ndarray) -> "CalibrationEngine":
        """Fits both Isotonic and Platt models on validation scores."""
        scores = np.asarray(raw_scores, dtype=float).clip(1e-5, 1.0 - 1e-5)
        y = np.asarray(y_true, dtype=int)

        # 1. Fit Isotonic
        self.isotonic_calibrator = IsotonicRegression(out_of_bounds="clip")
        self.isotonic_calibrator.fit(scores, y)

        # 2. Fit Platt (Logistic Regression on log-odds)
        log_odds = np.log(scores / (1.0 - scores)).reshape(-1, 1)
        self.platt_calibrator = LogisticRegression(C=1.0)
        self.platt_calibrator.fit(log_odds, y)

        self.is_fitted = True
        return self

    def predict_proba(self, raw_scores: np.ndarray) -> np.ndarray:
        """Transforms raw model scores into calibrated fraud risk estimates."""
        if not self.is_fitted:
            return np.asarray(raw_scores, dtype=float).clip(0.0, 1.0)

        scores = np.asarray(raw_scores, dtype=float).clip(1e-5, 1.0 - 1e-5)
        if self.method == "isotonic" and self.isotonic_calibrator:
            return self.isotonic_calibrator.predict(scores).clip(0.0, 1.0)
        elif self.method == "platt" and self.platt_calibrator:
            log_odds = np.log(scores / (1.0 - scores)).reshape(-1, 1)
            return self.platt_calibrator.predict_proba(log_odds)[:, 1]
        return scores

    def evaluate_calibration(self, raw_scores: np.ndarray, y_true: np.ndarray) -> Dict[str, Any]:
        """Calculates Brier Score, Expected Calibration Error (ECE), and 10-bin Reliability Curves."""
        y = np.asarray(y_true, dtype=int)
        raw_p = np.asarray(raw_scores, dtype=float).clip(0.0, 1.0)
        cal_p = self.predict_proba(raw_p)

        # Brier Score = mean((p - y)^2)
        brier_raw = float(np.mean((raw_p - y) ** 2))
        brier_cal = float(np.mean((cal_p - y) ** 2))

        # Expected Calibration Error (ECE) with 10 bins
        num_bins = 10
        bin_edges = np.linspace(0.0, 1.0, num_bins + 1)
        ece_cal = 0.0
        reliability_curve = []

        for i in range(num_bins):
            b_low, b_high = bin_edges[i], bin_edges[i + 1]
            mask = (cal_p >= b_low) & (cal_p < b_high if i < num_bins - 1 else cal_p <= b_high)
            bin_size = int(np.sum(mask))

            if bin_size > 0:
                mean_conf = float(np.mean(cal_p[mask]))
                actual_acc = float(np.mean(y[mask]))
                ece_cal += (bin_size / len(y)) * abs(mean_conf - actual_acc)
                reliability_curve.append({
                    "bin_index": i,
                    "bin_range": f"{round(b_low, 1)}-{round(b_high, 1)}",
                    "predicted_prob": round(mean_conf, 4),
                    "empirical_accuracy": round(actual_acc, 4),
                    "count": bin_size
                })
            else:
                reliability_curve.append({
                    "bin_index": i,
                    "bin_range": f"{round(b_low, 1)}-{round(b_high, 1)}",
                    "predicted_prob": round((b_low + b_high) / 2.0, 4),
                    "empirical_accuracy": 0.0,
                    "count": 0
                })

        return {
            "calibration_method": self.method,
            "brier_score_uncalibrated": round(brier_raw, 4),
            "brier_score_calibrated": round(brier_cal, 4),
            "brier_score_reduction_pct": round(max(0.0, (brier_raw - brier_cal) / max(1e-5, brier_raw)) * 100, 2),
            "expected_calibration_error": round(ece_cal, 4),
            "reliability_curve": reliability_curve
        }


calibration_engine = CalibrationEngine()
