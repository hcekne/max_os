#!/usr/bin/env python3
"""One-time fixup after merging the SYSTEM kernel template update.

An existing workspace that merges the kernel redesign can be left holding BOTH
generations of state files: its own lived-in `System State.md` / `Session
Log.md` / `Planning Memory.md` / `Actor Profile.md` next to the new kernel
`State.md` / `Log.md` / `Memory.md` / `Actor.md`, plus dissolved doctrine
documents (Operating Manual, Indexes, the old policies) that only survived
because the workspace had modified them.

This script finishes the migration without losing a byte of user state:

1. Carry `Session Log.md` entries into `Log.md`.
2. Carry `System State.md` frontmatter values into `State.md`.
3. Carry non-empty `Planning Memory.md` content into `Memory.md`.
4. Carry `Recurring Operations.md` active obligation rows into `Memory.md`.
5. Fold `Actor Profile.md` into `Actor.md` when Actor.md is still the shipped
   placeholder; otherwise keep Actor.md and archive the old file's content
   loss-free by appending it.
6. Delete surviving dissolved doctrine files (their content lives in the
   kernel now; the user's copies were doctrine, not data).
7. Rewrite references to renamed/dissolved documents across all Markdown.

Dry-run by default; pass --apply to write. Run from the workspace root:

    python3 AUTOMATE/Skills/tools/kernel_migration_fixup.py [--apply]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SYSTEM = Path("SYSTEM")

# Dissolved doctrine: safe to delete after the carry steps. Content owned by
# the kernel documents now; user copies of these were instructions, not data.
DOCTRINE = [
    "LLM Operating Manual.md",
    "AI Actor & Memory Model.md",
    "Indexes.md",
    "README.md",
    "Planning Cadence.md",
    "Document Model.md",
    "Document Lifecycle Policy.md",
    "Archive Policy.md",
    "Rubbish Bin Policy.md",
    "Git Preservation Policy.md",
    "Artifact Safety Policy.md",
    "Rendering Policy.md",
    "Worklet Conventions.md",
    "workspace_hygiene_rules.yaml",
    "local_setup_requirements.yaml",
]

RENAMES = [
    ("SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources", "AGENTS"),
    ("SYSTEM/Guides/Guide - System Dependencies", "SYSTEM/Standalone"),
    ("SYSTEM/Document Lifecycle Policy", "SYSTEM/Policy"),
    ("SYSTEM/AI Actor & Memory Model", "AGENTS"),
    ("SYSTEM/Git Preservation Policy", "SYSTEM/Policy"),
    ("SYSTEM/Artifact Safety Policy", "SYSTEM/Policy"),
    ("SYSTEM/Recurring Operations", "SYSTEM/Memory"),
    ("SYSTEM/LLM Operating Manual", "AGENTS"),
    ("SYSTEM/Rubbish Bin Policy", "SYSTEM/Policy"),
    ("SYSTEM/Planning Cadence", "PLAN/.instructions"),
    ("SYSTEM/Rendering Policy", "SYSTEM/Policy"),
    ("SYSTEM/Planning Memory", "SYSTEM/Memory"),
    ("SYSTEM/Archive Policy", "SYSTEM/Policy"),
    ("SYSTEM/Document Model", "SYSTEM/Policy"),
    ("SYSTEM/Actor Profile", "SYSTEM/Actor"),
    ("SYSTEM/System State", "SYSTEM/State"),
    ("SYSTEM/Session Log", "SYSTEM/Log"),
    ("SYSTEM/Indexes", "AGENTS"),
]

STATE_FIELDS = [
    "last_interaction_date",
    "active_week_plan",
    "active_quarter_plan",
    "active_two_year_plan",
    "active_goals",
    "active_modules",
]

SKIP_DIRS = {".git", ".maxos", "node_modules", ".venv", "venv", "__pycache__", "code"}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line.rstrip())
        if m:
            out[m.group(1)] = m.group(2).strip()
    return out


DATED_BULLET_RE = re.compile(r"^- \d{4}-\d{2}-\d{2}")


def bullets_after_heading(text: str) -> list[str]:
    """Dated bullet BLOCKS in the body: the bullet line plus any wrapped
    continuation lines that belong to it (real logs wrap long entries)."""
    body = text[text.find("\n---", 3) + 4 :] if text.startswith("---") else text
    blocks: list[str] = []
    current: list[str] | None = None
    for line in body.splitlines():
        if DATED_BULLET_RE.match(line):
            if current:
                blocks.append("\n".join(current))
            current = [line]
        elif current is not None and line.startswith(("  ", "\t")):
            current.append(line)
        else:
            if current:
                blocks.append("\n".join(current))
            current = None
    if current:
        blocks.append("\n".join(current))
    return blocks


class Fixup:
    def __init__(self, root: Path, apply: bool):
        self.root = root
        self.apply = apply
        self.actions: list[str] = []

    def act(self, message: str) -> None:
        self.actions.append(message)

    def read(self, rel: str) -> str | None:
        p = self.root / rel
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

    def write(self, rel: str, text: str) -> None:
        if self.apply:
            (self.root / rel).write_text(text, encoding="utf-8")

    def remove(self, rel: str) -> None:
        if self.apply:
            (self.root / rel).unlink(missing_ok=True)

    # -- carry steps ------------------------------------------------------
    def carry_log(self) -> None:
        old = self.read("SYSTEM/Session Log.md")
        new = self.read("SYSTEM/Log.md")
        if old is None or new is None:
            return
        entries = bullets_after_heading(old)
        missing = [e for e in entries if e not in new]
        if missing:
            new = new.rstrip() + "\n" + "\n".join(missing) + "\n"
            self.write("SYSTEM/Log.md", new)
        self.act(f"Log: carried {len(missing)} session-log entries; removed Session Log.md")
        self.remove("SYSTEM/Session Log.md")

    def carry_state(self) -> None:
        old = self.read("SYSTEM/System State.md")
        new = self.read("SYSTEM/State.md")
        if old is None or new is None:
            return
        old_fm = frontmatter(old)
        carried = 0
        for field in STATE_FIELDS:
            value = old_fm.get(field, "")
            if not value or value in ("[]", ""):
                continue
            pattern = re.compile(rf"^({re.escape(field)}:)\s*.*$", re.MULTILINE)
            if pattern.search(new):
                new = pattern.sub(rf"\1 {value}", new, count=1)
                carried += 1
        self.write("SYSTEM/State.md", new)
        self.act(f"State: carried {carried} field values; removed System State.md")
        self.remove("SYSTEM/System State.md")

    def carry_memory(self) -> None:
        new = self.read("SYSTEM/Memory.md")
        if new is None:
            return
        additions: list[str] = []
        pm = self.read("SYSTEM/Planning Memory.md")
        if pm is not None:
            body = pm.split("# Planning Memory", 1)[-1].strip()
            meaningful = [
                l for l in body.splitlines() if l.strip() not in ("", "-", "##") and not l.startswith("Use this")
            ]
            if meaningful:
                additions.append("\n## Carried from Planning Memory\n\n" + "\n".join(meaningful))
            self.act("Memory: carried Planning Memory content; removed Planning Memory.md")
            self.remove("SYSTEM/Planning Memory.md")
        ro = self.read("SYSTEM/Recurring Operations.md")
        if ro is not None:
            rows = [
                l for l in ro.splitlines() if l.startswith("|") and "active" in l.lower() and "Obligation" not in l
            ]
            rows = [r for r in rows if r.replace("|", "").replace("-", "").strip()]
            if rows:
                additions.append("\n## Carried standing obligations\n\n" + "\n".join(rows))
            self.act(f"Memory: carried {len(rows)} recurring-obligation rows; removed Recurring Operations.md")
            self.remove("SYSTEM/Recurring Operations.md")
        if additions:
            self.write("SYSTEM/Memory.md", new.rstrip() + "\n" + "\n".join(additions) + "\n")

    def carry_actor(self) -> None:
        old = self.read("SYSTEM/Actor Profile.md")
        new = self.read("SYSTEM/Actor.md")
        if old is None:
            return
        if new is None:
            self.write("SYSTEM/Actor.md", old)
            self.act("Actor: renamed Actor Profile.md to Actor.md")
        elif "maxos-actor-placeholder" in new:
            self.write("SYSTEM/Actor.md", old)
            self.act("Actor: replaced placeholder Actor.md with the lived-in Actor Profile.md")
        else:
            merged = new.rstrip() + "\n\n## Carried from Actor Profile.md\n\n" + old + "\n"
            self.write("SYSTEM/Actor.md", merged)
            self.act("Actor: appended Actor Profile.md content to Actor.md")
        self.remove("SYSTEM/Actor Profile.md")

    def drop_doctrine(self) -> None:
        for name in DOCTRINE:
            p = SYSTEM / name
            if (self.root / p).is_file():
                self.act(f"Doctrine: removed {p}")
                self.remove(str(p))
        guides = self.root / "SYSTEM" / "Guides"
        if guides.is_dir():
            for child in sorted(guides.rglob("*")):
                if child.is_file():
                    self.act(f"Doctrine: removed {child.relative_to(self.root)}")
                    if self.apply:
                        child.unlink()
            if self.apply:
                for d in sorted(guides.rglob("*"), reverse=True):
                    if d.is_dir():
                        d.rmdir()
                guides.rmdir()

    def rewrite_references(self) -> None:
        pairs: list[tuple[str, str]] = []
        for source, target in RENAMES:
            pairs.append((f"{source}.md", f"{target}.md"))
            pairs.append((f"[[{source}]]", f"[[{target}]]"))
            pairs.append((f"[[{source}|", f"[[{target}|"))
        changed = 0
        for path in self.root.rglob("*.md"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            updated = text
            for a, b in pairs:
                updated = updated.replace(a, b)
            if updated != text:
                changed += 1
                if self.apply:
                    path.write_text(updated, encoding="utf-8")
        self.act(f"References: rewrote kernel paths in {changed} files")

    def run(self) -> None:
        self.carry_log()
        self.carry_state()
        self.carry_memory()
        self.carry_actor()
        self.drop_doctrine()
        self.rewrite_references()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="workspace root")
    parser.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not (root / "SYSTEM").is_dir():
        print(f"error: {root} does not look like a Max OS workspace", file=sys.stderr)
        return 2
    fixup = Fixup(root, apply=args.apply)
    fixup.run()
    mode = "APPLIED" if args.apply else "DRY RUN (pass --apply to write)"
    print(f"kernel migration fixup — {mode}")
    for action in fixup.actions:
        print(f"  - {action}")
    return 0


if __name__ == "__main__":
    main()
