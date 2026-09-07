"""
AegisPay v2 - Unified Rail-Aware Decision Engine
Integrates structural guards, model scoring, calibration, confidence, reason codes, and rail-aware policies.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import numpy as np

from backend.defense.structural_guards import structural_guards, StructuralGuardResult
from backend.models.calibration import calibration_engine
from backend.defense.confidence import confidence_estimator
from backend.defense.reason_codes import map_features_to_reason_codes, REASON_CODES
from backend.simulator.rails.upi import UPIPaymentRail
from backend.simulator.rails.card import CardPaymentRail
from backend.simulator.rails.a2a import A2APaymentRail
from backend.simulator.rails.wallet import WalletPaymentRail
from backend.simulator.rails.mandate import RecurringMandateRail


RAIL_MAP = {
    "UPI": UPIPaymentRail(),
    "Card": CardPaymentRail(),
    "A2A": A2APaymentRail(),
    "Wallet": WalletPaymentRail(),
    "Recurring Mandate": RecurringMandateRail()
}


@dataclass
class DefenseDecision:
    action: str  # ALLOW, FRICTION, REVIEW, BLOCK
    rail_directive: str  # e.g. CARD_MANDATORY_EMV_3DS_CHALLENGE, UPI_COOLING_OFF_4H_HOLD
    calibrated_fraud_risk: float  # 0.0 to 1.0
    unified_risk_score_100: float  # 0.0 to 100.0
    confidence_level: str  # HIGH, MEDIUM, LOW
    confidence_score: float  # 0.0 to 1.0
    reason_codes: List[str]
    primary_reason_description: str
    structural_guard_intercepted: bool
    latency_ms: float = 0.85


class UnifiedDecisionEngine:
    """Orchestrates end-to-end payment risk evaluation and rail-aware policy enforcement."""

    def __init__(
        self,
        allow_threshold: float = 0.25,
        friction_threshold: float = 0.55,
        block_threshold: float = 0.80
    ):
        self.allow_th = allow_threshold
        self.friction_th = friction_threshold
        self.block_th = block_threshold

    def evaluate_transaction(
        self,
        feature_dict: Dict[str, Any],
        model_scores: Dict[str, float],
        rail: str = "Card",
        raw_model_prob: float = 0.50
    ) -> DefenseDecision:
        """Executes full defensive decision pipeline."""
        # 1. Evaluate Pre-ML Structural Guards
        guard_res = structural_guards.evaluate_transaction(feature_dict)
        if guard_res.is_blocked_by_guard:
            rail_obj = RAIL_MAP.get(rail, CardPaymentRail())
            policy_act = rail_obj.map_risk_action("BLOCK", guard_res.reason_code or "R17")
            return DefenseDecision(
                action="BLOCK",
                rail_directive=policy_act.rail_specific_directive,
                calibrated_fraud_risk=1.00,
                unified_risk_score_100=100.0,
                confidence_level="HIGH",
                confidence_score=1.0,
                reason_codes=[guard_res.reason_code or "R17"],
                primary_reason_description=guard_res.explanation or "Blocked by pre-ML structural security guard.",
                structural_guard_intercepted=True,
                latency_ms=0.20
            )

        # 2. Probability Calibration
        cal_prob = float(calibration_engine.predict_proba(np.array([raw_model_prob]))[0])

        # 3. Confidence & Abstention
        conf_level, conf_score, should_abstain = confidence_estimator.estimate_confidence(cal_prob, model_scores)

        # 4. Determine Action Tier
        if should_abstain:
            action = "REVIEW"
        elif cal_prob >= self.block_th:
            action = "BLOCK"
        elif cal_prob >= self.friction_th:
            action = "FRICTION"
        elif cal_prob >= self.allow_th:
            action = "REVIEW"
        else:
            action = "ALLOW"

        # 5. Map to Reason Codes & Rail-Specific Directives
        codes = map_features_to_reason_codes(feature_dict, cal_prob)
        primary_code = codes[0] if codes else "R20"
        code_def = REASON_CODES.get(primary_code)
        desc = code_def.description if code_def else "Standard policy evaluation."

        rail_obj = RAIL_MAP.get(rail, CardPaymentRail())
        policy_act = rail_obj.map_risk_action(action, primary_code)

        return DefenseDecision(
            action=action,
            rail_directive=policy_act.rail_specific_directive,
            calibrated_fraud_risk=round(cal_prob, 4),
            unified_risk_score_100=round(cal_prob * 100.0, 1),
            confidence_level=conf_level,
            confidence_score=conf_score,
            reason_codes=codes,
            primary_reason_description=desc,
            structural_guard_intercepted=False,
            latency_ms=0.85
        )


decision_engine = UnifiedDecisionEngine()
