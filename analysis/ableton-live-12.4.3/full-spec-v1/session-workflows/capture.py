"""Extract Session chapter locators from an existing pinned source; no network/run."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json

PACKET = Path(__file__).resolve().parent
SOURCE = PACKET.parent / 'recording/manual-12-session-view-2026-10-19.html'
DIGEST = '16e29141f823e298d5fa7fee3b993861f6c38415f8432cd00ac89789e9470a31'


class Chapter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.kind = None
        self.rows = []
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            if attrs.get('id') == 'chapter_content':
                self.depth = 1
            elif self.depth:
                self.depth += 1
        if self.depth and tag in {'h1', 'h2', 'h3', 'h4', 'p', 'li'} and self.kind is None:
            self.kind, self.buf = tag, []
            self.line = self.getpos()[0]
            if tag.startswith('h'):
                self.anchor = attrs.get('id')

    def handle_data(self, value):
        if self.kind:
            self.buf.append(value)

    def handle_endtag(self, tag):
        if self.kind == tag:
            text = ' '.join(''.join(self.buf).split())
            if text:
                self.rows.append({'id': f'SV-B{len(self.rows)+1:03d}', 'tag': tag,
                                  'anchor': self.anchor, 'html_line': self.line, 'text': text})
            self.kind = None
        if tag == 'div' and self.depth:
            self.depth -= 1


def extract():
    raw = SOURCE.read_bytes()
    assert len(raw) == 267328 and hashlib.sha256(raw).hexdigest() == DIGEST
    parser = Chapter()
    parser.feed(raw.decode())
    assert parser.rows[0]['anchor'] == 'session-view'
    assert parser.rows[-1]['anchor'] == 'recording-sessions-into-the-arrangement'
    return parser.rows


if __name__ == '__main__':
    rows = extract()
    outputs = {
        'source-blocks.json': (json.dumps(rows, indent=2, ensure_ascii=False)+'\n').encode(),
        'source-blocks.txt': ('\n'.join(f"{r['id']} #{r['anchor']} HTML{r['html_line']} {r['text']}" for r in rows)+'\n').encode(),
    }
    for name, data in outputs.items():
        path = PACKET / name
        assert not path.exists() or path.read_bytes() == data, 'Refuse changed retained extract'
        path.write_bytes(data)
    print(f'{len(rows)} blocks extracted; original source unchanged')
