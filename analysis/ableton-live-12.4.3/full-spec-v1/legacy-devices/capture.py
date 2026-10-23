"""Bounded documentary/package capture; no device or original code execution."""
from pathlib import Path
from html.parser import HTMLParser
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
I = P.parent / 'inventory'
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
SLUGS = ['auto-filter', 'auto-pan', 'chorus', 'erosion', 'flanger', 'frequency-shifter', 'phaser', 'redux-legacy']

def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))

def write(name, obj):
    b = (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode()
    p = P / name
    if p.exists():
        assert p.read_bytes() == b, p
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b)

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.device = self.tag = None
        self.rows = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h2':
            self.device = a.get('id') if a.get('id') in SLUGS else None
        if self.device and self.tag is None and tag in ['h2', 'h3', 'h4', 'p', 'li']:
            self.tag, self.buf = tag, []
            self.loc = dict(html_line=self.getpos()[0], anchor=a.get('id'), section=a.get('data-number'))

    def handle_data(self, data):
        if self.tag:
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag == self.tag:
            text = ' '.join(''.join(self.buf).split())
            if text:
                self.rows.append(dict(device=self.device, kind=tag, text=text, **self.loc))
            self.tag = None

manual = P / 'manual-11-audio-effects-2026-10-19.html'
parser = Blocks()
parser.feed(manual.read_text())
for slug in SLUGS:
    rows = [r for r in parser.rows if r['device'] == slug]
    assert rows and rows[0]['kind'] == 'h2', slug
    for n, row in enumerate(rows, 1):
        row['locator'] = f'{slug}:B{n:03}'
    write(f'manual-{slug}-blocks.json', rows)
    text = '\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n'
    path = P / f'manual-{slug}.txt'
    if path.exists():
        assert path.read_text() == text
    else:
        path.write_text(text)

sources = [dict(id='D11-AUDIO-EFFECTS', url='https://www.ableton.com/en/live-manual/11/live-audio-effect-reference/', capture_date='2026-10-19', version='Ableton Reference Manual Version 11; exact minor/date unadvertised; legacy 12.4.3 applicability unresolved', **pin(manual))]
current = P.parent / 'audio-utilities/manual-audio-effects-2026-10-19.html'
assert pin(current)['sha256'] == '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
sources.append(dict(id='D12-AUDIO-EFFECTS', url='https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/', capture_date='2026-10-19', version='Reference Manual Version 12; exact 12.4.3 applicability unknown', **pin(current)))
now = Blocks()
now.feed(current.read_text())
write('manual-12-erosion-migration-blocks.json', [r for r in now.rows if r['device'] == 'erosion' and 'Legacy' in r['text']])
schema = I / '12.0_12402.txt'
assert pin(schema)['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
sources.append(dict(id='PKG-SCHEMA', version='12.0_12402 retained from pinned 12.4.3', **pin(schema)))
ledger = P.parent / 'inventory-revisions/r2-spectral-aliases/devices-r2.json'
sources.append(dict(id='DEVICE-LEDGER-R2', **pin(ledger)))
devices = [d for d in json.loads(ledger.read_text()) if d['kind'] == 'legacy-native']
assert len(devices) == 8
classes = {d['schema_class'] for d in devices}
fields = [c for c in json.loads((I / 'schema-classes.json').read_text())['classes'] if c['class'] in classes]
assert len(fields) == 8
write('schema-fields.json', fields)
observations = []
for device in devices:
    f = APP / device['example']['path']
    assert pin(f)['sha256'] == device['example']['sha256']
    local = P / 'package' / device['name'] / f.name
    local.parent.mkdir(parents=True, exist_ok=True)
    b = f.read_bytes()
    if local.exists():
        assert local.read_bytes() == b
    else:
        local.write_bytes(b)
    sources.append(dict(id='PKG-' + device['schema_class'], original_path=str(f), capture_date='2026-10-19', **pin(local)))
    root = ET.fromstring(gzip.decompress(b))
    elem = root.find(device['schema_class'])
    assert elem is not None
    folder = f.parent
    folder_rows = []
    for preset in sorted(folder.glob('*.adv')):
        data = preset.read_bytes()
        if data.startswith(b'\x1f\x8b'):
            doc = ET.fromstring(gzip.decompress(data))
            folder_rows.append(dict(**pin(preset), roots=[c.tag for c in doc], parse='gzip XML'))
        else:
            folder_rows.append(dict(**pin(preset), roots=None, parse='unknown non-gzip format; not analyzed', prefix_hex=data[:8].hex()))
    observations.append(dict(surface=device['id'], name=device['name'], schema_class=device['schema_class'], file=str(local.relative_to(P)), root_attributes=root.attrib, locator='/Ableton/' + elem.tag, fields=[dict(field=c.tag, xml=ET.tostring(c, encoding='unicode')) for c in elem], folder_presets=folder_rows, limitation='Folder and matching roots establish artifact association only; no runtime, migration, constructor default, GUI bounds, enum meaning or DSP law.'))
write('package-observations.json', observations)
write('sources-r2.json', sources)
print(json.dumps(dict(profiles=len(devices), schema_classes=len(fields), folder_presets=sum(len(o['folder_presets']) for o in observations), manual_blocks=len(parser.rows))))
