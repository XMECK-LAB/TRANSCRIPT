
from dataclasses import dataclass
import hmac
from .model import *
from .canonical import digest_hex, mac_hex
@dataclass(frozen=True)
class ExecutionResult:
    allowed:bool; state:str; reason_codes:tuple
def assurance_ok(a,r): return ASSURANCE[a]>=ASSURANCE[r]
class SemanticKernel:
    def __init__(self,key:bytes):
        if len(key)<32: raise ValueError("key")
        self.key=bytes(key); self.consumed=set()
    def evaluate(self,req,ctx,cv,provider):
        if req.project_id!=ctx.project_id: return self._d(req,ctx,cv,provider,"REFUSE",("PROJECT_MISMATCH",))
        if req.workload_id!=ctx.workload_id: return self._d(req,ctx,cv,provider,"REFUSE",("WORKLOAD_MISMATCH",))
        if req.context_digest!=ctx.digest: return self._d(req,ctx,cv,provider,"REFUSE",("TRUST_CONTEXT_CHANGED",))
        if req.policy_hint and req.policy_hint!=ctx.policy_id: return self._d(req,ctx,cv,provider,"REFUSE",("POLICY_CHANGED",))
        if not provider.healthy: return self._d(req,ctx,cv,provider,"HOLD",("PROVIDER_UNAVAILABLE",))
        if not assurance_ok(provider.profile,req.required_assurance): return self._d(req,ctx,cv,provider,"REFUSE",("PROVIDER_ASSURANCE_INSUFFICIENT",))
        if ctx.appraisal_state=="UNKNOWN" or ctx.completeness<100: return self._d(req,ctx,cv,provider,"HOLD",("TRUST_CONTEXT_UNKNOWN",))
        if ctx.appraisal_state!="TRUSTED": return self._d(req,ctx,cv,provider,"REFUSE",("TRUST_EVIDENCE_INVALID",))
        return self._d(req,ctx,cv,provider,"OPEN",())
    def _d(self,req,ctx,cv,p,state,reasons):
        did="dec:"+digest_hex({"r":req.request_id,"c":ctx.context_id,"v":cv.as_dict()})[:32]
        return ProtectionDecision(req.request_id,did,state,ctx.context_id,cv,p.profile,p.profile,tuple(reasons),
                                  "ev:"+digest_hex({"d":did,"s":state,"r":list(reasons)})[:32])
    def issue(self,req,dec,ctx,p,deps=frozenset({"project","workload","provider","policy","recovery"}),one_use=True,nonce="abcdefghijklmnop"):
        if dec.state!="OPEN": raise ValueError("not open")
        eid="env:"+digest_hex({"r":req.request_id,"d":dec.decision_id,"n":nonce})[:32]
        u={"envelope_id":eid,"project_id":req.project_id,"workload_id":req.workload_id,"resource_id":req.resource_id,
           "authority_id":req.authority_id,"operation_id":req.operation_id,"trust_context_digest":ctx.digest,
           "decision_id":dec.decision_id,"continuity":dec.continuity.as_dict(),"continuity_dependencies":sorted(deps),
           "policy_id":ctx.policy_id,"policy_digest":ctx.policy_digest,"provider_id":p.provider_id,"provider_profile":p.profile,
           "required_assurance":req.required_assurance,"issuance_receipt_ref":dec.evidence_ref,"nonce":nonce,
           "constraints":{"one_use":bool(one_use)}}
        tag=mac_hex(self.key,"KAVACH2/PROTECTION-ENVELOPE",u)
        return ProtectionEnvelope(eid,req.project_id,req.workload_id,req.resource_id,req.authority_id,req.operation_id,
                                  ctx.digest,dec.decision_id,dec.continuity,frozenset(deps),ctx.policy_id,ctx.policy_digest,
                                  p.provider_id,p.profile,req.required_assurance,dec.evidence_ref,nonce,{"one_use":bool(one_use)},tag)
    def _unsigned(self,e):
        return {"envelope_id":e.envelope_id,"project_id":e.project_id,"workload_id":e.workload_id,"resource_id":e.resource_id,
           "authority_id":e.authority_id,"operation_id":e.operation_id,"trust_context_digest":e.trust_context_digest,
           "decision_id":e.decision_id,"continuity":e.continuity.as_dict(),"continuity_dependencies":sorted(e.continuity_dependencies),
           "policy_id":e.policy_id,"policy_digest":e.policy_digest,"provider_id":e.provider_id,"provider_profile":e.provider_profile,
           "required_assurance":e.required_assurance,"issuance_receipt_ref":e.issuance_receipt_ref,"nonce":e.nonce,
           "constraints":e.constraints}
    def execute(self,e,req,ctx,current,p):
        if not hmac.compare_digest(e.authenticator,mac_hex(self.key,"KAVACH2/PROTECTION-ENVELOPE",self._unsigned(e))):
            return ExecutionResult(False,"REFUSE",("AUTHORITY_REFUSED",))
        checks=[(e.project_id==req.project_id==ctx.project_id,"PROJECT_MISMATCH"),
                (e.workload_id==req.workload_id==ctx.workload_id,"WORKLOAD_MISMATCH"),
                (e.resource_id==req.resource_id,"RESOURCE_MISMATCH"),
                (e.authority_id==req.authority_id and e.operation_id==req.operation_id,"AUTHORITY_MISMATCH"),
                (e.trust_context_digest==ctx.digest==req.context_digest,"TRUST_CONTEXT_CHANGED"),
                (e.policy_id==ctx.policy_id and e.policy_digest==ctx.policy_digest,"POLICY_CHANGED"),
                (e.provider_id==p.provider_id and e.provider_profile==p.profile,"PROVIDER_CHANGED")]
        for ok,err in checks:
            if not ok: return ExecutionResult(False,"REFUSE",(err,))
        if not p.healthy:return ExecutionResult(False,"HOLD",("PROVIDER_UNAVAILABLE",))
        if not assurance_ok(p.profile,e.required_assurance):return ExecutionResult(False,"REFUSE",("PROVIDER_ASSURANCE_INSUFFICIENT",))
        if ctx.appraisal_state=="UNKNOWN" or ctx.completeness<100:return ExecutionResult(False,"HOLD",("TRUST_CONTEXT_UNKNOWN",))
        if ctx.appraisal_state!="TRUSTED":return ExecutionResult(False,"REFUSE",("TRUST_EVIDENCE_INVALID",))
        if e.continuity.mismatch(current,e.continuity_dependencies):return ExecutionResult(False,"REFUSE",("STALE_CONTINUITY",))
        if e.envelope_id in self.consumed:return ExecutionResult(False,"REFUSE",("CAPABILITY_CONSUMED",))
        if e.constraints.get("one_use"): self.consumed.add(e.envelope_id)
        return ExecutionResult(True,"OPEN",())
    def recover(self,cv):
        return ContinuityVector(cv.project,cv.workload,cv.provider,cv.policy,cv.recovery+1)
