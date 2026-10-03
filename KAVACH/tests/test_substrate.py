import unittest,tempfile,shutil,json,time
from pathlib import Path
from dataclasses import replace
from kavach_runtime import KAVACHRuntime, EvidenceObservation
from kavach_semantic import ProtectionRequest
from kavach_substrate.profiles import CATALOG,resolve_profiles,ProfileError
from kavach_substrate.extensions import REGISTRY,ExtensionFramework,ExtensionContract,ExtensionError
from kavach_substrate.adapters import MANIFESTS,AdapterManifest,AdapterError
from kavach_substrate.sdk import KAVACHClient
from kavach_substrate.compatibility import V1RuntimeAdapter

AK=b'A'*32; PK=b'P'*32; EK=b'E'*32

def obs(state='TRUSTED'): return [EvidenceObservation('runtime',state,'1'*64,{'kind':'runtime'},True)]
class Base(unittest.TestCase):
    def setUp(self):
        self.tmp=Path(tempfile.mkdtemp()); self.r=KAVACHRuntime(self.tmp,authority_key=AK,provider_key=PK,evidence_key=EK); self.c=KAVACHClient(self.r)
        self.ctx=self.r.build_context('xpadi','xpadi.runtime',obs(),context_id='ctx:c')
        self.req=ProtectionRequest('req:c','xpadi','xpadi.runtime','generation:1','xpadi.generation.commit','commit',self.ctx.digest,'b'*64,'SOFTWARE_REFERENCE')
    def tearDown(self): shutil.rmtree(self.tmp,ignore_errors=True)

class ProfileTests(Base):
    def test_catalog_exact(self): self.assertEqual(set(CATALOG),{'KAVACH-BASE','KAVACH-KEY','KAVACH-RUNTIME','KAVACH-SURVIVAL','KAVACH-RECOVERY'})
    def test_base_activates(self): self.assertIn('KAVACH-BASE',self.c.activate_profiles(['KAVACH-BASE'])['profiles'])
    def test_unknown_profile_fails(self):
        with self.assertRaises(ProfileError): self.c.activate_profiles(['KAVACH-MAGIC'])
    def test_key_provider_capabilities(self): self.assertIn('key.derive',self.c.activate_profiles(['KAVACH-KEY'])['provider_capabilities'])
    def test_survival_preserves_extensions(self): self.assertIn('airs-sff',self.c.activate_profiles(['KAVACH-SURVIVAL'])['extensions'])
    def test_profile_does_not_remove_recovery_dependency(self): self.assertIn('recovery',self.c.activate_profiles(['KAVACH-BASE'])['continuity_dependencies'])
    def test_provider_missing_capability_fails(self):
        self.r.provider.descriptor=lambda: type('D',(object,),{'capabilities':frozenset({'capability.authority'}),'profile':'SOFTWARE_REFERENCE'})()
        with self.assertRaises(ProfileError): resolve_profiles(['KAVACH-KEY'],self.r.provider.descriptor(),ExtensionFramework().registry)

class ExtensionTests(unittest.TestCase):
    def test_all_retained_present(self):
        for x in ('airs-pwe','airs-sff','faso','rap','srm','isolated-recovery','gpt-reconstruction','fragment-survivability','recovery-ceremony'): self.assertIn(x,REGISTRY)
    def test_no_extension_has_forbidden_privilege(self): self.assertTrue(all(not e.privileges for e in REGISTRY.values()))
    def test_forbidden_privilege_rejected(self):
        with self.assertRaises(ValueError): ExtensionContract('evil','PROJECT-BOUND','x','x',frozenset({'evidence.observation'}),frozenset({'project'}),'dependent-authorities-only',frozenset({'set.open'}))
    def test_unpermitted_output_refused(self):
        with self.assertRaises(ExtensionError): ExtensionFramework().validate_output('airs-pwe','authority.issue')
    def test_pwe_is_experimental(self): self.assertEqual(REGISTRY['airs-pwe'].status,'EXPERIMENTAL-HOLD')
    def test_sff_is_project_bound(self): self.assertEqual(REGISTRY['airs-sff'].status,'PROJECT-BOUND')

class AdapterTests(unittest.TestCase):
    def test_all_project_manifests_valid(self):
        for m in MANIFESTS.values(): self.assertTrue(m.validate())
    def test_xpadi_profiles(self): self.assertEqual(set(MANIFESTS['xpadi'].profiles),{'KAVACH-BASE','KAVACH-KEY','KAVACH-SURVIVAL','KAVACH-RECOVERY','KAVACH-RUNTIME'})
    def test_transcript_ownership_excludes_semantics(self): self.assertIn('package.semantics',MANIFESTS['transcript'].ownership_exclusions)
    def test_xaipt_ownership_excludes_payment(self): self.assertIn('payment.logic',MANIFESTS['xaipt'].ownership_exclusions)
    def test_xlp_ownership_excludes_veda(self): self.assertIn('veda.semantics',MANIFESTS['xlp'].ownership_exclusions)
    def test_namespace_escape_rejected(self):
        m=replace(MANIFESTS['xpadi'],authorities=('xaipt.payment.authorize',))
        with self.assertRaises(AdapterError): m.validate()
    def test_non_failclosed_adapter_rejected(self):
        m=replace(MANIFESTS['xpadi'],failure_policy='FAIL_OPEN')
        with self.assertRaises(AdapterError): m.validate()

class SDKTests(Base):
    def test_connect(self): self.assertTrue(self.c.connect()['connected'])
    def test_status(self): self.assertTrue(self.c.status()['evidence_valid'])
    def test_passport_truthful(self):
        p=self.c.security_passport(['KAVACH-BASE','KAVACH-KEY']); self.assertEqual(p['assurance_boundary'],'SOFTWARE_REFERENCE'); self.assertIn('HARDWARE_ROOT_ASSURANCE',p['unsupported_guarantees'])
    def test_passport_digest_stable(self):
        a=self.c.security_passport(['KAVACH-BASE']); b=self.c.security_passport(['KAVACH-BASE']); self.assertEqual(a['passport_digest'],b['passport_digest'])
    def test_sdk_acquire_execute(self):
        a=self.c.acquire(self.req,self.ctx,['KAVACH-BASE'],one_use=False); self.assertEqual(a.state,'OPEN'); self.assertEqual(self.c.execute(a.envelope,self.req,self.ctx).state,'OPEN')
    def test_profile_continuity_applied(self):
        a=self.c.acquire(self.req,self.ctx,['KAVACH-BASE'],one_use=False); self.r.trusted_recovery('xpadi','xpadi.runtime'); self.assertEqual(self.r.execute(a.envelope,self.req,self.ctx).reason_codes,('STALE_CONTINUITY',))
    def test_sdk_does_not_expose_set_open(self): self.assertFalse(hasattr(self.c,'set_open'))
    def test_sdk_does_not_expose_provider_root(self): self.assertFalse(hasattr(self.c,'provider_root'))
    def test_receipt_verify(self):
        a=self.c.acquire(self.req,self.ctx,['KAVACH-BASE']); self.assertTrue(self.c.verify_receipt(a.receipt))

class CompatibilityTests(Base):
    def test_v1_connect(self): self.assertTrue(self.c.v1.connect()['connected'])
    def test_v1_epoch_status(self): self.assertEqual(self.c.v1.status()['epoch'],1)
    def test_v1_acquire_uses_recovery_dependency(self):
        a=self.c.v1.acquire(self.req,self.ctx,False); self.assertEqual(a.envelope.continuity_dependencies,frozenset({'recovery'}))
    def test_v1_kvc001_after_recovery(self):
        a=self.c.v1.acquire(self.req,self.ctx,False); self.r.trusted_recovery('xpadi','xpadi.runtime'); self.assertEqual(self.c.v1.execute(a.envelope,self.req,self.ctx).reason_codes,('STALE_CONTINUITY',))
    def test_v1_verify_receipt(self):
        a=self.c.v1.acquire(self.req,self.ctx,False); self.assertTrue(self.c.v1.verify_receipt(a.receipt))

class AdversarialTests(Base):
    def test_profile_cannot_downgrade_required_request_assurance(self):
        q=replace(self.req,required_assurance='TPM_BOUND'); d=self.c.evaluate(q,self.ctx); self.assertEqual(d.state,'REFUSE')
    def test_sdk_request_tamper_is_core_refused(self):
        a=self.c.acquire(self.req,self.ctx,['KAVACH-BASE'],one_use=False); q=replace(self.req,resource_id='generation:2'); self.assertEqual(self.c.execute(a.envelope,q,self.ctx).state,'REFUSE')
    def test_optional_extension_failure_not_global_open(self):
        x=ExtensionFramework();
        with self.assertRaises(ExtensionError): x.validate_output('airs-pwe','authority.issue')
        c2=self.r.build_context('xpadi','xpadi.runtime',obs('UNKNOWN'),context_id='ctx:u'); q=replace(self.req,context_digest=c2.digest); self.assertEqual(self.r.evaluate(q,c2).state,'HOLD')
    def test_malicious_adapter_cannot_claim_core_authority(self):
        m=replace(MANIFESTS['xpadi'],authorities=('kavach.core.set_open',))
        with self.assertRaises(AdapterError): m.validate()

if __name__=='__main__': unittest.main()
