# Outbox

Finished items ready to download, share, send, or hand to an external recipient.
Use My Inbox instead when the owner still needs to review or approve the work.

## Rules
- Drop finished items here only when they are ready for downstream pickup.
- Treat the outbox as transient; do not keep delivered items here long-term.
- One item per file, or one subfolder per multi-file delivery.
- Use `<recipient>/` subfolders when delivering to multiple downstream destinations.
- After delivery, move items to `SYSTEM/Cleaning/Archive/ACTION CENTER/Outbox/` (historical value) or `SYSTEM/Cleaning/Rubbish Bin/ACTION CENTER/Outbox/` (low retention).
- Do not use the outbox as a working area; in-progress drafts belong with the canonical project note.
- Cross-link each outbox item back to the canonical source note(s) that produced it.

## Suggested layout
- `<recipient>/` — one subfolder per recipient when delivering to several parties.
- `Delivered/` — short-term hold for items already picked up but not yet archived (optional).

## Suggested prompt
"List everything in `ACTION CENTER/Outbox/`, who each item is for, what canonical source it came from, and whether it has been delivered yet."
