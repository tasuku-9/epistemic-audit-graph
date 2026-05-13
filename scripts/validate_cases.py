from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from epistemic_audit import load_domain_rules, validate_case  # noqa: E402


def iter_cases() -> list[Path]:
    return sorted((ROOT / "data" / "sample_cases").glob("*/*.json"))


def expected_status(case: dict) -> str:
    explicit = case.get("validator_expected_result")
    if explicit:
        return explicit
    legacy = case.get("expected_validation", {}).get("status", "PASS")
    return {
        "valid": "PASS_WITH_WARNINGS",
        "invalid": "REJECT",
        "PASS": "PASS",
        "PASS_WITH_WARNINGS": "PASS_WITH_WARNINGS",
        "REJECT": "REJECT",
        "FAIL_VALIDATION": "REJECT",
    }.get(legacy, legacy)


def status_matches(expected: str, actual: str) -> bool:
    if expected == "PASS_OR_PASS_WITH_WARNINGS":
        return actual in {"PASS", "PASS_WITH_WARNINGS"}
    if expected == "FAIL_VALIDATION":
        expected = "REJECT"
    return expected == actual


def write_frontend_assets(reports: list[dict], frontend_dir: Path) -> None:
    frontend_dir.mkdir(parents=True, exist_ok=True)
    case_manifest = []
    for report in reports:
        case_path = ROOT / report["path"]
        case = json.loads(case_path.read_text(encoding="utf-8"))
        case_manifest.append({
            "path": report["path"],
            "case_id": case.get("case_id"),
            "domain": case.get("domain"),
            "case_type": case.get("case_type", "mixed"),
            "title": case.get("title"),
            "summary": case.get("summary", ""),
            "user_input": case.get("user_input", ""),
            "japanese_title": case.get("japanese_title", ""),
            "key_warning_theme": case.get("key_warning_theme", ""),
            "expected": report["expected"],
            "actual_status": report["status"],
            "valid": report["valid"],
            "matched": report["matched"],
            "errors": report["errors"],
            "warnings": report["warnings"],
            "overclaim_flags": report.get("overclaim_flags", []),
            "m_tag_flags": report.get("m_tag_flags", []),
            "tier_mismatch_flags": report.get("tier_mismatch_flags", []),
        })

    (frontend_dir / "case_manifest.generated.json").write_text(
        json.dumps(case_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (frontend_dir / "validation_report.generated.json").write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print JSON report")
    parser.add_argument(
        "--write-frontend",
        action="store_true",
        help="write frontend/case_manifest.generated.json and frontend/validation_report.generated.json",
    )
    args = parser.parse_args()

    rules = load_domain_rules(ROOT / "data" / "domain_rules")
    reports = []
    failed = False

    for path in iter_cases():
        case = json.loads(path.read_text(encoding="utf-8"))
        result = validate_case(case, rules)
        expected = expected_status(case)
        matched = status_matches(expected, result.status)
        if not matched:
            failed = True
        reports.append({
            "path": path.relative_to(ROOT).as_posix(),
            "expected": expected,
            "matched": matched,
            **result.to_dict(),
        })

    if args.write_frontend:
        write_frontend_assets(reports, ROOT / "frontend")

    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            status = "PASS" if r["matched"] else "MISMATCH"
            print(f"[{status}] {r['path']} expected={r['expected']} actual={r['status']}")
            for e in r["errors"]:
                print(f"  ERROR: {e}")
            for w in r["warnings"]:
                print(f"  WARN:  {w}")
        print(f"\nChecked {len(reports)} cases.")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
