"""Finite source-only Automation/Clip Envelopes audit; --check only, stdout/no writes.
Only own stdlib and pinned inspected pure analyst HTML parser; no old owner tool.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'automation-workflows';PARSER=P.parent/'midi-editing-source-audit/source_parser.py'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def ptr(v,p):
 for k in p.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~')
  if isinstance(v,list):assert re.fullmatch(r'0|[1-9][0-9]*',k);v=v[int(k)]
  else:v=v[k]
 return v
STATUS={'R':'represented-bounded-source-clause-and-actual-case-subset','X':'mixed-represented-subset-and-action-qualifier-gap','G':'missing-selected-owner-role-or-action','U':'documented-outcome-or-context-U','M':'research-or-optional-guidance','O':'selected-other-owner-context','E':'editorial-or-structural'}
CAP={'AUT':{5:[1],14:[2],18:[2],20:[2],22:[3],27:[3],30:[5],32:[5],36:[5],39:[8],41:[1],44:[11],47:[11],49:[12],52:[14],54:[14],56:[14],58:[15],60:[16],62:[16],64:[17],66:[18],73:[22],76:[23],79:[23],81:[23],83:[24],85:[24],87:[25],93:[27],95:[29],98:[21],101:[31],103:[31],105:[32],110:[35],113:[36]},'CE':{3:[38],15:[43],17:[44],19:[45],23:[39],25:[39],27:[46],29:[47],32:[50],34:[51,52],36:[52],41:[54]}}

def build(plan=None):
 plan=load(P/'plan.json') if plan is None else plan;extract=runpy.run_path(str(PARSER))['extract'];sources=load(K/'sources.json');blocks=[];resources=[];cases=load(K/'cases.json')
 for s,prefix in zip(sources,['AUT','CE']):
  b,r=extract((K/s['path']).read_text(),prefix);blocks+=b
  for n,x in enumerate(r,1):
   x.update(id=f'{prefix}:R{n:03}',source_id=prefix,pixels_or_destination_inspected=False)
   if x['kind']=='caption':
    nums=CAP[prefix][n];x.update(disposition='G' if x['id']=='CE:R029' else 'R',assessment='Literal caption text reconciled with related bounded body/action roles, not inspected image content or complete outcomes.',related_case_indices=nums,proposal_groups=['G14'] if x['id']=='CE:R029' else (['G09'] if x['id']=='AUT:R103' else ['G16'] if x['id']=='CE:R034' else []))
    if x['id']=='CE:R029':x.update(plan['resource_notes'][x['id']])
    if x['id'] in ['CE:R019','CE:R034','CE:R036']:x['disposition']='M' if x['id']=='CE:R019' else 'U';x['assessment']+=' Offset/fade/start timing and output remain source context/null, not a measured result.'
    if x['id']=='CE:R003':x.update(disposition='O',assessment='Literal Session Clip Envelopes tab caption; selected current ClipView008/CV008 actually switches tabs/routes. AW038 owns category subset only; no icon pixels inspected.')
    if x['id'] in ['CE:R015','CE:R017']:x.update(disposition='X',proposal_groups=['G11' if x['id']=='CE:R015' else 'G12'],assessment='Literal transposition-step/ramp or sample-volume shape caption. Existing043/044 sound/fine-edit/attenuation subsets do not explicitly invoke all Draw/method entries; proposed G11/G12 retain that distinction. No figure waveform/pixel/audio result.')
   else:x.update(disposition='uninspected-image-pixels' if x['kind']=='image' else 'uninspected-linked-destination',assessment='All literal attributes/text/URL and raw starttag retained/read. Pixels or linked contents not inspected; filenames/empty alt do not create an observable control law.',related_case_indices=[],proposal_groups=[])
   x['case_refs']=[{'catalog':'owner_cases','json_pointer':f'/{ci-1}','id':cases[ci-1]['id'],'actual_action_pointer':f'/{ci-1}/setup_and_action'} for ci in x['related_case_indices']]
   x.update(documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0);resources.append(x)
 req=load(K/'requirements.json');cases=load(K/'cases.json');assess=[];routes={}
 for bi,b in enumerate(blocks):
  local=('automation' if b['source_id']=='AUT' else 'clip-envelopes')+':'+b['id'].split(':')[1];routes[b['id']]={'owner_local_block':local,'actual_paragraph_anchor':b['attributes'].get('id'),'heading_ancestry':b['heading_context'],'source_id':b['source_id']}
  j={'disposition':'E','cases':[],'proposal_groups':[],'assessment':'Literal actual numbered heading/ancestry only; no behavior/leaf completeness from title.'} if b['kind'].startswith('h') else plan['judgments'][b['id']]
  ri=[i for i,r in enumerate(req) if local in r['source_blocks'] or r['id'] in {rid for ci in j['cases'] for rid in cases[ci-1]['requirements']}]
  assess.append({'id':f'AWS-A{bi+1:03}','block':b['id'],'block_pointer':f'/blocks/{bi}','local_block':local,'quote':b['text'],'quote_sha256':sha256(b['text'].encode()).hexdigest(),'full_qualifier_context_pointer':f'/blocks/{bi}/text','scope':'WHOLE qualified paragraph/list or heading, not atomic claim count or complete source coverage. Related refs support only named assessment subsets.','disposition':STATUS[j['disposition']],'assessment':j['assessment'],'proposal_groups':j['proposal_groups'],'requirement_refs':[{'catalog':'owner_requirements','json_pointer':f'/{i}','id':req[i]['id'],'scoped_predicate_pointer':f'/{i}/contract'} for i in ri],'case_refs':[{'catalog':'owner_cases','json_pointer':f'/{n-1}','id':cases[n-1]['id'],'actual_action_pointer':f'/{n-1}/setup_and_action'} for n in j['cases']],'documentary_expected':None,'documentary_comparison':None,'actual_expected':None,'actual_comparison':None,'target':'U','executed':False,'complete':False,'coverage_credit':0})
 props=deepcopy(plan['proposals'])
 for g in props:g['assessment_ids']=[x['id'] for x in assess if g['id'] in x['proposal_groups']];g['resource_ids']=[x['id'] for x in resources if g['id'] in x['proposal_groups']]
 qs=deepcopy(plan['source_questions'])
 for q in qs:q.update(quotes=[{'block':b['id'],'json_pointer':f'/blocks/{i}/text','quote':b['text']} for i,b in enumerate(blocks) if b['id'] in q['blocks']],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0)
 reverse={key:[{'id':r['id'],'json_pointer':f'/{key}/{i}','related_assessment_ids':[x['id'] for x in assess if any(z['id']==r['id'] for z in x[field])],'complete':False,'coverage_credit':0} for i,r in enumerate(rows)] for key,rows,field in [('owner_requirements',req,'requirement_refs'),('owner_cases',cases,'case_refs')]}
 inputs=load(P/'inputs.json');summary={'source_blocks':192,'per_chapter':{'AUT':114,'CE':78},'block_kinds':dict(Counter(b['kind'] for b in blocks)),'manual_whole_text_judgments':151,'assessments':len(assess),'dispositions':dict(Counter(x['disposition'] for x in assess)),'literal_resources':154,'resource_kinds':dict(Counter(x['kind'] for x in resources)),'requirements':62,'cases':76,'visible_documentary_cases':44,'null_documentary_cases':32,'proposals':19,'source_questions':5,'input_pins':len(inputs['files']),'old_owner_files':18,'historical_authorities':13,'released_payloads':26,'selected_other_owner_records':14,'new_normative_IDs':0,'new_cases':0,'new_documentary_nonnull':0,'actual_nonnull':0,'executed':0,'coverage_credit':0,'complete_topics':0}
 return {'role':'Analyst source-only WHOLE-context audit; finite proposals are not normative adoption, atomic completeness or runtime coverage.','source':sources,'scope':plan['read_scope'],'blocks':blocks,'resources':resources,'block_routes':routes,'owner_requirements':req,'owner_cases':cases,'owner_fixtures':load(K/'fixtures.json'),'owner_asof':{'manifest':'automation-workflows/manifest-author-r1.json','sha256':'5b7fc430a608c7fddbafd7a0fd20b0d09dc8b9d4002fbbb85c2a26d4560c7638','canonical_providers':'inputs.json#/canonical_snapshots','policy':'R1freeze and historicalpendingprose preserved; actual independent priorreview approvedpartial. No live historical pin gate.'},'assessments':assess,'proposals':props,'source_questions':qs,'common_future_prerequisites':plan['common_future_prerequisites'],'selected_other_owner_records':inputs['selected_other_owner_records'],'case_scope':[{'id':c['id'],'case_pointer':f'/owner_cases/{i}','documentary_oracle_nonnull':c['documentary_expected'] is not None,'audit_actual_expected':None,'audit_actual_comparison':None,'target':'U','executed':False,'complete':False} for i,c in enumerate(cases)],'reverse_catalogs':reverse,'summary':summary}

def guards(a,plan):
 assert len(a['blocks'])==len(a['assessments'])==192 and len(a['resources'])==154
 assert Counter(b['kind'] for b in a['blocks'])=={'h1':2,'h2':14,'h3':24,'h4':1,'p':138,'li':13}
 assert Counter(r['kind'] for r in a['resources'])=={'image':50,'caption':49,'link':55}
 assert set(plan['judgments'])=={b['id'] for b in a['blocks'] if not b['kind'].startswith('h')}
 req=load(K/'requirements.json');cases=load(K/'cases.json');assert a['owner_requirements']==req and a['owner_cases']==cases and a['owner_fixtures']==load(K/'fixtures.json')
 for i,x in enumerate(a['assessments']):
  b=ptr(a,x['block_pointer']);assert b['id']==x['block'] and x['quote']==b['text'] and x['quote_sha256']==sha256(b['text'].encode()).hexdigest() and ptr(a,x['full_qualifier_context_pointer'])==b['text'];assert i==int(x['block_pointer'].split('/')[-1])
  for ref in x['requirement_refs']+x['case_refs']:
   rows=a[ref['catalog']];r=ptr(rows,ref['json_pointer']);assert r['id']==ref['id'];field='contract' if ref['catalog']=='owner_requirements' else 'setup_and_action';bp=ref.get('scoped_predicate_pointer',ref.get('actual_action_pointer'));assert ptr(rows,bp)==r[field] and r[field]
  assert all(x[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and x['target']=='U' and x['executed'] is x['complete'] is False and x['coverage_credit']==0
 # Fixed semantic boundaries reject jointly edited plan+derived association claims.
 by={x['block']:x for x in a['assessments']}
 expected={'AUT:B036':('X',['AW-012','AW-013'],'G02'),'AUT:B044':('X',['AW-015'],'G03'),'AUT:B048':('X',['AW-017'],'G04'),'AUT:B083':('X',['AW-027'],'G06'),'AUT:B085':('X',['AW-028'],'G07'),'AUT:B088':('X',['AW-030'],'G08'),'AUT:B092':('X',['AW-031'],'G09'),'CE:B044':('R',['AW-046'],None),'CE:B052':('X',['AW-050'],'G15'),'CE:B068':('X',['AW-052','AW-053'],'G17'),'CE:B036':('O',['AW-U-REPLACEMENT'],'G19'),'CE:B076':('X',['AW-024','AW-031','AW-053'],'G18'),'CE:B078':('R',['AW-054'],None),'CE:B004':('O',['AW-038'],None)}
 for block,(st,cs,g) in expected.items():
  row=by[block];assert row['disposition']==STATUS[st] and [r['id'] for r in row['case_refs']]==cs
  if g:assert g in row['proposal_groups']
 assert 'does not explicitly' in by['AUT:B088']['assessment'] and 'butnot explicitMIDI Ctrl/Controlchooser' in by['CE:B052']['assessment']
 assert 'no explicitBrowserdrop' in by['CE:B020']['assessment'] and by['AUT:B020']['disposition']==STATUS['U']
 assert len(a['proposals'])==19 and len(a['source_questions'])==5 and [q['id'] for q in a['source_questions']][:3]==['Q-AW-001','Q-AW-002','Q-AW-003']
 groups={g['id']:g for g in a['proposals']}
 for i,g in enumerate(a['proposals']):
  assert g['id']==f'G{i+1:02}' and g['assessment_ids']==[x['id'] for x in a['assessments'] if g['id'] in x['proposal_groups']] and g['resource_ids']==[x['id'] for x in a['resources'] if g['id'] in x['proposal_groups']]
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and g['target']=='U' and g['executed'] is g['complete'] is False and not g['new_normative_IDs'] and g['coverage_credit']==0
  assert g['proposed_minimal_delta'] and g['proposed_future_positive_baseline'] and g['limits']
  for ident in g['source_blocks']:assert ident in by or any(r['id']==ident for r in a['resources'])
 required={'G01':['BOTH','received-note','working note-recording positive'],'G06':['UI-only','working point/segment drag baseline'],'G11':['NONEMPTY','NONZERO','genuinely','nonmuted'],'G13':['NONEMPTY','NONZERO','positive','nonmuted'],'G14':['BOTH independent','NONZERO send','nonmuted wet return'],'G15':['independently accepted','NONZERO','genuine receiver positive'],'G16':['NONEMPTY','genuine independent','nonmuted'],'G17':['NONEMPTY sample AND envelope/target','not two Loop flags']}
 for ident,tokens in required.items():assert all(t in groups[ident]['proposed_future_positive_baseline'] for t in tokens),ident
 assert all(t in groups['G06']['proposed_minimal_delta'] for t in ['dragging near','Shift-click','release Shift','fine vertical','horizontal segment'])
 assert all(t in groups['G08']['proposed_minimal_delta'] for t in ['Edit Value','type','point and segment'])
 assert 'Optional source advice' in groups['G11']['proposed_minimal_delta'] and 'no response guarantee' in groups['G11']['proposed_minimal_delta'] # no DSP result assigned
 assert 'G14' in next(r for r in a['resources'] if r['id']=='CE:R029')['proposal_groups'] and 'blue' in next(r for r in a['resources'] if r['id']=='CE:R029')['text'].lower()
 for r in a['resources']:
  assert not r['pixels_or_destination_inspected'] and all(r[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and not r['complete'] and not r['executed']
  for ref in r['case_refs']:assert ptr(a['owner_cases'],ref['json_pointer'])['id']==ref['id'] and ptr(a['owner_cases'],ref['actual_action_pointer'])==ptr(a['owner_cases'],ref['json_pointer'])['setup_and_action']
 assert a['common_future_prerequisites']==plan['common_future_prerequisites'] and 'NONEMPTY' in a['common_future_prerequisites'][2] and 'BOTH' in a['common_future_prerequisites'][3] and 'running transport' in a['common_future_prerequisites'][4]
 for q in a['source_questions']:
  for quote in q['quotes']:assert ptr(a,quote['json_pointer'])==quote['quote']
  assert all(q[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison'])
 for x in a['case_scope']:
  c=ptr(a,x['case_pointer']);assert c['id']==x['id'] and x['audit_actual_expected'] is x['audit_actual_comparison'] is None and not x['executed']
 for c in cases:assert c['expected'] is c['comparison'] is None and c['target_grade']=='U' and c['executed'] is False
 assert len(cases)==76 and len(req)==62 and sum(c['documentary_expected'] is not None for c in cases)==44
 for key,field in [('owner_requirements','requirement_refs'),('owner_cases','case_refs')]:
  assert len(a['reverse_catalogs'][key])==len(a[key])
  for x in a['reverse_catalogs'][key]:assert ptr(a,x['json_pointer'])['id']==x['id'] and x['related_assessment_ids']==[j['id'] for j in a['assessments'] if any(r['id']==x['id'] for r in j[field])]

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported writes refused before inputs'
 packet={str(p):dg(p) for p in P.rglob('*') if p.is_file()};inp=load(P/'inputs.json');before={x['path']:dg(ROOT/x['path']) for x in inp['files']}
 assert len(inp['files'])==62 and len(inp['old_owner_files'])==18
 for x in inp['files']:assert before[x['path']]=={k:x[k] for k in ['bytes','sha256']},x['path']
 assert dg(PARSER)=={'bytes':3428,'sha256':'648bb1ebce827d136ab6074d6b80fe32475534d87d57a367e9de9aa9fc8fdad8'}
 old=load(K/'manifest-author-r1.json');assert len(old['files'])==17
 for name,row in old['files'].items():assert dg(K/name)==row
 for x in inp['canonical_snapshots']:assert dg(ROOT/x['provider'])=={k:x[k] for k in ['bytes','sha256']}
 for x in inp['historical_authority_resolutions']:
  pin=x['original_historical_pin'];identity=dg(ROOT/x['provider']) if 'provider' in x else {'bytes':len(x['embedded_asof_text'].encode()),'sha256':sha256(x['embedded_asof_text'].encode()).hexdigest()};assert identity=={k:pin[k] for k in ['bytes','sha256']}
 for x in inp['selected_other_owner_records']:assert ptr(load(ROOT/x['path']),x['json_pointer'])==x['record'] and x['record']['id']==x['id']
 plan=load(P/'plan.json');a=build(plan);guards(a,plan);assert a==load(P/'audit.json')
 for prefix,local in [('AUT','automation'),('CE','clip-envelopes')]:
  oldblocks=load(K/f'manual-{local}-blocks.json');new=[b for b in a['blocks'] if b['source_id']==prefix];assert len(oldblocks)==len(new)
  for ob,nb in zip(oldblocks,new):assert all(ob[k]==nb[k] for k in ['kind','text','html_line']) and ob['locator']==a['block_routes'][nb['id']]['owner_local_block']
 raw={prefix:(K/src['path']).read_text() for prefix,src in zip(['AUT','CE'],a['source'])}
 for b in a['blocks']:assert raw[b['source_id']][b['raw_start']:b['raw_end']]==b['raw_html']
 for r in a['resources']:
  t=raw[r['source_id']];start=r['raw_start'];assert sha256(t[start:t.index('>',start)+1].encode()).hexdigest()==r['starttag_sha256']
 rejected=[]
 for name in ['omit-source','wrong-action-pointer','wrong-valid-case','invent-oracle','point-for-segment','baseline-flags','one-send-path','miss-note-positive','borrow-generic-local','erase-true-dot','erase-true-Warp-editor','caption-as-pixel','reset-set-invention']:
  t=deepcopy(a)
  if name=='omit-source':t['blocks'].pop()
  elif name=='wrong-action-pointer':t['assessments'][87]['case_refs'][0]['actual_action_pointer']='/28/setup_and_action'
  elif name=='wrong-valid-case':t['assessments'][87]['case_refs'][0]['json_pointer']='/28'
  elif name=='invent-oracle':t['proposals'][0]['actual_expected']='pass'
  elif name=='point-for-segment':t['proposals'][5]['proposed_minimal_delta']='Point drag alone proves all segment methods'
  elif name=='baseline-flags':t['common_future_prerequisites'][2]='Enabled flag sufficient'
  elif name=='one-send-path':t['proposals'][13]['proposed_future_positive_baseline']='Only a send knob needs exist'
  elif name=='miss-note-positive':t['proposals'][0]['proposed_future_positive_baseline']='No received notes or positive recording required'
  elif name=='borrow-generic-local':t['assessments'][189]['disposition']=STATUS['R']
  elif name=='erase-true-dot':t['assessments'][157]['disposition']=STATUS['G']
  elif name=='erase-true-Warp-editor':t['assessments'][-1]['case_refs']=[]
  elif name=='caption-as-pixel':next(r for r in t['resources'] if r['id']=='CE:R029')['pixels_or_destination_inspected']=True
  else:t['source_questions'][2]['actual_expected']='All119reset'
  try:guards(t,plan)
  except (AssertionError,KeyError,IndexError):rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 # Joint manual+derived edit cannot promote inspected/setup roles to actual input.
 for block,name in [('AUT:B088','joint-EditValue-inspection'),('CE:B052','joint-MIDI-chooser-borrow'),('AUT:B088','joint-wrong-actual-case')]:
  q=deepcopy(plan);q['judgments'][block].update(disposition='R',assessment='Existing case fully invokes all methods',proposal_groups=[])
  if name=='joint-wrong-actual-case':q['judgments'][block].update(disposition='X',cases=[29],proposal_groups=['G08'])
  t=build(q)
  try:guards(t,q)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Joint unsafe mutation accepted '+name)
 extract=runpy.run_path(str(PARSER))['extract'];bb,rr=extract('<div id="chapter_content"><h1 id="r" data-number="1">Root</h1><p>Press <img alt="" data-src="glyph"> tab.</p><figcaption>Caption role.</figcaption><ul><li>One</li></ul><table><tr><th>H</th><td>V</td></tr></table></div>','FIX');assert [b['kind'] for b in bb]==['h1','p','li','tr'] and bb[1]['text']=='Press tab.' and bb[-1]['cells'][1]['text']=='V' and Counter(r['kind'] for r in rr)=={'image':1,'caption':1}
 seal=P/'manifest.json'
 if seal.exists():
  m=load(seal);assert m['summary']==a['summary'] and set(packet)=={str(P/n) for n in m['files']}|{str(seal)}
  for n,pin in m['files'].items():assert dg(P/n)==pin
 for p in P.iterdir():
  b=p.read_bytes();assert b.endswith(b'\n') and all(x.rstrip(b' \t')==x for x in b.splitlines()),p
  if p.suffix=='.json':load(p)
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/dest.split('#')[0]).exists() or (dest=='manifest.json' and not seal.exists())
 assert before=={x['path']:dg(ROOT/x['path']) for x in inp['files']} and packet=={str(p):dg(p) for p in P.rglob('*') if p.is_file()}
 print(json.dumps({'status':'pass','sealed':seal.exists(),'summary':a['summary'],'unsafe_fixtures_rejected':rejected,'pure_parser_caption_inline_table_fixture':True,'immutable_inputs_unchanged':62,'packet_unchanged':True,'writes':False,'oldtools_runtime_decodes_replays':False},indent=2))
if __name__=='__main__':main()
