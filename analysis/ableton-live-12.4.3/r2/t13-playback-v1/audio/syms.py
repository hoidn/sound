"""Print Mach-O nlist symbols (value, name) whose name matches a regex (read-only; output is data).
usage: python3 -I syms.py <slice> <regex>      (names are printed mangled; pipe through c++filt to demangle)
"""
import re, struct, sys


def main():
    path, rx = sys.argv[1], re.compile(sys.argv[2])
    b = open(path, 'rb').read()
    ncmds, off = struct.unpack_from('<I', b, 16)[0], 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', b, off)
        if cmd == 0x2:
            symoff, nsyms, stroff, _ = struct.unpack_from('<IIII', b, off + 8)
            for k in range(nsyms):
                strx, typ, sect, desc, val = struct.unpack_from('<IBBHQ', b, symoff + 16 * k)
                name = b[stroff + strx:b.index(b'\0', stroff + strx)].decode('latin-1')
                if rx.search(name) and not typ & 0xe0:
                    print(f'{val:#x} {typ:#04x} {name}')
        off += size


if __name__ == '__main__':
    main()
