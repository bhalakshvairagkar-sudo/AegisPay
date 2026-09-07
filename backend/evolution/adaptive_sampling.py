"""
AegisPay v2 - Closed-Loop Adaptive Red Team Sampler
Shifts attack generation probability distribution toward detector blind spots while preserving exploration.
"""

from typing import Dict, Any, List, Tuple
import numpy as np

from backend.attacks.primitives import ATTACK_PRIMITIVES, AttackPrimitive
from backend.attacks.grammar import AttackComposition, PAYMENT_RAILS
from backend.evolution.priority import priority_engine, PriorityWeights
from backend.gap_analysis.clustering import EvasionCluster


class AdaptiveRedTeamSampler:
    """Adaptive attack generator shifting probability distribution to detector weaknesses."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.rng = np.random.RandomState(seed)
        self.primitives = list(ATTACK_PRIMITIVES.values())
        self.sampling_weights = np.ones(len(self.primitives), dtype=float) / len(self.primitives)

    def update_sampling_distribution(
        self,
        clusters: List[EvasionCluster],
        unexplored_primitives: List[str]
    ):
        """
        Calculates new priority scores for each primitive and normalizes into sampling probabilities.
        """
        new_scores = []
        for prim in self.primitives:
            # 1. Match against identified evasion clusters
            matched_blindspot = 0.0
            for c in clusters:
                if c.dominant_attack_family == prim.family:
                    matched_blindspot = max(matched_blindspot, c.blind_spot_score)

            is_unexplored = (prim.primitive_id in unexplored_primitives)
            impact = 0.85 if prim.family in ["AI Adaptive Fraud", "Identity & Synthetic Fraud", "Account Takeover"] else 0.50

            p_dict = priority_engine.compute_priority(
                blind_spot_score=matched_blindspot,
                novelty_score=0.70 if is_unexplored else 0.30,
                impact_score=impact,
                fidelity_score_pct=95.0,
                historical_evasion=0.60 if matched_blindspot > 0 else 0.15,
                diversity_bonus=0.50,
                is_unexplored=is_unexplored
            )
            new_scores.append(p_dict["composite_priority_score"])

        scores_arr = np.array(new_scores, dtype=float)
        # Apply Softmax with temperature 0.5 to sharpen focus on high-priority targets
        exp_s = np.exp(scores_arr / 0.5)
        self.sampling_weights = exp_s / np.sum(exp_s)

    def sample_attack_campaign(
        self,
        count: int = 100,
        difficulty: int = 3
    ) -> List[AttackComposition]:
        """Draws candidate attack compositions according to the adaptive probability distribution."""
        selected_prims = self.rng.choice(self.primitives, size=count, p=self.sampling_weights)
        campaign: List[AttackComposition] = []

        for p in selected_prims:
            # Choose rail: 80% default rail, 20% cross-rail exploration
            rail = p.default_rail if self.rng.rand() > 0.20 else self.rng.choice(PAYMENT_RAILS)
            comp = AttackComposition(
                access=p.default_access,
                trust=p.default_trust,
                rail=rail,
                evasion=p.default_evasion,
                behavior=p.default_behavior,
                monetization=p.default_monetization,
                temporal_pattern=p.default_temporal,
                family=p.family,
                vector=p.primitive_id,
                difficulty=difficulty,
                seed=int(self.rng.randint(1000, 999999)),
                provenance="MEASURED"
            )
            campaign.append(comp)

        return campaign


adaptive_sampler = AdaptiveRedTeamSampler()
