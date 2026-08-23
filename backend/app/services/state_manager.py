"""
State Manager & Execution Orchestrator
Maintains in-memory models, active simulators, and links REST APIs to ML engines.
"""

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np

from backend.simulator.transactions import PaymentSimulator, SyntheticTransaction
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator
from backend.attacks.taxonomy import taxonomy_instance
from backend.models.registry import global_registry
from backend.models.baseline import RuleBasedClassifier, RandomForestBaselineWrapper
from backend.models.xgboost_model import XGBoostClassifierWrapper
from backend.models.anomaly_model import IsolationForestAnomalyDetector
from backend.models.ensemble import AegisPayHybridDefense
from backend.models.explainability import ExplainabilityEngine
from backend.evaluation.fidelity import FidelityEngine
from backend.evaluation.robustness import RobustnessEvaluator
from backend.evaluation.experiments import experiment_registry
from backend.gap_analysis.clustering import GapAnalyzer
from backend.retraining.adversarial_training import AdversarialTrainer
from backend.retraining.evolution import EvolutionLab


class SystemStateManager:
    """Singleton state manager coordinating models, simulations, and experiments."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.simulator = PaymentSimulator(seed=seed)
        self.generator = AttackScenarioGenerator(simulator=self.simulator, seed=seed)
        self.fidelity_engine = FidelityEngine(seed=seed)
        self.robustness_evaluator = RobustnessEvaluator(self.generator)
        self.gap_analyzer = GapAnalyzer(seed=seed)
        self.trainer = AdversarialTrainer(simulator=self.simulator, seed=seed)
        self.evolution_lab = EvolutionLab(simulator=self.simulator, seed=seed)
        self.taxonomy = taxonomy_instance

        self.current_model_version = "v1.0"
        self._ensure_models_loaded()

    def _ensure_models_loaded(self):
        """Loads models from disk or initializes defaults if not yet trained."""
        # Try loading latest experiment
        latest_exp = experiment_registry.get_latest()
        if not latest_exp:
            # Train initial fast models if none exist
            legit = self.simulator.generate_legitimate_stream(600)
            attacks = self.generator.generate_scenarios(200, mutation_strength=0.35, difficulty="Moderate")
            attacks_known = [a for a in attacks if a.attack_family != "AI Adaptive Fraud"]
            all_data = legit + attacks_known
            np.random.shuffle(all_data)

            X = pd.DataFrame([t.to_feature_dict() for t in all_data])
            y = np.array([t.is_fraud for t in all_data])

            v1 = AegisPayHybridDefense(version="v1.0", seed=self.seed).fit(X, y)
            v2 = AegisPayHybridDefense(version="v2.0", seed=self.seed + 1).fit(X, y)
            v3 = AegisPayHybridDefense(version="v3.0", seed=self.seed + 2).fit(X, y)
            xgb = XGBoostClassifierWrapper(seed=self.seed).fit(X, y)
            iso = IsolationForestAnomalyDetector(seed=self.seed).fit(X[y == 0])
            rf = RandomForestBaselineWrapper(seed=self.seed).fit(X, y)
            rule = RuleBasedClassifier()

            global_registry.register("aegispay_v1", v1)
            global_registry.register("aegispay_v2", v2)
            global_registry.register("aegispay_v3", v3)
            global_registry.register("xgboost", xgb)
            global_registry.register("iso_forest", iso)
            global_registry.register("random_forest", rf)
            global_registry.register("rule_engine", rule)
        else:
            # Load models from registry
            for m_id in ["rule_engine", "random_forest", "xgboost", "iso_forest", "aegispay_v1", "aegispay_v2", "aegispay_v3"]:
                global_registry.load_model(m_id)

    def get_model(self, model_id: str) -> Optional[Any]:
        return global_registry.get(model_id)

    def get_active_defense(self) -> AegisPayHybridDefense:
        m_id = f"aegispay_{self.current_model_version.replace('.', '_')}"
        model = self.get_model(m_id)
        if not model:
            model = self.get_model("aegispay_v1")
        return model or AegisPayHybridDefense(version="v1.0")

    def get_explainability_engine(self) -> ExplainabilityEngine:
        return ExplainabilityEngine(self.get_active_defense())


system_state = SystemStateManager()
