"""Validate retained analyst data only; never execute a device or candidate."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote
from collections import Counter
import gzip
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
SLUGS = ['auto-filter', 'auto-pan', 'chorus', 'erosion', 'flanger', 'frequency-shifter', 'phaser', 'redux-legacy']
KEYS = ['AUTO-FILTER', 'AUTO-PAN', 'CHORUS', 'EROSION', 'FLANGER', 'FREQUENCY-SHIFTER', 'PHASER', 'REDUX']
CLASSES = ['AutoFilter', 'AutoPan', 'Chorus', 'Erosion', 'Flanger', 'FrequencyShifter', 'Phaser', 'Redux']


def read(name):
    return json.loads((P / name).read_text())


def pin(record, base=P):
    path = base / record['path']
    data = path.read_bytes()
    assert len(data) == record['bytes'], path
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


originals = read('resumed-inputs.json')['files']
assert len(originals) == 33
for name, record in originals.items():
    pin({'path': name, **record})
sources = read('sources-r3.json')
assert len(sources) == 14 and len({s['id'] for s in sources}) == 14
source = {s['id']: s for s in sources}
for s in sources:
    data = pin(s)
    if 'original_path' in s:
        assert Path(s['original_path']).read_bytes() == data, s['id']
assert source['D11-AUDIO-EFFECTS']['sha256'] == '98a59baaa97cff409894870f26eb04697c28f8c59ecedc40ade395dcf36438d4'
assert source['D12-AUDIO-EFFECTS']['sha256'] == '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
assert source['PKG-SCHEMA']['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
catalog = json.loads(pin(source['D12-ORIGINAL-CAPTURE-CATALOG']))
assert any(r['id'] == 'D12-AUDIO-EFFECTS' and all(r[k] == source['D12-AUDIO-EFFECTS'][k] for k in ['sha256', 'url', 'capture_date', 'bytes']) for r in catalog)


class Extract(HTMLParser):
    def __init__(self, selected):
        super().__init__()
        self.selected = selected
        self.device = self.tag = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h2':
            self.device = a.get('id') if a.get('id') in self.selected else None
        if self.device and self.tag is None and tag in ['h2', 'h3', 'h4', 'p', 'li']:
            self.tag, self.buf = tag, []
            self.meta = dict(html_line=self.getpos()[0], anchor=a.get('id'), section=a.get('data-number'))

    def handle_data(self, data):
        if self.tag:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == self.tag:
            text = ' '.join(''.join(self.buf).split())
            if text:
                self.rows.append(dict(device=self.device, kind=tag, text=text, **self.meta))
            self.tag = None


parser = Extract(SLUGS + ['redux'])
parser.feed(pin(source['D11-AUDIO-EFFECTS']).decode())
locators = {}
for slug in SLUGS + ['redux']:
    rows = [r for r in parser.rows if r['device'] == slug]
    for i, row in enumerate(rows, 1):
        row['locator'] = f'{slug}:B{i:03d}'
    assert rows == read(f'manual-{slug}-blocks.json'), slug
    assert (P / f'manual-{slug}.txt').read_text() == '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n'
    locators[f'manual-{slug}-blocks.json'] = {r['locator'] for r in rows}
assert sum(len(locators[f'manual-{s}-blocks.json']) for s in SLUGS) == 114
assert len(locators['manual-redux-blocks.json']) == 15
now = Extract(SLUGS)
now.feed(pin(source['D12-AUDIO-EFFECTS']).decode())
assert [r for r in now.rows if r['device'] == 'erosion' and 'Legacy' in r['text']] == read('manual-12-erosion-migration-blocks.json')
assert read('manual-12-erosion-migration-blocks.json')[0]['html_line'] == 1144

schema_bytes = pin(source['PKG-SCHEMA'])
schema = ET.fromstring(schema_bytes)
lines = schema_bytes.decode().splitlines()
class_catalog = json.loads(pin(source['SCHEMA-CLASS-CATALOG']))['classes']
fields = read('schema-fields.json')
assert fields == [c for c in class_catalog if c['class'] in CLASSES]
assert len(fields) == 8
for c in fields:
    element = schema.find(c['class'])
    assert element is not None
    assert lines[c['line'] - 1].strip() == '<' + c['class'] + '>'
    assert c['fields'] == [dict(name=child.tag, **child.attrib) for child in element]
locators['schema-fields.json'] = {'class=' + c['class'] for c in fields}

ledger = [d for d in json.loads(pin(source['DEVICE-LEDGER-R2'])) if d['kind'] == 'legacy-native']
package = read('package-observations.json')
assert len(package) == len(ledger) == 8
assert {d['schema_class'] for d in ledger} == set(CLASSES)
scan_counts = Counter()
for r in package:
    d = next(d for d in ledger if d['id'] == r['surface'])
    assert d['schema_class'] == r['schema_class'] and d['name'] == r['name']
    preset_source = source['PKG-' + r['schema_class']]
    data = (P / r['file']).read_bytes()
    assert data == pin(preset_source)
    assert d['example']['sha256'] == hashlib.sha256(data).hexdigest()
    root = ET.fromstring(gzip.decompress(data))
    element = root.find(r['schema_class'])
    assert element is not None
    assert r['root_attributes'] == root.attrib
    assert root.attrib['Creator'] == 'Ableton Live 12.4d1'
    assert root.attrib['MinorVersion'] == '12.0_12402'
    assert r['locator'] == '/Ableton/' + r['schema_class']
    assert r['fields'] == [dict(field=c.tag, xml=ET.tostring(c, encoding='unicode')) for c in element]
    for f in r['folder_presets']:
        data = pin(f)
        scan_counts[f['parse']] += 1
        if f['parse'] == 'gzip XML':
            assert [c.tag for c in ET.fromstring(gzip.decompress(data))] == f['roots'] == [r['schema_class']]
            assert not Path(f['path']).name.startswith('._')
        else:
            assert f['parse'] == 'unknown non-gzip format; not analyzed'
            assert Path(f['path']).name.startswith('._') and not data.startswith(b'\x1f\x8b')
            assert f['roots'] is None and f['prefix_hex'] == data[:8].hex()
    folder = Path(preset_source['original_path']).parent
    assert {str(f) for f in folder.glob('*.adv')} == {f['path'] for f in r['folder_presets']}
assert scan_counts == {'gzip XML': 105, 'unknown non-gzip format; not analyzed': 105}
locators['package-observations.json'] = {'class=' + r['schema_class'] for r in package}

requirements, cases = read('requirements.json'), read('cases.json')
assert len(requirements) == 77 and len(cases) == 178
assert Counter(r['provenance'] for r in requirements) == {'D11': 45, 'Dpkg': 8, 'U': 24}
assert Counter(c['provenance'] for c in cases) == {'D11': 45, 'Dpkg': 8, 'U': 125}
counts = read('author-counts.json')
assert counts == {'requirements': 77, 'requirement_grades': dict(Counter(r['provenance'] for r in requirements)), 'cases': 178, 'case_grades': dict(Counter(c['provenance'] for c in cases))}
assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
reqmap = {r['id']: r for r in requirements}
spec = ROOT / 'wiki/specs/legacy-native-devices.md'
research = ROOT / 'wiki/research/legacy-native-devices.md'
text = spec.read_text()
assert set(re.findall(r'^### (REQ-LEG-[A-Z-]+-\d{3})', text, re.M)) == set(reqmap)
for r in requirements:
    assert '**' + r['provenance'] + '.** ' + r['text'] in text, r['id']
    if r['provenance'] == 'D11':
        assert r['text'].startswith('Live 11 predecessor only: ')
        assert 'Target 12.4.3 Legacy applicability is U.' in r['text']
        related = [c for c in cases if c['requirement'] == r['id']]
        assert len(related) == 2 and {c['provenance'] for c in related} == {'D11', 'U'}
        assert all(e.startswith('manual-') and not e.startswith('manual-redux-blocks') for e in r['evidence'])
for c in cases:
    assert c['requirement'] in reqmap and c['device'] == reqmap[c['requirement']]['device']
    assert c['setup'] and c['action'] and c['comparison']
    assert c['exact_target_expected'] is None and c['execution'].startswith('unexecuted')
    assert (c['expected'] is None) == (c['provenance'] == 'U')
    row = f"| {c['id']} | {c['requirement']} | {c['kind']} | {c['provenance']}; target U | {c['title']} |"
    assert row in text, c['id']
for r in requirements + cases:
    assert r['exact_target_applicability'] == 'unknown'
    assert r['provenance'] == 'U' or r['evidence']
    for e in r['evidence']:
        filename, locator = e.split('#')
        assert locator in locators[filename], e
for key in KEYS:
    rs = [r for r in requirements if r['device'] == key]
    cs = [c for c in cases if c['device'] == key]
    assert rs and cs
    assert {'package', 'documentary', 'positive', 'negative', 'boundary', 'migration', 'sample-rate', 'automation', 'persistence', 'undo', 'malformed', 'cancel', 'teardown', 'sidechain'} <= {c['kind'] for c in cs}, key
    assert all(any(c['requirement'] == r['id'] for c in cs) for r in rs)
    rg = Counter(r['provenance'] for r in rs)
    cg = Counter(c['provenance'] for c in cs)
    row = f"| {rs[0]['name']} | {len(rs)} | {rg['D11']} / {rg['Dpkg']} / {rg['U']} | {len(cs)} | {cg['D11']} / {cg['Dpkg']} / {cg['U']} |"
    assert row in text, key
fixtures = read('fixtures.json')
assert all(f'F{i}' in fixtures for i in range(6))
assert 'nonzero processed output' in fixtures['nonvacuity_gate']
assert 'positive control' in fixtures['nonvacuity_gate']
assert 'expected=null' in fixtures['comparison']


def slug(heading):
    heading = re.sub(r'<[^>]+>', '', heading).replace('`', '').replace('*', '').lower()
    return re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')


for page, snapshot in [(spec, 'spec-r1.md'), (research, 'research-r1.md')]:
    content = page.read_text()
    for field in ['id', 'type', 'status', 'updated', 'access']:
        assert re.search(r'^' + field + r': .+', content, re.M), (page, field)
    assert content.startswith('---\n') and '\nrevision: 1\n' in content
    assert (P / snapshot).read_bytes() == page.read_bytes()
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('http://', 'https://')):
            continue
        filename, _, anchor = unquote(target).partition('#')
        dest = (page.parent / filename).resolve() if filename else page
        assert dest.is_file(), (page, target)
        if anchor and dest.suffix == '.md':
            anchors = {slug(h) for h in re.findall(r'^#+ (.+)$', dest.read_text(), re.M)}
            assert anchor in anchors, (page, target)

manifest = read('manifest-author-r1.json')
assert manifest['canonical_snapshots'] == {'spec-r1.md': 'wiki/specs/legacy-native-devices.md', 'research-r1.md': 'wiki/research/legacy-native-devices.md'}
assert manifest['requirements'] == 77 and manifest['cases'] == 178
assert manifest['requirement_grades'] == counts['requirement_grades']
assert manifest['case_grades'] == counts['case_grades']
for name, record in manifest['files'].items():
    pin({'path': name, **record})
assert {str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f.name != manifest['filename']} == set(manifest['files'])
for path in [spec, research] + [p for p in P.rglob('*') if p.is_file() and p.suffix in {'.json', '.md', '.txt', '.py'}]:
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], text=True, capture_output=True)
    assert result.returncode in [0, 1] and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

print(json.dumps({'status': 'pass', 'scope': 'analyst author-packet integrity only', **counts, 'all_target_expected_null': True, 'pre_existing_files_unchanged': 33, 'sources': 14, 'D11_profile_blocks': 114, 'modern_Redux_context_blocks': 15, 'D12_migration_blocks': 1, 'schema_classes': 8, 'copied_presets': 8, 'external_folder_entries': 210, 'external_XML_presets': 105, 'external_unparsed_companions': 105, 'checks': ['all source pins and exemplar originals', 'independent HTML block reproduction and capture identity', 'schema class lines/fields from raw XML and catalog', 'exemplar root/field derivation and complete bounded folder re-scan', 'IDs, evidence, counts, per-device case kinds, null target oracles', 'canonical snapshots, case/count tables, local links and Markdown anchors', 'manifest coverage and hashes', 'untracked-aware whitespace'], 'limits': ['author self-check; separate semantic review required', 'no original/extracted-original/candidate execution', 'no target parity, constructor/default, DSP, migration, lifecycle or compatibility proof', 'non-gzip companion contents unparsed; broader content inventory not established']}, indent=2))
