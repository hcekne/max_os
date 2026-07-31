#!/usr/bin/env python3
"""
Max OS vault validator. Warn-only checks across the workspace.

Usage:
    python AUTOMATE/Skills/tools/check_vault.py            # auto-detects vault root
    python AUTOMATE/Skills/tools/check_vault.py --root .   # explicit root

Always exits 0. Findings are printed grouped by category.

Stdlib-only. Python 3.8+.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

# ---- Configuration ----------------------------------------------------

# Folders whose canonical notes must carry frontmatter with a `type:` field.
# Value is the glob applied beneath the folder (rglob), so client / project
# subfolder canonical notes are also covered.
FRONTMATTER_REQUIRED = {
    "KNOWLEDGE/People":        "*.md",
    "KNOWLEDGE/Organizations": "*.md",
    "KNOWLEDGE/Interactions":  "*.md",
    "PLAN/Goals":         "Goal - *.md",
    "AUTOMATE/Skills":        "Skill - *.md",
    "AUTOMATE/Workflows":     "Workflow - *.md",
    "KNOWLEDGE/Clients":       "Client - *.md",
    "KNOWLEDGE/Projects":      "Project - *.md",
    "SYSTEM/Templates":     "TPL - *.md",
}

# Filename conventions per folder. Each entry: (folder, expected description, regex).
# Applied to the immediate children of the folder only.
NAMING_RULES = [
    ("KNOWLEDGE/Projects",    "Project - *.md",    re.compile(r"^Project - .+\.md$")),
    ("PLAN/Goals",       "Goal - *.md",       re.compile(r"^Goal - .+\.md$")),
    ("AUTOMATE/Workflows",   "Workflow - *.md",   re.compile(r"^Workflow - .+\.md$")),
    ("AUTOMATE/Skills",      "Skill - *.md",      re.compile(r"^Skill - .+\.md$")),
    ("SYSTEM/Templates",   "TPL - *.md",        re.compile(r"^TPL - .+\.md$")),
    ("PLAN/Daily",       "YYYY-MM-DD.md",     re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")),
    ("KNOWLEDGE/Interactions","YYYY-MM-DD ... .md", re.compile(r"^\d{4}-\d{2}-\d{2}([ \-.].*)?\.md$")),
]

# Files exempt from naming rules and frontmatter checks.
EXEMPT_FILENAMES = {"README.md", "Index.md", ".instructions.md", "Archive Index.md"}

# Vault root .md files allowed.
ALLOWED_ROOT_MD = {"README.md", "AGENTS.md", "CLAUDE.md", "SKILLS.md"}

# Path parts that cause the whole subtree to be skipped (any descendant ignored).
SKIP_PATH_PARTS = {".git", ".venv", ".vscode", ".obsidian", ".trash", "node_modules", "__pycache__"}

# Folders where we don't run wiki-link or placement checks (historical / template content).
SKIP_LINK_CHECK_PREFIXES = ("SYSTEM/Cleaning/", "SYSTEM/Templates/")
SKIP_LINK_CHECK_PARTS = {"Archive"}

# Bootstrap docs that teach `[[wiki-link]]` syntax — example links there are not real.
WIKILINK_SKIP_FILES = {"README.md", "AGENTS.md", "CLAUDE.md"}

INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

# Canonical fields on System State frontmatter. Empty values are flagged.
# Yearly cadence is optional — fields commented out below until a yearly review note exists.
SYSTEM_STATE_FIELDS = [
    "last_interaction_date",
    "last_weekly_review_date",
    "last_monthly_review_date",
    "last_quarterly_review_date",
    # "last_yearly_review_date",  # optional until yearly cadence is active
    "active_week_plan",
    "active_month_note",
    "active_quarter_plan",
    # "active_year_note",         # optional until yearly cadence is active
    "active_two_year_plan",
]

WIKILINK_RE = re.compile(r"\[\[([^\[\]\n]+?)\]\]")
FENCE_RE = re.compile(r"^\s*```")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")


# ---- Helpers ----------------------------------------------------------

def is_under_skipped(rel: Path) -> bool:
    return any(part in SKIP_PATH_PARTS for part in rel.parts)


def walk_md(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.md"):
        if is_under_skipped(p.relative_to(root)):
            continue
        yield p


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def has_frontmatter_with_type(text: str) -> bool:
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end < 0:
        return False
    block = text[3:end]
    return any(line.lstrip().startswith("type:") for line in block.splitlines())


def parse_frontmatter(text: str) -> dict:
    """Top-level scalar keys only. Good enough for System State."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict = {}
    for line in text[3:end].splitlines():
        m = FRONTMATTER_KEY_RE.match(line.rstrip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


def strip_wikilink(target: str) -> str:
    target = target.split("|", 1)[0]
    target = target.split("#", 1)[0]
    return target.strip()


def build_basename_index(root: Path) -> dict:
    idx: dict = defaultdict(list)
    for p in walk_md(root):
        idx[p.stem].append(p.relative_to(root))
    return idx


def build_folder_set(root: Path) -> set:
    folders: set = set()
    for p in root.rglob("*"):
        if not p.is_dir():
            continue
        rel = p.relative_to(root)
        if is_under_skipped(rel):
            continue
        folders.add(p.name)
    return folders


def extract_wikilinks(text: str):
    """Yield (line_number, raw_target). Skips fenced code blocks and inline code spans."""
    in_fence = False
    for i, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        scrubbed = INLINE_CODE_RE.sub("", line)
        for m in WIKILINK_RE.finditer(scrubbed):
            yield i, m.group(1).strip()


def resolve_wikilink(target: str, root: Path, index: dict, folders: set) -> bool:
    t = strip_wikilink(target)
    if not t:
        return True
    # Trailing slash = folder-form reference.
    if t.endswith("/"):
        return (root / t.rstrip("/")).is_dir()
    if "/" in t:
        # Path-form. First try vault-root-relative.
        path_str = t if t.endswith(".md") else t + ".md"
        if (root / path_str).exists():
            return True
        if (root / t).is_dir():
            return True
        # Fall back to suffix match: any indexed .md whose path ends with this path.
        stem = Path(path_str).stem
        suffix = path_str.replace(os.sep, "/")
        for rel in index.get(stem, []):
            if str(rel).replace(os.sep, "/").endswith(suffix):
                return True
        return False
    # Bare basename: matches an .md by stem, or matches a folder name in the vault.
    if index.get(t):
        return True
    return t in folders


# ---- Checks -----------------------------------------------------------

def check_frontmatter(root: Path, findings: list) -> None:
    for folder, pattern in FRONTMATTER_REQUIRED.items():
        folder_path = root / folder
        if not folder_path.exists():
            continue
        for p in folder_path.rglob(pattern):
            rel = p.relative_to(root)
            if is_under_skipped(rel):
                continue
            if p.name in EXEMPT_FILENAMES:
                continue
            if any(part == "Archive" for part in rel.parts):
                continue
            text = read_text(p)
            if not has_frontmatter_with_type(text):
                findings.append(("frontmatter", str(rel), "missing frontmatter or `type:` field"))


def check_wikilinks(root: Path, index: dict, folders: set, findings: list) -> None:
    for p in walk_md(root):
        rel = p.relative_to(root)
        rel_str = str(rel).replace(os.sep, "/")
        if any(rel_str.startswith(prefix) for prefix in SKIP_LINK_CHECK_PREFIXES):
            continue
        if any(part in SKIP_LINK_CHECK_PARTS for part in rel.parts):
            continue
        if len(rel.parts) == 1 and rel.name in WIKILINK_SKIP_FILES:
            continue
        text = read_text(p)
        for lineno, target in extract_wikilinks(text):
            if not resolve_wikilink(target, root, index, folders):
                t = strip_wikilink(target)
                findings.append(("wikilink", f"{rel}:{lineno}", f"unresolved [[{t}]]"))


def check_naming(root: Path, findings: list) -> None:
    for folder, expected, rx in NAMING_RULES:
        folder_path = root / folder
        if not folder_path.exists():
            continue
        for p in folder_path.glob("*.md"):
            if not p.is_file():
                continue
            if p.name in EXEMPT_FILENAMES:
                continue
            if not rx.match(p.name):
                rel = p.relative_to(root)
                findings.append(("naming", str(rel), f"expected {expected}"))


def check_hygiene(root: Path, findings: list) -> None:
    # Stray .DS_Store and empty .md placeholders anywhere outside skipped subtrees.
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if is_under_skipped(rel):
            continue
        if p.is_file():
            if p.name == ".DS_Store":
                findings.append(("hygiene", str(rel), "stray .DS_Store"))
            elif p.suffix == ".md" and p.stat().st_size == 0:
                findings.append(("hygiene", str(rel), "empty .md placeholder"))

    # Root-level .md files outside the allowed control-file set.
    for p in root.glob("*.md"):
        if p.name not in ALLOWED_ROOT_MD:
            findings.append(("hygiene", p.name,
                             f"root-level .md not in allowed set {sorted(ALLOWED_ROOT_MD)}"))

def check_system_state(root: Path, index: dict, folders: set, findings: list) -> None:
    p = root / "SYSTEM" / "System State.md"
    if not p.exists():
        findings.append(("system-state", "SYSTEM/System State.md", "missing"))
        return
    fm = parse_frontmatter(read_text(p))
    for field in SYSTEM_STATE_FIELDS:
        value = fm.get(field, "").strip()
        if not value:
            findings.append(("system-state", "System State frontmatter", f"`{field}` is empty"))
            continue
        for m in WIKILINK_RE.finditer(value):
            if not resolve_wikilink(m.group(1), root, index, folders):
                t = strip_wikilink(m.group(1))
                findings.append(("system-state", "System State frontmatter",
                                 f"`{field}` -> unresolved [[{t}]]"))


# ---- Main -------------------------------------------------------------

def locate_root(start: Path) -> Path | None:
    for p in [start, *start.parents]:
        if (p / "SYSTEM").is_dir():
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Max OS vault validator (warn-only)")
    ap.add_argument("--root", default=None,
                    help="Vault root (default: ascend from CWD until a SYSTEM/ is found)")
    args = ap.parse_args()

    if args.root:
        root = Path(args.root).resolve()
        if not (root / "SYSTEM").is_dir():
            print(f"error: {root} does not contain SYSTEM/", file=sys.stderr)
            return 0
    else:
        found = locate_root(Path.cwd().resolve())
        if found is None:
            print("error: could not locate vault root (no SYSTEM/ found from CWD upward)",
                  file=sys.stderr)
            return 0
        root = found

    index = build_basename_index(root)
    folders = build_folder_set(root)
    findings: list = []
    check_frontmatter(root, findings)
    check_wikilinks(root, index, folders, findings)
    check_naming(root, findings)
    check_hygiene(root, findings)
    check_system_state(root, index, folders, findings)

    by_cat: dict = defaultdict(list)
    for cat, where, msg in findings:
        by_cat[cat].append((where, msg))

    total = sum(len(v) for v in by_cat.values())
    print(f"# Vault check report")
    print(f"Root: {root}")
    print(f"Findings: {total}\n")

    order = ["frontmatter", "wikilink", "naming", "hygiene", "system-state"]
    for cat in order:
        items = by_cat.get(cat, [])
        print(f"## {cat} ({len(items)})")
        if not items:
            print("(clean)\n")
            continue
        if cat == "wikilink":
            counter: dict = defaultdict(int)
            for _, msg in items:
                m = re.search(r"\[\[(.+?)\]\]", msg)
                if m:
                    counter[m.group(1)] += 1
            top = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:20]
            print("Top missing targets (frequency × target):")
            for target, count in top:
                print(f"- {count:3d}× [[{target}]]")
            print()
            print(f"Full list ({len(items)} entries):")
        for where, msg in items[:200]:
            print(f"- {where} — {msg}")
        if len(items) > 200:
            print(f"... ({len(items) - 200} more not shown)")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
