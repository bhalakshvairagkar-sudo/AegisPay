"""
Tests for 3-Arm Controlled Loop Evaluation and Operational Capacity Curves.
"""

import pytest
import numpy as np
from backend.evaluation.control_arms import controlled_loop_evaluator
from backend.evaluation.capacity import capacity_evaluator


def test_control_arms_contribution():
    res = controlled_loop_evaluator.evaluate_control_arms()
    assert "control_arm_a" in res
    assert "control_arm_b" in res
    assert "treatment_aegispay" in res
    assert "loop_contributions" in res

    # Treatment (Adaptive loop) must outperform static baseline in PR-AUC and holdout recall
    pr_gain = res["loop_contributions"]["pr_auc_gain_vs_static_baseline"]
    assert pr_gain > 0.15  # At least +15 pp


def test_capacity_curve_evaluation():
    np.random.seed(42)
    y_test = np.random.binomial(1, 0.20, 200)
    probs = np.random.uniform(0.0, 1.0, 200)
    cap_res = capacity_evaluator.evaluate_capacity_metrics(y_test, probs)
    assert "operational_analyst_count" in cap_res
    assert "capacity_curve" in cap_res
    assert len(cap_res["capacity_curve"]) == 10
