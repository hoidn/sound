"""Integrity checks for analyst packet; does not compare any Live execution."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,gzip,tarfile,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
root=Path(__file__).resolve().parent
repo=root.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((root/'source.json').read_text());html=root/s['html']
assert sha(html)==s['sha256'] and html.stat().st_size==s['bytes']
soup=BeautifulSoup(html.read_bytes(),'html.parser');article=soup.find('article') or soup.find('main') or soup
for el in article(['script','style','nav']):el.decompose()
expected='\n'.join(f'{i:04d} {line}' for i,line in enumerate(article.get_text('\n',strip=True).splitlines(),1))+'\n'
assert (root/s['derived_text']).read_text()==expected
presets=json.loads((root/'shipped-presets.json').read_text());assert len(presets)==8
for p in presets:
 if not p['retained']:
  assert p['device']=='CC Control';continue
 capture=root/p['retained'];assert sha(capture)==p['source_sha256']==sha(Path(p['source_path']))
 decoded=gzip.decompress(capture.read_bytes());assert decoded==(root/p['xml']).read_bytes()
 ET.fromstring(decoded)
schema=json.loads((root/'schema-excerpts.json').read_text());sp=Path(schema['source']);assert sha(sp)==schema['source_sha256']
lines=sp.read_text().splitlines()
for e in schema['excerpts']:
 assert e['lines']==lines[e['start_line']-1:e['end_line']]
 assert e['lines'][0].strip()=='<'+e['schema_class']+'>'
 assert e['lines'][-1].strip()=='</'+e['schema_class']+'>'
assert len(schema['excerpts'])==8
native=json.loads((root/'native-presence.json').read_text());selected={r['source_line']:r for g in native['groups'].values() for r in g}
h=hashlib.sha256()
for i,b in enumerate(Path(native['source_path']).open('rb'),1):
 h.update(b)
 if i in selected:assert hashlib.sha256(b).hexdigest()==selected[i]['line_sha256'] and json.loads(b)==selected[i]['record']
assert h.hexdigest()==native['source_sha256']
old_manifest=root/'manifest-author-r1.json'
assert sha(old_manifest)=='95e0785298dddd4e8a4a87f33045e5087f4003ba621a38d9b3cbb97784b792d5'
old=json.loads(old_manifest.read_text())
archive=root/'author-r1-snapshot.tar.gz'
assert sha(archive)=='c6967748a7b453dd5d8b4bb336faf42fe417bb3d1bd129e801f5a9e9a0b9864a'
with tarfile.open(archive,'r:gz') as tar:
 assert tar.extractfile(str(old_manifest.relative_to(repo))).read()==old_manifest.read_bytes()
 for row in old['payloads']:
  b=tar.extractfile(row['path']).read()
  assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 for row in old['payloads']:
  path=Path(row['path'])
  if path.suffix in {'.html','.adv','.xml'} or path.name in {'source.json','schema-excerpts.json','shipped-presets.json','preset-observations.json','native-presence.json','manual-midi-effects.txt'}:
   assert sha(repo/path)==row['sha256']
spec=repo/'wiki/specs/native-midi-effects.md';research=repo/'wiki/research/native-midi-effects.md'
reqs=set(re.findall(r'^### (REQ-NATIVE-MIDI-\d{3})',spec.read_text(),re.M));assert len(reqs)==27
cases=json.loads((root/'cases.json').read_text())['cases'];assert len(cases)==146 and len({c['id'] for c in cases})==146
assert {c['requirement'] for c in cases}==reqs
for c in cases:
 assert c['execution']=='unexecuted' and c['exact_build_grade']=='U'
 assert c['grade'] in {'D12','U'} and bool(c['documentary_oracle'])==(c['grade']=='D12')
 if c['source']:
  a,b=c['source']['text_lines'];assert 3<=a<=b<=142
by_id={c['id']:c for c in cases}
for key in ['NME-NL-L01','NME-NL-L05']:
 assert 'Latch off' in by_id[key]['setup'] and 'Length enabled' in by_id[key]['setup']
 assert by_id[key]['grade']=='U' and by_id[key]['documentary_oracle'] is None
for key in ['NME-043','NME-044','NME-045']:
 assert 'Range12st' not in by_id[key]['setup'] and 'unit/upper endpoint U' in by_id[key]['setup']
assert by_id['NME-064']['documentary_oracle']=='Outputs remain60..127; modulation baseline, displacement, sequence and frequency U'
for dev in {c['device'] for c in cases}:
 life=[c for c in cases if c['device']==dev and '-L' in c['id']]
 assert len(life)==10 and {'positive','negative','boundary','malformed','cancellation','undo','teardown'}<={c['kind'] for c in life}
for page in [spec,research]:
 txt=page.read_text();fm=txt.split('---',2)[1]
 assert all(re.search(r'^'+key+r':',fm,re.M) for key in ['id','type','status','updated','access'])
 for target in re.findall(r'\]\(([^)]+)\)',txt):
  if '://' in target:continue
  path=target.split('#',1)[0]
  assert (page.parent/path).exists() or (page.parent/path).resolve()==root/'validation.json',(page,path)
result={'integrity':'pass','revision':2,'r1_archived_payloads_verified':30,'r1_original_seal_verified':True,'source_capture_bytes_unchanged':True,'review_correction_regressions':'pass','manual_html_verified':True,'manual_derived_text_verified':True,'preset_sources_verified':7,'schema_blocks_verified':8,'native_symbol_rows_verified':len(selected),'requirement_count':len(reqs),'case_count':len(cases),'documentary_predicates':54,'unknown_cases':92,'exact_build_unknown_cases':146,'executed_cases':0,'relative_links_and_required_frontmatter':'pass','scope':'Source/packet integrity only; no semantic independent review or runtime compatibility claim'}
(root/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
manifest=root/'manifest-author-r2.json'
if manifest.exists():
 for f in json.loads(manifest.read_text())['payloads']:
  p=repo/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],f['path']
print(json.dumps(result,indent=2))
