# Skills

This folder contains agent-executable skill definitions — structured descriptions of tasks that AI agents can perform autonomously within Max OS.

## What is a skill?

A skill is a capability an agent can execute with defined inputs, steps, and outputs. Skills differ from workflows:

| | Skill | Workflow |
|---|---|---|
| **Executor** | Agent (autonomous) | Human-led, AI-assisted |
| **Structure** | Input → process → output | Step-by-step with human checkpoints |
| **Location** | `15_Skills/` | `12_Workflows/` |

Some workflows in `12_Workflows/` are also agent-executable. Those are listed in `SKILLS.md` at the vault root.

## Creating a new skill

Use the template `99_Templates/TPL - Skill.md` or follow this structure:

```
# Skill - [Name]

## Purpose
One sentence describing what this skill does.

## Trigger
When should this skill be invoked?

## Inputs
- What the agent needs to start

## Steps
1. Step-by-step execution instructions

## Outputs
- What the agent produces

## Quality Checks
- How to verify the output is correct
```

## See also
- `SKILLS.md` — master manifest of all skills (at vault root)
- `12_Workflows/` — human-led processes (some also agent-executable)
- `00_System/LLM Operating Manual.md` — core algorithms that function as built-in skills
