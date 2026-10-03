
from dataclasses import dataclass
import hashlib, hmac, secrets
from kavach_semantic.model import ProviderDescriptor

class ProviderError(RuntimeError): pass

class SoftwareReferenceProvider:
    PROFILE='SOFTWARE_REFERENCE'
    PROVIDER_ID='provider.software_reference'
    def __init__(self, root_key: bytes):
        if not isinstance(root_key,(bytes,bytearray)) or len(root_key) < 32:
            raise ValueError('root key must be >=32 bytes')
        self._root=bytes(root_key)
        self._healthy=True
    def descriptor(self):
        return ProviderDescriptor(self.PROVIDER_ID,self.PROFILE,
            frozenset({'capability.authority','key.derive','crypto.mac','crypto.verify','random'}),self._healthy)
    def set_health(self, healthy: bool): self._healthy=bool(healthy)
    def derive(self, purpose: str, context: bytes) -> bytes:
        if not self._healthy: raise ProviderError('provider unavailable')
        if not purpose or len(purpose)>128 or len(context)>65536: raise ProviderError('invalid derive request')
        return hmac.new(self._root,b'KAVACH2/DERIVE\x00'+purpose.encode('utf-8')+b'\x00'+context,hashlib.sha256).digest()
    def mac(self, purpose: str, data: bytes) -> str:
        k=self.derive('mac:'+purpose,b'')
        return hmac.new(k,b'KAVACH2/MAC\x00'+purpose.encode('utf-8')+b'\x00'+data,hashlib.sha256).hexdigest()
    def verify_mac(self, purpose: str, data: bytes, tag: str) -> bool:
        try: expected=self.mac(purpose,data)
        except ProviderError: return False
        return hmac.compare_digest(expected,tag)
    def random(self,n=32):
        if not self._healthy: raise ProviderError('provider unavailable')
        if not (16<=n<=64): raise ProviderError('random length out of bounds')
        return secrets.token_bytes(n)
    def public_status(self):
        d=self.descriptor()
        return {'provider_id':d.provider_id,'profile':d.profile,'capabilities':sorted(d.capabilities),'healthy':d.healthy}
    def diagnostics(self):
        # Explicitly excludes root key / derived key material.
        return self.public_status()
