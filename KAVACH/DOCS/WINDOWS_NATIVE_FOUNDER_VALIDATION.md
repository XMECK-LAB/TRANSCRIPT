# Windows Native Founder Validation

The final native founder gate is intentionally short.

1. Build or install `KAVACH_Setup.exe` on Windows x64.
2. Launch the desktop **KAVACH** icon. Confirm there is no browser/localhost surface.
3. In Authority Console verify Runtime = ONLINE, IPC = AUTHENTICATED, Provider = SOFTWARE_REFERENCE.
4. Open Trust Lab and run the complete eight-stage sequence.
5. Confirm controlled trust loss produces HOLD/REFUSE, K-LOCK refuses protected execution, recovery advances epoch, prior-epoch capability replay is refused, fresh-epoch capability succeeds, receipt chain verifies.
6. Run installed **KAVACH ProofCheck**; require all acceptance tests PASS.
7. Run the installed/reference SDK example against the same runtime.
8. Validate high-DPI resize, keyboard navigation, close/reopen, runtime persistence and evidence persistence.
9. Uninstall KAVACH. Confirm binaries/shortcuts are removed and choose whether to preserve or delete local evidence when prompted.

Any failure in steps 2–9 blocks founder acceptance.
