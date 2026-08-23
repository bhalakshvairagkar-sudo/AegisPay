"""
Data Leakage Prevention Test Suite
Verifies that no metadata or ground-truth features leak into model input matrices.
"""

import pytest
import pandas as pd
import numpy as np
from backend.simulator.transactions import PaymentSimulator
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator


PROHIBITED_FEATURE_KEYS = [
    "attack_id",
    "attack_family",
    "attack_name",
    "gen_ai",
    "genAi",
    "sophistication",
    "difficulty",
    "mutation_strength",
    "is_fraud",
    "fraud_label",
    "ground_truth"
]


def test_feature_dict_segregation():
    sim = PaymentSimulator(seed=42)
    generator = AttackScenarioGenerator(simulator=sim, seed=42)

    legit = sim.generate_legitimate_stream(20)
    attacks = generator.generate_scenarios(20)

    for item in legit + attacks:
        feat_dict = item.to_feature_dict()

        for prohibited in PROHIBITED_FEATURE_KEYS:
            assert prohibited not in feat_dict, f"Data leakage detected! '{prohibited}' found in model input feature dict."

        # Verify allowed features are strictly numeric
        for k, v in feat_dict.items():
            assert isinstance(v, (int, float, np.number)), f"Non-numeric feature '{k}' with value '{v}' in input matrix."
