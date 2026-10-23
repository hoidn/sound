"""Read-only analyst source/member integrity; stdout only; run with python -B."""
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
I = P.parent / 'max-api'
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows


def load(path):
    return json.loads(path.read_text())


def pin(path, record):
    data = path.read_bytes()
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


def slug(heading):
    heading = re.sub(r'<[^>]*>|[`*]', '', heading)
    return re.sub(r'[^\w\- ]', '', heading.strip().lower()).replace(' ', '-')


before = {str(f.relative_to(P)): hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*') if f.is_file()}
inputs = load(P / 'inventory-pins.json')
assert len(inputs) == 7
assert {Path(r['path']).name for r in inputs} == {'manifest-inventory-r1.json', 'all-sources-r1.json', 'reference-blocks.json', 'derive_inventory.py', 'source-page-r1.md', 'lom-entries.json', 'lom-members.json'}
for record in inputs:
    pin(ROOT / record['path'], record)
assert hashlib.sha256((I / 'manifest-inventory-r1.json').read_bytes()).hexdigest() == '67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73'
inventory = load(I / 'manifest-inventory-r1.json')
assert len(inventory['files']) == 65 and inventory['summary']['index_declares_live_version'] == '12.4.5'
for name, record in inventory['files'].items():
    pin(I / name, record)
owners = load(P / 'owner-pins.json')
assert len(owners) == 15
for record in owners:
    pin(ROOT / record['path'], record)
allentries, allmembers = load(I / 'lom-entries.json'), load(I / 'lom-members.json')
assert len(allentries) == 45 and len(allmembers) == 588
assert not any(e['name'] == 'Chain.View' for e in allentries)
entries = load(P / 'selected-entries.json')
names = ['Device', 'Device.View', 'DeviceParameter', 'MixerDevice', 'RackDevice', 'RackDevice.View', 'Chain', 'ChainMixerDevice', 'DrumChain', 'DrumPad']
assert [e['name'] for e in entries] == names
assert entries == [next(e for e in allentries if e['name'] == name) for name in names]
allsource = {s['id']: s for s in load(I / 'all-sources-r1.json')}
original_blocks = load(I / 'reference-blocks.json')
sources, blocks = load(P / 'sources.json'), load(P / 'source-blocks.json')
assert len(sources) == 10 and list(blocks) == [e['source_id'] for e in entries]
extract = runpy.run_path(str(I / 'derive_inventory.py'))['extract']
span = runpy.run_path(str(P / 'derive.py'))['member_span']
for source, entry in zip(sources, entries):
    assert source['id'] == entry['source_id'] and source['name'] == entry['name']
    assert {k: v for k, v in source.items() if k != 'retained_path'} == allsource[source['id']]
    assert source['retained_path'] == '../max-api/' + source['file']
    raw = pin(P / source['retained_path'], source)
    assert datetime.fromisoformat(source['capture_utc']).utcoffset().total_seconds() == 0
    assert '12.4.3 applicability U' in source['version']
    assert extract(raw.decode()) == original_blocks[source['id']] == blocks[source['id']]
assert sum(map(len, blocks.values())) == 315
assert (P / 'source-blocks.txt').read_text() == ''.join(f"{sid}:{b['block']} HTML{b['html_line']}:{b['html_column']} {b['tag']} {b['text']}\n" for sid, rows in blocks.items() for b in rows)
locators = {sid + ':' + b['block']: b for sid, rows in blocks.items() for b in rows}
ledger, requirements, cases = load(P / 'member-ledger.json'), load(P / 'requirements.json'), load(P / 'cases.json')
expected = [(entry, member) for entry in entries for member in allmembers if member['reference_entry'] == entry['id']]
assert len(ledger) == len(expected) == 95
assert len({r['inventory_member_id'] for r in ledger}) == 95
for row, (entry, member) in zip(ledger, expected):
    derived = span(entry, member, blocks[entry['source_id']])
    assert {k: row[k] for k in derived} == derived
    texts = ' '.join(row['source_text'][1:])
    args = [dict(name=n, type=t, optional_marker=bool(o)) for n, t, o in re.findall(r'(\w+) \[([^\]]+)\](\s*\(optional\))?', texts)] if row['category'] == 'functions' else []
    assert row['argument_declarations'] == (args or None), (row['reference_name'], row['name'])
    returns = re.search(r'Returns: \[([^\]]+)\]', texts)
    assert row['declared_function_return'] == (returns[1] if returns else None)
    unit = 'samples' if (row['reference_name'], row['name']) == ('Device', 'latency_in_samples') else 'milliseconds' if (row['reference_name'], row['name']) == ('Device', 'latency_in_ms') else None
    assert row['explicit_unit'] == unit
    assert row['target_applicability'] == 'U' and row['complete'] is False
    heading_only = row['reference_name'] == 'DrumPad' and row['name'] == 'delete_all_chains'
    assert row['documentary_mapping'] == ('declaration-only-U' if heading_only else 'bounded-direct-role')
    if heading_only:
        assert len(row['source_text']) == 1 and row['declared_type'] is None and row['argument_declarations'] is None and row['declared_function_return'] is None
assert sum(r['argument_declarations'] is not None for r in ledger) == 6
assert sum(r['declared_function_return'] is not None for r in ledger) == 2
reqmap = {r['id']: r for r in requirements}
assert len(reqmap) == len(requirements) == 103
assert Counter(r['provenance'] for r in requirements) == {'D-current-public': 94, 'U': 9}
assert len({c['id'] for c in cases}) == len(cases) == 113
assert set(reqmap) == {rid for c in cases for rid in c['requirements']}
for row in ledger:
    requirement = reqmap[row['requirement_id']]
    assert requirement['inventory_member_id'] == row['inventory_member_id']
    assert requirement['category'] == row['category']
    assert requirement['source_blocks'] == [row['source_id'] + ':' + b for b in row['source_blocks']]
    assert requirement['declaration'] == dict(type=row['declared_type'], access=row['access_roles'], arguments=row['argument_declarations'], function_return=row['declared_function_return'], explicit_unit=row['explicit_unit'])
    assert requirement['title'] == row['reference_name'] + '.' + row['name']
    assert requirement['provenance'] == ('U' if row['documentary_mapping'] == 'declaration-only-U' else 'D-current-public')
for requirement in requirements:
    assert requirement['target_applicability'] == 'U' and requirement['complete'] is False and requirement['contract']
    assert set(requirement['source_blocks']) <= locators.keys()
    if requirement['inventory_member_id'] is None:
        assert requirement['id'].startswith('REQ-LADR-U-') and requirement['provenance'] == 'U' and not requirement['source_blocks'] and requirement['declaration'] is None
for case in cases:
    assert len(case['requirements']) == 1 and case['setup_and_action'] and case['preconditions'] == ['common', 'active-positive-guard']
    requirement = reqmap[case['requirements'][0]]
    assert case['source_blocks'] == requirement['source_blocks']
    assert case['source_claim'] == (requirement['contract'] if requirement['inventory_member_id'] else None)
    assert case['documentary_expected'] is None and case['documentary_comparator'] is None
    assert case['expected'] is None and case['comparison'] is None and case['target_grade'] == 'U' and case['executed'] is False
counts = dict(selected_references=10, requested_names=11, absent_requested_names=['Chain.View'], direct_members=95,
              direct_categories=dict(Counter(r['category'] for r in ledger)), direct_documentary_roles=94,
              direct_heading_only_unknowns=1, direct_mapped_to_requirements=95, direct_unmapped_to_requirements=0,
              complete_target_members=0, requirements=103, requirement_grades=dict(Counter(r['provenance'] for r in requirements)),
              cases=113, case_kinds=dict(Counter(c['kind'] for c in cases)), documentary_oracles=0,
              null_documentary_oracles=113, retained_sources=10, retained_blocks=315, target_oracles=0)
assert counts == load(P / 'counts.json') and counts['direct_categories'] == {'children': 25, 'properties': 53, 'functions': 17}
denominator = load(P / 'denominator.json')
assert denominator['counts'] == counts and denominator['selected_names'] == names and denominator['absent_requested_names'] == ['Chain.View']
assert len(denominator['requested_names']) == 11 and denominator['global_R1_inventory'] == {'reference_entries': 45, 'direct_declarations': 588}
assert denominator['selected_references'] == [dict(name=e['name'], id=e['id'], direct_declarations=len(e['declared_members']), members=e['declared_members']) for e in entries]
assert {m for e in denominator['selected_references'] for m in e['members']} == {r['inventory_member_id'] for r in ledger}
fixtures = load(P / 'fixtures.json')
assert len(fixtures['not_provided']) == 5
assert all(s in fixtures['active-positive-guard'] for s in ['independently valid owned patch', 'initialized accepted Live/Max/API', 'positive binding', 'nonempty eligible valid source', 'nonzero', 'nonmuted', 'calibrated positive', 'Monitor/arm/receiver/clip/transport/record', 'U, never pass'])
specpath, researchpath = ROOT / 'wiki/specs/live-api-device-rack.md', ROOT / 'wiki/research/live-api-device-rack.md'
spec = specpath.read_text()
headings = re.findall(r'^### (REQ-LADR-[A-Z0-9-]+) — (.+)$', spec, re.M)
assert len(headings) == 103 and {r[0] for r in headings} == reqmap.keys()
for requirement in requirements:
    assert f"### {requirement['id']} — {requirement['title']}\n\n**{requirement['provenance']}/target-U.** {requirement['contract']}" in spec
for case in cases:
    assert f"| {case['id']} | {case['requirements'][0]} | {case['kind']} | {case['title']} |" in spec
browser = spec_rows(specpath, spec)
assert len(browser) == 103 and {r['id'] for r in browser} == reqmap.keys()
questions = load(P / 'questions.json')
assert [q['id'] for q in questions] == [f'Q-LADR-{i:03d}' for i in range(1, 10)]
for question in questions:
    assert question['id'] in spec and question['id'] in researchpath.read_text()
links = 0
for path in (specpath, researchpath):
    text = path.read_text()
    match = re.match(r'---\n(.*?)\n---\n', text, re.S)
    assert match
    metadata = dict(line.split(': ', 1) for line in match.group(1).splitlines() if ': ' in line)
    assert {'id', 'type', 'status', 'updated', 'access', 'revision', 'target'} <= metadata.keys()
    assert metadata['access'] == 'analysis' and metadata['status'] == 'draft' and metadata['revision'] == '1'
    for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)', text):
        if re.match(r'[A-Za-z]+:', target):
            continue
        name, _, fragment = target.partition('#')
        dest = (path.parent / name).resolve() if name else path
        assert dest.exists(), (path, target)
        if fragment and dest.suffix == '.md':
            assert fragment in {slug(h) for h in re.findall(r'^#+\s+(.+)$', dest.read_text(), re.M)}, (path, target)
        links += 1
manifest = load(P / 'manifest-author-r1.json')
assert manifest['counts'] == counts and len(manifest['files']) == 17
assert set(before) == set(manifest['files']) | {'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    pin(P / name, record)
assert len(manifest['canonical_snapshots']) == 2
for snapshot, canonical in manifest['canonical_snapshots'].items():
    assert (P / snapshot).read_bytes() == (ROOT / canonical).read_bytes()
for path in [specpath, researchpath, P / 'manifest-author-r1.json'] + [P / n for n in manifest['files'] if Path(n).suffix in ('.json', '.txt', '.md', '.py')]:
    if path.suffix == '.json':
        load(path)
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in (0, 1) and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
assert before == {str(f.relative_to(P)): hashlib.sha256(f.read_bytes()).hexdigest() for f in P.rglob('*') if f.is_file()}
print(json.dumps(dict(status='pass', scope='Partial analyst member/source documentation integrity only', **counts,
                      inventory_input_pins=7, immutable_inventory_R1_payloads=65, owner_tool_pins=15,
                      explicit_function_argument_declarations=6, explicit_function_returns=2,
                      frozen_payloads=17, canonical_snapshot_pairs=2, browser_ID_equality=103,
                      local_links_and_anchors=links, all_documentary_and_target_expected_comparison_null=True,
                      all_target_U_unexecuted=True, writes=False, API_Max_patch_original_candidate_execution=False), indent=2))
