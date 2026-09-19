# Workflows

Use this folder for repeatable step-by-step work processes.

floThink supports two workflow forms:

- **Workflow notes** in this folder root: human-led processes with optional AI
  assistance.
- **Executable automations** in `AUTOMATE/Workflows/Automations/`: machine-readable
  recipes created by the floThink Workflow Builder.

For reusable agent-executable capabilities that are not whole workflows, see
`AUTOMATE/Skills/` and `SKILLS.md`.

## Use This Folder When
- the same task happens often
- you want consistent quality
- a human drives the process and AI assists selected steps

## Workflow Note Shape
1. Goal
2. Inputs
3. Steps
4. Outputs
5. Quality checklist

## Guidance
- Use `SYSTEM/Templates/TPL - Workflow.md` when creating a new workflow.
- Use the folder listing as the source of truth instead of maintaining a second workflow catalog here.
- If a workflow is promoted into a skill, mark that in the workflow note itself.

## Executable Automations
- Executable recipes carry `type: maxos-workflow` in YAML frontmatter.
- Keep recipe definitions in `AUTOMATE/Workflows/Automations/`.
- Keep run outputs out of the recipe list. The harness writes intermediate
  outputs to `AUTOMATE/Workflows/Automations/artifacts/` and delivers final outputs to
  the inbox.
- `AUTOMATE/Workflows/Automations/WORKFLOW-PRIMITIVES.md` is the single, always
  current description of the recipe format: every node type, its fields, and the
  Workflow Library categories. floThink regenerates it, so do not copy it into
  another note and do not describe the schema anywhere else.
- The Workflow Builder is the easiest way to author a recipe. Hand-authoring one
  from that reference is fully supported; the backend validates a recipe on save
  and before every run.
- Document inputs should be picked through the Workflow Builder so they point to
  files the owner can access in the workspace or an authorized organization
  project.
