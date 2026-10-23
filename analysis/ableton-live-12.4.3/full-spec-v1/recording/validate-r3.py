"""Read-only Recording RC-020 successor verification; no vendor/inventory execution."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from copy import deepcopy
from collections import Counter
import ast,json,re,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode and sys.argv[1:] in (['--preflight'],['--check'])
preflight=sys.argv[1:]==['--preflight'];assert not preflight or not (P/'manifest-author-r3.json').exists()
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in n for n in before)
delta=load(P/'delta-r3.json');assert len(delta['old_packet_files'])==12
for n,r in delta['old_packet_files'].items():pin(P/n,r)
pin(P/'manifest.json',delta['prior_manifest']);assert delta['prior_manifest']['sha256']=='0b1dd1222cfded8bdddad25a367eb7822c743a6bd783f8f183458cb9a97656c1'
prior=load(P/'manifest.json');assert len(prior['files'])==11
for n,r in prior['files'].items():pin(P/n,r)
for path,n in [('wiki/specs/recording-comping.md','spec-before-r3.md'),('wiki/research/recording-comping.md','research-before-r3.md')]:assert info(P/n)['sha256']==prior['canonical_documents'][path]
inputs=load(P/'inputs-r3.json');assert len(inputs)==len({r['path'] for r in inputs}) and not any(r['path'].startswith('wiki/') for r in inputs)
external_before={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
assert info(B/'reviews/settings-owner-reconciliation-review.json')['sha256']=='7cb939ffccb397dba402a4ffa74f2b907704793cf5c8748e61ad37cdbe835172'
oldspec=(P/'spec-before-r3.md').read_text();trans=load(P/'case-transcription-before-r3.json');assert trans['canonical_snapshot']=='spec-before-r3.md'
fields=['id','requirement_suffix','kind','action','documentary_comparator_or_unknown','evidence']
rows=[];offset=0
for line_number,line in enumerate(oldspec.splitlines(True),1):
 if line.startswith('| RC-'):
  cells=[x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))];assert len(cells)==6
  rows.append(dict(fields=dict(zip(fields,cells)),raw_row=line.rstrip('\n'),spec_line=line_number,spec_character_span=[offset,offset+len(line.rstrip('\n'))]))
 offset+=len(line)
assert len(rows)==81 and rows==trans['rows']
assert len({r['fields']['id'] for r in rows})==81
for r in rows:
 a,b=r['spec_character_span'];assert oldspec[a:b]==r['raw_row']
# SOR's separately frozen transcription confirms prior row identities, not live canonical authority.
sor=load(B/'settings-owner-reconciliation/owners/recording/cases.json');assert len(sor)==81
for a,b in zip(rows,sor):assert a['raw_row']==b['raw_row'] and a['fields']['action']==b['action'] and a['spec_character_span']==b['spec_character_span']
assert (B/'settings-owner-reconciliation/owners/recording/spec.md').read_text()==oldspec
catalog=load(P/'cases-r3.json');cases=catalog['records'];assert catalog['historical_transcription']=='case-transcription-before-r3.json'
def check_cases(records):
 assert len(records)==81
 changes=[]
 for i,(a,b) in enumerate(zip(rows,records)):
  assert set(b)==set(fields)|{'expected','comparison','target_grade','executed'}
  assert b['expected'] is b['comparison'] is None and b['target_grade']=='U' and b['executed'] is False
  for k,v in a['fields'].items():
   if v!=b[k]:changes.append(dict(pointer=f'/records/{i}/{k}',id=a['fields']['id'],old=v,new=b[k]))
 assert changes==delta['case_field_changes'] and len(changes)==1 and changes[0]['pointer']=='/records/19/action' and changes[0]['id']=='RC-020'
 assert records[20]['action']=='Enable Start Recording on Scene Launch; repeat'
 action=records[19]['action']
 assert all(x in action for x in ['genuinely productive recording baseline of RC-021','fresh empty slots','explicitly set Start Recording on Scene Launch Off','record its actual value','eligible','active','U, never a passing no-recording observation'])
check_cases(cases)
rejected=0
for mode in ['changed-comparator','target-pass','default-not-explicit-Off']:
 x=deepcopy(cases)
 if mode=='changed-comparator':x[19]['documentary_comparator_or_unknown']='new behavior'
 elif mode=='target-pass':x[19]['expected']='passed recording absence'
 else:x[19]['action']=rows[19]['fields']['action']
 try:check_cases(x)
 except AssertionError:rejected+=1
 else:raise AssertionError(mode)
assert rejected==3
strength=lambda c:'D12403' if c['evidence'].startswith('D12403') else 'D12' if c['evidence'].startswith('D12') else 'U'
assert Counter(strength(c) for c in cases)=={'D12':65,'D12403':4,'U':12}
assert sum(c['kind']=='F' for c in cases)==4
sp=ROOT/'wiki/specs/recording-comping.md';rp=ROOT/'wiki/research/recording-comping.md';canon_before={str(q):info(q) for q in [sp,rp]}
for r in delta['canonical_changes']:
 text=(P/r['old_snapshot']).read_text()
 for x in r['replacements']:assert text.count(x['old'])==1;text=text.replace(x['old'],x['new'],1)
 text+=r['appended'];assert text==(P/r['new_snapshot']).read_text()==(ROOT/r['canonical']).read_text() and 'revision: 3\n' in text
spec=sp.read_text();section=lambda t:t.split('## Requirements\n',1)[1].split('## Timing and state\n',1)[0]
assert section(spec)==section(oldspec)
reqids=set(re.findall(r'^### (REQ-RECORDING-COMPING-\d+) —',spec,re.M));assert len(reqids)==32
assert {f'REQ-RECORDING-COMPING-{n}' for c in cases for n in c['requirement_suffix'].split(',')}==reqids
tool=ROOT/'tools/spec_browser.py';tree=ast.parse(tool.read_text());names={'anchor','frontmatter','cells','spec_rows'}
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(funcs)==4
ns={'re':re};exec(compile(ast.Module(body=funcs,type_ignores=[]),str(tool),'exec'),ns)
browser=ns['spec_rows'](sp,spec);assert len(browser)==32 and {r['id'] for r in browser}==reqids
current=[ns['cells'](line) for line in spec.splitlines() if line.startswith('| RC-')];assert len(current)==81
for a,c in zip(current,cases):assert a==[c[k] for k in fields]
sources=load(P/'sources.json');assert len(sources)==4
for r in sources:pin(P/r['file'],r)
ctx=load(P/'source-context-r3.json');assert ctx['source']==sources[0] and ctx['anchor']=='recording-into-session-slots'
html=(P/ctx['source']['file']).read_text();m=re.search(r'<h[1-6][^>]*id="recording-into-session-slots"[^>]*>',html);end=re.search(r'<h[1-6] ',html[m.end():]).start()+m.end();base=html[:m.start()].count('\n')
class Blocks(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tag=None;self.parts=[];self.rows=[]
 def handle_starttag(self,t,a):
  if t in ['p','li']:self.tag=t;self.parts=[];self.pos=self.getpos()
 def handle_data(self,d):
  if self.tag:self.parts.append(d)
 def handle_endtag(self,t):
  if t==self.tag:self.rows.append(dict(tag=t,html_line=base+self.pos[0],text=' '.join(''.join(self.parts).split())));self.tag=None
parser=Blocks();parser.feed(html[m.start():end]);assert len(parser.rows)==8 and parser.rows==ctx['blocks']
assert Counter(r['tag'] for r in parser.rows)=={'p':3,'li':5}
assert 'by default' in parser.rows[-1]['text'] and 'empty record-enabled slots belonging to that scene' in parser.rows[-1]['text'] and 'Start Recording on Scene Launch' in parser.rows[-1]['text']
impact=load(P/'impact-r3.json');assert len(impact['records'])==18
def resolve(x,p):
 for k in p.lstrip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
for r in impact['records']:
 pin(ROOT/r['consumer'],r['consumer_pin']);x=resolve(load(ROOT/r['consumer']),r['pointer'])
 assert (x==r['sha256'] if isinstance(x,str) else x['path']==r['target'] and x['sha256']==r['sha256'])
 assert r['matches_before']==(r['sha256']==impact['original_canonical_hashes'][r['target']])
 if r['matches_before']:assert info(P/r['historical_snapshot'])['sha256']==r['sha256']
 else:assert r['historical_snapshot'] is None
links=0
for q in [sp,rp,P/'README-r3.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  name,_,frag=target.partition('#');dest=(q.parent/name).resolve() if name else q
  if preflight and dest==P/'manifest-author-r3.json':continue
  assert dest.is_file(),(q,target)
  if frag and dest.suffix=='.md':assert frag in {ns['anchor'](h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(q,target)
  elif frag and dest.suffix=='.html':assert 'id="'+frag+'"' in dest.read_text(),(q,target)
  links+=1
if not preflight:
 manifest=load(P/'manifest-author-r3.json');assert set(manifest['files'])==set(before)-{'manifest-author-r3.json'}
 for n,r in manifest['files'].items():pin(P/n,r)
 for r in manifest['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
for q in [sp,rp]+[P/n for n in before if n not in delta['old_packet_files'] and Path(n).suffix in ['.md','.json','.py','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
 assert r.returncode in (0,1) and not r.stdout and not r.stderr,q
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external_before=={r['path']:info(ROOT/r['path']) for r in inputs} and canon_before=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',prior_packet_files_preserved=12,prior_manifest_payloads=11,requirements=32,requirements_verbatim=True,cases=81,changed_actions=1,other80actions_and_all_documentary_comparators_unchanged=True,case_provenance={'D12':65,'D12403_artifact_only':4,'U':12},all_current_actual_outcomes_null_U_unexecuted=True,original_JSON_case_catalog=False,source_blocks=8,input_pins=len(inputs),historical_pin_identity_records=18,browser_exact_IDs=32,local_links=links,rejection_fixtures=3,full_crosspacket_replay=False,writes=False),indent=2))
