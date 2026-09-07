"""
AegisPay v2 - User Entity
Models cardholder demographics, account history, spending baselines, and behavioral profiles.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class UserEntity:
    user_id: str
    account_vintage_days: int
    mean_ticket_amount: float
    std_ticket_amount: float
    home_latitude: float
    home_longitude: float
    primary_device_id: str
    known_devices: List[str] = field(default_factory=list)
    known_beneficiaries: List[str] = field(default_factory=list)
    active_hour_mean: float = 14.0  # Peak hour 2 PM
    active_hour_std: float = 3.5
    daily_velocity_baseline: float = 2.4
    risk_tier: str = "LOW"

    def is_typical_amount(self, amount: float) -> bool:
        """Evaluates whether amount falls within 3 standard deviations of baseline."""
        z = abs(amount - self.mean_ticket_amount) / max(1.0, self.std_ticket_amount)
        return z < 3.0

    def is_known_beneficiary(self, beneficiary_id: str) -> bool:
        return beneficiary_id in self.known_beneficiaries

    def is_known_device(self, device_id: str) -> bool:
        return device_id in self.known_devices or device_id == self.primary_device_id
