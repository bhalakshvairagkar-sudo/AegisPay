"""
AegisPay v2 - Typed Attack Grammar
Defines the 7-slot semantic attack composition model and 5 metadata attributes.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import hashlib
import json


# -------------------------------------------------------------
# 7 SEMANTIC ATTACK SLOTS VOCABULARIES
# -------------------------------------------------------------

ACCESS_MECHANISMS = [
    "Credential Stuffing",
    "Session Hijacking",
    "SIM Swap",
    "Social Engineering Phishing",
    "Malware Protocol Downgrade",
    "Automated Botnet",
    "Malware Agent",
    "Voice Call Deception",
    "Malicious QR Code",
    "Screen Sharing Malware",
    "Contextual SMS/Email Chatbot",
    "Voice Clone Telephony",
    "Compromised Merchant Key",
    "Man-in-the-Middle Network Proxy",
    "Card Testing Botnet",
    "Stolen Card Credentials",
    "Corrupted Point-of-Sale Terminal",
    "Compromised Merchant Account",
    "Stolen Card Portfolio",
    "Distributed Proxy Network",
    "Legitimate Cardholder Credentials",
    "Affiliate Tracking Cookie Stuffing",
    "Stolen SSN/Tax ID + Real Address",
    "Synthetic Identity Credential",
    "Synthetic Face GAN Generation",
    "Purchased Student/Dormant Account",
    "Puppeteer Automated Framework",
    "Compromised Smart Home Botnet",
    "Rooted Virtual Machine Cluster",
    "Mock Location Provider Service",
    "Adversarial ML Model Probe",
    "Autonomous Multi-Agent Generative AI",
    "Stolen Credentials with Genetic Algorithm"
]

TRUST_MECHANISMS = [
    "Residential Proxy",
    "Cookie Replay",
    "Carrier Spoof",
    "Compromised SSO",
    "Client Feature Stripping",
    "Biometric Mimicry",
    "Browser Environment Hook",
    "Geofence Match",
    "Emulated Touch Screen",
    "Legitimate User Device",
    "Legitimate Mobile App",
    "Legitimate Session",
    "Lookalike Merchant Web",
    "Internal Employee Trust",
    "Automated Billing Agreement",
    "Interbank Gateway Session",
    "Direct Merchant API",
    "Automated Fuel / Hospitality Merchant",
    "Merchant Refund Privilege",
    "Established Terminal ID",
    "Legitimate Retail Platform",
    "Public Checkout Endpoint",
    "Legitimate Device & IP",
    "Affiliate Network Key",
    "Fabricated Credit Bureau History",
    "Clean Payment History",
    "Virtual Camera Driver",
    "Established Account Vintage",
    "Forged Browser Fingerprint",
    "Local Residential ISP IP",
    "Generated IMEI/Android ID",
    "Spoofed Geo Coordinates",
    "Multi-Account Probing",
    "Synthetic Persona Cluster"
]

PAYMENT_RAILS = [
    "UPI",
    "Card",
    "A2A",
    "Wallet",
    "Recurring Mandate"
]

EVASION_MECHANISMS = [
    "Temporal Pacing",
    "Header Mimicry",
    "Carrier Porting Pacing",
    "OAuth Scope Abuse",
    "Fallback Downgrade",
    "Synthetic Keystroke Cadence",
    "Deterministic Trajectory",
    "Temporal Timing Alignment",
    "Bezier Curve Touch Emulation",
    "Artificial Hesitation Jitter",
    "Legitimate User Biometrics",
    "Deceptive Mandate Description",
    "Remote Cursor Injection",
    "Dynamic LLM Personalization",
    "Acoustic Voice Print Match",
    "Micro Amount Below Alert Trigger",
    "Header Preserved Payload Modified",
    "Algorithmic Expiry/CVV Step",
    "Exploit Settlement Latency Window",
    "Orphan Refund Request",
    "Inflated Low-Velocity Legitimate Purchases",
    "Victim Real Address Shipping",
    "Luhn-Compliant Synthetic Range",
    "Legitimate Baseline Mimicry",
    "Purchases Cancelled Post Commission Settlement",
    "Dormant Account Seasoning",
    "Perfect Repayment Behavior Before Raid",
    "Synthesized Liveness Verification Response",
    "Rapid In-and-Out Smurfing",
    "Faked Hardware Telemetry",
    "Local Subnet IP Geo Match",
    "Fake Proximity to Merchant POS",
    "Perturbation Directed at Decision Surface",
    "Coordinated Cross-Platform Synthetic History",
    "Evolutionary Feature Space Trajectory"
]

BEHAVIORAL_PATTERNS = [
    "Synthetic Cadence",
    "Burst Rapid Action",
    "New Device First Login",
    "Security Profile Modification",
    "Failing Hardware Auth",
    "Learned Timing Jitter",
    "Zero Hesitation Navigation",
    "Baseline Hour Mimicry",
    "Curved Drag Events",
    "Humanized Thinking Pauses",
    "High Urgency Out-of-Pattern Transfer",
    "Subscription Registration",
    "Concurrent Accessibility Service",
    "Real-Time Dynamic Dialogue",
    "High Value Corporate Wire",
    "High Cardinality Low Ticket",
    "Beneficiary Routing Alteration",
    "Rapid Sequential Micro Authorizations",
    "Multiple Concurrent Pre-Auths",
    "Refund Without Prior Charge",
    "Structured Off-Peak Settlements",
    "Third-Party Consumer Fulfillment",
    "High Velocity Testing",
    "Normal Checkout followed by Claim",
    "High Volume Referrals",
    "Gradual Balance Building",
    "Sudden 100% Utilization",
    "Virtual Video Stream Injection",
    "Sudden Reactivation After Dormancy",
    "Scripted DOM Interactions",
    "Attacker Remote Commands",
    "Automated UI Automation Framework",
    "Static Coordinate Broadcast",
    "Boundary Wandering",
    "Distributed Adaptive Activity",
    "Stepwise Perturbations"
]

MONETIZATION_PATHWAYS = [
    "P2P Transfer",
    "Immediate Checkout",
    "Immediate P2P Drain",
    "Beneficiary Addition",
    "Card Not Present Checkout",
    "Digital Goods Purchase",
    "High Velocity Merchant Cart",
    "Scheduled Bill Pay Abuse",
    "Wallet Top-Up",
    "Split P2P Transfer",
    "Immediate Mule Account Credit",
    "Future Automated Pulls",
    "Multiple Rapid Beneficiary Payouts",
    "Merchant Token Harvesting",
    "Overseas Beneficiary Escrow",
    "Dispersed Aggregate Extraction",
    "Intermediary Mule Redirection",
    "Card Validity Verification",
    "Instant Asset Extraction",
    "Direct Credit to Attacker Card",
    "Merchant Payout Splitting",
    "Marketplace Cash Collection",
    "Valid Account Identification",
    "Item Retained + Chargeback Credit",
    "Affiliate Network Commission",
    "Full Credit Line Drawdown",
    "Immediate Multi-Channel Cash Advances",
    "Account Unlocking for Mule Operation",
    "Layered Crypto/P2P Dispersal",
    "E-Commerce Checkout",
    "P2P Wallet Drain",
    "New User Bonus & P2P Drain",
    "Proximity-Based Payment Authorization",
    "High Value Transfer Just Below Threshold",
    "Multi-Channel Loan & Overdraft Drain",
    "Gradual Account Liquidation"
]

TEMPORAL_PATTERNS = [
    "Micro-Pacing",
    "Instantaneous Burst",
    "Post-Midnight Quiet Window",
    "Low Velocity Probe",
    "Sequential Retries",
    "Realistic Typing Intervals",
    "Sub-Second Form Fill",
    "Cardholder Active Window",
    "Uniform Inter-Touch Spacing",
    "Gaussian Pauses Between Inputs",
    "Call Concurrent Session",
    "Delayed Recurring Schedule",
    "Extended Inactive Baseline Then Burst",
    "Rapid Responsive Exchange",
    "End-of-Quarter Financial Close",
    "Periodic Staggered Execution",
    "In-Flight Packet Interception",
    "Millisecond Cadence",
    "Simultaneous Geographic Locations",
    "End-of-Day Settlement Batch",
    "Late Night Batch Processing",
    "Order Concurrent Timing",
    "Constant Distributed Rate",
    "Dispute Lodged 30 Days Post-Tx",
    "Synchronized with Commission Lock Windows",
    "Months-Long Maturation",
    "Coordinated 48-Hour Bust-Out",
    "Single-Attempt Instant Onboarding",
    "Hop Transfers Within 60 Seconds",
    "Scheduled Script Execution",
    "Distributed Inter-Request Intervals",
    "Concurrent Mass Execution",
    "Instantaneous Teleportation Across Cities",
    "Iterative Feedback-Guided Probes",
    "Synchronized Cross-Entity Action",
    "Adaptive Dynamic Pacing"
]


# -------------------------------------------------------------
# ATTACK COMPOSITION DATACLASS
# -------------------------------------------------------------

@dataclass
class AttackComposition:
    # 7 Semantic Attack Slots
    access: str
    trust: str
    rail: str
    evasion: str
    behavior: str
    monetization: str
    temporal_pattern: str

    # 5 Metadata Attributes
    family: str = "Unknown"
    vector: str = "CUSTOM-01"
    difficulty: int = 1  # Tier 1 to 5
    seed: int = 42
    provenance: str = "DESIGN TARGET"  # MEASURED / DERIVED / DESIGN TARGET

    def get_composition_signature(self) -> str:
        """Returns a deterministic SHA256 signature for this exact semantic composition."""
        content = f"{self.access}|{self.trust}|{self.rail}|{self.evasion}|{self.behavior}|{self.monetization}|{self.temporal_pattern}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slots": {
                "access": self.access,
                "trust": self.trust,
                "rail": self.rail,
                "evasion": self.evasion,
                "behavior": self.behavior,
                "monetization": self.monetization,
                "temporal_pattern": self.temporal_pattern
            },
            "metadata": {
                "family": self.family,
                "vector": self.vector,
                "difficulty": self.difficulty,
                "seed": self.seed,
                "provenance": self.provenance,
                "composition_id": f"CMP-{self.get_composition_signature()}"
            }
        }
