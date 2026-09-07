"""
AegisPay v2 - Attack Primitives Catalog
Contains the 36 seed attack vectors across 8 threat families mapped into 7-slot typed primitives.
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class AttackPrimitive:
    primitive_id: str
    family: str
    name: str
    default_access: str
    default_trust: str
    default_rail: str
    default_evasion: str
    default_behavior: str
    default_monetization: str
    default_temporal: str
    observable_signals: List[str]
    mitigation_policy: str
    description: str


# Catalog of all 36 seed attack primitives
ATTACK_PRIMITIVES: Dict[str, AttackPrimitive] = {
    # 1. Account Takeover (ATO)
    "ATO-01": AttackPrimitive(
        primitive_id="ATO-01",
        family="Account Takeover",
        name="Credential Stuffing with Micro-Delays",
        default_access="Credential Stuffing",
        default_trust="Residential Proxy",
        default_rail="UPI",
        default_evasion="Temporal Pacing",
        default_behavior="Synthetic Cadence",
        default_monetization="P2P Transfer",
        default_temporal="Micro-Pacing",
        observable_signals=["burst_login_attempts", "unrecognized_device_fp", "ip_subnet_dispersion"],
        mitigation_policy="Enforce Step-Up WebAuthn & Progressive Rate Limiting",
        description="Automated login probing using breached credential pairs with randomized micro-delays to evade rate limiters."
    ),
    "ATO-02": AttackPrimitive(
        primitive_id="ATO-02",
        family="Account Takeover",
        name="Session Token Hijacking & Replay",
        default_access="Session Hijacking",
        default_trust="Cookie Replay",
        default_rail="Card",
        default_evasion="Header Mimicry",
        default_behavior="Burst Rapid Action",
        default_monetization="Immediate Checkout",
        default_temporal="Instantaneous Burst",
        observable_signals=["ip_change_mid_session", "tls_fingerprint_mismatch", "missing_handshake"],
        mitigation_policy="Bind Session to Hardware Enclave Token & Silent Block",
        description="Extracts and replays active authorization session bearer tokens from untrusted network endpoints."
    ),
    "ATO-03": AttackPrimitive(
        primitive_id="ATO-03",
        family="Account Takeover",
        name="Cellular SIM Swap & OTP Re-route",
        default_access="SIM Swap",
        default_trust="Carrier Spoof",
        default_rail="UPI",
        default_evasion="Carrier Porting Pacing",
        default_behavior="New Device First Login",
        default_monetization="Immediate P2P Drain",
        default_temporal="Post-Midnight Quiet Window",
        observable_signals=["carrier_imsi_change", "device_id_delta", "velocity_surge_post_login"],
        mitigation_policy="Mandate 24-Hour Cooling-Off Window on Device/SIM Change",
        description="Fraudulent porting of cardholder mobile IMSI to intercept SMS OTP authentication flows."
    ),
    "ATO-04": AttackPrimitive(
        primitive_id="ATO-04",
        family="Account Takeover",
        name="Password Reset Cascade with OAuth Intercept",
        default_access="Social Engineering Phishing",
        default_trust="Compromised SSO",
        default_rail="A2A",
        default_evasion="OAuth Scope Abuse",
        default_behavior="Security Profile Modification",
        default_monetization="Beneficiary Addition",
        default_temporal="Low Velocity Probe",
        observable_signals=["email_forwarding_rule", "recovery_factor_updated", "immediate_fund_out"],
        mitigation_policy="Step-Up 3DS & Risk-Weighted Recovery Hold",
        description="Manipulates identity provider recovery flows to hijack access delegation tokens across integrated accounts."
    ),
    "ATO-05": AttackPrimitive(
        primitive_id="ATO-05",
        family="Account Takeover",
        name="Passkey Downgrade to SMS Fallback",
        default_access="Malware Protocol Downgrade",
        default_trust="Client Feature Stripping",
        default_rail="Card",
        default_evasion="Fallback Downgrade",
        default_behavior="Failing Hardware Auth",
        default_monetization="Card Not Present Checkout",
        default_temporal="Sequential Retries",
        observable_signals=["passkey_assertion_suppressed", "legacy_sms_fallback_invoked", "browser_capability_strip"],
        mitigation_policy="Deny SMS Fallback for High-Value Transactions",
        description="Deliberately alters client authentication payload headers to force authentication servers to fall back to vulnerable SMS OTP."
    ),

    # 2. Behavioral Impersonation (BIO)
    "BIO-01": AttackPrimitive(
        primitive_id="BIO-01",
        family="Behavioral Impersonation",
        name="GAN Keystroke Dynamics Synthesis",
        default_access="Credential Stuffing",
        default_trust="Biometric Mimicry",
        default_rail="Card",
        default_evasion="Synthetic Keystroke Cadence",
        default_behavior="Learned Timing Jitter",
        default_monetization="Digital Goods Purchase",
        default_temporal="Realistic Typing Intervals",
        observable_signals=["inter_key_flight_time_synthetic", "zero_touch_micro_jitter", "unnatural_dwell_smoothness"],
        mitigation_policy="Hardware Enclave Sensor Integrity Verification",
        description="Deep generative neural network models mimic victim keystroke dwell and flight timings during payment entry."
    ),
    "BIO-02": AttackPrimitive(
        primitive_id="BIO-02",
        family="Behavioral Impersonation",
        name="Automated Checkout Script Replay",
        default_access="Automated Botnet",
        default_trust="Browser Environment Hook",
        default_rail="Card",
        default_evasion="Deterministic Trajectory",
        default_behavior="Zero Hesitation Navigation",
        default_monetization="High Velocity Merchant Cart",
        default_temporal="Sub-Second Form Fill",
        observable_signals=["navigation_timing_sub_100ms", "linear_mouse_interpolation", "focus_blur_missing"],
        mitigation_policy="Deploy Proof-of-Work Challenge & Step-Up 3DS",
        description="Headless browser runners executing recorded checkout trajectories without human cognitive delays."
    ),
    "BIO-03": AttackPrimitive(
        primitive_id="BIO-03",
        family="Behavioral Impersonation",
        name="Circadian Rhythm Mimicry",
        default_access="Credential Stuffing",
        default_trust="Geofence Match",
        default_rail="UPI",
        default_evasion="Temporal Timing Alignment",
        default_behavior="Baseline Hour Mimicry",
        default_monetization="Scheduled Bill Pay Abuse",
        default_temporal="Cardholder Active Window",
        observable_signals=["time_of_day_perfect_match", "device_fingerprint_drift", "amount_profile_anomaly"],
        mitigation_policy="Multi-Signal Risk Correlation & Velocity Gating",
        description="Schedules automated fraudulent transfers strictly during the cardholder's historical active daytime window."
    ),
    "BIO-04": AttackPrimitive(
        primitive_id="BIO-04",
        family="Behavioral Impersonation",
        name="Synthetic Scroll & Touch Velocity",
        default_access="Malware Agent",
        default_trust="Emulated Touch Screen",
        default_rail="Wallet",
        default_evasion="Bezier Curve Touch Emulation",
        default_behavior="Curved Drag Events",
        default_monetization="Wallet Top-Up",
        default_temporal="Uniform Inter-Touch Spacing",
        observable_signals=["touch_radius_invariant", "scroll_acceleration_exact_zero", "pointer_events_synthetic_flag"],
        mitigation_policy="Capacitive Sensor Telemetry Verification",
        description="Generates synthetic touchscreen touch curves to evade heuristic bot-detection libraries."
    ),
    "BIO-05": AttackPrimitive(
        primitive_id="BIO-05",
        family="Behavioral Impersonation",
        name="Cognitive Hesitation Injection",
        default_access="Phishing",
        default_trust="Residential Proxy",
        default_rail="UPI",
        default_evasion="Artificial Hesitation Jitter",
        default_behavior="Humanized Thinking Pauses",
        default_monetization="Split P2P Transfer",
        default_temporal="Gaussian Pauses Between Inputs",
        observable_signals=["pause_duration_exact_gaussian", "mouse_idle_at_submit_button", "cursor_wander_pattern"],
        mitigation_policy="Adaptive Anomaly Detection & Graph Fan-Out Gating",
        description="Injects statistically calculated cognitive hesitation pauses to mimic human decision-making."
    ),

    # 3. Social Engineering & Authorized Push Payment (APP)
    "SOC-01": AttackPrimitive(
        primitive_id="SOC-01",
        family="Social Engineering & APP",
        name="Manipulated Authorized Push Payment",
        default_access="Voice Call Deception",
        default_trust="Legitimate User Device",
        default_rail="UPI",
        default_evasion="Legitimate User Biometrics",
        default_behavior="High Urgency Out-of-Pattern Transfer",
        default_monetization="Immediate Mule Account Credit",
        default_temporal="Call Concurrent Session",
        observable_signals=["concurrent_active_telephony_call", "new_beneficiary_high_amount", "speed_to_auth_abnormal"],
        mitigation_policy="Mandatory Cooling-Off Hold & Confirmation Challenge",
        description="Victim is actively coerced over a fraudulent phone call into completing a high-value real-time transfer."
    ),
    "SOC-02": AttackPrimitive(
        primitive_id="SOC-02",
        family="Social Engineering & APP",
        name="Recurring Mandate Phishing Injection",
        default_access="Malicious QR Code",
        default_trust="Legitimate Mobile App",
        default_rail="Recurring Mandate",
        default_evasion="Deceptive Mandate Description",
        default_behavior="Subscription Registration",
        default_monetization="Future Automated Pulls",
        default_temporal="Delayed Recurring Schedule",
        observable_signals=["mandate_amount_at_max_limit", "unregistered_payee_vpa", "first_execution_immediate"],
        mitigation_policy="Mandate Limit Throttling & Independent Review",
        description="Induces user into approving an auto-debit mandate disguised as a one-time refund or lottery credit."
    ),
    "SOC-03": AttackPrimitive(
        primitive_id="SOC-03",
        family="Social Engineering & APP",
        name="Remote Desktop Assistance Hijack",
        default_access="Screen Sharing Malware",
        default_trust="Legitimate Session",
        default_rail="A2A",
        default_evasion="Remote Cursor Injection",
        default_behavior="Concurrent Accessibility Service",
        default_monetization="Multiple Rapid Beneficiary Payouts",
        default_temporal="Extended Inactive Baseline Then Burst",
        observable_signals=["accessibility_api_active", "remote_screen_capture_running", "mouse_events_injected"],
        mitigation_policy="Auto-Terminate Session on Remote Admin Tool Detection",
        description="Attacker uses remote administration software (AnyDesk, TeamViewer) to guide victim and manipulate transfer destinations."
    ),
    "SOC-04": AttackPrimitive(
        primitive_id="SOC-04",
        family="Social Engineering & APP",
        name="Multi-Agent AI Phishing Swarm",
        default_access="Contextual SMS/Email Chatbot",
        default_trust="Lookalike Merchant Web",
        default_rail="Card",
        default_evasion="Dynamic LLM Personalization",
        default_behavior="Real-Time Dynamic Dialogue",
        default_monetization="Merchant Token Harvesting",
        default_temporal="Rapid Responsive Exchange",
        observable_signals=["domain_age_under_24h", "ssl_issuer_free_tier", "inbound_referer_phishing_vector"],
        mitigation_policy="Real-Time Domain Risk Scoring & Immediate Block",
        description="Autonomous LLM agents hold tailored context-aware conversations with cardholders to harvest one-time credentials."
    ),
    "SOC-05": AttackPrimitive(
        primitive_id="SOC-05",
        family="Social Engineering & APP",
        name="Deepfake Executive Voice Authorization",
        default_access="Voice Clone Telephony",
        default_trust="Internal Employee Trust",
        default_rail="A2A",
        default_evasion="Acoustic Voice Print Match",
        default_behavior="High Value Corporate Wire",
        default_monetization="Overseas Beneficiary Escrow",
        default_temporal="End-of-Quarter Financial Close",
        observable_signals=["voice_synthetic_watermark_absent", "wire_destination_jurisdiction_high_risk", "override_flag_set"],
        mitigation_policy="Dual-Custody Out-of-Band Physical Key Authorization",
        description="Generative audio synthesis clones executive voice to authorize emergency high-value corporate treasury transfers."
    ),

    # 4. Transaction Manipulation (TXN)
    "TXN-01": AttackPrimitive(
        primitive_id="TXN-01",
        family="Transaction Manipulation",
        name="Sub-Threshold Salami Slicing",
        default_access="Compromised Merchant Key",
        default_trust="Automated Billing Agreement",
        default_rail="Card",
        default_evasion="Micro Amount Below Alert Trigger",
        default_behavior="High Cardinality Low Ticket",
        default_monetization="Dispersed Aggregate Extraction",
        default_temporal="Periodic Staggered Execution",
        observable_signals=["ticket_amount_under_threshold", "card_fanout_across_bins", "chargeback_ratio_creeping"],
        mitigation_policy="Aggregate Velocity Matrix & BIN Concentration Filter",
        description="Issues thousands of sub-$2 transaction requests across card portfolios staying below per-transaction alert floors."
    ),
    "TXN-02": AttackPrimitive(
        primitive_id="TXN-02",
        family="Transaction Manipulation",
        name="ISO 20022 Rich Message Field Tampering",
        default_access="Man-in-the-Middle Network Proxy",
        default_trust="Interbank Gateway Session",
        default_rail="A2A",
        default_evasion="Header Preserved Payload Modified",
        default_behavior="Beneficiary Routing Alteration",
        default_monetization="Intermediary Mule Redirection",
        default_temporal="In-Flight Packet Interception",
        observable_signals=["xml_digital_signature_invalid", "pac_008_routing_delta", "message_digest_mismatch"],
        mitigation_policy="Strict End-to-End Payload Cryptographic Verification",
        description="Alters XML routing headers (CreditorAccount / ClearingSystemMember) in transit within ISO 20022 payment packages."
    ),
    "TXN-03": AttackPrimitive(
        primitive_id="TXN-03",
        family="Transaction Manipulation",
        name="Incremental BIN Laddering Probes",
        default_access="Card Testing Botnet",
        default_trust="Direct Merchant API",
        default_rail="Card",
        default_evasion="Algorithmic Expiry/CVV Step",
        default_behavior="Rapid Sequential Micro Authorizations",
        default_monetization="Card Validity Verification",
        default_temporal="Millisecond Cadence",
        observable_signals=["sequential_pan_probe", "cvv_failure_retry_cascade", "merchant_checkout_dwell_zero"],
        mitigation_policy="Automated IP/Merchant BIN Flood Suppression",
        description="Automated card testing iterating expiry date and CVV combinations against high-speed checkout endpoints."
    ),
    "TXN-04": AttackPrimitive(
        primitive_id="TXN-04",
        family="Transaction Manipulation",
        name="Pre-Authorization Hold Arbitrage",
        default_access="Stolen Card Credentials",
        default_trust="Automated Fuel / Hospitality Merchant",
        default_rail="Card",
        default_evasion="Exploit Settlement Latency Window",
        default_behavior="Multiple Concurrent Pre-Auths",
        default_monetization="Instant Asset Extraction",
        default_temporal="Simultaneous Geographic Locations",
        observable_signals=["available_balance_overdraw", "concurrent_auth_different_geos", "delayed_settlement_spike"],
        mitigation_policy="Real-Time Shadow Ledger & Global Velocity Lock",
        description="Simultaneously places pre-authorization holds across merchant categories before clearing settles against available limit."
    ),
    "TXN-05": AttackPrimitive(
        primitive_id="TXN-05",
        family="Transaction Manipulation",
        name="Refund Ledger Desynchronization",
        default_access="Corrupted Point-of-Sale Terminal",
        default_trust="Merchant Refund Privilege",
        default_rail="Card",
        default_evasion="Orphan Refund Request",
        default_behavior="Refund Without Prior Charge",
        default_monetization="Direct Credit to Attacker Card",
        default_temporal="End-of-Day Settlement Batch",
        observable_signals=["refund_unmatched_to_original_arn", "refund_card_mismatch", "offline_settlement_batch_override"],
        mitigation_policy="Mandate ARN Token Matching for All Credit Returns",
        description="Injects standalone refund instructions lacking a corresponding original authorization Reference Number."
    ),

    # 5. Merchant & Collusive Abuse (MER)
    "MER-01": AttackPrimitive(
        primitive_id="MER-01",
        family="Merchant & Collusive Abuse",
        name="Collusive Merchant Credit Laundering",
        default_access="Compromised Merchant Account",
        default_trust="Established Terminal ID",
        default_rail="Card",
        default_evasion="Inflated Low-Velocity Legitimate Purchases",
        default_behavior="Structured Off-Peak Settlements",
        default_monetization="Merchant Payout Splitting",
        default_temporal="Late Night Batch Processing",
        observable_signals=["chargeback_rate_exceeding_threshold", "card_reuse_across_restricted_pool", "median_ticket_exact_clustering"],
        mitigation_policy="Collusion Graph Analysis & Immediate Payout Freeze",
        description="Merchant entity colludes with carding operators to process fraudulent charges and split payout before chargebacks arrive."
    ),
    "MER-02": AttackPrimitive(
        primitive_id="MER-02",
        family="Merchant & Collusive Abuse",
        name="Proxy Triangulation E-Commerce Laundering",
        default_access="Stolen Card Portfolio",
        default_trust="Legitimate Retail Platform",
        default_rail="Card",
        default_evasion="Victim Real Address Shipping",
        default_behavior="Third-Party Consumer Fulfillment",
        default_monetization="Marketplace Cash Collection",
        default_temporal="Order Concurrent Timing",
        observable_signals=["billing_shipping_geo_divergence", "buyer_account_created_under_1h", "disposable_email_domain"],
        mitigation_policy="Cross-Check Buyer Payment Fingerprint Against Seller Graph",
        description="Attacker sells goods at discount on marketplace, purchases them on legitimate site using stolen cards, shipping to buyer."
    ),
    "MER-03": AttackPrimitive(
        primitive_id="MER-03",
        family="Merchant & Collusive Abuse",
        name="Algorithmic Luhn PAN Permutation Flood",
        default_access="Distributed Proxy Network",
        default_trust="Public Checkout Endpoint",
        default_rail="Card",
        default_evasion="Luhn-Compliant Synthetic Range",
        default_behavior="High Velocity Testing",
        default_monetization="Valid Account Identification",
        default_temporal="Constant Distributed Rate",
        observable_signals=["consecutive_pan_distance_minimal", "declined_issuer_code_surge", "http_user_agent_homogeneity"],
        mitigation_policy="Rate-Limit BIN Routing & Challenge IP Cluster",
        description="Generates synthetically valid card numbers using Luhn checksum algorithms to discover live issuing ranges."
    ),
    "MER-04": AttackPrimitive(
        primitive_id="MER-04",
        family="Merchant & Collusive Abuse",
        name="Friendly Chargeback First-Party Abuse",
        default_access="Legitimate Cardholder Credentials",
        default_trust="Legitimate Device & IP",
        default_rail="Card",
        default_evasion="Legitimate Baseline Mimicry",
        default_behavior="Normal Checkout followed by Claim",
        default_monetization="Item Retained + Chargeback Credit",
        default_temporal="Dispute Lodged 30 Days Post-Tx",
        observable_signals=["delivery_confirmed_gps_match", "dispute_frequency_high_ratio", "social_media_location_verification"],
        mitigation_policy="Proof-of-Delivery Cryptographic Binding & Scoring",
        description="Cardholder completes authentic purchase, receives physical goods, and fraudulently files 'unauthorized transaction' claim."
    ),
    "MER-05": AttackPrimitive(
        primitive_id="MER-05",
        family="Merchant & Collusive Abuse",
        name="Affiliate Commission Micro-Arbitrage",
        default_access="Affiliate Tracking Cookie Stuffing",
        default_trust="Affiliate Network Key",
        default_rail="Card",
        default_evasion="Purchases Cancelled Post Commission Settlement",
        default_behavior="High Volume Referrals",
        default_monetization="Affiliate Network Commission",
        default_temporal="Synchronized with Commission Lock Windows",
        observable_signals=["return_rate_near_100_percent", "referrer_traffic_zero_dwell", "cookie_stuffing_headers_detected"],
        mitigation_policy="Delay Affiliate Payouts Pending Final Charge Settlement",
        description="Generates high volume of card purchases to collect instant affiliate commissions, then triggers charge reversals."
    ),

    # 6. Identity & Synthetic Fraud (SYN)
    "SYN-01": AttackPrimitive(
        primitive_id="SYN-01",
        family="Identity & Synthetic Fraud",
        name="Frankenstein Synthetic Identity Creation",
        default_access="Stolen SSN/Tax ID + Real Address",
        default_trust="Fabricated Credit Bureau History",
        default_rail="A2A",
        default_evasion="Dormant Account Seasoning",
        default_behavior="Gradual Balance Building",
        default_monetization="Full Credit Line Drawdown",
        default_temporal="Months-Long Maturation",
        observable_signals=["ssn_issuance_date_incompatible_with_dob", "address_shared_with_multiple_synthetic_profiles", "credit_file_depth_shallow"],
        mitigation_policy="Government Registry Identity Verification Gate",
        description="Combines legitimate tax IDs with fabricated names and addresses, cultivating clean credit profiles over months."
    ),
    "SYN-02": AttackPrimitive(
        primitive_id="SYN-02",
        family="Identity & Synthetic Fraud",
        name="Credit File Seasoning & Bust-Out",
        default_access="Synthetic Identity Credential",
        default_trust="Clean Payment History",
        default_rail="Card",
        default_evasion="Perfect Repayment Behavior Before Raid",
        default_behavior="Sudden 100% Utilization",
        default_monetization="Immediate Multi-Channel Cash Advances",
        default_temporal="Coordinated 48-Hour Bust-Out",
        observable_signals=["credit_limit_increase_requested_recently", "sudden_velocity_jump_10x", "cash_equivalent_merchant_spend"],
        mitigation_policy="Dynamic Exposure Caps & Real-Time Velocity Throttling",
        description="Maintains flawless small-ticket payment history for 12 months, requests credit increases, then instantly maxes out all limits."
    ),
    "SYN-03": AttackPrimitive(
        primitive_id="SYN-03",
        family="Identity & Synthetic Fraud",
        name="3D Biometric Mesh Onboarding Injection",
        default_access="Synthetic Face GAN Generation",
        default_trust="Virtual Camera Driver",
        default_rail="UPI",
        default_evasion="Synthesized Liveness Verification Response",
        default_behavior="Virtual Video Stream Injection",
        default_monetization="Account Unlocking for Mule Operation",
        default_temporal="Single-Attempt Instant Onboarding",
        observable_signals=["virtual_webcam_driver_detected", "depth_map_inconsistency", "micro_texture_repetition_artifacts"],
        mitigation_policy="Hardware-Attested TrueDepth Sensor Assertion",
        description="Feeds photorealistic 3D facial avatar streams directly into KYC video verification APIs to bypass human liveness checks."
    ),
    "SYN-04": AttackPrimitive(
        primitive_id="SYN-04",
        family="Identity & Synthetic Fraud",
        name="Dormant Mule Account Layering Cascade",
        default_access="Purchased Student/Dormant Account",
        default_trust="Established Account Vintage",
        default_rail="A2A",
        default_evasion="Rapid In-and-Out Smurfing",
        default_behavior="Sudden Reactivation After Dormancy",
        default_monetization="Layered Crypto/P2P Dispersal",
        default_temporal="Hop Transfers Within 60 Seconds",
        observable_signals=["dormant_account_rapid_in_and_out", "fan_in_fan_out_graph_structure", "zero_residual_balance"],
        mitigation_policy="Flag Reactivated Accounts with Real-Time Outbound Freeze",
        description="Reactivates dormant legitimate accounts to receive stolen funds and immediately disperse them across micro-layers."
    ),

    # 7. Device & Network Spoofing (DEV)
    "DEV-01": AttackPrimitive(
        primitive_id="DEV-01",
        family="Device & Network Spoofing",
        name="Browser Canvas & WebGL Environment Hooking",
        default_access="Puppeteer Automated Framework",
        default_trust="Forged Browser Fingerprint",
        default_rail="Card",
        default_evasion="Faked Hardware Telemetry",
        default_behavior="Scripted DOM Interactions",
        default_monetization="E-Commerce Checkout",
        default_temporal="Scheduled Script Execution",
        observable_signals=["navigator_webdriver_flag_true", "webgl_vendor_renderer_override", "canvas_hash_collision"],
        mitigation_policy="Execute Client-Side Cryptographic Runtime Integrity Check",
        description="Overrides JavaScript `HTMLCanvasElement` and `WebGLRenderingContext` prototypes to forge victim device fingerprints."
    ),
    "DEV-02": AttackPrimitive(
        primitive_id="DEV-02",
        family="Device & Network Spoofing",
        name="Residential IoT Proxy Routing",
        default_access="Compromised Smart Home Botnet",
        default_trust="Local Residential ISP IP",
        default_rail="UPI",
        default_evasion="Local Subnet IP Geo Match",
        default_behavior="Attacker Remote Commands",
        default_monetization="P2P Wallet Drain",
        default_temporal="Distributed Inter-Request Intervals",
        observable_signals=["tcp_ip_os_fingerprint_mismatch", "high_latency_jitter_vs_asn", "tor_exit_or_vpn_intermediate_hop"],
        mitigation_policy="Deep Packet TLS Client Hello Fingerprint Verification",
        description="Routes malicious payment traffic through hijacked residential smart appliances located in the victim's immediate city."
    ),
    "DEV-03": AttackPrimitive(
        primitive_id="DEV-03",
        family="Device & Network Spoofing",
        name="Android Containerized Emulator Farm",
        default_access="Rooted Virtual Machine Cluster",
        default_trust="Generated IMEI/Android ID",
        default_rail="UPI",
        default_evasion="Fake Hardware Telemetry",
        default_behavior="Automated UI Automation Framework",
        default_monetization="New User Bonus & P2P Drain",
        default_temporal="Concurrent Mass Execution",
        observable_signals=["build_hardware_goldfish_qemu", "battery_charging_state_invariant", "sensor_gyroscope_static_zero"],
        mitigation_policy="Google Play Protect Integrity API Verification",
        description="Spins up hundreds of cloud Android instances with synthetic hardware identifiers to execute automated payment flows."
    ),
    "DEV-04": AttackPrimitive(
        primitive_id="DEV-04",
        family="Device & Network Spoofing",
        name="Mock GPS Location Injection",
        default_access="Mock Location Provider Service",
        default_trust="Spoofed Geo Coordinates",
        default_rail="UPI",
        default_evasion="Fake Proximity to Merchant POS",
        default_behavior="Static Coordinate Broadcast",
        default_monetization="Proximity-Based Payment Authorization",
        default_temporal="Instantaneous Teleportation Across Cities",
        observable_signals=["is_from_mock_provider_true", "altitude_and_accuracy_invariant", "haversine_speed_exceeds_mach_1"],
        mitigation_policy="Correlate GPS with Cellular Cell Tower IDs & BSSID",
        description="Injects artificial GPS coordinates into mobile payment apps to fake physical presence near a payment merchant terminal."
    ),

    # 8. AI Adaptive Fraud (ADV - Sealed Holdout Tier)
    "ADV-01": AttackPrimitive(
        primitive_id="ADV-01",
        family="AI Adaptive Fraud",
        name="Whitebox Decision Boundary Gradient Probing",
        default_access="Adversarial ML Model Probe",
        default_trust="Multi-Account Probing",
        default_rail="UPI",
        default_evasion="Perturbation Directed at Decision Surface",
        default_behavior="Boundary Wandering",
        default_monetization="High Value Transfer Just Below Threshold",
        default_temporal="Iterative Feedback-Guided Probes",
        observable_signals=["score_clustering_near_decision_boundary", "feature_delta_orthogonal_to_gradients", "low_entropy_score_oscillation"],
        mitigation_policy="Deploy Non-Linear Regularized Ensemble & Randomized Policy Thresholds",
        description="Iteratively probes payment fraud classifiers with minimal parameter perturbations to map the exact decision boundary."
    ),
    "ADV-02": AttackPrimitive(
        primitive_id="ADV-02",
        family="AI Adaptive Fraud",
        name="Multimodal Identity Synthesis Swarm",
        default_access="Autonomous Multi-Agent Generative AI",
        default_trust="Synthetic Persona Cluster",
        default_rail="A2A",
        default_evasion="Coordinated Cross-Platform Synthetic History",
        default_behavior="Distributed Adaptive Activity",
        default_monetization="Multi-Channel Loan & Overdraft Drain",
        default_temporal="Synchronized Cross-Entity Action",
        observable_signals=["cross_persona_temporal_synchronicity", "synthetic_graph_density_anomaly", "shared_latent_embedding_variance"],
        mitigation_policy="Global Graph Entity Community Detection & Graph Neural Defense",
        description="Multi-agent generative networks construct dozens of intertwined synthetic personas that mutually endorse and transacting with each other."
    ),
    "ADV-03": AttackPrimitive(
        primitive_id="ADV-03",
        family="AI Adaptive Fraud",
        name="Constrained Feature-Space Boundary Wanderer",
        default_access="Stolen Credentials with Genetic Algorithm",
        default_trust="Legitimate Account Vintage",
        default_rail="Card",
        default_evasion="Evolutionary Feature Space Trajectory",
        default_behavior="Stepwise Perturbations",
        default_monetization="Gradual Account Liquidation",
        default_temporal="Adaptive Dynamic Pacing",
        observable_signals=["feature_trajectory_convex_hull_boundary", "evasion_score_monotonic_decrease", "risk_score_variance_near_zero"],
        mitigation_policy="High-Order Non-Linear Feature Interactions & Unsupervised Isolation Modeling",
        description="Uses evolutionary genetic algorithms to mutate payment attributes while strictly satisfying business domain constraints."
    )
}
