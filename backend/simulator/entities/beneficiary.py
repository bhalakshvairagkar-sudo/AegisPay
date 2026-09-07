"""
AegisPay v2 - Beneficiary Entity
Models recipient endpoints, mule probability, and routing fan-in patterns.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class BeneficiaryEntity:
    beneficiary_id: str
    account_number_masked: str
    routing_code: str
    name: str
    rail: str  # UPI, Card, A2A, Wallet
    vintage_days: int
    is_mule_account: bool = False
    inbound_transfer_fanin: int = 1
    total_inbound_volume_24h: float = 0.0
