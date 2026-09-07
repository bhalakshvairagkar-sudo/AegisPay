"""
AegisPay v2 - Adversarial Retraining Pipeline
Retrains Blue Team hybrid models using combined base and weighted hard-example pools.
"""

from typing import Dict, Any, List, Tuple, Optional
import pandas as pd
import numpy as np

from backend.models.ensemble import AegisPayHybridDefense
from backend.models.registry import global_registry
from backend.models.calibration import calibration_engine
from backend.retraining.hard_example_pool import hard_example_pool


class AdversarialRetrainingPipeline:
    """Orchestrates closed-loop adversarial retraining and registers new model checkpoints."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def retrain_model(
        self,
        base_X: pd.DataFrame,
        base_y: np.ndarray,
        target_version: str = "v2.0",
        round_index: int = 1
    ) -> Tuple[AegisPayHybridDefense, Dict[str, Any]]:
        """
        Retrains defense model by combining base dataset with hard-example pool.
        """
        hard_X, hard_y, hard_w = hard_example_pool.get_hard_examples()

        if len(hard_X) > 0:
            # Base samples have default weight 1.0
            base_w = np.ones(len(base_X), dtype=float)
            X_combined = pd.concat([base_X, hard_X], ignore_index=True)
            y_combined = np.concatenate([base_y, hard_y])
            w_combined = np.concatenate([base_w, hard_w])
        else:
            X_combined = base_X.copy()
            y_combined = base_y.copy()
            w_combined = np.ones(len(base_X), dtype=float)

        # Shuffle combined dataset
        rng = np.random.RandomState(self.seed + round_index)
        idx = rng.permutation(len(X_combined))
        X_shuffled = X_combined.iloc[idx].reset_index(drop=True)
        y_shuffled = y_combined[idx]
        w_shuffled = w_combined[idx]

        # Train new defense ensemble instance
        new_model = AegisPayHybridDefense(
            version=target_version,
            seed=self.seed + round_index
        )
        new_model.fit(X_shuffled, y_shuffled, sample_weight=w_shuffled)

        # Fit Calibration on retrained model predictions
        raw_preds = new_model.predict_proba(X_shuffled)
        calibration_engine.fit(raw_preds, y_shuffled)

        # Register in global registry
        model_id = f"aegispay_{target_version.replace('.', '_')}"
        meta = {
            "model_id": model_id,
            "version": target_version,
            "round_index": round_index,
            "total_training_samples": len(X_shuffled),
            "hard_examples_count": len(hard_X),
            "mean_sample_weight": round(float(np.mean(w_shuffled)), 3),
            "status": "DEPLOYED"
        }
        global_registry.register(model_id, new_model, meta)

        return new_model, meta


retraining_pipeline = AdversarialRetrainingPipeline()
