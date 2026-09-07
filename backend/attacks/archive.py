"""
AegisPay v2 - Quality-Diversity (QD) Attack Archive
Maintains a 2D behavioral repertoire grid (Novelty vs Detector Difficulty) storing the highest-evasion attacks found.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
import numpy as np


@dataclass
class ArchiveCell:
    novelty_bin: int  # 0 to 4 (e.g. 5 bins)
    difficulty_bin: int  # 0 to 4 (Difficulty 1 to 5)
    best_evasion_score: float = 0.0  # 1.0 - detector_probability (higher = harder evasion)
    attack_composition: Optional[Dict[str, Any]] = None
    attack_id: Optional[str] = None
    failure_density: int = 0  # Count of false negatives falling into this cell
    occupied: bool = False


class QualityDiversityArchive:
    """Quality-Diversity repertoire tracking coverage of novel and evasive attack behaviors."""

    def __init__(self, novelty_bins: int = 5, difficulty_bins: int = 5):
        self.num_novelty_bins = novelty_bins
        self.num_diff_bins = difficulty_bins
        self.grid: Dict[Tuple[int, int], ArchiveCell] = {}
        self._init_grid()

    def _init_grid(self):
        for n in range(self.num_novelty_bins):
            for d in range(self.num_diff_bins):
                self.grid[(n, d)] = ArchiveCell(novelty_bin=n, difficulty_bin=d)

    def _compute_novelty_bin(self, composition_dict: Dict[str, Any]) -> int:
        """Determines behavioral novelty bin from composition hash and behavioral deviation."""
        # Map behavioral novelty into 0..4
        slots = composition_dict.get("slots", {})
        h = sum(ord(c) for c in slots.get("behavior", "") + slots.get("evasion", ""))
        return h % self.num_novelty_bins

    def _compute_diff_bin(self, difficulty: int) -> int:
        """Maps difficulty 1..5 into bin 0..4."""
        return int(np.clip(difficulty - 1, 0, self.num_diff_bins - 1))

    def update(
        self,
        attack_id: str,
        composition: Dict[str, Any],
        difficulty: int,
        detector_fraud_prob: float,
        is_false_negative: bool
    ) -> bool:
        """Attempts to insert or update an attack in the QD archive."""
        n_bin = self._compute_novelty_bin(composition)
        d_bin = self._compute_diff_bin(difficulty)

        evasion_score = round(1.0 - detector_fraud_prob, 4)
        cell = self.grid[(n_bin, d_bin)]

        is_improved = False
        if is_false_negative:
            cell.failure_density += 1

        if not cell.occupied or evasion_score > cell.best_evasion_score:
            cell.occupied = True
            cell.best_evasion_score = evasion_score
            cell.attack_id = attack_id
            cell.attack_composition = composition
            is_improved = True

        return is_improved

    def get_stats(self) -> Dict[str, Any]:
        """Calculates measured QD metrics."""
        total_cells = len(self.grid)
        occupied_cells = sum(1 for c in self.grid.values() if c.occupied)
        total_failures = sum(c.failure_density for c in self.grid.values())
        mean_evasion = float(np.mean([c.best_evasion_score for c in self.grid.values() if c.occupied])) if occupied_cells > 0 else 0.0

        grid_matrix = []
        for d in range(self.num_diff_bins - 1, -1, -1):  # High difficulty at top
            row = []
            for n in range(self.num_novelty_bins):
                c = self.grid[(n, d)]
                row.append({
                    "novelty_bin": n,
                    "difficulty_bin": d,
                    "occupied": c.occupied,
                    "best_evasion_score": c.best_evasion_score,
                    "failure_density": c.failure_density,
                    "attack_id": c.attack_id
                })
            grid_matrix.append(row)

        return {
            "total_cells": total_cells,
            "occupied_cells": occupied_cells,
            "archive_coverage_pct": round((occupied_cells / total_cells) * 100, 2),
            "total_failures_indexed": total_failures,
            "mean_evasion_score": round(mean_evasion, 4),
            "grid": grid_matrix
        }


qd_archive = QualityDiversityArchive()
