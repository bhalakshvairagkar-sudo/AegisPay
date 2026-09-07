"""
AegisPay v2 - Failure Attribution Taxonomy
Distinguishes model blind spots from generator artifacts, simulator limitations, and label delays.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class FailureAttribution:
    failure_type: str  # MODEL_BLIND_SPOT, GENERATOR_ARTIFACT, SIMULATOR_LIMITATION, FEATURE_LIMITATION, LABEL_MATURITY_DELAY
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    root_cause: str
    recommended_remedy: str
    is_adversarial_candidate: bool


def attribute_evasion_failure(
    attack_info: Dict[str, Any],
    feature_dict: Dict[str, Any],
    model_score: float,
    decision_threshold: float = 0.50
) -> FailureAttribution:
    """Attributes the root cause of an undetected fraud transaction."""
    amt = float(feature_dict.get("amount", 0.0))
    v1 = float(feature_dict.get("velocity_1h", 1.0))
    df = float(feature_dict.get("device_familiarity", 0.7))
    bd = float(feature_dict.get("behavioral_deviation", 0.1))

    # 1. Feature limitation (signals completely in legitimate baseline range)
    if 0.35 <= df <= 0.85 and bd < 0.25 and v1 <= 2.0:
        return FailureAttribution(
            failure_type="FEATURE_LIMITATION",
            severity="HIGH",
            root_cause="Attack parameters perfectly mimic cardholder historical baseline, leaving no observable anomaly in standard telemetry.",
            recommended_remedy="Incorporate relational graph fan-out and multi-hop beneficiary signals into detection matrix.",
            is_adversarial_candidate=True
        )

    # 2. Generator artifact
    if amt <= 0.50 and v1 >= 40.0:
        return FailureAttribution(
            failure_type="GENERATOR_ARTIFACT",
            severity="LOW",
            root_cause="Synthetic generator produced an extreme edge-case parameter combination unrepresentative of production traffic.",
            recommended_remedy="Refine generator constraint bounds and apply semantic invariant filtering.",
            is_adversarial_candidate=False
        )

    # 3. Model blind spot (clear anomalies present, but model weights failed to trigger policy)
    if model_score < decision_threshold and (v1 > 4.0 or df < 0.20 or bd > 0.60):
        return FailureAttribution(
            failure_type="MODEL_BLIND_SPOT",
            severity="CRITICAL",
            root_cause="Observable anomalous signals (velocity/device/deviation) were present but the decision tree weights under-weighted their interaction.",
            recommended_remedy="Synthesize centroid counterexamples and execute sample-weighted adversarial retraining.",
            is_adversarial_candidate=True
        )

    return FailureAttribution(
        failure_type="MODEL_BLIND_SPOT",
        severity="MEDIUM",
        root_cause="Subtle feature interaction bypassed current linear/tree boundary partition.",
        recommended_remedy="Targeted boundary synthesis in adversarial retraining.",
        is_adversarial_candidate=True
    )
