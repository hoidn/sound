"""Check retained evidence and case predicates; this is not a device test."""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import gzip
import hashlib
import json
import math
import re
import struct
import wave
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((OUT / name).read_text())

sources = read('sources.json')
assert len(sources) == 5
for source in sources:
    data = (OUT / source['file']).read_bytes()
    assert len(data) == source['bytes'] and sha(data) == source['sha256'], source['id']
    if 'path' in source:
        assert Path(source['path']).read_bytes() == data, source['path']

class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5') and attrs.get('id'):
            self.anchors[attrs['id']] = self.getpos()[0]

headings = Headings()
headings.feed((OUT / sources[0]['file']).read_text())
for heading in read('manual-headings.json'):
    if heading['anchor']:
        assert headings.anchors[heading['anchor']] == heading['html_line']

schema_data = (OUT / '12.0_12402.txt').read_text()
schema = ET.fromstring(schema_data)
schema_lines = schema_data.splitlines()
for cls, record in read('schema-fields.json').items():
    node = schema.find(cls)
    assert node is not None and schema_lines[record['line'] - 1].strip() == f'<{cls}>'
    assert [{'name': child.tag, **child.attrib} for child in node] == record['fields']

for preset in read('preset-observations.json'):
    stem = f'preset-{preset["device"].lower()}'
    xml = gzip.decompress((OUT / f'{stem}.adv').read_bytes())
    assert xml == (OUT / f'{stem}.xml').read_bytes()
    root = ET.fromstring(xml)
    node = root.find(preset['class'])
    assert node is not None and root.attrib == preset['creator']
    assert [c.tag for c in node] == preset['top_level_fields']
    assert len(list(node.iter('SampleRef'))) == len(preset['sample_references'])
    assert len(list(node.iter('MultiSamplePart'))) == preset['multisample_parts']
assert [len(p['sample_references']) for p in read('preset-observations.json')] == [0, 0, 8]

for fixture in read('fixtures.json')['audio']:
    path = OUT / fixture['path']
    assert sha(path.read_bytes()) == fixture['sha256']
    with wave.open(str(path), 'rb') as audio:
        assert (audio.getnchannels(), audio.getsampwidth(), audio.getframerate(), audio.getnframes()) == (2, 2, 48000, 192000)
        samples = struct.iter_unpack('<hh', audio.readframes(192000))
        for frame, (left, right) in enumerate(samples):
            hz = fixture['frequencies_by_second_hz'][frame // 48000]
            expected = round(8192 * math.sin(2 * math.pi * hz * (frame % 48000) / 48000))
            assert left == right == expected

for fixture in read('fixtures.json')['malformed']:
    data = (OUT / fixture['path']).read_bytes()
    assert len(data) == fixture['bytes'] and sha(data) == fixture['sha256']
    try:
        with wave.open(str(OUT / fixture['path']), 'rb'):
            pass
    except (EOFError, wave.Error):
        continue
    raise AssertionError(f'Malformed fixture unexpectedly parsed: {fixture["path"]}')

requirements = read('requirements.json')
req_by_id = {r['id']: r for rows in requirements.values() for r in rows}
assert len(req_by_id) == 61
assert Counter(r['strength'] for r in req_by_id.values()) == {'D': 46, 'U': 15}
cases = read('cases.json')
assert len(cases) == len({c['id'] for c in cases}) == 88
assert Counter(c['strength'] for c in cases) == {'D': 72, 'U': 16}
assert set(c['requirement'] for c in cases) == set(req_by_id)
for case in cases:
    req = req_by_id[case['requirement']]
    assert case['executed'] is False and case['exact_12_4_3'] == 'U'
    assert all(case[k] for k in ('setup', 'action', 'expected', 'fixture', 'comparator', 'kind'))
    assert case['evidence_anchor'] == req['anchor']
    if req['anchor']:
        assert req['anchor'] in headings.anchors
    if case['comparator'] == 'unknown':
        assert case['strength'] == 'U'

pages = [ROOT / f'wiki/specs/device-{device}.md' for device in requirements]
pages.append(ROOT / 'wiki/research/sample-instruments.md')
link_count = 0
for page in pages:
    content = page.read_text()
    assert content.startswith('---\n')
    metadata = content.split('---', 2)[1]
    for key in ('id', 'type', 'status', 'updated', 'access'):
        assert re.search(rf'^{key}: .+$', metadata, re.M)
    assert all(not line.endswith((' ', '\t')) for line in content.splitlines())
    if page.parent.name == 'specs':
        device = page.stem.removeprefix('device-')
        declared = re.findall(r'^### (REQ-[A-Z]+-\d+) ', content, re.M)
        assert declared == [r['id'] for r in requirements[device]]
        assert all(c['id'] in content for c in cases if c['requirement'].startswith(f'REQ-{device.upper()}-'))
    for target in re.findall(r'\]\(([^)]+)\)', content):
        if target.startswith(('https:', 'http:')):
            continue
        path, _, anchor = target.partition('#')
        destination = (page.parent / path).resolve() if path else page
        assert destination.exists(), (page, target)
        if anchor and destination.suffix == '.md':
            titles = re.findall(r'^#+ (.+)$', destination.read_text(), re.M)
            anchors = {re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-') for title in titles}
            assert anchor in anchors, (page, target)
        link_count += 1

manifest_path = OUT / 'manifest-author-r1.json'
if manifest_path.exists():
    for record in read(manifest_path.name)['payloads']:
        data = (OUT / record['path']).read_bytes()
        assert len(data) == record['bytes'] and sha(data) == record['sha256'], record['path']
    for record in read(manifest_path.name)['canonical_snapshots']:
        assert (ROOT / record['canonical']).read_bytes() == (OUT / record['snapshot']).read_bytes()

print(json.dumps({'check': 'static packet integrity only', 'sources': len(sources),
                  'requirements': len(req_by_id), 'requirement_strengths': {'D': 46, 'U': 15},
                  'cases': len(cases), 'case_strengths': {'D': 72, 'U': 16},
                  'unexecuted': 88, 'exact_12_4_3_unknown': 88,
                  'synthetic_wav_samples_checked': 576000, 'local_links': link_count,
                  'manifest_checked': manifest_path.exists(),
                  'original_or_candidate_executed': False, 'result': 'pass'}, indent=2))
