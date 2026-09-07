"""
AegisPay v2 - Payment Lifecycle Engine
Simulates realistic event chains across stages and rails.
"""

from typing import Dict, Any, List, Optional
import numpy as np

from backend.simulator.lifecycle.events import PaymentSessionLifecycle, PaymentLifecycleEvent


class PaymentLifecycleEngine:
    """Executes stateful multi-event lifecycle transitions for payment transactions."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.RandomState(seed)

    def simulate_full_lifecycle(
        self,
        transaction_id: str,
        rail: str,
        amount: float,
        is_fraud: bool = False,
        policy_action: str = "ALLOW"
    ) -> PaymentSessionLifecycle:
        """Simulates the sequence of events from initiation through settlement or dispute."""
        session = PaymentSessionLifecycle(
            session_id=f"SES-{transaction_id[:8]}",
            transaction_id=transaction_id,
            rail=rail,
            current_stage="INITIATED"
        )

        # 1. Initiation
        session.add_event("INITIATION", {
            "amount": amount,
            "rail": rail,
            "channel": "MOBILE_APP" if rail in ["UPI", "Wallet"] else "WEB_CHECKOUT"
        }, timestamp_offset_seconds=0.0)

        # 2. Authentication
        auth_duration = float(self.rng.uniform(1.2, 8.5))
        session.add_event("AUTHENTICATION", {
            "auth_method": "EMV_3DS" if rail == "Card" else ("MPIN" if rail == "UPI" else "OAUTH_BEARER"),
            "auth_status": "SUCCESS" if policy_action != "BLOCK" else "FAILED_BLOCKED"
        }, timestamp_offset_seconds=auth_duration)

        if policy_action == "BLOCK":
            return session

        # 3. Authorization
        authz_duration = auth_duration + float(self.rng.uniform(0.3, 1.5))
        session.add_event("AUTHORIZATION", {
            "authz_code": f"AUTH-{self.rng.randint(100000, 999999)}",
            "decision": policy_action
        }, timestamp_offset_seconds=authz_duration)

        # 4. Presentment / Capture (Card / Mandate)
        if rail in ["Card", "Recurring Mandate"]:
            pres_duration = authz_duration + float(self.rng.uniform(3600.0, 86400.0))  # 1-24h
            session.add_event("PRESENTMENT", {
                "batch_id": f"BATCH-{self.rng.randint(1000, 9999)}",
                "clearing_status": "MATCHED"
            }, timestamp_offset_seconds=pres_duration)
            settle_offset = pres_duration + float(self.rng.uniform(3600.0, 172800.0))  # T+1 / T+2
        else:
            settle_offset = authz_duration + float(self.rng.uniform(0.2, 2.0))  # Instant

        # 5. Settlement
        session.add_event("SETTLEMENT", {
            "settlement_rail": rail,
            "settled_amount": amount,
            "status": "COMPLETED"
        }, timestamp_offset_seconds=settle_offset)

        # 6. Dispute (if fraudulent and not blocked)
        if is_fraud and policy_action != "BLOCK":
            dispute_delay = settle_offset + float(self.rng.uniform(86400.0 * 3, 86400.0 * 30))  # 3-30 days
            session.add_event("DISPUTE", {
                "dispute_reason": "FRAUDULENT_UNAUTHORIZED_TRANSACTION",
                "dispute_stage": "FIRST_CHARGEBACK_FILED"
            }, timestamp_offset_seconds=dispute_delay)
            session.is_disputed = True

        return session


lifecycle_engine = PaymentLifecycleEngine()
