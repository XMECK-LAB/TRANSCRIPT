
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import threading, hashlib, json
from kavach_semantic import *
from kavach_semantic.canonical import digest_hex, canonical_bytes
from .provider import SoftwareReferenceProvider
from .airs import AIRS, EvidenceObservation
from .state import RuntimeStateStore, StateError
from .evidence import EvidenceRuntime, EvidenceError
from .ipc import IPCAuthenticator
from .util import atomic_write_json

@dataclass(frozen=True)
class RuntimeResult:
    state:str
    reason_codes:tuple
    envelope:object=None
    receipt:object=None

class KAVACHRuntime:
    # Authoritative Block-B runtime. Client never mutates trust/continuity/evidence directly.
    def __init__(self, workspace:Path, *, authority_key:bytes, provider_key:bytes, evidence_key:bytes):
        self.workspace=Path(workspace); self.workspace.mkdir(parents=True,exist_ok=True)
        self.provider=SoftwareReferenceProvider(provider_key)
        self.kernel=SemanticKernel(authority_key)
        self.airs=AIRS()
        self.state=RuntimeStateStore(self.workspace/'state')
        self.evidence=EvidenceRuntime(self.workspace/'evidence',evidence_key)
        self.ipc=IPCAuthenticator(self.provider.derive('ipc-auth',b'local-runtime'), self.workspace/'state'/'ipc_replay.json')
        self.lock=threading.RLock()
        self.state.initialize(ContinuityVector(1,1,1,1,1),provider=self.provider)
        self.evidence.recover_pending()
        self._recover_transition()
    def _recovery_journal_path(self):
        return self.workspace/'state'/'recovery_pending.json'
    def _recover_transition(self):
        p=self._recovery_journal_path()
        if not p.exists(): return 'CLEAN'
        from kavach_semantic.canonical import strict_json_loads
        j=strict_json_loads(p.read_bytes()); old=ContinuityVector(**j['old']); new=ContinuityVector(**j['new']); tx=j['transaction_id']
        cur=self.continuity()
        if cur==old:
            p.unlink(); return 'ABORTED'
        if cur!=new:
            raise StateError('ambiguous recovery transaction state')
        if not self.evidence.has_transaction(tx,'continuity.recovery'):
            self.evidence.append({'event':'continuity.recovery','transaction_id':tx,'project_id':j['project_id'],'workload_id':j['workload_id'],
              'trust_context_ref':'ctx:recovery','decision_ref':'dec:recovery','authority_ref':'authority:recovery','operation_id':'recover',
              'resource_id':'runtime:continuity','continuity':new.as_dict(),'policy_id':self._policy()['policy_id'],
              'provider_profile':self.provider.descriptor().profile,'result_digest':digest_hex({'old':old.as_dict(),'new':new.as_dict()}),'reason_codes':[]})
        p.unlink(); return 'RECOVERED'
    def _policy(self):
        return self.state.read('policy.json')
    def continuity(self): return self.state.get_continuity()
    def status(self):
        return {'schema':'kavach.runtime-status/v2','continuity':self.continuity().as_dict(),'provider':self.provider.public_status(),'evidence_valid':self.evidence.verify_chain()}
    def build_context(self, project_id, workload_id, observations, context_id='ctx:runtime'):
        pol=self._policy(); cv=self.continuity()
        return self.airs.build_trust_context(context_id=context_id,project_id=project_id,workload_id=workload_id,
            observations=observations,provider_state='healthy' if self.provider.descriptor().healthy else 'unavailable',
            recovery_state='normal',continuity=cv,policy_id=pol['policy_id'],policy_digest=pol['policy_digest'])
    def evaluate(self,req,ctx):
        with self.lock:
            return self.kernel.evaluate(req,ctx,self.continuity(),self.provider.descriptor())
    def acquire(self,req,ctx,*,deps=frozenset({'project','workload','provider','policy','recovery'}),one_use=True,nonce='abcdefghijklmnop'):
        with self.lock:
            d=self.evaluate(req,ctx)
            ev=self.evidence.append({'event':'authority.evaluate','project_id':req.project_id,'workload_id':req.workload_id,
              'trust_context_ref':ctx.context_id,'decision_ref':d.decision_id,'authority_ref':'none','operation_id':req.operation_id,
              'resource_id':req.resource_id,'continuity':self.continuity().as_dict(),'policy_id':ctx.policy_id,
              'provider_profile':self.provider.descriptor().profile,'result_digest':digest_hex({'state':d.state,'reasons':list(d.reason_codes)}),
              'reason_codes':list(d.reason_codes)})
            if d.state!='OPEN': return RuntimeResult(d.state,d.reason_codes,receipt=ev)
            env=self.kernel.issue(req,d,ctx,self.provider.descriptor(),deps=deps,one_use=one_use,nonce=nonce)
            issued=self.evidence.append({'event':'authority.issue','project_id':req.project_id,'workload_id':req.workload_id,
              'trust_context_ref':ctx.context_id,'decision_ref':d.decision_id,'authority_ref':env.envelope_id,'operation_id':req.operation_id,
              'resource_id':req.resource_id,'continuity':self.continuity().as_dict(),'policy_id':ctx.policy_id,
              'provider_profile':self.provider.descriptor().profile,'result_digest':digest_hex({'envelope':env.envelope_id}),'reason_codes':[]})
            return RuntimeResult('OPEN',(),envelope=env,receipt=issued)
    def execute(self,env,req,current_ctx):
        with self.lock:
            if env.constraints.get('one_use',False) and self.evidence.has_successful_execution(env.envelope_id):
                x=ExecutionResult(False,'REFUSE',('CAPABILITY_CONSUMED',))
            else:
                x=self.kernel.execute(env,req,current_ctx,self.continuity(),self.provider.descriptor())
            try:
                receipt=self.evidence.append({'event':'authority.execute' if x.allowed else 'authority.refuse','project_id':req.project_id,
                  'workload_id':req.workload_id,'trust_context_ref':current_ctx.context_id,'decision_ref':env.decision_id,
                  'authority_ref':env.envelope_id,'operation_id':req.operation_id,'resource_id':req.resource_id,
                  'continuity':self.continuity().as_dict(),'policy_id':current_ctx.policy_id,'provider_profile':self.provider.descriptor().profile,
                  'result_digest':digest_hex({'allowed':x.allowed,'state':x.state,'reasons':list(x.reason_codes)}),'reason_codes':list(x.reason_codes)})
            except Exception:
                if x.allowed and env.constraints.get('one_use',False): self.kernel.consumed.discard(env.envelope_id)
                raise
            return RuntimeResult(x.state,x.reason_codes,receipt=receipt)
    def trusted_recovery(self,project_id,workload_id,fail_stage=None):
        with self.lock:
            old=self.continuity(); new=self.kernel.recover(old)
            tx='tx:'+digest_hex({'project':project_id,'workload':workload_id,'old':old.as_dict(),'new':new.as_dict()})[:32]
            j={'schema':'kavach.recovery-tx/v2','transaction_id':tx,'project_id':project_id,'workload_id':workload_id,'old':old.as_dict(),'new':new.as_dict()}
            atomic_write_json(self._recovery_journal_path(),j)
            if fail_stage=='after_journal': raise RuntimeError('injected recovery crash after journal')
            self.state.set_continuity(new)
            if fail_stage=='after_state': raise RuntimeError('injected recovery crash after state')
            receipt=self.evidence.append({'event':'continuity.recovery','transaction_id':tx,'project_id':project_id,'workload_id':workload_id,
              'trust_context_ref':'ctx:recovery','decision_ref':'dec:recovery','authority_ref':'authority:recovery','operation_id':'recover',
              'resource_id':'runtime:continuity','continuity':new.as_dict(),'policy_id':self._policy()['policy_id'],
              'provider_profile':self.provider.descriptor().profile,'result_digest':digest_hex({'old':old.as_dict(),'new':new.as_dict()}),'reason_codes':[]})
            if fail_stage=='after_evidence': raise RuntimeError('injected recovery crash after evidence')
            self._recovery_journal_path().unlink()
            return new,receipt
    def diagnostics(self):
        # No root/provider/evidence keys are exposed.
        return {'runtime':self.status(),'workspace':str(self.workspace),'secrets_exposed':False}
