from pathlib import Path
from html.parser import HTMLParser
import urllib.request, hashlib, json, gzip, xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
ROOT=Path('/home/ollie/Documents/sound')
APP=Path('/home/ollie/Ableton Live 12 Suite.app')
URL='https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/'
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,data):
 p=P/name;p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=data:raise RuntimeError('Refusing to overwrite retained capture: '+name)
 p.write_bytes(data);return {'path':name,'sha256':sha(data),'bytes':len(data)}
def js(name,data):return save(name,(json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
cached=P/'manual-audio-effects-2026-10-19.html'
b=cached.read_bytes() if cached.exists() else urllib.request.urlopen(URL).read()
sources=[{'id':'D12-AUDIO-EFFECTS','url':URL,'capture_date':'2026-10-19','version':'Version 12; no exact 12.4.3 pin',**save('manual-audio-effects-2026-10-19.html',b)}]
class Parse(HTMLParser):
 def __init__(self):super().__init__();self.active=None;self.depth=0;self.buf=[];self.kind=None;self.rows=[];self.loc=None
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h2':self.active=a.get('id') if a.get('id') in ['utility','tuner','spectrum'] else None
  if self.active and t in ['h2','h3','h4','p','li'] and self.kind is None:self.kind=t;self.buf=[];self.loc={'html_line':self.getpos()[0],'anchor':a.get('id')}
 def handle_data(self,d):
  if self.kind:self.buf.append(d)
 def handle_endtag(self,t):
  if self.kind==t:
   s=' '.join(''.join(self.buf).split())
   if s:self.rows.append({'device':self.active,'kind':t,'text':s,**self.loc})
   self.kind=None
p=Parse();p.feed(b.decode());
for dev in ['utility','tuner','spectrum']:
 rows=[x for x in p.rows if x['device']==dev]
 for i,x in enumerate(rows,1):x['locator']=f'{dev}:B{i:02d}'
 js('manual-'+dev+'-blocks.json',rows)
 save('manual-'+dev+'.txt','\n'.join(f"{x['locator']} {x['kind']} #{x['anchor'] or ''} (HTML line {x['html_line']}) {x['text']}" for x in rows).encode())
schema=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/inventory/12.0_12402.txt'
sources.append({'id':'PKG-SCHEMA','source_path':str(schema),'capture_date':'2026-10-19','version':'12.0_12402 shipped in 12.4.3',**save('12.0_12402.txt',schema.read_bytes())})
classes=json.load(open(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/inventory/schema-classes.json'))['classes']
js('schema-fields.json',[x for x in classes if x['class'] in ['StereoGain','SpectrumAnalyzer','Tuner']])
files=[]
for dev in ['Utility','Spectrum']:
 for f in sorted((APP/'Contents/App-Resources/Core Library/Devices/Audio Effects'/dev).glob('*.adv')):
  if not f.name.startswith('._'):files.append((dev,f))
files.append(('Tuner',APP/'Contents/App-Resources/Core Library/Templates/Guitar Recording.als'))
records=[]
for dev,f in files:
 raw=f.read_bytes();name='package/'+dev+'/'+f.name
 sources.append({'id':'PKG-'+dev.upper()+'-'+f.stem.upper().replace(' ','-'),'source_path':str(f),'capture_date':'2026-10-19','target':'installed 12.4.3 package; historical Creator preserved',**save(name,raw)})
 root=ET.fromstring(gzip.decompress(raw));tag={'Utility':'StereoGain','Spectrum':'SpectrumAnalyzer','Tuner':'Tuner'}[dev]
 for i,e in enumerate(root.iter(tag)):
  fields=[]
  for child in e:
   vals=[{'relative_path':'/'.join([child.tag,z.tag]),**z.attrib} for z in child if z.tag in ['Manual','Min','Max']]
   if child.attrib or vals:fields.append({'field':child.tag,'attributes':child.attrib,'values':vals})
  records.append({'device':dev,'source':name,'root_attributes':root.attrib,'locator':f'.//{tag}[{i+1}]','fields':fields})
js('package-values.json',records)
js('sources.json',sources)
print('manual blocks',[(x,len(json.load(open(P/('manual-'+x+'-blocks.json'))))) for x in ['utility','tuner','spectrum']]);print('package files',len(files),'device occurrences',len(records))
