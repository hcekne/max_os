---
type: maxos-workflow
name: Operating Model and Org Design Diagnostic Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: client_or_function
    type: string
    label: Client or function
  - name: transformation_goal
    type: string
    label: Transformation goal
  - name: current_pain_points
    type: string
    label: Current pain points
  - name: org_doc_path
    type: document
    label: Org or process document
  - name: scope
    type: string
    label: Scope
steps:
- id: operating_model_intake
  name: Operating Model Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the operating model diagnostic input. If org_doc_path is provided, read it: {org_doc_path}

    Produce:
    - Transformation goal
    - Scope
    - Current pain points
    - Known org/process facts
    - Unknowns
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: current_state_mapper
  name: Current-State Mapper
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Infer and map the current operating model.

    Cover:
    - Roles and decision rights
    - Core processes
    - Handoffs
    - Governance forums
    - Systems and data
    - Pain points and root causes
  inputs:
  - operating_model_intake
  output:
    as: text
  position:
    x: 760
    y: -40
- id: target_state_designer
  name: Target-State Designer
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Design a business-level target operating model. Do not specify technical architecture.

    Include:
    - Design principles
    - Roles and decision rights
    - Process changes
    - Governance
    - Human/agent or automation opportunities if relevant
    - Transition risks
  inputs:
  - current_state_mapper
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: diagnostic_draft
  name: Diagnostic Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the operating model diagnostic from the loop context. Make it useful for executives and process owners.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: diagnostic_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the diagnostic so a smart 12-year-old could understand who does what today, what is broken, and how the future model fixes it.
  inputs:
  - diagnostic_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: diagnostic_critique
  name: Operating Model Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the diagnostic. Look for vague roles, unrealistic governance, missing handoffs, weak root causes, and too much jargon.
  inputs:
  - diagnostic_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_operating_model_diagnostic
  name: Final Operating Model Diagnostic
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown diagnostic:
    # Operating Model and Org Design Diagnostic: {client_or_function}
    1. Executive Summary
    2. Current-State Operating Model
    3. Pain Points and Root Causes
    4. Roles, Decision Rights, and Handoffs
    5. Systems, Data, and Governance
    6. Target-State Operating Model
    7. Change Roadmap
    8. Risks and Controls
    9. Validation Questions
  inputs:
  - operating_model_loop
  output:
    as: file
    format: md
    filename: '{client_or_function} - Operating Model Diagnostic - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: operating_model_loop
  name: Operating Model Quality Loop
  inputs:
  - target_state_designer
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Clear, realistic, business-level operating model diagnostic.
  judge_every: 1
  cycle_targets:
  - diagnostic_draft
  feedback_sources:
  - diagnostic_plain_english
  - diagnostic_critique
  exit_targets:
  - operating_model_judge
  position:
    x: 1320
    y: 205
judges:
- id: operating_model_judge
  name: Operating Model Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the diagnostic is realistic, specific, business-level, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_operating_model_diagnostic
  retry_targets:
  - operating_model_loop
  position:
    x: 2430
    y: 205
---

# Operating Model and Org Design Diagnostic Flow

Maps current-state operating model pain points, designs a business-level target model, and checks clarity through a looped reviewer.
