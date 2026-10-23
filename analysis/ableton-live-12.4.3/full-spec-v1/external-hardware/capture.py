"""Extract two retained manual sections and frozen schema presence; no product run."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

P = Path(__file__).resolve().parent
BASE = P.parent


def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}


def retain(name, value):
    data = (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()
    path = P / name
    if path.exists():
        assert path.read_bytes() == data, path
    else:
        path.write_bytes(data)


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


sources = []
for slug, packet, file, source_id, digest, url in [
    ('external-audio-effect', 'audio-utilities', 'manual-audio-effects-2026-10-19.html', 'D12-AUDIO-EFFECTS', '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299', 'https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/'),
    ('external-instrument', 'sample-instruments', 'manual-instruments-2026-10-19.html', 'SAMPLE-INSTRUMENTS-MANUAL', '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a', 'https://www.ableton.com/en/live-manual/12/live-instrument-reference/'),
]:
    source = pin(BASE / packet / file)
    assert source['sha256'] == digest
    sources.append({'id': source_id, 'url': url, 'capture_date': '2026-10-19', 'version': 'Live Version 12; exact 12.4.3 runtime applicability unknown', 'original_catalog': f'../{packet}/sources.json', **source})
    sources.append({'id': 'CAPTURE-CATALOG-' + slug.upper(), **pin(BASE / packet / 'sources.json')})
    parser = Section(slug)
    parser.feed(Path(source['path']).read_text())
    assert len(parser.rows) == 10 and sum(r['kind'] == 'p' for r in parser.rows) == 9
    retain('manual-' + slug + '-blocks.json', parser.rows)
for source_id, file in [('FROZEN-DEVICE-INVENTORY', 'devices.json'), ('FROZEN-SCHEMA-INVENTORY', 'schema-classes.json'), ('PKG-SCHEMA', '12.0_12402.txt')]:
    sources.append({'id': source_id, **pin(BASE / 'inventory' / file)})
assert sources[-1]['sha256'] == 'b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
classes = {'BufferAudioDevice', 'BufferInstrument'}
retain('schema-fields.json', [r for r in json.loads((BASE / 'inventory/schema-classes.json').read_text())['classes'] if r['class'] in classes])
retain('inventory-associations.json', [r for r in json.loads((BASE / 'inventory/devices.json').read_text()) if r.get('schema_class') in classes])
retain('sources.json', sources)
assert len(sources) == 7
print('Retained 18 paragraphs / two headings, two schema classes and seven external byte pins; no product execution.')
