
import unittest
from dataclasses import replace
from kavach_semantic import *
from kavach_semantic.canonical import canonical_bytes, strict_json_loads, CanonicalError, digest_hex
K=b"K"*32
def cv(**kw):
 d=dict(project=1,workload=2,provider=3,policy=4,recovery=5);d.update(kw);return ContinuityVector(**d)
def ctx(state="TRUSTED",complete=100,project="xpadi",workload="xpadi.runtime",v=None):
 v=v or cv(); b=dict(context_id="ctx:1",project_id=project,workload_id=workload,appraisal_state=state,
 evidence_refs=("ev:1",),measurement_summary={"runtime":"ok"},provider_state="healthy",recovery_state="normal",
 continuity_inputs=v.as_dict(),policy_id="policy.main",policy_digest="a"*64,completeness=complete)
 return TrustContext(**b,digest=digest_hex(b))
def req(c=None,project="xpadi",workload="xpadi.runtime",resource="generation:1",authority="xpadi.generation.commit",op="commit",assurance="SOFTWARE_REFERENCE"):
 c=c or ctx(project=project,workload=workload)
 return ProtectionRequest("req:1",project,workload,resource,authority,op,c.digest,"b"*64,assurance)
def prov(pid="provider.software",profile="SOFTWARE_REFERENCE",healthy=True):
 return ProviderDescriptor(pid,profile,frozenset({"capability.authority"}),healthy)

class Canonical(unittest.TestCase):
 def test_order(self): self.assertEqual(canonical_bytes({"b":1,"a":2}),b'{"a":2,"b":1}')
 def test_roundtrip(self):
  r=canonical_bytes({"a":[1,2],"b":"x"}); self.assertEqual(strict_json_loads(r),{"a":[1,2],"b":"x"})
 def test_noncanonical(self):
  with self.assertRaises(CanonicalError): strict_json_loads(b'{"b":1, "a":2}')
 def test_duplicate(self):
  with self.assertRaises(CanonicalError): strict_json_loads(b'{"a":1,"a":2}')
 def test_float(self):
  with self.assertRaises(CanonicalError): canonical_bytes({"a":1.5})

class Semantics(unittest.TestCase):
 def setUp(self):
  self.k=SemanticKernel(K);self.v=cv();self.c=ctx(v=self.v);self.p=prov();self.r=req(self.c)
 def test_open(self): self.assertEqual(self.k.evaluate(self.r,self.c,self.v,self.p).state,"OPEN")
 def test_unknown_hold(self):
  c=ctx("UNKNOWN",v=self.v);r=req(c);self.assertEqual(self.k.evaluate(r,c,self.v,self.p).state,"HOLD")
 def test_untrusted_refuse(self):
  c=ctx("UNTRUSTED",v=self.v);r=req(c);self.assertEqual(self.k.evaluate(r,c,self.v,self.p).state,"REFUSE")
 def test_incomplete_hold(self):
  c=ctx("TRUSTED",50,v=self.v);r=req(c);self.assertEqual(self.k.evaluate(r,c,self.v,self.p).state,"HOLD")
 def test_cross_project(self):
  r=req(self.c,project="xaipt");self.assertEqual(self.k.evaluate(r,self.c,self.v,self.p).reason_codes,("PROJECT_MISMATCH",))
 def test_assurance(self):
  r=replace(self.r,required_assurance="TPM_BOUND");self.assertEqual(self.k.evaluate(r,self.c,self.v,self.p).reason_codes,("PROVIDER_ASSURANCE_INSUFFICIENT",))
 def test_provider_down(self):
  self.assertEqual(self.k.evaluate(self.r,self.c,self.v,prov(healthy=False)).state,"HOLD")

class Authority(unittest.TestCase):
 def setUp(self):
  self.k=SemanticKernel(K);self.v=cv();self.c=ctx(v=self.v);self.p=prov();self.r=req(self.c)
  self.d=self.k.evaluate(self.r,self.c,self.v,self.p);self.e=self.k.issue(self.r,self.d,self.c,self.p,one_use=False)
 def test_execute_current(self): self.assertTrue(self.k.execute(self.e,self.r,self.c,self.v,self.p).allowed)
 def test_kvc001_recovery(self):
  x=self.k.execute(self.e,self.r,self.c,self.k.recover(self.v),self.p);self.assertEqual(x.reason_codes,("STALE_CONTINUITY",))
 def test_provider_generation(self):
  self.assertEqual(self.k.execute(self.e,self.r,self.c,cv(provider=99),self.p).reason_codes,("STALE_CONTINUITY",))
 def test_policy_generation(self):
  self.assertEqual(self.k.execute(self.e,self.r,self.c,cv(policy=99),self.p).reason_codes,("STALE_CONTINUITY",))
 def test_cross_resource(self):
  self.assertEqual(self.k.execute(self.e,replace(self.r,resource_id="generation:2"),self.c,self.v,self.p).reason_codes,("RESOURCE_MISMATCH",))
 def test_cross_authority(self):
  self.assertEqual(self.k.execute(self.e,replace(self.r,authority_id="xpadi.recovery.begin"),self.c,self.v,self.p).reason_codes,("AUTHORITY_MISMATCH",))
 def test_provider_substitution(self):
  self.assertEqual(self.k.execute(self.e,self.r,self.c,self.v,prov("provider.other")).reason_codes,("PROVIDER_CHANGED",))
 def test_policy_substitution(self):
  self.assertEqual(self.k.execute(self.e,self.r,replace(self.c,policy_digest="c"*64),self.v,self.p).reason_codes,("POLICY_CHANGED",))
 def test_exec_reappraises_unknown(self):
  self.assertEqual(self.k.execute(self.e,self.r,replace(self.c,appraisal_state="UNKNOWN"),self.v,self.p).state,"HOLD")
 def test_v1_projection(self):
  self.assertEqual(V1Compatibility.epoch_from_v2(self.v),5);self.assertEqual(V1Compatibility.epoch_from_v2(self.k.recover(self.v)),6)
 def test_v1_old_epoch_refused(self):
  e=self.k.issue(self.r,self.d,self.c,self.p,deps=V1Compatibility.deps_for_v1(),one_use=False)
  self.assertEqual(self.k.execute(e,self.r,self.c,self.k.recover(self.v),self.p).reason_codes,("STALE_CONTINUITY",))
 def test_tamper_authenticator(self):
  e=replace(self.e,resource_id="generation:2");self.assertEqual(self.k.execute(e,self.r,self.c,self.v,self.p).reason_codes,("AUTHORITY_REFUSED",))
 def test_one_use(self):
  e=self.k.issue(self.r,self.d,self.c,self.p,one_use=True,nonce="1234567890abcdef")
  self.assertTrue(self.k.execute(e,self.r,self.c,self.v,self.p).allowed)
  self.assertEqual(self.k.execute(e,self.r,self.c,self.v,self.p).reason_codes,("CAPABILITY_CONSUMED",))
 def test_rejected_does_not_consume(self):
  e=self.k.issue(self.r,self.d,self.c,self.p,one_use=True,nonce="fedcba0987654321")
  self.assertFalse(self.k.execute(e,replace(self.r,resource_id="generation:2"),self.c,self.v,self.p).allowed)
  self.assertTrue(self.k.execute(e,self.r,self.c,self.v,self.p).allowed)
 def test_recovery_no_mutation(self):
  before=self.e.continuity.recovery;self.k.recover(self.v);self.assertEqual(self.e.continuity.recovery,before)

class Determinism(unittest.TestCase):
 def test_decision_repeatable(self):
  v=cv();c=ctx(v=v);r=req(c);p=prov()
  self.assertEqual(SemanticKernel(K).evaluate(r,c,v,p),SemanticKernel(K).evaluate(r,c,v,p))
 def test_envelope_repeatable(self):
  v=cv();c=ctx(v=v);r=req(c);p=prov()
  k1=SemanticKernel(K);d1=k1.evaluate(r,c,v,p);e1=k1.issue(r,d1,c,p,one_use=False)
  k2=SemanticKernel(K);d2=k2.evaluate(r,c,v,p);e2=k2.issue(r,d2,c,p,one_use=False)
  self.assertEqual(e1,e2)

if __name__=="__main__":unittest.main()
