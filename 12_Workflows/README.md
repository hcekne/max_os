# Workflows

Use this folder for repeatable step-by-step work processes.

Max OS supports two workflow forms:

- **Workflow notes** in this folder root: human-led processes with optional AI
  assistance.
- **Executable automations** in `12_Workflows/Automations/`: machine-readable
  recipes created by the MaxOS Workflow Builder.

For reusable agent-executable capabilities that are not whole workflows, see
`15_Skills/` and `SKILLS.md`.

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
- Use `99_Templates/TPL - Workflow.md` when creating a new workflow.
- Use the folder listing as the source of truth instead of maintaining a second workflow catalog here.
- If a workflow is promoted into a skill, mark that in the workflow note itself.

## Executable Automations
- Executable recipes carry `type: maxos-workflow` in YAML frontmatter.
- Keep recipe definitions in `12_Workflows/Automations/`.
- Keep run outputs out of the recipe list. The harness writes intermediate
  outputs to `12_Workflows/Automations/artifacts/` and delivers final outputs to
  the inbox.
- Prefer editing executable recipes in the Workflow Builder. Hand-edit only when
  you understand the schema.
- Document inputs should be picked through the Workflow Builder so they point to
  files the owner can access in the workspace or an authorized organization
  project.
