# Repository Map

A visitor should be able to understand the repository in three passes.

## Pass 1 — Understand the idea

1. [README.md](../README.md)
2. [KAVACH/README.md](../KAVACH/README.md)
3. [assets/authority-flow.svg](../assets/authority-flow.svg)

## Pass 2 — Inspect the contracts

1. [KAVACH/docs/NORMATIVE_CONTRACT.md](../KAVACH/docs/NORMATIVE_CONTRACT.md)
2. [KAVACH/docs/RUNTIME_CONTRACT.md](../KAVACH/docs/RUNTIME_CONTRACT.md)
3. [KAVACH/docs/SUBSTRATE_CONTRACT.md](../KAVACH/docs/SUBSTRATE_CONTRACT.md)
4. [KAVACH/contracts/FINAL_PRODUCT_CONTRACT.json](../KAVACH/contracts/FINAL_PRODUCT_CONTRACT.json)

## Pass 3 — Inspect executable reference code

### Semantic kernel
KAVACH/src/kavach_semantic/

Canonical models, deterministic encoding, evaluation, authority envelopes, and V1 projection.

### Runtime
KAVACH/src/kavach_runtime/

AIRS, provider, execution runtime, evidence, IPC, state, and supporting utilities.

### Substrate
KAVACH/src/kavach_substrate/

Profiles, extensions, adapters, compatibility, SDK, and security-passport surface.

### SDK
KAVACH/sdk/

Reference integration surface for consumers.

### Tests
KAVACH/tests/

Public tests covering semantic, runtime, persistence, compatibility, substrate, SDK, and adversarial behaviors.

## Releases

- [KAVACH 2.0 — Software Reference](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v2.0.0)
- [KAVACH 1.0 — Engineering Preview](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v1.0.0)

## Boundary

Private founder evidence, private adapters, unreleased provider work, KAVACH-OS lineage, and other private ecosystem engineering are not part of this public projection.
