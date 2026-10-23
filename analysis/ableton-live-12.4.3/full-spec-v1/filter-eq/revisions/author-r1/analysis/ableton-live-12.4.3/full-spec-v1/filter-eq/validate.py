"""Check retained-document consistency only; never grade Live compatibility."""
from pathlib import Path
import gzip, hashlib, html, json, re, xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
SPECS=[ROOT/'wiki/specs/filter-eq-devices.md',ROOT/'wiki/research/filter-eq-devices.md']
def sha(b):return hashlib.sha256(b).hexdigest()
checks={};sources=json.load(open(P/'sources.json'))
for src in sources:
 b=(P/src['path']).read_bytes()
 assert len(b)==src['bytes'] and sha(b)==src['sha256'],src['id']
checks['source_hashes']=len(sources)
manual=(P/'../audio-utilities/manual-audio-effects-2026-10-19.html').read_text().splitlines()
blocks={}
for file in sorted(P.glob('manual-*-blocks.json')):
 rows=json.load(open(file));assert rows and rows[0]['kind']=='h2'
 for i,row in enumerate(rows,1):
  assert row['locator']==row['device']+f':B{i:02d}'
  line=manual[row['html_line']-1]
  # Some paragraph-inline image tags span source lines; strip complete tags.
  window='\n'.join(manual[row['html_line']-1:row['html_line']+100])
  normalized=' '.join(html.unescape(re.sub(r'<[^>]*>','',window)).split())
  assert row['text'] in normalized,(row['locator'],row['html_line'])
  if row['anchor']:assert 'id="'+row['anchor']+'"' in line,row['locator']
  blocks[row['locator']]=row
checks['manual_blocks']=len(blocks)
schema=(P/'../inventory/12.0_12402.txt').read_text().splitlines()
classes=json.load(open(P/'schema-fields.json'))
for cls in classes:
 assert schema[cls['line']-1].strip()=='<'+cls['class']+'>',(cls['class'],schema[cls['line']-1])
 start=cls['line']-1;end=next(i for i in range(start+1,len(schema)) if schema[i].strip()=='</'+cls['class']+'>')
 node=ET.fromstring('\n'.join(schema[start:end+1]))
 assert [{'name':f.tag,**f.attrib} for f in node]==cls['fields'],cls['class']
checks['schema_classes']=len(classes)
observations=json.load(open(P/'package-values.json'))
for o in observations:
 raw=(P/o['source']).read_bytes();xml=gzip.decompress(raw)
 assert xml==(P/(o['source']+'.xml')).read_bytes()
 root=ET.fromstring(xml);assert root.attrib==o['root_attributes']
 assert len(list(root.iter(o['class'])))==1
checks['package_documents']=len(observations)
reqs=json.load(open(P/'requirements.json'));cases=json.load(open(P/'cases.json'))
ids={r['id'] for r in reqs};assert len(ids)==len(reqs)
assert len({c['id'] for c in cases})==len(cases)
assert {r for c in cases for r in c['requirements']}==ids

def evidence(e):
 if e.startswith(('U','PKG-')):return
 device,parts=e.split(':',1)
 for part in parts.split(','):
  span=part.split('–');lo=int(span[0][1:]);hi=int(span[-1][1:])
  for n in range(lo,hi+1):assert device+f':B{n:02d}' in blocks,e
for r in reqs:
 assert re.fullmatch(r'REQ-DEVICE-(AF|CEQ|EQ8|EQ3)-\d{3}',r['id'])
 evidence(r['evidence'])
 assert ('### '+r['id']+' — '+r['title']) in SPECS[0].read_text()
for c in cases:
 assert c['status']=='unexecuted' and set(c['requirements'])<=ids
 assert c['setup_action'] and c['criterion']
 assert (c['expected'] is None)==(c['provenance']=='U'),c['id']
 evidence(c['evidence'])
 assert '| '+c['id']+' |' in SPECS[0].read_text()
 if 'file_assertions' in c:
  a=c['file_assertions'];root=ET.fromstring(gzip.decompress((P/a['path']).read_bytes()));node=root.find(a['class']);assert node is not None
  for path,expected in a['values'].items():assert node.find(path).get('Value')==expected,(c['id'],path)
for dev in ['AF','CEQ','EQ8','EQ3']:
 owned=[c for c in cases if c['device']==dev]
 kinds='/'.join(c['kind'] for c in owned)
 for kind in ['positive','negative','boundary','automation','malformed','cancel','undo','persistence','teardown','sample-rate']:assert kind in kinds,(dev,kind)
checks['requirements']=len(reqs);checks['cases']=len(cases)
checks['by_device']={dev:{'requirements':sum(r['device']==dev for r in reqs),'cases':{label:sum(c['device']==dev and c['provenance']==label for c in cases) for label in ['D12','Dpkg','U']}} for dev in ['AF','CEQ','EQ8','EQ3']}
for page in SPECS:
 text=page.read_text();assert text.startswith('---\n')
 header=text.split('---',2)[1]
 for key in ['id','type','status','updated','access']:assert re.search(r'^'+key+r': .+',header,re.M),(page,key)
 for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if link.startswith(('https://','http://','#')):continue
  path=link.split('#',1)[0];target=(page.parent/path).resolve()
  if target in [P/'manifest-author-r1.json',P/'validation-author-r1.json']:continue
  assert target.exists(),(page,link)
checks['canonical_pages']=2
report={'scope':'retained source/document/fixture consistency only; no Live or candidate execution; no audio pass','checks':checks,'external_source_pins':sum(bool(x.get('external_pin')) for x in sources),'original_web_capture_time':'date only; exact HTTP fetch timestamp unknown','index_log_coverage_integration':'root-owned; not checked here','result':'pass'}
(P/'validation-author-r1.json').write_text(json.dumps(report,indent=2)+'\n')
# The self manifest and future reviews are excluded to avoid recursive hashes.
paths=sorted(f for f in P.rglob('*') if f.is_file() and f.name!='manifest-author-r1.json')+SPECS
manifest={'id':'FILTER-EQ-AUTHOR-R1','status':'partial draft; ready for independent review','target':'Ableton Live 12 Suite 12.4.3','files':[{'path':str(f.relative_to(ROOT)),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in paths],'external_pins':sources[:2],'requirements':len(reqs),'cases':len(cases),'application_executions':0,'whole_device_complete':False}
(P/'manifest-author-r1.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert (P/'manifest-author-r1.json').exists() and (P/'validation-author-r1.json').exists()
print(json.dumps(report,indent=2))
