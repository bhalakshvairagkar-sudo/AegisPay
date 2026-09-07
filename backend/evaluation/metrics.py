"""
AegisPay v2 - Scientific Evaluation Metrics
Computes PR-AUC, Recall @ fixed low FPR (0.1%), 95% bootstrapped confidence intervals, and strict denominators.
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve
)


def compute_recall_at_fixed_fpr(y_true: np.ndarray, y_scores: np.ndarray, target_fpr: float = 0.001) -> float:
    """Calculates Recall at a fixed, low False Positive Rate (e.g. 0.1% / 0.001)."""
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    # Find largest TPR where FPR <= target_fpr
    valid_indices = np.where(fpr <= target_fpr)[0]
    if len(valid_indices) == 0:
        return float(tpr[0])
    return float(tpr[valid_indices[-1]])


def bootstrap_metric_confidence_interval(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    y_pred: np.ndarray,
    n_bootstraps: int = 200,
    seed: int = 42
) -> Dict[str, Tuple[float, float]]:
    """Calculates 95% empirical confidence intervals via non-parametric bootstrapping."""
    rng = np.random.RandomState(seed)
    n = len(y_true)
    if n < 10:
        return {}

    f1_boot = []
    prauc_boot = []
    rec_boot = []

    for _ in range(n_bootstraps):
        idx = rng.randint(0, n, size=n)
        if len(np.unique(y_true[idx])) < 2:
            continue
        f1_boot.append(f1_score(y_true[idx], y_pred[idx], zero_division=0))
        prauc_boot.append(average_precision_score(y_true[idx], y_scores[idx]))
        rec_boot.append(recall_score(y_true[idx], y_pred[idx], zero_division=0))

    def get_ci(arr):
        if not arr:
            return (0.0, 0.0)
        return (round(float(np.percentile(arr, 2.5)), 4), round(float(np.percentile(arr, 97.5)), 4))

    return {
        "f1_ci_95": get_ci(f1_boot),
        "pr_auc_ci_95": get_ci(prauc_boot),
        "recall_ci_95": get_ci(rec_boot)
    }


def compute_comprehensive_metrics(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    threshold: float = 0.50,
    seed: int = 42
) -> Dict[str, Any]:
    """Computes all primary and secondary evaluation metrics with denominators and confidence intervals."""
    y = np.asarray(y_true, dtype=int)
    scores = np.asarray(y_scores, dtype=float).clip(0.0, 1.0)
    y_pred = (scores >= threshold).astype(int)

    tn, fp, fn, tp = confusion_matrix(y, y_pred, labels=[0, 1]).ravel()
    total_samples = len(y)
    total_positives = int(tp + fn)
    total_negatives = int(tn + fp)
    total_alerts = int(tp + fp)

    # Primary metrics
    pr_auc = float(average_precision_score(y, scores)) if len(np.unique(y)) > 1 else 0.50
    recall_01_fpr = compute_recall_at_fixed_fpr(y, scores, target_fpr=0.001)
    recall_1_fpr = compute_recall_at_fixed_fpr(y, scores, target_fpr=0.01)

    rec = float(recall_score(y, y_pred, zero_division=0))
    prec = float(precision_score(y, y_pred, zero_division=0))
    f1 = float(f1_score(y, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y, scores)) if len(np.unique(y)) > 1 else 0.50

    fpr = float(fp / max(1, total_negatives))
    fnr = float(fn / max(1, total_positives))
    false_decline_rate = fpr

    # 95% Confidence Intervals
    cis = bootstrap_metric_confidence_interval(y, scores, y_pred, seed=seed)

    return {
        "primary_metrics": {
            "pr_auc": round(pr_auc, 4),
            "recall_at_01_fpr": round(recall_01_fpr, 4),
            "recall_at_1_fpr": round(recall_1_fpr, 4),
            "recall": round(rec, 4),
            "precision": round(prec, 4),
            "false_negative_rate": round(fnr, 4),
            "false_decline_rate": round(false_decline_rate, 4)
        },
        "secondary_metrics": {
            "roc_auc": round(roc_auc, 4),
            "f1_score": round(f1, 4),
            "accuracy": round(float((tp + tn) / max(1, total_samples)), 4)
        },
        "denominators": {
            "total_samples": total_samples,
            "actual_fraud_count": total_positives,
            "actual_legitimate_count": total_negatives,
            "total_alerts_fired": total_alerts,
            "true_positives": int(tp),
            "false_positives": int(fp),
            "true_negatives": int(tn),
            "false_negatives": int(fn)
        },
        "confidence_intervals_95": cis,
        "provenance_tier": "MEASURED"
    }


evaluate_model_performance = compute_comprehensive_metrics
compute_metrics = compute_comprehensive_metrics
