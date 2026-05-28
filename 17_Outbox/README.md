# Outbox

Publishing surface for materials this Max OS has produced and is staging for delivery to another actor, agent, or external recipient.

Symmetric to `10_Inbox/`:
- `10_Inbox/` = things arriving for this workspace to process.
- `17_Outbox/` = things leaving this workspace for someone else to pick up.

## Rules
- Drop finished items here only when they are ready for downstream pickup.
- Treat the outbox as transient; do not keep delivered items here long-term.
- One item per file, or one subfolder per multi-file delivery.
- Use `<recipient>/` subfolders when delivering to multiple downstream destinations.
- After delivery, move items to `16_Cleaning/Archive/17_Outbox/` (historical value) or `16_Cleaning/Rubbish Bin/17_Outbox/` (low retention).
- Do not use the outbox as a working area; in-progress drafts belong with the canonical project note.
- Cross-link each outbox item back to the canonical source note(s) that produced it.

## Suggested layout
- `<recipient>/` — one subfolder per recipient when delivering to several parties.
- `Drafts/` — items being prepared but not yet ready for pickup (optional).
- `Delivered/` — short-term hold for items already picked up but not yet archived (optional).

## Suggested prompt
"List everything in `17_Outbox/`, who each item is for, what canonical source it came from, and whether it has been delivered yet."
