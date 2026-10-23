"""Fixed ownedpacket-only checks; no external pins/corpus/images/tools/children/oldimports or models."""
import copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent
PRE='73825cb1842e6cce84198baf9cb946d7a716b0983d13f06da41db0b2b07781c5'
CALLS={0x101b0:0x1cf3c,0x101dc:0x1cf3c,0x101fc:0x1ed6c,0x1021c:0x1ed6c,0x1023c:0x20cc0,0x1025c:0x1ed6c,0x1027c:0x1ed6c,0x1029c:0x1ed6c}
# pc: kind, Rt, Rn, encoded byte offset, effective incomingI offset, full store width
STORES={0x10090:('X',31,0,0,0,8),0x10094:('W',31,0,8,8,4),0x100a4:('preX',8,19,0x10,0x10,8),0x100ac:('preX',31,28,0x20,0x20,8),0x100b0:('pair',31,0,0x28,0x28,16),0x100b8:('preX',8,20,0x68,0x68,8),0x100c0:('preX',31,22,0x78,0x78,8),0x100c4:('pair',31,0,0x80,0x80,16),0x100d4:('preX',25,21,0xc0,0xc0,8),0x100dc:('preX',31,23,0xd0,0xd0,8),0x100e0:('pair',31,0,0xd8,0xd8,16),0x100ec:('X',25,0,0x110,0x110,8),0x100f8:('pair',31,0,0x128,0x128,16),0x100fc:('X',31,0,0x120,0x120,8),0x10110:('X',8,0,0x160,0x160,8),0x1011c:('pair',31,0,0x170,0x170,16),0x10120:('X',31,0,0x180,0x180,8),0x1012c:('X',25,0,0x1b0,0x1b0,8),0x10138:('pair',31,0,0x1c0,0x1c0,16),0x1013c:('X',31,0,0x1d0,0x1d0,8),0x10144:('X',25,0,0x200,0x200,8),0x10150:('X',31,0,0x218,0x218,8),0x10154:('X',31,0,0x210,0x210,8),0x10158:('X',31,0,0x220,0x220,8),0x10160:('X',25,0,0x250,0x250,8),0x1016c:('X',31,0,0x268,0x268,8),0x10170:('X',31,0,0x260,0x260,8),0x10174:('X',31,0,0x270,0x270,8),0x1017c:('D',0,0,0x2a0,0x2a0,8),0x10180:('D',0,0,0x2a8,0x2a8,8),0x10184:('D',0,0,0x2b0,0x2b0,8)}
FIX={0x1006c:0xd10283ff,0x1008c:0xaa0003f8,0x100a0:0xaa0003f3,0x100a8:0xaa0003fc,0x100b4:0xaa0003f4,0x100bc:0xaa0003f6,0x100d0:0xaa0003f5,0x100d8:0xaa0003f7,0x100e4:0x91044008,0x100e8:0xf9001fe8,0x10100:0x91058008,0x10104:0xf9001be8,0x10124:0x9106c008,0x10128:0xf90017e8,0x10140:0x9108001a,0x1015c:0x9109401b,0x10178:0x0f03f600,0x10188:0x529c0008,0x1018c:0x72a8d568,0x10190:0x1e270101,0x10194:0x52a88f48,0x10198:0x1e270102,0x1019c:0x1e27d000,0x101a0:0xaa1303e0,0x101b4:0x529999a8,0x101b8:0x72a7b988,0x101c0:0x52a85e08,0x101cc:0xaa1403e0,0x101ec:0xaa1503e0,0x1020c:0xf9401fe0,0x1022c:0xf9401be0,0x1024c:0xf94017e0,0x1026c:0xaa1a03e0,0x1028c:0xaa1b03e0,0x102a0:0xaa1803e0,0x102bc:0x910283ff,0x102c0:0xd65f03c0}
def need(v,m):
 if not v:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def fields(W):
 for pc,(kind,rt,rn,off,eff,width)in STORES.items():
  w=W[pc];need(w&31==rt and w>>5&31==rn,'storereg')
  if kind=='preX':need(w&0xffe00c00==0xf8000c00 and sx(w>>12&511,9)==off,'preindexX')
  elif kind=='pair':need(w&0xffc00000==0xa9000000 and w>>10&31==31 and sx(w>>15&127,7)*8==off,'GPRpair')
  else:
   op,scale={'X':(0xf9000000,8),'W':(0xb9000000,4),'D':(0xfd000000,8)}[kind];need(w&0xffc00000==op and(w>>10&4095)*scale==off,'unsignedstore')
 for pc,w in FIX.items():need(W[pc]==w,'criticalcarrier/FP/frame:'+hex(pc))
 for pc,target in CALLS.items():need(W[pc]&0xfc000000==0x94000000 and pc+4*sx(W[pc]&0x3ffffff,26)==target,'all8directcalls')
 for pc,t in[(0x10098,0x583e0),(0x100c8,0x584c0),(0x10108,0x585a0)]:
  w=W[pc];need(w&0x9f000000==0x10000000 and pc+sx((w>>5&0x7ffff)*4+(w>>29&3),21)==t,'codeADR')
def claims(a):
 need(a['scope']=={'whole_C_records':1,'C_bytes':1467,'C_lines':55,'warnings':0,'native_bytes':600,'native_rows':150,'new_data_bytes':0},'scope')
 r=a['carrier_status'];need(r['return_incoming_I']=='conditional-normal-return-callee-preservation'and r['direct_store_excludes_Q_firstword']=='conditional-offset-only','conditionalreturn/store')
 for k in['full_helper_preserves_Q_current_vptr','actual_public_entry_class_ABI','runtime_encoding_current_table_callback_E_R','callee_effects_and_lifecycle','numeric_default_math_calibration_oracle']:need(r[k]=='unknown','unknownjoin')
 need(len(a['claims'])==6 and len(a['direct_state_writes'])==31 and len(a['call_frontier'])==8 and a['no_successor_selected']and a['required_status']=='U/OPEN unchanged'and a['new_resolved_runtime_sites']==a['new_cases_grades_releases']==0,'noclosure')
 need(a['main_Live_inventory']=='25095 of268015 unchanged','maincount')
def check():
 pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');p=json.loads(pb);need(p['ranges']==[{'start':'0x1006c','end_exclusive':'0x102c4','file_offset':65644,'bytes':600,'words':150}]and p['data_words']==[],'exactscope')
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');need(len(before)==18 and before==[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]==after['files']and after['unchanged'],'18custody')
 for pin in p['pins']:
  q=Path(pin['path'])
  if q.parent==P:
   b=q.read_bytes();need(len(b)==pin['bytes']and H(b)==pin['sha256'],'ownedpin')
 st=J('capture/status.json');need(st['error']is None and st['watch_unchanged']and not st['automatic_retry']and st['attempts']==st['children_started']==1 and st['selected_bytes_read']==st['validated_bytes']==600 and st['validated_words']==150 and st['selected_table_bytes_read']==st['native_original_instruction_execution']==0,'oncecapture')
 need(J('capture/table-words.json')['words']==[],'nodata')
 src=(P/'source-context.jsonl').read_bytes();md=J('selected-metadata.json')['source'];d=json.loads(src);c=d.pop('code');need(len(src)==1874 and H(src)==md['raw_sha256']and d==md['metadata'],'rawC1');need(len(c.encode())==1467 and len(c.splitlines())==55 and H(c.encode())==d['code_sha256'],'wholeC');need(d['body_ranges']==[['0x1006c','0x102c3']]and d['body_bytes']==600 and not d['thunk']and not d['warnings']and not d['partial_code']and not d['timed_out']and d['error']is None,'Cstatus')
 rr=J('source-read-receipt.json');need(rr['approval_verified_before_C_read_utc']<=rr['selected_C_retention_finished_utc']<st['started_utc'],'sourcechronology')
 raw=(P/'capture/1006c.bin').read_bytes();rows=J('capture/1006c.stdout.json');need(len(raw)==600 and len(rows)==150,'wholeextent');need(J('capture/extraction.json')['ranges']==[{**p['ranges'][0],'sha256':H(raw)}],'extracthash');W={};flows=[];pairs=[]
 for i,r in enumerate(rows):
  pc=0x1006c+4*i;bb=raw[4*i:4*i+4];need(type(r['offset'])is int and r['offset']==pc and type(r['size'])is int and r['size']==4 and r['bytes']==bb.hex(),'all150associations');w=int.from_bytes(bb,'little');W[pc]=w
  if w&0x7c000000==0x14000000:
   target=pc+4*sx(w&0x3ffffff,26);need(r.get('jump')==target,'rawrelative');flows.append({'pc':hex(pc),'form':'BL'if w>>31 else'B','target':hex(target)})
  elif w&0xfffffc1f in[0xd61f0000,0xd63f0000,0xd65f0000]:flows.append({'pc':hex(pc),'form':{0xd61f0000:'BR',0xd63f0000:'BLR',0xd65f0000:'RET'}[w&0xfffffc1f],'Rn':w>>5&31})
  elif w&0xff000010==0x54000000 or w&0x7e000000 in[0x34000000,0x36000000]:raise ValueError('unexpectedconditionalbranch')
  if w&0x3a000000==0x28000000:
   v=w>>26&1;opc=w>>30;scale=(4<<opc)if v else(8 if opc==2 else 4);pairs.append({'pc':hex(pc),'FP_SIMD':bool(v),'load':bool(w>>22&1),'element_bytes':scale,'Rt':w&31,'Rt2':w>>10&31,'Rn':w>>5&31,'byte_offset':sx(w>>15&127,7)*scale,'mode':w>>23&3})
 fields(W);need(len(flows)==9 and len(pairs)==18,'allflowpairs')
 a=J('assessment.json');claims(a)
 for x,(pc,(kind,rt,rn,off,eff,width))in zip(a['direct_state_writes'],STORES.items()):need(x['pc']==hex(pc)and x['effective_I_offset']==hex(eff)and x['bytes']==width and x['end_exclusive']==hex(eff+width),'allstoreledger')
 need(min(x[4]for x in STORES.values())==0 and max(x[4]+x[5]for x in STORES.values())==0x2b8,'boundinginterval')
 for x,(pc,t)in zip(a['call_frontier'],CALLS.items()):need(x['pc']==hex(pc)and x['target']==hex(t)and x['target_content_read']is False,'wholecallfrontier')
 rc=J('capture/1006c.invocation-after.json');pr=J('capture/1006c.invocation-before.json');pid=J('capture/1006c.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m','0x1006c','-s','0x1006c','-q','-c','pdj 150',str(P/'capture/1006c.bin')]
 need(rc['argv']==pr['argv']==pid['argv']==argv and rc['pid']==pid['pid']==pid['pgid'],'argvpid');need(rc['started_utc']<=pid['spawned_utc']<=rc['finished_utc'],'times');need(rc['exit_code']==0 and rc['error']is None and not rc['timed_out']and(P/'capture/1006c.stderr').read_bytes()==b''and rc['timeout_seconds']==30 and rc['stdin']=='DEVNULL'and rc['core_limit_bytes']==0 and rc['new_process_session']and rc['cleanup']=='process-group-already-gone','processstatus')
 neg=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError,TypeError):neg.append(n);return
  raise ValueError('acceptednegative:'+n)
 for name,pc,bit in[('savedIcarrier',0x1008c,16),('incomingreturn',0x102a0,16),('preindexwriteback',0x100a4,10),('scalarwidth',0x10094,30),('firstaddress',0x10098,5),('laststateoffset',0x10184,10),('FPrawform',0x10178,5),('nestedcalltarget',0x101b0,0),('stackinteriorpointer',0x1020c,10),('frameamount',0x102bc,10)]:
  z=W.copy();z[pc]^=1<<bit;reject(name,lambda z=z:fields(z))
 for name,key,v in[('wholehelperexclusion','full_helper_preserves_Q_current_vptr','proved'),('publicABI','actual_public_entry_class_ABI','proved'),('runtimeclass','runtime_encoding_current_table_callback_E_R','proved'),('calleeeffects','callee_effects_and_lifecycle','provedbounded'),('defaultmathoracle','numeric_default_math_calibration_oracle','proved'),('unconditionalreturn','return_incoming_I','unconditional')]:
  z=copy.deepcopy(a);z['carrier_status'][key]=v;reject(name,lambda z=z:claims(z))
 z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automaticfollow',lambda:claims(z))
 if(P/'manifest.json').exists():
  m=J('manifest.json');need({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and q.name!='manifest.json'}=={x['path']for x in m['files']},'sealedtree')
  for x in m['files']:
   b=(P/x['path']).read_bytes();need(len(b)==x['bytes']and H(b)==x['sha256'],'sealedpin')
 return {'status':'PASS-ownedpacket-only','C_bytes':1467,'C_lines':55,'warnings':0,'native_bytes':600,'native_rows':150,'data_bytes':0,'recorded_custody_pairs':18,'receipts':[rc],'all_raw_flow_fields':flows,'all_GPR_FP_SIMD_pairs':pairs,'all31_direct_state_store_fields':[{'pc':hex(pc),'kind':v[0],'Rt':v[1],'Rn':v[2],'encoded_offset':hex(v[3]),'effective_I_offset':hex(v[4]),'bytes':v[5]}for pc,v in STORES.items()],'critical_carrier_FP_frame_forms':len(FIX),'negative_controls':neg,'external_domain_reopens':0,'decoder_original_model_calls':0,'limits':'Exactstaticselectedfields/directspanonly, nottransitivehelperexclusion/translatedmodel/runtimeABI/class/math/publicproof;ESILunused.'}
if __name__=='__main__':
 need(sys.argv[1:]==['--check'],'only --check')
 print(json.dumps(check(),indent=2))
