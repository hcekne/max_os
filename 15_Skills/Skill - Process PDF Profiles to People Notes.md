---
type: skill
status: active
trigger_phrase: process my PDF profiles
tags: [skill, profiles, linkedin, extraction, people-notes]
---

# Skill - Process PDF Profiles to People Notes

## Purpose
Process LinkedIn profile PDFs end-to-end: extract text, create or update person notes in `01_People/`, and move files through the processing pipeline automatically.

## Trigger
Use this skill when the user says **"process my PDF profiles"** or when new PDFs appear in `10_Inbox/PDF_Profiles/Unprocessed/`.

## Folder Contract
All PDF profile processing uses this folder structure inside `10_Inbox/PDF_Profiles/`:

```
10_Inbox/PDF_Profiles/
├── Unprocessed/         ← Drop LinkedIn profile PDFs here
├── Extracted_Text/      ← Intermediate text files (auto-managed)
└── Processed/           ← Successfully processed PDFs land here
```

For instructions on how to create LinkedIn profile PDFs, see `14_Guides/Guide - Export LinkedIn Profiles as PDF.md`.

## Inputs
- One or more `.pdf` files in `10_Inbox/PDF_Profiles/Unprocessed/`

## End-State Definition
After a successful run:
- `10_Inbox/PDF_Profiles/Unprocessed/` is empty (except failures)
- `10_Inbox/PDF_Profiles/Extracted_Text/` is empty (except ambiguities)
- PDFs have been moved to `10_Inbox/PDF_Profiles/Processed/`
- All corresponding person notes in `01_People/` are updated or created

---

## Phase 1 — Intake and Extraction

1. Scan `10_Inbox/PDF_Profiles/Unprocessed/` for `.pdf` files.
2. For each PDF, run primary extraction with `pdftotext -layout`.
3. If `pdftotext -layout` is unavailable or produces empty output, use fallback parser chain: `pypdf → pymupdf → pdfplumber`.
4. Save extracted text as one file per person in `10_Inbox/PDF_Profiles/Extracted_Text/`.
5. If extraction succeeds (non-empty text), move source PDF to `10_Inbox/PDF_Profiles/Processed/`.
6. If extraction fails, keep PDF in `10_Inbox/PDF_Profiles/Unprocessed/` and flag it in the run summary.

### Extraction method details
- Default command per file:
  ```
  pdftotext -layout "10_Inbox/PDF_Profiles/Unprocessed/<file>.pdf" "10_Inbox/PDF_Profiles/Extracted_Text/<file>.txt"
  ```
- Consider extraction successful only when output text is non-empty and contains usable profile fields.
- Use parser-chain fallback only when default extraction fails due to missing binary, runtime error, or empty/garbled output.
- Record fallback usage in the run summary when it is used.

## Phase 2 — One-by-One Person Processing

Process each file in `10_Inbox/PDF_Profiles/Extracted_Text/` sequentially, one at a time:

1. Derive person name from filename.
2. Search for corresponding note in `01_People/`.
3. If note exists: update and enrich that specific note.
4. If note does not exist: create a new note using `99_Templates/TPL - Person.md`.
5. After successful update/create, delete the text file from `10_Inbox/PDF_Profiles/Extracted_Text/`.

---

## Mandatory Data-Quality Rules (strict)

These rules are required for every profile and override any weak extraction artifacts.

### A) Employment vs Education Separation
- Never use `Education` section as source for current role or current organization.
- Never map school names (e.g., MIT, Harvard, Imperial) into current employer fields unless the profile clearly shows active employment there.
- Current organization and role must come from:
  1. Headline, and/or
  2. Most recent `Experience` item with `Present`.

### B) Frontmatter must be coherent
Ensure frontmatter is fully aligned with extracted current-employment signals:
- `organization:` current employer (wiki-link if applicable)
- `role:` current role/title
- `location:` current location from profile header
- `last_interaction:` only update if a real interaction occurred
- `next_follow_up:` set only when an actual follow-up date exists

### C) Snapshot must mirror frontmatter
In `## Snapshot`, ensure:
- Organization matches frontmatter organization.
- Role matches frontmatter role.
- Location matches frontmatter location.
- No blank role field.

### D) Employment history quality
When updating history sections:
- Prioritize `Experience` chronology for current/previous roles.
- Keep role progression coherent (avoid mixing different entries into one broken title).
- Do not import noisy UI fragments (e.g., "Show all", "More", "Contact info", ads, recommendations).

### E) New profile minimum standard
A newly created note must include:
- Valid frontmatter (`organization`, `role`, `location` populated when available)
- `## Snapshot`
- `## What I Know`
- `## Current Topics`
- `## How I Can Add Value`
- `## Open Loops`
- `## Interactions`
- `## Next Actions`
- `## LinkedIn Profile Snapshot (YYYY-MM-DD)` with source file reference

## Field Mapping Priority (for role/organization correctness)
Use this precedence when conflicts occur:
1. Experience entry with `Present` (highest confidence)
2. Headline
3. Top profile organization line near name
4. Historical experience
5. Education (never for current employment fields)

---

## Validation Checklist (run at end)
1. **Coverage check:**
   - Count input PDFs processed.
   - Count text files processed.
   - Confirm no files remain in Unprocessed/ or Extracted_Text/ (except explicit failures or ambiguities).
2. **Note completeness check for touched people:**
   - No blank `role` in frontmatter.
   - No blank `- Role:` in Snapshot.
3. **Contamination check:**
   - Flag if `organization` appears to be an education institution while current role indicates another employer.
4. **Report:**
   - Updated notes list
   - Created notes list
   - Extraction failures list
   - Ambiguous matches requiring manual confirmation

## Ambiguity Handling
If two existing person notes are plausible matches for one text profile:
- Do not merge automatically.
- Mark as ambiguous and request confirmation.
- Keep text file in `10_Inbox/PDF_Profiles/Extracted_Text/` until resolved.

## Output Summary Format (for each run)
```
PDFs found in Unprocessed/:       N
Text files extracted:             N
Person notes updated:             N
Person notes created:             N
PDFs moved to Processed/:        N
Text files cleaned up:            N
Failures/ambiguities:             N + list
```

## Operating Principle
Precision over speed. One profile at a time. No bulk profile writing.
