# Validation Plan

## Validation Goal

We are not validating whether every claim is true. We are validating whether the audit structure forces useful distinctions across six evidence regimes.

Highest-priority rule: every meaningful hypothesis needs a falsifier, limiting condition, or linked `FalsifierNode`.

## Validator Statuses

- `PASS`: structurally valid and no warnings
- `PASS_WITH_WARNINGS`: valid, with source/review/scope warnings
- `REJECT`: hard rule failure

## Shared Hard Rules

The validator rejects:

- hypothesis without falsification conditions or linked falsifier
- evidence without source claim references
- source claim / inference collapse, including Evidence directly supporting Hypothesis
- invalid edge references
- A-tier hypothesis supported only by M-tag or analogy evidence
- A-tier hypothesis without domain-appropriate evidence tags
- domain overclaim patterns asserted as strong claims
- tier or weight changes without reasons

## Six-Domain Validation Matrix

| Domain | Good case should pass because... | Overclaim case should reject because... |
| --- | --- | --- |
| history_humanities | Jomon / Dotaku / Kiki observations, inferences, risks, falsifiers, and narratives are separated | Y-DNA, myth, and ritual discontinuity are used as certain conquest proof |
| biomedicine | mouse-model evidence is limited to preclinical candidate status | animal evidence is used as human cancer cure / clinical efficacy |
| social_science | association is separated from causal policy claim | correlation-only evidence is used as causal proof |
| climate_earth | observation, model projection, scenario, uncertainty, and attribution are separated | one hot year proves an entire long-term model |
| ai_computer_science | benchmark result is scoped to protocol | benchmark score implies general intelligence, safety, and deployment reliability |
| law_policy_ethics | legal, empirical, and normative claims remain separate | legal validity proves effectiveness and ethical correctness |

## Domain Rule Files

Rules live in `data/domain_rules/`:

- `history_humanities.json`
- `biomedicine.json`
- `social_science.json`
- `climate_earth.json`
- `ai_computer_science.json`
- `law_policy_ethics.json`

Each rule file records required fields, forbidden overclaims, warning conditions, accepted evidence types, weakened evidence types, tier restrictions, and required falsifier style.

## Regression Tests

Unit tests cover:

- all six good cases pass or pass with warnings
- all six overclaim cases reject
- missing falsifier causes rejection
- M-tag-only A-tier claim is rejected
- source claim / inference collapse is rejected
- benchmark-to-AGI claim is rejected
- legal-to-ethical correctness claim is rejected
- animal-to-human clinical claim is rejected
- correlation-to-causation claim is rejected
- single-event climate proof claim is rejected

## Review Limits

The sample cases are scaffolding. They are not expert-reviewed domain truth claims. A real pilot must replace placeholder citations, recruit domain reviewers, and preserve disagreements as audit metadata.
