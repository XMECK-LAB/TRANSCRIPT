# KAVACH K3 — Adversarial Qualification Findings (2026-10-13)

**Status:** `HOLD_SECURITY_AND_BINARY_ADMISSION`  
**Authority:** `XMECK-LAB/TRANSCRIPT` `main` baseline `a59c8f0e02ea6b27ca47853b76ad9bebd7526222`  
**Scope:** Read-only source review and existing GitHub CI evidence; *not* an independent executable security assessment.

## Verified positive evidence

- GitHub Actions run [38432601912](https://github.com/XMECK-LAB/TRANSCRIPT/actions/runs/38432601912) is successful for the exact K2 baseline, with four successful jobs: Ubuntu and Windows, Python 3.11 and 3.12. The public reference tests and reference-demo smoke test passed in all four jobs.
- Public suites `test_semantics.py`, `test_runtime.py`, and `test_substrate.py` include semantic refusal, context binding, stale continuity, single-process concurrency, restart replay, crash recovery, IPC tamper, and evidence-chain mutation tests.
- Historical Git tags and all nine release assets remain preserved as originally reported in [the K2 asset inventory](KAVACH_K2_RELEASE_ASSET_INVENTORY.md).

## Security gaps requiring proof before admission

| ID | Severity / classification | Source evidence | Specific acceptance requirement |
| --- | --- | --- | --- |
| K3-01 | **High — cross-process atomicity unproven** | `KAVACHRuntime.lock`, `EvidenceRuntime.lock`, `RuntimeStateStore.lock` are `threading.RLock`, scoped to one process. State, replay and receipt files are shared paths. | Run independent processes against the same workspace, simultaneously executing a single one-use authority and appending receipts; exactly one execution may succeed, sequences and receipts must remain valid under kills/restarts. Implement a proven exclusive writer/transaction boundary or reject concurrent writer startup before claiming cross-process safety. |
| K3-02 | **High — host-side side-effect binding unproven** | `KAVACHRuntime.execute` returns an authorization result and appends a receipt; no real protected external side-effect is performed by this method. | Qualify a real external consumer with a single enforced action boundary; denial must prevent side effects, including after crashes and stale/replayed authority. |
| K3-03 | **High — key lifecycle and rollback controls unproven** | Root keys are supplied to `KAVACHRuntime`; chain and state are stored under the workspace. `EvidenceRuntime.verify_chain` authenticates using a provided shared key and local head. | Prove key provisioning, permissions, rotation, adversarial rollback detection and independent anchor/custody. Explain precisely the host-compromise boundary; do not claim hardware-backed trust. |
| K3-04 | **Medium — deterministic default authorization nonce** | `KAVACHRuntime.acquire` currently defaults to `nonce='abcdefghijklmnop'`; the semantic envelope ID derives from request ID, decision ID and nonce. | Demonstrate unique issuance under repeated requests, or refuse repeated issuance explicitly. Make randomness/uniqueness part of the production contract and test collision/replay handling. |
| K3-05 | **High — binary provenance not independently qualified** | Release API exposes nine assets and GitHub-reported digests; no independent package-byte inspection has been performed here. | Privately preserve package bytes, compute SHA-256 locally, compare manifests and source tree, inspect third-party licenses and malware indicators, qualify signing and Windows install/uninstall. |
| K3-06 | **Medium — supply-chain governance unverified** | CI workflow uses version-tagged third-party Actions, e.g. `actions/checkout@v4` and `actions/setup-python@v5`; private vulnerability reporting settings were not independently inspected. | Pin reviewed Actions commits; verify least privilege, secret scanning, dependency/license inventory and vulnerability-reporting route. |
| K3-07 | **High — final product contract not admitted** | `KAVACH/contracts/FINAL_PRODUCT_CONTRACT.json` requires an accepted external consumer, full regression and Windows lifecycle. | Demonstrate all three gates with evidence before claiming a final Windows product or new binary release. |

These are **risk findings and missing assurance evidence**, not claims that exploitation has occurred. Some may be resolved by architectural constraints (such as one writer per workspace) if those constraints are enforced and tested.

## Next bounded test campaign

1. Freeze the exact starting SHA and capture failure evidence for tests without changing historical tags.
2. Run multi-process contention tests for duplicate authority consumption, IPC replay, evidence append and recovery transitions; add fault injection at every durable-write boundary.
3. Verify unique issuance semantics under repeated API calls and process restarts.
4. Run a real protected consumer with explicit denial and crash-side-effect assertions.
5. Privately archive old release assets, inspect and independently hash all nine; compare GitHub-reported digests and source manifests.
6. Only then propose security code corrections on a new review branch, with tests passing on both Windows and Ubuntu.

## Current admission verdict

- **K3 source inspection:** PARTIAL PASS (reviewed security-relevant modules and public test suites).
- **K3 public reference CI:** PASS for K2 baseline `a59c8f0e...`.
- **K3 multiprocess/external consumer/Windows binary qualification:** NOT PROVEN.
- **K3 security admission and final release:** **HOLD**.
- No historical sourcepoint or release-asset mutation is authorized by this report.
