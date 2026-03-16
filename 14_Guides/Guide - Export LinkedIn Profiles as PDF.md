# Guide - Export LinkedIn Profiles as PDF

## Purpose
Capture high-quality snapshots of LinkedIn profiles as PDFs so they can be processed into `01_People/` notes using the skill `15_Skills/Skill - Process PDF Profiles to People Notes.md`.

## Why PDF?
LinkedIn does not offer a structured export of other people's profiles. The best method is to print the full profile page to PDF from your browser. This captures the name, headline, experience, education, skills, and about section in a format that text extraction tools can parse.

## Step-by-Step Instructions

### 1. Open the profile
Navigate to the person's LinkedIn profile in your browser (Chrome, Edge, Firefox, etc.).

### 2. Zoom out to fit more content
This is the key step most people miss. LinkedIn profiles are long and the browser's default zoom cuts off content.

- **Zoom out to 50–67%** using:
  - `Ctrl + -` (Windows/Linux) or `Cmd + -` (Mac) — press multiple times
  - Or use the browser menu: View → Zoom Out
- Scroll through the entire page first to ensure all "Show more" sections and lazy-loaded content have expanded.
- Click **"Show all experiences"**, **"Show all education"**, and any other expand links before printing.

### 3. Print to PDF
- Press `Ctrl + P` (Windows/Linux) or `Cmd + P` (Mac) to open the Print dialog.
- Set **Destination** to **"Save as PDF"** (not a physical printer).
- Set **Layout** to **Portrait**.
- Set **Scale** to **Custom: 50–70%** if available (this helps fit more content per page).
- Under **More settings**, disable **Headers and footers** (removes browser chrome from the output).
- Click **Save**.

### 4. Name the file
Use the person's name as the filename:
- `First Last.pdf` (e.g., `Jane Smith.pdf`)
- This helps the processing skill match the PDF to existing person notes.

### 5. Drop into the inbox
Move or save the PDF directly into:
```
10_Inbox/PDF_Profiles/Unprocessed/
```

### 6. Process
Ask your AI assistant: **"process my PDF profiles"**

The skill will extract text, create or update person notes, and move files through the pipeline automatically.

## Tips for Better Quality
- **Expand everything first.** Click every "Show more", "Show all N experiences", "Show all education" link before printing. LinkedIn lazy-loads content.
- **Scroll to the bottom** before printing. Some sections only render after scrolling to them.
- **Use Chrome or Edge** for the most consistent PDF output. Firefox works but sometimes clips content.
- **One profile per PDF.** Do not try to combine multiple profiles.
- **Profile must be public or connected.** Limited profiles produce sparse output.

## What the Processing Skill Extracts
The skill reads these fields from the PDF text:
- Name, headline, location
- Current employer and role (from Experience section)
- Full employment history
- Education
- About/summary section
- Skills (when visible)

Fields are mapped to person notes in `01_People/` following the data-quality rules in the skill definition.

## See Also
- `15_Skills/Skill - Process PDF Profiles to People Notes.md` — the agent skill that processes these PDFs
- `01_People/` — where person notes are created/updated
- `99_Templates/TPL - Person.md` — template for new person notes
