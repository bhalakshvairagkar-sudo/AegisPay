"""
AegisPay v2 - Semantic Invariants Engine & Build Gate
Enforces 100% compliance with domain invariants and blocks invalid simulations.
"""

from typing import Dict, Any, List, Tuple
from backend.simulator.invariants.rules import CATEGORIZED_INVARIANTS, InvariantViolationError, SemanticInvariant


class SemanticInvariantsEngine:
    """Evaluates transactions against categorized semantic invariant gates."""

    def __init__(self):
        self.invariants = CATEGORIZED_INVARIANTS

    def evaluate_transaction(self, tx_dict: Dict[str, Any], raise_on_failure: bool = False) -> Tuple[bool, List[Dict[str, Any]]]:
        """Evaluates a single transaction dictionary against all invariants."""
        violations = []
        for inv in self.invariants:
            passed, expected, observed = inv.check_fn(tx_dict)
            if not passed:
                violation_info = {
                    "invariant_id": inv.invariant_id,
                    "category": inv.category,
                    "name": inv.name,
                    "expected": expected,
                    "observed": observed
                }
                violations.append(violation_info)
                if raise_on_failure:
                    raise InvariantViolationError(
                        invariant_name=inv.name,
                        category=inv.category,
                        expected=expected,
                        observed=observed
                    )

        return len(violations) == 0, violations

    def evaluate_batch(self, transactions: List[Dict[str, Any]], raise_on_failure: bool = False) -> Dict[str, Any]:
        """Evaluates an entire dataset batch and returns compliance metrics."""
        total = len(transactions)
        passed_count = 0
        all_violations = []

        category_counts: Dict[str, int] = {}
        for inv in self.invariants:
            category_counts[inv.category] = category_counts.get(inv.category, 0) + 1

        for tx in transactions:
            is_valid, v_list = self.evaluate_transaction(tx, raise_on_failure=raise_on_failure)
            if is_valid:
                passed_count += 1
            else:
                all_violations.extend(v_list)

        compliance_pct = round((passed_count / max(1, total)) * 100, 2)
        return {
            "total_transactions_checked": total,
            "passed_count": passed_count,
            "failed_count": total - passed_count,
            "compliance_percentage": compliance_pct,
            "status": "PASS" if passed_count == total else "FAIL",
            "active_invariants_count": len(self.invariants),
            "invariant_categories": category_counts,
            "violations_summary": all_violations[:20]  # First 20 violations for diagnosis
        }


invariants_engine = SemanticInvariantsEngine()
