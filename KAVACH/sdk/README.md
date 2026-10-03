# KAVACH 2.0 SDK / API — Founder Qualification

The SDK is a bounded consumer surface. It may request evaluation, protected authority and evidence verification; it cannot set OPEN, mutate continuity, issue authority, access provider root material or forge Evidence.

## V1 compatibility surface
`connect / status / evaluate / acquire / execute / verify_receipt`

## KAVACH 2.0 surface
`get_continuity / get_trust_context / provider_capabilities / discover_profiles / activate_profiles / security_passport / recover_authority`

## Assurance boundary
`SOFTWARE_REFERENCE`. No TPM/HSM/TEE production assurance is claimed.

## External adapters
XPADI, TRANSCRIPT, XAIPT and XLP contracts are included as declarative integration references. They are not live integrations until G10.
