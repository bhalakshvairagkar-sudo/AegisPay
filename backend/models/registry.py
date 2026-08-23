"""
Model Registry & Version Management
Saves, loads, and manages trained model artifacts and performance metadata.
"""

from typing import Dict, Any, Optional
import os
from pathlib import Path
import json
import joblib

from backend.models.baseline import RuleBasedClassifier, RandomForestBaselineWrapper
from backend.models.xgboost_model import XGBoostClassifierWrapper
from backend.models.anomaly_model import IsolationForestAnomalyDetector
from backend.models.ensemble import AegisPayHybridDefense


class ModelRegistry:
    """Manages active models, serialized checkpoints, and performance logs."""

    def __init__(self, base_dir: str = "backend/trained_models"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.active_models: Dict[str, Any] = {}
        self.model_metadata: Dict[str, Dict[str, Any]] = {}

    def register(self, model_id: str, model_instance: Any, metadata: Optional[Dict[str, Any]] = None):
        """Registers an in-memory model instance."""
        self.active_models[model_id] = model_instance
        self.model_metadata[model_id] = metadata or {
            "model_id": model_id,
            "name": getattr(model_instance, "name", model_id),
            "type": getattr(model_instance, "model_type", "Model"),
            "version": getattr(model_instance, "version", "v1.0")
        }

    def get(self, model_id: str) -> Optional[Any]:
        return self.active_models.get(model_id)

    def save_model(self, model_id: str, filepath: Optional[str] = None):
        """Serializes model instance to disk."""
        model = self.get(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found in registry.")

        save_path = Path(filepath) if filepath else self.base_dir / f"{model_id}.joblib"
        joblib.dump(model, save_path)

        meta_path = save_path.with_suffix(".json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(self.model_metadata.get(model_id, {}), f, indent=2)

    def load_model(self, model_id: str, filepath: Optional[str] = None) -> Any:
        """Loads serialized model instance from disk."""
        load_path = Path(filepath) if filepath else self.base_dir / f"{model_id}.joblib"
        if not load_path.exists():
            return None

        model = joblib.load(load_path)
        meta_path = load_path.with_suffix(".json")
        meta = {}
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)

        self.register(model_id, model, meta)
        return model


global_registry = ModelRegistry()
