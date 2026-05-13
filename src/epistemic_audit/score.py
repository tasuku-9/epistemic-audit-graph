from __future__ import annotations

from typing import Any, Dict, List

TIER_ORDER = {"A": 4, "B": 3, "C": 2, "X": 1}


def provisional_score(case: Dict[str, Any], hypothesis_id: str) -> Dict[str, Any]:
    """Return a transparent toy score breakdown.

    This is intentionally simple. Do not present it as a truth score.
    It exists only to demonstrate how a future dependency engine can expose
    score components.
    """
    nodes = case.get("nodes", [])
    edges = case.get("edges", [])
    by_id = {n.get("id"): n for n in nodes}
    direct_support = 0.0
    refutation = 0.0
    risk_penalty = 0.0
    analogy_penalty = 0.0

    for edge in edges:
        if edge.get("to") != hypothesis_id:
            continue
        src = by_id.get(edge.get("from"))
        if not src:
            continue
        strength = float(edge.get("strength", 1.0))
        if edge.get("edge_type") == "supports" and src.get("node_type") == "evidence":
            contribution = float(src.get("weight", 0)) * strength
            direct_support += contribution
            if src.get("m_tag") or src.get("directness") == "analogy":
                analogy_penalty += contribution * 0.5
        if edge.get("edge_type") == "refutes" and src.get("node_type") == "evidence":
            refutation += float(src.get("weight", 0)) * strength

    for risk in nodes:
        if risk.get("node_type") == "risk" and hypothesis_id in (risk.get("targets") or []):
            severity = risk.get("severity", "medium")
            risk_penalty += {"low": 0.05, "medium": 0.1, "high": 0.2, "critical": 0.35}.get(severity, 0.1)

    raw = direct_support - refutation - risk_penalty - analogy_penalty
    score = max(0.0, min(1.0, raw))
    return {
        "hypothesis_id": hypothesis_id,
        "score": round(score, 3),
        "components": {
            "direct_support": round(direct_support, 3),
            "refutation": round(refutation, 3),
            "risk_penalty": round(risk_penalty, 3),
            "analogy_penalty": round(analogy_penalty, 3),
        },
        "warning": "Provisional audit score only; not a truth score.",
    }
