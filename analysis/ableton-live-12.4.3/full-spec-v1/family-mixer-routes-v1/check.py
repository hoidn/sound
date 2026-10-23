#!/usr/bin/env python3
"""Owned data-only integrity checks. No predecessor imports or execution."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ptr(value, path):
    for key in path.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def ledger_check(ledger, spans, basis, case_ids):
    rows = ledger['outcomes']
    assert len(rows) == len({r['id'] for r in rows}) == 104
    assert ledger['status'] == 'PENDING INDEPENDENT STRUCTURE REVIEW'
    assert {r['source_span_ref'] for r in rows} == set(spans)
    assert collections.Counter(r['route'] for r in rows) == {'X': 14, 'S': 52, 'no-established-route': 38}
    for r in rows:
        assert r['requirements'] == [r['source_span_ref']]
        assert r['predicate'] and r['missing_join']
        assert set(r['evidence_basis']) <= basis.keys() and r['evidence_basis']
        assert set(r['existing_cases']) <= case_ids
        assert r['new_actual'] is None and r['new_expected'] is None
        assert r['new_grade'] == 'unchanged / no new grade'
    by_id = {r['id']: r for r in rows}
    assert by_id['MVO-014-table']['route'] == 'S'
    assert 'off-grid0.96' in by_id['MVO-014-table']['missing_join']
    assert 'both conversions' in by_id['MVO-011-converted-floor']['missing_join']
    assert 'MV034 stays U' in by_id['MVO-011-converted-floor']['missing_join']
    assert 'A5' in by_id['MVO-011-assign-branch']['premises'][0]
    assert 'A4' in by_id['MVO-012-send-port']['premises'][0]
    assert 'A3' in by_id['MVO-011-volume-port']['premises'][0]
    assert 'not a general bound' in by_id['MVO-005-roundtrip']['missing_join']
    for i in range(7):
        row = by_id[f'MVO-014-scalar-{i}']
        assert row['route'] == 'X' and 'UNGRADED discovery' in row['missing_join']
        assert row['existing_cases'] == [f'MIXER-VALUES-{74+i:03d}']
    assert by_id['MVO-010-save']['route'] == 'no-established-route'
    assert by_id['MVO-015-alternative-range']['route'] == 'no-established-route'
    assert len(ledger['auxiliary_not_outcomes']) == 3
    assert ledger['summary']['rows'] == 104 and ledger['summary']['requirements'] == 15
    assert all(ledger['summary'][k] == 0 for k in ('new_requirements', 'new_cases', 'new_grades'))


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('read-only --check only; no write/seal/replay mode')
    here = Path(__file__).resolve().parent
    root = here.parents[3]
    load = lambda name: json.loads((here / name).read_text())
    pins = {p['id']: p for p in load('pins.json')['providers']}
    data, asof = {}, []
    for key, pin in pins.items():
        raw = (root / pin['path']).read_bytes()
        if pin['kind'] == 'immutable-provider':
            assert len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], key
            data[key] = raw
        elif sha(raw[:pin['bytes']]) == pin['sha256']:
            data[key] = raw[:pin['bytes']]
            asof.append({'id': key, 'prefix_available': True})
        else:
            asof.append({'id': key, 'prefix_available': False})
    spans = load('source-spans.json')['requirements']
    basis = load('evidence-locators.json')['locators']
    span_count, pointer_count, unavailable = 0, 0, 0

    def locator(loc):
        nonlocal span_count, pointer_count, unavailable
        assert loc['provider'] in pins
        if loc['provider'] not in data:
            unavailable += 1
            return
        raw = data[loc['provider']]
        if 'pointer' in loc:
            ptr(json.loads(raw), loc['pointer'])
            pointer_count += 1
        else:
            a, size = loc['byte_start'], loc['bytes']
            assert 0 <= a <= a+size <= len(raw)
            assert sha(raw[a:a+size]) == loc['sha256']
            lines = raw.splitlines(keepends=True)
            assert sum(map(len, lines[:loc['first_line']-1])) == a
            assert sum(map(len, lines[loc['first_line']-1:loc['last_line']])) == size
            span_count += 1

    for loc in spans.values():
        locator(loc)
    for group in basis.values():
        for loc in group:
            locator(loc)
    assert len(spans) == 15
    sets = load('input-sets.json')['sets']
    for s in sets.values():
        if 'provider' in s:
            obj = ptr(json.loads(data[s['provider']]), s['pointer'])
            if 'count' in s:
                assert len(obj) == s['count']
    cases = ptr(json.loads(data['cases']), '/cases')
    cset = sets['release-cases']
    assert [x['id'] for x in cases] == cset['record_ids']
    assert [sha(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()) for x in cases] == cset['record_sha256']
    assert collections.Counter(x['action'] for x in cases) == {'open': 37, 'compute': 43}
    ledger = load('route-ledger.json')
    ledger_check(ledger, spans, basis, set(cset['record_ids']))
    levels = json.loads(data['batch-boundaries'])
    assert len(levels) == 301 and len({r['function'] for r in levels}) == 7
    assert len({r['position_hex'] for r in levels}) == 43
    assert sum(r['historical_overlap'] for r in levels) == 49
    assert all(r['grade'] == 'ungraded-discovery' for r in levels)
    neg = [r for r in levels if r['function'] == '0x101b1a880' and r['position_hex'] == '0x1.eb851e0000000p-1']
    assert len(neg) == 1 and neg[0]['level_binary32_hex'] == 'b33bbd2e'
    # Exact input-coordinate check only; no waveform/math model is evaluated.
    n, d = float.fromhex(neg[0]['position_hex']).as_integer_ratio()
    assert n*64 % d != 0
    analysis = json.loads(data['batch-analysis'])
    assert analysis['new_distinct_boundary_evaluations'] == 252 and analysis['new_behavior_grades'] == 0
    assert analysis['historical_mismatches'] == [] and len(json.loads(data['withheld'])) == 36
    edges = load('chain-edges.json')
    assert len(edges['edges']) == 14 and len(edges['unknown_bridges']) == 6
    for edge in edges['edges']:
        assert edge['runtime_sequence_proved'] is False and edge['premises_and_unknowns']
        assert set(edge['evidence_basis'].split(',')) <= basis.keys()
    add = load('canonical-addition.json')
    old = pins['research-before']
    raw = (root / add['path']).read_bytes()
    assert add['before_sha256'] == old['sha256'] and add['before_bytes'] == old['bytes']
    assert sha(raw[:add['before_bytes']]) == add['before_sha256']
    assert raw[add['before_bytes']:add['after_bytes']] == add['append_utf8'].encode()
    assert sha(raw[:add['after_bytes']]) == add['after_sha256']
    assert sha(add['append_utf8'].encode()) == add['append_sha256']
    mutations = [
        ('MVO-014-table', 'route', 'X'),
        ('MVO-014-table', 'missing_join', 'Scalar value proves public factor'),
        ('MVO-005-roundtrip', 'missing_join', 'All gains return exactly'),
        ('MVO-011-converted-floor', 'missing_join', 'Floor stored gain directly'),
        ('MVO-011-assign-branch', 'premises', []),
        ('MVO-012-send-port', 'premises', []),
        ('MVO-011-volume-port', 'premises', []),
        ('MVO-014-scalar-5', 'missing_join', '252 graded pairs'),
        ('MVO-010-save', 'route', 'S'),
        ('MVO-001-location', 'source_span_ref', 'REQ-NOT-AN-OWNER'),
        ('MVO-001-location', 'existing_cases', ['MIXER-VALUES-999']),
        ('MVO-001-location', 'new_actual', 'pass'),
    ]
    for id, key, value in mutations:
        bad = copy.deepcopy(ledger)
        next(r for r in bad['outcomes'] if r['id'] == id)[key] = value
        try:
            ledger_check(bad, spans, basis, set(cset['record_ids']))
        except (AssertionError, IndexError, KeyError):
            continue
        raise AssertionError(('unsafe fixture accepted', id, key))
    print(json.dumps({'result': 'PASS', 'rows': 104, 'routes': ledger['summary']['routes'],
                      'requirements': 15, 'case_objects': 80, 'source_spans': span_count,
                      'json_pointers': pointer_count, 'unavailable_asof_spans': unavailable,
                      'pins': len(pins), 'negative_fixtures': len(mutations),
                      'scalar_pairs': 301, 'new_ungraded_pairs': 252, 'withheld_rows': 36,
                      'mutable_context': asof}, indent=2))


if __name__ == '__main__':
    main()
