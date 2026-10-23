"""Extract five documentary sections from the already pinned chapter; no network/runtime."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

P = Path(__file__).resolve().parent
DEVICES = ['drift', 'drum-sampler', 'meld', 'operator', 'wavetable']
source = P.parent / 'sample-instruments/manual-instruments-2026-10-19.html'
assert hashlib.sha256(source.read_bytes()).hexdigest() == '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a'

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.device = self.kind = None
        self.rows = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.device = attrs.get('id') if attrs.get('id') in DEVICES else None
        if self.device and tag in ['h2', 'h3', 'h4', 'h5', 'p', 'li'] and self.kind is None:
            self.kind = tag
            self.parts = []
            self.loc = {'html_line': self.getpos()[0], 'anchor': attrs.get('id'), 'section': attrs.get('data-number')}
    def handle_data(self, data):
        if self.kind:
            self.parts.append(data)
    def handle_endtag(self, tag):
        if self.kind == tag:
            text = ' '.join(''.join(self.parts).split())
            if text:
                self.rows.append({'device': self.device, 'kind': tag, 'text': text, **self.loc})
            self.kind = None

parser = Blocks()
parser.feed(source.read_text())
for device in DEVICES:
    rows = [r for r in parser.rows if r['device'] == device]
    assert rows and rows[0]['kind'] == 'h2'
    for i, row in enumerate(rows, 1):
        row['locator'] = f'{device}:B{i:03d}'
    data = (json.dumps(rows, indent=2, ensure_ascii=False) + '\n').encode()
    target = P / f'manual-{device}-blocks.json'
    if target.exists():
        assert target.read_bytes() == data
    else:
        target.write_bytes(data)
    (P / f'manual-{device}.txt').write_text('\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n')
    print(device, len(rows))
