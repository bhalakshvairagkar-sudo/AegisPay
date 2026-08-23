"""
Synthetic User Profile Generator
Generates realistic cardholder demographic, behavioral, and geographical baselines.
"""

from dataclasses import dataclass
from typing import List
import numpy as np


@dataclass
class UserProfile:
    user_id: str
    account_age_days: int
    mean_ticket_amount: float
    std_ticket_amount: float
    avg_velocity_1h: float
    home_lat: float
    home_lon: float
    preferred_mccs: List[str]
    primary_device_id: str
    baseline_touch_pressure: float
    biometric_stability: float


def generate_user_population(n_users: int = 100, seed: int = 42) -> List[UserProfile]:
    """Generates a seeded population of realistic cardholders with distinct behavioral baselines."""
    rng = np.random.default_rng(seed)
    users = []

    mcc_pool = ["5411", "5812", "5912", "5311", "5732", "4829", "6011", "7011"]

    for i in range(n_users):
        user_id = f"USR-{10000 + i}"
        account_age_days = int(rng.exponential(scale=365) + 30)
        account_age_days = min(3650, max(15, account_age_days))

        # Spending profile: most users spend $20-$80 on average, some are affluent ($200+)
        is_affluent = rng.random() < 0.15
        if is_affluent:
            mean_ticket = float(rng.uniform(150, 450))
            std_ticket = float(mean_ticket * rng.uniform(0.3, 0.6))
        else:
            mean_ticket = float(rng.uniform(25, 95))
            std_ticket = float(mean_ticket * rng.uniform(0.25, 0.5))

        # Geographical anchoring (Major metro centroids with Gaussian spread)
        metro_anchors = [
            (40.7128, -74.0060),  # NYC
            (34.0522, -118.2437), # LA
            (51.5074, -0.1278),   # London
            (19.0760, 72.8777),   # Mumbai
            (1.3521, 103.8198),   # Singapore
        ]
        anchor = metro_anchors[rng.integers(0, len(metro_anchors))]
        home_lat = float(anchor[0] + rng.normal(0, 0.2))
        home_lon = float(anchor[1] + rng.normal(0, 0.2))

        # User preferred MCCs (2-4 typical spending categories)
        n_mccs = rng.integers(2, 5)
        user_mccs = list(rng.choice(mcc_pool, size=n_mccs, replace=False))

        users.append(UserProfile(
            user_id=user_id,
            account_age_days=account_age_days,
            mean_ticket_amount=round(mean_ticket, 2),
            std_ticket_amount=round(std_ticket, 2),
            avg_velocity_1h=float(rng.uniform(0.1, 1.2)),
            home_lat=home_lat,
            home_lon=home_lon,
            preferred_mccs=user_mccs,
            primary_device_id=f"DEV-PRIM-{user_id}",
            baseline_touch_pressure=float(rng.uniform(0.45, 0.75)),
            biometric_stability=float(rng.uniform(0.85, 0.98)),
        ))

    return users
