"""
Synthetic Payment Transaction Engine
Generates realistic cardholder transaction streams using authentic statistical distributions:
- Heavy-tailed Log-normal monetary amounts
- Poisson transaction inter-arrival processes
- Haversine geographical coordinate distances
- Multi-window historical velocities (1h, 24h)
- Sensor telemetry and behavioral deviation metrics
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Tuple
import math
import numpy as np
import pandas as pd

from backend.simulator.users import UserProfile, generate_user_population
from backend.simulator.merchants import MerchantProfile, generate_merchant_network
from backend.simulator.devices import DeviceFingerprint, generate_device_pool


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates the great-circle distance between two geographical points on Earth in kilometers."""
    R = 6371.0  # Earth's mean radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


@dataclass
class SyntheticTransaction:
    txn_id: str
    user_id: str
    merchant_id: str
    device_id: str
    amount: float
    velocity_1h: int
    velocity_24h: int
    device_familiarity: float
    geo_distance_km: float
    behavioral_deviation: float
    merchant_risk_score: float
    account_age_days: int
    touch_pressure_deviation: float
    carrier_change_flag: int
    mcc_risk_weight: float
    hour_of_day: int
    is_international: int
    is_fraud: int

    # Metadata fields (Strictly segregated from model inputs)
    attack_id: str = "LEGIT"
    attack_family: str = "Legitimate"
    attack_name: str = "Legitimate Transaction"
    difficulty: str = "None"
    gen_ai: bool = False

    def to_feature_dict(self) -> Dict[str, Any]:
        """Returns only allowed numeric features for ML model ingestion."""
        return {
            "amount": self.amount,
            "velocity_1h": self.velocity_1h,
            "velocity_24h": self.velocity_24h,
            "device_familiarity": self.device_familiarity,
            "geo_distance_km": self.geo_distance_km,
            "behavioral_deviation": self.behavioral_deviation,
            "merchant_risk_score": self.merchant_risk_score,
            "account_age_days": self.account_age_days,
            "touch_pressure_deviation": self.touch_pressure_deviation,
            "carrier_change_flag": self.carrier_change_flag,
            "mcc_risk_weight": self.mcc_risk_weight,
            "hour_of_day": self.hour_of_day,
            "is_international": self.is_international,
        }

    def to_full_dict(self) -> Dict[str, Any]:
        """Returns full transaction record including metadata for logging and UI display."""
        d = asdict(self)
        d["genAi"] = self.gen_ai
        return d


class PaymentSimulator:
    """Generates parameterized synthetic payment populations with seeded reproducibility."""

    def __init__(self, seed: int = 42, n_users: int = 150, n_merchants: int = 60, n_devices: int = 200):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.users = generate_user_population(n_users, seed=seed)
        self.merchants = generate_merchant_network(n_merchants, seed=seed + 1)
        self.devices = generate_device_pool(n_devices, seed=seed + 2)
        self.user_map = {u.user_id: u for u in self.users}
        self.merchant_map = {m.merchant_id: m for m in self.merchants}

    def generate_legitimate_stream(self, n_transactions: int = 1000) -> List[SyntheticTransaction]:
        """Generates realistic legitimate transaction records following standard cardholder behaviors."""
        txns = []
        n_users = len(self.users)
        n_merchants = len(self.merchants)

        for i in range(n_transactions):
            txn_id = f"TXN-LGT-{100000 + i}"
            user = self.users[self.rng.integers(0, n_users)]

            # Select merchant (bias towards user's preferred MCCs)
            if self.rng.random() < 0.70:
                preferred_merchants = [m for m in self.merchants if m.mcc in user.preferred_mccs]
                merchant = preferred_merchants[self.rng.integers(0, len(preferred_merchants))] if preferred_merchants else self.merchants[self.rng.integers(0, n_merchants)]
            else:
                merchant = self.merchants[self.rng.integers(0, n_merchants)]

            # Amount follows log-normal distribution centered around user/merchant mean
            target_mean = (user.mean_ticket_amount + merchant.avg_ticket_amount) / 2.0
            sigma = 0.45
            mu = math.log(max(1.0, target_mean)) - (sigma ** 2) / 2.0
            raw_amount = float(self.rng.lognormal(mean=mu, sigma=sigma))
            amount = round(float(np.clip(raw_amount, 2.50, 4500.0)), 2)

            # Velocity in 1h: mostly 0 or 1, occasionally 2-3
            velocity_1h = int(self.rng.poisson(lam=0.4))
            velocity_1h = min(6, velocity_1h)
            velocity_24h = int(velocity_1h + self.rng.poisson(lam=2.1))

            # Device familiarity: 92% of genuine transactions use primary/familiar device
            is_familiar_device = self.rng.random() < 0.92
            if is_familiar_device:
                device_id = user.primary_device_id
                device_fam = float(np.clip(self.rng.normal(0.88, 0.08), 0.65, 1.0))
            else:
                device_id = f"DEV-SEC-{user.user_id}"
                device_fam = float(np.clip(self.rng.normal(0.45, 0.15), 0.15, 0.75))

            # Geolocation: mostly within home metro area (distance < 25 km)
            is_traveling = self.rng.random() < 0.04
            if is_traveling:
                geo_dist = float(self.rng.uniform(150.0, 1800.0))
                is_international = int(self.rng.random() < 0.35)
            else:
                geo_dist = float(abs(self.rng.normal(8.0, 12.0)))
                is_international = 0

            # Behavioral deviation: Low for genuine user (mean 0.15)
            bio_dev = float(np.clip(self.rng.normal(0.12, 0.06), 0.01, 0.35))
            touch_dev = float(np.clip(self.rng.normal(0.10, 0.05), 0.01, 0.30))

            # Time of day: natural human diurnal rhythm (peak daytime/evening)
            hour_probs = np.array([
                0.01, 0.01, 0.005, 0.005, 0.01, 0.02,
                0.04, 0.06, 0.08, 0.08, 0.07, 0.08,
                0.09, 0.08, 0.07, 0.06, 0.07, 0.08,
                0.06, 0.05, 0.03, 0.02, 0.015, 0.01
            ])
            hour_probs /= hour_probs.sum()
            hour_of_day = int(self.rng.choice(24, p=hour_probs))

            txns.append(SyntheticTransaction(
                txn_id=txn_id,
                user_id=user.user_id,
                merchant_id=merchant.merchant_id,
                device_id=device_id,
                amount=amount,
                velocity_1h=velocity_1h,
                velocity_24h=velocity_24h,
                device_familiarity=round(device_fam, 3),
                geo_distance_km=round(geo_dist, 2),
                behavioral_deviation=round(bio_dev, 3),
                merchant_risk_score=merchant.merchant_risk_score,
                account_age_days=user.account_age_days,
                touch_pressure_deviation=round(touch_dev, 3),
                carrier_change_flag=0,
                mcc_risk_weight=merchant.mcc_risk_weight,
                hour_of_day=hour_of_day,
                is_international=is_international,
                is_fraud=0,
                attack_id="LEGIT",
                attack_family="Legitimate",
                attack_name="Legitimate Transaction",
                difficulty="None",
                gen_ai=False,
            ))

        return txns
