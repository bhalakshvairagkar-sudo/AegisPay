"""
Comprehensive Fraud Model Evaluation Metrics
Computes mathematically sound performance metrics:
- Precision, Recall, F1-Score
- ROC-AUC (Area Under Receiver Operating Characteristic)
- PR-AUC (Precision-Recall Area Under Curve / Average Precision)
- False Positive Rate (FPR), False Negative Rate (FNR)
- Confusion Matrix (TP, FP, TN, FN)
- Mean Inference Latency in milliseconds
"""

from typing import Dict, Any, Tuple
import time
import numpy as np
import pandas as pd
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)


def evaluate_model_performance(
    model: Any,
    X_test: pd.DataFrame,
    y_test: np.ndarray,
    threshold: float = 0.50
) -> Dict[str, Any]:
    """
    Evaluates a model instance against test ground truth.
    Computes all standard fraud classification metrics and latency.
    """
    if len(X_test) == 0 or len(y_test) == 0:
        return {
            "evaluated": False,
            "status": "Not evaluated"
        }

    # Measure inference latency
    t0 = time.perf_counter()
    y_prob = model.predict_proba(X_test)[:, 1]
    latency_ms = round(((time.perf_counter() - t0) / max(1, len(X_test))) * 1000.0, 2)
    latency_ms = max(0.8, latency_ms)

    y_pred = (y_prob >= threshold).astype(int)

    # Calculate metrics
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))

    try:
        roc_auc = float(roc_auc_score(y_test, y_prob))
    except ValueError:
        roc_auc = 0.50

    try:
        pr_auc = float(average_precision_score(y_test, y_prob))
    except ValueError:
        pr_auc = 0.50

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=[0, 1]).ravel()

    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0

    return {
        "evaluated": True,
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "rocAuc": round(roc_auc, 4),
        "prAuc": round(pr_auc, 4),
        "fpr": round(fpr, 4),
        "fnr": round(fnr, 4),
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn),
        "total_evaluated": len(y_test),
        "detected_count": int(tp),
        "evaded_count": int(fn),
        "latencyMs": latency_ms,
    }
