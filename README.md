<div align="center">

<img src="assets/transcript-kavach-hero.svg" alt="TRANSCRIPT / KAVACH — Authority Before Protected Action" width="100%">

# TRANSCRIPT / KAVACH

**Governed Execution Infrastructure**  
**Authority Before Protected Action**

**XMECK-AI LAB · Public Engineering Reference**

[Architecture](docs/ARCHITECTURE.md) · [KAVACH Reference](KAVACH/README.md) · [Quickstart](KAVACH/docs/QUICKSTART.md) · [Evidence & Qualification](docs/KAVACH_K3_ADVERSARIAL_QUALIFICATION.md) · [Security](SECURITY.md)

**KAVACH 2.0: Software Reference** · **KAVACH 1.0: Historical Engineering Preview**  
**Packaged distribution: ON HOLD pending independent qualification**

</div>

---

## The engineering problem

An identity may be recognized, a workload may be trusted, and a request may appear valid—yet none of those facts alone should authorize a protected action.

**TRANSCRIPT** explores governed execution: how to connect trust appraisal to bounded permission, execution-time revalidation, recovery continuity and verifiable evidence.

**KAVACH** is the public authority-and-continuity reference subsystem within TRANSCRIPT.

> **Trust ≠ Authority ≠ Execution**

## Reference architecture

<div align="center">
<img src="assets/authority-flow.svg" alt="KAVACH reference authority flow" width="92%">
</div>

```text
IDENTITY / CONTEXT
       |
       v
AIRS — trust appraisal
       |
       v
KAVACH — OPEN / HOLD / REFUSE
       |
       v
K-LOCK — scoped, continuity-bound authority
       |
       v
Execution-time revalidation
       |
       v
Protected action (only while authorized)
       |
       v
Authenticated reference evidence
```

This is the **documented reference model**, not a claim that KAVACH already enforces operating-system security or prevents bypass in third-party applications.

## What the public software reference covers

| Area | Engineering behavior |
| --- | --- |
| Decision semantics | Explicit `OPEN`, `HOLD` and `REFUSE` outcomes |
| Bounded authority | Project, workload, resource, operation, provider and policy context |
| Continuity | Generation-aware validity checks, including recovery-dependent invalidation |
| Execution boundary | Revalidation before the reference accepts an authorized execution |
| Replay semantics | One-use authority consumption, with existing thread/restart regression coverage |
| Evidence | Authenticated, append-oriented reference receipts |
| SDK and adapters | Bounded consumer interfaces and explicitly constrained authority surfaces |

**Scope matters:** CI coverage of reference behavior is not proof of cross-process safety, external side-effect enforcement, hardware assurance or production certification. Current gaps are documented in the [K3 technical qualification report](docs/KAVACH_K3_ADVERSARIAL_QUALIFICATION.md).

## Public engineering versions

| Line | Purpose | Current interpretation |
| --- | --- | --- |
| **KAVACH 2.0** | Current software reference | `SOFTWARE_REFERENCE`; qualification of final product and binaries remains on hold |
| **KAVACH 1.0** | Historical Windows engineering preview | Preserved engineering lineage; unsigned historical installer is not endorsed for deployment |

The frozen V1 and V2 tags and branches remain historical source authorities. Documentation maintenance on `main` does **not** alter them.

**Packaged distribution is currently suspended as a publication decision.** Previously uploaded GitHub Release assets may still be accessible; they have not been withdrawn or independently qualified as part of the documentation work. This README contains no binary download promotion. See [Distribution Status](KAVACH/DOWNLOADS.md), [Version Authority](KAVACH/VERSIONS.md) and the [Release Asset Inventory](docs/KAVACH_K2_RELEASE_ASSET_INVENTORY.md).

## Explore the implementation

| Start here | What it contains |
| --- | --- |
| [KAVACH reference overview](KAVACH/README.md) | Invariants, architecture and assurance limits |
| [Architecture](docs/ARCHITECTURE.md) | System boundaries and reference model |
| [Quickstart](KAVACH/docs/QUICKSTART.md) | Requirements and source-based local execution |
| [Semantic / runtime source](KAVACH/src/) | Reference authority and continuity implementation |
| [Contracts](KAVACH/contracts/) | Normative and engineering interfaces |
| [SDK](KAVACH/sdk/) | Bounded integration surfaces |
| [Tests](KAVACH/tests/) | Reference regression and adversarial test modules |
| [Security Policy](SECURITY.md) | Responsible vulnerability reporting |
| [Publication Model](docs/PUBLICATION.md) | Source, release and public/private governance |

### Run the public reference locally

From a local checkout with Python installed:

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python -m unittest discover KAVACH\tests -v
python KAVACH\examples\protected_action_demo.py --check
```

These commands run the Python reference. They do not install a Windows protection product.

### Visual architecture demonstration

<div align="center">
<img src="assets/demo-authority-lifecycle.svg" alt="Illustrative KAVACH authority lifecycle" width="92%">
</div>

Explore the [HTML architecture demonstration](demo/index.html). Illustrations, screenshots and the Orb/HUD are presentation surfaces—not independently verified proof of real-system protection.

## Engineering evidence and current qualification

The public reference CI runs the tests and demo smoke check on **Windows and Ubuntu, Python 3.11 and 3.12**. A successful run is recorded for K2 commit `a59c8f0e02ea6b27ca47853b76ad9bebd7526222`: [CI evidence](https://github.com/XMECK-LAB/TRANSCRIPT/actions/runs/38432601912).

The follow-on K3 review identified unresolved assurance obligations, including:

- independent-process authorization and evidence consistency;
- host-side enforcement of a real protected action;
- key lifecycle, rollback and independent evidence custody;
- issuance uniqueness and replay resistance across process boundaries;
- independently checked package provenance, dependencies and Windows installer lifecycle.

See the [K3 adversarial qualification record](docs/KAVACH_K3_ADVERSARIAL_QUALIFICATION.md). **Final product and packaged binary admission remain HOLD.**

## Security, intellectual property and claim boundaries

This repository does **not** claim hardware-backed authority, TPM/TEE/HSM assurance, formal verification, independent security certification, vulnerability-free operation, or universal operating-system enforcement.

No general open-source license is granted by public visibility. Read [LICENSE-NOTICE.md](LICENSE-NOTICE.md) before any reuse or redistribution. Security concerns should follow [SECURITY.md](SECURITY.md); do not post confidential vulnerability details publicly.

The public reference is not the private KAVACH-OS lineage, a complete operating-system protection product, or an approved integration into other XMECK products.

## XMECK-AI LAB engineering identity

**TRANSCRIPT** — governed execution infrastructure.  
**KAVACH** — continuity-bound authority and protected-action reference.  
**XMECK-AI LAB** — publishing engineering organization.

**Independent engineering: Raaj Mandale**

> What should exist between *“we trust this”* and *“the system is allowed to execute this”*?

KAVACH explores that boundary through explicit decisions, bounded authority, continuity checks and authenticated reference evidence.
