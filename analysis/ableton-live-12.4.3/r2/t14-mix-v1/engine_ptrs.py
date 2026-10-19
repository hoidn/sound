"""Read qwords/floats at virtual addresses of the x86_64 Ableton Live Engine slice and name pointer targets.

usage: python3 -I engine_ptrs.py ptr ADDR...        qword at ADDR, with the alias name of the target function
       python3 -I engine_ptrs.py f32 ADDR [N]       N float32 values at ADDR
       python3 -I engine_ptrs.py f64 ADDR [N]       N float64 values at ADDR
       python3 -I engine_ptrs.py name ADDR...       alias names of functions at ADDR
Slice: $ENGINE (default below); segments __TEXT/__DATA_CONST have VA == file offset (image base 0).
Names: corpus indexes/aliases.jsonl. Read-only; output is data.
"""
import json, os, struct, sys
ENGINE = os.environ.get('ENGINE', '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/Ableton_Live_Engine_x86_64.x86_64')
ALIASES = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/corpus/indexes/aliases.jsonl'

def segments(d):
    ncmds, off, segs = struct.unpack_from('<I', d, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, cs = struct.unpack_from('<II', d, off)
        if cmd == 0x19:
            vm, vs, fo, fs = struct.unpack_from('<QQQQ', d, off + 24)
            segs.append((vm, vm + fs, fo))
        off += cs
    return segs

def names():
    m = {}
    for line in open(ALIASES):
        r = json.loads(line)
        if r['external']:
            continue
        m[int(r['entry'], 16)] = [s['name'] for s in r['symbols'] if not s['name'].startswith('__Z')] or [r['name']]
    return m

def at(d, segs, va, n):
    for lo, hi, fo in segs:
        if lo <= va < hi:
            return d[fo + va - lo:fo + va - lo + n]
    raise ValueError(f'{va:#x} not file-backed')

if __name__ == '__main__':
    d = open(ENGINE, 'rb').read(); segs = segments(d); cmd, args = sys.argv[1], sys.argv[2:]
    if cmd in ('ptr', 'name'):
        nm = names()
        for a in args:
            va = int(a, 16)
            t = struct.unpack('<Q', at(d, segs, va, 8))[0] if cmd == 'ptr' else va
            print(f'{va:#x} -> {t:#x} {" | ".join(nm.get(t, ["?"]))}')
    else:
        fmt, size = {'f32': ('<f', 4), 'f64': ('<d', 8)}[cmd]
        va, n = int(args[0], 16), int(args[1]) if len(args) > 1 else 1
        for i in range(n):
            b = at(d, segs, va + i * size, size)
            print(f'{va + i * size:#x} {struct.unpack(fmt, b)[0]!r} 0x{b[::-1].hex()}')
