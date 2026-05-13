# Change Request Builder Prompt

Input: user free-text claim plus optional source/DOI.

Output: JSON matching `schemas/change_request.schema.json`.

Required behavior:

- If creating a hypothesis, include at least one falsification condition.
- If creating evidence, include or request a source claim.
- If the user makes a strong claim from analogy, correlation, benchmark, animal model, single event, or legal/normative material, add a RiskNode candidate.
- If the claim is not yet publishable, return `operation: create_hypothesis` with status-like notes in `ai_audit.warnings`; do not pretend it passed validation.

Template output:

```json
{
  "operation": "create_hypothesis",
  "reason_for_change": "...",
  "patch": {
    "hypothesis": {},
    "source_claims": [],
    "evidence": [],
    "falsifiers": [],
    "risks": [],
    "edges": []
  },
  "ai_audit": {
    "rules_checked": [
      "falsification_required",
      "source_claim_required",
      "source_claim_inference_separation",
      "domain_overclaim_check"
    ],
    "warnings": [],
    "missing_fields": []
  }
}
```
