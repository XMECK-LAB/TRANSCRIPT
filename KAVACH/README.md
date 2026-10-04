# KAVACH 2.0

## Continuity-Bound Authority & Protection Substrate

> **Authority before protected action.**

**Current public status:** Software Reference / Public Engineering Preview  
**Parent:** TRANSCRIPT — Governed Execution Infrastructure  
**Assurance:** `SOFTWARE_REFERENCE`

## Start here

- **[Downloads](DOWNLOADS.md)** — package vs source archive, V1 installer, V2 software reference
- **[Versions](VERSIONS.md)** — branches, tags, frozen release authority
- **[Quickstart](docs/QUICKSTART.md)** — run tests and the public reference
- **[Executable demo](examples/README.md)** — protected-action lifecycle
- **[Claim boundary](docs/CLAIM_BOUNDARY.md)** — exact public assurance limits

## Current download

**KAVACH 2.0 Software Reference**

[Download `KAVACH-2.0.0-Software-Reference.zip`](https://github.com/XMECK-LAB/TRANSCRIPT/releases/download/kavach-v2.0.0/KAVACH-2.0.0-Software-Reference.zip)

SDK:

[Download `KAVACH-2.0.0-SDK.zip`](https://github.com/XMECK-LAB/TRANSCRIPT/releases/download/kavach-v2.0.0/KAVACH-2.0.0-SDK.zip)

> The automatic GitHub **Source code (zip/tar.gz)** entries are source snapshots. They are not the packaged release asset.

## Architecture

```text
ProtectionRequest
      │
      ▼
TrustContext  ← AIRS appraisal
      │
      ▼
ProtectionDecision
OPEN / HOLD / REFUSE
      │
      ▼
ProtectionEnvelope
bounded authority + continuity
      │
      ▼
execution-time revalidation
      │
      ▼
RuntimeResult
      │
      ▼
Authenticated evidence
```

### Core invariants

1. **Trust does not directly authorize execution.**
2. **Authority is bound, not ambient.**
3. **Continuity is revalidated at execution.**
4. **Recovery invalidates stale dependent authority.**
5. **One-use authority is consumed on successful execution.**
6. **Evidence is part of the execution model.**

## Public implementation

```text
KAVACH/
├── DOWNLOADS.md
├── VERSIONS.md
├── PUBLIC-MANIFEST.json
├── contracts/
├── docs/
├── examples/
├── sdk/
├── src/
│   ├── kavach_semantic/
│   ├── kavach_runtime/
│   └── kavach_substrate/
└── tests/
```

## Run the public tests

### PowerShell

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python -m unittest discover KAVACH\tests -v
```

### Bash

```bash
PYTHONPATH="$PWD/KAVACH/src" python -m unittest discover KAVACH/tests -v
```

## Run the protected-action demo

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python KAVACH\examples\protected_action_demo.py
```

## Release lineage

- **Current:** [KAVACH 2.0 — Software Reference](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v2.0.0)
- **Historical:** [KAVACH 1.0 — Engineering Preview](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v1.0.0)

The V2 frozen release does not claim a Windows installer. The V1 release contains the historical Windows x64 setup.

## Assurance boundary

This public line does not claim hardware-backed authority, TPM/TEE/HSM assurance, independent certification, formal verification, or production security certification.

---

**KAVACH** · Built by **Raaj Mandale** · Published under **XMECK-LAB / TRANSCRIPT**
