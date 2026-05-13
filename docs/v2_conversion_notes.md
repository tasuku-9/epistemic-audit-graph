# V2 Conversion Notes

Last updated: 2026-05-13

## Scope

This note documents the first conversion of the original history/humanities visual demo:

- source: `demos/ancient_history/legacy_hypothesis_credibility_v2.html`
- output: `data/legacy_cases/history_humanities/v2_converted.json`
- domain: `history_humanities`
- role in the six-domain plan: this is the richer history/humanities demo case; the other five domains remain represented by their good and overclaim sample cases.

The converted case is structurally valid under the current validator. Structural validity is not expert endorsement of the historical claims.

## Extracted Legacy Arrays

The original demo contained:

| Legacy array | Count | Converted role |
| --- | ---: | --- |
| `NAR` | 4 | `narrative` nodes |
| `EV` | 20 | `source`, `source_claim`, and `evidence` nodes |
| `HY` | 10 | `hypothesis`, `inference`, `falsifier`, and `risk` nodes |

The converted output contains 98 nodes and 127 edges.

## Mapping Rules

| Legacy field | New structure |
| --- | --- |
| `EV.source` / `EV.doi` | `source` node metadata |
| `EV.title` | `source_claim.claim_text` and `evidence.title` |
| `EV.type` | `evidence.evidence_type` plus domain evidence tags |
| `EV.weight` | `evidence.weight` and support/refute edge strength |
| `EV.m` | `evidence.m_tag`; if true, `directness: analogy` |
| `EV.sup` | `supports` edges to hypotheses |
| `EV.con` | `refutes` edges, except for `h7` as noted below |
| `HY.title` / `HY.desc` | `hypothesis.title`, `hypothesis.description`, and an explicit `inference` node |
| `HY.tier` | `hypothesis.tier` |
| `HY.fc` | `falsifier.required_test` and `falsified_by` edge |
| `HY.oc` | `risk` node with suggested patch |
| `HY.narConflicts` | narrative, paper, or frame conflict edges |
| `NAR` entries | `narrative` nodes |

## Normalization Decisions

- The legacy `con` relations targeting `h7` were normalized as support edges. In the original data, those evidence items are marked as contradicting the Trans-Eurasian position, while `h7` itself is already phrased as the negated claim: "Trans-Eurasian hypothesis is difficult." Preserving them as `refutes h7` would invert the intended argument.
- M-tagged evidence remains visible as evidence, but it also creates a risk node when it supports a hypothesis.
- Source claims are currently derived from legacy evidence labels. They need citation-level review before being treated as verified quotations or source-local claims.
- Genetic evidence is tagged as `ancient_dna`, linguistic evidence as `direct_philology`, archaeological evidence as `secure_stratigraphy`, and mythological evidence as `primary_text_with_context` for the current history/humanities validator.

## Validation Result

After conversion:

```bash
python scripts/validate_cases.py --write-frontend
python -m unittest discover -s tests
```

Expected result:

- 13 sample cases checked.
- `data/legacy_cases/history_humanities/v2_converted.json` is retained as a legacy stress-test and UI reference, outside the public 12-case validation set.
- Existing good and overclaim cases keep their expected outcomes.

Warnings remain for sources that have only `citation_text` and no DOI or URL. This is expected for the starter data and should be reduced during citation cleanup.

## Remaining Work

- Replace derived source claims with exact quotations, locators, or source-local paraphrases.
- Decide whether the converted v2 case should be presented as a main demo, a technical appendix, or a stress-test case.
- Add a compact visual graph view for the converted case in the data-driven frontend.
- Continue using the six-domain matrix in `docs/VALIDATION_PLAN.md` so the project does not become history-only.
