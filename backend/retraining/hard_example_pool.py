"""
AegisPay v2 - Hard Example Pool Management
Maintains high-priority adversarial counterexamples with difficulty and recency weighting.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np


class HardExamplePool:
    """Manages accumulated hard adversarial counter-samples with sample weighting."""

    def __init__(self, max_capacity: int = 2000):
        self.max_capacity = max_capacity
        self.pool_df = pd.DataFrame()
        self.pool_weights = np.array([])
        self.pool_metadata: List[Dict[str, Any]] = []

    def add_counterexamples(
        self,
        new_df: pd.DataFrame,
        difficulty_tier: int = 4,
        round_index: int = 1
    ):
        """Appends new counterexamples with severity and difficulty weighting."""
        if len(new_df) == 0:
            return

        # Base weight: Harder examples get higher loss weighting (Tier 4=2.0x, Tier 5=3.0x)
        weight_mult = 1.0 + (difficulty_tier * 0.4)
        new_weights = np.full(len(new_df), fill_value=weight_mult)

        if len(self.pool_df) == 0:
            self.pool_df = new_df.copy()
            self.pool_weights = new_weights
        else:
            self.pool_df = pd.concat([self.pool_df, new_df], ignore_index=True)
            self.pool_weights = np.concatenate([self.pool_weights, new_weights])

        # Enforce capacity
        if len(self.pool_df) > self.max_capacity:
            self.pool_df = self.pool_df.iloc[-self.max_capacity:].reset_index(drop=True)
            self.pool_weights = self.pool_weights[-self.max_capacity:]

    def get_hard_examples(self) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
        """Returns (X_counter, y_counter, sample_weights)."""
        if len(self.pool_df) == 0:
            return pd.DataFrame(), np.array([]), np.array([])
        y = np.ones(len(self.pool_df), dtype=int)
        return self.pool_df.copy(), y, self.pool_weights.copy()


hard_example_pool = HardExamplePool()
