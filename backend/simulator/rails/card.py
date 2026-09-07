"""
AegisPay v2 - Card Payment Rail (Card-Not-Present / Card-Present)
Dual-message authorization, presentment/capture, and clearing rail with EMV 3D-Secure step-up.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.rails.base_rail import BasePaymentRail, RailPolicyAction


class CardPaymentRail(BasePaymentRail):
    def __init__(self):
        super().__init__(rail_name="Card", allows_dispute=True, is_real_time=False)

    def get_allowed_lifecycle_states(self) -> List[str]:
        return ["INITIATED", "AUTHENTICATED_3DS", "PRE_AUTHORIZED", "CAPTURED_PRESENTED", "SETTLED_CLEARING", "CHARGEBACK_LODGED"]

    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        if risk_level == "BLOCK":
            return RailPolicyAction("BLOCK", "CARD_HARD_DECLINE_05", reason_code, 0.0)
        elif risk_level == "REVIEW":
            return RailPolicyAction("REVIEW", "CARD_MANUAL_FRAUD_HOLD", reason_code, 25.0)
        elif risk_level == "FRICTION":
            return RailPolicyAction("FRICTION", "CARD_MANDATORY_EMV_3DS_CHALLENGE", reason_code, 3.5)
        return RailPolicyAction("ALLOW", "CARD_FRICTIONLESS_AUTHORIZE", reason_code, 0.0)

    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errs = []
        if float(tx_dict.get("amount", 0.0)) <= 0.0:
            errs.append("Card Error: Transaction amount must be positive.")
        return len(errs) == 0, errs
