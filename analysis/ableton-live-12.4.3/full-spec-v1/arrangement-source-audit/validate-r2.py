"""Read-only focused correction integrity; original R1 validator remains historical."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,re,runpy,subprocess,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3]
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pin(p,r):assert dg(p)=={k:r[k] for k in ['bytes','sha256']},str(p)
def tree():return {str(p.relative_to(P)):dg(p) for p in P.iterdir() if p.is_file()}
def differences(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):
  assert set(a)==set(b);return [q for k in a for q in differences(a[k],b[k],p+'/'+k)]
 if isinstance(a,list):
  assert len(a)==len(b);return [q for i,(x,y) in enumerate(zip(a,b)) for q in differences(x,y,p+'/'+str(i))]
 return [] if a==b else [p]
def main():
 assert sys.dont_write_bytecode and len(sys.argv)==1
 before=tree();pins=load(P/'input-pins.json');external_before={r['path']:dg(ROOT/r['path']) for r in pins}
 for r in pins:pin(ROOT/r['path'],r)
 old=load(P/'manifest.json');preserve=load(P/'preservation-r1.json');assert dg(P/'manifest.json')['sha256']==preserve['manifest_sha256']=='d86dad9a12cb997c771b51d99adcb285fca85b301ce6553f1ee09226bf8905d3'
 assert len(old['files'])==31 and old['files']==preserve['files']
 for n,r in old['files'].items():pin(P/n,r)
 assert dg(P/'review-r1.json')['sha256']==preserve['review_sha256']=='8b603617d4d24108f8ab0482855f3968beb0c5662f23dcc0b3d2eae75b937414'
 review=load(P/'review-r1.json');assert 'ASA-REVIEW-001' in json.dumps(review)
 d=runpy.run_path(str(P/'derive-r2.py'));plan=load(P/'claim-plan-r2.json');claims=load(P/'claims-r2.json');d['verify'](plan,claims)
 actual=[dict(file=n,json_pointer=p) for n,oldn in [('claim-plan-r2.json','claim-plan.json'),('claims-r2.json','claims.json')] for p in differences(load(P/oldn),load(P/n))]
 delta=load(P/'delta-r2.json')['deltas'];assert actual==[{k:r[k] for k in ['file','json_pointer']} for r in delta] and len(delta)==6
 oldplan=load(P/'claim-plan.json');oldclaims=load(P/'claims.json')
 ptr=runpy.run_path(str(P/'derive.py'))['pointer']
 for r in delta:
  olddata=oldplan if r['file']=='claim-plan-r2.json' else oldclaims;newdata=plan if r['file']=='claim-plan-r2.json' else claims
  assert ptr(olddata,r['json_pointer'])==r['before'] and ptr(newdata,r['json_pointer'])==r['after']==d['ASSESSMENT']
 rejected=0
 for mutation in ['old-overclaim','borrow-later-case','change-source-contract','change-unrelated-assessment']:
  pp,cc=deepcopy(plan),deepcopy(claims)
  if mutation=='old-overclaim':pp['CON-B032'][0]['assessment']=oldplan['CON-B032'][0]['assessment']
  elif mutation=='borrow-later-case':next(c for c in cc if c['id']=='ASA-C270')['selected_external_contexts'][0]['id']='SV-041'
  elif mutation=='change-source-contract':next(c for c in cc if c['id']=='ASA-C271')['source_excerpt']='Only sequential launch supported'
  else:cc[0]['assessment']='unrelated changed'
  try:d['verify'](pp,cc)
  except AssertionError:rejected+=1
  else:raise AssertionError('Mutation accepted: '+mutation)
 assert rejected==4
 # Replay unchanged pure R1 derivation, not the old exact-tree validator which predates additions.
 replay=subprocess.run(['python3','-B',str(P/'derive.py'),'--check'],capture_output=True,text=True);assert replay.returncode==0,replay.stdout+replay.stderr
 if (P/'manifest-author-r2.json').exists():
  mf=load(P/'manifest-author-r2.json');assert set(before)==set(mf['files'])|{'manifest-author-r2.json'}
  for n,r in mf['files'].items():pin(P/n,r)
 links=0
 for target in re.findall(r'\]\(([^)]+)\)',(P/'README-r2.md').read_text()):
  if re.match(r'^[A-Za-z]+:',target):continue
  assert (P/target.split('#')[0]).is_file();links+=1
 for f in P.iterdir():
  if f.is_file() and f.name not in old['files'] and f.name!='manifest.json':
   if f.suffix=='.json':load(f)
   r=subprocess.run(['git','diff','--no-index','--check','/dev/null',str(f)],capture_output=True,text=True);assert not r.stdout and not r.stderr and r.returncode in (0,1)
 assert before==tree() and external_before=={r['path']:dg(ROOT/r['path']) for r in pins}
 print(json.dumps(dict(status='pass',sealed=(P/'manifest-author-r2.json').exists(),scope='ASA-REVIEW-001 only; no new full semantic approval',preserved_R1_payloads=31,preserved_R1_seal=True,review_preserved=True,assessment_field_deltas=6,source_case_pointer_ID_status_counts_unchanged=True,input_pins=len(pins),old_pure_derivation_replay=True,old_exact_tree_validator_invoked=False,negative_fixtures=rejected,README_links=links,all_packet_and_inputs_unchanged=True,watched_paths=len(before)+len(pins),writes=False,original_runtime_native_hardware_network_candidate_execution=False),indent=2))
if __name__=='__main__':main()
