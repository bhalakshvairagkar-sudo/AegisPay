"""
AegisPay v2 - Operational Analyst Capacity Evaluation Engine
Evaluates detector alerts under realistic human investigation bandwidth constraints.
"""

from typing import Dict, Any, List
import numpy as np


class OperationalCapacityEvaluator:
    """Evaluates fraud detection performance at fixed operational analyst queue capacities."""

    def __init__(
        self,
        num_analysts: int = 5,
        cases_per_analyst_per_shift: int = 40,
        shifts_per_day: int = 3
    ):
        self.num_analysts = num_analysts
        self.cases_per_shift = cases_per_analyst_per_shift
        self.shifts_per_day = shifts_per_day
        self.daily_capacity = num_analysts * cases_per_analyst_per_shift * shifts_per_day  # e.g. 600 alerts/day

    def evaluate_capacity_metrics(
        self,
        y_true: np.ndarray,
        fraud_probabilities: np.ndarray,
        daily_tx_volume: int = 50000
    ) -> Dict[str, Any]:
        """
        Computes Top-K precision, Top-K recall, and queue overflow where K = daily analyst capacity.
        """
        y = np.asarray(y_true, dtype=int)
        probs = np.asarray(fraud_probabilities, dtype=float)

        # Scale K proportionally to test dataset size
        scale_ratio = len(y) / max(1, daily_tx_volume)
        k_eval = max(5, int(self.daily_capacity * scale_ratio))

        # Sort transactions by descending risk score
        sorted_indices = np.argsort(probs)[::-1]
        top_k_indices = sorted_indices[:k_eval]

        total_actual_fraud = int(np.sum(y))
        top_k_fraud_caught = int(np.sum(y[top_k_indices]))

        top_k_precision = round((top_k_fraud_caught / max(1, k_eval)) * 100, 2)
        top_k_recall = round((top_k_fraud_caught / max(1, total_actual_fraud)) * 100, 2)

        # Generate capacity curve across varying analyst team sizes (1 to 10 analysts)
        capacity_curve = []
        for a_count in range(1, 11):
            cap = a_count * self.cases_per_shift * self.shifts_per_day
            k_step = max(5, int(cap * scale_ratio))
            sub_indices = sorted_indices[:k_step]
            caught = int(np.sum(y[sub_indices]))
            capacity_curve.append({
                "analysts_count": a_count,
                "daily_alert_capacity": cap,
                "precision_at_capacity_pct": round((caught / max(1, k_step)) * 100, 2),
                "recall_at_capacity_pct": round((caught / max(1, total_actual_fraud)) * 100, 2),
                "queue_overflow_risk": "LOW" if (caught / max(1, total_actual_fraud)) > 0.85 else "HIGH"
            })

        return {
            "operational_analyst_count": self.num_analysts,
            "daily_investigation_capacity": self.daily_capacity,
            "top_k_alerts_evaluated": k_eval,
            "actual_frauds_in_queue": total_actual_fraud,
            "frauds_caught_within_capacity": top_k_fraud_caught,
            "precision_at_analyst_capacity_pct": top_k_precision,
            "recall_at_analyst_capacity_pct": top_k_recall,
            "capacity_curve": capacity_curve
        }


capacity_evaluator = OperationalCapacityEvaluator()
