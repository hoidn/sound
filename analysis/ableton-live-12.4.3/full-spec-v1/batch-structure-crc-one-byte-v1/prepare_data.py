#!/usr/bin/env python3
"""Historical one-time materialization only. No old Python import or original invocation."""
import hashlib,json,os,pathlib,platform,shutil,sys
H=pathlib.Path(__file__).resolve().parent;B=H.parent;V=B.parent;T=V/'r2/t11-structure-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=pathlib.Path(p).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def crc(b):
 c=b<<8
 for _ in range(8):c=((c<<1)^0x8005 if c&0x8000 else c<<1)&65535
 return c
assert not (H/'inputs.json').exists()
manifest=json.loads((T/'manifest.json').read_text())
for n in ('x-crc/x_crc.py','out/x-crc.json'):
 p=T/n;z=manifest['files'][n];q=pin(p);assert q['bytes']==z['bytes'] and q['sha256']==z['sha256']
s=json.loads((T/'out/x-crc.json').read_text());assert s['function']=='0x101191310' and s['all_equal']
old={}
for index,byte in ((2,0),(3,255),(4,183)):
 r=s['runs'][index];assert r['bytes']==1 and r['sha256']==sha(bytes([byte])) and r['x86_result']==crc(byte) and r['ok'] and r['used_imports']=={} and r['calls']==1
 old[byte]={'summary_pointer':f'/runs/{index}','summary_path':str((T/'out/x-crc.json').resolve()),'summary_sha256':pin(T/'out/x-crc.json')['sha256'],'input_sha256':r['sha256'],'crc16':r['x86_result'],'rule':r['rule'],'calls':1,'used_imports':{},'pid':None,'utc':None,'raw_receipt':None,'limits':'Inherited approved summary and exact retained driver47-52/zeroing protocol; no oldraw reopening or invented PID/UTC/fulloutputword/return carriers'}
rows=[]
for b in range(256):rows.append({'id':f'CRC-{b:02x}','byte':b,'payload_hex':f'{b:02x}','input_sha256':sha(bytes([b])),'entry':'0x101191310','length':1,'initial_seed_bytes_le':'00000000','expected_low16':crc(b),'expected_low16_hex':f'{crc(b):04x}','expected_full32':None,'portable_comparator':None,'provenance':'inherited-summary' if b in old else 'fresh-selected','historical':old.get(b)})
fresh=[r for r in rows if r['byte'] not in old];plans=[]
for i,rs in enumerate((fresh[:127],fresh[127:])):
 tokens=[]
 for j,r in enumerate(rs):tokens+=['call','0x101191310','hex:'+r['payload_hex'],'i:1','buf:4','dump',f'b{2*j+1}','4']
 plans.append({'child':i,'calls':len(rs),'buffers':len(rs)*2,'row_ids':[r['id'] for r in rs],'tokens':tokens})
save('inputs.json',{'schema':'whole-initial-zero-one-byte-crc-v1','counts':{'logical':256,'inherited':3,'fresh_calls':253,'children':2,'calls_each':[127,126],'buffers_each':[254,252]},'rule':'Existing CRC16 poly0x8005,MSB first,initial0,no reflection,no finalxor; freeze expected integer before calls, not fit','semantic':'low16 of four output bytes little-endian; upper16 and RAX not promoted','rows':rows,'plans':plans})
(H/'protocol').mkdir()
for src,name in [(pathlib.Path('tools/xexec/xexec.c'),'xexec.c'),(pathlib.Path('tools/xexec/xexec.py'),'xexec.py'),(T/'x-crc/x_crc.py','x_crc.py'),(T/'out/x-crc.json','inherited-summary.json')]:shutil.copyfile(src,H/'protocol'/name)
paths=[T/'manifest.json',T/'x-crc/x_crc.py',T/'out/x-crc.json',pathlib.Path('tools/xexec/xexec.c'),pathlib.Path('tools/xexec/xexec.py'),B/'family-structure-als-routes-v1/manifest.json',B/'family-structure-als-routes-v1/structure.md',B/'family-structure-als-routes-v1/input-sets.json',B/'reviews/family-structure-als-routes-v1-review.json',pathlib.Path('wiki/research/live-set-structure.md'),pathlib.Path('wiki/specs/live-set-structure.md')]
save('authority-pins.json',[pin(p) for p in paths])
loader='/var/tmp/sound-analysis/xexec-t11/xexec';image='/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64';watched=[pin(p) for p in [loader,image,sys.executable,'/usr/lib/x86_64-linux-gnu/libc.so.6','/usr/lib/x86_64-linux-gnu/libm.so.6','/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2']]
assert watched[0]['bytes']==74096 and watched[0]['sha256']=='48dd0ba0c8d8c9de0d492f950ded67575885e7ccb62623eeb550d0334f5b7b40';assert watched[1]['sha256']=='1bae9a972abadea304271696a2ccfe0ffb878d37e23a8d8e52effa297be999b0'
assert pin('tools/xexec/xexec.c')['sha256']==manifest['harness']['tools/xexec/xexec.c'] and pin('tools/xexec/xexec.py')['sha256']==manifest['harness']['tools/xexec/xexec.py']
save('context.json',{'loader':loader,'image':image,'watched':watched,'environment':{'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC'},'host':{'uname':list(platform.uname()),'python':sys.version,'python_executable':sys.executable,'byteorder':sys.byteorder},'protocol':'Existing unmodified xexec-t11. RDI=data owned1B buffer, RSI=integer1, RDX=freshzero4B seed/output buffer by retained xcall tooling; no target-entry register tracing. dump b(2j+1) 4; result little-endian32 &ffff.','counted_imports_allowed':[],'limits':'253new target calls/2children127+126;two fresh owned buffers per call254/252<256. No object/factory/init/patch/GDB or new model/tool/runtime. Input buffer mutation/oracle disagreement/status/import anomaly stops later unlaunched children; queued calls inside an already running child may already execute.','hash_role':'Fresh full image/executable/runtime hashes custody only, no code/symbol/provider/content analysis.','source_scope':'Existing bounded x_crc.py and tools/xexec protocol read inertly, no oldraw/originalfunction body/native/provider acquisition. Existing driver is never imported/run (Runner could autobuild).','scope':'Local initial0 one-byte checksum only; not actual file reading,matching,Save/Open,ARM,public applicability or release/grade'})
print(json.dumps({'logical':256,'fresh':253,'historical_bytes':[0,183,255],'new_plans':[{'calls':p['calls'],'buffers':p['buffers']} for p in plans],'loader':watched[0]}))
