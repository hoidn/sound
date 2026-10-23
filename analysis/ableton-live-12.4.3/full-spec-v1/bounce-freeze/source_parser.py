"""Retained-manual section parser; pure reads and parsing, no capture or writes."""
from html.parser import HTMLParser


class Section(HTMLParser):
    def __init__(self, anchor, stop_level=None):
        super().__init__()
        self.anchor, self.stop_level = anchor, stop_level
        self.active, self.current = False, None
        self.rows, self.headings = [], []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5'):
            if attrs.get('id') == self.anchor:
                self.active = True
            elif self.active and ((self.stop_level and int(tag[1]) <= self.stop_level) or (tag in ('h1', 'h2') and not attrs.get('data-number'))):
                self.active = False
        if self.active and self.current is None and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li'):
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


def extract(text, name, anchor, stop_level=None):
    parser = Section(anchor, stop_level)
    parser.feed(text)
    assert parser.rows and parser.rows[0]['anchor'] == anchor
    for i, row in enumerate(parser.rows, 1):
        row['locator'] = f'{name}:B{i:03d}'
    return parser.rows
