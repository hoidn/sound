"""Independent stdlib data arithmetic only. No supplied functions or CLI imports."""
from pathlib import Path
import datetime,hashlib,json,math,struct,sys
if sys.argv[1:]!=['--check']:raise SystemExit('Only --check; no supplied code replay.')
ROOT=Path('/home/ollie/Documents/sound');BASE=ROOT/'analysis/ableton-live-12.4.3';F=BASE/'full-spec-v1'
STAGE=BASE/'handoff-staging/device-corpus-v5-r2';PRE=BASE/'handoff-staging/device-corpus-v5-r2-analysis/preflight';NUM=PRE.parent/'numeric-validation'
RE=F/'reviews/corpus-v5-r2-root-numeric-execution';METHOD=F/'depth-corpus-pickup-step-method-validation'
OLD=F/'reviews/corpus-v4-handoff-review-cli-evidence/stdout.json'
OUT=F/'reviews/corpus-v5-content-and-results-review-evidence.json';assert not OUT.exists()
STEP='1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
AXES=[('preL',4096,8192,0),('preR',4096,8192,1),('postL',8192,16384,0),('postR',8192,16384,1)]
ORDER=[0,2,1,3];LABELS=['left pickup pre waveform','left pickup post waveform','right pickup pre waveform','right pickup post waveform']
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pairs(items):
 d={}
 for k,v in items:assert k not in d;d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=pairs)
def exact(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def fingerprint(rows):return hashlib.sha256(exact(rows).encode()).hexdigest()
root_before=load(RE/'watch-before.json');root_after=load(RE/'watch-after.json');assert root_before==root_after and len(root_before)==2382
assert len({r['path'] for r in root_before})==len(root_before)
inner_before=load(NUM/'watch-before.json');inner_after=load(NUM/'watch-after.json');assert inner_before==inner_after and len(inner_before)==294
assert all(path==row['path'] for path,row in inner_before.items())
watched={Path(r['path']) for r in root_before}|set(RE.iterdir())|set(NUM.iterdir())|{Path(__file__),OLD,F/'reviews/corpus-v4-handoff-review-cli-addendum.json'}
assert all(p.is_file() for p in watched)
before=[ident(p) for p in sorted(watched)]
assert ident(STAGE/'manifest.json')['sha256']=='f3638adab97494b60654270224d1a5dd5100f5a62a44db8272efe8e3804292b0'
assert ident(PRE/'manifest.json')['sha256']=='174b6a499c243ba13cbcc87c3643945968371f43dcee6e5f3c1ba3bbb57ca37e'
assert ident(NUM/'manifest.json')['sha256']=='dec9d54c036f973b7c27d05188ddaa7fd568aba67adc6d5f1f5bd3942725451e'
for directory in [STAGE,PRE,METHOD,NUM]:
 records=load(directory/'manifest.json')['files']
 listed={str((directory/r['path']).resolve()) for r in records}
 actual={str(p.resolve()) for p in directory.rglob('*') if p.is_file() and p!=directory/'manifest.json'}
 assert listed==actual
 for row in records:
  got=ident(directory/row['path']);assert got['bytes']==row['bytes'] and got['sha256']==row['sha256']
selection=load(RE/'selection.json');attempt=load(RE/'attempt.json');pid=load(RE/'returned-pid.json');receipt=load(RE/'receipt.json');inner_attempt=load(NUM/'attempt.json')
assert selection['argv']==attempt['argv'] and selection['argv'][-1]==ident(PRE/'manifest.json')['sha256']
assert receipt['exit']==0 and receipt['exception'] is None and receipt['pid']==pid['pid']
assert selection['selected_utc']<=attempt['attempted_utc']<=pid['utc']<=inner_attempt['utc']<=receipt['finished_utc']
assert receipt['original_Corpus_children_after']==selection['original_Corpus_children_before']==17 and receipt['new_original_or_candidate_calls']==0
for name in ['stdout','stderr']:assert ident(RE/receipt[name]['path'])==receipt[name]
assert (RE/'stderr').read_bytes()==(NUM/'public-cli.stderr.txt').read_bytes()==b''
assert load(NUM/'receipt.json')['status']=='PASS' and load(NUM/'public-cli-receipt.json')['exit']==0
assert ident(OLD)['sha256']=='2bb209cdc0d696061d705386ab391f10193e588b7ae010ec6ddcc31d004c8759'
new=load(NUM/'public-cli.stdout.json');old=load(OLD)
assert new['pass'] and old['pass'] and len(new['results'])==73 and len(old['results'])==72
assert exact(new['results'][:72])==exact(old['results'])
assert all(r['pass'] and all(m['pass'] and math.isfinite(m['error']) and m['error']<=m['tolerance'] for m in r['measurements']) for r in new['results'])
measurements=[m for r in new['results'] for m in r['measurements']]
assert len(measurements)==4799 and sum(m['error']!=0 for m in measurements)==311
assert sum(len(r['measurements']) for r in old['results'])==4795
assert [m['check'] for m in new['results'][-1]['measurements']]==LABELS
assert all(m['error']==0 and m['tolerance']==.01 for m in new['results'][-1]['measurements'])
source=load(METHOD/'results.json');public=load(NUM/'controls.json');assert len(source['comparisons'])==len(public['comparisons'])==38 and public['complete']
by_hash={}
for row in load(METHOD/'manifest.json')['files']:
 if row['path'].endswith('.f32'):by_hash.setdefault(row['sha256'],METHOD/row['path'])
def decode(path):
 raw=path.read_bytes()
 if len(raw)!=131072:return None,path.name+': expected exactly 16384 stereo frames'
 values=struct.unpack('<32768f',raw)
 if not all(math.isfinite(x) for x in values):return None,path.name+': non-finite sample'
 return values,None
checks=[];valid_records=0;invalid_records=0;own_axis_measurements=0
for i,(s,p) in enumerate(zip(source['comparisons'],public['comparisons'])):
 assert s['name']==p['name'] and p['source_expected']==s['result'] and p['match'] is True
 path=Path(s['path']);ref=by_hash[s['reference_sha256']]
 assert ident(path)['bytes']==s['bytes'] and ident(path)['sha256']==s['sha256']
 y,invalid=decode(path);r,ref_invalid=decode(ref)
 invalid=invalid or ref_invalid
 guard=not s['synthetic_arithmetic_only'] and s['reference_sha256']!=STEP
 axes=[]
 if invalid is None and not guard:
  for axis,lo,hi,ch in AXES:
   yr=y[2*lo+ch:2*hi:2];rr=r[2*lo+ch:2*hi:2]
   R=math.fsum(x*x for x in rr);Y=math.fsum(x*x for x in yr)
   D=math.fsum((a-b)*(a-b) for a,b in zip(yr,rr))
   E=math.sqrt(D/R) if R>0 and Y>0 else None
   axes.append({'axis':axis,'reference_energy':R,'candidate_energy':Y,'error_energy':D,'error':E,'pass':E is not None and E<=.01})
  if any(a['error'] is None for a in axes):invalid='Pickup step requires positive energy in each window/channel'
 if guard:
  assert invalid is None
  assert p['public_guard_result']=={'id':'CORPUS-AUDIO-027-01','pass':False,'error':'Pickup step reference hash differs from the pinned capture'}
  invalid_records+=1
 elif invalid is not None:
  assert p['public_invalid']==invalid and not s['result']['valid'] and not s['result']['pass']
  assert 'public_result' not in p;invalid_records+=1
 else:
  expected=[{'check':label,'error':axes[index]['error'],'tolerance':.01,'pass':axes[index]['pass']} for label,index in zip(LABELS,ORDER)]
  assert p['public_result']=={'pass':all(a['pass'] for a in axes),'measurements':expected}
  for a,original in zip(axes,s['result']['axes']):
   assert all(a[k]==original[k] for k in ['axis','reference_energy','candidate_energy','error_energy','error','pass'])
  valid_records+=1;own_axis_measurements+=4
 checks.append({'pointer':'/comparisons/'+str(i),'name':s['name'],'guard_refusal':guard,'whole_case_invalid':invalid,'independent_axes':axes,'exact_public_agreement':True})
assert valid_records==24 and invalid_records==14 and own_axis_measurements==96
messages={'ramp_waveform':('CORPUS-AUDIO-020-02','Ramp reference hash differs from the pinned capture'),'noteoff_decay_zero_waveform':('CORPUS-AUDIO-026-01','NoteOff zero endpoint reference hash differs from the pinned capture'),'pickup_step_waveform':('CORPUS-AUDIO-027-01','Pickup step reference hash differs from the pinned capture')}
assert len(public['strict_hash_guards'])==3
for row in public['strict_hash_guards']:
 name,error=messages[row['kind']];assert row['result']=={'id':name,'pass':False,'error':error}
published=[r for r in root_before if str(Path(r['path'])).startswith(str(ROOT/'handoff')+'/')]
release_dirs={Path(r['path']).relative_to(ROOT/'handoff').parts[0] for r in published if len(Path(r['path']).relative_to(ROOT/'handoff').parts)>1}
assert len(release_dirs)==33
for row in published:assert ident(Path(row['path']))==row
# No historical mutable wiki path is compared to its old map as a future gate.
after=[ident(p) for p in sorted(watched)];assert before==after
summary=load(NUM/'summary.json');assert summary['evaluations']==73 and summary['measurements']==4799 and summary['controls']==38 and summary['hash_guard_controls']==3
result={'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS independent new-metric arithmetic, exact old-result data and preservation','stage_manifest':ident(STAGE/'manifest.json'),'preflight_manifest':ident(PRE/'manifest.json'),'numeric_manifest':ident(NUM/'manifest.json'),'numeric_stdout':ident(NUM/'public-cli.stdout.json'),'controls':ident(NUM/'controls.json'),'old_v4_stdout':ident(OLD),'old72_full_result_objects_exact':True,'old_measurements':4795,'new_measurements':4,'total_measurements':4799,'nonzero_self_errors':311,'max_self_error':max(m['error'] for m in measurements),'new_self':new['results'][-1],'independent_controls':checks,'whole_valid_controls':valid_records,'whole_invalid_controls':invalid_records,'emitted_control_axis_measurements':own_axis_measurements,'strict_guards':public['strict_hash_guards'],'root_paired_paths':2382,'inner_paired_paths':294,'published_files_current_verified':len(published),'published_release_trees':len(release_dirs),'own_watch_count':len(before),'own_before_fingerprint':fingerprint(before),'own_after_fingerprint':fingerprint(after),'own_changed':[],'watch_enumeration':'Paths from pinned Root before-map plus Root receipt files, numeric result files, current reviewer checker and oldv4stdout/addendum; hashes captured immediately before and after the independent check. Root paired maps retained separately.','root_before_map':ident(RE/'watch-before.json'),'root_after_map':ident(RE/'watch-after.json'),'inner_before_map':ident(NUM/'watch-before.json'),'inner_after_map':ident(NUM/'watch-after.json'),'supplied_tool_or_model_replays':0,'new_original_calls':0,'candidate_or_application_grade':None}
with OUT.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['independent_controls','strict_guards','new_self']},indent=2))
