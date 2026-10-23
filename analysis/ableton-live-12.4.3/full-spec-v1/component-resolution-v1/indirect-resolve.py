"""One bounded retained-class batch. Static Rizin decoding only, no original execution."""
from pathlib import Path
from collections import defaultdict
import datetime,hashlib,json,os,resource,subprocess,sys,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
OUT=Path(__file__).resolve().parent
I=Path('/var/tmp/sound-analysis/corpus/indexes')
CHUNKS=Path('/var/tmp/sound-analysis/corpus/decomp/chunks')
N3=B.parent/'r2/n3-transitions-v1'
IMAGE=B.parent/'derived/Live.arm64'
TOOL=Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
CTOR='0x101ab7348'; CANONICAL='0x101a4abd8'; TABLE=0x106756188; TARGET='0x101ab7898'
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def iterrows(p):
 with p.open('rb') as f:
  n=0
  while True:
   offset=f.tell();raw=f.readline()
   if not raw:break
   n+=1;yield json.loads(raw),dict(path=str(p),line=n,byte_offset=offset,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())
def select():
 calls=defaultdict(list);ind=defaultdict(list)
 for x,w in iterrows(I/'calls.jsonl'):
  if x['to']==CTOR:calls[x['caller']].append(dict(record=x,locator=w))
 for x,w in iterrows(I/'indirect.jsonl'):
  if x['function'] in calls:ind[x['function']].append(dict(record=x,locator=w))
 eligible=[f for f in sorted(calls,key=lambda x:int(x,16)) if len(calls[f])==len(ind[f])==1 and not ind[f][0]['record']['resolved_targets'] and ind[f][0]['record']['kind']=='call' and 0<int(ind[f][0]['record']['site'],16)-int(calls[f][0]['record']['site'],16)<=512]
 chosen=[CANONICAL]+[f for f in eligible if f!=CANONICAL][:23];assert len(chosen)==24 and CANONICAL in eligible
 ordinal=0;positions={}
 for x,w in iterrows(I/'aliases.jsonl'):
  if not x['external']:
   if x['entry'] in chosen:positions[x['entry']]=(ordinal,w)
   ordinal+=1
 records=[]
 for f in chosen:
  k,alias=positions[f];p=CHUNKS/f'chunk-{k//100:05d}.jsonl';found=[(x,w) for x,w in iterrows(p) if x['entry']==f];assert len(found)==1
  x,w=found[0];assert x['state'] in ('exported','exported-with-warnings') and not x['partial_code'] and not x['timed_out'] and not x['thunk']
  site=int(ind[f][0]['record']['site'],16);start=int(f,16);end=site+4;assert start%4==end%4==0 and (end-start)//4<=512
  assert any(int(a,16)<=start and end-1<=int(z,16) for a,z in x['body_ranges'])
  assert len(x['code'].encode())==x['code_bytes'] and hashlib.sha256(x['code'].encode()).hexdigest()==x['code_sha256']
  records.append(dict(function=f,constructor=calls[f][0],indirect=ind[f][0],alias_locator=alias,source_locator=w,source_metadata={k:v for k,v in x.items() if k!='code'},source_code=x['code'],start=hex(start),end_exclusive=hex(end),instructions=(end-start)//4,reuse_native_dossier=f==CANONICAL))
 assert sum(r['instructions'] for r in records)<=4096
 return dict(constructor=CTOR,constructor_callers=len(calls),eligible_callers=len(eligible),rule='Canonical transport caller then first23 other eligible functions sorted numeric VA; exactly one ctorcall and one empty indirectCALL afterctor<=512B. No ownership inferred from numeric proximity.',max_functions=24,max_instructions_per_function=512,max_total_instructions=4096,selected_instructions=sum(r['instructions'] for r in records),records=records)
def no_core():resource.setrlimit(resource.RLIMIT_CORE,(0,0))
def native_collect(selection):
 receipt=OUT/'indirect-native-batch.json';assert not receipt.exists()
 assert ident(IMAGE)['sha256']=='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad' and IMAGE.stat().st_size==149711904
 assert ident(TOOL)['sha256']=='ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba'
 with IMAGE.open('rb') as f:
  header=f.read(32);v=struct.unpack('<IiiIIIII',header);assert v[:3]==(0xfeedfacf,0x100000c,0);commands=f.read(v[5]);segments=[];cursor=0
  for _ in range(v[4]):
   cmd,n=struct.unpack_from('<II',commands,cursor);assert n>=8 and cursor+n<=len(commands)
   if cmd==0x19:
    name,va,vs,fo,fs,mp,ip,ns,fl=struct.unpack_from('<16sQQQQiiII',commands,cursor+8);assert fo+fs<=149711904;segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,initprot=ip))
   cursor+=n
  assert cursor==len(commands)
  save(OUT/'indirect-native-header.json',dict(image=ident(IMAGE),tool=ident(TOOL),header_hex=header.hex(),load_commands_sha256=hashlib.sha256(commands).hexdigest(),ncmds=v[4],sizeofcmds=v[5],segments=segments))
  results=[]
  for r in selection['records']:
   if r['reuse_native_dossier']:continue
   a,z=int(r['start'],16),int(r['end_exclusive'],16);match=[s for s in segments if s['vmaddr']<=a and z<=s['vmaddr']+s['filesize'] and s['initprot']&4];assert len(match)==1
   offset=match[0]['fileoff']+a-match[0]['vmaddr'];f.seek(offset);raw=f.read(z-a);assert len(raw)==z-a
   stem='indirect-native-'+r['function'];binary=OUT/(stem+'.bin');stdout=OUT/(stem+'.json');stderr=OUT/(stem+'.stderr');assert not binary.exists() and not stdout.exists() and not stderr.exists();binary.write_bytes(raw)
   argv=[str(TOOL),'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(a),'-s',hex(a),'-q','-c','pdj '+str(len(raw)//4),str(binary)]
   status=dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),function=r['function'],start=r['start'],end_exclusive=r['end_exclusive'],file_offset=offset,raw=ident(binary),argv=argv,attempted=1,returned_pid=None,exit=None,exception=None,original_execution=False)
   save(OUT/(stem+'-attempt.json'),status);child=None;out=err=b''
   try:
    child=subprocess.Popen(argv,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C'},cwd=OUT,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=no_core);status['returned_pid']=child.pid
    try:out,err=child.communicate(timeout=30)
    except subprocess.TimeoutExpired:child.kill();out,err=child.communicate();raise
    status['exit']=child.returncode
   except BaseException as e:status['exception']=type(e).__name__+': '+str(e)
   finally:
    if child is not None and child.poll() is None:child.kill();out,err=child.communicate()
    if child is not None:status['exit']=child.returncode
    status['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();stdout.write_bytes(out);stderr.write_bytes(err);save(OUT/(stem+'-status.json'),status);results.append(status);save(receipt,dict(status='IN_PROGRESS_OR_FAILURE',results=results))
   assert status['exception'] is None and status['exit']==0 and not err,'Decoder failure; stop batch, no retry'
   rows=json.loads(out);assert len(rows)==len(raw)//4
   assert b''.join(bytes.fromhex(x['bytes']) for x in rows)==raw
   for i,x in enumerate(rows):assert x['offset']==a+4*i and x['size']==4 and x['type'] not in ('invalid','ill') and isinstance(x.get('opcode'),str) and x['opcode'].strip().lower() not in ('','invalid','ill','none')
 save(receipt,dict(status='PASS STATIC_DATA_ONLY',results=results,decoder_children=len(results),original_calls=0))
def word(row):return int.from_bytes(bytes.fromhex(row['bytes']),'little')
def add_sp_x0(w):
 if w&0xffc003ff==0x910003e0:return (w>>10&0xfff)
 return None
def ldr_sp_x8(w):
 if w&0xffc003ff==0xf94003e8:return (w>>10&0xfff)*8
 return None
def bl_target(w,pc):
 if w>>26!=0x25:return None
 n=w&0x3ffffff;n=n-(1<<26) if n&(1<<25) else n;return pc+4*n
def safe_arg_setup(w):
 # Small allowlist only; no calls/branches/stores/SP or X0 writes between receiver formation and ctor.
 rd=w&31
 return rd not in (0,31) and ((w&0x1f800000)==0x12800000 or (w&0x1f000000)==0x10000000 or (w&0x7f000000)==0x11000000 or (w&0x7fe0ffe0)==0x2a0003e0)
def bind(rows,ctor_site,site):
 by={x['offset']:i for i,x in enumerate(rows)}
 if ctor_site not in by or site not in by:return None,'selected PCs absent'
 c,k=by[ctor_site],by[site]
 if bl_target(word(rows[c]),ctor_site)!=int(CTOR,16):return None,'ctor BL target mismatch'
 if k<3 or word(rows[k])!=0xd63f0100 or word(rows[k-2])!=0xf9400908:return None,'not literal slot10/BLRx8 suffix'
 offset=ldr_sp_x8(word(rows[k-3]));arg=add_sp_x0(word(rows[k-1]))
 if offset is None or arg!=offset:return None,'finish receiver and vptr load stack addresses differ/unsupported'
 setups=[i for i in range(max(0,c-12),c) if add_sp_x0(word(rows[i]))==offset]
 if not setups:return None,'no matching ctor stack receiver in bounded prefix'
 setup=setups[-1]
 if not all(safe_arg_setup(word(x)) for x in rows[setup+1:c]):return None,'unclassified receiver clobber/control before ctor'
 for x in rows[c+1:k-3]:
  op=x.get('opcode',x.get('text','')).lower()
  if x.get('type') in ('jmp','cjmp','rjmp','ujmp','ret') or op.startswith(('b.','b ','br ','cbz ','cbnz ','tbz ','tbnz ')):return None,'unfollowed non-call control flow between ctor/dispatch'
  if op.startswith(('add sp,','sub sp,')) or ('[sp' in op and ('!' in op or '], ' in op)):return None,'stack base changed between ctor/dispatch'
 return dict(stack_offset=offset,constructor_receiver_pc=hex(rows[setup]['offset']),constructor_call_pc=hex(ctor_site),dispatch_pcs=[hex(x['offset']) for x in rows[k-3:k+1]],opaque_intermediate_calls=[hex(x['offset']) for x in rows[c+1:k-3] if bl_target(word(x),x['offset']) is not None]),None
def selfcheck():
 def row(pc,w):return dict(offset=pc,bytes=w.to_bytes(4,'little').hex(),opcode='synthetic',type='mov')
 pc=0x101a00000;ctor=pc+8;site=pc+24;bl=0x94000000|((int(CTOR,16)-ctor)//4&0x3ffffff)
 rows=[row(pc,0x910003e0),row(pc+4,0x52800004),row(ctor,bl),row(pc+12,0xf94003e8),row(pc+16,0xf9400908),row(pc+20,0x910003e0),row(site,0xd63f0100)]
 assert bind(rows,ctor,site)[0] is not None
 bad=[]
 for i,w in [(3,0xf94007e8),(4,0xf9400d08),(5,0x910023e0),(6,0xd63f0120),(1,0x910023e0)]:
  q=[dict(r) for r in rows];q[i]=row(q[i]['offset'],w);assert bind(q,ctor,site)[0] is None;bad.append(i)
 assert bl_target(bl,ctor)==int(CTOR,16) and add_sp_x0(0x910083e0)==32 and ldr_sp_x8(0xf94013e8)==32
 return dict(valid=1,rejections=len(bad),predicate_fields=3)
def derive(selection):
 binary= json.loads((N3/'binary-reads.json').read_text());v=[x for x in binary['vtables'] if int(x['address_point'],16)==TABLE];assert len(v)==1 and v[0]['slots']['0x10']==TARGET and v[0]['rtti_name']=='18OSendThreadMessage'
 ctor=json.loads((N3/'results/n3-0002/functions/0x101ab7348.json').read_text());cs={x['address']:x for x in ctor['disassembly']};assert cs['0x101ab7360']['bytes']=='e86402f0' and cs['0x101ab7364']['bytes']=='08210691' and cs['0x101ab7368']['bytes']=='087c00a9'
 class_rows=[(x,w) for x,w in iterrows(OUT/'class-tables.jsonl') if int(x['address_point'],16)==TABLE]
 assert len(class_rows)==1
 cl,clwhere=class_rows[0]
 assert cl['literal_type_encoding']=='18OSendThreadMessage'
 slot=[x for x in cl['slots'] if x['offset']==16]
 assert len(slot)==1 and slot[0]['target']==TARGET and slot[0]['raw8_hex']=='9878ab0101000000'
 common=[ident(N3/'binary-reads.json'),ident(N3/'results/n3-0002/functions/0x101ab7348.json')];resolved=[];candidates=[]
 for r in selection['records']:
  if r['reuse_native_dossier']:
   source=N3/'results/n3-0001/functions/0x101a4abd8.json';native=json.loads(source.read_text())['disassembly'];rows=[dict(offset=int(x['address'],16),bytes=x['bytes'],opcode=x['text'],size=4,type='call' if x['text'].startswith('bl ') else 'ret' if x['text']=='ret' else 'unknown') for x in native];locator=dict(source=ident(source),pointer='/disassembly')
  else:
   source=OUT/('indirect-native-'+r['function']+'.json');rows=json.loads(source.read_text());locator=dict(source=ident(source),raw=ident(OUT/('indirect-native-'+r['function']+'.bin')))
  proof,reason=bind(rows,int(r['constructor']['record']['site'],16),int(r['indirect']['record']['site'],16))
  item=dict(site=r['indirect']['record']['site'],function=r['function'],kind=r['indirect']['record']['kind'],index_locator=r['indirect']['locator'],index_exported_targets=r['indirect']['record']['resolved_targets'],receiver_class_literal='18OSendThreadMessage',address_point=hex(TABLE),slot='0x10',implementation_targets=[TARGET],native=locator,constructor_source=common,source_locator=r['source_locator'],code_sha256=r['source_metadata']['code_sha256'],class_record_pointer='/vtables/0',class_recovery_locator=clwhere,class_recovery_slot=slot[0],premises=['Reached normal constructor/call/dispatch, valid stack/object and stable code.','Normal ABI-preserved SP and stack object; opaque helper calls do not change its firstword or create interfering aliases.','Nominal table/RTTI and unslid pointer interpretation hold; not current runtime dispatch or execution order.'])
  if proof:item.update(status='new_conditional_static_exact_target',proof=proof);resolved.append(item)
  else:item.update(status='candidate_not_counted',reason=reason);candidates.append(item)
 with (OUT/'indirect-resolution.jsonl').open('w') as f:
  for x in resolved+candidates:f.write(json.dumps(x,separators=(',',':'))+'\n')
 baseline=json.loads((OUT/'indirect-baseline.json').read_text());save(OUT/'indirect-report.json',dict(status='STATIC INVENTORY; not outcome coverage',baseline_exported_ref_sites=baseline['census']['nonempty_target_sites'],baseline_function_target_sites=baseline['census']['sites_with_function_field_target'],new_grounded_conditional_sites=len(resolved),candidate_sites_not_counted=len(candidates),combined_exported_or_conditional_site_inventory=baseline['census']['nonempty_target_sites']+len(resolved),denominator=baseline['census']['unique_sites'],selection={k:v for k,v in selection.items() if k!='records'},selfcheck=selfcheck(),receiver_class='18OSendThreadMessage',semantics='Only this constructed receiver class and constant slot are joined to native PCs. No class crossproduct or runtime/order/behavior assertion. Other class sources remain unassigned to sites until receiver+slot+PC proof.',sources=common,original_calls=0))
def main():
 if sys.argv[1:] not in (['--select'],['--decode-static'],['--derive']):raise SystemExit('Only fixed --select / separately selected --decode-static / cached --derive; no original execution.')
 selfcheck()
 if sys.argv[1:] == ['--select']:
  x=select();save(OUT/'indirect-selection.json',x);print(json.dumps({k:v for k,v in x.items() if k!='records'},indent=2))
 elif sys.argv[1:]==['--decode-static']:native_collect(json.loads((OUT/'indirect-selection.json').read_text()))
 else:derive(json.loads((OUT/'indirect-selection.json').read_text()))
if __name__=='__main__':main()
