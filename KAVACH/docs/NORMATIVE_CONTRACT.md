# KAVACH 2.0 Block A Normative Semantic Contract

Scope: semantic contract + deterministic semantic kernel only.
Excludes runtime/IPC/UI/TPM/HSM/TEE/PWE/SFF/FASO/RAP/SRM/XPADI adapter/installer.

## Authority split
AIRS appraises. KAVACH decides. K-LOCK enforces. Evidence proves.

## States
OPEN, HOLD, REFUSE.

## Identifiers
Lower-case ASCII: `^[a-z0-9][a-z0-9._:-]{0,127}$`. No normalization of authority-bearing identifiers.

## Canonical serialization
Deterministic canonical JSON for Block A:
UTF-8, no BOM, lexicographically sorted keys, separators `,` and `:`, integers only,
unknown fields rejected by strict constructors, duplicate JSON keys rejected, floats/NaN/Infinity rejected.

## TrustContext
appraisal_state = TRUSTED | UNKNOWN | UNTRUSTED.
UNKNOWN => HOLD. UNTRUSTED => REFUSE. TRUSTED is necessary, not sufficient, for OPEN.

## ContinuityVector
Fields: project, workload, provider, policy, recovery. Non-negative 64-bit integers.
Each envelope declares continuity_dependencies.

KVC-001-V2:
For every dependency d:
`envelope.continuity[d] == current.continuity[d]`.
Mismatch => REFUSE(STALE_CONTINUITY).

V1 projection: V1 epoch == recovery generation. V1 capabilities depend on recovery.

## ProtectionRequest
project_id, workload_id, resource_id, authority_id, operation_id, context_digest,
input_digest, required_assurance. Consumers never submit authoritative trust decisions.

## ProtectionDecision
OPEN/HOLD/REFUSE + trust_context_ref + continuity + constraints + provider/assurance + reasons + evidence_ref.

## ProtectionEnvelope
Binds project/workload/resource/authority/operation/trust context/decision/continuity/policy/provider/assurance/nonce/constraints.
Opaque authority object; possession alone never guarantees execution.

## Authority ancestry
TrustContext -> Decision -> Envelope -> Execution -> Receipt.
Recovery increments recovery generation and closes prior recovery-dependent authority lineage.

## Provider assurance
SOFTWARE_REFERENCE < PLATFORM_BOUND < TPM_BOUND < TEE_ATTESTED < HSM_BOUND < EXTERNAL_AUTHORITY.

## Evidence
Receipts bind project/workload/event/trust/decision/authority/operation/resource/continuity/policy/provider/result/predecessor/authenticator.

## Evaluation order
1 schema/binding
2 context digest
3 policy
4 provider/assurance
5 appraisal state
6 continuity
7 consumption/replay
8 constraints
9 OPEN

## Execution-time re-appraisal
Current TrustContext and ContinuityVector are checked again at execution.

## One-use
Successful one-use execution consumes envelope id. Rejected attempts do not consume it.

## V1 Compatibility Profile 1
connect/status/evaluate/acquire/execute/verify_receipt project onto the V2 kernel without relaxing V1 security semantics.

## Classification
V1-PROVEN: OPEN/HOLD/REFUSE, recovery epoch invalidation, stale authority refusal, execution-time re-appraisal, evidence-chain concept, V1 SDK shape.
FOUNDER-RETAINED: AIRS appraisal role, K-LOCK authority/key role, reversible HOLD, state-gates-authority.
NEW-2.0: ContinuityVector, authority ancestry, ProtectionRequest/Decision/Envelope, provider assurance descriptors, profile descriptors, strict deterministic schema rules.
