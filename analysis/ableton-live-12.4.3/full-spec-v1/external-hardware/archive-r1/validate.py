"""Assert analyst-packet integrity; never run hardware, plug-ins or product code."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
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
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'], path
    return data


sources = read('sources.json')
pins = {s['id']: s for s in sources}
assert len(sources) == len(pins) == 7
for source in sources:
    check_pin(source)
assert pins['D12-AUDIO-EFFECTS']['sha256'] == '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
assert pins['SAMPLE-INSTRUMENTS-MANUAL']['sha256'] == '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a'
assert pins['PKG-SCHEMA']['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
devices = read('authored-contracts.json')
assert set(devices) == {'EA', 'EI'} and all(len(d['requirements']) == 10 for d in devices.values())


class Section(HTMLParser):
    def __init__(self, slug):
        super().__init__()
        self.slug, self.active, self.tag, self.rows = slug, False, None, []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.active = attrs.get('id') == self.slug
        if self.active and tag in {'h2', 'p'} and self.tag is None:
            self.tag, self.text = tag, []
            self.meta = {'html_line': self.getpos()[0], 'anchor': attrs.get('id'), 'section': attrs.get('data-number')}

    def handle_data(self, text):
        if self.tag:
            self.text.append(text)

    def handle_endtag(self, tag):
        if self.tag == tag:
            text = ' '.join(''.join(self.text).split())
            if text:
                self.rows.append({'locator': f'{self.slug}:B{len(self.rows) + 1:03d}', 'kind': tag, 'text': text, **self.meta})
            self.tag = None


blocks = {}
for prefix, device in devices.items():
    slug = device['slug']
    source = pins[device['source']]
    catalog = json.loads(check_pin(pins['CAPTURE-CATALOG-' + slug.upper()]))
    original = next(r for r in catalog if r['id'] == device['source'])
    assert all(original[k] == source[k] for k in ['id', 'sha256', 'bytes', 'url'])
    assert original.get('capture_date', original.get('captured_utc', '')[:10]) == source['capture_date'] == '2026-10-19'
    parser = Section(slug)
    parser.feed(check_pin(source).decode())
    assert parser.rows == read(f'manual-{slug}-blocks.json')
    assert len(parser.rows) == 10 and sum(r['kind'] == 'p' for r in parser.rows) == 9
    assert parser.rows[0]['html_line'] == (1144 if prefix == 'EA' else 1016)
    assert {r['html_line'] for r in parser.rows[1:]} == ({1154} if prefix == 'EA' else {1026})
    blocks.update({r['locator']: r for r in parser.rows})
schema_bytes = check_pin(pins['PKG-SCHEMA'])
schema = ET.fromstring(schema_bytes)
schema_lines = schema_bytes.decode().splitlines()
classes = {d['schema_class'] for d in devices.values()}
inventory_classes = json.loads(check_pin(pins['FROZEN-SCHEMA-INVENTORY']))['classes']
assert read('schema-fields.json') == [r for r in inventory_classes if r['class'] in classes]
assert len(read('schema-fields.json')) == 2
for record in read('schema-fields.json'):
    assert schema_lines[record['line'] - 1].strip() == '<' + record['class'] + '>'
    assert record['fields'] == [{'name': child.tag, **child.attrib} for child in schema.find(record['class'])]
inventory = json.loads(check_pin(pins['FROZEN-DEVICE-INVENTORY']))
assert read('inventory-associations.json') == [r for r in inventory if r.get('schema_class') in classes]
assert len(read('inventory-associations.json')) == 2
for record in read('inventory-associations.json'):
    assert record['example'] is None and record['complete'] is False and 'inferred' in record['alias_basis']
    assert record['schema_line'] == (939 if record['schema_class'] == 'BufferAudioDevice' else 963)

requirements, cases = read('requirements.json'), read('cases.json')
reqids = {r['id']: r for r in requirements}
assert len(requirements) == len(reqids) == 24 and len(cases) == len({c['id'] for c in cases}) == 56
assert Counter(r['strength'] for r in requirements) == {'D12': 20, 'U': 4}
assert Counter(c['strength'] for c in cases) == {'D12': 20, 'U': 36}
assert Counter(c['kind'] for c in cases if c['kind'].startswith('documented-')) == {'documented-control': 16, 'documented-state': 4}
assert sum(c['kind'] == 'signal' for c in cases) == 10
spec = ROOT / 'wiki/specs/external-hardware-devices.md'
research = ROOT / 'wiki/research/external-hardware-devices.md'
assert set(re.findall(r'REQ-EHW-(?:EA|EI)-(?:\d{3}|SIGNAL|LIFECYCLE)', spec.read_text())) == set(reqids)
for requirement in requirements:
    assert requirement['contract'] in spec.read_text() and requirement['exact_target_applicability'] == 'unknown'
    assert bool(requirement['evidence']) == (requirement['strength'] == 'D12')
    for evidence in requirement['evidence']:
        assert evidence['block'] in blocks and evidence['html_line'] == blocks[evidence['block']]['html_line']
        assert evidence['source'] in pins
for case in cases:
    assert case['id'] in spec.read_text() and case['requirements']
    assert all(rid in reqids and reqids[rid]['device'] == case['device'] for rid in case['requirements'])
    assert case['setup'] and case['action'] and case['fixture'] == 'fixtures.json'
    assert case['expected'] is None and case['executed'] is False and case['exact_target_applicability'] == 'unknown'
    assert case['comparison'] is None
    if case['strength'] == 'U':
        assert case['documentary_expected'] is None and case['documentary_comparator'] is None and case['unknown']
        assert 'positive-signal-guard' in case['setup']
    else:
        assert case['documentary_expected'] and case['documentary_comparator']
        row = next(r for d in devices.values() for r in d['requirements'] if r['id'] == case['requirements'][0])
        assert case['action'] == row['action'] and case['documentary_expected'] == row['documentary_expected']
    for evidence in case['evidence']:
        assert evidence['block'] in blocks and evidence['html_line'] == blocks[evidence['block']]['html_line']
for prefix, device in devices.items():
    owned = [c for c in cases if c['device'] == device['name']]
    assert {c['kind'] for c in owned if '-U-' in c['id']} == {'boundary', 'automation', 'transport', 'persistence', 'undo', 'malformed', 'cancel', 'disconnect', 'sample-rate', 'bypass', 'ownership', 'recovery', 'teardown'}
    assert all(any(r['id'] in c['requirements'] for c in owned) for r in requirements if r['device'] == device['name'])
fixtures = read('fixtures.json')
for text in ['active physical', 'positive response baseline', 'nonzero', 'unmuted', 'dry-only']:
    assert text in fixtures['positive-signal-guard']
assert 'unexecuted' in fixtures['rate-state'] and 'input definitions only' in fixtures['audio']


def slugify(heading):
    text = re.sub(r'[^\w\- ]', '', heading.lower())
    return text.replace(' ', '-')


for page, snapshot in [(spec, 'spec-r1.md'), (research, 'research-r1.md')]:
    content = page.read_text()
    assert content.startswith('---\n') and 'access: analysis\n' in content
    for key in ['id', 'type', 'status', 'updated', 'access', 'revision']:
        assert re.search(r'^' + key + r': .+', content, re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('https://', 'http://')):
            continue
        filename, _, anchor = target.partition('#')
        path = (page.parent / filename).resolve() if filename else page
        assert path.exists(), (page, target)
        if anchor and path.suffix == '.md':
            assert anchor in {slugify(h) for h in re.findall(r'^#+ (.+)$', path.read_text(), re.M)}, (page, target)
    assert (P / snapshot).read_bytes() == page.read_bytes()
manifest = read('manifest-author-r1.json')
assert set(manifest['files']) == {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name != 'manifest-author-r1.json'}
for name, record in manifest['files'].items():
    check_pin({'path': name, **record})
for path in [spec, research] + sorted(p for p in P.rglob('*') if p.is_file()):
    if path.suffix == '.json':
        json.loads(path.read_text())
    if path.suffix in {'.md', '.txt', '.json', '.py'}:
        result = subprocess.run(['git', 'diff', '--no-index', '--check', '/dev/null', str(path)], capture_output=True, text=True)
        assert result.returncode in {0, 1} and not result.stdout and not result.stderr, (path, result.stdout, result.stderr)
print(json.dumps({'status': 'pass', 'scope': 'author integrity check only; independent semantic review required', 'requirements': 24, 'D12_requirements': 20, 'U_requirements': 4, 'cases': 56, 'documented_control_cases': 16, 'documented_state_cases': 4, 'ungraded_signal_cases': 10, 'U_lifecycle_cases': 26, 'all_target_expected_null': True, 'all_cases_unexecuted': True, 'source_pins': 7, 'manual_paragraphs': 18, 'manual_headings': 2, 'schema_classes': 2, 'matched_preset_examples': 0, 'checks': ['source hashes and original capture catalog identity', 'exact manual text/block/line reproduction', 'schema declarations, field lists and inferred inventory associations', 'requirement/case ownership, finite inputs and source references', 'all lifecycle kinds, positive-signal prerequisites and null unknowns', 'canonical snapshot equality, frontmatter and relative links/heading anchors', 'complete author payload hashes, JSON syntax and untracked-aware whitespace'], 'limits': ['no original, candidate, external hardware, plug-in or emulation execution', 'no physical calibration or signal/MIDI/latency numerical oracle', 'all exact 12.4.3 runtime applicability unknown; neither profile complete']}, indent=2))
