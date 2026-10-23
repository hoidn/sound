"""Read-only retained seven-section audit checker. No vendor/old tools execute."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,sys,importlib.util,collections
A=Path(__file__).resolve().parent;P=A.parent;R=P.parents[2];D=P/'delay-reverb'
def j(p):return json.loads(p.read_text())
def path(s):return Path(s) if Path(s).is_absolute() else R/s
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,s):
 for k in s.strip('/').split('/') if s else []:v=v[int(k)] if isinstance(v,list) else v[k]
 return v

def shape(a,plan=None):
 if plan is None:plan=j(A/'plan.json')
 assert len(a['blocks'])==207 and len(a['assessments'])==207
 assert [x['block'] for x in a['assessments']]==[x['id'] for x in a['blocks']]
 assert len(a['proposals'])==26 and len(a['source_questions'])==7
 assert a['owner_requirements']==j(D/'requirements.json') and a['owner_cases']==j(D/'cases.json') and a['owner_fixtures']==j(D/'fixtures.json')
 assert len(a['owner_requirements'])==92 and len(a['owner_cases'])==149
 assert collections.Counter(c['provenance'] for c in a['owner_cases'])=={'D12':77,'Dpkg':7,'U':65}
 assert all(c['exact_target_expected'] is None and c['exact_target_applicability']=='unknown' and c['execution'].startswith('unexecuted') for c in a['owner_cases'])
 assert next(c for c in a['owner_cases'] if c['id']=='DR-ECHO-014')['expected'] is None
 assert all(a[k]==plan[k] for k in ['assessments','proposals','source_questions','common_future_prerequisites'])
 for i,x in enumerate(a['assessments']):
  b=a['blocks'][i];assert x['id']==f'DRA-A{i+1:03}' and x['quote']==b['text'] and x['source_pointer']==f'/blocks/{i}/text' and x['quote_sha256']==sha256(b['text'].encode()).hexdigest()
  for q in x['existing_requirement_refs']:
   assert q['catalog']==str((D/'requirements.json').relative_to(R)) and ptr(a['owner_requirements'],q['json_pointer'])['id']==q['id']
  for q in x['existing_case_refs']:
   assert q['catalog']==str((D/'cases.json').relative_to(R)) and ptr(a['owner_cases'],q['json_pointer'])['id']==q['id'] and q['action_pointer']==q['json_pointer']+'/action'
  assert set(x['open_groups'])=={g['id'] for g in a['proposals'] if b['id'] in g['source_blocks']}
 for x in a['assessments']+a['proposals']+a['source_questions']:
  assert all(x[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and x['target']=='U' and x['executed'] is False and x['complete'] is False and x['coverage_credit']==0
 for i,g in enumerate(a['proposals']):
  assert g['id']==f'DRA-G{i+1:02}' and g['new_normative_IDs']==[] and g['assessment_ids']==[x['id'] for x in a['assessments'] if x['block'] in g['source_blocks']]
 notes={x['block']:x['assessment'] for x in a['assessments']};g={x['id']:x for x in a['proposals']}
 assert 'research ONLY' in notes['FX:B403'] and next(x for x in a['assessments'] if x['block']=='FX:B403')['disposition']=='research-only-internal-outcome-U'
 assert '006actually' in notes['FX:B385'] and '007actually' in notes['FX:B386'] and '008actually selects all6waves' in notes['FX:B390']
 assert '009actualA/BFreeze/FreezeIn' in notes['FX:B539'] and 'CONVOLUTION output, not rawinputAlgo' in notes['FX:B522']
 assert '010actualnonzerofrozentail' in notes['FX:B819'] and '004actually admits A/B' in notes['FX:B317']
 assert '002actually Spin' in notes['FX:B806'] and '006actually Chorus' in notes['FX:B813'] and 'ALL3Smooth' in notes['FX:B816']
 assert 'EACHvoicewithmatching-channel positive' in notes['FX:B792'] and 'genuineIIoutput true' in notes['FX:B795']
 essential={2:('BOTH channel input identities','positive_baseline'),3:('Keep007ALL6/7enumeration','proposed_minimal_delta'),7:('BOTHisolatedLFO andchangingENV','proposed_minimal_delta'),10:('matching NONEMPTY input','proposed_future_positive_baseline'),14:('No grainsizeequation/tuning/RNGdistribution','limits'),18:('recognized validowned IR AND productive','proposed_future_positive_baseline'),19:('NONZEROtail','proposed_future_positive_baseline'),25:('BOTHIand EACHtestedII/III/IV/V','proposed_minimal_delta'),26:('BOTH channels/componentcontributions','proposed_future_positive_baseline')}
 for n,(token,k) in essential.items():
  if k=='positive_baseline':k='proposed_future_positive_baseline'
  assert token in g[f'DRA-G{n:02}'][k],(n,token)
 assert a['read_scope']['atomic_facets_claimed'] is False and a['read_scope']['whole_AudioEffects_chapter'] is False
 assert all(a['summary'][k]==0 for k in ['new_normative_IDs','new_cases','new_documentary_nonnull','actual_nonnull','executed','coverage_credit','complete_topics'])
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no write/decode/replay mode'
 ins=j(A/'inputs.json');a=j(A/'audit.json');watch={path(x['path']) for x in ins['files']}|{p for p in A.iterdir() if p.is_file()};before={str(p):dg(p) for p in watch}
 for x in ins['files']:assert dg(path(x['path']))=={k:x[k] for k in ['bytes','sha256']},x['path']
 assert len(ins['files'])==82
 assert dg(D/'manifest-author-r2.json')['sha256']=='90b2a69eca5ffbf5a86f0bce0142abdead4326fe658d5a6e36730650bb216866'
 assert dg(D/'archive-r1/manifest-author-r1.json')['sha256']=='560dc1d7f8df587ac138b3bf54978cd76d004b899bb65d543dc4a6cd61609654'
 for parent,name,count in [(D,'manifest-author-r2.json',33),(D/'archive-r1','manifest-author-r1.json',32)]:
  mf=j(parent/name);assert len(mf['files'])==count
  for name,expected in mf['files'].items():assert dg(parent/name)==expected,name
 for q in ins['canonical_providers']:assert dg(path(q['provider']['path']))=={k:q['provider'][k] for k in ['bytes','sha256']}
 assert a['canonical_providers']==ins['canonical_providers'] and a['source']==ins['source'] and a['source']['capture_utc'] is None
 shape(a)
 parser=P/'clip-view-source-audit/source_parser.py';assert dg(parser)['sha256']=='648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'
 spec=importlib.util.spec_from_file_location('inspected_pure_parser',parser);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 raw=path(ins['source']['path']).read_text();blocks,res=m.extract(raw,'FX');assert len(blocks)==1137
 anchors=set(ins['selection']['h2_anchors'])
 def h2(b):return next((h['anchor'] for h in b.get('heading_context',[]) if h['level']==2),None)
 selected=[b for b in blocks if h2(b) in anchors];anchor_to_h2={h['anchor']:h2(b) for b in blocks for h in b['heading_context'] if h.get('anchor')};resources=[r for r in res if anchor_to_h2.get(r.get('heading_context_anchor')) in anchors]
 assert selected==a['blocks'] and resources==a['resources'] and sum(len(b.get('cells',[])) for b in selected)==0
 assert collections.Counter(b['kind'] for b in selected)=={'p':145,'li':30,'h2':7,'h3':18,'h4':7}
 assert collections.Counter(r['kind'] for r in resources)=={'image':22,'caption':22,'link':4}
 counts=collections.Counter();local={}
 for b in selected:
  s=h2(b);counts[s]+=1;local[b['id']]=f'{s}:B{counts[s]:03}';old=j(D/f'manual-{s}-blocks.json')[counts[s]-1];assert old['text']==b['text']
  assert raw[b['raw_start']:b['raw_end']]==b['raw_html']
 assert local==a['local_owner_block_crosswalk']
 # Small retained parser omission fixture, including inlinekey text, list, tablecells and literal image.
 fb,fr=m.extract('<div id="chapter_content"><h2 id="delay">Delay</h2><p>Press <kbd>Q</kbd>.</p><ul><li>A</li></ul><table><tr><td>X</td><td>Y</td></tr></table><img alt="" src="x"></div>','FIX')
 assert [b['kind'] for b in fb]==['h2','p','li','tr'] and fb[1]['text']=='Press Q.' and [c['text'] for c in fb[3]['cells']]==['X','Y'] and len(fr)==1
 rejected=[]
 for name,change in [
 ('omit-list',lambda b:b['assessments'].pop(15)),('wrong-action-pointer',lambda b:next(x for x in b['assessments'] if x['existing_case_refs'])['existing_case_refs'][0].update(action_pointer='/0/setup')),
 ('invent-output',lambda b:b['proposals'][0].update(actual_expected='pass')),('internal-shutdown-oracle',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B403').update(documentary_expected='CPUzero')),
 ('Serial-raw-Algorithm',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B522').update(assessment='Serial0/100 is raw Algorithm')),
 ('erase-true-Delay-Freeze',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B317').update(assessment='No input-admission action exists')),
 ('erase-true-Echo-wave-actions',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B390').update(assessment='Allsix only enumerated')),
 ('erase-true-Reverb-Spin',lambda b:next(x for x in b['assessments'] if x['block']=='FX:B806').update(assessment='Spin only label')),
 ('one-voice-before-loss',lambda b:b['proposals'][24].update(proposed_minimal_delta=b['proposals'][24]['proposed_minimal_delta'].replace('BOTHIand EACHtestedII/III/IV/V','one enabled flag'))),
 ('no-tail-before-Freeze',lambda b:b['proposals'][18].update(proposed_future_positive_baseline=b['proposals'][18]['proposed_future_positive_baseline'].replace('NONZEROtail','Freeze flag'))),
 ('IRfilename-proves-recognition',lambda b:b['proposals'][17].update(proposed_future_positive_baseline=b['proposals'][17]['proposed_future_positive_baseline'].replace('recognized validowned IR AND productive','filename'))),
 ('RNG-statistical-pass',lambda b:b['proposals'][13].update(documentary_expected='alwaysdistinct')),
 ('file-runtime-promotion',lambda b:next(c for c in b['owner_cases'] if c['provenance']=='Dpkg').update(provenance='S')),
 ('source-topic-complete',lambda b:b['summary'].update(complete_topics=7))]:
  bad=deepcopy(a);change(bad)
  try:shape(bad,bad)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 for p in A.iterdir():
  if p.is_file():assert all(l.rstrip()==l for l in p.read_text().splitlines()),p.name
 seal=A/'manifest.json'
 if seal.exists():
  mf=j(seal)
  for q in mf['files']:assert dg(path(q['path']))=={k:q[k] for k in ['bytes','sha256']}
  assert {str(p.relative_to(R)) for p in A.iterdir() if p.is_file()}=={q['path'] for q in mf['files']}|{str(seal.relative_to(R))}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=seal.exists(),summary=a['summary'],immutable_pins=len(ins['files']),canonical_asof_providers=2,source_local_crosswalk=207,negative_fixtures=rejected,parser_inline_list_table_resource_fixture=True,retained_true_subsets='Delay/Echo/Reverb/Hybrid Freeze and modulation; Resonatorsmatchingchannel andII-survival; all149oldrecords unchanged',watched_paths=len(watch),all_unchanged=True,writes=False,oldmain_imports_decodes_runtime=False),indent=2))
if __name__=='__main__':main()
