"""Bounded manual/schema/three-preset capture. Executes no original code."""
from pathlib import Path
from html.parser import HTMLParser
import datetime
import gzip
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
INVENTORY = OUT.parent / 'inventory'
DEVICES = {'Simpler': 'OriginalSimpler', 'Sampler': 'MultiSampler', 'Impulse': 'InstrumentImpulse'}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

class Article(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.heading = None
        self.headings = []
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'h1':
            self.active = True
        if not self.active:
            return
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5'):
            self.heading = {'anchor': dict(attrs).get('id'), 'html_line': self.getpos()[0], 'text': ''}
            self.headings.append(self.heading)
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5'):
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5'):
            self.heading = None
        if tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5'):
            self.parts.append('\n')

    def handle_data(self, value):
        if self.active:
            self.parts.append(value)
            if self.heading is not None:
                self.heading['text'] += value

url = 'https://www.ableton.com/en/live-manual/12/live-instrument-reference/'
html_path = OUT / 'manual-instruments-2026-10-19.html'
if html_path.exists():
    sources = json.loads((OUT / 'sources.json').read_text())
    manual_source = sources[0]
    data = html_path.read_bytes()
    assert digest(data) == manual_source['sha256']
else:
    with urllib.request.urlopen(url) as response:
        data = response.read()
        final_url = response.url
    html_path.write_bytes(data)
    manual_source = {'id': 'SAMPLE-INSTRUMENTS-MANUAL', 'url': url, 'final_url': final_url,
                     'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                     'file': html_path.name, 'bytes': len(data), 'sha256': digest(data),
                     'version': 'Live 12; exact 12.4.3 behavioral applicability unknown'}
parser = Article()
parser.feed(data.decode())
article = '\n'.join(' '.join(line.split()) for line in ''.join(parser.parts).splitlines() if line.strip())
article = article.split('\nAbleton Reference Manual')[0]
assert all(f' {device}\n' in article for device in DEVICES)
(OUT / 'manual-instruments.txt').write_text(article + '\n')
write('manual-headings.json', parser.headings)
sources = [manual_source]

schema_path = APP / 'Contents/App-Resources/Schema/12.0_12402.txt'
schema_bytes = schema_path.read_bytes()
assert digest(schema_bytes) == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
(OUT / '12.0_12402.txt').write_bytes(schema_bytes)
schema = ET.fromstring(schema_bytes)
lines = schema_bytes.decode().splitlines()
names = set(DEVICES.values()) | {'MultiSamplePart', 'SampleRef', 'SampleLoop', 'ZoneRange', 'ZoneSettings', 'SampleWarpProperties'}
records = {node.tag: {'line': next(i + 1 for i, line in enumerate(lines) if line.strip() == f'<{node.tag}>'),
                      'fields': [{'name': child.tag, **child.attrib} for child in node]}
           for node in schema if node.tag in names or node.tag.startswith('Impulse')}
assert set(DEVICES.values()) <= records.keys()
write('schema-fields.json', records)
sources.append({'id': 'SAMPLE-INSTRUMENTS-SCHEMA', 'path': str(schema_path), 'file': '12.0_12402.txt',
                'bytes': len(schema_bytes), 'sha256': digest(schema_bytes), 'version': '12.0_12402 in pinned 12.4.3'})

device_inventory = json.loads((INVENTORY / 'devices.json').read_text())
preset_records = []
for name, cls in DEVICES.items():
    entry = next(item for item in device_inventory if item['name'] == name)
    path = APP / entry['example']['path']
    data = path.read_bytes()
    assert digest(data) == entry['example']['sha256']
    root = ET.fromstring(gzip.decompress(data))
    node = root.find(cls)
    assert node is not None
    retained = f'preset-{name.lower()}.adv'
    (OUT / retained).write_bytes(data)
    xml = gzip.decompress(data)
    (OUT / f'preset-{name.lower()}.xml').write_bytes(xml)
    preset_records.append({'device': name, 'class': cls, 'creator': root.attrib, 'locator': f'/Ableton/{cls}',
                           'top_level_fields': [child.tag for child in node],
                           'sample_references': [ET.tostring(n, encoding='unicode') for n in node.iter('SampleRef')],
                           'multisample_parts': len(list(node.iter('MultiSamplePart')))})
    sources.append({'id': f'SAMPLE-INSTRUMENTS-PRESET-{name.upper()}', 'path': str(path), 'file': retained,
                    'bytes': len(data), 'sha256': digest(data), 'version': root.attrib,
                    'limit': 'Shipped historical preset: stored vocabulary, not execution or DSP evidence'})
write('preset-observations.json', preset_records)
write('sources.json', sources)
print(json.dumps({'sources': len(sources), 'schema_classes': len(records), 'presets': len(preset_records),
                  'manual_sha256': manual_source['sha256'], 'original_code_executed': False}))
