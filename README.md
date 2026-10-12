<div align="center">

# TRANSCRIPT / KAVACH

**Governed Execution Infrastructure · Authority Before Protected Action**

**XMECK-AI LAB · Public Engineering Reference**

[Architecture](docs/ARCHITECTURE.md) · [KAVACH](KAVACH/README.md) · [Version History](KAVACH/VERSIONS.md) · [Demonstration](demo/index.html) · [Security](SECURITY.md)

</div>

---

## Purpose

TRANSCRIPT explores governed execution for software operations that require more than a trust assessment before an action is allowed. KAVACH is the public authority-and-continuity reference within this engineering line.

The guiding distinction is:

> **Trust ≠ Authority ≠ Execution**

An assessed identity or context does not by itself grant permission to execute. A protected action requires an applicable, bounded authorization decision and a final validity check at execution time.

## Execution model

```text
Identity / Context
       |
       v
Trust appraisal (AIRS boundary)
       |
       v
KAVACH decision: OPEN / HOLD / REFUSE
       |
       v
Bounded authority (K-LOCK)
       |
       v
Execution-time revalidation
       |
       v
Protected action (if still authorized)
       |
       v
Authenticated evidence / receipts
```

This diagram communicates the intended reference flow; it is not a blanket assurance claim for third-party environments.

## KAVACH public engineering lines

| Line | Role | Assurance boundary |
| --- | --- | --- |
| **KAVACH 2.0** | Current software-reference engineering line | `SOFTWARE_REFERENCE` |
| **KAVACH 1.0** | Historical Windows engineering-preview line | Historical engineering evidence; not a production-security certification |

Publication of packaged binaries and archives is **temporarily suspended pending a distribution-policy and provenance review**. This README intentionally provides **no ZIP, installer, executable, or externally hosted binary download links**. The repository's reference source and documentation remain available for inspection.

For source-line context, see [Version History](KAVACH/VERSIONS.md). A listed source branch or tag indicates version history, not independent security certification.

## Capabilities represented in the KAVACH 2.0 reference

| Area | Reference behavior |
| --- | --- |
| Decision | `OPEN`, `HOLD`, `REFUSE` |
| Scope | Authority bounded to relevant project, workload, resource, operation, provider and policy context |
| Continuity | Generation-based continuity checks for relevant contexts |
| Enforcement | Authority rechecked immediately before protected execution |
| Replay control | Single-use / consumption semantics where implemented by the reference |
| Recovery | Prior authority may become stale when recovery continuity advances |
| Evidence | Append-oriented authenticated receipts in the reference model |
| Consumer SDK | Governed consumer interfaces rather than arbitrary authority elevation |

Behavior should be assessed against source, tests, and actual integration conditions; this table does not promise enforcement outside the reference boundary.

## Local source reference demonstration

The repository includes a Python example at `KAVACH/examples/protected_action_demo.py`. In a local clone, with a supported Python environment and required dependencies in place, the reference demonstration can be invoked from the repository root:

```powershell
git clone https://github.com/XMECK-LAB/TRANSCRIPT.git
cd TRANSCRIPT
$env:PYTHONPATH = "$PWD\KAVACH\src"
python KAVACH\examples\protected_action_demo.py
```

The intended demonstration concerns authorization, protected execution, continuity advancement, stale-authority refusal, and evidence checks. Consult the local source and tests for precise runnable behavior and prerequisites.

## Repository navigation

| Area | Description |
| --- | --- |
| [`KAVACH/README.md`](KAVACH/README.md) | KAVACH subsystem architecture and usage scope |
| [`KAVACH/VERSIONS.md`](KAVACH/VERSIONS.md) | Lineage, branches and version boundaries |
| [`KAVACH/contracts/`](KAVACH/contracts/) | Authority interfaces and contracts |
| [`KAVACH/src/`](KAVACH/src/) | Reference implementation |
| [`KAVACH/sdk/`](KAVACH/sdk/) | Consumer integration surfaces |
| [`KAVACH/examples/`](KAVACH/examples/) | Reference exercises |
| [`KAVACH/tests/`](KAVACH/tests/) | Qualification and regression tests |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Execution architecture |
| [`docs/ECOSYSTEM.md`](docs/ECOSYSTEM.md) | Position within XMECK-AI LAB |
| [`docs/OPERATIONS.md`](docs/OPERATIONS.md) | Operational notes |
| [`demo/index.html`](demo/index.html) | Conceptual Orb/HUD architecture demo |
| [`assets/screenshots/README.md`](assets/screenshots/README.md) | Engineering UI image index |
| [`SECURITY.md`](SECURITY.md) | Security reporting guidance |

Visual designs, screenshots and the HTML demonstration are **illustrative engineering surfaces**. They do not independently prove runtime enforcement, platform integration, or security certification.

## Source and version integrity

The public source model distinguishes ongoing `main` maintenance from versioned engineering lineages. Existing version tags and release history should remain unchanged during documentation remediation. This README change is not a new KAVACH version and makes no claim to requalify historical binaries.

## Security and assurance boundaries

The public KAVACH 2.0 software reference **does not** claim:

- TPM, TEE, HSM, or hardware-backed authority enforcement;
- formal verification or independent security certification;
- vulnerability-free or bypass-proof operation;
- production suitability for a particular customer environment without further validation;
- enforcement by third-party applications unless a real integration has been implemented and tested.

For disclosure and security-related communications, see [SECURITY.md](SECURITY.md).

## Publication and distribution policy

This repository is intended for transparent engineering review. External links to downloadable ZIP files, installers, or executables are not included here. Any future packaged release must undergo content review, provenance/integrity validation, and compliance assessment before distribution is restored. Repository maintainers should also review release descriptions, other documentation, issues, pull requests and organization/profile pages for obsolete download references.

## Project identity

**TRANSCRIPT** — governed execution infrastructure.  
**KAVACH** — authority, continuity and protected-action reference subsystem.  
**XMECK-AI LAB** — publishing engineering organization.

Independent engineering project by **Raaj Mandale**, published under **XMECK-AI LAB**.

> What should exist between *“we trust this”* and *“the system is allowed to execute this”*?

The KAVACH public reference explores that boundary through explicit decisions, bounded authority, execution-time checking and evidence.
