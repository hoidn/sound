"""One Max-device reference chapter and exact inventory associations; no patch execution."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,urllib.request
P=Path(__file__).resolve().parent
URL='https://www.ableton.com/en/live-manual/12/max-for-live-devices/'
def sha(data):return hashlib.sha256(data).hexdigest()
def write(name,value):
 data=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode();path=P/name
 if path.exists():assert path.read_bytes()==data,path
 else:path.write_bytes(data)
path=P/'manual-max-devices-2026-10-19.html'
if path.exists():
 source=json.loads((P/'source.json').read_text());assert sha(path.read_bytes())==source['sha256']
else:
 with urllib.request.urlopen(URL,timeout=60) as response:data,final=response.read(),response.geturl()
 path.write_bytes(data);source={'id':'D12-MAX-DEVICES','url':URL,'final_url':final,'file':path.name,'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':len(data),'sha256':sha(data),'version':'Official Version 12; exact12.4.3 applicability unknown','original_execution':False};write('source.json',source)
class Blocks(HTMLParser):
 def __init__(self):
  super().__init__();self.active=False;self.kind=None;self.rows=[];self.headings=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='aside':self.active=False
  if tag=='h1' and attrs.get('id')=='max-for-live-devices':self.active=True
  if self.active and tag in ['h1','h2','h3','h4','h5','p','li'] and self.kind is None:
   self.kind=tag;self.parts=[];self.loc={'html_line':self.getpos()[0],'anchor':attrs.get('id'),'section':attrs.get('data-number')}
 def handle_data(self,data):
  if self.kind:self.parts.append(data)
 def handle_endtag(self,tag):
  if self.kind==tag:
   text=' '.join(''.join(self.parts).split())
   if text:
    if tag.startswith('h'):
     level=int(tag[1]);self.headings=[h for h in self.headings if h['level']<level];self.headings.append({'level':level,'text':text,**self.loc})
    self.rows.append({'kind':tag,'text':text,**self.loc,'heading_context':list(self.headings)})
   self.kind=None
parser=Blocks();parser.feed(path.read_text())
for i,b in enumerate(parser.rows,1):b['locator']=f'MXD:B{i:03d}'
assert parser.rows[0]['section']=='33' and parser.rows[-1]['heading_context'][-1]['section']=='33.3.6'
write('manual-blocks.json',parser.rows)
(P/'manual-text.txt').write_text('\n'.join(f"{b['locator']} HTML:{b['html_line']} {b['text']}" for b in parser.rows)+'\n')
inv=json.loads((P.parent/'inventory/devices.json').read_text());selected=[d for d in inv if d['kind']=='max-device'];assert len(selected)==20;write('inventory-devices.json',selected)
print(json.dumps({'sha256':source['sha256'],'bytes':source['bytes'],'blocks':len(parser.rows),'inventory_profiles':len(selected)}))
