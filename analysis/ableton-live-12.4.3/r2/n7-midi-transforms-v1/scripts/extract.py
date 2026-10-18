"""extract.py OUTDIR APP LIVE_ARM64 CORPUS_CHUNKS
Reproduce N7 static extracts (read-only; nothing from the bundle is executed):
  OUTDIR/corpus-excerpts.jsonl  decompiler text of every cited function not covered by a kept dossier
  OUTDIR/native-constants.json  acceleration tables and other constants read from Live.arm64
  OUTDIR/onoff-thresholds.json  MidiCCOnOffThresholds Min/Max pairs in the shipped .als sets
"""
import sys, os, json, glob, gzip, re, struct, hashlib, collections

out, app, live, chunks = sys.argv[1:5]
EXCERPTS = [  # entry -> role (see ../notes.md)
    ('0x103b4ca90', 'Python MidiMap module registration: MapMode enum values, map_midi_cc_with_feedback_map signature'),
    ('0x101b842cc', 'static init: acceleration tables (vectors at 0x106fba2a8 and 0x106fba2c0)'),
    ('0x101b7bbcc', 'decoder helper'), ('0x101b7f2d4', 'CC receiver constructor'),
    ('0x101b7fc28', '14-bit receiver constructor'), ('0x101b7fc74', '14-bit receiver init (avoid flag at +0x44)'),
    ('0x101b7c16c', 'TTimeableDetails kind/range packer'), ('0x101b7c214', 'TTimeableDetails constructor (Zoom at +0x1c)'),
    ('0x101b7c70c', 'OChangeControllerDataCommand and OSetMidiTakeOverMode field registration'),
    ('0x1026f3290', 'class registration ATimeableBool/Enum/Float'),
    ('0x1026eb938', 'ATimeableBool members incl. mpMidiCCOnOffThresholds'),
    ('0x1026f0200', 'class id ATimeableFloat'), ('0x1026eb7a8', 'class id ATimeableBool'), ('0x1026ee884', 'class id ATimeableEnum'),
    ('0x1011afc2c', 'controller maximum (127 / 8191)'), ('0x1011aeb80', 'registry lookup gating the threshold flag'),
    ('0x101b65588', 'prior-value table read with -129 default'), ('0x101b6569c', 'prior-value table init (-129 pattern)'),
    ('0x101b65c1c', 'prior-value table reset'),
    ('0x1022df424', 'takeover preference UI entries (None, Pick-Up, Value Scaling)'),
    ('0x103afd98c', 'Python DeviceParameter bindings: is_quantized/min/max'),
    ('0x103afe2cc', 'is_quantized getter (vtable +0x2e0)'), ('0x103afe3c0', 'min getter (vtable +0x2f0)'),
    ('0x103afe3d0', 'max getter (vtable +0x2f8)'), ('0x101ab9f78', 'handler registry store'), ('0x101ab9f5c', 'handler registry slot'),
]
want = {e: r for e, r in EXCERPTS}
with open(os.path.join(out, 'corpus-excerpts.jsonl'), 'w') as o:
    found = {}
    for p in sorted(glob.glob(os.path.join(chunks, 'chunk-*.jsonl'))):
        with open(p) as f:
            for line in f:
                if '"entry":"0x' not in line[:40]: continue
                r = json.loads(line)
                if r['entry'] in want:
                    found[r['entry']] = {'entry': r['entry'], 'name': r['name'], 'state': r['state'],
                                         'role': want[r['entry']], 'chunk': os.path.basename(p),
                                         'code_sha256': r.get('code_sha256'), 'code': r.get('code')}
    missing = sorted(set(want) - set(found))
    assert not missing, missing
    for e, _ in EXCERPTS: o.write(json.dumps(found[e]) + '\n')

data = open(live, 'rb').read()
ncmds = struct.unpack_from('<I', data, 16)[0]; off = 32; segs = []
for _ in range(ncmds):
    cmd, size = struct.unpack_from('<II', data, off)
    if cmd == 0x19:
        vm, vs, fo, fs = struct.unpack_from('<QQQQ', data, off + 24); segs.append((vm, fo, fs))
    off += size
def f32(va, n):
    for vm, fo, fs in segs:
        if vm <= va < vm + fs: return list(struct.unpack_from('<%df' % n, data, fo + va - vm))
    raise SystemExit('unmapped %x' % va)
consts = {
    'live_arm64_sha256': hashlib.sha256(data).hexdigest(),
    'table_B_0x10584a580_modes_2_3_4': f32(0x10584a580, 8),
    'table_A_0x10584a5a0_mode_1_first8': f32(0x10584a5a0, 8),
    'table_A_ninth_element_stored_by_0x101b842cc': 50.0,
    'fourteen_bit_divisor_0x10584a8b4': f32(0x10584a8b4, 1)[0],
    'prior_fill_pattern_0x105849f70': f32(0x105849f70, 4),
}
json.dump(consts, open(os.path.join(out, 'native-constants.json'), 'w'), indent=1)

sets = sorted(p for p in glob.glob(os.path.join(app, 'Contents/App-Resources/**/*.als'), recursive=True)
              if not os.path.basename(p).startswith('._'))
pat = re.compile(r'<MidiCCOnOffThresholds>\s*<Min Value="([^"]*)"\s*/>\s*<Max Value="([^"]*)"\s*/>')
cnt = collections.Counter(); files = []
for p in sets:
    raw = open(p, 'rb').read()
    try: x = gzip.decompress(raw).decode('utf-8', 'replace')
    except OSError: continue
    c = collections.Counter(m.groups() for m in pat.finditer(x)); cnt.update(c)
    files.append({'path': os.path.relpath(p, app), 'sha256': hashlib.sha256(raw).hexdigest(), 'occurrences': sum(c.values())})
json.dump({'sets_parsed': len(files), 'pairs': [{'min': a, 'max': b, 'count': n} for (a, b), n in cnt.most_common()],
           'files': files}, open(os.path.join(out, 'onoff-thresholds.json'), 'w'), indent=1)
print('ok', len(found), len(files))
