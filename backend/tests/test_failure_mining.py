"""
Tests for False Negative Mining, Cluster Stability Analysis, and Explain Failure.
"""

import pytest
import pandas as pd
import numpy as np
from backend.gap_analysis.clustering import cluster_analyzer
from backend.gap_analysis.false_negatives import fn_extractor
from backend.gap_analysis.explain_failure import explain_missed_attack
from backend.features.data_matrix import STANDARD_FEATURE_COLUMNS


def test_cluster_stability_evaluation():
    np.random.seed(42)
    # Generate 50 points with 3 clear clusters
    data = np.vstack([
        np.random.normal(0, 0.2, (20, len(STANDARD_FEATURE_COLUMNS))),
        np.random.normal(3, 0.2, (20, len(STANDARD_FEATURE_COLUMNS))),
        np.random.normal(6, 0.2, (10, len(STANDARD_FEATURE_COLUMNS)))
    ])
    df = pd.DataFrame(data, columns=STANDARD_FEATURE_COLUMNS)
    norm = fn_extractor.scaler.fit_transform(df)

    optimal_k, stability = cluster_analyzer.find_optimal_k(norm, k_range=range(3, 6))
    assert optimal_k in [3, 4, 5]
    assert "best_silhouette" in stability


def test_explain_missed_attack():
    scen = {"attack_id": "ATO-01", "name": "Credential Stuffing", "family": "Account Takeover", "rail": "UPI", "difficulty": "Adversarial"}
    feat = {"amount": 500.0, "velocity_1h": 1.0, "device_familiarity": 0.85, "behavioral_deviation": 0.15}
    card = explain_missed_attack(scen, feat, model_score=0.38, threshold=0.50)
    assert card["attack_id"] == "ATO-01"
    assert "top_missing_signals" in card
    assert card["evasion_margin_score"] > 0.0
