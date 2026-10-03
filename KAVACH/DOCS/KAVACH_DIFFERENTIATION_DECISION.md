# KAVACH V1 Differentiation Decision

## Decision: D2

KAVACH V1 is best characterized as a **distinctive protocol/system composition whose legal novelty remains unproven and requires an independent professional patent search**.

The defensible engineering center is not OPEN/HOLD/REFUSE naming, HMAC, SHA-256, epochs, attestation, capability tokens, policy engines, or audit chains individually. All have substantial prior art.

The candidate differentiating composition is **trust-continuity capability security**: protected authority is bound to a measured Trust Context and continuity epoch; execution re-appraises current trust; a trust discontinuity prevents prior authority from executing; recovery creates fresh authority in a new epoch; and the transition is represented by authenticated evidence receipts.

This is an engineering differentiation decision, not a legal patentability opinion.

## Prior-art collision map

- Policy decision/enforcement separation: established (NIST ZTA, OPA).
- Workload identity/attestation: established (SPIFFE/SPIRE, IETF RATS, confidential computing).
- Context-bound credentials/caveats: established (Macaroons and related token systems).
- Epoch-bound authorization/capability revocation: established, including patent literature.
- Signed/hash-chained provenance/transparency: established (in-toto, Sigstore/Rekor and audit-log literature).
- Attestation-conditioned authorization: established, including patent literature.

## Candidate KAVACH territory

The candidate territory is the **specific lifecycle composition and invariant set**, especially the combination of:
1. a versioned Trust Context;
2. capability/resource/workload binding;
3. execution-time re-appraisal rather than issuance-only trust;
4. discontinuity-triggered epoch closure;
5. no resurrection of prior authority after recovery;
6. authenticated transition evidence linking appraisal, issuance/refusal, execution/refusal, discontinuity and recovery;
7. provider-independent enforcement semantics with an explicit assurance profile.

Any future invention disclosure should claim concrete state transitions, bindings, invariants and embodiments—not generic “continuous trust”, “epoch security”, “attestation authorization”, or “capability revocation”.
