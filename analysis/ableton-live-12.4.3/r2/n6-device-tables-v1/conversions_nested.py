"""Per-parameter conversion tables for Analog, Tension and Collision and their cross-check against the
bundle-side index tables (analyst tool; output is data).

usage: python3 -I conversions_nested.py <out-dir> <h4-out-dir>

Joins out/live_index_map.tsv (index order and mapping mode, extract_nested.py) with out/constructors.tsv
(internal range, user converter, default, constructors.py) and H4's param_table.tsv (stored modal range,
Defaults-preset value) and param_tables.json (bundle kind and range). For every vector entry it derives
the range the mapping module emits (N5 module semantics; mode 5 sends its flag to the index in the
entry's high word, modes 1 and 3 to the next index) and compares it with the bundle entry at that index.
Asserts: every stored parameter has one constructor row; the user domain of its converter equals the
stored modal range; every empty vector entry receives the second output of a two-output module or is
the Tension gap. Writes out/conversions.tsv and out/crosscheck.json.
Depends on: ../n5-device-mapping-v1/conversions.py (sent(): stored value -> value on the index).
"""
import ast, csv, importlib.util, json, os, sys
sys.dont_write_bytecode = True  # do not leave __pycache__ in other packets' directories

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('n5c', os.path.join(HERE, '../n5-device-mapping-v1/conversions.py'))
n5c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n5c)
BUNDLE_KEY = {'UltraAnalog': 'Analog', 'StringStudio': 'Tension', 'Collision': 'Collision'}


def rng_of(lo, hi):
    return f'{lo:g}..{hi:g}'


def emitted(mode, arg, lo, hi):
    """Range a mapping module emits on its own index for inputs in [lo, hi] (N5 module table)."""
    if mode == 0 or mode == 8:  # mode 8 multiplies by 0.125 only while the source mode is 4 or 9
        return lo, hi
    if mode == 1:
        return 0.0, max(abs(lo), abs(hi))
    if mode == 2:
        return 0.0, hi + 1
    if mode == 3:
        return float(int(lo) >> 1), float(int(hi) >> 1)
    if mode == 4:
        return 0.0, 1.0
    if mode == 5:
        return max(lo - 1, 0.0), max(hi - 1, 0.0)
    if mode == 6:
        a, b = arg['off'] + arg['mult'] * lo, arg['off'] + arg['mult'] * hi
        return min(a, b), max(a, b)
    if mode == 7:
        return float(min(arg['table'])), float(max(arg['table']))
    raise ValueError(mode)


def verdict(kind, bmin, bmax, lo, hi):
    if kind is None:
        return 'no bundle entry'
    if kind == 0:
        bmin, bmax = 0.0, 1.0
    if bmin is None and kind != 3:
        return 'bundle range not recovered'
    if kind == 3:
        bmin = 0.0
    if abs(lo - bmin) < 1e-6 and abs(hi - bmax) < 1e-6:
        return 'exact'
    if lo >= bmin - 1e-6 and hi <= bmax + 1e-6:
        return 'within'
    return 'MISMATCH'


def parse_arg(s):
    out = {}
    for part in s.split():
        k, v = part.split('=', 1)
        out[k] = [int(x) for x in v.split(',')] if k == 'table' else float(v) if k in ('mult', 'off') else int(v)
    return out


def main(out, h4):
    idx = list(csv.DictReader(open(os.path.join(out, 'live_index_map.tsv')), delimiter='\t'))
    ctor = {}
    for r in csv.DictReader(open(os.path.join(out, 'constructors.tsv')), delimiter='\t'):
        assert (r['device'], r['name']) not in ctor, r
        ctor[(r['device'], r['name'])] = r
    stored = {(r['device'], r['path']): r for r in csv.DictReader(open(os.path.join(h4, 'param_table.tsv')), delimiter='\t')}
    bundle = json.load(open(os.path.join(h4, 'param_tables.json')))
    rows, xc = [], {}
    for dev, bkey in BUNDLE_KEY.items():
        brows = {b['index']: b for b in bundle[bkey]['rows']}
        ent = [r for r in idx if r['device'] == dev]
        second = {}  # index -> (source index, kind of flag)
        for r in ent:
            m, i = int(r['mode']), int(r['index'])
            if m in (1, 3):
                second[i + 1] = (i, f'mode {m} second output')
            if m == 5:
                second[parse_arg(r['mode_arg'])['param']] = (i, 'mode 5 flag')
        counts = {}
        for r in ent:
            i, m = int(r['index']), int(r['mode'])
            b = brows.get(i)
            bk, bmin, bmax = (b['kind'], b['min'], b['max']) if b else (None, None, None)
            row = {'device': dev, 'index': i, 'stored_name': r['name'], 'class': r['value_class'], 'stored_domain': '',
                   'user_converter': '', 'internal_range': '', 'default': '', 'default_preset': '', 'default_note': '',
                   'mode': r['mode_name'] + (f' {r["mode_arg"]}' if r['mode_arg'] else '') +
                           (f' toggle={r["second"]}' if r['second'] else ''),
                   'emitted_range': '', 'sent_for_default': '', 'bundle_kind': '' if b is None else bk,
                   'bundle_range': '' if b is None or bmin is None else rng_of(bmin, bmax),
                   'bundle_virtual': '' if b is None else b['virtual'], 'crosscheck': '', 'source': ''}
            if not r['name']:
                src = second.get(i)
                assert src or (dev == 'StringStudio' and i == 2), (dev, i)
                row['stored_name'] = f'(second output of index {src[0]}: {src[1]})' if src else '(unused index; no bundle entry)'
                row['emitted_range'] = '0..1' if src else ''
                row['crosscheck'] = verdict(bk, bmin, bmax, 0.0, 1.0) if src else ('gap: no bundle entry' if b is None else 'MISMATCH')
                rows.append(row)
                counts[row['crosscheck']] = counts.get(row['crosscheck'], 0) + 1
                continue
            c = ctor[(dev, r['name'])]
            st = stored.get((dev, r['name']))
            cls = c['cls']
            if cls in ('enum', 'bool'):
                lo, hi = 0.0, (float(int(st['range'].split('..')[1])) if cls == 'enum' else 1.0)
                dom = st['range'] if st else ''
                conv, internal, d = cls, (lo, hi), float(c['default'])
                v = n5c.sent(cls, internal, None, d)
            else:
                internal = ast.literal_eval(c['internal'])
                cv = ast.literal_eval(c['conv'])
                kindc, c0, c1 = cv
                user = (c0, c1) if kindc != 'quantizing' else internal
                dom = rng_of(*user)
                if st:
                    assert st['range'] == dom, (dev, r['name'], st['range'], dom)
                lo, hi = float(internal[0]), float(internal[1])
                conv, d = kindc, float(c['default'])
                v = n5c.sent(kindc, internal, user, d)
            arg = parse_arg(r['mode_arg']) if r['mode_arg'] else {}
            elo, ehi = emitted(m, arg, lo, hi)
            if m == 6:
                v = arg['off'] + arg['mult'] * v
            elif m == 7:
                v = float(arg['table'][int(v)])
            elif m in (1, 2, 3, 4, 5):
                v = {1: abs(v), 2: None, 3: float(int(v) >> 1), 4: float(v <= 0.5), 5: max(v - 1, 0.0)}[m]
            row.update(stored_domain=st['range'] if st else f'{dom} (not stored)',
                       user_converter=conv if conv in ('enum', 'bool') else f'{conv}({rng_of(*user)})',
                       internal_range=rng_of(lo, hi), default=f'{d:.7g}',
                       default_preset=st['default'] if st else '', emitted_range=rng_of(elo, ehi),
                       sent_for_default='' if v is None else f'{v:.6g}',
                       crosscheck=verdict(bk, bmin, bmax, elo, ehi),
                       source=f"{c['ctor']} {c['helper']}#{c['nth']} \"{c['display']}\"")
            if st and st['default'] != '':
                pv = {'true': 1.0, 'false': 0.0}.get(st['default'], None)
                pv = float(st['default']) if pv is None else pv
                row['default_note'] = 'equal' if abs(pv - d) < 1e-6 * max(1, abs(d)) else 'differs'
            rows.append(row)
            counts[row['crosscheck']] = counts.get(row['crosscheck'], 0) + 1
        in_vec = {r['name'] for r in ent} | {r['second'] for r in ent}
        for (d2, name), c in ctor.items():  # stored parameters that no vector entry carries
            st = stored.get((dev, name))
            if d2 != dev or name in in_vec or not st:
                continue
            internal, cv = ast.literal_eval(c['internal']), ast.literal_eval(c['conv'])
            assert st['range'] == rng_of(cv[1], cv[2]), (dev, name)
            rows.append({'device': dev, 'index': '', 'stored_name': name, 'class': c['value_class'],
                         'stored_domain': st['range'], 'user_converter': f'{cv[0]}({rng_of(cv[1], cv[2])})',
                         'internal_range': rng_of(*internal), 'default': f"{float(c['default']):.7g}",
                         'default_preset': st['default'],
                         'default_note': 'equal' if st['default'] != '' and abs(float(st['default']) - float(c['default'])) < 1e-6 else 'differs',
                         'mode': 'not passed to the bundle', 'emitted_range': '', 'sent_for_default': '',
                         'bundle_kind': '', 'bundle_range': '', 'bundle_virtual': '', 'crosscheck': 'not in vector',
                         'source': f"{c['ctor']} {c['helper']}#{c['nth']} \"{c['display']}\""})
        xc[dev] = {'entries': len(ent), 'bundle_entries': len(brows), 'crosscheck': counts,
                   'defaults_differing_from_preset': [r['stored_name'] for r in rows if r['device'] == dev and r['default_note'] == 'differs'],
                   'mismatches': [(r['index'], r['stored_name'], r['emitted_range'], r['bundle_kind'], r['bundle_range'])
                                  for r in rows if r['device'] == dev and r['crosscheck'] == 'MISMATCH'],
                   'within_not_exact': [(r['index'], r['stored_name'], r['emitted_range'], r['bundle_kind'], r['bundle_range'])
                                        for r in rows if r['device'] == dev and r['crosscheck'] == 'within']}
    cols = list(rows[0])
    with open(os.path.join(out, 'conversions.tsv'), 'w') as f:
        f.write('\t'.join(cols) + '\n')
        for r in rows:
            f.write('\t'.join(str(r[k]) for k in cols) + '\n')
    json.dump(xc, open(os.path.join(out, 'crosscheck.json'), 'w'), indent=1)
    print(json.dumps({d: {k: v[k] for k in ('entries', 'bundle_entries', 'crosscheck')} for d, v in xc.items()}, indent=1))


if __name__ == '__main__':
    main(*sys.argv[1:3])
