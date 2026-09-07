"""
AegisPay v2 - Attack Semantic Compatibility Engine & Validator
Parses, type-checks, and validates 7-slot attack compositions with explanatory diagnostic reasons.
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

from backend.attacks.grammar import (
    AttackComposition,
    ACCESS_MECHANISMS,
    TRUST_MECHANISMS,
    PAYMENT_RAILS,
    EVASION_MECHANISMS,
    BEHAVIORAL_PATTERNS,
    MONETIZATION_PATHWAYS,
    TEMPORAL_PATTERNS
)


@dataclass
class ValidationResult:
    is_type_valid: bool
    is_semantic_valid: bool
    is_executable: bool
    diagnostic_rejection_reasons: List[str]
    compatibility_score: float  # 0.0 to 1.0


class SemanticCompatibilityValidator:
    """Type-checks and semantically validates attack compositions with explanatory rejections."""

    def __init__(self):
        self.access_vocab = set(ACCESS_MECHANISMS)
        self.trust_vocab = set(TRUST_MECHANISMS)
        self.rail_vocab = set(PAYMENT_RAILS)
        self.evasion_vocab = set(EVASION_MECHANISMS)
        self.behavior_vocab = set(BEHAVIORAL_PATTERNS)
        self.monetization_vocab = set(MONETIZATION_PATHWAYS)
        self.temporal_vocab = set(TEMPORAL_PATTERNS)

    def validate_types(self, composition: AttackComposition) -> Tuple[bool, List[str]]:
        """Checks if all 7 slots belong to recognized vocabulary types."""
        errors = []
        if composition.access not in self.access_vocab:
            errors.append(f"Type Error: Unrecognized access mechanism '{composition.access}'.")
        if composition.trust not in self.trust_vocab:
            errors.append(f"Type Error: Unrecognized trust mechanism '{composition.trust}'.")
        if composition.rail not in self.rail_vocab:
            errors.append(f"Type Error: Unrecognized payment rail '{composition.rail}'. Must be one of {sorted(list(self.rail_vocab))}.")
        if composition.evasion not in self.evasion_vocab:
            errors.append(f"Type Error: Unrecognized evasion mechanism '{composition.evasion}'.")
        if composition.behavior not in self.behavior_vocab:
            errors.append(f"Type Error: Unrecognized behavioral pattern '{composition.behavior}'.")
        if composition.monetization not in self.monetization_vocab:
            errors.append(f"Type Error: Unrecognized monetization pathway '{composition.monetization}'.")
        if composition.temporal_pattern not in self.temporal_vocab:
            errors.append(f"Type Error: Unrecognized temporal pattern '{composition.temporal_pattern}'.")

        return len(errors) == 0, errors

    def validate_semantics(self, composition: AttackComposition) -> Tuple[bool, List[str]]:
        """Applies domain rules checking payment semantics, entity state, and lifecycle compatibility."""
        errors = []

        # Rule 1: Rail vs Monetization & State Compatibility
        if composition.rail == "Recurring Mandate":
            if composition.monetization not in ["Future Automated Pulls", "Scheduled Bill Pay Abuse", "Immediate P2P Drain"]:
                errors.append(
                    f"Semantic Error: Rail 'Recurring Mandate' does not support monetization '{composition.monetization}'. "
                    "Mandate rails operate via registered standing debits or future automated pulls."
                )
            if composition.behavior not in ["Subscription Registration", "Gradual Balance Building", "Baseline Hour Mimicry"]:
                errors.append(
                    f"Semantic Error: Rail 'Recurring Mandate' requires registration or scheduled behavior, but observed '{composition.behavior}'."
                )

        if composition.rail in ["UPI", "A2A"]:
            if composition.evasion in ["Pre-Authorization Hold Arbitrage", "Orphan Refund Request", "Exploit Settlement Latency Window"]:
                errors.append(
                    f"Semantic Error: Rail '{composition.rail}' is a single-message real-time settlement rail. "
                    f"Evasion '{composition.evasion}' requires dual-message acquirer authorization/clearing delay present only in Card networks."
                )
            if composition.monetization in ["Card Not Present Checkout", "Card Validity Verification", "Item Retained + Chargeback Credit"]:
                errors.append(
                    f"Semantic Error: Monetization '{composition.monetization}' is an e-commerce merchant card flow incompatible with '{composition.rail}'."
                )

        if composition.rail == "Card":
            if composition.monetization in ["P2P Wallet Drain", "Layered Crypto/P2P Dispersal", "Immediate Mule Account Credit"]:
                errors.append(
                    f"Semantic Error: Card processing rails execute merchant checkout or ATM advances. "
                    f"Direct account disbursement '{composition.monetization}' requires an A2A or UPI real-time push network."
                )

        # Rule 2: Access vs Trust Mechanism Compatibility
        if composition.access == "SIM Swap" and composition.trust in ["Cookie Replay", "Browser Environment Hook"]:
            errors.append(
                f"Semantic Error: Access mechanism 'SIM Swap' targets cellular SMS/carrier OTP channels, "
                f"which is incompatible with browser web-session trust mechanism '{composition.trust}'."
            )

        if composition.access == "Synthetic Face GAN Generation" and composition.trust not in ["Virtual Camera Driver", "Biometric Mimicry", "Synthetic Persona Cluster"]:
            errors.append(
                f"Semantic Error: Access 'Synthetic Face GAN Generation' requires biometric or virtual camera trust injection, "
                f"incompatible with '{composition.trust}'."
            )

        if composition.access == "Malware Protocol Downgrade" and composition.trust not in ["Client Feature Stripping", "Emulated Touch Screen", "Legitimate Mobile App"]:
            errors.append(
                f"Semantic Error: Protocol downgrade requires client-side capability interception (e.g. stripping FIDO2 headers), "
                f"incompatible with '{composition.trust}'."
            )

        # Rule 3: Temporal vs Behavioral Dynamics Compatibility
        if composition.temporal_pattern == "Instantaneous Burst" and composition.behavior in ["Humanized Thinking Pauses", "Learned Timing Jitter", "Boundary Wandering"]:
            errors.append(
                f"Semantic Error: Temporal pattern 'Instantaneous Burst' conflicts with behavioral pattern '{composition.behavior}', "
                "which requires gradual pacing and human-like inter-arrival jitter."
            )

        if composition.temporal_pattern == "Months-Long Maturation" and composition.behavior in ["Burst Rapid Action", "High Velocity Testing", "Rapid Sequential Micro Authorizations"]:
            errors.append(
                f"Semantic Error: Long-term seasoning maturation cannot coexist with sub-second rapid testing behavior."
            )

        return len(errors) == 0, errors

    def validate(self, composition: AttackComposition) -> ValidationResult:
        """Executes full multi-stage validation pipeline."""
        is_type_valid, type_errors = self.validate_types(composition)
        if not is_type_valid:
            return ValidationResult(
                is_type_valid=False,
                is_semantic_valid=False,
                is_executable=False,
                diagnostic_rejection_reasons=type_errors,
                compatibility_score=0.0
            )

        is_semantic_valid, semantic_errors = self.validate_semantics(composition)
        all_errors = type_errors + semantic_errors

        # Executable requires both type and semantic validity
        is_executable = is_type_valid and is_semantic_valid
        comp_score = 1.0 if is_executable else max(0.0, 1.0 - (len(all_errors) * 0.25))

        return ValidationResult(
            is_type_valid=is_type_valid,
            is_semantic_valid=is_semantic_valid,
            is_executable=is_executable,
            diagnostic_rejection_reasons=all_errors,
            compatibility_score=comp_score
        )


compatibility_validator = SemanticCompatibilityValidator()
