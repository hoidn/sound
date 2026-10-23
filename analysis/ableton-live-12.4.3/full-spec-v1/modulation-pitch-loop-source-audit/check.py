"""Read-only ten-section retained-source audit. No old owner tool or vendor code executes."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,sys,importlib.util,collections,re
A=Path(__file__).resolve().parent;P=A.parent;R=P.parents[2];D=P/'modulation-pitch-loop'
def j(p):return json.loads(p.read_text())
def path(s):return Path(s) if Path(s).is_absolute() else R/s
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,s):
 for k in s.strip('/').split('/') if s else []:v=v[int(k)] if isinstance(v,list) else v[k]
 return v

def shape(a,plan=None):
 if plan is None:plan=j(A/'plan.json')
 assert len(a['blocks'])==len(a['assessments'])==332 and len(a['proposals'])==22 and len(a['source_questions'])==8
 assert [x['block'] for x in a['assessments']]==[x['id'] for x in a['blocks']]
 assert a['owner_requirements']==j(D/'requirements.json') and a['owner_cases']==j(D/'cases.json') and a['owner_fixtures']==j(D/'stimulus-recipes.json')
 assert len(a['owner_requirements'])==106 and len(a['owner_cases'])==186
 assert collections.Counter(r['strength'] for r in a['owner_requirements'])=={'D12':96,'U':10}
 assert all(c['expected'] is None and c['target_grade']=='U' and not c['executed'] for c in a['owner_cases'])
 assert collections.Counter(c['kind'] for c in a['owner_cases'])==a['summary']['case_kinds']
 assert all(a[k]==plan[k] for k in ['assessments','proposals','source_questions','common_future_prerequisites'])
 reqids={r['id'] for r in a['owner_requirements']}
 for i,x in enumerate(a['assessments']):
  b=a['blocks'][i];assert x['id']==f'MPLA-A{i+1:03}' and x['quote']==b['text'] and x['source_pointer']==f'/blocks/{i}/text' and x['quote_sha256']==sha256(b['text'].encode()).hexdigest()
  for q in x['existing_requirement_refs']:
   assert q['catalog']==str((D/'requirements.json').relative_to(R)) and ptr(a['owner_requirements'],q['json_pointer'])['id']==q['id']
  for q in x['existing_case_refs']:
   assert q['catalog']==str((D/'cases.json').relative_to(R)) and ptr(a['owner_cases'],q['json_pointer'])['id']==q['id'] and q['action_pointer']==q['json_pointer']+'/setup_and_action'
  assert set(x['open_groups'])=={g['id'] for g in a['proposals'] if b['id'] in g['source_blocks']}
 for x in a['assessments']+a['proposals']+a['source_questions']:
  assert all(x[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and x['target']=='U' and x['executed'] is False and x['complete'] is False and x['coverage_credit']==0
 for i,g in enumerate(a['proposals']):
  assert g['id']==f'MPLA-G{i+1:02}' and g['new_normative_IDs']==[] and set(g['route_to_existing_requirements'])<=reqids
  assert g['assessment_ids']==[x['id'] for x in a['assessments'] if x['block'] in g['source_blocks']]
 notes={x['block']:x['assessment'] for x in a['assessments']};groups={g['id']:g for g in a['proposals']}
 retained={'FX:B100':'does NOT actually adjust Phase180','FX:B141':'no held-first note-off','FX:B219':'does not actually adjust Rate','FX:B610':'actually compares Clear Overdub/running versus Play/running','FX:B611':'actually records A, completesB, addsC','FX:B628':'actually divides while BOTH first/second halves','FX:B644':'BOTH InsertLooper taps true','FX:B746':'actually Blend0/1 true','FX:B758':'actual DutyCycle sweep and deterministic positive baseline true','FX:B940':'raw source says Hertz','FX:B978':'inspects Gate eligibility only','FX:B992':'actually ChorusRate0/nonzeroRate true','FX:B1013':'QUALIFIED by Frz>Dly','FX:B1023':'XFade ms/percentage ambiguity U','FX:B1101':'research ONLY','FX:B1118':'BOTH channels of BOTH signals independently productive','FX:B1129':'BOTHarm action not explicitly performed'}
 for block,token in retained.items():assert token in notes[block],(block,token)
 essential={3:('BOTH independently received distinguishable notes','proposed_future_positive_baseline'),4:('Each independent source-target path','proposed_future_positive_baseline'),6:('BOTH Rate dial AND vertical display drag','proposed_minimal_delta'),7:('BOTH independent mainLFO and LFO2','proposed_future_positive_baseline'),9:('before zeroSpread contrast','proposed_minimal_delta'),11:('overrides default Poly16','proposed_future_positive_baseline'),14:('recognized NONEMPTY notes','proposed_minimal_delta'),15:('Genuine nonzero frozen audio BEFORE','proposed_future_positive_baseline'),16:('Dly>Frz actual processed/capture history','proposed_minimal_delta'),18:('BOTH Range sliders/BW','proposed_minimal_delta'),19:('BOTH channels of EACH','proposed_future_positive_baseline'),20:('finite traversal liveness','limits'),21:('genuine nonzero observed loop BEFORE Clear','proposed_future_positive_baseline'),22:('actual NONZERO loop AND productive inserted-effect return','proposed_future_positive_baseline')}
 for n,(token,k) in essential.items():assert token in groups[f'MPLA-G{n:02}'][k],(n,token)
 assert a['spectral_association_reconciliation']==j(D/'association-reconciliation.json')
 rec={r['corrected_inventory_surface']:r for r in a['spectral_association_reconciliation']};assert rec['SURF-DEVICE-SPECTRAL-RESONATOR']['class']=='Transmute' and rec['SURF-DEVICE-SPECTRAL-RESONATOR']['schema_line']==8118 and rec['SURF-DEVICE-SPECTRAL-TIME']['class']=='Spectral' and rec['SURF-DEVICE-SPECTRAL-TIME']['schema_line']==7423
 assert a['read_scope']['atomic_facets_claimed'] is False and a['read_scope']['whole_AudioEffects_chapter'] is False and a['read_scope']['external_companion_full_chapters']==[]
 assert all(a['summary'][k]==0 for k in ['new_normative_IDs','new_cases','new_documentary_nonnull','actual_nonnull','executed','coverage_credit','complete_topics'])
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no write/decode/replay mode'
 ins=j(A/'inputs.json');a=j(A/'audit.json');watch={path(x['path']) for x in ins['files']}|{p for p in A.iterdir() if p.is_file()};before={str(p):dg(p) for p in watch}
 assert len(ins['files'])==122 and ins['prior_packet_files']==107
 for q in ins['files']:assert dg(path(q['path']))=={k:q[k] for k in ['bytes','sha256']},q['path']
 assert dg(D/'manifest-author-r2.json')['sha256']=='a1fb912a505dc8546f3ca17fd12d8616eb62fdf2e5dc0e685ed6ce0b72d15ab8'
 assert dg(D/'archive-r1/manifest-author-r1.json')['sha256']=='f68b16954c3b95fc7e9ac288d78ad10651a0fd0217271ccb5493bf61f4e044a5'
 for parent,name,count in [(D,'manifest-author-r2.json',51),(D/'archive-r1','manifest-author-r1.json',49)]:
  mf=j(parent/name);assert len(mf['files'])==count
  for name,expected in mf['files'].items():assert dg(parent/name)==expected,name
 for q in ins['canonical_providers']:assert dg(path(q['provider']['path']))=={k:q['provider'][k] for k in ['bytes','sha256']}
 assert a['canonical_providers']==ins['canonical_providers'] and a['source']==ins['source'] and a['source']['capture_utc'] is None
 shape(a)
 # Exact Browser-style bare first cells/headings from immutable as-of spec, never future wiki gate.
 spec=(D/'spec-r2.md').read_text();ids=set(re.findall(r'^\|\s*(REQ-[A-Z0-9-]+)\s*\|',spec,re.M))|set(re.findall(r'^###\s+(REQ-[A-Z0-9-]+)(?:\s|$)',spec,re.M))
 assert ids=={r['id'] for r in a['owner_requirements']} and len(ids)==106
 assert all(r['contract'] in spec for r in a['owner_requirements'] if r['strength']=='D12')
 assert spec.count('**U.** The device-specific lifecycle matrix below is required and ungraded; control/preset presence does not close those outcomes.')==10
 parser=P/'clip-view-source-audit/source_parser.py';assert dg(parser)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
 loader=importlib.util.spec_from_file_location('inspected_pure_parser',parser);m=importlib.util.module_from_spec(loader);loader.loader.exec_module(m)
 raw=path(ins['source']['path']).read_text();blocks,res=m.extract(raw,'FX');assert len(blocks)==1137
 anchors=set(ins['selection']['h2_anchors'])
 def h2(b):return next((h['anchor'] for h in b.get('heading_context',[]) if h['level']==2),None)
 selected=[b for b in blocks if h2(b) in anchors]
 # Use the heading at that exact source position, avoiding h1 overwrite by descendant contexts.
 anchor_to_h2={}
 for b in blocks:
  if b['kind'] in ['h2','h3','h4','h5','h6']:anchor_to_h2[b['attributes'].get('id')]=h2(b)
 resources=[dict(r,inspection='literal metadata/caption/link role only; pixels/destination content uninspected') for r in res if anchor_to_h2.get(r.get('heading_context_anchor')) in anchors]
 assert selected==a['blocks'] and resources==a['resources'] and sum(len(b.get('cells',[])) for b in selected)==0
 assert collections.Counter(b['kind'] for b in selected)=={'p':231,'li':60,'h2':10,'h3':25,'h4':6}
 assert collections.Counter(r['kind'] for r in resources)=={'image':44,'caption':43,'link':18}
 counts=collections.Counter();local={}
 for b in selected:
  s=h2(b);counts[s]+=1;local[b['id']]=f'{s}:B{counts[s]:03}';old=j(D/f'manual-{s}-blocks.json')[counts[s]-1];assert old['text']==b['text']
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 assert local==a['local_owner_block_crosswalk'] and dict(counts)==ins['selection']['per_section']
 fb,fr=m.extract('<div id="chapter_content"><h2 id="x">X</h2><p>Press <kbd>Q</kbd>.</p><ul><li>A</li></ul><table><tr><td>X</td><td>Y</td></tr></table><img alt="" src="x"><h2 id="outside">Outside</h2><p>Notselected</p></div>','FIX')
 assert [b['kind'] for b in fb]==['h2','p','li','tr','h2','p'] and fb[1]['text']=='Press Q.' and [c['text'] for c in fb[3]['cells']]==['X','Y'] and len(fr)==1 and len([b for b in fb if h2(b)=='x'])==4
 rejected=[]
 for name,change in [
 ('omit-list',lambda b:b['assessments'].pop(66)),('wrong-action-pointer',lambda b:next(x for x in b['assessments'] if x['existing_case_refs'])['existing_case_refs'][0].update(action_pointer='/0/title')),
 ('invent-output',lambda b:b['proposals'][0].update(actual_expected='pass')),('Rate-inspection-promoted',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B219').update(assessment='CE006 actually drags Rate')),
 ('erase-true-Blend',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B746').update(assessment='PF001 only labels')),
 ('erase-true-Looperhalves',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B628').update(assessment='LP009 retains firsthalf only')),
 ('unconditional-freezerfeedsdelay',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B1013').update(assessment='always feeds delay')),
 ('repair-Shifter-unit',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B940').update(assessment='Delay in milliseconds proven')),
 ('invent-XFadeequation',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B1023').update(assessment='XFade percent times Interval')),
 ('one-modsource-before-loss',lambda b:b['proposals'][6].update(proposed_future_positive_baseline='LFO2 enabled flag')),
 ('freeze-flag-as-tail',lambda b:b['proposals'][14].update(proposed_future_positive_baseline='Freeze flag On')),
 ('loop-flag-before-clear',lambda b:b['proposals'][20].update(proposed_future_positive_baseline='Loop indicator On')),
 ('conversion-flag-as-MIDI-output',lambda b:b['proposals'][13].update(proposed_minimal_delta='MIDI generation completion flag is enough')),
 ('only-one-Vocoder-channel',lambda b:b['proposals'][18].update(proposed_future_positive_baseline='onechannel tested')),
 ('spectral-alias-swap',lambda b:b.update(spectral_association_reconciliation={})),('random-statistical-pass',lambda b:b['proposals'][19].update(documentary_expected='alwaysdistinctwithin32')),
 ('source-topic-complete',lambda b:b['summary'].update(complete_topics=10))]:
  bad=deepcopy(a);change(bad)
  try:shape(bad,bad)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe joint plan/audit mutation accepted '+name)
 for p in A.iterdir():
  if p.is_file():assert all(l.rstrip()==l for l in p.read_text().splitlines()),p.name
 seal=A/'manifest.json'
 if seal.exists():
  mf=j(seal);assert len(mf['files'])==5
  for q in mf['files']:assert dg(path(q['path']))=={k:q[k] for k in ['bytes','sha256']}
  assert {str(p.relative_to(R)) for p in A.iterdir() if p.is_file()}=={q['path'] for q in mf['files']}|{str(seal.relative_to(R))}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],immutable_pins=len(ins['files']),prior_packet_files=107,canonical_asof_providers=2,browser_IDs=106,source_local_crosswalk=332,literal_resources=105,negative_fixtures=rejected,parser_inline_list_table_resource_scope_fixture=True,watched_paths=len(watch),all_unchanged=True,writes=False,oldmain_imports_decodes_runtime=False),indent=2))
if __name__=='__main__':main()
