# Graph Rendering Spec

## Concept

Hypotheses, evidence, and narrative frames are nodes in a force-directed audit graph.
Support, counterevidence, paper conflict, narrative conflict, and frame conflict are edges.
Each claim carries an A/B/C/X audit tier, falsification condition, overclaim state, and narrative-audit context.

Short seed description:

```text
A force-directed epistemic audit graph where hypotheses, evidence, and narrative frames are nodes.
Claims carry A/B/C/X tiers, falsification conditions, M-tags, and narrative-audit links.
```

## Display Schema

The frontend projects the full audit case schema into a smaller display model:

```json
{
  "hypothesis": {
    "id": "string",
    "title": "string",
    "tier": "A | B | C | X | M",
    "desc": "string",
    "fc": "falsification or limiting condition",
    "overclaim": "risk text or validator flags",
    "narConflicts": ["narrative_conflict | paper_conflict | frame_conflict"],
    "fields": ["evidence type tags"]
  },
  "evidence": {
    "id": "string",
    "title": "string",
    "type": "genetic | archaeological | biomedical | social | climate | ai | legal | circumstantial",
    "weight": "number",
    "isM": "boolean",
    "source": "source claim summary",
    "doi": "optional string",
    "sup": ["claim ids"],
    "con": ["claim ids"]
  },
  "narrative": {
    "id": "string",
    "title": "string",
    "type": "narrative | paper | frame"
  },
  "frontier": {
    "id": "string",
    "meaning": "disputed, unresolved, or question-bearing but not rejected",
    "visual": "dashed node ring"
  }
}
```

## Rendering Rules

- Left panel: important claims only, meaning hypotheses and inference nodes.
- Center panel: Canvas or SVG force graph.
- Right panel: details, risks, falsifiers, source claims, and validator flags.
- Large circles: hypotheses and important inference claims.
- Small circles: evidence nodes.
- Diamonds: narrative, paper, or frame nodes.
- Dashed node rings: frontier / disputed nodes. These are unresolved or source-sensitive claims, not rejected claims.
- Solid red rings or X-tier badges: parked overclaims that must remain visibly weak.
- Hidden from graph but shown in detail: SourceClaim, Risk, Falsifier, Source, Assumption, ChangeRequest.
- Physics: nodes repel, edges behave like springs, and weak centering keeps the graph readable.
- Edge types: `sup`, `con`, `paper_conflict`, `narrative_conflict`, `frame_conflict`.
- Scores are provisional audit-support scores, not truth scores.

## Future Temporal DAG Mode

The main public WikiCred demos use a force-directed layout.
The experimental Uncertainty Workspace demo at `demos/uncertainty_workspace/index.html` can switch between temporal DAG and relation-force views over the same graph data.

A mature temporal DAG mode should add:

- `date`, `date_range`, or `epistemic_time` fields on nodes.
- cycle detection in the deterministic validator.
- a horizontal time axis that places older evidence before newer claims.
- separate visual routing for older evidence supporting later claims and newer evidence weakening earlier claims.
- hard rejection or warning when a claim depends on a circular causal chain.

This should remain optional because the current force graph is easier to read for first-contact wiki demos, while DAG mode is better for research, policy, legal, and scientific uncertainty work.

## Dual-View Uncertainty Mode

Uncertainty Workspace treats layout as an analysis lens, not as part of the claim itself:

- temporal DAG view: checks sequence, chronology, later audit, and causal-order plausibility.
- relation-force view: shows proximity, clusters, blockers, and narrative-pressure neighborhoods.
- both views preserve the same node ids, edge ids, frontier markers, falsifiers, and overclaim markers.
- arrowheads show audit-relation direction. They should not be read as direct physical causation unless the edge type explicitly says so.

## Legacy History Demos

- `demos/kpg_extinction/index.html`: K-Pg extinction flagship WikiCred demo.
- `data/legacy_cases/kpg_extinction/kpg_extinction_wikigraph_v0_5.json`: source-weighted K-Pg graph data.
- `demos/bronze_age_collapse/index.html`: Bronze Age Collapse research demo with UTF-8 standalone wrapper.
- `data/legacy_cases/bronze_age_collapse/bronze_age_collapse_wikigraph.json`: extracted Bronze Age Collapse graph data.
- `demos/uncertainty_workspace/index.html`: experimental temporal DAG for structuring unresolved uncertainty.
- `data/uncertainty_cases/seed_temporal_dag_case.json`: toy seed data for the Uncertainty Workspace DAG.
- `demos/ancient_history/legacy_hypothesis_credibility_v2.html`: original legacy history stress-test.
- `demos/ancient_history/legacy_hypothesis_credibility_v2_en.html`: English legacy history stress-test with the same three-panel force-graph interaction.
- `demos/ancient_history/wikigraph_v2_interactive.html`: embeddable wrapper for the English v2 widget.
- `data/legacy_cases/history_humanities/epistemic_wikigraph_v2.json`: display data for the v2 widget.
