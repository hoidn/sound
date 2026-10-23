"""Check preserved documentary launch packet and browser IDs; no source/runtime execution."""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib,html,json,re,sys
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
def read(name):return json.loads((P/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
initial=read('resumed-inputs.json')['files'];assert len(initial)==4
for name,r in initial.items():
 path=P/name;assert path.stat().st_size==r['bytes'] and sha(path)==r['sha256']
source=read('source.json')
assert source['sha256']=='dc9c4e21a480e1adeeb2daf548d34547ccb73153a2561fb93f56391f003a82af' and source['bytes']==262997
assert source['url']=='https://www.ableton.com/en/live-manual/12/launching-clips/'
assert sha(P/source['file'])==source['sha256']
blocks=read('source-blocks.json');assert len(blocks)==73
lookup={b['id']:b for b in blocks};assert len(lookup)==73
lines=(P/source['file']).read_text().splitlines();raw=(P/source['file']).read_text()
for b in blocks:
 assert 280<=b['html_line']<=508
 assert 'id="'+b['anchor']+'"' in raw

class Paragraphs(HTMLParser):
 def __init__(self):
  super().__init__();self.active=False;self.kind=None;self.anchor=None;self.rows=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=='aside':self.active=False
  if tag=='h1' and attrs.get('id')=='launching-clips':self.active=True
  if self.active and tag in ['h1','h2','h3','h4','p','li'] and self.kind is None:
   if tag.startswith('h'):self.anchor=attrs.get('id')
   self.kind=tag;self.parts=[];self.line=self.getpos()[0]
 def handle_data(self,data):
  if self.kind:self.parts.append(data)
 def handle_endtag(self,tag):
  if tag==self.kind:
   text=' '.join(''.join(self.parts).split())
   if text:self.rows.append({'id':f'LC-B{len(self.rows)+1:03d}','tag':tag,'anchor':self.anchor,'html_line':self.line,'text':text})
   self.kind=None
parser=Paragraphs();parser.feed(raw)
assert parser.rows==blocks, 'HTML paragraph reproduction including multiline image tags'
requirements,cases=read('requirements.json'),read('cases.json')
assert len(requirements)==43 and len(cases)==68
assert Counter(r['provenance'] for r in requirements)=={'D12':37,'U':6}
assert Counter(c['provenance'] for c in cases)=={'D12':37,'U':31}
assert len({r['id'] for r in requirements})==43 and len({c['id'] for c in cases})==68
assert {r['id'] for r in requirements}=={r for c in cases for r in c['requirements']}
assert all(r['target_applicability']=='U' for r in requirements)
assert all(c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False for c in cases)
for r in requirements:
 linked=[c for c in cases if r['id'] in c['requirements']]
 assert all(b in lookup for b in r['source_blocks'])
 if r['provenance']=='D12':
  assert len(linked)==1 and linked[0]['source_claim']==r['contract'] and linked[0]['source_blocks']==r['source_blocks']
 else:
  assert linked and all(c['provenance']=='U' and c['documentary_expected'] is None and c['documentary_comparator'] is None and c['unknown'] for c in linked)
for c in cases:
 assert c['fixture']=='fixtures.json#SLC-F0'
 if c['kind'] not in ['documented-control','documented-state']:
  assert c['documentary_expected'] is None and c['documentary_comparator'] is None,c['id']
 if c['fixture_group'] in ['FOLLOW','SCENES','CHAIN']:
  assert 'active-follow-guard' in c['preconditions']
for prefix in ['CLIP','SCENE']:
 own=[c for c in cases if 'REQ-SESSION-LAUNCH-U-'+prefix+'-LIFECYCLE' in c['requirements']]
 assert len(own)==10
 assert {c['kind'] for c in own}=={'automation','transport','persistence','undo-redo','malformed','cancellation','source-loss','teardown','sample-rate','signal-obligation'}
fixture=read('fixtures.json')
assert fixture['id']=='SLC-F0' and not fixture['original_execution'] and not fixture['candidate_comparison']
assert 'Both local Follow' in fixture['active-follow-guard'] and 'Globally on' in fixture['active-follow-guard']
assert 'positive baseline' in fixture['active-follow-guard'] and 'nonzero' in fixture['active-follow-guard']
context=read('boundary-context.json');assert len(context)==4
assert {r['id'] for r in context}=={f'REQ-CLIP-LAUNCH-{n:03d}' for n in [20,21,22,23]}
assert all('**U.**' in r['retained_section'] for r in context)
for r in context:
 current=(ROOT/r['canonical']).read_text()
 section=re.search(r'^### '+r['id']+r'[^\n]*\n(.*?)(?=^### |^## |\Z)',current,re.M|re.S)
 assert section and section[0]==r['retained_section'],r['id']
assert lookup['LC-B021']['anchor']=='clip-launch-quantization' and lookup['LC-B047']['anchor']=='follow-actions'
assert any(r['source_blocks']==['LC-B021','LC-B047'] and r['provenance']=='U' for r in requirements)
assert any(r['source_blocks']==['LC-B033'] and r['provenance']=='U' for r in requirements)
sys.path.insert(0,str(ROOT/'tools'))
from spec_browser import spec_rows,anchor
spec=ROOT/'wiki/specs/session-launch-workflows.md'
browser=spec_rows(spec,spec.read_text())
assert len(browser)==43 and {r['id'] for r in browser}=={r['id'] for r in requirements}
counts=read('counts.json');assert counts['requirements']==43 and counts['cases']==68 and counts['target_graded']==0
assert counts['case_kinds']==dict(Counter(c['kind'] for c in cases))
manifest=read('manifest-author-r1.json')
for r in manifest['payloads']+manifest['external_pins']:
 path=P/r['file'];assert path.is_file() and path.stat().st_size==r['bytes'] and sha(path)==r['sha256'],r
links=0
for r in manifest['canonical_snapshots']:
 canonical,snapshot=ROOT/r['canonical'],P/r['snapshot']
 assert canonical.read_bytes()==snapshot.read_bytes() and sha(canonical)==r['sha256']
 text=canonical.read_text();front=text.split('---',2)[1];assert text.startswith('---\n')
 for key in ['id','type','status','updated','access']:assert re.search(r'^'+key+r': .+',front,re.M)
 assert 'access: analysis' in front and 'updated: 2026-10-19' in front
 for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
  if '://' in dest or dest.startswith('#'):continue
  path,_,fragment=dest.partition('#');target=canonical.parent/path;assert target.is_file(),dest
  if fragment and target.suffix=='.json':assert json.loads(target.read_text()).get('id')==fragment
  if fragment and target.suffix=='.md':assert fragment in {anchor(h) for h in re.findall(r'^#+ (.+)$',target.read_text(),re.M)},dest
  links+=1
 assert not any(line.rstrip(' \t')!=line for line in text.splitlines())
for f in P.iterdir():
 if f.suffix in ['.json','.md','.py','.txt']:assert not any(line.rstrip(' \t')!=line for line in f.read_text().splitlines()),f
result={'result':'pass','scope':'Four preserved inputs/source hash;73 exact HTML text/anchor locators;43 requirement IDs via existing spec_browser;68 source/case relationships and null target/signal/timing/RNG oracles;clip/scene lifecycle kinds and guards;retained old-U context;frozen payload/canonical snapshots,relative links/anchors,metadata and untracked-aware whitespace only','preserved_inputs':4,'source_blocks':73,'requirements':43,'requirement_provenance':{'D12':37,'U':6},'browser_requirements':43,'cases':68,'case_provenance':{'D12':37,'U':31},'target_graded':0,'payloads':len(manifest['payloads']),'external_pins':len(manifest['external_pins']),'local_links':links,'original_execution':False,'candidate_comparison':False,'independent_semantic_review':'pending','limits':['Inline action figures/images not inspected;no image-derived label/runtime association','Global Follow quantization and A/B UI coupling unresolved','No source controller/media/render or runtime result','Existing storage/normalization/grid/X timing and four runtime U requirements unchanged','All stochastic/event/audio/timing outputs U;no finite eventual-success or probability law','Shared integration and browser regeneration owned by root']}
(P/'validation-author-r1.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
