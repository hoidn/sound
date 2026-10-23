"""Read-only analyst/source retention checks; never run original audio or a host."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote
from capture import Sections, INPUTS

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
sys.path.insert(0, str(ROOT / 'tools'))
from spec_browser import spec_rows


def read(name):
    return json.loads((P / name).read_text())


def pin(r, base=P):
    path = base / r['path']
    data = path.read_bytes()
    assert len(data) == r['bytes'] and hashlib.sha256(data).hexdigest() == r['sha256'], path
    return data


sources = read('sources.json')
assert len(sources) == 4 and len({s['id'] for s in sources}) == 4
src = {s['id']: s for s in sources}
for s in sources:
    pin(s)
for source_id, catalog_id in [('SAMPLE-INSTRUMENTS-MANUAL', 'SAMPLE-INSTRUMENTS-CAPTURE-CATALOG'), ('D12-AUDIO-EFFECTS', 'AUDIO-UTILITIES-CAPTURE-CATALOG')]:
    catalog = json.loads(pin(src[catalog_id]))
    original = next(r for r in catalog if r['id'] == source_id)
    assert all(original[k] == src[source_id][k] for k in ['id', 'url', 'bytes', 'sha256'])
    for k in ['captured_utc', 'capture_date']:
        assert original.get(k) == src[source_id].get(k)
expected = {'analog': 76, 'collision': 88, 'electric': 36, 'tension': 110, 'amp': 24, 'cabinet': 18, 'corpus': 49}
locators = {}
for source, digest, devices in INPUTS:
    data = (P / source).read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest
    parser = Sections(devices)
    parser.feed(data.decode())
    for device in devices:
        rows = [r for r in parser.rows if r['device'] == device]
        assert len(rows) == expected[device] and rows[0]['anchor'] == device
        for i, r in enumerate(rows, 1):
            r['locator'] = f'{device}:B{i:03d}'
            locators[r['locator']] = r
        assert rows == read(f'manual-{device}-blocks.json')
        assert (P / f'manual-{device}.txt').read_text() == '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n'
assert len(locators) == 401

authorities = read('existing-authority-pins.json')
assert len(authorities['files']) == 22 and len(authorities['releases']) == 5
for r in authorities['files']:
    pin(r)
release_files = {}
for release in authorities['releases']:
    folder = ROOT / 'handoff' / release
    manifest = json.loads((folder / 'manifest.json').read_text())
    for record in manifest['files']:
        pin(record, folder)
    release_files[release] = len(manifest['files'])

requirements, cases, counts = read('requirements.json'), read('cases.json'), read('counts.json')
assert len(requirements) == len({r['id'] for r in requirements}) == 55
assert len(cases) == len({c['id'] for c in cases}) == 118
assert Counter(r['provenance'] for r in requirements) == {'D12': 41, 'U': 14}
reqmap = {r['id']: r for r in requirements}
assert {rid for c in cases for rid in c['requirements']} == set(reqmap)
assert counts['requirements'] == 55 and counts['cases'] == 118
assert counts['requirement_grades'] == dict(Counter(r['provenance'] for r in requirements))
assert counts['case_kinds'] == dict(Counter(c['kind'] for c in cases))
assert counts['documentary_oracles'] == sum(c['documentary_expected'] is not None for c in cases) == 33
assert counts['null_documentary_oracles'] == sum(c['documentary_expected'] is None for c in cases) == 85
for r in requirements:
    assert r['target_applicability'] == 'U'
    assert r['provenance'] == 'U' or r['source_blocks']
    assert all(b in locators for b in r['source_blocks'])
for c in cases:
    assert c['expected'] is None and c['comparison'] is None and c['target_grade'] == 'U' and c['executed'] is False
    assert c['setup_and_action'] and len(c['requirements']) == 1
    r = reqmap[c['requirements'][0]]
    assert c['device'] == r['device'] and c['source_blocks'] == r['source_blocks']
    assert c['preconditions'] == ['F0', 'positive-path-guard', r['prefix']]
    if c['kind'] == 'signal-obligation' or r['provenance'] == 'U':
        assert c['documentary_expected'] is None and c['documentary_comparator'] is None
    else:
        assert c['documentary_expected'] == r['contract']
        assert 'no waveform, timing, private-state or numerical DSP grade' in c['documentary_comparator']
for device, count in counts['per_device'].items():
    rs = [r for r in requirements if r['device'] == device]
    cs = [c for c in cases if c['device'] == device]
    assert count == {'requirements': len(rs), 'D12_requirements': sum(r['provenance'] == 'D12' for r in rs), 'U_requirements': 2, 'cases': len(cs)}
    assert {'positive', 'negative', 'boundary', 'lifecycle'} <= {c['case_class'] for c in cs}
    assert {'negative', 'boundary', 'automation', 'persistence', 'undo', 'malformed', 'cancel', 'transport', 'sample-rate', 'teardown', 'mpe-tuning'} <= {c['kind'] for c in cs}
    assert len([r for r in rs if r['provenance'] == 'U']) == 2
fixtures = read('fixtures.json')
assert len(fixtures['device_states']) == 7
assert 'matched active positive control' in fixtures['positive-path-guard']
assert 'nonzero' in fixtures['positive-path-guard'] and 'remain U' in fixtures['positive-path-guard']
assert 'blocked' in fixtures['blocked-route'] and 'fake Live identity' in fixtures['blocked-route']

spec = ROOT / 'wiki/specs/bundled-device-workflows.md'
research = ROOT / 'wiki/research/bundled-device-workflows.md'
text = spec.read_text()
assert {r['id'] for r in spec_rows(spec, text)} == set(reqmap), 'Existing requirements browser must discover exactly all new normative IDs'
assert len(spec_rows(spec, text)) == 55
for r in requirements:
    assert '**' + r['provenance'] + '/target-U.** ' + r['contract'] in text
    assert f"### {r['id']} — {r['title']}" in text
for c in cases:
    value = 'visible controls/state only' if c['documentary_expected'] is not None else 'U / null'
    assert f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {value} |" in text
for name, count in counts['per_device'].items():
    assert f"| {name} | {count['D12_requirements']} / 2 | {count['cases']} |" in text


def slug(heading):
    return re.sub(r'[^\w\- ]', '', re.sub(r'<[^>]+>', '', heading).replace('`', '').replace('*', '').lower()).replace(' ', '-')


links = 0
for page, snapshot in [(spec, 'spec-r1.md'), (research, 'research-r1.md')]:
    content = page.read_text()
    assert (P / snapshot).read_bytes() == page.read_bytes()
    assert content.startswith('---\n') and '\nrevision: 1\n' in content
    frontmatter = content.split('---', 2)[1]
    for key in ['id', 'type', 'status', 'updated', 'access']:
        assert re.search('^' + key + ': .+', frontmatter, re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('http://', 'https://')):
            continue
        filename, _, anchor = unquote(target).partition('#')
        dest = (page.parent / filename).resolve() if filename else page
        assert dest.is_file(), (page, target)
        if anchor and dest.suffix == '.md':
            assert anchor in {slug(h) for h in re.findall(r'^#+ (.+)$', dest.read_text(), re.M)}, (page, target)
        links += 1
manifest = read('manifest-author-r1.json')
assert manifest['requirements'] == 55 and manifest['cases'] == 118
for name, record in manifest['files'].items():
    pin(dict(path=name, **record))
assert set(manifest['files']) == {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name != 'manifest-author-r1.json'}
for path in [spec, research] + [f for f in P.rglob('*') if f.is_file() and f.suffix in {'.md', '.py', '.json', '.txt'}]:
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in [0, 1] and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

print(json.dumps({'status': 'pass', 'scope': 'Author analyst packet integrity and unchanged authority retention only', 'requirements': 55, 'D12_requirements': 41, 'U_requirements': 14, 'cases': 118, 'documentary_control_state_oracles': 33, 'null_documentary_signal_lifecycle_oracles': 85, 'all_target_expected_comparison_null_U_unexecuted': True, 'source_records': 4, 'manual_sources': 2, 'retained_blocks': 401, 'existing_authority_pins_unchanged': 22, 'immutable_release_payload_hashes': release_files, 'requirements_browser_exact_ID_set': 55, 'canonical_snapshots': 2, 'local_links_and_anchors': links, 'checks': ['original capture identity and exact source hashes', '401 source block texts/lines/headings reproduced', 'five immutable release payload inventories and current owner identities unchanged', 'IDs, evidence, counts, positive/negative/boundary/lifecycle coverage and null oracles', 'existing browser discovers all and only catalog normative IDs', 'canonical wording/snapshots, case/count tables, frontmatter, local links and Markdown anchors', 'complete author manifest inventory/hashes', 'untracked-aware authored whitespace'], 'limits': ['author self-check; independent semantic review remains required', 'no original/native/extracted-original/candidate/runtime/audio/hardware execution', 'Amp/Cabinet original host route blocked; no fake identity or platform shim introduced', 'no expanded finite release, numerical mode/MPE/lifecycle or compatibility proof', 'figures uninspected; future positive signal/expression fixtures not retained']}, indent=2))
