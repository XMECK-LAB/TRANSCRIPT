<p align="center">
  <img src="../assets/authority-flow.svg" alt="KAVACH authority lifecycle" width="100%" />
</p>

<h1 align="center">KAVACH 2.0</h1>

<p align="center"><strong>Continuity-Bound Authority & Protection Substrate</strong></p>

<p align="center">
  <strong>Authority before protected action.</strong><br/>
  Software Reference / Public Engineering Preview
</p>

---

## KAVACH in one sentence

**KAVACH separates trust from authority, authority from execution, and execution from evidence — then binds those stages through current continuity.**

The system is designed for protected software actions where a permission should not remain valid merely because it was valid earlier.

## Architecture

```text
ProtectionRequest
      │
      ▼
TrustContext  ←  AIRS appraisal
      │
      ▼
ProtectionDecision
OPEN / HOLD / REFUSE
      │
      ▼
ProtectionEnvelope
bounded authority + continuity
      │
      ▼
execution-time revalidation
      │
      ▼
RuntimeResult
      │
      ▼
Evidence receipt
```

The public implementation is organized into three layers:

| Layer | Responsibility |
|---|---|
| **kavach_semantic** | Canonical models, deterministic encoding, decision semantics, authority envelopes |
| **kavach_runtime** | AIRS appraisal boundary, provider, state, IPC, evidence, execution |
| **kavach_substrate** | Profiles, SDK, compatibility, adapters, extensions, security passport |

## Core invariants

### 1. Trust does not directly authorize execution

AIRS produces bounded trust context. KAVACH owns the decision.

### 2. Authority is bound, not ambient

A protection envelope binds authority to the exact project, workload, resource, operation, policy, provider, assurance level, and continuity vector.

### 3. Continuity is checked again at execution

A valid envelope can still be refused if current continuity no longer matches its declared dependencies.

### 4. Recovery invalidates stale authority

Recovery advances recovery continuity. Earlier recovery-dependent authority becomes stale rather than silently surviving.

### 5. One-use authority is consumed only on successful execution

Rejected attempts do not consume one-use authority; successful execution does.

### 6. Evidence is part of the execution model

Receipts bind the result back to the authority lineage and continuity state.

## Public software surface

```text
KAVACH/
├── contracts/
├── docs/
├── sdk/
├── src/
│   ├── kavach_semantic/
│   ├── kavach_runtime/
│   └── kavach_substrate/
└── tests/
```

## Fast path

### PowerShell

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python -m unittest discover KAVACH\tests
```

### Bash

```bash
PYTHONPATH="$PWD/KAVACH/src" python -m unittest discover KAVACH/tests
```

Continue with [docs/QUICKSTART.md](docs/QUICKSTART.md).

## Decision model

| State | Meaning |
|---|---|
| **OPEN** | Current trust, policy, provider, assurance, continuity, and constraints admit protected execution |
| **HOLD** | The system cannot safely admit execution yet; additional or current evidence/state is required |
| **REFUSE** | The request conflicts with authority, policy, assurance, continuity, or another protected invariant |

**HOLD is not failure and REFUSE is not uncertainty.**

## Continuity model

KAVACH 2.0 tracks independent continuity generations:

- project
- workload
- provider
- policy
- recovery

An authority envelope declares the continuity dimensions it depends on. Execution compares the envelope against current state before allowing the protected action.

This turns permission into a time- and state-bound object instead of a timeless flag.

## Evidence model

```text
context
  ↓
decision
  ↓
authority
  ↓
operation
  ↓
continuity
  ↓
provider / policy
  ↓
result
  ↓
authenticated evidence
```

The public runtime uses software-reference cryptographic mechanisms and does **not** represent itself as hardware-backed.

## Compatibility

KAVACH 2.0 includes a V1 compatibility projection so the historical capability/epoch model can map into the V2 continuity model without weakening stale-authority behavior.

## Release line

- **Current:** [KAVACH 2.0 — Software Reference](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v2.0.0)
- **Historical:** [KAVACH 1.0 — Engineering Preview](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v1.0.0)

## Assurance boundary

This public release demonstrates software-reference semantics. It does not claim hardware-backed authority, TPM/TEE/HSM assurance, independent security certification, formal verification, or production certification.

See [docs/CLAIM_BOUNDARY.md](docs/CLAIM_BOUNDARY.md).

---

**KAVACH** · Built by **Raaj Mandale** · Published under **XMECK-LAB / TRANSCRIPT**
