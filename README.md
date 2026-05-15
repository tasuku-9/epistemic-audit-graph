# Epistemic Audit Graph

A source-weighted dispute map for wiki-style claims.

This prototype does not score truth. It structures claims so editors can inspect:

- what the source actually says;
- what inference is being made;
- what evidence supports or weakens the claim;
- what would falsify or downgrade it;
- where Wikipedia-style policy guardrails matter.

Start here:

- K-Pg Extinction WikiGraph: `demos/kpg_extinction/index.html`
- Bronze Age Collapse WikiGraph: `demos/bronze_age_collapse/index.html`
- Six-domain validator demo: `frontend/index.html`
- Experimental Uncertainty Workspace DAG: `demos/uncertainty_workspace/index.html`

Core message:

```text
AI structures claims.
Code enforces audit rules.
Humans inspect and revise.
```

## Problem

AI answers, papers, Wikipedia-style articles, and public debates often mix source claims, user inference, evidence, narrative framing, and normative conclusions. Once those layers collapse, a claim can sound credible while becoming hard to audit.

## Solution

Epistemic Audit Graph decomposes a user claim into structured nodes:

```text
Source -> SourceClaim -> Evidence -> Inference -> Hypothesis
                                      |             |
                                      |             +-> Falsifier
                                      +-> Risk      +-> Narrative conflict
```

The validator then applies deterministic shared and domain-specific rules. It checks falsifiability, source-claim separation, inference separation, tier reasons, M-tag / analogy limits, and domain overclaim patterns.

## Why AI-Mediated Editing

The AI is an intake and drafting layer. It may propose structured nodes or change requests, but it is not the final authority. A human reviewer can inspect the proposed hypothesis, evidence, inference, risk, falsifier, and narrative conflict before accepting a change.

## Why Deterministic Validation

The validator is deliberately small and inspectable. The important rules are enforced by Python and JSON rule files, not by asking an LLM whether a claim is true.

Validator statuses:

- `PASS`: structurally valid and no warnings
- `PASS_WITH_WARNINGS`: valid, but citations, scope, or review status need attention
- `REJECT`: hard rule failure

## Six-Domain Demo List

| Domain | Good case | Overclaim case |
| --- | --- | --- |
| history_humanities | Jomon / Dotaku / Kiki as scoped abductive hypothesis | D-M55 / Dotaku / Kiki as certain conquest proof |
| biomedicine | mouse model as preclinical candidate evidence | mouse result cures human cancer |
| social_science | observational association | correlation proves policy causation |
| climate_earth | event, model, and attribution separated | single hot year proves whole model |
| ai_computer_science | benchmark-scoped performance | benchmark proves AGI, safety, deployment reliability |
| law_policy_ethics | legal, empirical, and normative claims separated | legal means effective and ethically correct |

## Run Validation

```bash
python scripts/validate_cases.py
```

Refresh frontend data:

```bash
python scripts/validate_cases.py --write-frontend
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Hackathon Demo Path

Serve the repository root or `frontend/` over a tiny local HTTP server, then open:

```text
frontend/index.html
```

The static page shows six domain cards, good/overclaim case buttons, user input, extracted nodes, validation output, and graph links.

## WikiCred Demo Route

For WikiCred outreach, use two public-facing demos together:

```text
demos/bronze_age_collapse/index.html
demos/kpg_extinction/index.html
```

Suggested order:

1. Open the Bronze Age Collapse demo first as the easier humanities/history route.
2. Then open the K-Pg extinction WikiGraph as the denser source-audited flagship.

Why K-Pg remains the strongest flagship:

- globally recognizable scientific topic
- clear source-weighting problem
- consensus, minority, uncertain, and overclaim nodes are all visible
- Wikipedia policy guardrails are represented directly
- source audit, schema summary, validation report, and source index are included in `docs/kpg_extinction/`

The Bronze Age Collapse demo shows the same graph pattern in a more accessible historical debate. The six-domain frontend remains the validation-suite proof that the same deterministic audit structure generalizes beyond one topic.

## Experimental Uncertainty Workspace

`demos/uncertainty_workspace/index.html` is a sibling prototype for structuring uncertainty beyond wiki claims. It can switch between a temporal DAG view and a relation-force view, keeps unknowns as first-class nodes, draws frontier claims with dashed rings, and parks overclaims with X-tier red rings.

Seed concept:

```text
Structure uncertainty without prematurely resolving it.
```

The PDF one-pager for email attachment is included at:

```text
docs/WIKICRED_ONE_PAGER.pdf
```

## Legacy Demo

The original stronger history/humanities HTML prototype is preserved as:

```text
demos/ancient_history/legacy_hypothesis_credibility_v2.html
```

Additional legacy history views:

```text
demos/ancient_history/legacy_hypothesis_credibility_v2_en.html
demos/ancient_history/wikigraph_v2_interactive.html
data/legacy_cases/history_humanities/epistemic_wikigraph_v2.json
demos/bronze_age_collapse/index.html
data/legacy_cases/bronze_age_collapse/bronze_age_collapse_wikigraph.json
```

These are legacy stress-tests, UI references, and stronger internal examples. They are not the default public-facing history/humanities demo.

## Vision

See `docs/VISION.md` for the long-term contribution model:

```text
No wiki claim without a falsification condition should be accepted as audit-ready.
```

## GitHub Pages

For the static demo, publish the repository root with GitHub Pages and open:

```text
frontend/index.html
```

The frontend loads generated JSON from `frontend/` and sample cases from `data/`, so publishing from the repository root is the simplest configuration.

## Limitations

- sample citations are placeholders and need expert review
- no DOI/PDF extraction yet
- no production server, auth, database, or multi-user editing
- no LLM API integration yet
- domain rules are hackathon validation rules, not expert consensus
- provisional audit scores, if used, are not truth scores

## License

- Code: MIT License. See `LICENSE`.
- Documentation and demo data: Creative Commons Attribution 4.0 International (CC BY 4.0).
