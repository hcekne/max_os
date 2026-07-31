# System

This folder holds the control and memory surfaces for Max OS — the files that let the workspace's owner recover state at the start of a session and persist it at the end.

Max OS is **owner-neutral**: the owner may be a **human working with an LLM** or a **pure-AI actor** (e.g. a chief-of-staff agent booted from the public template). The same surfaces serve both. `Actor Profile.md` declares which mode this workspace runs in.

- `Actor Profile.md` is the actor's identity — owner type, role, autonomy, and permissions.
- `LLM Operating Manual.md` is the canonical operating instruction set for any AI working in (or owning) this vault.
- `AI Actor & Memory Model.md` explains how the vault works as an actor's persistent memory across sessions.
- `System State.md` holds current dates, review checkpoints, and active plan links (working memory).
- `Session Log.md` is the append-only narrative of past sessions (episodic memory).
- `Indexes.md` is the placement map for the rest of the vault.
- `Planning Cadence.md` and `Planning Memory.md` support review loops and learned memory.

For an orientation overview, start in the vault-root `README.md`.
