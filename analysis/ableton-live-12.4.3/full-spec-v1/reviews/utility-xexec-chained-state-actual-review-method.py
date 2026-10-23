from pathlib import Path
import ast,hashlib,json,re,struct,datetime
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-xexec-chained-state-preparation';A=B/'depth-utility-xexec-chained-state';O=B/'reviews/utility-xexec-chained-state-selected-execution'
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for r in iter(lambda:f.read(1048576),b''):h.update(r);n+=len(r)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def load(p):return json.loads(p.read_text())
def maprows(x):return x if isinstance(x,list) else x['files']
inner=maprows(load(A/'before-map.json'));outer=maprows(load(O/'before-map.json'));assessment=B/'reviews/utility-xexec-chained-state-root-assessment.json'
paths=sorted({Path(x['path']) for x in inner+outer}|set(A.iterdir())|set(O.iterdir())|set(P.iterdir())|{assessment});before=[ident(p) for p in paths]
assert ident(A/'manifest.json')['sha256']=='63846593390a469fc9883f8c574b2b67a72c59739a98e5704feda92140c5d4e4';assert ident(O/'manifest.json')['sha256']=='8203b7ecd5a7a5de64d8213db99f5f7e37324a8ecfa9030e6b34e8887b268d36'
for root,count in [(P,7),(A,10),(O,12)]:
 m=load(root/'manifest.json');assert len(m['files'])==count;assert {x['path'] for x in m['files']}=={p.name for p in root.iterdir() if p.is_file() and p.name!='manifest.json'}
 for x in m['files']:
  y=ident(root/x['path']);assert(y['bytes'],y['sha256'])==(x['bytes'],x['sha256'])
for root,rows,count in [(A,inner,48),(O,outer,5136)]:
 assert len(rows)==count and rows==maprows(load(root/'after-map.json')) and load(root/'after-map.json')['unchanged']
 for x in rows:assert ident(Path(x['path']))==x
pins=load(P/'inputs.json')['pins'];opins=load(O/'pins.json')
for x in pins+opins:assert ident(Path(x['path']))==x
sel=load(O/'selection.json');wrapper=(O/'execute-selected-once.py').read_text();old=Path(sel['wrapper_parent']['path']);assert ident(old)==sel['wrapper_parent']
restored=wrapper
for a,b in reversed(sel['literal_operations']):assert restored.count(b)==1;restored=restored.replace(b,a)
assert restored==old.read_text() and len(sel['literal_operations'])==8
for k in ['preparation','collector','root_preflight','peer_preflight','wrapper']:assert ident(Path(sel[k]['path']))==sel[k]
assert ident(A/'capture-once.py')['sha256']==ident(P/'capture-once.py')['sha256']
plan=load(P/'plan.json');inv=load(A/'invocation.json');assert inv['argv']==plan['argv'] and inv['environment']==plan['environment'] and inv['timeout_seconds']==20 and inv['posthoc_code_comparison']
assert load(A/'attempt.json')['argv']==inv['argv'];status=load(A/'status.json');receipt=load(O/'receipt.json');assert status['attempts']==1 and status['returned_pid']==858017 and status['completed_original_call_rows']==4 and status['exit']==0 and status['exception'] is None and not status['timeout'] and status['capture_complete']
assert receipt['outer_wrapper_pid']==857997 and receipt['returned_collector_pid']==858014 and receipt['attempted_collector_launches']==1 and receipt['exit']==0 and receipt['exception'] is None and not receipt['timeout'] and not receipt['cleanup_group_killed'];assert load(O/'collector-pid.json')['pid']==858014 and load(A/'returned-pid.json')['pid']==858017
assert load(O/'collector.stdout.json')==status and not (O/'collector.stderr').read_bytes() and not (A/'child.stderr').read_bytes()
assert sel['utc']<receipt['started_utc']<status['started_utc']<status['finished_utc']<receipt['finished_utc'];assert load(O/'post-group-observation.json')['observed_residuals']==[]
# Independently read every line; no supplied parser/function import or execution.
ls=(A/'child.stdout').read_text().splitlines();parsed=load(A/'parsed.json');head=re.fullmatch(r'loaded rebases=(\d+) binds-linux=(\d+) binds-trap=(\d+) symbols=(\d+)',ls[0]);assert head
imports={};i=1
while i<len(ls) and ls[i].startswith('import '):
 m=re.fullmatch(r'import (linux|linux-data|trap) (\S+) slots=([1-9]\d*)',ls[i]);assert m;k,n,c=m.groups();assert n not in imports;imports[n]=dict(category=k,slots=int(c));i+=1
counts=list(map(int,head.groups()));assert counts==[789951,103,42781,1882] and len(imports)==1882
assert sum(x['slots'] for x in imports.values() if x['category']!='trap')==103 and sum(x['slots'] for x in imports.values() if x['category']=='trap')==42781
assert parsed['imports']==imports and parsed['loaded']==dict(rebases=789951,linux_slots=103,trap_slots=42781,symbols=1882)
expected=[('0x104b8c760',13,'554889e54088b7cf0000005dc3'),('0x104b8c7b0',920,((B/'depth-utility-x86-process-span/process-span-904.bin').read_bytes()+(B/'depth-utility-x86-mode-table-data/mode-table-16.bin').read_bytes()).hex())]
for a,n,h in expected:
 assert ls[i]==f'dump {a} {a} {h}';i+=1
assert parsed['code_dumps']==[dict(address=a,bytes=n,hex=h,matches_retained=True) for a,n,h in expected] and parsed['code_matches']
returns=[];states=[];auto=None;auto_input=None;pointer0=None;pointer1=None
for k,addr in enumerate(['0x104b8c7b0','0x104b8c7b0','0x104b8c760','0x104b8c7b0']):
 m=re.fullmatch(r'call (\d+) (0x[0-9a-f]+) rax=(0x[0-9a-f]+) rdx=(0x[0-9a-f]+) xmm0=(0x[0-9a-f]+) xmm1=(0x[0-9a-f]+)',ls[i]);assert m;i+=1;g=m.groups();assert int(g[0])==k and g[1]==addr and all(int(x,16)<1<<64 for x in g[2:]);returns.append(dict(index=k,address=addr,**dict(zip(['rax','rdx','xmm0','xmm1'],g[2:]))))
 if k==0:
  m=re.fullmatch(r'out b0 (0x[0-9a-f]+) ([0-9a-f]{416})',ls[i]);assert m;i+=1;pointer0,auto=m.groups()
  m=re.fullmatch(r'out b1 (0x[0-9a-f]+) ([0-9a-f]{16})',ls[i]);assert m;i+=1;pointer1,auto_input=m.groups()
 m=re.fullmatch(r'dump b0 (0x[0-9a-f]+) ([0-9a-f]{416})',ls[i]);assert m;i+=1;ptr,h=m.groups();assert ptr==pointer0;raw=bytes.fromhex(h)
 states.append(dict(after_call=k,hex=h,counter48_u64=struct.unpack_from('<Q',raw,0x48)[0],counter88_u64=struct.unpack_from('<Q',raw,0x88)[0],pair38_hex=raw[0x38:0x40].hex(),common78_hex=raw[0x78:0x80].hex(),flag_cf_u8=raw[207]))
assert ls[i]=='dump b1 '+pointer1+' '+auto_input;i+=1;assert i==len(ls)
assert int(pointer0,16)%16==0 and int(pointer1,16)%16==0 and int(pointer0,16)+208<=int(pointer1,16)
assert parsed['calls']==returns and parsed['states_after_each_call']==states and parsed['state_buffer_address']==pointer0 and parsed['input_buffer_address']==pointer1
assert parsed['automatic_state_after_call0_hex']==auto and auto==states[0]['hex'];assert parsed['automatic_input_after_call0_hex']==parsed['final_input_hex']==auto_input=='0000803f000000c0'
assert parsed['used']=={} and parsed['actual_expected'] is None and parsed['comparison'] is None and parsed['new_grade']==0
assert parsed['observations']==dict(automatic_vs_explicit_state0_equal=True,input_after_history_unchanged=True,final_helper_low64_xmm0_zero=True) and parsed['completed_original_call_rows']==4
assert set(parsed)=={'loaded','imports','used','code_dumps','code_matches','calls','completed_original_call_rows','state_buffer_address','input_buffer_address','automatic_state_after_call0_hex','automatic_input_after_call0_hex','states_after_each_call','final_input_hex','observations','actual_expected','comparison','new_grade','limits'}
helpers=[struct.unpack('<ff',int(returns[k]['xmm0'],16).to_bytes(8,'little')) for k in (0,1,3)];commons=[struct.unpack('<ff',bytes.fromhex(s['common78_hex'])) for s in states]
assert helpers==[(1.,-2.),(1.5,-2.5),(0.,0.)] and commons==[(1.5,1.25),(2.,1.5),(2.,1.5),(2.,1.5)]
diff_setter=[k for k,(a,b) in enumerate(zip(bytes.fromhex(states[1]['hex']),bytes.fromhex(states[2]['hex']))) if a!=b];assert diff_setter==[207] and states[2]['hex']==states[3]['hex']
assert [s['counter48_u64'] for s in states]==[1,2,2,2] and [s['counter88_u64'] for s in states]==[1,2,2,2]
after=[ident(p) for p in paths];assert before==after
maphash=lambda rows:hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
evidence=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),subject_manifest=ident(A/'manifest.json'),outer_manifest=ident(O/'manifest.json'),status='PASS independent retained-data review',inventories=dict(prep=7,actual=10,outer=12),inner_paired=48,outer_paired=5136,current_pins=len(pins),outer_pins=len(opins),wrapper_inverse_operations=8,original_children=1,complete_original_return_rows=4,stdout_lines=len(ls),all_import_records=len(imports),import_slots=counts,all_raw_fields_equal_parsed=True,code_dumps_match_retained=True,returns=returns,helper_pairs=helpers,state_pairs78=commons,state_counter48=[s['counter48_u64'] for s in states],state_counter88=[s['counter88_u64'] for s in states],setter_change_byte_indices=diff_setter,post_setter_equals_post_helper=True,automatic_state0_equals_explicit=True,input_post0_equals_final=True,input_before0_snapshot=False,root_assessment=ident(assessment),watch=dict(paths=len(paths),before_metadata_sha256=maphash(before),after_metadata_sha256=maphash(after),unchanged=True,scope='Union of retained paired-map paths/current preparation+actual+outer+Root assessment. Full old durable maps referenced in actual packets, not duplicated here.'),reviewer_original_or_collector_or_decoder_execution=False)
p=B/'reviews/utility-xexec-chained-state-actual-review-evidence.json'
with p.open('x') as f:json.dump(evidence,f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=ident(p),watch=len(paths),helper_pairs=helpers,common_pairs=commons,imports=len(imports),wrapper_inverse=8),indent=2))
