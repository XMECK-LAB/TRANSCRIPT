from dataclasses import dataclass
from typing import FrozenSet, Dict
from kavach_semantic.model import ASSURANCE, CF

class ProfileError(RuntimeError): pass

@dataclass(frozen=True)
class ProtectionProfile:
    profile_id:str
    authorities:FrozenSet[str]
    provider_capabilities:FrozenSet[str]
    required_assurance:str
    continuity_dependencies:FrozenSet[str]
    evidence_required:bool=True
    extensions:FrozenSet[str]=frozenset()
    def __post_init__(self):
        if self.required_assurance not in ASSURANCE: raise ValueError('invalid assurance')
        if not self.continuity_dependencies or not self.continuity_dependencies.issubset(set(CF)): raise ValueError('invalid continuity dependencies')
        if not self.profile_id.startswith('KAVACH-'): raise ValueError('invalid profile id')

CATALOG={
 'KAVACH-BASE':ProtectionProfile('KAVACH-BASE',frozenset({'capability.authority'}),frozenset({'capability.authority'}),'SOFTWARE_REFERENCE',frozenset({'project','workload','policy','recovery'})),
 'KAVACH-KEY':ProtectionProfile('KAVACH-KEY',frozenset({'key.authority','crypto.authority'}),frozenset({'key.derive','crypto.mac','crypto.verify'}),'SOFTWARE_REFERENCE',frozenset({'project','workload','provider','policy','recovery'})),
 'KAVACH-RUNTIME':ProtectionProfile('KAVACH-RUNTIME',frozenset({'runtime.execute'}),frozenset({'capability.authority'}),'SOFTWARE_REFERENCE',frozenset({'project','workload','provider','policy','recovery'})),
 'KAVACH-SURVIVAL':ProtectionProfile('KAVACH-SURVIVAL',frozenset({'survival.authorize'}),frozenset({'capability.authority'}),'SOFTWARE_REFERENCE',frozenset({'project','workload','policy','recovery'}),extensions=frozenset({'airs-pwe','airs-sff','faso'})),
 'KAVACH-RECOVERY':ProtectionProfile('KAVACH-RECOVERY',frozenset({'recovery.authorize'}),frozenset({'capability.authority'}),'SOFTWARE_REFERENCE',frozenset({'project','workload','provider','policy','recovery'}),extensions=frozenset({'rap','srm','isolated-recovery'})),
}

def resolve_profiles(ids, provider_descriptor, extension_registry):
    if not ids: raise ProfileError('at least one protection profile required')
    unknown=set(ids)-set(CATALOG)
    if unknown: raise ProfileError('unknown profile: '+','.join(sorted(unknown)))
    profiles=[CATALOG[x] for x in sorted(set(ids))]
    required_caps=set(); deps=set(); required_ext=set(); max_assurance='SOFTWARE_REFERENCE'
    for p in profiles:
        required_caps.update(p.provider_capabilities); deps.update(p.continuity_dependencies); required_ext.update(p.extensions)
        if ASSURANCE[p.required_assurance]>ASSURANCE[max_assurance]: max_assurance=p.required_assurance
    missing=required_caps-set(provider_descriptor.capabilities)
    if missing: raise ProfileError('provider missing capabilities: '+','.join(sorted(missing)))
    # Extensions that are PROJECT_BOUND are not required to activate the profile runtime itself.
    for eid in sorted(required_ext):
        e=extension_registry.get(eid)
        if e is None: raise ProfileError('extension contract missing: '+eid)
        if e.status=='REJECTED': raise ProfileError('rejected extension required: '+eid)
    return {'profiles':tuple(p.profile_id for p in profiles),'continuity_dependencies':frozenset(deps),'required_assurance':max_assurance,
            'provider_capabilities':frozenset(required_caps),'extensions':frozenset(required_ext)}
