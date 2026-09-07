"""
Tests for 6-Tier Generalization Lab and Retention % Computation.
"""

import pytest
from backend.evaluation.generalization import generalization_lab


def test_6_tier_generalization_hierarchy():
    res = generalization_lab.evaluate_holdouts(model=None, known_baseline_recall_pct=95.0)
    assert "known_baseline_recall_pct" in res
    assert "mean_generalization_retention_pct" in res
    tiers = res["tier_results"]
    assert len(tiers) == 6
    tier_ids = [t["tier_id"] for t in tiers]
    assert tier_ids == ["TIER-A", "TIER-B", "TIER-C", "TIER-D", "TIER-E", "TIER-F"]
    for t in tiers:
        assert 0.0 <= t["retention_pct"] <= 100.0
        assert t["generalization_gap_pct"] >= 0.0
