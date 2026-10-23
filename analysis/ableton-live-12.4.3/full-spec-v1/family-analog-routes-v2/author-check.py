#!/usr/bin/env python3
"""Bounded retained-history integrity; never execute retained study/original code."""
import ast
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify(raw, identity):
    assert len(raw) == identity['bytes'] and sha(raw) == identity['sha256'], identity


def at(value, pointer):
    for key in pointer.strip('/').split('/') if pointer else []:
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def reject(call, name):
    try:
        call()
    except (AssertionError, KeyError, IndexError):
        return name
    raise AssertionError('negative fixture accepted: ' + name)


pins = read(HERE / 'source-pins.json')
for p in pins['pins']:
    verify((ROOT / p['path']).read_bytes(), p)
history = read(HERE / 'history-correction.json')
overlay = read(HERE / 'route-ledger.json')
batch = read(HERE / 'batch-inputs.json')
assert history['predecessor_manifest']['sha256'] == '7eb26d849e950f329d2dd94494f67389e6bf530f106461c7f6ca1a35986ce9fa'
assert history['final_blocking_review']['sha256'] == '1046e9cf911970e96aff9fa5fe9dd2ac2617c690e95f4f609f5d11eca45b0f19'
review = read(ROOT / history['final_blocking_review']['path'])
assert review['disposition'] == 'correction-required'
assert review['reviewed_manifest']['sha256'] == history['predecessor_manifest']['sha256']
assert review['findings'][0]['id'] == history['finding'] == 'ANRMAP-001'
qualification = read(ROOT / history['root_owner_qualification']['path'])
assert history['root_owner_qualification']['sha256'] == '300ec5c63a9a9d005960380c14e2056301addf1e3cd279281d7d8e67d68d50e2'
assert qualification['owner_after'] == history['current_owner_as_of'] == overlay['current_owner_as_of']
assert qualification['owner_before'] == history['historical_owner_as_of_v1'] == overlay['historical_owner_as_of_v1']
assert qualification['source_review']['sha256'] == history['final_blocking_review']['sha256']
assert history['current_owner_as_of']['sha256'] == 'a63ceb8be20b5c24a7b3270ead540f45f79ee2eb01032d7f17516913c4ccd993'
assert pins['source_spans'] == history['exact_source_spans'] == review['findings'][0]['exact_source_spans']
for s in history['exact_source_spans']:
    lines = (ROOT / s['path']).read_text().splitlines()
    a, b = s['lines']
    assert sha(('\n'.join(lines[a-1:b]) + '\n').encode()) == s['span_sha256']

method_path = ROOT / 'analysis/ableton-live-12.4.3/r2/t12-analog-v1/measure.py'
tree = ast.parse(method_path.read_text())
loop = next(n for n in ast.walk(tree) if isinstance(n, ast.For) and n.lineno == 719)
tuples = ast.literal_eval(loop.iter)  # Parse literal input data only; no retained function call.
assert len(tuples) == 8
method = method_path.read_text().splitlines()
assert "an.script(hv, [(4400, 0x90, 60, 100)], fs, 26624, 512)" in method[720]
assert "['process 13312 512', f'param {idx} {val!r}', 'process 13312 512', 'destroy']" in method[721]
assert "['process 13312 512', 'process 13312 512', 'destroy']" in method[722]
driver = (ROOT / 'analysis/ableton-live-12.4.3/r2/t12-analog-v1/harness/xdev.c').read_text()
assert 'static event_t events[4096];' in driver and 'static int nevents;' in driver
assert 'long done = 0,' in driver
assert 'events[e].frame >= done && events[e].frame < done + k' in driver
assert 'blk[m++].frame -= done;' in driver
assert 'events[nevents++] = (event_t)' in driver
assert 'abs_frame' not in driver and 'nevents = 0' not in driver


def validate_history(value):
    h = value['history']
    assert h['history_label'] == 'retained-two-process-repeated-note'
    assert h['event_coordinate_scope'] == 'per-process-command-local-done'
    assert h['queued_event_consumption'] == 'persistent-global-queue-not-consumed'
    assert h['uninterrupted_held_history_established'] is False
    assert h['held_sustain_delay_established'] is False
    assert h['device_effect_frame_for_replayed_note'] is None
    assert h['queued_event'] == {'frame': 4400, 'status': 144, 'key': 60, 'velocity': 100}
    assert h['process_commands'] == [{'frames': 13312, 'block': 512}, {'frames': 13312, 'block': 512}]
    # Integer source-history coordinates only; no DSP/trajectory/audio model.
    event = h['queued_event']['frame']
    block = h['process_commands'][0]['block']
    callback_local = event // block * block
    start = 0
    expected = []
    for i, command in enumerate(h['process_commands'], 1):
        expected.append({'process_command': i, 'callback_cumulative_start': start + callback_local,
                         'callback_event_offset': event - callback_local,
                         'queued_timestamp_cumulative': start + event})
        start += command['frames']
    assert h['deliveries'] == expected
    assert expected[1]['callback_cumulative_start'] == 17408
    assert expected[1]['callback_event_offset'] == 304
    assert expected[1]['queued_timestamp_cumulative'] == 17712
    raw = read(ROOT / value['retained_result_container']['path'])
    results = raw['parameter_changes']
    assert len(results) == 8
    for i, (name, index, target) in enumerate(tuples):
        r = results[i]
        assert (r['parameter'], r['index'], r['value'], r['change_frame']) == (name, index, target, 13312)
    for link in value['affected_row_result_links']:
        r = at(raw, link['result_pointer'])
        assert r['first_changed_frame'] == link['retained_first_changed_frame']
        if link['outcome'] == 'AN-OUT-229':
            assert r['index'] == 105 and r['first_changed_frame'] == 17734
            assert link['support_scope'] == 'historical-repeated-note-result-only-not-held-sustain-delay'
            assert r['first_changed_frame'] > expected[1]['queued_timestamp_cumulative']
        else:
            assert r['first_changed_frame'] < expected[1]['callback_cumulative_start']
            assert link['support_scope'] == 'finite-first-change-before-second-replayed-event-callback'


validate_history(history)
base = read(ROOT / overlay['base_ledger']['path'])
assert len(base['rows']) == base['required_outcomes_enumerated'] == 241
assert len(base['owner_clauses']) == 128
base_ids = {r['id']: r for r in base['rows']}


def resolve(value):
    effective = copy.deepcopy(base)
    ids = {r['id']: r for r in effective['rows']}
    wanted = {f'AN-OUT-{n:03}' for n in range(222, 232)}
    assert {p['id'] for p in value['row_updates']} == wanted
    assert len(value['row_updates']) == 10
    allowed = {'context', 'history_ref', 'analysis_qualification', 'missing_join'}
    for p in value['row_updates']:
        assert set(p['set']) == allowed
        assert p['set']['context'] == 'module-between-block-change-repeated-note-history'
        assert p['set']['history_ref'] == 'history-correction.json#/history'
        assert p['set']['analysis_qualification'] and p['set']['missing_join']
        ids[p['id']].update(p['set'])
    assert set(value['context_updates']) == {'module-between-block-change-repeated-note-history'}
    assert set(value['auxiliary_dependency_updates']) == {'AUX-X86-PROTOCOL'}
    assert set(value['auxiliary_dependency_updates']['AUX-X86-PROTOCOL']) == {'parameter_change_history_ref', 'parameter_change_scope'}
    for key, context_text in value['context_updates'].items():
        effective['contexts'][key] = context_text
    for key, dependency_updates in value['auxiliary_dependency_updates'].items():
        effective['auxiliary_dependencies'][key].update(dependency_updates)
    for key, r in ids.items():
        if key not in wanted:
            assert r == base_ids[key]
        else:
            for field in base_ids[key]:
                if field not in allowed:
                    assert r[field] == base_ids[key][field]
    assert dict(Counter(r['route'] for r in effective['rows'])) == {'X-route': 199, 'S-route': 30, 'no-established-route': 12}
    assert sum(r['route'] == 'X-route' and r['owner_basis_unchanged'] == 'U' for r in effective['rows']) == 37
    assert all(r['public_application_binding'] == 'no-established-route' for r in effective['rows'])
    assert ids['AN-OUT-230']['owner_basis_unchanged'] == ids['AN-OUT-231']['owner_basis_unchanged'] == 'U'
    assert ids['AN-OUT-232'] == base_ids['AN-OUT-232']
    assert effective['owner_clauses'] == base['owner_clauses']
    return effective


effective = resolve(overlay)
original_sources = read(ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/family-analog-routes-v1/sources.json')
assert len(original_sources['records']) == 64 and len(original_sources['selected_call_index_rows']) == 18
original_pins = read(ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/family-analog-routes-v1/source-pins.json')
assert len(original_pins['pins']) == 90  # Unit assertion only; do not replay them.
# Metadata shifted old line numbers; locate unchanged exact span hashes. Never
# verify current owner bytes against the old v1 fullfile hash.
owner = (ROOT / base['owner']['path']).read_text().splitlines()
owner_span_locations = {}
for tag in ['L474-483', 'L484-486', 'L487-488']:
    p = base['owner_clauses'][tag]
    a, b = p['lines']
    length = b-a+1
    matches = [n for n in range(len(owner)-length+1)
               if sha(('\n'.join(owner[n:n+length]) + '\n').encode()) == p['sha256_of_text']]
    assert len(matches) == 1, tag
    owner_span_locations[tag] = [matches[0]+1, matches[0]+length]
base_batch = read(ROOT / batch['base_batch']['path'])
assert set(batch['group_updates']) == {'PROTOCOL'}
assert set(batch['prospective_updates']) == {'P2'}
assert set(batch['group_updates']['PROTOCOL']) == {'meaning', 'history_ref', 'parameter_change_result_pointer'}
assert batch['group_updates']['PROTOCOL']['history_ref'] == 'history-correction.json#/history'
assert set(batch['prospective_updates']['P2']) == {'status', 'input_basis', 'unresolved', 'history_correction_ref'}
assert next(p for p in base_batch['prospective_unexecuted'] if p['id'] == 'P2')['host_index_set'] == list(range(203))
assert 'parked-unselected' in batch['prospective_updates']['P2']['status']

negative = []
bad = copy.deepcopy(history)
bad['history']['history_label'] = 'uninterrupted-held-note'
negative.append(reject(lambda: validate_history(bad), 'uninterrupted-held-label-rejected'))
bad = copy.deepcopy(history)
bad['history']['held_sustain_delay_established'] = True
negative.append(reject(lambda: validate_history(bad), 'held-sustain-delay-claim-rejected'))
bad = copy.deepcopy(history)
bad['history']['deliveries'][1]['callback_cumulative_start'] = 17712
negative.append(reject(lambda: validate_history(bad), 'timestamp-as-callback-rejected'))
bad = copy.deepcopy(history)
bad['affected_row_result_links'][-1]['retained_first_changed_frame'] = 17712
negative.append(reject(lambda: validate_history(bad), 'altered-retained-result-rejected'))
bad = copy.deepcopy(overlay)
bad['row_updates'][-1]['set']['observable_predicate'] = 'new-law'
negative.append(reject(lambda: resolve(bad), 'predicate-mutation-rejected'))
negative.append(reject(lambda: verify(b'bad', {'bytes': 3, 'sha256': sha(b'abc')}), 'corrupt-source-rejected'))

prefix = pins['canonical_research_prefix']
canonical = (ROOT / prefix['path']).read_bytes()
verify(canonical[:prefix['bytes']], prefix)
assert b'## Analog retained-history correction' in canonical[prefix['bytes']:]
links = 0
for p in [HERE / 'structure.md', ROOT / prefix['path']]:
    content = p.read_text() if p.parent == HERE else canonical[prefix['bytes']:].decode()
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if '://' in target or target.startswith('#'):
            continue
        assert (p.parent / target.split('#')[0]).resolve().exists(), target
        links += 1
for p in HERE.iterdir():
    if p.is_file() and not p.name.startswith('.'):
        assert not re.search(r'[ \t]+\n', p.read_text()), p
payloads = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
            for p in sorted(HERE.iterdir()) if p.is_file() and not p.name.startswith('.')
            and p.name not in ['manifest.json', 'author-check.json']]
result = {'status': 'PASS-author-bounded-correction-integrity-pending-independent-review',
          'finding': 'ANRMAP-001', 'selected_pins_checked': len(pins['pins']),
          'source_spans_checked': len(history['exact_source_spans']), 'historical_control_result_tuples_checked': 8,
          'qualified_current_owner': history['current_owner_as_of'], 'affected_owner_span_locations': owner_span_locations,
          'patched_rows': 10, 'unchanged_rows': 231, 'predicates_inherited_unchanged': 241,
          'route_inventory_not_grades': base['counts_inventory_only'], 'investigative_U_X_preserved': 37,
          'all_public_bindings': 'no-established-route', 'negative_fixtures_rejected': negative,
          'canonical_prefix': prefix, 'links_checked': links, 'payloads': payloads,
          'new_history_batch_prepared_or_executed': False,
          'original_provider_decoder_harness_measurement_model_comparator_candidate_execution': False,
          'full_predecessor_or_release_universe_replay': False,
          'limitation': 'Author integrity only; independent review and Root current-owner/shared integration remain separate.'}
(HERE / 'author-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['payloads', 'canonical_prefix']}, indent=2))
