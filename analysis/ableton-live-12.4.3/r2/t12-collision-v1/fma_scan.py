"""Fused multiply-add instructions in a device bundle's two slices (static aid; output is data).

    python3 -I fma_scan.py UNIVERSAL_EXECUTABLE ARM64_FUNCTION_ENTRY...   # hex entries, image base 0

arm64: every scalar FP 3-source instruction (FMADD, FMSUB, FNMADD, FNMSUB) and every vector or
by-element FMLA/FMLS, decoded from the raw words of __text, counted per function (bounds from
LC_FUNCTION_STARTS); the decoding follows x2-mixer-v1/fp_scan.py. x86_64: VEX FMA opcodes are
looked for in objdump output of __text and _fma/_fmaf in the import names.
"""
import re
import struct
import subprocess
import sys
import tempfile


def slices(data):
    n = struct.unpack_from('>I', data, 4)[0]
    out = {}
    for i in range(n):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', data, 8 + 20 * i)
        out[{0x01000007: 'x86_64', 0x0100000c: 'arm64'}[cpu]] = data[off:off + size]
    return out


def text_and_starts(m):
    ncmds, off = struct.unpack_from('<I', m, 16)[0], 32
    text, starts = None, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', m, off)
        if cmd == 0x19:
            for k in range(struct.unpack_from('<I', m, off + 64)[0]):
                s = off + 72 + 80 * k
                if m[s:s + 6] == b'__text':
                    addr, sz, fo = struct.unpack_from('<QQI', m, s + 32)
                    text = (addr, sz, fo)
        elif cmd == 0x26:
            fo, fs = struct.unpack_from('<II', m, off + 8)
            p, addr = fo, 0
            while p < fo + fs and m[p]:
                v = sh = 0
                while True:
                    b = m[p]; p += 1; v |= (b & 0x7f) << sh; sh += 7
                    if not b & 0x80:
                        break
                addr += v
                starts.append(addr)
        off += size
    return text, starts


def arm64_fused(m):
    (addr, size, fo), starts = text_and_starts(m)
    per = {}
    for a in range(addr, addr + size, 4):
        w = struct.unpack_from('<I', m, fo + a - addr)[0]
        hit = (w & 0xff000000 == 0x1f000000) or (w & 0xbfa0fc00 in (0x0e20cc00, 0x0ea0cc00)) or (w & 0xbf80f400 in (0x0f801000, 0x0f805000))
        if hit:
            f = max(s for s in starts if s <= a)
            per[f] = per.get(f, 0) + 1
    return per


def x86_fused(m):
    (addr, size, fo), _ = text_and_starts(m)
    with tempfile.NamedTemporaryFile(suffix='.bin') as t:
        t.write(m); t.flush()
        dis = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', f'--start-address={addr:#x}',
                              f'--stop-address={addr + size:#x}', t.name], capture_output=True, text=True, check=True).stdout
    return len(re.findall(r'\bvf(n?m(add|sub))', dis)), sorted(set(re.findall(rb'_fmaf?\x00', m)))


def main():
    data = open(sys.argv[1], 'rb').read()
    s = slices(data)
    per = arm64_fused(s['arm64'])
    vex, imports = x86_fused(s['x86_64'])
    print(f'arm64: {sum(per.values())} fused instructions in {len(per)} functions')
    for f in sorted(per, key=lambda f: -per[f])[:12]:
        print(f'  {f:#x} {per[f]}')
    for e in sys.argv[2:]:
        print(f'  named {e}: {per.get(int(e, 16), 0)}')
    print(f'x86_64: {vex} VEX FMA instructions; fma imports: {[i.decode() for i in imports]}')


if __name__ == '__main__':
    main()
