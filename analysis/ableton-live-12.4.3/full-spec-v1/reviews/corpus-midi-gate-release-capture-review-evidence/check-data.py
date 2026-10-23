"""Independent stdlib-only checks of already captured bytes; never invoke a helper/native."""
from pathlib import Path
import datetime, hashlib, json, math, re, struct
ROOT=Path('/home/ollie/Documents/sound')
P=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-midi-gate-release'
PROP=json.loads((P/'proposal.json').read_text())
NAMES=['gate1-held','gate1-off','gate0-off']
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(name):return json.loads((P/name).read_text())
def decode(p):
 b=p.read_bytes();assert len(b)==131072
 x=list(struct.iter_unpack('<ff',b));assert all(math.isfinite(v) for frame in x for v in frame)
 return b,x
result=load('results.json');attempt=load('attempt.json');invocation=load('root-invocation.json');selection=load('root-selection.json')
assert selection['argv']==invocation['argv']
assert selection['selected_utc_before_execution']<invocation['started_utc']<invocation['finished_utc']
assert invocation['collector_exit']==0 and (P/'root-stderr.txt').read_bytes()==b''
assert attempt['child_environment_complete']==PROP['child_environment_complete'] and attempt['child_limits']['RLIMIT_CORE']==[0,0]
assert attempt['timeout_seconds_per_child']==30 and attempt['max_launch_attempts']==3
assert [r['name'] for r in result['runs']]==NAMES
assert (result['attempted_launches'],result['returned_pid_children'],result['structurally_valid_captures'])==(3,3,3)
assert result['all3_structurally_valid'] and result['criterion'] is None and result['grade'] is None
raw={};data={};rows=[];last=invocation['started_utc']
for name,r in zip(NAMES,result['runs']):
 assert r==load(name+'-result.json')
 assert last<r['started_utc']<r['finished_utc']<invocation['finished_utc'];last=r['finished_utc']
 assert r['launch_attempted'] and r['popen_returned_pid'] and r['valid_capture']
 assert r['exit_code']==0 and not r['timeout'] and r['exception'] is None and r['signal'] is None
 assert isinstance(r['pid'],int) and r['pid']>0
 assert r['argv']==[PROP['source_pins']['xdev']['path'],PROP['source_pins']['bundle']['path'],str(P/'raw'/(name+'.script')),str(P/'raw'/(name+'.f32')),'--imports']
 for suffix in ['stdout','stderr']:
  assert ident(P/'raw'/(name+'.'+suffix))=={k:r[suffix][k] for k in ['bytes','sha256']}
 assert (P/'raw'/(name+'.stderr')).read_bytes()==b''
 text=(P/'raw'/(name+'.stdout')).read_text();lines=text.splitlines();script=(P/(name+'.script')).read_text().splitlines()
 assert script==(P/'raw'/(name+'.script')).read_text().splitlines()
 params=[s.split()[1:] for s in lines if s.startswith('param ')];wanted=[s.split()[1:] for s in script if s.startswith('param ')]
 assert len(params)==38 and [p[0] for p in params]==[p[0] for p in wanted]==[str(i) for i in range(38)]
 assert all(struct.pack('<f',float(a[1]))==struct.pack('<f',float(b[1])) for a,b in zip(params,wanted))
 events=[s for s in lines if s.startswith('event ')];assert events==[s for s in script if s.startswith('event ')]==r['event_lines']
 assert [s for s in lines if s.startswith('process ')]==['process 16384 512 flags: 32x(ret=0,flag=1) blocks=32']
 assert 'create ok' in lines and 'rate 44100 ret=1' in lines and 'destroy' in lines and 'cxx-failbits 0' in lines
 assert 'mxcsr 0x1f80' in lines and 'transport 0 0 120' in lines and 'inflag 1' in lines
 assert not any('TRAP' in s or 'FAULT' in s or s.startswith('xdev:') for s in lines)
 assert [s for s in lines if s.startswith('used ')]==r['used_imports']
 assert [s for s in lines if s.startswith('import ')]==r['declared_imports']
 raw[name],data[name]=decode(P/'raw'/(name+'.f32'));assert ident(P/'raw'/(name+'.f32'))=={k:r['output'][k] for k in ['bytes','sha256']}
 for c in r['channels']:
  v=[f[c['channel']] for f in data[name][4096:8192]]
  assert c['before_off_peak']==max(map(abs,v)) and c['before_off_mean_square']==math.fsum(t*t for t in v)/len(v)
  assert c['before_off_nonzero']==sum(t!=0 for t in v)==4096 and c['productive_before_off']
 rows.append({'name':name,'pid':r['pid'],'exit':r['exit_code'],'bytes':len(raw[name]),'sha256':hashlib.sha256(raw[name]).hexdigest(),'events':events,'fullfinite':True,'productive_both_channels':True})
assert len({r['pid'] for r in result['runs']})==3
hist=Path(PROP['source_pins']['historical_reference']['path']);raw['historical-gate0-held'],data['historical-gate0-held']=decode(hist)
assert raw['gate1-held']==raw['gate1-off'] and raw['gate0-off']==raw['historical-gate0-held']
assert all(raw[n][4096*8:]==raw['historical-gate0-held'][4096*8:] for n in NAMES)
windows=[('prefix',0,4096),('pre_off_command_block',4096,8192),('later_command_block_onward',8192,16384)]
energies=[]
for name,x in data.items():
 for label,start,stop in windows:
  for ch in [0,1]:
   samples=[f[ch] for f in x[start:stop]]
   energies.append({'name':name,'window':label,'frames_half_open':[start,stop],'channel':ch,'mean_square':math.fsum(v*v for v in samples)/len(samples),'peak':max(map(abs,samples)),'nonzero':sum(v!=0 for v in samples)})
differences=[]
for left,right in [('gate1-held','historical-gate0-held'),('gate1-off','gate1-held'),('gate0-off','historical-gate0-held'),('gate1-off','gate0-off')]:
 for label,start,stop in windows:
  for ch in [0,1]:
   samples=[data[left][i][ch]-data[right][i][ch] for i in range(start,stop)]
   differences.append({'left':left,'right':right,'window':label,'channel':ch,'different_samples':sum(v!=0 for v in samples),'max_abs_difference':max(map(abs,samples)),'rms_difference':math.sqrt(math.fsum(v*v for v in samples)/len(samples))})
saved=load('descriptive.json');assert saved['energies']==energies and saved['differences']==differences
before=load('watch-before.json');after=load('watch-after.json');assert len(before)==601 and before==after['files'] and after['changed']==[]
assert len({r['path'] for r in before})==601
context=load('context-asof.json');lookup={r['path']:r for r in before}
for path,text in context.items():
 b=text.encode();assert len(b)==lookup[path]['bytes'] and hashlib.sha256(b).hexdigest()==lookup[path]['sha256']
inputraw,inputframes=decode(Path(PROP['source_pins']['input']['path']));assert [(i,*f) for i,f in enumerate(inputframes) if any(f)]==[(4096,1.,1.)]
print(json.dumps({'status':'Independent bounded capture-data checks PASS; no criterion/grade','rows':rows,'paired_durable_watch':601,'wiki_asof_texts_bound':len(context),'descriptive_energies_exact':len(energies),'descriptive_difference_rows_exact':len(differences),'A_equals_B_full':True,'C_equals_historical_full':True,'all3_post4096_equal_historical':True,'prefix_A_minus_historical_max_abs_by_channel':[max(abs(data['gate1-held'][i][c]-data['historical-gate0-held'][i][c]) for i in range(4096)) for c in [0,1]],'energies':energies,'differences':differences,'original_calls_this_review':0,'collector_or_diagnostic_invocations':0,'criterion':None,'grade':None},indent=2,allow_nan=False))
