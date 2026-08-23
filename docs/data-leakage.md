# AegisPay Data Leakage Prevention Specification

## 1. Objective
Machine learning models evaluated in adversarial security settings must not inadvertently learn artifacts of the synthetic attack generation pipeline. This document defines the strict feature-selection boundary, prohibited generator metadata, and feature validation pipeline implemented in AegisPay.

---

## 2. Prohibited Features (Strictly Excluded from Model Input Matrix $\mathbf{X}$)

The following features describe scenario generation metadata and ground truth labels. They are strictly prohibited from being passed to any model during training, validation, testing, or real-time inference:

| Feature Key | Description | Risk of Leakage |
| :--- | :--- | :--- |
| `attack_id` | Unique ID of the attack vector (e.g., `ATO-01`, `BIO-01`) | High: Allows model to memorize discrete vector signatures. |
| `family` / `attack_family` | High-level attack family (e.g., `Account Takeover`, `Social Engineering`) | Critical: Directly encodes attack taxonomy category. |
| `attack_name` | Human-readable attack title | Critical: Exact semantic label of the attack. |
| `genAi` / `is_gen_ai` | Boolean flag indicating GenAI-enhanced synthesis | High: Leaks generation mechanism. |
| `sophistication` | Red Team baseline sophistication rating (1.0 - 10.0) | High: Direct statistical proxy for difficulty. |
| `difficulty` | Categorical difficulty (`Easy`, `Moderate`, `Hard`, `Adversarial`, `Unseen`) | High: Artificially separates test distributions. |
| `mutation_strength` | Numerical mutation perturbation scale (0.1 - 0.9) | Critical: Direct generator parameter. |
| `target_attack` / `generator_type` | Internal generator module identifier | High: Identifies specific synthetic code path. |
| `is_adversarial` / `is_synthetic_counterexample` | Boolean flag tagging retraining counterexamples | Critical: Leaks whether sample is an adversarial augmentation. |
| `fraud_label` / `ground_truth` | Binary fraud target ($y \in \{0, 1\}$) | Critical: Target label leakage. |

---

## 3. Allowed Model Input Features ($\mathbf{X} \in \mathbb{R}^{D}$)

Models receive strictly observable payment, telemetry, and historical behavioral features available to a payment switch / fraud engine at authorization time:

| Feature Key | Type | Distribution / Range | Operational Meaning |
| :--- | :--- | :--- | :--- |
| `amount` | Float | $\mathbb{R}^+$, typically $\$0.50 - \$5,000.00$ | Transaction authorized monetary amount in USD. |
| `velocity_1h` | Integer | $0 - 50$ | Count of authorized transactions for this cardholder in preceding 1 hour. |
| `velocity_24h` | Integer | $0 - 200$ | Count of authorized transactions for this cardholder in preceding 24 hours. |
| `device_familiarity` | Float | $[0.0, 1.0]$ | Ratio of user's historical transactions conducted on this hardware fingerprint. |
| `geo_distance_km` | Float | $\mathbb{R}^+$, $0 - 20,000\text{ km}$ | Haversine distance between current transaction IP/GPS and user 30-day centroid. |
| `behavioral_deviation`| Float | $[0.0, 1.0]$ | Mahalanobis / biometric variance vs. user historical typing/touch cadence. |
| `merchant_risk_score` | Float | $[0.0, 1.0]$ | Historical chargeback ratio and MCC baseline risk for the merchant. |
| `account_age_days` | Integer | $1 - 3,650$ | Number of days since payment account / cardholder onboarding. |
| `touch_pressure_deviation`| Float| $[0.0, 1.0]$ | Biometric sensor deviation (touch pressure / mouse curve physics). |
| `carrier_change_flag`| Integer | $\{0, 1\}$ | Binary indicator of cellular SIM/carrier re-registration within last 48 hours. |
| `mcc_risk_weight` | Float | $[0.0, 1.0]$ | Risk weighting associated with Merchant Category Code (e.g. 6011 high, 5411 low). |
| `hour_of_day` | Integer | $0 - 23$ | Local hour of transaction initiation. |
| `is_international` | Integer | $\{0, 1\}$ | Binary flag indicating cross-border transaction. |

---

## 4. Preprocessing & Feature Isolation Pipeline

```
Raw Scenario Payload (JSON)
       ↓
[ Feature Selector Layer ]
       ├── Allowed Feature Extractor ────→ Matrix X (Clean Numeric Vector) ──→ ML Model Input
       └── Metadata Preserver ───────────→ Metadata Store (Evaluation, Gap Clustering, Auditing)
```

### Feature Isolation Code Implementation:
```python
ALLOWED_FEATURES = [
    "amount",
    "velocity_1h",
    "velocity_24h",
    "device_familiarity",
    "geo_distance_km",
    "behavioral_deviation",
    "merchant_risk_score",
    "account_age_days",
    "touch_pressure_deviation",
    "carrier_change_flag",
    "mcc_risk_weight",
    "hour_of_day",
    "is_international",
]

def extract_clean_features(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    # Strict validation: raise error if prohibited keys are found in training input
    clean_df = df[ALLOWED_FEATURES].copy()
    return clean_df
```

---

## 5. Train / Validation / Test / Holdout Separation
To prevent data contamination:
1. **Train Set ($60\%$)**: Synthesized legitimate user streams + Known Attack Families (ATO, BIO, SOC, TXN, MER, SYN, DEV).
2. **Validation Set ($15\%$)**: Independent user/attack sequences for hyperparameter tuning and threshold selection.
3. **Standard Test Set ($15\%$)**: Unseen seeds of known attack families for evaluating standard generalization.
4. **Zero-Shot Unseen Holdout Set ($10\%$)**: Attack family `ADV` (AI Adaptive Fraud: `ADV-01`, `ADV-02`) strictly reserved. Never used for training, feature extraction, or hyperparameter selection.
