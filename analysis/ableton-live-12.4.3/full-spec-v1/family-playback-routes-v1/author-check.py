#!/usr/bin/env python3
"""Read-only source/ledger checks. Runs no retained driver or original code."""
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def pointer(value, path):
    if not path:
        return value
    assert path.startswith('/'), path
    for part in path[1:].split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def verify_bytes(data, expected):
    assert len(data) == expected['bytes'], expected
    assert digest(data) == expected['sha256'], expected


def locator(record):
    path = Path(record['path'])
    if not path.is_absolute():
        path = ROOT / path
    with path.open('rb') as stream:
        stream.seek(record['byte_offset'])
        raw = stream.read(record['raw_bytes'])
    assert digest(raw) == record['raw_sha256'], record
    return json.loads(raw)


# Small owned controls: broken digest and missing pointers must not pass.
verify_bytes(b'abc', {'bytes': 3, 'sha256': digest(b'abc')})
try:
    verify_bytes(b'bad', {'bytes': 3, 'sha256': digest(b'abc')})
except AssertionError:
    pass
else:
    raise AssertionError('corrupted bytes accepted')
assert pointer({'a/b': [{'~x': 7}]}, '/a~1b/0/~0x') == 7
try:
    pointer({'a': []}, '/a/0')
except IndexError:
    pass
else:
    raise AssertionError('absent pointer accepted')

pins = read_json(HERE / 'source-pins.json')
for pin in pins['pins']:
    verify_bytes((ROOT / pin['path']).read_bytes(), pin)
rp = pins['canonical_research_prefix']
research = (ROOT / rp['path']).read_bytes()
verify_bytes(research[:rp['bytes']], rp)
assert b'## Bounded playback route inventory' in research[rp['bytes']:]
led = read_json(HERE / 'route-ledger.json')
verify_bytes((ROOT / led['owner']['path']).read_bytes(), led['owner'])
assert led['predecessor_manifest']['sha256'] == '7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83'
assert digest((ROOT / led['predecessor_manifest']['path']).read_bytes()) == led['predecessor_manifest']['sha256']
review = read_json(ROOT / 'analysis/ableton-live-12.4.3/full-spec-v1/reviews/integration-structure-v1-review.json')
assert review['disposition'] == 'approved-bounded-integration-structure'
assert review['reviewed_manifest']['sha256'] == led['predecessor_manifest']['sha256']

outcomes = led['outcomes']
ids = {o['id'] for o in outcomes}
assert len(ids) == len(outcomes) == led['required_outcomes_enumerated'] == 243
counts = dict(Counter(o['route'] for o in outcomes))
assert counts == led['counts_inventory_only']
assert counts == {'X-route': 43, 'S-route': 69, 'no-established-route': 131}
assert {o['requirement'] for o in outcomes} == {f'REQ-PLAYBACK-CORE-{n:03}' for n in range(1, 24)}
owner = (ROOT / led['owner']['path']).read_text().splitlines()
for o in outcomes:
    a, b = o['source_span']['lines']
    assert owner[a-1].startswith('### ' + o['requirement'] + ' ')
    assert b > a
    assert o['observable'] and o['missing_join_or_reason'] and o['owner_U_treatment']
    assert o['route_is_grade'] is False
    if o['route'] == 'no-established-route':
        assert o['unresolved_enumeration']
        assert all('partial' in x['role'] for x in o['enumerable_batch_links'])
    for e in o['route_evidence']:
        assert (ROOT / e['path']).is_file()
        if 'pointer' in e:
            pointer(read_json(ROOT / e['path']), e['pointer'])
    c = o['existing_case_links']
    pointer(read_json(ROOT / c['path']), c['pointer'])

aliases = led['cross_references_not_counted']
assert len(aliases) == 8
assert all(x['outcome'] in ids and x['clause_id'] not in ids for x in aliases)
clauses = list(csv.DictReader((HERE / 'outcomes.tsv').open(), delimiter='\t'))
assert len(clauses) == 251
assert {r['clause_id'] for r in clauses} == ids | {r['clause_id'] for r in aliases}
assert sum(r['counted'] == 'true' for r in clauses) == 243
assert all(r['ledger_outcome'] in ids for r in clauses)

sources = read_json(HERE / 'source-map.json')
assert set(sources) == {f'{n:03}' for n in range(1, 24)}
seen = set()
for v in sources.values():
    assert v['retained_locators'], v
    for r in v['retained_locators']:
        key = (r['path'], r['byte_offset'], r['raw_sha256'])
        if key in seen:
            continue
        row = locator(r)
        rec = pointer(row, r['record_pointer'])
        assert rec['entry'] == r['entry']
        if r['C_available']:
            code = rec['code']
            assert code and digest(code.encode()) == r['code_sha256']
            assert len(code.splitlines()) == r['code_lines'][1]
        else:
            assert r['code_lines'] is None
        seen.add(key)

comp = read_json(HERE / 'component-edges.json')
pcs = 0
index_seen = set()
for e in comp['edges']:
    assert e['exact_index_observations']
    cl = e['C_locator']
    code = pointer(read_json(ROOT / cl['path']), cl['pointer'])
    assert digest(code.encode()) == cl['code_sha256']
    assert cl['matching_lines']
    for hit in cl['matching_lines']:
        assert code.splitlines()[hit['line']-1] == hit['text']
    for obs in e['exact_index_observations']:
        original = pointer(read_json(ROOT / obs['path']), obs['pointer'])
        assert original['source'] == e['source'] and original['target'] == e['target']
        assert original['site'] == obs['native_PC']
        ir = obs['index_evidence']['locator']
        key = (ir['path'], ir['byte_offset'], ir['raw_sha256'])
        row = locator(ir)
        assert row == obs['index_evidence']['record']
        index_seen.add(key)
        pcs += 1
for e in comp['local_expression_landmarks']:
    code = pointer(read_json(ROOT / e['path']), e['pointer'])
    assert min(e['lines']) >= 1 and max(e['lines']) <= len(code.splitlines())
assert len(comp['edges']) == 14 and len(comp['unknown_edges']) == 7

batches = read_json(HERE / 'batch-inputs.json')['batches']
for b in batches:
    assert b['row_count'] == len(b['rows'])
    for row in b['rows']:
        pointer(read_json(ROOT / row['source']), row['pointer'])
assert sum(b['row_count'] for b in batches) == 703
batch_ids = {b['id'] for b in batches}
assert all(x['batch'] in batch_ids for o in outcomes for x in o['enumerable_batch_links'])

case_sets = read_json(HERE / 'case-links.json')
for cases in case_sets.values():
    for c in cases['draft']:
        assert owner[c['line']-1].startswith('| ' + c['id'] + ' |')
    for c in cases['released']:
        assert pointer(read_json(ROOT / c['path']), c['pointer'])['id'] == c['id']

# Local Markdown file links only; exact source JSON pointers checked above.
for page in [HERE / 'structure.md']:
    for target in re.findall(r'\]\(([^)]+)\)', page.read_text()):
        path = target.split('#', 1)[0]
        if path and not target.startswith(('http:', 'https:')) and path != 'author-check.json':
            assert (page.parent / path).resolve().exists(), target
result = {
    'status': 'PASS-author-mechanical-checks-only',
    'review_status': 'pending-independent-structure-review',
    'author_check_sha256': digest(Path(__file__).read_bytes()),
    'selected_source_pins': len(pins['pins']),
    'protected_canonical_research_prefix_bytes': rp['bytes'],
    'required_outcomes_inventory_only': len(outcomes),
    'route_counts_inventory_only': counts,
    'cross_references_not_counted': len(aliases),
    'distinct_retained_excerpt_rows_checked': len(seen),
    'component_edges': len(comp['edges']),
    'exact_index_PC_observation_occurrences': pcs,
    'distinct_index_rows_checked': len(index_seen),
    'unknown_component_bridges': len(comp['unknown_edges']),
    'historical_input_result_rows_not_calls_or_outcomes': 703,
    'controls': ['corrupt-digest-rejected', 'escaped-JSON-pointer-resolves', 'missing-pointer-rejected'],
    'new_original_calls': 0,
    'new_original_instruction_execution': False,
    'provider_decoder_harness_installation_candidate_execution': False,
    'normative_changes': False,
    'not_checked': 'No application/candidate/audio/file output; no full predecessor replay; no independent semantic review or frozen whole-product denominator.',
    'payload_identities': [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())}
                           for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'author-check.json'],
}
(HERE / 'author-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k:v for k,v in result.items() if k != 'payload_identities'}, indent=2))
