"""Current bounded Recording R4 integrity; no old tools/parser/runtime or writes."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
from collections import Counter
import ast, json, re, sys
P=Path(__file__).resolve().parent;R=P.parents[3];A=P.parent/'recording-comping-source-audit'
def j(p):return json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,path):
 assert path.startswith('/')
 for k in path.split('/')[1:]:
  if isinstance(v,list):assert re.fullmatch(r'0|[1-9][0-9]*',k);v=v[int(k)]
  else:v=v[k.replace('~1','/').replace('~0','~')]
 return v
def reqs(text):
 out=[]
 for m in re.finditer(r'^### (REQ-RECORDING-COMPING-\d{3}) — ([^\n]+)\n',text,re.M):
  n=re.search(r'^### |^## ',text[m.end():],re.M);end=len(text) if n is None else m.end()+n.start();out.append(dict(id=m.group(1),title=m.group(2),contract=text[m.end():end].strip(),raw_start=m.start(),raw_end=end,quote=text[m.start():end],line=text[:m.start()].count('\n')+1))
 return out
def validate(req,c,f,ad,a):
 assert req[:32]==reqs((P/'spec-r3.md').read_text()) and len(req)==34
 old=j(P/'cases-r3.json')['records'];assert c[:81]==old and len(c)==90 and len({x['id'] for x in c})==90
 assert [r['id'] for r in req[-2:]]==['REQ-RECORDING-COMPING-033','REQ-RECORDING-COMPING-034']
 assert 'Left Arrow' in req[-2]['contract'] and 'folds all take lanes' in req[-2]['contract']
 assert 'sequential tracks' in req[-1]['contract'] and 'not a claim about multi-MIDI-file distribution' in req[-1]['contract']
 assert req[-2]['source_references']==[dict(path=str((A/'audit.json').relative_to(R)),pointer='/blocks/7',block_id='CMP:B008')]
 assert req[-1]['source_references']==[dict(path=str((A/'audit.json').relative_to(R)),pointer='/blocks/25',block_id='CMP:B026')]
 for r in req[-2:]:
  for ref in r['source_references']:assert ptr(j(R/ref['path']),ref['pointer'])['id']==ref['block_id']
 route={'G01':'019,033','G02':'020','G03':'020','G04':'020','G06':'034','G07':'021','G08':'022,023','G09':'022','G10':'025'}
 common=f['current_version_overlay']['policy'];assert all(s in common for s in ['EACH genuine NONEMPTY','BOTH independently productive','NONZERO nonmuted','not flags, presets or meters','UI-only'])
 for index,x in enumerate(c[81:],82):
  assert x['id']==f'RC-{index:03}' and x['requirement_suffix']==route[x['adoption_group']]
  ref=x['reviewed_proposal'];g=ptr(j(R/ref['path']),ref['pointer']);assert g['id']==ref['id']==x['adoption_group']
  assert x['action']==g['proposed_action'] and x['setup']==common+g['positive_baseline'] and x['source_limits_asof']==g['limits']
  assert all(x[k] is None for k in ['documentary_comparator_or_unknown','expected','comparison','documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and x['target_grade']=='U' and not x['executed']
  assert x['fixture']=='fixtures-r4.json#/current_version_overlay' and ptr(f,x['fixture'].split('#')[1])==f['current_version_overlay']
  want=[dict(path=str((A/'audit.json').relative_to(R)),pointer=s['pointer'],block_id=s['id'],text_sha256=s['text_sha256']) for s in g['source_references']];assert x['source_references']==want
  for s in want:
   b=ptr(j(R/s['path']),s['pointer']);assert b['id']==s['block_id'] and sha256(b['text'].encode()).hexdigest()==s['text_sha256']
 assert Counter(x['kind']=='F' for x in c)=={False:86,True:4}
 assert f['actual_oracles']==[dict(id=x['id'],expected=None,comparison=None,target='U',executed=False,role='historical-artifact-only' if x['kind']=='F' else 'planned-application-probe') for x in c]
 ov=f['current_version_overlay'];assert all(t in ov['recording_refinement'] for t in ['genuinely completed NONEMPTY NONZERO','BOTH distinct takes and main comp','no greedy allocation'])
 assert all(t in ov['highlight_refinement'] for t in ['FIRST establish actual visible highlights','BOTH distinct source takes and adjacent comp pieces','mismatch outcome remain U'])
 assert 'Four old kind F' in ov['historical_roles'] and '86 application cases ungraded' in ov['historical_roles']
 assert len(ad['groups'])==13 and ad['source_questions']==f['source_questions']==a['source_questions'] and not ad['complete'] and not ad['coverage_credit']
 for n,(row,g) in enumerate(zip(ad['groups'],a['proposals'])):
  assert row['id']==g['id'] and row['audit_pointer']==f'/proposals/{n}' and ptr(a,row['audit_pointer'])==g
  assert row['new_cases']==[x['id'] for x in c[81:] if x['adoption_group']==row['id']]
  assert row['overlay_only']==(g['id'] in ['G05','G11']) and row['unadopted']==(g['id'] in ['G12','G13'])
  assert all(row[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and not row['executed'] and not row['complete'] and not row['coverage_credit']
 assert 'AS OF SOURCE AUDIT FREEZE' in ad['historical_source_audit']
 return True
def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before inputs'
 inp=j(P/'inputs-r4.json');paths={R/p for p in inp['files']}|{p for p in P.rglob('*') if p.is_file()}|{R/'wiki/specs/recording-comping.md',R/'wiki/research/recording-comping.md'};before={str(p):dg(p) for p in paths}
 assert len(inp['old_packet_files'])==26 and len(inp['files'])==41
 for path,row in inp['files'].items():assert dg(R/path)==row,path
 for path,row in inp['old_packet_files'].items():assert dg(R/path)==row,path
 assert inp['approved_source_review']['sha256']=='4b90b691afd85fac2ca8e18138548898a70b61c6541094819e7fe9e960b49e25'
 req=j(P/'requirements-r4.json');c=j(P/'cases-r4.json')['records'];f=j(P/'fixtures-r4.json');ad=j(P/'adoption-r4.json');a=j(A/'audit.json');validate(req,c,f,ad,a)
 delta=j(P/'delta-r4.json');render=delta['canonical_delta']
 for kind,folder in [('spec','specs'),('research','research')]:
  old=(P/f'{kind}-r3.md').read_text();end=old.index('\n',old.index('\n# ')+1);want=(old[:end]+'\n'+render['intro']+old[end:]+render['append']).replace('revision: 3\n','revision: 4\n',1)
  assert want==(P/f'{kind}-r4.md').read_text()==(R/f'wiki/{folder}/recording-comping.md').read_text()
  assert 'historical R3 context' in want and 'AS OF AUTHOR FREEZE' in want
 spec=(P/'spec-r4.md').read_text();current=reqs(spec);assert len(current)==34 and all(current[i]['contract']==r['contract'] for i,r in enumerate(req[:32]))
 assert all(r['contract'] in spec for r in req[-2:])
 tree=ast.parse((R/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4;env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-inspected-pure-browser-definitions','exec'),env);assert {r['id'] for r in env['spec_rows'](P/'spec-r4.md',spec)}=={r['id'] for r in req}
 variants=[('oldclause',lambda r,c,f,a:r[0].update(contract='changed')),('oldaction',lambda r,c,f,a:c[0].update(action='changed')),('neworacle',lambda r,c,f,a:c[81].update(documentary_expected='pass')),('actualoracle',lambda r,c,f,a:f['actual_oracles'][0].update(expected='pass')),('file-to-application',lambda r,c,f,a:f['actual_oracles'][60].update(role='planned-application-probe')),('no-positive',lambda r,c,f,a:c[81].update(setup='enabled flag')),('sequential-take-lanes',lambda r,c,f,a:r[-1].update(contract='all MIDI files enter sequential take lanes')),('global-Left',lambda r,c,f,a:r[-2].update(contract='Global Left key always folds')),('wrong-source',lambda r,c,f,a:c[81]['source_references'][0].update(pointer='/cases/0')),('no-record-positive',lambda r,c,f,a:f['current_version_overlay'].update(recording_refinement='flags enough')),('TakeId-enough',lambda r,c,f,a:f['current_version_overlay'].update(highlight_refinement='Shared TakeId enough')),('color-adopted',lambda r,c,f,a:a['groups'][11].update(unadopted=False)),('completegroup',lambda r,c,f,a:a['groups'][0].update(complete=True)),('inspection-only',lambda r,c,f,a:c[81].update(action='Inspect listed commands'))]
 for name,change in variants:
  rr,cc,ff,aa=deepcopy((req,c,f,ad));change(rr,cc,ff,aa)
  try:validate(rr,cc,ff,aa,a)
  except (AssertionError,KeyError,IndexError):pass
  else:raise AssertionError('Unsafe variant accepted '+name)
 links=0;pending=[]
 for p in [P/'README-r4.md',R/'wiki/specs/recording-comping.md',R/'wiki/research/recording-comping.md']:
  for dest in re.findall(r'\]\(([^)\s]+)\)',p.read_text()):
   if re.match(r'(https?://|#|mailto:)',dest):continue
   target=(p.parent/dest.split('#')[0]).resolve()
   if target==P/'manifest-author-r4.json' and not target.exists():pending.append(str(target));continue
   assert target.exists(),(p,dest);links+=1
 currentfiles=[p for p in P.rglob('*') if p.is_file()]
 for p in currentfiles:
  if str(p.relative_to(R)) not in inp['old_packet_files']:
   b=p.read_bytes();assert b.endswith(b'\n') and b'\0' not in b and all(s.rstrip(b' \t')==s for s in b.splitlines()),p
 sealed=(P/'manifest-author-r4.json').exists()
 if sealed:
  m=j(P/'manifest-author-r4.json');assert set(m['payloads'])=={str(p.relative_to(R)) for p in currentfiles if p.name!='manifest-author-r4.json'}
  for path,row in m['payloads'].items():assert dg(R/path)==row,path
 assert before=={str(p):dg(p) for p in paths}
 print(json.dumps(dict(status='pass',sealed=sealed,pending_declared_artifacts=pending,requirements=34,old_requirement_objects_exact=32,cases=90,old_case_objects_exact=81,old_files_exact=26,new_documentary_null=9,current_actual_null_U=90,historical_artifact_only=4,ungraded_application_cases=86,case_groups=9,overlay_only_groups=2,unadopted_groups=2,unsafe_fixtures_rejected=[x[0] for x in variants],browser_exact_IDs=34,links=links,input_pins=41,watched_unchanged=len(paths),writes=False,complete=False,scope='Bounded current owner integrity only; independent semantic review pending AS OF AUTHOR FREEZE. No runtime or oldtool execution.'),indent=2))
if __name__=='__main__':main()
