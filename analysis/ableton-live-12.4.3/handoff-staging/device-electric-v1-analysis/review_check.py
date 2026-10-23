"""Independent Electric source-vector, measurement identity and boundary review."""
import copy, hashlib, importlib.util, json, math, re, shutil, struct, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
P=HERE.with_name('device-electric-v1')
SOURCE=HERE.parents[1]/'r2/t12-electric-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wav(p):
 b=p.read_bytes();assert b[:4]==b'RIFF' and b[8:12]==b'WAVE' and int.from_bytes(b[4:8],'little')+8==len(b)
 off=12;chunks={}
 while off<len(b):
  n=int.from_bytes(b[off+4:off+8],'little');key=b[off:off+4];assert key not in chunks;chunks[key]=b[off+8:off+8+n];off+=8+n+(n%2)
 assert off==len(b);fmt=struct.unpack_from('<HHIIHH',chunks[b'fmt ']);assert fmt[0]==3 and fmt[1]==1 and fmt[5]==32
 return chunks[b'data'],fmt[2]
def main():
 manifest=json.loads((P/'manifest.json').read_text());files={r['path'] for r in manifest['files']}
 assert files|{'manifest.json'}=={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}
 for r in manifest['files']:assert sha(P/r['path'])==r['sha256'] and (P/r['path']).stat().st_size==r['bytes']
 assert not any(p.is_symlink() for p in P.rglob('*'))
 for p in P.rglob('*'):
  if p.suffix in ['.md','.json','.py']:
   assert not re.search(r'0x[0-9a-f]{6,}|FUN_|DAT_|DEL-\d|/home/|/var/tmp/|t12-electric|SetParameterA|CreateInstanceU|CalcA',p.read_text()),p
   if p.suffix=='.md':
    for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):assert (p.parent/target.split('#')[0]).is_file(),target
 source_manifest=json.loads((SOURCE/'manifest.json').read_text())
 for path,row in source_manifest['files'].items():assert sha(SOURCE/path)==row['sha256'] and (SOURCE/path).stat().st_size==row['bytes']
 for row in source_manifest['external_inputs'].values():
  path=Path(row['path']);assert sha(path)==row.get('file_sha256',row.get('sha256'))
  if 'x86_64_offset' in row:
   b=path.read_bytes()
   for arch in ['x86_64','arm64']:assert hashlib.sha256(b[row[arch+'_offset']:row[arch+'_offset']+row[arch+'_size']]).hexdigest()==row[arch+'_sha256']
 original=json.loads((SOURCE/'results/cases.json').read_text())['cases']
 mapping=json.loads((HERE/'traceability.json').read_text());cases=json.loads((P/'cases.json').read_text())['cases'];assert len(cases)==117
 assert set(original)-{r['source_case'] for r in mapping['cases']}=={'p04_0','p05_1_key36','p05_1_key84'}
 tables={r['case']:r for r in mapping['cases']};metrics=0;partial_count=0;history=0;max_difference=0.;sample=None;silent=None
 for c in cases:
  assert len(c['evaluations'])==1;e=c['evaluations'][0];row=tables[c['id']];old=original[row['source_case']]
  lines=(SOURCE/row['source_script']).read_text().splitlines();params=[l.split()[1:] for l in lines if l.startswith('param ')][:33];assert [int(v[0]) for v in params]==list(range(33))
  assert len(e['parameters'])==len(e['parameter_order'])==33
  for i,(index,v) in enumerate(params):assert struct.pack('<f',e['parameters'][e['parameter_order'][i]])==struct.pack('<f',float(v))
  ev=[l.split()[1:] for l in lines if l.startswith('event ')];assert [[int(f)-e['warm_up_frames'],int(s,0),int(k),int(v)] for f,s,k,v in ev]==old['events']
  expected=[{'frame':f,'type':'note_on' if status==144 else 'note_off','key':key,'velocity':vel,'channel':1} for f,status,key,vel in old['events']];assert e['events']==expected
  seen=0;frame=0;captured=[]
  for line in lines:
   v=line.split()
   if not v:continue
   if v[0]=='param':
    seen+=1
    if seen>33:captured.append({'frame':frame-e['warm_up_frames'],'action':'set_parameter','parameter':e['parameter_order'][int(v[1])],'value':float(np.float32(v[2]))})
   if v[0]=='process':assert int(v[2])==512;frame+=int(v[1])
  assert frame==e['warm_up_frames']+e['frames'];assert captured==e['during_processing'];assert all(a['frame']%512==0 for a in captured);history+=len(captured)
  b,rate=wav(SOURCE/row['source_wav']);assert rate==e['sample_rate_hz'];assert b==(P/e['reference']).read_bytes();assert len(b)==e['frames']*4
  assert (P/e['signal']).read_bytes()==bytes(len(b))
  actual=e['expected_measurements'];m=e['metric']
  if m['kind']=='silence':assert old['measures']['onset'] is None and not np.any(np.frombuffer(b,'<f4'));silent=e;continue
  assert m['graded']==old['graded'] and m['tolerances']==old['tolerances'];assert m['onset_min_frame']<=old['measures']['onset']<=m['onset_max_frame']
  assert sum(len(v) for v in m['graded']['bands'])+len(m['graded']['env'])>0
  for indices,aa,bb in [(m['graded']['env'],actual['envelope_db'],old['measures']['env'])]+[(indices,actual['bands_db'][j],old['measures']['bands'][j]) for j,indices in enumerate(m['graded']['bands'])]:
   for i in indices:d=abs(aa[i]-bb[i]);assert d<1e-8;max_difference=max(max_difference,d);metrics+=1
  src={r['k']:r for r in old['measures'].get('partials',[])}
  for r in actual.get('partials',[]):
   k=r['harmonic'];assert k in src
   for a,bkey in [('frequency_hz','hz'),('amplitude_db','amp_db'),('decay_db_per_second','decay_db_s')]:
    d=abs(r[a]-src[k][bkey]);assert d<1e-8,(row['source_case'],a,d);max_difference=max(max_difference,d);partial_count+=1
  if row['source_case']=='defaults_c4':sample=e
 spec=importlib.util.spec_from_file_location('electric_review_comparator',P/'compare.py');cmp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cmp)
 assert sample is not None and silent is not None
 y=cmp.audio(P/sample['reference'],sample['frames']);assert cmp.compare(y,sample)['pass']
 for scale in [0,2,-2]:
  # The metric intentionally does not judge polarity; sign inversion alone is outside scope.
  try: accepted=cmp.compare(y*scale,sample)['pass']
  except ValueError: accepted=False
  assert not accepted
 assert cmp.compare(-y,sample)['pass']
 i=sample['metric']['graded']['env'][0];bound=sample['metric']['tolerances']['env']
 for scale,expect in [(0.99,True),(1.01,False)]:
  e=copy.deepcopy(sample);e['expected_measurements']['envelope_db'][i]+=scale*bound;assert cmp.compare(y,e)['pass']==expect
 assert cmp.compare(cmp.audio(P/silent['reference'],silent['frames']),silent)['pass']
 return {'status':'pass','case_count':117,'source_payloads':len(source_manifest['files']),'vectors_verified':117*33,'events_and_processing_histories':'exact source scripts','parameter_actions':history,'reference_bytes_and_zero_signals':117,'calibrated_selected_measurements':metrics,'partial_measurement_values':partial_count,'max_measurement_difference_from_calibration':max_difference,'metric_boundary':'two-sided envelope tolerance, silence, gain; polarity explicitly ungraded','original_code_executed':False,'manifest_sha256':sha(P/'manifest.json')}
if __name__=='__main__':
 r=main();(HERE/'review-validation.json').write_text(json.dumps(r,indent=1)+'\n');print(json.dumps(r))
