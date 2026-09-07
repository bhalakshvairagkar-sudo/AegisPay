"""
AegisPay v2 - Pre-ML Structural Guards
Model-independent safety gate that intercepts and blocks physically/legally impossible transactions before ML inference.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class StructuralGuardResult:
    is_blocked_by_guard: bool
    guard_id: Optional[str] = None
    reason_code: Optional[str] = None
    explanation: Optional[str] = None


class StructuralGuardEngine:
    """Evaluates hard business and security guardrails prior to machine learning scoring."""

    def evaluate_transaction(self, tx_dict: Dict[str, Any]) -> StructuralGuardResult:
        amt = float(tx_dict.get("amount", 0.0))
        rail = tx_dict.get("rail", "Card")
        v1 = float(tx_dict.get("velocity_1h", 1.0))
        geo_km = float(tx_dict.get("geo_distance_km", 0.0))

        # Guard 1: Extreme regulatory ceiling breach
        if amt > 250000.0:
            return StructuralGuardResult(
                is_blocked_by_guard=True,
                guard_id="GUARD-01",
                reason_code="R17",  # Regulatory limit exceeded
                explanation="Transaction amount strictly exceeds maximum allowed statutory clearing limit."
            )

        # Guard 2: Negative or zero ticket
        if amt <= 0.0:
            return StructuralGuardResult(
                is_blocked_by_guard=True,
                guard_id="GUARD-02",
                reason_code="R05",  # Unusual amount
                explanation="Negative or zero ticket amount rejected by structural guard."
            )

        # Guard 3: Impossible physical velocity (Mach 2 displacement)
        if geo_km > 5000.0 and v1 > 10.0:
            return StructuralGuardResult(
                is_blocked_by_guard=True,
                guard_id="GUARD-03",
                reason_code="R06",  # Geographic deviation
                explanation="Haversine displacement combined with burst velocity exceeds physical supersonic transit limits."
            )

        # Guard 4: Extreme bot velocity flood
        if v1 > 50.0:
            return StructuralGuardResult(
                is_blocked_by_guard=True,
                guard_id="GUARD-04",
                reason_code="R03",  # Abnormal velocity
                explanation="Transaction frequency exceeds human interface thresholds (50+ tx/hr)."
            )

        return StructuralGuardResult(is_blocked_by_guard=False)


structural_guards = StructuralGuardEngine()
