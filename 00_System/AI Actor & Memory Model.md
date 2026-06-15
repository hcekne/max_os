# AI Actor & Memory Model

Max OS is owner-neutral: the actor that owns a workspace may be a **human working with an LLM**, or a **pure-AI actor** (for example a chief-of-staff agent booted from the public template). This note explains how the vault works as that actor's **persistent memory across sessions**.

An AI agent keeps nothing between runs except what is written to disk. The control surfaces below are not just planning hygiene — for an AI actor they *are* its memory. Read them at session start to recover state; write them to persist it.

## Memory surfaces

| Memory type | File / folder | Holds |
| --- | --- | --- |
| Identity (self) | [[00_System/Actor Profile]] | Who the actor is: type, role, autonomy level, permissions, escalation rules. |
| Working memory | [[00_System/System State]] | Current checkpoints, active goals/plans, what is due now. |
| Episodic memory | [[00_System/Session Log]] | Append-only narrative of past sessions. |
| Learned memory | [[00_System/Planning Memory]] | Lessons and patterns distilled from past planning cycles. |
| Intentions | `13_Goals/`, `09_Planning/` | Durable objectives and horizon plans. |
| Perception / action | `10_Inbox/` ↔ `17_Outbox/` | What arrives for the actor, and what it sends to other actors. |

## Read/write contract
- **At session start:** read Identity → Working memory → Episodic (recent) → Learned, following the Session Start Algorithm in [[00_System/LLM Operating Manual]]. Do not duplicate that algorithm here.
- **During the session:** route new facts into canonical notes; record durable decisions, not transient chatter.
- **At session end:** update `System State` after completed reviews, append one dated bullet to `Session Log`, and add to `Planning Memory` when a reusable lesson emerged.

## Principles
- Plain Markdown is the memory substrate — human-readable and editable by either owner type.
- Keep one canonical note per topic; persist durable state, not noise.
- Identity / working / episodic / learned is shared vocabulary for humans and AIs alike.
- For a human-owned workspace the same surfaces serve a **cooperation between a human mind and an LLM** — see [[00_System/Actor Profile]].
