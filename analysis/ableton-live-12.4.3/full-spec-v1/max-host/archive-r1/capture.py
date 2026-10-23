"""Capture one host manual chapter and copy five inventory-pinned templates as data."""
from pathlib import Path
from html.parser import HTMLParser
import datetime
import hashlib
import json
import urllib.request

P=Path(__file__).resolve().parent
APP=Path('/home/ollie/Ableton Live 12 Suite.app')
URL='https://www.ableton.com/en/live-manual/12/max-for-live/'
def digest(data):return hashlib.sha256(data).hexdigest()
def write(name,value):
    target=P/name
    data=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
    if target.exists():assert target.read_bytes()==data,target
    else:target.write_bytes(data)
path=P/'manual-max-for-live-2026-10-19.html'
if path.exists():
    source=json.loads((P/'source.json').read_text())
    assert digest(path.read_bytes())==source['sha256']
else:
    with urllib.request.urlopen(URL,timeout=60) as response:
        data,final=response.read(),response.geturl()
    path.write_bytes(data)
    source={'id':'D12-MAX-HOST','url':URL,'final_url':final,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'file':path.name,'bytes':len(data),'sha256':digest(data),'version':'Official Version 12; exact 12.4.3 applicability unknown','original_execution':False}
    write('source.json',source)

class Blocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active=False;self.kind=None;self.rows=[];self.headings=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='aside':self.active=False
        if tag=='h1' and attrs.get('id')=='max-for-live':self.active=True
        if self.active and tag in ['h1','h2','h3','h4','p','li'] and self.kind is None:
            self.kind=tag;self.parts=[];self.loc={'html_line':self.getpos()[0],'anchor':attrs.get('id'),'section':attrs.get('data-number')}
    def handle_data(self,data):
        if self.kind:self.parts.append(data)
    def handle_endtag(self,tag):
        if self.kind==tag:
            text=' '.join(''.join(self.parts).split())
            if text:
                if tag.startswith('h'):
                    level=int(tag[1]);self.headings=[h for h in self.headings if h['level']<level]
                    self.headings.append({'level':level,'text':text,**self.loc})
                self.rows.append({'kind':tag,'text':text,**self.loc,'heading_context':list(self.headings)})
            self.kind=None
parser=Blocks();parser.feed(path.read_text())
assert parser.rows[0]['section']=='32' and parser.rows[-1]['heading_context'][-1]['section']=='32.6'
for i,b in enumerate(parser.rows,1):b['locator']=f'MAX:B{i:03d}'
write('manual-blocks.json',parser.rows)
text='\n'.join(f"{b['locator']} HTML:{b['html_line']} {b['text']}" for b in parser.rows)+'\n'
(P/'manual-text.txt').write_text(text)
inv=json.loads((P.parent/'inventory/devices.json').read_text())
selected=[d for d in inv if d['kind'] in ['max-device','max-midi-tool','max-template']]
assert len(selected)==27
write('inventory-boundary.json',selected)
templates=[]
for d in selected:
    if d['kind']!='max-template':continue
    original=APP/d['source']['path'];data=original.read_bytes()
    assert len(data)==d['source']['bytes'] and digest(data)==d['source']['sha256']
    name=d['name'].lower().replace(' ','-')+'.amxd';target=P/name
    if target.exists():assert target.read_bytes()==data
    else:target.write_bytes(data)
    templates.append({'id':d['id'],'name':d['name'],'original_path':str(original),'file':name,'bytes':len(data),'sha256':digest(data),'prefix_hex':data[:16].hex(),'limit':'Exact supplied file identity only; contents not parsed, patch not executed, no inferred I/O/default/algorithm/API behavior'})
assert len(templates)==5
write('template-files.json',templates)
print(json.dumps({'manual_bytes':source['bytes'],'manual_sha256':source['sha256'],'blocks':len(parser.rows),'templates':len(templates),'inventory_only_devices':20,'inventory_only_tools':2,'original_execution':False}))
