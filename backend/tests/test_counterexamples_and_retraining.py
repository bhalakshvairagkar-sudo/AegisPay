"""
Tests for Targeted Counterexample Synthesis, Quality Gates, and Retraining.
"""

import pytest
import pandas as pd
import numpy as np
from backend.retraining.counterexamples import counterexample_generator
from backend.retraining.hard_example_pool import hard_example_pool
from backend.retraining.trainer import retraining_pipeline
from backend.features.data_matrix import STANDARD_FEATURE_COLUMNS


def test_counterexample_synthesis_and_quality_gates():
    dummy_centroid = {col: 0.5 for col in STANDARD_FEATURE_COLUMNS}
    counter_df, counter_y, reports = counterexample_generator.synthesize_counterexamples(
        cluster_centroids=[dummy_centroid],
        count_per_cluster=5
    )
    assert len(counter_df) == 5
    assert len(counter_y) == 5
    assert all(y == 1 for y in counter_y)
    assert all(r.is_valid_payment is True for r in reports)
    assert all(r.quality_status == "ACCEPTED" for r in reports)


def test_hard_example_pool_weighting():
    pool = hard_example_pool.__class__(max_capacity=100)
    df = pd.DataFrame([{"amount": 100.0, "velocity_1h": 2.0}], columns=["amount", "velocity_1h"])
    pool.add_counterexamples(df, difficulty_tier=4)
    x_p, y_p, w_p = pool.get_hard_examples()
    assert len(x_p) == 1
    assert w_p[0] > 1.5  # Tier 4 weight multiplier
