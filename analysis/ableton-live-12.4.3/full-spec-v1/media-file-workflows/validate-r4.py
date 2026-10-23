"""Read-only finite Media R4 two-action successor check; never operates media."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
from html import unescape
from copy import deepcopy
from collections import Counter
import ast, json, re, subprocess, sys

P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.dont_write_bytecode and sys.argv[1:] in (['--check'],['--preflight'])
preflight=sys.argv[1:]==['--preflight'];assert not preflight or not (P/'manifest-author-r4.json').exists()
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def pin(q,r):assert info(q)=={k:r[k] for k in ['bytes','sha256']},q
before={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert not any('__pycache__' in n for n in before)
delta=load(P/'delta-r4.json');assert len(delta['old_packet_files'])==32
for n,r in delta['old_packet_files'].items():pin(P/n,r)
pin(P/'manifest.json',delta['prior_manifest'])
assert delta['prior_manifest']['sha256']=='3f6a1d3c3265181023a55aaca5badd80ce45504320e285d1e87dacf2bf418843'
oldpages={'wiki/specs/media-file-workflows.md':'spec-before-r4.md','wiki/research/media-file-workflows.md':'research-before-r4.md'}
oldmanifest=load(P/'manifest.json');assert len(oldmanifest['payloads'])==33
for r in oldmanifest['payloads']:pin(P/oldpages[r['path']] if r['path'] in oldpages else ROOT/r['path'],r)
inputs=load(P/'inputs-r4.json');assert len(inputs)==len({r['path'] for r in inputs})
assert not any(r['path'].startswith('wiki/') for r in inputs)
external_before={r['path']:info(ROOT/r['path']) for r in inputs}
for r in inputs:pin(ROOT/r['path'],r)
assert info(B/'reviews/settings-owner-reconciliation-review.json')['sha256']=='7cb939ffccb397dba402a4ffa74f2b907704793cf5c8748e61ad37cdbe835172'
# Legacy schemas are preserved exactly: documentary predicate != actual result.
old=load(P/'cases.json');cases=load(P/'cases-r4.json');assert len(old)==len(cases)==32
def check_cases(rows):
 assert len(rows)==32 and [x['id'] for x in rows]==[x['id'] for x in old]
 diffs=[{'pointer':f'/{i}/{k}','id':a['id'],'old':a[k],'new':b[k]} for i,(a,b) in enumerate(zip(old,rows)) for k in a if a[k]!=b[k]]
 assert diffs==delta['case_field_changes']
 assert [x['pointer'] for x in diffs]==['/10/action','/14/action']
 assert [x['id'] for x in diffs]==['MF-011','MF-015']
 for a,b in zip(old,rows):
  assert set(a)==set(b) and b['exact_target']=='U' and b['execution']=='not-run'
  assert not any(k in b for k in ['actual','expected','comparison','target_expected','result','passed'])
 assert Counter(x['basis'] for x in rows)=={'D12':21,'U':11}
 for c in [rows[10],rows[14]]:
  assert all(t in c['action'] for t in ['fresh','owned','writable','no ASD' if c['id']=='MF-015' else 'no-ASD','completed','baseline','U'])
 assert 'Explicitly select On' in rows[10]['action'] and 'Explicitly select Create Analysis Files Off' in rows[14]['action']
 assert 'MF-015' in rows[10]['action'] and 'MF-011' in rows[14]['action']
check_cases(cases)
rejected=0
for mode in ['changed-old-predicate','invented-target-pass','lost-positive-action']:
 x=deepcopy(cases)
 if mode=='changed-old-predicate':x[10]['predicate']='new sidecar law'
 elif mode=='invented-target-pass':x[10]['exact_target']='pass'
 else:x[10]['action']=old[10]['action']
 try:check_cases(x)
 except AssertionError:rejected+=1
 else:raise AssertionError(mode)
assert rejected==3
sp=ROOT/'wiki/specs/media-file-workflows.md';rp=ROOT/'wiki/research/media-file-workflows.md'
canon_before={str(q):info(q) for q in [sp,rp]}
for r in delta['canonical_changes']:
 text=(P/r['old_snapshot']).read_text()
 for change in r['replacements']:
  assert text.count(change['old'])==1;text=text.replace(change['old'],change['new'],1)
 text+=r['appended']
 assert text==(P/r['new_snapshot']).read_text()==(ROOT/r['canonical']).read_text()
 assert 'revision: 4\n' in text
oldspec=(P/'spec-before-r4.md').read_text();spec=sp.read_text()
section=lambda t:t.split('## Requirements\n',1)[1].split('## Acceptance cases\n',1)[0]
assert section(oldspec)==section(spec)
reqids=set(re.findall(r'^### (REQ-MEDIA-FILE-\d+) —',spec,re.M));assert len(reqids)==17
assert {c['requirement'] for c in cases}==reqids
# Execute only four inspected analyst Markdown parser functions, avoiding browser build/import side effects.
tool=ROOT/'tools/spec_browser.py';tree=ast.parse(tool.read_text());names={'anchor','frontmatter','cells','spec_rows'}
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(funcs)==4
ns={'re':re};exec(compile(ast.Module(body=funcs,type_ignores=[]),str(tool),'exec'),ns)
browser=ns['spec_rows'](sp,spec);assert len(browser)==17 and {x['id'] for x in browser}==reqids
table={}
for line in spec.splitlines():
 if line.startswith('| MF-'):
  cells=ns['cells'](line);table[cells[0]]=cells
assert len(table)==32
for c in cases:
 cells=table[c['id']];assert cells[3]==c['action'];assert cells[4]==(c['predicate'] if c['predicate'] is not None else c['unknown'])
# Reconstruct only the focused ASD paragraphs and SET-B058 from immutable retained bytes.
ctx=load(P/'source-context-r4.json');html=(ROOT/ctx['ASD']['path']).read_text()
start=html.index('<h3 data-number="5.1.2" id="analysis-files-asd">');end=html.index('<h3 ',start+1)
class Paragraphs(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.active=False;self.text=[];self.rows=[]
 def handle_starttag(self,tag,attrs):
  if tag=='p':self.active=True;self.text=[];self.pos=self.getpos()
 def handle_data(self,data):
  if self.active:self.text.append(data)
 def handle_endtag(self,tag):
  if tag=='p' and self.active:self.rows.append({'html_line':html[:start].count('\n')+self.pos[0],'text':' '.join(''.join(self.text).split())});self.active=False
parser=Paragraphs();parser.feed(html[start:end]);assert parser.rows==ctx['ASD']['paragraphs'] and len(parser.rows)==9
assert ctx['ASD']['metadata']==load(B/'project-media/source.json');pin(ROOT/ctx['ASD']['path'],ctx['ASD']['metadata'])
assert ctx['Settings']['metadata']==load(B/'settings-learning/source.json');pin(ROOT/ctx['Settings']['path'],ctx['Settings']['metadata'])
assert ctx['Settings']['block']==next(x for x in load(B/'settings-learning/source-blocks.json') if x['id']=='SET-B058')
assert ctx['Settings']['block']['text']=='The Create Analysis Files setting determines whether or not Live creates Analysis Files upon importing audio data.'
settings_html=(ROOT/ctx['Settings']['path']).read_text();i=settings_html.index('The Create Analysis Files setting determines whether')
a=settings_html.rfind('<p>',0,i);b=settings_html.index('</p>',i)+4
assert ' '.join(unescape(re.sub('<[^>]*>','',settings_html[a:b])).split())==ctx['Settings']['block']['text']
assert settings_html[:a].count('\n')+1==ctx['Settings']['block']['html_line']
sources=load(P/'sources.json');assert len(sources)==1 and len(sources[0]['anchors'])==6;pin(ROOT/sources[0]['path'],sources[0])
for anchor,line in sources[0]['anchors'].items():
 assert html[:html.index('id="'+anchor+'"')].count('\n')+1==line
impact=load(P/'impact-r4.json')
def resolve(x,pointer):
 for k in pointer.lstrip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x
for r in impact['records']:
 pin(ROOT/r['consumer'],r['consumer_pin']);x=resolve(load(ROOT/r['consumer']),r['pointer'])
 assert (x==r['sha256'] if isinstance(x,str) else x['path']==r['target'] and x['sha256']==r['sha256'])
 assert r['matches_before']==(r['sha256']==impact['original_canonical_hashes'][r['target']])
 if r['matches_before']:assert info(P/r['historical_snapshot'])['sha256']==r['sha256']
 else:assert r['historical_snapshot'] is None
assert len(impact['records'])==22
assert 'Recording RC-020 default-versus-explicit-Off remains a separate Q051 gap.' in rp.read_text()
links=0
for q in [sp,rp,P/'README-r4.md']:
 for target in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',q.read_text()):
  if re.match('[A-Za-z]+:',target):continue
  name,_,frag=target.partition('#');dest=(q.parent/name).resolve() if name else q
  if preflight and dest==P/'manifest-author-r4.json':continue
  assert dest.is_file(),(q,target)
  if frag and dest.suffix=='.md':assert frag in {ns['anchor'](h) for h in re.findall(r'^#+\s+(.+)$',dest.read_text(),re.M)},(q,target)
  elif frag and dest.suffix=='.html':assert 'id="'+frag+'"' in dest.read_text(),(q,target)
  links+=1
if not preflight:
 m=load(P/'manifest-author-r4.json');assert set(m['files'])==set(before)-{'manifest-author-r4.json'}
 for n,r in m['files'].items():pin(P/n,r)
 for r in m['canonical_snapshots']:pin(ROOT/r['canonical'],r);pin(P/r['snapshot'],r)
for q in [sp,rp]+[P/n for n in before if n not in delta['old_packet_files'] and Path(n).suffix in ['.md','.json','.py','.txt']]:
 if q.suffix=='.json':load(q)
 r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
 assert r.returncode in (0,1) and not r.stdout and not r.stderr,q
assert before=={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file()}
assert external_before=={r['path']:info(ROOT/r['path']) for r in inputs} and canon_before=={str(q):info(q) for q in [sp,rp]}
print(json.dumps(dict(status='passed-read-only-preflight' if preflight else 'passed-read-only-frozen',old_packet_files_preserved=32,old_manifest_payloads=33,requirements=17,requirements_verbatim=True,cases=32,case_field_deltas=2,case_IDs_predicates_oracles_unchanged=True,documentary_basis={'D12':21,'U':11},all_target_U_not_run=True,actual_fields='absent unchanged legacy schema; no pass invented',focused_ASD_paragraphs=9,FirstSteps_blocks=1,input_pins=len(inputs),historical_consumer_identity_records=22,browser_exact_IDs=17,local_links=links,rejection_fixtures=3,recording_correction=False,full_crosspacket_replay=False,writes=False),indent=2))
