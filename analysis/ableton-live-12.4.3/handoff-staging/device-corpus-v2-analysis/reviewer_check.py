"""Independent finite handoff checks. Data/new measurement code only; no DSP execution."""
from pathlib import Path
import base64, hashlib, importlib.util, json, math, os, re, shutil, struct, subprocess, sys, tempfile
R=Path(__file__).resolve().parents[4]
A=Path(__file__).resolve().parent
P=A.with_name('device-corpus-v2')
OLD=R/'handoff/device-corpus-v1'
B=R/'analysis/ableton-live-12.4.3/full-spec-v1'
sys.dont_write_bytecode=True

def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 if sys.argv[1:]!=['--check']:raise SystemExit('Only --check; no original execution/replay.')
 assert not (A/'reviewer-validation.json').exists()
 stage_files=[q for q in P.rglob('*') if q.is_file()]
 old_files=[q for q in OLD.rglob('*') if q.is_file()]
 private=[q for q in A.iterdir() if q.is_file()]
 providers=[]
 for directory in ['depth-corpus-lfo-ramp-up','depth-corpus-lfo-ramp-sensitivity','depth-corpus-lfo-ramp-criterion','corpus-owner-r4']:
  providers += [q for q in (B/directory).rglob('*') if q.is_file()]
 for n in ['corpus-lfo-ramp-up-review.json','corpus-lfo-ramp-sensitivity-review.json','corpus-lfo-ramp-criterion-review.json','corpus-owner-r4-review.json']:
  providers.append(B/'reviews'/n)
 watched={str(q):pin(q) for q in stage_files+old_files+private+providers}
 assert len(stage_files)==85 and len(old_files)==84
 assert (A/'manifest-at-review.json').read_bytes()==(P/'manifest.json').read_bytes()
 assert pin(P/'manifest.json')=={'bytes':17270,'sha256':'014ea1087dd0ff1f0b0017118538c9de507a80b41814e2ef5fda6fd43af0d854'}
 for directory in [P,OLD]:
  manifest=json.loads((directory/'manifest.json').read_text());paths={x['path'] for x in manifest['files']}
  assert {str(q.relative_to(directory)) for q in directory.rglob('*') if q.is_file()}==paths|{'manifest.json'}
  for x in manifest['files']:assert pin(directory/x['path'])=={k:x[k] for k in ['bytes','sha256']}
 old=json.loads((OLD/'cases.json').read_text());new=json.loads((P/'cases.json').read_text())
 old_eval={e['id']:e for g in old['cases'] for e in g['evaluations']};new_eval={e['id']:e for g in new['cases'] for e in g['evaluations']}
 assert len(old_eval)==68 and len(new_eval)==69 and all(new_eval[k]==v for k,v in old_eval.items())
 assert len(new['cases'])==24 and list(new_eval.keys()-old_eval.keys())==['CORPUS-AUDIO-020-02']
 for i,(g,h) in enumerate(zip(old['cases'],new['cases'])):
  if i==19:assert {k:v for k,v in g.items() if k not in ['evaluations','purpose']}=={k:v for k,v in h.items() if k not in ['evaluations','purpose']}
  else:assert g==h
 fixtures=[q for q in OLD.rglob('*.f32')];assert len(fixtures)==77
 assert all(q.read_bytes()==(P/q.relative_to(OLD)).read_bytes() for q in fixtures)
 refs=list((P/'reference').glob('*.f32'));signals=list((P/'signals').glob('*.f32'))
 assert len(refs)==69 and len(signals)==9 and len({pin(q)['sha256'] for q in refs})==62
 # Exact v1 code reconstruction is text comparison ONLY, never old tool replay.
 source=(P/'compare.py').read_text();restored=source.replace('import hashlib\n','',1)
 start=restored.index("        elif kind == 'ramp_waveform':");end=restored.index("        elif kind == 'startup':",start);restored=restored[:start]+restored[end:]
 start=restored.index("                if evaluation['metric']['kind'] == 'ramp_waveform':");end=restored.index('                result = compare(',start);restored=restored[:start]+restored[end:]
 assert restored.encode()==(OLD/'compare.py').read_bytes()
 ramp=new_eval['CORPUS-AUDIO-020-02'];sine=new_eval['CORPUS-AUDIO-020-01']
 for k in sine:
  if k not in ['id','parameters','reference','metric']:assert ramp[k]==sine[k]
 assert {k:(v,ramp['parameters'][k]) for k,v in sine['parameters'].items() if v!=ramp['parameters'][k]}=={'LfoType':(0.,3.)}
 script=(B/'depth-corpus-lfo-ramp-up/raw/ramp-up.script').read_text().splitlines()
 params=[x.split()[1:] for x in script if x.startswith('param ')]
 assert len(params)==len(ramp['parameter_order'])==38
 for (i,v),n in zip(params,ramp['parameter_order']):assert ramp['parameter_order'][int(i)]==n and struct.pack('<f',float(v))==struct.pack('<f',ramp['parameters'][n])
 # Use the exact source pin from private trace rather than constructing source paths by guess.
 trace=json.loads((A/'traceability-new-ramp.json').read_text())
 assert (P/ramp['signal']).read_bytes()==Path(trace['signal_source']['path']).read_bytes()
 assert (P/ramp['reference']).read_bytes()==(R/trace['new_capture_raw']['path']).read_bytes()
 assert ramp['before_parameters']==ramp['after_parameters']==[] and ramp['metric']=={'kind':'ramp_waveform'}
 assert pin(B/'corpus-owner-r4/spec-r4.md')=={'bytes':41194,'sha256':'62ccc40debde55baf7fed54bbbc6eaa803f0d6a12f2a3b4b2841baabae6775d8'}
 for row in trace['independent_pins']:assert pin(R/row['path'])=={k:row[k] for k in ['bytes','sha256']}
 # Payload types/sanitization and local links, with no analyst sibling resolution.
 assert all(not q.is_symlink() for q in P.rglob('*'))
 assert len([q for q in stage_files if q.suffix=='.py'])==1
 links=0
 for q in stage_files:
  if q.suffix=='.f32':assert len(q.read_bytes())==131072;continue
  text=q.read_text()
  assert not re.search(r'/home/|/var/tmp/|analysis/|wiki/|FUN_[0-9a-fA-F]|Ghidra|\.bundle|0x10[0-9a-fA-F]{7}',text),q
  if q.suffix=='.md':
   for target in re.findall(r'\]\(([^)]+)\)',text):
    if '://' in target or target.startswith('#'):continue
    dest=(q.parent/target.split('#')[0]).resolve();assert dest.is_relative_to(P.resolve()) and dest.is_file(),(q,target);links+=1
 measure=load(P/'compare.py','independent_current_handoff_measurement')
 pure=load(B/'depth-corpus-lfo-ramp-criterion/compare_ramp.py','independent_new_criterion')
 assert len(pure.self_test())==19
 ref=measure.audio(P/ramp['reference']);raw=(P/ramp['reference']).read_bytes();metric=ramp['metric'];checks=[]
 with tempfile.TemporaryDirectory(prefix='corpus-v2-independent-export-') as td:
  temp=Path(td)
  for label,rel in [('nominal','depth-corpus-lfo-ramp-up/raw/ramp-up.f32'),('plus1','depth-corpus-lfo-ramp-sensitivity/raw/plus1.f32'),('minus1','depth-corpus-lfo-ramp-sensitivity/raw/minus1.f32'),('Sine','depth-corpus-lfo-ramp-up/raw/sine-baseline.f32')]:
   b=(B/rel).read_bytes();q=temp/'trial.f32';q.write_bytes(b);actual=measure.compare(measure.audio(q),ref,metric,44100);expected=pure.compare_bytes(raw,b)
   assert actual['pass']==expected['accepted'] and [x['error'] for x in actual['measurements']]==[x['relative_rms_error'] for x in expected['channels']];checks.append('exact-vector-'+label)
  syn=measure.np.zeros((16384,2));syn[4096]=[100.,100.];bits=struct.unpack('<I',struct.pack('<f',101.))[0];lo=struct.unpack('<f',struct.pack('<I',bits-1))[0];hi=struct.unpack('<f',struct.pack('<I',bits+1))[0]
  for n,l,r,expected in [('below',lo,lo,True),('equal',101.,101.,True),('above',hi,hi,False),('left-only-fails',hi,100.,False),('right-only-fails',100.,hi,False)]:
   q=syn.copy();q[4096]=[l,r];assert measure.compare(q,syn,metric,44100)['pass'] is expected;checks.append(n)
  for c in [0,1]:
   q=ref.copy();q[4096:,c]=0
   try:measure.compare(q,ref,metric,44100)
   except ValueError:checks.append('silent-channel-'+str(c))
   else:raise AssertionError('silent channel accepted')
  for n,b in [('short',raw[:-4]),('extra',raw+bytes(8)),('prefixNaN',struct.pack('<f',float('nan'))+raw[4:]),('lastInf',raw[:-4]+struct.pack('<f',float('inf')))]:
   q=temp/'invalid.f32';q.write_bytes(b)
   try:measure.audio(q)
   except ValueError:checks.append(n)
   else:raise AssertionError('invalid file admitted')
  for frame in [4096,16383]:
   q=ref.copy();q[frame,0]=100.;assert not measure.compare(q,ref,metric,44100)['pass'];checks.append('scored-endpoint-'+str(frame))
  q=ref.copy();q[:4096]=123.;assert measure.compare(q,ref,metric,44100)['pass'];checks.append('finite-prefix-ungraded')
  export=temp/'export';shutil.copytree(P,export);output=temp/'outputs';shutil.copytree(P/'reference',output)
  env=os.environ.copy();env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
  def cli():
   result=subprocess.run([sys.executable,'-B',str(export/'compare.py'),str(output)],cwd=temp,env=env,capture_output=True,text=True);return result.returncode,json.loads(result.stdout)
  code,all_results=cli();assert code==0 and all_results['pass'] and len(all_results['results'])==69
  measurements=sum(len(x['measurements']) for x in all_results['results']);assert measurements==4603;checks.append('portable-69-selfcomparisons-4603-measurements')
  (export/'cases.json').write_text(json.dumps({'cases':[{'evaluations':[ramp]}]}))  # one-evaluation test fixture for negative CLI paths
  (export/ramp['reference']).write_bytes((B/'depth-corpus-lfo-ramp-up/raw/sine-baseline.f32').read_bytes())
  code,failed=cli();row=next(x for x in failed['results'] if x['id']==ramp['id']);assert code==1 and not row['pass'] and 'reference hash' in row['error'];checks.append('portable-reference-hash-refused')
  (export/ramp['reference']).write_bytes(raw);(output/(ramp['id']+'.f32')).unlink()
  code,failed=cli();row=next(x for x in failed['results'] if x['id']==ramp['id']);assert code==1 and not row['pass'];checks.append('portable-missing-output-refused')
 assert all(pin(Path(n))==h for n,h in watched.items())
 result={'status':'pass','stage_manifest_at_review':pin(P/'manifest.json'),'checks':checks,'pure_selftests':19,'old_evaluations_exact':68,'old_fixtures_exact':77,'new_evaluation':'CORPUS-AUDIO-020-02','parent_case':'DCO-029','groups':24,'evaluations':69,'references':69,'distinct_reference_streams':62,'signals':9,'self_measurements':4603,'old_comparator_reconstruction_exact':True,'links':links,'stage_files':85,'watched_paths':len(watched),'watch_before':watched,'after_equal':True,'pending_REVIEW_bytes_base64':base64.b64encode((P/'REVIEW.md').read_bytes()).decode(),'pending_REVIEW_identity':pin(P/'REVIEW.md'),'private_author_validation_named_checks':len(json.loads((A/'author-validation.json').read_text())['checks']),'no_original_or_candidate_execution':True,'execution_scope':'Only fully inspected newly staged measurement code and newly authored criterion pure checks; no old tool/collector/native DSP/replay.','final_public_review_not_yet_written':True}
 (A/'reviewer-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['watch_before','pending_REVIEW_bytes_base64']},indent=2))
if __name__=='__main__':main()
