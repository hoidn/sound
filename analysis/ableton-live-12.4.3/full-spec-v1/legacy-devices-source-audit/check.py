"""Read-only selected D11 source reconciliation; no old author/validator/main/decode or vendor execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,sys
A=Path(__file__).resolve().parent;R=A.parents[3];O=A.parent/'legacy-devices'
SECTIONS=['auto-filter','auto-pan','chorus','erosion','flanger','frequency-shifter','phaser','redux-legacy']
DISP={'E':'editorial-or-structural','R':'research-or-guidance','U':'documented-precursor-context-target-U','X':'represented-subset-with-missing-actual-action-or-context'}
def j(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,p):
 for k in p.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v

def primary(inp):
 parser=R/inp['parser'];assert dg(parser)==inp['files'][inp['parser']]
 scope={};exec(compile(parser.read_text(),str(parser),'exec'),scope)
 html=(O/'manual-11-audio-effects-2026-10-19.html').read_text();allb,allr=scope['extract'](html,'D11')
 chosen=[];ranges=[]
 for b in allb:
  h=next((h for h in b['heading_context'] if h['level']==2),None)
  if h and h['anchor'] in SECTIONS:b['profile_section']=h['anchor'];chosen.append(b)
 for s in SECTIONS:
  ch=[b for b in chosen if b['profile_section']==s];first=ch[0]['raw_start'];i=next(i for i,b in enumerate(allb) if b['raw_start']==first);end=next((b['raw_start'] for b in allb[i+1:] if b['kind']=='h2'),len(html));ranges.append((first,end))
  retained=j(O/f'manual-{s}-blocks.json');assert len(ch)==len(retained)
  for b,q in zip(ch,retained):b['legacy_locator']=q['locator'];assert b['text']==q['text'] and b['html_line']==q['html_line']
 resources=[q for q in allr if any(start<=q['raw_start']<end for start,end in ranges)]
 assert len(allb)==994 and len(chosen)==114 and len(resources)==23
 return chosen,resources

def build(plan,inp):
 b,resources=primary(inp);req=j(O/'requirements.json');cases=j(O/'cases.json');assess=[]
 for i,block in enumerate(b):
  row=plan['judgments'][block['legacy_locator']];selected=row['selected_requirements'];rr=[];cc=[]
  for rid in selected:
   ri=next(n for n,r in enumerate(req) if r['id']==rid);rr.append(dict(path=str((O/'requirements.json').relative_to(R)),json_pointer=f'/{ri}',body_pointer=f'/{ri}/text',id=rid,role='Manually selected precursor/unknown context only; assessment limits sufficiency.'))
   for ci,c in enumerate(cases):
    if c['requirement']==rid:cc.append(dict(path=str((O/'cases.json').relative_to(R)),json_pointer=f'/{ci}',action_pointer=f'/{ci}/action',id=c['id'],provenance=c['provenance'],role='retained-source-content check only; never target gesture' if c['provenance']=='D11' else 'file-only check; not executed/decoded here' if c['provenance']=='Dpkg' else 'planned target-U history; only explicitly named operations, not setup/inspection inferred as gesture'))
  assess.append(dict(id=f'LDSA-A{i+1:03}',block=block['id'],legacy_locator=block['legacy_locator'],source_pointer=f'/blocks/{i}',quote=block['text'],quote_sha256=sha256(block['text'].encode()).hexdigest(),scope='Manually read WHOLE context; grouped note, not atomic assertion census or complete source qualifier coverage.',disposition=DISP[row['disposition']],assessment=row['assessment'],requirement_refs=rr,case_refs=cc,proposal_groups=row['proposal_groups'],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 proposals=deepcopy(plan['proposals'])
 for g in proposals:g['assessment_ids']=[q['id'] for q in assess if g['id'] in q['proposal_groups']]
 d=j(A.parent/'distortion/requirements.json');dc=j(A.parent/'distortion/cases.json')
 return dict(role='Analyst retained-source-only audit; no normative adoption',source=dict(path=str((O/'manual-11-audio-effects-2026-10-19.html').relative_to(R)),bytes=497168,sha256='98a59baaa97cff409894870f26eb04697c28f8c59ecedc40ade395dcf36438d4',url='https://www.ableton.com/en/live-manual/11/live-audio-effect-reference/',capture_date='2026-10-19',capture_utc=None,version='Version11; exact minor/date unadvertised; target12.4.3U'),blocks=b,resources=resources,owner_requirements=req,owner_cases=cases,owner_fixtures=j(O/'fixtures.json'),canonical_asof=inp['canonical_asof'],selected_neighbors=[dict(path=str((A.parent/'distortion/requirements.json').relative_to(R)),pointer='/16',record=d[16]),dict(path=str((A.parent/'distortion/cases.json').relative_to(R)),pointer='/40',record=dc[40])],assessments=assess,proposals=proposals,source_questions=plan['source_questions'],common_future_prerequisites=plan['common_future_prerequisites'],summary=dict(whole_chapter_blocks_FILTERING_ONLY=994,selected_contexts=114,section_counts=dict(Counter(q['profile_section'] for q in b)),block_kinds=dict(Counter(q['kind'] for q in b)),literal_resources=23,resource_kinds=dict(Counter(q['kind'] for q in resources)),whole_context_judgments=114,atomic_facets=False,requirements=77,requirement_grades=dict(Counter(q['provenance'] for q in req)),cases=178,case_grades=dict(Counter(q['provenance'] for q in cases)),all_exact_target_expected_null=True,proposals=len(proposals),questions=len(plan['source_questions']),immutable_pins=len(inp['files']),old_packet_files=44,new_normative_IDs=0,new_cases=0,adoptions=0,coverage_credit=0,complete_profiles=0,executed=0,dispositions=dict(Counter(q['disposition'] for q in assess))))

# Finite semantic guards against joint plan+audit laundering; not a substitute for independent review.
GUARDS={
 'auto-filter:B010':(['REQ-LEG-AUTO-FILTER-003'],['not an explicit Drive slider edit','G16']),
 'auto-filter:B011':(['REQ-LEG-AUTO-FILTER-005'],['actually selects Morph','each named context snap']),
 'auto-filter:B019':(['REQ-LEG-AUTO-FILTER-007'],['donor-modulation positives','does not explicitly','G02']),
 'auto-filter:B022':(['REQ-LEG-AUTO-FILTER-008'],['inspects shapes/Hz-sync','not actual each-shape','G01']),
 'auto-filter:B024':(['REQ-LEG-AUTO-FILTER-008'],['B023 says Phase and Offset','B025 describes Spin']),
 'chorus:B007':(['REQ-LEG-CHORUS-005'],['actually compares numeric and X-Y','toggles *20']),
 'chorus:B012':(['REQ-LEG-CHORUS-008'],['only inspects Crisp','does not explicitly','G05']),
 'erosion:B003':(['REQ-LEG-EROSION-002','REQ-LEG-EROSION-003'],['actually performs ordinary','actually compares ordinary and platform-appropriate modifier']),
 'flanger:B007':(['REQ-LEG-FLANGER-004'],['only inspects six shapes','G07']),
 'flanger:B013':(['REQ-LEG-FLANGER-007'],['inspects AND toggles Hi-Quality']),
 'frequency-shifter:B010':(['REQ-LEG-FREQUENCY-SHIFTER-006'],['inspects shapes/Hz-sync','G09']),
 'frequency-shifter:B014':(['REQ-LEG-FREQUENCY-SHIFTER-004','REQ-LEG-FREQUENCY-SHIFTER-008'],['genuinely contrasts Drive','compares mix endpoints']),
 'phaser:B010':(['REQ-LEG-PHASER-005'],['inspection is not explicit selection','G10']),
 'redux-legacy:B005':(['REQ-LEG-REDUX-003'],['inspects Soft/Hard','does not explicitly select','G13']),
 'redux-legacy:B009':(['REQ-LEG-REDUX-005'],['inspects BitReduction enable','rather than explicitly toggling','G15'])}

def semantic(plan,a):
 assert len(plan['judgments'])==len(a['assessments'])==114 and len(a['owner_requirements'])==77 and len(a['owner_cases'])==178
 actual={q['legacy_locator']:q for q in a['assessments']}
 for key,(ids,phrases) in GUARDS.items():
  row=plan['judgments'][key];assert row['selected_requirements']==ids
  for phrase in phrases:
   if re.fullmatch('G[0-9]+',phrase):assert phrase in row['proposal_groups']
   else:assert phrase in row['assessment']
  assert actual[key]['assessment']==row['assessment']
 for q in a['assessments']+a['proposals']:
  assert all(q[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and q['target']=='U' and not q['executed'] and not q['complete'] and q['coverage_credit']==0
 assert len(a['proposals'])==16 and len(a['source_questions'])==8
 for g in a['proposals']:
  assert g['new_normative_IDs']==[] and 'NONEMPTY' in g['proposed_future_positive_baseline'] and 'before' in g['proposed_future_positive_baseline'].lower() and g['assessment_ids']
 assert 'BOTH independently productive' in plan['common_future_prerequisites'] and 'EACH' in plan['common_future_prerequisites']
 assert a['owner_requirements']==j(O/'requirements.json') and a['owner_cases']==j(O/'cases.json') and a['owner_fixtures']==j(O/'fixtures.json')
 assert all(q['exact_target_expected'] is None and q['exact_target_applicability']=='unknown' and (q['provenance']!='U' or q['expected'] is None) for q in a['owner_cases'])
 assert a['source']['capture_utc'] is None
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before input reads'
 inp=j(A/'inputs.json');plan=j(A/'plan.json');a=j(A/'audit.json');watch={R/p for p in inp['files']}|{p for p in A.iterdir() if p.is_file()};before={p:dg(p) for p in watch}
 for p,q in inp['files'].items():assert dg(R/p)==q,p
 assert len(inp['old_packet_files'])==44
 old=j(O/'manifest-author-r1.json');assert len(old['files'])==43
 for name,row in old['files'].items():assert dg(O/name)==row
 assert dg(O/'manifest-author-r1.json')['sha256']=='804eaebe8be0d1ca523041d01eb0ab4732e61870f5facf4cc3a979668e687d89'
 for s in j(O/'sources-r3.json'):assert dg(Path(s['path']))=={k:s[k] for k in ['bytes','sha256']}
 assert a==build(plan,inp);semantic(plan,a)
 assert set(plan['judgments'])=={q['legacy_locator'] for q in a['blocks']}
 ids={r['id'] for r in a['owner_requirements']};assert ids==set(re.findall(r'^### (REQ-[A-Z0-9-]+) ',(O/'spec-r1.md').read_text(),re.M))
 for q in a['assessments']:
  b=ptr(a,q['source_pointer']);assert b['text']==q['quote'] and b['legacy_locator']==q['legacy_locator'] and b['id']==q['block']
  for ref in q['requirement_refs']+q['case_refs']:
   resolved=ptr(j(R/ref['path']),ref['json_pointer']);assert resolved['id']==ref['id']
   field='body_pointer' if 'body_pointer' in ref else 'action_pointer';assert ptr(j(R/ref['path']),ref[field])==resolved['text' if field=='body_pointer' else 'action']
   if ref.get('provenance')=='D11':assert 'never target gesture' in ref['role']
 for n in a['selected_neighbors']:assert ptr(j(R/n['path']),n['pointer'])==n['record']
 assert a['selected_neighbors'][0]['record']['id']=='REQ-DST-EROSION-005' and a['selected_neighbors'][1]['record']['id']=='DST-EROSION-007'
 assert (R/inp['canonical_asof']['spec']).read_bytes()==(O/'spec-r1.md').read_bytes() and (R/inp['canonical_asof']['research']).read_bytes()==(O/'research-r1.md').read_bytes()
 rejected=[]
 for key,badnote in [('chorus:B012','015 actually toggles Crisp from its menu'),('redux-legacy:B005','005 actually selects Soft and Hard'),('auto-filter:B022','015 actually selects all shapes and Hz/sync'),('auto-filter:B011','009 only inspects Morph; no snap action'),('chorus:B007','009 only inspects XY; no edits'),('flanger:B013','013 merely inspects quality'),('phaser:B010','009 actually changes every control'),('frequency-shifter:B010','011 actually chooses every shape')]:
  bp=deepcopy(plan);bad=deepcopy(a);bp['judgments'][key]['assessment']=badnote;next(q for q in bad['assessments'] if q['legacy_locator']==key)['assessment']=badnote
  try:semantic(bp,bad)
  except AssertionError:rejected.append(key)
  else:raise AssertionError('Unsafe joint note accepted '+key)
 for name,change in [('new-oracle',lambda b:b['proposals'][0].update(actual_expected='pass')),('positive-erased',lambda b:b['proposals'][0].update(proposed_future_positive_baseline='enabled flag')),('old-U-promoted',lambda b:next(q for q in b['owner_cases'] if q['provenance']=='U').update(expected='pass')),('D11-promoted-to-target',lambda b:b['owner_cases'][1].update(exact_target_expected=b['owner_cases'][1]['expected'])),('fabricated-source-UTC',lambda b:b['source'].update(capture_utc='2026-10-19T00:00:00Z'))]:
  bad=deepcopy(a);change(bad)
  try:semantic(plan,bad)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 # Source omission, pointer and quote fixtures have independent equality/dereference checks.
 for name,change in [('omit-context',lambda b:b['assessments'].pop()),('wrong-action-pointer',lambda b:next(q for q in b['assessments'] if q['case_refs'])['case_refs'][0].update(action_pointer='/0/action')),('wrong-quote',lambda b:b['assessments'][10].update(quote='modern filter'))]:
  bad=deepcopy(a);change(bad)
  try:
   assert bad==build(plan,inp)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe source/pointer mutation accepted '+name)
 for n in ['README.md','inputs.json','plan.json','audit.json','check.py']:assert all(l.rstrip()==l for l in (A/n).read_text().splitlines()),n
 sealed=(A/'manifest.json').exists()
 if sealed:
  m=j(A/'manifest.json');assert len(m['files'])==5
  for name,row in m['files'].items():assert dg(A/name)==row
  assert {p.name for p in A.iterdir() if p.is_file()}==set(m['files'])|{'manifest.json'}
 assert before=={p:dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=sealed,contexts=114,resources=23,requirements=77,cases=178,D11_source_content_checks=45,Dpkg_file_only=8,target_U_probes=125,all178_exact_target_null=True,proposals=16,questions=8,new_adoption=0,unsafe_fixtures_rejected=rejected,requirement_heading_IDs=77,immutable_pins=len(inp['files']),old_files_exact=44,watched_unchanged=len(watch),writes=False,independent_review='pending as of author freeze'),indent=2))
if __name__=='__main__':main()
