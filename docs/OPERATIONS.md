# Public Repository Operations

This document defines the public maintenance posture for `XMECK-LAB/TRANSCRIPT`.

## Release authority

The published release lines remain anchored to their release tags:

- `kavach-v1.0.0` — historical Windows engineering preview
- `kavach-v2.0.0` — current KAVACH software reference

Routine documentation, CI, examples, and repository-maintenance improvements on `main` do not retroactively change those release artifacts.

## Required public checks

A professional public maintenance cycle should preserve:

1. deterministic public tests;
2. protected-action demo smoke test;
3. release-tag immutability;
4. public/private source boundary;
5. no claim expansion without new evidence.

## Recommended GitHub repository settings

These settings are administrative and are not stored in Git:

### Repository description

`Governed execution infrastructure with KAVACH continuity-bound authority, protected execution, and authenticated evidence.`

### Topics

- `governed-execution`
- `authority`
- `continuity`
- `runtime-security`
- `capability-security`
- `evidence`
- `authorization`
- `python`
- `software-reference`

### Security

For a public repository, enable where available:

- Dependabot alerts
- secret scanning
- push protection
- code scanning
- private vulnerability reporting

### Main-branch governance

Create an active ruleset for `main` that at minimum:

- blocks deletion;
- blocks force-push;
- requires the `Public Reference CI` status check for merges;
- preserves an administrator/founder recovery path rather than locking the repository out of emergency maintenance.

## Release integrity

Existing release assets must not be silently replaced. A changed artifact belongs to a separately admitted release or an explicitly documented corrective release process.

## Public/private boundary

Do not publish:

- founder-only qualification evidence;
- unreleased KAVACH-OS source;
- private R18 lineage;
- private downstream adapters or private roadmap material;
- credentials, provider-root material, or bearer-sensitive authority material.
