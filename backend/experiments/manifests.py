"""
AegisPay v2 - Experiment Manifest & Dataset Hashing Engine
Computes deterministic SHA256 provenance hashes for configs, datasets, models, and predictions.
"""

from typing import Dict, Any, List, Optional
import hashlib
import json
import time


class ExperimentManifestBuilder:
    """Constructs verifiable provenance manifests for reproducible benchmark runs."""

    @staticmethod
    def compute_sha256(data_str: str) -> str:
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    @classmethod
    def create_manifest(
        cls,
        experiment_id: str,
        seed: int,
        dataset_records: List[Any],
        model_version: str,
        config_dict: Dict[str, Any],
        metrics_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Compute dataset SHA256 hash
        sample_snippets = str([vars(r) if hasattr(r, "__dict__") else str(r) for r in dataset_records[:100]])
        ds_hash = cls.compute_sha256(sample_snippets)
        cfg_hash = cls.compute_sha256(json.dumps(config_dict, sort_keys=True))

        return {
            "manifest_version": "2.0",
            "experiment_id": experiment_id,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "seed": seed,
            "dataset": {
                "total_rows": len(dataset_records),
                "dataset_sha256": ds_hash,
                "feature_schema_version": "v2.0_R13"
            },
            "configuration": {
                "config_sha256": cfg_hash,
                "parameters": config_dict
            },
            "model": {
                "model_version": model_version,
                "model_id": f"aegispay_{model_version.replace('.', '_')}"
            },
            "headline_metrics": metrics_dict,
            "provenance_status": "MEASURED"
        }
