# Architecture

## Core Design

The project separates claim layers that are often mixed in normal wiki writing and AI answers.

```text
SourceNode
  -> says
SourceClaimNode
  -> extracted_as
EvidenceNode
  -> supports / uses_evidence
InferenceNode
  -> supports / refutes
HypothesisNode
  -> falsified_by FalsifierNode
  -> has_risk RiskNode
  -> conflicts_with NarrativeNode
```

The system is not a truth scorer. It is an audit structure plus deterministic validation rules.

## Why This Structure Matters

The system is designed to catch overclaim. It must be able to say:

- the source is real, but the source does not say what the user claims
- the evidence is strong, but the inference is weak
- the hypothesis is interesting, but the falsification condition is missing
- the claim is plausible in one domain scope but overgeneralized to another
- the narrative conflict is real but does not itself prove the alternative hypothesis

## Data Model Overview

### Source

Represents a paper, book, dataset, benchmark, statute, precedent, report, or primary text.

Required:

- `id`
- `node_type: source`
- `title`
- `source_type`
- at least one of `doi`, `url`, or `citation_text`

### SourceClaim

Represents what the source actually says.

Required:

- `source_id`
- `claim_text`
- `quote_or_locator` where possible

### Evidence

Represents the observation or result being used in the audit.

Required:

- `evidence_type`
- `directness`
- `weight`
- `source_claim_ids`

Evidence should feed an `InferenceNode`, not directly support a `HypothesisNode`.

### Inference

Represents a reasoning step from evidence to hypothesis.

This is where many errors happen:

- animal model -> human clinical claim
- benchmark result -> real-world capability
- correlation -> causation
- myth/text pattern -> historical event
- legal precedent -> empirical policy impact

### Hypothesis

Represents the claim being audited. It must include falsification conditions and either a linked `FalsifierNode` or limiting conditions.

### Falsifier

Represents a condition or observation that would weaken or refute a hypothesis.

### Risk

Represents overclaim, citation debt, M-tag analogy, extrapolation, narrative conflict, or missing source risk.

### Narrative

Represents the consensus, popular, legal, policy, or interpretive frame being challenged.

## MVP Architecture

```text
static sample JSON
        -> Python validator
        -> validation report
        -> static frontend demo
        -> Codex tasks for improvement
```

No server is required for the hackathon starter.

## Validator Contract

The validator returns:

- `status`: `PASS`, `PASS_WITH_WARNINGS`, or `REJECT`
- `errors`
- `warnings`
- `missing_fields`
- `overclaim_flags`
- `m_tag_flags`
- `tier_mismatch_flags`
- `suggested_fixes`

The validator is deterministic. It does not ask an LLM whether a claim is true.

## Legacy Demo Boundary

The old `hypothesis_credibility_v2.html` file is preserved as `demos/ancient_history/legacy_hypothesis_credibility_v2.html`. It is no longer the default public demo.

The public history/humanities demo is the scoped Jomon / Dotaku / Kiki JSON case under `data/sample_cases/history_humanities/`.
