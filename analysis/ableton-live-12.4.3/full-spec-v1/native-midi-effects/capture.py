"""Read official HTML and installed data only; no original code execution."""
from pathlib import Path
import hashlib,json,urllib.request,gzip,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
url='https://www.ableton.com/en/live-manual/12/live-midi-effect-reference/'
html=root/'manual-12-midi-effects-2026-10-19.html'
if html.exists():
 raw=html.read_bytes()
else:
 raw=urllib.request.urlopen(url).read();html.write_bytes(raw)
soup=BeautifulSoup(raw,'html.parser');article=soup.find('article') or soup.find('main') or soup
for e in article(['script','style','nav']):e.decompose()
lines=article.get_text('\n',strip=True).splitlines()
(root/'manual-midi-effects.txt').write_text('\n'.join(f'{i:04d} {line}' for i,line in enumerate(lines,1))+'\n')
heads=[{'tag':h.name,'id':h.get('id'),'text':h.get_text(' ',strip=True)} for h in article.find_all(['h1','h2','h3'])]
source={'id':'SRC-NATIVE-MIDI-MANUAL-20261019','url':url,'capture_date':'2026-10-19','edition':'Live 12; exact publication revision unstated','target_applicability':'12.4.3 unknown','html':html.name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'derived_text':'manual-midi-effects.txt','headings':heads}
(root/'source.json').write_text(json.dumps(source,indent=2)+'\n')
base=Path('/home/ollie/Ableton Live 12 Suite.app')
devices=json.loads((root.parent/'inventory/devices.json').read_text())
names={'Arpeggiator','CC Control','Chord','Note Length','Pitch','Random','Scale','Velocity'}
rows=[]
for d in devices:
 if d['name'] not in names:continue
 if d['example'] is None:
  rows.append({'device':d['name'],'surface_id':d['id'],'schema_class':d['schema_class'],'schema_line':d['schema_line'],'retained':None,'limitation':'no example preset in inventory'})
  continue
 p=base/d['example']['path'];b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==d['example']['sha256']
 copy=root/(d['name'].replace(' ','-').lower()+'-shipped.adv');copy.write_bytes(b)
 xml=gzip.decompress(b) if b[:2]==b'\x1f\x8b' else b
 xp=copy.with_suffix('.xml');xp.write_bytes(xml)
 rows.append({'device':d['name'],'surface_id':d['id'],'schema_class':d['schema_class'],'schema_line':d['schema_line'],'source_path':str(p),'source_sha256':hashlib.sha256(b).hexdigest(),'retained':copy.name,'xml':xp.name,'locator':d['example']['locator'],'root_tag':ET.fromstring(xml).tag})
(root/'shipped-presets.json').write_text(json.dumps(rows,indent=2)+'\n')
schema=root.parent/'inventory/12.0_12402.txt';b=schema.read_bytes()
assert hashlib.sha256(b).hexdigest()=='b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299'
text=schema.read_text().splitlines();excerpts=[]
for d in rows:
 start=d['schema_line']-1;end=next(i+1 for i in range(start+1,len(text)) if text[i].strip()=='</'+d['schema_class']+'>')
 excerpts.append({'device':d['device'],'schema_class':d['schema_class'],'start_line':start+1,'end_line':end,'lines':text[start:end]})
(root/'schema-excerpts.json').write_text(json.dumps({'source':str(schema),'source_sha256':hashlib.sha256(b).hexdigest(),'excerpts':excerpts},indent=2)+'\n')
assert len(rows)==8 and len(heads)>=9
print(json.dumps({'manual_bytes':source['bytes'],'manual_sha256':source['sha256'],'presets':len(rows),'headings':heads},indent=2))
