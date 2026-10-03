# KAVACH Native Product Contract

## Non-negotiable process boundary

The UI process is never authoritative. It communicates with `KAVACH_Runtime.exe` through authenticated loopback IPC. A UI event may request a Trust Lab action, but the runtime performs measurement, appraisal, state transition, capability issuance/execution, epoch advancement and evidence creation.

## Native information architecture

**COMMAND** — Overview  
**TRUST** — AIRS / Trust Core / Capabilities / K-LOCK  
**PROOF** — Evidence / Trust Lab / ProofCheck  
**SYSTEM** — Runtime / Integrations / SDK/API

## Visual identity

Ceramic white + deep blue + electric cyan/blue + controlled KAVACH orange. Motion is semantic:

- OPEN: coherent cyan/blue continuity flow.
- HOLD: orange interruption at capability boundary.
- REFUSE: capability path closed.
- Recovery: prior epoch sealed and new epoch formed.
- Replay: prior-epoch handle refused at current epoch boundary.
- Evidence: transitions emitted into authenticated receipt chain.

No fake threat counters, fake AI telemetry, fake security state or conversational/GPT-style explanatory surface is allowed.
