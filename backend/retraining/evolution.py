"""
Closed-Loop Adversarial Evolution Lab & Zero-Shot Holdout Evaluator
Tracks the multi-round evolution history (R1 -> R2 -> R3) and evaluates models
against unseen holdout attack families (ADV-01, ADV-02).
"""

from typing import List, Dict, Any, Tuple
import datetime
import numpy as np
import pandas as pd

from backend.simulator.transactions import SyntheticTransaction, PaymentSimulator
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator
from backend.models.ensemble import AegisPayHybridDefense
from backend.evaluation.metrics import evaluate_model_performance
from backend.gap_analysis.clustering import GapAnalyzer
from backend.retraining.adversarial_training import AdversarialTrainer


class EvolutionLab:
    """Orchestrates closed-loop evolutionary rounds and holdout benchmarking."""

    def __init__(self, simulator: PaymentSimulator, seed: int = 42):
        self.simulator = simulator
        self.seed = seed
        self.generator = AttackScenarioGenerator(simulator=simulator, seed=seed)
        self.gap_analyzer = GapAnalyzer(seed=seed)
        self.trainer = AdversarialTrainer(simulator=simulator, seed=seed)

    def evaluate_holdout_attacks(
        self,
        baseline_model: Any,
        hardened_model: Any,
        n_holdout_samples: int = 60
    ) -> Dict[str, Any]:
        """
        Evaluates models against the strictly reserved unseen attack family: AI Adaptive Fraud (ADV-01, ADV-02).
        Measures true zero-shot adversarial generalization.
        """
        # Generate attacks from the reserved holdout family only
        holdout_scenarios = self.generator.generate_scenarios(
            count=n_holdout_samples,
            family_filter="AI Adaptive Fraud",
            mutation_strength=0.75,
            difficulty="Unseen"
        )
        df_holdout = pd.DataFrame([s.to_feature_dict() for s in holdout_scenarios])
        y_holdout = np.ones(len(holdout_scenarios), dtype=int)

        # Baseline evaluation
        base_pred = baseline_model.predict(df_holdout)
        base_detection_rate = round(float(np.mean(base_pred == 1)) * 100.0, 1)

        # Hardened evaluation
        hardened_pred = hardened_model.predict(df_holdout)
        hardened_detection_rate = round(float(np.mean(hardened_pred == 1)) * 100.0, 1)

        return {
            "family_tested": "AI Adaptive Fraud (Zero-Shot Holdout)",
            "primary_vector": "ADV-01 Model Inversion Gradient Perturbation",
            "samples_tested": len(holdout_scenarios),
            "baselineDetectionRate": base_detection_rate,
            "hardenedDetectionRate": hardened_detection_rate,
            "generalizationDelta": round(hardened_detection_rate - base_detection_rate, 1),
            "description": "Evaluated against attack family AI Adaptive Fraud, which was strictly held out during training."
        }
