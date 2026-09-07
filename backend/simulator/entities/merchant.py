"""
AegisPay v2 - Merchant Entity
Models MCC classification, chargeback baselines, geography, and transaction volume limits.
"""

from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class MerchantEntity:
    merchant_id: str
    name: str
    mcc_code: str
    category_name: str
    baseline_risk_score: float  # 0.0 to 1.0
    chargeback_rate_baseline: float  # e.g. 0.005 = 0.5%
    latitude: float
    longitude: float
    is_high_risk_mcc: bool = False
    average_daily_volume: int = 150


MCC_DIRECTORY: Dict[str, Dict[str, Any]] = {
    "5411": {"category": "Grocery Stores / Supermarkets", "risk": 0.08, "chargeback": 0.001, "high_risk": False},
    "5812": {"category": "Restaurants / Dining", "risk": 0.12, "chargeback": 0.002, "high_risk": False},
    "5732": {"category": "Consumer Electronics", "risk": 0.45, "chargeback": 0.015, "high_risk": False},
    "6051": {"category": "Crypto / Foreign Currency / Quasi-Cash", "risk": 0.88, "chargeback": 0.052, "high_risk": True},
    "7995": {"category": "Gambling / Casinos / Lottery", "risk": 0.92, "chargeback": 0.068, "high_risk": True},
    "4829": {"category": "Wire Money Transfer", "risk": 0.82, "chargeback": 0.045, "high_risk": True},
    "5944": {"category": "Jewelry / Luxury Goods", "risk": 0.65, "chargeback": 0.028, "high_risk": True},
    "4722": {"category": "Travel Agencies / Airlines", "risk": 0.38, "chargeback": 0.012, "high_risk": False},
    "5311": {"category": "Department Stores", "risk": 0.18, "chargeback": 0.004, "high_risk": False},
    "5999": {"category": "Miscellaneous Retail", "risk": 0.30, "chargeback": 0.008, "high_risk": False}
}
