"""
Experiment Registry & Benchmarking Records
Stores reproducible experiment runs with EXP-YYYYMMDD-XXXX identifiers.
"""

from typing import Dict, Any, List, Optional
import os
import json
import time
from datetime import datetime
from pathlib import Path


class ExperimentRegistry:
    """Stores and retrieves experiment records."""

    def __init__(self, storage_dir: str = "backend/experiments"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._experiments: Dict[str, Dict[str, Any]] = {}
        self._load_existing()

    def _load_existing(self):
        for f in self.storage_dir.glob("EXP-*.json"):
            try:
                with open(f, "r", encoding="utf-8") as exp_file:
                    data = json.load(exp_file)
                    exp_id = data.get("experiment_id")
                    if exp_id:
                        self._experiments[exp_id] = data
            except Exception:
                pass

    def create_experiment_id(self) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        existing_today = [k for k in self._experiments.keys() if f"EXP-{date_str}" in k]
        seq = len(existing_today) + 1
        return f"EXP-{date_str}-{seq:04d}"

    def record_experiment(
        self,
        experiment_id: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        models_evaluated: Optional[List[Dict[str, Any]]] = None,
        evolution_rounds: Optional[List[Dict[str, Any]]] = None,
        fidelity_metrics: Optional[Dict[str, Any]] = None,
        robustness_metrics: Optional[Dict[str, Any]] = None,
        unseen_metrics: Optional[Dict[str, Any]] = None,
        dataset_version: str = "SYN-2026.1",
        seed: int = 42
    ) -> Dict[str, Any]:
        """Creates and stores a complete experiment artifact."""
        exp_id = experiment_id or self.create_experiment_id()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "experiment_id": exp_id,
            "timestamp": timestamp,
            "dataset_version": dataset_version,
            "seed": seed,
            "config": config or {},
            "models_evaluated": models_evaluated or [],
            "evolution_rounds": evolution_rounds or [],
            "fidelity_metrics": fidelity_metrics or {},
            "robustness_metrics": robustness_metrics or {},
            "unseen_metrics": unseen_metrics or {},
        }

        self._experiments[exp_id] = record

        # Save to disk
        file_path = self.storage_dir / f"{exp_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        return record

    def get_latest(self) -> Optional[Dict[str, Any]]:
        if not self._experiments:
            return None
        sorted_keys = sorted(self._experiments.keys(), reverse=True)
        return self._experiments[sorted_keys[0]]

    def get_by_id(self, exp_id: str) -> Optional[Dict[str, Any]]:
        return self._experiments.get(exp_id)

    def list_all(self) -> List[Dict[str, Any]]:
        return [self._experiments[k] for k in sorted(self._experiments.keys(), reverse=True)]


experiment_registry = ExperimentRegistry()
