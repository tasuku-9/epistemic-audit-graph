from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from epistemic_audit import load_domain_rules, validate_case  # noqa: E402


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules = load_domain_rules(ROOT / "data" / "domain_rules")

    def load_case(self, path: str):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    def iter_cases(self, pattern: str):
        return sorted((ROOT / "data" / "sample_cases").glob(pattern))

    def test_all_six_good_cases_pass_with_warnings_or_pass(self):
        paths = self.iter_cases("*/good_*.json")
        self.assertEqual(6, len(paths))
        for path in paths:
            with self.subTest(path=path):
                case = json.loads(path.read_text(encoding="utf-8"))
                result = validate_case(case, self.rules)
                self.assertIn(result.status, {"PASS", "PASS_WITH_WARNINGS"}, result.to_dict())

    def test_all_six_overclaim_cases_reject(self):
        paths = self.iter_cases("*/overclaim_*.json")
        self.assertEqual(6, len(paths))
        for path in paths:
            with self.subTest(path=path):
                case = json.loads(path.read_text(encoding="utf-8"))
                result = validate_case(case, self.rules)
                self.assertEqual("REJECT", result.status, result.to_dict())

    def test_missing_falsifier_causes_rejection(self):
        case = self.load_case("data/sample_cases/social_science/good_observational_association_scoped.json")
        modified = copy.deepcopy(case)
        modified["nodes"] = [n for n in modified["nodes"] if n["node_type"] != "falsifier"]
        modified["edges"] = [e for e in modified["edges"] if e["edge_type"] != "falsified_by"]
        for node in modified["nodes"]:
            if node["node_type"] == "hypothesis":
                node["falsification_conditions"] = []
        result = validate_case(modified, self.rules)
        self.assertEqual("REJECT", result.status)
        self.assertTrue(any("falsification" in e or "FalsifierNode" in e for e in result.errors))

    def test_m_tag_only_a_tier_claim_is_rejected(self):
        case = self.load_case("data/sample_cases/history_humanities/good_egm_jomon_dotaku_kiki_scoped.json")
        modified = copy.deepcopy(case)
        for node in modified["nodes"]:
            if node["id"] == "h_social_reorganization":
                node["tier"] = "A"
            if node["node_type"] == "evidence":
                node["m_tag"] = True
                node["directness"] = "analogy"
                node["evidence_tags"] = ["mythic_text"]
        result = validate_case(modified, self.rules)
        self.assertEqual("REJECT", result.status)
        self.assertIn("m_tag_only_a_tier", result.m_tag_flags)

    def test_source_claim_inference_collapse_is_rejected(self):
        case = self.load_case("data/sample_cases/ai_computer_science/good_benchmark_scoped.json")
        modified = copy.deepcopy(case)
        hypothesis_id = next(n["id"] for n in modified["nodes"] if n["node_type"] == "hypothesis")
        evidence_id = next(n["id"] for n in modified["nodes"] if n["node_type"] == "evidence")
        modified["edges"].append({"from": evidence_id, "to": hypothesis_id, "edge_type": "supports", "strength": 0.8})
        result = validate_case(modified, self.rules)
        self.assertEqual("REJECT", result.status)
        self.assertTrue(any("EvidenceNode" in fix or "InferenceNode" in fix for fix in result.suggested_fixes))

    def assert_case_rejects_with_flag(self, path: str, expected_flag: str):
        case = self.load_case(path)
        result = validate_case(case, self.rules)
        self.assertEqual("REJECT", result.status, result.to_dict())
        self.assertIn(expected_flag, result.overclaim_flags, result.to_dict())

    def test_benchmark_to_agi_claim_is_rejected(self):
        self.assert_case_rejects_with_flag(
            "data/sample_cases/ai_computer_science/overclaim_benchmark_to_agi_rejected.json",
            "benchmark_overgeneralization",
        )

    def test_legal_to_ethical_correctness_claim_is_rejected(self):
        self.assert_case_rejects_with_flag(
            "data/sample_cases/law_policy_ethics/overclaim_legal_to_effective_ethical_rejected.json",
            "normative_to_empirical",
        )

    def test_animal_to_human_clinical_claim_is_rejected(self):
        self.assert_case_rejects_with_flag(
            "data/sample_cases/biomedicine/overclaim_mouse_to_human_rejected.json",
            "animal_to_human",
        )

    def test_correlation_to_causation_claim_is_rejected(self):
        self.assert_case_rejects_with_flag(
            "data/sample_cases/social_science/overclaim_correlation_to_causation_rejected.json",
            "correlation_to_causation",
        )

    def test_single_event_climate_proof_claim_is_rejected(self):
        self.assert_case_rejects_with_flag(
            "data/sample_cases/climate_earth/overclaim_single_event_model_proof_rejected.json",
            "single_event_to_trend",
        )

    def test_invalid_claim_state_status_is_rejected(self):
        case = self.load_case("data/sample_cases/social_science/overclaim_correlation_to_causation_rejected.json")
        modified = copy.deepcopy(case)
        for node in modified["nodes"]:
            if node.get("id") == "h_cause":
                node["claim_state"]["status"] = "winning_argument"
                node["claim_state"]["evidence_challenges"][0]["status"] = "done_by_user"
        result = validate_case(modified, self.rules)
        self.assertEqual("REJECT", result.status)
        self.assertTrue(any("claim_state.status" in e for e in result.errors))
        self.assertTrue(any("evidence_challenge" in e and "invalid status" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()
