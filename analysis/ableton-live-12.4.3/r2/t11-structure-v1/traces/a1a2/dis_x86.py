"""objdump ranges of the x86_64 Live slice (read-only; output is data).
usage: python3 -I dis_x86.py <slice> <lo:hi[:label]>..."""
import struct, subprocess, sys
S = sys.argv[1]
b = open(S, 'rb').read()
ncmds, off = struct.unpack_from('<I', b, 16)[0], 32
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', b, off)
    if cmd == 0x19 and b[off + 8:off + 24].rstrip(b'\0') == b'__TEXT':
        vm, _, fo, _ = struct.unpack_from('<QQQQ', b, off + 24)
    off += size
for spec in sys.argv[2:]:
    lo, hi, *label = spec.split(':')
    print(f'### {lo} .. {hi}' + (f' ({label[0]})' if label else ''))
    out = subprocess.run(['objdump', '-D', '-b', 'binary', '-m', 'i386:x86-64', f'--adjust-vma={vm - fo:#x}',
                          f'--start-address={lo}', f'--stop-address={hi}', S], capture_output=True, text=True).stdout
    print('\n'.join(l for l in out.splitlines() if l.startswith('   1')))
