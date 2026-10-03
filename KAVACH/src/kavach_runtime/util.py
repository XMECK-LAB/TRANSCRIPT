
from pathlib import Path
import json, os, tempfile, hashlib
from kavach_semantic.canonical import canonical_bytes

class AtomicWriteError(RuntimeError): pass

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def atomic_write(path: Path, data: bytes, fail_before_replace=False):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd,'wb') as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        if fail_before_replace:
            raise AtomicWriteError('injected failure before replace')
        os.replace(tmp,path)
        try:
            dfd=os.open(str(path.parent),os.O_RDONLY)
            try: os.fsync(dfd)
            finally: os.close(dfd)
        except Exception:
            pass
    finally:
        if os.path.exists(tmp):
            try: os.unlink(tmp)
            except OSError: pass

def atomic_write_json(path: Path, obj, fail_before_replace=False):
    atomic_write(path, canonical_bytes(obj), fail_before_replace)
