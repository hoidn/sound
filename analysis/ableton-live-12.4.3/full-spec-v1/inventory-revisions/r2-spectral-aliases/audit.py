"""Read-only package association audit; no original code or compatibility tests."""
from pathlib import Path
import gzip,hashlib,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[5]
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/inventory'
APP=Path('/home/ollie/Ableton Live 12 Suite.app')
sha=lambda b:hashlib.sha256(b).hexdigest()
ledger=json.loads((BASE/'devices.json').read_text())
schema=(BASE/'12.0_12402.txt').read_text().splitlines()
observed=[]
for name,expected,count in [('Spectral Resonator','Transmute',8),('Spectral Time','Spectral',6)]:
 folder=APP/'Contents/App-Resources/Core Library/Devices/Audio Effects'/name
 rows=[]
 for f in sorted(folder.rglob('*.adv')):
  if f.name.startswith('._'):continue
  b=f.read_bytes();xml=ET.fromstring(gzip.decompress(b));classes=[x.tag for x in xml]
  assert classes==[expected],(str(f),classes)
  rows.append({'path':str(f.relative_to(APP)),'bytes':len(b),'sha256':sha(b),'root_attributes':xml.attrib,'root_children':classes})
 assert len(rows)==count
 line=next(i for i,x in enumerate(schema,1) if x.strip()=='<'+expected+'>')
 end=next(i for i in range(line,len(schema)) if schema[i].strip()=='</'+expected+'>')
 fields=[n.tag for n in ET.fromstring('\n'.join(schema[line-1:end+1]))]
 observed.append({'device_folder':name,'class':expected,'schema_line':line,'preset_count':len(rows),'presets':rows,'schema_fields':fields,'runtime_alias_and_behavior':'not tested; artifact association only'})
# Catch the exact two crossed named factory-example associations in the old ledger;
# Set/template/default-dropping examples are explicitly outside this path assertion.
mismatches=[]
for x in ledger:
 e=x.get('example')
 if x['kind']=='native' and e and '/Core Library/Devices/Audio Effects/' in e['path'] and x['name'] not in e['path']:
  mismatches.append(x['id'])
assert mismatches==['SURF-DEVICE-SPECTRAL-RESONATOR','SURF-DEVICE-SPECTRAL-TIME'],mismatches
out={'scope':'installed folder/preset/schema associations; no runtime, DSP or complete profile pass','original_ledger_sha256':sha((BASE/'devices.json').read_bytes()),'original_schema_sha256':sha((BASE/'12.0_12402.txt').read_bytes()),'factory_example_mismatches_in_original':mismatches,'observations':observed}
print(json.dumps(out,indent=2))
