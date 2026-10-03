
from pathlib import Path
import json, hashlib, threading
from kavach_semantic.model import ContinuityVector
from kavach_semantic.canonical import strict_json_loads, canonical_bytes
from .util import atomic_write_json

class StateError(RuntimeError): pass

class RuntimeStateStore:
    FILES=('runtime.json','continuity.json','policy.json','provider.json','extension.json','compatibility.json','ipc_replay.json')
    def __init__(self, root: Path):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock()
    def _p(self,name):
        if name not in self.FILES: raise StateError('unknown store')
        return self.root/name
    def write(self,name,obj,fail_before_replace=False):
        with self.lock: atomic_write_json(self._p(name),obj,fail_before_replace)
    def read(self,name):
        p=self._p(name)
        if not p.exists(): return None
        try: return strict_json_loads(p.read_bytes())
        except Exception as e: raise StateError(f'corrupt state store: {name}') from e
    def initialize(self, cv: ContinuityVector, *, policy_id='policy.main', policy_digest='a'*64, provider=None):
        with self.lock:
            if self.read('continuity.json') is None: self.write('continuity.json',{'schema':'kavach.continuity/v2','vector':cv.as_dict()})
            if self.read('policy.json') is None: self.write('policy.json',{'schema':'kavach.policy/v2','policy_id':policy_id,'policy_digest':policy_digest})
            if self.read('runtime.json') is None: self.write('runtime.json',{'schema':'kavach.runtime/v2','generation':1,'clean_shutdown':True})
            if provider is not None and self.read('provider.json') is None: self.write('provider.json',{'schema':'kavach.provider/v2',**provider.public_status()})
            if self.read('extension.json') is None: self.write('extension.json',{'schema':'kavach.extensions/v2','extensions':[]})
            if self.read('compatibility.json') is None: self.write('compatibility.json',{'schema':'kavach.compat/v2','v1_enabled':True})
    def get_continuity(self):
        o=self.read('continuity.json')
        if not o or o.get('schema')!='kavach.continuity/v2': raise StateError('continuity missing/invalid')
        return ContinuityVector(**o['vector'])
    def set_continuity(self,cv,fail_before_replace=False):
        self.write('continuity.json',{'schema':'kavach.continuity/v2','vector':cv.as_dict()},fail_before_replace)
