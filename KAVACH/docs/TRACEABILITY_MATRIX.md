# Block A Traceability Matrix

| Mechanism | Class | Specification | Implementation | Proof |
|---|---|---|---|---|
| OPEN/HOLD/REFUSE | V1-PROVEN | Contract §§2,14 | SemanticKernel.evaluate | Semantics tests |
| KVC-001 | V1-PROVEN + NEW-2.0 extension | §6 | ContinuityVector + execute | recovery/provider/policy continuity tests |
| AIRS appraisal boundary | FOUNDER-RETAINED | §§1,5 | TrustContext only | UNKNOWN/UNTRUSTED fail-closed |
| K-LOCK protected authority | FOUNDER-RETAINED + NEW-2.0 | §9 | ProtectionEnvelope | binding/tamper/one-use tests |
| Authority ancestry | NEW-2.0 | §10 | decision/envelope references | deterministic vectors |
| V1 compatibility | V1-PROVEN | §18 | V1Compatibility | V1 projection/stale epoch tests |
| Provider assurance | NEW-2.0 | §11 | ProviderDescriptor | assurance/provider tests |
| Canonical encoding | NEW-2.0 | §4 | canonical.py | canonical/duplicate/float tests |
