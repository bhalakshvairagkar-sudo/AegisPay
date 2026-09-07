"""
AegisPay v2 - Point-in-Time Temporal Training Guards
Guarantees that feature timestamps <= decision timestamp and label timestamp >= event timestamp.
"""

from typing import Dict, Any, List


class TemporalLeakageError(Exception):
    """Raised when future temporal information is used in current decision feature extraction."""
    pass


class FutureFeatureError(TemporalLeakageError):
    """Feature timestamp is strictly in the future relative to transaction decision time."""
    pass


class FutureLabelError(TemporalLeakageError):
    """Label timestamp is prematurely exposed before its realistic maturity window."""
    pass


def assert_point_in_time_validity(
    feature_timestamp_epoch: float,
    decision_timestamp_epoch: float,
    label_timestamp_epoch: float,
    is_training_phase: bool = True
):
    """Machine-enforced assertion that no future leakage occurs in model training or scoring."""
    # 1. Feature cannot use future information
    if feature_timestamp_epoch > decision_timestamp_epoch:
        raise FutureFeatureError(
            f"TEMPORAL LEAKAGE: Feature timestamp ({feature_timestamp_epoch}) > decision timestamp ({decision_timestamp_epoch})."
        )

    # 2. In point-in-time training, if label is unconfirmed at decision time, it cannot be leaked into feature set
    if is_training_phase and label_timestamp_epoch < decision_timestamp_epoch:
        raise FutureLabelError(
            f"TEMPORAL LEAKAGE: Ground-truth label timestamp ({label_timestamp_epoch}) precedes decision timestamp ({decision_timestamp_epoch})."
        )
