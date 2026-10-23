"""Read-only retained-data verification; never imports/runs collector, native or old code."""
from pathlib import Path
import copy,datetime,hashlib,json,math,re,struct,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'depth-corpus-lfo-ramp-up'
BASE_SEAL='b30f110700d57892331dd9b218fc99b765afc97176e25c48de9e89e65733bd26'
RAW_HASHES={'plus1':'d7cce1ebf94a1a23a38e79a707835467b96428141072ed250b00b4072473d180','minus1':'6e4937f37118dc99160932e7388e06e858ef6c590320b6003d1f2e7ceffc1d29'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((HERE/n).read_text())
def ident(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def audio(b):
 assert len(b)==131072
 x=list(struct.iter_unpack('<ff',b));assert all(math.isfinite(v) for f in x for v in f)
 assert all(sum(f[c]*f[c] for f in x[4096:])>0 for c in range(2))
 return x
def relative_rms(x,r):
 assert len(x)==len(r)==16384
 return [math.sqrt(sum((a[c]-b[c])**2 for a,b in zip(x[4096:],r[4096:]))/sum(b[c]**2 for b in r[4096:])) for c in range(2)]
def protocol(a,rows,results):
 assert a['max_native_children']==results['native_child_count']==2 and a['no_retry']
 assert a['timeout_seconds_per_child']==30 and a['child_limits']['RLIMIT_CORE']==[0,0]
 assert a['numeric_window']==[4096,16384] and a['criterion'] is None and a['grade'] is None
 assert a['cwd']==str(HERE/'raw') and a['base_packet']==str(BASE)
 base_env=a['child_environment_base_complete'];assert base_env['XDEV_TIME']=='0'
 assert set(base_env)<=set(['PATH','LANG','LC_ALL','LC_CTYPE','TZ','XDEV_TIME'])
 assert a['child_environments_complete']==[{**base_env,'XDEV_LIBM_ULP':v} for v in ['+1','-1']]
 assert [(r['name'],r['direction_ascii']) for r in rows]==[('plus1','+1'),('minus1','-1')]
 assert rows[0]['pid']!=rows[1]['pid']
 assert datetime.datetime.fromisoformat(rows[0]['finished_utc'])<=datetime.datetime.fromisoformat(rows[1]['started_utc'])
 for r,e in zip(rows,a['child_environments_complete']):
  assert r['child_environment_complete']==e and not set(e)&{'LD_PRELOAD','LD_LIBRARY_PATH','XDEV_TRACE_OSTREAM'}
 for key in ['criterion','grade','confidence_interval']:assert results[key] is None
 assert results['new_normative_ids']==0 and results['modal174_status']=='all unchanged ungraded'
def capture(r,b,out,err,ramp,sine):
 name=r['name'];x=audio(b)
 assert r['actual_original_x86_capture'] and r['valid_capture'] and r['valid_numeric'] and r['numeric_error'] is None
 assert r['exit_code']==0 and r['signal'] is None and not r['timeout'] and r['exception'] is None
 assert r['output']['sha256']==sha(b)==RAW_HASHES[name] and r['output']['bytes']==len(b)
 assert not err and r['stderr']['bytes']==0 and r['stderr']['sha256']==sha(err)
 assert r['stdout']['bytes']==len(out) and r['stdout']['sha256']==sha(out)
 lines=out.decode().splitlines();assert not any('TRAP' in x or 'FAULT' in x or x.startswith('xdev:') for x in lines)
 assert r['trap_or_fault']==[] and r['cxx_failbits']==['cxx-failbits 0'] and lines[-1]=='cxx-failbits 0'
 assert r['process_lines']==['process 16384 512 flags: 32x(ret=0,flag=1) blocks=32']
 assert all(x in lines for x in ['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok','rate 44100 ret=1','inflag 1','destroy',r['process_lines'][0]])
 baseline_lines=(BASE/'raw/ramp-up.stdout').read_text().splitlines()
 for prefix in ['param ','export ','input ','import ']:assert [x for x in lines if x.startswith(prefix)]==[x for x in baseline_lines if x.startswith(prefix)]
 assert r['imports']==[x for x in lines if x.startswith('import ')] and r['used_imports']==[x for x in lines if x.startswith('used ')]
 bindings={x.split()[2]:x.split()[1] for x in r['imports']}
 assert all(bindings[x.split()[1]]=='linux' and int(x.split()[2])>0 for x in r['used_imports'])
 assert r['relative_rms_to_frozen_ramp_by_channel']==relative_rms(x,ramp)
 assert r['frozen_sine_wrong_shape_relative_rms_to_frozen_ramp_by_channel']==relative_rms(sine,ramp)
 for c in range(2):
  assert r['channels'][c]=={'channel':c,'post_impulse_energy':sum(f[c]*f[c] for f in x[4096:]),'post_impulse_nonzero':sum(f[c]!=0 for f in x[4096:]),'peak_abs':max(abs(f[c]) for f in x)}
def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no write/capture/replay mode.')
 m=load('manifest.json');payload_paths={r['path'] for r in m['files']}
 for pin in m['external_pins']:assert ident(pin['path'])==pin
 assert {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='manifest.json'}==payload_paths
 for r in m['files']:
  b=(HERE/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],r['path']
 assert sha((BASE/'manifest.json').read_bytes())==BASE_SEAL
 a=load('attempt.json');before=load('watch-before.json');after=load('watch-after.json');ctx=load('context-asof.json')
 assert len(before)==422 and after['files']==before and after['changed']==[]
 for r in before:
  if '/wiki/' in r['path']:
   b=ctx[r['path']].encode();assert len(b)==r['bytes'] and sha(b)==r['sha256']
  else:assert ident(r['path'])==r,r['path']
 assert len(a['provider_pins'])==20 and all(r in before for r in a['provider_pins'])
 assert len(a['frozen_provider_files'])==21 and all(r in before for r in a['frozen_provider_files']) and a['base_manifest'] in before
 source=load('source-context.json');text=source['full_source_asof'];assert len(text.encode())==source['file']['bytes'] and sha(text.encode())==source['file']['sha256'] and source['file'] in before
 entries=re.findall(r'\{"([^"]+)"',text.split('} perturbed[] = {',1)[1].split('};',1)[0])
 assert len(entries)==23 and source['ordinary_perturbed_entries']==entries
 assert 'no inexactness test' in source['roles'][0]['role']
 assert 'nextafterf(r, ulp_dir > 0 ? INFINITY : -INFINITY)' in text and 'nextafter(r, ulp_dir > 0 ? INFINITY : -INFINITY)' in text
 assert source['fixed_wrappers_also_using_pf_pd']==['___sincosf_stret','___sincos_stret','___exp10','___exp10f']
 assert len(source['author_readback_note'])>0
 script=(BASE/'raw/ramp-up.script').read_bytes();assert ident(BASE/'raw/ramp-up.script')==a['all_scripts_exact_source']
 for name in ['plus1','minus1']:assert (HERE/'raw'/f'{name}.script').read_bytes()==script
 ramp=audio((BASE/'raw/ramp-up.f32').read_bytes());sine=audio((BASE/'raw/sine-baseline.f32').read_bytes())
 rows=[load(n+'-result.json') for n in ['plus1','minus1']];results=load('results.json');assert results['runs']==rows and results['watch_count']==422 and results['watch_unchanged']
 protocol(a,rows,results);triples=[]
 for r in rows:
  n=r['name'];triple=tuple((HERE/'raw'/f'{n}.{ext}').read_bytes() for ext in ['f32','stdout','stderr']);triples.append(triple)
  assert r['argv']==[a['provider_pins'][0]['path'],a['provider_pins'][1]['path'],str(HERE/'raw'/f'{n}.script'),str(HERE/'raw'/f'{n}.f32'),'--imports']
  capture(r,*triple,ramp,sine)
 fixtures=[]
 def reject(label,fn):
  try:fn()
  except AssertionError:fixtures.append(label);return
  raise AssertionError('Fixture accepted:'+label)
 def changed(obj,k,v):
  x=copy.deepcopy(obj);x[k]=v;return x
 reject('short-write',lambda:audio(triples[0][0][:-8]))
 reject('nonfinite-output',lambda:audio(struct.pack('<f',float('nan'))+triples[0][0][4:]))
 reject('zero-reference-energy',lambda:audio(bytes(131072)))
 reject('failed-native-exit',lambda:capture(changed(rows[0],'exit_code',1),*triples[0],ramp,sine))
 reject('native-timeout',lambda:capture(changed(rows[0],'timeout',True),*triples[0],ramp,sine))
 reject('trap-hit',lambda:capture(rows[0],triples[0][0],triples[0][1]+b'TRAP _sinf\n',triples[0][2],ramp,sine))
 reject('stream-failure',lambda:capture(changed(rows[0],'cxx_failbits',['cxx-failbits 1']),*triples[0],ramp,sine))
 reject('window-exclusion',lambda:protocol(changed(a,'numeric_window',[8192,16384]),rows,results))
 reject('extra-native-child',lambda:protocol(changed(a,'max_native_children',3),rows,results))
 reject('core-enabled',lambda:protocol(changed(a,'child_limits',{'RLIMIT_CORE':[1,1]}),rows,results))
 bad=copy.deepcopy(a);bad['child_environments_complete'][0]['XDEV_LIBM_ULP']='-1'
 reject('wrong-perturbation-direction',lambda:protocol(bad,rows,results))
 bad=copy.deepcopy(rows);bad[0]['child_environment_complete']['LD_PRELOAD']='unselected'
 reject('library-injection',lambda:protocol(a,bad,results))
 reject('invented-acceptance-grade',lambda:protocol(a,rows,changed(results,'grade','PASS')))
 reject('invented-confidence-interval',lambda:protocol(a,rows,changed(results,'confidence_interval',[0,1])))
 print(json.dumps({'status':'PASS retained-data-only','payloads':len(payload_paths),'historical_watch':422,'original_replay':False,'new_native_captures':2,'negative_fixtures':fixtures,'criterion':None,'grade':None}))
if __name__=='__main__':main()
