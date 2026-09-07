"""
Tests for Semantic Invariant Build Gates.
"""

import pytest
from backend.simulator.invariants.engine import invariants_engine
from backend.simulator.invariants.rules import InvariantViolationError


def test_positive_amount_invariant_passes():
    valid_tx = {"amount": 45.50, "velocity_1h": 1.0, "velocity_24h": 2.0, "device_familiarity": 0.8, "behavioral_deviation": 0.1, "rail": "Card"}
    is_valid, violations = invariants_engine.evaluate_transaction(valid_tx)
    assert is_valid is True
    assert len(violations) == 0


def test_negative_amount_fails_invariant():
    invalid_tx = {"amount": -10.0, "velocity_1h": 1.0, "velocity_24h": 2.0, "device_familiarity": 0.8, "behavioral_deviation": 0.1, "rail": "Card"}
    is_valid, violations = invariants_engine.evaluate_transaction(invalid_tx)
    assert is_valid is False
    assert any(v["invariant_id"] == "INV-F01" for v in violations)


def test_temporal_monotonicity_violation():
    time_travel_tx = {
        "amount": 100.0,
        "velocity_1h": 1.0,
        "velocity_24h": 2.0,
        "initiation_timestamp_epoch": 1000.0,
        "authorization_timestamp_epoch": 900.0,  # 100s before initiation
        "device_familiarity": 0.8,
        "behavioral_deviation": 0.1,
        "rail": "UPI"
    }
    is_valid, violations = invariants_engine.evaluate_transaction(time_travel_tx)
    assert is_valid is False
    assert any(v["invariant_id"] == "INV-T01" for v in violations)


def test_build_gate_raises_exception():
    bad_tx = {"amount": 0.0}
    with pytest.raises(InvariantViolationError):
        invariants_engine.evaluate_transaction(bad_tx, raise_on_failure=True)
