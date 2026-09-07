"""
AegisPay v2 - Account Entity
Represents the underlying payment credential, limits, and standing state.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class AccountEntity:
    account_id: str
    user_id: str
    currency: str = "USD"
    balance: float = 5000.00
    credit_limit: float = 10000.00
    is_active: bool = True
    is_frozen: bool = False
    registered_mandates: List[str] = field(default_factory=list)
    daily_spend_current: float = 0.0
    daily_spend_limit: float = 2500.00
