import hashlib,hmac,time
from pathlib import Path
from kavach_semantic.canonical import canonical_bytes, CanonicalError, strict_json_loads
from .util import atomic_write_json

class IPCError(RuntimeError): pass

class IPCAuthenticator:
    MAX_MESSAGE=1024*1024
    MAX_CLOCK_SKEW=300
    def __init__(self,key:bytes,replay_state_path=None):
        if len(key)<32: raise ValueError('IPC key must be >=32 bytes')
        self._key=bytes(key); self._seen=set()
        self._state_path=Path(replay_state_path) if replay_state_path else None
        if self._state_path and not self._state_path.exists():
            atomic_write_json(self._state_path,{'schema':'kavach.ipc-replay/v2','clients':{}})
    def _state(self):
        if not self._state_path: return {'schema':'kavach.ipc-replay/v2','clients':{}}
        try:
            o=strict_json_loads(self._state_path.read_bytes())
            if o.get('schema')!='kavach.ipc-replay/v2' or not isinstance(o.get('clients'),dict): raise IPCError('replay state invalid')
            return o
        except IPCError: raise
        except Exception as e: raise IPCError('replay state invalid') from e
    def sign(self, *, client_id, seq:int, nonce:str, issued_at:int, body:dict):
        frame={'schema':'kavach.ipc/v2','client_id':client_id,'seq':seq,'nonce':nonce,'issued_at':issued_at,'body':body}
        try: raw=canonical_bytes(frame)
        except CanonicalError as e: raise IPCError('message invalid or too large') from e
        if len(raw)>self.MAX_MESSAGE: raise IPCError('message too large')
        tag=hmac.new(self._key,b'KAVACH2/IPC\x00'+raw,hashlib.sha256).hexdigest()
        return {**frame,'authenticator':tag}
    def verify(self,frame,now=None):
        now=int(time.time()) if now is None else int(now)
        required={'schema','client_id','seq','nonce','issued_at','body','authenticator'}
        if set(frame)!=required: raise IPCError('malformed frame')
        unsigned={k:frame[k] for k in ('schema','client_id','seq','nonce','issued_at','body')}
        try: raw=canonical_bytes(unsigned)
        except CanonicalError as e: raise IPCError('message invalid or too large') from e
        if len(raw)>self.MAX_MESSAGE: raise IPCError('message too large')
        if frame['schema']!='kavach.ipc/v2': raise IPCError('schema unsupported')
        expected=hmac.new(self._key,b'KAVACH2/IPC\x00'+raw,hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected,frame['authenticator']): raise IPCError('authentication failed')
        if abs(now-int(frame['issued_at']))>self.MAX_CLOCK_SKEW: raise IPCError('stale frame')
        client=frame['client_id']; seq=int(frame['seq']); token=(client,seq,frame['nonce'])
        if self._state_path:
            st=self._state(); last=int(st['clients'].get(client,-1))
            if seq<=last: raise IPCError('replay')
            st['clients'][client]=seq
            atomic_write_json(self._state_path,st)
        else:
            if token in self._seen: raise IPCError('replay')
            self._seen.add(token)
        return frame['body']
