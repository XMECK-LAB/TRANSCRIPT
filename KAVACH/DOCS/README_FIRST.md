# KAVACH™ V1 — Native Productization

KAVACH V1 is a research/reference security runtime and technical demonstrator for the frozen Trust-Continuity Capability mechanism.

## Product modes

- **A — Integration Kit:** SDK/API contracts and reference consumer for future project integration.
- **B — Public Demonstrator:** simplified native Trust Core, AIRS, capability and proof experience for grants/research/public explanation.
- **C — Authority Console:** full founder/engineering instrumentation including AIRS, K-LOCK, Evidence, Runtime, ProofCheck and SDK/API.

All three modes consume exactly the same authoritative KAVACH Runtime. Mode selection changes only UI visibility; it does not change security semantics.

## Security architecture

`Identity → AIRS appraisal → KAVACH OPEN/HOLD/REFUSE → K-LOCK protected capability → authenticated evidence`

Recovery advances the trust epoch. A capability issued in epoch N cannot execute after transition to epoch N+1.

## Assurance boundary

The V1 provider is **SOFTWARE_REFERENCE**. KAVACH V1 does not claim TPM/HSM-grade key isolation or production certification.

## Native Windows construction

The native UI is Qt 6 / QML. `BUILD_WINDOWS_NATIVE.bat` performs Python/core validation, ProofCheck, native executable packaging, SDK smoke testing and Inno Setup installer creation. A final Windows founder artifact is accepted only if that build completes on Windows and the installed clean-machine validation passes.
