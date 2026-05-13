from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sample_cases"


def source(id: str, title: str, source_type: str = "paper") -> dict:
    return {
        "id": id,
        "node_type": "source",
        "title": title,
        "source_type": source_type,
        "citation_text": f"Sample source packet for {title}; replace with reviewed citation before real use.",
    }


def sc(id: str, source_id: str, title: str, claim_text: str) -> dict:
    return {
        "id": id,
        "node_type": "source_claim",
        "title": title,
        "source_id": source_id,
        "claim_text": claim_text,
        "quote_or_locator": "sample locator; verification needed",
    }


def ev(
    id: str,
    title: str,
    evidence_type: str,
    directness: str,
    weight: float,
    source_claim_ids: list[str],
    evidence_tags: list[str],
    tier: str = "A",
    m_tag: bool = False,
    **extra,
) -> dict:
    node = {
        "id": id,
        "node_type": "evidence",
        "title": title,
        "evidence_type": evidence_type,
        "directness": directness,
        "weight": weight,
        "source_claim_ids": source_claim_ids,
        "evidence_tags": evidence_tags,
        "tier": tier,
        "m_tag": m_tag,
    }
    node.update(extra)
    return node


def inf(
    id: str,
    title: str,
    description: str,
    depends_on: list[str],
    source_claim_ids: list[str],
    tier: str = "B",
    **extra,
) -> dict:
    node = {
        "id": id,
        "node_type": "inference",
        "title": title,
        "description": description,
        "depends_on": depends_on,
        "source_claim_ids": source_claim_ids,
        "tier": tier,
    }
    node.update(extra)
    return node


def hyp(
    id: str,
    title: str,
    description: str,
    tier: str,
    falsification_conditions: list[str],
    reason_for_tier: str,
    **extra,
) -> dict:
    node = {
        "id": id,
        "node_type": "hypothesis",
        "title": title,
        "description": description,
        "tier": tier,
        "provisional_tier": tier,
        "reason_for_tier": reason_for_tier,
        "falsification_conditions": falsification_conditions,
    }
    node.update(extra)
    return node


def risk(
    id: str,
    title: str,
    risk_type: str,
    targets: list[str],
    severity: str = "medium",
    suggested_patch: str = "Reduce scope and separate source claim, evidence, inference, and hypothesis.",
    tier: str = "C",
    tags: list[str] | None = None,
) -> dict:
    return {
        "id": id,
        "node_type": "risk",
        "title": title,
        "risk_type": risk_type,
        "risk_tags": tags or [risk_type],
        "targets": targets,
        "severity": severity,
        "tier": tier,
        "suggested_patch": suggested_patch,
    }


def falsifier(id: str, title: str, targets: list[str], required_test: str) -> dict:
    return {
        "id": id,
        "node_type": "falsifier",
        "title": title,
        "would_weaken": targets,
        "required_test": required_test,
    }


def narrative(id: str, title: str, narrative_type: str, description: str) -> dict:
    return {
        "id": id,
        "node_type": "narrative",
        "title": title,
        "narrative_type": narrative_type,
        "description": description,
    }


def edge(frm: str, to: str, edge_type: str, strength: float = 1.0, note: str = "") -> dict:
    item = {"from": frm, "to": to, "edge_type": edge_type, "strength": strength}
    if note:
        item["note"] = note
    return item


def base_case(
    case_id: str,
    domain: str,
    case_type: str,
    title: str,
    japanese_title: str,
    summary: str,
    user_input: str,
    expected: str,
    key_warning_theme: str,
    tier: str,
    reason: str,
    notes: str,
    directness: str = "scoped",
) -> dict:
    return {
        "case_id": case_id,
        "domain": domain,
        "case_type": case_type,
        "title": title,
        "japanese_title": japanese_title,
        "summary": summary,
        "user_input": user_input,
        "validator_expected_result": expected,
        "validator_expected_warnings": ["sample sources require expert review"] if expected != "REJECT" else [],
        "expected_validation": {"status": expected},
        "source_status": "sample_unverified",
        "directness": directness,
        "tier": tier,
        "provisional_tier": tier,
        "reason_for_tier": reason,
        "audit_notes": notes,
        "key_warning_theme": key_warning_theme,
        "nodes": [],
        "edges": [],
    }


def add_indexes(case: dict) -> dict:
    groups = {
        "hypotheses": "hypothesis",
        "source_claims": "source_claim",
        "evidence_nodes": "evidence",
        "inference_nodes": "inference",
        "risk_nodes": "risk",
        "falsifier_nodes": "falsifier",
        "narrative_nodes": "narrative",
    }
    for key, node_type in groups.items():
        case[key] = [
            {k: n[k] for k in ("id", "title", "tier", "claim_text", "description", "risk_type", "directness") if k in n}
            for n in case["nodes"]
            if n.get("node_type") == node_type
        ]
    return case


def write_case(path: str, case: dict) -> None:
    if case.get("case_type") == "overclaim" and not any(n.get("node_type") == "falsifier" for n in case["nodes"]):
        targets = [n["id"] for n in case["nodes"] if n.get("node_type") == "hypothesis"]
        case["nodes"].append(
            falsifier(
                "f_missing_required",
                "Required falsifier was not linked to the asserted claim",
                targets,
                "A valid strong claim would need a concrete contrary observation, limiting condition, or test.",
            )
        )
    add_indexes(case)
    full = SAMPLE / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(json.dumps(case, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preserve_legacy() -> None:
    legacy_dir = ROOT / "data" / "legacy_cases" / "history_humanities"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    old_v2 = SAMPLE / "history_humanities" / "v2_converted.json"
    if old_v2.exists():
        (legacy_dir / "v2_converted.json").write_text(old_v2.read_text(encoding="utf-8"), encoding="utf-8")

    html = ROOT / "demos" / "ancient_history" / "hypothesis_credibility_v2.html"
    legacy_html = ROOT / "demos" / "ancient_history" / "legacy_hypothesis_credibility_v2.html"
    if html.exists() and not legacy_html.exists():
        html.rename(legacy_html)


def clean_public_cases() -> None:
    for path in SAMPLE.glob("*/*.json"):
        path.unlink()
    for directory in list(SAMPLE.glob("*")):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()


def history_cases() -> None:
    c = base_case(
        "history_humanities_good_egm_jomon_dotaku_kiki_scoped",
        "history_humanities",
        "good",
        "Auditing an abductive cross-domain historical hypothesis",
        "分野横断型の歴史仮説を監査する",
        "A scoped EGM-style Jomon / Dotaku / Kiki case that keeps observations, inferences, risks, falsifiers, and narrative conflicts separate.",
        "現代日本人における縄文系父系D-M55の残存、弥生後期の銅鐸祭祀の終焉、記紀神話に見られる降臨・国譲り・農耕起源構造は、後期弥生から古墳初期にかけての社会再編を検討するための分野横断的な作業仮説として扱えるかもしれない。",
        "PASS_WITH_WARNINGS",
        "Cross-domain abductive hypothesis; myth and genetics are not direct proof.",
        "B",
        "The central hypothesis is framed as a working cross-domain hypothesis. Observations are A-level, inferences are B-level, vulnerabilities are C-level, and explicit overclaim paths are X-level risks.",
        "Main public history/humanities demo. Legacy stronger HTML remains only as stress-test/UI reference.",
        "abductive_cross_domain",
    )
    c["nodes"] = [
        source("src_genetics", "Japanese paternal-lineage population genetics packet", "dataset_or_paper"),
        source("src_dotaku", "Late Yayoi Dotaku ritual archaeology packet", "archaeology_report"),
        source("src_kiki", "Kojiki / Nihon Shoki mythic structure packet", "primary_text"),
        sc("sc_d_m55", "src_genetics", "D-M55 persistence observation", "Sources report persistence of D1a2a / D-M55 in modern Japanese paternal lineages."),
        sc("sc_dotaku", "src_dotaku", "Dotaku ritual discontinuity observation", "Archaeological syntheses describe discontinuity or termination in Dotaku ritual practice around the Late Yayoi to early Kofun transition."),
        sc("sc_kiki", "src_kiki", "Kiki mythic complex observation", "Kiki mythic complexes include descent, transfer of land, and agricultural-origin motifs."),
        hyp("h_social_reorganization", "D-M55, Dotaku discontinuity, and Kiki structures may be compared as traces of social reorganization", "Jomon-associated paternal-lineage persistence, Dotaku ritual discontinuity, and Kiki mythic structures may be examined as potentially connected traces of Late Yayoi to early Kofun social reorganization.", "B", ["Kofun elite ancient DNA does not show elevated D-M55.", "Dotaku discontinuity can be fully explained by internal ritual chronology.", "Kiki motifs can be fully explained by broader myth typology."], "Cross-domain connection is plausible enough to audit but not proven; it needs ancient DNA, chronology, text-critical, and narrative tests."),
        ev("e_d_m55", "D1a2a / D-M55 persistence in Japanese paternal lineages", "archaeogenetic_observation", "indirect", 0.68, ["sc_d_m55"], ["modern_y_dna", "paternal_lineage"], tier="A"),
        ev("e_dotaku", "Dotaku ritual discontinuity", "ritual_archaeology", "indirect", 0.66, ["sc_dotaku"], ["ritual_discontinuity", "dated_artifact"], tier="A"),
        ev("e_kiki", "Kiki descent, land-transfer, and agricultural-origin motifs", "primary_text_motif", "analogy", 0.38, ["sc_kiki"], ["mythic_text", "primary_text_with_context"], tier="A", m_tag=True),
        inf("i_paternal_asymmetry", "Paternal asymmetry as possible social signal", "D-M55 persistence may be audited as a possible social signal, not as proof of conquest.", ["e_d_m55"], ["sc_d_m55"], tier="B"),
        inf("i_dotaku_reorganization", "Dotaku discontinuity as possible social reorganization", "Dotaku discontinuity may indicate ritual or political reorganization, while internal chronology remains a live alternative.", ["e_dotaku"], ["sc_dotaku"], tier="B"),
        inf("i_kiki_memory", "Kiki structures as possible ritual-political memory", "Kiki structures may preserve or rework ritual-political memory, but myth-to-history correspondence is not direct evidence.", ["e_kiki"], ["sc_kiki"], tier="B"),
        risk("r_social_advantage", "Social advantage mechanism is not directly proven", "social_mechanism_unproven", ["h_social_reorganization"], "medium", "State the mechanism as a research question and require direct burial, kinship, or elite-context tests.", "C"),
        risk("r_dotaku_internal", "Dotaku discontinuity may have internal chronology explanations", "internal_chronology_alternative", ["h_social_reorganization"], "medium", "Keep internal ritual transformation as an explicit competing explanation.", "C"),
        risk("r_myth_direct", "Myth-to-history correspondence is not direct evidence", "myth_as_direct_history", ["h_social_reorganization"], "high", "Use Kiki motifs as narrative evidence only, not direct event record.", "X", ["myth_as_direct_history", "m_tag_as_direct_history"]),
        risk("r_continental_bridge", "Continental event bridge remains speculative", "continental_event_bridge_speculative", ["h_social_reorganization"], "medium", "Require an explicit bridge source before connecting continental events to the Japanese case.", "C"),
        risk("r_y_dna_conquest", "X-risk: Y-DNA proves conquest", "y_dna_proves_conquest", ["h_social_reorganization"], "high", "Never let modern paternal-lineage frequency prove conquest without independent ancient and archaeological evidence.", "X"),
        risk("r_comparative_proof", "X-risk: comparative examples prove the Japanese case", "comparative_examples_prove_case", ["h_social_reorganization"], "high", "Treat comparisons as heuristic analogy only.", "X"),
        risk("r_dotaku_immigrant", "X-risk: Dotaku sphere was definitively an immigrant group", "dotaku_definitive_immigrant_group", ["h_social_reorganization"], "high", "Keep Dotaku social identity open unless supported by direct evidence.", "X"),
        falsifier("f_elite_dna", "Kofun elite ancient DNA lacks elevated D-M55", ["h_social_reorganization"], "Compare securely contextualized elite Kofun male lineages against the predicted paternal-lineage pattern."),
        falsifier("f_dotaku_chronology", "Dotaku discontinuity fully explained by internal ritual chronology", ["h_social_reorganization"], "Show a complete local chronology that explains discontinuity without broader social reorganization."),
        falsifier("f_myth_typology", "Kiki motifs fully explained by broader myth typology", ["h_social_reorganization"], "Demonstrate that descent, land transfer, and agricultural motifs follow widespread mythic typology without local historical signal."),
        narrative("n_passive_survival", "Passive Jomon survival narrative", "popular_or_textbook_frame", "Jomon-associated lineages are treated as passive survivals rather than active social signals."),
        narrative("n_internal_dotaku", "Internal Dotaku transformation narrative", "archaeological_frame", "Dotaku change is explained internally without broader political reorganization."),
        narrative("n_kiki_legitimation_only", "Kiki as royal legitimation only", "interpretive_frame", "Kiki structures are read only as later royal legitimation, not as possible transformed memory."),
    ]
    c["edges"] = [
        edge("src_genetics", "sc_d_m55", "says"),
        edge("src_dotaku", "sc_dotaku", "says"),
        edge("src_kiki", "sc_kiki", "says"),
        edge("sc_d_m55", "e_d_m55", "extracted_as"),
        edge("sc_dotaku", "e_dotaku", "extracted_as"),
        edge("sc_kiki", "e_kiki", "extracted_as"),
        edge("e_d_m55", "i_paternal_asymmetry", "supports", 0.65),
        edge("e_dotaku", "i_dotaku_reorganization", "supports", 0.62),
        edge("e_kiki", "i_kiki_memory", "supports", 0.32),
        edge("i_paternal_asymmetry", "h_social_reorganization", "supports", 0.48),
        edge("i_dotaku_reorganization", "h_social_reorganization", "supports", 0.46),
        edge("i_kiki_memory", "h_social_reorganization", "supports", 0.28),
    ]
    for node_id in ["r_social_advantage", "r_dotaku_internal", "r_myth_direct", "r_continental_bridge", "r_y_dna_conquest", "r_comparative_proof", "r_dotaku_immigrant"]:
        c["edges"].append(edge("h_social_reorganization", node_id, "has_risk"))
    for node_id in ["f_elite_dna", "f_dotaku_chronology", "f_myth_typology"]:
        c["edges"].append(edge("h_social_reorganization", node_id, "falsified_by"))
    for node_id in ["n_passive_survival", "n_internal_dotaku", "n_kiki_legitimation_only"]:
        c["edges"].append(edge("h_social_reorganization", node_id, "narrative_conflict", 0.7))
    write_case("history_humanities/good_egm_jomon_dotaku_kiki_scoped.json", c)

    c = base_case(
        "history_humanities_overclaim_egm_jomon_dotaku_kiki_rejected",
        "history_humanities",
        "overclaim",
        "Rejected overclaim: Y-DNA, Dotaku, and Kiki as direct conquest proof",
        "父系・銅鐸・記紀を直接征服証明にする過剰主張を拒否",
        "An intentionally rejected version of the Jomon / Dotaku / Kiki case.",
        "D-M55が残っているので縄文系男性が弥生人を征服したことは確実であり、銅鐸の終焉と記紀神話はその歴史事件を直接記録している。",
        "REJECT",
        "Y-DNA frequency, ritual discontinuity, and mythic text are treated as direct proof.",
        "A",
        "Rejected because A-tier certainty is asserted from indirect and M-tag evidence without adequate falsifiers.",
        "This is the public overclaim contrast for the scoped EGM history case.",
        "overclaimed",
    )
    c["nodes"] = [
        source("src_packet", "Jomon / Dotaku / Kiki mixed packet", "mixed_sources"),
        sc("sc_d_m55", "src_packet", "D-M55 persistence observation", "Sources report persistence of D-M55 in Japanese paternal lineages."),
        sc("sc_dotaku", "src_packet", "Dotaku discontinuity observation", "Sources describe discontinuity in Dotaku ritual practice."),
        sc("sc_kiki", "src_packet", "Kiki mythic motifs", "Kiki mythic texts include descent, land-transfer, and agricultural-origin motifs."),
        hyp("h_conquest_certainty", "D-M55 proves Jomon males conquered Yayoi and Kiki directly records it", "D-M55 proves conquest, Dotaku discontinuity proves the same single event, and Kiki mythology directly records that historical event.", "A", [], "Rejected: Y-DNA frequency, ritual discontinuity, and mythic analogy cannot support A-tier historical certainty."),
        ev("e_d_m55", "D-M55 frequency", "archaeogenetic_observation", "direct", 0.82, ["sc_d_m55"], ["modern_y_dna", "paternal_lineage"], tier="A"),
        ev("e_dotaku", "Dotaku discontinuity", "ritual_archaeology", "indirect", 0.78, ["sc_dotaku"], ["ritual_discontinuity"], tier="A"),
        ev("e_kiki", "Kiki mythic motifs", "primary_text_motif", "analogy", 0.92, ["sc_kiki"], ["mythic_text", "primary_text_with_context"], tier="M", m_tag=True),
        inf("i_overclaim", "Collapsed conquest inference", "D-M55, Dotaku discontinuity, and Kiki mythology are treated as direct proof that a conquest certainly happened and was directly recorded.", ["e_d_m55", "e_dotaku", "e_kiki"], ["sc_d_m55", "sc_dotaku", "sc_kiki"], tier="X"),
        risk("r_y_dna", "Y-DNA proves conquest", "y_dna_proves_conquest", ["h_conquest_certainty"], "high", "Reframe paternal lineage as a possible social signal only.", "X"),
        risk("r_myth", "Myth treated as direct historical record", "myth_as_direct_history", ["h_conquest_certainty"], "high", "Treat mythic structure as narrative material, not direct event record.", "X"),
        risk("r_ritual", "Ritual discontinuity treated as single-cause proof", "ritual_discontinuity_single_cause", ["h_conquest_certainty"], "high", "Add internal chronology and multi-causal alternatives.", "X"),
        narrative("n_passive_survival", "Passive Jomon survival narrative", "popular_or_textbook_frame", "The rejected claim also fails to distinguish narrative conflict from proof."),
    ]
    c["edges"] = [
        edge("src_packet", "sc_d_m55", "says"),
        edge("src_packet", "sc_dotaku", "says"),
        edge("src_packet", "sc_kiki", "says"),
        edge("sc_d_m55", "e_d_m55", "extracted_as"),
        edge("sc_dotaku", "e_dotaku", "extracted_as"),
        edge("sc_kiki", "e_kiki", "extracted_as"),
        edge("e_d_m55", "i_overclaim", "supports", 0.9),
        edge("e_dotaku", "i_overclaim", "supports", 0.85),
        edge("e_kiki", "i_overclaim", "supports", 0.95),
        edge("i_overclaim", "h_conquest_certainty", "supports", 0.95),
        edge("h_conquest_certainty", "r_y_dna", "has_risk"),
        edge("h_conquest_certainty", "r_myth", "has_risk"),
        edge("h_conquest_certainty", "r_ritual", "has_risk"),
        edge("h_conquest_certainty", "n_passive_survival", "narrative_conflict", 0.5),
    ]
    write_case("history_humanities/overclaim_egm_jomon_dotaku_kiki_rejected.json", c)


def two_case_domain(
    domain: str,
    good_file: str,
    over_file: str,
    good: dict,
    over: dict,
) -> None:
    write_case(f"{domain}/{good_file}", good)
    write_case(f"{domain}/{over_file}", over)


def biomedicine_cases() -> None:
    c = base_case("biomedicine_good_mouse_model_scoped", "biomedicine", "good", "From mouse model to human clinical claim", "マウス実験からヒト治療効果への飛躍を検出", "Mouse evidence is kept at preclinical candidate scope.", "Compound X reduced tumor size in a mouse model under specified experimental conditions. This may justify further investigation as a therapeutic candidate, but it does not yet establish human clinical efficacy.", "PASS_WITH_WARNINGS", "Animal-to-human extrapolation warning.", "B", "Preclinical result supports further investigation, not clinical efficacy.", "No patient advice or clinical recommendation is made.", "preclinical")
    c.update({"organism": "mouse", "endpoint": "tumor size", "intervention_condition": "Compound X under specified experimental conditions"})
    c["nodes"] = [
        source("src_mouse", "Mouse tumor model experiment"),
        sc("sc_mouse", "src_mouse", "Mouse tumor reduction", "Compound X reduced tumor size in a mouse model under specified experimental conditions."),
        hyp("h_candidate", "Compound X may be a preclinical therapeutic candidate", "The mouse result may justify further investigation as a therapeutic candidate, but does not establish human clinical efficacy.", "B", ["A human clinical trial fails the primary endpoint.", "Independent mouse replication fails.", "The effect disappears at clinically relevant dose.", "Adverse effects outweigh benefit."], "Tier B because the evidence is direct for a mouse endpoint but indirect for human clinical relevance.", organism="mouse", endpoint="tumor size", intervention_condition="Compound X under specified experimental conditions"),
        ev("e_mouse", "Mouse tumor size reduction", "animal_model", "direct", 0.7, ["sc_mouse"], ["animal_model", "mouse_model", "surrogate_endpoint"], organism="mouse", endpoint="tumor size", intervention_condition="Compound X under specified experimental conditions"),
        inf("i_preclinical", "Mouse result supports candidate status", "Animal-model evidence supports further study but not human clinical efficacy.", ["e_mouse"], ["sc_mouse"]),
        risk("r_animal_human", "Animal-to-human extrapolation", "animal_to_human", ["h_candidate"], "medium", "Require human clinical evidence before any efficacy claim."),
        falsifier("f_human_trial", "Human trial fails primary endpoint", ["h_candidate"], "Run or cite a registered human clinical trial with prespecified primary endpoint."),
        falsifier("f_replication", "Independent replication fails", ["h_candidate"], "Repeat comparable animal-model experiment independently."),
        narrative("n_translational_hype", "Preclinical success implies treatment narrative", "popular_science_frame", "A common narrative treats animal-model success as near-clinical proof."),
    ]
    c["edges"] = [edge("src_mouse", "sc_mouse", "says"), edge("sc_mouse", "e_mouse", "extracted_as"), edge("e_mouse", "i_preclinical", "supports", 0.7), edge("i_preclinical", "h_candidate", "supports", 0.6), edge("h_candidate", "r_animal_human", "has_risk"), edge("h_candidate", "f_human_trial", "falsified_by"), edge("h_candidate", "f_replication", "falsified_by"), edge("h_candidate", "n_translational_hype", "narrative_conflict", 0.5)]

    b = base_case("biomedicine_overclaim_mouse_to_human_rejected", "biomedicine", "overclaim", "Rejected overclaim: mouse result cures human cancer", "マウス結果からヒトがん治療効果を断定する過剰主張を拒否", "Mouse tumor reduction is asserted as a human cancer cure.", "A mouse experiment showed that Compound X reduced tumors, so Compound X cures human cancer.", "REJECT", "Animal model alone is used as human clinical proof.", "A", "Rejected: A-tier clinical claim lacks human evidence and required clinical metadata.", "No direct patient advice should be derived from this case.", "overclaimed")
    b["nodes"] = [source("src_mouse", "Mouse tumor model experiment"), sc("sc_mouse", "src_mouse", "Mouse tumor reduction", "Compound X reduced tumors in mice under experimental conditions."), hyp("h_cure", "Compound X cures human cancer", "A mouse animal model result proves human clinical efficacy and cures human cancer.", "A", [], "Rejected: animal-model evidence alone cannot establish a human clinical treatment claim."), ev("e_mouse", "Mouse tumor reduction", "animal_model", "direct", 0.82, ["sc_mouse"], ["animal_model", "mouse_model", "surrogate_endpoint"], organism="mouse", endpoint="tumor size"), inf("i_clinical_jump", "Mouse-to-human clinical leap", "The inference jumps from mouse tumor reduction to human clinical efficacy and cure.", ["e_mouse"], ["sc_mouse"], tier="X"), risk("r_animal_human", "Animal model treated as human efficacy", "animal_to_human", ["h_cure"], "high", "Limit to preclinical evidence or add human clinical trials.", "X")]
    b["edges"] = [edge("src_mouse", "sc_mouse", "says"), edge("sc_mouse", "e_mouse", "extracted_as"), edge("e_mouse", "i_clinical_jump", "supports", 0.9), edge("i_clinical_jump", "h_cure", "supports", 0.95), edge("h_cure", "r_animal_human", "has_risk")]
    two_case_domain("biomedicine", "good_mouse_model_scoped.json", "overclaim_mouse_to_human_rejected.json", c, b)


def social_cases() -> None:
    c = base_case("social_science_good_observational_association_scoped", "social_science", "good", "Correlation is not policy causation", "相関と因果を分離する政策仮説監査", "Education spending and scores are kept as observational association.", "A region with increased education spending also showed improved test scores. This supports an observational association, but a causal policy claim requires an identification strategy and confounder checks.", "PASS_WITH_WARNINGS", "Confounders, selection effects, pre-trends, and control groups remain open.", "B", "Tier B because the association is observable but causal identification is not established.", "The case records the causal requirements without claiming they are satisfied.", "observational")
    c.update({"time_window": "specified study period", "comparison_group": "not yet established", "confounder_discussion": "required before causal claim"})
    c["nodes"] = [source("src_education", "Regional education spending observational report", "report"), sc("sc_association", "src_education", "Spending and test-score association", "The region had increased education spending and improved test scores during the same period."), hyp("h_association", "Increased spending is observationally associated with improved scores", "The observation supports an association, not a definite causal policy effect.", "B", ["The effect disappears after controls.", "The pre-trend assumption fails.", "A comparison region shows the same trend without the policy.", "The measurement method changed during the period."], "B-tier association; causal policy proof requires identification strategy and counterfactual design.", time_window="specified study period", comparison_group="not yet established", confounder_discussion="required before causal claim"), ev("e_association", "Observed spending-score association", "observational_association", "observational", 0.58, ["sc_association"], ["observational", "correlation_only"], time_window="specified study period"), inf("i_association", "Association but not causation", "The evidence supports association while leaving confounding, selection, pre-trends, and measurement change unresolved.", ["e_association"], ["sc_association"]), risk("r_correlation", "Correlation-to-causation risk", "correlation_to_causation", ["h_association"], "medium", "Require identification strategy, control group, pre-trend checks, and confounder discussion."), falsifier("f_controls", "Effect disappears after controls", ["h_association"], "Control for plausible confounders and re-estimate the association."), narrative("n_policy_simple", "More spending automatically improves scores narrative", "policy_frame", "A popular policy frame treats temporal association as causal proof.")]
    c["edges"] = [edge("src_education", "sc_association", "says"), edge("sc_association", "e_association", "extracted_as"), edge("e_association", "i_association", "supports", 0.58), edge("i_association", "h_association", "supports", 0.5), edge("h_association", "r_correlation", "has_risk"), edge("h_association", "f_controls", "falsified_by"), edge("h_association", "n_policy_simple", "narrative_conflict", 0.5)]

    b = base_case("social_science_overclaim_correlation_to_causation_rejected", "social_science", "overclaim", "Rejected overclaim: correlation treated as policy causation", "相関から政策因果を断定する過剰主張を拒否", "A same-region before/after association is asserted as definite causation.", "Education spending rose and test scores rose in the same region, so increasing education spending definitely caused the improvement.", "REJECT", "Correlation-only evidence is used as causal proof.", "A", "Rejected: causal policy claim lacks identification strategy, confounder discussion, time window, and comparison group.", "The case intentionally omits causal design metadata.", "overclaimed")
    b["nodes"] = [source("src_education", "Regional education spending observational report", "report"), sc("sc_correlation", "src_education", "Same-region correlation", "Spending and scores rose in the same region."), hyp("h_cause", "Increased spending definitely caused score improvement", "The correlation proves a causal policy effect and increasing spending definitely caused the improvement.", "A", [], "Rejected: observational correlation cannot establish policy causation."), ev("e_correlation", "Same-region spending-score correlation", "observational_association", "observational", 0.8, ["sc_correlation"], ["observational", "correlation_only"]), inf("i_causal_jump", "Correlation-to-causation jump", "The inference treats a same-region correlation as causal proof without identification strategy or counterfactual.", ["e_correlation"], ["sc_correlation"], tier="X"), risk("r_correlation", "Correlation used as causation", "correlation_to_causation", ["h_cause"], "high", "Add an identification strategy and counterfactual or reduce to association.", "X")]
    b["edges"] = [edge("src_education", "sc_correlation", "says"), edge("sc_correlation", "e_correlation", "extracted_as"), edge("e_correlation", "i_causal_jump", "supports", 0.9), edge("i_causal_jump", "h_cause", "supports", 0.95), edge("h_cause", "r_correlation", "has_risk")]
    two_case_domain("social_science", "good_observational_association_scoped.json", "overclaim_correlation_to_causation_rejected.json", c, b)


def climate_cases() -> None:
    c = base_case("climate_earth_good_event_model_attribution_scoped", "climate_earth", "good", "Observation, model, and attribution are different claims", "観測・モデル・帰属主張の分離", "A heat anomaly is separated from model projection and attribution scope.", "A recent heat anomaly is consistent with model projections of increased extreme heat frequency under a specified scenario, but a single event does not by itself prove the entire long-term model.", "PASS_WITH_WARNINGS", "Single-event observation is not long-term model proof.", "B", "B-tier because model consistency and attribution framing are scoped and probabilistic.", "Observation, model projection, and attribution are separate nodes.", "model_scoped")
    c.update({"scenario": "specified emissions scenario", "uncertainty_range": "reported model interval", "time_horizon": "multi-decadal", "region": "specified region", "observational_baseline": "historical baseline period"})
    c["nodes"] = [source("src_heat", "Regional heat anomaly and model projection packet", "attribution_study"), sc("sc_observation", "src_heat", "Recent heat anomaly", "A recent heat anomaly was observed relative to a historical baseline."), sc("sc_model", "src_heat", "Model projection", "A model ensemble projects increased frequency of extreme heat under a specified scenario with uncertainty range."), hyp("h_consistent", "Heat anomaly is consistent with increased extreme heat frequency projection", "The event is consistent with model projections under a specified scenario, but a single event does not prove the entire long-term model.", "B", ["Long-term observations persistently fall outside the model uncertainty range.", "An alternative model explains the observations better.", "Attribution analysis fails under counterfactual comparison."], "B-tier because consistency is weaker than full model proof.", scenario="specified emissions scenario", uncertainty_range="reported model interval", time_horizon="multi-decadal", region="specified region", observational_baseline="historical baseline period"), ev("e_event", "Recent heat anomaly observation", "weather_observation", "direct", 0.48, ["sc_observation"], ["single_event", "weather_observation"], region="specified region", observational_baseline="historical baseline period"), ev("e_model", "Model ensemble projection", "model_projection", "model", 0.7, ["sc_model"], ["model_ensemble", "attribution_study"], scenario="specified emissions scenario", uncertainty_range="reported model interval", time_horizon="multi-decadal", region="specified region"), inf("i_consistency", "Event-model consistency inference", "The observation is consistent with projected increased frequency, while attribution remains probabilistic and scale-bound.", ["e_event", "e_model"], ["sc_observation", "sc_model"]), risk("r_single_event", "Single event cannot prove trend", "single_event_to_trend", ["h_consistent"], "medium", "State event observation, model projection, and attribution as separate claims."), falsifier("f_uncertainty", "Observations fall outside uncertainty range", ["h_consistent"], "Compare multi-decadal observations to the model uncertainty interval."), narrative("n_event_proof", "One event proves or disproves climate narrative", "public_debate_frame", "Public debate often treats one hot or cold event as decisive.")]
    c["edges"] = [edge("src_heat", "sc_observation", "says"), edge("src_heat", "sc_model", "says"), edge("sc_observation", "e_event", "extracted_as"), edge("sc_model", "e_model", "extracted_as"), edge("e_event", "i_consistency", "supports", 0.4), edge("e_model", "i_consistency", "supports", 0.7), edge("i_consistency", "h_consistent", "supports", 0.62), edge("h_consistent", "r_single_event", "has_risk"), edge("h_consistent", "f_uncertainty", "falsified_by"), edge("h_consistent", "n_event_proof", "narrative_conflict", 0.5)]

    b = base_case("climate_earth_overclaim_single_event_model_proof_rejected", "climate_earth", "overclaim", "Rejected overclaim: single event proves model", "単一イベントで長期モデル証明を断定する過剰主張を拒否", "One hot year is treated as complete proof of a long-term climate model.", "This year was extremely hot, so this climate model is completely proven.", "REJECT", "Single event is used as proof of the entire long-term model.", "A", "Rejected: single-event evidence cannot prove a long-term trend or model and lacks scale/scenario uncertainty metadata.", "The alternative cold-week denial example would be rejected by the same rule.", "overclaimed")
    b["nodes"] = [source("src_weather", "Annual weather anomaly report", "dataset"), sc("sc_hot_year", "src_weather", "One hot year", "This year was extremely hot in the observed region."), hyp("h_model_proven", "This year's heat completely proves the long-term climate model", "One hot year proves the long-term model and makes the projection completely proven.", "A", [], "Rejected: a single event cannot prove a long-term model."), ev("e_hot_year", "One hot year", "weather_observation", "direct", 0.72, ["sc_hot_year"], ["single_event", "one_year_anomaly"]), inf("i_event_proof", "Single event to model proof", "The inference jumps from one year of weather to complete proof of a long-term model.", ["e_hot_year"], ["sc_hot_year"], tier="X"), risk("r_single_event", "Single event proves model", "single_event_to_trend", ["h_model_proven"], "high", "Require long-term observations, model ensemble, uncertainty range, scenario, and attribution method.", "X")]
    b["edges"] = [edge("src_weather", "sc_hot_year", "says"), edge("sc_hot_year", "e_hot_year", "extracted_as"), edge("e_hot_year", "i_event_proof", "supports", 0.9), edge("i_event_proof", "h_model_proven", "supports", 0.95), edge("h_model_proven", "r_single_event", "has_risk")]
    two_case_domain("climate_earth", "good_event_model_attribution_scoped.json", "overclaim_single_event_model_proof_rejected.json", c, b)


def ai_cases() -> None:
    c = base_case("ai_computer_science_good_benchmark_scoped", "ai_computer_science", "good", "Benchmark score is not general intelligence", "ベンチマーク成績と実世界性能の分離", "Benchmark result is scoped to protocol P.", "Model X achieved 90% on Benchmark B under evaluation protocol P. This supports a benchmark-scoped performance claim, but not a general intelligence or safety claim.", "PASS_WITH_WARNINGS", "Benchmark scope, contamination, replication, transfer, and safety remain separate.", "B", "B-tier because the benchmark score is inspectable but broad capability and safety are not established.", "Leaderboard and safety claims are explicitly out of scope.", "benchmark_scoped")
    c.update({"evaluation_protocol": "protocol P", "contamination_check": "not yet independently audited", "reproduction_status": "single reported evaluation"})
    c["nodes"] = [source("src_benchmark", "Benchmark B evaluation report", "benchmark_report"), sc("sc_score", "src_benchmark", "Benchmark score", "Model X achieved 90% on Benchmark B under evaluation protocol P."), hyp("h_benchmark", "Model X achieved benchmark-scoped performance under protocol P", "The claim is limited to Benchmark B under protocol P and does not imply general intelligence, safety, or real-world deployment reliability.", "B", ["Independent replication fails.", "Train/test contamination is discovered.", "Real-world task performance collapses.", "Safety evaluation reveals a major failure.", "The score depends on prompt or hidden tool access."], "B-tier because benchmark evidence is direct for the benchmark but indirect for deployment.", evaluation_protocol="protocol P", contamination_check="not yet independently audited", reproduction_status="single reported evaluation"), ev("e_score", "90% on Benchmark B", "benchmark_result", "benchmark", 0.7, ["sc_score"], ["benchmark_result", "single_benchmark"], evaluation_protocol="protocol P", contamination_check="not yet independently audited", reproduction_status="single reported evaluation"), inf("i_scope", "Benchmark-scoped inference", "The result supports performance on Benchmark B under protocol P, not broad intelligence or safety.", ["e_score"], ["sc_score"]), risk("r_benchmark", "Benchmark overgeneralization", "benchmark_overgeneralization", ["h_benchmark"], "medium", "Separate benchmark score, contamination check, transfer, and safety evaluation."), falsifier("f_replication", "Independent replication fails", ["h_benchmark"], "Repeat the same protocol independently and compare score."), narrative("n_leaderboard", "Leaderboard equals general capability narrative", "AI_evaluation_frame", "A common frame treats benchmark rank as broad intelligence or safety.")]
    c["edges"] = [edge("src_benchmark", "sc_score", "says"), edge("sc_score", "e_score", "extracted_as"), edge("e_score", "i_scope", "supports", 0.7), edge("i_scope", "h_benchmark", "supports", 0.66), edge("h_benchmark", "r_benchmark", "has_risk"), edge("h_benchmark", "f_replication", "falsified_by"), edge("h_benchmark", "n_leaderboard", "narrative_conflict", 0.5)]

    b = base_case("ai_computer_science_overclaim_benchmark_to_agi_rejected", "ai_computer_science", "overclaim", "Rejected overclaim: benchmark to general intelligence and safety", "ベンチマークから汎用知能・安全性を断定する過剰主張を拒否", "A 90% benchmark score is asserted as general intelligence and deployment safety.", "Model X scored 90% on Benchmark B, so it is generally intelligent, safe, and reliable in real-world deployment.", "REJECT", "Benchmark score alone is used for general intelligence, safety, and deployment reliability.", "A", "Rejected: benchmark result lacks contamination check, reproduction status, transfer evidence, and safety evaluation.", "This case keeps the source claim separate but rejects the overextended inference.", "overclaimed")
    b["evaluation_protocol"] = "not specified"
    b["nodes"] = [source("src_benchmark", "Leaderboard report", "benchmark_report"), sc("sc_score", "src_benchmark", "Benchmark score", "Model X scored 90% on Benchmark B."), hyp("h_agi_safe", "Model X is generally intelligent, safe, and reliable in real-world deployment", "Benchmark B proves general intelligence, safety, and reliable real-world deployment.", "A", [], "Rejected: benchmark score alone cannot support broad intelligence or safety."), ev("e_score", "90% benchmark score", "benchmark_result", "benchmark", 0.88, ["sc_score"], ["benchmark_result", "leaderboard", "single_benchmark"]), inf("i_agi_jump", "Benchmark-to-AGI/safety jump", "The inference treats a benchmark score as proof of general intelligence and safety.", ["e_score"], ["sc_score"], tier="X"), risk("r_benchmark", "Benchmark overgeneralization", "benchmark_overgeneralization", ["h_agi_safe"], "high", "Add independent replication, contamination audit, real-world transfer tests, and safety evaluations.", "X")]
    b["edges"] = [edge("src_benchmark", "sc_score", "says"), edge("sc_score", "e_score", "extracted_as"), edge("e_score", "i_agi_jump", "supports", 0.9), edge("i_agi_jump", "h_agi_safe", "supports", 0.95), edge("h_agi_safe", "r_benchmark", "has_risk")]
    two_case_domain("ai_computer_science", "good_benchmark_scoped.json", "overclaim_benchmark_to_agi_rejected.json", c, b)


def law_cases() -> None:
    c = base_case("law_policy_ethics_good_legal_empirical_normative_separated", "law_policy_ethics", "good", "Legal, empirical, and normative claims are not the same", "法的主張・政策効果・価値判断の分離", "A legal finding is separated from effectiveness and ethical desirability.", "A court found Policy X legal in a specific jurisdiction and legal context. That legal finding should be separated from empirical claims about policy effectiveness and normative claims about whether the policy is ethically desirable.", "PASS_WITH_WARNINGS", "Jurisdiction, legal authority, outcome measure, and value premise must stay explicit.", "B", "B-tier because legal validity is scoped, while empirical and normative claims require separate evidence.", "The case uses three separated hypotheses rather than one blended truth claim.", "legal_empirical_normative_split")
    c.update({"jurisdiction": "specific jurisdiction", "date": "specified decision date", "court_level": "specified court level", "legal_issue": "validity of Policy X in legal context", "value_premise": "ethical desirability requires an explicit value premise", "counter_principle": "rights, equity, or proportionality may conflict"})
    c["nodes"] = [source("src_court", "Court decision on Policy X", "case_law"), source("src_eval", "Policy X evaluation placeholder", "policy_evaluation"), sc("sc_legal", "src_court", "Legal finding", "A court found Policy X legal in a specific jurisdiction and legal context."), sc("sc_eval", "src_eval", "Policy effectiveness separate", "Empirical effectiveness requires separate policy evaluation evidence."), hyp("h_legal_scope", "Policy X is legal within the scoped jurisdiction and legal context", "The legal finding is scoped to jurisdiction, date, court level, and legal issue; it does not establish effectiveness or ethical desirability.", "B", ["The legal claim is reversed on appeal.", "The claim is limited by jurisdiction.", "A policy evaluation finds no empirical effect.", "The normative claim depends on a contested value premise."], "B-tier because the legal source directly supports a scoped legal claim only.", jurisdiction="specific jurisdiction", date="specified decision date", court_level="specified court level", legal_issue="validity of Policy X", value_premise="ethical desirability requires explicit value premise", counter_principle="rights, equity, or proportionality may conflict"), ev("e_legal", "Scoped legal validity finding", "case_law", "direct", 0.68, ["sc_legal"], ["case_law", "binding_precedent", "legal_validity"], jurisdiction="specific jurisdiction", date="specified decision date", court_level="specified court level", legal_issue="validity of Policy X"), ev("e_eval_gap", "Need separate policy evaluation", "policy_evaluation", "indirect", 0.32, ["sc_eval"], ["policy_evaluation", "impact_assessment"], outcome_measure="not specified in legal source"), inf("i_legal_scope", "Legal scope only", "The court finding supports legal validity in context, not empirical effectiveness or ethical correctness.", ["e_legal", "e_eval_gap"], ["sc_legal", "sc_eval"]), risk("r_legal_empirical", "Legal-to-empirical overclaim", "normative_to_empirical", ["h_legal_scope"], "medium", "Separate legal validity, empirical effectiveness, and normative desirability claims."), falsifier("f_reversal", "Reversal on appeal or jurisdictional limit", ["h_legal_scope"], "Track appellate reversal, later authority, and jurisdictional limits."), narrative("n_law_equals_good", "Legal means effective and ethical narrative", "public_policy_frame", "Public debate often treats legality as policy success or moral correctness.")]
    c["edges"] = [edge("src_court", "sc_legal", "says"), edge("src_eval", "sc_eval", "says"), edge("sc_legal", "e_legal", "extracted_as"), edge("sc_eval", "e_eval_gap", "extracted_as"), edge("e_legal", "i_legal_scope", "supports", 0.68), edge("e_eval_gap", "i_legal_scope", "supports", 0.25), edge("i_legal_scope", "h_legal_scope", "supports", 0.62), edge("h_legal_scope", "r_legal_empirical", "has_risk"), edge("h_legal_scope", "f_reversal", "falsified_by"), edge("h_legal_scope", "n_law_equals_good", "narrative_conflict", 0.5)]

    b = base_case("law_policy_ethics_overclaim_legal_to_effective_ethical_rejected", "law_policy_ethics", "overclaim", "Rejected overclaim: legal means effective and ethically correct", "合法性から有効性・倫理的正しさを断定する過剰主張を拒否", "Legal validity is asserted as empirical effectiveness and ethical correctness.", "The court said Policy X is legal, so Policy X is effective and ethically correct.", "REJECT", "Legal validity is used to prove empirical and normative claims.", "A", "Rejected: legal source lacks policy evaluation evidence and explicit value premise.", "The overclaim intentionally omits jurisdiction/date/court-level/value-premise details.", "overclaimed")
    b["nodes"] = [source("src_court", "Court decision on Policy X", "case_law"), sc("sc_legal", "src_court", "Legal finding", "A court found Policy X legal."), hyp("h_effective_ethical", "Policy X is effective and ethically correct because it is legal", "Legal validity proves Policy X is effective and ethically correct.", "A", [], "Rejected: legality cannot establish empirical effectiveness or ethical correctness."), ev("e_legal", "Legal validity finding", "case_law", "direct", 0.82, ["sc_legal"], ["case_law", "binding_precedent", "legal_validity"]), inf("i_legal_jump", "Legal-to-effective/ethical jump", "The inference treats legal validity as empirical effectiveness and ethical correctness.", ["e_legal"], ["sc_legal"], tier="X"), risk("r_legal_empirical", "Legal validity treated as empirical and ethical proof", "normative_to_empirical", ["h_effective_ethical"], "high", "Separate legal, empirical, and normative claims.", "X")]
    b["edges"] = [edge("src_court", "sc_legal", "says"), edge("sc_legal", "e_legal", "extracted_as"), edge("e_legal", "i_legal_jump", "supports", 0.9), edge("i_legal_jump", "h_effective_ethical", "supports", 0.95), edge("h_effective_ethical", "r_legal_empirical", "has_risk")]
    two_case_domain("law_policy_ethics", "good_legal_empirical_normative_separated.json", "overclaim_legal_to_effective_ethical_rejected.json", c, b)


def main() -> int:
    preserve_legacy()
    clean_public_cases()
    history_cases()
    biomedicine_cases()
    social_cases()
    climate_cases()
    ai_cases()
    law_cases()
    print(f"wrote {len(list(SAMPLE.glob('*/*.json')))} public sample cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
