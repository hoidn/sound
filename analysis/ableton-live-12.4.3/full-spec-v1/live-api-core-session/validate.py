"""Read-only analyst integrity checks; no API, Max, examples or patch execution."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib
import json
import re
import runpy
import subprocess
import sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
ORIGIN = P.parent / 'max-api'
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    raw = path.read_bytes()
    assert len(raw) == record['bytes'] and hashlib.sha256(raw).hexdigest() == record['sha256'], path
    return raw


inventory_pins = load(P / 'inventory-pins.json')
assert len(inventory_pins) == 7
for record in inventory_pins:
    pin(ROOT / record['path'], record)
assert hashlib.sha256((ORIGIN / 'manifest-inventory-r1.json').read_bytes()).hexdigest() == '67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73'
original_manifest = load(ORIGIN / 'manifest-inventory-r1.json')
assert len(original_manifest['files']) == 65
for name, record in original_manifest['files'].items():
    pin(ORIGIN / name, record)
assert original_manifest['summary']['index_declares_live_version'] == '12.4.5'
original_blocks = load(ORIGIN / 'reference-blocks.json')
original_sources = {s['id']: s for s in load(ORIGIN / 'all-sources-r1.json')}
entries = load(ORIGIN / 'lom-entries.json')
members = load(ORIGIN / 'lom-members.json')
names = ['Application', 'Application.View', 'Song', 'Song.View', 'Track', 'Track.View', 'Scene', 'ClipSlot', 'CuePoint', 'TakeLane']
selected = [next(e for e in entries if e['name'] == n) for n in names]
selected_members = [m for e in selected for m in members if m['reference_entry'] == e['id']]
assert len(selected_members) == len({m['id'] for m in selected_members}) == 226
extract = runpy.run_path(str(ORIGIN / 'derive_inventory.py'))['extract']
sources, blocks = load(P / 'sources.json'), load(P / 'source-blocks.json')
assert len(sources) == len(blocks) == 10
assert [s['name'] for s in sources] == names
locators = {}
for source, e in zip(sources, selected):
    assert {k: v for k, v in source.items() if k != 'retained_path'} == original_sources[e['source_id']]
    assert source['retained_path'] == '../max-api/' + source['file']
    assert datetime.fromisoformat(source['capture_utc']).utcoffset().total_seconds() == 0
    raw = pin(P / source['retained_path'], source)
    assert extract(raw.decode()) == original_blocks[source['id']] == blocks[source['id']]
    for row in blocks[source['id']]:
        locators[source['id'] + ':' + row['block']] = row
assert len(locators) == 659
assert (P / 'source-blocks.txt').read_text() == ''.join(f"{sid}:{r['block']} HTML:{r['html_line']}:{r['html_column']} {r['tag']} {r['text']}".rstrip() + '\n' for sid, rows in blocks.items() for r in rows)
owner_pins = load(P / 'owner-pins.json')
assert len(owner_pins) == 24
for record in owner_pins:
    pin(ROOT / record['path'], record)

rs, cs, ledger, denominator, counts = [load(P / (n + '.json')) for n in ['requirements', 'cases', 'member-ledger', 'denominator', 'counts']]
reqmap = {r['id']: r for r in rs}
casemap = {c['id']: c for c in cs}
assert len(rs) == len(reqmap) == 234
assert Counter(r['provenance'] for r in rs) == {'D-current-public': 226, 'U': 8}
assert len(cs) == len(casemap) == 262
assert len(ledger) == 226
assert [r['inventory_member'] for r in ledger] == selected_members
for m, mapped in zip(selected_members, ledger):
    r = reqmap[mapped['requirement']]
    assert r['member'] == m['id'] and r['category'] == m['category']
    e = next(e for e in selected if e['id'] == m['reference_entry'])
    assert r['title'] == e['name'] + '.' + m['anchor'] and r['section'] == e['name']
    assert r['source_member_url'] == m['url']
    rows = blocks[e['source_id']]
    start = next(i for i, row in enumerate(rows) if row['block'] == m['block'])
    end = next((i for i in range(start + 1, len(rows)) if rows[i]['tag'] in ('h2', 'h3')), len(rows))
    section = rows[start:end]
    assert section[0]['tag'] == 'h3' and section[0]['anchor'] == m['anchor']
    assert section[0]['html_line'] == m['html_line'] and section[0]['html_column'] == m['html_column']
    assert r['source_blocks'] == [e['source_id'] + ':' + row['block'] for row in [rows[1], rows[3]] + section]
    expected_context = dict(description=rows[1]['text'], canonical_path=rows[3]['text'], source_blocks=[e['source_id'] + ':' + rows[i]['block'] for i in [1, 3]])
    assert r['class_context'] == mapped['class_context'] == expected_context
    desc = [b for b in section[1:] if b['text'] and not b['text'].startswith('Access:')]
    assert mapped['description_blocks'] == [e['source_id'] + ':' + b['block'] for b in desc]
    body = ' '.join(b['text'] for b in desc)
    if body:
        assert 'Publisher member description: ' + body in r['contract']
    else:
        assert 'no-member-description-beyond-heading-access' in r['unknown_fields']
    s = r['signature']
    assert s == mapped['signature']
    assert s['value_type'] == (m['heading'][len(m['anchor']):].strip() or None)
    assert s['return_source_text'] == (body.split('Returns:', 1)[1] if 'Returns:' in body else None)
    if m['category'] != 'functions':
        assert s['arguments'] is None and s['result_type'] == s['value_type']
        assert s['access'] == [a for a in ['get', 'set', 'observe'] if any(b['text'].startswith('Access:') and a in b['text'] for b in section)]
    else:
        assert s['value_type'] is None and s['access'] is None
        if s['result_type'] is not None:
            assert 'Returns:' in body and s['result_type'] in body
        if s['arguments'] is None:
            assert not body.startswith(('Parameter:', 'Parameters:', 'Parameter (optional):'))
            assert 'argument-list-not-stated-not-proved-empty' in r['unknown_fields']
        else:
            assert body.startswith(('Parameter:', 'Parameters:', 'Parameter (optional):'))
            positions = []
            for a in s['arguments']:
                assert set(a) == {'name', 'type', 'optional', 'source_default'}
                assert a['name'] in body
                positions.append(body.index(a['name']))
                if a['type'] is not None:
                    assert '[' + a['type'] + ']' in body
                assert a['optional'] in (True, None)
                if a['optional'] is True:
                    assert 'optional' in body
                if a['source_default'] is not None:
                    assert 'default' in body and a['source_default'] in body
            assert positions == sorted(positions)
    assert mapped['unknown_fields'] == r['unknown_fields'] and len(r['unknown_fields']) >= 3
    assert mapped['mapping'] == 'documentary-direct-member-mapped' and mapped['complete'] is False and mapped['target_applicability'] == 'U'
    assert mapped['cases'] == r['cases']
    assert any(casemap[c]['kind'] == 'member-positive' for c in mapped['cases'])
for r in rs:
    assert r['target_applicability'] == 'U' and r['contract']
    assert all(ref in locators for ref in r['source_blocks'])
    assert bool(r['source_blocks']) == (r['provenance'] == 'D-current-public')
    assert r['cases'] == [c['id'] for c in cs if r['id'] in c['requirements']]
for c in cs:
    assert len(c['requirements']) == 1 and c['setup_and_action']
    r = reqmap[c['requirements'][0]]
    assert c['source_blocks'] == r['source_blocks']
    assert c['source_claim'] == (r['contract'] if r['provenance'] == 'D-current-public' else None)
    assert c['member'] == r.get('member')
    assert c['preconditions'] == ['common', 'active-positive-guard', 'values', 'destructive-isolation']
    assert c['documentary_expected'] is None and c['documentary_comparator'] is None
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
assert {rid for c in cs for rid in c['requirements']} == set(reqmap)
assert counts == dict(requirements=234, requirement_grades=dict(Counter(r['provenance'] for r in rs)), cases=262, case_kinds=dict(Counter(c['kind'] for c in cs)), documentary_oracles=0, null_documentary_oracles=262, target_oracles=0, sources=10, source_blocks=659, mapped_direct_members=226, unmapped_family_direct_members=0, unknown_members=226, complete_members=0)
assert denominator['global_reference_entries'] == len(entries) == 45
assert denominator['global_direct_members'] == len(members) == 588
assert denominator['mapped_direct_members'] == denominator['selected_direct_members'] == 226
assert denominator['selected_unmapped_direct_members'] == 0 and denominator['outside_family_direct_members'] == 362
assert denominator['selected_reference_entries'] == 10 and denominator['outside_family_reference_entries'] == 35
assert denominator['complete_members'] == denominator['complete_entries'] == denominator['target_applicable_members'] == 0
assert denominator['selected_categories'] == {'children': 30, 'properties': 123, 'functions': 73}
for e, item in zip(selected, denominator['classes']):
    assert item == dict(name=e['name'], inventory_entry=e['id'], direct_members=len(e['declared_members']), mapped=len(e['declared_members']), unmapped=0, unknown_members=len(e['declared_members']), complete=False)
assert {'negative', 'boundary', 'source-context', 'malformed', 'version', 'persistence', 'timing', 'recovery', 'undo', 'cancel', 'source-loss', 'teardown', 'automation', 'sample-rate', 'transport', 'concurrency'} <= {c['kind'] for c in cs}
fixtures = load(P / 'fixtures.json')
assert {'common', 'active-positive-guard', 'values', 'observation', 'destructive-isolation', 'not-provided'} == set(fixtures)
assert all(phrase in fixtures['active-positive-guard'] for phrase in ['independently valid owned patch', 'available initialized Live/Max/API context', 'matched positive baseline', 'nonzero', 'nonmuted', 'remain U'])

specpath = ROOT / 'wiki/specs/live-api-core-session.md'
researchpath = ROOT / 'wiki/research/live-api-core-session.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-LAPI-CORE-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 234 and {h[0] for h in headings} == set(reqmap)
for r in rs:
    assert f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}" in spec
    assert all(c in spec for c in r['cases'])
browser = spec_rows(specpath, spec)
assert len(browser) == 234 and {r['id'] for r in browser} == set(reqmap)
assert '12.4.5' in spec and 'REQ-AUTOMATION-ENVELOPES-013' in spec and 'REQ-CLIP-LAUNCH-020/021/022/023' in spec
assert all(f'Q-LCS-{n:03d}' in researchpath.read_text() for n in range(1, 10))


def slug(value):
    return re.sub(r'[^\w\- ]', '', re.sub(r'[`*]|<[^>]*>', '', value).strip().lower()).replace(' ', '-')


links = 0
for canonical, snapshot in [(specpath, 'spec-r1.md'), (researchpath, 'research-r1.md')]:
    assert canonical.read_bytes() == (P / snapshot).read_bytes()
    value = canonical.read_text()
    meta = dict(line.split(': ', 1) for line in re.match(r'---\n(.*?)\n---\n', value, re.S).group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= meta.keys()
    assert meta['access'] == 'analysis' and meta['revision'] == '1'
    for dest in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', value):
        if re.match(r'[A-Za-z]+:', dest): continue
        name, _, fragment = dest.partition('#')
        path = (canonical.parent / name).resolve() if name else canonical
        if path == P / 'manifest-author-r1.json' and not path.exists(): continue
        assert path.exists(), (canonical, dest)
        if fragment and path.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', path.read_text(), re.M)}, dest
        links += 1
for path in [specpath, researchpath] + [f for f in P.rglob('*') if f.is_file() and f.suffix in ('.py', '.json', '.md', '.txt')]:
    if path.suffix == '.json': load(path)
    check = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert check.returncode in (0, 1) and not check.stdout and not check.stderr, (path, check.stdout, check.stderr)
manifest_path = P / 'manifest-author-r1.json'
if manifest_path.exists():
    manifest = load(manifest_path)
    assert manifest['counts'] == counts
    assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()} == set(manifest['files']) | {'manifest-author-r1.json'}
    for name, record in manifest['files'].items(): pin(P / name, record)
    assert manifest['canonical_snapshots'] == {'spec-r1.md': 'wiki/specs/live-api-core-session.md', 'research-r1.md': 'wiki/research/live-api-core-session.md'}
print(json.dumps(dict(status='pass', scope='Analyst documentary/member identity only; no runtime', **counts, original_R1_payload_pins=65, inventory_identity_pins=7, owner_and_browser_pins=24, browser_ID_equality=234, canonical_snapshots=2, local_links_and_anchors=links, sealed_manifest_checked=manifest_path.exists(), writes=False, API_or_patch_execution=False, original_execution=False, candidate_execution=False), indent=2))
