#!/usr/bin/env python3
"""Byte-substring scan of each Mach-O slice of BINARY for NEEDLES (read-only).

Usage: needle_scan.py BINARY OUT.json NEEDLE...
For each fat slice (or the thin file) reports every occurrence offset (relative to
the slice) and the NUL-delimited string that contains it. Presence of a string is
not evidence that code references or executes it.
"""
import hashlib, json, struct, sys

CPU = {0x01000007: 'x86_64', 0x0100000c: 'arm64', 7: 'i386'}


def slices(data):
    if struct.unpack_from('>I', data)[0] != 0xcafebabe:
        return [('thin', 0, len(data))]
    n = struct.unpack_from('>I', data, 4)[0]
    return [(CPU.get(c, hex(c)), o, s) for c, _, o, s, _ in
            (struct.unpack_from('>IIIII', data, 8 + 20 * i) for i in range(n))]


def main(path, out, *needles):
    data = open(path, 'rb').read()
    result = {'path': path, 'sha256': hashlib.sha256(data).hexdigest(), 'slices': []}
    for arch, off, size in slices(data):
        body = data[off:off + size]
        hits = {}
        for needle in needles:
            rows, pos = [], body.find(needle.encode())
            while pos != -1 and len(rows) < 200:
                start = body.rfind(b'\0', 0, pos) + 1
                end = body.find(b'\0', pos)
                rows.append({'offset': f'0x{pos:x}', 'string': body[start:min(end, start + 300)].decode('utf-8', 'replace')})
                pos = body.find(needle.encode(), pos + 1)
            hits[needle] = rows
        result['slices'].append({'arch': arch, 'offset': off, 'size': size,
                                 'sha256': hashlib.sha256(body).hexdigest(), 'hits': hits})
    with open(out, 'w') as fh:
        json.dump(result, fh, indent=1)
        fh.write('\n')


if __name__ == '__main__':
    main(*sys.argv[1:])
