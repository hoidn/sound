"""Read-only disclosed README/manifest successor; historical checker unchanged."""
from pathlib import Path
import hashlib
import sys
assert sys.argv[1:] == ['--check']
P = Path(__file__).resolve().parent
old = P / 'check.py'
assert hashlib.sha256(old.read_bytes()).hexdigest() == '899f2058692271cc259a69eb3798f1437d59d5703ea9fd6dfadc191ae3d9d4d6'
code = old.read_text()
for before, after in [("read(P / 'manifest.json')", "read(P / 'manifest-r2.json')"),
                      ("(P / 'README.md').read_text()", "(P / 'README-r2.md').read_text()")]:
    assert code.count(before) == 1
    code = code.replace(before, after)
# The original before-file set expects the current manifest beside its payloads.
assert code.count("{str(P / 'manifest.json')}") == 1
code = code.replace("{str(P / 'manifest.json')}", "{str(P / 'manifest-r2.json')}")
exec(compile(code, str(old), 'exec'), {'__name__': '__main__', '__file__': str(old)})
