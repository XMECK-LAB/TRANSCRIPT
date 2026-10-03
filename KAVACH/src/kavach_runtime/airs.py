
from dataclasses import dataclass
from typing import Dict, Any, Iterable
from kavach_semantic.model import TrustContext, ContinuityVector
from kavach_semantic.canonical import digest_hex

@dataclass(frozen=True)
class EvidenceObservation:
    source_id: str
    state: str  # TRUSTED | UNKNOWN | UNTRUSTED
    digest: str
    details: Dict[str,Any]
    required: bool=True

class AIRS:
    # Appraisal only. Never grants authority.
    def build_trust_context(self, *, context_id, project_id, workload_id, observations: Iterable[EvidenceObservation],
                            provider_state, recovery_state, continuity: ContinuityVector,
                            policy_id, policy_digest):
        obs=tuple(observations)
        if not obs:
            appraisal='UNKNOWN'; completeness=0
        else:
            states=[o.state for o in obs if o.required]
            if any(s=='UNTRUSTED' for s in states): appraisal='UNTRUSTED'
            elif any(s=='UNKNOWN' for s in states): appraisal='UNKNOWN'
            elif states and all(s=='TRUSTED' for s in states): appraisal='TRUSTED'
            else: appraisal='UNKNOWN'
            required=[o for o in obs if o.required]
            complete=sum(1 for o in required if o.state!='UNKNOWN')
            completeness=100 if not required else int(100*complete/len(required))
        evidence_refs=tuple(sorted(o.source_id for o in obs))
        measurement_summary={o.source_id:{'state':o.state,'digest':o.digest,'details':o.details} for o in sorted(obs,key=lambda x:x.source_id)}
        base={
          'context_id':context_id,'project_id':project_id,'workload_id':workload_id,
          'appraisal_state':appraisal,'evidence_refs':evidence_refs,'measurement_summary':measurement_summary,
          'provider_state':provider_state,'recovery_state':recovery_state,
          'continuity_inputs':continuity.as_dict(),'policy_id':policy_id,'policy_digest':policy_digest,
          'completeness':completeness,
        }
        return TrustContext(**base,digest=digest_hex(base))
