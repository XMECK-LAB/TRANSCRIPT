
from pathlib import Path
import json, threading, hashlib, hmac
from kavach_semantic.canonical import canonical_bytes, strict_json_loads, digest_hex
from .util import atomic_write_json

ZERO='0'*64
class EvidenceError(RuntimeError): pass

class EvidenceRuntime:
    def __init__(self,root:Path,key:bytes):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
        self.log=self.root/'receipts.jsonl'; self.head=self.root/'head.json'
        if len(key)<32: raise ValueError('evidence key must be >=32 bytes')
        self._key=bytes(key); self.lock=threading.RLock()
        if not self.head.exists(): atomic_write_json(self.head,{'schema':'kavach.evidence-head/v2','sequence':-1,'digest':ZERO})
    def _tag(self,unsigned):
        return hmac.new(self._key,b'KAVACH2/EVIDENCE\x00'+canonical_bytes(unsigned),hashlib.sha256).hexdigest()
    def append(self,event:dict,fail_stage=None):
        # Append then advance independent head. A pending journal makes recovery deterministic.
        with self.lock:
            self.verify_chain()
            h=strict_json_loads(self.head.read_bytes()); seq=h['sequence']+1; pred=h['digest']
            unsigned={'schema':'kavach.receipt/v2','sequence':seq,'predecessor_digest':pred,**event}
            receipt={**unsigned,'authenticator':self._tag(unsigned)}
            digest=digest_hex(receipt)
            journal=self.root/'pending.json'
            atomic_write_json(journal,{'schema':'kavach.pending/v2','receipt':receipt,'digest':digest})
            if fail_stage=='after_journal': raise EvidenceError('injected after journal')
            with self.log.open('ab') as f:
                f.write(canonical_bytes(receipt)+b'\n'); f.flush();
                try:
                    import os; os.fsync(f.fileno())
                except Exception: pass
            if fail_stage=='after_log': raise EvidenceError('injected after log')
            atomic_write_json(self.head,{'schema':'kavach.evidence-head/v2','sequence':seq,'digest':digest})
            try: journal.unlink()
            except FileNotFoundError: pass
            return receipt
    def recover_pending(self):
        with self.lock:
            p=self.root/'pending.json'
            if not p.exists(): return 'CLEAN'
            pending=strict_json_loads(p.read_bytes()); receipt=pending['receipt']; dg=pending['digest']
            lines=self._read_lines_raw()
            log_has=bool(lines and digest_hex(lines[-1])==dg)
            head=strict_json_loads(self.head.read_bytes())
            if log_has and head['digest']!=dg:
                atomic_write_json(self.head,{'schema':'kavach.evidence-head/v2','sequence':receipt['sequence'],'digest':dg})
            elif not log_has:
                # journal only => no committed receipt; discard.
                pass
            p.unlink()
            self.verify_chain()
            return 'RECOVERED'
    def _read_lines_raw(self):
        if not self.log.exists(): return []
        out=[]
        for raw in self.log.read_bytes().splitlines():
            if not raw: continue
            out.append(strict_json_loads(raw))
        return out
    def verify_chain(self):
        with self.lock:
            lines=self._read_lines_raw(); prev=ZERO
            for i,r in enumerate(lines):
                if r.get('sequence')!=i: raise EvidenceError('sequence/reorder/truncation anomaly')
                if r.get('predecessor_digest')!=prev: raise EvidenceError('predecessor/fork anomaly')
                unsigned={k:v for k,v in r.items() if k!='authenticator'}
                if not hmac.compare_digest(self._tag(unsigned),r.get('authenticator','')): raise EvidenceError('receipt mutation')
                prev=digest_hex(r)
            h=strict_json_loads(self.head.read_bytes())
            exp_seq=len(lines)-1; exp_dg=ZERO if not lines else prev
            if h.get('sequence')!=exp_seq or h.get('digest')!=exp_dg: raise EvidenceError('head rollback/truncation')
            return True

    def receipts(self):
        with self.lock:
            self.verify_chain()
            return tuple(self._read_lines_raw())
    def has_successful_execution(self, authority_ref):
        with self.lock:
            self.verify_chain()
            for r in self._read_lines_raw():
                if r.get('event')=='authority.execute' and r.get('authority_ref')==authority_ref and not r.get('reason_codes'):
                    return True
            return False
    def has_transaction(self, transaction_id, event=None):
        with self.lock:
            self.verify_chain()
            for r in self._read_lines_raw():
                if r.get('transaction_id')==transaction_id and (event is None or r.get('event')==event):
                    return True
            return False

    def verify_receipt(self,receipt):
        unsigned={k:v for k,v in receipt.items() if k!='authenticator'}
        return hmac.compare_digest(self._tag(unsigned),receipt.get('authenticator',''))
