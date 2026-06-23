# Indexes

## Vault Root Surface
- Keep the vault root limited to numbered folders, hidden config/state folders, and a small control-file set.
- Allowed root markdown files: `README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILLS.md`.
- Do not keep numbered markdown files at the root that mirror numbered folders such as `06_Interactions.md`.
- If a root-level markdown file belongs to a numbered domain, move it into the matching folder or delete it if it is only an empty placeholder.

## People Index
- Store all person notes in `01_People`.
- Suggested filename: `First Last.md`.

## Organization Index
- Store all organization notes in `02_Organizations`.
- Use one note per organization unless a subfolder is clearly needed.
- In MaxOS Online, organizations may also exist as shared runtime containers
  outside this personal workspace. Those organization projects and skills can be
  added to an agent's chat/workflow scope without being copied into
  `02_Organizations/`.

## Client Index
- One folder per client inside `03_Clients` if needed for sub-notes.
- Keep the main client note at top of each client folder as `Client - Name.md`.

## Project Index
- Store active projects in `04_Projects`.
- Suggested filename: `Project - Name.md`.
- Keep one canonical project note in the root.
- Add a matching project folder only when the project has meaningful supporting material.
- Organization projects in MaxOS Online are shared workspaces outside the
  owner's private `04_Projects/` folder. If they are added to scope, treat them
  as authorized shared resources, not as personal notes to silently copy.

## Content Index
- Store written content in `05_Content`.
- Add links to related clients/projects/people in frontmatter and body.
- Use pillar + derivative model for content repurposing.
- Keep only the current canonical version of a content family in the active content surface when possible.
- Move older content versions to `16_Cleaning/Rubbish Bin/05_Content/` unless they have clear historical value.

## Cleaning Index
- Central historical retention lives in `16_Cleaning/Archive/`.
- Central short-retention delete queue lives in `16_Cleaning/Rubbish Bin/`.
- Mirror the original source path beneath those folders so origin context stays obvious.

## Notes Index
- Store general ideas and unclassified notes in `11_Notes`.
- Move or link notes later if they become person, client, project, or content specific.
- Keep active notes in `11_Notes/` root.
- Keep one canonical note per major topic when practical.
- Move superseded or redundant notes into central cleaning based on retention value.

## Workflow Index
- Store repeatable human-led processes in `12_Workflows`.
- Store executable Workflow Builder recipes in `12_Workflows/Automations/`.
- Use workflow notes for step-by-step execution with checkpoints and quality checks.
- Use `type: maxos-workflow` frontmatter to identify executable automations.
- Use the folder listing as the source of truth instead of maintaining a second workflow catalog here.

## Guides Index
- Store setup and usage guides in `14_Guides`.
- Keep beginner setup instructions for supported AI tools here.

## Goals Index
- Store major work goals in `13_Goals`.
- Keep one note per major goal.
- Link goals to projects and planning notes.

## Interaction Index
- One note per interaction in `06_Interactions`.
- Use date-first naming for easy sorting.

## TODO Index
- Store actionable backlog and active tasks in `08_Todos`.
- Keep one task per note for larger initiatives.
- Start from template: `99_Templates/TPL - Todo.md`.

## Inbox Index
- Store raw and unprocessed captures in `10_Inbox`.
- Process inbox items daily into canonical folders.

## Outbox Index
- Store materials staged for delivery to another actor, agent, or external recipient in `17_Outbox`.
- Symmetric to `10_Inbox/`: inbox is what arrives, outbox is what leaves.
- Treat the outbox as transient; archive or rubbish-bin items after pickup.
- Use `<recipient>/` subfolders to group deliveries to multiple downstream destinations.
- Cross-link each outbox item back to the canonical source note(s) that produced it.
- Move delivered items to `16_Cleaning/Archive/17_Outbox/` (historical value) or `16_Cleaning/Rubbish Bin/17_Outbox/` (low retention).

## Skills Index
- Store agent-executable skill definitions in `15_Skills`.
- Each skill should define Purpose, Trigger, Inputs, Steps, Outputs, and Quality Checks.
- The master manifest is `SKILLS.md` at the vault root.
- Skills differ from workflows: skills are agent-autonomous, workflows are human-led.
- Keep `10_Inbox` transient; avoid long-term storage there.

## Planning Index
- Store horizon plans and reviews in `09_Planning`.
- Keep one active note per horizon (weekly, quarterly, two-year).
- Use weekly reviews to update `00_System/Planning Memory`.

## System Control Files
- Primary LLM instructions: `00_System/LLM Operating Manual.md`.
- Last checkpoint tracker: `00_System/System State.md`.
- Append-only narrative session log: `00_System/Session Log.md`.
- Planning schedule definitions: `00_System/Planning Cadence.md`.
- Recurring operations register: `00_System/Recurring Operations.md`.
- Planning learning memory: `00_System/Planning Memory.md`.
- Folder and note placement map: `00_System/Indexes.md`.
- Document lifecycle rules: `00_System/Document Lifecycle Policy.md`.
- Archive rules: `00_System/Archive Policy.md`.
- Rubbish-bin rules: `00_System/Rubbish Bin Policy.md`.
- Git preservation rules: `00_System/Git Preservation Policy.md`.
- Machine-readable hygiene rules: `00_System/workspace_hygiene_rules.yaml`.
- Local clone setup requirements: `00_System/local_setup_requirements.yaml`.
- Public-template denylist example: `00_System/public_template_denylist.example.txt`.
- Harness-era scope guidance: `14_Guides/Guide - MaxOS Online Scope and Shared Resources.md`.

## Planning Templates
- Templates live in `99_Templates/`.
- Use the folder README and template filenames there as the source of truth.

## Optional Modules
- Optional personal capability packs live in `20_Modules`.
- Default recommendation for shared deployments: keep modules disabled until needed.
