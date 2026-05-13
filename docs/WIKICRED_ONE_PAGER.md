# WikiCred One-Pager Draft

Last updated: 2026-05-13

## Working Title

Falsification-first wiki editing: making credible claims auditable before they are accepted

## One-Sentence Pitch

This is a lightweight audit layer for wiki-style claims where every significant claim must separate source claim, evidence, inference, risk, and falsification condition before it can present itself as credible.

## Problem

Wikipedia and AI-assisted knowledge work often focus on whether a claim has a citation. That is necessary, but not sufficient.

A citation can still be used to support a claim the source does not actually make. A plausible synthesis can hide weak inference. A controversial hypothesis can appear more settled than it is if readers cannot see what would weaken or falsify it.

## Core Principle

A credible wiki claim should answer two questions:

1. What does the source actually say?
2. What would weaken or falsify this claim?

The second question is the differentiator. Falsification conditions make claims reviewable, contestable, and safer to improve.

## Prototype

The current prototype is a static, offline-friendly epistemic-audit wiki layer.

It separates:

- `Source`: paper, dataset, article, benchmark, report, statute, or primary text
- `SourceClaim`: what that source actually says
- `Evidence`: the observation or result being used
- `Inference`: the reasoning step from evidence to hypothesis
- `Hypothesis`: the claim under audit
- `Falsifier`: what would weaken or refute the hypothesis
- `Risk`: overclaim, analogy inflation, domain transfer, or citation debt
- `Narrative`: the broader story or standard framing the claim interacts with

## Validation

The validator enforces hard rules:

- hypotheses require falsification conditions
- evidence must reference source claims
- source claims and user inferences stay separate
- analogy or M-tag evidence cannot alone justify an A-tier hypothesis
- domain-specific overclaim patterns must have risk nodes

The demo currently includes 13 validation cases:

- six domains with good and overclaim examples
- one richer converted history/humanities v2 case

The six domains are:

1. history / humanities
2. biomedicine
3. social science
4. climate / earth science
5. AI / computer science
6. law / policy / ethics

## Why This Fits WikiCred

WikiCred focuses on credibility, information integrity, citation transparency, source evaluation, and credibility tools for the Wikimedia ecosystem.

This project is not a truth-scoring system. It is a write-gated structure that helps editors and readers see what kind of claim is being made, what supports it, where it overreaches, and what would change our mind.

## Demo Flow

1. Start with a plausible claim.
2. Show the source claim separately from the user's inference.
3. Show the required falsification condition.
4. Show validator rejection when a high-tier claim lacks a falsifier or relies only on analogy.
5. Show the same structure working across six evidence regimes.

## Current Ask

We are looking for feedback from WikiCred/Wikimedia credibility builders on:

- whether falsification conditions are a useful addition to citation transparency
- which existing WikiCred projects this should align with
- whether this should be framed as an editor tool, a media-literacy tool, or a research/provenance data model
- whether it fits an upcoming monthly WikiCred online meetup, WikiCred Demo Hour, builder outreach, or another participation route

## Repository Artifacts

- Data-driven demo: `frontend/index.html`
- Validator: `scripts/validate_cases.py`
- Six-domain sample cases: `data/sample_cases/`
- WikiCred pitch: `docs/HACKATHON_PITCH.md`
- Validation plan: `docs/VALIDATION_PLAN.md`
- Main history/humanities case: `data/sample_cases/history_humanities/good_egm_jomon_dotaku_kiki_scoped.json`
- Legacy history/humanities stress-test: `data/legacy_cases/history_humanities/v2_converted.json`

## Limitations

- The converted history/humanities case is structurally valid, not expert endorsement.
- Several starter sources still use citation labels without DOI/URL.
- The current prototype is static and local; it does not yet implement authenticated wiki editing or live change requests.
