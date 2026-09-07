"""
AegisPay v2 - Fixed Operational Reason Codes
Defines 20 standardized, operational reason codes for analyst investigations and policy decisions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ReasonCodeDefinition:
    code: str
    short_name: str
    category: str
    operational_action: str
    description: str


REASON_CODES: Dict[str, ReasonCodeDefinition] = {
    "R01": ReasonCodeDefinition("R01", "New Unrecognized Device", "Device", "Step-Up 3DS / Biometric Challenge", "Transaction initiated from a hardware fingerprint never previously bound to cardholder."),
    "R02": ReasonCodeDefinition("R02", "Device-Account Fanout", "Relational", "Manual Fraud Hold", "Device fingerprint has authenticated with 3+ distinct cardholder credentials in 24h."),
    "R03": ReasonCodeDefinition("R03", "Abnormal Velocity Surge", "Velocity", "Rate Limit & Step-Up", "Transaction frequency in 1h window exceeds 4x historical baseline."),
    "R04": ReasonCodeDefinition("R04", "New High-Risk Beneficiary", "Beneficiary", "Cooling-Off 4H Hold", "First-time transfer to a newly added payee account exceeding $500 threshold."),
    "R05": ReasonCodeDefinition("R05", "Unusual Out-of-Pattern Amount", "Financial", "Step-Up Authentication", "Ticket amount exceeds 3 standard deviations of user 90-day spending profile."),
    "R06": ReasonCodeDefinition("R06", "Geographic Haversine Anomaly", "Location", "Step-Up Challenge", "Physical transit speed between successive transactions implies impossible supersonic displacement."),
    "R07": ReasonCodeDefinition("R07", "Session Cadence Anomaly", "Behavioral", "Manual Review Queue", "Form interaction dwell and typing pacing deviates significantly from human baseline."),
    "R08": ReasonCodeDefinition("R08", "Authentication Inconsistency", "Security", "Deny & Force Re-Auth", "Client header indicates feature stripping or fallback downgrade from WebAuthn."),
    "R09": ReasonCodeDefinition("R09", "High-Risk Merchant MCC", "Merchant", "Enhanced Risk Scoring", "Transaction routed to merchant category associated with quasi-cash or crypto off-ramps."),
    "R10": ReasonCodeDefinition("R10", "Temporal Timing Anomaly", "Temporal", "Passive Risk Flag", "High-value transaction attempted during dormant off-peak midnight hours."),
    "R11": ReasonCodeDefinition("R11", "Carrier SIM Porting Alert", "Carrier", "24-Hour Cooling Off", "Cellular subscriber IMSI altered within preceding 48 hours."),
    "R12": ReasonCodeDefinition("R12", "Mule Beneficiary Fan-In", "Graph", "Silent Freeze Account", "Payee account receiving rapid fan-in credits from multiple unrelated source accounts."),
    "R13": ReasonCodeDefinition("R13", "International Cross-Border Mismatch", "Geography", "Step-Up 3DS", "Payment issued to overseas acquiring endpoint without historical cross-border travel."),
    "R14": ReasonCodeDefinition("R14", "Sub-Threshold Amount Cluster", "Structuring", "Aggregate Monitoring", "Repetitive structured payments just below statutory reporting limit ($2,000 / $10,000)."),
    "R15": ReasonCodeDefinition("R15", "Rooted / Emulator Environment", "Device", "Hard Decline", "Android emulator, rooted jailbreak sandbox, or virtual webcam hook detected."),
    "R16": ReasonCodeDefinition("R16", "Mandate Authorization Inconsistency", "Mandate", "Refuse Registration", "Recurring mandate creation requested with immediate maximal recurring amount."),
    "R17": ReasonCodeDefinition("R17", "Regulatory Ceiling Exceeded", "Compliance", "Hard Block", "Single transaction amount strictly exceeds statutory clearing threshold."),
    "R18": ReasonCodeDefinition("R18", "Unsupervised Isolation Anomaly", "Novelty", "Manual Review Queue", "Transaction feature vector occupies a sparse unpopulated manifold in latent space."),
    "R19": ReasonCodeDefinition("R19", "Adversarial Gradient Surface Match", "Model Defense", "Silent Honeypot Route", "Perturbations exhibit signature boundary-wandering orthogonal to model gradients."),
    "R20": ReasonCodeDefinition("R20", "Normal Low-Risk Profile", "Baseline", "Frictionless Allow", "All behavioral, device, and financial indicators align with legitimate baseline.")
}


def map_features_to_reason_codes(
    feature_dict: Dict[str, Any],
    calibrated_prob: float,
    shap_attributions: Optional[Dict[str, float]] = None
) -> List[str]:
    """Deterministically identifies the top primary reason codes for a transaction."""
    codes = []
    amt = float(feature_dict.get("amount", 0.0))
    v1 = float(feature_dict.get("velocity_1h", 1.0))
    df = float(feature_dict.get("device_familiarity", 0.7))
    geo = float(feature_dict.get("geo_distance_km", 0.0))
    bd = float(feature_dict.get("behavioral_deviation", 0.1))
    sim = int(feature_dict.get("carrier_change_flag", 0))
    mcc_risk = float(feature_dict.get("mcc_risk_weight", 0.1))
    fanout = int(feature_dict.get("device_account_fanout", 1))

    if calibrated_prob < 0.25:
        return ["R20"]

    if fanout >= 3:
        codes.append("R02")
    if df < 0.25:
        codes.append("R01")
    if v1 >= 5.0:
        codes.append("R03")
    if amt > 2500.0:
        codes.append("R05")
    if geo > 500.0:
        codes.append("R06")
    if bd > 0.60:
        codes.append("R07")
    if sim == 1:
        codes.append("R11")
    if mcc_risk > 0.70:
        codes.append("R09")

    if not codes:
        codes.append("R18" if calibrated_prob > 0.60 else "R20")

    return codes[:3]  # Return top 3 operational reason codes
