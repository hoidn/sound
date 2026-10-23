#!/usr/bin/env python3
"""Tamper isolated copies of this owned packet only; never invokes capture."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile

ROOT = Path(__file__).resolve().parent
module = runpy.run_path(str(ROOT/'capture-once.py'), run_name='owned_inert_checker')
check = module['check']
passed = []
for name in ['raw_byte_flip', 'word_byte_flip', 'receipt_offset', 'custody_drift', 'runtime_promotion', 'extra_read', 'missing_raw']:
    with tempfile.TemporaryDirectory(prefix='electric-owned-control-') as d:
        p = Path(d)
        shutil.copytree(ROOT/'capture', p/'capture')
        shutil.copyfile(ROOT/'pre-call-manifest.json', p/'pre-call-manifest.json')
        if name in ['raw_byte_flip', 'word_byte_flip']:
            f = p/'capture'/('bind.bin' if name == 'raw_byte_flip' else 'word-300c0.bin')
            b = bytearray(f.read_bytes())
            b[0] ^= 1
            f.write_bytes(b)
        elif name == 'missing_raw':
            (p/'capture'/'rebase.bin').unlink()
        else:
            f = p/'capture'/('projection.json' if name == 'runtime_promotion' else 'receipt.json')
            j = json.loads(f.read_text())
            if name == 'receipt_offset':
                j['reads'][0]['file_offset'] = 1
            elif name == 'custody_drift':
                j['after'][0]['bytes'] -= 1
            elif name == 'runtime_promotion':
                j['runtime_bindings_proved'] = True
            elif name == 'extra_read':
                j['reads'].append(j['reads'][0])
            f.write_text(json.dumps(j))
        check.__globals__['HERE'] = p
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                check()
        except (ValueError, FileNotFoundError):
            passed.append(name)
        else:
            raise AssertionError('accepted tamper '+name)
print(json.dumps({'owned_packet_only': True, 'rejected': passed, 'count': len(passed), 'original_or_decoder_calls': 0}, indent=2))
