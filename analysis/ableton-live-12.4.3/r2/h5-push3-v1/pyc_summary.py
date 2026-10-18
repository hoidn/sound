"""H5: static summary of selected Push3.app Python 3.11 bytecode modules.

marshal.loads + code-object walk only; never imports, execs or evals target code.
  python3.11 -I pyc_summary.py > pyc-summary.txt
Prints per module: SHA-256, co_filename, sorted co_names, and short string constants.
For CONSTANT_MODULES also prints module-level `NAME = <constant>` assignments (LOAD_CONST then STORE_NAME).
"""
import dis, hashlib, importlib.util, marshal, sys, types
from pathlib import Path

PY = Path('/home/ollie/Ableton Live 12 Suite.app/Contents/Helpers/Push3.app/Contents/Resources/python')
MODULES = ['live_model/model', 'live_model/Live/__init__', 'Push2/__init__', 'Push2/push2', 'Push2/push2_model',
           'Push2/firmware_utils', 'Push2/upgrader', 'Push2/flash_firmware_update_status_watcher',
           'Push2/software_update_progress_component', 'Push2/sysex', 'Push2/elements']
CONSTANT_MODULES = {'Push2/sysex'}


def walk(co):
    yield co
    for c in co.co_consts:
        if isinstance(c, types.CodeType):
            yield from walk(c)


assert importlib.util.MAGIC_NUMBER == b'\xa7\x0d\x0d\x0a', 'need CPython 3.11 (magic 3495)'
print(f'# decoder CPython {sys.version.split()[0]}; marshal.loads only, not executed')
for m in MODULES:
    data = (PY / f'{m}.pyc').read_bytes()
    assert data[:4] == importlib.util.MAGIC_NUMBER, m
    co = marshal.loads(data[16:])
    names, strs = set(), set()
    for c in walk(co):
        names.update(c.co_names)
        strs.update(k for k in c.co_consts if isinstance(k, str) and 2 < len(k) < 100)
    print(f'\n## {m}.pyc sha256={hashlib.sha256(data).hexdigest()}\nco_filename: {co.co_filename}')
    print('names:', ' '.join(sorted(names)))
    print('strings:', ' | '.join(repr(s) for s in sorted(strs)))
    if m in CONSTANT_MODULES:
        ins = list(dis.get_instructions(co))
        for a, b in zip(ins, ins[1:]):
            if a.opname == 'LOAD_CONST' and b.opname == 'STORE_NAME' and not isinstance(a.argval, types.CodeType):
                print(f'const {b.argval} = {a.argval!r}')
        for i, x in enumerate(ins):  # composed constants, e.g. MANUFACTURER_ID + (..)
            if x.opname == 'STORE_NAME' and str(x.argval).startswith(('IDENTITY_RESPONSE', 'MESSAGE_START')):
                print(f'expr {x.argval} <-', [(y.opname, y.argval) for y in ins[i - 6:i]])
