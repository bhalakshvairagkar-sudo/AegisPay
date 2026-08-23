# AegisPay Implementation Audit & Hardening Matrix

## 1. Executive Summary
This audit rigorously examines the prototype codebase (`aegispay_platform.tsx`), identifying all simulated behaviors, mocked metrics, heuristic decision rules, and hardcoded values. The objective is to replace every simulated layer with genuine mathematical computation, authentic machine learning models, statistical distributions, and real-time backend API integration.

---

## 2. Comprehensive Audit Matrix

| Category | CURRENT (Prototype Implementation) | PROBLEM (Research & Competition Defect) | REQUIRED CHANGE (Hardened Implementation) | FILES AFFECTED |
| :--- | :--- | :--- | :--- | :--- |
| **Data Generation** | `Math.random() * 800 + 10` uniformly generates transaction amounts in React. | Uniform random amounts fail to model real payment distributions (which follow heavy-tailed log-normal curves) and ignore inter-feature dependencies. | Implement Python `PaymentSimulator` with log-normal ticket amounts, Poisson inter-arrival intervals, user home geofences, and multi-window velocity aggregations. | `backend/simulator/`, `backend/simulator/transactions.py`, `frontend/src/components/RedTeamGenerator.tsx` |
| **Attack Detection Logic** | Hardcoded heuristics in React: `detected_v1 = sophistication < 6.5; detected_v2 = sophistication < 8.2 \|\| Math.random() > mut`. | The Red Team generator pre-determines Blue Team detection outcomes without running an actual ML model. | Decouple Red and Blue teams. Red Team generates only observable scenario features and ground truth labels. Blue Team ML models independently output predictions and probabilities. | `backend/attacks/generators/`, `backend/models/`, `frontend/src/components/ScenarioTable.tsx` |
| **Model Benchmarks** | Static `BASELINE_MODELS` array with hardcoded Precision (0.91), Recall (0.82), F1 (0.86), ROC-AUC (0.93), FPR (0.02), Latency (6.2ms). | Fabricated benchmark metrics presented as experimental results violate competition integrity. | Implement real `RandomForestClassifier`, `XGBClassifier`, `IsolationForest`, and `AegisPayHybridDefense`. Compute metrics on a standardized held-out test split. Un-evaluated states display `"Not evaluated"`. | `backend/models/`, `backend/evaluation/metrics.py`, `frontend/src/components/ModelBenchmarkTable.tsx` |
| **SHAP Explainability** | Hardcoded linear formula: `behavioralVariance * 28`, `(1 - deviceFamiliarity) * 22`, `velocityCount * 4.5`. | Fabricated feature attribution masks true model decision boundaries and feature importance. | Compute exact Tree SHAP values via TreeExplainer / exact feature contribution breakdown from the trained XGBoost and Hybrid models. | `backend/models/explainability.py`, `backend/app/api/predict.py`, `frontend/src/components/TransactionSandbox.tsx` |
| **Gap Analysis & Evasion Clustering** | Hardcoded static clusters: Cluster #1 (GAN Keystroke), Cluster #2 (Micro-Amount Slicing), Cluster #3 (Residential Proxy). | Evasion clusters do not reflect actual false negatives produced by the trained model. | Extract actual False Negatives (evaded attacks), normalize feature vectors, and execute K-Means clustering to isolate empirical feature vulnerabilities. | `backend/gap_analysis/clustering.py`, `backend/gap_analysis/failure_analysis.py`, `frontend/src/components/GapAnalysisPanel.tsx` |
| **Adversarial Retraining & Evolution** | Hardcoded evolution rounds R1, R2, R3 with pre-set detection rates (62%, 86%, 96%) and enforced monotonic improvement. | Artificially forcing $v1 < v2 < v3$ lacks scientific rigor. Fails to demonstrate true empirical closed-loop behavior. | Implement genuine closed-loop pipeline: extract false negatives $\rightarrow$ generate targeted counter-samples in evasion feature space $\rightarrow$ retrain model $\rightarrow$ evaluate independently. Honest reporting of gains or trade-offs. | `backend/retraining/adversarial_training.py`, `backend/retraining/evolution.py`, `frontend/src/components/EvolutionTimeline.tsx` |
| **Synthetic Data Fidelity** | Hardcoded static metrics: KS-Test Distance `0.024`, Wasserstein `0.018`, Category Density `96.2%`, Overall `94.8%`. | Hardcoded statistical metrics misrepresent data fidelity validation. | Compute authentic two-sample Kolmogorov-Smirnov test (`scipy.stats.ks_2samp`), 1D Wasserstein distance (`scipy.stats.wasserstein_distance`), and Jensen-Shannon divergence between reference and synthetic distributions. | `backend/evaluation/fidelity.py`, `backend/app/api/fidelity.py`, `frontend/src/components/FidelityEvaluationPanel.tsx` |
| **Adversarial Robustness & Attack Diversity** | Hardcoded robustness score `64/100`, `82/100`, `94/100` and static level bar heights (94%, 78%, 52%, 28%). | Fabricated degradation curves without underlying empirical tests against stepped difficulty levels. | Calculate robustness curve from actual model recall across 5 distinct difficulty levels (Easy, Moderate, Hard, Adversarial, Unseen). Compute normalized Attack Diversity Score from feature-space dispersion. | `backend/evaluation/robustness.py`, `frontend/src/components/RobustnessChart.tsx` |
| **Holdout / Unseen Attack Evaluation** | Static numbers for `ADV-01` Gradient Probing (42.0% vs 89.5%). | Zero-shot evaluation was purely static rather than tested against an unexposed attack family. | Strictly reserve attack family `ADV` (AI Adaptive Fraud) during training and counterexample synthesis. Evaluate only during final zero-shot evaluation. | `backend/retraining/evolution.py`, `frontend/src/components/HoldoutEvaluationCard.tsx` |
| **Judge 1-Click Demo** | Frontend-only `setTimeout` chain (2.5s, 5.5s, 8.5s, 11.5s) updating local UI state. | Simulated demo does not execute or prove the closed-loop pipeline. | Connect 1-Click Demo to backend orchestrator that executes the full 10-step pipeline or replays genuine precomputed artifacts with real progress tracking. | `backend/app/api/judge_demo.py`, `frontend/src/components/JudgeDemoModal.tsx` |
| **Attack Taxonomy & Threat Model** | Prototype descriptions included operational exploit terms (e.g. Frida hooking, APK builds). | Defensive research platforms must focus on observable behavioral characteristics and detection signatures rather than operational exploit instructions. | Refine 36 attack vectors to describe observable behavioral features, synthetic anomaly signals, detection challenges, and mitigation policies. | `backend/attacks/taxonomy.py`, `docs/threat-model.md`, `frontend/src/components/AttackCatalog.tsx` |
| **Frontend Architecture** | Single monolithic 1,615-line file (`aegispay_platform.tsx`) mixing state, mocks, and presentation. | Difficult to maintain, test, and connect cleanly to backend REST endpoints. | Modularize into clean component hierarchy with typed API service layer, React hooks, and live/demo mode state toggles. | `frontend/src/`, `frontend/src/App.tsx`, `frontend/src/services/api.ts` |

---

## 3. Data Leakage Prevention Protocol
To guarantee ML integrity:
1. **Forbidden Features during Model Training/Inference**:
   - `attack_id`, `attack_family`, `attack_name`, `sophistication`, `genAi`, `is_adversarial`, `mutation_strength`, `ground_truth_label`.
2. **Allowed Input Features (Standardized Feature Matrix $\mathbf{X}$)**:
   - `amount`, `velocity_1h`, `velocity_24h`, `device_familiarity`, `geo_distance_km`, `behavioral_deviation`, `merchant_risk_score`, `account_age_days`, `touch_pressure_deviation`, `carrier_change_flag`, `mcc_risk_weight`, `hour_of_day`.
3. **Explicit Isolation**: Metadata is maintained solely in the evaluation layer for post-hoc gap analysis and evasion clustering.

---

## 4. Verification & Hardening Plan
The transition from prototype to research-grade platform will proceed across structured phases:
- **Phase 1**: Data Leakage Documentation & Threat Model Refinement.
- **Phase 2**: Python Synthetic Payment Simulator with Seeded Reproducibility.
- **Phase 3**: Parameterized Safe Attack Generator & Difficulty Mutation Engine.
- **Phase 4**: Real ML Baselines (Rule, RF, XGBoost, Isolation Forest) & AegisPay Hybrid Ensemble with SHAP attribution.
- **Phase 5**: Evaluation Engine, Robustness Matrix, and Mathematical Fidelity Calculator.
- **Phase 6**: False Negative Extraction, K-Means Evasion Clustering, and Targeted Retraining Loop.
- **Phase 7**: REST API Layer (FastAPI) & Offline Demo Artifact Generator.
- **Phase 8**: Frontend Refactoring & Integration with Live Experiment / Demo Artifact Badges.
- **Phase 9**: Comprehensive Automated Test Suite & End-to-End Validation.
