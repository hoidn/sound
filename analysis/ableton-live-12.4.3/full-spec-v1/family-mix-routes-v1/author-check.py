#!/usr/bin/env python3
"""Check this documentary inventory; never execute reference or candidate code."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(path):
    return json.loads(path.read_text())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pointer(value, path):
    for part in path.lstrip('/').split('/') if path else []:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validate(ledger, basis, batches, source):
    outcomes = ledger['outcomes']
    all_records = outcomes + ledger['auxiliary_clause_records']
    ids = [r['id'] for r in all_records]
    assert len(ids) == len(set(ids)), 'duplicate local outcome/auxiliary ID'
    requirements = {f'REQ-MIX-GRAPH-{n:03}' for n in range(1, 17)}
    assert {r['requirement'] for r in outcomes} == requirements, 'requirement missing'
    assert dict(Counter(r['route'] for r in outcomes)) == ledger['counts']['by_route']
    assert len(outcomes) == ledger['counts']['outcomes']
    assert len(ledger['auxiliary_clause_records']) == 2
    assert len(ledger['unresolved_or_excluded_scope']) == 13
    batch_ids = {b['id'] for b in batches['batches']}
    for r in all_records:
        assert r['route'] in {'X', 'S', 'no-established-route'}
        assert r['route_basis'] and set(r['route_basis']) <= set(basis), 'unknown route basis'
        assert set(r['candidate_batches']) <= batch_ids
        s = r['source']
        first, last = s['lines']
        assert s['path'] == 'wiki/specs/mix-graph.md' and s['revision'] == 2
        assert first <= s['anchor_line'] <= last
        assert s['anchor'] in source[s['anchor_line'] - 1], 'bad anchor'
        assert sha(('\n'.join(source[first-1:last]) + '\n').encode()) == s['span_sha256'], 'bad span'
        prior = [x for x in source[:first] if x.startswith('### REQ-MIX-GRAPH-')]
        assert prior and r['requirement'] in prior[-1], 'span outside requirement'
        if r['route'] == 'no-established-route':
            assert r['missing_joins'], 'unknown without boundary'
    # Parent bullets are documentary obligations, not the outcome count. Auxiliary
    # correction/restatement dispositions preserve clauses without double counting.
    begin = source.index('## Requirements')
    end = source.index('## Timing and state')
    clauses = [n for n in range(begin, end) if source[n].startswith('- **')]
    for n in clauses:
        assert any(r['source']['lines'][0] <= n+1 <= r['source']['lines'][1]
                   for r in all_records), f'orphaned parent clause at {n+1}'
    case_rows = {}
    for n, line in enumerate(source, 1):
        if re.match(r'\| MG-\d{3} \|', line):
            case_rows[line.split('|')[1].strip()] = (n, line)
    assert len(case_rows) == 34
    assert {c['id'] for c in ledger['cases']} == set(case_rows), 'bad case inventory'
    assert len(ledger['cases']) == 34
    for c in ledger['cases']:
        n, line = case_rows[c['id']]
        fields = [x.strip() for x in line.strip('|').split('|')]
        assert c['source_line'] == n and sha((line+'\n').encode()) == c['row_sha256'], 'bad case'
        assert (c['kind'], c['label']) == (fields[2], fields[-1])
        assert c['outcomes'] == [r['id'] for r in outcomes if c['id'] in r['cases']]
        assert c['outcomes'] or c['id'] == 'MG-008'
    for r in outcomes:
        assert set(r['cases']) <= set(case_rows)
        expected = {b['id'] for b in batches['batches'] if r['id'] in b['related_outcomes']}
        assert set(r['candidate_batches']) == expected
    for b in batches['batches']:
        assert b['execution'] == 'NOT_RUN_IN_THIS_PACKET'
        assert set(b['related_outcomes']) <= {r['id'] for r in outcomes}
    assert ledger['new_behavior_grades'] == ledger['new_original_execution'] == 0
    return len(clauses)


def main():
    ledger = read(HERE/'route-ledger.json')
    basis = read(HERE/'route-basis.json')
    batches = read(HERE/'candidate-batches.json')
    source = (ROOT/'wiki/specs/mix-graph.md').read_text().splitlines()
    clauses = validate(ledger, basis, batches, source)
    pins = read(HERE/'pins.json')
    checked = 0
    mutable_changes = []
    for pin in pins['inputs']:
        data = (ROOT/pin['path']).read_bytes()
        matches = len(data) == pin['bytes'] and sha(data) == pin['sha256']
        if pin['kind'] == 'mutable-as-of-input' and pin['path'] != 'wiki/specs/mix-graph.md':
            if not matches:
                mutable_changes.append(pin['path'])
        else:
            assert matches, f'pin mismatch {pin["path"]}'
        checked += 1
    integration = ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/integration-structure-v1/manifest.json'
    assert sha(integration.read_bytes()) == pins['integration_manifest_sha256']
    component = integration.parent.parent/'component-resolution-v1/manifest.json'
    assert sha(component.read_bytes()) == pins['component_manifest_sha256']
    selected_paths = {p['path'] for p in pins['inputs']}
    predecessor_matches = 0
    for relative in [
        'analysis/ableton-live-12.4.3/r2/t14-mix-v1/manifest.json',
        'analysis/ableton-live-12.4.3/r2/x2-mixer-v1/manifest.json',
        'analysis/ableton-live-12.4.3/full-spec-v1/integration-structure-v1/manifest.json',
        'handoff/mix-graph-v1/manifest.json',
    ]:
        manifest = ROOT/relative
        files = read(manifest)['files']
        entries = files.items() if isinstance(files, dict) else [(x['path'], x['sha256']) for x in files]
        for relative_file, digest in entries:
            file = manifest.parent/relative_file
            if str(file.relative_to(ROOT)) in selected_paths:
                assert sha(file.read_bytes()) == digest, f'predecessor mismatch {file}'
                predecessor_matches += 1
    locators = read(HERE/'source-locators.json')['records']
    for loc in locators:
        path = ROOT/loc['path']
        with path.open('rb') as stream:
            stream.seek(loc['byte_offset'])
            row = stream.read(loc['bytes'])
        assert sha(row) == loc['retained_row_sha256']
        rec = json.loads(row)
        assert rec['record']['entry'] == loc['entry']
        assert rec['line_sha256'] == loc['original_row_sha256']
        assert sha(rec['record'].get('code', '').encode()) == loc['code_sha256']
        assert len(rec['record'].get('code', '').splitlines()) == loc['code_lines']
        assert loc['code_lines'] > 0
        assert path.read_bytes().splitlines(keepends=True)[loc['line']-1] == row
    evidence = [x for b in basis.values() for x in b['locators']]
    evidence += [x for b in batches['batches'] for x in b['input_set_locators']]
    for loc in evidence:
        path = ROOT/loc['path']
        assert path.is_file()
        if 'json_pointer' in loc:
            pointer(read(path), loc['json_pointer'])
        if 'lines' in loc:
            a, b = loc['lines']
            assert 1 <= a <= b <= len(path.read_text().splitlines())
    callsets = read(HERE/'retained-callsets.json')['sets']
    callset_rows = 0
    for batch, callset in zip(batches['batches'], callsets, strict=True):
        assert batch['id'] == callset['batch']
        assert len(callset['rows']) == batch['callset_rows']
        assert sum(bool(r['recorded_patches']) for r in callset['rows']) == batch['patched_rows']
        for loc in callset['rows']:
            with (ROOT/loc['path']).open('rb') as stream:
                stream.seek(loc['byte_offset'])
                raw = stream.read(loc['bytes'])
            assert sha(raw) == loc['sha256']
            record = json.loads(raw)
            args = record['argv']
            assert [args[n+1] for n, arg in enumerate(args) if arg == 'call'] == loc['direct_call_entries_in_order']
            assert [args[n+1] for n, arg in enumerate(args) if arg == '--patch'] == loc['recorded_patches']
            assert (record['timeout'], record['rc']) == (loc['recorded_timeout'], loc['recorded_rc'])
            if loc['recorded_patches']:
                assert loc['replay_gate'].startswith('outside-standing-')
            callset_rows += 1
    mutations = []

    def orphan_clause(trial):
        trial['outcomes'] = [r for r in trial['outcomes']
                             if r['source']['anchor'] != 'Automation override']
        trial['counts']['outcomes'] = len(trial['outcomes'])
        trial['counts']['by_route'] = dict(Counter(r['route'] for r in trial['outcomes']))

    for name, mutate in [
        ('omitted-requirement', lambda d: d.update(outcomes=[r for r in d['outcomes'] if r['requirement'] != 'REQ-MIX-GRAPH-001'])),
        ('orphaned-parent-clause', orphan_clause),
        ('duplicate-ID', lambda d: d['outcomes'].append(copy.deepcopy(d['outcomes'][0]))),
        ('bad-span', lambda d: d['outcomes'][0]['source'].update(span_sha256='0'*64)),
        ('bad-case', lambda d: d['cases'][0].update(row_sha256='0'*64)),
        ('unknown-basis', lambda d: d['outcomes'][0].update(route_basis=['invented'])),
    ]:
        trial = copy.deepcopy(ledger)
        mutate(trial)
        try:
            validate(trial, basis, batches, source)
        except AssertionError:
            mutations.append(name)
        else:
            raise AssertionError(f'failed to reject {name}')
    result = dict(status='PASS',scope='documentary integrity/completeness associations, not semantic review or behavior grades',requirements=16,parent_clauses=clauses,required_predicates=len(ledger['outcomes']),route_counts=ledger['counts']['by_route'],case_ids=34,auxiliary_records=2,input_pins=checked,selected_files_matching_predecessor_manifests=predecessor_matches,changed_mutable_context=mutable_changes,retained_source_row_locators=len(locators),retained_command_rows=callset_rows,patched_rows_require_separate_gate=36,evidence_paths_or_pointers=len(evidence),mutation_rejections=mutations,original_calls=0,new_behavior_grades=0,release_payload_edits=0)
    (HERE/'author-check-result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
