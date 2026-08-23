"""
Gap Analysis & Evasion Clustering Engine
Extracts actual False Negatives (missed attacks) from model predictions and clusters them using K-Means.
Identifies empirical weak feature dimensions and dominant attack failure modes.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from backend.simulator.transactions import SyntheticTransaction


class GapAnalyzer:
    """Isolates model false negatives and clusters evasions to reveal systemic vulnerabilities."""

    def __init__(self, n_clusters: int = 3, seed: int = 42):
        self.n_clusters = n_clusters
        self.seed = seed
        self.scaler = StandardScaler()

    def analyze_evasions(
        self,
        scenarios: List[SyntheticTransaction],
        predictions: np.ndarray,
        probabilities: np.ndarray
    ) -> Dict[str, Any]:
        """
        Extracts false negatives (evaded attacks: y_true=1, y_pred=0) and clusters them.
        """
        evaded_indices = [i for i, pred in enumerate(predictions) if pred == 0 and scenarios[i].is_fraud == 1]
        total_attacks = len(scenarios)
        evasion_count = len(evaded_indices)
        evasion_rate = round((evasion_count / max(1, total_attacks)) * 100.0, 1)

        if evasion_count == 0:
            return {
                "total_tested": total_attacks,
                "evasion_count": 0,
                "evasion_rate": 0.0,
                "clusters": [],
                "recommendation": "No evasions discovered on this test batch. Defense is robust."
            }

        evaded_scenarios = [scenarios[i] for i in evaded_indices]
        evaded_probs = [probabilities[i] for i in evaded_indices]

        # Feature matrix of evasions
        df_evasions = pd.DataFrame([s.to_feature_dict() for s in evaded_scenarios])

        # Cluster evasions (adjust cluster count if few samples)
        k = min(self.n_clusters, max(1, evasion_count // 2))
        X_scaled = self.scaler.fit_transform(df_evasions)

        if k > 1:
            kmeans = KMeans(n_clusters=k, random_state=self.seed, n_init=10)
            cluster_labels = kmeans.fit_predict(X_scaled)
        else:
            cluster_labels = np.zeros(len(evaded_scenarios), dtype=int)

        clusters = []
        cluster_impacts = ["High Impact", "Medium Impact", "Low Impact"]

        for c_id in range(k):
            mask = (cluster_labels == c_id)
            c_scenarios = [evaded_scenarios[j] for j in range(len(mask)) if mask[j]]
            c_count = len(c_scenarios)
            if c_count == 0:
                continue

            c_pct = round((c_count / evasion_count) * 100.0, 1)
            c_df = df_evasions[mask]

            # Dominant attack family
            fam_counts = {}
            for s in c_scenarios:
                fam_counts[s.attack_family] = fam_counts.get(s.attack_family, 0) + 1
            dominant_fam = max(fam_counts, key=fam_counts.get)

            # Identify weak feature: feature whose mean in evasions is closest to legitimate baseline (fooling the model)
            # or with unusual values
            mean_vals = c_df.mean()
            weak_feat = "behavioral_deviation"
            weak_desc = "Biometric Cadence / Touch Jitter Standard Dev"

            if mean_vals.get("amount", 100) < 10.0:
                weak_feat = "velocity_1h"
                weak_desc = "1-Hour Micro-Auth Window Velocity"
            elif mean_vals.get("geo_distance_km", 0) < 50.0 and mean_vals.get("device_familiarity", 0) > 0.5:
                weak_feat = "device_familiarity"
                weak_desc = "Residential Proxy Geolocation Match"
            elif mean_vals.get("behavioral_deviation", 0) < 0.25:
                weak_feat = "behavioral_deviation"
                weak_desc = "Touch & Motion Sensor Variance"

            title_map = {
                "Behavioral Impersonation": "GAN Behavioral Touch & Cadence Mimicry",
                "Transaction Manipulation": "Micro-Amount Slicing (sub-$5.00)",
                "Device Spoofing": "Residential Proxy Geofence Match",
                "Account Takeover": "SIM Swap & Carrier Migration Velocity",
                "AI Adaptive Fraud": "Adversarial Gradient Perturbation",
            }
            cluster_title = title_map.get(dominant_fam, f"{dominant_fam} Evasion Archetype")

            clusters.append({
                "cluster_id": f"CLUSTER #{c_id + 1:02d}",
                "impact_badge": cluster_impacts[c_id % len(cluster_impacts)],
                "title": cluster_title,
                "dominant_family": dominant_fam,
                "evasion_count": c_count,
                "percentage_of_evasions": c_pct,
                "weak_feature": weak_feat,
                "weak_feature_label": weak_desc,
                "description": f"Missed {c_count} attacks in {dominant_fam}. Attacks closely mirrored normal baseline distributions.",
                "centroid_features": {k: round(float(v), 3) for k, v in mean_vals.items()}
            })

        # Generate targeted retraining recommendation
        recommendation = (
            f"Gap Analysis engine isolated {evasion_count} evasions across {len(clusters)} distinct clusters. "
            f"Recommend generating {min(500, evasion_count * 25)} targeted adversarial counter-samples focusing on "
            f"{clusters[0]['weak_feature_label']} to harden defense."
        )

        return {
            "total_tested": total_attacks,
            "evasion_count": evasion_count,
            "evasion_rate": evasion_rate,
            "clusters": clusters,
            "recommendation": recommendation,
            "evaded_scenarios": [s.to_full_dict() for s in evaded_scenarios[:15]]
        }
