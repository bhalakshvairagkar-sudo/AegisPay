"""
Tests for Structural Guards, Calibration, Cost Optimization, and Reason Codes.
"""

import pytest
import numpy as np
from backend.defense.structural_guards import structural_guards
from backend.defense.decision_engine import decision_engine
from backend.defense.reason_codes import map_features_to_reason_codes
from backend.defense.cost_model import cost_engine


def test_structural_guard_blocks_excessive_amount():
    extreme_tx = {"amount": 500000.0, "rail": "Card"}
    guard_res = structural_guards.evaluate_transaction(extreme_tx)
    assert guard_res.is_blocked_by_guard is True
    assert guard_res.reason_code == "R17"


def test_decision_engine_rail_directive():
    tx = {
        "amount": 250.0,
        "velocity_1h": 1.0,
        "velocity_24h": 2.0,
        "device_familiarity": 0.8,
        "geo_distance_km": 5.0,
        "behavioral_deviation": 0.1,
        "merchant_risk_score": 0.2,
        "account_age_days": 180,
        "touch_pressure_deviation": 0.1,
        "carrier_change_flag": 0,
        "mcc_risk_weight": 0.2,
        "hour_of_day": 14,
        "is_international": 0
    }
    dec = decision_engine.evaluate_transaction(
        feature_dict=tx,
        model_scores={"xgboost": 0.10, "isolation_forest": 0.12},
        rail="Card",
        raw_model_prob=0.10
    )
    assert dec.action == "ALLOW"
    assert dec.rail_directive == "CARD_FRICTIONLESS_AUTHORIZE"
    assert "R20" in dec.reason_codes


def test_reason_code_mapping():
    risky_tx = {
        "amount": 4000.0,
        "velocity_1h": 8.0,
        "device_familiarity": 0.1,
        "device_account_fanout": 4
    }
    codes = map_features_to_reason_codes(risky_tx, calibrated_prob=0.85)
    assert "R02" in codes  # Device fanout
    assert "R01" in codes  # New device
    assert "R03" in codes  # Abnormal velocity
