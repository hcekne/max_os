---
type: workflow
status: active
owner:
review_cycle: monthly
tags: [workflow, open-source, pull-request, governance, curation]
---

# Workflow - Backport Private Learnings to Public Repo via Pull Request

## Goal
Turn private Max OS learnings into public, reusable improvements through clean pull requests without leaking sensitive information.

## Inputs
- One or more private learnings (process, template, rule, checklist, workflow)
- Public repo clone/fork
- Target files in public repo

## Steps
1. **Select candidate learning**
   - Choose a learning that is broadly reusable.
   - Prefer system/process improvements over personal specifics.

2. **Run public-safety filter**
   - Remove personal names, private client details, confidential numbers, and internal-only context.
   - Generalize examples where needed.

3. **Define contribution shape**
   - Pick smallest useful change set:
     - system manual update,
     - index/README clarification,
     - reusable workflow/template.

4. **Implement in public repo**
   - Create/modify files in a focused way.
   - Keep naming and folder conventions consistent.

5. **Update discoverability links**
   - Update relevant README/index files so users can find new guidance.
   - Avoid orphan workflows/notes.

6. **Quality pass**
   - Confirm no private data remains.
   - Confirm instructions are actionable by external users.
   - Ensure active vs archive guidance is coherent.

7. **Open pull request**
   - Use branch name describing change scope.
   - PR should include:
     - problem solved,
     - files changed,
     - why this helps all users,
     - any migration/usage notes.

8. **Review and refine**
   - Address feedback with minimal, focused updates.
   - Merge once quality and safety checks pass.

## Outputs
- One public-safe pull request with reusable system improvements
- Updated public documentation/workflows discoverable from indexes

## Quality checklist
- [ ] Contribution is useful beyond one private environment
- [ ] No private names/clients/confidential details included
- [ ] File placement follows `00_System`, `11_Notes`, `12_Workflows`, etc. conventions
- [ ] README/index links updated
- [ ] PR description explains reusable value clearly

## Automation opportunities
- AI-assisted private-to-public redaction pass
- AI-generated PR summary template from git diff
- Automated check for private names/tokens before PR creation
