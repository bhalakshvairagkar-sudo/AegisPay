"""
AegisPay v2 - Account-to-Account (A2A) / Wire Transfer Rail
High-value corporate wire and interbank clearing rail with dual-custody verification.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.rails.base_rail import BasePaymentRail, RailPolicyAction


class A2APaymentRail(BasePaymentRail):
    def __init__(self):
        super().__init__(rail_name="A2A", allows_dispute=False, is_real_time=True)

    def get_allowed_lifecycle_states(self) -> List[str]:
        return ["INITIATED", "DUAL_CUSTODY_VERIFIED", "AUTHORIZED_INTERBANK", "SETTLED_RTGS", "REVERSED_UNMATCHED"]

    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        if risk_level == "BLOCK":
            return RailPolicyAction("BLOCK", "A2A_WIRE_SUSPEND", reason_code, 0.0)
        elif risk_level == "REVIEW":
            return RailPolicyAction("REVIEW", "A2A_TREASURY_ANALYST_QUEUE", reason_code, 40.0)
        elif risk_level == "FRICTION":
            return RailPolicyAction("FRICTION", "A2A_OUT_OF_BAND_CALLBACK", reason_code, 12.0)
        return RailPolicyAction("ALLOW", "A2A_IMMEDIATE_RELEASE", reason_code, 0.0)

    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        return True, []
