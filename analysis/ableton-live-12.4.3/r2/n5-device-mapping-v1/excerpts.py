"""Copy cited decompiled functions into the evidence directory (analyst tool; output is data).

usage: python3 -I excerpts.py <out-dir> <Corpus.bundle executable>

Writes out/live_corpus_excerpts.jsonl (Live C1 corpus records cited in notes.md but not served as
dossiers), out/corpus_bundle_excerpts.jsonl (Corpus helper corpus records) and
out/corpus_bundle_facts.json (vtable slot 0 of the class built by CreateInstanceU, the class names from
the typeinfo strings, and the ResonanceType table), read from the arm64 slice of the bundle.
Depends on /var/tmp/sound-analysis/corpus and /var/tmp/sound-analysis/helpers/Corpus/corpus.
"""
import glob, json, os, struct, sys

LIVE = ['0x103196ec0', '0x1030b54ec', '0x1030ca554', '0x1030df330', '0x1030e6104', '0x1030ec8d0',
        '0x103196dcc', '0x1031b1368', '0x102fbe07c', '0x102fbdeb4', '0x103198c00', '0x103198c80',
        '0x102fbf220', '0x102fbf19c', '0x102fbf340', '0x102fbf9a0', '0x102fbff98', '0x102fbe580',
        '0x102fcc390', '0x102fccddc', '0x102fccdf4', '0x102fccda0', '0x101e504ec', '0x102faab70',
        '0x102faabd8', '0x102faac0c', '0x102faac40', '0x102faaca8', '0x102faacf4', '0x102faad1c',
        '0x102faad38', '0x102faad58', '0x10295fec8', '0x102fa7bf0', '0x10319c4dc', '0x103197830',
        '0x103197bf8', '0x103197e1c', '0x10319285c', '0x1031980a4', '0x101575868', '0x101577e1c',
        '0x101578050', '0x101576354', '0x10157590c', '0x101577ec0', '0x1015780bc', '0x1015780d0',
        '0x101576448', '0x10157432c', '0x101568960', '0x1025856a0', '0x1015748cc', '0x1015748e8',
        '0x101574564', '0x1015745d4', '0x1026f0390', '0x1026f070c', '0x1026f18bc', '0x10213a858',
        '0x101bb4fe8', '0x1030ed054', '0x1030c50c0', '0x1030ed1cc', '0x1030ed9c0', '0x1030c4c98',
        '0x1030ed468', '0x1030ed63c', '0x10319bd08', '0x1020ef18c', '0x1020ee0f4', '0x1030c990c',
        '0x1030b4350', '0x1030df76c', '0x102fbe650', '0x1031a0358']
BUNDLE = ['0x46e4', '0x4f40', '0xc40c', '0xd75c', '0x50c0', '0xd984', '0xd98c', '0x5238', '0x5240']
ARM64_SLICE = (278528, 248624)  # offset, size of the arm64 slice (H4 out/bundles.json)


def dump(pattern, entries, path):
    want, got = set(entries), {}
    for f in sorted(glob.glob(pattern)):
        for line in open(f):
            r = json.loads(line)
            if r['entry'] in want:
                got[r['entry']] = r
    assert set(got) == want, f'missing: {want - set(got)}'
    with open(path, 'w') as f:
        for e in entries:
            f.write(json.dumps(got[e], sort_keys=True) + '\n')


def facts(exe):
    off, size = ARM64_SLICE
    d = open(exe, 'rb').read()[off:off + size]
    ptr = lambda a: struct.unpack_from('<Q', d, a)[0] & 0xFFFFFFFFF  # chained rebase target
    cstr = lambda a: d[a:a + 80].split(b'\0')[0].decode()
    out = {'slice_offset': off, 'slice_size': size}
    for vt in (0x2cb88, 0x2c090):  # the vtable FUN_0000c40c stores (0x2cb88) and its base
        ti = ptr(vt - 8)
        out[hex(vt)] = {'slots': [hex(ptr(vt + 8 * i)) for i in range(3)], 'typeinfo': hex(ti),
                        'class': cstr(ptr(ti + 8)), 'base_typeinfo': hex(ptr(ti + 16))}
    out['resonance_table_0x2a450'] = list(struct.unpack_from('<7i', d, 0x2a450))
    return out


def main(out, exe):
    dump('/var/tmp/sound-analysis/corpus/decomp/chunks/*.jsonl', LIVE, os.path.join(out, 'live_corpus_excerpts.jsonl'))
    dump('/var/tmp/sound-analysis/helpers/Corpus/corpus/decomp/chunks/*.jsonl', BUNDLE,
         os.path.join(out, 'corpus_bundle_excerpts.jsonl'))
    f = facts(exe)
    assert f['0x2cb88']['slots'][0] == '0xd75c' and f['0x2cb88']['class'] == '13CorpusWrapper', f
    json.dump(f, open(os.path.join(out, 'corpus_bundle_facts.json'), 'w'), indent=1, sort_keys=True)
    print(json.dumps(f, indent=1, sort_keys=True))


if __name__ == '__main__':
    main(*sys.argv[1:3])
