# scripts/orchestrator/check_coverage.py
import os, sys, json, pathlib, re

REPO = pathlib.Path(__file__).resolve().parents[2]

def exists(*parts) -> bool:
    return (REPO.joinpath(*parts)).exists()

def file_contains(path, needle: str) -> bool:
    p = REPO / path
    if not p.exists(): return False
    try:
        return needle in p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False

def count_index(path):
    p = REPO / path
    if not p.exists(): return 0
    try:
        return len(json.loads(p.read_text(encoding="utf-8")))
    except Exception:
        return 0

def main():
    # Requirements we can check automatically right now
    results = {}

    # CI workflows presence
    req_files = {
        "R-CI-LINT": ".github/workflows/ci-lint.yml",
        "R-CI-TEST": ".github/workflows/ci-test.yml",
        "R-CI-SECURITY": ".github/workflows/ci-security.yml",
        "R-CI-DEPS-LICENSE": ".github/workflows/ci-deps-license.yml",
        "R-CI-SMOKE": ".github/workflows/ci-smoke.yml",
        "R-CI-BUILD-PREVIEW": ".github/workflows/ci-build-push.yml",
    }
    for rid, rel in req_files.items():
        results[rid] = (exists(*rel.split("/")), f"{rel} present")

    # SAFE-MODE guard in preview build
    results["R-SAFE-MODE-GUARD"] = (
        file_contains(".github/workflows/ci-build-push.yml", "ops/flags/safe-mode.json"),
        "ci-build-push.yml checks SAFE-MODE flag"
    )

    # PR template sections
    pr_tmpl = ".github/pull_request_template.md"
    results["R-PR-TEMPLATE-EXISTS"] = (exists(*pr_tmpl.split("/")), "PR template present")
    results["R-PR-ACCESS-SECTION"] = (file_contains(pr_tmpl, "Access & Traceability"), "PR template has Access & Traceability")
    results["R-PR-BLUEPRINT-SECTION"] = (file_contains(pr_tmpl, "Blueprint Concordance"), "PR template has Blueprint Concordance")

    # Knowledge indexes (non-technical + technical)
    results["R-INDEX-NT"] = (count_index("docs/blueprints/nt-index.json") > 0, "Non-technical index generated")
    results["R-INDEX-TD"] = (count_index("docs/blueprints/td-index.json") > 0, "Technical index generated")

    # Normalized plain outputs exist
    plain_dir = REPO / "docs" / "blueprints" / "plain"
    results["R-NORMALIZED-PLAIN"] = (plain_dir.exists() and any(plain_dir.glob("*.md")), "plain/*.md exist")

    # Produce HEALTH.md
    lines = ["# Orchestrator Health", ""]
    fail = False
    for rid, (ok, msg) in sorted(results.items()):
        lines.append(f"- **{rid}** — {'✅ PASS' if ok else '❌ FAIL'} — {msg}")
        if not ok: fail = True
    out = REPO / "docs" / "orchestrator" / "HEALTH.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out.relative_to(REPO))

    sys.exit(1 if fail else 0)

if __name__ == "__main__":
    main()
