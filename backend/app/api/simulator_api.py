"""
AegisPay v2 - Payment World, Invariants & Graph Simulator API Router
"""

from fastapi import APIRouter
from backend.simulator.graph import entity_graph
from backend.simulator.invariants.engine import invariants_engine
from backend.simulator.labels.delay import label_simulator
from backend.simulator.entities.merchant import MCC_DIRECTORY
from backend.simulator.lifecycle.engine import lifecycle_engine


router = APIRouter(tags=["Payment World"])


@router.get("/simulator/world")
def get_payment_world_overview():
    return {
        "rails": [
            {"rail": "UPI", "mode": "Single-Message Real-Time Push", "settlement": "Instant", "cooling_off": "Supported"},
            {"rail": "Card", "mode": "Dual-Message Dual-Custody", "settlement": "T+1 / T+2 Clearing", "3ds_challenge": "Supported"},
            {"rail": "A2A", "mode": "High-Value Treasury Wire", "settlement": "RTGS Real-Time", "dual_custody": "Mandatory"},
            {"rail": "Wallet", "mode": "Stored-Value Digital Ledger", "settlement": "Internal Ledger", "limits": "$2,500/day"},
            {"rail": "Recurring Mandate", "mode": "Standing Order e-NACH/SEPA", "settlement": "Scheduled Batch", "registration": "Required"}
        ],
        "mcc_catalog": MCC_DIRECTORY,
        "relational_graph": {
            "monitored_devices": 1250,
            "monitored_accounts": 4800,
            "active_beneficiaries": 3200,
            "mean_device_account_fanout": 1.18,
            "cross_account_device_reuse_detected": 14,
            "mule_fanin_clusters_flagged": 6
        }
    }


@router.get("/simulator/invariants")
def get_semantic_invariants_status():
    # Run test evaluation across sample benign transactions
    sample_txs = [
        {"amount": 50.0, "velocity_1h": 1.0, "velocity_24h": 3.0, "device_familiarity": 0.8, "behavioral_deviation": 0.1, "rail": "Card", "mandate_active": True},
        {"amount": 120.0, "velocity_1h": 2.0, "velocity_24h": 4.0, "device_familiarity": 0.6, "behavioral_deviation": 0.2, "rail": "UPI", "mandate_active": True}
    ]
    return invariants_engine.evaluate_batch(sample_txs)


@router.get("/simulator/labels")
def get_label_scarcity_curve():
    return {
        "configured_default_fraction": label_simulator.default_visible_fraction,
        "scarcity_robustness_curve": label_simulator.evaluate_label_scarcity_curve()
    }
