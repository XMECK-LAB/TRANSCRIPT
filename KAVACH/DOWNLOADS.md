# KAVACH Downloads

This page distinguishes **source snapshots** from **packaged release assets**.

## Important GitHub behavior

GitHub automatically adds:

- `Source code (zip)`
- `Source code (tar.gz)`

to a tag/release.

Those archives are generated from the **Git tree at the tag**. They do **not** contain separately uploaded GitHub Release binaries such as the V1 Windows setup.

## KAVACH 2.0 — Current Software Reference

**Release:** [`kavach-v2.0.0`](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v2.0.0)

### Recommended package

**[KAVACH-2.0.0-Software-Reference.zip](https://github.com/XMECK-LAB/TRANSCRIPT/releases/download/kavach-v2.0.0/KAVACH-2.0.0-Software-Reference.zip)**

SHA-256:

```text
F1B3DF6A3CF81E6512D3C19354CE3241AEE5804E82099629C112FDBD3E82011D
```

### SDK

**[KAVACH-2.0.0-SDK.zip](https://github.com/XMECK-LAB/TRANSCRIPT/releases/download/kavach-v2.0.0/KAVACH-2.0.0-SDK.zip)**

SHA-256:

```text
8C4ACB3E77044370B3BBDB7288662E5CD7D5F45D3BD7D26713D0A04FD4BE2408
```

### Source

- Branch: [`release/kavach-2.x`](https://github.com/XMECK-LAB/TRANSCRIPT/tree/release/kavach-2.x)
- Tag: [`kavach-v2.0.0`](https://github.com/XMECK-LAB/TRANSCRIPT/tree/kavach-v2.0.0)

### Windows status

**No Windows installer is admitted by the frozen KAVACH 2.0 release.**

Windows GUI screenshots document a real engineering surface, but screenshot evidence alone does not create a qualified installer release.

---

## KAVACH 1.0 — Historical Windows Engineering Preview

**Release:** [`kavach-v1.0.0`](https://github.com/XMECK-LAB/TRANSCRIPT/releases/tag/kavach-v1.0.0)

### Windows x64 setup

**[KAVACH-1.0.0-Windows-x64-Setup.exe](https://github.com/XMECK-LAB/TRANSCRIPT/releases/download/kavach-v1.0.0/KAVACH-1.0.0-Windows-x64-Setup.exe)**

SHA-256:

```text
4CA6D3BB5BE76632EEB53F9A00B123CEE36AFD7A9B365478C82316F733E0275F
```

Status:

- historical engineering preview;
- unsigned;
- not production-certified;
- trusted publisher signing is not claimed.

### Source

- Branch: [`release/kavach-1.x`](https://github.com/XMECK-LAB/TRANSCRIPT/tree/release/kavach-1.x)
- Tag: [`kavach-v1.0.0`](https://github.com/XMECK-LAB/TRANSCRIPT/tree/kavach-v1.0.0)

Again: the automatic GitHub Source ZIP is the source projection, **not** the setup EXE.

---

## Which file should I choose?

| Goal | File |
|---|---|
| Evaluate current KAVACH semantics/source | `KAVACH-2.0.0-Software-Reference.zip` |
| Integrate against current bounded SDK surface | `KAVACH-2.0.0-SDK.zip` |
| Inspect exact V2 tagged Git source | GitHub `Source code (zip)` or `release/kavach-2.x` |
| Run the historical Windows preview | `KAVACH-1.0.0-Windows-x64-Setup.exe` |
| Inspect exact V1 historical source projection | GitHub `Source code (zip)` or `release/kavach-1.x` |
