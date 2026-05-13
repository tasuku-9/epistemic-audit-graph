# 3-Minute Demo Script

## 0:00-0:30 - Problem

"Normal wiki pages and AI answers often flatten the difference between a source claim, a user inference, evidence, and narrative framing. This prototype makes those layers inspectable."

## 0:30-1:10 - Show Static Selector

Open:

```text
frontend/index.html
```

Show the six domain cards:

- history/humanities
- biomedicine
- social science
- climate/earth
- AI/computer science
- law/policy/ethics

## 1:10-1:50 - Show Main History Case

Open the good history/humanities case:

```text
data/sample_cases/history_humanities/good_egm_jomon_dotaku_kiki_scoped.json
```

Point out:

- D-M55, Dotaku, and Kiki are separate observations
- paternal asymmetry, ritual discontinuity, and mythic memory are inferences
- Y-DNA conquest and myth-as-record are X-level risks
- falsifiers are explicit
- narrative conflicts are visible but do not prove the hypothesis

## 1:50-2:25 - Show Overclaim Rejection

Open the overclaim history/humanities case or any domain overclaim button.

Explain:

- the source claim can exist
- the evidence can be real
- the inference can still be invalid
- the deterministic validator rejects the overclaim

## 2:25-2:50 - Show Validator

Run:

```bash
python scripts/validate_cases.py
python -m unittest discover -s tests
```

Explain that 12 public cases are checked: six good cases pass with warnings, and six overclaim cases reject.

## 2:50-3:00 - Wrap

"This is not a truth machine. It is a write-gated epistemic wiki layer: AI structures the edit, code enforces falsifiability and domain rules, and humans review the evidence."
