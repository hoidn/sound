"""Extract retained public documentation only; no original/candidate execution."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

P = Path(__file__).resolve().parent
BASE = P.parent
INPUTS = [
    ('routing', BASE / 'recording/manual-12-routing-and-i-o-2026-10-19.html', 'routing-and-io', '1a9c9c842c7a2d04b59794ee12d959f7fad15e3b67f41622109ea14e06e4b9b9'),
    ('compensation', BASE / 'racks/manual-devices-2026-10-19.html', 'device-delay-compensation', '6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82'),
    ('mixing', P / 'manual-12-mixing-2026-10-19.html', 'mixing', '255923c650a256ea0c663e83351e3ac0d8f14ba8dfe12706825754b2066de02e'),
]


class Extract(HTMLParser):
    def __init__(self, start):
        super().__init__()
        self.start = start
        self.active = False
        self.tag = None
        self.rows = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ['h1', 'h2']:
            if a.get('id') == self.start:
                self.active = True
            elif self.active and not a.get('data-number'):
                self.active = False
        if self.active and self.tag is None and tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']:
            self.tag = tag
            self.parts = []
            self.meta = dict(html_line=self.getpos()[0], anchor=a.get('id'), section=a.get('data-number'))

    def handle_data(self, data):
        if self.tag:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if self.tag == tag:
            text = ' '.join(''.join(self.parts).split())
            if text:
                if tag.startswith('h'):
                    level = int(tag[1])
                    self.headings = [h for h in self.headings if h['level'] < level]
                    self.headings.append(dict(level=level, text=text, **self.meta))
                self.rows.append(dict(kind=tag, text=text, heading_context=list(self.headings), **self.meta))
            self.tag = None


def immutable(path, data):
    if path.exists():
        assert path.read_bytes() == data, path
    else:
        path.write_bytes(data)


if __name__ == '__main__':
    for name, path, anchor, digest in INPUTS:
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        parser = Extract(anchor)
        parser.feed(data.decode())
        assert parser.rows and parser.rows[0]['anchor'] == anchor
        for i, r in enumerate(parser.rows, 1):
            r['locator'] = f'{name}:B{i:03d}'
        immutable(P / f'manual-{name}-blocks.json', (json.dumps(parser.rows, indent=2, ensure_ascii=False) + '\n').encode())
        immutable(P / f'manual-{name}.txt', ('\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in parser.rows) + '\n').encode())
        print(name, len(parser.rows))
