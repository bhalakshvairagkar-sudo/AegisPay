"""
Adversarial Mutation Engine
Modulates transaction feature distributions across 5 distinct difficulty levels:
- Level 1: Easy (Obvious statistical outliers, high velocity, unfamiliar device, gross geo jumps)
- Level 2: Moderate (Moderate deviations, slight velocity bursts)
- Level 3: Hard (Subtle amounts, near-boundary velocity, localized proxy)
- Level 4: Adversarial (Multi-feature coordinated evasion, biometric smoothing, sub-threshold slicing)
- Level 5: Unseen (Novel feature combinations designed for zero-shot holdout testing)

NOTE: Difficulty influences the statistical feature perturbations ONLY.
It does NOT determine or hardcode the Blue Team detection outcome.
"""

from typing import Dict, Any, Tuple
import numpy as np


class AdversarialMutator:
    """Applies controlled mathematical perturbations to base attack feature vectors."""

    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def apply_mutation(
        self,
        base_features: Dict[str, Any],
        difficulty_level: str,
        mutation_strength: float = 0.4
    ) -> Dict[str, Any]:
        """
        Perturbs base features based on difficulty and mutation strength.
        Higher difficulty shifts features closer to legitimate cardholder baselines to test detector limits.
        """
        features = base_features.copy()
        mut = float(np.clip(mutation_strength, 0.1, 0.9))

        # Scale factor inversely proportional to difficulty (Higher difficulty = harder to separate from legit)
        if difficulty_level == "Easy" or difficulty_level == "Level 1":
            # Easy: Exaggerated fraud signals
            features["velocity_1h"] = int(max(4, features.get("velocity_1h", 3) + self.rng.integers(3, 8)))
            features["velocity_24h"] = int(features["velocity_1h"] + self.rng.integers(5, 15))
            features["device_familiarity"] = float(np.clip(features.get("device_familiarity", 0.2) * 0.4, 0.0, 0.25))
            features["geo_distance_km"] = float(max(600.0, features.get("geo_distance_km", 200.0) * (1.5 + mut)))
            features["behavioral_deviation"] = float(np.clip(0.70 + self.rng.uniform(0.1, 0.25), 0.6, 0.99))
            features["touch_pressure_deviation"] = float(np.clip(0.65 + self.rng.uniform(0.1, 0.25), 0.5, 0.95))

        elif difficulty_level == "Moderate" or difficulty_level == "Level 2":
            # Moderate: Distinct but realistic anomalies
            features["velocity_1h"] = int(max(2, features.get("velocity_1h", 2) + self.rng.integers(1, 4)))
            features["velocity_24h"] = int(features["velocity_1h"] + self.rng.integers(3, 8))
            features["device_familiarity"] = float(np.clip(features.get("device_familiarity", 0.35) + self.rng.normal(0, 0.08), 0.15, 0.55))
            features["geo_distance_km"] = float(np.clip(features.get("geo_distance_km", 150.0) + self.rng.normal(50, 40), 50.0, 800.0))
            features["behavioral_deviation"] = float(np.clip(0.45 + self.rng.uniform(0.05, 0.20), 0.35, 0.75))
            features["touch_pressure_deviation"] = float(np.clip(0.40 + self.rng.uniform(0.05, 0.18), 0.30, 0.70))

        elif difficulty_level == "Hard" or difficulty_level == "Level 3":
            # Hard: Low-profile perturbations near decision boundaries
            features["velocity_1h"] = int(max(1, min(4, features.get("velocity_1h", 2) + self.rng.integers(0, 2))))
            features["velocity_24h"] = int(features["velocity_1h"] + self.rng.integers(1, 4))
            features["device_familiarity"] = float(np.clip(0.55 + self.rng.normal(0, 0.1), 0.35, 0.78))
            features["geo_distance_km"] = float(np.clip(self.rng.normal(85.0, 30.0), 15.0, 220.0))
            features["behavioral_deviation"] = float(np.clip(0.28 + self.rng.normal(0, 0.05) * (1.0 - mut * 0.3), 0.18, 0.48))
            features["touch_pressure_deviation"] = float(np.clip(0.25 + self.rng.normal(0, 0.05), 0.15, 0.45))

        elif difficulty_level == "Adversarial" or difficulty_level == "Level 4":
            # Adversarial: Coordinated mimicked features designed to probe detector weak spots
            # Subtle amount adjustments, mimicked biometric touch, residential proxy geo match
            features["velocity_1h"] = int(max(1, min(3, self.rng.poisson(lam=1.2))))
            features["velocity_24h"] = int(features["velocity_1h"] + self.rng.poisson(lam=2.0))
            features["device_familiarity"] = float(np.clip(0.68 + self.rng.normal(0, 0.08), 0.50, 0.88))
            features["geo_distance_km"] = float(np.clip(abs(self.rng.normal(25.0, 18.0)), 2.0, 95.0))
            # Biometric mimicry dampens obvious deviations
            features["behavioral_deviation"] = float(np.clip(0.19 + self.rng.normal(0, 0.04), 0.11, 0.32))
            features["touch_pressure_deviation"] = float(np.clip(0.16 + self.rng.normal(0, 0.03), 0.08, 0.28))

        elif difficulty_level == "Unseen" or difficulty_level == "Level 5":
            # Unseen Holdout: Cross-feature non-linear correlations
            features["velocity_1h"] = int(self.rng.choice([1, 2, 3]))
            features["velocity_24h"] = int(features["velocity_1h"] + self.rng.choice([2, 4, 6]))
            features["device_familiarity"] = float(np.clip(0.62 + self.rng.normal(0, 0.12), 0.40, 0.85))
            features["geo_distance_km"] = float(np.clip(abs(self.rng.normal(45.0, 35.0)), 5.0, 250.0))
            features["behavioral_deviation"] = float(np.clip(0.22 + self.rng.normal(0, 0.05), 0.12, 0.38))
            features["touch_pressure_deviation"] = float(np.clip(0.18 + self.rng.normal(0, 0.04), 0.09, 0.34))

        return features
