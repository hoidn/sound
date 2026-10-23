"""Owned read-only Racks R2 source/delta/preservation checks, never old tools."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,importlib.util,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'racks-source-audit'
def load(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/') if s else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def safety(cat,plan,status,fixture):
 cs=cat['cases'];old=load(P/'cases.json')['cases'];assert len(cs)==81 and cs[:61]==old
 assert [c['id'] for c in cs]==[f'RCK-{i:03}' for i in range(1,82)]
 assert Counter(c['criterion_domain'] for c in cs)=={'installed-document':3,'Live-12-documented':66,'unknown':12}
 assert len(status['cases'])==81
 for c,s in zip(cs,status['cases']):assert s==dict(id=c['id'],actual_expected=None,actual_comparison=None,target='U',executed=False)
 assert len(plan['groups'])==22 and all(plan['groups'][i]['new_case'] is None for i in [13,21])
 assert plan['groups'][21]['retained_cases']==[f'RCK-{i:03}' for i in range(53,62)]
 assert all(fixture['guard'].values()) and fixture['guard']==plan['guard']
 a=load(A/'audit.json')
 for c in cs[61:]:
  g=next(g for g in plan['groups'] if g['new_case']==c['id']);assert c['adoption_group']==g['group']
  assert c['setup_action']==fixture['common']+g['action'] and c['positive_guard']==fixture['guard'] and c['requirements']==g['requirements']
  assert c['expected_comparator'] is c['open_result'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['execution']=='unexecuted' and c['exact_12_4_3_runtime_applicability']=='U' and c['fixture']=='fixtures-r2.json#RACKS-OWNED-R2'
  claims=[]
  for r in c['source_contexts']:
   b=pointer(load(ROOT/r['catalog']),r['json_pointer']);assert b['id']==r['block'];claims.append(b['text'])
  assert c['source_claim']==' '.join(claims)
  assert [r['block'] for r in c['source_contexts']]==g['source_blocks']
  assert c['documentary_expected']==g['documentary_expected'] and c['documentary_comparator']==g['documentary_comparator']
  if c['id'] not in ['RCK-063','RCK-076','RCK-079']:assert c['documentary_expected'] is c['documentary_comparator'] is None
 assert sum(c['documentary_comparator'] is not None for c in cs[61:])==3
 actions={c['id']:c['setup_action'] for c in cs[61:]}
 for case,required in {
 'RCK-067':['VELOCITY zone fade','actual SELECTOR fade','020 actual KEY fade'],
 'RCK-068':['receipt of BOTH the chosen note AND the chosen CC','BOTH note and CC positives'],
 'RCK-069':['sustained NONZERO audible effect tail with NO selector exit','nonmuted wet/output'],
 'RCK-071':['NONZERO chain input/output AND nonzero send','nonmuted return/output'],
 'RCK-073':['BOTH known populated pads/chains','modifier-drag one populated pad onto another','actually change an identifiable chain Receive'],
 'RCK-074':['BOTH finite known chains','actual productive note reception'],
 'RCK-075':['factory/no-custom/no-loaded-preset','empty-alt'],
 'RCK-077':['SAME unit type but DIFFERENT ranges','generic name','AND same-range'],
 'RCK-078':['BOTH mapped controls A and B are genuinely productive','NO USER exclusion override'],
 'RCK-079':['BOTH mapped controls A and B are genuinely productive','included recall of BOTH'],
 'RCK-080':['044 actual','045 equal-start-volume'],
 'RCK-081':['046 actual Drum38 mixer devices+MIDI versus chain-list devices only','047 return-to-Set-return']}.items():
  assert all(t in actions[case] for t in required),(case,required)
 assert not any(rid in plan['clause_appends'] for rid in [f'REQ-DEVICE-RACKS-{i:03}' for i in range(23,29)])
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check']
 prior=load(P/'prior-files-r2.json');pins=load(P/'inputs-r2.json');inherited=load(A/'inputs.json')['files'];history=load(P/'consumer-impact-r2.json')
 assert len(prior)==18 and len(pins)==11 and len(inherited)==21
 watch={p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in pins+inherited}|{ROOT/n for n in history['consumer_identities']}|{ROOT/'wiki/specs/device-racks.md',ROOT/'wiki/research/device-racks.md'};before={str(p):dg(p) for p in watch}
 for n,r in prior.items():assert dg(P/n)==r,n
 for r in pins+inherited:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
 assert dg(A/'manifest.json')['sha256']=='3173fa2b45588725abab7193e793009d8ad1f4ef41c3e686d86d7c274a0219c2'
 assert dg(P.parent/'reviews/racks-source-audit-review.json')['sha256']=='bc4ca028eca17ee1d9eb51eeb9ea3fb488124359c6c65a086c3ad86abb47bb15'
 for n,r in load(A/'manifest.json')['files'].items():assert dg(A/n)==r
 for snap in load(A/'inputs.json')['canonical_snapshots']:
  n='spec-before-r2.md' if '/specs/' in snap['original_canonical'] else 'research-before-r2.md';assert (P/n).read_text()==snap['text'] and dg(P/n)=={k:snap[k] for k in ['bytes','sha256']}
 for n,r in history['consumer_identities'].items():assert dg(ROOT/n)==r
 assert len(history['records'])==28 and len(history['consumer_identities'])==26 and not history['consumer_mutations'] and not history['historical_replay']
 for r in history['records']:assert pointer(load(ROOT/r['consumer']),r['json_pointer'])==dg(P/r['historical_snapshot'])['sha256']==r['literal_sha256']
 author=module(P/'author-r2.py','racks_owned_author_r2');plan=load(P/'adoption-r2.json');cat=load(P/'cases-r2.json');status=load(P/'actual-status-r2.json');fixture=load(P/'fixtures-r2.json');assert safety(cat,plan,status,fixture)
 for n,t in author.build().items():assert (P/n).read_text()==t,n
 for n,c in [('spec-r2.md','wiki/specs/device-racks.md'),('research-r2.md','wiki/research/device-racks.md')]:assert (P/n).read_bytes()==(ROOT/c).read_bytes()
 old=author.reqs((P/'spec-before-r2.md').read_text());now=author.reqs((P/'spec-r2.md').read_text());assert len(old)==len(now)==28 and [r['id'] for r in old]==[r['id'] for r in now]
 changed=[dict(id=o['id'],before=o['contract'],after=n['contract']) for o,n in zip(old,now) if o!=n];assert changed==load(P/'delta-r2.json')['changed_contracts'] and len(changed)==6
 assert old[22:]==now[22:] and cat['cases'][47:52]==load(P/'cases.json')['cases'][47:52]
 assert all(old[i]==now[i] for i in [0,10,12,13]),'installed/RR01/RR02 predicates exact'
 assert (P/'research-r2.md').read_text().startswith((P/'research-before-r2.md').read_text().replace('revision: 1\n','revision: 2\n',1))
 parser=module(P.parent/'clip-view-source-audit/source_parser.py','racks_retained_parser');a=load(A/'audit.json');blocks,resources=parser.extract((P/'manual-racks-2026-10-19.html').read_text(),'RACK');assert blocks==a['blocks'] and len(blocks)==124 and len(resources)==53
 for raw,r in zip(resources,a['resources']):assert raw=={k:v for k,v in r.items() if k not in {'role','pixels_or_destination_inspected','complete','target'}}
 dev,_=parser.extract((P/'manual-devices-2026-10-19.html').read_text(),'DEV');assert len(a['selected_common_device_context'])==7
 for b in a['selected_common_device_context']:assert b==next(d for d in dev if d['id']==b['id'])
 spans={b['id']:[] for b in blocks};assert len(a['assessments'])==264
 for f in a['assessments']:
  b=pointer(a,f['block_pointer']);lo,hi=f['text_span'];assert b['id']==f['block'] and b['text'][lo:hi]==f['quote'] and sha256(f['quote'].encode()).hexdigest()==f['quote_sha256'];spans[b['id']].append((lo,hi))
  assert pointer(a,f['full_qualifier_context_pointer'])==b['text']
  for r in f['case_refs']+f['requirement_refs']:assert pointer(a[r['catalog']],r['json_pointer'])['id']==r['id']
 for b in blocks:
  seen=set()
  for lo,hi in spans[b['id']]:assert not seen.intersection(range(lo,hi));seen.update(range(lo,hi))
  assert all(i in seen for i,c in enumerate(b['text']) if not c.isspace()),b['id']
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4 and all(not n.decorator_list for n in defs);env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned Browser read functions>','exec'),env)
 ids={r['id'] for r in env['spec_rows'](ROOT/'wiki/specs/device-racks.md',(P/'spec-r2.md').read_text())};assert ids=={r['id'] for r in now}
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
  elif name=='CommonDevices-expanded':g['clause_appends']['REQ-DEVICE-RACKS-023']='A/B'
  try:safety(c,g,s,f)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('accepted unsafe fixture '+name)
 retained=['RCK-020','RCK-023','RCK-026','RCK-028','RCK-042','RCK-043','RCK-044','RCK-045','RCK-046','RCK-047']
 assert all(cat['cases'][int(n[-3:])-1]==a['owner_cases'][int(n[-3:])-1] for n in retained)
 links=0
 for n,base in [('README-r2.md',P),('spec-r2.md',ROOT/'wiki/specs'),('research-r2.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)]+)\)',(P/n).read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   target=base/dest.split('#')[0];assert target.exists(),dest;links+=1
   if '#' in dest and target.suffix=='.md':assert dest.split('#',1)[1] in {env['anchor'](l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')},dest
 for p in [p for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in prior]+[ROOT/'wiki/specs/device-racks.md',ROOT/'wiki/research/device-racks.md']:
  b=p.read_bytes();assert b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines()),str(p)
 sealed=(P/'manifest-author-r2.json').exists()
 if sealed:
  mf=load(P/'manifest-author-r2.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(mf['files'])|{'manifest-author-r2.json'}
  for n,r in mf['files'].items():assert dg(P/n)==r,n
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=sealed,requirements=28,refined_contracts=6,cases=81,old61_exact=True,new_cases=20,installed=3,documentary=66,U=12,new_named_pairs=3,new_null_pairs=17,all_actual_null_U=True,executed=0,complete_topics=0,source_blocks=124,facets=264,resources=53,selected_CommonDevices=7,groups=22,groups_with_new_actions=20,prior_files=18,input_pins=11,audit_input_pins=21,BrowserIDs=len(ids),links=links,historical_occurrences=28,consumer_files=26,negative_fixtures=rejected,retained_positive_subsets=retained,watch_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
