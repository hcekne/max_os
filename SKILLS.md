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

## Vault Skills (in 15_Skills/)

### Executive Thought Leadership Rewriter with Review Loops
- **File:** `15_Skills/Skill - Executive Thought Leadership Rewriter with Review Loops.md`
- **Inputs:** Original article draft, stakeholder feedback, optional style benchmarks, optional target word count
- **Outputs:** Intake summary, rewrite brief, new structure, two critique/revision loops, final polished draft

### Evidence Finding and Narrative Integration with Validation Loops
- **File:** `15_Skills/Skill - Evidence Finding and Narrative Integration with Validation Loops.md`
- **Inputs:** Full article draft, optional stakeholder feedback, optional geography/sector/source preferences
- **Outputs:** Argument map, insertion points, evidence bank, selected proof points, validation log, rewritten article with integrated evidence

### Process PDF Profiles to People Notes
- **File:** `15_Skills/Skill - Process PDF Profiles to People Notes.md`
- **Inputs:** PDF files in `10_Inbox/PDF_Profiles/Unprocessed/`
- **Outputs:** Created/updated notes in `01_People/`
- **Guide:** `14_Guides/Guide - Export LinkedIn Profiles as PDF.md`

### Digest Deck to Markdown
- **File:** `15_Skills/Skill - Digest Deck to Markdown.md`
- **Inputs:** One source presentation deck as PDF, optional output filename/path
- **Outputs:** One slide-by-slide Markdown digest in `05_Content/` or a requested project folder

### Export Markdown to Word Document
- **File:** `15_Skills/Skill - Export Markdown to Word Document.md`
- **Inputs:** One source Markdown note, optional output filename/path, optional title override, optional portrait/landscape orientation, optional PDF export
- **Outputs:** One formatted `.docx` file suitable for sharing externally, optional `.pdf` export, optional export report

### Create HTML Artifact
- **File:** `15_Skills/Skill - Create HTML Artifact.md`
- **Inputs:** Canonical Markdown source files, artifact purpose, optional output filename
- **Outputs:** Self-contained HTML artifact in `05_Content/Artifacts/`, optional artifact manifest, optional Markdown proposal

### Create HTML Worklet
- **File:** `15_Skills/Skill - Create HTML Worklet.md`
- **Inputs:** Worklet purpose, source files, input/output contract, optional JSON state shape
- **Outputs:** HTML worklet in `20_Modules/Worklets/`, worklet manifest, optional JSON state example or proposal

### Review HTML Artifact Safety
- **File:** `15_Skills/Skill - Review HTML Artifact Safety.md`
- **Inputs:** HTML artifact or worklet, companion manifest, source files, intended viewing context
- **Outputs:** Safety review summary, required fixes, approval recommendation

### Convert Markdown to HTML Artifact
- **File:** `15_Skills/Skill - Convert Markdown to HTML Artifact.md`
- **Inputs:** Source Markdown note or notes, optional target audience, optional artifact filename
- **Outputs:** Read-only HTML artifact in `05_Content/Artifacts/`, optional manifest, optional Markdown proposal

### Workspace Hygiene and File Lifecycle Review
- **File:** `15_Skills/Skill - Workspace Hygiene and File Lifecycle Review.md`
- **Inputs:** Workspace root, optional target folder/project, optional mode (`PLAN_ONLY`, `APPLY_SAFE`, `APPLY_APPROVED`)
- **Outputs:** Hygiene proposal, file classification table, canonical file recommendations, archive/delete/merge candidates, lifecycle metadata recommendations

### Knowledge System Lint and Link Check
- **File:** `15_Skills/Skill - Knowledge System Lint and Link Check.md`
- **Inputs:** Workspace root, optional changed-file scope, optional report path
- **Outputs:** Frontmatter, heading, wiki-link, local Markdown link, and lifecycle metadata validation report

### Pre-Commit Knowledge Quality Gate
- **File:** `15_Skills/Skill - Pre-Commit Knowledge Quality Gate.md`
- **Inputs:** Workspace root, optional full-workspace mode, optional public-template privacy mode, optional private denylist
- **Outputs:** Pass/fail summary for whitespace, knowledge lint, runtime byproducts, and privacy/secret checks

---

## Workflow Skills (in 12_Workflows/)

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

### Weekly Workspace Hygiene Review
- **File:** `12_Workflows/Workflow - Weekly Workspace Hygiene Review.md`
- **Inputs:** Recent file changes, workspace scope, Git status, active project state
- **Outputs:** Weekly hygiene proposal, safe archive recommendations, lifecycle metadata recommendations
