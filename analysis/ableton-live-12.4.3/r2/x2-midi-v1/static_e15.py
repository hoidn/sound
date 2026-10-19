"""Static evidence for spec E15 (not X): decompiler text of the takeover-preference chain and the
previous-value reset in both corpora, and the shipped scripts that name reset_input_history.

usage: python3 -I -B static_e15.py    (writes static-e15.txt next to this file)
Inputs: /var/tmp/sound-analysis/corpus{,-x86}/decomp/chunks (read-only), the installed package below.
"""
import bisect
import glob
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPORA = {'arm64': '/var/tmp/sound-analysis/corpus', 'x86_64': '/var/tmp/sound-analysis/corpus-x86'}
APP = os.environ.get('LIVE_APP', '/home/ollie/Ableton Live 12 Suite.app')
WANT = {
    'x86_64': ['0x1023e0050', '0x1023e2a60', '0x101556330', '0x1015566d0', '0x101bc0770', '0x101bb8da0'],
    'arm64': ['0x1022cc18c', '0x1022cec38', '0x1015661b8', '0x101b83750', '0x101b68f98', '0x101b65c1c',
              '0x101b67c9c', '0x10259b710', '0x1039fa2a4'],
}
KEYS = ('TakeOver', 'ResetInputHistory', 'reset_input_history', 'OnTakeOverModeChanged', '0xd8', '0x148',
        'DAT_1070084d0', 'DAT_10749a2b0', 'DAT_106fb2110', 'DAT_107443e78', 'DAT_10700b3f0', '_memset_pattern16',
        'DAT_1070085', 'DAT_10749a2', 'FUN_101567bfc', 'FUN_101557e20', 'CallMemberFunc', 'guard')


def chunks(root):
    files = sorted(glob.glob(f'{root}/decomp/chunks/*.jsonl'))
    firsts = []
    for f in files:
        with open(f) as fh:
            firsts.append(int(json.loads(fh.readline())['entry'], 16))
    return files, firsts


def find(files, firsts, entry):
    i = bisect.bisect_right(firsts, int(entry, 16)) - 1
    for f in files[max(0, i):i + 2]:
        for line in open(f):
            d = json.loads(line)
            if d['entry'] == entry:
                return d


def excerpt(code):
    """Whole function when short, else the lines that mention the keys above (with one line of context)."""
    lines = code.splitlines()
    if len(lines) <= 40:
        return code
    keep = sorted({j for i, l in enumerate(lines) if any(k in l for k in KEYS) for j in (i - 1, i, i + 1)
                   if 0 <= j < len(lines)})
    out, prev = [], None
    for j in keep:
        if prev is not None and j != prev + 1:
            out.append('  ...')
        out.append(lines[j])
        prev = j
    return '\n'.join(out)


out = []
for slice_, root in CORPORA.items():
    files, firsts = chunks(root)
    for e in WANT[slice_]:
        d = find(files, firsts, e)
        out.append(f'### {slice_} {e} {d["body_ranges"] if d else "NOT FOUND"}\n{excerpt(d["code"]) if d else ""}\n')
scripts = Path(APP) / 'Contents/App-Resources/MIDI Remote Scripts'
hits = sorted(str(p.relative_to(scripts)) for p in scripts.rglob('*.pyc') if b'reset_input_history' in p.read_bytes())
out.append(f'### MIDI Remote Scripts .pyc files containing b"reset_input_history" ({scripts})\n' + '\n'.join(hits) + '\n')
(HERE / 'static-e15.txt').write_text('\n'.join(out))
print(f'static-e15.txt: {len(out)} sections; reset_input_history in {hits}')
