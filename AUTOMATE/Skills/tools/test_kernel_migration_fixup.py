#!/usr/bin/env python3
"""Focused losslessness regression for kernel_migration_fixup.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from kernel_migration_fixup import Fixup


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
            old_manual = b"# Manual\n\nKEEP CUSTOM RULE.\n"
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
            self.assertEqual((archive / "SYSTEM/System State.md").read_text(), old_state)
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
            self.assertEqual(
                (root / "Note.md").read_text(),
                "See [[SYSTEM/State]], [[AUTOMATE/Skills/Skill - Set Up Standalone MaxOS]], "
                "and SYSTEM/Log.md.\n",
            )
            self.assertTrue(
                (system / "Proposals/Proposal - Review Standalone Kernel Migration.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()
