# KAVACH Version & Release Authority

## Canonical public lines

| Line | Branch | Tag | Role | Packaged artifact |
|---|---|---|---|---|
| **KAVACH 2.0** | `release/kavach-2.x` | `kavach-v2.0.0` | Current Software Reference | Software Reference ZIP + SDK ZIP |
| **KAVACH 1.0** | `release/kavach-1.x` | `kavach-v1.0.0` | Historical Windows Engineering Preview | Windows x64 Setup |

## Frozen authority

### V2

```text
release/kavach-2.x
kavach-v2.0.0
→ e343b139872a6a923ff5e86d20a1e4d30a39eb36
```

V2 release source tree:

```text
c9cdd13d241ecc5a2cd486821b2778e5dace1566
```

### V1

```text
release/kavach-1.x
kavach-v1.0.0
→ 87c637b33789708764124fcb4ded3563779568a1
```

V1 release source tree:

```text
0dc520faf12154d161eb0f5e4a17228370f2df24
```

## `main`

`main` is the maintained public repository surface. It may advance with:

- documentation;
- CI;
- executable examples;
- public visual evidence;
- repository operations and navigation.

Advancing `main` does **not** rewrite a frozen release tag or silently replace release artifacts.

## Source archive vs release asset

A tag’s automatic GitHub source archive is created from the Git tree.

A GitHub Release asset is an explicitly uploaded package/binary.

They are intentionally different distribution surfaces.
