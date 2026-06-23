---
type: maxos-workflow
name: Meeting Prep and Stakeholder Intelligence Flow
version: 1
status: draft
trigger:
  position:
    x: 120
    y: 180
  type: manual
  params:
  - name: meeting_title
    type: string
    label: Meeting title
  - name: client_or_company
    type: string
    label: Client or company
  - name: meeting_date
    type: string
    label: Meeting date
  - name: participant_names
    type: string
    label: Participants
  - name: meeting_goal
    type: string
    label: Meeting goal
  - name: agenda_doc_path
    type: document
    label: Agenda or brief
  - name: previous_notes_doc_path
    type: document
    label: Previous notes
steps:
- id: context_intake
  name: Context Intake Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Normalize the meeting input.

    Inputs:
    - meeting_title: {meeting_title}
    - client_or_company: {client_or_company}
    - meeting_date: {meeting_date}
    - participant_names: {participant_names}
    - meeting_goal: {meeting_goal}
    - agenda_doc_path: {agenda_doc_path}
    - previous_notes_doc_path: {previous_notes_doc_path}

    If an optional document path is non-empty, read that workspace file. If it is blank or missing, continue without it.

    Produce a concise Markdown context pack:
    - Known facts from user input
    - Facts from agenda or previous notes
    - Missing context
    - What the prep needs to answer
    - Evidence tags: user-provided, document-derived, external-research-needed, inferred
  inputs:
  - trigger
  output:
    as: text
  position:
    x: 440
    y: 80
- id: stakeholder_research
  name: Stakeholder Research Agent
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Research the participants and organizations relevant to this meeting. Use current external sources where useful, plus the context intake.

    Produce:
    - Participant table: person, role, organization, likely responsibilities, likely priorities, useful conversation hooks
    - Organization context: business model, current news, strategic priorities, commercial pressures
    - Relationship map: who likely influences whom
    - Confidence and source notes
  inputs:
  - context_intake
  output:
    as: text
  position:
    x: 780
    y: -40
- id: agenda_analysis
  name: Agenda and Objective Analyst
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Analyze the meeting objective, agenda, and previous notes.

    Produce:
    - What this meeting is really about
    - Decisions or outcomes likely expected
    - Questions the client may ask
    - Questions we should ask
    - Sensitive topics or risks
    - Materials or examples to prepare
  inputs:
  - context_intake
  output:
    as: text
  position:
    x: 780
    y: 190
- id: prep_strategy_pack
  name: Meeting Strategy Aggregator
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Combine the stakeholder research and agenda analysis into one meeting strategy pack.

    Keep it practical. Do not repeat raw research. Produce:
    - Meeting thesis
    - Desired outcome
    - Stakeholder-specific angles
    - Recommended opening
    - 8-12 sharp questions
    - Likely objections and responses
    - Follow-up actions to propose
    - Evidence gaps
  inputs:
  - stakeholder_research
  - agenda_analysis
  output:
    as: text
  position:
    x: 1120
    y: 80
- id: prep_draft
  name: Meeting Prep Draft Writer
  provider: claude
  model: opus
  thinking: high
  prompt: |
    Draft the meeting prep note from the loop context. Make it useful for a consultant walking into the meeting.

    Include:
    - One-page brief
    - Stakeholder map
    - Talk track
    - Questions to ask
    - Watch-outs
    - Suggested follow-up email bullets
  inputs: []
  output:
    as: text
  position:
    x: 1510
    y: -30
- id: prep_plain_english
  name: Plain-English Rewrite Agent
  provider: claude
  model: sonnet
  thinking: medium
  prompt: |
    Rewrite the draft so a smart 12-year-old could understand what is going on and why it matters.

    Keep professional tone, but remove jargon. Use concrete examples. If any part is vague, make it specific or flag it.
  inputs:
  - prep_draft
  output:
    as: text
  position:
    x: 1840
    y: -30
- id: prep_critique
  name: Prep Challenger
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Critique the meeting prep like a skeptical partner.

    Identify:
    - Unsupported claims
    - Missing stakeholder logic
    - Weak or generic questions
    - Anything too complex for a non-expert
    - Concrete improvements for the next loop
  inputs:
  - prep_plain_english
  output:
    as: text
  position:
    x: 2170
    y: -30
- id: final_meeting_prep
  name: Final Meeting Prep Pack
  provider: codex
  model: gpt-5.5
  thinking: high
  prompt: |
    Create the final Markdown meeting prep pack from the approved loop output.

    Structure:
    # Meeting Prep: {meeting_title}
    1. Executive Summary
    2. Meeting Goal and Desired Outcome
    3. Participant and Stakeholder Map
    4. Client/Company Context
    5. Likely Agenda and Hidden Agenda
    6. Recommended Talk Track
    7. Questions to Ask
    8. Likely Objections and Responses
    9. Follow-Up Actions
    10. Assumptions, Evidence, and Confidence

    Separate facts, document-derived context, external research, and hypotheses.
  inputs:
  - prep_quality_loop
  output:
    as: file
    format: md
    filename: '{client_or_company} - Meeting Prep - {date}'
  position:
    x: 2830
    y: 95
loops:
- id: prep_quality_loop
  name: Prep Clarity and Quality Loop
  inputs:
  - prep_strategy_pack
  mode: count
  max_iterations: 3
  interval_minutes: 0
  goal: Clear, specific, evidence-aware meeting prep that scores at least 8/10.
  judge_every: 1
  cycle_targets:
  - prep_draft
  feedback_sources:
  - prep_plain_english
  - prep_critique
  exit_targets:
  - prep_quality_judge
  position:
    x: 1390
    y: 205
judges:
- id: prep_quality_judge
  name: Prep Quality Judge
  provider: codex
  model: gpt-5.5
  thinking: xhigh
  prompt: |
    Judge whether the meeting prep is specific, clear, evidence-aware, and practical.
    Return:
    Decision: PASS or RETRY
    Score: N/10
    Reasons:
    Required fixes:
  pass_condition: score >= 8
  inputs: []
  pass_targets:
  - final_meeting_prep
  retry_targets:
  - prep_quality_loop
  position:
    x: 2490
    y: 205
---

# Meeting Prep and Stakeholder Intelligence Flow

Prepares a consultant for a meeting by combining agenda/notes context, stakeholder research, a practical meeting strategy, a plain-English rewrite, and a judge-gated quality loop.
