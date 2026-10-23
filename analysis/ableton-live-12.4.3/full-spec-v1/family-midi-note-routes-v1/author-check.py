#!/usr/bin/env python3
"""Check documentary inventory only; execute no reference/candidate function."""
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


def check_pin(pin):
    raw = (ROOT/pin['path']).read_bytes()
    assert (len(raw), sha(raw)) == (pin['bytes'], pin['sha256']), 'bad pin'


def pointer(value, path):
    for part in path.lstrip('/').split('/') if path else []:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validate(ledger, bases, source):
    outcomes = ledger['outcomes']
    records = outcomes + ledger['auxiliary_clause_records']
    ids = [r['id'] for r in records]
    assert len(ids) == len(set(ids)), 'duplicate ID'
    requirements = {f'REQ-MIDI-NOTE-STORAGE-{n:03}' for n in range(1, 18)}
    assert {r['id'] for r in ledger['requirements']} == requirements
    assert {r['requirement'] for r in records} == requirements
    assert not any(r['requirement'].endswith('-011') for r in outcomes), 'unsafe-key outcome'
    assert len(outcomes) == ledger['counts']['required_predicates']
    assert dict(Counter(r['route'] for r in outcomes)) == ledger['counts']['by_route']
    for record in records:
        first, last = record['source']['lines']
        line = record['source']['anchor_line']
        assert first <= line <= last
        assert record['source']['anchor'] in source[line-1]
        assert sha(('\n'.join(source[first-1:last])+'\n').encode()) == record['source']['span_sha256'], 'bad span'
        heading = [x for x in source[:first] if x.startswith('### REQ-MIDI-NOTE-STORAGE-')][-1]
        assert record['requirement'] in heading
    for row in outcomes:
        assert row['route'] in {'X', 'S', 'no-established-route'}
        assert row['basis'] and set(row['basis']) <= set(bases), 'unknown basis'
        if row['route'] == 'no-established-route':
            assert row['missing_joins']
    first, last = source.index('## Requirements'), source.index('## Timing and state')
    parents = [n+1 for n in range(first, last) if source[n].startswith('- **')]
    for line in parents:
        assert any(r['source']['lines'][0] <= line <= r['source']['lines'][1] for r in records), 'orphan clause'
    case_rows = {s.split('|')[1].strip(): (n, s) for n, s in enumerate(source, 1)
                 if re.match(r'\| MNS-\d{3} \|', s)}
    assert len(ledger['cases']) == len(case_rows) == 75
    assert {c['id'] for c in ledger['cases']} == set(case_rows)
    for c in ledger['cases']:
        line, text = case_rows[c['id']]
        fields = [x.strip() for x in text.strip('|').split('|')]
        assert c['source_line'] == line and c['row_sha256'] == sha((text+'\n').encode()), 'bad case'
        assert c['kind'] == fields[2]
        assert c['navigation_outcomes'] == [r['id'] for r in outcomes if r['requirement'] in c['requirements']]
        assert c['navigation_outcomes'] or c['id'] == 'MNS-037'
    assert [c['id'] for c in ledger['cases'] if c['blocked']] == [f'MNS-{n:03}' for n in range(54, 60)]
    for requirement in ledger['requirements']:
        assert requirement['outcomes'] == [r['id'] for r in outcomes if r['requirement'] == requirement['id']]
    return len(parents)


def main():
    ledger, smap, pins, batches = [read(HERE/name) for name in
        ['route-ledger.json', 'source-map.json', 'pins.json', 'candidate-batches.json']]
    source = (ROOT/'wiki/specs/midi-note-storage.md').read_text().splitlines()
    parents = validate(ledger, smap['bases'], source)
    mutable_changes = []
    for pin in pins['inputs']:
        raw = (ROOT/pin['path']).read_bytes()
        matches = (len(raw), sha(raw)) == (pin['bytes'], pin['sha256'])
        if pin['kind'] == 'mutable-as-of-context' and pin['path'] != 'wiki/specs/midi-note-storage.md':
            if not matches:
                mutable_changes.append(pin['path'])
        else:
            check_pin(pin)
    for pred in pins['predecessors']:
        assert sha((ROOT/pred['path']).read_bytes()) == pred['sha256']
    prefix = pins['protected_research_prefix']
    assert sha((ROOT/prefix['path']).read_bytes()[:prefix['bytes']]) == prefix['sha256']
    selected = {p['path'] for p in pins['inputs']}
    predecessor_matches = 0
    for path in ['r2/s7-midi-notes-v1', 'r2/x2-notes-launch-v1', 'r2/x2-transport-v1',
                 'full-spec-v1/integration-structure-v1', 'full-spec-v1/family-playback-routes-v1']:
        directory = ROOT/'analysis/ableton-live-12.4.3'/path
        files = read(directory/'manifest.json')['files']
        entries = files.items() if isinstance(files, dict) else [(x['path'], x['sha256']) for x in files]
        for relative, digest in entries:
            file = directory/relative
            if str(file.relative_to(ROOT)) in selected:
                raw = file.read_bytes()
                if isinstance(digest, dict):
                    assert len(raw) == digest['bytes']
                    digest = digest['sha256']
                assert sha(raw) == digest
                predecessor_matches += 1
    records = {}
    for loc in smap['retained_records']:
        with (ROOT/loc['path']).open('rb') as stream:
            stream.seek(loc['byte_offset'])
            raw = stream.read(loc['bytes'])
        assert sha(raw) == loc['row_sha256']
        assert (ROOT/loc['path']).read_bytes().splitlines(keepends=True)[loc['line']-1] == raw
        record = json.loads(raw)
        assert record['record']['entry'] == loc['entry']
        assert record['line_sha256'] == loc['original_row_sha256']
        code = record['record']['code']
        assert sha(code.encode()) == loc['code_sha256']
        assert len(code.splitlines()) == loc['code_lines']
        records[loc['id']] = record['record']
    for edge in smap['component_edges']:
        for loc in edge['source_matches']:
            line = records[loc['record']]['code'].splitlines()[loc['C_line']-1]
            assert edge['needle'] in line and sha((line+'\n').encode()) == loc['line_sha256']
    for basis in smap['bases'].values():
        assert set(basis['source_record_ids']) <= set(records)
        for loc in basis['sources']:
            assert (ROOT/loc['path']).is_file()
            if 'pointer' in loc:
                pointer(read(ROOT/loc['path']), loc['pointer'])
    result_rows = raw_rows = 0
    for batch in batches['batches']:
        count = 0
        assert batch['related_predicates'] == [r['id'] for r in ledger['outcomes'] if batch['id'] in r['candidate_batches']]
        for loc in batch['result_locators']:
            result = pointer(read(ROOT/loc['path']), loc['pointer'])
            count += len(result) if isinstance(result, list) else 1
        assert count == batch['retained_result_rows']
        result_rows += count
        for loc in batch['raw_command_rows']:
            with (ROOT/loc['path']).open('rb') as stream:
                stream.seek(loc['byte_offset'])
                raw = stream.read(loc['bytes'])
            assert sha(raw) == loc['sha256']
            row = json.loads(raw)
            args = row['argv']
            assert [args[n+1] for n, a in enumerate(args) if a == 'call'] == loc['calls_in_order']
            assert [args[n+1] for n, a in enumerate(args) if a == '--patch'] == loc['patches'] == []
            assert sha((row.get('gdb_script') or '').encode()) == loc['gdb_script_sha256']
            assert (row['rc'], row['timeout']) == (loc['result_rc'], loc['result_timeout'])
            raw_rows += 1
    gaps = read(HERE/'scope-gaps.json')['gaps']
    for gap in gaps:
        assert all(gap['source']['anchor'] in source[n-1] for n in gap['source']['matching_lines'])

    def orphan_clause(trial):
        trial['outcomes'] = [r for r in trial['outcomes'] if r['source']['anchor'] != 'largest finite 64-bit']
        trial['counts']['required_predicates'] = len(trial['outcomes'])
        trial['counts']['by_route'] = dict(Counter(r['route'] for r in trial['outcomes']))

    controls = []
    for name, mutate in [
        ('bad-span', lambda d: d['outcomes'][0]['source'].update(span_sha256='0'*64)),
        ('orphan-clause', orphan_clause),
        ('duplicate-ID', lambda d: d['outcomes'].append(copy.deepcopy(d['outcomes'][0]))),
        ('unsafe-key-count', lambda d: d['outcomes'][0].update(requirement='REQ-MIDI-NOTE-STORAGE-011')),
        ('unknown-basis', lambda d: d['outcomes'][0].update(basis=['invented'])),
        ('bad-case', lambda d: d['cases'][0].update(row_sha256='0'*64)),
    ]:
        trial = copy.deepcopy(ledger)
        mutate(trial)
        try:
            validate(trial, smap['bases'], source)
        except AssertionError:
            controls.append(name+'-rejected')
        else:
            raise AssertionError('mutation escaped '+name)
    bad = copy.deepcopy(pins['inputs'][0])
    bad['sha256'] = '0'*64
    try:
        check_pin(bad)
    except AssertionError:
        controls.append('bad-pin-rejected')
    else:
        raise AssertionError('bad-pin mutation escaped')
    result = dict(status='PASS-author-documentary-checks-only',required_predicates=ledger['counts']['required_predicates'],route_inventory=ledger['counts']['by_route'],requirements=17,parent_clauses=parents,cases=75,auxiliary_records=17,scope_gaps=len(gaps),pins=len(pins['inputs']),selected_predecessor_payload_matches=predecessor_matches,changed_mutable_context=mutable_changes,source_rows=len(records),source_edges=len(smap['component_edges']),candidate_batches=len(batches['batches']),historical_result_rows=result_rows,raw_command_rows=raw_rows,protected_prefix_bytes=prefix['bytes'],controls=controls,new_original_calls=0,new_behavior_grades=0,limits='No semantic independent review,application/candidate run,public load/save/player/error proof or complete unchanged predecessor/release replay.')
    (HERE/'author-check.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
