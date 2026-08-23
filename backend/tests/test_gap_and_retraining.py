"""
Unit Tests for Data Fidelity & Gap Analysis / Retraining
"""

import pytest
import pandas as pd
import numpy as np

from backend.simulator.transactions import PaymentSimulator
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator
from backend.models.ensemble import AegisPayHybridDefense
from backend.evaluation.fidelity import FidelityEngine
from backend.gap_analysis.clustering import GapAnalyzer
from backend.retraining.adversarial_training import AdversarialTrainer


def test_fidelity_engine_computations():
    sim = PaymentSimulator(seed=42)
    txns = sim.generate_legitimate_stream(300)
    df = pd.DataFrame([t.to_feature_dict() for t in txns])

    fidelity_engine = FidelityEngine(seed=42)
    report = fidelity_engine.evaluate_fidelity(df)

    assert "fidelityScore" in report
    assert 0.0 <= report["fidelityScore"] <= 100.0
    assert "ksDistanceAmount" in report
    assert 0.0 <= report["ksDistanceAmount"] <= 1.0
    assert "wassersteinDistanceAmount" in report
    assert report["wassersteinDistanceAmount"] >= 0.0
    assert "densityCurve" in report
    assert len(report["densityCurve"]["bins"]) == 10


def test_gap_analysis_and_retraining_loop():
    sim = PaymentSimulator(seed=42)
    gen = AttackScenarioGenerator(simulator=sim, seed=42)
    gap_analyzer = GapAnalyzer(seed=42)
    trainer = AdversarialTrainer(simulator=sim, seed=42)

    legit = sim.generate_legitimate_stream(300)
    attacks = gen.generate_scenarios(100, mutation_strength=0.5)
    all_data = legit + attacks
    np.random.shuffle(all_data)

    X_train = pd.DataFrame([t.to_feature_dict() for t in all_data])
    y_train = np.array([t.is_fraud for t in all_data])

    # 1. Train v1
    v1 = AegisPayHybridDefense(version="v1.0", seed=42).fit(X_train, y_train)

    # 2. Test against hard attacks
    adv_scenarios = gen.generate_scenarios(50, mutation_strength=0.7, difficulty="Hard")
    df_adv = pd.DataFrame([s.to_feature_dict() for s in adv_scenarios])
    pred = v1.predict(df_adv)
    prob = v1.predict_proba(df_adv)[:, 1]

    # 3. Gap Analysis
    gap_report = gap_analyzer.analyze_evasions(adv_scenarios, pred, prob)
    assert "evasion_count" in gap_report
    assert "clusters" in gap_report

    # 4. Synthesize counterexamples & train v2
    counterexamples = trainer.generate_targeted_counterexamples(gap_report["clusters"], n_samples=100)
    v2 = trainer.train_hardened_model(X_train, y_train, counterexamples, target_version="v2.0")

    assert v2.version == "v2.0"
    assert v2.is_fitted
