from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any, Dict, Iterable, List

NODE_TYPE_ALIASES = {
    "SourceNode": "source",
    "SourceClaimNode": "source_claim",
    "EvidenceNode": "evidence",
    "InferenceNode": "inference",
    "HypothesisNode": "hypothesis",
    "FalsifierNode": "falsifier",
    "RiskNode": "risk",
    "NarrativeNode": "narrative",
    "AssumptionNode": "assumption",
    "ChangeRequest": "change_request",
}

ALLOWED_NODE_TYPES = {
    "source",
    "source_claim",
    "evidence",
    "inference",
    "hypothesis",
    "falsifier",
    "risk",
    "narrative",
    "assumption",
    "change_request",
}

ALLOWED_TIERS = {"A", "B", "C", "X", "M"}
ALLOWED_DIRECTNESS = {
    "direct",
    "indirect",
    "analogy",
    "circumstantial",
    "model",
    "benchmark",
    "observational",
}
ALLOWED_EDGE_TYPES = {
    "says",
    "extracted_as",
    "supports",
    "refutes",
    "depends_on",
    "falsified_by",
    "has_risk",
    "conflicts_with",
    "paper_conflict",
    "narrative_conflict",
    "frame_conflict",
    "uses_evidence",
    "derived_from",
}


@dataclass
class ValidationResult:
    case_id: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    overclaim_flags: List[str] = field(default_factory=list)
    m_tag_flags: List[str] = field(default_factory=list)
    tier_mismatch_flags: List[str] = field(default_factory=list)
    suggested_fixes: List[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    @property
    def status(self) -> str:
        if self.errors:
            return "REJECT"
        if self.warnings:
            return "PASS_WITH_WARNINGS"
        return "PASS"

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_missing_field(self, field_name: str, *, error: bool = True) -> None:
        if field_name not in self.missing_fields:
            self.missing_fields.append(field_name)
        message = f"missing required field: {field_name}"
        if error:
            self.add_error(message)
        else:
            self.add_warning(message)

    def add_overclaim(self, flag: str, message: str) -> None:
        if flag not in self.overclaim_flags:
            self.overclaim_flags.append(flag)
        self.add_error(message)

    def add_m_tag_flag(self, flag: str, message: str) -> None:
        if flag not in self.m_tag_flags:
            self.m_tag_flags.append(flag)
        self.add_error(message)

    def add_tier_mismatch(self, flag: str, message: str) -> None:
        if flag not in self.tier_mismatch_flags:
            self.tier_mismatch_flags.append(flag)
        self.add_error(message)

    def add_suggested_fix(self, message: str) -> None:
        if message not in self.suggested_fixes:
            self.suggested_fixes.append(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "status": self.status,
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "missing_fields": self.missing_fields,
            "overclaim_flags": self.overclaim_flags,
            "m_tag_flags": self.m_tag_flags,
            "tier_mismatch_flags": self.tier_mismatch_flags,
            "suggested_fixes": self.suggested_fixes,
        }


def load_domain_rules(rules_dir: str | Path) -> Dict[str, Dict[str, Any]]:
    path = Path(rules_dir)
    out: Dict[str, Dict[str, Any]] = {}
    for file in sorted(path.glob("*.json")):
        data = json.loads(file.read_text(encoding="utf-8"))
        out[data["domain"]] = data
    return out


def _text_blob(*items: Any) -> str:
    parts: List[str] = []
    for item in items:
        if isinstance(item, dict):
            for key in (
                "title",
                "description",
                "summary",
                "claim_text",
                "suggested_patch",
                "user_input",
                "reason_for_tier",
                "audit_notes",
                "required_test",
            ):
                value = item.get(key)
                if isinstance(value, str):
                    parts.append(value)
            for value in item.get("falsification_conditions", []) or []:
                if isinstance(value, str):
                    parts.append(value)
        elif isinstance(item, list):
            parts.append(_text_blob(*item))
        elif isinstance(item, str):
            parts.append(item)
    return "\n".join(parts).lower()


def _has_any(text: str, terms: Iterable[str]) -> bool:
    return any(term.lower() in text for term in terms)


def _node_type(node: Dict[str, Any]) -> str | None:
    raw = node.get("node_type")
    return NODE_TYPE_ALIASES.get(raw, raw)


def _node_map(nodes: List[Dict[str, Any]], result: ValidationResult) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for node in nodes:
        node_id = node.get("id")
        if not node_id:
            result.add_error("node missing id")
            continue
        if node_id in index:
            result.add_error(f"duplicate node id: {node_id}")
            continue
        index[node_id] = node
    return index


def _supporting_evidence_for(hypothesis_id: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    evidence_by_id = {n["id"]: n for n in nodes if _node_type(n) == "evidence" and n.get("id")}
    inference_by_id = {n["id"]: n for n in nodes if _node_type(n) == "inference" and n.get("id")}
    evidence: List[Dict[str, Any]] = []
    inference_ids = {
        edge.get("from")
        for edge in edges
        if edge.get("edge_type") == "supports" and edge.get("to") == hypothesis_id and edge.get("from") in inference_by_id
    }
    for edge in edges:
        if edge.get("edge_type") in {"uses_evidence", "depends_on", "supports"} and edge.get("to") in inference_ids:
            src = evidence_by_id.get(edge.get("from"))
            if src:
                evidence.append(src)
    return evidence


def _risks_for(target_id: str, nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [n for n in nodes if n.get("node_type") == "risk" and target_id in (n.get("targets") or [])]


def validate_case(case: Dict[str, Any], domain_rules: Dict[str, Dict[str, Any]] | None = None) -> ValidationResult:
    result = ValidationResult(case_id=case.get("case_id", "<unknown>"))
    nodes = case.get("nodes") or []
    edges = case.get("edges") or []
    rules = (domain_rules or {}).get(case.get("domain"))

    if not isinstance(nodes, list):
        result.add_error("nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        result.add_error("edges must be a list")
        edges = []

    index = _node_map(nodes, result)

    for field_name in (
        "case_id",
        "domain",
        "title",
        "user_input",
        "source_status",
        "directness",
        "reason_for_tier",
        "audit_notes",
    ):
        if not case.get(field_name):
            result.add_missing_field(field_name)

    for field_name in (rules or {}).get("required_case_fields", []):
        if not case.get(field_name):
            result.add_missing_field(field_name)

    if case.get("source_status") in {"sample_unverified", "needs_review", "placeholder"}:
        result.add_warning(f"case source_status is {case.get('source_status')}; citations need expert review")

    node_types_present = {_node_type(node) for node in nodes}
    for node_type in (rules or {}).get("required_node_types", []):
        if node_type not in node_types_present:
            result.add_missing_field(f"node_type:{node_type}")

    for node in nodes:
        node_id = node.get("id", "<missing>")
        node_type = _node_type(node)
        if node_type not in ALLOWED_NODE_TYPES:
            result.add_error(f"{node_id}: invalid node_type {node.get('node_type')!r}")
        if not node.get("title"):
            result.add_error(f"{node_id}: missing title")

        if node_type == "source":
            if not node.get("source_type"):
                result.add_error(f"{node_id}: source missing source_type")
            if not (node.get("doi") or node.get("url") or node.get("citation_text")):
                result.add_error(f"{node_id}: source requires doi, url, or citation_text")
            elif not (node.get("doi") or node.get("url")):
                result.add_warning(f"{node_id}: source has citation_text but no doi/url")

        if node_type == "source_claim":
            source_id = node.get("source_id")
            if not source_id or source_id not in index:
                result.add_error(f"{node_id}: source_claim references missing source_id {source_id!r}")
            elif index[source_id].get("node_type") != "source":
                result.add_error(f"{node_id}: source_id {source_id!r} is not a source node")
            if not node.get("claim_text"):
                result.add_error(f"{node_id}: source_claim missing claim_text")

        if node_type == "evidence":
            if node.get("directness") not in ALLOWED_DIRECTNESS:
                result.add_error(f"{node_id}: evidence invalid directness {node.get('directness')!r}")
            weight = node.get("weight")
            if not isinstance(weight, (int, float)) or not 0 <= weight <= 1:
                result.add_error(f"{node_id}: evidence weight must be a number between 0 and 1")
            source_claim_ids = node.get("source_claim_ids") or []
            if not source_claim_ids:
                result.add_error(f"{node_id}: evidence requires source_claim_ids")
            for claim_id in source_claim_ids:
                if claim_id not in index:
                    result.add_error(f"{node_id}: missing source_claim_id {claim_id!r}")
                elif index[claim_id].get("node_type") != "source_claim":
                    result.add_error(f"{node_id}: {claim_id!r} is not a source_claim")

        if node_type == "hypothesis":
            tier = node.get("tier")
            if tier not in ALLOWED_TIERS:
                result.add_error(f"{node_id}: hypothesis tier must be one of {sorted(ALLOWED_TIERS)}")
            if not node.get("falsification_conditions"):
                result.add_error(f"{node_id}: hypothesis requires at least one falsification condition")
                result.add_suggested_fix(f"{node_id}: add a falsifier or limiting condition")
            if tier in {"A", "B", "C", "X"} and not node.get("reason_for_tier"):
                result.add_error(f"{node_id}: tier or provisional tier requires reason_for_tier")
                result.add_suggested_fix(f"{node_id}: explain why the tier is provisional")

        if node_type == "inference":
            if not node.get("depends_on"):
                result.add_warning(f"{node_id}: inference has no depends_on references")
            if not node.get("source_claim_ids"):
                result.add_warning(f"{node_id}: inference should reference source_claim_ids to preserve separation")

        if node_type == "risk":
            if not node.get("targets"):
                result.add_error(f"{node_id}: risk requires targets")
            if not node.get("suggested_patch"):
                result.add_warning(f"{node_id}: risk should include suggested_patch")

    for edge in edges:
        edge_type = edge.get("edge_type")
        src = edge.get("from")
        dst = edge.get("to")
        if edge_type not in ALLOWED_EDGE_TYPES:
            result.add_error(f"edge {src}->{dst}: invalid edge_type {edge_type!r}")
        if src not in index:
            result.add_error(f"edge references missing from-node {src!r}")
        if dst not in index:
            result.add_error(f"edge references missing to-node {dst!r}")
        strength = edge.get("strength", 1.0)
        if not isinstance(strength, (int, float)) or not 0 <= strength <= 1:
            result.add_error(f"edge {src}->{dst}: strength must be 0..1")
        src_node = index.get(src)
        dst_node = index.get(dst)
        if (
            edge_type == "supports"
            and src_node
            and dst_node
            and _node_type(src_node) == "evidence"
            and _node_type(dst_node) == "hypothesis"
        ):
            result.add_error(
                f"edge {src}->{dst}: evidence cannot directly support hypothesis; add an InferenceNode"
            )
            result.add_suggested_fix("Route support as EvidenceNode -> InferenceNode -> HypothesisNode")

    for h in [n for n in nodes if _node_type(n) == "hypothesis"]:
        h_id = h.get("id")
        has_falsifier_edge = any(
            edge.get("from") == h_id
            and edge.get("edge_type") == "falsified_by"
            and index.get(edge.get("to"))
            and _node_type(index[edge.get("to")]) == "falsifier"
            for edge in edges
        )
        if not has_falsifier_edge and not h.get("limiting_conditions"):
            result.add_error(f"{h_id}: hypothesis requires a linked FalsifierNode or limiting_conditions")
            result.add_suggested_fix(f"{h_id}: link at least one FalsifierNode with falsified_by")

    # Generic A-tier safeguards.
    for h in [n for n in nodes if _node_type(n) == "hypothesis"]:
        if h.get("tier") != "A":
            continue
        h_id = h.get("id")
        supporting = _supporting_evidence_for(h_id, nodes, edges)
        if not supporting:
            result.add_tier_mismatch("a_tier_no_supporting_evidence", f"{h_id}: A-tier hypothesis has no supporting evidence")
            continue
        if all(e.get("m_tag") or e.get("directness") == "analogy" for e in supporting):
            result.add_m_tag_flag("m_tag_only_a_tier", f"{h_id}: A-tier cannot be supported only by M-tag or analogy evidence")
        if not any((not e.get("m_tag")) and e.get("directness") in {"direct", "model", "benchmark"} for e in supporting):
            result.add_tier_mismatch("a_tier_missing_direct_domain_evidence", f"{h_id}: A-tier requires at least one non-M direct/model/benchmark supporting evidence node")
        if any(r.get("severity") in {"high", "critical"} for r in _risks_for(h_id, nodes)):
            result.add_tier_mismatch("a_tier_unresolved_high_risk", f"{h_id}: A-tier hypothesis has unresolved high/critical risk")

    # Domain-specific overclaim patterns and A-tier evidence tags.
    if rules:
        asserted_nodes = [n for n in nodes if _node_type(n) in {"hypothesis", "inference"}]
        asserted_text = _text_blob(case.get("user_input", ""), asserted_nodes)
        risk_tags = set()
        for risk in [n for n in nodes if _node_type(n) == "risk"]:
            risk_tags.update(risk.get("risk_tags") or [])
            if risk.get("risk_type"):
                risk_tags.add(risk["risk_type"])
        for pattern in rules.get("overclaim_patterns", []):
            if _has_any(asserted_text, pattern.get("trigger_terms", [])) and _has_any(asserted_text, pattern.get("overclaim_terms", [])):
                if pattern["id"] not in risk_tags:
                    result.add_overclaim(pattern["id"], f"domain overclaim pattern missing RiskNode: {pattern['id']}")
                    result.add_suggested_fix(f"Add a RiskNode tagged {pattern['id']}")
                strong_assertion = case.get("case_type") == "overclaim" or any(
                    n.get("tier") == "A" for n in asserted_nodes if _node_type(n) == "hypothesis"
                )
                if pattern.get("reject_when_asserted", False) and strong_assertion:
                    result.add_overclaim(pattern["id"], f"domain overclaim asserted: {pattern['id']}")

        evidence_by_id = {n.get("id"): n for n in nodes if _node_type(n) == "evidence"}
        for h in [n for n in nodes if _node_type(n) == "hypothesis"]:
            h_id = h.get("id")
            h_text = _text_blob(h, [n for n in nodes if _node_type(n) == "inference" and any(e.get("from") == n.get("id") and e.get("to") == h_id for e in edges)])
            supporting = _supporting_evidence_for(h_id, nodes, edges)
            supporting_tags = set()
            for evidence in supporting:
                supporting_tags.update(evidence.get("evidence_tags") or [])
                if evidence.get("m_tag"):
                    supporting_tags.add("m_tag")
                if evidence.get("evidence_type"):
                    supporting_tags.add(evidence["evidence_type"])
            for pattern in rules.get("forbidden_support_patterns", []):
                evidence_match = bool(supporting_tags.intersection(pattern.get("evidence_tags_any", [])))
                claim_match = _has_any(h_text, pattern.get("claim_terms_any", []))
                allowed_tags = set(pattern.get("allowed_evidence_tags_any", []))
                allowed_match = bool(supporting_tags.intersection(allowed_tags)) if allowed_tags else False
                strong_assertion = case.get("case_type") == "overclaim" or h.get("tier") == "A"
                if evidence_match and claim_match and not allowed_match and strong_assertion:
                    result.add_overclaim(pattern["id"], f"{h_id}: {pattern.get('message', pattern['id'])}")
                    result.add_suggested_fix(pattern.get("suggested_fix", f"Reduce scope or add evidence for {pattern['id']}"))

            for requirement in rules.get("required_metadata_when_claim_terms", []):
                if not _has_any(h_text, requirement.get("claim_terms_any", [])):
                    continue
                if requirement.get("strong_assertion_only") and not (case.get("case_type") == "overclaim" or h.get("tier") == "A"):
                    continue
                for field_name in requirement.get("required_fields", []):
                    if not _metadata_present(field_name, h, supporting, case):
                        result.add_missing_field(f"{h_id}:{field_name}")

        required_tags = set(rules.get("a_tier_requires_any_evidence_tag") or [])
        if required_tags:
            for h in [n for n in nodes if _node_type(n) == "hypothesis" and n.get("tier") == "A"]:
                supporting = _supporting_evidence_for(h.get("id"), nodes, edges)
                evidence_tags = set()
                for e in supporting:
                    evidence_tags.update(e.get("evidence_tags") or [])
                if not evidence_tags.intersection(required_tags):
                    result.add_tier_mismatch(
                        "a_tier_missing_domain_evidence_tag",
                        f"{h.get('id')}: A-tier lacks required domain evidence tags: {sorted(required_tags)}"
                    )
    else:
        result.add_warning(f"no domain rules found for domain {case.get('domain')!r}")

    return result


def _metadata_present(field_name: str, hypothesis: Dict[str, Any], supporting: List[Dict[str, Any]], case: Dict[str, Any]) -> bool:
    if case.get(field_name) or hypothesis.get(field_name):
        return True
    return any(evidence.get(field_name) for evidence in supporting)
