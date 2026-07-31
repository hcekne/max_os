# Agent Registry (Optional Module)

## Purpose
- Provide a simple catalog of specialized agents/tools available to the user.
- Keep this as a discovery and governance layer, not autonomous orchestration.

## Why optional
- Max OS core philosophy remains human + AI collaboration over canonical files.
- This module helps with meta-tasks without turning Max OS into a heavy platform.

## What to store here
- One note per available agent with:
  - `agent_name`
  - `purpose`
  - `allowed_inputs`
  - `produced_outputs`
  - `trigger_examples`
  - `risk_level`
  - `human_approval_required`

## Suggested workflow
1. Check registry when a specialized task appears.
2. Choose the smallest capable agent.
3. Confirm risk level and approval rule.
4. Run task and log outcome in project/todo context.

## Files
- `STATUS.md`
- `Agent - Template.md`
