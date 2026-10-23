"""Extract public manual sections from pinned captures; no network/runtime."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

P = Path(__file__).resolve().parent
INPUTS = [
    ('../sample-instruments/manual-instruments-2026-10-19.html', '3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a', ['analog', 'collision', 'electric', 'tension']),
    ('../audio-utilities/manual-audio-effects-2026-10-19.html', '9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299', ['amp', 'cabinet', 'corpus']),
]


class Sections(HTMLParser):
    def __init__(self, selected):
        super().__init__()
        self.selected = selected
        self.device = self.tag = None
        self.rows = []
        self.headings = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'h2':
            self.device = a.get('id') if a.get('id') in self.selected else None
        if self.device and self.tag is None and tag in ['h2', 'h3', 'h4', 'h5', 'p', 'li']:
            self.tag = tag
            self.buf = []
            self.meta = dict(html_line=self.getpos()[0], anchor=a.get('id'), section=a.get('data-number'))

    def handle_data(self, text):
        if self.tag:
            self.buf.append(text)

    def handle_endtag(self, tag):
        if tag == self.tag:
            text = ' '.join(''.join(self.buf).split())
            if text:
                if tag.startswith('h'):
                    level = int(tag[1])
                    self.headings = [h for h in self.headings if h['level'] < level]
                    self.headings.append(dict(level=level, text=text, **self.meta))
                self.rows.append(dict(device=self.device, kind=tag, text=text, heading_context=list(self.headings), **self.meta))
            self.tag = None


if __name__ == '__main__':
    for source, expected, devices in INPUTS:
        data = (P / source).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected
        parser = Sections(devices)
        parser.feed(data.decode())
        for device in devices:
            rows = [r for r in parser.rows if r['device'] == device]
            assert rows and rows[0]['anchor'] == device
            for i, r in enumerate(rows, 1):
                r['locator'] = f'{device}:B{i:03d}'
            outputs = {
                f'manual-{device}-blocks.json': (json.dumps(rows, indent=2, ensure_ascii=False) + '\n').encode(),
                f'manual-{device}.txt': ('\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows) + '\n').encode(),
            }
            for name, raw in outputs.items():
                path = P / name
                assert not path.exists() or path.read_bytes() == raw
                if not path.exists():
                    path.write_bytes(raw)
            print(device, len(rows))
