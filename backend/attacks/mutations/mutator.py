"""
Adversarial Mutation Engine
Modulates transaction feature distributions across 5 distinct difficulty levels.
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np

from backend.attacks.grammar import AttackComposition
from backend.attacks.difficulty import DIFFICULTY_TIERS, DifficultyTier


class AttackMutator:
    """Applies slot-directed and difficulty-governed perturbations to transaction features."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.RandomState(seed)

    def mutate_transaction_features(
        self,
        base_features: Dict[str, Any],
        composition: AttackComposition,
        tier: Optional[DifficultyTier] = None
    ) -> Dict[str, Any]:
        level = composition.difficulty
        tier = tier or DIFFICULTY_TIERS.get(level, DIFFICULTY_TIERS[1])

        feat = dict(base_features)

        # 1. Amount Perturbation
        amt_scale = float(self.rng.uniform(tier.amount_perturbation_range[0], tier.amount_perturbation_range[1]))
        if composition.evasion == "Micro Amount Below Alert Trigger":
            feat["amount"] = round(float(self.rng.uniform(0.50, 4.99)), 2)
        elif composition.monetization in ["Full Credit Line Drawdown", "High Value Corporate Wire"]:
            feat["amount"] = round(float(feat.get("amount", 100.0) * amt_scale * 2.5), 2)
        else:
            feat["amount"] = round(float(feat.get("amount", 100.0) * amt_scale), 2)

        # 2. Velocity Perturbation
        base_v1 = float(feat.get("velocity_1h", 1.0))
        base_v24 = float(feat.get("velocity_24h", 2.0))
        if composition.temporal_pattern in ["Instantaneous Burst", "Millisecond Cadence", "Sub-Second Form Fill"]:
            feat["velocity_1h"] = float(round(base_v1 * tier.velocity_multiplier * self.rng.uniform(2.0, 4.0), 1))
            feat["velocity_24h"] = float(round(base_v24 * tier.velocity_multiplier * self.rng.uniform(2.5, 5.0), 1))
        elif composition.temporal_pattern in ["Micro-Pacing", "Low Velocity Probe", "Distributed Inter-Request Intervals"]:
            feat["velocity_1h"] = float(round(max(1.0, base_v1 * 0.8), 1))
            feat["velocity_24h"] = float(round(max(1.0, base_v24 * 0.9), 1))
        else:
            feat["velocity_1h"] = float(round(base_v1 * tier.velocity_multiplier, 1))
            feat["velocity_24h"] = float(round(base_v24 * tier.velocity_multiplier, 1))

        # 3. Behavioral Deviation
        b_dev = float(self.rng.uniform(tier.behavioral_deviation_min, tier.behavioral_deviation_max))
        if composition.evasion in ["Synthetic Keystroke Cadence", "Bezier Curve Touch Emulation", "Humanized Thinking Pauses"]:
            b_dev = float(np.clip(b_dev * 0.6, 0.05, 0.40))
        feat["behavioral_deviation"] = round(b_dev, 4)

        # 4. Device Familiarity
        d_fam = float(self.rng.uniform(tier.device_familiarity_min, tier.device_familiarity_max))
        if composition.trust in ["Legitimate User Device", "Legitimate Mobile App", "Established Terminal ID"]:
            d_fam = float(np.clip(d_fam + 0.35, 0.60, 0.98))
        elif composition.trust in ["Generated IMEI/Android ID", "Forged Browser Fingerprint"]:
            d_fam = float(np.clip(d_fam * 0.4, 0.0, 0.35))
        feat["device_familiarity"] = round(d_fam, 4)

        # 5. Geographic Distance
        if composition.trust in ["Residential Proxy", "Local Residential ISP IP", "Geofence Match"]:
            feat["geo_distance_km"] = round(float(self.rng.uniform(1.0, 15.0)), 2)
            feat["is_international"] = 0
        elif composition.evasion == "Fake Proximity to Merchant POS":
            feat["geo_distance_km"] = round(float(self.rng.uniform(0.1, 2.0)), 2)
            feat["is_international"] = 0
        else:
            feat["geo_distance_km"] = round(float(self.rng.uniform(80.0, 1200.0)), 2)
            feat["is_international"] = 1 if self.rng.rand() > 0.6 else 0

        # 6. Merchant & Carrier Flags
        if composition.family in ["Merchant & Collusive Abuse", "Social Engineering & APP"]:
            feat["merchant_risk_score"] = round(float(self.rng.uniform(0.65, 0.95)), 4)
            feat["mcc_risk_weight"] = round(float(self.rng.uniform(0.70, 0.98)), 4)
        else:
            feat["merchant_risk_score"] = round(float(self.rng.uniform(0.20, 0.60)), 4)
            feat["mcc_risk_weight"] = round(float(self.rng.uniform(0.30, 0.70)), 4)

        feat["carrier_change_flag"] = 1 if self.rng.rand() < tier.carrier_change_prob else 0

        # 7. Account Vintage
        if composition.family == "Identity & Synthetic Fraud" and composition.evasion == "Dormant Account Seasoning":
            feat["account_age_days"] = int(self.rng.uniform(300, 800))
        elif composition.family == "Account Takeover" and composition.behavior == "New Device First Login":
            feat["account_age_days"] = int(self.rng.uniform(50, 400))
        else:
            feat["account_age_days"] = int(max(1, feat.get("account_age_days", 180) * (0.8 if level >= 3 else 0.2)))

        return feat

    def apply_mutation(
        self,
        base_features: Dict[str, Any],
        difficulty_level: str,
        mutation_strength: float = 0.4
    ) -> Dict[str, Any]:
        """Backward compatible helper."""
        diff_int = 3
        if "1" in difficulty_level or "Easy" in difficulty_level:
            diff_int = 1
        elif "2" in difficulty_level or "Mod" in difficulty_level:
            diff_int = 2
        elif "4" in difficulty_level or "Adv" in difficulty_level:
            diff_int = 4
        elif "5" in difficulty_level or "Unseen" in difficulty_level:
            diff_int = 5

        dummy_comp = AttackComposition(
            access="Credential Stuffing",
            trust="Residential Proxy",
            rail="Card",
            evasion="Temporal Pacing",
            behavior="Synthetic Cadence",
            monetization="P2P Transfer",
            temporal_pattern="Micro-Pacing",
            difficulty=diff_int
        )
        return self.mutate_transaction_features(base_features, dummy_comp)


AdversarialMutator = AttackMutator
