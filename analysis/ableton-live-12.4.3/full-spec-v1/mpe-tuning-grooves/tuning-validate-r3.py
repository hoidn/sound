"""Read-only bounded Tuning owner/source/preservation checks; no old checker imports."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,importlib.util,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'tuning-source-audit'
def load(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 if not s:return v
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def safety(cases,plan,status,fixture):
 old=[c for c in load(P/'cases.json') if c['id'].startswith('TUN-')];assert cases[:32]==old,'old32 records exact'
 assert len(cases)==43 and [c['id'] for c in cases]==[f'TUN-{i:03}' for i in range(1,44)]
 assert Counter(c['documentary_grade'] for c in cases)=={'D12':32,'U':11}
 assert len(status['cases'])==43
 for c,s in zip(cases,status['cases']):assert s==dict(id=c['id'],actual_expected=None,actual_comparison=None,target='U',executed=False)
 assert len(plan['groups'])==12 and plan['groups'][9]['new_case'] is None and plan['groups'][9]['retained_cases']==['TUN-015']
 assert 'DTU028' in plan['groups'][9]['boundary'] and 'not TUN015' in plan['groups'][9]['boundary']
 guard=fixture['guard'];assert all(guard.values())
 audit=load(A/'audit.json');new=cases[32:];assert len(new)==11
 assert [c['adoption_group'] for c in new]==[f'TSA-G{i:02}' for i in list(range(1,10))+[11,12]]
 for c in new:
  assert c['target_build_grade']=='U' and c['execution']=='unexecuted'
  assert c['expected'] is c['comparator'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['positive_guard']==guard and c['setup']==fixture['common'] and c['fixture']=='tuning-fixtures-r3.json#TUNING-OWNED-R3'
  g=next(g for g in plan['groups'] if g['new_case']==c['id']);assert c['action']==g['action'] and c['requirement']==g['requirements'][0]
  refs=c['source_contexts'];claims=[]
  for ref in refs:
   v=pointer(load(ROOT/ref['catalog']),ref['json_pointer']);assert v['id']==ref.get('block',ref.get('supplement'));claims.append(v.get('text',v.get('quote')))
  assert c['source_claim']==' '.join(claims).strip()
  assert c['documentary_expected']==g['documentary_expected'] and c['documentary_comparator']==g['documentary_comparator']
  if c['id'] not in ['TUN-034','TUN-036','TUN-041']:assert c['documentary_expected'] is c['documentary_comparator'] is None
 assert sum(c['documentary_comparator'] is not None for c in new)==3
 assert 'matched Retune-On load' in new[3]['action'] and 'documented confirmation' in new[3]['action'] and 'Only then reset' in new[3]['action']
 assert 'productive direct-frequency pitch change' in new[5]['action'] and 'before separately changing Octave and Note' in new[5]['action']
 assert 'actually available enabled link-arrow control' in new[6]['action'] and 'successful ordinary tuning Save' in new[6]['action']
 assert 'genuinely effective accepted tuning' in new[7]['action'] and 'before Bypass' in new[7]['action']
 assert 'recognized valid UTF-8 ASCL' in new[9]['action'] and 'productive ordinary import' in new[9]['action']
 assert 'not SCL fallback440 near middle' in new[10]['action'] and 'not sorted frequency extrema' in new[5]['action']
 assert 'All Keys and Closest in Pitch to Keyboard' in new[8]['action']
 return True
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check']
 prior=load(P/'tuning-prior-files-r3.json');assert len(prior)==97
 pins=load(P/'tuning-inputs-r3.json');assert len(pins)==11
 inherited=load(A/'inputs.json');assert len(inherited['files'] if isinstance(inherited,dict) else inherited)==85
 inherited=inherited['files'] if isinstance(inherited,dict) else inherited
 history=load(P/'tuning-consumer-impact-r3.json')
 watch={p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in pins+inherited}|{ROOT/n for n in history['consumer_identities']}|{ROOT/'wiki/specs/tuning-systems.md',ROOT/'wiki/research/mpe-tuning-grooves.md'}
 before={str(p):dg(p) for p in watch}
 for n,r in prior.items():assert dg(P/n)==r,n
 for r in pins+inherited:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
 assert dg(A/'manifest.json')['sha256']=='61bc7f4c72097e4c9d1da9b4ba4f04cc0b2d775deb93b76ac76275a802b3d916'
 assert dg(P.parent/'reviews/tuning-source-audit-review.json')['sha256']=='6b1b0a47ac1655c3dfcb02f0e7af29c2d5982477c8c81ddc946911bbe14803d2'
 for n,r in load(A/'manifest.json')['files'].items():assert dg(A/n)==r
 for n,r in history['consumer_identities'].items():assert dg(ROOT/n)==r
 assert len(history['records'])==33 and len(history['consumer_identities'])==19 and not history['consumer_mutations'] and not history['historical_replay']
 for r in history['records']:assert pointer(load(ROOT/r['consumer']),r['json_pointer'])==dg(P/r['historical_snapshot'])['sha256']==r['literal_sha256']
 author=module(P/'tuning-author-r3.py','tuning_r3_owned_author');plan=load(P/'tuning-adoption-r3.json');cases=load(P/'tuning-cases-r3.json');status=load(P/'tuning-actual-status-r3.json');fixture=load(P/'tuning-fixtures-r3.json');assert safety(cases,plan,status,fixture)
 for n,t in author.build().items():assert (P/n).read_text()==t,n
 for n,canon in [('tuning-systems-author-r3.md','wiki/specs/tuning-systems.md'),('tuning-research-author-r3.md','wiki/research/mpe-tuning-grooves.md')]:assert (P/n).read_bytes()==(ROOT/canon).read_bytes()
 oldrows=author.rows((P/'tuning-spec-before-r3.md').read_text());rows=author.rows((P/'tuning-systems-author-r3.md').read_text());assert len(rows)==21 and set(rows)==set(oldrows)
 changed=[dict(id=k,column=i,before=oldrows[k][i],after=rows[k][i]) for k in rows for i in range(4) if oldrows[k][i]!=rows[k][i]];assert changed==load(P/'tuning-delta-r3.json')['changed_fields'] and len(changed)==5
 assert set(d['id'] for d in changed)=={'REQ-TUNING-001','REQ-TUNING-002','REQ-TUNING-005','REQ-TUNING-012','REQ-TUNING-013'}
 oldresearch=(P/'tuning-research-before-r3.md').read_text().replace('revision: 4\n','revision: 5\n',1);assert (P/'tuning-research-author-r3.md').read_text().startswith(oldresearch)
 parser=module(P.parent/'clip-view-source-audit/source_parser.py','tuning_retained_parser');audit=load(A/'audit.json');raw=(P/'manual-12-using-tuning-systems-2026-10-19.html').read_text();blocks,resources=parser.extract(raw,'TUN');assert blocks==audit['blocks'] and len(blocks)==49 and len(resources)==32
 for parsed,retained in zip(resources,audit['resources']):assert parsed=={k:v for k,v in retained.items() if k not in {'pixels_or_destination_inspected','target','complete','role'}}
 assert len(audit['assessments'])==68 and len(audit['supplemental_contexts'])==19
 for a in audit['assessments']:
  b=pointer(audit,a['block_json_pointer']);lo,hi=a['text_span'];assert b['id']==a['block'] and b['text'][lo:hi]==a['quote'] and sha256(a['quote'].encode()).hexdigest()==a['quote_sha256']
 for s in audit['supplemental_contexts']:
  lo,hi=s['text_span'];assert (ROOT/s['source_path']).read_text()[lo:hi]==s['quote'];assert dg(ROOT/s['source_path'])['sha256']==s['source_sha256'];assert s['capture_utc'] is None
 assert audit['source']['capture_utc'] is None
 # Only these four previously inspected own Browser functions; no module imports/writer.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4 and all(not n.decorator_list for n in defs);env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned Browser read functions>','exec'),env)
 ids={r['id'] for r in env['spec_rows'](ROOT/'wiki/specs/tuning-systems.md',(P/'tuning-systems-author-r3.md').read_text())};assert ids==set(rows)
 negatives=[]
 for name in ['old-case-erased','actual-oracle','flag-only-sound','no-On-positive','no-frequency-positive','no-Save-positive','no-enabled-link-positive','no-tuned-bypass-positive','no-valid-UTF8-positive','new-numeric-oracle','Tuner-borrowed','wrong-source','SCL-ASCL-conflated','sorted-extrema']:
  c,g,s,f=deepcopy(cases),deepcopy(plan),deepcopy(status),deepcopy(fixture)
  if name=='old-case-erased':c[14]['action']='changed'
  elif name=='actual-oracle':s['cases'][0]['actual_expected']='observed'
  elif name=='flag-only-sound':f['guard']['actual_effective_tuning_and_nonzero_route_before_audio_or_bypass']=False
  elif name=='no-On-positive':c[35]['action']=g['groups'][3]['action']=c[35]['action'].replace('matched Retune-On load','flag')
  elif name=='no-frequency-positive':c[37]['action']=g['groups'][5]['action']=c[37]['action'].replace('productive direct-frequency pitch change','flag')
  elif name=='no-Save-positive':c[38]['action']=g['groups'][6]['action']=c[38]['action'].replace('successful ordinary tuning Save','flag')
  elif name=='no-enabled-link-positive':c[38]['action']=g['groups'][6]['action']=c[38]['action'].replace('actually available enabled link-arrow control','LINK text')
  elif name=='no-tuned-bypass-positive':c[39]['action']=g['groups'][7]['action']=c[39]['action'].replace('genuinely effective accepted tuning','loaded flag')
  elif name=='no-valid-UTF8-positive':c[41]['action']=g['groups'][10]['action']=c[41]['action'].replace('recognized valid UTF-8 ASCL','grammar text')
  elif name=='new-numeric-oracle':c[37]['documentary_expected']=g['groups'][5]['documentary_expected']='exact frequency';c[37]['documentary_comparator']=g['groups'][5]['documentary_comparator']='numeric'
  elif name=='Tuner-borrowed':g['groups'][9]['new_case']='TUN-044'
  elif name=='wrong-source':c[33]['source_contexts'][0]['json_pointer']='/blocks/0'
  elif name=='SCL-ASCL-conflated':c[42]['action']=g['groups'][11]['action']=c[42]['action'].replace('not SCL fallback440 near middle','SCL identical')
  elif name=='sorted-extrema':c[37]['action']=g['groups'][5]['action']=c[37]['action'].replace('not sorted frequency extrema','sorted extrema')
  try:safety(c,g,s,f)
  except AssertionError:negatives.append(name)
  else:raise AssertionError('accepted unsafe fixture '+name)
 retained=['TUN-003','TUN-007','TUN-008','TUN-009','TUN-010','TUN-011','TUN-013','TUN-014','TUN-015','TUN-016','TUN-017','TUN-018','TUN-019','TUN-020','TUN-021'];assert all(cases[int(n[-3:])-1]==audit['owner_cases'][int(n[-3:])-1] for n in retained)
 links=0
 for n,base in [('tuning-README-r3.md',P),('tuning-systems-author-r3.md',ROOT/'wiki/specs'),('tuning-research-author-r3.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)]+)\)',(P/n).read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   target=base/dest.split('#')[0]
   if target.resolve()==(P/'tuning-manifest-author-r3.json').resolve() and not target.exists():continue # Sole own not-yet-sealed preflight link; postseal must exist.
   assert target.exists(),dest;links+=1
   if '#' in dest and target.suffix=='.md':assert dest.split('#',1)[1] in {env['anchor'](l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')},dest
 for p in [p for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in prior]+[ROOT/'wiki/specs/tuning-systems.md',ROOT/'wiki/research/mpe-tuning-grooves.md']:
  b=p.read_bytes();assert b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines()),str(p)
 sealed=(P/'tuning-manifest-author-r3.json').exists()
 if sealed:
  mf=load(P/'tuning-manifest-author-r3.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(mf['files'])|{'tuning-manifest-author-r3.json'}
  for n,r in mf['files'].items():assert dg(P/n)==r,n
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=sealed,requirements=21,refined_fields=5,cases=43,old32_exact=True,new_cases=11,documentary_D12=32,documentary_U=11,new_named_documentary_pairs=3,new_null_pairs=8,all_actual_null_U=True,executed=0,complete_topics=0,primary_blocks=49,source_facets=68,resources=32,selected_supplements=19,selected_external=35,partial_groups=12,prior_files_exact=97,owned_input_pins=11,audit_input_pins=85,BrowserIDs=len(ids),links=links,consumer_occurrences=33,consumer_files=19,negative_fixtures=negatives,retained_positive_contexts=retained,watch_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
