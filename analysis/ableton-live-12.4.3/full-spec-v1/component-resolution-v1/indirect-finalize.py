"""Cached static DATA readback only: never invokes decoder/collector/original code."""
from pathlib import Path
import ast,hashlib,json,datetime,sys
OUT=Path(__file__).resolve().parent
B=OUT.parent;N3=B.parent/'r2/n3-transitions-v1'
def load(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def locate(p,predicate):
 found=[]
 with p.open('rb') as f:
  line=0
  while True:
   off=f.tell();r=f.readline()
   if not r:break
   line+=1;x=json.loads(r)
   if predicate(x):found.append((x,dict(path=str(p),line=line,byte_offset=off,raw_bytes=len(r),raw_sha256=hashlib.sha256(r).hexdigest())))
 assert len(found)==1;return found[0]
def main():
 if sys.argv[1:]!=['--check-cached']:raise SystemExit('Only cached data readback; no decoder or original execution.')
 selection=load(OUT/'indirect-selection.json');batch=load(OUT/'indirect-native-batch.json');header=load(OUT/'indirect-native-header.json');baseline=load(OUT/'indirect-baseline.json')
 assert batch['status']=='PASS STATIC_DATA_ONLY' and len(batch['results'])==23
 classfile=OUT/'class-tables.jsonl';assert ident(classfile)['sha256']=='ca8bfd6d39d486fab03b4f6fe5cdb28b9b255a5d4c86d16da81d8507bf6a2bf6'
 table,where=locate(classfile,lambda x:x['address_point']=='0x106756188')
 assert where['line']==9532 and where['byte_offset']==25461166 and where['raw_sha256']=='a6c177a66b81174aaf5c71fe22a2cc74fb0a8f93e6103fd6996b57f881f4e7ea'
 assert table['literal_type_encoding']=='18OSendThreadMessage' and table['literal_store_candidate_count']==12
 slot=next(x for x in table['slots'] if x['offset']==16);assert slot['target']=='0x101ab7898' and slot['raw8_hex']=='9878ab0101000000'
 paths={Path(x['path']) for x in load(OUT/'indirect-native-before.json')['files']}|{classfile,N3/'manifest.json',N3/'binary-reads.json',N3/'results/n3-0002/functions/0x101ab7348.json',N3/'results/n3-0001/functions/0x101a4abd8.json'}
 for r in batch['results']:
  assert r['exit']==0 and r['exception'] is None and r['attempted']==1 and r['returned_pid'] is not None
  stem='indirect-native-'+r['function'];paths.update(OUT/(stem+s) for s in ('.bin','.json','.stderr','-status.json','-attempt.json'))
 before=[ident(p) for p in sorted(paths)]
 manifest=load(N3/'manifest.json')
 for p in [N3/'binary-reads.json',N3/'results/n3-0002/functions/0x101ab7348.json',N3/'results/n3-0001/functions/0x101a4abd8.json']:
  g=ident(p);e=manifest['files'][str(p.relative_to(N3))];assert(g['bytes'],g['sha256'])==(e['bytes'],e['sha256'])
 # Reuse only fully read pure analyst integer/predicate definitions, never collector/import/main.
 source=(OUT/'indirect-resolve.py').read_text();tree=ast.parse(source);names={'word','add_sp_x0','ldr_sp_x8','bl_target','safe_arg_setup','bind','selfcheck'};functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names];assert len(functions)==7
 ns={'CTOR':'0x101ab7348'};exec(compile(ast.Module(body=functions,type_ignores=[]),'<pure-class-slot-readback>','exec'),ns);checks=ns['selfcheck']()
 result=[];fresh=0;no_caller_helpers=0
 for r in selection['records']:
  if r['reuse_native_dossier']:
   p=N3/'results/n3-0001/functions/0x101a4abd8.json';native=load(p)['disassembly'];rows=[dict(offset=int(x['address'],16),bytes=x['bytes'],opcode=x['text'],size=4,type='unknown') for x in native];source_ref=ident(p);rawref=None;actualrowprefix='/disassembly/'
  else:
   stem='indirect-native-'+r['function'];p=OUT/(stem+'.json');rows=load(p);raw=(OUT/(stem+'.bin')).read_bytes();status=load(OUT/(stem+'-status.json'));assert status['raw']==ident(OUT/(stem+'.bin')) and not (OUT/(stem+'.stderr')).read_bytes();assert len(rows)*4==len(raw) and b''.join(bytes.fromhex(x['bytes']) for x in rows)==raw
   assert all(x['offset']==int(r['start'],16)+i*4 and x['size']==4 for i,x in enumerate(rows));fresh+=len(rows);source_ref=ident(p);rawref=status['raw'];actualrowprefix='/'
  proof,reason=ns['bind'](rows,int(r['constructor']['record']['site'],16),int(r['indirect']['record']['site'],16));assert reason is None and proof is not None
  no_caller_helpers+=not proof['opaque_intermediate_calls'];wanted=set(proof['dispatch_pcs']+[proof['constructor_receiver_pc'],proof['constructor_call_pc']]);critical=[]
  for i,x in enumerate(rows):
   if hex(x['offset']) in wanted:critical.append(dict(pc=hex(x['offset']),raw4=x['bytes'],decoder_text=x['opcode'],json_pointer=actualrowprefix+str(i)))
  # Every native/index/source locator is dereferenced rather than trusted by shape.
  for key in ('constructor','indirect'):
   w=r[key]['locator'];p0=Path(w['path'])
   with p0.open('rb') as f:f.seek(w['byte_offset']);rawrow=f.read(w['raw_bytes'])
   assert hashlib.sha256(rawrow).hexdigest()==w['raw_sha256'] and json.loads(rawrow)==r[key]['record']
  w=r['source_locator']
  with Path(w['path']).open('rb') as f:f.seek(w['byte_offset']);rawrow=f.read(w['raw_bytes'])
  assert hashlib.sha256(rawrow).hexdigest()==w['raw_sha256'] and json.loads(rawrow)['code']==r['source_code']
  result.append(dict(site=r['indirect']['record']['site'],function=r['function'],status='new_conditional_static_exact_target',index_locator=r['indirect']['locator'],index_exported_targets=[],class_literal='18OSendThreadMessage',address_point='0x106756188',slot='0x10',target='0x101ab7898',class_recovery_locator=where,class_slot=slot,native_source=source_ref,native_raw=rawref,native_critical_rows=critical,proof=proof,source_locator=w,code_sha256=r['source_metadata']['code_sha256'],premises=['Reached normal constructor and later indexed dispatch, valid stack/code/memory.','SP ABI and the constructed object firstword survive constructor and intervening opaque calls; no interfering aliases or relevant writes.','Nominal RTTI/table/unslid slot chain holds; no actual runtime execution, order, owner semantics or complete class set established.']))
 assert fresh==675 and len(result)==24 and len({x['site'] for x in result})==24 and no_caller_helpers==5
 after=[ident(p) for p in sorted(paths)];assert before==after
 with (OUT/'indirect-resolution.jsonl').open('w') as f:
  for r in result:f.write(json.dumps(r,separators=(',',':'))+'\n')
 report=load(OUT/'indirect-report.json');report.update(fresh_decoder_children=23,fresh_instructions=675,fresh_bytes=2700,reused_selected_instructions=33,reused_dossier_total_rows=40,selected_instruction_budget=708,no_intervening_caller_call_sites=5,intervening_caller_call_sites=19,class_recovery=ident(classfile),class_recovery_locator=where,input_readback=dict(watched=len(paths),unchanged=True),source_read_scope='All24selected complete C projections and all constructor-setup/dispatch critical native rows read; exact675new rows bytevalidated and sourcePC/slot/receiver integer predicates checked. This is not all98,328sourcefunctions or every table/method reviewed.',predecode_authoring_failure='One SyntaxError before source selection/decoder execution; corrected before any decoder. No failed decoder/retry.',selfcheck=checks)
 (OUT/'indirect-report.json').write_text(json.dumps(report,indent=2)+'\n')
 (OUT/'indirect-validation.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),before=before,after=after,unchanged=True,checks=checks,new_sites=24,exported_metric_unchanged=25071,function_target_metric_unchanged=21685,combined_conditional_inventory=25095,decoder_replay=False,original_execution=False),indent=2)+'\n')
 print(json.dumps(dict(status='PASS cached readback',resolved_conditional=24,watched=len(paths),fresh_instructions=fresh,class_locator=where),indent=2))
if __name__=='__main__':main()
