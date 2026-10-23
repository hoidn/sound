#!/usr/bin/env python3
"""Read-only stdlib integrity checks; never import or execute retained studies."""
import copy
import csv
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
    if not pointer:
        return value
    assert pointer.startswith('/')
    for key in pointer[1:].split('/'):
        key = key.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def reject(call, label):
    try:
        call()
    except (AssertionError, KeyError, IndexError):
        return label
    raise AssertionError('negative fixture accepted: ' + label)


pins = read(HERE / 'source-pins.json')
for p in pins['pins']:
    verify((ROOT / p['path']).read_bytes(), p)
prefix = pins['canonical_research_prefix']
canonical = (ROOT / prefix['path']).read_bytes()
verify(canonical[:prefix['bytes']], prefix)
assert b'## Bounded Electric route inventory' in canonical[prefix['bytes']:]
ledger = read(HERE / 'route-ledger.json')
verify((ROOT / ledger['owner']['path']).read_bytes(), ledger['owner'])
owner = (ROOT / ledger['owner']['path']).read_text().splitlines()
source = read(HERE / 'sources.json')
batch = read(HERE / 'batch-inputs.json')
for c in ledger['owner_clauses'].values():
    a, b = c['lines']
    assert 1 <= a <= b <= len(owner)
    assert sha(('\n'.join(owner[a-1:b]) + '\n').encode()) == c['sha256_of_text']


def validate_rows(value):
    rows = value['rows']
    ids = [r['id'] for r in rows]
    assert len(set(ids)) == len(ids) == value['required_outcomes_enumerated'] == 181
    assert {r['requirement'] for r in rows} == {
        f'REQ-DEVICE-ELECTRIC-{n:03}' for n in range(1, 17)
    } | {'TIMING-STATE'}
    assert dict(Counter(r['route'] for r in rows)) == value['counts_inventory_only'] == {
        'X-route': 149, 'S-route': 11, 'no-established-route': 21
    }
    predicates = {(r['requirement'], r['context'], r['observable_predicate']) for r in rows}
    assert len(predicates) == len(rows)
    for r in rows:
        assert r['observable_predicate'] and r['missing_join'] and r['context']
        assert r['public_application_binding'] == 'no-established-route'
        assert r['source_span'] in value['owner_clauses']
        if r['route'] == 'X-route':
            assert 'AUX-X86-PROTOCOL' in r['auxiliary_dependencies']
        for s in r['route_evidence']:
            assert s in source['records'] or s in value['auxiliary_dependencies']
        for g in r['existing_input_groups']:
            assert g in batch['groups']
        if r['case_links_ref']:
            assert r['case_links_ref'] in value['existing_case_links']
        a, b = value['owner_clauses'][r['source_span']]['lines']
        if r['requirement'] != 'TIMING-STATE':
            heading = next(line for line in reversed(owner[:a]) if line.startswith('### REQ-'))
            assert heading.startswith('### ' + r['requirement'] + ' '), (r['id'], a, heading)
            assert not any(line.startswith('### REQ-') for line in owner[a:b]), r['id']
    for alias in value['aliases']:
        assert alias['span'] in value['owner_clauses']
        assert alias['targets'] and set(alias['targets']) <= set(ids)
    covered = set()
    for c in value['owner_clauses'].values():
        a, b = c['lines']
        covered.update(range(a, b+1))
    # Every explicit requirement bullet receives a row or an alias; this catches
    # dropped U clauses as well as positive predicates. Semantics still need review.
    required_bullets = {n for n, line in enumerate(owner, 1)
                        if 75 <= n <= 348 and re.match(r'- \*\*', line)}
    assert required_bullets <= covered, sorted(required_bullets - covered)


validate_rows(ledger)
negative = [reject(lambda: verify(b'bad', {'bytes': 3, 'sha256': sha(b'abc')}), 'corrupt-hash')]
assert at({'a/b': [{'~x': 7}]}, '/a~1b/0/~0x') == 7
negative.append(reject(lambda: at({'a': []}, '/a/0'), 'missing-pointer'))
bad = copy.deepcopy(ledger)
bad['rows'][1]['id'] = bad['rows'][0]['id']
negative.append(reject(lambda: validate_rows(bad), 'duplicate-outcome'))
bad = copy.deepcopy(ledger)
bad['rows'] = [r for r in bad['rows'] if r['requirement'] != 'REQ-DEVICE-ELECTRIC-016']
negative.append(reject(lambda: validate_rows(bad), 'omitted-unknown-requirement'))
bad = copy.deepcopy(ledger)
bad['rows'][0]['public_application_binding'] = 'X-route'
negative.append(reject(lambda: validate_rows(bad), 'fabricated-public-binding'))
bad = copy.deepcopy(ledger)
bad['rows'][0]['existing_input_groups'] = ['ABSENT']
negative.append(reject(lambda: validate_rows(bad), 'unbound-input-selector'))

for p in ledger['predecessors'] + [ledger['current_release']]:
    verify((ROOT / p['path']).read_bytes(), p)
reviews = [read(ROOT / ('analysis/ableton-live-12.4.3/full-spec-v1/reviews/' + name))
           for name in ['integration-structure-v1-review.json', 'family-mix-routes-v1-review.json']]
assert reviews[0]['disposition'] == 'approved-bounded-integration-structure'
assert reviews[1]['disposition'].startswith('approved-bounded-family-route-structure')
assert [r['reviewed_manifest']['sha256'] for r in reviews] == [p['sha256'] for p in ledger['predecessors']]
release = read(ROOT / 'handoff/device-electric-v2/manifest.json')
old = read(ROOT / 'handoff/device-electric-v1/manifest.json')
assert release['evaluation_count'] == release['case_count'] == 117
assert release['reviewer_disposition']['status'] == 'approved-editorial-supersession'
old_files = {p['path']: p for p in old['files']}
numeric = [p for p in release['files'] if p['path'] in ['compare.py', 'cases.json']
           or p['path'].startswith(('reference/', 'signals/'))]
for p in numeric:
    assert p['sha256'] == old_files[p['path']]['sha256'] and p['bytes'] == old_files[p['path']]['bytes']
# Compare manifest entries only. No full old/current signal corpus replay.
all_cases = read(ROOT / 'handoff/device-electric-v2/cases.json')['cases']
assert len(all_cases) == 117 and all(len(c['evaluations']) == 1 for c in all_cases)
for req, links in ledger['existing_case_links'].items():
    for c in links['owner_cases']:
        assert owner[c['line']-1].startswith('| ' + c['id'] + ' |')
    for c in links['release_cases']:
        evaluation = at({'cases': all_cases}, c['pointer'])
        assert evaluation['id'] == c['id']
for group in batch['groups'].values():
    value = at(read(ROOT / group['path']), group['pointer'])
    assert type(value).__name__ == group['container_kind'] and len(value) == group['count']
    if group['members'] is not None:
        assert list(value) == group['members']
assert batch['groups']['RAW']['count'] == 120 and batch['groups']['RELEASED']['count'] == 117
assert len(batch['prospective_unexecuted']) == 3

for s in source['records'].values():
    p = ROOT / s['path']
    if s['kind'] == 'original-jsonl-record':
        raw = p.read_bytes()[s['byte_offset']:s['byte_offset']+s['raw_bytes']]
        assert sha(raw) == s['raw_sha256']
        assert p.read_bytes().splitlines(keepends=True)[s['line']-1] == raw
        d = json.loads(raw)
        assert d['entry'] == s['entry']
        assert sha(d['code'].encode()) == s['code_sha256']
        assert s['C_lines'] == [1, len(d['code'].splitlines())]
        assert s['warnings'] == d.get('warnings', [])
        original = s.get('original_locator')
        if original and 'original_path' in original:
            p = Path(original['original_path'])
            raw2 = p.read_bytes()[original['original_byte_offset']:original['original_byte_offset']+original['raw_bytes']]
            assert raw == raw2 and sha(raw2) == original['raw_sha256']
    else:
        d = read(p)
        assert d['entry'] == s['entry']
        if s['companion_C']:
            assert s['C_lines'] == [1, len((ROOT / s['companion_C']).read_text().splitlines())]
for s in source['selected_call_index_rows']:
    with Path(s['path']).open('rb') as f:
        f.seek(s['byte_offset'])
        raw = f.read(s['raw_bytes'])
    assert sha(raw) == s['raw_sha256'] and json.loads(raw) == s['record']
assert len(source['records']) == 55 and len(source['selected_call_index_rows']) == 51
tsv = list(csv.DictReader((HERE / 'clauses.tsv').open(), delimiter='\t'))
assert [r['outcome'] for r in tsv] == [r['id'] for r in ledger['rows']]

# Focused changed Markdown links and whitespace, not full historical wiki replay.
links = 0
for p in [HERE / 'structure.md', ROOT / prefix['path']]:
    text = p.read_text() if p.parent == HERE else canonical[prefix['bytes']:].decode()
    for target in re.findall(r'\]\(([^)]+)\)', text):
        if '://' in target or target.startswith('#'):
            continue
        assert (p.parent / target.split('#')[0]).resolve().exists(), target
        links += 1
for p in HERE.iterdir():
    if p.is_file() and p.suffix in ['.md', '.py', '.tsv', '.json'] and not p.name.startswith('.'):
        assert not re.search(r'[ \t]+\n', p.read_text()), p
payloads = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}
            for p in sorted(HERE.iterdir()) if p.is_file() and not p.name.startswith('.')
            and p.name not in ['author-check.json', 'manifest.json']]
result = {'status': 'PASS-author-integrity-only-pending-independent-review',
          'required_outcomes': len(ledger['rows']), 'route_inventory_not_grades': ledger['counts_inventory_only'],
          'owner_spans': len(ledger['owner_clauses']), 'selected_source_entries': len(source['records']),
          'selected_call_index_rows': len(source['selected_call_index_rows']),
          'source_pins': len(pins['pins']), 'negative_fixtures_rejected': negative,
          'valid_escaped_pointer': 'accepted', 'canonical_prefix': prefix,
          'finite_release_evaluations': 117, 'numerical_manifest_entries_equal_v1': len(numeric),
          'markdown_links_checked': links, 'payloads': payloads,
          'original_provider_decoder_harness_candidate_or_measurement_executed': False,
          'full_previous_corpus_or_release_payload_replay': False,
          'limitations': 'Integrity is not independent semantic review. Existing grades/U and application joins unchanged.'}
(HERE / 'author-check.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['payloads', 'canonical_prefix']}, indent=2))
