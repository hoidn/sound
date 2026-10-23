#!/usr/bin/env python3
"""Read-only author-as-of JSON/text/identity checks; no predecessor code imports."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pointer(value, path):
    for key in path.split('/')[1:]:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def check_ledger(ledger, spans, locators, sets, cases):
    rows = ledger['outcomes']
    ids = {r['id'] for r in rows}
    assert len(rows) == len(ids) == 196
    assert ledger['status'] == 'PENDING INDEPENDENT STRUCTURE REVIEW'
    assert ledger['predecessor_integration_sha256'] == '7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83'
    assert set(spans) == {q for r in rows for q in r['requirements']}
    for r in rows:
        assert r['requirements'] == r['source_span_refs'] and r['requirements']
        assert set(r['requirements']) <= spans.keys()
        assert r['route'] in ('X', 'S', 'no-established-route')
        assert r['predicate'] and r['missing_join']
        assert r['evidence'] and set(r['evidence']) <= locators.keys()
        assert set(r['input_sets']) <= sets.keys()
        assert set(r['existing_cases']) <= cases.keys()
        assert r['new_expected'] is None and r['new_actual'] is None
        assert r['new_grade'] == 'unchanged / no new grade'
        assert r['context'] == ('als-envelope' if r['id'].startswith('ALSO-') else 'lss-current')
    assert collections.Counter(r['route'] for r in rows) == ledger['summary']['routes']
    assert ledger['summary']['rows'] == len(rows) and ledger['summary']['owner_requirements'] == 27
    assert all(ledger['summary'][k] == 0 for k in ('new_requirements', 'new_cases', 'new_grades'))
    assert [r['id'] for r in rows if r['route'] == 'X'] == ['LSSO-008-CRC']
    by_id = {r['id']: r for r in rows}
    assert 'not applicationFileOpen' in by_id['ALSO-001-plain']['missing_join']
    assert 'no filesystem' in by_id['LSSO-008-CRC']['missing_join']
    assert 'not a new general' in by_id['LSSO-013-append-gain']['missing_join']
    for key in ('LSSO-009-codes2-7', 'ALSO-007-public-container', 'ALSO-009-previous-set'):
        assert by_id[key]['route'] == 'no-established-route'
    assert 'A7' in by_id['LSSO-017-members']['predicate']
    return ids


def main():
    # Reject unsupported modes before provider or packet reads.
    if sys.argv[1:] != ['--check']:
        raise SystemExit('read-only: use --check; writes/sealing/replay unsupported')
    here = Path(__file__).resolve().parent
    root = here.parents[3]
    read = lambda name: json.loads((here / name).read_text())
    pin_rows = read('pins.json')['providers']
    pins = {r['id']: r for r in pin_rows}
    assert len(pins) == len(pin_rows)
    data, mutable_context, immutable = {}, [], 0
    for key, pin in pins.items():
        raw = (root / pin['path']).read_bytes()
        if pin['kind'] == 'immutable-provider':
            assert len(raw) == pin['bytes'] and digest(raw) == pin['sha256'], key
            immutable += 1
            data[key] = raw
        elif digest(raw[:pin['bytes']]) == pin['sha256']:
            data[key] = raw[:pin['bytes']]
            mutable_context.append({'id': key, 'asof_prefix_available': True, 'current_bytes': len(raw)})
        else:
            # As-of wiki pins are not future mutable-file gates or snapshots.
            mutable_context.append({'id': key, 'asof_prefix_available': False, 'current_bytes': len(raw)})
    spans = read('source-spans.json')['requirements']
    locators = read('evidence-locators.json')['locators']
    checked_spans, deferred_spans, checked_pointers = 0, 0, 0

    def verify_locator(loc):
        nonlocal checked_spans, deferred_spans, checked_pointers
        assert loc['provider'] in pins
        if loc['provider'] not in data:
            deferred_spans += 1
            return
        raw = data[loc['provider']]
        if 'pointer' in loc:
            pointer(json.loads(raw), loc['pointer'])
            checked_pointers += 1
        else:
            start, size = loc['byte_start'], loc['bytes']
            assert 0 <= start <= start + size <= len(raw)
            assert digest(raw[start:start+size]) == loc['sha256']
            lines = raw.splitlines(keepends=True)
            line = loc.get('first_line', loc.get('line'))
            assert start == sum(map(len, lines[:line-1]))
            if 'last_line' in loc:
                assert size == sum(map(len, lines[line-1:loc['last_line']]))
            checked_spans += 1

    for loc in spans.values():
        verify_locator(loc)
    for group in locators.values():
        for loc in group:
            verify_locator(loc)
    sets = read('input-sets.json')['sets']
    cases = {}
    for key in ('lss-cases', 'als-cases'):
        s = sets[key]
        values = pointer(json.loads(data[s['provider']]), s['pointer'])
        assert len(values) == s['count']
        assert [v['id'] for v in values] == s['case_ids']
        assert [v['input'] for v in values] == s['input_paths']
        hashes = [digest(json.dumps(v, sort_keys=True, separators=(',', ':')).encode()) for v in values]
        assert hashes == s['record_sha256']
        cases.update({v['id']: v for v in values})
    for key in ('crc-eight', 'integer-texts'):
        s = sets[key]
        assert len(pointer(json.loads(data[s['provider']]), s['pointer'])) == s['count']
    for i in range(3, 8):
        assert cases[f'ALS-CONTAINER-{i:03d}']['expected']['outcome'] == 'refused'
    ledger = read('route-ledger.json')
    ids = check_ledger(ledger, spans, locators, sets, cases)
    crosswalk = read('minimal-status-crosswalk.json')
    assert crosswalk['counted_as_additional_outcomes'] is False and len(crosswalk['table_rows']) == 33
    for row in crosswalk['table_rows']:
        verify_locator(row['source'])
        assert set(row['outcome_refs']) <= ids
        assert row['outcome_refs'] or row['other_owner_boundaries']
    edges = read('chain-edges.json')
    assert len(edges['edges']) == 24 and len(edges['unknown_bridges']) == 6
    for edge in edges['edges']:
        assert edge['runtime_sequence_proved'] is False and edge['premises_and_unknowns']
        for loc in edge['evidence']:
            if isinstance(loc, str):
                assert loc in locators
            else:
                verify_locator(loc)
    for add in read('canonical-additions.json')['changes']:
        pin = pins[add['provider']]
        raw = (root / add['path']).read_bytes()
        assert pin['sha256'] == add['before_sha256'] and pin['bytes'] == add['before_bytes']
        assert digest(raw[:add['before_bytes']]) == add['before_sha256']
        suffix = add['append_utf8'].encode()
        assert raw[add['before_bytes']:add['after_bytes']] == suffix
        assert digest(raw[:add['after_bytes']]) == add['after_sha256']
        assert digest(suffix) == add['append_sha256']
    # These guard data associations only, not the full semantic truth of prose.
    mutations = [
        (0, 'new_actual', 'pass'), (0, 'new_expected', 'opens'),
        (0, 'new_grade', 'D12'), (0, 'route', 'X'),
        (0, 'source_span_refs', ['REQ-NOT-AN-OWNER-001']),
        (0, 'existing_cases', ['ALS-CONTAINER-999']),
    ]
    for name, field, value in [
        ('ALSO-001-plain', 'missing_join', 'Set opens'),
        ('LSSO-008-CRC', 'missing_join', 'File binding proved'),
        ('ALSO-007-public-container', 'route', 'S'),
        ('LSSO-017-members', 'predicate', 'Public Save always does this'),
    ]:
        mutations.append((next(i for i, r in enumerate(ledger['outcomes']) if r['id'] == name), field, value))
    for index, field, value in mutations:
        bad = copy.deepcopy(ledger)
        bad['outcomes'][index][field] = value
        try:
            check_ledger(bad, spans, locators, sets, cases)
        except (AssertionError, KeyError):
            continue
        raise AssertionError(('unsafe fixture accepted', index, field))
    print(json.dumps({'result': 'PASS', 'rows': len(ids), 'requirements': len(spans),
                      'cases': len(cases), 'immutable_pins': immutable,
                      'spans': checked_spans, 'pointers': checked_pointers,
                      'deferred_asof_spans': deferred_spans, 'negative_fixtures': len(mutations),
                      'mutable_asof_context': mutable_context}, indent=2))


if __name__ == '__main__':
    main()
