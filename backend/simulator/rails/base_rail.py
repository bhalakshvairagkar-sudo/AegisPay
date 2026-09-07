"""
AegisPay v2 - Base Payment Rail Specification
Abstract interface defining schema, allowed lifecycle states, and rail-specific policies.
"""

from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RailPolicyAction:
    action_type: str  # ALLOW, FRICTION, REVIEW, BLOCK
    rail_specific_directive: str  # e.g. "DECLINE", "COOLING_OFF_HOLD", "STEP_UP_3DS"
    reason_code: str
    friction_cost: float


class BasePaymentRail(ABC):
    """Abstract specification for a payment execution rail."""

    def __init__(self, rail_name: str, allows_dispute: bool = True, is_real_time: bool = True):
        self.rail_name = rail_name
        self.allows_dispute = allows_dispute
        self.is_real_time = is_real_time

    @abstractmethod
    def get_allowed_lifecycle_states(self) -> List[str]:
        pass

    @abstractmethod
    def map_risk_action(self, risk_level: str, reason_code: str) -> RailPolicyAction:
        pass

    @abstractmethod
    def validate_rail_transaction(self, tx_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        pass
