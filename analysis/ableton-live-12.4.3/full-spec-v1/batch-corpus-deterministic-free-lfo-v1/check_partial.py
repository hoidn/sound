#!/usr/bin/env python3
"""Additive retained-data-only partial readback; frozen complete-run guard remains failed."""
import copy,hashlib,json,math,pathlib,re,struct,sys
sys.dont_write_bytecode=True
import record as rec
H=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((H/n).read_text())
def own(pin):
 p=pathlib.Path(pin['path']);assert p.is_relative_to(H);b=p.read_bytes();assert len(b)==pin['bytes'] and rec.sha(b)==pin['sha256']
def readback(d,a):
 rec.validate(d);assert a['status']=='STOPPED-NO-RETRY' and a['error']=={'type':'AssertionError','message':''}
 assert len(a['children'])==1 and [x.name for x in (H/'attempts').iterdir()]==['shape-1']
 assert a['phases']=={'validated':True,'custody_before':True,'calls_started':True,'all_children_completed':False,'custody_after':False}
 assert a['custody_after_failure']==a['custody_before']==load('context.json')['watched']+load('manifest-before.json')['frozen_files']
 c=a['children'][0];assert c['shape']==1 and c['pid']>0 and c['exit']==0 and not c['timeout'] and c['status']=='RUNNING' and 'parsed' not in c and 'audio_stats' not in c
 # RUNNING is retained recorder status; process has exited, but postparse RECORDED was not reached.
 ctx=load('context.json');p=d['plans'][0];assert c['argv']==[ctx['exe'],ctx['bundle'],p['script'],str(H/'attempts/shape-1/output.f32'),'--imports']
 for key in ('stdout','stderr','audio'):own(c[key])
 text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert err==''
 imports=[];exports={};inits=[];used={};commands=[]
 for line in text.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line)
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'kind':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1] not in exports;exports[m[1]]=m[2]
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) (\d+)',line);assert m and m[1] not in used;used[m[1]]=int(m[2])
  else:commands.append(line)
 assert len(imports)==127 and len({x['symbol'] for x in imports})==127 and sum(x['kind']=='trap' for x in imports)==21
 assert set(used)<={x['symbol'] for x in imports if x['kind']=='linux'} and all(v>0 for v in used.values())
 assert set(exports)=={'_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'}
 assert commands[:4]==['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok']
 m=re.fullmatch(r'rate 44100 ret=(-?\d+)',commands[4]);assert m;rate_return=int(m[1])
 params=[];vector=d['base_params'].copy();vector[18]=1
 for i,line in enumerate(commands[5:43]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and rec.bits(float(m[2]))==rec.bits(vector[i]);params.append({'index':i,'token':m[2],'bits32':rec.bits(float(m[2]))})
 assert len(params)==38 and commands[43:]==['inflag 1','input '+d['base_script'].split('\ninput ')[1].splitlines()[0],'process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy','cxx-failbits 0']
 # Reproduce only the frozen DATA parser rejection, never an original call or changed guard.
 try:rec.parse_output(text,err,c['exit'],p,d)
 except AssertionError:guard_failed=True
 else:guard_failed=False
 assert guard_failed and rate_return!=0
 stats=rec.audio(c['audio']['path']);assert all(s['finite'] for s in stats['channels'])
 return {'status':'PARTIAL_RETAINED_FULL_BATCH_GUARD_FAILED_NO_RETRY','attempted_shape':1,'unlaunched_shapes':[2,4],'observed_direct_exports':73,'observed_CalcA':32,'planned_direct_exports':219,'planned_CalcA':96,'rate_return_observed':rate_return,'frozen_guard_required_rate_return':0,'frozen_data_guard_rejection_reproduced':guard_failed,'child_exit_nonzero':False,'native_function_failure_meaning':None,'full_selected_class_completed':False,'audio':c['audio'],'audio_stats':stats,'parameters':params,'exports':exports,'imports':imports,'used_imports':used,'initializers':inits,'commands':commands,'pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'prior_waveform_expected':None,'portable_comparator':None,'independent_shape_or_rate_meaning':None,'custody_after_failure_equal':True,'diagnosis':'Author bookkeeping guard overconstrained opaque SetSampleRateU return to0. Actual Rate returned1, process returned0/flag1 for32blocks. No shape/native failure or semantic Rate-success law is inferred. Frozen guard/code/NULL priors/stop status stay unchanged; no retry or later launch.'}
def controls(d,a):
 out=[]
 for label,mut in [('false-complete',lambda x:x.update(status='COMPLETE-ONCE-NO-RETRY')),('invented-child',lambda x:x['children'].append(copy.deepcopy(x['children'][0]))),('wrong-shape',lambda x:x['children'][0].update(shape=2)),('failed-child',lambda x:x['children'][0].update(exit=1)),('timeout',lambda x:x['children'][0].update(timeout=True)),('missing-custody',lambda x:x.pop('custody_after_failure')),('changed-custody',lambda x:x['custody_after_failure'][0].update(sha256='0'*64)),('raw-hash',lambda x:x['children'][0]['audio'].update(sha256='0'*64)),('false-all-children-phase',lambda x:x['phases'].update(all_children_completed=True)),('claimed-parser-success',lambda x:x['children'][0].update(parsed={}))]:
  z=copy.deepcopy(a);mut(z)
  try:readback(d,z)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(label)
  else:raise AssertionError('invalid partial accepted '+label)
 return out
def main():
 assert sys.argv[1:]==['--check'];d=load('inputs.json');a=load('results.json')
 for p in load('manifest-before.json')['frozen_files']:own(p)
 observed=readback(d,a);report={'status':'PASS_PARTIAL_INTEGRITY_NOT_COMPLETE_BATCH','input_negatives':rec.input_controls(d),'partial_negatives':controls(d,a),'attempted_children':1,'unlaunched':2,'original_calls_by_checker':0,'outside_runtime_source_oldaudio_reads':0,'frozen_complete_guard':'still fails, reproduced unchanged','native_oracle_failure_claim':False}
 if (H/'manifest.json').exists():
  m=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in m['files']}
  for f in m['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and rec.sha(b)==f['sha256']
  assert load('partial-readback.json')==observed and load('partial-author-check.json')==report
 else:rec.save(H/'partial-readback.json',observed);rec.save(H/'partial-author-check.json',report)
 print(json.dumps(report))
if __name__=='__main__':main()
