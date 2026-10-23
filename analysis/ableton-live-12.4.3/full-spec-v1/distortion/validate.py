"""Assert documentary packet integrity; never execute Live or grade unknown audio."""
from pathlib import Path
from html import unescape
import json,hashlib,gzip,xml.etree.ElementTree as ET,re,sys
P=Path(__file__).resolve().parent
R=P.parents[3]
def get(n):return json.loads((P/n).read_text())
def pin(p):
 b=p.read_bytes();return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def same(p,entry):assert pin(p)=={k:entry[k] for k in ('sha256','bytes')},str(p)
req=get('requirements.json');cases=get('cases.json');sources=get('sources.json');schemas=get('schema-fields.json');records=get('package-values.json')
assert (len(req),len(cases),len(schemas),len(records),len(sources))==(67,190,9,9,11)
assert len({r['id'] for r in req})==len(req) and len({c['id'] for c in cases})==len(cases)
# Verify the entire r1 seal before validating corrections; old root seal is unchanged.
archive=P/'archive-r1';oldseal=archive/'manifest-author-r1.json'
assert hashlib.sha256(oldseal.read_bytes()).hexdigest()=='5a75e9b74f218fb34b19dc46ad1134b63a7c4546ede9c10b379eea72262e5ade'
assert oldseal.read_bytes()==(P/'manifest-author-r1.json').read_bytes()
old=json.loads(oldseal.read_text());assert len(old['payloads'])==38
for entry in old['payloads']:same(archive/entry['path'],entry)
# Source bytes, derivations and signal definitions must remain invariant.
mutable={'requirements.json','cases.json','validate.py'}
for entry in old['payloads']:
 if entry['path'] not in mutable:assert (P/entry['path']).read_bytes()==(archive/entry['path']).read_bytes(),entry['path']
for s in sources:same(Path(s['path']),s)
oldcases=json.loads((archive/'cases.json').read_text())
assert [c['id'] for c in cases]==[c['id'] for c in oldcases]
changed=[]
for new,prior in zip(cases,oldcases):
 assert {k:v for k,v in new.items() if k!='input'}=={k:v for k,v in prior.items() if k!='input'}
 if new['input']!=prior['input']:changed.append(new['id'])
assert changed==['DST-EROSION-003','DST-EROSION-005','DST-EROSION-006']
positive=next(c for c in cases if c['id']=='DST-EROSION-003')
disabled=next(c for c in cases if c['id']=='DST-EROSION-005')
width=next(c for c in cases if c['id']=='DST-EROSION-006')
assert all(t in positive['input'] for t in ['Noise Blend=100%','accepted nonzero','Filter Width is enabled'])
assert 'modifier-drag Y' in disabled['input'] and disabled['expected'] is None and disabled['provenance']=='U'
assert all(t in width['input'] for t in ['only S1 first-second segment','1 second of 500 Hz','identical L/R','phase0','nonmuted processed output'])
assert width['expected'] is None and width['provenance']=='U'
oldreq=json.loads((archive/'requirements.json').read_text())
assert [r['id'] for r in req]==[r['id'] for r in oldreq]
assert [r['id'] for r,prior in zip(req,oldreq) if r!=prior]==['REQ-DST-EROSION-002']
response=get('review-response-r2.json');same(Path(response['review_input']['path']),response['review_input'])
original=get('../audio-utilities/sources.json')[0]
assert sources[0]['id']==original['id'] and sources[0]['sha256']==original['sha256']
manual=Path(sources[0]['path']).read_text();lines=manual.splitlines();count=0
for p in P.glob('manual-*-blocks.json'):
 rows=json.loads(p.read_text());assert len({r['locator'] for r in rows})==len(rows)
 for i,row in enumerate(rows):
  line=row['html_line'];assert 1<=line<=len(lines)
  end=rows[i+1]['html_line'] if i+1<len(rows) else line+64
  text=' '.join(unescape(re.sub('<[^>]*>','','\n'.join(lines[line-1:end]))).split())
  assert row['text'] in text,(row['locator'],line)
  count+=1
assert count==216
schema_text=Path(sources[1]['path']).read_text();schema_root=ET.fromstring(schema_text)
for s in schemas:
 e=schema_root.find(s['class']);assert e is not None
 assert '<'+s['class']+'>' in schema_text.splitlines()[s['line']-1]
 assert [{'name':c.tag,**c.attrib} for c in e]==s['fields']
for record in records:
 root=ET.fromstring(gzip.decompress((P/record['file']).read_bytes()));el=root.find(record['class']);assert el is not None
 assert root.attrib==record['root_attributes']
 assert root.attrib['Creator']=='Ableton Live 12.4d1' and root.attrib['MinorVersion']=='12.0_12402'
 for f in record['fields']:assert ET.tostring(el.find(f['field']),encoding='unicode')==f['xml']
for r in req:
 for ev in r['evidence']:
  fname,loc=ev.split('#',1);data=get(fname)
  assert any(x.get('class')==loc[6:] for x in data) if loc.startswith('class=') else any(x.get('locator')==loc for x in data)
 assert any(c['requirement']==r['id'] for c in cases),r['id']
for c in cases:
 assert any(r['id']==c['requirement'] and r['device']==c['device'] for r in req)
 assert c['input'] and c['comparison'] and c['execution'].startswith('unexecuted')
 assert (c['expected'] is None)==(c['provenance']=='U')
 if c['provenance']=='D12':assert c['exact_target_applicability']=='unknown'
 if c['kind']=='signal-interaction':assert c['provenance']=='U'
 # Verify named malformed numeric/enum mutations address actual retained fields.
 if c['kind']=='malformed':
  cl=next(r['evidence'][0].split('class=')[-1] for r in req if r['device']==c['device'] and r['provenance']=='Dpkg')
  el=ET.fromstring(gzip.decompress((P/next(r['file'] for r in records if r['class']==cl)).read_bytes())).find(cl)
  for mutation in c['input']['mutations']:
   if mutation.startswith('set '):
    path=mutation.split()[1];elem,attr=path.rsplit('/@',1)
    assert el.find(elem) is not None and attr in el.find(elem).attrib,(cl,path)
for d in {r['device'] for r in req}:
 kinds={c['kind'] for c in cases if c['device']==d}
 assert {'positive','boundary','negative','automation','persistence','undo','malformed','cancellation','transport','rate','teardown','signal-interaction'}<=kinds,(d,kinds)
signal=get('fixture-signals.json');assert set(signal['signals'])=={'S0','S1','S2','S3'} and len(signal['P-AUDIO'])==7
# Local links and frontmatter in assigned canonicals; root handles inbound indexes.
docs=[R/'wiki/specs/distortion-devices.md',R/'wiki/research/distortion-devices.md']
for doc in docs:
 text=doc.read_text();assert text.startswith('---\n')
 for field in ['id','type','status','updated','access']:assert re.search(r'^'+field+r': .+',text,re.M)
 for link in re.findall(r'\]\(([^)]+)\)',text):
  if '://' in link or link.startswith('#'):continue
  target=(doc.parent/link.split('#')[0]).resolve()
  if target.name in ['manifest-author-r2.json','validation-author-r2.json'] and '--freeze' in sys.argv:continue
  assert target.exists(),str(target)
text=docs[0].read_text()
assert sorted(re.findall(r'^### (REQ-DST-[A-Z-]+-\d{3})',text,re.M))==sorted(r['id'] for r in req)
assert sorted(re.findall(r'^\| (DST-[A-Z-]+-\d{3}) \|',text,re.M))==sorted(c['id'] for c in cases)
for r in req:assert r['contract'] in text,r['id']
for c in cases:
 row=next(l for l in text.splitlines() if l.startswith('| '+c['id']+' |'))
 assert c['requirement'] in row and (c['expected'] or 'U — expected outcome null; ungraded.') in row
 inp=c['input'] if isinstance(c['input'],str) else json.dumps(c['input'],ensure_ascii=False)
 assert inp.replace('|','\\|') in row,c['id']
report={'scope':'Documentary checks only; no original or candidate execution.','checks':['11 source hashes/byte counts and reused manual identity','216 exact HTML line/text block locators','9 schema class/line/field records checked against pinned XML','9 historical preset roots/fields and malformed field locators','67 unique requirements and190 case IDs with canonical rendered clauses/rows','each requirement has cases; all9 device lifecycle/kind sets','all143 U expected values null; all29 D12 exact-target applicability unknown','four proposed signals and7 path prerequisites','assigned canonical file links/frontmatter'],'r1_archive_payloads_verified':38,'r1_root_manifest_unchanged':True,'source_signal_invariance':True,'review_findings_addressed':['DST-REVIEW-01','DST-REVIEW-02'],'requirements':len(req),'cases':len(cases),'case_provenance':{p:sum(c['provenance']==p for c in cases) for p in ['D12','Dpkg','U']},'by_device':{d:{'requirements':sum(r['device']==d for r in req),'cases':sum(c['device']==d for c in cases)} for d in sorted({r['device'] for r in req})},'independent_review':'pending; separate reviewer required','runtime_result':'unexecuted'}
manifest=P/'manifest-author-r2.json'
if '--freeze' in sys.argv:
 assert not manifest.exists(),'Existing freeze immutable; create a new revision.'
 for doc,name in zip(docs,['spec-r2.md','research-r2.md']):(P/name).write_bytes(doc.read_bytes())
 (P/'validation-author-r2.json').write_text(json.dumps(report,indent=2)+'\n')
 payloads=[{'path':str(p.relative_to(P)),**pin(p)} for p in sorted(P.rglob('*')) if p.is_file() and p!=manifest and not p.is_relative_to(archive) and p.name not in {'manifest-author-r1.json','spec-r1.md','research-r1.md','validation-author-r1.json'}]
 value={'id':'DISTORTION-AUTHOR-R2','date':'2026-10-19','target':'Ableton Live 12 Suite 12.4.3','status':'frozen partial author draft; independent review pending','payloads':payloads,'external_sources':[s for s in sources if not Path(s['path']).is_relative_to(P)],'draft_snapshots':{'spec-r2.md':'wiki/specs/distortion-devices.md','research-r2.md':'wiki/research/distortion-devices.md'},'prior_revision':{'manifest':'archive-r1/manifest-author-r1.json','sha256':'5a75e9b74f218fb34b19dc46ad1134b63a7c4546ede9c10b379eea72262e5ade','payloads':38,'root_seal_unchanged':True},'not_established':['exact-build applicability of D12','audio DSP/timing/no-effect/normalization','random distributions/seed','lifecycle','complete device profile','candidate compatibility']}
 manifest.write_text(json.dumps(value,indent=2)+'\n')
if manifest.exists():
 m=get(manifest.name)
 for entry in m['payloads']:same(P/entry['path'],entry)
 for entry in m['external_sources']:same(Path(entry['path']),entry)
 for snap,path in m['draft_snapshots'].items():assert (P/snap).read_bytes()==(R/path).read_bytes(),path+' canonical differs from frozen draft'
 print('Frozen payloads verified:',len(m['payloads']))
print(json.dumps(report,indent=2))
