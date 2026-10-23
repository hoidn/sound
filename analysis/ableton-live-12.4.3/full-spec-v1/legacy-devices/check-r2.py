"""Current read-only Legacy owner integrity. Stdlib/data only; no old tool, parser, decode or vendor code."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,sys
P=Path(__file__).resolve().parent;R=P.parents[3];A=P.parent/'legacy-devices-source-audit'
ROUTE=[('AUTO-FILTER',30,8),('AUTO-FILTER',31,7),('AUTO-FILTER',32,12),('AUTO-FILTER',33,10),('CHORUS',26,8),('CHORUS',27,2),('FLANGER',24,4),('FREQUENCY-SHIFTER',26,2),('FREQUENCY-SHIFTER',27,6),('PHASER',22,5),('CHORUS',28,7),('PHASER',23,6),('REDUX',20,3),('EROSION',18,3),('REDUX',21,5),('AUTO-FILTER',34,3)]
def j(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,p):
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v

def shape(c,f,ad):
 old=j(P/'cases.json');req=j(P/'requirements.json');a=j(A/'audit.json');assert c[:178]==old and len(c)==194 and len({x['id'] for x in c})==194 and len(req)==77
 for i,(x,g,(device,num,rnum)) in enumerate(zip(c[178:],a['proposals'],ROUTE)):
  assert x['id']==f'LEG-{device}-{num:03}' and x['device']==device and x['requirement']==f'REQ-LEG-{device}-{rnum:03}' and x['requirement'] in {r['id'] for r in req}
  assert x['title']==g['title'] and x['action']==g['proposed_future_action'] and x['source_audit_limits_asof']==g['limits']
  assert 'Future unexecuted history only' in x['setup'] and g['proposed_future_positive_baseline'] in x['setup']
  assert 'EACH genuinely NONEMPTY' in x['setup'] and 'BOTH independently productive' in x['setup'] and 'BEFORE zero/disabled/no-effect' in x['setup'] and 'UI-only' in x['setup']
  assert all(x[k] is None for k in ['documentary_expected','documentary_comparison','expected','comparison','actual_expected','actual_comparison','exact_target_expected']) and x['target_grade']=='U' and x['provenance']=='U' and not x['executed'] and x['exact_target_applicability']=='unknown'
  assert x['source_claim'].startswith('D11 predecessor-only source context;') and 'No target law' in x['source_claim']
  assert x['fixture']=='fixtures-r2.json#/current_version_overlay' and ptr(f,x['fixture'].split('#')[1])==f['current_version_overlay']
  rp=x['reviewed_proposal'];assert rp==dict(path=str((A/'audit.json').relative_to(R)),json_pointer=f'/proposals/{i}',id=g['id']) and ptr(j(R/rp['path']),rp['json_pointer'])==g
  expected=[]
  for ident in g['assessment_ids']:
   q=next(q for q in a['assessments'] if q['id']==ident);bi=int(q['source_pointer'].split('/')[-1]);b=a['blocks'][bi];expected.append(dict(path=str((A/'audit.json').relative_to(R)),json_pointer=f'/blocks/{bi}',block_id=b['id'],legacy_locator=b['legacy_locator']))
  assert x['source_references']==expected
  for s in x['source_references']:
   b=ptr(j(R/s['path']),s['json_pointer']);assert b['id']==s['block_id'] and b['legacy_locator']==s['legacy_locator'] and b['source_id']=='D11'
  ag=ad['groups'][i];assert ag['id']==g['id'] and ag['audit_pointer']==f'/proposals/{i}' and ag['case_id']==x['id'] and ag['requirement']==x['requirement']
  assert 'remain U' in ag['remaining_U'] and not ag['complete'] and ag['coverage_credit']==0 and not ag['executed'] and all(ag[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
 assert len(ad['groups'])==16 and ad['new_normative_IDs']==[] and not ad['complete'] and 'AS OF ITS FREEZE' in ad['historical_source_audit']
 assert f['actual_oracles']==[dict(id=x['id'],actual_expected=None,actual_comparison=None,exact_target_expected=None,target='U',executed=False,role='historical-source-content-only' if x['provenance']=='D11' else 'historical-file-only' if x['provenance']=='Dpkg' else 'planned-target-probe') for x in c]
 assert f['source_questions']==a['source_questions'] and f['old_fixture_provider']=='fixtures.json'
 assert 'SOURCE-CONTENT' in f['current_version_overlay']['historical_roles'] and 'FILE-ONLY' in f['current_version_overlay']['historical_roles']
 rr={x['id']:x for x in req}
 for x in old:
  assert x['exact_target_expected'] is None and x['exact_target_applicability']=='unknown'
  if x['provenance']=='D11':assert x['expected']==rr[x['requirement']]['text'].removeprefix('Live 11 predecessor only: ').removesuffix(' Target 12.4.3 Legacy applicability is U.') and x['evidence']==rr[x['requirement']]['evidence']
  elif x['provenance']=='U':assert x['expected'] is None
 assert dict(Counter(x['provenance'] for x in c))=={'Dpkg':8,'D11':45,'U':141}
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before input reads'
 inp=j(P/'inputs-r2.json');paths={R/p for p in inp['files']}|{p for p in P.rglob('*') if p.is_file()}|{R/'wiki/specs/legacy-native-devices.md',R/'wiki/research/legacy-native-devices.md'};before={p:dg(p) for p in paths}
 assert len(inp['old_packet_files'])==44
 for path,q in {**inp['old_packet_files'],**inp['files']}.items():assert dg(R/path)==q,path
 assert inp['review']['sha256']=='19ce923a3a8357750e4f8c1604b23622b7d627ce6374d00f7bf9dfa44a2e5367'
 assert inp['reviewed_source']['sha256']=='afa664a1d55f455753b5dea02a0f7f15ca9d451de1cc33713abd7822501f1b00'
 for source in j(P/'sources-r3.json'):assert dg(Path(source['path']))=={k:source[k] for k in ['bytes','sha256']}
 old=j(P/'manifest-author-r1.json');assert len(old['files'])==43
 for name,row in old['files'].items():assert dg(P/name)==row
 c=j(P/'cases-r2.json');f=j(P/'fixtures-r2.json');ad=j(P/'adoption-r2.json');shape(c,f,ad)
 tests=[('Crisp-inspection-only',lambda c,f,a:c[182].update(action='Inspect Crisp')),('LFO-inventory-only',lambda c,f,a:c[178].update(action='Inspect choices')),('SoftHard-inspection-only',lambda c,f,a:c[190].update(action='Inspect Soft and Hard')),('sidechain-donor-omitted',lambda c,f,a:c[179].update(action='Unfold only')),('indefinite-ring-guarantee',lambda c,f,a:c[180].update(documentary_expected='Rings forever')),('fake-oldSet-admission',lambda c,f,a:c[181].update(action='Upgrade any retained preset')),('single-delay-only',lambda c,f,a:c[183].update(action='Change Delay1 only')),('positive-erased',lambda c,f,a:c[178].update(setup='enabled flag')),('wrong-ring-clause',lambda c,f,a:c[180].update(requirement='REQ-LEG-AUTO-FILTER-006')),('new-oracle',lambda c,f,a:c[178].update(actual_expected='pass')),('D11-to-target',lambda c,f,a:c[1].update(exact_target_expected=c[1]['expected'])),('old-action',lambda c,f,a:c[0].update(action='Decode now')),('overlay-source-to-app',lambda c,f,a:f['actual_oracles'][1].update(role='planned-target-probe')),('overlay-oracle',lambda c,f,a:f['actual_oracles'][0].update(actual_expected='pass')),('group-complete',lambda c,f,a:a['groups'][0].update(complete=True)),('wrong-source-pointer',lambda c,f,a:c[178]['source_references'][0].update(json_pointer='/blocks/0'))]
 for name,fn in tests:
  cc,ff,aa=deepcopy((c,f,ad));fn(cc,ff,aa)
  try:shape(cc,ff,aa)
  except (AssertionError,KeyError,IndexError):pass
  else:raise AssertionError('Unsafe fixture accepted '+name)
 delta=j(P/'delta-r2.json');render=delta['canonical_delta'];assert delta['new_cases']==[x['id'] for x in c[178:]] and delta['cases']==194 and delta['requirements']==77 and not delta['complete']
 for name,folder in [('spec','specs'),('research','research')]:
  original=(P/f'{name}-r1.md').read_text();end=original.index('\n',original.index('\n# ')+1);expected=(original[:end]+'\n'+render['intro']+original[end:]+render['append']).replace('revision: 1\n','revision: 2\n',1)
  assert (P/f'{name}-r2.md').read_text()==expected==(R/f'wiki/{folder}/legacy-native-devices.md').read_text()
  assert 'historical R1 context' in expected and '141target-Uprobes' in expected and 'AS OF AUTHOR FREEZE' in expected
 spec=(P/'spec-r2.md').read_text();oldspec=(P/'spec-r1.md').read_text();section=lambda t:t.split('## Requirements\n',1)[1].split('## Case index and counts\n',1)[0];assert section(spec)==section(oldspec)
 assert {r['id'] for r in j(P/'requirements.json')}==set(re.findall(r'^### (REQ-[A-Z0-9-]+) ',spec,re.M))
 links=0
 for q in [R/'wiki/specs/legacy-native-devices.md',R/'wiki/research/legacy-native-devices.md',P/'README-r2.md']:
  t=q.read_text();assert t.endswith('\n') and all(l.rstrip()==l for l in t.splitlines())
  for dest in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',t):
   if re.match(r'(https?://|mailto:|#)',dest):continue
   from urllib.parse import unquote
   path=(q.parent/unquote(dest.split('#')[0])).resolve();assert path.exists(),(q,dest);links+=1
 newnames=['README-r2.md','cases-r2.json','adoption-r2.json','fixtures-r2.json','inputs-r2.json','delta-r2.json','spec-r2.md','research-r2.md','check-r2.py']
 for n in newnames:assert all(l.rstrip()==l for l in (P/n).read_text().splitlines()),n
 sealed=(P/'manifest-author-r2.json').exists()
 if sealed:
  m=j(P/'manifest-author-r2.json');assert set(m['payloads'])=={str(p.relative_to(R)) for p in P.rglob('*') if p.is_file() and p.name!='manifest-author-r2.json'} and len(m['payloads'])==53
  for path,row in m['payloads'].items():assert dg(R/path)==row
 assert before=={p:dg(p) for p in paths}
 print(json.dumps(dict(status='pass',sealed=sealed,requirements=77,normative_section_exact=True,cases=194,old_cases_exact=178,old_files_exact=44,new_U_histories=16,D11_source_only=45,Dpkg_file_only=8,target_U_probes=141,all194_actual_overlay_null_U=True,groups_partial=16,unsafe_fixtures_rejected=[n for n,_ in tests],immutable_pins=len(inp['files']),links=links,watched_unchanged=len(paths),writes=False,complete=False,independent_review='pending as of author freeze'),indent=2))
if __name__=='__main__':main()
