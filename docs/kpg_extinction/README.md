# Epistemic WikiGraph v0.5 - K-Pg Extinction Flagship Demo

This is an English-language, Wikipedia-facing demo of an **Epistemic WikiGraph**: a moving graph that represents claims, evidence, counterevidence, sources, open questions, and article-policy guardrails.

## Why this topic?

The Cretaceous-Paleogene extinction is globally recognizable and scientifically rich:

- strong physical evidence for the Chicxulub impact;
- legitimate but bounded debate around Deccan Traps volcanism;
- active disagreement over whether non-avian dinosaurs were already declining;
- clear relevance to Wikipedia's NPOV / Verifiability / No original research policies.

That makes it a better flagship demo for English-language Wiki/Wikimedia audiences than a high-context local-history controversy.

## Files

- `demos/kpg_extinction/index.html`: standalone interactive graph.
- `data/legacy_cases/kpg_extinction/kpg_extinction_wikigraph_v0_5.json`: source-audited graph data.
- `docs/kpg_extinction/SOURCE_AUDIT.md`: source audit notes.
- `docs/kpg_extinction/SCHEMA.md`: schema summary.
- `docs/kpg_extinction/WIKI_PITCH_NOTE.md`: short positioning note for Wiki/Wikimedia audiences.
- `docs/kpg_extinction/VALIDATION_REPORT.json`: ID-reference validation.
- `docs/kpg_extinction/SOURCE_INDEX.tsv`: source table.

## How to use the HTML

Open the HTML file in a browser. It is self-contained and has no external JavaScript dependency.

Controls:

- drag nodes;
- drag background to pan;
- mouse wheel to zoom;
- switch between composition maps;
- filter by node type, claim tier, and edge type;
- click a node to inspect evidence, source, audit notes, and relations;
- export PNG.

## Claim tiers

- **A**: strong consensus or strong physical evidence;
- **B**: supported but materially qualified;
- **C**: active hypothesis, weak support, or incomplete support;
- **X**: parked overclaim / high-risk wording.

The important design point is not to make every view look equal. The graph keeps minority or overclaim nodes visible while making their weaker status obvious.

## Dataset counts

```json
{
  "wiki_pages": 11,
  "claims": 15,
  "evidence": 20,
  "sources": 15,
  "relations": 196,
  "composition_maps": 4,
  "narratives": 5,
  "questions": 5
}
```

Validation errors: `[]`
