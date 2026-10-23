"""Read-only finite analyst MIDI Tools R4 checks. No source/application execution."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast,importlib.util,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'midi-tools-source-audit'
def load(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def safety(cat,plan):
 old=load(P/'acceptance-cases-r3.json')['cases'];new=cat['cases'][72:]
 assert len(cat['cases'])==93 and cat['cases'][:72]==old,'preserve72 exact old records'
 assert [c['id'] for c in cat['cases']]==[f'MED-{i:03}' for i in range(1,94)]
 assert Counter(c['documented_domain_grade'] for c in cat['cases'])=={'D12':77,'U':16}
 assert cat['actual_result_status']['actual_expected'] is cat['actual_result_status']['actual_comparison'] is None
 assert cat['actual_result_status']['executed'] is False and cat['actual_result_status']['target_grade']=='U'
 audit=load(A/'audit.json')
 for i,c in enumerate(new):
  g=plan['groups'][i];ap=audit['proposals'][i]
  assert c['adoption_group']==g['group']==ap['id'] and c['requirement']==g['requirement']
  assert c['source_claim']==' '.join(audit['blocks'][int(b[-3:])-1]['text'] for b in ap['source_blocks'])
  assert [r['block'] for r in c['source_contexts']]==ap['source_blocks']
  for r in c['source_contexts']:
   b=pointer(load(ROOT/r['catalog']),r['json_pointer']);assert b['id']==r['block']
  assert c['expected'] is c['comparator'] is c['actual_expected'] is c['actual_comparison'] is None
  assert c['target_12_4_3_grade']=='U' and c['execution']=='not-run'
  assert c['documentary_expected']==g['documentary_expected'] and c['documentary_comparator']==g['documentary_comparator']
  guard=c['positive_guard'];assert guard['hardware_required_for_editor_data'] is False
  assert all(guard[k] is True for k in ['independently_owned_admitted_editable_target','transformer_nonempty_input','generator_initial_empty_allowed','actual_nonempty_output_before_generator_bounds_capacity_origin_absence','productive_matched_operation_before_negative','separate_exact_original_reset','failed_prerequisite_stays_U'])
  assert g['action'] in c['setup_action'] and 'actual NONEMPTY' in c['setup_action']
  assert c['fixture']=='fixtures-r4.json#MIDI-TOOLS-OWNED-R4'
  for r in c.get('related_current_owner_contexts',[]):assert pointer(load(ROOT/r['catalog']),r['json_pointer'])['id'] in ['MPE-030','MPE-031','MPE-042']
 assert new[0]['documented_domain_grade']=='U' and new[0]['documentary_expected'] is None
 assert sum(c['documentary_comparator'] is not None for c in new)==3
 assert new[13]['id']=='MED-086' and 'NONZERO' in new[13]['setup_action'] and 'both Low and High to zero' in new[13]['setup_action'] and 'baseline fails' in new[13]['setup_action']
 assert all('NONEMPTY' in new[i]['setup_action'] for i in range(16,21))
 assert plan['no_resolution']==['C1','C2','C3','Q052','Q053','MTA-Q04']

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'python3 -B validate-r4.py --check only'
 pins=load(P/'inputs-r4.json');prior=load(P/'prior-files-r4.json');assert len(pins)==59 and len(prior)==38
 history=load(P/'consumer-impact-r4.json')
 watch={p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in pins}|{ROOT/n for n in history['consumer_identities']}|{ROOT/'wiki/specs/midi-editing-tools.md',ROOT/'wiki/research/midi-editing-tools.md'}
 before={str(p):dg(p) for p in watch}
 for n,r in prior.items():assert dg(P/n)==r,n
 for r in pins:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']},r['path']
 for n,r in history['consumer_identities'].items():assert dg(ROOT/n)==r
 assert len(history['records'])==4 and not history['consumers_modified'] and not history['historical_replay']
 for r in history['records']:assert pointer(load(ROOT/r['consumer']),r['json_pointer'])==dg(P/r['historical_snapshot'])['sha256']==r['literal_sha256']
 assert (P/'spec-before-r4.md').read_bytes()==(P/'spec-r3.md').read_bytes() and (P/'research-before-r4.md').read_bytes()==(P/'research-r3.md').read_bytes()
 for name,digest in [('manifest-author-r3.json','cd58218699444b9cc61562a94329137d1f2eb197b0f1fdeaf7768e15f0e04def')]:assert dg(P/name)['sha256']==digest
 assert dg(A/'manifest.json')['sha256']=='1ff435b3a0bd4470e4576886cb63dcf98b902998fea40ba2bdc1830a39b64128'
 for n,r in load(A/'manifest.json')['files'].items():assert dg(A/n)==r
 author=module(P/'author-r4.py','midi_tools_r4_author');plan=load(P/'tools-increment-r4.json');cat=load(P/'acceptance-cases-r4.json');safety(cat,plan)
 for n,t in author.build().items():assert (P/n).read_text()==t,n
 spec=(P/'spec-r4.md').read_text();oldrows=author.rows((P/'spec-r3.md').read_text());now=author.rows(spec);r2rows=author.rows((P/'spec-r2.md').read_text())
 assert set(now)==set(oldrows)=={f'REQ-MIDI-EDIT-{i:03}' for i in range(1,44)}
 assert all(now[k]==oldrows[k] for k in list(now)[:22])
 assert all(oldrows[f'REQ-MIDI-EDIT-{i:03}']==r2rows[f'REQ-MIDI-EDIT-{i:03}'] for i in range(27,44)),'audit R2 17tools align current R3'
 assert load(P/'acceptance-cases-r3.json')['cases'][:60]==load(P/'acceptance-cases-r2.json')['cases']
 assert len([k for k in now if now[k]!=oldrows[k]])==21
 for k in list(now)[22:]:assert all(now[k][i]==oldrows[k][i] for i in [0,1,2,4]) and now[k][3].startswith(oldrows[k][3])
 for n,canon in [('spec-r4.md','wiki/specs/midi-editing-tools.md'),('research-r4.md','wiki/research/midi-editing-tools.md')]:assert (P/n).read_bytes()==(ROOT/canon).read_bytes()
 parser=module(P.parent/'clip-view-source-audit/source_parser.py','retained_tools_parser');audit=load(A/'audit.json');raw=(P/'manual-12-midi-tools-2026-10-19.html').read_text();blocks,resources=parser.extract(raw,'TOOLS')
 assert blocks==audit['blocks'] and len(blocks)==146 and len(resources)==101
 for parsed,retained in zip(resources,audit['resources']):
  assert parsed=={k:v for k,v in retained.items() if k not in {'pixels_or_destination_inspected','target','complete','role'}}
  assert retained['pixels_or_destination_inspected'] is retained['complete'] is False and retained['target']=='U'
 assert len(audit['assessments'])==302
 for a in audit['assessments']:
  b=pointer(audit,a['block_json_pointer']);assert b['id']==a['block'] and pointer(audit,a['qualifier_context_pointer'])==b['text'];lo,hi=a['text_span'];assert b['text'][lo:hi]==a['quote'] and sha256(a['quote'].encode()).hexdigest()==a['quote_sha256']
 for e in audit['external_contexts']:
  if 'json_pointer' in e:assert pointer(load(ROOT/e['catalog']),e['json_pointer'])==e['row']
  else:lo,hi=e['text_span'];assert (ROOT/e['catalog']).read_text()[lo:hi]==e['quote']
 # Four inspected pure Browser functions only, excluding module imports and writer.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4 and all(not n.decorator_list for n in defs);env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned Browser read functions>','exec'),env)
 ids={r['id'] for r in env['spec_rows'](ROOT/'wiki/specs/midi-editing-tools.md',spec)};assert ids==set(now)
 rejected=[]
 for name in ['old-gesture-erased','actual-oracle','generator-flag-only','zero-without-positive','offline-hardware','wrong-source','C1-resolved','numeric-new-oracle','Strum-baseline-erased','lost-generator-output']:
  c,g=deepcopy(cat),deepcopy(plan)
  if name=='old-gesture-erased':c['cases'][71]['setup_action']='changed'
  elif name=='actual-oracle':c['cases'][72]['actual_expected']='measured'
  elif name=='generator-flag-only':c['cases'][89]['positive_guard']['actual_nonempty_output_before_generator_bounds_capacity_origin_absence']=False
  elif name=='zero-without-positive':c['cases'][85]['positive_guard']['productive_matched_operation_before_negative']=False
  elif name=='offline-hardware':c['cases'][73]['positive_guard']['hardware_required_for_editor_data']=True
  elif name=='wrong-source':c['cases'][76]['source_contexts'][0]['json_pointer']='/blocks/0'
  elif name=='C1-resolved':c['cases'][72]['documented_domain_grade']='D12'
  elif name=='numeric-new-oracle':c['cases'][76]['documentary_expected']=g['groups'][4]['documentary_expected']='exact numeric output';c['cases'][76]['documentary_comparator']=g['groups'][4]['documentary_comparator']='numeric'
  elif name=='Strum-baseline-erased':c['cases'][85]['setup_action']=c['cases'][85]['setup_action'].replace('NONZERO','zero');g['groups'][13]['action']=g['groups'][13]['action'].replace('NONZERO','zero')
  elif name=='lost-generator-output':c['cases'][89]['setup_action']=c['cases'][89]['setup_action'].replace('NONEMPTY','flag');g['groups'][17]['action']=g['groups'][17]['action'].replace('NONEMPTY','flag')
  try:safety(c,g)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('accepted unsafe fixture '+name)
 assert len(rejected)==10
 links=0
 for n,base in [('README-r4.md',P),('spec-r4.md',ROOT/'wiki/specs'),('research-r4.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)]+)\)',(P/n).read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   target=(base/dest.split('#')[0]);assert target.exists(),dest;links+=1
   if '#' in dest and target.suffix=='.md':
    anchor=dest.split('#',1)[1];assert anchor in {env['anchor'](l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')},dest
 for p in [p for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in prior]+[ROOT/'wiki/specs/midi-editing-tools.md',ROOT/'wiki/research/midi-editing-tools.md']:
  b=p.read_bytes();assert b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines()),str(p)
 if (P/'manifest-author-r4.json').exists():
  mf=load(P/'manifest-author-r4.json');assert {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}==set(mf['files'])|{'manifest-author-r4.json'}
  for n,r in mf['files'].items():assert dg(P/n)==r,n
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',requirements=43,refined_existing_rows=21,old_cases_exact=72,new_cases=21,cases=93,documentary_D12=77,documentary_U=16,new_named_comparators=3,new_null_comparators=18,actual_nonnull=0,executed=0,complete_topics=0,partial_groups=21,source_blocks=146,quotation_pointers=302,selected_audit_external=30,Browser_IDs=len(ids),links=links,prior_files_exact=38,input_pins=59,consumer_occurrences=4,negative_fixtures=rejected,watched_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
