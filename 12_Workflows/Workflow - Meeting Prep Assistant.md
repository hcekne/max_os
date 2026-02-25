---
type: workflow
status: active
owner: 
review_cycle: monthly
tags: [workflow, meeting, prep, interaction]
---

# Workflow - Meeting Prep Assistant

## Goal
Prepare for meetings with clear strategy, tailored messaging, and concrete next-step plans.

## Inputs
- meeting invite details (date, attendees, agenda)
- relevant notes from people/client/project/interaction history
- current open loops and active priorities

## Steps
1. Create a prep note from `TPL - Meeting Prep` in `06_Interactions/`.
2. Link known participants, client/project, and related prior interactions.
3. Ask AI to synthesize known context and draft a first prep brief.
4. Run a clarification Q&A round with the user (required) before finalizing:
   - What is the real objective of this meeting?
   - What outcome would make this meeting a success?
   - Are there any sensitive topics, red lines, or politics?
   - What do you think each participant wants most?
   - What is your preferred tone/posture for this meeting?
5. Update prep note with clarified answers.
6. Ask AI for final meeting prep package:
   - opening talk track
   - key messages
   - likely objections/questions + suggested responses
   - decision targets and fallback options
   - follow-up actions and owners
7. Review and approve prep note before the meeting.

## AI context rule
Before final prep output, AI should read:
- current prep note
- linked people/client/project notes
- recent interaction notes
- open todos relevant to the meeting topic

## Outputs
- finalized meeting prep note
- concise meeting brief (1-page equivalent)
- post-meeting follow-up checklist draft

## Quality checklist
- [ ] Meeting objective is explicit
- [ ] Stakeholder intent map is filled
- [ ] Key messages are specific and role-appropriate
- [ ] Objection handling is prepared
- [ ] Next-step asks are concrete and time-bound
