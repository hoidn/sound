"""Pure article.body HTML parsing; never executes, fetches or mutates a source."""
from html.parser import HTMLParser


class Body(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.headings, self.rows = [], []

    def handle_starttag(self, tag, attributes):
        if self.current is None and tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'th', 'td'):
            self.current = (tag, dict(attributes), self.getpos()[0], [])

    def handle_data(self, text):
        if self.current:
            self.current[3].append(text)

    def handle_endtag(self, tag):
        if self.current and self.current[0] == tag:
            kind, attrs, line, parts = self.current
            self.current = None
            text = ' '.join(''.join(parts).split())
            if not text:
                return
            if kind.startswith('h'):
                level = int(kind[1])
                self.headings = [h for h in self.headings if h['level'] < level]
                self.headings.append(dict(level=level, text=text, body_html_line=line, anchor=attrs.get('id')))
            self.rows.append(dict(kind=kind, text=text, body_html_line=line, anchor=attrs.get('id'), heading_context=list(self.headings)))


def extract(body, prefix, source_id):
    parser = Body()
    parser.feed(body)
    assert parser.current is None
    for i, row in enumerate(parser.rows, 1):
        row['id'] = f'{prefix}-B{i:03d}'
        row['source_id'] = source_id
        row['source_pointer'] = '/article/body'
    return parser.rows
