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

## Use Max OS With AI (important)
Max OS works best when used with an AI assistant.
Think of it like this:
- your Markdown notes are the operating system
- you + AI together are the CPU that runs it every day

Pick one setup guide:
- `14_Guides/Guide - VS Code Chat.md`
- `14_Guides/Guide - Codex CLI.md`
- `14_Guides/Guide - Claude Code.md`

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
- `14_Guides/` -> setup guides for VS Code Chat, Codex CLI, and Claude Code
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

## Set Up Your Own Private Max OS Repo (recommended)
Use Max OS as a public starter, then keep your real notes in your own private GitHub repo.

### One-time setup
1. Clone this public repo:
	- `git clone git@github.com:hcekne/max_os.git max_os_personal`
2. Enter the folder:
	- `cd max_os_personal`
3. Rename current remote to `upstream` (public starter):
	- `git remote rename origin upstream`
4. Create your own private repo on GitHub (empty), for example `yourname/max_os_personal`.
5. Add your private repo as `origin`:
	- `git remote add origin git@github.com:<your-username>/max_os_personal.git`
6. Push your copy:
	- `git push -u origin main`

### Daily/weekly sync routine
- Pull latest starter updates from Max OS:
  - `git fetch upstream && git merge upstream/main`
- Push your personal notes to your private repo:
  - `git push origin main`

### Safety tip
Disable accidental push to the public starter remote:
- `git remote set-url --push upstream DISABLED`

## For Advanced Users (optional)
- AI uses `00_System/` as its instruction layer.
- Most users can ignore `00_System/` and just use chat + notes.
