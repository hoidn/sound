#!/usr/bin/env python3
"""Documentary checks only: no original/candidate/provider/decoder execution."""
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


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def check_pin(pin):
    raw = (ROOT/pin['path']).read_bytes()
    assert (len(raw), sha(raw)) == (pin['bytes'], pin['sha256']), 'bad pin'


def pointer(value, path):
    for part in path.lstrip('/').split('/') if path else []:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def validate(ledger, bases, source):
    rows = ledger['outcomes']
    records = rows + ledger['auxiliary_clause_records']
    ids = [x['id'] for x in records]
    assert len(ids) == len(set(ids)), 'duplicate ID'
    assert {r['requirement'] for r in rows} == {f'REQ-WARP-MARKERS-{n:03}' for n in range(1, 17)}
    assert not any(r.get('helper_only') for r in rows), 'helper counted as outcome'
    assert len(rows) == ledger['counts']['required_predicates']
    assert dict(Counter(r['route'] for r in rows)) == ledger['counts']['by_route']
    for r in records:
        a, b = r['source']['lines']
        n = r['source']['anchor_line']
        assert a <= n <= b and r['source']['anchor'] in source[n-1]
        assert sha(('\n'.join(source[a-1:b])+'\n').encode()) == r['source']['span_sha256'], 'bad span'
        assert r['requirement'] in [s for s in source[:a] if s.startswith('### REQ-WARP-MARKERS-')][-1]
        assert b < source.index('## Timing and state')
    for r in rows:
        assert r['route'] in {'X', 'S', 'no-established-route'}
        assert r['basis'] and set(r['basis']) <= set(bases), 'bad basis'
        if r['route'] == 'no-established-route':
            assert r['missing_joins']
    first, last = source.index('## Requirements'), source.index('## Timing and state')
    parents = [n+1 for n in range(first, last) if source[n].startswith('- **')]
    for n in parents:
        assert any(r['source']['lines'][0] <= n <= r['source']['lines'][1] for r in records), 'orphan clause'
    cases = {s.split('|')[1].strip(): (n, s) for n, s in enumerate(source, 1) if re.match(r'\| WMK-\d{3} \|', s)}
    assert len(ledger['cases']) == len(cases) == 39
    for c in ledger['cases']:
        n, text = cases[c['id']]
        assert (n, sha((text+'\n').encode())) == (c['source_line'], c['row_sha256']), 'bad case'
        assert c['navigation_predicates'] == [r['id'] for r in rows if r['requirement'] in c['requirements']]
    assert sum(c['unresolved'] for c in ledger['cases']) == 7
    assert not any('REQ-WARP-MARKERS-009' in c['requirements'] for c in ledger['cases'])
    return len(parents)


def main():
    ledger, smap, pins, batches = [read(HERE/name) for name in ['route-ledger.json', 'source-map.json', 'pins.json', 'candidate-batches.json']]
    source = (ROOT/'wiki/specs/warp-markers.md').read_text().splitlines()
    parents = validate(ledger, smap['bases'], source)
    mutable = []
    for pin in pins['inputs']:
        if pin['kind'] == 'mutable-as-of-context' and pin['path'] != 'wiki/specs/warp-markers.md':
            raw = (ROOT/pin['path']).read_bytes()
            if (len(raw), sha(raw)) != (pin['bytes'], pin['sha256']):
                mutable.append(pin['path'])
        else:
            check_pin(pin)
    for pred in pins['predecessors']:
        assert sha((ROOT/pred['path']).read_bytes()) == pred['sha256']
    prefix = pins['protected_research_prefix']
    assert sha((ROOT/prefix['path']).read_bytes()[:prefix['bytes']]) == prefix['sha256']
    selected = {p['path'] for p in pins['inputs']}
    matches = 0
    for path in ['r2/s8-warp-v1', 'r2/d7-warp-v1', 'r2/x2-envelope-warp-v1', 'full-spec-v1/integration-structure-v1', 'full-spec-v1/family-playback-routes-v1']:
        base = ROOT/'analysis/ableton-live-12.4.3'/path
        files = read(base/'manifest.json')['files']
        entries = files.items() if isinstance(files, dict) else [(x['path'], x['sha256']) for x in files]
        for name, digest in entries:
            path = base/name
            if str(path.relative_to(ROOT)) in selected:
                raw = path.read_bytes()
                if isinstance(digest, dict):
                    assert len(raw) == digest['bytes']
                    digest = digest['sha256']
                assert sha(raw) == digest
                matches += 1
    codes = {}
    for loc in smap['records']:
        path = ROOT/loc['path']
        if loc['kind'] == 'retained-jsonl':
            with path.open('rb') as stream:
                stream.seek(loc['byte_offset'])
                raw = stream.read(loc['bytes'])
            assert sha(raw) == loc['sha256']
            assert path.read_bytes().splitlines(keepends=True)[loc['line']-1] == raw
            d = json.loads(raw)
            assert d['record']['entry'] == loc['entry'] and d['line_sha256'] == loc['original_row_sha256']
            code = d['record']['code']
        else:
            assert sha(path.read_bytes()) == loc['sha256']
            assert read(ROOT/loc['metadata_path'])['entry'] == loc['entry']
            code = path.read_text()
        assert sha(code.encode()) == loc['code_sha256']
        codes[loc['id']] = code
    for edge in smap['edges']:
        for loc in edge['source_matches']:
            line = codes[loc['record']].splitlines()[loc['C_line']-1]
            assert edge['needle'] in line and sha((line+'\n').encode()) == loc['line_sha256']
    for basis in smap['bases'].values():
        assert set(basis['records']) <= set(codes)
        for loc in basis['sources']:
            assert (ROOT/loc['path']).is_file()
            if 'pointer' in loc:
                pointer(read(ROOT/loc['path']), loc['pointer'])
    result_rows = raw_rows = 0
    for b in batches['batches']:
        count = sum(len(pointer(read(ROOT/x['path']), x['pointer'])) for x in b['result_locators'])
        assert count == b['result_rows']
        assert b['related_predicates'] == [r['id'] for r in ledger['outcomes'] if b['id'] in r['candidate_batches']]
        result_rows += count
        for loc in b['raw_rows']:
            with (ROOT/loc['path']).open('rb') as stream:
                stream.seek(loc['byte_offset'])
                raw = stream.read(loc['bytes'])
            assert sha(raw) == loc['sha256']
            row = json.loads(raw)
            args = row['argv']
            assert [args[n+1] for n, x in enumerate(args) if x == 'call'] == loc['calls']
            assert (row['label'], row['rc'], row['timeout']) == (loc['label'], loc['rc'], loc['timeout'])
            if b['id'] == 'WPB-03':
                assert loc['gate'].startswith('outside-standing-')
            raw_rows += 1
    gaps = read(HERE/'scope-gaps.json')['gaps']
    for gap in gaps:
        if 'source_line' in gap:
            assert sha((source[gap['source_line']-1]+'\n').encode()) == gap['source_sha256']

    def orphan(trial):
        trial['outcomes'] = [r for r in trial['outcomes'] if r['source']['anchor'] != 'What the user sees']
        trial['counts']['required_predicates'] = len(trial['outcomes'])
        trial['counts']['by_route'] = dict(Counter(r['route'] for r in trial['outcomes']))

    controls = []
    for name, mutate in [('bad-span', lambda d: d['outcomes'][0]['source'].update(span_sha256='0'*64)), ('orphan-clause', orphan), ('duplicate-ID', lambda d: d['outcomes'].append(copy.deepcopy(d['outcomes'][0]))), ('helper-only-count', lambda d: d['outcomes'][0].update(helper_only=True)), ('bad-basis', lambda d: d['outcomes'][0].update(basis=['invented'])), ('bad-case', lambda d: d['cases'][0].update(row_sha256='0'*64))]:
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
    result = dict(status='PASS-author-documentary-checks-only',required_predicates=len(ledger['outcomes']),routes=ledger['counts']['by_route'],requirements=16,parent_clauses=parents,cases=39,auxiliary=21,scope_gaps=len(gaps),pins=len(pins['inputs']),selected_predecessor_payload_matches=matches,changed_mutable_context=mutable,source_records=len(codes),source_edges=len(smap['edges']),candidate_batches=3,historical_result_rows=result_rows,raw_command_rows=raw_rows,protected_research_prefix_bytes=prefix['bytes'],controls=controls,new_original_calls=0,new_behavior_grades=0,limits='No independent semantic review or original/candidate execution;no complete predecessor replay;no public scripting,save or audio proof.')
    (HERE/'author-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
