#!/usr/bin/env python3
"""Focused losslessness regression for kernel_migration_fixup.py."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from kernel_migration_fixup import Fixup, unmerged_index, validate_workspace
from knowledge_lint import lint_files


SCRIPT = Path(__file__).with_name("kernel_migration_fixup.py")


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        capture_output=True,
    )


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def commit(repo: Path, message: str) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-m", message)


def run_fixup(root: Path, *, apply: bool = False) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable,
        str(SCRIPT),
        "--root",
        str(root),
        "--resolve-known-conflicts",
    ]
    if apply:
        command.append("--apply")
    return subprocess.run(command, check=False, text=True, capture_output=True)


class KernelMigrationFixupTest(unittest.TestCase):
    def test_preserves_sources_and_carries_only_safe_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            system = root / "SYSTEM"
            for relative in (
                "Cleaning/Archive",
                "Proposals",
                "Templates",
                "Storage References",
                "Guides",
            ):
                (system / relative).mkdir(parents=True)
            (root / "PLAN/Weekly").mkdir(parents=True)
            (root / "PLAN/Weekly/Current.md").write_text("# Current\n")

            (system / "State.md").write_text(
                "---\nlast_interaction_date:\nactive_week_plan:\n"
                "active_quarter_plan:\nactive_two_year_plan:\n"
                "active_goals: []\nactive_modules: []\n---\n# State\n"
            )
            old_state = (
                "---\nlast_interaction_date: 2026-08-07\n"
                "active_week_plan: [[PLAN/Weekly/Current]]\n"
                "active_quarter_plan: [[PLAN/Quarterly/Missing]]\n"
                "active_two_year_plan:\nactive_goals: []\nactive_modules: []\n"
                "custom_field: KEEP EXACT\n---\n# System State\n"
            )
            (system / "System State.md").write_text(old_state)
            (system / "Log.md").write_text("# Log\n\n## Entries\n\n_No entries yet._\n")
            (system / "Session Log.md").write_text(
                "# Session Log\n\n- 2026-08-07: Keep this result.\n"
            )
            (system / "Memory.md").write_text(
                "# Memory\n\n## Standing obligations\n\n"
                "| Obligation | Trigger | Valid from | Valid until | Linked note |\n"
                "| --- | --- | --- | --- | --- |\n|  |  |  |  |  |\n"
            )
            (system / "Planning Memory.md").write_text(
                "# Planning Memory\n\n## Planning Principles\n"
                "- Keep plans realistic relative to known capacity.\n\n"
                "## Lessons\n- KEEP CUSTOM LESSON.\n"
            )
            (system / "Recurring Operations.md").write_text(
                "# Recurring Operations\n\n## Active Recurring Obligations\n\n"
                "| Obligation | Trigger | Status | Valid from | Valid until | Linked note |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                "| Keep task | Friday | active | 2026-01-01 | | |\n\n"
                "## Client / Project Obligation Pattern\n\n"
                "| Example | Monthly | active | YYYY-MM-DD | | |\n"
            )
            (system / "Actor.md").write_text(
                "<!-- maxos-actor-placeholder -->\n# Actor\n\n## Role\n\n- Purpose.\n"
            )
            (system / "Actor Profile.md").write_text(
                "---\ntype: actor_profile\n---\n# Actor Profile - Owner\n\n"
                "## Operating Notes\n\n- KEEP ACTOR NOTE.\n"
            )
            old_manual = (
                b"# Manual\n\nKEEP CUSTOM RULE. See [[Retired Missing Note]].\n"
            )
            (system / "LLM Operating Manual.md").write_bytes(old_manual)
            (system / "Guides/Guide - Private.md").write_text("# KEEP GUIDE\n")
            (root / "Note.md").write_text(
                "See [[System State]], [[Standalone]], and SYSTEM/Session Log.md.\n"
            )

            Fixup(root, apply=True).run()

            archive = system / "Cleaning/Archive/System Kernel Migration/Standalone"
            self.assertEqual(
                (archive / "SYSTEM/LLM Operating Manual.md").read_bytes(), old_manual
            )
            self.assertEqual(
                (archive / "SYSTEM/System State.md").read_text(), old_state
            )
            self.assertFalse((system / "System State.md").exists())
            state = (system / "State.md").read_text()
            self.assertIn("last_interaction_date: 2026-08-07", state)
            self.assertIn("active_week_plan: [[PLAN/Weekly/Current]]", state)
            self.assertNotIn("Missing", state)
            self.assertIn("Keep this result", (system / "Log.md").read_text())
            memory = (system / "Memory.md").read_text()
            self.assertIn("KEEP CUSTOM LESSON", memory)
            self.assertNotIn("Keep plans realistic relative to known capacity", memory)
            self.assertIn("| Keep task | Friday | 2026-01-01 |  |  |", memory)
            self.assertNotIn("Example", memory)
            self.assertIn("KEEP ACTOR NOTE", (system / "Actor.md").read_text())
            self.assertFalse(
                any(
                    issue.code == "MD005"
                    for issue in lint_files(root, [system / "Actor.md"])
                )
            )
            self.assertEqual(
                (root / "Note.md").read_text(),
                "See [[SYSTEM/State]], [[AUTOMATE/Skills/Skill - Set Up Standalone MaxOS]], "
                "and SYSTEM/Log.md.\n",
            )
            self.assertTrue(
                (
                    system
                    / "Proposals/Proposal - Review Standalone Kernel Migration.md"
                ).is_file()
            )
            self.assertIn(
                "status: pending",
                (
                    system
                    / "Proposals/Proposal - Review Standalone Kernel Migration.md"
                ).read_text(),
            )
            self.assertEqual(
                lint_files(root, [archive / "SYSTEM/LLM Operating Manual.md"]), []
            )

    def test_real_numbered_repo_merge_is_lossless_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "workspace"
            root.mkdir()
            git(root, "init", "-b", "main")
            git(root, "config", "user.email", "test@example.invalid")
            git(root, "config", "user.name", "Test")

            write(root, "AGENTS.md", "Read [[00_System/LLM Operating Manual]].\n")
            write(root, "CLAUDE.md", "Read [[00_System/LLM Operating Manual]].\n")
            write(root, "00_System/.instructions.md", "# Legacy system instructions\n")
            write(root, "00_System/LLM Operating Manual.md", "# Manual\n")
            write(
                root,
                "00_System/System State.md",
                "---\nlast_interaction_date:\nactive_week_plan:\n"
                "active_quarter_plan:\nactive_two_year_plan:\nactive_goals: []\n"
                "active_modules: []\n---\n# System State\n",
            )
            write(root, "00_System/Session Log.md", "# Session Log\n")
            write(root, "00_System/Planning Memory.md", "# Planning Memory\n")
            write(root, "00_System/Actor Profile.md", "# Actor Profile - Owner\n")
            write(root, "01_People/README.md", "# People\n")
            write(root, "04_Projects/README.md", "# Projects\n")
            write(root, "14_Guides/README.md", "# Guides\n")
            commit(root, "legacy template")

            git(root, "switch", "-c", "template")
            for legacy in ("00_System", "01_People", "04_Projects", "14_Guides"):
                shutil.rmtree(root / legacy)
            write(root, "AGENTS.md", "# Agents\n\nRead `SYSTEM/Actor.md`.\n")
            write(root, "CLAUDE.md", "Read AGENTS.md.\n")
            write(root, ".gemini/GEMINI.md", "Read AGENTS.md.\n")
            write(root, "ACTION CENTER/.instructions.md", "# Action Center\n")
            write(root, "AUTOMATE/.instructions.md", "# Automate\n")
            write(root, "KNOWLEDGE/.instructions.md", "# Knowledge\n")
            write(root, "KNOWLEDGE/People/README.md", "# People\n")
            write(root, "KNOWLEDGE/Projects/README.md", "# Projects\n")
            write(root, "PLAN/.instructions.md", "# Plan\n")
            write(root, "PLAN/Weekly/Current.md", "# Current\n")
            write(root, "SYSTEM/.instructions.md", "# System\n")
            write(root, "SYSTEM/Actor.md", "# Actor\n\n## Role\n\n- Current owner.\n")
            write(
                root,
                "SYSTEM/State.md",
                "---\nlast_interaction_date:\nactive_week_plan:\n"
                "active_quarter_plan:\nactive_two_year_plan:\nactive_goals: []\n"
                "active_modules: []\n---\n# State\n",
            )
            write(root, "SYSTEM/Log.md", "# Log\n\n## Entries\n\n_No entries yet._\n")
            write(root, "SYSTEM/Memory.md", "# Memory\n")
            write(root, "SYSTEM/Policy.md", "# Policy\n")
            for relative in (
                "SYSTEM/Cleaning/Archive/.gitkeep",
                "SYSTEM/Proposals/.gitkeep",
                "SYSTEM/Storage References/.gitkeep",
                "SYSTEM/Templates/.gitkeep",
            ):
                write(root, relative, "")
            commit(root, "current layout and kernel")

            git(root, "switch", "main")
            write(
                root,
                "CLAUDE.md",
                "Read [[00_System/LLM Operating Manual]].\n\nKEEP CLAUDE RULE.\n",
            )
            write(
                root,
                "00_System/LLM Operating Manual.md",
                "# Manual\n\nKEEP OPERATING RULE. See [[00_System/System State]].\n",
            )
            write(
                root,
                "00_System/System State.md",
                "---\nlast_interaction_date: 2026-08-07\n"
                "active_week_plan: [[PLAN/Weekly/Current]]\nactive_quarter_plan:\n"
                "active_two_year_plan:\nactive_goals: []\nactive_modules: []\n"
                "custom_field: KEEP EXACT\n---\n# System State\n\nKEEP STATE BODY.\n",
            )
            write(
                root,
                "00_System/Session Log.md",
                "# Session Log\n\n- 2026-08-07: KEEP LOG ENTRY.\n",
            )
            write(
                root,
                "00_System/Actor Profile.md",
                "# Actor Profile - Owner\n\n## Operating Notes\n\n- KEEP ACTOR NOTE.\n",
            )
            write(
                root,
                "01_People/Private Person.md",
                "# Private Person\n\nKEEP PERSON.\n",
            )
            write(
                root,
                "04_Projects/Private Project.md",
                "# Private Project\n\nKEEP PROJECT. See `01_People/Private Person.md`.\n",
            )
            write(
                root, "14_Guides/Guide - Private.md", "# Private Guide\n\nKEEP GUIDE.\n"
            )
            write(root, "Research Archive/Market.md", "# Market\n\nKEEP RESEARCH.\n")
            commit(root, "lived-in workspace")

            merge = git(
                root, "merge", "--no-commit", "--no-ff", "template", check=False
            )
            self.assertNotEqual(merge.returncode, 0)
            conflicts_before = unmerged_index(root)
            self.assertTrue(conflicts_before)

            preview = run_fixup(root)
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertEqual(unmerged_index(root), conflicts_before)
            applied = run_fixup(root, apply=True)
            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertEqual(unmerged_index(root), {})
            self.assertEqual(validate_workspace(root), [])

            self.assertIn("KEEP CLAUDE RULE", (root / "CLAUDE.md").read_text())
            self.assertIn(
                "KEEP PERSON", (root / "KNOWLEDGE/People/Private Person.md").read_text()
            )
            self.assertIn(
                "KNOWLEDGE/People/Private Person.md",
                (root / "KNOWLEDGE/Projects/Private Project.md").read_text(),
            )
            self.assertIn(
                "KEEP RESEARCH",
                (root / "KNOWLEDGE/Research Archive/Market.md").read_text(),
            )
            self.assertIn("KEEP LOG ENTRY", (root / "SYSTEM/Log.md").read_text())
            self.assertIn("KEEP ACTOR NOTE", (root / "SYSTEM/Actor.md").read_text())
            self.assertIn(
                "last_interaction_date: 2026-08-07",
                (root / "SYSTEM/State.md").read_text(),
            )
            self.assertFalse((root / "00_System").exists())
            self.assertFalse((root / "01_People").exists())
            self.assertFalse((root / "Research Archive").exists())

            archives = list(
                (
                    root / "SYSTEM/Cleaning/Archive/System Kernel Migration/Standalone"
                ).rglob("*.md")
            )
            self.assertTrue(
                any("KEEP OPERATING RULE" in path.read_text() for path in archives)
            )
            self.assertTrue(any("KEEP GUIDE" in path.read_text() for path in archives))
            self.assertTrue(
                any("custom_field: KEEP EXACT" in path.read_text() for path in archives)
            )

            commit(root, "migrate legacy workspace")
            again = run_fixup(root, apply=True)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(git(root, "status", "--porcelain").stdout, "")

    def test_unknown_merge_conflict_is_refused_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git(root, "init", "-b", "main")
            git(root, "config", "user.email", "test@example.invalid")
            git(root, "config", "user.name", "Test")
            write(root, "SYSTEM/Policy.md", "# Policy\n")
            write(root, "README.md", "# Original\n")
            commit(root, "base")
            git(root, "switch", "-c", "template")
            write(root, "README.md", "# Template\n")
            commit(root, "template change")
            git(root, "switch", "main")
            write(root, "README.md", "# Workspace\n")
            commit(root, "workspace change")
            git(root, "merge", "--no-commit", "--no-ff", "template", check=False)
            before = (root / "README.md").read_bytes()

            result = run_fixup(root, apply=True)

            self.assertEqual(result.returncode, 3)
            self.assertIn("refusing unrecognized merge conflicts", result.stderr)
            self.assertEqual((root / "README.md").read_bytes(), before)
            self.assertIn("README.md", unmerged_index(root))


if __name__ == "__main__":
    unittest.main()
