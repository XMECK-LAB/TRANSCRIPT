
from dataclasses import dataclass, asdict
from typing import FrozenSet
import re
ID=re.compile(r"^[a-z0-9][a-z0-9._:-]{0,127}$")
HEX=re.compile(r"^[0-9a-f]{64}$")
CF=("project","workload","provider","policy","recovery")
ASSURANCE={"SOFTWARE_REFERENCE":0,"PLATFORM_BOUND":1,"TPM_BOUND":2,"TEE_ATTESTED":3,"HSM_BOUND":4,"EXTERNAL_AUTHORITY":5}
def rid(n,v):
    if not isinstance(v,str) or not ID.fullmatch(v): raise ValueError(n)
def hx(n,v):
    if not isinstance(v,str) or not HEX.fullmatch(v): raise ValueError(n)
@dataclass(frozen=True)
class ContinuityVector:
    project:int; workload:int; provider:int; policy:int; recovery:int
    def __post_init__(self):
        for n in CF:
            v=getattr(self,n)
            if type(v) is not int or v<0 or v>2**63-1: raise ValueError("continuity."+n)
    def as_dict(self): return asdict(self)
    def mismatch(self,other,deps): return [n for n in sorted(deps) if getattr(self,n)!=getattr(other,n)]
@dataclass(frozen=True)
class ProviderDescriptor:
    provider_id:str; profile:str; capabilities:FrozenSet[str]; healthy:bool=True
    def __post_init__(self):
        rid("provider_id",self.provider_id)
        if self.profile not in ASSURANCE: raise ValueError("profile")
        for c in self.capabilities: rid("capability",c)
@dataclass(frozen=True)
class TrustContext:
    context_id:str; project_id:str; workload_id:str; appraisal_state:str; evidence_refs:tuple
    measurement_summary:dict; provider_state:str; recovery_state:str; continuity_inputs:dict
    policy_id:str; policy_digest:str; completeness:int; digest:str
    def __post_init__(self):
        for n in ("context_id","project_id","workload_id","policy_id"): rid(n,getattr(self,n))
        if self.appraisal_state not in {"TRUSTED","UNKNOWN","UNTRUSTED"}: raise ValueError("appraisal")
        hx("policy_digest",self.policy_digest); hx("digest",self.digest)
        if type(self.completeness) is not int or not 0<=self.completeness<=100: raise ValueError("completeness")
@dataclass(frozen=True)
class ProtectionRequest:
    request_id:str; project_id:str; workload_id:str; resource_id:str; authority_id:str; operation_id:str
    context_digest:str; input_digest:str; required_assurance:str; policy_hint:str|None=None
    def __post_init__(self):
        for n in ("request_id","project_id","workload_id","resource_id","authority_id","operation_id"): rid(n,getattr(self,n))
        hx("context_digest",self.context_digest); hx("input_digest",self.input_digest)
        if self.required_assurance not in ASSURANCE: raise ValueError("assurance")
        if self.policy_hint is not None: rid("policy_hint",self.policy_hint)
@dataclass(frozen=True)
class ProtectionDecision:
    request_id:str; decision_id:str; state:str; trust_context_ref:str; continuity:ContinuityVector
    provider_profile:str; assurance_profile:str; reason_codes:tuple; evidence_ref:str
@dataclass(frozen=True)
class ProtectionEnvelope:
    envelope_id:str; project_id:str; workload_id:str; resource_id:str; authority_id:str; operation_id:str
    trust_context_digest:str; decision_id:str; continuity:ContinuityVector; continuity_dependencies:FrozenSet[str]
    policy_id:str; policy_digest:str; provider_id:str; provider_profile:str; required_assurance:str
    issuance_receipt_ref:str; nonce:str; constraints:dict; authenticator:str
    def __post_init__(self):
        for n in ("envelope_id","project_id","workload_id","resource_id","authority_id","operation_id","decision_id","policy_id","provider_id","issuance_receipt_ref"): rid(n,getattr(self,n))
        hx("trust_context_digest",self.trust_context_digest); hx("policy_digest",self.policy_digest); hx("authenticator",self.authenticator)
        if not self.continuity_dependencies or not self.continuity_dependencies.issubset(set(CF)): raise ValueError("deps")
        if self.provider_profile not in ASSURANCE or self.required_assurance not in ASSURANCE: raise ValueError("assurance")
        if not isinstance(self.nonce,str) or not 16<=len(self.nonce)<=128: raise ValueError("nonce")
