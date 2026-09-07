"""
AegisPay v2 - UPI Payment Rail
Real-time instant payment push rail with VPA routing, dynamic QR, and cooling-off directives.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.rails.base_rail import BasePaymentRail, RailPolicyAction


class UPIPaymentRail(BasePaymentRail):
    def __init__(self):
        super().__init__(rail_name="UPI", allows_dispute=True, is_real_time=True)

    def get_allowed_lifecycle_states(self) -> List[str]:
        return ["INITIATED", "AUTHENTICATED_MPIN", "AUTHORIZED", "SETTLED_INSTANT", "DISPUTED_CHARGEBACK"]

    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        if risk_level == "BLOCK":
            return RailPolicyAction("BLOCK", "UPI_SILENT_REJECT", reason_code, 0.0)
        elif risk_level == "REVIEW":
            return RailPolicyAction("REVIEW", "UPI_COOLING_OFF_4H_HOLD", reason_code, 15.0)
        elif risk_level == "FRICTION":
            return RailPolicyAction("FRICTION", "UPI_STEP_UP_BIOMETRIC", reason_code, 5.0)
        return RailPolicyAction("ALLOW", "UPI_INSTANT_CLEAR", reason_code, 0.0)

    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errs = []
        if float(tx_dict.get("amount", 0.0)) > 100000.0:  # ₹100,000 / $10,000 UPI limit
            errs.append("UPI Error: Amount exceeds per-transaction statutory regulatory ceiling.")
        return len(errs) == 0, errs
