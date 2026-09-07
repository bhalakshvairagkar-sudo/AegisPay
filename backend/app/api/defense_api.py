"""
AegisPay v2 - Calibration, Cost Matrix & Reason Codes API Router
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import numpy as np

from backend.models.calibration import calibration_engine
from backend.defense.cost_model import cost_engine, CostParameters
from backend.defense.reason_codes import REASON_CODES


router = APIRouter(tags=["Defense Lab & Policies"])


class CostEvaluationRequest(BaseModel):
    false_negative_multiplier: Optional[float] = 1.0
    false_positive_fixed: Optional[float] = 15.0
    manual_review_fixed: Optional[float] = 8.5
    friction_fixed: Optional[float] = 3.2


@router.get("/defense/calibration")
def get_calibration_metrics():
    # Evaluate calibration curve on sample scores
    np.random.seed(42)
    raw_s = np.random.uniform(0.05, 0.95, 200)
    y_s = (raw_s > 0.45).astype(int)
    return calibration_engine.evaluate_calibration(raw_s, y_s)


@router.get("/defense/reason-codes")
def get_reason_codes_catalog():
    return [
        {
            "code": rc.code,
            "short_name": rc.short_name,
            "category": rc.category,
            "operational_action": rc.operational_action,
            "description": rc.description
        }
        for rc in REASON_CODES.values()
    ]


@router.post("/defense/cost")
def evaluate_policy_cost(req: CostEvaluationRequest):
    p = CostParameters(
        cost_false_negative_multiplier=req.false_negative_multiplier or 1.0,
        cost_false_positive_fixed=req.false_positive_fixed or 15.0,
        cost_manual_review_fixed=req.manual_review_fixed or 8.5,
        cost_friction_abandonment_fixed=req.friction_fixed or 3.2
    )
    temp_engine = cost_engine.__class__(params=p)

    # Sample evaluation on 300 test transactions
    np.random.seed(42)
    y_test = np.random.binomial(1, 0.25, 300)
    actions = []
    amts = np.random.lognormal(4.0, 1.0, 300)
    for y in y_test:
        if y == 1:
            actions.append("BLOCK" if np.random.rand() > 0.08 else "ALLOW")
        else:
            actions.append("ALLOW" if np.random.rand() > 0.02 else "FRICTION")

    return temp_engine.compute_expected_loss(y_test, actions, amts)
