# KAVACH V1 Threat & Assurance Model

## V1 protects/demonstrates
- stale capability use after trust-epoch transition;
- cross-workload and cross-resource capability reuse;
- execution while current measured trust is not OPEN;
- one-use capability replay;
- malformed/unknown capability use;
- authenticated IPC replay at the request layer;
- receipt mutation/reordering and, with the local ledger-head checkpoint, accidental/simple tail truncation;
- provider failure by failing closed.

## V1 detects/records
- protected fixture integrity discontinuity;
- trust decisions, capability issuance/execution/refusal, recovery and epoch transition;
- receipt-chain verification status.

## V1 does not claim to defeat
- a fully privileged hostile Windows kernel/administrator;
- a same-user attacker able to copy/replace the SOFTWARE_REFERENCE root plus all local state;
- rollback of the complete local workspace by a privileged attacker;
- TPM/HSM/TEE compromise;
- remote hardware attestation attacks;
- causal attribution of why a measurement changed.

`SOFTWARE_REFERENCE` therefore proves protocol semantics and integration behavior, not hardware-rooted host compromise resistance.
