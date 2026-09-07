"""
AegisPay v2 - Attack Taxonomy, Grammar & Explorer API Router
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from backend.attacks.primitives import ATTACK_PRIMITIVES
from backend.attacks.grammar import (
    AttackComposition,
    ACCESS_MECHANISMS,
    TRUST_MECHANISMS,
    PAYMENT_RAILS,
    EVASION_MECHANISMS,
    BEHAVIORAL_PATTERNS,
    MONETIZATION_PATHWAYS,
    TEMPORAL_PATTERNS
)
from backend.attacks.compatibility import compatibility_validator
from backend.attacks.compiler import attack_compiler
from backend.attacks.explorer import attack_explorer


router = APIRouter(tags=["Attack Intelligence"])


class ValidateCompositionRequest(BaseModel):
    access: str
    trust: str
    rail: str
    evasion: str
    behavior: str
    monetization: str
    temporal_pattern: str
    family: Optional[str] = "Account Takeover"
    vector: Optional[str] = "CUSTOM-01"
    difficulty: Optional[int] = 1


@router.get("/attacks/taxonomy")
def get_attack_taxonomy():
    prims = [
        {
            "primitive_id": p.primitive_id,
            "family": p.family,
            "name": p.name,
            "default_slots": {
                "access": p.default_access,
                "trust": p.default_trust,
                "rail": p.default_rail,
                "evasion": p.default_evasion,
                "behavior": p.default_behavior,
                "monetization": p.default_monetization,
                "temporal_pattern": p.default_temporal
            },
            "observable_signals": p.observable_signals,
            "mitigation_policy": p.mitigation_policy,
            "description": p.description
        }
        for p in ATTACK_PRIMITIVES.values()
    ]
    families = sorted(list(set(p["family"] for p in prims)))

    attacks = [
        {
            "id": p.primitive_id,
            "family": p.family,
            "name": p.name,
            "genAi": True if "AI" in p.family or "Biometric" in p.name or "GAN" in p.description else False,
            "sophistication": 7.5,
            "severity": "CRITICAL" if p.family in ["Account Takeover", "AI Adaptive Fraud"] else "HIGH",
            "detectability": "LOW" if p.family in ["Behavioral Impersonation", "AI Adaptive Fraud"] else "MEDIUM",
            "evasionStrategy": p.description,
            "signals": p.observable_signals,
            "description": p.description,
            "mitigationPolicy": p.mitigation_policy
        }
        for p in ATTACK_PRIMITIVES.values()
    ]

    return {
        "total_vectors": len(prims),
        "primitives_count": len(prims),
        "families_count": len(families),
        "families": families,
        "primitives": prims,
        "attacks": attacks,
        "grammar_vocabularies": {
            "access_mechanisms": ACCESS_MECHANISMS,
            "trust_mechanisms": TRUST_MECHANISMS,
            "payment_rails": PAYMENT_RAILS,
            "evasion_mechanisms": EVASION_MECHANISMS,
            "behavioral_patterns": BEHAVIORAL_PATTERNS,
            "monetization_pathways": MONETIZATION_PATHWAYS,
            "temporal_patterns": TEMPORAL_PATTERNS
        }
    }


@router.get("/attacks/graph")
def get_attack_graph():
    nodes = []
    edges = []
    families = sorted(list(set(p.family for p in ATTACK_PRIMITIVES.values())))
    for fam in families:
        nodes.append({"id": fam, "label": fam, "type": "family"})
    for p in ATTACK_PRIMITIVES.values():
        nodes.append({"id": p.primitive_id, "label": p.name, "type": "vector", "family": p.family})
        edges.append({"source": p.family, "target": p.primitive_id, "relation": "contains"})
    return {"nodes": nodes, "edges": edges}


@router.get("/attacks/explorer")
def get_attack_space_explorer():
    return attack_explorer.compute_combinatorial_metrics()


@router.post("/attacks/validate")
def validate_attack_composition(req: ValidateCompositionRequest):
    comp = AttackComposition(
        access=req.access,
        trust=req.trust,
        rail=req.rail,
        evasion=req.evasion,
        behavior=req.behavior,
        monetization=req.monetization,
        temporal_pattern=req.temporal_pattern,
        family=req.family or "Custom",
        vector=req.vector or "CUSTOM-01",
        difficulty=req.difficulty or 1
    )
    val_res = compatibility_validator.validate(comp)
    return {
        "composition_signature": comp.get_composition_signature(),
        "is_type_valid": val_res.is_type_valid,
        "is_semantic_valid": val_res.is_semantic_valid,
        "is_executable": val_res.is_executable,
        "compatibility_score": val_res.compatibility_score,
        "rejection_reasons": val_res.diagnostic_rejection_reasons
    }


@router.post("/attacks/compile")
def compile_attack_composition(req: ValidateCompositionRequest):
    comp = AttackComposition(
        access=req.access,
        trust=req.trust,
        rail=req.rail,
        evasion=req.evasion,
        behavior=req.behavior,
        monetization=req.monetization,
        temporal_pattern=req.temporal_pattern,
        family=req.family or "Custom",
        vector=req.vector or "CUSTOM-01",
        difficulty=req.difficulty or 1
    )
    scenario, val_res = attack_compiler.compile(comp)
    if not scenario:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "COMPILATION_REJECTED",
                "reasons": val_res.diagnostic_rejection_reasons
            }
        )

    # Log execution in explorer
    attack_explorer.record_execution(comp)

    return {
        "scenario_id": scenario.scenario_id,
        "target_rail": scenario.target_rail,
        "difficulty_level": scenario.difficulty_level,
        "feature_perturbation_spec": scenario.feature_perturbation_spec,
        "composition": comp.to_dict()
    }
