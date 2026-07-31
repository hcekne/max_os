---
type: guide
status: active
---

# Guide - MaxOS Online Scope and Shared Resources

MaxOS Online runs agents against an explicit scope. The scope is the set of
folders, organization projects, skills, and code repositories the owner has made
available for the current chat or workflow.

## Core Idea

The personal Max OS workspace remains the owner's private Markdown memory.
MaxOS Online can temporarily add other resources to a run:

- **Personal workspace** — the owner's private workspace folders and notes.
- **Organization project** — a shared project workspace owned by an
  organization. It may be read-only or read-write for this run.
- **Organization skill** — a shared skill or instruction supplied by the
  organization context.
- **Code repository** — a Git repository selected for engineering work. It is a
  scoped working resource, not canonical Markdown memory.

If a resource is not in scope, behave as if it does not exist.

## Agent Rules

1. Inspect the available scope before assuming where files live.
2. Keep personal workspace facts in the personal workspace.
3. Treat organization project files as shared project material.
4. Treat code repositories as codebases, not as note folders.
5. Do not bulk-copy organization or client content into personal notes.
6. Do not write to a shared project or repository unless the user asked for it
   and the run has write access.
7. When a durable lesson belongs in the owner's knowledge system, write a short
   summary or link in Markdown rather than copying large source material.

## Workflows

Executable workflows live in `AUTOMATE/Workflows/Automations/` and are identified by
`type: maxos-workflow` frontmatter. The Workflow Builder can use document
inputs from the personal workspace or authorized organization projects.

Use document picker paths rather than hard-coded private paths. This keeps
workflow recipes reusable across users and organizations.

Workflow run artifacts are stored under
`AUTOMATE/Workflows/Automations/artifacts/`. Final leaf outputs are delivered to the
workspace inbox by the harness.

## Public Template Contributions

Reusable improvements can move from a private workspace into the public Max OS
template, but they must be privacy-safe.

Before proposing a public-template contribution:

- remove personal names, client names, private project paths, and proprietary
  facts;
- keep examples generic or clearly fictional;
- include only reusable process structure, templates, skills, or guidance;
- run the public-template quality gate;
- submit the change for human review rather than pushing directly.
