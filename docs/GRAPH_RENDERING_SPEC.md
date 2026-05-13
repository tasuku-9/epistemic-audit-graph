# Graph Rendering Spec

## Concept

仮説・証拠・通説をノードとする力学グラフ。A/B/C/Xティア・反証条件・Mタグ・ナラティブ監査を持つ認識論的信憑性フレーム。

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
  }
}
```

## Rendering Rules

- Left panel: important claims only, meaning hypotheses and inference nodes.
- Center panel: Canvas force graph.
- Right panel: details, risks, falsifiers, source claims, and validator flags.
- Large circles: hypotheses and important inference claims.
- Small circles: evidence nodes.
- Diamonds: narrative, paper, or frame nodes.
- Hidden from graph but shown in detail: SourceClaim, Risk, Falsifier, Source, Assumption, ChangeRequest.
- Physics: nodes repel, edges behave like springs, and weak centering keeps the graph readable.
- Edge types: `sup`, `con`, `paper_conflict`, `narrative_conflict`, `frame_conflict`.
- Scores are provisional audit-support scores, not truth scores.

## Legacy History Demos

- `demos/kpg_extinction/index.html`: K-Pg extinction flagship WikiCred demo.
- `data/legacy_cases/kpg_extinction/kpg_extinction_wikigraph_v0_5.json`: source-weighted K-Pg graph data.
- `demos/bronze_age_collapse/index.html`: Bronze Age Collapse research demo with UTF-8 standalone wrapper.
- `data/legacy_cases/bronze_age_collapse/bronze_age_collapse_wikigraph.json`: extracted Bronze Age Collapse graph data.
- `demos/ancient_history/legacy_hypothesis_credibility_v2.html`: original legacy history stress-test.
- `demos/ancient_history/legacy_hypothesis_credibility_v2_en.html`: English legacy history stress-test with the same three-panel force-graph interaction.
- `demos/ancient_history/wikigraph_v2_interactive.html`: embeddable wrapper for the English v2 widget.
- `data/legacy_cases/history_humanities/epistemic_wikigraph_v2.json`: display data for the v2 widget.
