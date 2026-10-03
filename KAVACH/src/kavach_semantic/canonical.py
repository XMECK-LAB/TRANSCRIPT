
import json, hashlib, hmac
class CanonicalError(ValueError): pass
def _bad_const(x): raise CanonicalError("non-finite numeric")
def _pairs(pairs):
    d={}
    for k,v in pairs:
        if k in d: raise CanonicalError("duplicate key")
        d[k]=v
    return d
def _walk(v,depth=0):
    if depth>32: raise CanonicalError("depth")
    if isinstance(v,dict):
        if len(v)>256: raise CanonicalError("members")
        for k,x in v.items():
            if not isinstance(k,str) or len(k.encode())>128: raise CanonicalError("key")
            _walk(x,depth+1)
    elif isinstance(v,(list,tuple)):
        if len(v)>1024: raise CanonicalError("array")
        for x in v:_walk(x,depth+1)
    elif isinstance(v,str):
        if len(v.encode("utf-8"))>65536: raise CanonicalError("string")
    elif isinstance(v,bool) or v is None: pass
    elif isinstance(v,int):
        if not -(2**63)<=v<=2**63-1: raise CanonicalError("int")
    else: raise CanonicalError("type")
def canonical_bytes(o):
    _walk(o)
    return json.dumps(o,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()
def strict_json_loads(raw):
    if raw.startswith(b"\xef\xbb\xbf"): raise CanonicalError("bom")
    try: t=raw.decode("utf-8","strict")
    except UnicodeDecodeError as e: raise CanonicalError("utf8") from e
    o=json.loads(t,object_pairs_hook=_pairs,parse_constant=_bad_const,
                 parse_float=lambda x: (_ for _ in ()).throw(CanonicalError("float")))
    if canonical_bytes(o)!=raw: raise CanonicalError("noncanonical")
    return o
def digest_hex(o): return hashlib.sha256(canonical_bytes(o)).hexdigest()
def mac_hex(key,domain,o):
    if len(key)<32: raise CanonicalError("short mac key")
    return hmac.new(key,domain.encode("ascii")+b"\0"+canonical_bytes(o),hashlib.sha256).hexdigest()
