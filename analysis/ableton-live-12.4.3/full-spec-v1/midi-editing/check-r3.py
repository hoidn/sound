"""Read-only current MIDI gesture increment checks; retained source data, no vendor code."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];AUDIT=P.parent/'midi-editing-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def rows(text):
 return {c[0]:c for line in text.splitlines() if line.startswith('| REQ-MIDI-EDIT-') for c in [[s.strip() for s in line.strip('|').split('|')]]}
def check_catalog(cat,inc):
 old=load(P/'acceptance-cases-r2.json')['cases'];new=cat['cases'][60:]
 assert len(cat['cases'])==72 and cat['cases'][:60]==old,'old60 exact actions/predicates must remain'
 assert new==inc['new_cases'] and [r['id'] for r in cat['cases']]==[f'MED-{i:03}' for i in range(1,73)]
 assert Counter(c['documented_domain_grade'] for c in cat['cases'])=={'D12':57,'U':15}
 assert cat['actual_result_status']==load(P/'acceptance-cases-r2.json')['actual_result_status']
 for c in new:
  assert c['actual_expected'] is c['actual_comparison'] is None and c['target_12_4_3_grade']=='U' and c['execution']=='not-run'
  assert all(c['positive_guard'][k] is True for k in ['owned_nonempty_editable_source','independently_admitted_values_controls','productive_matched_operation_before_negative','separate_exact_original_reset','failed_prerequisite_stays_U'])
  assert c['positive_guard']['hardware_required_for_editor_data'] is False
  assert c['source_contexts'] and c['fixture']=='fixtures-r3.json#MIDI-OWNED-R3'
 assert new[8]['id']=='MED-069' and new[8]['expected'] is new[8]['comparator'] is None and new[8]['documented_domain_grade']=='U','Humanize Q053 stays U'
 assert [r['id'] for r in new if r['comparator'] is None]==['MED-066','MED-068','MED-069','MED-070']
 assert 'velocity' in old[19]['setup_action'] and 'foreground A' in old[19]['setup_action']
 assert 'Chance' in new[11]['setup_action'] and 'disable Focus' in new[11]['setup_action']
 assert inc['no_resolution']==['Q052','Q053','C1','C2','C3'] and inc['source_questions_retained'] is True

def check_rows(spec,inc):
 old=rows((P/'spec-r2.md').read_text());now=rows(spec)
 assert set(old)==set(now)=={f'REQ-MIDI-EDIT-{i:03}' for i in range(1,44)}
 changed={k for k in old if old[k]!=now[k]};assert changed==set(inc['requirement_rows_after'])=={f'REQ-MIDI-EDIT-{i:03}' for i in [1,2,5,6,9,14]}
 for k in old:
  if k in changed:
   assert old[k]==inc['requirement_rows_before'][k] and now[k]==inc['requirement_rows_after'][k]
   assert all(now[k][i].startswith(old[k][i]) for i in range(5)),'add literal source entries, preserve previous full predicates'
  else:assert now[k]==old[k]
 assert all(now[f'REQ-MIDI-EDIT-{i:03}']==old[f'REQ-MIDI-EDIT-{i:03}'] for i in range(27,44)),'17tool rows exact'
 return old,now

def check_sources(new):
 raw=(P/'manual-12-editing-midi-2026-10-19.html').read_text();referenced=set()
 expected_blocks={61:[27,28],62:[34],63:[38,39],64:[72],65:[86],66:[116,117],67:[125],68:[127],69:[123],70:[146,147],71:[148],72:[217,165]}
 for c in new:
  assert [r['block'] for r in c['source_contexts']]==[f'MIDI:B{i:03}' for i in expected_blocks[int(c['id'][-3:])]]
  for r in c['source_contexts']:
   b=pointer(load(ROOT/r['catalog']),r['json_pointer']);assert b['id']==r['block'] and raw[b['raw_start']:b['raw_end']]==b['raw_html'];referenced.add(b['id'])
 return referenced

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'python3 -B check-r3.py --check; no write mode'
 prior=load(P/'prior-files-r3.json');pins=load(P/'inputs-r3.json');assert len(prior)==25 and len(pins)==8
 history=load(P/'consumer-impact-r3.json')
 watched={ROOT/r['path'] for r in history['occurrences'] if not r['active_author_input']}|{p for p in P.rglob('*') if p.is_file()}|{ROOT/r['path'] for r in pins}|{ROOT/'wiki/specs/midi-editing-tools.md',ROOT/'wiki/research/midi-editing-tools.md'}
 # Immutable audit payloads are checked via their own seal; active consumer author inputs are as-of, not watched gates.
 mf=load(AUDIT/'manifest.json');watched|={AUDIT/n for n in mf['files']}
 before={str(p):dg(p) for p in watched}
 for n,r in prior.items():assert dg(P/n)==r
 for r in pins:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 for n,r in mf['files'].items():assert dg(AUDIT/n)==r
 assert dg(AUDIT/'manifest.json')['sha256']=='f31e97284b1a83587c82516ed79476e723462153629f191503dbd55e02083e99'
 assert load(P.parent/'reviews/midi-editing-source-audit-review.json')['disposition']=='approved-partial-source-audit'
 inc=load(P/'gesture-increment-r3.json');cat=load(P/'acceptance-cases-r3.json');check_catalog(cat,inc)
 spec=(P/'spec-r3.md').read_text();old,now=check_rows(spec,inc)
 for f,canonical in [('spec-r3.md','wiki/specs/midi-editing-tools.md'),('research-r3.md','wiki/research/midi-editing-tools.md')]:assert (P/f).read_bytes()==(ROOT/canonical).read_bytes(),'Current R3 check only; later owner advances retain this snapshot as history'
 referenced=check_sources(inc['new_cases'])
 groups=load(AUDIT/'proposed-deltas.json');assert set(inc['adopted_partial_groups'])=={c['adoption_group'] for c in inc['new_cases']}<={g['id'] for g in groups}
 assert len(inc['adopted_partial_groups'])==11 and len(groups)==38
 delta=load(P/'delta-r3.json');fields=[dict(id=k,column=['id','operation','preconditions_input','contract','evidence'][i],before=old[k][i],after=now[k][i]) for k in old for i in range(5) if old[k][i]!=now[k][i]]
 assert fields==delta['changed_fields'] and len(fields)==9 and delta['changed_requirement_rows']==sorted(inc['requirement_rows_after'])
 assert delta['new_named_documentary_comparators']==8 and delta['new_documentary_comparator_null']==4
 history=load(P/'consumer-impact-r3.json');assert len(history['occurrences'])==14
 frozen=0
 for r in history['occurrences']:
  # Active author files can grow; the exact old provider remains the preserved identity.
  assert dg(P/r['provider'])['sha256']==r['sha256']
  if not r['active_author_input']:assert pointer(load(ROOT/r['path']),r['json_pointer'])==r['sha256'];frozen+=1
 # Use only four fully inspected owned Browser functions, excluding module import and build/write entrypoints.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}]
 assert len(defs)==4 and all(not n.decorator_list for n in defs);env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'<owned Browser read functions>','exec'),env)
 browser=env['spec_rows'](ROOT/'wiki/specs/midi-editing-tools.md',spec);assert {r['id'] for r in browser}==set(now)
 rejected=[]
 for name in ['old-record-mutated','actual-oracle','Humanize-bound','erase-positive-baseline','offline-hardware','wrong-source','erase-true-Velocity','change-tool-contract']:
  cc,ii=deepcopy(cat),deepcopy(inc);ss=spec
  if name=='old-record-mutated':cc['cases'][0]['setup_action']='changed'
  elif name=='actual-oracle':cc['cases'][60]['actual_expected']=ii['new_cases'][0]['actual_expected']='invented'
  elif name=='Humanize-bound':cc['cases'][68]['expected']=ii['new_cases'][8]['expected']='quarter bound resolved'
  elif name=='erase-positive-baseline':cc['cases'][62]['positive_guard']['productive_matched_operation_before_negative']=False;ii['new_cases'][2]=deepcopy(cc['cases'][62])
  elif name=='offline-hardware':cc['cases'][60]['positive_guard']['hardware_required_for_editor_data']=True;ii['new_cases'][0]=deepcopy(cc['cases'][60])
  elif name=='wrong-source':
   cc['cases'][63]['source_contexts'][0]['block']='MIDI:B071';ii['new_cases'][3]=deepcopy(cc['cases'][63])
  elif name=='erase-true-Velocity':cc['cases'][19]['setup_action']='No velocity action'
  elif name=='change-tool-contract':ss=ss.replace('| REQ-MIDI-EDIT-028 | Chop tool','| REQ-MIDI-EDIT-028 | Rewritten tool')
  try:check_catalog(cc,ii);check_rows(ss,ii);check_sources(ii['new_cases'])
  except AssertionError:rejected.append(name)
  else:raise AssertionError('accepted unsafe mutation: '+name)
 assert len(rejected)==8
 links=0
 for file in [P/'README-r3.md',P/'spec-r3.md',P/'research-r3.md']:
  # Snapshot links are relative to their original canonical directories.
  parent=ROOT/'wiki/specs' if file.name=='spec-r3.md' else ROOT/'wiki/research' if file.name=='research-r3.md' else P
  for dest in re.findall(r'\]\(([^)]+)\)',file.read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   assert (parent/dest.split('#')[0]).exists(),dest;links+=1
 for file in [p for p in P.rglob('*') if p.is_file() and str(p.relative_to(P)) not in prior]+[ROOT/'wiki/specs/midi-editing-tools.md',ROOT/'wiki/research/midi-editing-tools.md']:
  b=file.read_bytes();assert b'\x00' not in b and all(line.rstrip(b' \t')==line for line in b.splitlines()),str(file)
 if (P/'manifest-author-r3.json').exists():
  own=load(P/'manifest-author-r3.json');assert {str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}==set(own['files'])|{'manifest-author-r3.json'}
  for n,r in own['files'].items():assert dg(P/n)==r
 assert before=={str(p):dg(p) for p in watched}
 print(json.dumps(dict(status='pass',requirements=43,changed_rows=6,changed_fields=9,cases=72,old_cases_exact=60,new_cases=12,documentary_D12=57,documentary_U=15,new_named_comparators=8,new_null_comparators=4,partial_groups=11,audit_groups=38,selected_source_blocks=len(referenced),Browser_IDs=len(browser),links=links,preserved_old_files=25,frozen_qualified_occurrences=frozen,active_asof_occurrences=14-frozen,negative_fixtures=rejected,watched_paths=len(watched),all_unchanged=True,actual_nonnull=0,executed=0,complete_topics=0,writes=False),indent=2))
if __name__=='__main__':main()
