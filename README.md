# Epistemic Audit Graph

## Start Here

**Public demo hub:** [https://tasuku-9.github.io/epistemic-audit-graph/](https://tasuku-9.github.io/epistemic-audit-graph/)

Open these first to understand the project before looking at the validation suite or domain examples.

**Recommended path:**

1. [Claim Cascade](https://tasuku-9.github.io/epistemic-audit-graph/demos/park_or_reopen/index.html) - first-touch interactive demo.
2. [Claim Lifecycle Workspace](https://tasuku-9.github.io/epistemic-audit-graph/demos/claim_lifecycle/index.html) - structured claim-state workspace.

Epistemic Audit Graph turns disputes into actionable evidence challenges.

The goal is not only to map disputes, but to make them actionable: each contested claim can show what evidence, source clarification, counterevidence, or policy review would move it forward, downgrade it, park it, or reopen it.

After those two, use the remaining routes as examples and implementation proof:

- [Claim lifecycle dashboard](https://tasuku-9.github.io/epistemic-audit-graph/frontend/index.html)
- [K-Pg claim-state graph](https://tasuku-9.github.io/epistemic-audit-graph/demos/kpg_extinction/index.html)
- [Bronze Age claim-state graph](https://tasuku-9.github.io/epistemic-audit-graph/demos/bronze_age_collapse/index.html)
- [Lifecycle timeline prototype](https://tasuku-9.github.io/epistemic-audit-graph/demos/uncertainty_workspace/index.html)

It does this by managing the lifecycle of contested claims:

```text
proposed -> supported -> contested -> weakened -> parked
        -> failed-by-current-evidence -> reopened
        -> accepted-with-caveats -> accepted -> superseded
```

Technically, it is a reopenable claim-state graph for contested knowledge.

It is not a simple argument map and not a truth-scoring system. The core idea is non-destructive downgrading: weak claims are not deleted, but parked with reasons, counterevidence, downgrade conditions, and reopening conditions.

A parked claim can be reopened only when its reopening conditions are met.

The graph makes these claim-state fields inspectable:

- what the source actually says;
- what inference is being made;
- supporting evidence and counterevidence;
- uncertainty and source-lineage risk;
- overclaim risk;
- downgrade conditions;
- reopening conditions;
- unresolved questions;
- evidence challenges;
- status history.

## From Disputes To Tasks

Ordinary disputes often become repeated argument: one side cites a source, another disputes the interpretation, and newcomers cannot tell what would actually move the issue forward.

Epistemic Audit Graph turns that loop into a claim challenge board. A parked claim can show:

- why it is parked;
- what evidence would reopen it;
- what counterevidence must be answered;
- what source-lineage or citation-loop check is needed;
- what downgrade condition would keep it out of the accepted set;
- what review would make it a candidate for adoption.

This makes participation smaller and more concrete. A contributor does not need to win the whole dispute. They can resolve one open challenge: find the earliest source, separate source wording from inference, add counterevidence, clarify a policy condition, or satisfy a reopening condition.

The board should not score people or reward factional wins. It tracks claim states, open challenges, resolved challenges, parked claims, reopened claims, and claims needing source audit.

In the sample cases, this board is now data-driven from each hypothesis node's `claim_state` object:

- `status`
- `status_reason`
- `source_says`
- `inference_made`
- `downgrade_conditions`
- `reopening_conditions`
- `evidence_challenges`

## Why This Is Different

Kialo-style debate maps make pros and cons visible; ASPIC-style systems formalize defeasible argument; Wikidata stores structured entities and statements; RAG retrieves documents for generation. Epistemic Audit Graph manages the state of a claim over time. It records what the source says, what inference is being made, why a claim was weakened or parked, and what evidence would reopen, downgrade, or supersede it.

## Why Parking Matters

Weak claims often come back because the prior objection is buried in prose, a discussion thread, or a binary verdict. Parking gives weak claims a durable middle state: not accepted, not erased. A parked claim stays visible with the reason it was downgraded and the evidence challenge that would move it forward.

```text
This claim is currently parked.
Reason: the inference is stronger than the source supports.
Reopen if: an independent high-quality source directly supports the claim
and addresses the listed counterevidence.
```

Local paths:

- Claim Cascade first-touch demo: `demos/park_or_reopen/index.html`
- Claim Lifecycle Workspace: `demos/claim_lifecycle/index.html`
- Claim lifecycle dashboard: `frontend/index.html`
- K-Pg claim-state graph: `demos/kpg_extinction/index.html`
- Bronze Age claim-state graph: `demos/bronze_age_collapse/index.html`
- Lifecycle timeline prototype: `demos/uncertainty_workspace/index.html`

Core explanatory docs:

- `docs/POSITIONING.md`: how this differs from argument maps, causal DAG tools, evidence maps, and decision frameworks.
- `docs/VISION.md`: why downgraded or failed claims should stay visible instead of being deleted.

Core message:

```text
AI structures claims.
Code enforces state transition rules.
Humans inspect and revise.
```

## Problem

Many knowledge systems preserve final outputs: articles, reports, policies, papers, legal decisions, fact-check verdicts, and discussion logs. They often do not preserve the intermediate state of contested claims.

A disputed claim may be repeated in prose, deleted, buried in discussion, reduced to a binary verdict, revived after being weakened, cited more strongly than its source supports, or regenerated by an LLM because the weak claim is widely repeated.

The missing layer is claim lifecycle management.

## Solution

Epistemic Audit Graph decomposes a contested claim into structured state objects:

```text
Source -> SourceClaim -> Evidence -> Inference -> ClaimState
                                      |             |
                                      |             +-> Downgrade condition
                                      |             +-> Reopening condition
                                      +-> Risk      +-> Evidence challenge
```

The validator applies deterministic shared and domain-specific rules. It checks source-claim separation, inference separation, tier reasons, analogy limits, domain overclaim patterns, and whether contested claims name the evidence that would weaken, park, or reopen them. Tier labels are internal validator shorthand; they should stay in the deeper validation layer rather than the first-touch demo path.

## Why AI-Mediated Editing

The AI is an intake and drafting layer. It may propose structured nodes or change requests, but it is not the final authority. A human reviewer can inspect the proposed claim state, source wording, inference, support, counterevidence, risks, downgrade conditions, reopening conditions, and unresolved challenges before accepting a change.

## Why Deterministic Validation

The validator is deliberately small and inspectable. The important rules are enforced by Python and JSON rule files, not by asking an LLM whether a claim is true.

Validator statuses:

- `PASS`: structurally valid and no blocking state-transition issue
- `PASS_WITH_WARNINGS`: valid, but citations, scope, or review status still need attention
- `REJECT`: hard rule failure; treat the claim as parked or failed by current evidence until the challenge is addressed

## Deep Validation Vocabulary

The guided demos avoid validator shorthand. The deeper dashboard and graph demos use it because implementation needs a compact way to show claim strength, unresolved conditions, and blocking failures.

Claim status and audit tier are related, but not identical:

- **Claim status** says what is currently happening to a claim in the lifecycle: `supported`, `contested`, `weakened`, `parked`, `failed-by-current-evidence`, `reopened`, and so on.
- **Audit tier** is a display and validation label for the current support structure. It is not a truth score and not a person or faction score.

Current tier labels:

| Tier | Meaning | Typical handling |
| --- | --- | --- |
| `A` | Direct observation, strong consensus, or strong evidence within the stated scope. | Can be accepted if caveats, falsifiers, and source scope remain inspectable. |
| `B` | Supported with material caveats. | Keep the claim, but preserve scope limits, assumptions, and reopening/downgrade conditions. |
| `C` | Unresolved evidence challenge, weak support, or incomplete support. | Keep visible as a question-bearing claim; do not upgrade without resolving the challenge. |
| `X` | Parked overclaim or failed by current evidence. | Do not delete it; park it with reasons, counterevidence, downgrade conditions, and reopening conditions. |
| `M` | Analogy, mythic, narrative, or metaphorical context rather than direct support. | Useful for framing or hypothesis generation, but cannot upgrade a claim by itself. |

`parked` is a lifecycle state. `X` is an audit-tier warning. Many `X` claims should be parked, but a parked claim is more than a red label: it must say why it is parked and what would reopen it.

The system is strict about propagation. A claim does not inherit only the support of its evidence; it also inherits the conditions and uncertainties attached to the evidence and to the inference step.

```text
Evidence E has condition C1
Inference E -> Claim X adds assumption C2
Claim X inherits C1 and adds C2

X park conditions = C1 + C2
```

This is why an overclaim can appear even when the evidence itself is real. The evidence may support a narrower claim, while the inference adds a stronger term, wider scope, missing bridge, or unverified context. The graph keeps that uncertainty traceable: which evidence node, inference edge, or added assumption made the claim parkable.

Typical transitions:

```text
C -> B   when an open evidence challenge is resolved but caveats remain
B -> A   when support is direct, in scope, and no blocking risk remains
B -> C   when a caveat becomes an unresolved evidence challenge
B/C -> X when the wording overclaims what the evidence can support
X -> reopened when the stated reopening conditions are met
reopened -> B/C/A after human review of the new evidence
```

This is the difference between deleting a weak claim and managing it. A weak claim can remain visible as `X` or `parked`, but it cannot silently function as an accepted claim until the graph records what changed.

## Six-Domain Demo List

| Domain | Scoped claim | Downgrade challenge |
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

## Local Demo Path

Serve the repository root or `frontend/` over a tiny local HTTP server, then open:

```text
frontend/index.html
```

The static page shows six domain cards, scoped/downgrade case buttons, user input, extracted claim-state nodes, validation state, and graph links.

## Claim-State Demo Routes

For contested-knowledge walkthroughs, use these demos together:

```text
demos/bronze_age_collapse/index.html
demos/kpg_extinction/index.html
```

Suggested order:

1. Open the Bronze Age Collapse graph first as the easier history route.
2. Then open the K-Pg extinction graph as the denser source-audited flagship.

Why K-Pg remains the strongest flagship:

- globally recognizable scientific topic
- clear source-lineage and inference-risk problem
- accepted, contested, unresolved, and parked claims are all visible
- downgrade and reopening conditions can be attached to claim states
- source audit, schema summary, validation report, and source index are included in `docs/kpg_extinction/`

The Bronze Age Collapse demo shows the same claim-state pattern in a more accessible historical debate. The six-domain frontend remains the validation-suite proof that the same deterministic lifecycle structure generalizes beyond one topic.

## Lifecycle Timeline Prototype

`demos/uncertainty_workspace/index.html` is a sibling prototype for claim lifecycle inspection. It can switch between a lifecycle timeline and an evidence-relation view, keeps unresolved challenges as first-class nodes, draws challenge states with dashed rings, and parks overclaims with X-tier red rings.

Seed concept:

```text
Move contested knowledge from repeated argument into structured state management.
```

Historical outreach artifacts are preserved at:

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

## Deep Dives

See `docs/VISION.md` for the long-term contribution model:

```text
No contested claim should present as audit-ready unless the graph says what would downgrade or reopen it.
```

See `docs/POSITIONING.md` for adjacent areas and prior positioning. The current product frame should lead with claim lifecycle management, non-destructive downgrading, reopening conditions, and actionable evidence challenges.

## GitHub Pages

For the static demo, publish the repository root with GitHub Pages and open the hub first:

```text
index.html
```

The validation dashboard at `frontend/index.html` loads generated JSON from `frontend/` and sample cases from `data/`, so publishing from the repository root is the simplest configuration.

## Limitations

- sample citations are placeholders and need expert review
- no DOI/PDF extraction yet
- no production server, auth, database, or multi-user editing
- no LLM API integration yet
- domain rules are hackathon validation rules, not expert consensus
- provisional audit scores, if used, are support-structure signals, not truth scores

## License

- Code: MIT License. See `LICENSE`.
- Documentation and demo data: Creative Commons Attribution 4.0 International (CC BY 4.0).
