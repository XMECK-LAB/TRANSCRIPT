import time
from dataclasses import asdict
from .profiles import resolve_profiles
from .extensions import ExtensionFramework
from .passport import security_passport
from .compatibility import V1RuntimeAdapter

class SDKError(RuntimeError): pass

class KAVACHClient:
    """Bounded in-process reference SDK over the authoritative runtime contract.
    Block C models authenticated transport semantics but is not final packaging.
    """
    def __init__(self,runtime,client_id='client.reference'):
        self.runtime=runtime; self.client_id=client_id; self.seq=0; self.extensions=ExtensionFramework(); self.v1=V1RuntimeAdapter(runtime)
    def _next_frame(self,op,payload):
        self.seq+=1
        return self.runtime.ipc.sign(client_id=self.client_id,seq=self.seq,nonce=f'nonce-{self.seq:016d}',issued_at=int(time.time()),body={'op':op,'payload':payload})
    def _authenticated(self,op,payload):
        frame=self._next_frame(op,payload); body=self.runtime.ipc.verify(frame,now=frame['issued_at'])
        if body.get('op')!=op: raise SDKError('transport operation mismatch')
        return body['payload']
    def connect(self): self._authenticated('connect',{}); return {'connected':True,'runtime':'KAVACH 2.0'}
    def status(self): self._authenticated('status',{}); return self.runtime.status()
    def get_continuity(self): self._authenticated('continuity',{}); return self.runtime.continuity().as_dict()
    def get_trust_context(self,ctx): self._authenticated('trust_context',{'context_id':ctx.context_id}); return asdict(ctx)
    def provider_capabilities(self): self._authenticated('provider',{}); return self.runtime.provider.public_status()
    def discover_profiles(self): return tuple(sorted(resolveable_profiles()))
    def activate_profiles(self,profile_ids):
        self._authenticated('profiles.activate',{'profiles':sorted(profile_ids)})
        r=resolve_profiles(profile_ids,self.runtime.provider.descriptor(),self.extensions.registry)
        return {k:(sorted(v) if isinstance(v,(set,frozenset,tuple)) else v) for k,v in r.items()}
    def security_passport(self,profile_ids):
        r=self.activate_profiles(profile_ids); return security_passport(self.runtime,r['profiles'],r['extensions'])
    def evaluate(self,req,ctx): self._authenticated('evaluate',{'request_id':req.request_id}); return self.runtime.evaluate(req,ctx)
    def acquire(self,req,ctx,profile_ids=('KAVACH-BASE',),one_use=True):
        r=self.activate_profiles(profile_ids)
        return self.runtime.acquire(req,ctx,deps=frozenset(r['continuity_dependencies']),one_use=one_use)
    def execute(self,env,req,ctx): self._authenticated('execute',{'envelope_id':env.envelope_id}); return self.runtime.execute(env,req,ctx)
    def recover_authority(self,project_id,workload_id): self._authenticated('recovery.authorize',{'project_id':project_id,'workload_id':workload_id}); return self.runtime.trusted_recovery(project_id,workload_id)
    def verify_receipt(self,receipt): self._authenticated('receipt.verify',{'sequence':receipt.get('sequence')}); return self.runtime.evidence.verify_receipt(receipt)

def resolveable_profiles():
    from .profiles import CATALOG
    return CATALOG.keys()
