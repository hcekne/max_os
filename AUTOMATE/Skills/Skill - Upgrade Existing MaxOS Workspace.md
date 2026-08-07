---
type: skill
status: active
tags: [migration, upgrade, git, standalone, hosted]
---

# Skill - Upgrade Existing MaxOS Workspace

## Purpose

Upgrade a lived-in legacy Max OS repository to the current five-root layout
and closed SYSTEM kernel without replacing the workspace or losing user files,
instructions, state, memory, or history.

## Trigger

- The owner imports an older personal Max OS repository into MaxOS Online.
- A standalone clone still uses numbered folders, `WORKSPACE/`, or the old
  SYSTEM instruction files.
- The owner asks to update an existing workspace from the public template.

## Inputs

- The existing workspace repository and its current branch.
- The public template remote, normally named `upstream`.
- Hosted or standalone execution mode.

## Hosted steps

1. Use **Import existing Max OS workspace**. Do not bootstrap over the repo;
   the import detects its default branch, creates an internal recovery point,
   and preflights the exact imported tree.
2. If **Migrate workspace** appears, review its preview and apply it. This moves
   numbered and custom folders into the current layout without overwrite.
3. Use **Update from template**. The harness preserves customized root
   instructions, archives retired SYSTEM files byte-for-byte, and carries safe
   State, Log, Memory, and Actor context into the new kernel.
4. Review the migration proposal under `SYSTEM/Proposals/` and the preserved
   sources under `SYSTEM/Cleaning/Archive/System Kernel Migration/`.
5. Push to the personal repository only when the owner chooses; hosted import
   and migration do not silently push there.

Stop and report any migration blocker or unknown Git conflict. Never choose a
blank re-bootstrap as a shortcut for a lived-in repository.

## Standalone steps

1. Start from a clean worktree. Record `git status --short --branch`, create a
   recovery branch, and confirm `upstream` points to the public Max OS template.
   Ensure pushes to `upstream` are disabled.
2. Run `git fetch upstream main`, then
   `git merge --no-commit --no-ff FETCH_HEAD`.
3. Preview the deterministic repair:

   ```sh
   python3 AUTOMATE/Skills/tools/kernel_migration_fixup.py \
     --resolve-known-conflicts
   ```

4. Inspect every reported move and archive action. If the tool reports an
   unknown conflict, collision, or symbolic link, stop for owner review.
5. Apply the same reviewed plan:

   ```sh
   python3 AUTOMATE/Skills/tools/kernel_migration_fixup.py \
     --resolve-known-conflicts --apply
   ```

6. Confirm `git diff --name-only --diff-filter=U` is empty. Review `git status`,
   the migration proposal, and the archive; then run
   `python3 AUTOMATE/Skills/tools/maxos_quality_gate.py --root .`.
7. Stage and commit the migration only after those checks pass. Push only to
   the owner's repository, never to `upstream`.

## Outputs

- Current roots: `ACTION CENTER/`, `KNOWLEDGE/`, `PLAN/`, `AUTOMATE/`, and
  `SYSTEM/`.
- User content retained at its mapped destination; custom folders under
  `KNOWLEDGE/`; technical folders and root control files left in place.
- Active context carried into `SYSTEM/State.md`, `Log.md`, `Memory.md`, and
  `Actor.md` where deterministic.
- Exact retired sources in the SYSTEM migration archive and a review proposal.

## Quality checks

- [ ] A recovery branch or hosted internal recovery snapshot exists.
- [ ] No unrecognized conflict was auto-resolved and no destination overwritten.
- [ ] No legacy layout root or unresolved Git conflict remains.
- [ ] Customized `CLAUDE.md` and user workspace content remain present.
- [ ] Retired SYSTEM material exists byte-for-byte in the migration archive.
- [ ] The Max OS quality gate passes before commit.
- [ ] A second fixup run is idempotent and produces no worktree changes.
