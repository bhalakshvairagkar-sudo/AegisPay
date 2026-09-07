"""
Tests for Deterministic Reproducibility.
Runs identical seeded runs and verifies bit-for-bit / manifest consistency.
"""

import pytest
import numpy as np
from backend.attacks.mutations import AttackMutator
from backend.attacks.grammar import AttackComposition
from backend.attacks.primitives import ATTACK_PRIMITIVES


def test_identical_seed_produces_identical_features():
    comp = AttackComposition(
        access="Credential Stuffing",
        trust="Residential Proxy",
        rail="UPI",
        evasion="Temporal Pacing",
        behavior="Synthetic Cadence",
        monetization="P2P Transfer",
        temporal_pattern="Micro-Pacing",
        family="Account Takeover",
        vector="ATO-01",
        difficulty=3,
        seed=42
    )
    base = {"amount": 50.0, "velocity_1h": 1.0, "velocity_24h": 2.0}

    mutator_1 = AttackMutator(seed=42)
    feat_1 = mutator_1.mutate_transaction_features(base, comp)

    mutator_2 = AttackMutator(seed=42)
    feat_2 = mutator_2.mutate_transaction_features(base, comp)

    assert feat_1 == feat_2
    assert feat_1["amount"] == feat_2["amount"]
    assert feat_1["behavioral_deviation"] == feat_2["behavioral_deviation"]
