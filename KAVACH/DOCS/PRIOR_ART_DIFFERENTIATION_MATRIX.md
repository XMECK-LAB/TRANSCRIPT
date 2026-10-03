# Prior-Art / Differentiation Matrix

| Area | Established prior art | KAVACH V1 position |
|---|---|---|
| Policy decision/enforcement | NIST ZTA, OPA | Reused pattern; not novel |
| Workload identity | SPIFFE/SPIRE | Future evidence-provider input; not novel |
| Evidence appraisal/attestation | IETF RATS, confidential computing | AIRS maps naturally to evidence/appraisal; not novel |
| Context-restricted authorization | Macaroons, policy/token systems | Capability binding is aligned prior art |
| Epoch capability revocation | Existing capability research/patents | Epoch concept alone is high collision risk |
| Provenance/evidence chains | in-toto, Sigstore/Rekor, audit logs | Hash-chain evidence alone is not novel |
| Attestation-conditioned access | Existing products/patents | High collision risk |
| Trust discontinuity -> old authority permanently non-executable -> verified recovery -> fresh epoch authority, with execution-time re-appraisal and transition receipts | Combination requires deeper claim-by-claim search | Candidate distinctive composition; D2 only |
