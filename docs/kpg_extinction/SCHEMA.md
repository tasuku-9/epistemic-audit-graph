# Schema v2.2-kpg Summary

Top-level collections:

- `meta`
- `wiki_pages`
- `claims`
- `evidence`
- `sources`
- `narratives`
- `questions`
- `relations`
- `composition_maps`
- `evaluation_model`

## Node types

### wiki_page
Represents a reusable wiki/article page. Pages contain local nodes and can import/export canonical nodes from other pages.

### claim
Represents a proposition to be evaluated. Key fields include `tier`, `status`, `fc`, `overclaim`, `evidence_refs`, `evaluation`, and `audit`.

### evidence
Represents a piece of evidence, not a claim. Key fields include `source_id`, `supports`, `contradicts`, `weight`, `directness`, `source_quality`, `independence`, and `isM`.

### source
Represents a source object shared by multiple evidence nodes.

### composition_map
A view assembled from multiple wiki pages and their imported/exported nodes.

## Relation types

`uses`, `asks`, `contains`, `imports`, `exports`, `supports`, `contradicts`, `conflicts_with`, `depends_on`, `cites`.

## Evaluation axes

- `credibility`: how well the claim is supported by current sources.
- `controversy`: how disputed or source-sensitive the claim is.
- `testability`: how clearly future evidence could strengthen or weaken the claim.
- `speculation`: how much the claim depends on inference, analogy, public shorthand, or incomplete evidence.
