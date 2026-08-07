# Agents

This workspace is **Max OS**. This file is the canonical entry point for any
AI agent, tool-neutral. Read it, then read `SYSTEM/Actor.md` to learn who you
are working for. Read everything else on demand through the routing table
below.

> MaxOS is an actor-owned, portable workspace and, when hosted, an
> application runtime. Markdown files provide canonical workspace context.
> MaxOS Online additionally provides accounts, scoped resources, storage,
> scheduled and event-triggered workflows, always-on execution, monitoring
> and run history. Hosted capabilities are available only when exposed by the
> current session. MaxOS must not be described as merely a collection of
> Markdown files.

Max OS is owner-neutral. Check `actor_type` in `SYSTEM/Actor.md`: in `human`
mode the workspace is a cooperation between a human mind and an LLM — surface
options and defer decisions that are the owner's to make; in `ai` mode you
are the principal — act within the autonomy recorded there.

## Core rules

- The workspace is the owner's system of record — and your memory. When a
  request names a person, company, project, or earlier work, SEARCH the
  workspace first (`rg -il "<name>"` or `grep -ril "<name>"`, plus listing
  the likely folders) and build from what you find. Give a generic answer
  only after a search found nothing, and say that you searched.
- Keep edits minimal, factual, and linked (`[[Note Name]]` wiki-links).
- Do not invent names, dates, commitments, or outcomes.
- One canonical note per topic. Route new material by the table below.
- Move stale material into `SYSTEM/Cleaning/` per `SYSTEM/Policy.md`;
  deletion only through the Rubbish Bin path with owner approval.
- Git safety: never push a remote named `upstream`. Outside the MaxOS
  harness, any push requires owner approval; inside hosted runs, follow the
  injected remotes model.
- Scope is an allowlist. If a folder, project, or repository is not in the
  current session's scope, do not assume it exists or try to reach it. Do not
  bulk-copy shared, organization, or client material into this workspace —
  summarize durable findings into canonical notes instead.
- After meaningful work, append one dated bullet to `SYSTEM/Log.md` and
  update `last_interaction_date` in `SYSTEM/State.md`.

## Routing — where information lives

| Question | Canonical home |
| --- | --- |
| How must every agent behave? | this file |
| Who owns this workspace? | `SYSTEM/Actor.md` |
| What is true right now? | `SYSTEM/State.md` |
| What should future sessions remember? | `SYSTEM/Memory.md` (curated) |
| What happened? | `SYSTEM/Log.md` (append-only) |
| How are files, archives, Git, and generated output handled? | `SYSTEM/Policy.md` |
| How do I run this workspace without the app? | `SYSTEM/Standalone.md` |
| How should a particular folder be used? | that folder's `.instructions.md` |
| How does an agent perform a task? | `AUTOMATE/Skills/` |
| When should work run automatically? | `AUTOMATE/Workflows/` + schedules |
| What structure should a new document use? | `SYSTEM/Templates/` |
| What change is waiting for approval? | `SYSTEM/Proposals/` |

If information fits no row, it does not belong in `SYSTEM/`.

## Validation

- `sh AUTOMATE/Skills/tools/ensure_local_setup.sh` — once per standalone
  clone (hosted runs come pre-wired; see `SYSTEM/Standalone.md`).
- `python3 AUTOMATE/Skills/tools/knowledge_lint.py --root . --changed-only
  --fail-on error` — before committing Markdown changes.
- `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .` — before
  structural commits; add `--full --public-template` for public-template
  work. The pre-commit hook runs the gate automatically once setup is
  installed.
- Do not commit runtime byproducts such as `__pycache__/` or `*.pyc`.

<!-- maxos-workspace-v2:start -->
## MaxOS workspace layout

Use the physical folder names exactly as written below when reading, writing,
linking, or telling the user where a file lives:

- `ACTION CENTER/My Inbox`: results and updates for the user to review.
- `ACTION CENTER/Agent Inbox`: new files and requests for MaxOS to process.
- `ACTION CENTER/Outbox`: finished items ready to download, share, or send.
- `KNOWLEDGE`: long-lived knowledge, including People, Organizations, Clients,
  Projects, Content, Interactions, Notes, and custom user folders.
- `PLAN`: Daily notes, Todos, Goals, Weekly, Quarterly, Reviews, and Two-Year plans.
- `AUTOMATE`: Workflows, Skills, and Modules.
- `SYSTEM`: operating instructions, Guides, Cleaning, Templates, and Storage References.

Do not invent or display retired numbered folder names. Root technical folders,
Git metadata, provider configuration, and `code/` remain at the workspace root.
<!-- maxos-workspace-v2:end -->
