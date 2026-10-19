"""Decode the floating-point and a few integer instructions of the thin arm64 Live slice in a VA range
(analyst tool; read-only; output is data). Copied from handoff-staging/clip-launch-v1-analysis/fp_opcodes.py
and extended with fcvtps/fcvtms/fcvtns, ldp d and scalar scvtf, register fields, ldr/str d immediates and fmadd operands.
usage: python3 -I a64.py <slice> <start_va_hex> <count>
"""
import struct, sys
path, va, n = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])
b = open(path, 'rb').read()
ncmds = struct.unpack_from('<I', b, 16)[0]
off, segs = 32, []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19:
        vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', b, off + 24)
        segs.append((vmaddr, fileoff, filesize))
    off += size
fo = next(f + va - vm for vm, f, fs in segs if vm <= va < vm + fs)
R = lambda w, s: (w >> s) & 31
PAT = [(0xFFFFFC00, 0x1E664000, 'frinta d'), (0xFFFFFC00, 0x1E644000, 'frintn d'), (0xFFFFFC00, 0x1E65C000, 'frintz d'),
       (0xFFFFFC00, 0x1E64C000, 'frintp d'), (0xFFFFFC00, 0x1E654000, 'frintm d'),
       (0xFFFFFC00, 0x9E780000, 'fcvtzs x,d'), (0xFFFFFC00, 0x1E780000, 'fcvtzs w,d'), (0xFFFFFC00, 0x9E640000, 'fcvtas x,d'),
       (0xFFFFFC00, 0x9E680000, 'fcvtps x,d'), (0xFFFFFC00, 0x1E680000, 'fcvtps w,d'), (0xFFFFFC00, 0x9E700000, 'fcvtms x,d'),
       (0xFFFFFC00, 0x9E600000, 'fcvtns x,d'), (0xFFFFFC00, 0x9E620000, 'scvtf d,x'), (0xFFFFFC00, 0x1E620000, 'scvtf d,w'),
       (0xFFFFFC00, 0x1E22C000, 'fcvt d,s'), (0xFFFFFC00, 0x1E624000, 'fcvt s,d'),
       (0xFFE0FC00, 0x1E600800, 'fmul d'), (0xFFE0FC00, 0x1E602800, 'fadd d'), (0xFFE0FC00, 0x1E601800, 'fdiv d'),
       (0xFFE0FC00, 0x1E603800, 'fsub d'), (0xFFFFFC00, 0x1E60C000, 'fabs d'), (0xFFE08000, 0x1F400000, 'fmadd d'),
       (0xFFE08000, 0x1F408000, 'fmsub d'), (0xFFE08000, 0x1F600000, 'fnmadd d'), (0xFFE08000, 0x1F608000, 'fnmsub d'),
       (0xFFFFFC00, 0x1E604000, 'fmov d,d'), (0xFFE0FC1F, 0x1E602000, 'fcmp d'), (0xFFC00000, 0xFD400000, 'ldr d,[x,#]'),
       (0xFFC00000, 0xFD000000, 'str d,[x,#]'), (0xFFC00000, 0xF9400000, 'ldr x,[x,#]'), (0xFFC00000, 0xBD400000, 'ldr s,[x,#]'),
       (0xFFC00000, 0x6D400000, 'ldp d,d,[x,#]'), (0xFFFFFC00, 0x5E61D800, 'scvtf d,d (int in fp reg)'),
       (0xFFE0FC00, 0xCB000000, 'sub x'), (0xFFE0FC00, 0x8B000000, 'add x'), (0xFC000000, 0x94000000, 'bl'),
       (0xFFFFFC1F, 0xD65F0000, 'ret'), (0xFF000000, 0x1E000000, 'other fp')]
for i in range(n):
    a = va + 4 * i
    w = struct.unpack_from('<I', b, fo + 4 * i)[0]
    name = next((nm for m, p, nm in PAT if w & m == p), '')
    ops = ''
    if name.startswith(('fmadd', 'fmsub', 'fnm')):
        ops = f'd{R(w,0)} = d{R(w,5)}*d{R(w,16)} +- d{R(w,10)}'
    elif name.startswith(('ldr d', 'str d', 'ldr x')):
        ops = f'{"dx"[name[4] == "x"] if name.startswith("ldr") else "d"}{R(w,0)}, [x{R(w,5)}, #{((w >> 10) & 0xfff) * 8:#x}]'
    elif name.startswith('ldp d'):
        imm = (w >> 15) & 0x7f
        imm -= 128 if imm >> 6 else 0
        ops = f'd{R(w,0)}, d{R(w,10)}, [x{R(w,5)}, #{imm * 8:#x}]'
    elif name.startswith('ldr s'):
        ops = f's{R(w,0)}, [x{R(w,5)}, #{((w >> 10) & 0xfff) * 4:#x}]'
    elif name.startswith(('fmul', 'fadd', 'fdiv', 'fsub', 'sub x', 'add x')):
        ops = f'{R(w,0)} = {R(w,5)} op {R(w,16)}'
    elif name.startswith(('frint', 'fcvt', 'scvtf', 'fabs', 'fmov')):  # noqa: E501
        ops = f'{R(w,0)} <- {R(w,5)}'
    elif name == 'bl':
        o = w & 0x3ffffff
        o -= (1 << 26) if o >> 25 else 0
        ops = f'{a + 4 * o:#x}'
    print(f'{a:#x} {w:08x} {name} {ops}')
