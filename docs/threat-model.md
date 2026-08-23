# AegisPay Threat Model & Attack Taxonomy

**Mastercard Innovation Challenge @ GFF 2026**  
**Track**: AI Defense Lab for Payment Security  

---

## 1. Threat Landscape & Scope

The rapid democratization of generative AI models (LLMs, diffusion models, GANs, voice cloners) has dramatically reduced the barrier to entry for automated, high-fidelity payment fraud.

AegisPay categorizes emerging attack vectors into **8 major families** comprising **36 structured vectors**, aligned with MITRE ATLAS (Adversarial Threat Landscape for AI Systems) and OWASP GenAI security guidelines:

| Family ID | Attack Family Name | Vectors | GenAI Focus | Key Detection Challenge |
|---|---|:---:|:---:|---|
| **ATO** | Account Takeover | 5 | Yes | Residential proxy rotation + WebAuthn downgrade fallback |
| **BIO** | Behavioral Impersonation | 5 | Yes | GAN synthesized mouse physics, touch pressure, & cadence jitter |
| **SOC** | Social Engineering & APP | 5 | Yes | LLM voice clone Authorized Push Payment (APP) coercion |
| **TXN** | Transaction Manipulation | 5 | Partial | Salami slicing ($<\$5.00$) & ISO 20022 rich field payload tampering |
| **MER** | Merchant & BIN Abuse | 5 | Partial | Synthetic storefront laundering & algorithmic BIN permutation |
| **SYN** | Synthetic Identity Abuse | 4 | Yes | Frankenstein identity creation & 3D biometric ID mesh bypass |
| **DEV** | Device & Network Spoofing | 4 | No | Browser WebGL hooking & containerized Android emulator farms |
| **ADV** | AI Adaptive Fraud *(Holdout)* | 3 | Yes | Black-box gradient estimation & decision boundary inversion |

---

## 2. Detailed Attack Vectors (36 Catalog)

### Family 1: Account Takeover (ATO)
- `ATO-01`: Distributed Credential Probing with Micro-Delays (GenAI: Yes)
- `ATO-02`: Session Token Reuse with Geolocation Match (GenAI: No)
- `ATO-03`: Carrier Migration & Liquidity Drain Simulation (GenAI: Yes)
- `ATO-04`: Multi-Card Password Probe Cascade (GenAI: No)
- `ATO-05`: Passkey / WebAuthn Downgrade Fallback Probe (GenAI: Yes)

### Family 2: Behavioral Impersonation (BIO)
- `BIO-01`: Synthetic Keystroke & Pointer Physics Synthesis (GenAI: Yes)
- `BIO-02`: Checkout Navigation Flow Replay (GenAI: No)
- `BIO-03`: Temporal Adaptive Purchase Profiling (GenAI: Yes)
- `BIO-04`: Synthetic Touch Pressure & Gyroscope Mimicry (GenAI: Yes)
- `BIO-05`: Dwell-Time Micro-Pacing Synthesis (GenAI: Yes)

### Family 3: Social Engineering & Authorized Push Payment (SOC)
- `SOC-01`: Manipulated Authorized Push Payment (APP) (GenAI: Yes)
- `SOC-02`: Contextual Subscription Mandate Injection (GenAI: Yes)
- `SOC-03`: Assisted Remote Access Liquidation (GenAI: No)
- `SOC-04`: Autonomous Collaborative Card-Testing Swarm (GenAI: Yes)
- `SOC-05`: Executive Voice Synthesis High-Value Wire Push (GenAI: Yes)

### Family 4: Transaction Manipulation (TXN)
- `TXN-01`: Sub-Threshold Micro-Amount Slicing (Salami) (GenAI: No)
- `TXN-02`: ISO 20022 Rich Field Contextual Tampering (GenAI: No)
- `TXN-03`: Incremental BIN Authorization Laddering (GenAI: Yes)
- `TXN-04`: Pre-Authorization Settlement Hold Exploitation (GenAI: No)
- `TXN-05`: Refund Ledger Desynchronization Arbitrage (GenAI: No)

### Family 5: Merchant & BIN Abuse (MER)
- `MER-01`: Synthetic Collusive Merchant Laundering (GenAI: Yes)
- `MER-02`: E-Commerce Proxy Triangulation (GenAI: No)
- `MER-03`: Algorithmic BIN Range Permutation (GenAI: Yes)
- `MER-04`: Dispute Window Friendly Fraud Simulation (GenAI: No)
- `MER-05`: Sub-Affiliate Commission Arbitrage Network (GenAI: Yes)

### Family 6: Identity & Synthetic Identity Abuse (SYN)
- `SYN-01`: Frankenstein Synthetic Identity Creation (GenAI: Yes)
- `SYN-02`: Synthetic Credit File Seasoning & Bust-Out Exhaust (GenAI: No)
- `SYN-03`: Synthetic ID Document & Biometric Onboarding Bypass (GenAI: Yes)
- `SYN-04`: Dormant Mule Account Fan-Out Layering (GenAI: Yes)

### Family 7: Device & Network Spoofing (DEV)
- `DEV-01`: Browser Telemetry & WebGL Environment Hooking (GenAI: No)
- `DEV-02`: Residential IoT Network Tunneling (GenAI: No)
- `DEV-03`: Virtual Emulator Farm Automation (GenAI: Yes)
- `DEV-04`: Simulated Geolocation & Mock GPS Injection (GenAI: No)

### Family 8: AI-Adaptive Fraud *(Strictly Isolated Holdout)*
- `ADV-01`: Model Inversion Gradient Perturbation Probing (GenAI: Yes)
- `ADV-02`: Holistic Multimodal Identity Synthesis Swarm (GenAI: Yes)
- `ADV-03`: Constrained Feature-Space Boundary Wanderer (GenAI: Yes)

---

## 3. Safe Simulation Boundary & Responsible AI Policy

To maintain complete compliance with payment security safety standards:
- **No Operational Malware**: AegisPay does not generate executable exploits, malware payloads, or malicious scripts.
- **No Credential Theft or Interception**: The platform models behavioral telemetry and statistical distributions, never real cardholder PANs or plaintext OTPs.
- **Defensive Focus**: The objective is strictly benchmarking detector resilience and automating defensive model hardening.
