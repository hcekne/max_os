# Agent Inbox

Files and requests waiting for Max OS to process. **Upload to Max OS** places
ordinary workspace uploads here.

## Rules
- Capture quickly here first.
- Do not keep items here long-term.
- Process inbox items at session start or once daily.
- After routing, move processed captures out of active inbox roots.
- Use `SYSTEM/Cleaning/Rubbish Bin/ACTION CENTER/Agent Inbox/` as the default destination for low-retention processed raw captures.
- Use `SYSTEM/Cleaning/Archive/ACTION CENTER/Agent Inbox/` when the raw capture has historical value.
- When scanning inbox folders, list directories directly before relying on globbed search.

## Processing target folders
- People-related notes -> `KNOWLEDGE/People/`
- Organization notes -> `KNOWLEDGE/Organizations/`
- Client notes -> `KNOWLEDGE/Clients/`
- Project notes -> `KNOWLEDGE/Projects/`
- Reusable content -> `KNOWLEDGE/Content/`
- Conversation records -> `KNOWLEDGE/Interactions/`
- Day execution notes -> `PLAN/Daily/`
- Action backlog -> `PLAN/Todos/`

## Suggested prompt
"Process whatever I added yesterday in `ACTION CENTER/Agent Inbox/`. Create or update canonical notes using templates, extract tasks into `PLAN/Todos/` or today's daily note, and leave a short change summary."

LinkedIn profile PDFs can be placed directly here and processed with
`AUTOMATE/Skills/Skill - Process PDF Profiles to People Notes.md`; no special staging
subfolder is required. Extraction uses temporary runtime storage outside the
workspace. After a person note is validated, the processed PDF is moved out of
Agent Inbox; only failed or ambiguous inputs remain for attention.
