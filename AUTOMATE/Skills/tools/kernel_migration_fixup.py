#!/usr/bin/env python3
"""Finish a lossless legacy-workspace upgrade after merging the template.

The template merge moves numbered or `WORKSPACE/` layouts into the five current
roots and replaces the old SYSTEM instruction graph with the closed kernel. Git
may stop on safe directory-relocation and customized-kernel conflicts; this tool
can resolve only those recognized shapes and refuses everything else.

Every retired source file is moved byte-for-byte into
`SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone/` before its old
path disappears. User folders are moved into their current destinations,
recognized state is carried into the active kernel, and active references are
rewritten. The archive itself remains byte-for-byte unchanged.

1. Carry `Session Log.md` entries into `Log.md`.
2. Carry `System State.md` frontmatter values into `State.md`.
3. Carry non-empty `Planning Memory.md` content into `Memory.md`.
4. Carry `Recurring Operations.md` active obligation rows into `Memory.md`.
5. Fold `Actor Profile.md` into `Actor.md` when Actor.md is still the shipped
   placeholder; otherwise keep Actor.md and archive the old file's content
   loss-free by appending it.
6. Move numbered and custom roots into the current five-root layout.
7. Archive surviving dissolved doctrine and guides for owner review.
8. Rewrite active references to moved and dissolved documents.

Dry-run by default; pass --apply to write. Run from the workspace root:

    python3 AUTOMATE/Skills/tools/kernel_migration_fixup.py \
      --resolve-known-conflicts [--apply]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ARCHIVE_ROOT = Path("SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone")

LEGACY_PATHS = (
    ("10_Action_Center/Agent_Inbox", "ACTION CENTER/Agent Inbox"),
    ("10_Action_Center/My_Inbox", "ACTION CENTER/My Inbox"),
    ("10_Action_Center/Outbox", "ACTION CENTER/Outbox"),
    ("09_Planning/Two-Year", "PLAN/Two-Year"),
    ("12_Workflows/Automations/artifacts", "AUTOMATE/Workflows/Automations/artifacts"),
    ("12_Workflows/Automations", "AUTOMATE/Workflows/Automations"),
    ("00_System", "SYSTEM"),
    ("01_People", "KNOWLEDGE/People"),
    ("02_Organizations", "KNOWLEDGE/Organizations"),
    ("03_Clients", "KNOWLEDGE/Clients"),
    ("04_Projects", "KNOWLEDGE/Projects"),
    ("05_Content", "KNOWLEDGE/Content"),
    ("06_Interactions", "KNOWLEDGE/Interactions"),
    ("07_Daily", "PLAN/Daily"),
    ("08_Todos", "PLAN/Todos"),
    ("09_Planning", "PLAN"),
    ("10_Action_Center", "ACTION CENTER"),
    ("10_Inbox", "ACTION CENTER/Agent Inbox"),
    ("11_Notes", "KNOWLEDGE/Notes"),
    ("12_Workflows", "AUTOMATE/Workflows"),
    ("13_Goals", "PLAN/Goals"),
    ("14_Guides", "SYSTEM/Guides"),
    ("15_Skills", "AUTOMATE/Skills"),
    ("16_Cleaning", "SYSTEM/Cleaning"),
    ("17_Outbox", "ACTION CENTER/Outbox"),
    ("20_Modules", "AUTOMATE/Modules"),
    ("99_Templates", "SYSTEM/Templates"),
    ("Storage References", "SYSTEM/Storage References"),
    ("WORKSPACE", "KNOWLEDGE"),
)

CANONICAL_ROOTS = {"ACTION CENTER", "AUTOMATE", "KNOWLEDGE", "PLAN", "SYSTEM"}
RESERVED_ROOTS = {
    ".git",
    ".github",
    ".githooks",
    ".maxos",
    ".claude",
    ".codex",
    ".gemini",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "node_modules",
    "code",
    *CANONICAL_ROOTS,
}

REQUIRED_KERNEL_FILES = (
    "AGENTS.md",
    ".gemini/GEMINI.md",
    "SYSTEM/Actor.md",
    "SYSTEM/Log.md",
    "SYSTEM/Memory.md",
    "SYSTEM/Policy.md",
    "SYSTEM/State.md",
)
ALLOWED_SYSTEM_FILES = {
    ".instructions.md",
    "Actor.md",
    "Log.md",
    "Memory.md",
    "Policy.md",
    "State.md",
    "public_template_denylist.example.txt",
}
ALLOWED_SYSTEM_DIRS = {"Cleaning", "Proposals", "Storage References", "Templates"}

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

LEGACY_KERNEL_NAMES = frozenset(
    {
        *DOCTRINE,
        "Actor Profile.md",
        "Planning Memory.md",
        "Recurring Operations.md",
        "Session Log.md",
        "System State.md",
    }
)
KERNEL_CARRY_TARGETS = {
    "Actor Profile.md": "SYSTEM/Actor.md",
    "Planning Memory.md": "SYSTEM/Memory.md",
    "Recurring Operations.md": "SYSTEM/Memory.md",
    "Session Log.md": "SYSTEM/Log.md",
    "System State.md": "SYSTEM/State.md",
}


def safe_path(root: Path, relative: str | Path) -> Path:
    value = PurePosixPath(str(relative).replace("\\", "/"))
    if value.is_absolute() or ".." in value.parts:
        raise ValueError(f"unsafe workspace path: {relative}")
    candidate = (root / Path(*value.parts)).resolve(strict=False)
    candidate.relative_to(root.resolve())
    return candidate


def map_legacy_path(relative: str) -> str:
    for source, target in LEGACY_PATHS:
        if relative == source:
            return target
        prefix = f"{source}/"
        if relative.startswith(prefix):
            return f"{target}/{relative.removeprefix(prefix)}"
    return relative


def git_bytes(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def unmerged_index(root: Path) -> dict[str, dict[int, str]]:
    result = git_bytes(root, "ls-files", "-u", "-z")
    if result.returncode != 0:
        raise ValueError(
            result.stderr.decode(errors="replace").strip() or "git index read failed"
        )
    entries: dict[str, dict[int, str]] = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        parts = metadata.split()
        if not separator or len(parts) != 3:
            raise ValueError("unexpected unmerged Git index record")
        path = raw_path.decode("utf-8", errors="surrogateescape")
        entries.setdefault(path, {})[int(parts[2])] = parts[1].decode("ascii")
    return entries


def head_blob_paths(root: Path) -> dict[str, tuple[str, ...]]:
    result = git_bytes(root, "ls-tree", "-r", "-z", "HEAD")
    if result.returncode != 0:
        raise ValueError(
            result.stderr.decode(errors="replace").strip() or "HEAD tree read failed"
        )
    paths: dict[str, list[str]] = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, separator, raw_path = record.partition(b"\t")
        parts = metadata.split()
        if not separator or len(parts) != 3 or parts[1] != b"blob":
            continue
        object_id = parts[2].decode("ascii")
        paths.setdefault(object_id, []).append(
            raw_path.decode("utf-8", errors="surrogateescape")
        )
    return {object_id: tuple(sorted(values)) for object_id, values in paths.items()}


def is_retired_kernel_path(path: str) -> bool:
    current = map_legacy_path(path)
    if current.startswith("SYSTEM/Guides/"):
        return True
    return (
        current.startswith("SYSTEM/")
        and PurePosixPath(current).name in LEGACY_KERNEL_NAMES
    )


def _archive_blob(root: Path, source: str, content: bytes) -> str:
    archive = safe_path(root, ARCHIVE_ROOT / source)
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists() and archive.read_bytes() != content:
        counter = 1
        candidate = archive
        while candidate.exists():
            candidate = archive.with_name(f"{archive.stem} ({counter}){archive.suffix}")
            counter += 1
        archive = candidate
    if not archive.exists():
        archive.write_bytes(content)
    return archive.relative_to(root).as_posix()


def plan_known_merge_conflicts(
    root: Path,
) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    """Resolve only user-preserving conflicts produced by known layout/kernel renames."""
    entries = unmerged_index(root)
    if not entries:
        return [], []
    blobs = head_blob_paths(root)
    actions: list[tuple[str, str, str, str]] = []
    unknown: list[str] = []
    for path, stages in sorted(entries.items()):
        ours = stages.get(2, "")
        if path == "CLAUDE.md" and ours:
            actions.append(("keep", path, path, ours))
            continue
        if ours and is_retired_kernel_path(path):
            actions.append(("keep", path, path, ours))
            continue
        sources = blobs.get(ours, ()) if ours else ()
        guide_sources = tuple(
            source
            for source in sources
            if source.startswith(("14_Guides/", "SYSTEM/Guides/"))
        )
        if guide_sources:
            actions.append(("archive-remove", path, guide_sources[0], ours))
            continue
        carry_sources = tuple(
            source
            for source in sources
            if KERNEL_CARRY_TARGETS.get(PurePosixPath(source).name) == path
            and map_legacy_path(source).startswith("SYSTEM/")
        )
        if ours and carry_sources and 3 in stages:
            actions.append(("restore-source-take-theirs", path, carry_sources[0], ours))
            continue
        expected_sources = tuple(
            source for source in sources if map_legacy_path(source) == path
        )
        if ours and expected_sources and set(stages) == {2}:
            actions.append(("keep", path, expected_sources[0], ours))
            continue
        unknown.append(path)
    return actions, unknown


def apply_known_merge_conflicts(
    root: Path, actions: list[tuple[str, str, str, str]]
) -> list[str]:
    applied: list[str] = []
    entries = unmerged_index(root)
    for action, path, source, object_id in actions:
        if action == "keep":
            checkout = git_bytes(root, "checkout", "--ours", "--", path)
            if checkout.returncode != 0:
                checkout = git_bytes(
                    root, "checkout-index", "--force", "--stage=2", "--", path
                )
            if (
                checkout.returncode != 0
                or git_bytes(root, "add", "--", path).returncode != 0
            ):
                raise ValueError(f"could not preserve local merge side for {path}")
            applied.append(f"Preserved local file at {path}")
            continue

        blob = git_bytes(root, "cat-file", "blob", object_id)
        if blob.returncode != 0:
            raise ValueError(f"could not read local Git blob for {path}")
        if action == "restore-source-take-theirs":
            restored = safe_path(root, source)
            if restored.exists() and restored.read_bytes() != blob.stdout:
                raise ValueError(f"refusing legacy-source collision at {source}")
            restored.parent.mkdir(parents=True, exist_ok=True)
            restored.write_bytes(blob.stdout)
            checkout = git_bytes(root, "checkout", "--theirs", "--", path)
            if (
                checkout.returncode != 0
                or git_bytes(root, "add", "--", path).returncode != 0
            ):
                raise ValueError(f"could not accept the new kernel file at {path}")
            applied.append(f"Restored {source}; accepted new kernel file at {path}")
            continue
        archived = _archive_blob(root, source, blob.stdout)
        if 3 in entries[path]:
            checkout = git_bytes(root, "checkout", "--theirs", "--", path)
            resolved = (
                checkout.returncode == 0
                and git_bytes(root, "add", "--", path).returncode == 0
            )
        else:
            resolved = (
                git_bytes(root, "rm", "-f", "--ignore-unmatch", "--", path).returncode
                == 0
            )
        if not resolved or git_bytes(root, "add", "--", archived).returncode != 0:
            raise ValueError(f"could not preserve and resolve relocated guide {path}")
        applied.append(
            f"Preserved {source} at {archived}; rejected inferred location {path}"
        )
    return applied


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
        self.custom_moves: list[tuple[str, str]] = []

    def act(self, message: str) -> None:
        self.actions.append(message)

    def read(self, rel: str) -> str | None:
        p = self.root / rel
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else None

    def legacy_sources(self, name: str) -> tuple[str, ...]:
        return tuple(
            relative
            for relative in (f"SYSTEM/{name}", f"00_System/{name}")
            if (self.root / relative).is_file()
        )

    def write(self, rel: str, text: str) -> None:
        if self.apply:
            (self.root / rel).write_text(text, encoding="utf-8")

    def remove(self, rel: str) -> None:
        source = self.root / rel
        if not source.is_file():
            return
        archive = (
            self.root
            / "SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone"
            / rel
        )
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
                candidate = archive.with_name(
                    f"{archive.stem} ({counter}){archive.suffix}"
                )
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
        new = self.read("SYSTEM/Log.md")
        sources = self.legacy_sources("Session Log.md")
        if not sources or new is None:
            return
        entries = [
            entry
            for source in sources
            for entry in bullets_after_heading(self.read(source) or "")
        ]
        missing = [entry for entry in entries if entry not in new]
        if missing:
            new = new.rstrip() + "\n" + "\n".join(missing) + "\n"
            self.write("SYSTEM/Log.md", new)
        self.act(
            f"Log: carried {len(missing)} session-log entries; retired {len(sources)} source(s)"
        )
        for source in sources:
            self.remove(source)

    def carry_state(self) -> None:
        new = self.read("SYSTEM/State.md")
        sources = self.legacy_sources("System State.md")
        if not sources or new is None:
            return
        old_fm = frontmatter(self.read(sources[0]) or "")
        carried = 0
        for field in STATE_FIELDS:
            value = old_fm.get(field, "")
            if not value or value == "[]" or not self.links_exist(value):
                continue
            pattern = re.compile(
                rf"^({re.escape(field)}:)[ \t]*[^\r\n]*$", re.MULTILINE
            )
            if pattern.search(new):
                new = pattern.sub(
                    lambda match: f"{match.group(1)} {value}", new, count=1
                )
                carried += 1
        self.write("SYSTEM/State.md", new)
        self.act(
            f"State: carried {carried} field values; retired {len(sources)} source(s)"
        )
        for source in sources:
            self.remove(source)

    def carry_memory(self) -> None:
        new = self.read("SYSTEM/Memory.md")
        if new is None:
            return
        additions: list[str] = []
        planning_sources = self.legacy_sources("Planning Memory.md")
        for source in planning_sources:
            pm = self.read(source) or ""
            body = pm.split("# Planning Memory", 1)[-1].strip()
            meaningful = [
                line
                for line in body.splitlines()
                if line.strip() not in ("", "-", "##")
                and line.strip() not in PLANNING_MEMORY_DEFAULTS
            ]
            if meaningful:
                additions.append(
                    "\n## Carried from Planning Memory\n\n" + "\n".join(meaningful)
                )
            self.remove(source)
        if planning_sources:
            self.act(
                "Memory: carried and retired "
                f"{len(planning_sources)} Planning Memory source(s)"
            )
        recurring_sources = self.legacy_sources("Recurring Operations.md")
        recurring_rows: list[str] = []
        for source in recurring_sources:
            ro = self.read(source) or ""
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
            recurring_rows.extend(row for row in rows if row not in recurring_rows)
            self.remove(source)
        if recurring_rows:
            additions.append(
                "\n## Carried standing obligations\n\n" + "\n".join(recurring_rows)
            )
        if recurring_sources:
            self.act(
                f"Memory: carried {len(recurring_rows)} recurring-obligation rows; "
                f"retired {len(recurring_sources)} source(s)"
            )
        if additions:
            self.write(
                "SYSTEM/Memory.md", new.rstrip() + "\n" + "\n".join(additions) + "\n"
            )

    def carry_actor(self) -> None:
        new = self.read("SYSTEM/Actor.md")
        sources = self.legacy_sources("Actor Profile.md")
        if not sources:
            return
        merged = new or ""
        for source in sources:
            body = self.read(source) or ""
            if body.startswith("---"):
                end = body.find("\n---", 3)
                if end >= 0:
                    body = body[end + 4 :]
            body = re.sub(
                r"^# Actor Profile[^\n]*\n?", "", body.lstrip(), count=1
            ).strip()
            body = re.sub(
                r"^(#{2,6})\s+(.+?)\s*$",
                lambda match: f"{match.group(1)} Legacy: {match.group(2)}",
                body,
                flags=re.MULTILINE,
            )
            if body and body not in merged:
                merged += "\n\n## Carried from legacy Actor Profile\n\n" + body
            self.remove(source)
        self.write("SYSTEM/Actor.md", merged.rstrip() + "\n")
        self.act(f"Actor: carried and retired {len(sources)} Actor Profile source(s)")

    def drop_doctrine(self) -> None:
        for root_name in ("SYSTEM", "00_System"):
            for name in DOCTRINE:
                relative = f"{root_name}/{name}"
                if (self.root / relative).is_file():
                    self.act(f"Doctrine: retired {relative}")
                    self.remove(relative)
        for guide_name in ("SYSTEM/Guides", "14_Guides"):
            guides = self.root / guide_name
            if not guides.is_dir():
                continue
            for child in sorted(guides.rglob("*")):
                if child.is_symlink():
                    raise ValueError(
                        f"refusing symbolic link in retired guides: {child}"
                    )
                if child.is_file():
                    relative = child.relative_to(self.root).as_posix()
                    self.act(f"Guide: retired {relative}")
                    self.remove(relative)
            if self.apply:
                for directory in sorted(
                    (path for path in guides.rglob("*") if path.is_dir()),
                    key=lambda path: len(path.parts),
                    reverse=True,
                ):
                    directory.rmdir()
                guides.rmdir()

    def relocate_legacy_folders(self) -> None:
        known_roots = {
            PurePosixPath(source).parts[0] for source, _target in LEGACY_PATHS
        }
        roots: list[tuple[Path, str]] = []
        for candidate in sorted(
            self.root.iterdir(), key=lambda path: path.name.casefold()
        ):
            if not candidate.is_dir() or candidate.name.startswith("."):
                continue
            if candidate.name in RESERVED_ROOTS:
                continue
            if candidate.is_symlink():
                raise ValueError(f"refusing top-level symbolic link: {candidate.name}")
            target = (
                map_legacy_path(candidate.name)
                if candidate.name in known_roots
                else f"KNOWLEDGE/{candidate.name}"
            )
            if candidate.name not in known_roots:
                self.custom_moves.append((candidate.name, target))
            roots.append((candidate, target))

        moves: list[tuple[Path, Path]] = []
        directories: set[Path] = set()
        for source_root, target_root in roots:
            directories.add(safe_path(self.root, target_root))
            for source in source_root.rglob("*"):
                if source.is_symlink():
                    raise ValueError(
                        f"refusing symbolic link during migration: {source}"
                    )
                relative = source.relative_to(self.root).as_posix()
                target_relative = (
                    map_legacy_path(relative)
                    if source_root.name in known_roots
                    else f"{target_root}/{source.relative_to(source_root).as_posix()}"
                )
                target = safe_path(self.root, target_relative)
                if source.is_dir():
                    directories.add(target)
                    continue
                if target.exists() and target.read_bytes() != source.read_bytes():
                    raise ValueError(
                        f"refusing migration collision: {relative} -> {target_relative}"
                    )
                moves.append((source, target))

        if roots:
            self.act(
                f"Layout: relocated {len(moves)} remaining file(s) from "
                f"{len(roots)} legacy/custom root(s)"
            )
        if not self.apply:
            return
        for directory in sorted(directories, key=lambda path: len(path.parts)):
            directory.mkdir(parents=True, exist_ok=True)
        for source, target in moves:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                source.unlink()
            else:
                source.replace(target)
        for source_root, _target_root in roots:
            for directory in sorted(
                (path for path in source_root.rglob("*") if path.is_dir()),
                key=lambda path: len(path.parts),
                reverse=True,
            ):
                directory.rmdir()
            source_root.rmdir()

    def close_system_kernel(self) -> None:
        system = self.root / "SYSTEM"
        if not system.is_dir():
            return
        for entry in sorted(system.iterdir(), key=lambda path: path.name.casefold()):
            if entry.is_symlink():
                raise ValueError(
                    f"refusing symbolic link in SYSTEM kernel: {entry.name}"
                )
            allowed = (
                entry.name in ALLOWED_SYSTEM_FILES
                if entry.is_file()
                else entry.name in ALLOWED_SYSTEM_DIRS
            )
            if allowed:
                continue
            if entry.is_file():
                relative = entry.relative_to(self.root).as_posix()
                self.act(f"Kernel: retired unexpected file {relative}")
                self.remove(relative)
                continue
            for child in sorted(entry.rglob("*")):
                if child.is_symlink():
                    raise ValueError(
                        f"refusing symbolic link in SYSTEM kernel: {child}"
                    )
                if child.is_file():
                    relative = child.relative_to(self.root).as_posix()
                    self.act(f"Kernel: retired unexpected file {relative}")
                    self.remove(relative)
            if self.apply:
                for directory in sorted(
                    (path for path in entry.rglob("*") if path.is_dir()),
                    key=lambda path: len(path.parts),
                    reverse=True,
                ):
                    directory.rmdir()
                entry.rmdir()

    def rewrite_references(self) -> None:
        pairs: list[tuple[str, str]] = []
        for source, target in RENAMES:
            pairs.append((f"{source}.md", f"{target}.md"))
            pairs.append((f"[[{source}]]", f"[[{target}]]"))
            pairs.append((f"[[{source}|", f"[[{target}|"))
        for source, target in TITLE_RENAMES:
            pairs.append((f"[[{source}]]", f"[[{target}]]"))
            pairs.append((f"[[{source}|", f"[[{target}|"))
        layout_pairs = tuple(
            sorted(
                (*LEGACY_PATHS, *self.custom_moves),
                key=lambda item: len(item[0]),
                reverse=True,
            )
        )
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
            for source, target in layout_pairs:
                contextual = (
                    source == "WORKSPACE" or (source, target) in self.custom_moves
                )
                if contextual:
                    for separator in ("/", "\\"):
                        source_variant = source.replace("/", separator)
                        target_variant = target.replace("/", separator)
                        updated = re.sub(
                            rf"(?<![A-Za-z0-9_.\-/\\]){re.escape(source_variant)}"
                            rf"(?={re.escape(separator)})",
                            lambda _match, replacement=target_variant: replacement,
                            updated,
                        )
                    updated = re.sub(
                        rf"(\[\[|\]\(){re.escape(source)}(?=(?:[#|]|\]\]|\)))",
                        lambda match: match.group(1) + target,
                        updated,
                    )
                    updated = re.sub(
                        rf"([`\"']){re.escape(source)}\1",
                        lambda match: match.group(1) + target + match.group(1),
                        updated,
                    )
                else:
                    for source_variant, target_variant in (
                        (source, target),
                        (source.replace("/", "\\"), target.replace("/", "\\")),
                    ):
                        updated = re.sub(
                            rf"(?<![A-Za-z0-9_.\-/\\]){re.escape(source_variant)}"
                            rf"(?![A-Za-z0-9_-]|\.[A-Za-z0-9])",
                            lambda _match, replacement=target_variant: replacement,
                            updated,
                        )
            for a, b in pairs:
                updated = updated.replace(a, b)
            spaced_targets = tuple(
                target for _source, target in layout_pairs if " " in target
            )

            def wrap_spaced_link(match: re.Match[str]) -> str:
                destination = match.group(2).strip()
                if (
                    destination.startswith("<")
                    or ' "' in destination
                    or not any(target in destination for target in spaced_targets)
                ):
                    return match.group(0)
                return f"](<{destination}>)"

            updated = re.sub(r"(\]\()([^\r\n)]+)(\))", wrap_spaced_link, updated)
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
        self.relocate_legacy_folders()
        self.close_system_kernel()
        self.rewrite_references()
        if self.actions:
            proposal = (
                self.root
                / "SYSTEM/Proposals/Proposal - Review Standalone Kernel Migration.md"
            )
            if self.apply and not proposal.exists():
                proposal.parent.mkdir(parents=True, exist_ok=True)
                proposal.write_text(
                    "---\ntype: proposal\nstatus: pending\n---\n\n"
                    "# Review standalone SYSTEM kernel migration\n\n"
                    "Legacy files were preserved byte-for-byte under "
                    "`SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone/`. "
                    "Review owner-specific rules there and copy only still-current material "
                    "into `SYSTEM/Memory.md` or the relevant folder instructions.\n",
                    encoding="utf-8",
                )


def validate_workspace(root: Path) -> list[str]:
    findings = [
        relative
        for relative in REQUIRED_KERNEL_FILES
        if not (root / relative).is_file()
    ]
    for source_root in sorted(
        {PurePosixPath(source).parts[0] for source, _target in LEGACY_PATHS}
    ):
        if (root / source_root).exists() or (root / source_root).is_symlink():
            findings.append(f"legacy top-level folder remains: {source_root}")
    system = root / "SYSTEM"
    if system.is_dir():
        for entry in system.iterdir():
            if entry.is_file() and entry.name not in ALLOWED_SYSTEM_FILES:
                findings.append(f"unexpected SYSTEM file remains: SYSTEM/{entry.name}")
            if entry.is_dir() and entry.name not in ALLOWED_SYSTEM_DIRS:
                findings.append(
                    f"unexpected SYSTEM folder remains: SYSTEM/{entry.name}"
                )
    try:
        findings.extend(
            f"unresolved Git conflict: {path}" for path in unmerged_index(root)
        )
    except ValueError as exc:
        findings.append(str(exc))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="workspace root")
    parser.add_argument(
        "--apply", action="store_true", help="write changes (default: dry run)"
    )
    parser.add_argument(
        "--resolve-known-conflicts",
        action="store_true",
        help="resolve only recognized layout/kernel merge conflicts",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not (root / "SYSTEM").is_dir():
        print(f"error: {root} does not look like a Max OS workspace", file=sys.stderr)
        return 2
    try:
        conflicts = unmerged_index(root)
        merge_actions: list[str] = []
        if conflicts:
            if not args.resolve_known_conflicts:
                print(
                    "error: merge conflicts are present; rerun with "
                    "--resolve-known-conflicts after reviewing the dry run",
                    file=sys.stderr,
                )
                return 3
            planned, unknown = plan_known_merge_conflicts(root)
            for action, path, source, _object_id in planned:
                print(f"  - conflict: {action} {path} (local source: {source})")
            if unknown:
                print("error: refusing unrecognized merge conflicts:", file=sys.stderr)
                for path in unknown:
                    print(f"  - {path}", file=sys.stderr)
                return 3
            if args.apply:
                # Detect collisions and unsafe links before resolving the merge
                # or moving a single byte. The apply pass repeats the same
                # checks against the resolved tree.
                Fixup(root, apply=False).run()
                merge_actions = apply_known_merge_conflicts(root, planned)
        fixup = Fixup(root, apply=args.apply)
        fixup.run()
        if args.apply:
            remaining = unmerged_index(root)
            if remaining:
                raise ValueError(
                    "unresolved conflicts remain: " + ", ".join(sorted(remaining))
                )
            findings = validate_workspace(root)
            if findings:
                print("migration validation failed:", file=sys.stderr)
                for finding in findings:
                    print(f"  - {finding}", file=sys.stderr)
                return 4
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    mode = "APPLIED" if args.apply else "DRY RUN (pass --apply to write)"
    print(f"kernel migration fixup — {mode}")
    for action in merge_actions:
        print(f"  - {action}")
    for action in fixup.actions:
        print(f"  - {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
