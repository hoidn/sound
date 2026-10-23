#!/usr/bin/env python3
"""Verify selected retained data and authored routing; run no original study code."""
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
    for key in pointer[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def verify(data, identity):
    assert len(data) == identity['bytes'] and sha(data) == identity['sha256'], identity


verify(b'abc', {'bytes': 3, 'sha256': sha(b'abc')})
try:
    verify(b'bad', {'bytes': 3, 'sha256': sha(b'abc')})
except AssertionError:
    pass
else:
    raise AssertionError('corrupt source accepted')
assert at({'a/b': [{'~x': 7}]}, '/a~1b/0/~0x') == 7
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
assert b'## Bounded automation-envelope route inventory' in wiki[prefix['bytes']:]
led = read(HERE / 'route-ledger.json')
verify((ROOT / led['owner']['path']).read_bytes(), led['owner'])
for p in led['predecessors']:
    assert sha((ROOT / p['path']).read_bytes()) == p['sha256']
reviews = [read(ROOT / ('analysis/ableton-live-12.4.3/full-spec-v1/reviews/' + n))
           for n in ['integration-structure-v1-review.json', 'family-mix-routes-v1-review.json']]
assert reviews[0]['disposition'] == 'approved-bounded-integration-structure'
assert reviews[1]['disposition'].startswith('approved-bounded-family-route-structure')
assert [r['reviewed_manifest']['sha256'] for r in reviews] == [p['sha256'] for p in led['predecessors']]
owner = (ROOT / led['owner']['path']).read_text().splitlines()
for c in led['owner_clauses'].values():
    a, b = c['lines']
    assert 1 <= a <= b <= len(owner)
    assert sha(('\n'.join(owner[a-1:b]) + '\n').encode()) == c['sha256_of_text']
for tag, p in led['assumption_spans'].items():
    assert owner[p['lines'][0]-1].startswith('| ' + tag + ' |')
rows = led['rows']
ids = {r['id'] for r in rows}
assert len(ids) == len(rows) == led['required_outcomes_enumerated'] == 129
assert {r['requirement'] for r in rows} == {f'REQ-AUTOMATION-ENVELOPES-{n:03}' for n in range(1, 14)}
counts = dict(Counter(r['route'] for r in rows))
assert counts == led['counts_inventory_only'] == {'X-route': 22, 'S-route': 69, 'no-established-route': 38}
source = read(HERE / 'sources.json')
used_clauses = set()
for r in rows:
    c = led['owner_clauses'][r['source_clause']]
    assert r['source_span'] == c['lines']
    assert r['observable'] and r['missing_join'] in led['join_catalog']
    assert r['context'] in led['contexts'] and r['grade_effect'].startswith('none')
    assert r['source_clause'].startswith('AE-' + r['requirement'][-3:])
    at(source, r['route_evidence'].split('#', 1)[1])
    at(led, r['existing_cases'].split('#', 1)[1])
    used_clauses.add(r['source_clause'])
    used_clauses.update(r.get('source_contexts', []))
    used_clauses.update(r.get('supporting_owner_clauses', []))
    used_clauses.update(a['clause'] for a in r.get('additional_owner_clauses', []))
    if r['route'] == 'no-established-route':
        assert r['unresolved_enumeration']
assert all(k in used_clauses or not c['accounting'].startswith('required')
           for k, c in led['owner_clauses'].items())
aliases = led['cross_references_not_counted']
assert len(aliases) == 7 and all(a['clause_id'] not in ids and set(a['targets']) <= ids for a in aliases)
clauses = list(csv.DictReader((HERE / 'clauses.tsv').open(), delimiter='\t'))
assert len(clauses) == led['clause_formulations'] == 136
assert {c['id'] for c in clauses} == ids | {a['clause_id'] for a in aliases}
assert sum(c['counted'] == 'true' for c in clauses) == 129

unavailable = []
excerpt_rows = 0
for ident, s in source['functions'].items():
    p = ROOT / s['path']
    if s['kind'] == 'retained-C1-row':
        with p.open('rb') as f:
            f.seek(s['byte_offset'])
            raw = f.read(s['raw_bytes'])
        assert sha(raw) == s['raw_sha256']
        d = at(json.loads(raw), s['record_pointer'])
        assert d['entry'] == s['entry']
        assert d.get('error') == s['export_error'] and d.get('state') == s['export_state']
        if s['C_available']:
            assert d['code'] and sha(d['code'].encode()) == s['code_sha256']
            assert len(d['code'].splitlines()) == s['C_lines'][1]
        else:
            assert not d.get('code') and s['C_lines'] is None
            unavailable.append(ident)
        excerpt_rows += 1
    else:
        assert s['kind'] == 'retained-dossier'
        d = read(p)
        assert d['entry'] == s['entry'] and len(at(d, s['disassembly_pointer'])) == s['instruction_rows']
        if s['C_available']:
            assert len((ROOT / s['C_path']).read_text().splitlines()) == s['C_lines'][1]
        else:
            assert s['C_path'] is None and s['C_lines'] is None
            unavailable.append(ident)
for s in source['requirements'].values():
    assert all(i in source['functions'] for i in s['C_sources'] + s['other_sources'])
    for p in s.get('survey_evidence', []):
        at(read(ROOT / p['path']), p['pointer'])
for e in source['local_call_edges']:
    r = at(read(ROOT / e['path']), e['pointer'])
    assert r['from'] == e['native_PC'] and r['to'] == e['target'] and r['type'] == e['reference_kind']
    if e['C_path']:
        ls = (ROOT / e['C_path']).read_text().splitlines()
        assert e['C_matching_lines']
        assert all(ls[h['line']-1] == h['text'] for h in e['C_matching_lines'])
assert len(source['local_call_edges']) == 8
for e in source['conditional_virtual_validation_edges']:
    d = at(read(ROOT / e['path']), e['instruction_pointer'])
    assert d['address'] == e['native_PC']
    ls = (ROOT / e['C_path']).read_text().splitlines()
    assert all(ls[h['line']-1] == h['text'] for h in e['C_matching_lines'])
    fact = e['retained_table_fact']
    line = (ROOT / fact['path']).read_text().splitlines()[fact['line']-1]
    assert all(v.removeprefix('0x') in line for v in [fact['target'], fact['table_operand_address']])
    assert 'No new' in e['classification']
assert len(source['conditional_virtual_validation_edges']) == 2
for p in source['inherited_mix_bases']:
    at(read(ROOT / p['path']), p['pointer'])
for key in ['integration_sender', 'integration_scheduler']:
    p = source[key]
    ls = at(read(ROOT / p['path']), p['pointer']).splitlines()
    assert min(p['lines']) > 0 and max(p['lines']) <= len(ls)

batch = read(HERE / 'batch-inputs.json')
for s in batch['sets']:
    assert s['rows_not_calls_or_outcomes'] == sum(p['rows'] for p in s['selections'])
    for p in s['selections']:
        assert len(at(read(ROOT / p['path']), p['pointer'])) == p['rows']
assert sum(s['rows_not_calls_or_outcomes'] for s in batch['sets']) == batch['total_rows_not_calls_or_outcomes'] == 80
assert len(batch['prospective_vectors'][0]['inputs']) == 6
batch_ids = {s['id'] for s in batch['sets']}
assert all(set(r['batch_inputs']) <= batch_ids for r in rows)
for p in batch['excluded_input_controls']:
    at(read(ROOT / p['path']), p['pointer'])
release = read(ROOT / led['case_paths']['release'])
assert len(release['cases']) == 21
unique_draft = set()
withdrawn = set()
for cases in led['cases_by_requirement'].values():
    for c in cases['draft']:
        line = owner[c['line']-1]
        assert line.startswith('| ' + c['id'] + ' |') and line.split('|')[-2].strip() == c['owner_basis']
        unique_draft.add(c['id'])
        if c['status'] == 'withdrawn':
            withdrawn.add(c['id'])
    for c in cases['release']:
        assert at(release, c['pointer'])['id'] == c['id']
assert len(unique_draft) == 33 and withdrawn == {'AEN-001', 'AEN-002'}
for target in re.findall(r'\]\(([^)]+)\)', (HERE / 'structure.md').read_text()):
    path = target.split('#', 1)[0]
    if path != 'author-check.json':
        assert (HERE / path).resolve().exists(), target
for p in HERE.iterdir():
    if p.is_file():
        assert all(line == line.rstrip() for line in p.read_text().splitlines()), p.name
result = {
    'status': 'PASS-author-mechanical-checks-only',
    'review_status': 'pending-independent-structure-review',
    'author_check_sha256': sha(Path(__file__).read_bytes()),
    'selected_source_pins': len(pins['pins']),
    'protected_research_prefix_bytes': prefix['bytes'],
    'required_predicates_inventory_only': len(rows),
    'route_counts_inventory_only': counts,
    'clause_formulations': 136,
    'repeated_formulations_not_counted': len(aliases),
    'owner_clause_context_spans_checked': len(led['owner_clauses']),
    'selected_source_catalog_entries': len(source['functions']),
    'retained_excerpt_rows_checked': excerpt_rows,
    'unavailable_C_entries_preserved': unavailable,
    'exact_retained_dossier_call_PCs': 8,
    'conditional_virtual_validation_sites_not_new_resolution': 2,
    'historical_value_control_point_segment_rows_not_calls_or_outcomes': 80,
    'prospective_vectors_not_executed': 6,
    'draft_case_IDs': len(unique_draft),
    'withdrawn_cases_preserved': sorted(withdrawn),
    'released_case_records_navigation_only': 21,
    'controls': ['corrupt-source-rejected', 'escaped-pointer-resolves', 'missing-pointer-rejected'],
    'new_original_calls': 0,
    'new_original_instruction_execution': False,
    'provider_decoder_harness_installation_candidate_execution': False,
    'normative_changes': False,
    'not_checked': 'No application/candidate/UI/parameter/audio/file output, no full predecessor/corpus/release replay, no independent semantic approval or whole-product denominator.',
    'payload_identities': [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
                           for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'author-check.json'],
}
(HERE / 'author-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'payload_identities'}, indent=2))
