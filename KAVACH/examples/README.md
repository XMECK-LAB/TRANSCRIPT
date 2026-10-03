# KAVACH Public Examples

These examples exercise the public KAVACH 2.0 software-reference surface.

## Protected-action lifecycle

`protected_action_demo.py` demonstrates a complete bounded authority path:

```text
TRUSTED context
    ↓
OPEN authority
    ↓
OPEN protected execution
    ↓
recovery continuity advances
    ↓
previous authority becomes stale
    ↓
REFUSE(STALE_CONTINUITY)
    ↓
evidence chain remains valid
```

### PowerShell

```powershell
$env:PYTHONPATH = "$PWD\KAVACH\src"
python KAVACH\examples\protected_action_demo.py
```

### Bash

```bash
PYTHONPATH="$PWD/KAVACH/src" python KAVACH/examples/protected_action_demo.py
```

For deterministic automation:

```bash
PYTHONPATH="$PWD/KAVACH/src" python KAVACH/examples/protected_action_demo.py --check
```

The example uses fixed local byte strings only as software-reference demo material. It does not claim production key management or hardware-backed assurance.
