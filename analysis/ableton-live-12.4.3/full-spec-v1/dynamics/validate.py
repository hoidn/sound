"""Focused packet checks; asserts verify documentary fixtures, never Live behavior."""
from pathlib import Path
from html import unescape
import json,hashlib,gzip,xml.etree.ElementTree as ET,re,sys
P=Path(__file__).resolve().parent
R=P.parents[3]
def get(n):return json.loads((P/n).read_text())
def digest(p):
 b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
req=get('requirements.json');cases=get('cases.json');sources=get('sources.json');schemas=get('schema-fields.json');records=get('package-values.json')
assert len(req)==62 and len(cases)==129 and len(schemas)==5 and len(records)==5
assert len({r['id'] for r in req})==62 and len({c['id'] for c in cases})==129
for s in sources:
 assert digest(Path(s['path']))=={k:s[k] for k in ('sha256','bytes')},s
manual=Path(sources[0]['path']).read_text();lines=manual.splitlines()
for p in P.glob('manual-*-blocks.json'):
 rows=json.loads(p.read_text());assert len({r['locator'] for r in rows})==len(rows)
 for i,row in enumerate(rows):
  line=row['html_line'];assert 1<=line<=len(lines)
  # Paragraphs may span HTML lines (inline SVG); retain their exact starting line.
  end=rows[i+1]['html_line'] if i+1<len(rows) else line+64
  text=' '.join(unescape(re.sub('<[^>]*>','','\n'.join(lines[line-1:end]))).split())
  assert row['text'] in text,(row['locator'],line)
for record in records:
 root=ET.fromstring(gzip.decompress((P/record['file']).read_bytes()));el=root.find(record['class']);assert el is not None
 assert root.attrib==record['root_attributes']
 assert root.attrib['Creator']=='Ableton Live 12.4d1' and root.attrib['MinorVersion']=='12.0_12402'
 for f in record['fields']:assert ET.tostring(el.find(f['field']),encoding='unicode')==f['xml']
for r in req:
 for ev in r['evidence']:
  fname,loc=ev.split('#',1);data=get(fname)
  if loc.startswith('class='):assert any(x.get('class')==loc[6:] for x in data)
  else:assert any(x.get('locator')==loc for x in data)
 cc=[c for c in cases if c['requirement']==r['id']];assert cc,r['id']
for c in cases:
 assert any(r['id']==c['requirement'] and r['device']==c['device'] for r in req)
 assert c['input'] and c['comparison'] and c['execution'].startswith('unexecuted')
 assert (c['expected'] is None)==(c['provenance']=='U')
 if c['provenance']=='D12':assert c['exact_target_applicability']=='unknown'
for d in {r['device'] for r in req}:
 kinds={c['kind'] for c in cases if c['device']==d}
 assert {'boundary','negative','automation','persistence','undo','malformed','cancellation','transport','teardown'}<=kinds,(d,kinds)
# Local file links only; parent owns shared catalog and heading integration.
docs=[R/'wiki/specs/dynamics-devices.md',R/'wiki/research/dynamics-devices.md']
for doc in docs:
 text=doc.read_text();assert text.startswith('---\n')
 for field in ['id','type','status','updated','access']:assert re.search(r'^'+field+r': .+',text,re.M)
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if '://' in link or link.startswith('#'):continue
  target=(doc.parent/link.split('#')[0]).resolve()
  if target.name=='manifest-author-r1.json' and '--freeze' in sys.argv:continue
  assert target.exists(),str(target)
assert sorted(set(re.findall(r'^### (REQ-DYN-[A-Z-]+-\d{3})',docs[0].read_text(),re.M)))==sorted(r['id'] for r in req)
report={'scope':'Analyst documentary mechanics only; no application or candidate execution.','checks':['all seven source hashes and sizes','123 exact HTML line/text locators','five schema and preset roots/field XML','62 unique requirement IDs and129 case IDs','all requirements have cases; null U oracles; D12 target U','per-device required case kinds','changed-page file links and frontmatter'],'requirements':len(req),'cases':len(cases),'provenance_counts':{p:sum(c['provenance']==p for c in cases) for p in ['D12','Dpkg','U']},'separate_review':'pending; root assigns independent reviewer'}
manifest=P/'manifest-author-r1.json'
if '--freeze' in sys.argv:
 assert not manifest.exists(),'Frozen manifest already exists; create a new revision instead.'
 for doc,name in zip(docs,['spec-r1.md','research-r1.md']):(P/name).write_bytes(doc.read_bytes())
 (P/'validation-author-r1.json').write_text(json.dumps(report,indent=2)+'\n')
 payloads=[{'path':str(p.relative_to(P)),**digest(p)} for p in sorted(P.rglob('*')) if p.is_file() and p!=manifest]
 value={'id':'DYNAMICS-AUTHOR-R1','date':'2026-10-19','target':'Ableton Live12Suite12.4.3','status':'frozen partial author draft, independent review pending','payloads':payloads,'external_sources':[s for s in sources if not Path(s['path']).is_relative_to(P)],'draft_snapshots':{'spec-r1.md':'wiki/specs/dynamics-devices.md','research-r1.md':'wiki/research/dynamics-devices.md'},'not_established':['exact-build applicability of D12','effective DSP/timing','lifecycle behavior','complete device profile','implementation','compatibility pass']}
 manifest.write_text(json.dumps(value,indent=2)+'\n')
if manifest.exists():
 m=get(manifest.name)
 for entry in m['payloads']:assert digest(P/entry['path'])=={k:entry[k] for k in ['sha256','bytes']},entry['path']
 for entry in m['external_sources']:assert digest(Path(entry['path']))=={k:entry[k] for k in ['sha256','bytes']}
 print('Frozen payloads verified:',len(m['payloads']))
print(json.dumps(report,indent=2))
