---
type: skill
status: active
trigger_phrase: process my PDF profiles
tags: [skill, profiles, linkedin, extraction, people-notes]
---

# Skill - Process PDF Profiles to People Notes

## Purpose
Turn one or more LinkedIn profile PDFs into accurate, linked person notes in
`KNOWLEDGE/People/` without requiring a special profile-staging folder.

## Trigger
Run when the user asks to process LinkedIn profile PDFs, selects a profile PDF,
or a file-arrival workflow passes a profile PDF from Agent Inbox.

## Inputs
- Preferred: one or more explicit `.pdf` paths in
  `ACTION CENTER/Agent Inbox/`, including an event-provided file path.
- If no paths were supplied: directly list PDF files at the root of Agent Inbox
  and process only files the user identified as profiles or whose extracted
  contents clearly identify them as LinkedIn profiles.
- During migration, explicitly selected PDFs in a preserved legacy
  `PDF_Profiles/` subtree are also valid inputs. Never require that subtree for
  new work. After its last user file is resolved, remove its obsolete README and
  placeholder files, then remove the empty legacy directories.

For instructions on exporting profiles, see
`AUTOMATE/Modules/LinkedIn Profile Import/Guide - Export LinkedIn Profiles as PDF.md`.

## Guardrails
- Process one person at a time. Do not bulk-write person notes.
- Do not move a source PDF until its person note is safely written and checked.
- Never overwrite an existing file when moving a processed PDF; deduplicate the
  destination name.
- Leave failed or ambiguous inputs in Agent Inbox and report them.
- Keep extracted text in runtime scratch space, never in the Markdown workspace.

## Steps

### 1. Establish the input set

1. Resolve each explicit path inside the workspace and reject path escapes.
2. If no paths were supplied, list `ACTION CENTER/Agent Inbox/` directly;
   do not rely only on glob search.
3. Record the exact input count and original relative paths.

### 2. Create temporary extraction space

Create one run-scoped temporary directory outside the workspace and guarantee
cleanup when the run ends. For a shell-capable runner:

```bash
scratch="$(mktemp -d "${TMPDIR:-/tmp}/maxos-profile-XXXXXX")"
trap 'rm -rf "$scratch"' EXIT
```

Do not commit, index, or link to scratch files.

### 3. Extract and validate one profile

For each source PDF:

1. Run `pdftotext -layout "<source.pdf>" "$scratch/<unique-name>.txt"`.
2. If extraction fails or is empty, try an installed supported parser in this
   order: `pypdf`, `pymupdf`, then `pdfplumber`.
3. Treat extraction as successful only when the text contains usable identity
   and profile sections. Do not treat a generic PDF as a LinkedIn profile.
4. If no supported extractor succeeds, leave the PDF untouched and record a
   failure. Do not silently invent profile fields.

### 4. Create or update the person note

1. Derive the person's name from the extracted profile, not only the filename.
   LinkedIn exports may use names such as `Profile.pdf`.
2. Search `KNOWLEDGE/People/` for one clear corresponding note.
3. If one note matches, update that note. If none matches, create one from
   `SYSTEM/Templates/TPL - Person.md`.
4. If multiple notes plausibly match, do not merge. Leave the PDF in Agent
   Inbox and ask for confirmation.
5. Add `## LinkedIn Profile Snapshot (YYYY-MM-DD)` with the original source
   filename and factual profile details.

### 5. Validate and clean up

Only after the note exists on disk and passes the checks below:

1. Move the source PDF to the matching path below
   `SYSTEM/Cleaning/Rubbish Bin/ACTION CENTER/Agent Inbox/`.
2. Use a deduplicated destination name if the target already exists.
3. Delete the corresponding scratch text; the final trap removes the remaining
   run directory.
4. Run `python3 AUTOMATE/Skills/tools/check_vault.py` and confirm this run introduced
   no new structural findings.
5. If an input came from a legacy `PDF_Profiles/` subtree and no unresolved user
   files remain there, remove only its obsolete `README.md` and `.gitkeep`
   placeholders, then remove the empty directories. Never delete a non-empty
   directory or an unrecognized file.

## Data-quality rules

### Current employment
- Take current organization and role first from the latest Experience entry
  marked Present, then from the headline, then from the profile header.
- Never infer a current employer from Education.
- Keep role progression chronological; do not combine unrelated entries into a
  fabricated title.

### Person-note coherence
- Align frontmatter `organization`, `role`, and `location` with the evidence.
- Update `last_interaction` only for a real interaction.
- Set `next_follow_up` only when an actual follow-up date exists.
- Ensure `## Snapshot` matches frontmatter and has no blank role when a role is
  available.
- Exclude LinkedIn interface fragments such as “Show all”, “More”, ads, and
  recommendations.

### Minimum standard for a new note
- Valid frontmatter with available organization, role, and location facts.
- `## Snapshot`
- `## What I Know`
- `## Current Topics`
- `## How I Can Add Value`
- `## Open Loops`
- `## Interactions`
- `## Next Actions`
- `## LinkedIn Profile Snapshot (YYYY-MM-DD)` with source reference.

## Completion checks

- Input count equals processed + failed + ambiguous count.
- Every processed PDF has one corresponding updated or created person note.
- No processed source remains in Agent Inbox.
- Every failed or ambiguous source remains untouched in Agent Inbox.
- No extraction text remains in the workspace or runtime scratch directory.
- No persistent profile-staging folder is created. A legacy `PDF_Profiles/`
  subtree remains only when it still contains unresolved user files.
- Touched notes have coherent current-employment fields and valid links.

## Output summary

```text
PDFs selected:                    N
Person notes updated:             N
Person notes created:             N
PDFs moved to Rubbish Bin:        N
Extraction failures:              N + list
Ambiguous matches:                N + list
```

Precision over speed. Process and validate one profile at a time.
