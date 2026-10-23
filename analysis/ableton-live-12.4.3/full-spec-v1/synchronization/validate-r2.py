"""Read-only bounded owner R2 integrity checker, never original/runtime execution.
Historical Sync canonical pins resolve only through four explicit R1 records.
"""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import copy,json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P/'archive-r1'
load=lambda q:json.loads(q.read_text())
def sha(q):return sha256(q.read_bytes()).hexdigest()
def pin(q,p):assert q.is_file() and q.stat().st_size==p['bytes'] and sha(q)==p['sha256'],str(q)
def pointer(v,p):
 for k in p.strip('/').split('/'):
  k=k.replace('~1','/').replace('~0','~');v=v[int(k)] if isinstance(v,list) else v[k]
 return v

def check():
 before={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()};assert not any('__pycache__' in x for x in before),'Use python3 -B'
 r1=load(A/'manifest-author-r1.json');assert sha(A/'manifest-author-r1.json')=='e94dddb2bd443a5a20ffbacc03bc9b0ab48cde0c97cc085c2175481e13ea26d4'
 assert len(r1['files'])==13 and set(q.name for q in A.iterdir())==set(r1['files'])|{'manifest-author-r1.json'}
 for name,p in r1['files'].items():pin(A/name,p);pin(P/name,p);assert (A/name).read_bytes()==(P/name).read_bytes()
 assert (A/'manifest-author-r1.json').read_bytes()==(P/'manifest-author-r1.json').read_bytes()
 archivepins=load(P/'archive-r1-pins.json');assert len(archivepins)==14
 for p in archivepins:pin(ROOT/p['path'],p)
 inputs=load(P/'inputs-r2.json');assert len(inputs)==len({p['path'] for p in inputs})==73
 for p in inputs:pin(ROOT/p['path'],p)
 input_before={p['path']:sha(ROOT/p['path']) for p in inputs}
 adoption=load(P/'audit-adoption-r2.json');pin(ROOT/adoption['audit_manifest']['path'],adoption['audit_manifest']);pin(ROOT/adoption['review']['path'],adoption['review'])
 review=load(ROOT/adoption['review']['path']);assert review['disposition']=='approved-focused-partial-source-audit-successor' and review['required_findings']==[]
 assert review['reviewed_manifest_sha256']==adoption['audit_manifest']['sha256']=='3f7d1f6380758735139932d303da2d7f81ea339932f90e067720970305e8a1c5'
 assert [g['id'] for g in adoption['groups']]==[f'SA-G{i:02}' for i in range(1,10)]
 # Guarded analyst builder only; no old writer/validator or original code is run.
 author=runpy.run_path(str(P/'author-r2.py'));reqs,cases,fixture,counts=author['build']()
 for file,value in [('requirements-r2.json',reqs),('cases-r2.json',cases),('fixtures-r2.json',fixture),('counts-r2.json',counts)]:assert load(P/file)==value,file
 assert counts==adoption['counts'] and len(reqs)==27 and len(cases)==37
 assert Counter(r['strength'] for r in reqs)=={'D12':25,'U':2}
 oldreqs=load(A/'requirements.json');oldcases=load(A/'cases.json')
 assert reqs[:26]==[dict(r,contract=reqs[i]['contract']) if i in {4,11,14} else r for i,r in enumerate(oldreqs)]
 assert reqs[-1]['id']=='REQ-SYNC-WORKFLOW-025' and cases[-1]['id']=='SYNC-025'
 assert [r['id'] for r in reqs[:26]]==[r['id'] for r in oldreqs] and [c['id'] for c in cases[:36]]==[c['id'] for c in oldcases]
 # Complete exact finite patch set reconstructs versioned data from archived R1.
 delta=load(P/'delta-r2.json')['field_deltas'];assert len(delta)==68
 data={n:copy.deepcopy(load(A/n)) for n in ['requirements.json','cases.json','fixtures.json']}
 targets={'requirements.json':'requirements-r2.json','cases.json':'cases-r2.json','fixtures.json':'fixtures-r2.json'}
 for x in delta:
  assert x['old_file'] in targets and x['new_file']==targets[x['old_file']]
  keys=x['pointer'].strip('/').split('/');v=data[x['old_file']]
  for k in keys[:-1]:v=v[int(k)] if isinstance(v,list) else v[k]
  key=int(keys[-1]) if isinstance(v,list) else keys[-1]
  if x['operation']=='add':
   assert x['old'] is None
   if isinstance(v,list):assert key==len(v);v.append(copy.deepcopy(x['new']))
   else:assert key not in v;v[key]=copy.deepcopy(x['new'])
  else:assert x['operation']=='replace' and v[key]==x['old'];v[key]=copy.deepcopy(x['new'])
 for old,new in targets.items():assert data[old]==load(P/new),new
 assert {x['pointer'] for x in delta if x['old_file']=='requirements.json'}=={'/4/contract','/11/contract','/14/contract','/26'}
 refined={1,4,11,14,15}
 for i,c in enumerate(cases[:36]):
  allowed={'fixture'}
  if i in refined:allowed|={'setup_and_action','finite_contexts','refines_R1_case'}
  if i in {4,11,14}:allowed|={'source_claim','documentary_expected'}
  if i==11:allowed|={'kind','documentary_comparator','positive_processing_guard'}
  assert {k for k in set(c)|set(oldcases[i]) if c.get(k)!=oldcases[i].get(k)}<=allowed,c['id']
 source=load(P/'source.json');pin(P/source['file'],source)
 assert source['sha256']=='55dcef3b8171e721c641ab69476a075db8c3c8893055914538f9e4eb801d00ac' and source['bytes']==261580
 dep=load(P/'dependencies.json')[0];pin(ROOT/dep['path'],dep)
 parser=runpy.run_path(str(ROOT/dep['path']))['Chapter']();parser.feed((P/source['file']).read_text())
 for i,b in enumerate(parser.rows,1):b['id']=f'SYNC-B{i:03}'
 blocks=load(P/'source-blocks.json');assert parser.rows==blocks and len(blocks)==54
 blockmap={b['id']:b for b in blocks};rmap={r['id']:r for r in reqs};cmap={c['id']:c for c in cases}
 assert len(rmap)==27 and len(cmap)==37 and all(r['target_applicability']=='U' for r in reqs)
 for r in reqs:
  for e in r['evidence']:assert e['anchor']==blockmap[e['block']]['anchor'] and e['html_line']==blockmap[e['block']]['html_line']
 for c in cases:
  assert c['fixture']=='fixtures-r2.json#SYNC-OWNED' and c['setup_and_action']
  assert c['expected'] is None and c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
  assert c['requirements']==[c['requirements'][0]] and c['requirements'][0] in rmap
  if c['source_claim'] is not None:assert c['source_claim']==rmap[c['requirements'][0]]['contract']
  assert c['evidence']==rmap[c['requirements'][0]]['evidence']
  if c['kind']!='control' or c['id'].startswith('SYNC-U-'):assert c['documentary_expected'] is None and c['documentary_comparator'] is None
 assert sum(c['documentary_expected'] is not None for c in cases)==8 and sum(c['documentary_expected'] is None for c in cases)==29
 assert cmap['SYNC-012']['kind']=='signal' and 'genuine' in cmap['SYNC-012']['positive_processing_guard'] and cmap['SYNC-012']['documentary_expected'] is None
 assert len(cmap['SYNC-025']['finite_contexts'])==3 and 'A/B' in cmap['SYNC-025']['setup_and_action']
 redirects=load(P/'historical-pin-redirects-r2.json');assert len(redirects)==4
 expected_redirects={('analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r4-citation-crosswalk/inputs.json','/pins/66'),('analysis/ableton-live-12.4.3/full-spec-v1/inventory-revisions/r4-citation-crosswalk/inputs.json','/pins/70'),('analysis/ableton-live-12.4.3/full-spec-v1/synchronization-source-audit/inputs.json','/pins/27'),('analysis/ableton-live-12.4.3/full-spec-v1/synchronization-source-audit/inputs.json','/pins/34')}
 assert {(r['consumer'],r['record_pointer']) for r in redirects}==expected_redirects
 for r in redirects:
  original=pointer(load(ROOT/r['consumer']),r['record_pointer']);assert original['path']==r['original_path'] and original['bytes']==r['original_bytes'] and original['sha256']==r['original_sha256']
  assert r['original_path'] in {'wiki/specs/synchronization-workflows.md','wiki/research/synchronization-workflows.md'}
  q=ROOT/r['historical_snapshot']['path'];pin(q,r['historical_snapshot']);assert q.parent==A and q.name in {'spec-r1.md','research-r1.md'}
  assert r['historical_snapshot']['bytes']==original['bytes'] and r['historical_snapshot']['sha256']==original['sha256']
 sp=ROOT/'wiki/specs/synchronization-workflows.md';rp=ROOT/'wiki/research/synchronization-workflows.md'
 assert sp.read_bytes()==(P/'spec-r2.md').read_bytes() and rp.read_bytes()==(P/'research-r2.md').read_bytes()
 sys.path.insert(0,str(ROOT/'tools'))
 from spec_browser import spec_rows,frontmatter
 rows=spec_rows(sp,sp.read_text());assert len(rows)==27 and {r['id'] for r in rows}==set(rmap)
 assert frontmatter(sp.read_text())['revision']==frontmatter(rp.read_text())['revision']=='2'
 links=0
 for q in [sp,rp,P/'README-r2.md']:
  for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',q.read_text()):
   if re.match(r'https?://',target):continue
   name,_,fragment=target.partition('#');dest=q.parent/name if name else q;assert dest.is_file(),target
   if fragment and dest==q:assert fragment=='analysis-only-evidence'
   links+=1
 manifest=load(P/'manifest-author-r2.json');assert manifest['counts']==counts and manifest['status']=='partial-owner-successor-awaiting-independent-semantic-review'
 assert set(before)==set(manifest['files'])|{'manifest-author-r2.json'}|({'validation-author-r2.json'}&set(before))|({'freeze-author-r2.json'}&set(before))
 for name,p in manifest['files'].items():pin(P/name,p)
 if (P/'freeze-author-r2.json').exists():
  for name,p in load(P/'freeze-author-r2.json')['files'].items():pin(P/name,p)
 whitespace=0
 for q in [sp,rp]+[q for q in P.rglob('*') if q.is_file() and q.suffix in {'.py','.json','.md','.txt'}]:
  result=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(q)],capture_output=True)
  assert result.returncode in (0,1) and not result.stdout and not result.stderr,str(q);whitespace+=1
 assert before=={str(q.relative_to(P)):sha(q) for q in P.rglob('*') if q.is_file()},'packet mutation'
 assert input_before=={p['path']:sha(ROOT/p['path']) for p in inputs},'input mutation'
 return dict(status='pass',scope='ownerR2 archive/delta/pin/source/case/browser/snapshot integrity only; separate semantic review pending',requirements=27,strengths={'D12':25,'U':2},cases=37,documentary_visible=8,documentary_null=29,old_R1_payloads_and_manifest_preserved=14,archive_R1_files=14,exact_JSON_field_deltas=68,external_pins=73,source_blocks=54,historical_Sync_pin_redirects=4,browser_exact_ID_set=27,canonical_snapshots=2,local_links=links,payloads=len(manifest['files']),untracked_whitespace_files=whitespace,all_actual_target_outcomes_null_U_unexecuted=True,all_signal_timing_documentary_outcomes_null=True,writes=False,original_network_peer_hardware_candidate_execution=False)
if __name__=='__main__':
 assert not sys.argv[1:],'read-only validator accepts no arguments'
 print(json.dumps(check(),indent=2))
