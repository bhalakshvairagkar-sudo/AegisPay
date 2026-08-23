"""
Unit Tests for Attack Taxonomy & Scenario Generator
"""

import pytest
from backend.attacks.taxonomy import AttackTaxonomy, taxonomy_instance
from backend.attacks.generators.scenario_generator import AttackScenarioGenerator
from backend.simulator.transactions import PaymentSimulator


def test_taxonomy_coverage():
    all_attacks = taxonomy_instance.get_all()
    assert len(all_attacks) == 36
    families = taxonomy_instance.get_families()
    assert len(families) == 8

    # Ensure holdout family is isolated
    holdout = taxonomy_instance.get_holdout_attacks()
    assert len(holdout) == 3
    assert all(a.family == "AI Adaptive Fraud" for a in holdout)

    training_attacks = taxonomy_instance.get_training_attacks()
    assert len(training_attacks) == 33


def test_knowledge_graph_structure():
    graph = taxonomy_instance.get_knowledge_graph()
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 15
    assert len(graph["edges"]) > 10


def test_scenario_generator_produces_valid_records():
    sim = PaymentSimulator(seed=42)
    generator = AttackScenarioGenerator(simulator=sim, seed=42)

    scenarios = generator.generate_scenarios(
        count=30,
        family_filter="ALL",
        mutation_strength=0.5,
        difficulty="Moderate"
    )

    assert len(scenarios) == 30
    for s in scenarios:
        assert s.is_fraud == 1
        assert s.amount > 0
        assert 0.0 <= s.device_familiarity <= 1.0
        assert s.attack_id != "LEGIT"
        assert s.attack_family in taxonomy_instance.get_families()
