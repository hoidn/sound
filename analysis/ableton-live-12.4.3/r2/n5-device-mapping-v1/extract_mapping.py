"""Derive the Live-side SetParameterA index table for one device class (analyst tool; output is data).

usage: python3 -I extract_mapping.py <out-dir> <h4-out-dir>

For each device it reads, from the C1 Live corpus (decompiled text, not Ghidra), the
member registration function (offset -> L"mpName" and value-class getter) and the
parameter-vector builder found at vtable slot +0x5a0. The builder pushes one 0x38-byte
entry per SetParameterA index, in order. Each push has one out-of-line call
FUN_x(param_1,param_2 + OFF[,...]) whose OFF is the member; the inline fast path for
the same entry writes entry[2] (mode in the low 32 bits) and entry[3]. The table is
cross-checked against the bundle-side index table recovered by packet H4
(param_tables.json) and the stored ranges in param_table.tsv.
Depends on: /var/tmp/sound-analysis/corpus/decomp/chunks/*.jsonl; H4 out/ files.
Limitation: regex over decompiler text; only flat builders (Amp, Cabinet, Electric, Corpus).
"""
import json, re, sys, glob, csv, os

CHUNKS = '/var/tmp/sound-analysis/corpus/decomp/chunks/*.jsonl'
DEVICES = {  # xml element: (h4 key, registration fn, builder fn)
    'Amp': (None, '0x1030b4350', '0x1030b5220'),
    'Cabinet': (None, '0x1030c990c', '0x1030ca45c'),
    'LoungeLizard': ('Electric', '0x1030e7f80', '0x1030ebe78'),
    'Corpus': ('Corpus', '0x1030df76c', '0x1030e54e8'),
}
VALUE_CLASS = {'FUN_1026f01e8': 'TimeableFloat', 'FUN_1026ee86c': 'TimeableEnum',
               'FUN_1026eb790': 'TimeableBool', 'FUN_1026ebbac': 'TimeableBool'}
# Helper -> default mode it writes (low 32 bits of entry[2]); see notes.md "push helpers".
HELPER_MODE = {'FUN_1030c50c0': 0, 'FUN_1030ed054': 0, 'FUN_1030ed1cc': 0,
               'FUN_1030c4c98': 7, 'FUN_1030ed468': 7, 'FUN_1030ed9c0': 6}
MODE_NAME = {0: 'IndexedFloat (identity)', 1: 'ModulationPolarizer', 2: 'ToggleMapping',
             3: 'FilterType', 4: 'BoolInverter', 5: 'ToToggleMapping', 6: 'MultiplyOffset',
             7: 'IntegerMapping (table)', 8: 'CollisionScaledMode'}


def load(entries):
    want, out = set(entries), {}
    for f in sorted(glob.glob(CHUNKS)):
        for line in open(f):
            if any(f'"entry":"{e}"' in line for e in want - set(out)):
                r = json.loads(line)
                if r['entry'] in want:
                    out[r['entry']] = r['code']
        if len(out) == len(want):
            break
    missing = want - set(out)
    assert not missing, f'functions not in corpus: {missing}'
    return out


def registration(code):
    rx = re.compile(r'(FUN_[0-9a-f]+)\(\);\s*local_30\[0\][\s\S]*?FUN_10147e954\(&DAT_[0-9a-f]+,'
                    r'0xffffffff,0xffffffff,(0x[0-9a-f]+|\d+),\s*L"(\w+)"')
    return {int(o, 0): (n[2:], VALUE_CLASS.get(t, t)) for t, o, n in rx.findall(code)}


def builder(code):
    calls = [(f, int(o, 0)) for f, o in
             re.findall(r'(FUN_[0-9a-f]+)\(param_1,param_2 \+ (0x[0-9a-f]+|\d+)[,)]', code)]
    # inline fast-path fields, keyed by member offset (fast path reads member + 8)
    inline = {}
    for m in re.finditer(r'\*puVar1 = \*\(undefined8 \*\)\(param_2 \+ (0x[0-9a-f]+|\d+)\);([\s\S]*?)'
                         r'puVar1\[2\] = ([^;]+);', code):
        inline[int(m.group(1), 0) - 8] = m.group(3).strip()
    rows = []
    for i, (helper, off) in enumerate(calls):
        mode = HELPER_MODE.get(helper)
        f2 = inline.get(off)
        if f2 == '0x8000000000000000':
            mode = 0 if mode is None else mode
        elif f2 == 'DAT_1055d1ec0':
            mode = 6
        elif f2 == 'DAT_1055d1ed0':
            mode = 7
        rows.append({'index': i, 'member': hex(off), 'helper': helper, 'entry2': f2, 'mode': mode})
    return rows


def main(out_dir, h4):
    table = {}
    for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t'):
        table[(r['device'], r['path'])] = r
    bundle = json.load(open(os.path.join(h4, 'param_tables.json')))
    fns = [x for d in DEVICES.values() for x in d[1:] if x]
    code = load(fns)
    result, summary = [], {}
    for dev, (h4key, reg, bld) in DEVICES.items():
        names = registration(code[reg]) if reg else {}
        rows = builder(code[bld])
        brows = {b['index']: b for b in bundle[h4key]['rows']} if h4key else {}
        agree = 0
        for r in rows:
            name, cls = names.get(int(r['member'], 16), (None, None))
            st = table.get((dev, name)) if name else None
            b = brows.get(r['index'])
            r.update(device=dev, name=name, value_class=cls, mode_name=MODE_NAME.get(r['mode']),
                     stored_range=st['range'] if st else None, schema_param=bool(st),
                     bundle_kind=b['kind'] if b else None,
                     bundle_range=f"{b['min']:g}..{b['max']:g}" if b and b['min'] is not None else None)
            # integer-kind cross-check: enum/bool <-> bundle kind 3 with equal max (Corpus) or kind 2/3 (Electric)
            if b and st and cls in ('TimeableEnum', 'TimeableBool') and b['kind'] in (2, 3):
                agree += 1
            result.append(r)
        stored = [n for n, c in names.values() if (dev, n) in table]
        summary[dev] = {'builder': bld, 'registration': reg, 'entries': len(rows),
                        'bundle_entries': len(brows) or None,
                        'schema_params': len([k for k in table if k[0] == dev]),
                        'schema_params_in_vector': len({r['name'] for r in rows if r['schema_param']}),
                        'schema_params_not_in_vector': sorted(
                            k[1] for k in table if k[0] == dev and k[1] not in {r['name'] for r in rows}),
                        'enum_or_bool_on_integer_bundle_kind': agree}
    with open(os.path.join(out_dir, 'live_index_map.tsv'), 'w') as f:
        cols = ['device', 'index', 'name', 'member', 'value_class', 'helper', 'entry2', 'mode',
                'mode_name', 'stored_range', 'schema_param', 'bundle_kind', 'bundle_range']
        f.write('\t'.join(cols) + '\n')
        for r in result:
            f.write('\t'.join('' if r.get(c) is None else str(r.get(c)) for c in cols) + '\n')
    json.dump(summary, open(os.path.join(out_dir, 'live_index_summary.json'), 'w'), indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == '__main__':
    main(*sys.argv[1:3])
