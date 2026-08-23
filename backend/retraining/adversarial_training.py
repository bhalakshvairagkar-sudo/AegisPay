"""
Adversarial Retraining & Targeted Counter-Sample Generator
Synthesizes adversarial counterexamples in the exact feature regions where models previously failed,
and performs loss-weighted retraining to harden the Blue Team defenses.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd

from backend.simulator.transactions import SyntheticTransaction, PaymentSimulator
from backend.models.ensemble import AegisPayHybridDefense


class AdversarialTrainer:
    """Performs closed-loop adversarial retraining."""

    def __init__(self, simulator: PaymentSimulator, seed: int = 42):
        self.simulator = simulator
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def generate_targeted_counterexamples(
        self,
        evasion_clusters: List[Dict[str, Any]],
        n_samples: int = 300
    ) -> List[SyntheticTransaction]:
        """
        Generates synthetic counter-samples around the centroids of missed evasion clusters.
        """
        counterexamples: List[SyntheticTransaction] = []
        if not evasion_clusters:
            return counterexamples

        samples_per_cluster = max(10, n_samples // len(evasion_clusters))
        users = self.simulator.users
        merchants = self.simulator.merchants

        for c_idx, cluster in enumerate(evasion_clusters):
            centroid = cluster.get("centroid_features", {})
            dom_family = cluster.get("dominant_family", "Behavioral Impersonation")

            for i in range(samples_per_cluster):
                user = users[self.rng.integers(0, len(users))]
                merchant = merchants[self.rng.integers(0, len(merchants))]

                # Sample around cluster centroid with localized Gaussian jitter
                amt = float(max(1.0, centroid.get("amount", 85.0) + self.rng.normal(0, 15.0)))
                vel_1h = int(max(1, round(centroid.get("velocity_1h", 2) + self.rng.normal(0, 0.8))))
                vel_24h = int(vel_1h + max(1, round(centroid.get("velocity_24h", 4) + self.rng.normal(0, 1.2))))
                dev_fam = float(np.clip(centroid.get("device_familiarity", 0.6) + self.rng.normal(0, 0.05), 0.1, 0.95))
                geo_dist = float(max(2.0, centroid.get("geo_distance_km", 40.0) + self.rng.normal(0, 15.0)))
                bio_dev = float(np.clip(centroid.get("behavioral_deviation", 0.22) + self.rng.normal(0, 0.03), 0.08, 0.55))
                touch_dev = float(np.clip(centroid.get("touch_pressure_deviation", 0.18) + self.rng.normal(0, 0.03), 0.05, 0.45))

                txn = SyntheticTransaction(
                    txn_id=f"SCN-CNTR-{c_idx+1}-{100 + i}",
                    user_id=user.user_id,
                    merchant_id=merchant.merchant_id,
                    device_id=f"DEV-CNTR-{c_idx+1}-{i}",
                    amount=round(amt, 2),
                    velocity_1h=vel_1h,
                    velocity_24h=vel_24h,
                    device_familiarity=round(dev_fam, 3),
                    geo_distance_km=round(geo_dist, 2),
                    behavioral_deviation=round(bio_dev, 3),
                    merchant_risk_score=merchant.merchant_risk_score,
                    account_age_days=user.account_age_days,
                    touch_pressure_deviation=round(touch_dev, 3),
                    carrier_change_flag=int(centroid.get("carrier_change_flag", 0)),
                    mcc_risk_weight=merchant.mcc_risk_weight,
                    hour_of_day=int(self.rng.integers(0, 24)),
                    is_international=int(centroid.get("is_international", 0)),
                    is_fraud=1,
                    attack_id=f"CNTR-{c_idx+1}",
                    attack_family=dom_family,
                    attack_name=f"Targeted Counter-Sample ({cluster.get('title', 'Evasion')})",
                    difficulty="Adversarial",
                    gen_ai=True
                )
                counterexamples.append(txn)

        return counterexamples

    def train_hardened_model(
        self,
        base_train_df: pd.DataFrame,
        base_y_train: np.ndarray,
        counterexamples: List[SyntheticTransaction],
        target_version: str = "v2.0"
    ) -> AegisPayHybridDefense:
        """
        Merges base training data with targeted counterexamples and trains a new hardened model iteration.
        Applies higher sample weight to counterexamples to prioritize closed-loop learning.
        """
        cntr_df = pd.DataFrame([s.to_feature_dict() for s in counterexamples])
        cntr_y = np.ones(len(counterexamples), dtype=int)

        # Combine datasets
        combined_X = pd.concat([base_train_df, cntr_df], ignore_index=True)
        combined_y = np.concatenate([base_y_train, cntr_y])

        # Sample weighting: 2.0x weight for targeted adversarial counterexamples
        sample_weights = np.ones(len(combined_y))
        sample_weights[len(base_y_train):] = 2.2

        hardened_model = AegisPayHybridDefense(
            version=target_version,
            xgb_weight=0.52 if target_version == "v2.0" else 0.50,
            anomaly_weight=0.28 if target_version == "v2.0" else 0.30,
            rule_weight=0.10,
            behavior_weight=0.10,
            seed=self.seed + (2 if target_version == "v2.0" else 3)
        )

        hardened_model.fit(combined_X, combined_y, sample_weight=sample_weights)
        return hardened_model
