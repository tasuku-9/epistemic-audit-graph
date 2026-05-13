# CODEX_TASKS.md

Use this file as a task queue. Do not attempt all tasks at once.

## Task 0 — Baseline verification

Status: complete on 2026-05-13.

Run:

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests
```

Expected: all sample cases match `expected_validation.status`.

## Task 1 — Make the frontend data-driven

Status: complete on 2026-05-13.

Goal: replace the placeholder frontend with a static viewer that loads sample cases and shows:

- hypotheses
- evidence
- source claims
- falsifiers
- risks
- validator status
- domain rule flags

Constraints:

- no backend
- no external libraries
- keep it hackathon-demo friendly
- do not delete `demos/ancient_history/legacy_hypothesis_credibility_v2.html`

## Task 2 — Convert original v2 demo into structured case data

Status: complete on 2026-05-13.

Goal: parse or manually convert the original v2 `HY`, `EV`, `NAR` arrays into the shared case format.

Deliverables:

- `data/legacy_cases/history_humanities/v2_converted.json`
- a short report in `docs/v2_conversion_notes.md`

Important: split source metadata, source claims, evidence, inferences, risks, and falsifiers. The converted v2 case is now a legacy stress-test, not the public default history/humanities case.

## Task 3 — Add change request validation

Goal: implement `src/epistemic_audit/change_request_validator.py` using `schemas/change_request.schema.json`.

Rules:

- create_hypothesis requires falsification conditions
- create_evidence requires source claim references
- change_tier requires old tier, new tier, reason, and affected evidence
- high-tier upgrades must preserve domain-specific constraints

## Task 4 — Add minimal LLM-facing prompt workflow

Goal: add a prompt and example that converts free text into `change_request` JSON.

Deliverables:

- `prompts/change_request_builder.md` improved
- `examples/change_requests/*.json`
- validation tests

No actual LLM API integration yet.

## Task 5 — Hackathon packaging

Status: in progress on 2026-05-13.

Goal: create the submission package.

Deliverables:

- 3-minute demo script updated
- 5-slide pitch outline updated
- validation table updated
- screenshots or GIF plan added
- limitations and safety section made explicit

Completed so far:

- six public demo domains normalized to 12 cases
- deterministic validator updated for `PASS`, `PASS_WITH_WARNINGS`, and `REJECT`
- main history/humanities public demo replaced with scoped Jomon / Dotaku / Kiki case
- legacy HTML preserved as stress-test / UI reference / stronger internal example

## Task 6 — Optional local MVP

Only after Tasks 0–5.

Build a local-only API using FastAPI or a tiny Python HTTP server. Do not add this unless explicitly requested.
