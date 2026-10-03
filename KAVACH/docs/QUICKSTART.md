# KAVACH 2.0 Quickstart

This quickstart is for the public **Software Reference / Public Engineering Preview**.

## Requirements

- Git
- Python 3

No Windows installer is claimed for KAVACH 2.0.

## Clone

```bash
git clone https://github.com/XMECK-LAB/TRANSCRIPT.git
cd TRANSCRIPT
```

## Run the public tests

### PowerShell

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python -m unittest discover KAVACH\tests
```

### Bash / zsh

```bash
PYTHONPATH="$PWD/KAVACH/src" python -m unittest discover KAVACH/tests
```

## Inspect the system in the right order

1. [KAVACH/README.md](../README.md)
2. [NORMATIVE_CONTRACT.md](NORMATIVE_CONTRACT.md)
3. [RUNTIME_CONTRACT.md](RUNTIME_CONTRACT.md)
4. [SUBSTRATE_CONTRACT.md](SUBSTRATE_CONTRACT.md)
5. [TRACEABILITY_MATRIX.md](TRACEABILITY_MATRIX.md)
6. [../sdk/README.md](../sdk/README.md)
7. [../sdk/reference_client.py](../sdk/reference_client.py)

## Minimal reference-client orientation

The public client is intentionally bounded. It can inspect status, continuity, profiles, provider capabilities, request protected authority, execute through the runtime boundary, and verify receipts.

It does not expose a direct method to set OPEN, mutate protected continuity, or access provider-root material.

## Important release boundary

KAVACH 2.0 demonstrates the authority/continuity model as a software reference. It is not published as hardware-backed or production-certified security.

For the exact public claim boundary, see [CLAIM_BOUNDARY.md](CLAIM_BOUNDARY.md).
