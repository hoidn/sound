"""Independent stdlib byte recipes and four-axis arithmetic; no supplied code imported."""
from pathlib import Path
import datetime, hashlib, json, math, struct
BASE=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=BASE/'depth-corpus-pickup-step-method-validation'
ROOT=BASE/'reviews/corpus-pickup-step-method-root-validation'
OUT=BASE/'reviews/corpus-pickup-step-method-actual-review-evidence.json'
AX=[('preL',4096,8192,0),('preR',4096,8192,1),('postL',8192,16384,0),('postR',8192,16384,1)]
def digest(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=digest(b))
def verify(p,r):
 b=p.read_bytes();assert (len(b),digest(b))==(r['bytes'],r['sha256']),str(p)
def packed(v): return struct.pack('<32768f',*v)
def samples(b): return struct.unpack('<32768f',b)
def passed(v): return math.isfinite(v) and 0<=v<=.01
# Historical paired maps are assessed as-of, not asserted to be a future mutable canonical gate.
map_info=[]; watched=set(P.rglob('*'))|set(ROOT.iterdir())
for directory,count in [(P,128),(ROOT,2120)]:
 before=load(directory/'watch-before.json');after=load(directory/'watch-after.json')
 assert len(before)==count and len({x['path'] for x in before})==count
 assert before==after['files'] and after['changed']==[]
 map_info.append(dict(directory=str(directory),count=count,paired_equal=True))
 for r in before:
  if directory==P or '/handoff/' in r['path']:
   verify(Path(r['path']),r);watched.add(Path(r['path']))
watched={x for x in watched if x.is_file()}|{Path(__file__).resolve()}
watch_before=[identity(x) for x in sorted(watched)]
assert not OUT.exists()
manifest=load(P/'manifest.json')
assert digest((P/'manifest.json').read_bytes())=='1364401c1222cf8ec694383125790234ccac8553701e2be72ff60ec296f9cdc3'
assert len(manifest['files'])==87 and len({x['path'] for x in manifest['files']})==87
assert {x.relative_to(P).as_posix() for x in P.rglob('*') if x.is_file()}=={'manifest.json'}|{r['path'] for r in manifest['files']}
for r in manifest['files']:verify(P/r['path'],r)
pins=load(P/'source-preparation/inputs.json')['pins'];assert len(pins)==15
for r in pins:verify(Path(r['path']),r)
providers={r['role']:Path(r['path']) for r in pins}
for f in (P/'source-preparation').iterdir():assert f.read_bytes()==(BASE/'depth-corpus-pickup-step-method-validation-preparation'/f.name).read_bytes()
sel=load(ROOT/'selection.json');receipt=load(ROOT/'receipt.json');attempt=load(P/'attempt.json')
assert sel['argv']==['python3','-B',*attempt['argv']]
assert sel['selected_utc']<attempt['started_utc']<receipt['finished_utc']
assert receipt['exit']==0
assert sel['original_children_before']==receipt['original_children_after']==17
for k in ['stdout','stderr','results']:verify(Path(receipt[k]['path']),receipt[k])
assert (ROOT/'validator.stderr').read_bytes()==b''
stdout=load(ROOT/'validator.stdout');assert stdout['watch_unchanged'] and stdout['watched']==128
ref=providers['step_reference'].read_bytes();control=providers['matched_control'].read_bytes()
REF=digest(ref);assert REF=='1336d90115bd24c058e556aa95e9140014d168dad7111dec64eb8edd1d977e73'
v=list(samples(ref));cv=samples(control);syn=[0.0]*32768
for _,lo,_,c in AX:syn[2*lo+c]=100.
synraw=packed(syn);nanref=struct.pack('<f',math.nan)+synraw[4:]
assert (P/'controls/synthetic-reference.f32').read_bytes()==synraw
assert (P/'controls/synthetic-NaN-reference-input.f32').read_bytes()==nanref
# Derive the complete expected raw set independently from the declared recipes.
recipes={}
def add(name,data,reference=ref,synthetic=False,expected=None):
 assert name not in recipes;recipes[name]=(data,reference,synthetic,expected)
add('step-self',ref,expected=True);add('ignored-step-control',control,expected=False)
for axis,lo,hi,c in AX:
 z=v.copy()
 for n in range(lo,hi):z[2*n+c]=1.02*z[2*n+c]
 add('scaled-1p02-'+axis,packed(z),expected=False)
for axis,lo,hi,c in AX:
 z=v.copy()
 for n in range(lo,hi):z[2*n+c]=0.
 add('zero-'+axis,packed(z),expected=False)
for name,b in [('all-zero',bytes(131072)),('short',ref[:-4]),('extra',ref+bytes(4)),('odd',ref[:-1]),('prefix-NaN',struct.pack('<f',math.nan)+ref[4:]),('last-Inf',ref[:-4]+struct.pack('<f',math.inf))]:add(name,b,expected=False)
add('wrong-real-reference',control,control,expected=False)
add('synthetic-self',synraw,synraw,True,True);add('synthetic-rejected-by-real-gate',synraw,synraw,False,False)
bits=struct.unpack('<I',struct.pack('<f',101.))[0]
for axis,lo,_,c in AX:
 for label,shift in [('below',-1),('boundary',0),('above',1)]:
  z=syn.copy();z[2*lo+c]=struct.unpack('<f',struct.pack('<I',bits+shift))[0]
  add('synthetic-'+axis+'-'+label,packed(z),synraw,True,label!='above')
add('synthetic-zero-reference',synraw,bytes(131072),True,False)
add('synthetic-NaN-reference',synraw,nanref,True,False)
z=v.copy();z[-1]+=.005*math.sqrt(math.fsum(t*t for t in v[16385:32768:2]))
add('last-sample-concentrated-error',packed(z),expected=True)
for d in [1,512]:
 z=v.copy()
 for n in range(8192,16384):
  for c in [0,1]:z[2*n+c]=cv[2*n+c] if n<8192+d else v[2*(n-d)+c]
 add('artificial-waveform-splice-'+str(d),packed(z))
z=v.copy();z[31744:]=[0.]*1024;add('last512-zeroed-limit',packed(z))
z=v.copy();z[0]=123.;add('finite-prefix-not-scored',packed(z),expected=True)
def arithmetic(r,b,synthetic):
 reason=None
 if not synthetic and digest(r)!=REF:reason='Real reference hash differs from pinned pickup step'
 elif len(r)!=131072 or len(b)!=131072:reason='Expected exactly 16384 stereo binary32 frames'
 elif not all(math.isfinite(x) for raw in [r,b] for x in samples(raw)):reason='Nonfinite full-file sample'
 rows=[]
 for axis,lo,hi,c in AX:
  er=ey=de=error=None;valid=False
  if reason is None:
   rs=samples(r)[2*lo+c:2*hi:2];ys=samples(b)[2*lo+c:2*hi:2]
   er=math.fsum(x*x for x in rs);ey=math.fsum(x*x for x in ys)
   differences=[ys[i]-rs[i] for i in range(len(rs))]
   de=math.fsum(d*d for d in differences)
   valid=math.isfinite(er) and math.isfinite(ey) and er>0 and ey>0
   if valid:error=math.sqrt(de/er)
  rows.append(dict(axis=axis,window=[lo,hi],channel=c,valid=valid,reference_energy=er,candidate_energy=ey,error_energy=de,error=error,tolerance=.01,**{'pass':valid and passed(error)}))
 result=dict(valid=all(x['valid'] for x in rows),**{'pass':all(x['pass'] for x in rows)},axes=rows)
 if reason is not None:result['reason']=reason
 return result
results=load(P/'results.json');records=results['comparisons']
assert len(recipes)==len(records)==38 and [x['name'] for x in records]==list(recipes)
computed={};evidence=[]
for row in records:
 name=row['name'];b,r,synthetic,expected=recipes[name];path=P/'controls'/(name+'.f32')
 assert path.read_bytes()==b and load(path.with_suffix('.json'))==row
 assert row['path']==str(path) and row['bytes']==len(b) and row['sha256']==digest(b)
 assert row['reference_sha256']==digest(r) and row['synthetic_arithmetic_only']==synthetic and row['expected_pass'] is expected
 got=arithmetic(r,b,synthetic);assert got==row['result'],name
 computed[name]=got;evidence.append(dict(name=name,raw_bytes_reconstructed=True,result=got))
checks={}
def require(name,ok):assert name not in checks;checks[name]=bool(ok);assert ok,name
def rr(name):return computed[name]
for name,(_,_,_,exp) in recipes.items():
 if exp is not None:require(name+' outcome',rr(name)['pass'] is exp)
require('self all four zero',all(a['valid'] and a['error']==0 for a in rr('step-self')['axes']))
a=rr('ignored-step-control');require('ignored-step positive postL failure only',a['valid'] and a['axes'][2]['error']>.01 and all(a['axes'][i]['pass'] and a['axes'][i]['error']==0 for i in [0,1,3]))
for i,(axis,_,_,_) in enumerate(AX):
 a=rr('scaled-1p02-'+axis)
 require(axis+' positive finite error rejects',a['valid'] and a['axes'][i]['error']>.01 and not a['axes'][i]['pass'])
 require(axis+' other three remain self',all(a['axes'][j]==rr('step-self')['axes'][j] for j in range(4) if i!=j))
 require(axis+' zero energy invalid',not rr('zero-'+axis)['valid'])
 for label in ['below','boundary','above']:
  a=rr('synthetic-'+axis+'-'+label);x=a['axes'][i]['error']
  require(axis+' '+label+' numeric boundary',a['valid'] and (x<.01 if label=='below' else x==.01 if label=='boundary' else x>.01))
  require(axis+' '+label+' other axes zero',all(a['axes'][j]['error']==0 for j in range(4) if i!=j))
for name in ['all-zero','short','extra','odd','prefix-NaN','last-Inf']:require(name+' invalid not a scored pass',not rr(name)['valid'])
require('wrong hash gated before math',rr('wrong-real-reference')['reason']=='Real reference hash differs from pinned pickup step')
require('synthetic has no real trust',rr('synthetic-rejected-by-real-gate')['reason']=='Real reference hash differs from pinned pickup step')
require('synthetic reference energy checked',not rr('synthetic-zero-reference')['valid'])
require('synthetic reference full finite checked',not rr('synthetic-NaN-reference')['valid'])
scalar=[]
for name,x,exp in [('zero',0.,True),('inclusive',.01,True),('outside',math.nextafter(.01,math.inf),False),('negative',-1.,False),('NaN',math.nan,False),('Inf',math.inf,False)]:
 require('scalar '+name,passed(x) is exp);scalar.append(dict(name=name,value_repr=repr(x),**{'pass':passed(x)},expected=exp))
assert scalar==results['scalar_boundary_tests']
assert len(checks)==89 and {x['name']:x['pass'] for x in results['requirements']}==checks and len(results['requirements'])==89
assert sum(a['valid'] for x in computed.values() for a in x['axes'])==108
assert results['comparison_count']==38 and results['axis_records']==152 and results['all_required_controls_pass'] is True
assert results['grade'] is None and results['new_cases']==results['new_native_calls']==0
assert len(list((P/'controls').iterdir()))==78
watch_after=[identity(Path(x['path'])) for x in watch_before];assert watch_after==watch_before
report=dict(status='PASS independent byte recipes and exact arithmetic',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checker=identity(Path(__file__).resolve()),packet_manifest=identity(P/'manifest.json'),historical_maps=map_info,own_watch_before=watch_before,own_watch_after=watch_after,own_watch_unchanged=True,comparisons=38,axis_records=152,valid_axes=108,invalid_axes=44,required_checks=89,scalar_tests=scalar,all_required_checks=checks,independent_results=evidence,original_calls=0,supplied_evaluator_executed=False,grade=None)
with OUT.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=report['status'],comparisons=38,axes=152,required_checks=89,watch=len(watch_before),evidence=identity(OUT))))
