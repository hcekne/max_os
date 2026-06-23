---
type: maxos-workflow
name: Workshop Design and Facilitation Pack Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: workshop_topic
    type: string
    label: Workshop topic
  - name: client_or_team
    type: string
    label: Client or team
  - name: participants
    type: string
    label: Participants
  - name: desired_outcome
    type: string
    label: Desired outcome
  - name: duration
    type: string
    label: Duration
  - name: background_doc_path
    type: document
    label: Background document
steps:
- id: workshop_intake
  name: Workshop Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the workshop input. If background_doc_path is provided, read it: {background_doc_path}

    Produce:
    - Objective
    - Participants and likely needs
    - Decisions to make
    - Constraints
    - Risks
    - Missing context
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: workshop_flow_designer
  name: Workshop Flow Designer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Design a practical workshop flow for {workshop_topic}.

    Include:
    - Opening
    - Exercises
    - Discussion prompts
    - Decision moments
    - Breakouts if useful
    - Outputs captured
    - Timing
  inputs:
  - workshop_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: materials_builder
  name: Materials and Facilitation Builder
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Build the facilitation materials plan.

    Produce:
    - Facilitator script
    - Slide or board sections
    - Worksheets or templates
    - Pre-reads
    - Capture format
    - Follow-up outputs
  inputs:
  - workshop_flow_designer
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: workshop_pack_draft
  name: Workshop Pack Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the facilitation pack from the loop context. Make it usable by a facilitator without extra explanation.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: workshop_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the workshop pack so a smart 12-year-old could understand what happens in the room, why each activity exists, and what comes out of it.
  inputs:
  - workshop_pack_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: workshop_critique
  name: Facilitation Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the workshop design. Look for overloaded agenda, unclear decisions, weak exercises, missing outputs, and confusing instructions.
  inputs:
  - workshop_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_workshop_pack
  name: Final Workshop Facilitation Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown pack:
    # Workshop Facilitation Pack: {workshop_topic}
    1. Executive Summary
    2. Workshop Objective
    3. Participants and Roles
    4. Agenda and Timing
    5. Facilitator Script
    6. Exercises and Templates
    7. Decisions and Outputs
    8. Risks and Facilitation Watch-Outs
    9. Follow-Up Plan
  inputs:
  - workshop_loop
  output:
    as: file
    format: md
    filename: '{workshop_topic} - Workshop Facilitation Pack - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: workshop_loop
  name: Workshop Quality Loop
  inputs:
  - materials_builder
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: A practical, clear, timed workshop pack that a facilitator can run.
  judge_every: 1
  cycle_targets:
  - workshop_pack_draft
  feedback_sources:
  - workshop_plain_english
  - workshop_critique
  exit_targets:
  - workshop_judge
  position:
    x: 1320
    y: 205
judges:
- id: workshop_judge
  name: Workshop Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the workshop pack is practical, clear, timed, and outcome-oriented.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_workshop_pack
  retry_targets:
  - workshop_loop
  position:
    x: 2430
    y: 205
---

# Workshop Design and Facilitation Pack Flow

Creates a workshop agenda, facilitator script, exercises, templates, and follow-up plan with a plain-English clarity loop.
