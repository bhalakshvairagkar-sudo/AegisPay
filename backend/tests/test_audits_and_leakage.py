"""
Tests for 8 Self-Audit Leakage Build Gates, Artifact Auditor, and Feature Provenance.
"""

import pytest
import pandas as pd
import numpy as np
from backend.audits.leakage import audit_leakage_engine
from backend.audits.generator_artifacts import artifact_auditor
from backend.features.provenance import provenance_engine
from backend.features.data_matrix import STANDARD_FEATURE_COLUMNS


def test_clean_features_pass_leakage_audit():
    res = audit_leakage_engine.run_full_audit(
        feature_columns=STANDARD_FEATURE_COLUMNS,
        train_entities=["USER-1", "DEV-1"],
        test_entities=["USER-9", "DEV-9"]
    )
    assert res["overall_audit_status"] == "PASS"
    assert res["failed_gates_count"] == 0


def test_label_leakage_fails_audit():
    dirty_columns = STANDARD_FEATURE_COLUMNS + ["is_fraud"]
    res = audit_leakage_engine.run_full_audit(
        feature_columns=dirty_columns,
        train_entities=["USER-1"],
        test_entities=["USER-2"]
    )
    assert res["overall_audit_status"] == "BLOCKED"
    assert res["failed_gates_count"] > 0


def test_feature_provenance_manifest():
    manifest = provenance_engine.get_provenance_manifest()
    assert len(manifest) == 13
    assert all(r["decision_time_valid"] is True for r in manifest)
    assert all(r["uses_fraud_label"] is False for r in manifest)
