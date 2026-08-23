"""
AegisPay Attack Taxonomy & Threat Knowledge Graph
Provides 36 standardized adversarial attack vectors categorized across 8 distinct families.
Structured for defensive simulation and ML detection research.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import json
from pathlib import Path


@dataclass
class AttackVector:
    id: str
    family: str
    name: str
    gen_ai: bool
    sophistication: float  # 1.0 - 10.0 scale
    severity: str          # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    detectability: str     # 'VERY LOW', 'LOW', 'MEDIUM', 'HIGH'
    evasion_strategy: str
    signals: List[str]
    description: str
    mitigation_policy: str
    affected_channel: str = "Card-Not-Present (CNP) / Digital Banking"
    threat_actor_profile: str = "Organized Fraud Syndicate / AI-Equipped Bad Actor"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Add camelCase alias for frontend compatibility
        d["genAi"] = self.gen_ai
        d["evasionStrategy"] = self.evasion_strategy
        d["mitigationPolicy"] = self.mitigation_policy
        return d


ATTACK_TAXONOMY_RAW: List[AttackVector] = [
    # Family 1: Account Takeover (ATO)
    AttackVector(
        id="ATO-01",
        family="Account Takeover",
        name="Distributed Credential Probing with Micro-Delays",
        gen_ai=True,
        sophistication=6.8,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Rotates residential IPs and adds micro-delays mimicking human keystrokes.",
        signals=["IP Velocity Anomaly", "Device Familiarity Low", "Inter-keystroke Delay Variance"],
        description="Automated credential validation utilizing rotating residential endpoints and natural cadence synthesis.",
        mitigation_policy="Step-Up 3DS authentication upon low device familiarity and IP subnet transitions.",
    ),
    AttackVector(
        id="ATO-02",
        family="Account Takeover",
        name="Session Token Reuse with Geolocation Match",
        gen_ai=False,
        sophistication=8.1,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Reuses valid authorization headers through localized proxy gateways to match cardholder metro area.",
        signals=["Cookie Age Delta", "TLS Fingerprint Inconsistency", "Unusual Merchant MCC"],
        description="Replays hijacked session tokens through geographical proximity tunnels without triggering broad IP velocity alerts.",
        mitigation_policy="Enforce continuous behavioral biometric verification and device binding assertions.",
    ),
    AttackVector(
        id="ATO-03",
        family="Account Takeover",
        name="Carrier Migration & Liquidity Drain Simulation",
        gen_ai=True,
        sophistication=8.9,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Executes immediate high-ticket liquidation following mobile network carrier re-registration events.",
        signals=["Carrier Change Event", "Immediate High Amount", "Password Reset Timestamp Delta"],
        description="Models rapid balance liquidation following mobile SIM migration and authentication re-routing.",
        mitigation_policy="Apply 24-hour transaction velocity cap and biometric step-up following carrier porting flags.",
    ),
    AttackVector(
        id="ATO-04",
        family="Account Takeover",
        name="Multi-Card Password Probe Cascade",
        gen_ai=False,
        sophistication=5.4,
        severity="MEDIUM",
        detectability="HIGH",
        evasion_strategy="Distributes sequential password reset inquiries across secondary linked payment cards.",
        signals=["Multi-Account Reset Spike", "Failed Authorization Velocity", "Subnet Burst"],
        description="Multi-account credential recovery probing against interconnected issuer portfolios.",
        mitigation_policy="Enforce cross-account velocity throttles and mandatory secondary channel verification.",
    ),
    AttackVector(
        id="ATO-05",
        family="Account Takeover",
        name="Passkey / WebAuthn Downgrade Fallback Probe",
        gen_ai=True,
        sophistication=8.5,
        severity="HIGH",
        detectability="LOW",
        evasion_strategy="Simulates client-side biometric capability failures to force downgrade to vulnerable SMS/OTP channels.",
        signals=["Authenticator Capability Flag Mismatch", "Immediate Fallback Trigger", "New IP Geolocation"],
        description="Coerces authorization flow into legacy verification channels by reporting simulated secure-enclave hardware errors.",
        mitigation_policy="Prohibit silent downgrades to SMS OTP on high-value transfers without device attestation.",
    ),

    # Family 2: Behavioral Impersonation (BIO)
    AttackVector(
        id="BIO-01",
        family="Behavioral Impersonation",
        name="Synthetic Keystroke & Pointer Physics Synthesis",
        gen_ai=True,
        sophistication=9.2,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Generative models synthesize realistic pointer curvature, acceleration profiles, and typing jitter.",
        signals=["Subtle Biometric Variance", "Cadence Normalization", "Synthetic Acceleration Profile"],
        description="Emulates human-like pointer physics and keyboard touch dynamics to neutralize naive behavioral variance models.",
        mitigation_policy="Deploy high-dimensional spectral biometrics and multi-window micro-movement entropy checks.",
    ),
    AttackVector(
        id="BIO-02",
        family="Behavioral Impersonation",
        name="Checkout Navigation Flow Replay",
        gen_ai=False,
        sophistication=7.0,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Follows empirical standard deviation of legitimate checkout DOM interaction times.",
        signals=["Page Duration Uniformity", "DOM Interaction Delta", "Catalog Dwell Time Anomaly"],
        description="Automated checkout trajectory simulation matching statistical dwell times of genuine shoppers.",
        mitigation_policy="Correlate checkout dwell entropy with concurrent touch/gyroscope physical telemetry.",
    ),
    AttackVector(
        id="BIO-03",
        family="Behavioral Impersonation",
        name="Temporal Adaptive Purchase Profiling",
        gen_ai=True,
        sophistication=8.4,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Restricts unauthorized charges strictly to the historical shopping time windows of the cardholder.",
        signals=["Amount Trajectory Step", "Off-brand MCC Transition", "Velocity Deviation"],
        description="Executes fraudulent authorizations timed precisely to match cardholder active waking hours and shopping habits.",
        mitigation_policy="Cross-reference merchant category affinity and multi-day spending momentum.",
    ),
    AttackVector(
        id="BIO-04",
        family="Behavioral Impersonation",
        name="Synthetic Touch Pressure & Gyroscope Mimicry",
        gen_ai=True,
        sophistication=9.5,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Injects synthetic mobile device orientation and touch surface area distributions.",
        signals=["Sensor Payload Smoothness", "Orientation Lock Inconsistency", "Touch Area Invariance"],
        description="Bypasses mobile behavioral SDK heuristics by injecting synthetic motion sensor streams.",
        mitigation_policy="Analyze micro-vibrational noise harmonics and sensor hardware drift signatures.",
    ),
    AttackVector(
        id="BIO-05",
        family="Behavioral Impersonation",
        name="Dwell-Time Micro-Pacing Synthesis",
        gen_ai=True,
        sophistication=8.7,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Dynamically modulates payment form field dwell durations based on cardholder age and device baseline.",
        signals=["Inter-Field Dwell Distribution", "Scroll Momentum Variance", "Typing Burst Regularity"],
        description="Synthesizes realistic pauses and typing hesitations matching cardholder historical biometric distributions.",
        mitigation_policy="Integrate multi-modal sensor fusion combining touch dwell with capacitive contact size variance.",
    ),

    # Family 3: Social Engineering & APP Fraud (SOC)
    AttackVector(
        id="SOC-01",
        family="Social Engineering",
        name="Manipulated Authorized Push Payment (APP)",
        gen_ai=True,
        sophistication=9.4,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Legitimate cardholder initiates transaction from their authentic trusted device under deception.",
        signals=["New Payee High Amount", "Concurrent Voice Call Metadata", "Account Drain Velocity"],
        description="Cardholder is coerced into sending authorized high-value transfers to synthetic mule endpoints.",
        mitigation_policy="Hold transfer execution when active call signals coincide with rapid first-time payee additions.",
    ),
    AttackVector(
        id="SOC-02",
        family="Social Engineering",
        name="Contextual Subscription Mandate Injection",
        gen_ai=True,
        sophistication=7.9,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Injects low-ticket recurring mandate authorization requests disguised as standard digital services.",
        signals=["Referrer Header Anomaly", "Mandate Setup Burst", "Low Initial Auth Amount"],
        description="Deceives consumer into approving recurring standing authorizations using personalized merchant lures.",
        mitigation_policy="Mandate explicit multi-factor confirmation for initial standing instruction authorizations.",
    ),
    AttackVector(
        id="SOC-03",
        family="Social Engineering",
        name="Assisted Remote Access Liquidation",
        gen_ai=False,
        sophistication=6.2,
        severity="MEDIUM",
        detectability="HIGH",
        evasion_strategy="Guides victim to initiate instant peer-to-peer balance exhaust under the guise of an overpayment refund.",
        signals=["Remote Management Tool Active", "Peer-to-Peer Spike", "Session Duration Spike"],
        description="Simulates remote-desktop guided peer-to-peer liquidity drain targeting vulnerable accounts.",
        mitigation_policy="Detect active remote desktop management sessions and delay real-time outgoing settlements.",
    ),
    AttackVector(
        id="SOC-04",
        family="Social Engineering",
        name="Autonomous Collaborative Card-Testing Swarm",
        gen_ai=True,
        sophistication=9.7,
        severity="CRITICAL",
        detectability="VERY LOW",
        evasion_strategy="Multi-agent swarm dynamically negotiates authorization amounts and merchant endpoints in real time.",
        signals=["Cross-Merchant Micro-Probe", "Parameter Mutation Pattern", "Distributed Timing Correlation"],
        description="Coordinated agent network testing card validity across distributed low-friction merchant gateways.",
        mitigation_policy="Deploy cross-merchant network graph analytics to detect distributed micro-probe patterns.",
    ),
    AttackVector(
        id="SOC-05",
        family="Social Engineering",
        name="Executive Voice Synthesis High-Value Wire Push",
        gen_ai=True,
        sophistication=9.6,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Simulates corporate executive voice authorization to authorize urgent off-cycle treasury transfers.",
        signals=["Off-Hours Commercial Wire", "Unregistered Beneficiary Jurisdictions", "Urgency Signal In Telemetry"],
        description="Coerces corporate finance staff into initiating real-time corporate payments via cloned voice instructions.",
        mitigation_policy="Implement dual-custody cryptographic approvals and out-of-band video biometric verification.",
    ),

    # Family 4: Transaction & Amount Manipulation (TXN)
    AttackVector(
        id="TXN-01",
        family="Transaction Manipulation",
        name="Sub-Threshold Micro-Amount Slicing (Salami)",
        gen_ai=False,
        sophistication=6.1,
        severity="MEDIUM",
        detectability="MEDIUM",
        evasion_strategy="Keeps transactions strictly sub-$5.00 to evade static volume and amount rules.",
        signals=["Sub-Threshold Count Spike", "Cross-Merchant Spread", "Micro-Velocity Accumulation"],
        description="Splits unauthorized balance extractions into high-volume micro-charges below standard review thresholds.",
        mitigation_policy="Aggregate cumulative velocity momentum across sliding 1h, 24h, and 7d temporal windows.",
    ),
    AttackVector(
        id="TXN-02",
        family="Transaction Manipulation",
        name="ISO 20022 Rich Field Contextual Tampering",
        gen_ai=False,
        sophistication=8.0,
        severity="HIGH",
        detectability="LOW",
        evasion_strategy="Alters settlement currency codes and processing indicator flags within rich payment payloads.",
        signals=["MCC Mismatch", "Settlement Currency Shift", "Processing Flag Inconsistency"],
        description="Manipulates downstream payment routing metadata fields while preserving valid outer payloads.",
        mitigation_policy="Validate strict cryptographic consistency across ISO 20022 message envelopes.",
    ),
    AttackVector(
        id="TXN-03",
        family="Transaction Manipulation",
        name="Incremental BIN Authorization Laddering",
        gen_ai=True,
        sophistication=7.5,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Uses binary search stepped amounts to determine maximum authorization headroom without decline.",
        signals=["Incremental Amount Step", "High Auth Velocity", "Zero-Amount Verification Precursor"],
        description="Systematically queries authorization limits via progressive stepped ticket sizes.",
        mitigation_policy="Flag rapid monotonic ticket escalations originating from uniform device sessions.",
    ),
    AttackVector(
        id="TXN-04",
        family="Transaction Manipulation",
        name="Pre-Authorization Settlement Hold Exploitation",
        gen_ai=False,
        sophistication=7.2,
        severity="MEDIUM",
        detectability="MEDIUM",
        evasion_strategy="Exploits 72-hour lag between pre-authorization hold and final batch clearing.",
        signals=["Hold vs Clear Delta High", "Hospitality/Automotive MCC Abuse", "Credit Line Exhaust Velocity"],
        description="Maximizes credit availability across overlapping pre-authorization hold windows before clearing.",
        mitigation_policy="Maintain real-time shadow balance ledger accounting for pending holds dynamically.",
    ),
    AttackVector(
        id="TXN-05",
        family="Transaction Manipulation",
        name="Refund Ledger Desynchronization Arbitrage",
        gen_ai=False,
        sophistication=7.6,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Exploits async merchant refund clearing cycles to trigger multiple credits against a single original auth.",
        signals=["Refund to Auth Ratio Spike", "Cross-Terminal Credit Velocity", "Settlement Window Skew"],
        description="Simulates rapid multi-terminal refund claims exploiting asynchronous merchant settlement batch processing.",
        mitigation_policy="Enforce real-time cryptographic settlement tracking tying credits to authentic original authorization reference.",
    ),

    # Family 5: Merchant & BIN Abuse (MER)
    AttackVector(
        id="MER-01",
        family="Merchant Abuse",
        name="Synthetic Collusive Merchant Laundering",
        gen_ai=True,
        sophistication=8.6,
        severity="HIGH",
        detectability="LOW",
        evasion_strategy="Routes transactions through synthetic storefronts with simulated legitimate foot-traffic metrics.",
        signals=["Merchant Chargeback Spike", "Uniform Basket Distribution", "New Merchant Velocity"],
        description="Establishes synthetic merchant accounts to clear stolen card portfolios via automated synthetic transactions.",
        mitigation_policy="Deploy graph-based merchant peer-group clustering and chargeback velocity monitoring.",
    ),
    AttackVector(
        id="MER-02",
        family="Merchant Abuse",
        name="E-Commerce Proxy Triangulation",
        gen_ai=False,
        sophistication=7.8,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Fulfills legitimate customer orders on discount platforms using stolen card credentials at retail merchants.",
        signals=["Shipping vs Billing Geo Delta", "Third-Party Email Domain Pattern", "First-Time Buyer Anomaly"],
        description="Scammer collects clean payment from genuine buyer and uses compromised card to fulfill supplier order.",
        mitigation_policy="Correlate billing-shipping physical distance with recipient history and email domain age.",
    ),
    AttackVector(
        id="MER-03",
        family="Merchant Abuse",
        name="Algorithmic BIN Range Permutation",
        gen_ai=True,
        sophistication=8.3,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Generates Luhn-valid card numbers systematically targeting specific issuer BIN blocks.",
        signals=["Sequential PAN Structure", "Expiration Sweep Pattern", "Issuer Decline Ratio Anomaly"],
        description="Algorithmic card number generation probing vulnerable issuer BIN ranges across e-commerce gates.",
        mitigation_policy="Trigger network-level BIN authorization rate-limits upon elevated invalid CVV/expiry ratios.",
    ),
    AttackVector(
        id="MER-04",
        family="Merchant Abuse",
        name="Dispute Window Friendly Fraud Simulation",
        gen_ai=False,
        sophistication=5.0,
        severity="LOW",
        detectability="HIGH",
        evasion_strategy="Legitimate cardholder initiates genuine purchase on trusted hardware, later filing false non-receipt dispute.",
        signals=["Post-Delivery Dispute Velocity", "Clean Hardware History", "Familiar Geolocation"],
        description="Simulates first-party intentional chargeback claims on verified delivered digital/physical goods.",
        mitigation_policy="Record comprehensive cryptographic delivery receipts and historical dispute frequency indices.",
    ),
    AttackVector(
        id="MER-05",
        family="Merchant Abuse",
        name="Sub-Affiliate Commission Arbitrage Network",
        gen_ai=True,
        sophistication=8.1,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Generates synthetic low-value purchases across affiliate referral links to harvest automated payout bonuses.",
        signals=["Affiliate Sub-ID Concentration", "Rapid Payout Trigger Velocity", "Zero Post-Purchase Activity"],
        description="Exploits e-commerce affiliate commission payouts via automated synthetic customer referrals.",
        mitigation_policy="Enforce 30-day affiliate commission holdback and chargeback clawback escrow provisions.",
    ),

    # Family 6: Identity & Synthetic Identity (SYN)
    AttackVector(
        id="SYN-01",
        family="Identity Abuse",
        name="Hybrid Synthetic Persona Assembly",
        gen_ai=True,
        sophistication=9.0,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Combines authentic national identifiers with synthetic addresses, employment profiles, and credit histories.",
        signals=["Thin Credit File History", "Address Discrepancy", "Synthetic Persona Age Velocity"],
        description="Constructs synthetic consumer profiles, nurturing trade lines over months prior to execution.",
        mitigation_policy="Cross-verify public identity registry depth, SSN issuance vintage, and address physical stability.",
    ),
    AttackVector(
        id="SYN-02",
        family="Identity Abuse",
        name="Coordinated Bust-Out Line Exhaust",
        gen_ai=False,
        sophistication=8.5,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Builds flawless repayment history to secure credit limit increases, then executes simultaneous max draws.",
        signals=["Sudden Max Utilization", "Cash Advance Liquidity Spike", "Multiple Simultaneous Inquiries"],
        description="Simultaneous full credit line draw across multiple financial institutions following limit expansion.",
        mitigation_policy="Monitor cross-institution real-time utilization velocities and sudden cash advance ratio spikes.",
    ),
    AttackVector(
        id="SYN-03",
        family="Identity Abuse",
        name="Synthetic ID Document & Biometric Onboarding Bypass",
        gen_ai=True,
        sophistication=9.6,
        severity="CRITICAL",
        detectability="VERY LOW",
        evasion_strategy="Generates synthetic identity documents and synchronized 3D liveness video feeds for onboarding.",
        signals=["KYC Biometric Liveness Anomaly", "EXIF Metadata Stripping", "Texture Spectrum Inconsistency"],
        description="Circumvents automated identity verification and facial liveness checks using generative 3D meshes.",
        mitigation_policy="Apply micro-frequency surface reflection analysis and hardware-backed secure enclave attestation.",
    ),
    AttackVector(
        id="SYN-04",
        family="Identity Abuse",
        name="Dormant Mule Account Fan-Out Layering",
        gen_ai=True,
        sophistication=8.2,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Disperses incoming stolen funds across 50+ dormant mule accounts in rapid micro-transfers.",
        signals=["Fan-Out Transfer Velocity", "Account Dormancy Re-activation", "Immediate Cash Outflow"],
        description="Automated money mule orchestration network rapidly fragmenting and layering payment flows.",
        mitigation_policy="Deploy network graph flow analytics identifying high fan-out/fan-in topology patterns.",
    ),

    # Family 7: Device & Network Spoofing (DEV)
    AttackVector(
        id="DEV-01",
        family="Device Spoofing",
        name="Browser Telemetry & WebGL Environment Hooking",
        gen_ai=False,
        sophistication=8.8,
        severity="CRITICAL",
        detectability="LOW",
        evasion_strategy="Overrides canvas, audio context, and hardware reporting APIs to mimic trusted iPhone configurations.",
        signals=["WebGL Renderer Inconsistency", "Canvas Hash Collision", "Battery API Telemetry Anomaly"],
        description="Falsifies client-side browser fingerprint telemetry to present as an authorized consumer device.",
        mitigation_policy="Validate hardware-bound cryptographic credentials and server-side TLS stack fingerprints.",
    ),
    AttackVector(
        id="DEV-02",
        family="Device Spoofing",
        name="Residential IoT Network Tunneling",
        gen_ai=False,
        sophistication=7.2,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Routes automated payment attempts through compromised residential broadband IoT nodes.",
        signals=["ASN Reputation Shift", "TCP/IP vs HTTP Header Mismatch", "Subnet Device Diversity"],
        description="Masks automated fraud origins by tunneling traffic through residential consumer IP subnets.",
        mitigation_policy="Analyze TCP/IP stack latency anomalies and passive OS fingerprint discrepancies.",
    ),
    AttackVector(
        id="DEV-03",
        family="Device Spoofing",
        name="Virtual Emulator Farm Automation",
        gen_ai=True,
        sophistication=8.0,
        severity="HIGH",
        detectability="MEDIUM",
        evasion_strategy="Systematically cycles virtual hardware identifiers, build properties, and telephony signatures.",
        signals=["Debug Interface Telemetry", "Hardware Sensor Immobility", "OS Build Inconsistency"],
        description="Runs hundreds of containerized Android banking apps on cloud instances with randomized device properties.",
        mitigation_policy="Require hardware keystore attestation (Play Integrity / DeviceCheck API assertions).",
    ),
    AttackVector(
        id="DEV-04",
        family="Device Spoofing",
        name="Simulated Geolocation & Mock GPS Injection",
        gen_ai=False,
        sophistication=6.5,
        severity="MEDIUM",
        detectability="HIGH",
        evasion_strategy="Injects mock GPS coordinates matching merchant terminal physical checkout geofences.",
        signals=["Mock Provider Flag Active", "Impossible Transit Velocity", "Cell Tower vs GPS Inconsistency"],
        description="Injects false GPS telemetry to simulate in-store physical proximity for mobile payments.",
        mitigation_policy="Verify cellular tower tri-angulation and Wi-Fi BSSID environmental beacon consistency.",
    ),

    # Family 8: Unseen AI-Adaptive Fraud (ADV - Strictly Reserved Holdout)
    AttackVector(
        id="ADV-01",
        family="AI Adaptive Fraud",
        name="Model Inversion Gradient Perturbation Probing",
        gen_ai=True,
        sophistication=9.8,
        severity="CRITICAL",
        detectability="VERY LOW",
        evasion_strategy="Calculates minimal adversarial feature perturbations along decision boundaries to flip Block decisions to Allow.",
        signals=["Boundary Perturbation Profile", "Subtle Multimodal Noise", "Cross-Feature Correlation Shift"],
        description="Probes blackbox scoring boundaries using gradient approximation to discover model blind spots.",
        mitigation_policy="Incorporate adversarial regularization, robust loss functions, and randomized ensemble gating.",
    ),
    AttackVector(
        id="ADV-02",
        family="AI Adaptive Fraud",
        name="Holistic Multimodal Identity Synthesis Swarm",
        gen_ai=True,
        sophistication=9.9,
        severity="CRITICAL",
        detectability="VERY LOW",
        evasion_strategy="Simultaneously synthesizes voice, behavioral cadence, device environment, and transactional context.",
        signals=["Cross-Modal Micro-Deltas", "High Latency Computation Anomaly", "Ultra-Smooth Telemetry Spectrum"],
        description="Next-generation multi-agent framework orchestrating holistic fraud vectors across all communication channels.",
        mitigation_policy="Deploy continuous multidimensional zero-trust behavioral verification and out-of-band challenge protocols.",
    ),
    AttackVector(
        id="ADV-03",
        family="AI Adaptive Fraud",
        name="Constrained Feature-Space Boundary Wanderer",
        gen_ai=True,
        sophistication=9.7,
        severity="CRITICAL",
        detectability="VERY LOW",
        evasion_strategy="Walks the non-convex decision boundary using zeroth-order optimization without triggering rate alarms.",
        signals=["Sub-Threshold Parameter Walk", "Micro-Variance Coupling", "Boundary Exploration Pattern"],
        description="Black-box adversarial optimization algorithm mapping detector decision manifolds under query budget constraints.",
        mitigation_policy="Employ dynamic randomized decision thresholds and adversarial perturbation defense layers.",
    ),
]


class AttackTaxonomy:
    """Provides structured access, filtering, and graph topology for the 36 attack vectors."""

    def __init__(self):
        self._attacks: Dict[str, AttackVector] = {a.id: a for a in ATTACK_TAXONOMY_RAW}

    def get_all(self) -> List[AttackVector]:
        return list(self._attacks.values())

    def get_all_dicts(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self._attacks.values()]

    def get_by_id(self, attack_id: str) -> Optional[AttackVector]:
        return self._attacks.get(attack_id)

    def get_by_family(self, family: str) -> List[AttackVector]:
        if family == "ALL" or not family:
            return self.get_all()
        return [a for a in self._attacks.values() if a.family.lower() == family.lower()]

    def get_families(self) -> List[str]:
        return sorted(list({a.family for a in self._attacks.values()}))

    def get_training_attacks(self) -> List[AttackVector]:
        """Returns all attack vectors except the reserved holdout family (ADV)."""
        return [a for a in self._attacks.values() if a.family != "AI Adaptive Fraud"]

    def get_holdout_attacks(self) -> List[AttackVector]:
        """Returns the strictly reserved unseen holdout family (ADV-01, ADV-02)."""
        return [a for a in self._attacks.values() if a.family == "AI Adaptive Fraud"]

    def get_knowledge_graph(self) -> Dict[str, Any]:
        """Generates structured nodes and edges for the interactive Threat Knowledge Graph."""
        nodes = []
        edges = []

        family_colors = {
            "Account Takeover": "#ef4444",
            "Behavioral Impersonation": "#f97316",
            "Social Engineering": "#eab308",
            "Transaction Manipulation": "#ec4899",
            "Merchant Abuse": "#8b5cf6",
            "Identity Abuse": "#a855f7",
            "Device Spoofing": "#06b6d4",
            "AI Adaptive Fraud": "#f43f5e",
        }

        # 1. Family Nodes
        for fam in self.get_families():
            node_id = f"f_{fam.lower().replace(' ', '_')}"
            nodes.append({
                "id": node_id,
                "label": fam,
                "type": "family",
                "color": family_colors.get(fam, "#94a3b8")
            })

        # 2. Key Attack Nodes (Representative vectors for clean visualization)
        rep_attacks = ["ATO-01", "ATO-03", "BIO-01", "SOC-01", "TXN-01", "MER-01", "SYN-01", "DEV-01", "ADV-01"]
        for att_id in rep_attacks:
            att = self.get_by_id(att_id)
            if att:
                nodes.append({
                    "id": f"a_{att.id}",
                    "label": f"{att.id}: {att.name[:24]}...",
                    "type": "attack",
                    "color": "#f87171"
                })
                # Edge from family to attack
                fam_id = f"f_{att.family.lower().replace(' ', '_')}"
                edges.append({
                    "source": fam_id,
                    "target": f"a_{att.id}",
                    "relation": "contains"
                })

        # 3. Behavioral Signals
        signals_map = {
            "s_velocity": "Velocity Surge (1h)",
            "s_biometric": "Touch/Cadence Jitter",
            "s_device_fam": "Device Familiarity < 0.2",
            "s_carrier": "Carrier Change Flag",
            "s_geo": "Geo Deviation > 500km",
            "s_micro_salami": "Sub-$5 Micro Amount Slicing"
        }
        for s_id, s_label in signals_map.items():
            nodes.append({
                "id": s_id,
                "label": s_label,
                "type": "signal",
                "color": "#3b82f6"
            })

        # Edges from attacks to signals
        edges.extend([
            {"source": "a_ATO-01", "target": "s_device_fam", "relation": "triggers"},
            {"source": "a_ATO-01", "target": "s_velocity", "relation": "triggers"},
            {"source": "a_ATO-03", "target": "s_carrier", "relation": "triggers"},
            {"source": "a_BIO-01", "target": "s_biometric", "relation": "triggers"},
            {"source": "a_SOC-01", "target": "s_velocity", "relation": "triggers"},
            {"source": "a_TXN-01", "target": "s_micro_salami", "relation": "triggers"},
            {"source": "a_DEV-01", "target": "s_geo", "relation": "triggers"},
            {"source": "a_ADV-01", "target": "s_biometric", "relation": "triggers"},
        ])

        # 4. Defense Models
        defense_models = [
            {"id": "d_baseline_rule", "label": "Static Rule Baseline", "color": "#64748b"},
            {"id": "d_xgb_v1", "label": "XGBoost Classifier v1.0", "color": "#10b981"},
            {"id": "d_aegis_v3", "label": "AegisPay Hybrid v3.0 (Hardened)", "color": "#06b6d4"},
        ]
        nodes.extend(defense_models)

        # Edges from signals/attacks to defenses
        edges.extend([
            {"source": "a_TXN-01", "target": "d_baseline_rule", "relation": "evades"},
            {"source": "a_BIO-01", "target": "d_xgb_v1", "relation": "evades"},
            {"source": "a_BIO-01", "target": "d_aegis_v3", "relation": "detected_by"},
            {"source": "a_ADV-01", "target": "d_xgb_v1", "relation": "evades"},
            {"source": "a_ADV-01", "target": "d_aegis_v3", "relation": "detected_by"},
            {"source": "s_velocity", "target": "d_xgb_v1", "relation": "inputs_to"},
            {"source": "s_biometric", "target": "d_aegis_v3", "relation": "inputs_to"},
        ])

        return {"nodes": nodes, "edges": edges}

    def export_json(self, output_path: str):
        """Exports taxonomy to JSON file for machine-readable use."""
        data = {
            "version": "2026.1",
            "total_vectors": len(self._attacks),
            "families_count": len(self.get_families()),
            "attacks": self.get_all_dicts(),
            "knowledge_graph": self.get_knowledge_graph()
        }
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


taxonomy_instance = AttackTaxonomy()
