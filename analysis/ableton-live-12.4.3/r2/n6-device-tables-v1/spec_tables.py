"""Build the per-device stored-parameter tables of SPEC-BUNDLED-DEVICE-PARAMETERS (analyst tool; output is data).

usage: python3 -I spec_tables.py <out-dir> <h4-out-dir>

One row per stored parameter path (H4 param_table.tsv, 502 rows): value class, stored domain (modal
MidiControllerRange, or true/false), constructor default (N6 out/constructors.tsv for UltraAnalog,
StringStudio and Collision; the SPEC rows of N5 conversions.py for the other four, plus the four Amp/Cabinet
host parameters N5 states in prose), whether the value is integer-stepped, and the shipped Defaults-preset
text where it differs. Float defaults are given as the text the N1 32-bit writer rule produces. Rows whose paths differ only in an instance number (SignalChain1/2, Envelope.0/1,
Resonator1/2, Lfo1/2, Target1/2, ...) are merged; their defaults are listed per instance when they differ.
Asserts that every stored parameter has a default. Writes <out>/spec_tables.md and <out>/spec_defaults.tsv.
"""
import collections, csv, importlib.util, os, re, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


N5C = _load('n5c', '../n5-device-mapping-v1/conversions.py')  # SPEC rows: exact constructor defaults
N1N = _load('n1n', '../n1-transport-state-v1/check_number_format.py')  # 32-bit writer rule

ORDER = ['Amp', 'Cabinet', 'UltraAnalog', 'StringStudio', 'Collision', 'LoungeLizard', 'Corpus']
CLS = {'TimeableFloat': 'Float', 'TimeableEnum': 'Enum', 'TimeableBool': 'Bool'}
# N5 page "Load handling and defaults": host parameters with constructor defaults stated in prose
N5_PROSE = {('Amp', 'DualMono'): '0', ('Amp', 'DryWet'): '1', ('Cabinet', 'DualMono'): '0', ('Cabinet', 'DryWet'): '1'}
INSTANCE = re.compile(r'(SignalChain|Resonator|Lfo|Target|Amount|Range|Envelope\.)(\d)\b')


def fmt_default(cls, v):
    v = float(v)
    if cls == 'Bool':
        return 'true' if v else 'false'
    if cls == 'Enum':
        return str(int(v))
    return N1N.fmt(N1N.f32(repr(v)), 9, 8)  # the text the N1 writer rule gives for this 32-bit value


def main(out, h4):
    stored = [r for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t')]
    dflt, step = {}, {}
    for r in csv.DictReader(open(os.path.join(out, 'constructors.tsv')), delimiter='\t'):
        dflt[(r['device'], r['name'])] = r['default']
        step[(r['device'], r['name'])] = r['conv'].startswith(("('legacyint'", "('quantizing'"))
    for sp in N5C.SPEC:
        dev, name, conv = sp[0], sp[1], sp[2]
        dflt[(dev, name)] = sp[4] if len(sp) == 7 else sp[5]
        step[(dev, name)] = conv in ('legacyint', 'quantizing')
    dflt.update(N5_PROSE)
    rows = []
    for r in stored:
        k = (r['device'], r['path'])
        assert k in dflt, k
        cls = CLS[r['class']]
        d = fmt_default(cls, dflt[k])
        pre = r['default']
        pre = '' if pre == '' else pre if cls == 'Float' else fmt_default(cls, {'true': 1, 'false': 0}.get(pre, pre))
        rows.append({'device': r['device'], 'path': r['path'], 'class': cls,
                     'domain': 'true/false' if cls == 'Bool' else r['range'],
                     'step': 'integer' if step.get(k) else '', 'default': d,
                     'preset': pre, 'preset_differs': pre != '' and pre != d})
    with open(os.path.join(out, 'spec_defaults.tsv'), 'w') as f:
        cols = list(rows[0])
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r[c]) for c in cols) + '\n')
    md = []
    for dev in ORDER:
        groups = collections.OrderedDict()
        for r in (r for r in rows if r['device'] == dev):
            key = (INSTANCE.sub(lambda m: m.group(1) + '{n}', r['path']), r['class'], r['domain'], r['step'])
            groups.setdefault(key, []).append(r)
        md.append(f'#### `{dev}`\n')
        md.append('| Path below the device element | Class | Stored domain | Default when absent | Defaults preset (where different) |')
        md.append('| --- | --- | --- | --- | --- |')
        for (path, cls, dom, st), rs in groups.items():
            insts = [INSTANCE.findall(r['path']) for r in rs]
            if len(rs) > 1:
                insts = [tuple(n for _, n in INSTANCE.findall(r['path'])) for r in rs]
                p = path
                for j in range(len(insts[0])):
                    p = p.replace('{n}', '{' + ','.join(sorted({i[j] for i in insts})) + '}', 1)
                labels = ['/'.join(i) for i in insts]
                ds = [r['default'] for r in rs]
                d = ds[0] if len(set(ds)) == 1 else '; '.join(f'{l}: {v}' for l, v in zip(labels, ds))
                pre = '; '.join(f'{l}: {r["preset"]}' for l, r in zip(labels, rs) if r['preset_differs'])
            else:
                p, d, pre = rs[0]['path'], rs[0]['default'], rs[0]['preset'] if rs[0]['preset_differs'] else ''
            dom_txt = dom + (', integer steps' if st else '')
            md.append(f'| `{p}` | {cls} | {dom_txt} | {d} | {pre} |')
        md.append('')
    open(os.path.join(out, 'spec_tables.md'), 'w').write('\n'.join(md))
    c = collections.Counter(r['device'] for r in rows)
    print({d: (c[d], sum(1 for r in rows if r['device'] == d and r['preset_differs'])) for d in ORDER})


if __name__ == '__main__':
    main(*sys.argv[1:3])
