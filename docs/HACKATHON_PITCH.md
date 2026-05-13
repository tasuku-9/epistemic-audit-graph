# Hackathon Pitch

## Title

Epistemic Audit Graph: AI-mediated editing with deterministic credibility rules

## Problem

AI answers, papers, Wikipedia-style articles, and public debates often mix source claims, user inference, evidence, narrative framing, and normative conclusions.

That collapse makes overclaims hard to see:

- a source claim becomes a user hypothesis
- a benchmark becomes general intelligence
- a mouse result becomes a human treatment claim
- a legal finding becomes empirical effectiveness
- mythic or narrative material becomes direct historical proof

## Solution

Epistemic Audit Graph decomposes claims into structured nodes and applies deterministic domain-specific validation rules.

Core nodes:

- Source
- SourceClaim
- Evidence
- Inference
- Hypothesis
- Risk
- Falsifier
- Narrative

## Key Innovation

Writing is AI-mediated, but rule enforcement is deterministic. The AI proposes structured change requests; the validator enforces falsifiability, source separation, overclaim rules, and domain-specific limits.

The AI does not decide truth.

Instead:

```text
AI structures claims.
Code enforces audit rules.
Humans inspect and revise.
```

## Demo

Six evidence regimes:

- history/humanities: myth, genetics, ritual discontinuity, narrative conflict
- biomedicine: animal model to clinical claim
- social science: correlation to causation
- climate/earth: single event to model/trend claim
- AI/CS: benchmark to general intelligence/safety claim
- law/policy/ethics: legality to effectiveness/ethical correctness

Each domain has one scoped good case and one rejected overclaim case.

## Core Message

Not "AI decides truth."

Instead:

- AI structures claims.
- Code enforces audit rules.
- Humans inspect and revise.

## WikiCred Fit

WikiCred is a natural first community target because the project centers citation transparency, source evaluation, information integrity, and credibility tooling. The prototype contributes a write-gated credibility structure rather than a truth score.

The strongest short pitch:

> A next-generation wiki should not only ask "what is the source?" It should also ask "what would weaken this claim?"

## Ask

Feedback on:

- whether mandatory falsification conditions help Wikimedia-facing credibility work
- whether the node model maps to existing editor workflows
- which domain rules should be tightened before a real pilot
- whether this fits a WikiCred monthly meetup or Demo Hour-style feedback slot
