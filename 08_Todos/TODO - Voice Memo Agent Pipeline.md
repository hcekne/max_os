---
type: todo
status: backlog
priority: medium
owner: [[Hans Christian Ekne]]
created: 2026-02-24
target_date: 
tags: [todo, automation, voice, transcription]
---

# TODO - Voice Memo Agent Pipeline

## Why this matters
- Capture thoughts quickly during the day and turn them into searchable notes.
- Reduce manual effort by automating transcription and daily-note updates.

## Outcome (MVP)
- New voice files dropped into an intake folder are detected every 30 minutes.
- New files are transcribed in batch.
- Transcript blocks are appended to today's daily note in `07_Daily/`.
- Optional auto-commit/push keeps updates centralized in GitHub.

## Scope and approach
- Preferred flow: iPhone Voice Memos -> cloud sync/export folder -> polling script.
- Avoid direct device-folder polling as the first implementation.
- Build local-first, then move the same workflow to a cloud runner if useful.

## Tasks
- [ ] Decide intake source (Dropbox, Google Drive, OneDrive, or S3).
- [ ] Create intake folder convention and filename rules.
- [ ] Implement polling script (every 30 min) with a state file for deduplication.
- [ ] Integrate transcription provider (Whisper API or Deepgram).
- [ ] Append transcript entries with timestamp + source file to today's note.
- [ ] Add basic error handling and retry logging.
- [ ] Add optional Git auto-commit/push step.
- [ ] Pilot for 1 week and refine formatting/prompts.

## Risks / constraints
- iOS Voice Memos has limited direct Linux automation support.
- Cost and latency depend on transcription provider and file volume.
- Audio quality and language mix may impact transcript quality.

## Next trigger
- Start when daily capture friction feels high enough to justify automation.

## Links
- [[07_Daily]]
- [[00_System/Interaction Workflow]]
