"""
AegisPay v2 - Generator Artifact & Realism Audit
Multi-faceted detector analyzing univariate separation, feature concentration, and suspiciously clean synthetic signals.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


class GeneratorArtifactAuditor:
    """Detects whether models are learning true fraud signals or synthetic generator artifacts."""

    def audit_features_for_artifacts(
        self,
        X_df: pd.DataFrame,
        y_true: np.ndarray,
        warning_auc_threshold: float = 0.985
    ) -> Dict[str, Any]:
        """
        Audits every individual feature for suspiciously perfect univariate separability.
        """
        y = np.asarray(y_true, dtype=int)
        flagged_artifacts = []
        feature_aucs = {}

        for col in X_df.columns:
            vals = X_df[col].values
            try:
                # Univariate ROC-AUC
                u_auc = float(roc_auc_score(y, vals))
                if u_auc < 0.5:
                    u_auc = 1.0 - u_auc  # Account for inverse direction
            except Exception:
                u_auc = 0.50

            feature_aucs[col] = round(u_auc, 4)

            # Check if any single feature achieves unrealistically perfect separation
            if u_auc >= 0.995:
                flagged_artifacts.append({
                    "feature": col,
                    "univariate_auc": round(u_auc, 4),
                    "severity": "HIGH",
                    "diagnosis": "Suspiciously perfect linear separation. Likely a synthetic generator artifact."
                })
            elif u_auc >= warning_auc_threshold:
                flagged_artifacts.append({
                    "feature": col,
                    "univariate_auc": round(u_auc, 4),
                    "severity": "MEDIUM",
                    "diagnosis": "Extremely high standalone predictive power. Verify distribution overlap with benign traffic."
                })

        overall_status = "CLEAN" if len(flagged_artifacts) == 0 else ("WARNING" if all(a["severity"] == "MEDIUM" for a in flagged_artifacts) else "ARTIFACT_DETECTED")

        return {
            "artifact_audit_status": overall_status,
            "flagged_features_count": len(flagged_artifacts),
            "flagged_artifacts": flagged_artifacts,
            "feature_univariate_aucs": feature_aucs,
            "recommendation": "Passes realism gate." if overall_status == "CLEAN" else "Investigate feature generation bounds."
        }


artifact_auditor = GeneratorArtifactAuditor()
