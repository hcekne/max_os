---
type: actor
status: draft
actor_type: human
---
<!-- maxos-actor-placeholder: the MaxOS app replaces this file when the workspace is created -->

# Actor

Who owns this workspace, and what the acting agent may do. This is the first
file an agent reads after `AGENTS.md`.

- In the MaxOS app this file is stamped at workspace creation with the
  actor's real identity.
- Running standalone? Replace this placeholder: set `actor_type` in the
  frontmatter (`human` — a person working with an LLM, or `ai` — an agent
  that owns this workspace as its persistent memory), then fill the sections
  below.

## Role

- One line on the actor's purpose and remit.

## Autonomy & permissions

- What the agent may do unsupervised.
- What requires an owner checkpoint or escalation.

## Operating notes

- Standing preferences, constraints, and escalation rules to honour in every
  session.
