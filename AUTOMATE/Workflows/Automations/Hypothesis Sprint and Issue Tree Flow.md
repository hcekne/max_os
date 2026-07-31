---
type: maxos-workflow
name: Hypothesis Sprint and Issue Tree Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: client_or_problem
    type: string
    label: Client or problem
  - name: decision_to_support
    type: string
    label: Decision to support
  - name: known_context
    type: string
    label: Known context
  - name: briefing_doc_path
    type: document
    label: Briefing document
steps:
- id: problem_intake
  name: Problem Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the problem statement for {client_or_problem}. If briefing_doc_path is provided, read it: {briefing_doc_path}

    Produce:
    - Decision to support
    - Known facts
    - Unknowns
    - Constraints
    - Initial hypotheses
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 430
    y: 80
- id: issue_tree_builder
  name: Issue Tree Builder
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Build a MECE issue tree for the problem.

    Produce:
    - Primary question
    - Level 1 branches
    - Level 2 sub-questions
    - Hypotheses per branch
    - Evidence needed
    - Analyses required
  inputs:
  - problem_intake
  output:
    as: text
  position:
    x: 760
    y: -30
- id: analysis_plan_builder
  name: Analysis Plan Builder
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Turn the issue tree into an analysis plan.

    Include:
    - Data needed
    - Interviews needed
    - External research needed
    - Quick tests
    - Workplan by workstream
    - Likely charts or outputs
  inputs:
  - issue_tree_builder
  output:
    as: text
  position:
    x: 1090
    y: 80
- id: hypothesis_draft
  name: Hypothesis Pack Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the hypothesis sprint pack from the loop context. Make it useful for a consulting team starting work tomorrow.
  inputs: []
  output:
    as: text
  position:
    x: 1440
    y: -40
- id: hypothesis_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the hypothesis pack so a smart 12-year-old could explain the problem, the branches, and how we will test them.
  inputs:
  - hypothesis_draft
  output:
    as: text
  position:
    x: 1770
    y: -40
- id: hypothesis_critique
  name: Issue Tree Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the issue tree and hypothesis pack. Look for overlapping branches, missing branches, untestable hypotheses, vague analyses, and unclear logic.
  inputs:
  - hypothesis_plain_english
  output:
    as: text
  position:
    x: 2100
    y: -40
- id: final_hypothesis_pack
  name: Final Hypothesis Sprint Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Produce the final Markdown pack:
    # Hypothesis Sprint and Issue Tree: {client_or_problem}
    1. Executive Summary
    2. Decision to Support
    3. Problem Definition
    4. Issue Tree
    5. Hypotheses
    6. Analyses and Evidence Needed
    7. Interview Plan
    8. First-Week Workplan
    9. Risks, Assumptions, and Confidence
  inputs:
  - hypothesis_loop
  output:
    as: file
    format: md
    filename: '{client_or_problem} - Hypothesis Sprint Issue Tree - {date}'
  position:
    x: 2760
    y: 95
loops:
- id: hypothesis_loop
  name: Hypothesis Quality Loop
  inputs:
  - analysis_plan_builder
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: MECE, testable, plain-English issue tree and hypothesis pack.
  judge_every: 1
  cycle_targets:
  - hypothesis_draft
  feedback_sources:
  - hypothesis_plain_english
  - hypothesis_critique
  exit_targets:
  - hypothesis_judge
  position:
    x: 1320
    y: 205
judges:
- id: hypothesis_judge
  name: Hypothesis Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the issue tree is MECE enough, testable, practical, and easy to understand.
    Return Decision: PASS or RETRY, Score: N/10, Reasons, Required fixes.
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_hypothesis_pack
  retry_targets:
  - hypothesis_loop
  position:
    x: 2430
    y: 205
---

# Hypothesis Sprint and Issue Tree Flow

Builds a consulting-style issue tree, hypothesis set, analysis plan, and first-week workplan with a judge-gated refinement loop.
