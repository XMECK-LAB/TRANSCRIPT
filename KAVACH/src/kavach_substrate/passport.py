from dataclasses import dataclass
from kavach_semantic.canonical import digest_hex

SUPPORTED_INVARIANTS=('AIRS_APPRAISAL_ONLY','CORE_AUTHORITY','KLOCK_ENFORCEMENT','KVC-001','EVIDENCE_CHAIN','NO_CLIENT_SET_OPEN')
UNSUPPORTED=('HARDWARE_ROOT_ASSURANCE','FULL_PRIVILEGED_HOST_RESISTANCE','CUSTOM_CRYPTO_NOVELTY')

def security_passport(runtime,active_profiles,extensions,build_id='kavach2.block-c'):
    p=runtime.provider.public_status(); cv=runtime.continuity().as_dict()
    body={'schema':'kavach.security-passport/v2','build_id':build_id,'runtime':'KAVACH 2.0','provider':p,
          'active_profiles':sorted(active_profiles),'continuity_classes':sorted(cv),'evidence':{'authenticated_chain':True,'independent_head':True},
          'supported_invariants':list(SUPPORTED_INVARIANTS),'unsupported_guarantees':list(UNSUPPORTED),'assurance_boundary':p['profile'],
          'extensions':sorted(extensions)}
    return {**body,'passport_digest':digest_hex(body)}
