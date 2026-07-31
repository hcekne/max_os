# Document Model

Max OS is Markdown-first and multi-format aware.

Operating principle:

> Markdown memory. HTML worklets. JSON state. Git history. Harness runtime.

## Document Types

### Note
A note is canonical Markdown memory.

Use notes for durable truth:
- people, organizations, clients, projects, goals, plans, daily notes, interactions, workflows, skills, system state, and long-term content
- decisions, commitments, facts, open loops, and review outcomes
- Obsidian-style wiki-links such as `[[Project - Name]]`

Notes may use YAML frontmatter for metadata, but the Markdown body remains the human-readable source of truth.

### Artifact
An artifact is a generated or hand-authored human-facing output.

Artifacts are usually HTML when the output benefits from layout, typography, visual grouping, or portable presentation. Artifacts may summarize or render canonical Markdown, but they do not replace it.

Store HTML artifacts in `KNOWLEDGE/Content/Artifacts/`. Each artifact should have source metadata and, when useful, a companion artifact manifest.

### Worklet
A worklet is a small interactive HTML tool or view.

Use worklets for task-specific interfaces such as calculators, review panels, visual planners, or guided forms. Worklets may read Markdown-derived inputs or JSON state, but they must not silently write back to canonical Markdown.

Store worklets in `AUTOMATE/Modules/Worklets/`. Worklets are optional capability modules and should remain usable without turning Max OS into an application repo.

### Proposal
A proposal is a suggested change that has not yet become canonical.

Use proposals for generated edits, review recommendations, draft plans, extracted tasks, or candidate updates to notes. A proposal can be Markdown, HTML, or JSON, but it is not truth until a human or approved workflow applies it to the relevant canonical Markdown note.

### Executable Workflow Recipe
An executable workflow recipe is Markdown with machine-readable YAML
frontmatter.

Use workflow recipes for repeatable MaxOS Online automations created in the
Workflow Builder. The frontmatter contains `type: maxos-workflow`, trigger
configuration, steps, document nodes, loops, judges, and layout metadata. The
Markdown body remains the human-readable description.

Store executable recipes in `AUTOMATE/Workflows/Automations/`. Do not store run
outputs beside the recipes except under `AUTOMATE/Workflows/Automations/artifacts/`.

### State
State is structured machine-readable data.

Use JSON for runtime or worklet state that needs strict structure. Use YAML frontmatter for lightweight note metadata. Avoid using HTML as a state store. Treat Git history as the durable record of how canonical files changed over time.

### Scoped Code Repository
A scoped code repository is a Git repository added to a MaxOS Online chat or
workflow run.

Use code repositories for source code, tests, and engineering work. They are
not canonical Markdown memory by default. If a durable project lesson or
decision should persist in Max OS, summarize it into an appropriate Markdown
note and link to the repository or commit.

## Format Rules

### Use Markdown when
- the file is canonical memory
- the content should be easy to inspect, diff, link, and edit
- the content belongs in core folders such as `KNOWLEDGE/People/`, `KNOWLEDGE/Projects/`, `PLAN/Daily/`, `PLAN/`, `AUTOMATE/Workflows/`, `PLAN/Goals/`, or `AUTOMATE/Skills/`
- the file is an executable workflow recipe whose YAML frontmatter is the recipe contract and whose body is a human description

### Use HTML when
- the output is a rich human-facing view
- layout, interaction, or visual scanning matters
- the file is an artifact or worklet, not canonical memory
- portability is useful

Prefer self-contained HTML unless a harness explicitly provides approved assets or runtime APIs.

### Use JSON when
- worklet state needs strict machine parsing
- the data is generated, runtime-scoped, or temporary
- validation, schema, or deterministic updates matter

JSON state should point back to canonical Markdown sources when relevant.

### Use YAML when
- simple metadata belongs with a Markdown note
- frontmatter improves filtering, routing, or automation

Do not move canonical note bodies into YAML.

## Precedence

When sources disagree, use this order:
1. Canonical Markdown notes and system files
2. Approved Markdown proposals applied to canonical notes
3. JSON state generated from canonical sources
4. HTML artifacts and worklets

Generated HTML is never the authority for changing canonical Markdown by itself.
