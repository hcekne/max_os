# Max OS

A simple operating system for work powered by AI and fully text based.

You write notes.

AI helps you organize them, plan your day, and keep projects moving.

As you create content into the structure the AI will become better at understanding your goals and helping you to fullfill and reach said goals.

Max OS is just organized Markdown files that link to each other.

## Start Here (Super Simple)
1. Open this folder in your editor.
2. Start a chat with AI.
3. Paste this:

"Use this workspace as Max OS. Read `00_System/LLM Operating Manual.md`. Check `00_System/System State.md` and tell me what I should do today. Then process anything in `10_Inbox/` and give me my top 3 actions."

That is enough to get started.

## How to Use Max OS Daily
1. Write notes during the day.
2. If you are in a hurry, dump rough notes in `10_Inbox/`.
3. Ask AI to process inbox notes and file them correctly.
4. Work your top tasks.
5. At the end of the day, ask AI to update `00_System/System State.md`.

## Goals vs Planning (important)
- `13_Goals/` = where you define big outcomes you want to achieve.
- `09_Planning/` = where you decide what to do this week/month/quarter.
- Best practice: every weekly plan should support one or more goals.

## What Goes Where
- `01_People/` -> people notes
- `02_Organizations/` -> organizations and companies
- `03_Clients/` -> client notes
- `04_Projects/` -> project notes
- `05_Content/` -> articles, video ideas, scripts, publishing notes
- `06_Interactions/` -> meeting/call/chat notes
- `07_Daily/` -> daily planning and daily log
- `08_Todos/` -> actionable tasks
- `09_Planning/` -> weekly/quarterly/yearly planning
- `10_Inbox/` -> quick capture, process later
- `11_Notes/` -> general notes and ideas that do not fit anywhere yet
- `12_Workflows/` -> step-by-step workflows (including AI/agent workflows)
- `13_Goals/` -> big work goals and long-term outcomes
- `20_Modules/` -> optional personal modules (off by default)
- `99_Templates/` -> templates for new notes

## Helpful Templates
- General note: `99_Templates/TPL - Note.md`
- Workflow: `99_Templates/TPL - Workflow.md`
- Goal: `99_Templates/TPL - Goal.md`
- Interaction: `99_Templates/TPL - Interaction.md`
- Project: `99_Templates/TPL - Project.md`
- Todo: `99_Templates/TPL - Todo.md`

## Linking Notes (simple)
- Use `[[Note Name]]` to link notes together.
- Example: link a project to a goal, then link daily tasks to that project.
- The more you link notes, the better AI can follow context.

## Obsidian Compatibility
- This structure works very well in Obsidian.
- You can browse folders normally and use backlinks/graph view for connected context.
- You can use Max OS in any Markdown app, but Obsidian gives the best linking experience.

## For Advanced Users (optional)
- AI uses `00_System/` as its instruction layer.
- Most users can ignore `00_System/` and just use chat + notes.
