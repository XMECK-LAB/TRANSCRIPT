# TRANSCRIPT / KAVACH Architecture

TRANSCRIPT is the governed execution infrastructure. KAVACH is its first public authority/protection subsystem.

## System boundary

```text
                  TRANSCRIPT
        Governed Execution Infrastructure
                         │
                         ▼
                      KAVACH
        Authority / Continuity / Protection
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      SEMANTIC        RUNTIME        SUBSTRATE
      contracts       execution      profiles / SDK
      models          evidence       compatibility
      authority       state / IPC    adapters
```

## Authority path

```text
Identity + Context
        │
        ▼
AIRS appraisal
        │ TrustContext
        ▼
KAVACH decision
        │ OPEN / HOLD / REFUSE
        ▼
K-LOCK / ProtectionEnvelope
        │ bounded authority
        ▼
Execution-time revalidation
        │
        ▼
Protected execution
        │
        ▼
Authenticated evidence
```

## Separation of responsibility

### AIRS
Appraises bounded evidence and constructs trust context. AIRS does not grant final execution authority.

### KAVACH semantic kernel
Evaluates the protection request against trust context, continuity, provider assurance, and policy. It owns the explicit execution state.

### K-LOCK / ProtectionEnvelope
Represents bounded authority tied to specific protected-action coordinates rather than a broad ambient permission.

### Runtime
Persists protected state, revalidates authority, controls protected execution, and records evidence.

### Substrate
Composes profiles, compatibility, extensions, project-bound adapters, SDK surfaces, and security-passport reporting around the core invariants.

## Continuity dimensions

KAVACH 2.0 separates continuity into independent generations:

- project
- workload
- provider
- policy
- recovery

This lets the system invalidate authority whose declared dependencies are stale.

## Assurance

The current public provider is a **software reference**. The public release does not claim hardware-backed provider roots or TPM/TEE/HSM assurance.

Continue with:

- [KAVACH/docs/NORMATIVE_CONTRACT.md](../KAVACH/docs/NORMATIVE_CONTRACT.md)
- [KAVACH/docs/RUNTIME_CONTRACT.md](../KAVACH/docs/RUNTIME_CONTRACT.md)
- [KAVACH/docs/SUBSTRATE_CONTRACT.md](../KAVACH/docs/SUBSTRATE_CONTRACT.md)
- [KAVACH/docs/TRACEABILITY_MATRIX.md](../KAVACH/docs/TRACEABILITY_MATRIX.md)
