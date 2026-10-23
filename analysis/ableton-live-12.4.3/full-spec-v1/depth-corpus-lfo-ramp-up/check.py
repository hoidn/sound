"""Verify retained data only. No native execution, capture imports, writes or replay."""
from pathlib import Path
import copy, datetime, hashlib, json, math, struct, sys
HERE=Path(__file__).resolve().parent
SINE='fadb3e890a943e637f440b83048d80a9153cc428e9c2840775057a0cc383028c'
RAMP='40b77412adfc4768bd18e76e5df330ecd536544c50553212ba3125a8de7982ec'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((HERE/n).read_text())
def ident(path):
 p=Path(path);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def scripts(a,b,proposal):
 assert a==proposal['scripts']['sine-baseline.script'] and b==proposal['scripts']['ramp-up.script']
 assert [(x,y) for x,y in zip(a.splitlines(),b.splitlines()) if x!=y]==[('param 18 0.0','param 18 3.0')]
 assert len(a.splitlines())==len(b.splitlines())
 for text in [a,b]:
  assert [int(x.split()[1]) for x in text.splitlines() if x.startswith('param ')]==list(range(38))
  assert text.startswith('mxcsr 0x1f80\ntransport 0 0 120\ncreate\nrate 44100\n')
  assert text.endswith('process 16384 512\ndestroy\n')
def capture(r,b,out,err,name):
 assert r['name']==name and r['exit_code']==0 and r['signal'] is None and not r['timeout'] and r['exception'] is None
 assert r['executed_original_x86'] and r['valid_capture'] and r['output_exists'] and r['size_valid'] and r['all_finite']
 assert len(b)==131072 and r['output']['bytes']==len(b) and r['output']['sha256']==sha(b)==(SINE if name=='sine-baseline' else RAMP)
 frames=list(struct.iter_unpack('<ff',b));assert len(frames)==r['frames']==16384
 assert all(math.isfinite(v) for f in frames for v in f)
 assert not err and r['stderr']['bytes']==0 and r['stderr']['sha256']==sha(err)
 assert r['stdout']['bytes']==len(out) and r['stdout']['sha256']==sha(out)
 log=out.decode();lines=log.splitlines()
 assert 'TRAP' not in log and 'FAULT' not in log and not any(x.startswith('xdev:') for x in lines)
 assert r['fault_or_trap']==[] and r['cxx_failbits_lines']==['cxx-failbits 0'] and lines[-1]=='cxx-failbits 0'
 required=['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok','rate 44100 ret=1','inflag 1','process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy']
 assert all(x in lines for x in required)
 assert r['process_lines']==['process 16384 512 flags: 32x(ret=0,flag=1) blocks=32']
 assert [int(x.split()[1]) for x in lines if x.startswith('param ')]==list(range(38))
 assert f'param 18 {0 if name=="sine-baseline" else 3}' in lines and 'param 19 0' in lines
 imports=[x for x in lines if x.startswith('import ')];used=[x for x in lines if x.startswith('used ')]
 assert r['declared_imports']==imports and r['used_imports']==used and imports and used
 bindings={x.split()[2]:x.split()[1] for x in imports}
 assert all(bindings[x.split()[1]]=='linux' and int(x.split()[2])>0 for x in used)
 assert sum(x.startswith('export ') for x in lines)==7
 for c in range(2):
  v=[f[c] for f in frames];post=v[4096:]
  expected={'channel':c,'nonzero_total':sum(x!=0 for x in v),'nonzero_after_impulse':sum(x!=0 for x in post),'peak_abs':max(map(abs,v)),'sum_square_after_impulse':sum(x*x for x in post),'first_nonzero':next((i for i,x in enumerate(v) if x!=0),None)}
  assert r['channels'][c]==expected and expected['nonzero_after_impulse']>0 and expected['sum_square_after_impulse']>0
 assert r['baseline_hash_match']==(True if name=='sine-baseline' else None)
 assert len(r['argv'])==5 and r['argv'][-1]=='--imports' and r['argv'][2:4]==[str(HERE/'raw'/f'{name}.script'),str(HERE/'raw'/f'{name}.f32')]
def protocol(a,rs,observations):
 assert a['case_count_max']==2 and a['no_retry'] and a['timeout_seconds_per_child']==30 and a['baseline_gate_sha256']==SINE
 assert a['child_limits']['RLIMIT_CORE']==[0,0] and a['cwd']==str(HERE/'raw')
 env=a['child_environment_complete'];assert env['XDEV_TIME']=='0'
 assert set(env)<=set(['PATH','LANG','LC_ALL','LC_CTYPE','TZ','XDEV_TIME'])
 assert not set(env)&{'XDEV_LIBM_ULP','XDEV_TRACE_OSTREAM','LD_PRELOAD','LD_LIBRARY_PATH'}
 assert [r['name'] for r in rs]==['sine-baseline','ramp-up'] and rs[0]['pid']!=rs[1]['pid']
 assert datetime.datetime.fromisoformat(rs[0]['finished_utc'])<=datetime.datetime.fromisoformat(rs[1]['started_utc'])
 assert observations['criterion'] is None and observations['compatibility_grade'] is None and observations['new_normative_ids']==0 and observations['modal174_status']=='all unchanged ungraded'
def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no capture, write, replay or regeneration mode.')
 m=load('manifest.json');payload_paths={r['path'] for r in m['files']}
 actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='manifest.json'}
 assert actual==payload_paths
 for r in m['files']:
  b=(HERE/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
 d=load('proposal-asof.json');context=load('context-asof.json');before=load('watch-before.json');after=load('watch-after.json')
 assert len(d['pins'])==20 and len(before)==400 and after['files']==before and after['changed']==[]
 for r in before:
  if '/wiki/' in r['path']:
   b=context[r['path']].encode();assert len(b)==r['bytes'] and sha(b)==r['sha256']
  else:assert ident(r['path'])==r,r['path']
 assert all(r in before for r in d['pins'])
 selection=load('source-selected-records.json');assert [r['record']['entry'] for r in selection]==['0x1ccd4','0x1d1b4','0x1d550','0x1d74c']
 for r in selection:
  raw=Path(r['path']).read_bytes().splitlines(keepends=True)[r['line']-1]
  assert sha(raw)==r['raw_sha256'] and json.loads(raw)==r['record'] and sha(r['record']['code'].encode())==r['record']['code_sha256']
 bundle=Path(d['future_argvs'][0][1]).read_bytes();assert sha(bundle[16384:266736])==d['x86_slice']['sha256']
 input_path=next(r['path'] for r in d['pins'] if r['path'].endswith('/inputs/impulse44.f32'))
 inp=list(struct.iter_unpack('<ff',Path(input_path).read_bytes()));assert len(inp)==16384 and [(i,*v) for i,v in enumerate(inp) if any(v)]==[(4096,1.,1.)]
 a=(HERE/'raw/sine-baseline.script').read_text();b=(HERE/'raw/ramp-up.script').read_text();scripts(a,b,d)
 rs=[load(n+'-result.json') for n in ['sine-baseline','ramp-up']];data=[];logs=[]
 for r in rs:
  n=r['name'];raw=(HERE/'raw'/f'{n}.f32').read_bytes();out=(HERE/'raw'/f'{n}.stdout').read_bytes();err=(HERE/'raw'/f'{n}.stderr').read_bytes()
  capture(r,raw,out,err,n);data.append(list(struct.iter_unpack('<ff',raw)));logs.append((raw,out,err))
 results=load('results.json');observations=load('observations.json');attempt=load('attempt.json')
 assert results['cases']==rs and results['watch_count']==400 and results['watch_unchanged'] and results['ramp_executed']
 assert results['grade'] is None and results['waveform_or_frequency_criterion'] is None and results['modal174_status']=='unchanged ungraded'
 protocol(attempt,rs,observations)
 for c in range(2):
  diff=[v[c]-u[c] for u,v in zip(*data)]
  expected={'channel':c,'different_frames':sum(u[c]!=v[c] for u,v in zip(*data)),'first_different_frame':next((i for i,(u,v) in enumerate(zip(*data)) if u[c]!=v[c]),None),'max_abs_difference':max(map(abs,diff)),'post_impulse_rms_difference':math.sqrt(sum(x*x for x in diff[4096:])/12288),'post_impulse_sine_sum_square':sum(x[c]**2 for x in data[0][4096:]),'post_impulse_ramp_sum_square':sum(x[c]**2 for x in data[1][4096:])}
  assert observations['channel_differences'][c]==expected
 negative=[]
 def reject(label,fn):
  try:fn()
  except AssertionError:negative.append(label);return
  raise AssertionError('Fixture accepted: '+label)
 def changed(record,key,value):
  x=copy.deepcopy(record);x[key]=value;return x
 reject('wrong-shape',lambda:scripts(a,b.replace('param 18 3.0','param 18 4.0'),d))
 reject('unselected-sync',lambda:scripts(a,b.replace('param 19 0.0','param 19 1.0'),d))
 reject('omitted-parameter',lambda:scripts(a,b.replace('param 37 0.0\n',''),d))
 reject('nonzero-exit',lambda:capture(changed(rs[0],'exit_code',1),*logs[0],'sine-baseline'))
 reject('timeout',lambda:capture(changed(rs[0],'timeout',True),*logs[0],'sine-baseline'))
 reject('short-write',lambda:capture(rs[1],logs[1][0][:-8],logs[1][1],logs[1][2],'ramp-up'))
 reject('NaN-output',lambda:capture(rs[1],struct.pack('<f',float('nan'))+logs[1][0][4:],logs[1][1],logs[1][2],'ramp-up'))
 reject('baseline-mismatch',lambda:capture(rs[0],logs[0][0][4:]+logs[0][0][:4],logs[0][1],logs[0][2],'sine-baseline'))
 reject('trap-hit',lambda:capture(rs[1],logs[1][0],logs[1][1]+b'TRAP _rand\n',logs[1][2],'ramp-up'))
 reject('stream-failbit',lambda:capture(changed(rs[1],'cxx_failbits_lines',['cxx-failbits 1']),*logs[1],'ramp-up'))
 bad=copy.deepcopy(attempt);bad['child_environment_complete']['LD_PRELOAD']='unselected'
 reject('injected-library',lambda:protocol(bad,rs,observations))
 bad=copy.deepcopy(attempt);bad['child_limits']['RLIMIT_CORE']=[1,1]
 reject('core-enabled',lambda:protocol(bad,rs,observations))
 bad=copy.deepcopy(rs);bad[1]['started_utc']=rs[0]['started_utc']
 reject('ramp-before-baseline-finish',lambda:protocol(attempt,bad,observations))
 reject('invented-grade',lambda:protocol(attempt,rs,changed(observations,'compatibility_grade','PASS')))
 print(json.dumps({'status':'PASS retained-data-only','payloads':len(payload_paths),'pins':20,'historical_watch':400,'new_X_captures':2,'negative_fixtures':negative,'read_only':True,'original_replay':False,'grade':None}))
if __name__=='__main__':main()
