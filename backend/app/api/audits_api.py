"""
AegisPay v2 - Self-Audit & Feature Provenance API Router
"""

from fastapi import APIRouter
import pandas as pd
import numpy as np

from backend.audits.leakage import audit_leakage_engine
from backend.audits.generator_artifacts import artifact_auditor
from backend.features.provenance import provenance_engine
from backend.features.data_matrix import STANDARD_FEATURE_COLUMNS


router = APIRouter(tags=["Self-Audit & Provenance"])


@router.get("/audits")
def get_self_audit_report():
    # 1. Leakage Gates Evaluation
    leakage_report = audit_leakage_engine.run_full_audit(
        feature_columns=STANDARD_FEATURE_COLUMNS,
        train_entities=["USER-101", "USER-102", "DEV-501"],
        test_entities=["USER-999", "DEV-999"],  # Sealed holdout
        temporal_valid=True
    )

    # 2. Generator Artifact Audit
    np.random.seed(42)
    sample_df = pd.DataFrame(
        np.random.uniform(0.1, 1.0, size=(200, len(STANDARD_FEATURE_COLUMNS))),
        columns=STANDARD_FEATURE_COLUMNS
    )
    y_synth = np.random.binomial(1, 0.3, 200)
    artifact_report = artifact_auditor.audit_features_for_artifacts(sample_df, y_synth)

    # 3. Provenance Manifest
    prov_manifest = provenance_engine.get_provenance_manifest()

    return {
        "leakage_gates_status": leakage_report["overall_audit_status"],
        "leakage_audit": leakage_report,
        "generator_artifact_audit": artifact_report,
        "feature_provenance_manifest": prov_manifest
    }
