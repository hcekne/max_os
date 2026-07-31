---
type: maxos-workflow
name: Weekly Project Steering Executive Briefing Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: project_name
    type: string
    label: Project name
  - name: reporting_period
    type: string
    label: Reporting period
  - name: project_notes_doc_path
    type: document
    label: Project notes
  - name: risks_or_decisions
    type: string
    label: Known risks or decisions
  - name: audience
    type: string
    label: Audience
steps:
- id: steering_intake
  name: Steering Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize project status input for {project_name}. If project_notes_doc_path is provided, read it: {project_notes_doc_path}

    Produce:
    - Reporting period
    - Audience
    - Known progress
    - Known risks or decisions
    - Missing status data
    - Evidence tags
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: status_synthesizer
  name: Project Status Synthesizer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Synthesize the project status.

    Cover:
    - Progress since last update
    - Milestones
    - Workstream status
    - Risks/issues/dependencies
    - Decisions needed
    - Next week priorities
  inputs:
  - steering_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: executive_message_builder
  name: Executive Message Builder
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Turn the project status into an executive steering narrative.

    Produce:
    - So-what headline
    - RAG status with rationale
    - Decisions needed
    - Escalations
    - Risks and mitigations
    - Suggested meeting agenda
  inputs:
  - status_synthesizer
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: steering_brief_draft
  name: Steering Brief Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the executive steering brief from the loop context. Make it concise enough for a busy steering committee.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: steering_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the steering brief so a smart 12-year-old could understand what happened, what matters, what is risky, and what decision is needed.
  inputs:
  - steering_brief_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: steering_critique
  name: Steering Brief Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the steering brief. Look for vague status, hidden risks, unclear decisions, too much detail, and weak executive framing.
  inputs:
  - steering_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_steering_brief
  name: Final Weekly Steering Brief
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown briefing:
    # Weekly Project Steering Brief: {project_name}
    1. Executive Summary
    2. RAG Status
    3. Progress This Period
    4. Workstream Updates
    5. Risks, Issues, and Dependencies
    6. Decisions Needed
    7. Next-Period Priorities
    8. Suggested Steering Agenda
    9. Evidence, Assumptions, and Open Questions
  inputs:
  - steering_loop
  output:
    as: file
    format: md
    filename: '{project_name} - Weekly Steering Brief - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: steering_loop
  name: Steering Brief Quality Loop
  inputs:
  - executive_message_builder
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Concise, executive-ready steering brief with clear decisions and risks.
  judge_every: 1
  cycle_targets:
  - steering_brief_draft
  feedback_sources:
  - steering_plain_english
  - steering_critique
  exit_targets:
  - steering_judge
  position:
    x: 1320
    y: 205
judges:
- id: steering_judge
  name: Steering Brief Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the steering brief is concise, executive-ready, risk-aware, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_steering_brief
  retry_targets:
  - steering_loop
  position:
    x: 2430
    y: 205
---

# Weekly Project Steering Executive Briefing Flow

Turns project notes into a concise steering-committee brief with decisions, risks, and an executive framing quality loop.
