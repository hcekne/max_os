# Agent Inbox

Files and requests waiting for Max OS to process. **Upload to Max OS** places
ordinary workspace uploads here.

## Rules
- Capture quickly here first.
- Do not keep items here long-term.
- Process inbox items at session start or once daily.
- After routing, move processed captures out of active inbox roots.
- Use `16_Cleaning/Rubbish Bin/10_Action_Center/Agent_Inbox/` as the default destination for low-retention processed raw captures.
- Use `16_Cleaning/Archive/10_Action_Center/Agent_Inbox/` when the raw capture has historical value.
- When scanning inbox folders, list directories directly before relying on globbed search.

## Processing target folders
- People-related notes -> `01_People/`
- Organization notes -> `02_Organizations/`
- Client notes -> `03_Clients/`
- Project notes -> `04_Projects/`
- Reusable content -> `05_Content/`
- Conversation records -> `06_Interactions/`
- Day execution notes -> `07_Daily/`
- Action backlog -> `08_Todos/`

## Suggested prompt
"Process whatever I added yesterday in `10_Action_Center/Agent_Inbox/`. Create or update canonical notes using templates, extract tasks into `08_Todos/` or today's daily note, and leave a short change summary."

LinkedIn profile PDFs can be placed directly here and processed with
`15_Skills/Skill - Process PDF Profiles to People Notes.md`; no special staging
subfolder is required.
