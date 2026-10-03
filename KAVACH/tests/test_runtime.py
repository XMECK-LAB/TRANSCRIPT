
import unittest, tempfile, shutil, threading, json, time
from pathlib import Path
from dataclasses import replace
from kavach_semantic import *
from kavach_semantic.canonical import digest_hex, canonical_bytes
from kavach_runtime import *

AK=b'A'*32; PK=b'P'*32; EK=b'E'*32

def obs(state='TRUSTED',sid='evidence.runtime'):
    return [EvidenceObservation(sid,state,'a'*64,{'source':'test'},True)]

class RBase(unittest.TestCase):
    def setUp(self):
        self.tmp=Path(tempfile.mkdtemp()); self.r=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        self.ctx=self.r.build_context('xpadi','xpadi.runtime',obs())
        self.req=ProtectionRequest('req:001','xpadi','xpadi.runtime','generation:001','xpadi.generation.commit','commit',self.ctx.digest,'b'*64,'SOFTWARE_REFERENCE')
    def tearDown(self): shutil.rmtree(self.tmp,ignore_errors=True)

class AIRSTests(RBase):
    def test_trusted(self): self.assertEqual(self.ctx.appraisal_state,'TRUSTED')
    def test_unknown(self): self.assertEqual(self.r.build_context('xpadi','xpadi.runtime',obs('UNKNOWN')).appraisal_state,'UNKNOWN')
    def test_untrusted(self): self.assertEqual(self.r.build_context('xpadi','xpadi.runtime',obs('UNTRUSTED')).appraisal_state,'UNTRUSTED')
    def test_no_evidence_unknown(self): self.assertEqual(self.r.build_context('xpadi','xpadi.runtime',[]).appraisal_state,'UNKNOWN')

class RuntimeAuthorityTests(RBase):
    def test_normal_acquire_execute(self):
        a=self.r.acquire(self.req,self.ctx,one_use=False); self.assertEqual(a.state,'OPEN')
        x=self.r.execute(a.envelope,self.req,self.ctx); self.assertEqual(x.state,'OPEN')
    def test_unknown_hold(self):
        c=self.r.build_context('xpadi','xpadi.runtime',obs('UNKNOWN')); q=replace(self.req,context_digest=c.digest)
        self.assertEqual(self.r.acquire(q,c).state,'HOLD')
    def test_untrusted_refuse(self):
        c=self.r.build_context('xpadi','xpadi.runtime',obs('UNTRUSTED')); q=replace(self.req,context_digest=c.digest)
        self.assertEqual(self.r.acquire(q,c).state,'REFUSE')
    def test_trust_changes_between_acquire_execute(self):
        a=self.r.acquire(self.req,self.ctx,one_use=False)
        c=self.r.build_context('xpadi','xpadi.runtime',obs('UNKNOWN'),context_id='ctx:later')
        q=replace(self.req,context_digest=c.digest)
        # retained envelope + current request/context cannot silently execute
        self.assertIn(self.r.execute(a.envelope,q,c).state,('HOLD','REFUSE'))
    def test_recovery_stales_old(self):
        a=self.r.acquire(self.req,self.ctx,one_use=False); self.r.trusted_recovery('xpadi','xpadi.runtime')
        c2=self.r.build_context('xpadi','xpadi.runtime',obs(),context_id='ctx:new')
        q2=replace(self.req,context_digest=c2.digest)
        x=self.r.execute(a.envelope,q2,c2); self.assertEqual(x.reason_codes,('TRUST_CONTEXT_CHANGED',))
        # Direct same-context attempt reaches continuity gate.
        x2=self.r.execute(a.envelope,self.req,self.ctx); self.assertEqual(x2.reason_codes,('STALE_CONTINUITY',))
    def test_provider_failure_hold(self):
        self.r.provider.set_health(False)
        d=self.r.evaluate(self.req,self.ctx); self.assertEqual(d.state,'HOLD')
    def test_provider_substitution_refuse(self):
        a=self.r.acquire(self.req,self.ctx,one_use=False)
        self.r.provider.PROVIDER_ID='provider.replaced'
        self.assertEqual(self.r.execute(a.envelope,self.req,self.ctx).reason_codes,('PROVIDER_CHANGED',))
    def test_policy_change_refuse(self):
        a=self.r.acquire(self.req,self.ctx,one_use=False)
        self.r.state.write('policy.json',{'schema':'kavach.policy/v2','policy_id':'policy.main','policy_digest':'c'*64})
        c2=self.r.build_context('xpadi','xpadi.runtime',obs(),context_id='ctx:p2')
        q2=replace(self.req,context_digest=c2.digest)
        self.assertIn(self.r.execute(a.envelope,q2,c2).reason_codes,(('TRUST_CONTEXT_CHANGED',),('POLICY_CHANGED',)))
    def test_one_use_concurrent_exactly_one(self):
        a=self.r.acquire(self.req,self.ctx,one_use=True); out=[]
        def f(): out.append(self.r.execute(a.envelope,self.req,self.ctx).state)
        ts=[threading.Thread(target=f) for _ in range(2)]
        [t.start() for t in ts]; [t.join() for t in ts]
        self.assertEqual(out.count('OPEN'),1); self.assertEqual(out.count('REFUSE'),1)
    def test_client_cannot_set_open(self):
        self.assertFalse(hasattr(self.r,'set_open'))
    def test_diagnostics_no_secrets(self):
        s=json.dumps(self.r.diagnostics()); self.assertNotIn('AAAA',s); self.assertNotIn('PPPP',s); self.assertFalse(self.r.diagnostics()['secrets_exposed'])

class RestartStateTests(RBase):
    def test_restart_preserves_continuity_and_evidence(self):
        self.r.acquire(self.req,self.ctx,one_use=False); before=self.r.continuity(); self.r.evidence.verify_chain()
        r2=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        self.assertEqual(r2.continuity(),before); self.assertTrue(r2.evidence.verify_chain())
    def test_corrupt_continuity_fails_closed(self):
        (self.tmp/'state/continuity.json').write_text('{bad',encoding='utf-8')
        with self.assertRaises(StateError): self.r.continuity()
    def test_atomic_state_failure_preserves_old(self):
        old=self.r.continuity(); new=self.r.kernel.recover(old)
        from kavach_runtime.util import AtomicWriteError
        with self.assertRaises(AtomicWriteError): self.r.state.set_continuity(new,fail_before_replace=True)
        self.assertEqual(self.r.continuity(),old)

class EvidenceTests(RBase):
    def test_chain_valid(self):
        self.r.acquire(self.req,self.ctx); self.assertTrue(self.r.evidence.verify_chain())
    def test_mutation_detected(self):
        self.r.acquire(self.req,self.ctx)
        p=self.tmp/'evidence/receipts.jsonl'; lines=p.read_bytes().splitlines(); o=json.loads(lines[0]); o['event']='evil'; lines[0]=canonical_bytes(o); p.write_bytes(b'\n'.join(lines)+b'\n')
        with self.assertRaises(EvidenceError): self.r.evidence.verify_chain()
    def test_truncation_detected_by_head(self):
        self.r.acquire(self.req,self.ctx); p=self.tmp/'evidence/receipts.jsonl'; lines=p.read_bytes().splitlines(); p.write_bytes(lines[0]+b'\n')
        with self.assertRaises(EvidenceError): self.r.evidence.verify_chain()
    def test_head_rollback_detected(self):
        self.r.acquire(self.req,self.ctx); hp=self.tmp/'evidence/head.json'; h=json.loads(hp.read_text()); h['sequence']=-1; h['digest']='0'*64; hp.write_bytes(canonical_bytes(h))
        with self.assertRaises(EvidenceError): self.r.evidence.verify_chain()
    def test_pending_after_journal_discards(self):
        e=EvidenceRuntime(self.tmp/'xev',EK)
        with self.assertRaises(EvidenceError): e.append({'event':'x','project_id':'xpadi','workload_id':'xpadi.runtime','trust_context_ref':'ctx:x','decision_ref':'dec:x','authority_ref':'a:x','operation_id':'x','resource_id':'r:x','continuity':{'project':1,'workload':1,'provider':1,'policy':1,'recovery':1},'policy_id':'policy.main','provider_profile':'SOFTWARE_REFERENCE','result_digest':'a'*64,'reason_codes':[]},fail_stage='after_journal')
        self.assertEqual(e.recover_pending(),'RECOVERED'); self.assertTrue(e.verify_chain())
    def test_pending_after_log_recovers_head(self):
        e=EvidenceRuntime(self.tmp/'yev',EK)
        event={'event':'x','project_id':'xpadi','workload_id':'xpadi.runtime','trust_context_ref':'ctx:x','decision_ref':'dec:x','authority_ref':'a:x','operation_id':'x','resource_id':'r:x','continuity':{'project':1,'workload':1,'provider':1,'policy':1,'recovery':1},'policy_id':'policy.main','provider_profile':'SOFTWARE_REFERENCE','result_digest':'a'*64,'reason_codes':[]}
        with self.assertRaises(EvidenceError): e.append(event,fail_stage='after_log')
        self.assertEqual(e.recover_pending(),'RECOVERED'); self.assertTrue(e.verify_chain())

class IPCTests(unittest.TestCase):
    def setUp(self): self.i=IPCAuthenticator(b'I'*32); self.now=1000000
    def frame(self,body={'op':'status'}): return self.i.sign(client_id='client.one',seq=1,nonce='abcdefghijklmnop',issued_at=self.now,body=body)
    def test_valid(self): self.assertEqual(self.i.verify(self.frame(),now=self.now),{'op':'status'})
    def test_replay(self):
        f=self.frame(); self.i.verify(f,now=self.now)
        with self.assertRaises(IPCError): self.i.verify(f,now=self.now)
    def test_tamper(self):
        f=self.frame(); f['body']={'op':'evil'}
        with self.assertRaises(IPCError): self.i.verify(f,now=self.now)
    def test_stale(self):
        with self.assertRaises(IPCError): self.i.verify(self.frame(),now=self.now+1000)
    def test_unknown_field(self):
        f=self.frame(); f['admin']=True
        with self.assertRaises(IPCError): self.i.verify(f,now=self.now)
    def test_oversize(self):
        with self.assertRaises(IPCError): self.i.sign(client_id='client.one',seq=1,nonce='abcdefghijklmnop',issued_at=self.now,body={'x':'a'*(1024*1024+1)})

class ProviderTests(unittest.TestCase):
    def test_deterministic_derive(self):
        p=SoftwareReferenceProvider(PK); self.assertEqual(p.derive('x',b'c'),p.derive('x',b'c'))
    def test_domain_separation(self):
        p=SoftwareReferenceProvider(PK); self.assertNotEqual(p.derive('x',b'c'),p.derive('y',b'c'))
    def test_health_fail(self):
        p=SoftwareReferenceProvider(PK); p.set_health(False)
        with self.assertRaises(Exception): p.derive('x',b'c')
    def test_root_not_in_public(self):
        p=SoftwareReferenceProvider(PK); self.assertNotIn('root',json.dumps(p.public_status()).lower())


class DurableReplayAndRecoveryTests(RBase):
    def test_one_use_replay_refused_after_restart(self):
        a=self.r.acquire(self.req,self.ctx,one_use=True)
        self.assertEqual(self.r.execute(a.envelope,self.req,self.ctx).state,'OPEN')
        r2=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        self.assertEqual(r2.execute(a.envelope,self.req,self.ctx).reason_codes,('CAPABILITY_CONSUMED',))
    def test_recovery_crash_after_journal_aborts_on_restart(self):
        old=self.r.continuity()
        with self.assertRaises(RuntimeError): self.r.trusted_recovery('xpadi','xpadi.runtime',fail_stage='after_journal')
        r2=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        self.assertEqual(r2.continuity(),old)
        self.assertFalse((self.tmp/'state/recovery_pending.json').exists())
    def test_recovery_crash_after_state_finalizes_evidence_on_restart(self):
        old=self.r.continuity()
        with self.assertRaises(RuntimeError): self.r.trusted_recovery('xpadi','xpadi.runtime',fail_stage='after_state')
        self.assertEqual(self.r.continuity().recovery,old.recovery+1)
        r2=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        self.assertEqual(r2.continuity().recovery,old.recovery+1)
        self.assertTrue(any(x.get('event')=='continuity.recovery' for x in r2.evidence.receipts()))
        self.assertFalse((self.tmp/'state/recovery_pending.json').exists())
    def test_recovery_crash_after_evidence_is_idempotent(self):
        with self.assertRaises(RuntimeError): self.r.trusted_recovery('xpadi','xpadi.runtime',fail_stage='after_evidence')
        before=len(self.r.evidence.receipts())
        r2=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK)
        after=len(r2.evidence.receipts())
        self.assertEqual(before,after)

class PersistentIPCTests(unittest.TestCase):
    def test_replay_refused_across_authenticator_restart(self):
        tmp=Path(tempfile.mkdtemp()); path=tmp/'ipc.json'; now=1000000
        try:
            a=IPCAuthenticator(b'I'*32,path); f=a.sign(client_id='client.one',seq=7,nonce='abcdefghijklmnop',issued_at=now,body={'op':'status'})
            a.verify(f,now=now)
            b=IPCAuthenticator(b'I'*32,path)
            with self.assertRaises(IPCError): b.verify(f,now=now)
        finally: shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__': unittest.main()
