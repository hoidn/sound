"""Print raw 32-bit instruction words of a thin arm64 Mach-O for a VM range.

Usage: python3 -I insn_words.py BINARY START END
Reviewer aid for browser-index-v1 (no disassembler is installed); decoding of
the few words of interest is done by hand in the review notes.
"""
import struct, sys

def segments(data):
    magic, cpu, sub, ftype, ncmds, sizeofcmds, flags, _ = struct.unpack_from('<IiiIIIII', data, 0)
    assert magic == 0xfeedfacf, hex(magic)
    off = 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            name = data[off+8:off+24].rstrip(b'\0').decode()
            vmaddr, vmsize, fileoff, filesize = struct.unpack_from('<QQQQ', data, off+24)
            yield name, vmaddr, vmsize, fileoff, filesize
        off += size

def main(path, start, end):
    data = open(path, 'rb').read()
    for name, vm, vms, fo, fs in segments(data):
        if vm <= start < vm + fs:
            for a in range(start, end, 4):
                w, = struct.unpack_from('<I', data, fo + a - vm)
                print(f'{a:#x} {w:08x}')
            return
    sys.exit('address not in a file-backed segment')

if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16))
