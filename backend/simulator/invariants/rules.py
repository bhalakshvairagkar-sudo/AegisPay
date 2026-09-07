"""
AegisPay v2 - Categorized Semantic Invariants
Defines formal semantic invariant rules across Temporal, Identity, Lifecycle, Rail, and Financial categories.
"""

from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass


class InvariantViolationError(Exception):
    """Raised when a payment transaction or simulation breaches semantic invariants."""
    def __init__(self, invariant_name: str, category: str, expected: str, observed: str):
        self.invariant_name = invariant_name
        self.category = category
        self.expected = expected
        self.observed = observed
        super().__init__(
            f"INVARIANT VIOLATION [{category} -> {invariant_name}]: Expected {expected}, but observed {observed}."
        )


@dataclass
class SemanticInvariant:
    invariant_id: str
    category: str  # Temporal, Identity, Lifecycle, Rail, Financial
    name: str
    description: str
    check_fn: Callable[[Dict[str, Any]], Tuple[bool, str, str]]


# -------------------------------------------------------------
# INVARIANT CHECK FUNCTIONS
# -------------------------------------------------------------

def check_positive_amount(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    amt = float(tx.get("amount", 0.0))
    if amt <= 0.0:
        return False, "amount > 0.00", f"amount = {amt}"
    return True, "", ""

def check_temporal_monotonicity(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    t_init = tx.get("initiation_timestamp_epoch", 0.0)
    t_auth = tx.get("authorization_timestamp_epoch", t_init + 1.0)
    if t_auth < t_init:
        return False, "authorization_time >= initiation_time", f"auth_time({t_auth}) < init_time({t_init})"
    return True, "", ""

def check_settlement_after_auth(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    t_auth = tx.get("authorization_timestamp_epoch", 0.0)
    t_settle = tx.get("settlement_timestamp_epoch", t_auth + 1.0)
    if t_settle < t_auth:
        return False, "settlement_time >= authorization_time", f"settle_time({t_settle}) < auth_time({t_auth})"
    return True, "", ""

def check_dispute_after_settlement(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    if tx.get("is_disputed", False):
        t_settle = tx.get("settlement_timestamp_epoch", 0.0)
        t_disp = tx.get("dispute_timestamp_epoch", t_settle + 10.0)
        if t_disp < t_settle:
            return False, "dispute_time >= settlement_time", f"dispute_time({t_disp}) < settle_time({t_settle})"
    return True, "", ""

def check_account_user_binding(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    u_id = tx.get("user_id")
    acct_u_id = tx.get("account_user_id", u_id)
    if u_id and acct_u_id and u_id != acct_u_id:
        return False, f"user_id == account_user_id ({u_id})", f"account_user_id = {acct_u_id}"
    return True, "", ""

def check_valid_rail(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    rail = tx.get("rail", "Card")
    allowed = ["UPI", "Card", "A2A", "Wallet", "Recurring Mandate"]
    if rail not in allowed:
        return False, f"rail in {allowed}", f"rail = '{rail}'"
    return True, "", ""

def check_mandate_execution_requires_active(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    if tx.get("rail") == "Recurring Mandate":
        has_mandate = tx.get("mandate_active", True)
        if not has_mandate:
            return False, "mandate_active == True for execution", "mandate_active == False"
    return True, "", ""

def check_velocity_non_negative(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    v1 = float(tx.get("velocity_1h", 0.0))
    v24 = float(tx.get("velocity_24h", 0.0))
    if v1 < 0.0 or v24 < 0.0:
        return False, "velocities >= 0.0", f"velocity_1h={v1}, velocity_24h={v24}"
    if v1 > v24:
        return False, "velocity_24h >= velocity_1h", f"v1({v1}) > v24({v24})"
    return True, "", ""

def check_device_familiarity_bounds(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    df = float(tx.get("device_familiarity", 0.5))
    if not (0.0 <= df <= 1.0):
        return False, "0.0 <= device_familiarity <= 1.0", f"device_familiarity = {df}"
    return True, "", ""

def check_behavioral_deviation_bounds(tx: Dict[str, Any]) -> Tuple[bool, str, str]:
    bd = float(tx.get("behavioral_deviation", 0.2))
    if not (0.0 <= bd <= 1.0):
        return False, "0.0 <= behavioral_deviation <= 1.0", f"behavioral_deviation = {bd}"
    return True, "", ""


# -------------------------------------------------------------
# CATEGORIZED INVARIANTS REGISTRY
# -------------------------------------------------------------

CATEGORIZED_INVARIANTS: List[SemanticInvariant] = [
    # 1. Temporal
    SemanticInvariant("INV-T01", "Temporal", "Temporal Monotonicity", "Authorization must occur after initiation", check_temporal_monotonicity),
    SemanticInvariant("INV-T02", "Temporal", "Settlement Sequence", "Settlement must occur after authorization", check_settlement_after_auth),
    SemanticInvariant("INV-T03", "Temporal", "Dispute Sequence", "Dispute can only occur after settlement", check_dispute_after_settlement),
    SemanticInvariant("INV-T04", "Temporal", "Velocity Monotonicity", "24-hour velocity must be greater than or equal to 1-hour velocity", check_velocity_non_negative),

    # 2. Financial
    SemanticInvariant("INV-F01", "Financial", "Positive Ticket Amount", "Transaction amount must be strictly positive", check_positive_amount),

    # 3. Identity & Behavioral Bounds
    SemanticInvariant("INV-I01", "Identity", "Account User Binding", "Debited account must belong to the initiating user entity", check_account_user_binding),
    SemanticInvariant("INV-I02", "Identity", "Device Familiarity Bounds", "Device familiarity coefficient must lie in [0, 1]", check_device_familiarity_bounds),
    SemanticInvariant("INV-I03", "Identity", "Behavioral Deviation Bounds", "Behavioral deviation score must lie in [0, 1]", check_behavioral_deviation_bounds),

    # 4. Rail & Lifecycle
    SemanticInvariant("INV-R01", "Rail", "Valid Payment Rail", "Transaction rail must belong to supported multi-rail catalog", check_valid_rail),
    SemanticInvariant("INV-R02", "Lifecycle", "Mandate Active Gate", "Mandate debit execution requires prior active mandate registration", check_mandate_execution_requires_active),
]
