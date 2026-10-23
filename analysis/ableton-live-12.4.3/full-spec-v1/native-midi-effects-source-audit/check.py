"""Finite retained MIDI-effects source audit. Own pure parser/data only.
--check is read-only. --write refuses a seal or existing audit. No old tools run.
"""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import importlib.util,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'native-midi-effects'
def load(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,s):
 for k in s.strip('/').split('/') if s else []:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def parser():
 p=P.parent/'clip-view-source-audit/source_parser.py';s=importlib.util.spec_from_file_location('retained_midi_parser',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m.extract
STATUS=dict(R='represented-actual-bounded-subset',G='missing-selected-clause-action-or-context',U='documented-outcome-or-source-context-U',M='research-or-guidance',E='editorial-or-structural',O='other-owner-context')
def build():
 inp=load(P/'inputs.json');plan=load(P/'plan.json');snap=next(s for s in inp['canonical_snapshots'] if '/specs/' in s['original_canonical']);req=[]
 for m in re.finditer(r'^### (REQ-NATIVE-MIDI-\d{3}) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',snap['text'],re.M|re.S):req.append(dict(id=m[1],title=m[2],contract=m[3],snapshot='inputs.json#/canonical_snapshots/0/text',text_span=[m.start(3),m.end(3)]))
 old=load(K/'cases.json');cases=old['cases'];index={c['id']:i for i,c in enumerate(cases)};blocks,resources=parser()((K/'manual-12-midi-effects-2026-10-19.html').read_text(),'NME');facets=[]
 for bi,b in enumerate(blocks):
  rows=[dict(part=0,span=[0,len(b['text'])],disposition='E',requirements=[],cases=[],assessment='Literal chapter/device heading, not a semantic completion or runtime requirement.',groups=[])] if b['kind'].startswith('h') else plan['parts'][b['id']]
  for row in rows:
   lo,hi=row['span'];q=b['text'][lo:hi]
   facets.append(dict(id=f'NMA-A{len(facets)+1:03}',block=b['id'],block_pointer=f'/blocks/{bi}',part=row['part'],text_span=[lo,hi],quote=q,quote_sha256=sha256(q.encode()).hexdigest(),full_qualifier_context_pointer=f'/blocks/{bi}/text',literal_paragraph_anchor=b['attributes'].get('id'),disposition=STATUS[row['disposition']],assessment=row['assessment'],requirement_refs=[dict(catalog='owner_requirements',json_pointer=f'/{i-1}',id=req[i-1]['id'],actual_contract_pointer=f'/{i-1}/contract') for i in row['requirements']],case_refs=[dict(catalog='owner_cases',json_pointer=f'/{index[c]}',id=c,actual_setup_pointer=f'/{index[c]}/setup',actual_action_pointer=f'/{index[c]}/action',legacy_documentary_predicate_pointer=f'/{index[c]}/documentary_oracle') for c in row['cases']],proposals=[f'NMA-G{i:02}' for i in row['groups']],documentary_expected=None,documentary_comparison=None,actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False,coverage_credit=0))
 for r in resources:r.update(pixels_or_destination_inspected=False,role='Literal caption/link text/href and image empty-alt/baseURL/attributes retained; repeated srcset/sizes hashchecked only, no pixels or separately followed destination.',target='U',complete=False)
 proposals=deepcopy(plan['proposals'])
 for g in proposals:g['assessment_ids']=[f['id'] for f in facets if g['id'] in f['proposals']]
 questions=deepcopy(plan['source_questions'])
 for q in questions:q['quotes']=[dict(block=b['id'],json_pointer=f'/blocks/{i}/text',quote=b['text']) for i,b in enumerate(blocks) if b['id'] in q['blocks']]
 reverse={key:[dict(id=r['id'],json_pointer=f'/{catalog}/{i}',related_assessment_ids=[f['id'] for f in facets if any(z['id']==r['id'] for z in f[field])],role='Qualified actual subset only; empty list allowed for source-silent lifecycle or boundaries. No complete assertion/case/profile.',target='U',complete=False) for i,r in enumerate(rows)] for key,catalog,rows,field in [('requirements','owner_requirements',req,'requirement_refs'),('cases','owner_cases',cases,'case_refs')]}
 summary=dict(primary_scope='Complete retained chapter_content: exactlyeightnativeeffectsections, no other profiles; footer/navexcluded',blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),paragraph_list_parts=sum(map(len,plan['parts'].values())),facets=len(facets),dispositions=dict(Counter(f['disposition'] for f in facets)),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),requirements=27,cases=146,old_D12=54,old_U=92,old_lifecycle_U=80,effect_profiles=8,selected_external=len(inp['selected_external_contexts']),proposal_groups=len(proposals),source_questions=len(questions),input_pins=len(inp['files']),old_packet_files=32,asof_snapshots=2,new_documentary_nonnull=0,actual_nonnull=0,executed=0,new_normative_IDs=0,complete_topics=0,coverage_credit=0)
 return dict(role='Retained source-only semantic reconciliation, no owner adoption or compatibility proof',source=dict(**load(K/'source.json'),capture_utc=None,source_kind='retained official Version12 HTML, precise publication revision unstated, exacttarget12.4.3U',filter='Pure retained parser enters only div#chapter_content; original source metadata footer heading AbletonReferenceManual is outside. Full112blocks/no tables/eighth2deviceentries retained; no sourceheading/title fuzzy filtering.',locator_policy='raw_start/end are decodedUnicode character positions, exact HTML line/column; heading ancestry not inferred paragraph anchor'),blocks=blocks,resources=resources,owner_requirements=req,owner_cases=cases,owner_asof=dict(manifest='native-midi-effects/manifest-author-r2.json',sha256='17d74ef752829a992416eb725bd459c70dd8d4dd61ea2480d6eb17c794c11743',canonical_snapshots='inputs.json#/canonical_snapshots',policy='ExactmatchingcurrentcorrectedR2 snapshots and full146fields, not future mutable wiki hash gates. Archive opaquehashonly; no extraction.'),legacy_expected_boundary='All old54documentary/92U records unchanged; nonnull legacy documentary_oracle/comparator is not actual result. All146exacttargetU/unexecuted; allnew documentary/actualoracles null.',external_contexts=inp['selected_external_contexts'],assessments=facets,proposals=proposals,source_questions=questions,common_future_prerequisites=plan['common_future_prerequisites'],reverse_catalogs=reverse,read_scope=dict(primary='All112fullparagraph/list/headings and all19literalresources read',owner='All27fullcontracts/all146fullsetup-action-predicate-comparator-fields read, including80lifecycleU',review='Originalandfinalindependentreviews/allthreeR2narrowings read',neighbors='Only30qualifiedactualselectedrecords, not fullMIDIeditor/Tools/MPE/Tuning/Automation/Routing chapters; editoractions are not liveeffects',archive='Opaquehashonly; no archive extraction/native/example/runtime',figures='8images/8captions/3links retained; pixels/destinationsuninspected'),summary=summary)
def guards(a):
 plan=load(P/'plan.json');inp=load(P/'inputs.json');assert len(a['blocks'])==112 and len(a['resources'])==19 and len(a['assessments'])==235
 assert Counter(b['kind'] for b in a['blocks'])=={'p':76,'li':27,'h1':1,'h2':8}
 assert [b['attributes']['id'] for b in a['blocks'] if b['kind']=='h2']==['arpeggiator','cc-control','chord','note-length','pitch','random','scale','velocity']
 assert Counter(r['kind'] for r in a['resources'])=={'link':3,'image':8,'caption':8}
 assert len(a['owner_requirements'])==27 and a['owner_cases']==load(K/'cases.json')['cases'] and len(a['owner_cases'])==146
 assert Counter(c['grade'] for c in a['owner_cases'])=={'D12':54,'U':92} and all(c['exact_build_grade']=='U' and c['execution']=='unexecuted' for c in a['owner_cases'])
 assert all(c['documentary_oracle'] is c['comparator'] is None for c in a['owner_cases'] if c['grade']=='U')
 assert len([c for c in a['owner_cases'] if '-L' in c['id']])==80
 spans={b['id']:[] for b in a['blocks']}
 for f in a['assessments']:
  b=ptr(a,f['block_pointer']);lo,hi=f['text_span'];assert b['id']==f['block'] and b['text'][lo:hi]==f['quote'] and sha256(f['quote'].encode()).hexdigest()==f['quote_sha256'];assert ptr(a,f['full_qualifier_context_pointer'])==b['text'];spans[b['id']].append((lo,hi))
  if not b['kind'].startswith('h'):
   p=plan['parts'][b['id']][f['part']];assert f['text_span']==p['span'] and f['disposition']==STATUS[p['disposition']] and f['assessment']==p['assessment'];assert [r['id'] for r in f['case_refs']]==p['cases'];assert [r['id'] for r in f['requirement_refs']]==[f'REQ-NATIVE-MIDI-{i:03}' for i in p['requirements']]
  for r in f['case_refs']+f['requirement_refs']:assert ptr(a[r['catalog']],r['json_pointer'])['id']==r['id']
  assert all(f[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and f['target']=='U' and not f['executed'] and not f['complete'] and f['coverage_credit']==0
 for b in a['blocks']:
  seen=set()
  for lo,hi in spans[b['id']]:assert not seen.intersection(range(lo,hi));seen.update(range(lo,hi))
  assert all(i in seen for i,c in enumerate(b['text']) if not c.isspace()),b['id']
 assert len(a['proposals'])==21 and len(a['source_questions'])==6
 for g in a['proposals']:
  assert all(g[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and g['new_normative_IDs']==[] and not g['executed'] and not g['complete'] and g['target']=='U' and g['coverage_credit']==0
  assert 'genuinely NONEMPTY' in g['proposed_future_positive_baseline'] and 'BOTH independent notes/events' in g['proposed_future_positive_baseline']
 assert a['proposals'][20]['existing_case_IDs']==[c['id'] for c in a['owner_cases'] if '-L' in c['id']]
 assert 'no duplicate placeholder' in a['proposals'][20]['proposed_minimal_delta']
 cs={c['id']:c for c in a['owner_cases']}
 for cid in ['NME-NL-L01','NME-NL-L05']:assert 'Latch off' in cs[cid]['setup'] and 'Length enabled' in cs[cid]['setup'] and cs[cid]['grade']=='U'
 for cid in ['NME-043','NME-044','NME-045']:assert 'accepted positive Range' in cs[cid]['setup'] and 'unit/upper endpoint U' in cs[cid]['setup']
 assert cs['NME-064']['documentary_oracle']=='Outputs remain60..127; modulation baseline, displacement, sequence and frequency U'
 assert cs['NME-050']['documentary_oracle'] is cs['NME-051']['documentary_oracle'] is None
 assert a['external_contexts']==inp['selected_external_contexts'] and len(a['external_contexts'])==30
 for e in a['external_contexts']:
  assert e['primary_source_case_proof'] is False
  if 'json_pointer' in e:assert ptr(load(ROOT/e['catalog']),e['json_pointer'])==e['row']
  else:lo,hi=e['text_span'];assert (ROOT/e['catalog']).read_text()[lo:hi]==e['quote']
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in [['--check'],['--write']]
 if sys.argv[1:]==['--write']:
  assert not (P/'manifest.json').exists(),'sealed: refuse overwrite';assert not (P/'audit.json').exists(),'refuse existing audit';a=build();guards(a);(P/'audit.json').write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n');return
 inp=load(P/'inputs.json');watch={p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in inp['files']};before={str(p):dg(p) for p in watch}
 for r in inp['files']:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
 for n,r in inp['old_packet_files'].items():assert dg(K/n)==r
 assert len(inp['old_packet_files'])==32 and len(inp['files'])==50
 mf=load(K/'manifest-author-r2.json');assert dg(K/'manifest-author-r2.json')['sha256']=='17d74ef752829a992416eb725bd459c70dd8d4dd61ea2480d6eb17c794c11743'
 for r in mf['payloads']:
  if r['path'].startswith('wiki/'):
   s=next(s for s in inp['canonical_snapshots'] if s['original_canonical']==r['path']);b=s['text'].encode();assert len(b)==r['bytes'] and sha256(b).hexdigest()==r['sha256']==s['sha256']
  else:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 a=load(P/'audit.json');assert a==build();guards(a)
 demo='<div id="chapter_content"><h1 id="demo">Demo</h1><p>Rel. <a href="#x">Vel.</a> and two <img alt="" src="x"> events.</p></div><h2>Outside</h2>'
 db,dr=parser()(demo,'FIX');assert len(db)==2 and len(dr)==2 and db[1]['text']=='Rel. Vel. and two events.' and db[1]['attributes'].get('id') is None and db[1]['heading_context'][0]['anchor']=='demo'
 rejected=[]
 for name in ['omit-facet','wrong-case-pointer','actual-oracle','fake-new-documentary','missing-NONEMPTY-positive','one-event-loss-baseline','lifecycle-graded','disabled-Length-edit','Pitch-unit-inferred','velocity-displacement','Alt-cycle-resolved','tool-case-borrowed','13th-class','archive-extracted-claim']:
  v=deepcopy(a)
  if name=='omit-facet':v['assessments'].pop(5)
  elif name=='wrong-case-pointer':f=next(f for f in v['assessments'] if f['case_refs']);f['case_refs'][0]['json_pointer']='/145'
  elif name=='actual-oracle':v['assessments'][10]['actual_expected']='measured'
  elif name=='fake-new-documentary':v['proposals'][1]['documentary_expected']='output'
  elif name=='missing-NONEMPTY-positive':v['proposals'][0]['proposed_future_positive_baseline']=v['proposals'][0]['proposed_future_positive_baseline'].replace('genuinely NONEMPTY','enabled flag')
  elif name=='one-event-loss-baseline':v['proposals'][0]['proposed_future_positive_baseline']=v['proposals'][0]['proposed_future_positive_baseline'].replace('BOTH independent notes/events','one event')
  elif name=='lifecycle-graded':v['owner_cases'][66]['grade']='D12'
  elif name=='disabled-Length-edit':next(c for c in v['owner_cases'] if c['id']=='NME-NL-L05')['setup']='NoteOn Latchon editLength'
  elif name=='Pitch-unit-inferred':next(c for c in v['owner_cases'] if c['id']=='NME-043')['setup']='Range12st'
  elif name=='velocity-displacement':next(c for c in v['owner_cases'] if c['id']=='NME-064')['documentary_oracle']='rawvelocity±50'
  elif name=='Alt-cycle-resolved':next(c for c in v['owner_cases'] if c['id']=='NME-050')['documentary_oracle']='13stepcycle'
  elif name=='tool-case-borrowed':v['external_contexts'][2]['primary_source_case_proof']=True
  elif name=='13th-class':v['blocks'][91]['text']='13noteclasses'
  elif name=='archive-extracted-claim':v['owner_asof']['policy']='archive extracted'
  try:
   guards(v);assert v['owner_asof']==a['owner_asof']
  except (AssertionError,KeyError):rejected.append(name)
  else:raise AssertionError('accepted unsafe fixture '+name)
 retained=['NME-001','NME-002','NME-003','NME-004','NME-005','NME-006','NME-007','NME-008','NME-009','NME-010','NME-011','NME-012','NME-013','NME-018','NME-019','NME-020','NME-021','NME-022','NME-024','NME-025','NME-027','NME-028','NME-029','NME-031','NME-032','NME-033','NME-034','NME-037','NME-038','NME-040','NME-041','NME-044','NME-046','NME-047','NME-049','NME-052','NME-053','NME-055','NME-057','NME-058','NME-059','NME-060','NME-061','NME-063','NME-064']
 assert all(next(c for c in a['owner_cases'] if c['id']==cid)==next(c for c in load(K/'cases.json')['cases'] if c['id']==cid) for cid in retained)
 for p in P.rglob('*'):
  if p.is_file():b=p.read_bytes();assert b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines()),p
 for dest in re.findall(r'\]\(([^)]+)\)',(P/'README.md').read_text()):
  if not re.match(r'^[A-Za-z]+:',dest):assert (P/dest.split('#')[0]).exists(),dest
 sealed=(P/'manifest.json').exists()
 if sealed:
  m=load(P/'manifest.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(m['files'])|{'manifest.json'}
  for n,r in m['files'].items():assert dg(P/n)==r,n
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=sealed,summary=a['summary'],negative_fixtures=rejected,retained_positive_contexts=len(retained),parser_inline_scope_fixture=True,all_inputs_unchanged=True,packet_unchanged=True,watch_paths=len(watch),writes=False,original_vendor_native_runtime_network_hardware_candidate=False),indent=2))
if __name__=='__main__':main()
