"""Pure retained-HTML chapter extraction; sources are data, never executed."""
from html.parser import HTMLParser


class Chapter(HTMLParser):
    def __init__(self, anchor):
        super().__init__()
        self.anchor, self.active, self.current = anchor, False, None
        self.rows, self.headings = [], []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'h1':
            if attrs.get('id') == self.anchor:
                self.active = True
            elif self.active:
                self.active = False
        elif self.active and tag == 'h2' and not attrs.get('data-number'):
            self.active = False
        if self.active and self.current is None and tag in ('h1', 'h2', 'h3', 'h4', 'p', 'li'):
            self.current = (tag, attrs, self.getpos()[0], [])

    def handle_data(self, data):
        if self.current:
            self.current[3].append(data)

    def handle_endtag(self, tag):
        if self.current and self.current[0] == tag:
            kind, attrs, line, parts = self.current
            self.current = None
            text = ' '.join(''.join(parts).split())
            if not text:
                return
            meta = dict(html_line=line, anchor=attrs.get('id'), section=attrs.get('data-number'))
            if kind.startswith('h'):
                level = int(kind[1])
                self.headings = [h for h in self.headings if h['level'] < level]
                self.headings.append(dict(level=level, text=text, **meta))
            self.rows.append(dict(kind=kind, text=text, heading_context=list(self.headings), **meta))


def extract(text, name):
    parser = Chapter(name)
    parser.feed(text)
    assert parser.rows and parser.rows[0]['anchor'] == name
    for i, row in enumerate(parser.rows, 1):
        row['locator'] = f'{name}:B{i:03d}'
    return parser.rows
