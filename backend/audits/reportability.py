"""
AegisPay v2 - Reportability & Sample Size Protection Guard
Prevents underpowered sample evaluations from generating deceptive 100% headline metrics.
"""

from typing import Dict, Any, Tuple


class ReportabilityGuard:
    """Enforces minimum statistical power constraints before metrics can be marked REPORTABLE."""

    MIN_TOTAL_SAMPLES = 100
    MIN_POSITIVE_SAMPLES = 25

    @classmethod
    def check_reportability(cls, total_samples: int, positive_samples: int) -> Tuple[bool, str]:
        if total_samples < cls.MIN_TOTAL_SAMPLES:
            return False, f"NOT REPORTABLE: Insufficient total sample size (N={total_samples} < {cls.MIN_TOTAL_SAMPLES})."
        if positive_samples < cls.MIN_POSITIVE_SAMPLES:
            return False, f"NOT REPORTABLE: Insufficient positive fraud samples (Positives={positive_samples} < {cls.MIN_POSITIVE_SAMPLES})."
        return True, "REPORTABLE: Statistical power requirements satisfied."
