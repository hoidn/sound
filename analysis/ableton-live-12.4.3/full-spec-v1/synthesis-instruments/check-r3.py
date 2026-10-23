"""Read-only finite current Synthesis owner R3 integrity; no oldtool/runtime/decode."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'synthesis-instruments-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def ptr(v,path):
 for k in path.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def effective_audit():
 a=load(A/'audit.json');changes=load(A/'response-r2.json')['changes'];assert len(changes)==25
 for x in changes:
  if x['document']!='audit.json':continue
  path,key=x['json_pointer'].rsplit('/',1);parent=ptr(a,path);key=int(key) if isinstance(parent,list) else key
  assert parent[key]==x['before'];parent[key]=deepcopy(x['after'])
 assert a['assessments'][393]['requirement_refs'][0]['id']=='REQ-SYN-OP-015' and a['assessments'][394]['requirement_refs'][0]['id']=='REQ-SYN-OP-015'
 return a

def validate(req,cases,f,ad,a):
 oldr=load(P/'requirements.json');oldc=load(P/'cases.json');assert req[:109]==oldr and cases[:154]==oldc and len(req)==110 and len(cases)==190
 assert len({r['id'] for r in req})==110 and len({c['id'] for c in cases})==190
 assert Counter(r['provenance'] for r in req)=={'D12':105,'U':5}
 nr=req[-1];assert nr['id']=='REQ-SYN-OP-024' and nr['target_applicability']=='U' and nr['source_blocks']==['operator:B004','operator:B005']
 assert 'shell parameter' in nr['contract'] and 'center display' in nr['contract'] and 'triangular button' in nr['contract'] and 'folds' in nr['contract']
 assert a['owner_requirements']==oldr and a['owner_cases']==oldc
 assert len(ad['groups'])==37 and sum(g['overlay_only'] for g in ad['groups'])==1 and ad['effective_source_corrections']['literal_fields']==25
 assert ad['effective_source_corrections']['applied_audit_changes']==[x for x in load(A/'response-r2.json')['changes'] if x['document']=='audit.json']
 ass={x['id']:x for x in a['assessments']};source={b['id']:(i,b) for i,b in enumerate(a['blocks'])};ids={r['id'] for r in req};new=cases[154:]
 for i,(g,sg) in enumerate(zip(ad['groups'],a['proposals'])):
  assert g['id']==sg['id'] and g['audit_pointer']==f'/proposals/{i}' and not g['complete'] and not g['coverage_credit'] and not g['executed'] and g['target']=='U'
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
  selected=[ass[x] for x in sg['assessment_ids']]
  for field,catalog,body in [('historical_requirement_refs',oldr,'contract'),('historical_case_refs',oldc,'setup_and_action')]:
   srcfield='requirement_refs' if body=='contract' else 'case_refs';expected=list({(x['json_pointer'],x['id']):x for s in selected for x in s[srcfield]}.values());assert g[field]==expected
   for ref in g[field]:
    row=ptr(catalog,ref['json_pointer']);assert row['id']==ref['id']
    bp=ref['scoped_predicate_pointer'] if body=='contract' else ref['actual_action_pointer'];assert ptr(catalog,bp)==row[body] and isinstance(ptr(catalog,bp),str) and ptr(catalog,bp)
  blocks=list(dict.fromkeys(s['block'] for s in selected))
  if g['id']=='G20':blocks=['INS:B485','INS:B486']
  if g['id']=='G10':blocks+=['INS:B275','INS:B278'];assert g['eligibility_bridge']['requirement']=='REQ-SYN-DS-003'
  refs=[{'path':str((A/'audit.json').relative_to(ROOT)),'pointer':f'/blocks/{source[x][0]}','block_id':x,'quote':source[x][1]['text']} for x in blocks];assert g['selected_source_contexts']==refs
  for ref in refs:assert ptr(a,ref['pointer'])['id']==ref['block_id'] and ptr(a,ref['pointer']+'/text')==ref['quote']
  linked=[c for c in new if c['adoption_group']==g['id']];assert g['new_cases']==[c['id'] for c in linked] and g['overlay_only']==(g['id']=='G19') and len(linked)==(0 if g['overlay_only'] else 1)
  for c in linked:
   assert c['source_references']==refs and c['source_blocks']==[a['block_routes'][x]['old_local_locator'] for x in blocks]
   assert c['requirements'] and set(c['requirements'])<=ids and c['provenance']=='U' and c['target_grade']=='U' and not c['executed']
   assert c['preconditions']==['fixtures-r3.json#/current_version_overlay','fixtures-r3.json#/current_version_overlay/positive_processing','independently-admitted-feature-and-history']
   assert c['fixture']=='fixtures-r3.json#/current_version_overlay' and c['positive_baseline'] and c['limits'] and c['source_claim']
   assert all(c[k] is None for k in ('documentary_expected','documentary_comparator','expected','comparison','actual_expected','actual_comparison'))
 by={c['adoption_group']:c for c in new}
 # Explicit operations; source labels/setup/expected roles cannot substitute for these histories.
 checks={'G01':['actually change Osc1 Oct','each Osc1/Osc2/Noise'],'G03':['Actually select','nine LFO waves','change the offered rate'],'G04':['both section click','display1/2 toggles','Freq/Res/HP knobs'],'G07':['explicitly invoke Show Similar Files','waveform HotSwap','title-bar HotSwap'],'G08':['drop-down','two dedicated knobs','toggle Effect On'],'G10':['toggle Velocity/Slide','ModAmount','eligible Trigger','Gate-disabled'],'G11':['Copy to B and Copy to A','X for each'],'G12':['Basic Shapes then Dual Basic Shapes','st->sd','do not assert Octaves/Cents unit changes'],'G13':['drag a numerical value vertically','type a value via keyboard'],'G14':['LFO1 type-dependent macro','each LFO','No LFO2 type-dependent macro'],'G15':['drag a selected cell up then down','other in a distinct history'],'G16':['Oscillator ScaleAwareness and Filter ScaleAwareness'],'G18':['move SVF L-B-H-N','SwitchedRes Lofi'],'G20':['change an admitted Operator shell parameter','click the upper-left triangular fold button','not adopted'],'G21':['non-Off Repeat','even/odd/all','Normalize off/on','distinct target'],'G22':['change Coarse/Fine','Level/Vel/Key/Phase'],'G23':['toggle LFO On','LowHiSync','A/B amounts/chooser'],'G24':['keyboard cursor keys','invoke (rather than inspect)','oscillator-parameter copy'],'G25':['change Freq/Res/Drive and continuous Morph','drag response curve'],'G26':['Velocity, Key, Aftertouch, Pitch Bend and Mod Wheel','Volume and Pan','amounts separately','choose Off'],'G27':['toggle PitchEnvelopeOn','DestinationB chooser'],'G28':['toggle Interpolation/Antialias'],'G29':['change its Gain/Pan/Semi/Detune','both choosers'],'G30':['explicitly drag from Browser','invoke Raw off/on'],'G31':['change its two controls separately','switch type'],'G32':['edit Drive and continuous Morph','eligible then ineligible'],'G33':['both mains disabled','both filters engaged'],'G34':['drag matrix amount up/down','Env2/3 Initial/Peak/Final'],'G35':['rate slider and waveform-display frequency drag','Attack/Offset/Amount'],'G36':['change global Transpose and Volume'],'G37':['actually invoke Hi-Quality off then on']}
 for g,parts in checks.items():assert all(s in by[g]['setup_and_action'] for s in parts),g
 assert 'REQ-SYN-DS-003' in by['G10']['requirements'] and by['G10']['eligibility_bridge']==next(g for g in ad['groups'] if g['id']=='G10')['eligibility_bridge']
 assert 'Filter Drive and continuous Morph' in by['G25']['limits'] and 'OP017 Shaper Drive/wet bypass remains separate' in by['G25']['limits']
 for g in ['G01','G02','G03','G05','G06','G08','G09','G10','G11','G12','G14','G15','G16','G17','G18','G21','G22','G23','G24','G25','G26','G27','G28','G29','G30','G31','G32','G33','G34','G35','G36','G37']:assert 'NONEMPTY' in by[g]['positive_baseline'],g
 assert 'UI-only' in by['G20']['positive_baseline'] and 'No Info View' in by['G20']['positive_baseline']
 ov=f['current_version_overlay'];policy=' '.join(ov['positive_processing']);assert ov['positive_processing']==a['common_future_prerequisites'] and all(x in policy for x in ['UI-only','NONEMPTY','NONZERO','BOTH independent','BEFORE','not the gesture'])
 assert ov['actual_oracles']==[{'id':c['id'],'expected':None,'comparison':None,'target':'U','executed':False} for c in cases]
 assert 'only' in ov['unit_qualification']['current_scoped_predicate'].lower() and 'st->sd' in ov['unit_qualification']['current_scoped_predicate'] and 'Octaves/Cents unit changes remain U' in ov['unit_qualification']['current_scoped_predicate']
 paired=ov['paired_engine_voice_refinement'];assert paired['existing_cases']==['SYN-ME-002','SYN-ME-019','SYN-ME-022','SYN-ME-023'] and all(x in paired['predicate'] for x in ['BOTH independent','NONEMPTY','NONZERO','nonmuted','mapped Spread->Pan'])
 assert 'LoopTime Sustain-to-Initial' in ov['operator_contexts'] and 'distinct unresolved' in ov['operator_contexts'] and f['source_questions']==ad['source_questions']==a['source_questions']
 assert sum(c['documentary_comparator'] is not None for c in cases)==58
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer or oldtool execution'
 inp=load(P/'inputs-r3.json');watched={ROOT/p for p in inp['files']}|{ROOT/p for p in inp['canonical_before']}|{p for p in P.rglob('*') if p.is_file()};before={str(p):dg(p) for p in watched}
 assert len(inp['old_packet_files'])==81 and len(inp['files'])==100
 for path,row in inp['files'].items():assert dg(ROOT/path)==row,path
 for path,row in inp['old_packet_files'].items():assert dg(ROOT/path)==row,path
 for canonical,provider in inp['canonical_before'].items():assert dg(P/provider)==inp['old_packet_files'][str((P/provider).relative_to(ROOT))]
 a=effective_audit();r=load(P/'requirements-r3.json');c=load(P/'cases-r3.json');f=load(P/'fixtures-r3.json');ad=load(P/'adoption-r3.json');validate(r,c,f,ad,a)
 mutations=[('old-clause',lambda r,c,f,ad:r[0].update(contract='changed')),('old-action',lambda r,c,f,ad:c[0].update(setup_and_action='changed')),('new-docoracle',lambda r,c,f,ad:c[154].update(documentary_expected='audible difference')),('current-actual',lambda r,c,f,ad:f['current_version_overlay']['actual_oracles'][0].update(expected='pass')),('inspection-not-Drive',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G25').update(setup_and_action='Inspect Filter Drive and Morph')),('drive-shaper-context',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G25').update(source_blocks=['operator:B151'])),('false-actual-pointer',lambda r,c,f,ad:ad['groups'][24]['historical_case_refs'][0].update(actual_action_pointer='/75/setup_and_action')),('joint-wrong-quote-pointer',lambda r,c,f,ad:(ad['groups'][24]['selected_source_contexts'][0].update(pointer='/blocks/396'),next(x for x in c if x.get('adoption_group')=='G25')['source_references'][0].update(pointer='/blocks/396'))),('no-positive',lambda r,c,f,ad:f['current_version_overlay'].update(positive_processing=['flags suffice'])),('no-paired-output',lambda r,c,f,ad:f['current_version_overlay']['paired_engine_voice_refinement'].update(predicate='Both enabled enough')),('all-pitch-degree',lambda r,c,f,ad:f['current_version_overlay']['unit_qualification'].update(current_scoped_predicate='All Octaves/Semitones/Cents are degrees')),('LFO2-macro-borrow',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G14').update(setup_and_action='Change LFO2 macros')),('Hold-no-Trigger-bridge',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G10').update(requirements=['REQ-SYN-DS-015'])),('group-complete',lambda r,c,f,ad:ad['groups'][0].update(complete=True)),('no-HiQuality-invocation',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G37').update(setup_and_action='Inspect Hi-Quality')),('missing-source-quote',lambda r,c,f,ad:next(x for x in c if x.get('adoption_group')=='G30')['source_references'][0].update(quote='title-only'))]
 rejected=[]
 for name,fn in mutations:
  rr,cc,ff,aa=deepcopy((r,c,f,ad));fn(rr,cc,ff,aa)
  try:validate(rr,cc,ff,aa,a)
  except (AssertionError,KeyError,IndexError):rejected.append(name)
  else:raise AssertionError('Unsafe fixture accepted '+name)
 for kind,canonical in [('spec','wiki/specs/synthesis-instruments.md'),('research','wiki/research/synthesis-instruments.md')]:
  text=(P/f'{kind}-r3.md').read_text();assert text==(ROOT/canonical).read_text() and text.startswith((P/f'{kind}-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1))
 spec=(P/'spec-r3.md').read_text();assert r[-1]['contract'] in spec # Historical table rendering is preserved by exact prefix, not raw JSON substring.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4;env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-inspected-pure-browser-definitions','exec'),env);assert {x['id'] for x in env['spec_rows'](P/'spec-r3.md',spec)}=={x['id'] for x in r}
 links=0;pending=[]
 for p in [ROOT/'wiki/specs/synthesis-instruments.md',ROOT/'wiki/research/synthesis-instruments.md',P/'README-r3.md']:
  for dest in re.findall(r'\]\(([^)\s]+)\)',p.read_text()):
   if re.match(r'(https?://|#|mailto:)',dest):continue
   target=(p.parent/dest.split('#')[0]).resolve()
   if not target.exists() and not (P/'manifest-author-r3.json').exists() and target==P/'manifest-author-r3.json':pending.append(str(target));continue
   assert target.exists(),(p,dest);links+=1
 current={p for p in P.rglob('*') if p.is_file()}
 for p in current:
  if str(p.relative_to(ROOT)) in inp['old_packet_files']:continue
  raw=p.read_bytes();assert raw.endswith(b'\n') and all(x.rstrip(b' \t')==x for x in raw.splitlines()),p
  if p.suffix=='.json':load(p)
 sealed=(P/'manifest-author-r3.json').exists()
 if sealed:
  m=load(P/'manifest-author-r3.json');assert set(m['payloads'])=={str(p.relative_to(ROOT)) for p in current if p.name!='manifest-author-r3.json'}
  for path,row in m['payloads'].items():assert dg(ROOT/path)==row,path
 assert before=={str(p):dg(p) for p in watched}
 print(json.dumps({'status':'pass' if sealed else 'pass-unsealed-preflight','sealed':sealed,'requirements':110,'cases':190,'old_files_exact':81,'old_requirement_objects_exact':109,'old_case_objects_exact':154,'new_doc_null_U':36,'current_actual_null_U':190,'old_doc_named':58,'old_doc_null':96,'partial_groups':37,'source_literal_fields':25,'unsafe_fixtures_rejected':rejected,'browser_exact_IDs':110,'links':links,'input_pins':100,'watched_unchanged':len(watched),'pending_declared_artifacts':pending,'writes':False,'complete':False,'scope':'Bounded current owner integrity only; independent ROOT semantic review pending. No oldtool/decode/runtime/coverage.'},indent=2))
if __name__=='__main__':main()
