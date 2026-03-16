# Skills

Agent-executable capabilities in Max OS. Each skill describes something an AI agent can perform autonomously within this workspace.

For detailed skill cards, see `15_Skills/`. For human-led step-by-step processes, see `12_Workflows/`.

---

## Core Skills (built into LLM Operating Manual)

### Session Start
- **Trigger:** Beginning of any session
- **Instructions:** `00_System/LLM Operating Manual.md` → Session Start Algorithm
- **Inputs:** Current date
- **Outputs:** Due reviews, operational reminders, daily plan, proposed actions

### Inbox Processing
- **Trigger:** Items pending in `10_Inbox/`
- **Instructions:** `00_System/LLM Operating Manual.md` → Inbox Processing Algorithm
- **Inputs:** Files in `10_Inbox/`
- **Outputs:** Routed notes, created/updated people/org/project notes, extracted tasks

### Interaction Processing
- **Trigger:** New interaction note provided
- **Instructions:** `00_System/LLM Operating Manual.md` → Interaction Update Algorithm
- **Inputs:** Interaction note
- **Outputs:** Updated people/org/client/project notes, changelog

### Note Lifecycle & Archive
- **Trigger:** Monthly review or duplicate notes detected
- **Instructions:** `00_System/LLM Operating Manual.md` → Note Lifecycle and Archive Protocol
- **Inputs:** Notes in `11_Notes/`
- **Outputs:** Archived duplicates, updated indexes

---

## Workflow Skills (in 15_Skills/)

### Process PDF Profiles to People Notes
- **File:** `15_Skills/Skill - Process PDF Profiles to People Notes.md`
- **Inputs:** PDF files in `10_Inbox/PDF_Profiles/Unprocessed/`
- **Outputs:** Created/updated notes in `01_People/`
- **Guide:** `14_Guides/Guide - Export LinkedIn Profiles as PDF.md`

### Meeting Prep
- **File:** `12_Workflows/Workflow - Meeting Prep Assistant.md`
- **Inputs:** Meeting details, attendee names
- **Outputs:** Briefing with attendee context, open loops, suggested talking points

### Write an Article
- **File:** `12_Workflows/Workflow - Write an Article.md`
- **Inputs:** Topic, thesis, target audience
- **Outputs:** Draft article in `05_Content/`

### Content Waterfall from Pillar Article
- **File:** `12_Workflows/Workflow - Content Waterfall from Pillar Article.md`
- **Inputs:** Pillar article
- **Outputs:** Derivative content pieces (LinkedIn posts, carousels, newsletters)

### Build AI GTM Deck
- **File:** `12_Workflows/Workflow - Build AI GTM Deck from Ideas or Articles.md`
- **Inputs:** Ideas or source articles
- **Outputs:** Go-to-market presentation deck

### Backport to Public Repo
- **File:** `12_Workflows/Workflow - Backport Private Learnings to Public Repo via Pull Request.md`
- **Inputs:** Private vault learnings to share
- **Outputs:** Pull request to public repo
