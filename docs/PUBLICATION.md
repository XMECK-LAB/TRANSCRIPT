# Publication Model

This repository has two distinct public layers:

## Release authority

The immutable release lines are represented by tags and GitHub Releases:

- **KAVACH 1.0** → `kavach-v1.0.0`
- **KAVACH 2.0** → `kavach-v2.0.0`

Release artifacts, provenance, hashes, and claim boundaries remain anchored to those release tags.

## Main branch

`main` may receive documentation-only presentation improvements after a release, provided they do not:

- alter release artifacts;
- rewrite release tags;
- expand product claims;
- change KAVACH execution semantics;
- publish private engineering lineage.

This keeps the repository presentation current without retroactively changing the admitted release.

## Public hierarchy

```text
XMECK-LAB
└── TRANSCRIPT
    └── KAVACH
```

TRANSCRIPT is the governed execution infrastructure. KAVACH is the currently public authority / continuity / protection subsystem.

## Public/private boundary

The public projection contains the software-reference surface necessary to understand and evaluate KAVACH.

It does not publish founder governance, private qualification evidence, unreleased provider engineering, KAVACH-OS source lineage, R18 private lineage, or private downstream ecosystem adapters.
