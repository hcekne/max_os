#!/usr/bin/env python3
"""One-time fixup after merging the SYSTEM kernel template update.

An existing workspace that merges the kernel redesign can be left holding BOTH
generations of state files: its own lived-in `System State.md` / `Session
Log.md` / `Planning Memory.md` / `Actor Profile.md` next to the new kernel
`State.md` / `Log.md` / `Memory.md` / `Actor.md`, plus dissolved doctrine
documents (Operating Manual, Indexes, the old policies) that only survived
because the workspace had modified them.

This script finishes the migration without losing user material. Every retired
source file is moved byte-for-byte into
`SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone/` before its old
path disappears; recognized state is also carried into the active kernel.

1. Carry `Session Log.md` entries into `Log.md`.
2. Carry `System State.md` frontmatter values into `State.md`.
3. Carry non-empty `Planning Memory.md` content into `Memory.md`.
4. Carry `Recurring Operations.md` active obligation rows into `Memory.md`.
5. Fold `Actor Profile.md` into `Actor.md` when Actor.md is still the shipped
   placeholder; otherwise keep Actor.md and archive the old file's content
   loss-free by appending it.
6. Archive surviving dissolved doctrine and guides for owner review.
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

# Retired doctrine. Preserve every surviving copy before removing its old path;
# owner-specific rules may have been added even when the template had a newer
# canonical destination.
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
    "Standalone.md",
    "Worklet Conventions.md",
    "workspace_hygiene_rules.yaml",
    "local_setup_requirements.yaml",
]

RENAMES = [
    ("SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources", "AGENTS"),
    (
        "SYSTEM/Guides/Guide - System Dependencies",
        "AUTOMATE/Skills/Skill - Set Up Standalone MaxOS",
    ),
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
    ("SYSTEM/Standalone", "AUTOMATE/Skills/Skill - Set Up Standalone MaxOS"),
    ("SYSTEM/Indexes", "AGENTS"),
]

TITLE_RENAMES = [
    ("Actor Profile", "SYSTEM/Actor"),
    ("System State", "SYSTEM/State"),
    ("Session Log", "SYSTEM/Log"),
    ("Planning Memory", "SYSTEM/Memory"),
    ("Recurring Operations", "SYSTEM/Memory"),
    ("Planning Cadence", "PLAN/.instructions"),
    ("LLM Operating Manual", "AGENTS"),
    ("Standalone", "AUTOMATE/Skills/Skill - Set Up Standalone MaxOS"),
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
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")

PLANNING_MEMORY_DEFAULTS = {
    "Use this as the persistent memory for how to plan better over time.",
    "- Keep plans realistic relative to known capacity.",
    "- Tie weekly commitments to quarterly priorities.",
    "- Leave buffer for incoming client work and urgent requests.",
    "- 2026-02-24: Created planning system baseline.",
}


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
        source = self.root / rel
        if not source.is_file():
            return
        archive = self.root / "SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone" / rel
        self.act(f"Preserved exact source at {archive.relative_to(self.root)}")
        if not self.apply:
            return
        archive.parent.mkdir(parents=True, exist_ok=True)
        if archive.exists():
            if archive.read_bytes() == source.read_bytes():
                source.unlink()
                return
            counter = 1
            candidate = archive
            while candidate.exists():
                candidate = archive.with_name(f"{archive.stem} ({counter}){archive.suffix}")
                counter += 1
            archive = candidate
        source.replace(archive)

    def links_exist(self, value: str) -> bool:
        for target in WIKILINK_RE.findall(value):
            relative = Path(target.strip().removesuffix(".md") + ".md")
            candidate = (self.root / relative).resolve(strict=False)
            try:
                candidate.relative_to(self.root)
            except ValueError:
                return False
            if not candidate.is_file():
                return False
        return True

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
            if not value or value == "[]" or not self.links_exist(value):
                continue
            pattern = re.compile(rf"^({re.escape(field)}:)[ \t]*[^\r\n]*$", re.MULTILINE)
            if pattern.search(new):
                new = pattern.sub(lambda match: f"{match.group(1)} {value}", new, count=1)
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
                line
                for line in body.splitlines()
                if line.strip() not in ("", "-", "##")
                and line.strip() not in PLANNING_MEMORY_DEFAULTS
            ]
            if meaningful:
                additions.append("\n## Carried from Planning Memory\n\n" + "\n".join(meaningful))
            self.act("Memory: carried Planning Memory content; removed Planning Memory.md")
            self.remove("SYSTEM/Planning Memory.md")
        ro = self.read("SYSTEM/Recurring Operations.md")
        if ro is not None:
            active_section = (
                ro.split("## Active Recurring Obligations", 1)[1].split("\n## ", 1)[0]
                if "## Active Recurring Obligations" in ro
                else ""
            )
            rows = []
            for line in active_section.splitlines():
                if not line.startswith("|"):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) == 6 and cells[2].lower() == "active":
                    rows.append(
                        f"| {cells[0]} | {cells[1]} | {cells[3]} | {cells[4]} | {cells[5]} |"
                    )
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
        else:
            body = old
            if body.startswith("---"):
                end = body.find("\n---", 3)
                if end >= 0:
                    body = body[end + 4 :]
            body = re.sub(r"^# Actor Profile[^\n]*\n?", "", body.lstrip(), count=1).strip()
            merged = new.rstrip()
            if body and body not in new:
                merged += "\n\n## Carried from legacy Actor Profile\n\n" + body
            merged += "\n"
            self.write("SYSTEM/Actor.md", merged)
            self.act("Actor: appended Actor Profile.md content to Actor.md")
        self.remove("SYSTEM/Actor Profile.md")

    def drop_doctrine(self) -> None:
        for name in DOCTRINE:
            p = SYSTEM / name
            if (self.root / p).is_file():
                self.act(f"Doctrine: retired {p}")
                self.remove(str(p))
        guides = self.root / "SYSTEM" / "Guides"
        if guides.is_dir():
            for child in sorted(guides.rglob("*")):
                if child.is_file():
                    relative = child.relative_to(self.root).as_posix()
                    self.act(f"Guide: retired {relative}")
                    self.remove(relative)
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
        for source, target in TITLE_RENAMES:
            pairs.append((f"[[{source}]]", f"[[{target}]]"))
            pairs.append((f"[[{source}|", f"[[{target}|"))
        changed = 0
        for path in self.root.rglob("*.md"):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            relative = path.relative_to(self.root).as_posix()
            if relative.startswith("SYSTEM/Cleaning/Archive/System Kernel Migration/"):
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
        if self.actions:
            proposal = self.root / "SYSTEM/Proposals/Proposal - Review Standalone Kernel Migration.md"
            if self.apply and not proposal.exists():
                proposal.parent.mkdir(parents=True, exist_ok=True)
                proposal.write_text(
                    "---\ntype: proposal\nstatus: proposed\n---\n\n"
                    "# Review standalone SYSTEM kernel migration\n\n"
                    "Legacy files were preserved byte-for-byte under "
                    "`SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone/`. "
                    "Review owner-specific rules there and copy only still-current material "
                    "into `SYSTEM/Memory.md` or the relevant folder instructions.\n",
                    encoding="utf-8",
                )


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
