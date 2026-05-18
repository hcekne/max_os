#!/usr/bin/env python3
"""Lint a Max OS Markdown workspace for frontmatter, headings, and links."""

from __future__ import annotations

import argparse
import dataclasses
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".maxos",
    ".obsidian",
    ".trash",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}

WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FRONTMATTER_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:")

ALLOWED_VALUES = {
    "lifecycle": {
        "evergreen",
        "active",
        "temporary",
        "expired",
        "superseded",
        "archive",
        "delete_candidate",
    },
    "status": {
        "draft",
        "active",
        "canonical",
        "superseded",
        "expired",
        "archived",
        "final",
        "backlog",
        "todo",
        "open",
        "closed",
        "pending",
        "in_progress",
        "blocked",
        "done",
        "complete",
        "completed",
    },
    "retention_policy": {
        "keep",
        "review",
        "archive",
        "delete_after_review",
        "preserve_final_only",
        "preserve_canonical_only",
    },
    "confidentiality": {
        "private",
        "client_confidential",
        "internal",
        "public_template_safe",
    },
}


@dataclasses.dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    path: Path
    line: int
    message: str


def rel(path: Path, root: Path) -> Path:
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        files.append(path)
    return sorted(files)


def git_changed_markdown(root: Path) -> list[Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--", "*.md"],
        ["git", "ls-files", "--others", "--exclude-standard", "--", "*.md"],
    ]
    paths: set[Path] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            if line.strip():
                path = root / line.strip()
                if path.exists() and path.suffix == ".md":
                    paths.add(path.resolve())
    return sorted(paths)


def iter_content_lines(lines: list[str]) -> Iterable[tuple[int, str]]:
    in_fence = False
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield index, line.rstrip("\n")


def remove_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def extract_frontmatter(lines: list[str]) -> tuple[int | None, list[str]]:
    if not lines or lines[0].strip() != "---":
        return None, []
    for index, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return index, lines[1 : index - 1]
    return None, lines[1:]


def parse_simple_frontmatter(frontmatter: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in frontmatter:
        match = FRONTMATTER_KEY_RE.match(line)
        if not match:
            continue
        key = match.group(1)
        raw_value = line.split(":", 1)[1].strip()
        values[key] = raw_value.strip("\"'")
    return values


def validate_yaml_with_optional_dependency(frontmatter: list[str]) -> str | None:
    try:
        import yaml  # type: ignore
    except Exception:
        return None

    try:
        yaml.safe_load("".join(frontmatter)) if frontmatter else None
    except Exception as exc:  # pragma: no cover - exact parser message varies.
        return str(exc)
    return None


def is_template_file(path: Path, root: Path) -> bool:
    relative_parts = rel(path, root).parts
    return "99_Templates" in relative_parts or path.name.startswith("TPL -")


def lint_frontmatter(path: Path, root: Path, lines: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    closing_line, frontmatter = extract_frontmatter(lines)
    if lines and lines[0].strip() == "---" and closing_line is None:
        issues.append(
            Issue("error", "FM001", rel(path, root), 1, "frontmatter starts but never closes")
        )
        return issues

    if not frontmatter:
        return issues

    yaml_error = None if is_template_file(path, root) else validate_yaml_with_optional_dependency(frontmatter)
    if yaml_error:
        issues.append(
            Issue("error", "FM002", rel(path, root), 1, f"frontmatter is invalid YAML: {yaml_error}")
        )

    seen: dict[str, int] = {}
    for offset, line in enumerate(frontmatter, start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or line.startswith((" ", "\t")):
            continue
        if stripped.startswith("- "):
            continue
        match = FRONTMATTER_KEY_RE.match(line)
        if not match:
            issues.append(
                Issue(
                    "warning",
                    "FM003",
                    rel(path, root),
                    offset,
                    "frontmatter line is not a simple top-level key or continuation",
                )
            )
            continue
        key = match.group(1)
        if key in seen:
            issues.append(
                Issue(
                    "warning",
                    "FM004",
                    rel(path, root),
                    offset,
                    f"duplicate frontmatter key also appears on line {seen[key]}: {key}",
                )
            )
        seen[key] = offset

    values = parse_simple_frontmatter(frontmatter)
    for key, allowed in ALLOWED_VALUES.items():
        value = values.get(key)
        if value and value not in allowed:
            issues.append(
                Issue(
                    "warning",
                    f"FM_{key.upper()}",
                    rel(path, root),
                    seen.get(key, 1),
                    f"`{key}` value `{value}` is outside the known Max OS set",
                )
            )

    return issues


def heading_slug(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"[^a-z0-9 _-]+", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")


def collect_headings(path: Path) -> dict[str, set[str]]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    headings: set[str] = set()
    slugs: set[str] = set()
    for _, line in iter_content_lines(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        text = match.group(2).strip()
        headings.add(text.lower())
        slugs.add(heading_slug(text))
    return {"text": headings, "slug": slugs}


def lint_headings(path: Path, root: Path, lines: list[str]) -> list[Issue]:
    issues: list[Issue] = []
    if path.name == ".instructions.md":
        return issues
    headings: list[tuple[int, int, str]] = []
    for line_number, line in iter_content_lines(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_number, len(match.group(1)), match.group(2).strip()))

    if not headings:
        issues.append(Issue("warning", "MD001", rel(path, root), 1, "file has no Markdown headings"))
        return issues

    if headings[0][1] != 1:
        issues.append(
            Issue("warning", "MD002", rel(path, root), headings[0][0], "first heading is not H1")
        )

    h1_count = sum(1 for _, level, _ in headings if level == 1)
    if h1_count > 1:
        issues.append(Issue("warning", "MD003", rel(path, root), 1, "file has multiple H1 headings"))

    previous_level = headings[0][1]
    seen_titles: dict[str, int] = {}
    for line_number, level, title in headings:
        if level > previous_level + 1:
            issues.append(
                Issue(
                    "warning",
                    "MD004",
                    rel(path, root),
                    line_number,
                    f"heading jumps from H{previous_level} to H{level}",
                )
            )
        previous_level = level

        key = title.lower()
        if key in seen_titles:
            issues.append(
                Issue(
                    "warning",
                    "MD005",
                    rel(path, root),
                    line_number,
                    f"duplicate heading text also appears on line {seen_titles[key]}",
                )
            )
        seen_titles[key] = line_number

    return issues


def build_wiki_index(files: list[Path], root: Path) -> tuple[dict[str, list[Path]], dict[str, Path]]:
    by_stem: dict[str, list[Path]] = {}
    by_path: dict[str, Path] = {}
    for path in files:
        by_stem.setdefault(path.stem.lower(), []).append(path)
        relative = rel(path, root).as_posix()
        by_path[relative.lower()] = path
        by_path[relative.removesuffix(".md").lower()] = path
    return by_stem, by_path


def split_wiki_target(raw_target: str) -> tuple[str, str | None]:
    target = raw_target.split("|", 1)[0].strip()
    if "#" in target:
        note, anchor = target.split("#", 1)
        return note.strip(), anchor.strip()
    return target.strip(), None


def anchor_exists(target: Path, anchor: str | None, heading_cache: dict[Path, dict[str, set[str]]]) -> bool:
    if not anchor:
        return True
    headings = heading_cache.setdefault(target, collect_headings(target))
    normalized = anchor.strip().lower()
    return normalized in headings["text"] or heading_slug(anchor) in headings["slug"]


def resolve_wiki(
    note: str,
    current_path: Path,
    root: Path,
    by_stem: dict[str, list[Path]],
    by_path: dict[str, Path],
) -> tuple[list[Path], str]:
    if not note:
        return [current_path], "self"
    if "/" in note:
        normalized = note.removesuffix(".md").lower()
        candidates = []
        directory_candidate = root / note
        if directory_candidate.exists() and directory_candidate.is_dir():
            candidates.append(directory_candidate)
        for key in (normalized, f"{normalized}.md"):
            if key in by_path:
                candidates.append(by_path[key])
        return candidates, "path"
    directory_candidate = root / note
    if directory_candidate.exists() and directory_candidate.is_dir():
        return [directory_candidate], "directory"
    return by_stem.get(note.lower(), []), "stem"


def clean_markdown_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(" ", 1)[0]
    return urllib.parse.unquote(target.strip())


def is_external_target(target: str) -> bool:
    return bool(
        re.match(r"^[a-z][a-z0-9+.-]*:", target, flags=re.IGNORECASE)
        or target.startswith("//")
    )


def resolve_local_markdown_target(target: str, current_path: Path, root: Path) -> Path | None:
    target_without_anchor = target.split("#", 1)[0]
    if not target_without_anchor:
        return current_path
    candidate_strings = [target_without_anchor]
    if not Path(target_without_anchor).suffix:
        candidate_strings.append(f"{target_without_anchor}.md")

    candidates: list[Path] = []
    for candidate_string in candidate_strings:
        candidate = Path(candidate_string)
        if candidate.is_absolute():
            candidates.append(root / candidate.relative_to("/"))
        else:
            candidates.append((current_path.parent / candidate).resolve())
            candidates.append((root / candidate).resolve())

    for candidate in candidates:
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if candidate.exists():
            return candidate
    return None


def lint_links(
    path: Path,
    root: Path,
    lines: list[str],
    by_stem: dict[str, list[Path]],
    by_path: dict[str, Path],
    heading_cache: dict[Path, dict[str, set[str]]],
) -> list[Issue]:
    issues: list[Issue] = []
    for line_number, line in iter_content_lines(lines):
        link_line = remove_inline_code(line)
        for match in WIKI_LINK_RE.finditer(link_line):
            note, anchor = split_wiki_target(match.group(1))
            candidates, mode = resolve_wiki(note, path, root, by_stem, by_path)
            target_display = note or "current file"
            if not candidates:
                issues.append(
                    Issue(
                        "error",
                        "WL001",
                        rel(path, root),
                        line_number,
                        f"wiki-link target does not resolve: [[{target_display}]]",
                    )
                )
                continue
            if len(candidates) > 1 and mode == "stem":
                issues.append(
                    Issue(
                        "warning",
                        "WL002",
                        rel(path, root),
                        line_number,
                        f"wiki-link target is ambiguous across {len(candidates)} files: [[{target_display}]]",
                    )
                )
            if len(candidates) == 1 and not anchor_exists(candidates[0], anchor, heading_cache):
                issues.append(
                    Issue(
                        "warning",
                        "WL003",
                        rel(path, root),
                        line_number,
                        f"wiki-link anchor was not found in target: [[{match.group(1)}]]",
                    )
                )

        for match in MD_LINK_RE.finditer(link_line):
            target = clean_markdown_link_target(match.group(1))
            if not target or is_external_target(target):
                continue
            resolved = resolve_local_markdown_target(target, path, root)
            if resolved is None:
                issues.append(
                    Issue(
                        "error",
                        "ML001",
                        rel(path, root),
                        line_number,
                        f"local Markdown link target does not exist: {target}",
                    )
                )
                continue
            if "#" in target and resolved.suffix == ".md":
                anchor = target.split("#", 1)[1]
                if anchor and not anchor_exists(resolved, anchor, heading_cache):
                    issues.append(
                        Issue(
                            "warning",
                            "ML002",
                            rel(path, root),
                            line_number,
                            f"local Markdown link anchor was not found: {target}",
                        )
                    )

    return issues


def lint_files(root: Path, files: list[Path]) -> list[Issue]:
    all_files = markdown_files(root)
    by_stem, by_path = build_wiki_index(all_files, root)
    heading_cache: dict[Path, dict[str, set[str]]] = {}
    issues: list[Issue] = []
    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        issues.extend(lint_frontmatter(path, root, lines))
        issues.extend(lint_headings(path, root, lines))
        issues.extend(lint_links(path, root, lines, by_stem, by_path, heading_cache))
    return sorted(issues, key=lambda issue: (str(issue.path), issue.line, issue.code))


def render_text(files: list[Path], issues: list[Issue], max_issues: int) -> str:
    errors = sum(1 for issue in issues if issue.severity == "error")
    warnings = sum(1 for issue in issues if issue.severity == "warning")
    output = [
        f"Knowledge lint checked {len(files)} Markdown files.",
        f"Errors: {errors}; warnings: {warnings}.",
    ]
    for issue in issues[:max_issues]:
        output.append(
            f"[{issue.severity.upper()}] {issue.path}:{issue.line} {issue.code} {issue.message}"
        )
    if len(issues) > max_issues:
        output.append(f"... {len(issues) - max_issues} additional issues not shown")
    return "\n".join(output)


def render_markdown(files: list[Path], issues: list[Issue], max_issues: int) -> str:
    errors = sum(1 for issue in issues if issue.severity == "error")
    warnings = sum(1 for issue in issues if issue.severity == "warning")
    rows = [
        "# Knowledge Lint Report",
        "",
        f"- Files checked: {len(files)}",
        f"- Errors: {errors}",
        f"- Warnings: {warnings}",
        "",
        "| Severity | File | Line | Code | Message |",
        "|---|---:|---:|---|---|",
    ]
    for issue in issues[:max_issues]:
        message = issue.message.replace("|", "\\|")
        rows.append(f"| {issue.severity} | `{issue.path}` | {issue.line} | `{issue.code}` | {message} |")
    if len(issues) > max_issues:
        rows.append(f"| info |  |  |  | {len(issues) - max_issues} additional issues not shown |")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="workspace root")
    parser.add_argument("--changed-only", action="store_true", help="lint changed/untracked Markdown files")
    parser.add_argument("--format", choices=["text", "markdown"], default="text")
    parser.add_argument("--output", help="write report to this path")
    parser.add_argument("--max-issues", type=int, default=200)
    parser.add_argument("--fail-on", choices=["error", "warning", "none"], default="error")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    files = git_changed_markdown(root) if args.changed_only else markdown_files(root)
    issues = lint_files(root, files)
    rendered = (
        render_markdown(files, issues, args.max_issues)
        if args.format == "markdown"
        else render_text(files, issues, args.max_issues)
    )

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)

    has_errors = any(issue.severity == "error" for issue in issues)
    has_warnings = any(issue.severity == "warning" for issue in issues)
    if args.fail_on == "error" and has_errors:
        return 1
    if args.fail_on == "warning" and (has_errors or has_warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
