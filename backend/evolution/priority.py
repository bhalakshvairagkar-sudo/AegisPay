"""
AegisPay v2 - Normalized Attack Priority Score Engine
Calculates mathematically principled priority rankings for candidate attacks combining exploitation and exploration.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
import numpy as np


@dataclass
class PriorityWeights:
    w_blindspot: float = 0.30
    w_novelty: float = 0.15
    w_impact: float = 0.15
    w_fidelity: float = 0.10
    w_evasion: float = 0.10
    w_diversity: float = 0.10
    w_exploration: float = 0.10

    def assert_normalized(self):
        total = sum([
            self.w_blindspot, self.w_novelty, self.w_impact,
            self.w_fidelity, self.w_evasion, self.w_diversity,
            self.w_exploration
        ])
        assert abs(total - 1.0) < 1e-4, f"Priority weights must sum to 1.0, got {total}"


class AttackPriorityEngine:
    """Calculates prioritized sampling scores for candidate attacks."""

    def __init__(self, weights: Optional[PriorityWeights] = None):
        self.weights = weights or PriorityWeights()
        self.weights.assert_normalized()

    def compute_priority(
        self,
        blind_spot_score: float,      # 0.0 to 1.0 (from failure clustering)
        novelty_score: float,         # 0.0 to 1.0 (repertoire distance)
        impact_score: float,          # 0.0 to 1.0 (financial/regulatory severity)
        fidelity_score_pct: float,    # 0.0 to 100.0 (semantic validity)
        historical_evasion: float,    # 0.0 to 1.0 (historical success rate)
        diversity_bonus: float,       # 0.0 to 1.0 (family/rail balance)
        is_unexplored: bool = False   # 20% exploration bonus
    ) -> Dict[str, float]:
        """
        Priority = w1*BlindSpot + w2*Novelty + w3*Impact + w4*Fidelity + w5*Evasion + w6*Diversity + w7*Exploration
        """
        fid_norm = min(1.0, max(0.0, fidelity_score_pct / 100.0))
        expl_val = 1.0 if is_unexplored else 0.0

        p = (
            self.weights.w_blindspot * blind_spot_score +
            self.weights.w_novelty * novelty_score +
            self.weights.w_impact * impact_score +
            self.weights.w_fidelity * fid_norm +
            self.weights.w_evasion * historical_evasion +
            self.weights.w_diversity * diversity_bonus +
            self.weights.w_exploration * expl_val
        )

        return {
            "composite_priority_score": round(float(np.clip(p, 0.0, 1.0)), 4),
            "blind_spot_component": round(self.weights.w_blindspot * blind_spot_score, 4),
            "novelty_component": round(self.weights.w_novelty * novelty_score, 4),
            "impact_component": round(self.weights.w_impact * impact_score, 4),
            "fidelity_component": round(self.weights.w_fidelity * fid_norm, 4),
            "evasion_component": round(self.weights.w_evasion * historical_evasion, 4),
            "diversity_component": round(self.weights.w_diversity * diversity_bonus, 4),
            "exploration_component": round(self.weights.w_exploration * expl_val, 4)
        }


priority_engine = AttackPriorityEngine()
