"""Check retained analyst evidence and authored views; execute no product code."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import gzip
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parents[3]


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
dependencies = read('dependencies.json')
assert len(sources) == 14 and len(dependencies) == 5
pins = {s['id']: s for s in sources + dependencies}
assert len(pins) == 19
for record in pins.values():
    data = check_pin(record)
    if 'original_path' in record:
        assert Path(record['original_path']).read_bytes() == data
manual = pins['D12-AUDIO-EFFECTS']
assert manual['sha256'] == '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
assert pins['PKG-SCHEMA']['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
catalog = json.loads(check_pin(pins['ORIGINAL-MANUAL-CAPTURE-CATALOG']))
assert any(s['id'] == manual['id'] and all(s[k] == manual[k] for k in ['sha256', 'bytes', 'url', 'capture_date']) for s in catalog)
devs = [line[1:-1].split('|') for line in (P / 'authored-contracts.txt').read_text().splitlines() if line.startswith('[')]
assert len(devs) == 10
slugs = {d[0] for d in devs}
classes = {d[3] for d in devs}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.device = self.tag = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.device = attrs.get('id') if attrs.get('id') in slugs else None
        if self.device and tag in ['h2', 'h3', 'h4', 'p', 'li'] and self.tag is None:
            self.tag, self.text = tag, []
            self.meta = {'html_line': self.getpos()[0], 'anchor': attrs.get('id'), 'section': attrs.get('data-number')}

    def handle_data(self, data):
        if self.tag:
            self.text.append(data)

    def handle_endtag(self, tag):
        if self.tag == tag:
            text = ' '.join(''.join(self.text).split())
            if text:
                self.rows.append({'device': self.device, 'kind': tag, 'text': text, **self.meta})
            self.tag = None


parser = Blocks()
parser.feed(check_pin(manual).decode())
blocks = {}
for slug in slugs:
    rows = [r for r in parser.rows if r['device'] == slug]
    for i, row in enumerate(rows, 1):
        row['locator'] = f'{slug}:B{i:03d}'
        blocks[row['locator']] = row
    assert rows == read(f'manual-{slug}-blocks.json'), slug
    assert (P / f'manual-{slug}.txt').read_text() == '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n'
assert len(blocks) == 332
schema_bytes = check_pin(pins['PKG-SCHEMA'])
schema_root = ET.fromstring(schema_bytes)
schema_lines = schema_bytes.decode().splitlines()
inventory_classes = json.loads(check_pin(pins['FROZEN-SCHEMA-INVENTORY']))['classes']
assert read('schema-fields.json') == [r for r in inventory_classes if r['class'] in classes]
for record in read('schema-fields.json'):
    assert schema_lines[record['line'] - 1].strip() == '<' + record['class'] + '>'
    assert record['fields'] == [{'name': child.tag, **child.attrib} for child in schema_root.find(record['class'])]
package = read('package-values.json')
assert len(package) == 10
for record in package:
    root = ET.fromstring(gzip.decompress((P / record['file']).read_bytes()))
    element = root.find(record['class'])
    assert element is not None and root.attrib == record['root_attributes']
    assert root.attrib['Creator'] == 'Ableton Live 12.4d1' and root.attrib['MinorVersion'] == '12.0_12402'
    assert root.attrib['Revision'] == '42bc084cd8152e4fb737ef3fefd04b2bea5320e7'
    assert record['locator'] == '/Ableton/' + record['class']
    assert record['fields'] == [{'field': c.tag, 'xml': ET.tostring(c, encoding='unicode')} for c in element]

folders = read('spectral-folder-observations.json')
assert len(folders) == 28
roots = Counter()
for record in folders:
    data = check_pin(record)
    if Path(record['path']).name.startswith('._'):
        assert record['root'] is None and 'excluded' in record['parse_status']
    else:
        root = ET.fromstring(gzip.decompress(data))
        assert [child.tag for child in root] == [record['root']]
        roots[record['factory_folder'], record['root']] += 1
assert roots == {('Spectral Resonator', 'Transmute'): 8, ('Spectral Time', 'Spectral'): 6}
for folder in {r['factory_folder'] for r in folders}:
    sample = next(r for r in folders if r['factory_folder'] == folder)
    assert {str(p) for p in Path(sample['path']).parent.glob('*.adv')} == {r['path'] for r in folders if r['factory_folder'] == folder}
corrected = {d['id']: d for d in json.loads(check_pin(pins['REVIEWED-DEVICE-INVENTORY-R2']))}
review = json.loads(check_pin(pins['SPECTRAL-CORRECTION-REVIEW']))
assert review['disposition'] == 'approved-artifact-association-correction'
assert review['reviewed_manifest_sha256'] == pins['SPECTRAL-CORRECTION-MANIFEST']['sha256']
for record in json.loads(check_pin(pins['SPECTRAL-CORRECTION-MANIFEST']))['files']:
    check_pin({**record, 'path': str(ROOT / record['path'])})
association = read('association-reconciliation.json')
assert len(association) == 10 and sum(r['source_id_is_historical'] for r in association) == 2
for record, original in zip(association, package):
    current = corrected[record['corrected_inventory_surface']]
    assert record['historical_inventory_surface'] == original['inventory_surface']
    assert record['class'] == original['class'] == current['schema_class']
    assert record['schema_line'] == current['schema_line'] and record['retained_preset'] == original['file']
    assert Path(original['file']).name == Path(current['example']['path']).name
for slug, prefix, name, cls in devs:
    assert corrected['SURF-DEVICE-' + slug.upper()]['schema_class'] == cls

requirements, cases, recipes = read('requirements.json'), read('cases.json'), read('stimulus-recipes.json')
assert len(requirements) == 106 and len(cases) == 186
assert Counter(r['strength'] for r in requirements) == {'D12': 96, 'U': 10}
assert Counter(c['kind'] for c in cases if c['kind'].startswith('documented')) == {'documented-control': 46, 'documented-state': 9}
assert sum(c['kind'] == 'signal-obligation' for c in cases) == 41
req_by_id = {r['id']: r for r in requirements}
assert len(req_by_id) == 106 and len({c['id'] for c in cases}) == 186
spec, research = ROOT / 'wiki/specs/modulation-pitch-loop-devices.md', ROOT / 'wiki/research/modulation-pitch-loop-devices.md'
spec_text = spec.read_text()
assert set(re.findall(r'REQ-MPL-[A-Z]+-(?:\d{3}|LIFECYCLE)', spec_text)) == set(req_by_id)
for requirement in requirements:
    assert requirement['id'] in spec_text and requirement['exact_build'] == 'U'
    assert bool(requirement['evidence']) == (requirement['strength'] == 'D12')
    if requirement['strength'] == 'D12':
        assert requirement['contract'] in spec_text
    for reference in requirement['evidence']:
        assert reference['id'] == manual['id'] and reference['html_line'] == blocks[reference['block']]['html_line']
for case in cases:
    assert len(case['requirements']) == 1 and case['requirements'][0] in req_by_id
    requirement = req_by_id[case['requirements'][0]]
    assert case['device'] == requirement['device'] and case['setup_and_action']
    assert case['source_blocks'] == [r['block'] for r in requirement['evidence']]
    assert case['expected'] is None and case['target_grade'] == 'U' and case['executed'] is False
    assert case['fixture'].split('#')[1] in recipes and case['fixture'].startswith('stimulus-recipes.json#')
    assert 'common-setup' in case['preconditions']
    if case['kind'] == 'signal-obligation' or requirement['strength'] == 'U':
        assert case.get('documentary_comparator') is None and case.get('comparison') is None
        assert 'positive-signal-guard' in case['preconditions']
    else:
        assert case['documentary_comparator'] and case['documentary_expected']
    if requirement['strength'] == 'U':
        assert case['documentary_expected'] is None and case['unknown']
for slug, prefix, name, cls in devs:
    owned = [c for c in cases if c['device'] == name]
    assert {c['kind'] for c in owned if '-U-' in c['id']} == {'boundary', 'automation', 'transport', 'persistence', 'undo', 'malformed', 'cancel', 'teardown', 'sample-rate'}
    assert all(any(r['id'] in c['requirements'] for c in owned) for r in requirements if r['device'] == name)
assert 'paired positive case' in recipes['positive-signal-guard']['baseline']
assert 'nonzero' in recipes['positive-signal-guard']['enabled']

for page, snapshot in [(spec, 'spec-r2.md'), (research, 'research-r2.md')]:
    text = page.read_text()
    assert text.startswith('---\n') and 'access: analysis\n' in text
    for key in ['id', 'type', 'status', 'updated', 'access']:
        assert re.search(r'^' + key + r': .+', text, re.M)
    assert re.search(r'^updated: \d{4}-\d{2}-\d{2}$', text, re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        if target.startswith(('https://', 'http://', '#')):
            continue
        assert (page.parent / target.split('#')[0]).resolve().exists(), (page, target)
    assert (P / snapshot).read_bytes() == page.read_bytes(), snapshot
manifest = read('manifest-author-r2.json')
prior_names = set(read('archive-r1/manifest-author-r1.json')['files'])
expected_names = prior_names - {'spec-r1.md', 'research-r1.md', 'validate.py', 'validation-author-r1.json'} | {'spec-r2.md', 'research-r2.md', 'validate-r2.py', 'validation-author-r2.json', 'revise-r2.py', 'response-author-r2.json'}
assert set(manifest['files']) == expected_names

# This successor checks the exact editorial delta against the immutable prior seal.
response = json.loads((P / 'response-author-r2.json').read_text())
prior_path = P / response['prior_manifest']
assert hashlib.sha256(prior_path.read_bytes()).hexdigest() == response['prior_manifest_sha256']
prior = json.loads(prior_path.read_text())
prior_records = list(prior['files'].items())
for rel, pin in prior_records:
    archived = prior_path.parent / rel
    raw = archived.read_bytes()
    assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], rel
    current = P / rel
    if True:
        assert current.read_bytes() == raw, rel
assert (P / 'manifest-author-r1.json').read_bytes() == prior_path.read_bytes()
for extra in response.get('preserved_extras', []):
    assert (P / extra['file']).read_bytes() == (prior_path.parent / extra['file']).read_bytes()
    assert hashlib.sha256((P / extra['file']).read_bytes()).hexdigest() == extra['sha256']
for change in response['page_changes']:
    expected = (P / change['archive_input']).read_text()
    for edit in change['replacements']:
        assert expected.count(edit['before']) == edit['occurrences']
        expected = expected.replace(edit['before'], edit['after'])
    expected += change['append']
    assert (ROOT / change['canonical']).read_text() == expected == (P / change['snapshot']).read_text()
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / 'tools'))
import spec_browser
browser_spec = ROOT / 'wiki/specs/modulation-pitch-loop-devices.md'
browser_rows = spec_browser.spec_rows(browser_spec, browser_spec.read_text())
requirement_ids = {r['id'] for r in json.loads((P / 'requirements.json').read_text())}
assert len(browser_rows) == 106 and {r['id'] for r in browser_rows} == requirement_ids
assert len(spec_browser.spec_rows(browser_spec, (prior_path.parent / 'spec-r1.md').read_text())) == 96

for name, record in manifest['files'].items():
    check_pin({'path': name, **record})
for path in [spec, research] + sorted(p for p in P.rglob('*') if p.is_file()):
    if path.suffix == '.json':
        json.loads(path.read_text())
    if path.suffix in {'.md', '.txt', '.json', '.py'}:
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
        assert result.returncode in [0, 1] and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)

print(json.dumps({'status': 'pass', 'scope': 'author packet integrity only; independent semantic review required', 'requirements': 106, 'D12_requirements': 96, 'U_requirements': 10, 'cases': 186, 'documented_control_cases': 46, 'documented_state_cases': 9, 'ungraded_signal_cases': 41, 'U_lifecycle_cases': 90, 'all_exact_target_expected_null': True, 'all_cases_unexecuted': True, 'source_pins': 19, 'spectral_folder_pins': 28, 'manual_blocks': 332, 'schema_classes': 10, 'example_presets': 10, 'checks': ['source and original capture catalog identities', 'manual blocks and line-numbered text independently reproduced', 'schema declarations, lines, fields and preset gzip/XML derivations', 'all spectral folders and reviewed R2 artifact associations', 'unique requirement/case IDs, exact evidence links and device ownership', 'all per-device lifecycle kinds, null unknowns and positive guards', 'canonical snapshot equality, metadata and local file links', 'all manifest payload hashes and JSON syntax', 'exact49payload prior archive and all original JSON/source bytes', 'heading-only canonical delta and browser106of106 regression', 'untracked-aware text whitespace'], 'limits': ['no original, extracted-original, emulation, Live or candidate execution', 'no exact-build runtime applicability, DSP, clock, MIDI codec, random distribution or tolerance established', 'shared catalogs and independent semantic review remain coordinator-owned']}, indent=2))
