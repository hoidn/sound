"""Locate exact NUL-terminated strings in a fat Mach-O file (static; never executes it).

usage: python3 -I find_strings.py BINARY STRINGS_FILE > out.json
STRINGS_FILE holds one exact string per line. Reports every occurrence as
(slice cpu, offset within the slice); a string with no occurrence is reported
with an empty list rather than omitted.
"""
import hashlib
import json
import struct
import sys

CPU = {0x1000007: 'x86_64', 0x100000c: 'arm64'}


def slices(data):
    magic, n = struct.unpack_from('>II', data)
    if magic != 0xcafebabe:
        raise ValueError(f'not a fat binary: {magic:#x}')
    for i in range(n):
        cpu, _, off, size, _ = struct.unpack_from('>IIIII', data, 8 + 20 * i)
        yield CPU.get(cpu, hex(cpu)), off, size


def main(binary, strings_file):
    data = open(binary, 'rb').read()
    wanted = [line.rstrip('\n') for line in open(strings_file, encoding='utf-8') if line.strip()]
    out = {'binary': binary, 'sha256': hashlib.sha256(data).hexdigest(), 'strings': {}}
    for s in wanted:
        needle = b'\0' + s.encode('utf-8') + b'\0'
        hits, pos = [], data.find(needle)
        while pos >= 0:
            for cpu, off, size in slices(data):
                if off <= pos + 1 < off + size:
                    hits.append({'cpu': cpu, 'slice_offset': hex(pos + 1 - off)})
            pos = data.find(needle, pos + 1)
        out['strings'][s] = hits
    json.dump(out, sys.stdout, indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
