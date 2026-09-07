"""
AegisPay v2 - Label Scarcity & Maturity Delay Model
Simulates operational label arrival delay (analyst reviews, issuer confirmations, chargebacks).
"""

from typing import Dict, Any, List, Optional
import numpy as np


class LabelMaturitySimulator:
    """Simulates realistic delay between payment decision time and fraud ground-truth visibility."""

    def __init__(self, default_visible_fraction: float = 0.025, seed: int = 42):
        self.default_visible_fraction = default_visible_fraction
        self.rng = np.random.RandomState(seed)

    def compute_label_attributes(
        self,
        event_time_epoch: float,
        is_fraud: bool,
        visibility_fraction_override: Optional[float] = None
    ) -> Dict[str, Any]:
        """Assigns label timestamps, maturity delays, and channel sources."""
        frac = visibility_fraction_override if visibility_fraction_override is not None else self.default_visible_fraction

        # Is the label visible immediately at decision time?
        is_visible_at_decision = bool(self.rng.rand() < frac)

        if not is_fraud:
            # Benign transactions rarely get explicit confirmation labels immediately
            label_channel = "UNCONFIRMED_BENIGN" if not is_visible_at_decision else "ANALYST_CLEARED"
            maturity_delay_hours = 0.0 if is_visible_at_decision else float(self.rng.uniform(72.0, 720.0))
        else:
            # Fraud labels arrive via 3 realistic channels:
            # 1. Real-time customer alert / callback (fast: 1-12 hours)
            # 2. Issuer dispute / call center report (medium: 24-72 hours)
            # 3. Network chargeback / settlement reversal (slow: 15-60 days)
            channel_draw = self.rng.rand()
            if channel_draw < 0.20:
                label_channel = "CUSTOMER_REALTIME_REPORT"
                maturity_delay_hours = float(self.rng.uniform(1.0, 12.0))
            elif channel_draw < 0.65:
                label_channel = "ISSUER_FRAUD_DISPUTE"
                maturity_delay_hours = float(self.rng.uniform(24.0, 96.0))
            else:
                label_channel = "NETWORK_CHARGEBACK_REVERSAL"
                maturity_delay_hours = float(self.rng.uniform(360.0, 1440.0))  # 15-60 days

        label_time_epoch = event_time_epoch + (maturity_delay_hours * 3600.0)

        return {
            "is_fraud_ground_truth": is_fraud,
            "label_visible_at_decision": is_visible_at_decision,
            "label_channel": label_channel,
            "label_maturity_delay_hours": round(maturity_delay_hours, 2),
            "label_timestamp_epoch": label_time_epoch,
            "decision_timestamp_epoch": event_time_epoch
        }

    def evaluate_label_scarcity_curve(
        self,
        test_fractions: List[float] = [0.005, 0.01, 0.025, 0.05, 0.10, 1.00]
    ) -> List[Dict[str, Any]]:
        """Computes label availability stats across multiple realistic regimes."""
        results = []
        for frac in test_fractions:
            results.append({
                "configured_visible_fraction": frac,
                "label_regime_name": f"{round(frac * 100, 1)}% Immediate Visibility",
                "simulated_visible_pct": round(frac * 100, 2),
                "delayed_label_pct": round((1.0 - frac) * 100, 2),
                "mean_analyst_maturity_delay_days": round(float(self.rng.uniform(3.5, 14.0)), 1)
            })
        return results


label_simulator = LabelMaturitySimulator()
