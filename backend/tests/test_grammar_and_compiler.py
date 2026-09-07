"""
Tests for 7-Slot Typed Attack Grammar, Semantic Compatibility Validator, and Attack Compiler.
"""

import pytest
from backend.attacks.grammar import AttackComposition
from backend.attacks.compatibility import compatibility_validator
from backend.attacks.compiler import attack_compiler
from backend.attacks.primitives import ATTACK_PRIMITIVES


def test_valid_primitive_compilation():
    scenario, val_res = attack_compiler.compile_from_primitive("ATO-01", difficulty=3)
    assert scenario is not None
    assert val_res.is_type_valid is True
    assert val_res.is_semantic_valid is True
    assert val_res.is_executable is True
    assert scenario.difficulty_level == 3
    assert scenario.target_rail == "UPI"


def test_invalid_type_rejection():
    invalid_comp = AttackComposition(
        access="NON_EXISTENT_ACCESS",
        trust="Residential Proxy",
        rail="Card",
        evasion="Temporal Pacing",
        behavior="Synthetic Cadence",
        monetization="P2P Transfer",
        temporal_pattern="Micro-Pacing"
    )
    val_res = compatibility_validator.validate(invalid_comp)
    assert val_res.is_type_valid is False
    assert val_res.is_executable is False
    assert any("NON_EXISTENT_ACCESS" in r for r in val_res.diagnostic_rejection_reasons)


def test_semantic_rail_conflict_rejection():
    # Card rail attempting P2P direct wallet drain
    conflicting_comp = AttackComposition(
        access="Credential Stuffing",
        trust="Residential Proxy",
        rail="Card",
        evasion="Temporal Pacing",
        behavior="Synthetic Cadence",
        monetization="P2P Wallet Drain",
        temporal_pattern="Micro-Pacing"
    )
    val_res = compatibility_validator.validate(conflicting_comp)
    assert val_res.is_semantic_valid is False
    assert val_res.is_executable is False
    assert any("P2P Wallet Drain" in r for r in val_res.diagnostic_rejection_reasons)
