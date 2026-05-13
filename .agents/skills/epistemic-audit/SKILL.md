---
name: epistemic-audit
description: "Use for Epistemic Gap Mapper work: hypothesis audit graphs, falsification conditions, source-claim separation, overclaim detection, domain rules, and Codex tasks for this repo."
---

# Epistemic Audit Skill

When working on this repository, use this method.

## Intake method

For any new claim, split it into:

1. `source`: where the information comes from
2. `source_claim`: what the source actually says
3. `evidence`: what observation/result is being used
4. `inference`: the user's reasoning step
5. `hypothesis`: the auditable claim
6. `falsifier`: what would weaken/refute it
7. `risk`: overclaim, analogy, domain transfer, citation debt
8. `edges`: explicit relations among the above

## Mandatory checks

- Hypothesis has falsification conditions.
- Evidence references source claims.
- Source claim and user inference are separate.
- M-tag / analogy evidence cannot alone justify A-tier.
- Domain overclaim patterns are checked.
- Strong claims include risk nodes when appropriate.

## Domain overclaim triggers

- history/humanities: myth, legend, folklore -> direct proof of historical fact
- biomedicine: mouse / animal / in vitro -> human clinical efficacy
- social science: correlation / survey -> causation
- climate: single event / one year -> global trend proof
- AI/CS: benchmark / leaderboard -> general intelligence or real-world safety
- law/policy/ethics: legal/normative claim -> empirical policy effectiveness

## Verification

Run:

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests
```

Explain any warnings and do not hide failing rules.
