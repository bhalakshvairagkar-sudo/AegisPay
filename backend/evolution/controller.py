"""
AegisPay v2 - Evolutionary Campaign Controller
Orchestrates sequential attack-defense rounds (R1 -> R2 -> R3 -> R4) tracking evasion rates and model evolution.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import numpy as np


@dataclass
class EvolutionaryRoundLog:
    round_index: int
    round_name: str
    active_defense_model: str
    difficulty_tier: int
    attack_samples_generated: int
    evasion_rate_pct: float
    detection_rate_pct: float
    blind_spots_discovered: int
    counterexamples_synthesized: int
    retrained_model_promoted: str


class EvolutionaryCampaignController:
    """Manages multi-round evolutionary campaigns and records honest empirical progression."""

    def __init__(self):
        self.round_history: List[EvolutionaryRoundLog] = []

    def record_round(
        self,
        round_index: int,
        active_model: str,
        difficulty: int,
        total_attacks: int,
        detected_count: int,
        blind_spots: int,
        counterexamples: int,
        next_model: str
    ) -> EvolutionaryRoundLog:
        """Logs a completed round of offense vs defense."""
        det_pct = round((detected_count / max(1, total_attacks)) * 100, 2)
        ev_pct = round(100.0 - det_pct, 2)

        log = EvolutionaryRoundLog(
            round_index=round_index,
            round_name=f"Round {round_index} (Tier {difficulty})",
            active_defense_model=active_model,
            difficulty_tier=difficulty,
            attack_samples_generated=total_attacks,
            evasion_rate_pct=ev_pct,
            detection_rate_pct=det_pct,
            blind_spots_discovered=blind_spots,
            counterexamples_synthesized=counterexamples,
            retrained_model_promoted=next_model
        )
        self.round_history.append(log)
        return log

    def get_timeline(self) -> List[Dict[str, Any]]:
        return [
            {
                "round_index": r.round_index,
                "round_name": r.round_name,
                "active_model": r.active_defense_model,
                "difficulty_tier": r.difficulty_tier,
                "total_attacks": r.attack_samples_generated,
                "evasion_rate_pct": r.evasion_rate_pct,
                "detection_rate_pct": r.detection_rate_pct,
                "blind_spots_count": r.blind_spots_discovered,
                "counterexamples_count": r.counterexamples_synthesized,
                "promoted_model": r.retrained_model_promoted
            }
            for r in self.round_history
        ]


evolution_controller = EvolutionaryCampaignController()
