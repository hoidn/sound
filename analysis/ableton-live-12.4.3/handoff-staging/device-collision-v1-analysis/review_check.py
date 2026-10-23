"""Independent finite-input, retained-audio and comparison-boundary review."""
import hashlib, importlib.util, json, math, re, shutil, struct, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
P=HERE.with_name('device-collision-v1')
SOURCE=ROOT/'analysis/ableton-live-12.4.3/r2/t12-collision-v1'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def wav_data(p, rate, frames):
 b=p.read_bytes();assert b[:4]==b'RIFF' and b[8:12]==b'WAVE'
 assert int.from_bytes(b[4:8],'little')+8==len(b)
 off=12;data=None;fmt=None
 while off<len(b):
  n=int.from_bytes(b[off+4:off+8],'little');chunk=b[off+8:off+8+n]
  if b[off:off+4]==b'fmt ':fmt=struct.unpack_from('<HHIIHH',chunk)
  if b[off:off+4]==b'data':assert data is None;data=chunk
  off+=8+n+(n%2)
 assert off==len(b) and fmt[0]==3 and fmt[1]==2 and fmt[2]==rate and fmt[5]==32
 assert len(data)==frames*8
 return data

def main():
 manifest=json.loads((P/'manifest.json').read_text());listed={f['path'] for f in manifest['files']}
 assert listed|{'manifest.json'}=={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file()}
 assert not any(f.is_symlink() for f in P.rglob('*'))
 for f in manifest['files']:
  p=P/f['path'];assert sha(p)==f['sha256'] and p.stat().st_size==f['bytes']
 for p in P.rglob('*'):
  if p.suffix in ('.md','.py','.json'):
   text=p.read_text();assert not re.search(r'DCL-\d|0x[0-9a-f]{6,}|FUN_|DAT_|/home/|/var/tmp/|t12-collision|SetParameterA|CalcA|CreateInstanceU',text),p
   if p.suffix=='.md':
    for target in re.findall(r'\]\(([^)]+)\)',text):assert (p.parent/target.split('#')[0]).exists(),target
 cases=json.loads((P/'cases.json').read_text())['cases'];assert len(cases)==2
 mapping=['ctor_c4','wg_pipe'];source=json.loads((SOURCE/'manifest.json').read_text())
 spec=importlib.util.spec_from_file_location('collision_review_comparison',P/'compare.py');cmp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cmp)
 rows=[]
 for case,tag in zip(cases,mapping):
  script=SOURCE/'raw'/(tag+'.script');wav=SOURCE/'raw'/(tag+'.wav')
  for f in (script,wav):assert sha(f)==source['files'][str(f.relative_to(SOURCE))]['sha256']
  lines=script.read_text().splitlines();params=[l.split() for l in lines if l.startswith('param ')];assert len(params)==139
  assert [int(l[1]) for l in params]==list(range(139))
  assert len(case['parameter_values'])==139
  for row,(_,index,value) in zip(case['parameter_values'],params):
   data=struct.pack('<f',float(value));assert data.hex()==row['binary32_hex'];assert struct.unpack('<f',data)[0]==row['value']
  expected_events=[]
  for l in lines:
   if l.startswith('event '):
    _,frame,status,key,velocity=l.split();expected_events.append({'frame':int(frame),'status':int(status,0),'key':int(key),'velocity':int(velocity)})
  assert case['events']==expected_events,(case['events'],expected_events)
  proc=[tuple(map(int,l.split()[1:])) for l in lines if l.startswith('process ')];assert proc==[(11264,512),(case['frames'],512)]
  reference=P/case['reference'];data=wav_data(wav,case['sample_rate_hz'],case['frames']);assert data==reference.read_bytes()
  _,ref=cmp.audio(reference,case['frames']);assert all(math.isfinite(v) for v in ref)
  assert cmp.measure(ref,ref,case['metric'])['pass']
  if tag=='wg_pipe':
   for amount,expected in [(0,False),(1.0029,True),(1.0031,False),(-1,False)]:
    candidate=tuple(v*amount for v in ref);assert cmp.measure(candidate,ref,case['metric'])['pass']==expected
   for ch in [0,1]:assert not cmp.measure(tuple(0 if i%2==ch else v for i,v in enumerate(ref)),ref,case['metric'])['pass']
  else:
   assert max(abs(v) for v in ref)<1e-18
   assert cmp.measure(tuple(0 for v in ref),ref,case['metric'])['pass']
   candidate=list(ref);candidate[0]=1e-17;assert not cmp.measure(tuple(candidate),ref,case['metric'])['pass']
  rows.append({'case':case['id'],'source_wav_sha256':sha(wav),'reference_sha256':sha(reference),'frames':case['frames'],'parameter_values':len(params)})
 with tempfile.TemporaryDirectory(prefix='collision-independent-export-') as tmp:
  export=Path(tmp)/'release';shutil.copytree(P,export);outputs=Path(tmp)/'outputs';outputs.mkdir()
  for c in cases:shutil.copyfile(export/c['reference'],outputs/(c['id']+'.f32'))
  result=subprocess.run([sys.executable,'-I','-B',str(export/'compare.py'),str(outputs)],capture_output=True,text=True);assert result.returncode==0,result.stderr
  assert json.loads(result.stdout)['pass']
  (outputs/(cases[1]['id']+'.f32')).unlink();result=subprocess.run([sys.executable,'-I','-B',str(export/'compare.py'),str(outputs)],capture_output=True,text=True);assert result.returncode==1;assert not json.loads(result.stdout)['pass']
 return {'status':'pass','cases':rows,'manifest_sha256':sha(P/'manifest.json'),'payload_files':len(listed),'boundaries':'self, two-sided Pipe gain boundary, silence, channel mute, sign reversal, audible injection and isolated missing-file rejection','original_code_executed':False}
if __name__=='__main__':
 result=main();(HERE/'review-validation.json').write_text(json.dumps(result,indent=1)+'\n');print(json.dumps(result))
