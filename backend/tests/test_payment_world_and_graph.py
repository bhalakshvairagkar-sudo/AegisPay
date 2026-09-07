"""
Tests for Relational Graph, Multi-Rail Lifecycles, and Label Scarcity.
"""

import pytest
from backend.simulator.graph import RelationalEntityGraph
from backend.simulator.lifecycle.engine import lifecycle_engine
from backend.simulator.labels.delay import label_simulator


def test_relational_graph_fanout_detection():
    graph = RelationalEntityGraph()
    # 3 accounts accessed from same device DEV-101
    graph.record_transaction_event("USER-1", "ACCT-1", "DEV-101")
    graph.record_transaction_event("USER-2", "ACCT-2", "DEV-101")
    graph.record_transaction_event("USER-3", "ACCT-3", "DEV-101")

    assert graph.get_device_account_fanout("DEV-101") == 3
    assert graph.is_cross_account_device_reuse("DEV-101") is True

    signals = graph.get_graph_relational_features("USER-1", "ACCT-1", "DEV-101")
    assert signals["cross_account_device_reuse_flag"] == 1
    assert signals["graph_fanout_risk_score"] > 0.0


def test_multi_stage_lifecycle_simulation():
    sess = lifecycle_engine.simulate_full_lifecycle(
        transaction_id="TX-TEST-001",
        rail="Card",
        amount=150.0,
        is_fraud=False,
        policy_action="ALLOW"
    )
    assert sess.is_completed is True
    assert len(sess.events) >= 4
    stages = [e.stage for e in sess.events]
    assert "INITIATION" in stages
    assert "AUTHENTICATION" in stages
    assert "AUTHORIZATION" in stages
    assert "SETTLEMENT" in stages


def test_label_delay_scarcity():
    attrs = label_simulator.compute_label_attributes(
        event_time_epoch=100000.0,
        is_fraud=True,
        visibility_fraction_override=0.05
    )
    assert "label_maturity_delay_hours" in attrs
    assert attrs["label_timestamp_epoch"] >= attrs["decision_timestamp_epoch"]
