from pathlib import Path
import hashlib, json, re, subprocess, sys, datetime, copy
ROOT=Path('/home/ollie/Documents/sound')
ST=ROOT/'analysis/ableton-live-12.4.3/handoff-staging'
REV=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/reviews'
FINAL=ST/'device-corpus-v5-final'
OLD=ST/'device-corpus-v5-r2'
PRIVATE=ST/'device-corpus-v5-final-analysis'
OUT=REV/'corpus-v5-handoff-final-seal-review-evidence.json'
def ident(p):
 b=p.read_bytes(); return {'path':str(p.relative_to(ROOT)), 'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def files(d):return {str(p.relative_to(d)):p for p in d.rglob('*') if p.is_file()}
def load(p):return json.loads(p.read_text())
def inventory(p):
 m=load(p); fs=files(p.parent); assert set(fs)=={r['path'] for r in m['files']}|{'manifest.json'}
 for r in m['files']:
  got=ident(p.parent/r['path']); assert got['bytes']==r['bytes'] and got['sha256']==r['sha256']
 return len(m['files'])
def fingerprint(rows):return hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def differences(a,b,p=''):
 if type(a)!=type(b): return [p]
 if isinstance(a,dict):
  assert a.keys()==b.keys(); return sum((differences(a[k],b[k],p+'/'+k) for k in a),[])
 if isinstance(a,list):
  if len(a)!=len(b):return [p]
  return sum((differences(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [p]
assert sys.argv[1:]==['--check'] and not OUT.exists()
dirs=[ST/'device-corpus-v5',ST/'device-corpus-v5-analysis/preflight',OLD,ST/'device-corpus-v5-r2-analysis/preflight',ST/'device-corpus-v5-r2-analysis/numeric-validation',FINAL,PRIVATE,ROOT/'handoff']
watched=set(p for d in dirs for p in files(d).values())
pins=load(PRIVATE/'inputs.json')['pins']
watched.update(Path(r['path']) for r in pins)
before=[ident(p) for p in sorted(watched)]
checks={}
checks['stage_payloads']=inventory(FINAL/'manifest.json')
checks['private_payloads']=inventory(PRIVATE/'manifest.json')
assert checks['stage_payloads']==88 and checks['private_payloads']==5
for row in pins:
 got=ident(Path(row['path']));assert (got['bytes'],got['sha256'])==(row['bytes'],row['sha256'])
oldfiles,newfiles=files(OLD),files(FINAL)
assert oldfiles.keys()==newfiles.keys() and len(newfiles)==89
changed=sorted(k for k in newfiles if newfiles[k].read_bytes()!=oldfiles[k].read_bytes())
assert changed==['README.md','REVIEW.md','cases.json','manifest.json','spec.md']
delta=load(PRIVATE/'delta.json');assert changed==delta['only_changed_paths']
for name,record in delta['files'].items():
 for label,base in [('before',OLD),('after',FINAL)]:
  got=ident(base/name);assert (str(base/name),got['bytes'],got['sha256'])==(record[label]['path'],record[label]['bytes'],record[label]['sha256'])
 if record['kind']=='literal-text':
  current=(FINAL/name).read_text()
  for op in reversed(record['operations']):
   assert current.count(op['after'])==1;current=current.replace(op['after'],op['before'],1)
  assert current.encode()==(OLD/name).read_bytes()
 else:
  current=copy.deepcopy(load(FINAL/name))
  for op in record['operations']:
   bits=op['pointer'].lstrip('/').split('/');target=current
   for bit in bits[:-1]:target=target[int(bit)] if isinstance(target,list) else target[bit]
   key=int(bits[-1]) if isinstance(target,list) else bits[-1]
   assert target[key]==op['after'];target[key]=op['before']
  assert (json.dumps(current,indent=2)+'\n').encode()==(OLD/name).read_bytes()
oldm,newm=load(OLD/'manifest.json'),load(FINAL/'manifest.json')
ptrs=differences(oldm,newm)
assert len(ptrs)==17 and set(ptrs)=={o['pointer'] for o in delta['files']['manifest.json']['operations']}
oldc,newc=load(OLD/'cases.json'),load(FINAL/'cases.json')
assert differences(oldc,newc)==['/status'] and oldc['cases']==newc['cases']
assert (OLD/'cases.json').read_text().split('  "cases": [',1)[1]==(FINAL/'cases.json').read_text().split('  "cases": [',1)[1]
assert len(newc['cases'])==27 and sum(len(g['evaluations']) for g in newc['cases'])==73
assert 'author-freeze history' in newc['status']
assets=[k for k in newfiles if k.endswith('.f32')];assert len(assets)==82
assert all(oldfiles[k].read_bytes()==newfiles[k].read_bytes() for k in assets+['compare.py','AGENTS.md'])
a=(OLD/'spec.md').read_text().split('## Input and protocol\n',1)[1].split('## Proposed changes from release4 to release5',1)[0]
b=(FINAL/'spec.md').read_text().split('## Input and protocol\n',1)[1].split('## Changes from release4 to release5',1)[0]
assert a==b
links=[]
for name,p in newfiles.items():
 if p.suffix=='.f32':continue
 t=p.read_text();assert t.endswith('\n') and all(s==s.rstrip() for s in t.splitlines())
 assert not re.search(r'/home/|/tmp/|analysis/|wiki/research/|0x[0-9a-fA-F]{8,}',t)
 if p.suffix=='.md':
  for target in re.findall(r'\]\(([^)]+)\)',t):
   local=target.split('#',1)[0]
   if local and not local.startswith(('http:','https:')):assert (p.parent/local).is_file();links.append([name,target])
review=load(REV/'corpus-v5-content-and-results-review.json')
assert review['required_findings']==[] and review['disposition']=='APPROVED_FINITE_CONTENT_AND_ACTUAL_VALIDATION_PENDING_FINAL_METADATA_SEAL'
assert newm['case_count']==27 and newm['evaluation_count']==73
assert newm['release_status']=='reviewed-finite-scope-ready-for-coordinator-publication'
assert newm['candidate_execution']=='not-run' and newm['supersedes']=='device-corpus-v4'
assert newm['review']['status']=='approved-finite-content-and-actual-validation'
assert '4799measurements' in newm['readiness']['numeric_validation']
assert 'author-freeze history' in newm['readiness']['handoff_review']
assert not (ROOT/'handoff/device-corpus-v5').exists()
command=[sys.executable,'-B',str(PRIVATE/'check_final.py'),'--check']
r=subprocess.run(command,capture_output=True,text=True,timeout=30)
assert r.returncode==0 and not r.stderr
ar=json.loads(r.stdout);assert ar['watched']==317 and ar['links']==14 and ar['numeric_or_audio_execution']==0
refusal=subprocess.run(command[:-1]+['--write'],capture_output=True,text=True,timeout=30)
assert refusal.returncode==1 and not refusal.stdout and 'Read-only --check only' in refusal.stderr
after=[ident(p) for p in sorted(watched)];assert before==after
result={'schema':'corpus-v5-focused-final-seal-own-evidence-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':ident(FINAL/'manifest.json'),'private_manifest':ident(PRIVATE/'manifest.json'),'delta':ident(PRIVATE/'delta.json'),'changed_paths':changed,'unchanged_paths':84,'manifest_leaf_deltas':ptrs,'literal_reversal_all_five':True,'all27_groups_73_evaluations_exact':True,'cases_only_status':True,'F32_exact':82,'compare_AGENTS_exact':True,'normative_body_exact':True,'public_links':links,'all_public_text_sanitized_and_whitespace_clean':True,'author_check':{'argv':command,'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr},'write_refusal':{'argv':command[:-1]+['--write'],'exit':refusal.returncode,'stdout':refusal.stdout,'stderr':refusal.stderr},'own_watch':{'scope':'all files under enumerated directories plus exact final input pins; scoped check interval only','directories':[str(d.relative_to(ROOT)) for d in dirs],'pin_paths':[r['path'] for r in pins],'count':len(before),'before_sha256':fingerprint(before),'after_sha256':fingerprint(after),'unchanged':True},'publication_copy_exists_at_check':False,'numeric_original_collector_comparator_execution':0,'failures':[]}
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS','evidence':ident(OUT),'watched':len(before),'changed':changed,'numeric_replay':False},indent=2))
