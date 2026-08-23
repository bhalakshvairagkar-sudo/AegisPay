"""
Unit Tests for Synthetic Payment Simulator
"""

import pytest
import numpy as np
from backend.simulator.transactions import PaymentSimulator, haversine_distance


def test_haversine_distance():
    # Distance between NYC and LA is ~3940 km
    d = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert 3900 < d < 4000
    # Zero distance for same point
    assert haversine_distance(10.0, 20.0, 10.0, 20.0) == 0.0


def test_simulator_reproducibility():
    sim1 = PaymentSimulator(seed=42)
    sim2 = PaymentSimulator(seed=42)

    txns1 = sim1.generate_legitimate_stream(50)
    txns2 = sim2.generate_legitimate_stream(50)

    for t1, t2 in zip(txns1, txns2):
        assert t1.amount == t2.amount
        assert t1.velocity_1h == t2.velocity_1h
        assert t1.device_familiarity == t2.device_familiarity
        assert t1.geo_distance_km == t2.geo_distance_km


def test_legitimate_transaction_distributions():
    sim = PaymentSimulator(seed=123)
    txns = sim.generate_legitimate_stream(200)

    amounts = [t.amount for t in txns]
    velocities = [t.velocity_1h for t in txns]
    device_fams = [t.device_familiarity for t in txns]

    # Amounts are positive and log-normally bounded
    assert min(amounts) >= 2.50
    assert np.median(amounts) < 250.0  # Most transactions are everyday amounts

    # Low velocity for legitimate users
    assert np.mean(velocities) < 2.0

    # High device familiarity on average for legitimate users
    assert np.mean(device_fams) > 0.70
