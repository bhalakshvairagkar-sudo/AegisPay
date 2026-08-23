"""
Adversarial Robustness Matrix & Attack Diversity Engine
Evaluates degradation curves across 5 difficulty tiers and computes Attack Diversity Metrics.
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd

from backend.attacks.generators.scenario_generator import AttackScenarioGenerator


class RobustnessEvaluator:
    """Evaluates model resilience across graduated adversarial difficulty levels."""

    def __init__(self, scenario_generator: AttackScenarioGenerator):
        self.generator = scenario_generator

    def evaluate_robustness_curve(
        self,
        model_v1: Any,
        model_v3: Any,
        n_samples_per_level: int = 40
    ) -> Dict[str, Any]:
        """
        Generates test batches for each difficulty level and measures detection rates for v1 vs v3.
        Returns authentic level bars and degradation curve.
        """
        levels = [
            ("Level 1 (Easy)", "Easy", 0.15),
            ("Level 2 (Moderate)", "Moderate", 0.35),
            ("Level 3 (Hard)", "Hard", 0.55),
            ("Level 4 (Adversarial)", "Adversarial", 0.80),
        ]

        level_results = []
        recalls_v1 = []
        recalls_v3 = []

        for label, diff_key, mut_scale in levels:
            scenarios = self.generator.generate_scenarios(
                count=n_samples_per_level,
                family_filter="ALL",
                mutation_strength=mut_scale,
                difficulty=diff_key
            )
            df = pd.DataFrame([s.to_feature_dict() for s in scenarios])
            y_true = np.ones(len(scenarios), dtype=int)

            # Evaluate v1
            pred_v1 = model_v1.predict(df)
            rec_v1 = float(np.mean(pred_v1 == 1))
            recalls_v1.append(rec_v1)

            # Evaluate v3
            pred_v3 = model_v3.predict(df)
            rec_v3 = float(np.mean(pred_v3 == 1))
            recalls_v3.append(rec_v3)

            level_results.append({
                "level": label,
                "difficulty_key": diff_key,
                "v1": round(rec_v1 * 100.0, 1),
                "v3": round(rec_v3 * 100.0, 1),
                "samples_tested": len(scenarios)
            })

        # Weighted Robustness Score: 10% Easy, 20% Moderate, 30% Hard, 40% Adversarial
        weights = np.array([0.10, 0.20, 0.30, 0.40])
        score_v1 = int(round(np.sum(np.array(recalls_v1) * weights) * 100))
        score_v3 = int(round(np.sum(np.array(recalls_v3) * weights) * 100))

        return {
            "levels": level_results,
            "robustnessScoreV1": score_v1,
            "robustnessScoreV3": score_v3,
            "formula_description": "Robustness Score = 100 * sum(w_i * Recall_i) where w=[0.10, 0.20, 0.30, 0.40]"
        }

    def compute_attack_diversity_score(self, scenarios: List[Any]) -> Dict[str, Any]:
        """
        Calculates attack diversity from feature-space variance and family coverage.
        """
        if not scenarios:
            return {"diversityScore": 0.0, "familyCoverage": 0.0, "uniqueVariants": 0}

        families = set(s.attack_family for s in scenarios)
        unique_attacks = set(s.attack_id for s in scenarios)

        # Feature matrix dispersion (mean standard deviation across normalized features)
        df = pd.DataFrame([s.to_feature_dict() for s in scenarios])
        std_devs = df.std(numeric_only=True).values
        mean_dispersion = float(np.mean(std_devs))

        # Normalized diversity score
        family_ratio = len(families) / 8.0
        variant_ratio = min(1.0, len(unique_attacks) / 20.0)
        diversity_score = round(float((0.4 * family_ratio + 0.3 * variant_ratio + 0.3 * min(1.0, mean_dispersion / 50.0)) * 100.0), 1)

        return {
            "diversityScore": diversity_score,
            "familyCoverage": round(family_ratio * 100.0, 1),
            "familiesRepresented": len(families),
            "uniqueVariants": len(unique_attacks),
            "meanFeatureDispersion": round(mean_dispersion, 2)
        }
