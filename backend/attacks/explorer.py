"""
AegisPay v2 - Attack Space Explorer & Metric Engine
Dynamically evaluates and measures raw, type-valid, semantic-valid, executable, and executed attack compositions.
"""

from typing import Dict, Any, List, Set
import itertools

from backend.attacks.primitives import ATTACK_PRIMITIVES
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
from backend.attacks.compatibility import compatibility_validator
from backend.attacks.compiler import attack_compiler


class AttackSpaceExplorer:
    """Discovers and measures the reachable attack space without hardcoding numbers."""

    def __init__(self):
        self.executed_signatures: Set[str] = set()
        self.family_executions: Dict[str, int] = {f: 0 for f in set(p.family for p in ATTACK_PRIMITIVES.values())}
        self.rail_executions: Dict[str, int] = {r: 0 for r in PAYMENT_RAILS}

    def compute_combinatorial_metrics(self) -> Dict[str, Any]:
        """Calculates theoretical raw combinations across the 7 semantic slots."""
        raw_combinations = (
            len(ACCESS_MECHANISMS) *
            len(TRUST_MECHANISMS) *
            len(PAYMENT_RAILS) *
            len(EVASION_MECHANISMS) *
            len(BEHAVIORAL_PATTERNS) *
            len(MONETIZATION_PATHWAYS) *
            len(TEMPORAL_PATTERNS)
        )

        # Measure primitive-derived valid baseline space
        primitive_count = len(ATTACK_PRIMITIVES)
        families_count = len(set(p.family for p in ATTACK_PRIMITIVES.values()))

        # Evaluate sample valid space across primitives x rails x difficulties
        tested_compositions = 0
        valid_compositions = 0
        rejected_compositions = 0
        rejection_reasons_tally: Dict[str, int] = {}

        sample_eval_limit = 500
        # Sample across primitives and cross-rail combinations
        for p_id, prim in itertools.islice(ATTACK_PRIMITIVES.items(), 36):
            for rail in PAYMENT_RAILS:
                for diff in range(1, 6):
                    tested_compositions += 1
                    comp = AttackComposition(
                        access=prim.default_access,
                        trust=prim.default_trust,
                        rail=rail,
                        evasion=prim.default_evasion,
                        behavior=prim.default_behavior,
                        monetization=prim.default_monetization,
                        temporal_pattern=prim.default_temporal,
                        family=prim.family,
                        vector=prim.primitive_id,
                        difficulty=diff,
                        provenance="MEASURED"
                    )
                    res = compatibility_validator.validate(comp)
                    if res.is_executable:
                        valid_compositions += 1
                    else:
                        rejected_compositions += 1
                        for r in res.diagnostic_rejection_reasons:
                            k = r.split(":")[0] if ":" in r else "Constraint"
                            rejection_reasons_tally[k] = rejection_reasons_tally.get(k, 0) + 1

        executed_count = len(self.executed_signatures)
        semantic_valid_pct = round((valid_compositions / max(1, tested_compositions)) * 100, 2)

        return {
            "primitives_count": primitive_count,
            "families_count": families_count,
            "raw_combinatorial_space": raw_combinations,
            "sample_tested_compositions": tested_compositions,
            "sample_valid_compositions": valid_compositions,
            "sample_rejected_compositions": rejected_compositions,
            "semantic_valid_ratio_pct": semantic_valid_pct,
            "actually_executed_unique": executed_count,
            "rejection_reasons_tally": rejection_reasons_tally,
            "family_coverage": {
                f: round((count / max(1, executed_count or 1)) * 100, 2)
                for f, count in self.family_executions.items()
            },
            "rail_coverage": {
                r: round((count / max(1, executed_count or 1)) * 100, 2)
                for r, count in self.rail_executions.items()
            }
        }

    def record_execution(self, composition: AttackComposition):
        """Logs an executed attack composition to update coverage tracking."""
        sig = composition.get_composition_signature()
        self.executed_signatures.add(sig)
        if composition.family in self.family_executions:
            self.family_executions[composition.family] += 1
        if composition.rail in self.rail_executions:
            self.rail_executions[composition.rail] += 1


attack_explorer = AttackSpaceExplorer()
