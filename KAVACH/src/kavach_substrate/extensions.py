from dataclasses import dataclass
from typing import FrozenSet

class ExtensionError(RuntimeError): pass
ALLOWED_STATUS={'CORE-SUPPORTED','PROJECT-BOUND','EXPERIMENTAL-HOLD'}
FORBIDDEN_PRIVILEGES=frozenset({'set.open','continuity.mutate','authority.issue','provider.root','evidence.fabricate'})

@dataclass(frozen=True)
class ExtensionContract:
    extension_id:str
    status:str
    owner:str
    purpose:str
    allowed_outputs:FrozenSet[str]
    continuity_dependencies:FrozenSet[str]
    failure_scope:str
    privileges:FrozenSet[str]=frozenset()
    def __post_init__(self):
        if self.status not in ALLOWED_STATUS: raise ValueError('invalid extension status')
        if self.privileges & FORBIDDEN_PRIVILEGES: raise ValueError('extension requests forbidden privilege')

REGISTRY={
 'airs-pwe':ExtensionContract('airs-pwe','EXPERIMENTAL-HOLD','AIRS extension','crypto/structural/temporal observations',frozenset({'evidence.observation'}),frozenset({'workload','policy'}),'dependent-authorities-only'),
 'airs-sff':ExtensionContract('airs-sff','PROJECT-BOUND','survival profile + consumer','fragment-survivability hooks/evidence',frozenset({'evidence.observation','protected.operation.request'}),frozenset({'project','recovery'}),'dependent-authorities-only'),
 'faso':ExtensionContract('faso','PROJECT-BOUND','survival profile + consumer','storage-overlay protection interface',frozenset({'evidence.observation','protected.operation.request'}),frozenset({'project','recovery'}),'dependent-authorities-only'),
 'rap':ExtensionContract('rap','PROJECT-BOUND','recovery profile','recovery-authority boundary/partition contract',frozenset({'evidence.observation','protected.operation.request'}),frozenset({'project','provider','recovery'}),'dependent-authorities-only'),
 'srm':ExtensionContract('srm','PROJECT-BOUND','recovery profile + consumer','survivable recovery method contract',frozenset({'evidence.observation','protected.operation.request'}),frozenset({'project','recovery'}),'dependent-authorities-only'),
 'isolated-recovery':ExtensionContract('isolated-recovery','PROJECT-BOUND','recovery profile','independent recovery-environment contract',frozenset({'evidence.observation','protected.operation.request'}),frozenset({'provider','recovery'}),'dependent-authorities-only'),
 'gpt-reconstruction':ExtensionContract('gpt-reconstruction','PROJECT-BOUND','consumer recovery product','full GPT reconstruction support interface',frozenset({'protected.operation.request'}),frozenset({'project','recovery'}),'dependent-authorities-only'),
 'fragment-survivability':ExtensionContract('fragment-survivability','PROJECT-BOUND','consumer survival product','full fragment survivability support interface',frozenset({'protected.operation.request','evidence.observation'}),frozenset({'project','recovery'}),'dependent-authorities-only'),
 'recovery-ceremony':ExtensionContract('recovery-ceremony','PROJECT-BOUND','recovery profile','human/authority recovery ceremony contract',frozenset({'protected.operation.request','evidence.observation'}),frozenset({'project','provider','policy','recovery'}),'dependent-authorities-only'),
}

class ExtensionFramework:
    def __init__(self,registry=None): self.registry=dict(REGISTRY if registry is None else registry)
    def describe(self):
        return tuple({'extension_id':e.extension_id,'status':e.status,'owner':e.owner,'purpose':e.purpose,'allowed_outputs':sorted(e.allowed_outputs),
                      'continuity_dependencies':sorted(e.continuity_dependencies),'failure_scope':e.failure_scope} for e in sorted(self.registry.values(),key=lambda x:x.extension_id))
    def validate_output(self,extension_id,kind):
        e=self.registry.get(extension_id)
        if not e: raise ExtensionError('extension unknown')
        if kind not in e.allowed_outputs: raise ExtensionError('extension output not permitted')
        return True
