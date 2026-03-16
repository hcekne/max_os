# PDF Profiles

Drop LinkedIn profile PDFs here for processing into `01_People/` notes.

## How it works

```
PDF_Profiles/
├── Unprocessed/      ← Put new PDFs here
├── Extracted_Text/   ← Intermediate text (auto-managed, don't touch)
└── Processed/        ← Done PDFs land here automatically
```

1. Save a LinkedIn profile as PDF (see `14_Guides/Guide - Export LinkedIn Profiles as PDF.md`).
2. Drop the PDF into `Unprocessed/`.
3. Ask your AI: **"process my PDF profiles"**.
4. The agent extracts text, creates/updates person notes in `01_People/`, and moves files through the pipeline.

## Naming convention
Name each PDF as `First Last.pdf` so the skill can match it to existing person notes.

## See also
- `15_Skills/Skill - Process PDF Profiles to People Notes.md` — full skill definition
- `14_Guides/Guide - Export LinkedIn Profiles as PDF.md` — how to export from LinkedIn
