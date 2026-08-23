# AegisPay Architecture & System Design

**Project**: AegisPay — AI Defense Lab for Payment Security  
**Event**: Mastercard Innovation Challenge @ Global Fintech Fest (GFF) 2026  
**Track**: AI Defense Lab for Payment Security  
**Version**: 2026.1  

---

## 1. System Overview

AegisPay is an autonomous closed-loop adversarial payment-security defense platform designed to simulate, detect, analyze, and defend against emerging generative-AI and automated payment fraud vectors.

Unlike conventional fraud systems that rely on static heuristics or non-adaptive batch-trained models, AegisPay implements a continuous closed feedback loop between an Adversarial Red Team scenario generator and an Adaptive Blue Team defense ensemble.

```
+-----------------------------------------------------------------------------+
|                           AEGISPAY CLOSED LOOP                              |
+-----------------------------------------------------------------------------+
|                                                                             |
|   [1. IDENTIFY]           [2. GENERATE]             [3. SIMULATE]           |
|  36 Attack Vectors    --> Parametric Mutator    --> Synthetic Payment Stream|
|  (8 Threat Families)       (Levels 1 to 5)          (Users, Devices, MCCs)  |
|                                                            |                |
|                                                            v                |
|   [6. HARDEN & RETRAIN]   [5. COUNTER-SAMPLES]      [4. DETECT & SCORE]     |
|  Adversarial Training <-- Cluster Centroids     <-- Hybrid Defense Ensemble |
|  (Weighted Retraining)     (Targeted Synthesis)     (XGB + Isolation Forest)|
|         |                                                  |                |
|         v                                                  v                |
|   [7. RE-EVALUATE]        [8. DISCOVER WEAKNESSES]  [4b. GAP ANALYSIS]      |
|  Multi-Round Evolution<-- Zero-Shot Holdout     <-- K-Means False Negative  |
|  (R1 -> R2 -> R3)          (ADV-01 Inversion)       Clustering Matrix       |
|                                                                             |
+-----------------------------------------------------------------------------+
```

---

## 2. Core Architectural Components

### 2.1 Synthetic Payment Simulator (`backend/simulator/`)
- **Cardholder Population (`users.py`)**: Models consumer risk personas with log-normal baseline spending, home geographic coordinates, and average velocity profiles.
- **Merchant Network (`merchants.py`)**: Simulates 12 MCC categories with empirical chargeback baselines and merchant risk weights.
- **Device Telemetry Pool (`devices.py`)**: Synthesizes device fingerprints, OS families, browser WebGL hashes, touch sensor variance, and carrier routing flags.
- **Statistical Transaction Stream (`transactions.py`)**: Combines log-normal monetary amounts, Poisson arrival processes, and Haversine distance computations to produce a realistic stream with zero synthetic data leakage.

### 2.2 Attack Intelligence & Red Team Mutator (`backend/attacks/`)
- **Attack Taxonomy (`taxonomy.py`)**: 36 structured attack vectors across 8 families with GenAI flags, observable signals, and mitigation policies.
- **Parametric Mutator (`mutations/mutator.py`)**: Applies deterministic feature perturbations across 5 difficulty levels (Level 1 Easy to Level 5 Unseen).
- **Scenario Generator (`generators/scenario_generator.py`)**: Constructs fully parameterized fraud scenarios combining attack profiles with baseline cardholder identities.

### 2.3 Blue Team Hybrid Defense Ensemble (`backend/models/`)
- **Supervised Classifier (`xgboost_model.py`)**: Gradient-boosted decision trees trained with `scale_pos_weight` to address class imbalance.
- **Unsupervised Anomaly Detector (`anomaly_model.py`)**: Isolation Forest trained strictly on legitimate transaction patterns to flag out-of-distribution behaviors.
- **Static Rules Engine (`baseline.py`)**: Legacy velocity and amount threshold engine serving as historical benchmark.
- **Hybrid Risk Gating (`ensemble.py`)**: Unified risk scoring (0-100) mapping into 4 automated policy decisions:
  - `0 - 29`: **ALLOW** (Frictionless baseline)
  - `30 - 59`: **STEP-UP 3DS VERIFY** (Passive authentication / challenge)
  - `60 - 79`: **MANUAL REVIEW** (Fraud analyst queue)
  - `80 - 100`: **SILENT BLOCK** (Gateway level rejection)
- **Explainability Engine (`explainability.py`)**: Feature attribution waterfall isolating positive risk drivers and negative mitigating safe factors.

### 2.4 Gap Analyzer & Adversarial Retraining Engine (`backend/gap_analysis/`, `backend/retraining/`)
- **Evasion Isolation (`clustering.py`)**: Isolates false negative evasion records where fraud passed undetected ($y=1, \hat{y}=0$).
- **K-Means Evasion Clustering**: Groups evasions into behavioral clusters, identifies dominant attack families, and pinpoints weak feature dimensions.
- **Targeted Counter-Sample Generator (`adversarial_training.py`)**: Synthesizes targeted counterexamples focused on evasion cluster centroids.
- **Sample-Weighted Hardening**: Retrains defense models with higher loss weighting on previously evaded manifolds.
- **Evolution Lab (`evolution.py`)**: Tracks multi-round defense progression ($R_1 \rightarrow R_2 \rightarrow R_3$) and validates generalization against strictly reserved holdout attacks (`ADV-01`).

---

## 3. Strict Feature Isolation & Data Leakage Prevention

To ensure scientific validity and avoid data leakage:
- **Clean Model Feature Matrix $\mathbf{X} \in \mathbb{R}^{13}$**:
  1. `amount`: Transaction amount ($)
  2. `velocity_1h`: Hourly transaction count
  3. `velocity_24h`: Daily transaction count
  4. `device_familiarity`: Historical device affinity index $[0, 1]$
  5. `geo_distance_km`: Haversine distance from cardholder home anchor (km)
  6. `behavioral_deviation`: Touch/cadence sensor deviation index $[0, 1]$
  7. `merchant_risk_score`: Baseline merchant risk index $[0, 1]$
  8. `account_age_days`: Age of payment credential (days)
  9. `touch_pressure_deviation`: Touch screen pressure variance index $[0, 1]$
  10. `carrier_change_flag`: Recent cellular carrier porting flag $\{0, 1\}$
  11. `mcc_risk_weight`: Merchant category code risk weighting $[0, 1]$
  12. `hour_of_day`: Local transaction hour $[0, 23]$
  13. `is_international`: Cross-border transaction indicator $\{0, 1\}$

- **Prohibited Metadata (Strictly Excluded from Training & Inference)**:
  `attack_id`, `attack_family`, `attack_name`, `gen_ai`, `sophistication`, `difficulty`, `mutation_strength`, `is_fraud`, `ground_truth`.

---

## 4. Hardware and Software Specifications
- **Backend**: Python 3.14, FastAPI, Uvicorn, Scikit-learn, XGBoost, NumPy, SciPy, Pandas, Joblib.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide React.
- **Test Suite**: Pytest (19/19 passing unit & integration tests).
- **Latency**: Sub-1ms per-transaction inference latency ($0.8\text{ms}$).
