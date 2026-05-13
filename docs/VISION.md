# Vision: What This System Is Trying to Be

This document explains the why behind the design: the goals that are not obvious from the code or data model.

## The One-Line Goal

A wiki where the primary act of contribution is not editing text, but **adding or improving a falsification condition**.

## Why Falsification Conditions Are the Core

Current Wikipedia asks: *What is the source?*

This system adds: *What would weaken or falsify this claim?*

That second question changes everything about how knowledge is managed.

## Contributions Become Structural, Not Editorial

When the meaningful contribution is a falsification condition, the system becomes:

- **Hard to vandalize.** Deleting or weakening a falsification condition is immediately visible as suspicious. Disagreement with a condition must be expressed as a better condition, which is itself a constructive contribution.
- **Self-sorting for expertise.** People who can write precise, testable falsification conditions surface as domain experts, not by credential or edit count, but by the quality of their epistemic reasoning.
- **Resistant to AI content floods.** AI-generated content can imitate fluent prose, but a claim without a real falsification condition is flagged automatically and should never present as credible.

## The Minimum Viable Contribution

The first thing a new contributor can do is find an existing claim without a falsification condition and add one. That single action improves the system more than any amount of text editing.

## Falsified Claims Must Stay

When a falsification condition is satisfied, the claim is not deleted. It is marked `FALSIFIED` and preserved.

```text
claim:h1 [FALSIFIED - 2028]
  Falsification condition:
    "If early Yayoi high-status burials consistently show O-lineage DNA
    with no D-lineage individuals, the hypothesis weakens substantially."
  Evidence that satisfied this:
    [Site XX, 2027 excavation report]
  Successor claim:
    claim:h1b - "Possible regional variation in status distribution,
    not system-wide pattern"
```

This matters because knowledge has stratigraphy. The layers of what was believed, tested, weakened, falsified, and revised are part of the knowledge itself, not noise to be cleaned up.

## The Contribution Model

| Level | Contribution | Effect |
| --- | --- | --- |
| New contributor | Add a falsification condition to an existing claim | Claim becomes auditable |
| Intermediate | Refine a weak condition into a specific, testable one | Claim becomes more honest about scope |
| Expert | Satisfy a falsification condition with new evidence | Claim moves to `FALSIFIED`; a successor claim can be born |
| System | Accumulate `FALSIFIED` claims over time | Knowledge stratigraphy becomes visible |

## What This System Is Not

- **Not a truth scorer.** No score says a claim is true. Scores reflect audit completeness and support structure.
- **Not an AI judge.** The AI proposes structure. Deterministic code enforces rules. Humans review and accept.
- **Not a replacement for Wikipedia.** It is a structured epistemic audit layer that can sit alongside or within wiki editing.

## The Long-Term Picture

If this model works at scale, a topic page on a contested subject would show:

1. Active claims with falsification conditions and supporting evidence.
2. Weakened claims where counter-evidence has accumulated but the condition is not yet satisfied.
3. Falsified claims preserved with the evidence that changed our minds.
4. Open questions: the specific tests or observations that would move active claims toward resolution.

This is not a fact database. It is a record of the current state of justified belief: honest about what is tested, what is contested, and what has already been tried and found wanting.

## Core Public Principle

No wiki claim without a falsification condition should be accepted as audit-ready.
