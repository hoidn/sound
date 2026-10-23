#!/usr/bin/env python3
"""Read-only JSON/text/hash checks; no old tools, numeric or original execution."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import sys


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def ptr(obj, path):
    for k in path.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        obj = obj[int(k)] if isinstance(obj, list) else obj[k]
    return obj


def ledger_check(ledger, span_ids, bases, group_ids, control_names):
    rows = ledger['outcomes']
    assert len(rows) == len({r['id'] for r in rows}) == 146
    assert ledger['status'] == 'PENDING INDEPENDENT STRUCTURE REVIEW'
    assert ledger['integration_host_bundle_join'] == 'UNKNOWN' and ledger['A1_accepted'] is False
    assert ledger['omission_status'] == {'historical': 174, 'note72': 2, 'all_ungraded': True}
    assert collections.Counter(r['route'] for r in rows) == {'X': 49, 'S': 83, 'no-established-route': 14}
    assert ledger['summary']['routes'] == dict(collections.Counter(r['route'] for r in rows))
    for r in rows:
        assert r['requirements'] and set(r['requirements']) <= span_ids
        assert r['source_span_ref'] in r['source_span_refs']
        assert set(r['source_span_refs']) <= span_ids
        assert set(r['requirements']) <= set(r['source_span_refs'])
        assert r['predicate'] and r['missing_join'] and r['route_scope']
        assert r['evidence_basis'] and set(r['evidence_basis']) <= bases
        assert set(r['parameters']) <= control_names
        assert set(r['existing_groups']) <= group_ids
        assert r['new_expected'] is None and r['new_actual'] is None
        assert r['new_grade'] == 'unchanged / no new grade'
    by_id = {r['id']: r for r in rows}
    for i in range(38):
        r = by_id[f'CO-002-index-{i:02d}']
        assert r['route'] == 'S' and r['parameters']
    for i in (14, 15, 16):
        assert 'A1' in by_id[f'CO-002-index-{i:02d}']['premises'][0]
    assert by_id['CO-002-a1']['route'] == 'no-established-route'
    assert by_id['CO-005-omissions']['route'] == 'no-established-route'
    assert by_id['CO-013-note72-omissions']['route'] == 'no-established-route'
    assert 'no4000duration' in by_id['CO-008-movement']['missing_join']
    assert 'stored' in by_id['CO-002-a1']['predicate']
    assert ledger['summary']['denominator'] is None and ledger['summary']['complete_profiles'] == 0
    assert all(ledger['summary'][k] == 0 for k in ('new_requirements', 'new_cases', 'new_grades'))
    assert ledger['summary']['requirements'] == 13 and ledger['summary']['rows'] == 146


def main():
    if sys.argv[1:] != ['--check']:
        raise SystemExit('read-only --check only; no write/seal/replay mode')
    here = Path(__file__).resolve().parent
    root = here.parents[3]
    load = lambda name: json.loads((here / name).read_text())
    pin_rows = load('pins.json')['providers']
    pins = {p['id']: p for p in pin_rows}
    assert len(pins) == len(pin_rows)
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
    spans_file = load('source-spans.json')
    spans = dict(spans_file['requirements'], **spans_file['sections'])
    bases = load('evidence-locators.json')['locators']
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
            a, n = loc['byte_start'], loc['bytes']
            assert 0 <= a <= a+n <= len(raw) and sha(raw[a:a+n]) == loc['sha256']
            lines = raw.splitlines(keepends=True)
            assert sum(map(len, lines[:loc['first_line']-1])) == a
            assert sum(map(len, lines[loc['first_line']-1:loc['last_line']])) == n
            span_count += 1

    for loc in spans.values():
        locator(loc)
    for group in bases.values():
        for loc in group:
            locator(loc)
    assert len(spans_file['requirements']) == 13
    cases = json.loads(data['v5-cases'])['cases']
    inputs = load('input-sets.json')
    sets = inputs['sets']
    current = sets['released-evaluations']
    assert len(cases) == current['groups'] == 27
    assert [sha(json.dumps(g, sort_keys=True, separators=(',', ':')).encode()) for g in cases] == current['group_sha256']
    evs = [e for g in cases for e in g['evaluations']]
    assert len(evs) == current['evaluations'] == len(current['records']) == 73
    for e, row in zip(evs, current['records']):
        assert ptr(json.loads(data['v5-cases']), row['pointer']) == e
        assert row['id'] == e['id'] and row['sha256'] == sha(json.dumps(e, sort_keys=True, separators=(',', ':')).encode())
        assert row['model_index'] == int(e['parameters']['ResonanceType'])
        assert row['quality'] == int(e['parameters']['ResonatorQuality'])
        assert row['metric_kind'] == e['metric']['kind']
        assert row['scored_mode_points'] == list(map(len, e['metric'].get('modes', [])))
        assert row['signal'] == e['signal'] and row['reference'] == e['reference']
    names = evs[0]['parameter_order']
    controls = load('control-navigation.json')
    assert len(names) == len(set(names)) == len(controls['controls']) == 38
    assert [(r['index'], r['name']) for r in controls['controls']] == list(enumerate(names))
    assert [r['name'] for r in controls['models']] == ['Beam', 'Marimba', 'String', 'Membrane', 'Plate', 'Pipe', 'Tube']
    ledger = load('route-ledger.json')
    ledger_check(ledger, set(spans), set(bases), {g['id'] for g in cases}, set(names))
    ids = {r['id'] for r in ledger['outcomes']}
    for row in controls['controls']:
        assert row['mapping_outcome'] in ids and set(row['outcome_refs']) <= ids
        assert row['outcome_refs'] == [r['id'] for r in ledger['outcomes'] if row['name'] in r['parameters']]
    for row in controls['models']:
        assert set(row['outcome_refs']) <= ids and row['existing_evaluations']
        assert row['existing_evaluations'] == [r['id'] for r in current['records'] if r['model_index'] == row['index']]
    omitted = ptr(json.loads(data['preflight']), '/omitted_modal_modes')
    assert len(omitted) == 14 and sum(x['occurrences'] for x in omitted) == 174
    assert sum(len(g['mode_indices']) for x in omitted for g in x['groups']) == 174
    assert sets['omissions']['historical_occurrences'] == 174 and sets['omissions']['extra_note72']['count'] == 2
    assert sets['omissions']['extra_note72']['channel_modes'] == [{'channel': 'L', 'mode': 16}, {'channel': 'R', 'mode': 16}]
    assert [len(m) for m in evs[-3]['metric']['modes']] == [15, 15]
    assert evs[-1]['parameter_updates'] == [{'frame': 8192, 'index': 15, 'parameter': 'ListeningXL', 'value': 0.75}]
    assert sets['parked96']['status'] == 'PREPARATION ONLY / UNEXECUTED' and sets['parked96']['bytes'] == 96
    assert inputs['required_outcome_denominator'] is None and inputs['complete_profiles'] == 0
    assert inputs['new_calls'] == inputs['new_grades'] == 0
    calls = load('callable-sets.json')
    assert calls['required_outcome_denominator'] is None and len(calls['historical_script_metadata']) == 64
    for row in calls['historical_script_metadata']:
        value = ptr(json.loads(data['t12']), row['pointer'])
        assert value['bytes'] == row['bytes'] and value['sha256'] == row['sha256']
    edges = load('chain-edges.json')
    assert len(edges['edges']) == 14 and len(edges['unknown_bridges']) == 8
    assert edges['edges'][0]['status'] == 'UNKNOWN'
    for e in edges['edges']:
        assert e['runtime_sequence_proved'] is False and e['premises_and_unknowns']
        assert set(e['evidence_basis']) <= bases.keys()
    add = load('canonical-addition.json')
    raw = (root / add['path']).read_bytes()
    assert sha(raw[:add['before_bytes']]) == add['before_sha256'] == pins['research-before']['sha256']
    assert raw[add['before_bytes']:add['after_bytes']] == add['append_utf8'].encode()
    assert sha(raw[:add['after_bytes']]) == add['after_sha256']
    assert sha(add['append_utf8'].encode()) == add['append_sha256']
    # Explicit wrong associations/promotions; no numerical estimator or old code.
    mutations = [('A1_accepted', True), ('integration_host_bundle_join', 'PROVED'),
                 ('omission_status', {'historical': 0, 'note72': 0, 'all_ungraded': False})]
    for key, value in mutations:
        bad = copy.deepcopy(ledger)
        bad[key] = value
        try:
            ledger_check(bad, set(spans), set(bases), {g['id'] for g in cases}, set(names))
        except AssertionError:
            continue
        raise AssertionError(('unsafe top-level mutation', key))
    row_mutations = [('CO-002-index-14', 'premises', []), ('CO-005-omissions', 'route', 'X'),
                     ('CO-013-note72-omissions', 'route', 'X'), ('CO-008-movement', 'missing_join', '4000 duration proved'),
                     ('CO-001-output', 'new_actual', 'pass'), ('CO-001-output', 'new_expected', 'all modes'),
                     ('CO-001-output', 'source_span_refs', ['MISSING']), ('CO-001-output', 'existing_groups', ['CORPUS-AUDIO-999'])]
    for id, key, value in row_mutations:
        bad = copy.deepcopy(ledger)
        next(r for r in bad['outcomes'] if r['id'] == id)[key] = value
        try:
            ledger_check(bad, set(spans), set(bases), {g['id'] for g in cases}, set(names))
        except (AssertionError, IndexError, KeyError):
            continue
        raise AssertionError(('unsafe row mutation', id, key))
    print(json.dumps({'result': 'PASS', 'rows': 146, 'routes': ledger['summary']['routes'],
                      'requirements': 13, 'groups': 27, 'evaluations': 73, 'controls': 38, 'models': 7,
                      'historical_omissions': 174, 'note72_omissions': 2, 'script_metadata': 64,
                      'provider_pins': len(pins), 'spans': span_count, 'pointers': pointer_count,
                      'unavailable_asof_spans': unavailable, 'negative_fixtures': len(mutations)+len(row_mutations),
                      'mutable_context': asof}, indent=2))


if __name__ == '__main__':
    main()
