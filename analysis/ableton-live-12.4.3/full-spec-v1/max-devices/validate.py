"""Focused analyst packet check, including existing browser visibility; no patch execution."""
from pathlib import Path
from collections import Counter
import hashlib,html,importlib.util,json,re,subprocess,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def read(name):return json.loads((P/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=read('manifest-author-r1.json')
for r in manifest['payloads']+manifest['external_pins']:
 path=P/r['file'];assert path.is_file() and path.stat().st_size==r['bytes'] and sha(path)==r['sha256'],r
sources=read('sources.json');assert len(sources)==4
for r in sources:
 path=P/r['file'];assert path.stat().st_size==r['bytes'] and sha(path)==r['sha256']
assert sources[0]['sha256']=='b95a0d3ed3d7217505437a0d7d65de68d37e0f894d27e9869122fbfb89728a46'
assert sources[1]['sha256']=='42fbd3794df0d69aaf522aea589bf08dd3dc8db3eb0e135cab041093875db976'
blocks=read('manual-blocks.json');dated=read('dated-blocks.json')
assert len(blocks)==218 and len(dated)==15
assert blocks[0]['section']=='33' and blocks[-1]['heading_context'][-1]['section']=='33.3.6'
lines=(P/sources[0]['file']).read_text().splitlines()
for b in blocks:
 assert all(h['section'] and h['anchor'] for h in b['heading_context'])
 actual=' '.join(html.unescape(re.sub('<[^>]*>','',lines[b['html_line']-1])).split());assert b['text'] in actual,b['locator']
for page,name,count in [(721,'ds-sampler-p721.txt',6),(730,'expression-context-p730.txt',1),(731,'expression-legacy-p731.txt',8)]:
 derived=subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(P/sources[1]['file']),'-']).decode()
 assert derived==(P/name).read_text()
 own=[b for b in dated if b['pdf_page_1based']==page];assert len(own)==count
 for b in own:
  assert b['file']==name
  assert b['text']==' '.join(' '.join(derived.splitlines()[b['line_start']-1:b['line_end']]).split())
  if page==731:assert b['line_start']>=16 and b['section']=='30.3.3'
lookup={b['locator']:b for b in blocks+dated};assert len(lookup)==233
inv=read('inventory-devices.json');assert len(inv)==20
original_inv=json.loads((P/'../inventory/devices.json').read_text())
assert inv==[d for d in original_inv if d['kind']=='max-device']
identities=read('package-identities.json');assert len(identities)==20
for f in identities:
 d=next(d for d in inv if d['id']==f['id']);data=Path(f['original_path']).read_bytes()
 assert d['name']==f['name'] and len(data)==f['bytes']==d['source']['bytes']
 assert hashlib.sha256(data).hexdigest()==f['sha256']==d['source']['sha256'] and data[:16].hex()==f['prefix_hex']
requirements,cases=read('requirements.json'),read('cases.json')
assert len(requirements)==135 and len(cases)==315
assert Counter(r['provenance'] for r in requirements)=={'D12':88,'D12-2025':7,'Dpkg':20,'U':20}
assert Counter(c['provenance'] for c in cases)=={'D12':88,'D12-2025':7,'Dpkg':20,'U':200}
assert len({r['id'] for r in requirements})==135 and len({c['id'] for c in cases})==315
assert {r['id'] for r in requirements}=={r for c in cases for r in c['requirements']}
assert all(r['target_applicability']=='U' for r in requirements)
assert all(c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
for r in requirements:
 linked=[c for c in cases if r['id'] in c['requirements']]
 assert len(linked)==(10 if r['provenance']=='U' else 1)
 assert all(c['device']==r['device'] for c in linked)
 assert all(b in lookup for b in r['source_blocks'])
 if r['provenance'] in ['D12','D12-2025']:
  assert linked[0]['documentary_expected']==r['contract'] and linked[0]['source_blocks']==r['source_blocks']
  assert all((b.startswith('MX25:') if r['provenance']=='D12-2025' else b.startswith('MXD:')) for b in r['source_blocks'])
  assert r['source_blocks']
 if r['device']=='Expression Control Legacy' and r['provenance']=='D12-2025':
  assert all(b.startswith('MX25:731:') or b=='MX25:730:B001' for b in r['source_blocks'])
for c in cases:
 assert c['fixture']=='fixtures.json#MXD-F0'
 if c['provenance']=='U':assert c['documentary_expected'] is None and c['documentary_comparator'] is None and c['unknown']
 if c['kind'] in ['signal-obligation','timing-obligation']:assert c['documentary_comparator'] is None
kinds={'boundary','automation','transport','persistence','undo-redo','malformed','cancellation','teardown','sample-rate','routing'}
for d in inv:
 own=[r for r in requirements if r['surface']==d['id']]
 assert sum(r['provenance']=='Dpkg' for r in own)==1 and sum(r['provenance']=='U' for r in own)==1
 assert sum(r['provenance'] in ['D12','D12-2025'] for r in own)>=3
 assert {c['kind'] for c in cases if c['device']==d['name'] and c['provenance']=='U'}==kinds
fixture=read('fixtures.json');assert fixture['id']=='MXD-F0' and not fixture['original_execution'] and not fixture['candidate_comparison']
# Use existing parser read-only; do not regenerate the shared browser from a worker.
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows
spec=ROOT/'wiki/specs/max-for-live-devices.md'
browser_rows=spec_rows(spec,spec.read_text())
assert len(browser_rows)==135 and {r['id'] for r in browser_rows}=={r['id'] for r in requirements}
links=0
for r in manifest['canonical_snapshots']:
 canonical,snapshot=ROOT/r['canonical'],P/r['snapshot']
 assert canonical.read_bytes()==snapshot.read_bytes() and sha(canonical)==r['sha256']
 text=canonical.read_text();front=text.split('---',2)[1]
 assert text.startswith('---\n')
 for key in ['id','type','status','updated','access']:assert re.search(r'^'+key+r': .+',front,re.M)
 assert 'access: analysis' in front and 'updated: 2026-10-19' in front
 for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
  if '://' in dest or dest.startswith('#'):continue
  path,_,anchor=dest.partition('#');target=canonical.parent/path;assert target.is_file(),dest
  if anchor and target.suffix=='.json':assert json.loads(target.read_text()).get('id')==anchor
  links+=1
 assert not any(line.rstrip(' \t')!=line for line in text.splitlines())
for f in P.iterdir():
 if f.suffix in ['.json','.md','.py','.txt']:assert not any(line.rstrip(' \t')!=line for line in f.read_text().splitlines()),f
result={'result':'pass','scope':'Frozen packet/source identities,20 unparsed external AMXD hashes/prefixes,218 HTML paragraph lines,15 dated paragraph/text/PDF page derivations,version separation,135 normative IDs via existing spec_browser,315 cases/null outcomes/lifecycle kinds,canonical snapshots/metadata/relative links,untracked-aware whitespace only','payloads':len(manifest['payloads']),'external_pins':len(manifest['external_pins']),'documentary_sources':2,'inventory_pins':2,'package_file_pins':20,'requirements':135,'browser_requirements':135,'requirement_provenance':dict(Counter(r['provenance'] for r in requirements)),'cases':315,'case_provenance':dict(Counter(c['provenance'] for c in cases)),'target_graded':0,'local_links':links,'original_execution':False,'candidate_comparison':False,'independent_semantic_review':'pending','limits':['Figures uninspected','Dated-source revision is not exact-target parity','No AMXD patch content parsed or executed','External package files path-dependent;20 profiles partial','No audio/MIDI/Max API numerical oracle or runtime result','Shared catalogs/browser generation/log integration belongs to root']}
(P/'validation-author-r1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
