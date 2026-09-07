"""
AegisPay v2 - "Why Did the Model Fail?" Explainability Engine
Generates deep failure attribution cards for missed attacks with decision boundary and missing signal diagnostics.
"""

from typing import Dict, Any, List, Optional
from backend.gap_analysis.failure_taxonomy import attribute_evasion_failure, FailureAttribution


def explain_missed_attack(
    scenario_dict: Dict[str, Any],
    feature_dict: Dict[str, Any],
    model_score: float,
    threshold: float = 0.50
) -> Dict[str, Any]:
    """Generates an operational 'Why Did the Model Fail?' diagnostic card for an evasion."""
    attribution = attribute_evasion_failure(scenario_dict, feature_dict, model_score, threshold)

    # Identify top missing signals
    missing_signals = []
    if float(feature_dict.get("device_familiarity", 1.0)) > 0.60:
        missing_signals.append("Device Familiarity Mimicry (Attacker used legitimate device/proxy, dampening device risk signal).")
    if float(feature_dict.get("velocity_1h", 1.0)) <= 2.0:
        missing_signals.append("Low Velocity Masking (Attacker throttled submission rate below velocity alert floor).")
    if float(feature_dict.get("behavioral_deviation", 0.0)) <= 0.30:
        missing_signals.append("Cadence Jitter Matching (Biometric touch/keystroke deviation stayed within 1-sigma of baseline).")
    if not missing_signals:
        missing_signals.append("High-Dimensional Non-Linear Masking (Features individually normal, combination evaded partition).")

    return {
        "attack_id": scenario_dict.get("attack_id", "ATT-UNKNOWN"),
        "attack_name": scenario_dict.get("name", "Unknown Vector"),
        "family": scenario_dict.get("family", "Unknown Family"),
        "rail": scenario_dict.get("rail", "Card"),
        "difficulty": scenario_dict.get("difficulty", "Adversarial"),
        "model_risk_score": round(model_score * 100.0, 1),
        "policy_threshold": round(threshold * 100.0, 1),
        "evasion_margin_score": round((threshold - model_score) * 100.0, 1),
        "failure_attribution": {
            "failure_type": attribution.failure_type,
            "severity": attribution.severity,
            "root_cause": attribution.root_cause,
            "remedy": attribution.recommended_remedy
        },
        "top_missing_signals": missing_signals,
        "counterexample_strategy": (
            f"Synthesize {attribution.severity.lower()}-priority boundary counterexamples around centroid "
            f"with perturbed {scenario_dict.get('family', 'threat')} parameters."
        )
    }
