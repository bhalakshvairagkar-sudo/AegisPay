"""
AegisPay v2 - Stored-Value Digital Wallet Rail
Closed-loop and semi-closed digital wallet top-up and peer transfer rail.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.rails.base_rail import BasePaymentRail, RailPolicyAction


class WalletPaymentRail(BasePaymentRail):
    def __init__(self):
        super().__init__(rail_name="Wallet", allows_dispute=True, is_real_time=True)

    def get_allowed_lifecycle_states(self) -> List[str]:
        return ["INITIATED", "PIN_CONFIRMED", "AUTHORIZED_STORED_VALUE", "SETTLED_WALLET_LEDGER", "DISPUTE_LODGED"]

    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        if risk_level == "BLOCK":
            return RailPolicyAction("BLOCK", "WALLET_FREEZE_ACCOUNT", reason_code, 0.0)
        elif risk_level == "REVIEW":
            return RailPolicyAction("REVIEW", "WALLET_LIMIT_WITHDRAWAL_HOLD", reason_code, 8.0)
        elif risk_level == "FRICTION":
            return RailPolicyAction("FRICTION", "WALLET_SMS_CHALLENGE", reason_code, 2.0)
        return RailPolicyAction("ALLOW", "WALLET_INSTANT_CREDIT", reason_code, 0.0)

    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        return True, []
