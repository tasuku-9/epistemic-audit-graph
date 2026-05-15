# Uncertainty Workspace

## Core Idea

Uncertainty Workspace is a sibling prototype to Epistemic Audit Graph.
It is not a truth engine and not a wiki replacement.
It is a workspace for structuring uncertainty without prematurely resolving it.

```text
Structure uncertainty without prematurely resolving it.
```

In Japanese:

```text
わからなさを、結論に潰さず、監査可能な形にする。
```

## Why Separate It

The WikiCred-facing demo is optimized for source-weighted wiki claims.
Uncertainty Workspace is broader: papers, policy memos, legal analysis, scientific hypotheses, safety reviews, and research notes.

The core shift is from a knowledge base to an uncertainty base.

## Design Principles

- Unknowns are first-class nodes.
- Evidence, inference, narrative pressure, risk, falsifier, and policy/legal/normative frames stay separated.
- A claim can remain visible without being accepted.
- Overclaims are parked, not deleted.
- Frontier nodes use dashed rings.
- Overclaims use X-tier or solid red rings.
- Time and causal ordering are represented by a DAG mode.
- The system should show what would weaken a claim before presenting the claim as credible.

## Node Types

| Type | Role |
| --- | --- |
| `hypothesis` | A scoped claim or working claim. |
| `evidence` | A source-local observation, measurement, result, or record. |
| `unknown` | A named uncertainty that must not disappear into prose. |
| `narrative` | A public, consensus, policy, legal, or interpretive frame. |
| `risk` | A known failure mode or overextension path. |
| `falsifier` | A condition, test, or limiting result that would weaken the claim. |

## Temporal DAG Rules

The first experimental DAG mode uses a horizontal time axis:

- older evidence appears left of newer claims;
- forward support / motivation edges arc above the axis;
- later evidence that weakens an earlier claim arcs below the axis;
- frontier / disputed nodes get dashed rings;
- overclaim nodes get solid red rings;
- cycles should be detected deterministically before a graph is trusted.

This separates two concepts:

- `forward_time`: evidence or reasoning that moves from older material to later claims;
- `backward_audit`: later findings that inspect, weaken, or revise earlier claims.

The visual can show a backward audit relation without treating it as a backward causal dependency.

## Seed Demo

Current seed files:

- `data/uncertainty_cases/seed_temporal_dag_case.json`
- `demos/uncertainty_workspace/index.html`

The seed case is a toy cross-domain science / policy example:

```text
Lab signal -> scoped lab hypothesis -> scale-up hypothesis -> policy-ready overclaim
```

It is intentionally not a real literature claim. The point is to test the visual grammar:

- structured unknowns;
- temporal ordering;
- frontier nodes;
- overclaim parking;
- limiting tests;
- support and weakening edges.

## What This Is Not Yet

- not a production app;
- not a general DAG editor;
- not a citation extraction tool;
- not a validator for all chronology claims;
- not a substitute for expert review.

## Next Useful Validator Rules

- reject graph cycles;
- require `epistemic_time` for DAG-visible nodes;
- require falsifiers for hypotheses above C-tier;
- warn when a forward causal claim depends only on narrative pressure;
- reject policy-ready or deployment-ready claims with unresolved blocker nodes;
- require reasons for tier changes.
