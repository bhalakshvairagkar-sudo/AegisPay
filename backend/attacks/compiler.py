"""
AegisPay v2 - Attack Compiler
Compiles typed 7-slot attack compositions into executable payment scenario definitions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import hashlib
import json

from backend.attacks.grammar import AttackComposition
from backend.attacks.compatibility import compatibility_validator, ValidationResult
from backend.attacks.primitives import ATTACK_PRIMITIVES
from backend.attacks.difficulty import DIFFICULTY_TIERS


@dataclass
class ExecutableAttackScenario:
    scenario_id: str
    composition: AttackComposition
    validation: ValidationResult
    feature_perturbation_spec: Dict[str, Any]
    target_rail: str
    difficulty_level: int
    is_adversarial: bool = True
    compilation_timestamp: str = "2026-09-07T12:00:00Z"


class AttackCompiler:
    """Compiles valid typed grammar sentences into executable payment attack scenarios."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def compile(self, composition: AttackComposition) -> Tuple[Optional[ExecutableAttackScenario], ValidationResult]:
        """Compiles composition into executable scenario or rejects with diagnostic reasons."""
        val_result = compatibility_validator.validate(composition)

        if not val_result.is_executable:
            return None, val_result

        tier = DIFFICULTY_TIERS.get(composition.difficulty, DIFFICULTY_TIERS[1])
        comp_sig = composition.get_composition_signature()
        scenario_id = f"SCN-V2-{composition.vector}-{comp_sig[:8]}"

        spec = {
            "amount_scale_range": tier.amount_perturbation_range,
            "velocity_mult": tier.velocity_multiplier,
            "behavioral_deviation_bounds": (tier.behavioral_deviation_min, tier.behavioral_deviation_max),
            "device_familiarity_bounds": (tier.device_familiarity_min, tier.device_familiarity_max),
            "carrier_change_prob": tier.carrier_change_prob,
            "rail": composition.rail,
            "access": composition.access,
            "trust": composition.trust,
            "evasion": composition.evasion,
            "behavior": composition.behavior,
            "monetization": composition.monetization,
            "temporal_pattern": composition.temporal_pattern
        }

        scenario = ExecutableAttackScenario(
            scenario_id=scenario_id,
            composition=composition,
            validation=val_result,
            feature_perturbation_spec=spec,
            target_rail=composition.rail,
            difficulty_level=composition.difficulty,
            is_adversarial=True
        )

        return scenario, val_result

    def compile_from_primitive(
        self,
        primitive_id: str,
        difficulty: int = 1,
        rail_override: Optional[str] = None
    ) -> Tuple[Optional[ExecutableAttackScenario], ValidationResult]:
        """Convenience method to compile directly from a seed primitive ID."""
        prim = ATTACK_PRIMITIVES.get(primitive_id)
        if not prim:
            val_res = ValidationResult(
                is_type_valid=False,
                is_semantic_valid=False,
                is_executable=False,
                diagnostic_rejection_reasons=[f"Primitive ID '{primitive_id}' not found in catalog."],
                compatibility_score=0.0
            )
            return None, val_res

        comp = AttackComposition(
            access=prim.default_access,
            trust=prim.default_trust,
            rail=rail_override or prim.default_rail,
            evasion=prim.default_evasion,
            behavior=prim.default_behavior,
            monetization=prim.default_monetization,
            temporal_pattern=prim.default_temporal,
            family=prim.family,
            vector=prim.primitive_id,
            difficulty=difficulty,
            seed=self.seed,
            provenance="MEASURED"
        )

        return self.compile(comp)


attack_compiler = AttackCompiler()
