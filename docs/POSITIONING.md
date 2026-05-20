# Positioning

## One-Line Aim

Epistemic Audit Graph and Uncertainty Workspace aim to structure uncertainty so humans can make responsible decisions without pretending unresolved claims are settled.

```text
AI structures claims.
Code enforces audit rules.
Humans make the decision.
```

## What This Is

This project is an audit workspace for claims, evidence, uncertainty, and decision readiness.

It separates:

- what a source actually says;
- what evidence is available;
- what inference is being made;
- what remains unknown;
- what would falsify or downgrade a claim;
- what narrative, policy, legal, or normative frame is being challenged;
- where an overclaim begins.

The goal is not to automate judgement.
The goal is to make the judgement surface smaller, clearer, and more honest.

## The Missing Operational Layer

The need for this layer is familiar outside public knowledge work.

In frontline sales work, people have to separate what a customer actually said from what the team inferred, assumed, promised, or still needs to confirm. Mixing those states can create real operational mistakes.

In engineering work, teams routinely separate requests, specifications, hypotheses, tests, issues, reviews, rollbacks, and accepted changes. Code has mature operational systems for this: version control, issue trackers, review states, failing tests, release gates, and rollback paths.

Public knowledge work has many adjacent pieces of this discipline, but they are often distributed across prose, citations, talk pages, review comments, fact-checks, policy language, and expert memory. A source statement, an interpretation, a derived claim, an unresolved assumption, and counterevidence can collapse into one fluent paragraph.

Epistemic Audit Graph is an attempt to bring that practical state discipline into the public knowledge layer. It does not claim that no prior system has addressed parts of the problem. The claim is narrower: contested public knowledge needs an inspectable operational layer for what was said, what was inferred, what remains uncertain, what was downgraded or parked, and what would reopen or strengthen a claim.

## Adjacent Work

This project is close to several existing traditions, but combines them differently.

| Adjacent area | What it already does well | Difference here |
| --- | --- | --- |
| Argument mapping / structured debate, such as [Kialo](https://www.kialo-edu.com/), [DebateGraph](https://debategraph.us/about/), and IBIS / [Dialogue Mapping](https://cognexus.org/id41.htm) | Makes arguments, positions, pros, cons, and debate structure visible. | Adds source-claim separation, falsification conditions, domain overclaim rules, M-tag limits, and deterministic validation. |
| Causal DAG tools, such as [DAGitty](https://www.dagitty.net/) | Makes causal assumptions and bias-control structure explicit. | Uses DAG as one view inside a broader uncertainty audit that also includes source claims, narratives, falsifiers, unknowns, and overclaim parking. |
| Evidence-to-decision frameworks, such as [GRADE Evidence to Decision](https://help.gradepro.org/support/solutions/articles/204000076798-etd-overview) | Structures how evidence informs recommendations, especially in healthcare and public health. | Generalizes the audit structure beyond one domain and keeps unresolved unknowns visible as graph nodes before a recommendation is made. |
| Evidence maps and living reviews, such as public-policy living maps from [IPPO / EPPI-Centre](https://theippo.co.uk/policy-research-tool/) | Map bodies of literature and evidence over time. | Focuses on claim-level auditability: which inference is being made, what would weaken it, and which overclaim rules apply. |
| Consulting issue trees, hypothesis trees, decision maps, and slide-based synthesis | Help teams turn messy information into a decision narrative. | Leaves behind an inspectable data structure instead of only a polished conclusion, and can show uncertainty the final deck usually compresses. |

## Core Difference

Most tools optimize for one of these:

- debate;
- causality;
- evidence synthesis;
- recommendation writing;
- decision presentation.

This project tries to connect the layer before decision:

```text
source claim -> evidence -> inference -> uncertainty -> falsifier -> decision boundary
```

The decision boundary is the point where humans must choose:

- proceed despite unresolved uncertainty;
- reject the overclaim;
- ask for more evidence;
- accept a value tradeoff;
- downgrade the claim;
- split one claim into weaker claims.

## Why This Matters

Many failures in papers, policy, law, science, and public debate come from collapsed layers:

- an animal result becomes a human treatment claim;
- a correlation becomes a causal policy claim;
- a legal ruling becomes an ethical conclusion;
- a benchmark becomes a real-world safety claim;
- a narrative becomes evidence;
- a source quote becomes a stronger inference than the source supports.

The project treats those collapses as validator-visible events, not just writing problems.

## What Humans Still Decide

The system should not decide truth, policy, law, clinical action, or ethics.

It can prepare the decision by making these explicit:

- evidence status;
- missing fields;
- source/inference separation;
- falsification conditions;
- unresolved frontier nodes;
- risks and overclaims;
- time or causal-order problems;
- value premises.

Humans still decide whether a remaining uncertainty is acceptable.

## Product Direction

There are two related but distinct product lines:

| Line | Primary audience | Current demo |
| --- | --- | --- |
| Epistemic Audit Graph | wiki editors, source evaluators, public-knowledge reviewers | `frontend/index.html`, `demos/kpg_extinction/index.html`, `demos/bronze_age_collapse/index.html` |
| Uncertainty Workspace | researchers, policy analysts, legal analysts, safety reviewers, decision teams | `demos/uncertainty_workspace/index.html` |

The first asks:

```text
Is this claim audit-ready?
```

The second asks:

```text
What is still unknown, and what decision can responsibly be made anyway?
```

## Near-Term Build Target

Keep the prototype small and inspectable:

- JSON case data;
- static HTML demos;
- deterministic Python validator;
- simple graph views;
- no production server;
- no authentication;
- no database dependency;
- no claim that the system decides truth.

The next useful step is to add deterministic DAG validation:

- require `epistemic_time` for DAG-visible nodes;
- reject graph cycles;
- warn when later evidence is being used as if it were prior support;
- require falsifiers or limiting conditions for decision-facing claims.
