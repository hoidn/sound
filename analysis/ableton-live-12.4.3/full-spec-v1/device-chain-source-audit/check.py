"""Read-only finite common Devices source audit. No old writer/main/vendor execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];F=P.parent
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v

def guards(a):
 assert len(a['blocks'])==len(a['assessments'])==153 and len(a['proposals'])==20
 for i,r in enumerate(a['assessments']):
  b=a['blocks'][i];assert r['id']==f'DCA-A{i+1:03}' and r['block']==b['id'] and r['source_pointer']==f'/blocks/{i}/text' and pointer(a,r['source_pointer'])==r['quote']==b['text']
  assert sha256(r['quote'].encode()).hexdigest()==r['quote_sha256']
  for k in ['represented_requirement_refs','represented_case_refs','external_refs']:
   for ref in r[k]:assert pointer(a,ref['pointer'])['id']==ref['id']
 for r in a['assessments']+a['proposals']:
  assert all(r[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and r['target']=='U' and r['executed'] is r['complete'] is False and r['coverage_credit']==0
 for i,g in enumerate(a['proposals'],1):
  assert g['id']==f'DCA-G{i:02}' and g['new_normative_IDs']==[] and g['assessment_ids']==[r['id'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']] and g['source_blocks']==[r['block'] for r in a['assessments'] if g['id'] in r['open_proposal_groups']] and g['assessment_ids']
 ids=lambda n,k:[r['id'] for r in a['assessments'][n-1][k]]
 assert ids(11,'external_refs')==['REQ-WORKSPACE-CONTROL-009','WORKSPACE-009'] and a['assessments'][14]['external_refs']==[],'track title != device fold'
 assert 'CV-001' in ids(13,'external_refs') and 'NAV-079' in ids(25,'external_refs') and 'RCK-049' in ids(26,'represented_case_refs')
 assert ids(33,'represented_case_refs')==['RCK-050'] and ids(71,'represented_case_refs')==['RCK-051'] and 'RCK-052' in ids(94,'represented_case_refs')
 assert 'RML-006' in ids(20,'external_refs') and 'MXW-U-ARM-INSERT' in ids(20,'external_refs')
 assert 'RML-054' in ids(152,'external_refs') and not a['assessments'][151]['open_proposal_groups'],'TrackDelay unavailability already observable'
 assert ids(52,'external_refs')==['REQ-LADR-012','REQ-LADR-013','REQ-LADR-015','LADR-012','LADR-013','LADR-015'] and a['assessments'][51]['represented_case_refs']==[] and not a['assessments'][51]['open_proposal_groups'],'API not UI coverage'
 assert 'PARAMETER context' in a['proposals'][6]['proposed_minimal_delta'] and 'returning alone must not be presumed to reactivate' in a['proposals'][6]['proposed_minimal_delta']
 assert 'active nonzero automation' in a['proposals'][6]['proposed_future_positive_baseline']
 assert 'does not create/edit Options.txt' in a['proposals'][10]['proposed_minimal_delta']
 assert 'except expanded Sampler Zone Editor always-visible context' in a['proposals'][11]['proposed_minimal_delta']
 assert 'LIST from parameter VALUES' in a['proposals'][14]['proposed_minimal_delta']
 assert 'Genuinely recognized successful owned saved default' in a['proposals'][13]['proposed_future_positive_baseline']
 assert 'factory/no-custom' in a['proposals'][18]['proposed_minimal_delta'] and 'single instrument OR Instrument Rack' in a['proposals'][18]['proposed_minimal_delta']
 assert 'actual NONEMPTY generated notes' in a['proposals'][18]['proposed_future_positive_baseline'] and 'no mandatory nonempty recognizer output' in a['proposals'][18]['proposed_future_positive_baseline']
 assert 'last ADDED' in a['proposals'][16]['proposed_minimal_delta'] and 'last-added' in a['proposals'][18]['proposed_minimal_delta']
 assert 'Project-specific versus User Library' in a['proposals'][19]['proposed_minimal_delta']
 assert a['summary']['new_normative_IDs']==a['summary']['new_cases']==a['summary']['coverage_credit']==a['summary']['complete_topics']==0

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only'
 inputs=load(P/'inputs.json');a=load(P/'audit.json');plan=load(P/'plan.json');files=inputs['files'];assert len(files)==54 and len({r['path'] for r in files})==54 and all(not r['path'].startswith('wiki/') for r in files)
 watch={q for q in P.iterdir() if q.is_file()}|{ROOT/r['path'] for r in files};before={str(q):dg(q) for q in watch}
 for r in files:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
 assert dg(F/'reviews/racks-source-audit-review.json')['sha256']=='bc4ca028eca17ee1d9eb51eeb9ea3fb488124359c6c65a086c3ad86abb47bb15'
 original=load(F/'racks-source-audit/inputs.json');assert inputs['canonical_snapshots'][:2]==original['canonical_snapshots']
 for r in inputs['canonical_snapshots']:assert dict(bytes=len(r['text'].encode()),sha256=sha256(r['text'].encode()).hexdigest())=={k:r[k] for k in ['bytes','sha256']}
 oldmf=load(F/'racks/manifest.json')
 for r in oldmf['payloads']:
  if r['path'].startswith('wiki/'):
   s=next(s for s in inputs['canonical_snapshots'] if s['original_canonical']==r['path']);assert {k:s[k] for k in ['bytes','sha256']}=={k:r[k] for k in ['bytes','sha256']}
  else:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 assert a['owner_requirements']==load(F/'racks-source-audit/audit.json')['owner_requirements'] and len(a['owner_requirements'])==28
 spec=inputs['canonical_snapshots'][1]['text']
 for r in a['owner_requirements']:
  lo,hi=r['text_span'];assert spec[lo:hi]==r['contract'] and spec.count('### '+r['id']+' — '+r['title'])==1
 assert a['owner_cases']==load(F/'racks/cases.json')['cases'] and len(a['owner_cases'])==61
 assert all(c['execution']=='unexecuted' for c in a['owner_cases'])
 for e in a['external_contexts']:
  if 'catalog' in e:assert pointer(load(ROOT/e['catalog']),e['json_pointer'])==e['row']
  else:lo,hi=e['text_span'];assert inputs['canonical_snapshots'][e['snapshot']]['text'][lo:hi]==e['quote']
 assert len(a['external_contexts'])==41
 assert a['summary']==dict(blocks=153,paragraphs=110,list_items=25,headings=18,whole_context_assessments=153,atomic_facets_claimed=False,resources=140,resource_kinds=dict(link=52,image=44,caption=44),owner_requirements_asof=28,owner_cases_asof=61,selected_external_records=41,proposals=20,source_questions=4,new_normative_IDs=0,new_cases=0,new_documentary_nonnull=0,actual_nonnull=0,executed=0,coverage_credit=0,complete_topics=0)
 src=next(s for s in load(F/'racks/sources.json') if s['id']=='RACKS-MAN-DEVICES');assert all(a['source'][k]==v for k,v in src.items())
 assert dg(ROOT/a['source']['path'])==dict(bytes=302488,sha256='6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82')
 extract=runpy.run_path(str(F/'clip-view-source-audit/source_parser.py'))['extract'];raw=(ROOT/a['source']['path']).read_text();blocks,resources=extract(raw,'DEVICES');assert a['blocks']==blocks and Counter(b['kind'] for b in blocks)==dict(h1=1,h2=3,h3=6,h4=8,p=110,li=25)
 assert len(resources)==len(a['resources'])==140 and Counter(r['kind'] for r in resources)==dict(link=52,image=44,caption=44)
 for r,v in zip(resources,a['resources']):
  assert r=={k:x for k,x in v.items() if k not in ['pixels_or_destination_inspected','target','complete','role']} and v['pixels_or_destination_inspected'] is v['complete'] is False
  assert sha256(raw[v['raw_start']:raw.index('>',v['raw_start'])+1].encode()).hexdigest()==v['starttag_sha256']
 for b in blocks:assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
 for k in ['assessments','proposals','common_future_prerequisites','source_questions']:assert a[k]==plan[k]
 guards(a);rejected=[]
 for name in ['omit-context','invent-oracle','erase-true-HotSwap-Esc','track-title-proves-device-fold','generic-edit-false-gap','API-proves-UI','auto-reenable','unproductive-default','all-samples-hover','config-retains-values','unqualified-conversion-factory','empty-recognition-preview','TrackDelay-private-only','Options-edit-executed']:
  t=deepcopy(a)
  if name=='omit-context':t['assessments'].pop()
  elif name=='invent-oracle':t['proposals'][0]['actual_expected']='pass'
  elif name=='erase-true-HotSwap-Esc':t['assessments'][70]['represented_case_refs']=[]
  elif name=='track-title-proves-device-fold':t['assessments'][14]['external_refs']=deepcopy(t['assessments'][10]['external_refs'])
  elif name=='generic-edit-false-gap':t['assessments'][24]['external_refs']=[]
  elif name=='API-proves-UI':t['assessments'][51]['represented_case_refs']=[dict(id='RCK-051',pointer='/owner_cases/50')]
  elif name=='auto-reenable':t['proposals'][6]['proposed_minimal_delta']='Returning automatically re-enables automation'
  elif name=='unproductive-default':t['proposals'][13]['proposed_future_positive_baseline']='Folder presence only'
  elif name=='all-samples-hover':t['proposals'][11]['proposed_minimal_delta']='All sample buttons require hover'
  elif name=='config-retains-values':t['proposals'][14]['proposed_minimal_delta']='Configuration saves values'
  elif name=='unqualified-conversion-factory':t['proposals'][18]['proposed_minimal_delta']='Every conversion always creates factory Rack'
  elif name=='empty-recognition-preview':t['proposals'][18]['proposed_future_positive_baseline']='Enabled instrument but empty notes'
  elif name=='TrackDelay-private-only':t['assessments'][151]['external_refs']=[]
  else:t['proposals'][10]['proposed_minimal_delta']='Create/edit Options.txt now'
  try:guards(t)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 fb,fr=extract('<p>Outside</p><div id="chapter_content"><h1 id="s">Root</h1><div><p>Set 1.1.1. Keep fixed.</p></div><ul><li>Qualified.</li></ul><figcaption>Caption.</figcaption><img alt="" src="unopened"></div><p>After</p>','FIX')
 assert [b['kind'] for b in fb]==['h1','p','li'] and fb[1]['text']=='Set 1.1.1. Keep fixed.' and [r['kind'] for r in fr]==['caption','image']
 links=0
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):assert (P/dest.split('#')[0]).exists();links+=1
 for q in P.iterdir():
  if q.is_file():b=q.read_bytes();assert b.endswith(b'\n') and b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines())
 if (P/'manifest.json').exists():
  m=load(P/'manifest.json');assert set(m['files'])=={q.name for q in P.iterdir() if q.is_file()}-{'manifest.json'}
  for n,v in m['files'].items():assert dg(P/n)==v
 assert before=={str(q):dg(q) for q in watch}
 print(json.dumps(dict(status='pass',summary=a['summary'],input_pins=54,asof_snapshots=4,selected_external=41,links=links,negative_fixtures=rejected,parser_fixture=True,watched_paths=len(watch),all_unchanged=True,write_mode=False,old_main_or_runtime=False),indent=2))
if __name__=='__main__':main()
