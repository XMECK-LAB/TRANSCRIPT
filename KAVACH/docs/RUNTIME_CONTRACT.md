# KAVACH 2.0 Block B Runtime Contract

- Runtime is authoritative; clients cannot set trust, continuity, OPEN/HOLD/REFUSE, or evidence.
- AIRS constructs TrustContext only from bounded evidence observations.
- SOFTWARE_REFERENCE implements the first provider contract using HMAC-SHA-256/HKDF-like domain-separated derivation semantics; it is not hardware-backed.
- Evidence uses an authenticated append sequence plus independent durable head and pending journal.
- IPC framing is authenticated, bounded, freshness-checked, and replay-detected.
- Continuity, policy, provider, runtime, extension, compatibility, and evidence state are separate stores.
- Execution repeats current TrustContext/provider/policy/continuity checks.
- Recovery increments only recovery continuity and never mutates existing envelopes.
- Block B does not admit UI, hardware provider claims, survival/recovery extensions, XPADI integration, or installer work.
