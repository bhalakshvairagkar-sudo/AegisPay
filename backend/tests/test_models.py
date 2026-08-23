"""
Unit Tests for Machine Learning Models & Explainability
"""

import pytest
import numpy as np
import pandas as pd

from backend.simulator.transactions import PaymentSimulator
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator
from backend.models.baseline import RuleBasedClassifier, RandomForestBaselineWrapper
from backend.models.xgboost_model import XGBoostClassifierWrapper
from backend.models.anomaly_model import IsolationForestAnomalyDetector
from backend.models.ensemble import AegisPayHybridDefense
from backend.models.explainability import ExplainabilityEngine
from backend.evaluation.metrics import evaluate_model_performance


@pytest.fixture
def sample_dataset():
    sim = PaymentSimulator(seed=42)
    gen = AttackScenarioGenerator(simulator=sim, seed=42)
    legit = sim.generate_legitimate_stream(150)
    attacks = gen.generate_scenarios(50, mutation_strength=0.3)
    all_data = legit + attacks
    np.random.shuffle(all_data)

    X = pd.DataFrame([t.to_feature_dict() for t in all_data])
    y = np.array([t.is_fraud for t in all_data])
    return X, y


def test_models_fit_and_predict(sample_dataset):
    X, y = sample_dataset

    # 1. Rule Model
    rule = RuleBasedClassifier()
    probs_rule = rule.predict_proba(X)
    assert probs_rule.shape == (len(X), 2)

    # 2. Random Forest
    rf = RandomForestBaselineWrapper(seed=42).fit(X, y)
    probs_rf = rf.predict_proba(X)
    assert probs_rf.shape == (len(X), 2)

    # 3. XGBoost
    xgb = XGBoostClassifierWrapper(seed=42).fit(X, y)
    probs_xgb = xgb.predict_proba(X)
    assert probs_xgb.shape == (len(X), 2)
    assert len(xgb.get_feature_importances()) > 5

    # 4. Isolation Forest
    iso = IsolationForestAnomalyDetector(seed=42).fit(X[y == 0])
    scores_iso = iso.score_samples(X)
    assert scores_iso.shape == (len(X),)
    assert 0.0 <= scores_iso.min() and scores_iso.max() <= 1.0

    # 5. AegisPay Hybrid
    hybrid = AegisPayHybridDefense(version="v1.0", seed=42).fit(X, y)
    evals = hybrid.evaluate_risk(X)
    assert len(evals) == len(X)
    assert 0 <= evals[0]["unified_risk_score"] <= 100
    assert evals[0]["decision"] in ["ALLOW", "STEP-UP 3DS VERIFY", "MANUAL REVIEW", "BLOCK"]


def test_explainability_drivers(sample_dataset):
    X, y = sample_dataset
    hybrid = AegisPayHybridDefense(version="v1.0", seed=42).fit(X, y)
    explainer = ExplainabilityEngine(hybrid)

    # Suspicious transaction
    sus_features = {
        "amount": 950.0,
        "velocity_1h": 8,
        "velocity_24h": 15,
        "device_familiarity": 0.05,
        "geo_distance_km": 850.0,
        "behavioral_deviation": 0.88,
        "merchant_risk_score": 0.75,
        "account_age_days": 12,
        "touch_pressure_deviation": 0.70,
        "carrier_change_flag": 1,
        "mcc_risk_weight": 0.60,
    }

    drivers = explainer.explain_transaction(sus_features)
    assert len(drivers) > 3
    # Top driver should be a high risk factor
    assert drivers[0]["impact"] in ["HIGH_RISK", "MEDIUM_RISK"]
    assert "+" in drivers[0]["value"]
