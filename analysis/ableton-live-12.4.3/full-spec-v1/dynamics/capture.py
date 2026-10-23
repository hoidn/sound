"""Retain bounded documentary dynamics evidence; never execute Live."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,gzip,xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
R=P.parents[3]
I=P.parent/'inventory'
A=Path('/home/ollie/Ableton Live 12 Suite.app')
DEV=['compressor','gate','glue-compressor','limiter','multiband-dynamics']
CL=['Compressor2','Gate','GlueCompressor','Limiter','MultibandDynamics']
def pin(p):
 b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def js(n,v):
 p=P/n;b=(json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
 if p.exists():assert p.read_bytes()==b, str(p)+' capture changed'
 else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
manual=P.parent/'audio-utilities/manual-audio-effects-2026-10-19.html'
assert pin(manual)['sha256']=='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.active=None;self.kind=None;self.rows=[];self.heading=None
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h2':self.active=a.get('id') if a.get('id') in DEV else None
  if self.active and t in ['h2','h3','h4','p','li'] and self.kind is None:self.kind=t;self.buf=[];self.loc={'html_line':self.getpos()[0],'anchor':a.get('id'),'section':a.get('data-number')}
 def handle_data(self,d):
  if self.kind:self.buf.append(d)
 def handle_endtag(self,t):
  if self.kind==t:
   s=' '.join(''.join(self.buf).split())
   if s:self.rows.append({'device':self.active,'kind':t,'text':s,**self.loc})
   self.kind=None
p=Parse();p.feed(manual.read_text())
for d in DEV:
 rows=[r for r in p.rows if r['device']==d]
 for i,r in enumerate(rows,1):r['locator']=f'{d}:B{i:03d}'
 assert rows and rows[0]['kind']=='h2'
 js('manual-'+d+'-blocks.json',rows)
 (P/('manual-'+d+'.txt')).write_text('\n'.join(f"{r['locator']} HTML:{r['html_line']} {r['text']}" for r in rows)+'\n')
sources=[{'id':'D12-AUDIO-EFFECTS','original_source_identity':'D12-AUDIO-EFFECTS in audio-utilities/sources.json','url':'https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/','capture_date':'2026-10-19','version':'Live Version 12, exact 12.4.3 applicability unknown',**pin(manual)}, {'id':'PKG-SCHEMA','version':'12.0_12402 shipped with pinned 12.4.3','capture_date':'2026-10-19',**pin(I/'12.0_12402.txt')}]
classes=json.loads((I/'schema-classes.json').read_text())['classes']
js('schema-fields.json',[r for r in classes if r['class'] in CL])
records=[]
for d in json.loads((I/'devices.json').read_text()):
 if d.get('schema_class') not in CL:continue
 f=A/d['example']['path'];b=f.read_bytes();assert hashlib.sha256(b).hexdigest()==d['example']['sha256']
 local=P/'package'/d['name']/f.name;local.parent.mkdir(parents=True,exist_ok=True)
 if local.exists():assert local.read_bytes()==b
 else:local.write_bytes(b)
 sources.append({'id':'PKG-'+d['id'],'original_path':str(f),'capture_date':'2026-10-19','historical_creator_is_not_current_constructor':True,**pin(local)})
 root=ET.fromstring(gzip.decompress(b));el=root.find(d['schema_class']);assert el is not None
 records.append({'surface':d['id'],'class':d['schema_class'],'file':str(local.relative_to(P)),'locator':'/Ableton/'+d['schema_class'],'root_attributes':root.attrib,'fields':[{'field':c.tag,'xml':ET.tostring(c,encoding='unicode')} for c in el]})
js('package-values.json',records);js('sources.json',sources)
print([(d,len([r for r in p.rows if r['device']==d])) for d in DEV]);print('schema classes',len([r for r in classes if r['class'] in CL]),'presets',len(records))
