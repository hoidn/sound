"""Retained data only. No collector, original code, unselected or old tool calls."""
from pathlib import Path
import copy,datetime,hashlib,json,math,runpy,struct,sys
HERE=Path(__file__).resolve().parent
PREFLIGHT='89b0bfa5c58b051309a1fa71546177a29b65131fd07c4a677ac5654ce8a39dfc'
METHOD='b6b80a9c04472e5627a48a464d36114af42aa434e957fc4bf9f077e3562559bf'
RAW={'note60':'5866c6b9e4915336648da87bd92c38927cb3e532fe81ab38b5300664c7bb984f','note72':'f98b465f7186680830bc87c97f4a4096e1e53b2ad1b07aa5333ccccd6ea36ddc'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((HERE/n).read_text())
def verified(b,pin):assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
def scripts(base,text,note):
 expected=base.replace('param 12 0.0\n','param 12 1.0\n').replace('param 17 1.0\n','param 17 0.0\n')
 assert text==expected.replace('inflag 1\n',f'event 1537 0x90 {note} 100\ninflag 1\n')
 assert [int(x.split()[1]) for x in text.splitlines() if x.startswith('param ')]==list(range(38))
 assert text.count('event ')==text.count('process ')==1
 assert (1537//512)*512==1536 and 1537%512==1
 assert len(struct.pack('<qBBBB4B',1,0x90,note,100,0,0,0,0,0))==16

def decoded(b):
 assert len(b)==131072
 x=list(struct.iter_unpack('<ff',b));assert all(math.isfinite(v) for f in x for v in f)
 return x

def capture(row,b,stdout,stderr,text,note):
 name='note'+str(note);x=decoded(b)
 assert row['name']==name and row['note']==note and row['output']['sha256']==sha(b)==RAW[name]
 assert row['actual_original_x86_capture'] and row['exit_code']==0 and row['signal'] is None and not row['timeout'] and row['exception'] is None
 assert row['valid_capture'] and row['numeric_valid'] and row['numeric_error'] is None and row['productive_both_channels']
 assert row['output']['bytes']==len(b);verified(stdout,row['stdout']);verified(stderr,row['stderr']);assert stderr==b''
 lines=stdout.decode().splitlines()
 assert not any('TRAP' in s or 'FAULT' in s or s.startswith('xdev:') for s in lines) and row['fault_or_trap']==[]
 assert row['cxx_failbits']==['cxx-failbits 0'] and lines[-1]=='cxx-failbits 0'
 assert row['process_lines']==['process 16384 512 flags: 32x(ret=0,flag=1) blocks=32']
 assert row['event_lines']==[f'event 1537 0x90 {note} 100']==[s for s in lines if s.startswith('event ')]
 assert all(s in lines for s in ['create ok','rate 44100 ret=1','mxcsr 0x1f80','transport 0 0 120','inflag 1','destroy',row['process_lines'][0]])
 expected=[s.split() for s in text.splitlines() if s.startswith('param ')];actual=[s.split() for s in lines if s.startswith('param ')]
 assert [int(s[1]) for s in actual]==list(range(38))
 assert [struct.pack('<f',float(s[2])) for s in actual]==[struct.pack('<f',float(s[2])) for s in expected]
 assert sum(s.startswith('export ') for s in lines)==7
 assert row['declared_imports']==[s for s in lines if s.startswith('import ')] and row['used_imports']==[s for s in lines if s.startswith('used ')]
 bindings={s.split()[2]:s.split()[1] for s in row['declared_imports']}
 assert all(bindings[s.split()[1]]=='linux' and int(s.split()[2])>0 for s in row['used_imports'])
 for c in range(2):
  pre=[f[c] for f in x[:4096]];post=[f[c] for f in x[4096:]]
  r={'channel':c,'pre_peak':max(map(abs,pre)),'post_peak':max(map(abs,post)),'pre_mean_square':math.fsum(v*v for v in pre)/4096,'post_mean_square':math.fsum(v*v for v in post)/12288,'post_nonzero':sum(v!=0 for v in post)}
  r['productive']=r['post_nonzero']>0 and r['post_peak']>r['pre_peak'] and r['post_mean_square']>r['pre_mean_square']
  assert r==row['channels'][c] and r['productive']

def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Read-only --check only; no capture/replay/write mode.')
 manifest=load('manifest.json');payloads={r['path'] for r in manifest['files']}
 assert {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='manifest.json'}==payloads
 for r in manifest['files']:verified((HERE/r['path']).read_bytes(),r)
 for r in manifest['external_pins']:verified(Path(r['path']).read_bytes(),r)
 assert sha((HERE/'manifest-preflight.json').read_bytes())==PREFLIGHT
 for r in load('manifest-preflight.json')['files']:verified((HERE/r['path']).read_bytes(),r)
 proposal=load('proposal.json');attempt=load('attempt.json');results=load('results.json');context=load('context-asof.json')
 before=load('watch-before.json');after=load('watch-after.json');assert len(before)==530 and after['files']==before and after['changed']==[]
 for r in before:
  b=context[r['path']].encode() if '/wiki/' in r['path'] else Path(r['path']).read_bytes();verified(b,r)
 for pin in proposal['immutable_pins']:verified(Path(pin['path']).read_bytes(),pin)
 for r in proposal['selected_source_contexts']:
  path=r['file_asof']['path'];text=context[path] if '/wiki/' in path else Path(path).read_text();verified(text.encode(),r['file_asof'])
  assert ''.join(text.splitlines(keepends=True)[r['start_line']-1:r['end_line_inclusive']])==r['selected_text']
 assert sha(Path(proposal['immutable_pins'][1]['path']).read_bytes()[16384:266736])==proposal['x86_slice']['sha256']
 inp=decoded(Path(proposal['immutable_pins'][7]['path']).read_bytes());assert [(i,*v) for i,v in enumerate(inp) if any(v)]==[(4096,1.,1.)]
 assert attempt['preflight_manifest_sha256']==PREFLIGHT and attempt['max_native_children']==results['native_children']==2 and attempt['no_retry']
 assert attempt['child_limits']['RLIMIT_CORE']==[0,0] and attempt['timeout_seconds_per_child']==30 and attempt['cwd']==str(HERE/'raw')
 assert attempt['child_environment_complete']==proposal['child_environment_complete'] and set(attempt['child_environment_complete'])<=set(['PATH','LANG','LC_ALL','LC_CTYPE','TZ','XDEV_TIME']) and attempt['child_environment_complete']['XDEV_TIME']=='0'
 assert results['criterion'] is None and results['grade'] is None and results['new_normative_cases']==0 and not results['wholeLive_sidechain_or_arm64_claim']
 assert results['watch_count']==530 and results['watch_unchanged'] and results['positive_control_note_delivery'].startswith('UNESTABLISHED:')
 base=Path(proposal['immutable_pins'][9]['path']).read_text();rows=[];raws=[]
 for note in [60,72]:
  name='note'+str(note);text=(HERE/(name+'.script')).read_text();scripts(base,text,note);assert (HERE/'raw'/(name+'.script')).read_text()==text
  row=load(name+'-result.json');b=(HERE/'raw'/(name+'.f32')).read_bytes();stdout=(HERE/'raw'/(name+'.stdout')).read_bytes();stderr=(HERE/'raw'/(name+'.stderr')).read_bytes()
  assert row['argv']==[proposal['immutable_pins'][0]['path'],proposal['immutable_pins'][1]['path'],str(HERE/'raw'/(name+'.script')),str(HERE/'raw'/(name+'.f32')),'--imports']
  capture(row,b,stdout,stderr,text,note);rows.append(row);raws.append((b,stdout,stderr,text))
 assert results['runs']==rows and rows[0]['pid']!=rows[1]['pid'] and datetime.datetime.fromisoformat(rows[0]['finished_utc'])<=datetime.datetime.fromisoformat(rows[1]['started_utc'])
 selection=load('diagnostic-selection.json');assert selection['path']=='diagnostic-selected.py' and selection['sha256']==METHOD
 method_bytes=(HERE/selection['path']).read_bytes();assert len(method_bytes)==selection['bytes']==6848 and sha(method_bytes)==METHOD
 assert selection['windows_half_open']==[[4096,16384],[4096,10240],[10240,16384]]
 # This NEW fully read selected data-only helper defines describe; its main/self-test are not invoked.
 method=runpy.run_path(str(HERE/'diagnostic-selected.py'))
 for name,triple in zip(['note60','note72'],raws):assert method['describe'](triple[0])==load(name+'-spectrum.json')
 failures=[]
 def reject(label,fn):
  try:fn()
  except AssertionError:failures.append(label);return
  raise AssertionError('Fixture accepted:'+label)
 reject('short-raw',lambda:decoded(raws[0][0][:-8]))
 reject('nonfinite-prefix',lambda:decoded(struct.pack('<f',float('nan'))+raws[0][0][4:]))
 reject('wrong-event-byte',lambda:scripts(base,raws[1][3].replace('0x90 72 100','0x90 73 100'),72))
 reject('wrong-MidiPitch-bit',lambda:scripts(base,raws[0][3].replace('param 12 1.0','param 12 0.0'),60))
 bad=copy.deepcopy(proposal['immutable_pins'][0]);bad['sha256']='0'*64
 reject('provider-hash',lambda:verified(Path(bad['path']).read_bytes(),bad))
 bad=copy.deepcopy(rows[0]);bad['exit_code']=1
 reject('nonzero-native-exit',lambda:capture(bad,*raws[0],60))
 bad=copy.deepcopy(rows[0]);bad['channels'][1]['productive']=False
 reject('unproductive-right-channel',lambda:capture(bad,*raws[0],60))
 print(json.dumps({'status':'PASS retained-data-only','payloads':len(payloads),'history_watch':530,'actual_x86_captures':2,'selected_spectra_reproduced':2,'negative_fixtures':failures,'collector_or_original_replay':False,'unselected_diagnostic_executed':False,'grade':None}))
if __name__=='__main__':main()
