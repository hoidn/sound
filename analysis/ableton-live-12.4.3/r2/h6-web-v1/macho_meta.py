"""Static Mach-O identity reader for packet H6 (never executes the input).

For each fat-binary slice: CPU, load-dylib list, LC_BUILD_VERSION, the
__TEXT,__info_plist section, and the code-signature identifier, team ID and
embedded entitlements plist.

usage: python3 -I macho_meta.py FILE... > out.json
"""
import hashlib
import json
import struct
import sys

CPU = {0x1000007: 'x86_64', 0x100000c: 'arm64'}
LC_SEGMENT_64, LC_LOAD_DYLIB, LC_CODE_SIGNATURE, LC_BUILD_VERSION = 0x19, 0xc, 0x1d, 0x32
LC_LOAD_WEAK_DYLIB, LC_REEXPORT_DYLIB = 0x80000018, 0x8000001f


def cstr(b):
    return b.split(b'\0', 1)[0].decode('utf-8', 'replace')


def ver(v):
    return f'{v >> 16}.{(v >> 8) & 0xff}.{v & 0xff}'


def code_signature(blob):
    out = {}
    magic, _, count = struct.unpack_from('>III', blob)
    if magic != 0xfade0cc0:
        raise ValueError(f'unexpected SuperBlob magic {magic:#x}')
    for i in range(count):
        slot, off = struct.unpack_from('>II', blob, 12 + 8 * i)
        bmagic, blen = struct.unpack_from('>II', blob, off)
        body = blob[off:off + blen]
        if bmagic == 0xfade0c02:  # CodeDirectory
            version, flags, _, ident_off = struct.unpack_from('>IIII', body, 8)
            out.setdefault('code_directories', []).append({
                'slot': slot, 'version': hex(version), 'flags': hex(flags),
                'identifier': cstr(body[ident_off:]),
                'team_id': cstr(body[struct.unpack_from('>I', body, 48)[0]:]) if version >= 0x20200 else None})
        elif bmagic == 0xfade7171:  # entitlements plist
            out['entitlements_xml'] = body[8:].decode('utf-8', 'replace')
    return out


def slice_meta(d):
    magic, cpu, _, _, ncmds, _, flags, _ = struct.unpack_from('<8I', d)
    if magic != 0xfeedfacf:
        raise ValueError(f'not a 64-bit Mach-O slice: {magic:#x}')
    meta = {'cpu': CPU.get(cpu, hex(cpu)), 'flags': hex(flags), 'dylibs': []}
    off = 32
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', d, off)
        if cmd in (LC_LOAD_DYLIB, LC_LOAD_WEAK_DYLIB, LC_REEXPORT_DYLIB):
            meta['dylibs'].append(cstr(d[off + struct.unpack_from('<I', d, off + 8)[0]:off + size]))
        elif cmd == LC_BUILD_VERSION:
            platform, minos, sdk = struct.unpack_from('<III', d, off + 8)
            meta['build_version'] = {'platform': platform, 'minos': ver(minos), 'sdk': ver(sdk)}
        elif cmd == LC_CODE_SIGNATURE:
            dataoff, datasize = struct.unpack_from('<II', d, off + 8)
            meta['code_signature'] = code_signature(d[dataoff:dataoff + datasize])
        elif cmd == LC_SEGMENT_64:
            nsects = struct.unpack_from('<I', d, off + 64)[0]
            for k in range(nsects):
                s = off + 72 + 80 * k
                sect, seg = cstr(d[s:s + 16]), cstr(d[s + 16:s + 32])
                if (seg, sect) == ('__TEXT', '__info_plist'):
                    size_, foff = struct.unpack_from('<Q', d, s + 40)[0], struct.unpack_from('<I', d, s + 48)[0]
                    meta['info_plist_xml'] = d[foff:foff + size_].decode('utf-8', 'replace')
        off += size
    return meta


def main(paths):
    report = []
    for p in paths:
        data = open(p, 'rb').read()
        entry = {'path': p, 'sha256': hashlib.sha256(data).hexdigest(), 'size': len(data), 'slices': []}
        magic, n = struct.unpack_from('>II', data)
        if magic != 0xcafebabe:
            raise ValueError(f'{p}: not a fat binary ({magic:#x})')
        for i in range(n):
            _, _, off, size, _ = struct.unpack_from('>IIIII', data, 8 + 20 * i)
            s = data[off:off + size]
            m = slice_meta(s)
            m.update(offset=off, size=size, sha256=hashlib.sha256(s).hexdigest())
            entry['slices'].append(m)
        report.append(entry)
    json.dump(report, sys.stdout, indent=1, sort_keys=True)


if __name__ == '__main__':
    main(sys.argv[1:])
