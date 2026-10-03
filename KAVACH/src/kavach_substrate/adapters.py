from dataclasses import dataclass
from typing import Tuple
from .profiles import CATALOG

class AdapterError(RuntimeError): pass
ALLOWED_PROJECTS={'xpadi','transcript','xaipt','xlp'}

@dataclass(frozen=True)
class AdapterManifest:
    project_id:str
    adapter_version:str
    profiles:Tuple[str,...]
    workloads:Tuple[str,...]
    resources:Tuple[str,...]
    authorities:Tuple[str,...]
    trust_inputs:Tuple[str,...]
    continuity_dependencies:Tuple[str,...]
    provider_requirement:str
    evidence_mapping:str
    failure_policy:str
    ownership_exclusions:Tuple[str,...]
    def validate(self):
        if self.project_id not in ALLOWED_PROJECTS: raise AdapterError('project not admitted')
        if set(self.profiles)-set(CATALOG): raise AdapterError('unknown profile')
        prefix=self.project_id+'.'
        if any(not a.startswith(prefix) for a in self.authorities): raise AdapterError('authority namespace escape')
        if self.failure_policy!='FAIL_CLOSED': raise AdapterError('adapter must fail closed')
        if not self.ownership_exclusions: raise AdapterError('ownership exclusions required')
        return True

MANIFESTS={
 'xpadi':AdapterManifest('xpadi','2.0',('KAVACH-BASE','KAVACH-KEY','KAVACH-SURVIVAL','KAVACH-RECOVERY','KAVACH-RUNTIME'),('xpadi.runtime',),('xpadi.generation','xpadi.recovery','xpadi.proof'),('xpadi.pida.key.derive','xpadi.generation.commit','xpadi.repair.commit','xpadi.recovery.begin','xpadi.recovery.release','xpadi.proof.export'),('runtime.integrity','generation.identity','recovery.state','provider.health','policy.identity'),('project','workload','provider','policy','recovery'),'SOFTWARE_REFERENCE','REFERENCE_PARENT_EVIDENCE','FAIL_CLOSED',('pida.algorithm','survival.algorithm','reconstruction.algorithm')),
 'transcript':AdapterManifest('transcript','2.0',('KAVACH-BASE','KAVACH-KEY','KAVACH-RUNTIME'),('transcript.runtime',),('transcript.package','transcript.permit'),('transcript.package.unseal','transcript.package.execute','transcript.permit.consume'),('runtime.integrity','package.identity','provider.health'),('project','workload','provider','policy','recovery'),'SOFTWARE_REFERENCE','REFERENCE_PARENT_EVIDENCE','FAIL_CLOSED',('package.semantics','code.protection.runtime')),
 'xaipt':AdapterManifest('xaipt','2.0',('KAVACH-BASE','KAVACH-KEY','KAVACH-RUNTIME'),('xaipt.runtime',),('xaipt.vault','xaipt.payment'),('xaipt.vault.unseal','xaipt.device.bind','xaipt.payment.authorize'),('device.identity','runtime.integrity','provider.health'),('project','workload','provider','policy','recovery'),'SOFTWARE_REFERENCE','REFERENCE_PARENT_EVIDENCE','FAIL_CLOSED',('payment.logic','escrow.logic','business.rules')),
 'xlp':AdapterManifest('xlp','2.0',('KAVACH-BASE','KAVACH-KEY','KAVACH-RUNTIME'),('xlp.runtime',),('xlp.veda','xlp.yuga','xlp.transform'),('xlp.veda.execute','xlp.yuga.authorize','xlp.protected.transform'),('runtime.integrity','package.identity','provider.health'),('project','workload','provider','policy','recovery'),'SOFTWARE_REFERENCE','REFERENCE_PARENT_EVIDENCE','FAIL_CLOSED',('veda.semantics','yuga.semantics','primary.transform.logic')),
}
