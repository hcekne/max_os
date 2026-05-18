---
type: rubbish-bin-index
status: active
created: 2026-05-18
scope: vault-wide
default_retention_days: 30
---

# Central Rubbish Bin Index

Use this surface for quick scans of clearly stale material before purge.

## Path Rule
- Mirror the original source path beneath `16_Cleaning/Rubbish Bin/`.

## Purge Rule
- Files in the rubbish bin are expected to be deleted after their `delete_after` date unless a human rescues them back to an active or archived location.

## Current Contents
This public template intentionally ships with an empty rubbish bin. User workspaces should add entries only for stale, superseded, low-retention material.
