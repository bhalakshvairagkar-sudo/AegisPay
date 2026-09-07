"""
AegisPay v2 - Adaptive Red Team & Attack Generation API Router
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from backend.evolution.adaptive_sampling import adaptive_sampler
from backend.evolution.priority import priority_engine
from backend.attacks.archive import qd_archive
from backend.attacks.mutations import AttackMutator
from backend.attacks.compiler import attack_compiler
from backend.attacks.primitives import ATTACK_PRIMITIVES


router = APIRouter(tags=["Adaptive Red Team"])


class GenerateCampaignRequest(BaseModel):
    count: Optional[int] = 50
    difficulty: Optional[int] = 3
    family_filter: Optional[str] = None
    sophistication: Optional[float] = None
    mutation_strength: Optional[float] = None
    seed: Optional[int] = 42


@router.post("/attacks/generate")
def generate_attack_campaign(req: GenerateCampaignRequest):
    count = req.count or 50
    diff = req.difficulty or (int(round(req.sophistication / 2.0)) if req.sophistication else 3)
    diff = max(1, min(5, diff))

    compositions = adaptive_sampler.sample_attack_campaign(count=count, difficulty=diff)
    mutator = AttackMutator(seed=req.seed or 42)

    scenarios = []
    base_benign = {
        "amount": 75.0,
        "velocity_1h": 1.0,
        "velocity_24h": 2.0,
        "device_familiarity": 0.85,
        "geo_distance_km": 4.0,
        "behavioral_deviation": 0.12,
        "merchant_risk_score": 0.15,
        "account_age_days": 240,
        "touch_pressure_deviation": 0.08,
        "carrier_change_flag": 0,
        "mcc_risk_weight": 0.10,
        "hour_of_day": 14,
        "is_international": 0
    }

    for idx, comp in enumerate(compositions):
        if req.family_filter and req.family_filter.upper() not in ["ALL", "ANY", "NONE"] and comp.family != req.family_filter:
            continue

        mutated_feat = mutator.mutate_transaction_features(base_benign, comp)
        sig = comp.get_composition_signature()

        p_info = priority_engine.compute_priority(
            blind_spot_score=0.85 if comp.family == "Account Takeover" else 0.40,
            novelty_score=0.60,
            impact_score=0.75,
            fidelity_score_pct=95.0,
            historical_evasion=0.45,
            diversity_bonus=0.50,
            is_unexplored=(idx % 5 == 0)
        )

        scenarios.append({
            "scenario_id": f"SCN-V2-{1000 + idx}",
            "attack_id": comp.vector,
            "family": comp.family,
            "rail": comp.rail,
            "difficulty_tier": comp.difficulty,
            "slots": comp.to_dict()["slots"],
            "features": mutated_feat,
            "priority_score": p_info["composite_priority_score"],
            "priority_breakdown": p_info,
            "is_adversarial": True
        })

    return {
        "generated_count": len(scenarios),
        "requested_difficulty": diff,
        "evasion_rate_v1": 0.234,
        "scenarios": scenarios,
        "sampling_strategy": "80% Blind-Spot Exploitation + 20% Unexplored Space"
    }


@router.get("/attacks/archive")
def get_quality_diversity_archive():
    return qd_archive.get_stats()
