# SDK Quickstart
Start KAVACH, then use `kavach.sdk.client.KavachClient`.

```python
c = KavachClient()
status = c.status()
h = c.acquire('demo.sign', 'fixture://challenge')
result = c.execute(h)
verified = c.verify_receipt()
```

Consumers do not receive KAVACH root/private material and cannot set AIRS/KAVACH trust state.
