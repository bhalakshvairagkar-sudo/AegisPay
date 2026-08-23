"""
Attack Taxonomy & Threat Knowledge Graph Endpoints
"""

from fastapi import APIRouter, Query
from typing import Optional
from backend.attacks.taxonomy import taxonomy_instance

router = APIRouter(prefix="/attacks", tags=["Taxonomy"])


@router.get("/taxonomy")
def get_taxonomy(family: Optional[str] = Query(default="ALL")):
    attacks = taxonomy_instance.get_by_family(family)
    return {
        "total_vectors": len(taxonomy_instance.get_all()),
        "filtered_count": len(attacks),
        "families": taxonomy_instance.get_families(),
        "attacks": [a.to_dict() for a in attacks]
    }


@router.get("/graph")
def get_knowledge_graph():
    return taxonomy_instance.get_knowledge_graph()
