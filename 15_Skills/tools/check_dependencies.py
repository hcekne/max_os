#!/usr/bin/env python3
"""Report which Max OS system dependencies are installed and which are missing.

Run on a fresh clone, or any time a Max OS tool stops working unexpectedly.

For each dependency the script prints:
  * an OK / MISSING marker
  * what it is used for
  * the install command to fix a gap

The script exits 0 even when items are missing, so it can be wired into a
non-blocking setup check. Use the printed install commands to fill the gaps.

See `14_Guides/Guide - System Dependencies.md` for the canonical reference.
"""

from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent

OK = "\033[32mOK\033[0m"
MISS = "\033[31mMISSING\033[0m"
WARN = "\033[33mWARN\033[0m"


@dataclass
class Result:
    label: str
    ok: bool
    detail: str
    used_for: str
    fix: str


def check_command(name: str, used_for: str, fix: str) -> Result:
    path = shutil.which(name)
    if path:
        version = ""
        try:
            out = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
            version = (out.stdout or out.stderr).splitlines()[0] if (out.stdout or out.stderr) else ""
        except Exception:
            pass
        return Result(name, True, f"{path}{(' — ' + version) if version else ''}", used_for, fix)
    return Result(name, False, "not on $PATH", used_for, fix)


def check_python_module(module: str, used_for: str, fix: str) -> Result:
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, "__version__", "")
        detail = f"importable{(' — ' + version) if version else ''}"
        return Result(f"python:{module}", True, detail, used_for, fix)
    except ImportError:
        return Result(f"python:{module}", False, "import failed", used_for, fix)


def check_playwright_workspace() -> Result:
    local_pw = REPO_ROOT / ".maxos" / "visual-check" / "node_modules" / "playwright"
    if not local_pw.exists():
        return Result(
            "playwright (workspace)",
            False,
            f"not installed at {local_pw}",
            "headless visual QA for slide decks via check_deck_visual.mjs",
            "cd .maxos/visual-check && npm init -y && npm install playwright && npx playwright install chromium",
        )
    return Result(
        "playwright (workspace)",
        True,
        f"installed at {local_pw}",
        "headless visual QA for slide decks via check_deck_visual.mjs",
        "—",
    )


def check_playwright_chromium() -> Result:
    cache = Path(os.path.expanduser("~/Library/Caches/ms-playwright"))
    if not cache.exists():
        return Result(
            "playwright chromium",
            False,
            f"no cache at {cache}",
            "actual headless browser used by Playwright to render slides",
            "cd .maxos/visual-check && npx playwright install chromium",
        )
    chromium_dirs = [p for p in cache.iterdir() if p.is_dir() and "chromium" in p.name]
    if not chromium_dirs:
        return Result(
            "playwright chromium",
            False,
            f"cache exists but no chromium build found in {cache}",
            "actual headless browser used by Playwright to render slides",
            "cd .maxos/visual-check && npx playwright install chromium",
        )
    return Result(
        "playwright chromium",
        True,
        f"{chromium_dirs[0].name}",
        "actual headless browser used by Playwright to render slides",
        "—",
    )


def check_git_hooks() -> Result:
    try:
        out = subprocess.run(
            ["git", "config", "--get", "core.hooksPath"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            timeout=5,
        )
        hooks_path = out.stdout.strip()
    except Exception:
        hooks_path = ""
    if hooks_path == ".githooks":
        return Result(
            "git hooks",
            True,
            "core.hooksPath = .githooks",
            "pre-commit knowledge lint, whitespace check, byproduct check",
            "—",
        )
    return Result(
        "git hooks",
        False,
        f"core.hooksPath = '{hooks_path}'",
        "pre-commit knowledge lint, whitespace check, byproduct check",
        "sh 15_Skills/tools/ensure_local_setup.sh",
    )


def print_table(results: list[Result]) -> None:
    name_w = max(len(r.label) for r in results)
    print()
    print(f"{'Dependency':<{name_w}}  Status   Used for")
    print(f"{'-' * name_w}  -------  --------")
    missing: list[Result] = []
    for r in results:
        mark = OK if r.ok else MISS
        plain_mark = "OK" if r.ok else "MISSING"
        # Pad the colourised marker so columns line up regardless of ANSI codes.
        pad = " " * (7 - len(plain_mark))
        print(f"{r.label:<{name_w}}  {mark}{pad}{r.used_for}")
        print(f"{'':<{name_w}}           detail: {r.detail}")
        if not r.ok:
            missing.append(r)
            print(f"{'':<{name_w}}           fix:    {r.fix}")
        print()

    if missing:
        print(f"\n{len(missing)} item(s) need attention. Run the printed fix commands.")
    else:
        print("\nAll Max OS system dependencies are present.")


def main() -> None:
    results = [
        check_command(
            "python3",
            "every Python tool in 15_Skills/tools/",
            "brew install python@3",
        ),
        check_command(
            "node",
            "running 15_Skills/tools/slides/check_deck_visual.mjs (headless visual QA)",
            "brew install node",
        ),
        check_command(
            "pandoc",
            "Markdown to HTML for slide deck builds and memo pack builds",
            "brew install pandoc",
        ),
        check_command(
            "weasyprint",
            "HTML to PDF for memo pack and interview-guide PDFs",
            "brew install weasyprint",
        ),
        check_python_module(
            "PIL",
            "slide-deck logo safety check (background-vs-slide compatibility)",
            "pip3 install --user --break-system-packages pillow",
        ),
        check_git_hooks(),
        check_playwright_workspace(),
        check_playwright_chromium(),
    ]
    print_table(results)


if __name__ == "__main__":
    main()
