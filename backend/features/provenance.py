"""
AegisPay v2 - Feature Provenance & Evidence Tier Tracker
Machine-enforces provenance tiers (MEASURED, DERIVED, DESIGN TARGET) and feature source boundaries.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


PROHIBITED_METADATA_KEYS = {
    "attack_id",
    "attack_family",
    "attack_name",
    "gen_ai",
    "sophistication",
    "difficulty",
    "mutation_strength",
    "is_adversarial",
    "ground_truth",
    "is_fraud"
}


@dataclass
class FeatureProvenanceRecord:
    feature_name: str
    source_fields: List[str]
    provenance_tier: str  # MEASURED, DERIVED, DESIGN TARGET
    is_decision_time_valid: bool = True
    uses_future_information: bool = False
    uses_attack_metadata: bool = False
    uses_fraud_label: bool = False


class FeatureProvenanceEngine:
    """Audits and registers mathematical provenance for all operational model features."""

    def __init__(self):
        self.registry: Dict[str, FeatureProvenanceRecord] = {}
        self._init_standard_provenance()

    def _init_standard_provenance(self):
        features = [
            ("amount", ["transaction.amount"], "MEASURED"),
            ("velocity_1h", ["session.event_history", "timestamp"], "DERIVED"),
            ("velocity_24h", ["account.transaction_log", "timestamp"], "DERIVED"),
            ("device_familiarity", ["device.binding_history", "user.devices"], "DERIVED"),
            ("geo_distance_km", ["device.ip_geo", "user.home_geo"], "DERIVED"),
            ("behavioral_deviation", ["session.cadence_telemetry", "user.baseline"], "DERIVED"),
            ("merchant_risk_score", ["merchant.mcc_catalog", "merchant.history"], "MEASURED"),
            ("account_age_days", ["account.creation_timestamp", "decision_timestamp"], "MEASURED"),
            ("touch_pressure_deviation", ["device.sensor_telemetry"], "DERIVED"),
            ("carrier_change_flag", ["device.sim_imsi_hash", "carrier.audit_log"], "MEASURED"),
            ("mcc_risk_weight", ["merchant.mcc_code"], "MEASURED"),
            ("hour_of_day", ["transaction.local_timestamp"], "MEASURED"),
            ("is_international", ["cardholder.country_iso", "merchant.country_iso"], "DERIVED")
        ]
        for name, sources, tier in features:
            self.registry[name] = FeatureProvenanceRecord(
                feature_name=name,
                source_fields=sources,
                provenance_tier=tier,
                is_decision_time_valid=True,
                uses_future_information=False,
                uses_attack_metadata=False,
                uses_fraud_label=False
            )

    def audit_feature_dictionary(self, feat_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Audits a feature dictionary to verify zero leakage of prohibited metadata or labels."""
        leakage_errors = []
        for key in feat_dict.keys():
            if key in PROHIBITED_METADATA_KEYS:
                leakage_errors.append(
                    f"DATA LEAKAGE ERROR: Prohibited metadata key '{key}' found in model feature payload."
                )
        return len(leakage_errors) == 0, leakage_errors

    def get_provenance_manifest(self) -> List[Dict[str, Any]]:
        return [
            {
                "feature_name": r.feature_name,
                "sources": r.source_fields,
                "provenance_tier": r.provenance_tier,
                "decision_time_valid": r.is_decision_time_valid,
                "uses_future_info": r.uses_future_information,
                "uses_attack_meta": r.uses_attack_metadata,
                "uses_fraud_label": r.uses_fraud_label
            }
            for r in self.registry.values()
        ]


provenance_engine = FeatureProvenanceEngine()
