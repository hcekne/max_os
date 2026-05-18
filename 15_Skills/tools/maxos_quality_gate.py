#!/usr/bin/env python3
"""Run Max OS pre-commit knowledge-system quality gates."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
]

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".html",
    ".css",
    ".js",
    ".py",
    ".sh",
    ".toml",
    ".ini",
}

SKIP_PARTS = {".git", ".maxos", ".obsidian", "__pycache__", "node_modules", ".venv", "venv"}


def run(command: list[str], root: Path) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return result.returncode, result.stdout.strip()


def changed_or_all_files(root: Path, full: bool) -> list[Path]:
    if full:
        candidates = [
            path
            for path in root.rglob("*")
            if path.is_file()
            and path.suffix in TEXT_SUFFIXES
            and not any(part in SKIP_PARTS for part in path.relative_to(root).parts)
        ]
        return sorted(candidates)

    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    paths: set[Path] = set()
    for command in commands:
        code, output = run(command, root)
        if code != 0:
            continue
        for line in output.splitlines():
            path = root / line.strip()
            if path.exists() and path.is_file() and path.suffix in TEXT_SUFFIXES:
                paths.add(path.resolve())
    return sorted(paths)


def tracked_runtime_byproducts(root: Path) -> list[str]:
    code, output = run(["git", "ls-files"], root)
    if code != 0:
        return []
    bad = []
    for line in output.splitlines():
        path = Path(line)
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo", ".pyd"}:
            bad.append(line)
    return bad


def untracked_runtime_byproducts(root: Path) -> list[str]:
    bad = []
    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo", ".pyd"}:
            bad.append(path.relative_to(root).as_posix())
    return sorted(bad)


def read_denylist(path: Path | None) -> list[str]:
    if not path or not path.exists():
        return []
    terms = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            terms.append(stripped)
    return terms


def default_denylist_path(root: Path, explicit_path: str | None) -> Path | None:
    if explicit_path:
        return Path(explicit_path).resolve()
    local_path = root / ".maxos" / "public_template_denylist.txt"
    return local_path if local_path.exists() else None


def scan_text_files(files: list[Path], root: Path, denylist: list[str]) -> list[str]:
    findings: list[str] = []
    lower_denylist = [(term, term.lower()) for term in denylist]
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            findings.append(f"{path.relative_to(root)}: could not read text: {exc}")
            continue

        for index, line in enumerate(text.splitlines(), start=1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        f"{path.relative_to(root)}:{index}: possible secret or credential pattern"
                    )
                    break
            lower_line = line.lower()
            for original, lowered in lower_denylist:
                if lowered in lower_line:
                    findings.append(
                        f"{path.relative_to(root)}:{index}: denylist term found: {original}"
                    )
    return findings


def print_section(title: str, ok: bool, details: str | list[str] = "") -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {title}")
    if isinstance(details, list):
        for item in details:
            print(f"  - {item}")
    elif details:
        for line in details.splitlines():
            print(f"  {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="workspace root")
    parser.add_argument("--full", action="store_true", help="run full workspace text scans")
    parser.add_argument("--public-template", action="store_true", help="enable public-template privacy checks")
    parser.add_argument("--denylist", help="optional newline-separated private term denylist")
    parser.add_argument("--skip-diff-check", action="store_true")
    parser.add_argument("--skip-knowledge-lint", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures = 0

    if not args.skip_diff_check:
        code, output = run(["git", "diff", "--check", "HEAD"], root)
        print_section("git diff whitespace check", code == 0, output)
        failures += int(code != 0)

    if not args.skip_knowledge_lint:
        lint_command = [sys.executable, "15_Skills/tools/knowledge_lint.py", "--root", "."]
        if not args.full:
            lint_command.append("--changed-only")
        lint_command.extend(["--fail-on", "error"])
        code, output = run(lint_command, root)
        print_section("knowledge lint", code == 0, output)
        failures += int(code != 0)

    tracked = tracked_runtime_byproducts(root)
    print_section("tracked runtime byproducts", not tracked, tracked)
    failures += int(bool(tracked))

    untracked = untracked_runtime_byproducts(root)
    print_section("untracked runtime byproducts", not untracked, untracked)
    failures += int(bool(untracked))

    if args.public_template:
        denylist_path = default_denylist_path(root, args.denylist)
        denylist = read_denylist(denylist_path)
        files = changed_or_all_files(root, args.full)
        findings = scan_text_files(files, root, denylist)
        print_section("public-template privacy and secret scan", not findings, findings)
        failures += int(bool(findings))

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
