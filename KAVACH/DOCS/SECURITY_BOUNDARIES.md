# Security Boundaries
- KAVACH V1 is a research/reference implementation and technical demonstrator.
- The software reference provider is not an HSM/TPM replacement.
- The UI cannot set trusted state; authoritative state lives in the runtime process.
- Protected execution re-appraises current trust at execution time.
- Capability handles are workload/resource/epoch/expiry/use bound.
- Evidence receipts are hash chained and authenticated by the reference runtime root.
- V1 does not claim kernel-compromise resistance, formal verification, new cryptographic primitives, post-quantum guarantees, or commercial certification.
