"""
Integration Tests for FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["closed_loop_engine"] == "ACTIVE"


def test_taxonomy_endpoints():
    res = client.get("/api/attacks/taxonomy")
    assert res.status_code == 200
    data = res.json()
    assert data["total_vectors"] == 36
    assert len(data["families"]) == 8

    res_graph = client.get("/api/attacks/graph")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    assert "nodes" in graph_data
    assert "edges" in graph_data


def test_attack_generation_endpoint():
    payload = {
        "count": 15,
        "family_filter": "ALL",
        "sophistication": 7.5,
        "mutation_strength": 0.4
    }
    res = client.post("/api/attacks/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["scenarios"]) == 15
    assert "evasion_rate_v1" in data


def test_predict_endpoint():
    payload = {
        "amount": 550.0,
        "velocityCount": 6,
        "deviceFamiliarity": 0.15,
        "locationDeviationKm": 320.0,
        "behavioralVariance": 0.82,
        "merchantRiskScore": 0.70,
        "accountAgeDays": 25
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "unifiedRiskScore" in data
    assert "decision" in data
    assert "shapDrivers" in data
    assert len(data["shapDrivers"]) > 0


def test_models_comparison_endpoint():
    res = client.get("/api/models/comparison")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)


def test_fidelity_endpoint():
    res = client.get("/api/fidelity")
    assert res.status_code == 200
    data = res.json()
    assert "fidelityScore" in data
    assert "ksDistanceAmount" in data


def test_dashboard_endpoint():
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "totalAttackVariants" in data
    assert "detectionRateF1" in data


def test_judge_demo_endpoint():
    res = client.post("/api/judge-demo/run")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert len(data["steps"]) >= 7
