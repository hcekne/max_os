# Indexes

## Vault Root Surface
- Keep the vault root limited to workspace folders, hidden config/state folders, and a small control-file set.
- Allowed root markdown files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILLS.md`.
- Do not keep domain mirror files at the root, such as `Interactions.md` or `Projects.md`.
- If a root-level markdown file belongs to a workspace area, move it into the matching folder or delete it if it is only an empty placeholder.

## People Index
- Store all person notes in `KNOWLEDGE/People`.
- Suggested filename: `First Last.md`.

## Organization Index
- Store all organization notes in `KNOWLEDGE/Organizations`.
- Use one note per organization unless a subfolder is clearly needed.
- In MaxOS Online, organizations may also exist as shared runtime containers
  outside this personal workspace. Those organization projects and skills can be
  added to an agent's chat/workflow scope without being copied into
  `KNOWLEDGE/Organizations/`.

## Client Index
- One folder per client inside `KNOWLEDGE/Clients` if needed for sub-notes.
- Keep the main client note at top of each client folder as `Client - Name.md`.

## Project Index
- Store active projects in `KNOWLEDGE/Projects`.
- Suggested filename: `Project - Name.md`.
- Keep one canonical project note in the root.
- Add a matching project folder only when the project has meaningful supporting material.
- Organization projects in MaxOS Online are shared workspaces outside the
  owner's private `KNOWLEDGE/Projects/` folder. If they are added to scope, treat them
  as authorized shared resources, not as personal notes to silently copy.

## Content Index
- Store written content in `KNOWLEDGE/Content`.
- Add links to related clients/projects/people in frontmatter and body.
- Use pillar + derivative model for content repurposing.
- Keep only the current canonical version of a content family in the active content surface when possible.
- Move older content versions to `SYSTEM/Cleaning/Rubbish Bin/KNOWLEDGE/Content/` unless they have clear historical value.

## Cleaning Index
- Central historical retention lives in `SYSTEM/Cleaning/Archive/`.
- Central short-retention delete queue lives in `SYSTEM/Cleaning/Rubbish Bin/`.
- Mirror the original source path beneath those folders so origin context stays obvious.

## Notes Index
- Store general ideas and unclassified notes in `KNOWLEDGE/Notes`.
- Move or link notes later if they become person, client, project, or content specific.
- Keep active notes in `KNOWLEDGE/Notes/` root.
- Keep one canonical note per major topic when practical.
- Move superseded or redundant notes into central cleaning based on retention value.

## Workflow Index
- Store repeatable human-led processes in `AUTOMATE/Workflows`.
- Store executable Workflow Builder recipes in `AUTOMATE/Workflows/Automations/`.
- Use workflow notes for step-by-step execution with checkpoints and quality checks.
- Use `type: maxos-workflow` frontmatter to identify executable automations.
- Use the folder listing as the source of truth instead of maintaining a second workflow catalog here.

## Guides Index
- Store setup and usage guides in `SYSTEM/Guides`.
- Keep beginner setup instructions for supported AI tools here.

## Goals Index
- Store major work goals in `PLAN/Goals`.
- Keep one note per major goal.
- Link goals to projects and planning notes.

## Interaction Index
- One note per interaction in `KNOWLEDGE/Interactions`.
- Use date-first naming for easy sorting.

## TODO Index
- Store actionable backlog and active tasks in `PLAN/Todos`.
- Keep one task per note for larger initiatives.
- Start from template: `SYSTEM/Templates/TPL - Todo.md`.

## Action Center Index
- Store raw inputs and requests for Max OS in `ACTION CENTER/Agent Inbox/`.
- Store agent results and updates awaiting the owner in
  `ACTION CENTER/My Inbox/`.
- Process both inboxes regularly into canonical folders.

## Outbox Index
- Store materials staged for delivery to another actor, agent, or external recipient in `ACTION CENTER/Outbox`.
- Use My Inbox, not Outbox, when the owner still needs to review or approve an
  item.
- Treat the outbox as transient; archive or rubbish-bin items after pickup.
- Use `<recipient>/` subfolders to group deliveries to multiple downstream destinations.
- Cross-link each outbox item back to the canonical source note(s) that produced it.
- Move delivered items to `SYSTEM/Cleaning/Archive/ACTION CENTER/Outbox/` (historical value) or `SYSTEM/Cleaning/Rubbish Bin/ACTION CENTER/Outbox/` (low retention).

## Skills Index
- Store agent-executable skill definitions in `AUTOMATE/Skills`.
- Each skill should define Purpose, Trigger, Inputs, Steps, Outputs, and Quality Checks.
- The master manifest is `SKILLS.md` at the vault root.
- Skills differ from workflows: skills are agent-autonomous, workflows are human-led.
- Keep `ACTION CENTER/Agent Inbox` transient; avoid long-term storage there.

## Planning Index
- Store horizon plans and reviews in `PLAN`.
- Keep one active note per horizon (weekly, quarterly, two-year).
- Use weekly reviews to update `SYSTEM/Planning Memory`.

## System Control Files
- Primary LLM instructions: `SYSTEM/LLM Operating Manual.md`.
- Last checkpoint tracker: `SYSTEM/System State.md`.
- Append-only narrative session log: `SYSTEM/Session Log.md`.
- Planning schedule definitions: `SYSTEM/Planning Cadence.md`.
- Recurring operations register: `SYSTEM/Recurring Operations.md`.
- Planning learning memory: `SYSTEM/Planning Memory.md`.
- Folder and note placement map: `SYSTEM/Indexes.md`.
- Document lifecycle rules: `SYSTEM/Document Lifecycle Policy.md`.
- Archive rules: `SYSTEM/Archive Policy.md`.
- Rubbish-bin rules: `SYSTEM/Rubbish Bin Policy.md`.
- Git preservation rules: `SYSTEM/Git Preservation Policy.md`.
- Machine-readable hygiene rules: `SYSTEM/workspace_hygiene_rules.yaml`.
- Local clone setup requirements: `SYSTEM/local_setup_requirements.yaml`.
- Public-template denylist example: `SYSTEM/public_template_denylist.example.txt`.
- Harness-era scope guidance: `SYSTEM/Guides/Guide - MaxOS Online Scope and Shared Resources.md`.

## Planning Templates
- Templates live in `SYSTEM/Templates/`.
- Use the folder README and template filenames there as the source of truth.

## Optional Modules
- Optional personal capability packs live in `AUTOMATE/Modules`.
- Default recommendation for shared deployments: keep modules disabled until needed.
