# Automations (machine-readable workflows)

Files in this folder are executable workflows created by the MaxOS Web Workflow
Builder. Each carries a `type: maxos-workflow` frontmatter marker; the harness
lists, schedules, and runs them by that marker — not by this folder.

- Prefer editing workflows in the Workflow Builder. The frontmatter holds the
  recipe (trigger + steps); edit it by hand only if you know the schema.
- The Markdown body is a human description and is safe to edit.
- Run artifacts are written to `12_Workflows/Automations/artifacts/`.
- Final leaf outputs are also delivered to the workspace inbox by the harness.
- Free-form workflows without the marker (e.g. in the `12_Workflows/` root) are
  ignored by the harness and left untouched.
- Document inputs should be selected through the Workflow Builder document
  picker. They must point to files the owner can access in the workspace or in a
  scoped organization project.
