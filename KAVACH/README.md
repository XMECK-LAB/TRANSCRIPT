# KAVACH 2.0

## Continuity-Bound Authority & Protection Substrate

**Status:** Software Reference / Public Engineering Preview  
**Parent:** TRANSCRIPT — Governed Execution Infrastructure  
**Assurance:** Software reference, non-hardware

KAVACH models protected software actions around an explicit authority lifecycle.

> **Trust is not authority. Authority is not execution. Execution requires current continuity.**

## Model

```text
IDENTITY / CONTEXT
        ↓
AIRS
trust appraisal
        ↓
KAVACH
OPEN / HOLD / REFUSE
        ↓
K-LOCK
bounded authority
        ↓
EXECUTION
        ↓
EVIDENCE
authenticated receipt
```

The public software reference demonstrates semantics for trust appraisal, bounded authority, continuity, stale-authority refusal, one-use authority, recovery invalidation and authenticated evidence.

## What this release does not claim

- hardware-backed authority
- TPM / TEE / HSM assurance
- independent security certification
- formal verification
- production security certification
- admitted external TRANSCRIPT / XPADI / XAIPT / XLP consumers
- trusted publisher signing

## Public source

- `src/kavach_semantic/`
- `src/kavach_runtime/`
- `src/kavach_substrate/`
- `sdk/`
- `tests/`
- `contracts/`
- `docs/`

Private Founder qualification evidence, predecessor custody, private adapters and future integration mappings are intentionally excluded.