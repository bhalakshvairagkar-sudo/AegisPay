"""
AegisPay v2 - Recurring Mandate / Standing Order Rail
Auto-debit mandate registration, recurring execution, and e-NACH/SEPA direct debit lifecycle.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.rails.base_rail import BasePaymentRail, RailPolicyAction


class RecurringMandateRail(BasePaymentRail):
    def __init__(self):
        super().__init__(rail_name="Recurring Mandate", allows_dispute=True, is_real_time=False)

    def get_allowed_lifecycle_states(self) -> List[str]:
        return ["MANDATE_INITIATED", "MANDATE_AUTHENTICATED", "MANDATE_REGISTERED_ACTIVE", "EXECUTION_PRESENTED", "SETTLED_DEBIT", "MANDATE_REVOKED"]

    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        if risk_level == "BLOCK":
            return RailPolicyAction("BLOCK", "MANDATE_REFUSE_REGISTRATION", reason_code, 0.0)
        elif risk_level == "REVIEW":
            return RailPolicyAction("REVIEW", "MANDATE_PAUSE_FOR_CUSTOMER_CONFIRMATION", reason_code, 10.0)
        elif risk_level == "FRICTION":
            return RailPolicyAction("FRICTION", "MANDATE_REQUIRE_NETBANKING_AUTH", reason_code, 4.0)
        return RailPolicyAction("ALLOW", "MANDATE_REGISTER_AND_EXECUTE", reason_code, 0.0)

    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        return True, []
