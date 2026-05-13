# Validation Report

Last updated: 2026-05-13

Command:

```bash
python scripts/validate_cases.py
```

## Summary

12 public demo cases were checked. Each case matched its expected validator status.

| Domain | Case | Expected | Actual | Matched | Brief reason |
| --- | --- | --- | --- | --- | --- |
| history_humanities | good_egm_jomon_dotaku_kiki_scoped | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Scoped abductive hypothesis; sample sources need review |
| history_humanities | overclaim_egm_jomon_dotaku_kiki_rejected | REJECT | REJECT | yes | Y-DNA conquest, myth-as-record, ritual single-cause overclaims |
| biomedicine | good_mouse_model_scoped | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Mouse-model claim limited to preclinical candidate scope |
| biomedicine | overclaim_mouse_to_human_rejected | REJECT | REJECT | yes | Animal-model evidence used as human cancer cure |
| social_science | good_observational_association_scoped | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Association separated from causal policy claim |
| social_science | overclaim_correlation_to_causation_rejected | REJECT | REJECT | yes | Correlation-only evidence used as causal proof |
| climate_earth | good_event_model_attribution_scoped | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Observation, model, scenario, and attribution separated |
| climate_earth | overclaim_single_event_model_proof_rejected | REJECT | REJECT | yes | One hot year used as proof of long-term model |
| ai_computer_science | good_benchmark_scoped | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Benchmark claim limited to protocol scope |
| ai_computer_science | overclaim_benchmark_to_agi_rejected | REJECT | REJECT | yes | Benchmark score used as AGI/safety/deployment proof |
| law_policy_ethics | good_legal_empirical_normative_separated | PASS_WITH_WARNINGS | PASS_WITH_WARNINGS | yes | Legal, empirical, and normative layers separated |
| law_policy_ethics | overclaim_legal_to_effective_ethical_rejected | REJECT | REJECT | yes | Legal validity used as effectiveness and ethical correctness |

## Expected Warnings

Good cases currently return `PASS_WITH_WARNINGS` because sources are sample packets with `citation_text` placeholders. This is intentional for the hackathon starter and should be replaced with reviewed citations before a real pilot.
