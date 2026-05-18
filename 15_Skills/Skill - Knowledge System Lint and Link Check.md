---
type: skill
status: active
trigger_phrase: run knowledge lint
tags: [skill, lint, validation, markdown, frontmatter, links]
---

# Skill - Knowledge System Lint and Link Check

## Purpose
Validate Markdown files before they enter or change the Max OS knowledge system, with deterministic checks for frontmatter, heading structure, wiki-links, local Markdown links, and lifecycle metadata values.

## When to Use
Use this skill when:
- adding or changing system files, skills, workflows, templates, policies, people notes, project notes, or content notes;
- processing many inbox files into canonical notes;
- preparing a commit that changes Markdown files;
- a user asks whether knowledge-system headers, metadata, or links work;
- weekly or monthly hygiene review needs a structural quality gate.

## Trigger Phrases
- "run knowledge lint"
- "check the knowledge system"
- "validate headers and links"
- "check frontmatter"
- "find broken wiki-links"
- "lint changed Markdown files"

## Inputs
- Workspace root
- Optional scope: changed files, target folder, or full workspace
- Optional report path
- Optional failure mode: errors only, warnings too, or report only

## Outputs
- Terminal lint summary
- Optional Markdown report
- List of broken links, malformed frontmatter, heading issues, and metadata value issues
- Recommended fixes before commit or public-template propagation

## Default Command
Run this before committing substantial Markdown changes:

```bash
python3 15_Skills/tools/knowledge_lint.py --root . --changed-only --fail-on error
```

For a full workspace scan:

```bash
python3 15_Skills/tools/knowledge_lint.py --root . --fail-on error
```

For a Markdown report:

```bash
python3 15_Skills/tools/knowledge_lint.py --root . --changed-only --format markdown --output "00_System/Proposals/Knowledge Lint Report - YYYY-MM-DD.md" --fail-on none
```

## Checks

### Frontmatter
- If YAML frontmatter starts with `---`, it must close.
- If PyYAML is available locally, parse the frontmatter as YAML.
- Warn on duplicate top-level keys.
- Warn on frontmatter lines that are not simple keys, list items, comments, or continuations.
- Warn when known lifecycle fields use values outside Max OS policy sets.

Known lifecycle fields:
- `status`
- `lifecycle`
- `retention_policy`
- `confidentiality`

### Headings
- Every Markdown file should have at least one heading.
- The first heading should be an H1.
- Avoid multiple H1 headings in one file.
- Avoid heading level jumps such as H2 to H4.
- Avoid duplicate heading text inside the same file unless intentional.

### Wiki-Links
- Resolve `[[Note Name]]` links against Markdown note filenames.
- Resolve path-style links such as `[[00_System/Planning Memory]]`.
- Warn when a wiki-link is ambiguous across multiple files.
- Warn when a wiki-link anchor is not found.

### Markdown Links
- Ignore external links such as `https://`, `mailto:`, and similar schemes.
- Check local Markdown links and local asset links.
- Resolve links relative to the current file and the workspace root.
- Warn when local anchors are not found in Markdown targets.

## Severity
- `error`: malformed frontmatter or a local/wiki link that does not resolve.
- `warning`: heading quality issue, ambiguous link, missing anchor, duplicate frontmatter key, or non-standard lifecycle metadata value.

## Process
1. Check `git status --short --branch`.
2. Choose scope:
   - changed files before a commit;
   - target folder after large inbox/project processing;
   - full workspace during monthly hygiene.
3. Run the lint command.
4. Fix `error` issues before committing unless the user explicitly accepts them.
5. Review `warning` issues and fix those that affect navigation, automation, or readability.
6. If many warnings are expected in an older workspace, create a report and handle them in batches.

## Quality Gate
Before committing Max OS structural changes:
- [ ] `knowledge_lint.py --changed-only --fail-on error` passes
- [ ] broken wiki-links are fixed or intentionally deferred in a report
- [ ] local Markdown links resolve
- [ ] frontmatter closes and parses
- [ ] new skills/workflows/templates have clear H1 headings
- [ ] lifecycle metadata uses allowed values where present

## Anti-Patterns
- Do not rely only on visual review for links.
- Do not add frontmatter fields that future agents cannot interpret.
- Do not suppress broken links by converting them to plain text unless the link is genuinely not needed.
- Do not make every warning block useful work in old vaults; report legacy cleanup separately.
- Do not use this lint as approval to delete files.

## Final Reporting Format
Report:
- command run;
- files checked;
- errors and warnings count;
- fixes applied;
- remaining issues needing human review;
- whether it is safe to commit from a knowledge-structure perspective.
