#!/usr/bin/env python3
"""One-time initial materialization; historical code, not a final replay recipe."""
import hashlib,json,os,pathlib,platform,re,shutil,struct,sys
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent;B=H.parent;R=B.parents[2];OLD=B/'batch-mix-leaves-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=pathlib.Path(p).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not (H/'inputs.json').exists()
manifest=json.loads((OLD/'manifest.json').read_text())
for name in ('inputs.json','results.jsonl'):
 p=OLD/name;q=next(x for x in manifest['files'] if x['path']==name);assert len(p.read_bytes())==q['bytes'] and sha(p.read_bytes())==q['sha256']
inputs=json.loads((OLD/'inputs.json').read_text());raw=(OLD/'results.jsonl').read_bytes().splitlines(keepends=True);offsets=[];at=0
for line in raw:offsets.append(at);at+=len(line)
results=[json.loads(x) for x in raw];fns=['0x101b1a470','0x101b1a550','0x101b1a630','0x101b1a6f0','0x101b1a7b0','0x101b1a880','0x101b1a8e0'];names=['NormalDip / Dipped','SlightDip / Intermediate','ConstantPower','Dipless / SlowFade','SlowCut','FastCut','Transition'];oldk={-64,-60,-48,-32,-16,0,16,32,48,60,64};joins={};chosen=set()
for c,fn in enumerate(fns):
 for k in sorted(oldk):
  token='f:'+(k/64).hex();matches=[]
  for i,d in enumerate(inputs):
   if k not in (-16,16) and i!=137+c:continue
   if k in (-16,16) and d['kind']!='retained-unpatched-call-shape':continue
   t=d['tokens']
   for j in range(0,len(t),3):
    if t[j:j+3]==['call',fn,token]:matches.append((i,j//3))
  assert len(matches)==1,(c,k,matches)
  i,j=matches[0];r=results[i];assert r['id']==inputs[i]['id'] and r['rc']==0 and not r['timeout'] and not r['stderr']
  line=next(x for x in r['stdout'].splitlines() if x.startswith(f'call {j} '));m=re.fullmatch(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)',line);assert m and m[2]==fn
  carriers={n:f'{int(v,16):016x}' for n,v in zip(('rax','rdx','xmm0','xmm1'),m.groups()[2:])};chosen.add(i)
  joins[c,k]={'input_row_index':i,'input_id':inputs[i]['id'],'input_tokens_offset':j*3,'result_line':i+1,'result_byte_offset':offsets[i],'result_raw_bytes':len(raw[i]),'result_raw_sha256':sha(raw[i]),'call_index':j,'call_line':line,'carriers64':carriers,'bits32':carriers['xmm0'][-8:],'started_utc':r['started_utc'],'finished_utc':r['finished_utc'],'pid':None,'pid_limit':'not recorded by historical recorder; no new receipt fabricated','source_locator':inputs[i].get('source_locator'),'result_source':str(OLD/'results.jsonl')}
selected=bytearray();record_index=[]
for i in sorted(chosen):
 record_index.append({'original_index':i,'original_line':i+1,'original_byte_offset':offsets[i],'selected_offset':len(selected),'bytes':len(raw[i]),'sha256':sha(raw[i])});selected.extend(raw[i])
assert len(chosen)==21
(H/'inherited-records.jsonl').write_bytes(selected);save('inherited-index.json',record_index)
rows=[];plans=[]
for c,fn in enumerate(fns):
 for k in range(-64,65):
  hist=joins.get((c,k));rows.append({'id':f'MK{c}-{k+64:03d}','curve':c,'name':names[c],'k':k,'i':k+64,'function':fn,'token':'f:'+(k/64).hex(),'input_bits32':f'{struct.unpack("<I",struct.pack("<f",k/64))[0]:08x}','provenance':'inherited-approved' if hist else 'fresh-selected','historical':hist,'expected_bits32':hist['bits32'] if hist else None,'oracle_class':'inherited-reference-bits' if hist else 'NULL-discovery-regular-node','portable_comparator':None})
 rr=[r for r in rows if r['curve']==c and r['historical'] is None];plans.append({'curve':c,'function':fn,'row_ids':[r['id'] for r in rr],'tokens':[v for r in rr for v in ('call',fn,r['token'])]})
save('inputs.json',{'schema':'whole-mixer-129-regular-knots-v1','counts':{'logical':903,'inherited':77,'fresh_targets':826,'children':7,'calls_per_child':118,'buffers':0,'initializers':0},'definition':'All seven helper functions at p=i/64-1, i=0..128; scalar outputs only, not runtime table observations','rows':rows,'plans':plans})
(H/'protocol').mkdir();src=B.parent/'r2/t14-mix-v1/harness'
# B.parent is version root; no old module imported/executed.
for name in ('xexec.c','xexec.py'):shutil.copyfile(src/name,H/'protocol'/name)
pins=[]
for p in [OLD/'manifest.json',OLD/'inputs.json',OLD/'results.jsonl',B/'reviews/batch-mix-leaves-v1-review.json',B/'family-mixer-routes-v1/manifest.json',B/'family-mixer-routes-v1/structure.md',B/'mixer-values-owner-r6-batch/manifest.json',B.parent/'r2/t14-mix-v1/manifest.json',src/'xexec.c',src/'xexec.py',pathlib.Path('wiki/specs/mixer-values.md'),pathlib.Path('wiki/research/mixer-values.md')]:pins.append(pin(p))
save('authority-pins.json',pins)
loader='/var/tmp/sound-analysis/xexec-t14/xexec';image='/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64';watched=[pin(p) for p in [loader,image,sys.executable,'/usr/lib/x86_64-linux-gnu/libc.so.6','/usr/lib/x86_64-linux-gnu/libm.so.6','/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2']]
assert watched[0]['sha256']=='188b1197bd69ab4700ae47eade48f00982a2d11139d865f3cee46e64b80d3078' and watched[1]['sha256']=='1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
save('context.json',{'loader':loader,'image':image,'watched':watched,'environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'},'host':{'uname':list(platform.uname()),'python':sys.version,'python_executable':sys.executable,'byteorder':sys.byteorder},'declared_header':'loaded rebases=789951 binds-linux=103 binds-trap=42781 symbols=1882','imports_allowed_used':['_cos','_cosf'],'execution':'Unmodified T14 xexec; f:hex binary32 argument; scalar entry; no buffers/init/patch; glibc trigonometry substitution only','limits':'20s per child/256 existing queued-call cap;118 direct calls selected; low32 XMM0 return; high lanes and RAX/RDX recorded without semantic assumption','phase_limit':'Host parser check does not prove actual entry-register contents or fenv; libc double-to-float temporary cast is recorded tooling, not original ABI proof','source_scope':'No newly acquired original source/body/native/provider; retained harness source copied inertly. Existing REQ014 tablebuilder crosswalk nominates grid only.'})
print(json.dumps({'materialized_rows':len(rows),'selected_historical_records':len(chosen),'runtime_custody':watched[:2]}))
