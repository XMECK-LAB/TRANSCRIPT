# KAVACH V1 Integration Contract

External consumers integrate only through the versioned SDK/API and schemas. They do not receive KAVACH root material and cannot set trust state or advance epochs directly.

Canonical calls:
- connect()
- status()
- evaluate(request)
- acquire(request)
- execute(handle, input)
- verify_receipt(receipt)

Future adapters for XPADI, TRANSCRIPT, XLP, SHIELD or XAIPT remain separate packages and must declare the active KAVACH Security Profile so downstream claims cannot exceed provider assurance.
