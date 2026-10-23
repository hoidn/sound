#!/usr/bin/env python3
"""Check retained data only; never import/run original study drivers."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def at(value, pointer):
    if not pointer:
        return value
    assert pointer.startswith('/')
    for part in pointer[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def verify(data, identity):
    assert len(data) == identity['bytes'] and sha(data) == identity['sha256'], identity


# Owned rejection controls protect the check, not original behavior.
verify(b'abc', {'bytes': 3, 'sha256': sha(b'abc')})
try:
    verify(b'bad', {'bytes': 3, 'sha256': sha(b'abc')})
except AssertionError:
    pass
else:
    raise AssertionError('corrupt source accepted')
assert at({'a/b': [{'~x': 9}]}, '/a~1b/0/~0x') == 9
try:
    at({'a': []}, '/a/0')
except IndexError:
    pass
else:
    raise AssertionError('missing pointer accepted')

pins = read(HERE / 'source-pins.json')
for p in pins['pins']:
    verify((ROOT / p['path']).read_bytes(), p)
prefix = pins['canonical_research_prefix']
wiki = (ROOT / prefix['path']).read_bytes()
verify(wiki[:prefix['bytes']], prefix)
assert b'## Bounded clip-launch route inventory' in wiki[prefix['bytes']:]
led = read(HERE / 'route-ledger.json')
verify((ROOT / led['owner']['path']).read_bytes(), led['owner'])
for p in led['predecessors']:
    assert sha((ROOT / p['path']).read_bytes()) == p['sha256']
review = read(ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/reviews/integration-structure-v1-review.json')
assert review['disposition'] == 'approved-bounded-integration-structure'
assert review['reviewed_manifest']['sha256'] == led['predecessors'][0]['sha256']
rows = led['rows']
ids = {r['id'] for r in rows}
assert len(ids) == len(rows) == led['required_outcomes_enumerated'] == 229
counts = dict(Counter(r['route'] for r in rows))
assert counts == led['counts_inventory_only'] == {'X-route': 21, 'S-route': 98, 'no-established-route': 110}
assert {r['requirement'] for r in rows} == {f'REQ-CLIP-LAUNCH-{n:03}' for n in range(1, 24)}
owner_lines = (ROOT / led['owner']['path']).read_text().splitlines()
sources = read(HERE / 'sources.json')
for r in rows:
    a, b = r['source_span']['lines']
    assert owner_lines[a-1].startswith('### ' + r['requirement'] + ' ') and b > a
    assert r['context'] in led['contexts'] and r['missing_join'] in led['join_catalog']
    assert r['grade_effect'].startswith('none')
    assert r['observable']
    at(sources, r['route_evidence'].split('#', 1)[1])
    at(led, r['existing_cases'].split('#', 1)[1])
    if r['route'] == 'no-established-route':
        assert r['unresolved_enumeration']
assert next(r for r in rows if r['missing_join'] == 'enabled')['route'] == 'no-established-route'
clauses = list(csv.DictReader((HERE / 'clauses.tsv').open(), delimiter='\t'))
assert len(clauses) == led['clause_formulations'] == 230
aliases = led['cross_references_not_counted']
assert len(aliases) == 1 and len(aliases[0]['targets']) == 3
assert aliases[0]['clause_id'] not in ids and set(aliases[0]['targets']) <= ids
assert sum(c['counted'] == 'true' for c in clauses) == 229
assert {c['id'] for c in clauses} == ids | {a['clause_id'] for a in aliases}

code_rows = 0
null_c = []
for ident, s in sources['functions'].items():
    p = ROOT / s['path']
    if s['kind'] == 'retained-C1-row':
        with p.open('rb') as stream:
            stream.seek(s['byte_offset'])
            raw = stream.read(s['raw_bytes'])
        assert sha(raw) == s['raw_sha256']
        rec = at(json.loads(raw), s['record_pointer'])
        assert rec['entry'] == s['entry']
        if s['C_available']:
            assert rec['code'] and sha(rec['code'].encode()) == s['code_sha256']
            assert len(rec['code'].splitlines()) == s['C_lines'][1]
        else:
            assert not rec.get('code') and s['C_lines'] is None
            null_c.append(ident)
        code_rows += 1
    elif s['kind'] == 'retained-dossier':
        d = read(p)
        assert d['entry'] == s['entry']
        assert len(at(d, s['disassembly_pointer'])) == s['instruction_rows']
        if s['C_available']:
            assert len((ROOT / s['C_path']).read_text().splitlines()) == s['C_lines'][1]
        else:
            assert s['C_path'] is None and s['C_lines'] is None
            null_c.append(ident)
    else:
        assert s['kind'] == 'retained-x86-disassembly'
        a, b = s['lines']
        ls = p.read_text().splitlines()
        assert ls[a-1].startswith('### ' + s['entry'] + ' ') and a <= b <= len(ls)
        assert s['C_available'] is False and s['C_lines'] is None
assert len(null_c) == 2
assert {sources['functions'][i]['entry'] for i in null_c} == {'0x103abc6e8'}
for r in sources['requirements'].values():
    assert all(i in sources['functions'] for i in r['C_sources'] + r['other_evidence'])
    assert r['spec_appendix_lines']
    for p in r.get('schema_data', []):
        at(read(ROOT / p['path']), p['pointer'])
for e in sources['local_call_edges']:
    ref = at(read(ROOT / e['source_path']), e['source_pointer'])
    assert ref['from'] == e['native_PC'] and ref['to'] == e['target'] and ref['type'] == e['reference_kind']
    if e['C_path']:
        ls = (ROOT / e['C_path']).read_text().splitlines()
        assert e['C_matching_lines']
        for h in e['C_matching_lines']:
            assert ls[h['line']-1] == h['text']
assert len(sources['local_call_edges']) == 10
integ = sources['integration_edges']
for p in integ['pointers']:
    e = at(read(ROOT / integ['path']), p)
    assert e['index_locator']['line'] and e['source_code_locator']['matching_lines']
same = sources['integration_same_record']
ls = at(read(ROOT / same['path']), same['pointer']).splitlines()
assert all('auStack_140' in ls[n-1] for n in same['lines'])

batch = read(HERE / 'batch-inputs.json')
for s in batch['sets']:
    assert len(at(read(ROOT / s['path']), s['pointer'])) == s['rows']
assert sum(s['rows'] for s in batch['sets']) == batch['total_rows_not_calls_or_outcomes'] == 11756
batch_ids = {s['id'] for s in batch['sets']}
assert all(set(r['batch_inputs']) <= batch_ids for r in rows)
old_follow = read(ROOT / 'analysis/ableton-live-12.4.3/r2/x2-notes-launch-v1/results/follow.json')['follow_time']
old_hex = {r['input']['hex'] for r in old_follow}
assert all(v['value']['hex'] not in old_hex for v in batch['prospective_vectors'][0]['inputs'])

released = read(ROOT / led['case_paths']['release'])
assert len(released['cases']) == 100
for cases in led['cases_by_requirement'].values():
    for c in cases['draft']:
        assert owner_lines[c['line']-1].startswith('| ' + c['id'] + ' |')
    for c in cases['release']:
        assert at(released, c['pointer'])['id'] == c['id']
for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
    path, _, anchor = target.partition('#')
    if path == 'author-check.json':
        continue
    dest = (HERE / path).resolve()
    assert dest.exists(), target
    if anchor and dest.suffix == '.md':
        heads = [re.sub(r'[^\w\- ]', '', line.lstrip('#').strip().lower()).replace(' ', '-')
                 for line in dest.read_text().splitlines() if line.startswith('#')]
        assert anchor in heads, target
for p in HERE.iterdir():
    if p.is_file():
        assert all(line == line.rstrip() for line in p.read_text().splitlines()), p.name
result = {
    'status': 'PASS-author-mechanical-checks-only',
    'review_status': 'pending-independent-structure-review',
    'author_check_sha256': sha(Path(__file__).read_bytes()),
    'selected_source_pins': len(pins['pins']),
    'protected_research_prefix_bytes': prefix['bytes'],
    'required_outcomes_inventory_only': 229,
    'route_counts_inventory_only': counts,
    'clause_formulations': 230,
    'cross_reference_clauses_not_counted': 1,
    'source_catalog_entries': len(sources['functions']),
    'retained_excerpt_rows_checked': code_rows,
    'unavailable_C_entries_preserved': null_c,
    'exact_retained_dossier_call_PCs': 10,
    'inherited_integration_edge_pointers': len(integ['pointers']),
    'historical_input_result_rows_not_calls_or_outcomes': 11756,
    'prospective_input_vectors_not_executed': 4,
    'controls': ['corrupt-source-rejected', 'escaped-pointer-resolves', 'missing-pointer-rejected'],
    'new_original_calls': 0,
    'new_original_instruction_execution': False,
    'provider_decoder_harness_installation_candidate_execution': False,
    'normative_changes': False,
    'not_checked': 'No application/candidate/audio/file output, no full predecessor replay, no independent semantic approval or whole-product denominator.',
    'payload_identities': [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
                           for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'author-check.json'],
}
(HERE / 'author-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'payload_identities'}, indent=2))
