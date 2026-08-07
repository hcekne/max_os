# Skills

Agent-executable capabilities live as files, not as a hand-maintained list —
list the folders to see what exists; read a card before running it.

- **Skills** (agent-autonomous, end-to-end): `AUTOMATE/Skills/` — one
  `Skill - *.md` card each, defining Purpose, Trigger, Inputs, Steps,
  Outputs, and Quality Checks.
- **Workflows** (human-led, step-by-step with checkpoints):
  `AUTOMATE/Workflows/` — one `Workflow - *.md` card each.
- **Executable automations** (Workflow Builder recipes, schedulable):
  `AUTOMATE/Workflows/Automations/` — identified by `type: maxos-workflow`
  frontmatter.
- **Tools** (scripts the skills call): `AUTOMATE/Skills/tools/` — each has a
  usage header; `check_dependencies.py` reports what external software they
  need (see `SYSTEM/Standalone.md`).
- **Modules** (optional capability packs, disabled by default):
  `AUTOMATE/Modules/` — each has a `STATUS.md`.

When adding a capability, add the card in the right folder with complete
frontmatter — no separate catalog needs updating.
