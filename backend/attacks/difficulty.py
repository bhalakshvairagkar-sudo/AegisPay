"""
AegisPay v2 - Attack Difficulty Tiers & Mutation Profiles
Defines 5 formal difficulty levels and their mathematical perturbation parameters.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class DifficultyTier:
    level: int
    name: str
    amount_perturbation_range: tuple  # min, max scale
    velocity_multiplier: float
    behavioral_deviation_min: float
    behavioral_deviation_max: float
    device_familiarity_min: float
    device_familiarity_max: float
    carrier_change_prob: float
    description: str


DIFFICULTY_TIERS: Dict[int, DifficultyTier] = {
    1: DifficultyTier(
        level=1,
        name="Obvious / Unconstrained",
        amount_perturbation_range=(4.0, 10.0),
        velocity_multiplier=6.0,
        behavioral_deviation_min=0.80,
        behavioral_deviation_max=1.00,
        device_familiarity_min=0.00,
        device_familiarity_max=0.10,
        carrier_change_prob=0.90,
        description="Crude brute-force attack with extreme amounts, massive velocity surges, and zero device familiarity."
    ),
    2: DifficultyTier(
        level=2,
        name="Lightly Mutated",
        amount_perturbation_range=(2.5, 4.5),
        velocity_multiplier=3.5,
        behavioral_deviation_min=0.55,
        behavioral_deviation_max=0.80,
        device_familiarity_min=0.10,
        device_familiarity_max=0.30,
        carrier_change_prob=0.60,
        description="Lightly masked attack using proxy subnets and randomized timing, but distinguishable on velocity."
    ),
    3: DifficultyTier(
        level=3,
        name="Behaviorally Close to Legitimate",
        amount_perturbation_range=(1.1, 2.2),
        velocity_multiplier=1.8,
        behavioral_deviation_min=0.30,
        behavioral_deviation_max=0.55,
        device_familiarity_min=0.35,
        device_familiarity_max=0.65,
        carrier_change_prob=0.25,
        description="Mimics cardholder historical ticket sizes and typical daytime active hours to blend into normal traffic."
    ),
    4: DifficultyTier(
        level=4,
        name="Adaptive Evasive",
        amount_perturbation_range=(0.9, 1.4),
        velocity_multiplier=1.2,
        behavioral_deviation_min=0.15,
        behavioral_deviation_max=0.35,
        device_familiarity_min=0.60,
        device_familiarity_max=0.85,
        carrier_change_prob=0.05,
        description="Precision attack specifically engineered to stay just under standard rule velocity and amount ceilings."
    ),
    5: DifficultyTier(
        level=5,
        name="Detector-Specific Hard Case / Whitebox",
        amount_perturbation_range=(0.95, 1.15),
        velocity_multiplier=1.05,
        behavioral_deviation_min=0.05,
        behavioral_deviation_max=0.20,
        device_familiarity_min=0.75,
        device_familiarity_max=0.95,
        carrier_change_prob=0.00,
        description="Synthesized counter-sample targeted directly at the classifier decision boundary to maximize evasion."
    )
}
