---
type: actor_profile
status: active
actor_type: human
---

# Actor Profile - Me

Identity surface for whoever (or whatever) owns this workspace. Read at session start to recover *who is acting* and *what they are allowed to do*. See [[00_System/AI Actor & Memory Model]] for how this fits the memory model.

## Owner Type
- `human` working with an LLM, or a pure-AI actor (e.g. a chief-of-staff agent booted from this template). Set `actor_type` in the frontmatter accordingly.

## Role
- One line on the actor's purpose and remit. Replace this with your own.

## Autonomy & Permissions
- Autonomy level and what the actor may do unsupervised.
- What requires a human checkpoint or escalation.

## Operating Notes
- Standing preferences, constraints, and escalation rules the actor should honour every session.
