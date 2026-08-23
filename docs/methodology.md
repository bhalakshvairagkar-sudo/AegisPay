# AegisPay Research Methodology & Mathematical Foundations

**Mastercard Innovation Challenge @ GFF 2026**  
**Track**: AI Defense Lab for Payment Security  

---

## 1. Adversarial Mutation Methodology

To evaluate model resilience against real-world evasion strategies, AegisPay implements parametric mutation vectors across 5 difficulty tiers:

$$\mathbf{x}_{\text{mutated}} = \mathbf{x}_{\text{base}} + \delta(\mu, \sigma, \lambda)$$

Where $\delta$ represents a bounded perturbation vector:
- **Level 1 (Easy)**: High noise ($\sigma=0.50$), obvious velocity spikes ($>8\text{ tx/h}$), high geographic displacement ($>800\text{ km}$).
- **Level 2 (Moderate)**: Realistic fraud patterns ($\sigma=0.35$), moderate velocity ($3-6\text{ tx/h}$).
- **Level 3 (Hard)**: Bounded perturbations ($\sigma=0.20$), sub-threshold amounts ($<\$50$), near-normal behavioral biometric cadence.
- **Level 4 (Adversarial Whitebox)**: Gradient-directed boundary walking ($\sigma=0.10$) keeping features just within normal cardholder distributions.
- **Level 5 (Unseen Holdout)**: Multi-modal zero-shot attacks (`ADV-01`, `ADV-02`) reserved strictly from the training corpus.

---

## 2. Evasion Clustering & Centroid Discovery (Gap Analysis)

When evaluating a defense model $f(\mathbf{x})$, the gap analysis engine isolates the false negative evasion set:

$$\mathcal{E} = \{ (\mathbf{x}_i, y_i) \mid y_i = 1 \land f(\mathbf{x}_i) = 0 \}$$

Using K-Means clustering on the normalized feature space $\tilde{\mathbf{X}}_{\mathcal{E}}$, the engine computes $k$ evasion centroids:

$$\mathbf{c}_j = \frac{1}{|\mathcal{C}_j|} \sum_{\mathbf{x} \in \mathcal{C}_j} \mathbf{x}$$

For each cluster $\mathcal{C}_j$, the feature $m$ exhibiting the highest variance relative to standard fraud distributions is identified as the **vulnerable feature dimension**:

$$m^* = \arg\max_m \left| c_{j, m} - \bar{x}_{\text{legit}, m} \right|$$

---

## 3. Targeted Adversarial Counter-Sample Synthesis

To harden the model against the discovered evasion manifolds without inducing catastrophic forgetting of clean transactions, the trainer synthesizes targeted counterexamples centered around $\mathbf{c}_j$:

$$\mathbf{x}_{\text{counter}} = \mathbf{c}_j + \epsilon \cdot \mathcal{N}(0, \mathbf{\Sigma}_j), \quad \epsilon \sim \mathcal{U}(0.05, 0.20)$$

The retraining loss function incorporates an evasion-weighted sample penalty:

$$\mathcal{L}_{\text{hardened}}(\theta) = \sum_{i \in \mathcal{D}_{\text{train}}} w_i \cdot \ell(f(\mathbf{x}_i; \theta), y_i) + \sum_{k \in \mathcal{D}_{\text{counter}}} w_{\text{counter}} \cdot \ell(f(\mathbf{x}_k; \theta), 1)$$

Where $w_{\text{counter}} = 2.5 \times w_{\text{standard}}$, ensuring the decision boundary shifts to encompass the previously exploited blind spots.

---

## 4. Synthetic Data Statistical Fidelity Metric

To ensure that the payment simulation produces high-fidelity, research-grade synthetic streams, AegisPay measures similarity across four statistical tests:

1. **Two-Sample Kolmogorov-Smirnov (KS) Test**:
   $$D_{\text{KS}} = \sup_x |F_{\text{ref}}(x) - F_{\text{syn}}(x)|$$

2. **1D Wasserstein (Earth Mover's) Distance**:
   $$W_1(P, Q) = \int_{-\infty}^{\infty} |F_P(x) - F_Q(x)| \, dx$$

3. **Jensen-Shannon (JS) Divergence**:
   $$D_{\text{JS}}(P \parallel Q) = \frac{1}{2} D_{\text{KL}}(P \parallel M) + \frac{1}{2} D_{\text{KL}}(Q \parallel M), \quad M = \frac{1}{2}(P + Q)$$

4. **Frobenius Correlation Alignment**:
   $$\text{CorrSim} = 100 \times \left( 1 - \frac{\| \mathbf{R}_{\text{ref}} - \mathbf{R}_{\text{syn}} \|_F}{\| \mathbf{R}_{\text{ref}} \|_F} \right)$$

### Open Composite Fidelity Score:
$$\text{Fidelity} = 100 \times \Big[ 0.35(1 - D_{\text{KS}}) + 0.25(1 - 2 W_1) + 0.20(1 - D_{\text{JS}}) + 0.20 \frac{\text{CorrSim}}{100} \Big]$$

Empirical baseline on AegisPay Simulator: **$80.2 / 100$**.

---

## 5. Honest Empirical Reporting (No Forced Monotonicity)

AegisPay strictly enforces honest performance measurement:
- Models $v1.0$, $v2.0$, and $v3.0$ are evaluated independently on held-out test distributions.
- No artificial $v1 < v2 < v3$ monotonicity constraints are imposed.
- Degradations, trade-offs, and unchanged metrics are reported transparently.
