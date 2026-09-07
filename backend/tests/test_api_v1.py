"""
Tests for FastAPI REST API v1 Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


client = TestClient(app)


def test_health_v1():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_taxonomy_v1():
    res = client.get("/api/v1/attacks/taxonomy")
    assert res.status_code == 200
    data = res.json()
    assert data["primitives_count"] == 36
    assert "grammar_vocabularies" in data


def test_attack_explorer_v1():
    res = client.get("/api/v1/attacks/explorer")
    assert res.status_code == 200
    data = res.json()
    assert data["primitives_count"] == 36
    assert data["raw_combinatorial_space"] > 100000


def test_predict_endpoint_v1():
    payload = {
        "amount": 250.0,
        "velocity_1h": 1.0,
        "velocity_24h": 2.0,
        "device_familiarity": 0.85,
        "geo_distance_km": 5.0,
        "behavioral_deviation": 0.1,
        "merchant_risk_score": 0.2,
        "account_age_days": 180,
        "touch_pressure_deviation": 0.1,
        "carrier_change_flag": 0,
        "mcc_risk_weight": 0.15,
        "hour_of_day": 14,
        "is_international": 0,
        "rail": "Card"
    }
    res = client.post("/api/v1/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "policy_action" in data
    assert "reason_codes" in data
    assert "shap_attributions" in data


def test_judge_demo_v1():
    res = client.post("/api/v1/judge-demo/run")
    assert res.status_code == 200
    data = res.json()
    assert data["hero_demo_status"] == "SUCCESS"
    assert len(data["steps"]) == 10
