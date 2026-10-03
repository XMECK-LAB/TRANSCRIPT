from dataclasses import replace
from kavach_semantic.compat_v1 import V1Compatibility

class V1RuntimeAdapter:
    def __init__(self,runtime): self.runtime=runtime
    def connect(self): return {'connected':True,'compatibility':'KAVACH-V1'}
    def status(self):
        s=self.runtime.status(); return {'state':'OPEN' if s['provider']['healthy'] and s['evidence_valid'] else 'HOLD','epoch':V1Compatibility.epoch_from_v2(self.runtime.continuity())}
    def evaluate(self,request,context):
        d=self.runtime.evaluate(request,context); return {'state':d.state,'reason_codes':list(d.reason_codes),'epoch':V1Compatibility.epoch_from_v2(d.continuity)}
    def acquire(self,request,context,one_use=True):
        return self.runtime.acquire(request,context,deps=V1Compatibility.deps_for_v1(),one_use=one_use)
    def execute(self,handle,request,current_context): return self.runtime.execute(handle,request,current_context)
    def verify_receipt(self,receipt): return self.runtime.evidence.verify_receipt(receipt)
