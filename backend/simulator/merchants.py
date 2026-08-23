"""
Synthetic Merchant Network Generator
Generates realistic merchant entities with Merchant Category Codes (MCC), risk ratings, and geographical coordinates.
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class MerchantProfile:
    merchant_id: str
    name: str
    mcc: str
    mcc_description: str
    mcc_risk_weight: float
    merchant_risk_score: float
    avg_ticket_amount: float
    lat: float
    lon: float
    is_high_risk: bool


MCC_TAXONOMY = {
    "5411": ("Grocery Stores, Supermarkets", 0.05, 45.0),
    "5812": ("Eating Places, Restaurants", 0.08, 38.0),
    "5912": ("Drug Stores, Pharmacies", 0.06, 32.0),
    "5311": ("Department Stores", 0.15, 110.0),
    "5732": ("Electronic Sales & Hardware", 0.45, 380.0),
    "4829": ("Money Transfer / Wire", 0.85, 420.0),
    "6011": ("Automated Cash Disbursements", 0.78, 250.0),
    "7011": ("Hotels, Lodging", 0.35, 290.0),
    "7995": ("Betting / Casino / Gambling", 0.92, 180.0),
    "5944": ("Jewelry and Watch Retail", 0.65, 850.0),
}


def generate_merchant_network(n_merchants: int = 50, seed: int = 42) -> List[MerchantProfile]:
    """Generates a seeded network of e-commerce and retail merchants."""
    rng = np.random.default_rng(seed)
    merchants = []

    mcc_keys = list(MCC_TAXONOMY.keys())
    mcc_probs = [0.25, 0.20, 0.15, 0.12, 0.10, 0.05, 0.05, 0.04, 0.02, 0.02]

    for i in range(n_merchants):
        mcc = str(rng.choice(mcc_keys, p=mcc_probs))
        desc, base_risk, base_ticket = MCC_TAXONOMY[mcc]

        # Individual merchant variance around MCC baseline
        merchant_risk = float(np.clip(base_risk + rng.normal(0, 0.08), 0.01, 0.99))
        avg_ticket = float(max(5.0, base_ticket * rng.uniform(0.7, 1.5)))
        is_high_risk = merchant_risk > 0.60

        merchants.append(MerchantProfile(
            merchant_id=f"MER-{20000 + i}",
            name=f"Merchant_{mcc}_{i+1}",
            mcc=mcc,
            mcc_description=desc,
            mcc_risk_weight=round(base_risk, 3),
            merchant_risk_score=round(merchant_risk, 3),
            avg_ticket_amount=round(avg_ticket, 2),
            lat=float(rng.uniform(-60.0, 60.0)),
            lon=float(rng.uniform(-150.0, 150.0)),
            is_high_risk=is_high_risk,
        ))

    return merchants
