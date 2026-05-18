# Indexes

## People Index
- Store all person notes in `01_People`.
- Suggested filename: `First Last.md`

## Organization Index
- Store all organization notes in `02_Organizations`.

## Client Index
- One folder per client inside `03_Clients` if needed for sub-notes.
- Keep the main client note at top of each client folder as `Client - Name.md`.

## Project Index
- Store active projects in `04_Projects`.
- Suggested filename: `Project - Name.md`

## Content Index
- Store written content in `05_Content`.
- Add links to related clients/projects/people in frontmatter and body.
- Use pillar + derivative model for content repurposing.
- Store rich generated HTML artifacts in `05_Content/Artifacts/`.
- Keep source Markdown in its canonical location; artifacts are rendered outputs, not replacement notes.

## Artifact Index
- Store static human-facing HTML artifacts in `05_Content/Artifacts/`.
- Use artifacts for rich visual summaries, previews, dashboards, and shareable views generated from canonical sources.
- Each meaningful artifact should include metadata identifying source files, generated date, generator, and approval status.
- Use `99_Templates/TPL - HTML Artifact.html` for new HTML artifacts.
- Use `99_Templates/TPL - Artifact Manifest.md` for companion manifests.
- Artifact manifests should record source files, artifact file, generation notes, review status, safety review, and any canonical backport plan.
- Generated artifacts may include proposal outputs, but proposed changes are not canonical until applied to Markdown source notes.
- Generated artifacts should be safe to delete without losing canonical truth.

## Notes Index
- Store general ideas and unclassified notes in `11_Notes`.
- Move or link notes later if they become client/project/person specific.
- Keep active notes in `11_Notes/` root.
- Move superseded or redundant notes to `16_Cleaning/Archive/11_Notes/` with `status: archived`.
- Keep one canonical note per major strategy topic when practical.

## Cleaning Index
- Central historical retention lives in `16_Cleaning/Archive/`.
- Central short-retention delete queue lives in `16_Cleaning/Rubbish Bin/`.
- Mirror original source paths under both cleaning roots.
- Rubbish-bin rules: `00_System/Rubbish Bin Policy.md`.

## Workflow Index
- Store repeatable processes in `12_Workflows`.
- Use this for step-by-step human workflows and AI/agent workflows.
- Content workflows:
	- `Workflow - Thought Leadership Article Lifecycle.md`
	- `Workflow - Content Waterfall from Pillar Article.md`
	- `Workflow - Build AI GTM Deck from Ideas or Articles.md`
- Meeting workflow:
	- `Workflow - Meeting Prep Assistant.md`
- HTML artifact and worklet workflows:
	- `Workflow - HTML Artifact Review.md`
	- `Workflow - Weekly Review as HTML Worklet.md`
- Hygiene workflow:
	- `Workflow - Weekly Workspace Hygiene Review.md`

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
- Keep `10_Inbox` transient; avoid long-term storage there.
- Move processed raw captures to `16_Cleaning/Rubbish Bin/10_Inbox/` unless they need historical archive retention.
- `10_Inbox/PDF_Profiles/` holds LinkedIn profile PDFs for processing into `01_People/`.

## Skills Index
- Store agent-executable skill definitions in `15_Skills`.
- Each skill has: Purpose, Trigger, Inputs, Steps, Outputs, Quality Checks.
- The master manifest is `SKILLS.md` at the vault root.
- Skills differ from workflows: skills are agent-autonomous, workflows are human-led.
- Some workflows in `12_Workflows/` are also listed as skills in `SKILLS.md`.
- Active skills:
	- `Skill - Process PDF Profiles to People Notes.md`
	- `Skill - Digest Deck to Markdown.md`
	- `Skill - Export Markdown to Word Document.md`
	- `Skill - Executive Thought Leadership Rewriter with Review Loops.md`
	- `Skill - Evidence Finding and Narrative Integration with Validation Loops.md`
	- `Skill - Create HTML Artifact.md`
	- `Skill - Create HTML Worklet.md`
	- `Skill - Review HTML Artifact Safety.md`
	- `Skill - Convert Markdown to HTML Artifact.md`
	- `Skill - Workspace Hygiene and File Lifecycle Review.md`
	- `Skill - Knowledge System Lint and Link Check.md`
	- `Skill - Pre-Commit Knowledge Quality Gate.md`

## Planning Index
- Store horizon plans and reviews in `09_Planning`.
- Keep one active note per horizon (weekly, quarterly, two-year).
- Use weekly reviews to update `00_System/Planning Memory`.

## System Control Files
- Primary LLM instructions: `00_System/LLM Operating Manual.md`.
- Last checkpoint tracker: `00_System/System State.md`.
- Planning schedule definitions: `00_System/Planning Cadence.md`.
- Planning learning memory: `00_System/Planning Memory.md`.
- Folder and note placement map: `00_System/Indexes.md`.
- Markdown/HTML/JSON document rules: `00_System/Document Model.md`.
- Document lifecycle rules: `00_System/Document Lifecycle Policy.md`.
- Archive rules: `00_System/Archive Policy.md`.
- Rubbish-bin rules: `00_System/Rubbish Bin Policy.md`.
- Git preservation rules: `00_System/Git Preservation Policy.md`.
- Machine-readable hygiene defaults: `00_System/workspace_hygiene_rules.yaml`.
- Local clone setup requirements: `00_System/local_setup_requirements.yaml`.
- Public-template denylist example: `00_System/public_template_denylist.example.txt`.
- Rendering rules for artifacts and worklets: `00_System/Rendering Policy.md`.
- HTML artifact and worklet safety rules: `00_System/Artifact Safety Policy.md`.
- Interactive worklet conventions: `00_System/Worklet Conventions.md`.

## Planning Templates
- Weekly review: `99_Templates/TPL - Review Weekly.md`
- Monthly review: `99_Templates/TPL - Review Monthly.md`
- Yearly review: `99_Templates/TPL - Review Yearly.md`
- General note: `99_Templates/TPL - Note.md`
- Workflow: `99_Templates/TPL - Workflow.md`
- Goal: `99_Templates/TPL - Goal.md`
- Pillar article: `99_Templates/TPL - Content Pillar Article.md`
- Review round: `99_Templates/TPL - Content Review Round.md`
- Derivative asset: `99_Templates/TPL - Content Derivative Asset.md`
- Presentation (AI GTM): `99_Templates/TPL - Presentation AI GTM.md`
- Meeting prep: `99_Templates/TPL - Meeting Prep.md`
- HTML artifact: `99_Templates/TPL - HTML Artifact.html`
- HTML worklet: `99_Templates/TPL - HTML Worklet.html`
- Artifact manifest: `99_Templates/TPL - Artifact Manifest.md`
- Worklet manifest: `99_Templates/TPL - Worklet Manifest.md`
- Lifecycle metadata: `99_Templates/TPL - Lifecycle Metadata.md`
- Archive index: `99_Templates/TPL - Archive Index.md`
- Workspace hygiene proposal: `99_Templates/TPL - Workspace Hygiene Proposal.md`
- Project closeout review: `99_Templates/TPL - Project Closeout Review.md`
- Knowledge lint report: `99_Templates/TPL - Knowledge Lint Report.md`

## Optional Modules
- Optional personal capability packs live in `20_Modules`.
- Default recommendation for shared deployments: keep modules disabled until needed.
- Store optional interactive HTML worklets in `20_Modules/Worklets/`.
- Use `99_Templates/TPL - HTML Worklet.html` for new worklets.
- Use `99_Templates/TPL - Worklet Manifest.md` for worklet manifests.
- Worklet manifests should record purpose, source files, inputs, outputs, state files, harness contract, safety notes, and approval status.
- Worklets may use JSON state for runtime data, but must not silently rewrite canonical Markdown.

## Proposal Outputs
- Store system proposals in `00_System/Proposals/`.
- Store proposed changes as Markdown wherever possible, linked to the canonical source notes they would update.
- HTML artifacts and worklets may display proposal outputs, but the proposal is not canonical until accepted into Markdown.
- If a generated file suggests updates to people, projects, goals, plans, workflows, skills, or system state, backport those updates through explicit Markdown edits.

## Generated vs Canonical Files
- Canonical files are Markdown notes and system files in their normal folders.
- Generated files include HTML artifacts, HTML worklets, JSON state exports, and rendered previews.
- Generated files should identify their source files and approval status.
- Do not silently overwrite canonical Markdown based on generated HTML.
- Treat Git history as the durable record of accepted canonical changes.
