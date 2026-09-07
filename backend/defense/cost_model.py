"""
AegisPay v2 - Cost Matrix & Expected Loss Optimization Engine
Computes expected financial and operational loss given policy threshold allocations.
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class CostParameters:
    cost_false_negative_multiplier: float = 1.00  # 100% of ticket amount lost
    cost_false_positive_fixed: float = 15.00  # Customer dissatisfaction & interchange loss ($15)
    cost_manual_review_fixed: float = 8.50  # Analyst operational labor cost ($8.50 per ticket)
    cost_friction_abandonment_fixed: float = 3.20  # Cart abandonment friction cost ($3.20)
    customer_lifetime_value_baseline: float = 450.00


class CostOptimizationEngine:
    """Evaluates expected operational loss across decision threshold policies."""

    def __init__(self, params: Optional[CostParameters] = None):
        self.params = params or CostParameters()

    def compute_expected_loss(
        self,
        y_true: np.ndarray,
        predicted_actions: List[str],  # ALLOW, FRICTION, REVIEW, BLOCK
        ticket_amounts: np.ndarray
    ) -> Dict[str, Any]:
        """Calculates exact financial and operational loss incurred under the policy."""
        y = np.asarray(y_true, dtype=int)
        amts = np.asarray(ticket_amounts, dtype=float)

        fn_count = 0
        fn_loss = 0.0
        fp_count = 0
        fp_loss = 0.0
        review_count = 0
        review_loss = 0.0
        friction_count = 0
        friction_loss = 0.0

        for i, act in enumerate(predicted_actions):
            is_fraud = (y[i] == 1)
            amt = amts[i]

            if act == "ALLOW":
                if is_fraud:
                    fn_count += 1
                    fn_loss += amt * self.params.cost_false_negative_multiplier
            elif act == "BLOCK":
                if not is_fraud:
                    fp_count += 1
                    fp_loss += self.params.cost_false_positive_fixed
            elif act == "REVIEW":
                review_count += 1
                review_loss += self.params.cost_manual_review_fixed
                if is_fraud:
                    pass  # Caught in review
                else:
                    pass  # Small delay
            elif act == "FRICTION":
                friction_count += 1
                friction_loss += self.params.cost_friction_abandonment_fixed

        total_loss = fn_loss + fp_loss + review_loss + friction_loss
        total_tx = max(1, len(y))

        return {
            "total_expected_loss_usd": round(total_loss, 2),
            "expected_loss_per_transaction": round(total_loss / total_tx, 4),
            "false_negative_loss_usd": round(fn_loss, 2),
            "false_negative_count": fn_count,
            "false_positive_loss_usd": round(fp_loss, 2),
            "false_positive_count": fp_count,
            "manual_review_cost_usd": round(review_loss, 2),
            "manual_review_count": review_count,
            "friction_cost_usd": round(friction_loss, 2),
            "friction_count": friction_count,
            "cost_parameters": {
                "c_fn_multiplier": self.params.cost_false_negative_multiplier,
                "c_fp_fixed": self.params.cost_false_positive_fixed,
                "c_review_fixed": self.params.cost_manual_review_fixed,
                "c_friction_fixed": self.params.cost_friction_abandonment_fixed
            }
        }


cost_engine = CostOptimizationEngine()
