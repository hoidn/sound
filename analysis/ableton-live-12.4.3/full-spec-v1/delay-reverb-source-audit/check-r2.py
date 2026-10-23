"""Focused read-only successor view. Select inspected pure analyst definitions, never old main."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import ast,collections,json,sys
A=Path(__file__).resolve().parent;P=A.parent;R=P.parents[2];D=P/'delay-reverb'
def j(p):return json.loads(p.read_text())
def path(s):return Path(s) if Path(s).is_absolute() else R/s
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def samepin(q):assert dg(path(q['path']))=={k:q[k] for k in ['bytes','sha256']},q['path']
CORRECTED='005 actually toggles Filter and inspects the named Freq/Width, X/Y and slider control roles under wet F2. Its action does not unambiguously perform X/Y drags or Freq/Width slider changes: those documented gestures remain unexercised/U. Preserve genuine effect-positive prerequisites; filter response, values, geometry and all numeric outcomes remain unknown.'
def apply(original,response):
 out=deepcopy(original);change=response['changes'][0]
 assert out['assessments'][8]['assessment']==change['before']
 out['assessments'][8]['assessment']=change['after'];return out

def focused(a,p):
 # Independent semantic guard also rejects a jointly edited plan+audit.
 for v in (a,p):
  x=v['assessments'][8];assert x['id']=='DRA-A009' and x['block']=='FX:B318'
  assert x['assessment']==CORRECTED
  assert all(x[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and x['target']=='U' and not x['executed'] and not x['complete'] and x['coverage_credit']==0
 c=a['owner_cases'][4];assert c['id']=='DR-DELAY-005'
 assert c['action']=='Inspect Freq/Width via X/Y and sliders, and toggle Filter. For any audio comparison use F2, 100% wet and nonzero delay output, rather than a silent source.'
 assert c['expected']=='Both input methods expose the named center/bandwidth controls; the Filter switch enables/disables this path.'
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; unsupported arguments refused before input reads'
 response=j(A/'response-r2.json');ins=j(A/'inputs.json');old=j(A/'audit.json');oldplan=j(A/'plan.json')
 watch={path(q['path']) for q in ins['files']}|{path(q['path']) for q in response['preserved_r1_files']}|{path(response['review']['path'])}|{p for p in A.iterdir() if p.is_file()}
 before={str(p):dg(p) for p in watch}
 for q in ins['files']+response['preserved_r1_files']+[response['review'],response['prior_manifest']]:samepin(q)
 assert len(response['preserved_r1_files'])==6 and len(ins['files'])==82
 assert response['prior_manifest']['sha256']=='6b9ef60cf2d6c862d11927b3e49c750d128565b479dfd16742449bef36df6e36'
 assert response['review']['sha256']=='f978dbbedfa0eaa570e3564d82dfa6cfdcc395c818ab8d8c9ef098883d2b054e'
 assert len(response['changes'])==1 and response['changes'][0]['json_pointer']=='/assessments/8/assessment' and response['changes'][0]['after']==CORRECTED
 assert response['changes'][0]['logical_documents']==['audit.json','plan.json']
 assert all(response[k] is None for k in ['documentary_expected','documentary_comparison','actual_expected','actual_comparison']) and response['target']=='U' and not response['executed'] and not response['complete'] and response['coverage_credit']==response['new_cases']==0 and response['new_normative_IDs']==[]
 for q in j(A/'manifest.json')['files']:samepin(q)
 a=apply(old,response);p=apply(oldplan,response);focused(a,p)
 for original,current in [(old,a),(oldplan,p)]:
  restored=deepcopy(current);restored['assessments'][8]['assessment']=original['assessments'][8]['assessment'];assert restored==original
 # R1 definitions j/path/dg/ptr/shape fully read before selective extraction. No imports, assignments, main or guard compiled from R1.
 assert dg(A/'check.py')['sha256']=='e51e5efa0c768cf831517bba37fedf8687602cca9e35045acd3329bb5238ac78'
 tree=ast.parse((A/'check.py').read_text());selected=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'j','path','dg','ptr','shape'}]
 assert [n.name for n in selected]==['j','path','dg','ptr','shape']
 ns=dict(A=A,P=P,R=R,D=D,Path=Path,sha256=sha256,json=json,collections=collections)
 exec(compile(ast.Module(body=selected,type_ignores=[]),'<inspected R1 pure definitions only>','exec'),ns)
 ns['shape'](a,p)
 rejected=[]
 for name,text in [('inspection-promoted-to-operation',response['changes'][0]['before']),('unqualified-slider-action','005 actually drags X/Y and changes both sliders'),('erase-true-toggle','No existing filter action is present')]:
  bad=deepcopy(a);bp=deepcopy(p);bad['assessments'][8]['assessment']=bp['assessments'][8]['assessment']=text
  try:focused(bad,bp)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe dual mutation accepted '+name)
 assert a['owner_cases']==old['owner_cases'] and a['owner_requirements']==old['owner_requirements'] and a['proposals']==old['proposals'] and a['source_questions']==old['source_questions']
 for name in ['response-r2.json','check-r2.py','README-r2.md']:
  assert all(l.rstrip()==l for l in (A/name).read_text().splitlines()),name
 if (A/'manifest-r2.json').exists():
  mf=j(A/'manifest-r2.json');assert len(mf['files'])==3
  for q in mf['files']:samepin(q)
  assert {p.name for p in A.iterdir() if p.is_file()}=={Path(q['path']).name for q in response['preserved_r1_files']}|{'response-r2.json','check-r2.py','README-r2.md','manifest-r2.json'}
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',sealed=(A/'manifest-r2.json').exists(),logical_field_changes_per_document=1,preserved_R1_files=6,immutable_inputs=82,requirements=92,cases=149,assessments=207,proposals=26,questions=7,all_new_oracles_null=True,all_target_U=True,adoption=0,negative_fixtures=rejected,preserved_true='Filter toggle and named control-role inspection',AST_selected_R1_definitions=[n.name for n in selected],old_main_import_replay=False,watched_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
