"""
Negative Testing Suite.
Verifies that invalid compositions, future features, impossible states, and corrupt schemas fail with structured errors.
"""

import pytest
from backend.attacks.grammar import AttackComposition
from backend.attacks.compatibility import compatibility_validator
from backend.features.temporal import assert_point_in_time_validity, FutureFeatureError, FutureLabelError
from backend.simulator.invariants.engine import invariants_engine
from backend.simulator.invariants.rules import InvariantViolationError


def test_future_feature_raises_exception():
    with pytest.raises(FutureFeatureError):
        assert_point_in_time_validity(
            feature_timestamp_epoch=2000.0,
            decision_timestamp_epoch=1000.0,
            label_timestamp_epoch=3000.0
        )


def test_impossible_lifecycle_state_rejected():
    with pytest.raises(InvariantViolationError):
        # Transaction where settlement is claimed before authorization occurred
        impossible_tx = {
            "amount": 50.0,
            "velocity_1h": 1.0,
            "velocity_24h": 2.0,
            "initiation_timestamp_epoch": 100.0,
            "authorization_timestamp_epoch": 200.0,
            "settlement_timestamp_epoch": 150.0,  # 50s before authz
            "rail": "Card"
        }
        invariants_engine.evaluate_transaction(impossible_tx, raise_on_failure=True)


def test_invalid_composition_diagnostic_rejection():
    # Mandate rail with single-message card authorization evasion
    bad_comp = AttackComposition(
        access="Credential Stuffing",
        trust="Residential Proxy",
        rail="Recurring Mandate",
        evasion="Pre-Authorization Hold Arbitrage",
        behavior="Zero Hesitation Navigation",
        monetization="Card Not Present Checkout",
        temporal_pattern="Micro-Pacing"
    )
    res = compatibility_validator.validate(bad_comp)
    assert res.is_executable is False
    assert len(res.diagnostic_rejection_reasons) > 0
