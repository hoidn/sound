#!/usr/bin/env python3
"""Documentary integrity only. Never import/run original drivers, DSP or comparator."""
import copy
import hashlib
import json
import math
import re
import struct
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
T = 'analysis/ableton-live-12.4.3/r2/t12-tension-v1'
H = 'handoff/device-tension-v1'
A = 'analysis/ableton-live-12.4.3/handoff-staging/device-tension-v1-analysis'


def read(path):
    return json.loads(path.read_text())


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pointer(data, path):
    for part in path.lstrip('/').split('/') if path else []:
        part = part.replace('~1', '/').replace('~0', '~')
        data = data[int(part)] if isinstance(data, list) else data[part]
    return data


def check_pin(pin):
    raw = (ROOT/pin['path']).read_bytes()
    assert (len(raw), sha(raw)) == (pin['bytes'], pin['sha256']), 'pin mismatch'


def check_span(s):
    lines = (ROOT/s['path']).read_text().splitlines(keepends=True)
    a, b = s['lines']
    assert 1 <= a <= b <= len(lines), 'bad span bounds'
    assert sha(''.join(lines[a-1:b]).encode()) == s['span_sha256'], 'span digest mismatch'


def validate(ledger, source, evaluations, cases, trace, runs, sensitivity, batches):
    rows = ledger['outcomes']
    ids = {r['id'] for r in rows}
    assert len(rows) == len(ids) == 93, 'outcome units changed/conflated'
    assert {r['requirement'] for r in rows} == {f'REQ-DEVICE-TENSION-{n:03}' for n in range(1, 16)}
    assert dict(Counter(r['route'] for r in rows)) == ledger['route_counts'] == {'X': 71, 'S': 12, 'no-established-route': 10}
    assert ledger['public_host_join'] == 'unknown' and ledger['arm64_equivalence'] == 'not-established'
    assert not ledger['new_execution'] and not source['new_traversal'] and source['new_indirect_resolutions'] == 0
    assert source['actual_tension_receiver_bound'] is False and source['arm64_execution'] is False
    batch_ids = {b['id'] for b in batches['batches']}
    owner = (ROOT/'wiki/specs/device-tension.md').read_text().splitlines()
    headers = [(i, re.search(r'REQ-DEVICE-TENSION-\d{3}', line)[0]) for i, line in enumerate(owner, 1) if line.startswith('### REQ-DEVICE-TENSION-')]
    bounds = {r: (n, headers[i+1][0] if i+1 < len(headers) else 407) for i, (n, r) in enumerate(headers)}
    for r in rows:
        check_span(r['source'])
        a, b = r['source']['lines']
        lo, hi = bounds[r['requirement']]
        assert lo < a <= b < hi, 'outcome outside owner requirement'
        assert r['public_binding'] == 'unknown' and r['missing_joins'] and not r['grade_change'], 'unsupported public credit'
        assert r['basis'] in source['bases'] and set(r['candidate_batches']) <= batch_ids
        assert r['route'] == source['bases'][r['basis']]['route'], 'route/basis conflict'
        assert all(c in {x['id'] for x in ledger['draft_case_index']} for c in r['case_ids'])
        for loc in r['retained_result_locators']:
            pointer(read(ROOT/loc['path']), loc['pointer'])
    assert len(ledger['draft_case_index']) == 42 and len(ledger['unresolved_enumeration']) == 12
    for x in ledger['draft_case_index'] + ledger['unresolved_enumeration']:
        check_span(x['source'])
    for b in source['bases'].values():
        for loc in b['locators']:
            if 'lines' in loc:
                check_span(loc)
            elif 'pointer' in loc:
                pointer(read(ROOT/loc['path']), loc['pointer'])
    es = evaluations['evaluations']
    assert len(es) == len({e['id'] for e in es}) == evaluations['units'] == 27, 'evaluation units changed/conflated'
    assert {e['id'] for e in es} == {c['id'] for c in cases['cases']}
    assert not (ids & {e['id'] for e in es}), 'case/evaluation IDs used as required predicates'
    assert dict(Counter(e['metric_class'] for e in es)) == {'stable': 26, 'repeated-strike': 1}
    assert evaluations['excluded_counts'] == {'chaotic': 4, 'uncalibrated': 37}
    assert Counter(trace['excluded'].values()) == Counter({'chaotic: no statistical comparator released': 4, 'no retained per-setting sensitivity study': 37})
    assert len(runs['runs']) == 68 and len(sensitivity)-1 == 31
    for row in es:
        ev = pointer(cases, row['release_pointer'])
        c = pointer(cases, row['release_case_pointer'])
        tr = pointer(trace, row['trace_pointer'])
        run = pointer(runs, row['run_pointer'])
        assert row['id'] == ev['id'] == c['id'] == tr['case']
        assert row['requirements'] == c['requirements']
        assert row['source_tag'] == tr['source_case'] not in trace['excluded']
        assert row['route'] == 'X' and row['public_binding'] == 'unknown' and row['arm64_equivalence'] == 'not-established'
        assert row['reference_sha256'] == tr['raw_reference_sha256']
        assert row['source_wav_sha256'] == tr['source_wav_sha256'] == run['wav_sha256']
        assert sha((ROOT/row['source_script']).read_bytes()) == row['source_script_sha256'] == tr['source_script_sha256']
        assert row['protocol_summary'] == dict(sample_rate_hz=ev['sample_rate_hz'], frames=ev['frames'], channels=1, block_frames=512, warm_up_frames=0, parameter_count=129, events=len(ev['events']))
        assert row['reference_bytes'] == 4*ev['frames']
        assert row['metric_class'] == ev['metric']['kind'] and pointer(cases, row['metric_pointer']) == ev['metric']
        assert row['calibration_variants'] == sorted(pointer(sensitivity, row['sensitivity_pointer'])) == sorted(['libm+1', 'libm-1', 'round_down', 'round_up', 'round_zero']), 'missing calibration'
        script = (ROOT/row['source_script']).read_text().splitlines()
        assert script[0] == 'create' and script[1] == f"rate {ev['sample_rate_hz']}" and script[-1] == 'destroy'
        assert [s for s in script if s.startswith('process ')] == [f"process {ev['frames']} 512"]
        assert script[-4:-1] == ['inflag 0', 'input zero', f"process {ev['frames']} 512"]
        params = [s.split()[1:] for s in script if s.startswith('param ')]
        assert [int(p[0]) for p in params] == [i for i in range(130) if i != 2]
        assert len(ev['parameter_order']) == len(set(ev['parameter_order'])) == len(ev['parameters']) == 129
        for (_, v), name in zip(params, ev['parameter_order']):
            assert math.isfinite(ev['parameters'][name])
            assert struct.pack('<f', float(v)) == struct.pack('<f', ev['parameters'][name]), 'binary32 vector mismatch'
        events = [[int(f), int(s, 0), int(k), int(v)] for f, s, k, v in [s.split()[1:] for s in script if s.startswith('event ')]]
        assert events == run['events']
        assert events == [[e['frame'], 144 if e['type'] == 'note_on' else 128, e['key'], e['velocity']] for e in ev['events']]
        assert all(e['channel'] == 1 for e in ev['events'])
        if row['metric_class'] == 'stable':
            assert ev['metric']['partials'] and ev['metric']['amplitude_normalizer'] > 0 and ev['metric']['partial_window']
        else:
            assert not ev['metric']['partials'] and len(ev['metric']['waveform_windows']) == 1


def source_checks(source):
    codes = {}
    for r in source['host_source_records']:
        raw = (ROOT/r['path']).read_bytes().splitlines(keepends=True)[r['line']-1]
        d = json.loads(raw)
        assert sha(raw) == r['record_sha256'] and d['entry'] == r['entry']
        assert sha(d['code'].encode()) == r['code_sha256'] == d['code_sha256']
        assert r['original_locator']['code_sha256'] == d['code_sha256']
        assert r['original_locator']['retained_line'] == r['line']
        assert d['warnings'] == r['warnings']
        assert not d['timed_out'] and not d['partial_code']
        codes[r['id']] = d['code']
    assert codes['HOST-20'].count('FUN_102fbff98(') == 4
    assert 'FUN_102fbff98(' not in codes['HOST-26'] + codes['HOST-31']
    assert '0x400' in codes['HOST-33']
    edge = next(x for x in source['edges'] if x['id'] == 'TNE-08')
    assert 'four 1024-frame' in edge['carried_state'] and 'no warm-up' in edge['carried_state'], 'reset path overgeneralized'
    assert next(x for x in source['edges'] if x['id'] == 'TNE-07')['classification'] == 'unknown'


def main():
    pins = read(HERE/'pins.json')
    for p in pins['pins']:
        if p['mode'] != 'author-time-context':
            check_pin(p)
    prefix = pins['canonical_research_preserved_prefix']
    assert sha((ROOT/prefix['path']).read_bytes()[:prefix['bytes']]) == prefix['sha256'], 'canonical history changed'
    ledger, source, es, batches = [read(HERE/n) for n in ['route-ledger.json', 'source-map.json', 'released-evaluations.json', 'candidate-batches.json']]
    cases, trace, runs, sens = [read(ROOT/p) for p in [H+'/cases.json', A+'/traceability.json', T+'/results/runs.json', T+'/results/sensitivity.json']]
    args = [ledger, source, es, cases, trace, runs, sens, batches]
    validate(*args)
    source_checks(source)
    negatives = []

    def reject(name, changed, fn):
        try:
            fn(changed)
        except (AssertionError, KeyError, ValueError, IndexError):
            negatives.append(name)
        else:
            raise AssertionError('negative control accepted: '+name)

    bad = copy.deepcopy(pins['pins'][0]); bad['sha256'] = '0'*64
    reject('bad-selected-pin', bad, check_pin)
    for name, index, mutate in [
        ('outcome-row-as-extra-evaluation', 0, lambda d: d['outcomes'].append(copy.deepcopy(d['outcomes'][0]))),
        ('owner-span-outside-requirement', 0, lambda d: d['outcomes'][0].update(source=copy.deepcopy(d['outcomes'][12]['source']))),
        ('unsupported-public-waveform-credit', 0, lambda d: d['outcomes'][0].update(public_binding='established')),
        ('U-upgraded-to-X', 0, lambda d: d['outcomes'][9].update(route='X')),
        ('ARM-equivalence-upgrade', 1, lambda d: d.update(arm64_execution=True)),
        ('actual-instance-inferred-from-generic-host', 1, lambda d: d.update(actual_tension_receiver_bound=True)),
        ('duplicate-finite-evaluation', 2, lambda d: d['evaluations'][1].update(id=d['evaluations'][0]['id'])),
        ('calibration-variant-omitted', 2, lambda d: d['evaluations'][0]['calibration_variants'].pop()),
        ('chaotic-setting-in-release', 2, lambda d: d['evaluations'][0].update(source_tag='exc_bow')),
        ('changed-binary32-finite-input', 3, lambda d: d['cases'][0]['evaluations'][0]['parameters'].update(Polyphony=100.0)),
    ]:
        changed = copy.deepcopy(args); mutate(changed[index])
        reject(name, changed, lambda v: validate(*v))
    bad = copy.deepcopy(source); next(x for x in bad['edges'] if x['id'] == 'TNE-08')['carried_state'] = 'Universal 1024-frame warm-up'
    reject('universal-reset-warmup-claim', bad, source_checks)
    report = dict(status='pass', scope='Documentary integrity only; no original/candidate/provider/harness/decoder/comparator execution or audio decoding', pins=len(pins['pins']), exact_selected_pins_checked=sum(p['mode'] != 'author-time-context' for p in pins['pins']), mutable_author_time_context_pins=1, requirements=15, required_predicates=93, routes=ledger['route_counts'], draft_case_ids=42, distinct_released_evaluations=27, stable_evaluations=26, repeated_evaluations=1, selected_scripts=27, source_records=16, structural_edges=9, unresolved_enumeration=12, auxiliary_records=3, negative_controls=negatives, preserved_canonical_prefix=prefix, missing=['Actual host-to-Tension receiver, timebase and instance/output join', 'Application reset/rate/activity/error/teardown observables', 'Per-setting calibration beyond the released27; chaotic statistical comparator', 'arm64 execution and Apple library equivalence'], grade_changes=0)
    (HERE/'author-check.json').write_text(json.dumps(report, indent=1)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'pins', 'required_predicates', 'routes', 'distinct_released_evaluations', 'negative_controls']}))


if __name__ == '__main__':
    main()
