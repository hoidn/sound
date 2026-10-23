"""Retain one inventory-routed official chapter and paragraph locators; no Live execution."""
from pathlib import Path
from html.parser import HTMLParser
import datetime
import hashlib
import json
import urllib.request

P = Path(__file__).resolve().parent
URL = 'https://www.ableton.com/en/live-manual/12/clip-view/'
path = P / 'manual-clip-view-2026-10-19.html'
if path.exists():
    source = json.loads((P / 'source.json').read_text())
    assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
else:
    with urllib.request.urlopen(URL, timeout=60) as response:
        data, final = response.read(), response.geturl()
    path.write_bytes(data)
    source = {'id':'D12-CLIP-VIEW','url':URL,'final_url':final,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':path.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'version':'Official reference Version 12; exact 12.4.3 applicability unknown','original_execution':False}
    (P / 'source.json').write_text(json.dumps(source,indent=2)+'\n')

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.kind = None
        self.rows = []
        self.headings = []
    def handle_starttag(self,tag,attrs):
        attrs = dict(attrs)
        if tag == 'aside':
            self.active = False
        if tag == 'h1' and attrs.get('id') == 'clip-view':
            self.active = True
        if self.active and tag in ['h1','h2','h3','h4','h5','p','li'] and self.kind is None:
            self.kind = tag
            self.parts = []
            self.loc = {'html_line':self.getpos()[0],'anchor':attrs.get('id'),'section':attrs.get('data-number')}
    def handle_data(self,data):
        if self.kind:
            self.parts.append(data)
    def handle_endtag(self,tag):
        if self.kind == tag:
            text = ' '.join(''.join(self.parts).split())
            if text:
                if tag.startswith('h'):
                    level=int(tag[1]);self.headings=[h for h in self.headings if h['level']<level]
                    self.headings.append({'level':level,'text':text,**self.loc})
                self.rows.append({'kind':tag,'text':text,**self.loc,'heading_context':list(self.headings)})
            self.kind = None
        if tag == 'main':
            self.active = False

parser = Blocks()
parser.feed(path.read_text())
assert len(parser.rows) == 180 and parser.rows[0]['kind']=='h1'
assert parser.rows[-1]['heading_context'][-1]['section'] == '8.14'
for i,row in enumerate(parser.rows,1):
    row['locator']=f'CV:B{i:03d}'
(P/'manual-blocks.json').write_text(json.dumps(parser.rows,indent=2,ensure_ascii=False)+'\n')
(P/'manual-text.txt').write_text('\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in parser.rows)+'\n')
print(json.dumps({'bytes':source['bytes'],'sha256':source['sha256'],'blocks':len(parser.rows),'first':parser.rows[0]['text'],'last':parser.rows[-1]['text'][:160]}))
