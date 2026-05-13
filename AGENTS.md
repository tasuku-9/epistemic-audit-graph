# AGENTS.md — Epistemic Audit Codex Starter

## Project purpose

This repository is a hackathon-oriented starter kit for an AI-mediated hypothesis audit graph.
It tests whether one shared claim-audit structure can work across six evidence regimes:

1. history / humanities
2. biomedicine
3. social science
4. climate / earth science
5. AI / computer science
6. law / policy / ethics

The goal is not to declare which claims are true. The goal is to make hypotheses auditable by separating:

- source claims: what a paper, document, dataset, benchmark, precedent, or source actually says
- evidence nodes: what observation or result is being used
- inference nodes: how the user connects that evidence to a hypothesis
- falsifier nodes: what would weaken or refute the hypothesis
- risk nodes: where overclaim, analogy, narrative conflict, or domain-specific misuse may occur

## Non-negotiable epistemic rules

Do not weaken these rules unless the user explicitly asks for a prototype that demonstrates failure modes.

1. A published hypothesis must have at least one falsification condition.
2. Evidence must have a source claim. Do not connect a paper/source directly to a hypothesis when the actual source claim has not been represented.
3. Methodological analogy, mythic parallel, benchmark extrapolation, animal-to-human extrapolation, or correlation-only evidence must not support an A-tier hypothesis by itself.
4. Keep `source_claim` and `inference` separate.
5. A score is not a truth score. It is a provisional audit score based on registered evidence, risks, and assumptions.
6. Domain-specific rules live in `data/domain_rules/`. Do not bake a single universal truth metric into the validator.
7. Every change proposal must be expressed as structured JSON before it can be applied.
8. Do not add network calls or external dependencies unless they are clearly justified. This starter should run offline.

## Repo layout

- `src/epistemic_audit/` — lightweight Python validator and scoring helpers.
- `data/sample_cases/` — six-domain validation examples, with one good case and one overclaim case per domain.
- `data/domain_rules/` — domain-specific overclaim triggers and tier constraints.
- `schemas/` — JSON schema-style contracts for cases and change requests.
- `frontend/` — static demo shell for browsing sample cases.
- `demos/ancient_history/legacy_hypothesis_credibility_v2.html` — original stronger v2 graph prototype, kept only as a legacy stress-test, UI reference, and internal example.
- `.agents/skills/epistemic-audit/` — repository skill for Codex.
- `docs/` — roadmap, pitch, validation plan, architecture.

## How to verify work

Run these before claiming completion:

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests
```

If you change the validator, add or update tests.
If you add a domain case, add `validator_expected_result` and an `expected_validation` block.
If you add a new rule, document it in `docs/VALIDATION_PLAN.md` and the relevant `data/domain_rules/*.json` file.

## Development style

- Prefer small, inspectable Python and static HTML over heavy frameworks.
- Keep sample cases human-readable.
- Keep warnings distinct from hard errors.
- Make validator output explain which rule failed and which node caused it.
- Treat the six domains as testbeds, not as claims of universal coverage.

## Review checklist

Before opening a PR or handing work back:

- [ ] all good sample cases validate without errors
- [ ] all overclaim sample cases fail for the intended reason
- [ ] no A-tier hypothesis is supported only by M-tag / analogy evidence
- [ ] all evidence nodes reference source claims
- [ ] all hypotheses include falsification conditions
- [ ] evidence reaches hypothesis through an `InferenceNode`, not by a direct Evidence -> Hypothesis support edge
- [ ] README and docs still match the code
