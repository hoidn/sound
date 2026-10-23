"""Bounded documentary/package capture; no original-code execution."""
from pathlib import Path
from html.parser import HTMLParser
import gzip, hashlib, json, xml.etree.ElementTree as ET

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
APP = Path('/home/ollie/Ableton Live 12 Suite.app')
DEVICES = {'auto-filter':'AutoFilter2','channel-eq':'ChannelEq','eq-eight':'Eq8','eq-three':'FilterEQ3'}
def digest(b): return hashlib.sha256(b).hexdigest()
def save(name, b):
    p=P/name; p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_bytes()!=b: raise RuntimeError('Changed retained source: '+name)
    p.write_bytes(b)
    return {'path':name,'sha256':digest(b),'bytes':len(b)}
def js(name, value): return save(name,(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())

sources=[]
manual=P.parent/'audio-utilities/manual-audio-effects-2026-10-19.html'
b=manual.read_bytes()
assert digest(b)=='9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299'
sources.append({'id':'D12-AUDIO-EFFECTS','path':'../audio-utilities/'+manual.name,'external_pin':True,'url':'https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/','capture_date':'2026-10-19','version':'Version 12; no exact 12.4.3 publication pin','sha256':digest(b),'bytes':len(b)})
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=None; self.kind=None; self.buf=[]; self.rows=[]
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='h2': self.active=a.get('id') if a.get('id') in DEVICES else None
        if self.active and t in ['h2','h3','h4','p','li'] and self.kind is None:
            self.kind=t; self.buf=[]; self.loc={'html_line':self.getpos()[0],'anchor':a.get('id')}
    def handle_data(self,d):
        if self.kind:self.buf.append(d)
    def handle_endtag(self,t):
        if self.kind==t:
            s=' '.join(''.join(self.buf).split())
            if s:self.rows.append({'device':self.active,'kind':t,'text':s,**self.loc})
            self.kind=None
p=Parser();p.feed(b.decode())
for dev in DEVICES:
    rows=[x for x in p.rows if x['device']==dev];assert rows and rows[0]['kind']=='h2'
    for i,x in enumerate(rows,1):x['locator']=f'{dev}:B{i:02d}'
    js(f'manual-{dev}-blocks.json',rows)
    save(f'manual-{dev}.txt','\n'.join(f"{x['locator']} {x['kind']} #{x['anchor'] or ''} (HTML line {x['html_line']}) {x['text']}" for x in rows).encode())
schema=P.parent/'inventory/12.0_12402.txt';raw=schema.read_bytes()
assert digest(raw)=='b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
sources.append({'id':'PKG-SCHEMA','path':'../inventory/'+schema.name,'external_pin':True,'source_path':str(APP/'Contents/App-Resources/Schema/12.0_12402.txt'),'capture_date':'2026-10-19','sha256':digest(raw),'bytes':len(raw),'version':'12.0_12402 shipped in 12.4.3'})
classes=json.load(open(P.parent/'inventory/schema-classes.json'))['classes']
js('schema-fields.json',[x for x in classes if x['class'] in set(DEVICES.values())|{'AutoFilter','AutoFilterLfo','Eq8Band','Eq8BandParameter','Eq8SpectrumAnalyzer','SideChain','SidechainRoutingDeviceHelper'}])
inventory=json.load(open(P.parent/'inventory/devices.json'))
records=[]
for entry in inventory:
    if entry.get('schema_class') not in set(DEVICES.values())|{'AutoFilter'}:continue
    src=APP/entry['example']['path'];raw=src.read_bytes()
    assert digest(raw)==entry['example']['sha256']
    name='package/'+entry['name']+'/'+src.name
    sources.append({'id':'PKG-'+entry['id'].removeprefix('SURF-DEVICE-'),'source_path':str(src),'capture_date':'2026-10-19',**save(name,raw)})
    xml=gzip.decompress(raw);save(name+'.xml',xml)
    root=ET.fromstring(xml);nodes=list(root.iter(entry['schema_class']));assert len(nodes)==1
    values=[]
    def walk(e,path):
        if e.attrib:values.append({'path':path,'attributes':e.attrib})
        for c in e:walk(c,path+'/'+c.tag+(('[@Id="'+c.get('Id')+'"]') if c.get('Id') is not None else ''))
    walk(nodes[0],'/Ableton/'+entry['schema_class'])
    records.append({'device':entry['name'],'class':entry['schema_class'],'source':name,'root_attributes':root.attrib,'values':values})
assert len(records)==5
js('package-values.json',records);js('sources.json',sources)
print('Captured blocks:',{d:len([r for r in p.rows if r['device']==d]) for d in DEVICES})
print('Retained package documents:',len(records))
