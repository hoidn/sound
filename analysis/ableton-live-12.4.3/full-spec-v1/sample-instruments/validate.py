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
    assert set(case['evidence_anchors']) <= set(req['evidence_anchors'])
    assert case['evidence_anchor'] == (case['evidence_anchors'][0] if case['evidence_anchors'] else None)
    assert [loc['anchor'] for loc in case['evidence_locators']] == case['evidence_anchors']
    for loc in case['evidence_locators']:
        assert loc['source'] == 'SAMPLE-INSTRUMENTS-MANUAL'
        assert headings.anchors[loc['anchor']] == loc['html_line']
    if req['anchor']:
        assert req['anchor'] in headings.anchors
    if case['comparator'] == 'unknown':
        assert case['strength'] == 'U'

# Regression checks for the reviewed qualifiers, discriminating paths and sibling evidence.
assert 'Without an enabled loop' in req_by_id['REQ-SAMPLER-009']['body']
assert 'controlling exception' in req_by_id['REQ-SAMPLER-009']['body']
assert 'relative ordering of sample Gain and filter is unknown' in req_by_id['REQ-SIMPLER-014']['body']
case_by_id = {case['id']: case for case in cases}
for cid, anchors in {
    'SIMPLER-007': ['context-menu-options-for-simpler'],
    'SIMPLER-023': ['classic-playback-mode'],
    'SAMPLER-030': ['title-bar-options'],
    'IMPULSE-009': ['filter', 'saturator-and-envelope'],
    'IMPULSE-012': ['pan-and-volume', 'global-controls'],
}.items():
    assert case_by_id[cid]['evidence_anchors'] == anchors
assert 'Enable LFO, Sine, 1 Hz' in case_by_id['SIMPLER-022']['setup']
assert 'nonzero offered depth' in case_by_id['SIMPLER-022']['setup']
assert 'enable main filter, Clean low-pass' in case_by_id['SAMPLER-025']['setup']
for cid in ('SIMPLER-022', 'SAMPLER-025'):
    assert case_by_id[cid]['positive_control']
    assert 'record unknown' in case_by_id[cid]['expected']

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

archive = OUT / 'revisions/r1'
archive_manifest = archive / 'manifest-author-r1.json'
assert sha(archive_manifest.read_bytes()) == '277da7d53e395b45bf9d58ea803636d79002e20101163ec244f20a9ce100cf4b'
assert (OUT / 'manifest-author-r1.json').read_bytes() == archive_manifest.read_bytes()
old_manifest = json.loads(archive_manifest.read_text())
assert len(old_manifest['payloads']) == 28 and len(old_manifest['canonical_snapshots']) == 4
for record in old_manifest['payloads']:
    data = (archive / record['path']).read_bytes()
    assert len(data) == record['bytes'] and sha(data) == record['sha256']
for record in old_manifest['canonical_snapshots']:
    assert (archive / record['snapshot']).read_bytes() == (OUT / record['snapshot']).read_bytes()

manifest_path = OUT / 'manifest-author-r2.json'
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
                  'archived_r1_payloads_verified': 28, 'archived_r1_snapshots_verified': 4,
                  'review_regression_checks': 'SI-REVIEW-001/002/003 pass statically',
                  'manifest_checked': manifest_path.exists(),
                  'original_or_candidate_executed': False, 'result': 'pass'}, indent=2))
