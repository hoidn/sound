"""N3 evidence extractor (analyst-only). Copies exact corpus records and reads fixed data words.

Usage: python3 -I extract.py <out-dir>
Reads (never writes): the Live arm64 corpus/indexes, the Engine x86_64 helper corpus/indexes and
the pinned Live arm64 slice. Writes live-functions.jsonl, engine-functions.jsonl, binary-reads.json,
atransport-members.json and engine-vtables.jsonl into <out-dir>. Output order is fixed, so a rerun
on unchanged inputs reproduces identical bytes. Stdlib only.
"""
import hashlib, json, os, re, struct, sys

LIVE_CORPUS = '/var/tmp/sound-analysis/corpus'
ENGINE_CORPUS = '/var/tmp/sound-analysis/helpers/Ableton_Live_Engine_x86_64/corpus'
LIVE_SLICE = '/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/derived/Live.arm64'
LIVE_SHA256 = '3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'

LIVE_FUNCS = """
0x101a4abd8 0x101ab7348 0x101ab7898 0x101ab786c 0x101a524b8 0x101a4ac8c 0x101a4adec 0x101a4af58
0x101a48488 0x101a4abac 0x101a4abb4 0x101a4b1d0 0x101a4b74c 0x101a4c224 0x101a4c2dc 0x101a4c38c
0x101a4a3b4 0x101a522c8 0x101a4a4d4 0x101a3d6d8 0x101a3d638 0x101a3d7d0 0x101a50bd4 0x101a8effc
0x101a44064 0x1026baa70 0x1026ba140 0x102332b5c 0x102332e08
0x10276a7b0 0x102767b70 0x102767a70 0x102767a7c 0x10276b2a0 0x10276b30c 0x10276b370 0x10276c538
0x10276a4f0 0x102769868 0x1027686f4 0x10275dc64 0x10275dccc 0x102760d88 0x10276d678 0x10276d80c
0x10276d814 0x10276e5d4 0x10276e79c 0x102767f74 0x10276933c 0x102768640 0x102769480 0x10276b900
0x102336410 0x1026de350
0x1015643d8 0x1015644d4 0x1015645a0 0x1015645e4 0x1015646f4 0x10156a5f8 0x101564728 0x101564768
0x10155e028
""".split()

ENGINE_FUNCS = """
0x9fbf0 0x9fc90 0x9fdc0 0x9ff20 0xa7a30 0xa6110 0xe68d0 0x110d30 0x111350 0x111300 0x9ce70 0x9fbb0
0x9fbc0 0xa0160 0xa0710 0xa1180 0xa1260 0xa01f0 0xa1250 0x9f390 0x9f410 0xa7840 0x9f4c0 0x91b90
0x91af0 0x91c80 0xa9920 0x98ea0 0xa0070 0xa0210 0x9fb60 0x99df0 0xa1310
""".split()

# (label, vtable address point) whose RTTI name and selected slots are read from the slice.
VTABLES = [('OSendThreadMessage', 0x106756188, [0x0, 0x8, 0x10]),
           ('ARemoteableBool', 0x10667d2c8, [0x248]),
           ('ALoopOn', 0x106803d50, [0x248]),
           ('ACurrentTime', 0x106803378, [0x248])]
SYMBOL_RANGE = (0x102770a30, 0x102770a80)


def extract_records(chunks, entries):
    want, found = set(entries), {}
    for name in sorted(os.listdir(chunks)):
        with open(os.path.join(chunks, name), 'rb') as fh:
            for line in fh:
                entry = re.match(rb'\{"entry":"([^"]+)"', line).group(1).decode()
                if entry in want:
                    found[entry] = line
    missing = want - found.keys()
    if missing:
        raise SystemExit('missing corpus records: ' + ' '.join(sorted(missing)))
    return b''.join(found[e] for e in sorted(found, key=lambda a: int(a, 16)))


def segments(d):
    ncmds, off, segs = struct.unpack_from('<I', d, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', d, off)
        if cmd == 0x19:
            vm, vms, fo, fs = struct.unpack_from('<QQQQ', d, off + 24)
            segs.append((vm, fo, fs))
        off += size
    return segs


def reader(d):
    segs = segments(d)

    def v2o(va):
        for vm, fo, fs in segs:
            if vm <= va < vm + fs:
                return fo + va - vm
        raise ValueError(hex(va))

    def word(va):
        return struct.unpack_from('<Q', d, v2o(va))[0]

    def cstr(va):
        o = v2o(va)
        return d[o:d.index(b'\0', o)].decode('latin1')
    return word, cstr


def symbols_in(d, lo, hi):
    ncmds, off, out = struct.unpack_from('<I', d, 16)[0], 32, []
    for _ in range(ncmds):
        cmd, size = struct.unpack_from('<II', d, off)
        if cmd == 2:
            symoff, nsyms, stroff, _ = struct.unpack_from('<IIII', d, off + 8)
            for i in range(nsyms):
                strx, ntype, _, _, value = struct.unpack_from('<IBBHQ', d, symoff + 16 * i)
                if lo <= value < hi:
                    e = d.index(b'\0', stroff + strx)
                    out.append({'address': hex(value), 'n_type': hex(ntype),
                                'name': d[stroff + strx:e].decode('latin1')})
        off += size
    return sorted(out, key=lambda r: (int(r['address'], 16), r['name']))


def main(out):
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'live-functions.jsonl'), 'wb') as fh:
        fh.write(extract_records(os.path.join(LIVE_CORPUS, 'decomp/chunks'), LIVE_FUNCS))
    with open(os.path.join(out, 'engine-functions.jsonl'), 'wb') as fh:
        fh.write(extract_records(os.path.join(ENGINE_CORPUS, 'decomp/chunks'), ENGINE_FUNCS))
    with open(os.path.join(ENGINE_CORPUS, 'indexes/vtables.jsonl'), 'rb') as src, \
            open(os.path.join(out, 'engine-vtables.jsonl'), 'wb') as dst:
        dst.write(b''.join(l for l in src if b'OSendThreadMessage::vtable' in l))

    d = open(LIVE_SLICE, 'rb').read()
    digest = hashlib.sha256(d).hexdigest()
    if digest != LIVE_SHA256:
        raise SystemExit('unexpected slice digest ' + digest)
    word, cstr = reader(d)
    vtables = []
    for label, vt, slots in VTABLES:
        ti = word(vt - 8)
        vtables.append({'label': label, 'address_point': hex(vt), 'typeinfo': hex(ti),
                        'rtti_name': cstr(word(ti + 8) & 0x7fffffffffffffff),
                        'slots': {hex(s): hex(word(vt + s)) for s in slots}})
    reads = {'slice': LIVE_SLICE, 'sha256': digest,
             'note': 'LC_DYLD_INFO_ONLY image: rebased pointers are stored as unslid vmaddrs',
             'vtables': vtables,
             'symbols': symbols_in(d, *SYMBOL_RANGE)}
    with open(os.path.join(out, 'binary-reads.json'), 'w') as fh:
        json.dump(reads, fh, indent=1, sort_keys=True)
        fh.write('\n')

    # ATransport member reflection table: (descriptor offset, UTF-16 member name).
    code = next(json.loads(l)['code'] for l in open(os.path.join(out, 'live-functions.jsonl'))
                if l.startswith('{"entry":"0x10275dccc"'))
    rows = re.findall(r'&DAT_106e53680,0xffffffff,0xffffffff,(0x[0-9a-f]+|\d+),\s*L"(\w+)"', code)
    members = [{'descriptor_offset': hex(int(o, 0)), 'pointer_offset': hex(int(o, 0) + 8), 'member': n}
               for o, n in sorted(rows, key=lambda r: int(r[0], 0))]
    with open(os.path.join(out, 'atransport-members.json'), 'w') as fh:
        json.dump({'source_function': '0x10275dccc', 'count': len(members), 'members': members},
                  fh, indent=1)
        fh.write('\n')


if __name__ == '__main__':
    main(sys.argv[1])
