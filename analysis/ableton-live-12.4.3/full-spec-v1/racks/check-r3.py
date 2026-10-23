"""Focused read-only Racks zone-role correction; no old main/writer execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'racks-source-audit';load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def replace(v,s,b,a):
 keys=s.strip('/').split('/');par=v
 for k in keys[:-1]:par=par[int(k)] if isinstance(par,list) else par[k]
 k=int(keys[-1]) if isinstance(par,list) else keys[-1];assert par[k]==b;par[k]=a

def roles(plan,cat):
 clause=plan['clause_appends']['REQ-DEVICE-RACKS-007'];action=plan['groups'][4]['action']
 assert 'Main and fade sections resize from their respective left/right edges.' in clause
 assert 'Move the zone itself by dragging an admitted interior of its lower main section' in clause
 assert 'independent fade-section translation is not established here and remains U' in clause
 assert 'Then move the zone itself by dragging an admitted interior of its lower main section.' in action
 assert 'Independent fade-section translation remains an ungraded U context' in action
 assert cat['cases'][65]['setup_action'].endswith(action)

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only'
 prior=load(P/'prior-files-r3.json');extra=load(P/'inputs-r3.json');pins=load(P/'inputs-r2.json');inherited=load(A/'inputs.json')['files']
 assert len(prior)==36 and len(extra)==1 and len(pins)==11 and len(inherited)==21
 watch={p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in extra+pins+inherited}|{ROOT/'wiki/specs/device-racks.md',ROOT/'wiki/research/device-racks.md'};before={str(p):dg(p) for p in watch}
 for n,v in prior.items():assert dg(P/n)==v
 for r in extra+pins+inherited:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 oldmf=load(P/'manifest-author-r2.json');assert set(prior)==set(oldmf['files'])|{'manifest-author-r2.json'}
 assert dg(P/'manifest-author-r2.json')['sha256']=='26779f614d153c8d85ae993ab80c0997569534d154b62bd2fd13d52769d1f5f4'
 assert extra[0]['sha256']=='cf8971575f1c65c9e0deb4255135f1f4a7c41a147218aeb83ee78134472a2e94'
 corr=load(P/'correction-r3.json');assert corr['finding']=='RACKS-R2-REVIEW-001' and corr['review']=={k:extra[0][k] for k in ['path','bytes','sha256']}
 assert [r['pointer'] for r in corr['plan_replacements']]==['/clause_appends/REQ-DEVICE-RACKS-007','/groups/4/action','/role']
 oldplan=load(P/'adoption-r2.json');plan=deepcopy(oldplan)
 for r in corr['plan_replacements']:replace(plan,r['pointer'],r['before'],r['after'])
 assert plan==load(P/'adoption-r3.json')
 cat=load(P/'cases-r2.json');assert [r['pointer'] for r in corr['case_replacements']]==['/cases/65/setup_action','/version','/criterion_scope']
 for r in corr['case_replacements']:replace(cat,r['pointer'],r['before'],r['after'])
 assert cat==load(P/'cases-r3.json') and cat['cases'][:61]==load(P/'cases.json')['cases']
 for i,(old,new) in enumerate(zip(load(P/'cases-r2.json')['cases'],cat['cases'])):
  assert set(old)==set(new) and {k for k in old if old[k]!=new[k]}==({'setup_action'} if i==65 else set())
 assert cat['cases'][65]['setup_action']==load(P/'cases-r2.json')['cases'][65]['setup_action'][:-len(oldplan['groups'][4]['action'])]+plan['groups'][4]['action']
 for kind in ['spec','research']:
  text=(P/f'{kind}-r2.md').read_text()
  if kind=='spec':
   r=corr['spec_clause_replacement'];assert text.count(r['before'])==1;text=text.replace(r['before'],r['after'],1)
   assert r['before']==oldplan['clause_appends']['REQ-DEVICE-RACKS-007'].strip() and r['after']==plan['clause_appends']['REQ-DEVICE-RACKS-007'].strip()
  for r in corr[f'{kind}_editorial']:assert text.count(r['before'])==1;text=text.replace(r['before'],r['after'],1)
  text+=corr[f'{kind}_suffix'];assert text==(P/f'{kind}-r3.md').read_text()
  assert (ROOT/f'wiki/{"specs" if kind=="spec" else "research"}/device-racks.md').read_bytes()==(P/f'{kind}-r3.md').read_bytes()
 spec=(P/'spec-r3.md').read_text();reqs=[dict(id=m[1],title=m[2],contract=m[3]) for m in re.finditer(r'^### (REQ-DEVICE-RACKS-\d{3}) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',spec,re.M|re.S)];assert reqs==load(P/'requirements-r3.json')
 oldreqs=load(P/'requirements-r2.json');assert len(reqs)==28 and {n['id'] for o,n in zip(oldreqs,reqs) if o!=n}=={'REQ-DEVICE-RACKS-007'}
 assert all(reqs[i]==oldreqs[i] for i in range(28) if i!=6)
 note=load(P/'audit-shorthand-qualification-r3.json');a=load(A/'audit.json');assert note['finding']==corr['finding']
 assert [r['json_pointer'] for r in note['original_audit_shorthand']]==['/assessments/88/assessment','/assessments/89/assessment','/proposals/4/proposed_minimal_delta']
 for r in note['original_audit_shorthand']:assert pointer(a,r['json_pointer'])==r['text'] and sha256(r['text'].encode()).hexdigest()==r['text_sha256']
 b=a['blocks'][43];assert note['raw_source']['text']==b['text'] and note['raw_source']['block']==b['id']=='RACK:B044';raw=(P/'manual-racks-2026-10-19.html').read_text();assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 assert note['actual_expected'] is note['actual_comparison'] is note['documentary_expected'] is None and note['target']=='U' and note['executed'] is False and note['coverage_credit']==0
 # Only a fully inspected pure helper from pinned R2, never its imports or main.
 defs=[n for n in ast.parse((P/'validate-r2.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='safety'];assert len(defs)==1 and not defs[0].decorator_list
 env=dict(P=P,ROOT=ROOT,A=A,load=load,pointer=pointer,Counter=Counter);exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned pinned R2 safety>','exec'),env);safety=env['safety'];status=load(P/'actual-status-r2.json');fixture=load(P/'fixtures-r2.json');safety(cat,plan,status,fixture);roles(plan,cat)
 rejected=[]
 for name in ['old-case-erased','actual-oracle','note-only-CC','no-sustained-tail','one-mapped-Rand','one-mapped-variation','no-per-chain-input','no-postfader-return','keyfade-borrowed','browser-layer-borrowed','configuredMulti-borrowed','same-range-instead-third','Volume-override-erased','new-numeric-oracle','wrong-source','controller-promoted','lifecycle-placeholder','CommonDevices-expanded']:
  c,g,s,f=deepcopy(cat),deepcopy(plan),deepcopy(status),deepcopy(fixture)
  def change(case,old,new):
   k=int(case[-3:])-1;group=next(x for x in g['groups'] if x['new_case']==case);c['cases'][k]['setup_action']=c['cases'][k]['setup_action'].replace(old,new);group['action']=group['action'].replace(old,new)
  if name=='old-case-erased':c['cases'][41]['setup_action']='changed'
  elif name=='actual-oracle':s['cases'][0]['actual_expected']='observed'
  elif name=='note-only-CC':change('RCK-068','receipt of BOTH the chosen note AND the chosen CC','note-only reception')
  elif name=='no-sustained-tail':change('RCK-069','sustained NONZERO audible effect tail with NO selector exit','loaded effect flag')
  elif name=='one-mapped-Rand':change('RCK-078','BOTH mapped controls A and B are genuinely productive','A only')
  elif name=='one-mapped-variation':change('RCK-079','BOTH mapped controls A and B are genuinely productive','A only')
  elif name=='no-per-chain-input':f['guard']['actual_per_chain_reception_before_mute_or_delete']=g['guard']['actual_per_chain_reception_before_mute_or_delete']=False
  elif name=='no-postfader-return':change('RCK-071','NONZERO chain input/output AND nonzero send','send flag')
  elif name=='keyfade-borrowed':change('RCK-067','VELOCITY zone fade','KEY fade')
  elif name=='browser-layer-borrowed':change('RCK-073','modifier-drag one populated pad onto another','browser sample drag')
  elif name=='configuredMulti-borrowed':change('RCK-073','actually change an identifiable chain Receive','already configured Multi')
  elif name=='same-range-instead-third':change('RCK-077','SAME unit type but DIFFERENT ranges','same units and range')
  elif name=='Volume-override-erased':change('RCK-078','NO USER exclusion override','any history')
  elif name=='new-numeric-oracle':c['cases'][66]['documentary_expected']=g['groups'][5]['documentary_expected']='exact velocity';c['cases'][66]['documentary_comparator']=g['groups'][5]['documentary_comparator']='numeric'
  elif name=='wrong-source':c['cases'][62]['source_contexts'][0]['json_pointer']='/blocks/0'
  elif name=='controller-promoted':g['groups'][13]['new_case']='RCK-082'
  elif name=='lifecycle-placeholder':g['groups'][21]['new_case']='RCK-082'
  else:g['clause_appends']['REQ-DEVICE-RACKS-023']='A/B'
  try:safety(c,g,s,f)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Retained unsafe fixture accepted '+name)
 focused=[]
 for name in ['both-sections-independent-move','case-only-fade-translation','lose-explicit-U-boundary']:
  g,c=deepcopy(plan),deepcopy(cat)
  if name=='both-sections-independent-move':g['clause_appends']['REQ-DEVICE-RACKS-007']=oldplan['clause_appends']['REQ-DEVICE-RACKS-007']
  elif name=='case-only-fade-translation':c['cases'][65]['setup_action']=c['cases'][65]['setup_action'].replace('Then move the zone itself','Then independently move the fade range')
  else:g['groups'][4]['action']=g['groups'][4]['action'].replace('Independent fade-section translation remains an ungraded U context','Independent fade-section translation is supported')
  try:roles(g,c)
  except AssertionError:focused.append(name)
  else:raise AssertionError('Movement conflation accepted '+name)
 true_subsets=[20,23,26,28,42,43,44,45,46,47];assert all(cat['cases'][i-1]==a['owner_cases'][i-1] for i in true_subsets)
 defs=[n for n in ast.parse((ROOT/'tools/spec_browser.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4 and all(not n.decorator_list for n in defs);be={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned Browser read functions>','exec'),be);ids={r['id'] for r in be['spec_rows'](ROOT/'wiki/specs/device-racks.md',spec)};assert ids=={r['id'] for r in reqs}
 links=0
 for n,base in [('README-r3.md',P),('spec-r3.md',ROOT/'wiki/specs'),('research-r3.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)]+)\)',(P/n).read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   target=base/dest.split('#')[0];assert target.exists(),dest;links+=1
   if '#' in dest and target.suffix=='.md':assert dest.split('#',1)[1] in {be['anchor'](l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')}
 for p in P.iterdir():
  if p.is_file() and p.name not in prior:
   b=p.read_bytes();assert b.endswith(b'\n') and b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines())
 if (P/'manifest-author-r3.json').exists():
  mf=load(P/'manifest-author-r3.json');assert set(mf['files'])=={p.name for p in P.iterdir() if p.is_file()}-{'manifest-author-r3.json'}
  for n,v in mf['files'].items():assert dg(P/n)==v
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',prior_files=36,owned_input_pins=12,inherited_audit_pins=21,requirements=28,cases=81,changed_appended_clauses=1,changed_setup_actions=1,all_source_claim_oracle_guard_fields_exact=True,original61exact=True,actual_nonnull=0,executed=0,complete_topics=0,retained_mutations=rejected,focused_mutations=focused,true_old_subsets=10,Browser_IDs=len(ids),links=links,watched_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
