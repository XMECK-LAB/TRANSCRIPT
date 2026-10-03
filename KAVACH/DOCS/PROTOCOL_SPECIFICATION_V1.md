# KAVACH Trust-Continuity Capability Protocol V1

## Trust Context
`TC = H(identity, manifest, integrity, structural/runtime state, policy, continuity, recovery, epoch, workload, runtime-instance)`.

## State transition
- REFUSE if identity/context/policy/recovery prerequisites fail.
- HOLD if integrity/structural/continuity evidence is degraded or invalid.
- OPEN only when all required predicates are satisfied.
- Unknown/degraded required evidence never becomes OPEN.

## Capability envelope
A capability is bound to workload, capability, resource, decision, Trust Context digest, epoch, nonce, expiry and provider. The envelope carries no root secret.

## Execution rule
Execution MUST re-appraise current Trust Context. It MUST refuse if current state is not OPEN, the capability epoch differs from the current epoch, the binding differs, the capability is consumed/expired/unknown, or provider validation fails.

## Recovery rule
Recovery verifies the trusted baseline and advances the epoch. It never changes an old capability into a current capability. Fresh authority requires a fresh decision and fresh capability.

## KVC-001
For any capability C issued in epoch N, if current epoch M != N, Execute(C) MUST refuse.

## Evidence
Every security transition is appended to an authenticated hash chain. V1 also maintains an authenticated local head checkpoint to detect simple tail truncation. Under SOFTWARE_REFERENCE this is not rollback-proof against a privileged same-user attacker.
