"""
Adversarial Attack Scenario Generator
Synthesizes parameterized attack vectors across 8 families with realistic feature modifications.
Outputs clean feature matrices and scenario metadata without leaking detection outcomes.
"""

from typing import List, Dict, Any, Optional
import numpy as np

from backend.attacks.taxonomy import AttackTaxonomy, AttackVector, taxonomy_instance
from backend.attacks.mutations.mutator import AdversarialMutator
from backend.simulator.transactions import SyntheticTransaction, PaymentSimulator


class AttackScenarioGenerator:
    """Generates synthetic adversarial attack scenarios against payment fraud models."""

    def __init__(self, simulator: Optional[PaymentSimulator] = None, seed: int = 42):
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.simulator = simulator or PaymentSimulator(seed=seed)
        self.taxonomy = taxonomy_instance
        self.mutator = AdversarialMutator(seed=seed)

    def generate_scenarios(
        self,
        count: int = 25,
        family_filter: str = "ALL",
        sophistication_target: float = 7.5,
        mutation_strength: float = 0.4,
        difficulty: Optional[str] = None
    ) -> List[SyntheticTransaction]:
        """
        Generates a batch of synthetic adversarial payment scenarios.
        Does NOT decide detection outcomes; detection is evaluated strictly by the ML defense models.
        """
        # Filter available attack vectors
        if family_filter == "ALL" or not family_filter:
            available_attacks = self.taxonomy.get_all()
        else:
            available_attacks = self.taxonomy.get_by_family(family_filter)

        if not available_attacks:
            available_attacks = self.taxonomy.get_all()

        scenarios: List[SyntheticTransaction] = []
        users = self.simulator.users
        merchants = self.simulator.merchants

        for i in range(count):
            base_attack: AttackVector = available_attacks[i % len(available_attacks)]
            user = users[self.rng.integers(0, len(users))]
            merchant = merchants[self.rng.integers(0, len(merchants))]

            # Compute effective difficulty if not specified
            if difficulty:
                eff_difficulty = difficulty
            else:
                if base_attack.family == "AI Adaptive Fraud":
                    eff_difficulty = "Unseen"
                elif base_attack.sophistication > 8.5 or mutation_strength > 0.6:
                    eff_difficulty = "Adversarial"
                elif base_attack.sophistication > 7.0:
                    eff_difficulty = "Hard"
                elif base_attack.sophistication < 5.5:
                    eff_difficulty = "Easy"
                else:
                    eff_difficulty = "Moderate"

            # Base feature generation customized by attack family characteristics
            base_amount = user.mean_ticket_amount * float(self.rng.uniform(1.2, 4.5))
            if base_attack.family == "Transaction Manipulation":
                # Micro-salami attack: amounts under $5.00
                if "Salami" in base_attack.name or "TXN-01" in base_attack.id:
                    base_amount = float(self.rng.uniform(0.85, 4.95))
            elif base_attack.family == "Account Takeover":
                # High ticket drain
                base_amount = float(self.rng.uniform(450.0, 3200.0))

            base_features = {
                "amount": round(base_amount, 2),
                "velocity_1h": int(self.rng.integers(3, 9)),
                "velocity_24h": int(self.rng.integers(8, 22)),
                "device_familiarity": float(np.clip(1.0 - (base_attack.sophistication / 10.0) + self.rng.normal(0, 0.1), 0.05, 0.85)),
                "geo_distance_km": float(abs(self.rng.normal(350.0, 180.0))),
                "behavioral_deviation": float(np.clip(0.60 + (base_attack.sophistication / 20.0), 0.25, 0.95)),
                "merchant_risk_score": merchant.merchant_risk_score,
                "account_age_days": user.account_age_days,
                "touch_pressure_deviation": float(np.clip(0.55 + self.rng.normal(0, 0.15), 0.20, 0.90)),
                "carrier_change_flag": 1 if ("SIM" in base_attack.name or "ATO-03" in base_attack.id) else 0,
                "mcc_risk_weight": merchant.mcc_risk_weight,
                "hour_of_day": int(self.rng.integers(0, 24)),
                "is_international": 1 if ("DEV-02" in base_attack.id or "Proxy" in base_attack.name) else 0,
            }

            # Apply adversarial mutation
            mutated_features = self.mutator.apply_mutation(
                base_features=base_features,
                difficulty_level=eff_difficulty,
                mutation_strength=mutation_strength
            )

            # Generate synthetic transaction record
            txn = SyntheticTransaction(
                txn_id=f"SCN-2026-{1000 + i}",
                user_id=user.user_id,
                merchant_id=merchant.merchant_id,
                device_id=f"DEV-ADV-{base_attack.id}-{i}",
                amount=round(float(mutated_features["amount"]), 2),
                velocity_1h=int(mutated_features["velocity_1h"]),
                velocity_24h=int(mutated_features["velocity_24h"]),
                device_familiarity=round(float(mutated_features["device_familiarity"]), 3),
                geo_distance_km=round(float(mutated_features["geo_distance_km"]), 2),
                behavioral_deviation=round(float(mutated_features["behavioral_deviation"]), 3),
                merchant_risk_score=float(mutated_features["merchant_risk_score"]),
                account_age_days=int(mutated_features["account_age_days"]),
                touch_pressure_deviation=round(float(mutated_features["touch_pressure_deviation"]), 3),
                carrier_change_flag=int(mutated_features["carrier_change_flag"]),
                mcc_risk_weight=float(mutated_features["mcc_risk_weight"]),
                hour_of_day=int(mutated_features["hour_of_day"]),
                is_international=int(mutated_features["is_international"]),
                is_fraud=1,
                attack_id=base_attack.id,
                attack_family=base_attack.family,
                attack_name=base_attack.name,
                difficulty=eff_difficulty,
                gen_ai=base_attack.gen_ai,
            )
            scenarios.append(txn)

        return scenarios
