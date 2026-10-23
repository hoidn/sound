"""Check packet integrity only; never execute original or candidate code."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import gzip
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
DEVICES = ['delay', 'echo', 'filter-delay', 'grain-delay', 'reverb', 'hybrid-reverb', 'resonators']
CLASSES = ['Delay', 'Echo', 'FilterDelay', 'GrainDelay', 'Reverb', 'Hybrid', 'Resonator']


def read(name):
    return json.loads((P / name).read_text())


def check_pin(record):
    path = Path(record['path'])
    if not path.is_absolute():
        path = P / path
    data = path.read_bytes()
    assert len(data) == record['bytes'], path
    assert hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


sources = read('sources.json')
assert len(sources) == 14
assert len({s['id'] for s in sources}) == len(sources)
for source in sources:
    data = check_pin(source)
    if 'original_path' in source:
        assert Path(source['original_path']).read_bytes() == data
manual = next(s for s in sources if s['id'] == 'D12-AUDIO-EFFECTS')
assert manual['sha256'] == '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
schema = next(s for s in sources if s['id'] == 'PKG-SCHEMA')
assert schema['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
catalog_source = next(s for s in sources if s['id'] == 'ORIGINAL-MANUAL-CAPTURE-CATALOG')
catalog = json.loads(check_pin(catalog_source))
assert any(s['id'] == manual['id'] and s['sha256'] == manual['sha256'] and s['url'] == manual['url'] and s['capture_date'] == manual['capture_date'] for s in catalog)


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.device = None
        self.tag = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.device = attrs.get('id') if attrs.get('id') in DEVICES else None
        if self.device and tag in ['h2', 'h3', 'h4', 'p', 'li'] and self.tag is None:
            self.tag = tag
            self.text = []
            self.meta = {'html_line': self.getpos()[0], 'anchor': attrs.get('id'), 'section': attrs.get('data-number')}

    def handle_data(self, data):
        if self.tag:
            self.text.append(data)

    def handle_endtag(self, tag):
        if self.tag == tag:
            content = ' '.join(''.join(self.text).split())
            if content:
                self.rows.append({'device': self.device, 'kind': tag, 'text': content, **self.meta})
            self.tag = None


parser = Blocks()
parser.feed(check_pin(manual).decode())
locators = {}
for device in DEVICES:
    rows = [r for r in parser.rows if r['device'] == device]
    for i, row in enumerate(rows, 1):
        row['locator'] = f'{device}:B{i:03d}'
    assert rows == read(f'manual-{device}-blocks.json'), device
    assert (P / f'manual-{device}.txt').read_text() == '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n'
    locators[f'manual-{device}-blocks.json'] = {r['locator'] for r in rows}
assert len(parser.rows) == 207

class_input = next(s for s in sources if s['id'] == 'INVENTORY-SCHEMA-CLASSES')
classes = json.loads(check_pin(class_input))['classes']
assert read('schema-fields.json') == [r for r in classes if r['class'] in CLASSES]
assert len(read('schema-fields.json')) == 7
package = read('package-values.json')
assert len(package) == 7
for record in package:
    root = ET.fromstring(gzip.decompress((P / record['file']).read_bytes()))
    element = root.find(record['class'])
    assert element is not None
    assert root.attrib == record['root_attributes']
    assert root.attrib['Creator'] == 'Ableton Live 12.4d1'
    assert root.attrib['MinorVersion'] == '12.0_12402'
    assert record['locator'] == '/Ableton/' + record['class']
    assert record['fields'] == [{'field': c.tag, 'xml': ET.tostring(c, encoding='unicode')} for c in element]
locators['package-values.json'] = {r['surface'] for r in package}

requirements = read('requirements.json')
cases = read('cases.json')
assert len(requirements) == 92 and len(cases) == 149
assert Counter(r['provenance'] for r in requirements) == {'D12': 77, 'U': 15}
assert Counter(c['provenance'] for c in cases) == {'D12': 77, 'U': 65, 'Dpkg': 7}
assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
reqids = {r['id'] for r in requirements}
spec = ROOT / 'wiki/specs/delay-reverb-devices.md'
research = ROOT / 'wiki/research/delay-reverb-devices.md'
assert set(re.findall(r'^### (REQ-DR-[A-Z-]+-\d{3})', spec.read_text(), re.M)) == reqids
for requirement in requirements:
    assert '**' + requirement['provenance'] + '.** ' + requirement['text'] in spec.read_text()
    assert requirement['exact_target_applicability'] == 'unknown'
    assert requirement['id'].startswith('REQ-DR-' + requirement['device'].upper() + '-')
for case in cases:
    assert case['requirement'] in reqids
    assert case['id'].startswith('DR-' + case['device'].upper() + '-')
    assert case['id'] in spec.read_text()
    assert case['action'] and case['setup'] and case['comparison']
    assert case['exact_target_applicability'] == 'unknown' and case['exact_target_expected'] is None
    assert case['execution'].startswith('unexecuted')
    assert (case['expected'] is None) == (case['provenance'] == 'U')
for record in requirements + cases:
    for reference in record['evidence']:
        file, locator = reference.split('#')
        assert locator in locators[file], reference
    assert record['provenance'] == 'U' or record['evidence']
for case in cases:
    row = f"| {case['id']} | {case['requirement']} | {case['kind']} | {case['title']} | {case['provenance']}; exact build U |"
    assert row in spec.read_text(), case['id']
labels = ['Delay', 'Echo', 'Filter Delay', 'Grain Delay', 'Reverb', 'Hybrid Reverb', 'Resonators']
for device, label in zip(DEVICES, labels):
    rs = [r for r in requirements if r['device'] == device]
    cs = [c for c in cases if c['device'] == device]
    rg = Counter(r['provenance'] for r in rs)
    cg = Counter(c['provenance'] for c in cs)
    row = f"| {label} | {len(rs)} | {rg['D12']} | {rg['U']} | {len(cs)} | {cg['D12']} / {cg['Dpkg']} / {cg['U']} |"
    assert row in spec.read_text(), device
for device in DEVICES:
    required_kinds = {'positive', 'negative', 'boundary', 'automation', 'persistence', 'undo', 'malformed', 'cancel', 'teardown', 'sample-rate', 'sidechain', 'package'}
    actual_kinds = {c['kind'] for c in cases if c['device'] == device}
    assert required_kinds <= actual_kinds, (device, required_kinds - actual_kinds)
    assert all(any(c['requirement'] == r['id'] for c in cases) for r in requirements if r['device'] == device)
fixtures = read('fixtures.json')
assert all(f'F{i}' in fixtures for i in range(7))
assert 'nonzero wet output' in fixtures['nonvacuity_gate']
assert 'positive control' in fixtures['nonvacuity_gate']
assert 'expected=null' in fixtures['F6']['record']

for page in [spec, research]:
    content = page.read_text()
    assert content.startswith('---\n')
    for key in ['id', 'type', 'status', 'updated', 'access']:
        assert re.search(r'^' + key + r': .+', content, re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('https://', 'http://', '#')):
            continue
        assert (page.parent / target.split('#')[0]).resolve().exists(), (page, target)
    snapshot = P / ('spec-r2.md' if page == spec else 'research-r2.md')
    assert snapshot.read_bytes() == page.read_bytes(), snapshot

manifest = P / 'manifest-author-r2.json'
if manifest.exists():
    for name, record in read(manifest.name)['files'].items():
        check_pin({'path': name, **record})
archive = P / 'archive-r1'
prior = archive / 'manifest-author-r1.json'
assert hashlib.sha256(prior.read_bytes()).hexdigest() == '560dc1d7f8df587ac138b3bf54978cd76d004b899bb65d543dc4a6cd61609654'
prior_manifest = json.loads(prior.read_text())
assert len(prior_manifest['files']) == 32
for name, pin in prior_manifest['files'].items():
    data = (archive / name).read_bytes()
    assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], name
assert (P / 'manifest-author-r1.json').read_bytes() == prior.read_bytes()
assert (P / 'spec-r1.md').read_bytes() == (archive / 'spec-r1.md').read_bytes()
assert (P / 'research-r1.md').read_bytes() == (archive / 'research-r1.md').read_bytes()
for name, current, changed_id, fields in [
    ('requirements.json', requirements, 'REQ-DR-ECHO-014', {'provenance', 'text'}),
    ('cases.json', cases, 'DR-ECHO-014', {'provenance', 'expected', 'comparison'}),
]:
    old = json.loads((archive / name).read_text())
    assert [r['id'] for r in old] == [r['id'] for r in current]
    changed = [(a, b) for a, b in zip(old, current) if a != b]
    assert len(changed) == 1 and changed[0][0]['id'] == changed_id
    a, b = changed[0]
    assert {key for key in a.keys() | b.keys() if a.get(key) != b.get(key)} == fields
    assert b['provenance'] == 'U' and a['evidence'] == b['evidence']
case = next(c for c in cases if c['id'] == 'DR-ECHO-014')
assert case['expected'] is None and 'Ungraded' in case['comparison']
for name in prior_manifest['files']:
    if name not in {'requirements.json', 'cases.json'}:
        assert (P / name).read_bytes() == (archive / name).read_bytes(), name
response = read('response-author-r2.json')
assert response['prior_manifest_sha256'] == hashlib.sha256(prior.read_bytes()).hexdigest()
assert response['case_grades'] == dict(Counter(c['provenance'] for c in cases))

mutable = [spec, research] + [p for p in P.rglob('*') if p.is_file() and p.suffix in {'.md', '.py', '.json', '.txt'}]
for path in mutable:
    result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
    assert result.returncode in [0, 1] and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

print(json.dumps({'status': 'pass', 'scope': 'author packet integrity only; no reference or candidate execution', 'requirements': 92, 'D12_requirements': 77, 'U_requirements': 15, 'cases': 149, 'D12_cases': 77, 'Dpkg_cases': 7, 'U_cases': 65, 'all_exact_target_expected_null': True, 'manual_blocks': 207, 'schema_classes': 7, 'presets': 7, 'source_pins': 14, 'checks': ['exact revision 1 seal and 32 archived payloads', 'only reviewed Echo requirement and case changed', 'source and original-capture identity pins', '207 manual blocks reproduced with line locators', 'seven schema class and preset XML derivations', 'unique requirements and case IDs with evidence references', 'all per-device required case kinds and null unknowns', 'canonical snapshot equality and local file links', 'author manifest pins when present', 'untracked-aware whitespace checks'], 'limits': ['author self-check only; independent semantic review remains separate', 'no exact-build applicability, DSP, defaults, timing, lifecycle or compatibility proof']}, indent=2))
