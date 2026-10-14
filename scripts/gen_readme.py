#!/usr/bin/env python3
"""Generate README.md from the skills on disk.

Skills live as top-level folders in the repo root (each contains a SKILL.md).
This scans them, reads each SKILL.md's name + description, groups by the category
map below, and updates the catalog and counts in the existing README. Shared
branding, setup instructions and manually maintained sections are preserved.

Usage:
    python3 scripts/gen_readme.py
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "JayRHa/agent-skills"

# Folders at the repo root that are NOT skills.
NON_SKILL_DIRS = {"scripts", ".github", ".git"}

CATEGORY = {
    "Engineering": ["code-reviewer","unit-test-author","refactoring-guide","debug-detective","api-designer","regex-architect","sql-optimizer","dockerfile-pro","git-workflow","dependency-upgrader","performance-profiler","error-handling-patterns"],
    "DevOps & Cloud": ["github-actions-builder","terraform-module-author","kubernetes-manifest-author","nginx-config-pro","incident-postmortem","observability-setup","secrets-manager","bash-script-hardening","cron-scheduler","aws-cost-optimizer"],
    "Data & ML": ["pandas-data-cleaning","sql-schema-designer","data-pipeline-architect","chart-chooser","json-schema-author","ab-test-analyzer","prompt-engineer","rag-pipeline-designer"],
    "Writing & Communication": ["technical-writer","readme-generator","changelog-keeper","blog-post-writer","release-notes-writer","adr-author","email-composer","meeting-summarizer","proofreader","api-docs-writer","public-speaking-coach","mermaid-diagram-builder","x-twitter-scraper"],
    "Productivity & Business": ["okr-writer","swot-analyzer","project-planner","decision-matrix","presentation-builder","user-story-writer","competitive-analysis","job-description-writer"],
    "Security": ["threat-modeler","security-auditor","secure-password-policy","gdpr-data-mapper","vulnerability-triage","secure-code-review"],
    "Career & Job Search": ["resume-writer","cover-letter-writer","interview-prep","salary-negotiator"],
    "Learning": ["concept-explainer","flashcard-generator","study-plan-builder","language-tutor","book-summarizer"],
    "Health & Wellness": ["meal-plan-builder","workout-planner","habit-builder"],
    "Home & Lifestyle": ["trip-planner","personal-budget-planner","event-planner","gift-advisor"],
}

EMOJI = {
    "Engineering":"🧑‍💻","DevOps & Cloud":"☁️","Data & ML":"📊","Writing & Communication":"✍️",
    "Productivity & Business":"📈","Security":"🔒","Career & Job Search":"💼","Learning":"🎓",
    "Health & Wellness":"💪","Home & Lifestyle":"🏡",
}


def read_desc(folder: str) -> str:
    md = (ROOT / folder / "SKILL.md").read_text(encoding="utf-8")
    parts = md.split("---", 2)
    fm = parts[1] if len(parts) >= 3 else md
    desc, key = "", None
    for line in fm.splitlines():
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            if key == "description":
                val = m.group(2).strip()
                # Ignore YAML block-scalar indicators (>, >-, |, |-, etc.).
                desc = "" if re.fullmatch(r"[>|][+-]?", val) else val
        elif key == "description" and line.strip():
            desc += (" " if desc else "") + line.strip()
    # first sentence only, for a tight table cell
    first = re.split(r"(?<=[.])\s+(?=[A-Z])", desc.strip())[0]
    return first.strip()


def existing(folder: str) -> bool:
    return (ROOT / folder / "SKILL.md").is_file()


def count_files(folder: str) -> int:
    d = ROOT / folder
    return sum(1 for p in d.rglob("*") if p.is_file()) if d.is_dir() else 0


def main() -> int:
    present = {
        p.name for p in ROOT.iterdir()
        if p.is_dir() and p.name not in NON_SKILL_DIRS and p.name != "0-template"
        and (p / "SKILL.md").is_file()
    }
    total = sum(1 for c in CATEGORY.values() for f in c if f in present)
    total_files = sum(count_files(f) for c in CATEGORY.values() for f in c if f in present)
    used_categories = [c for c in CATEGORY if any(f in present for f in CATEGORY[c])]

    # Warn about skills present on disk but not mapped to a category.
    mapped = {f for c in CATEGORY.values() for f in c}
    unmapped = sorted(present - mapped)
    if unmapped:
        print(f"warning: {len(unmapped)} skill(s) not in any category: {', '.join(unmapped)}")

    # Keep the curated introduction, setup and shared branding unchanged.
    # Only the catalog and its inventory counts are generated.
    readme = ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    catalog = ["<!-- skill-catalog:start -->", "## Skill Catalog", ""]
    for cat in CATEGORY:
        rows = [folder for folder in CATEGORY[cat] if folder in present]
        if not rows:
            continue
        catalog.extend([f"### {cat} ({len(rows)})", "",
                        "| Skill | What it does |", "| --- | --- |"])
        for folder in rows:
            description = read_desc(folder).replace("|", "\\|")
            catalog.append(f"| [`{folder}`](./{folder}) | {description} |")
        catalog.append("")
    catalog.append("<!-- skill-catalog:end -->")
    replacement = "\n".join(catalog) + "\n\n"
    marked = r"(?ms)^<!-- skill-catalog:start -->.*?^<!-- skill-catalog:end -->\s*"
    unmarked = r"(?ms)^## Skill Catalog\s*\n.*?(?=^## |\Z)"
    pattern = marked if "<!-- skill-catalog:start -->" in current else unmarked
    updated, count = re.subn(pattern, lambda _: replacement, current, count=1)
    if count != 1:
        raise RuntimeError("README.md must contain exactly one skill catalog section")
    updated = re.sub(
        r"`\d+ Skills` · `\d+ Categories` · `\d+\+? Files`",
        f"`{total} Skills` · `{len(used_categories)} Categories` · `{total_files} Files`",
        updated,
        count=1,
    )
    readme.write_text(updated, encoding="utf-8")
    print(f"Updated catalog: {total} skills, {len(used_categories)} categories, {total_files} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
