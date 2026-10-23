"""Fixedpacket-only retaineddata checker; no external opens, children, oldhelpers or original/model execution."""
import copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent
PRE='99b26b38684fa710e79b4e6551a49be17b944f60912734c248f4963e1698928e'
RANGES=[(0x1cf3c,216),(0x1ed6c,212),(0x20cc0,224)]
DIRECT={0x1cf80:0x5085c,0x1cf9c:0x50b14,0x1cfc0:0x50b14,0x1edac:0x5085c,0x20d00:0x5085c}
# pc: form, Rt, secondRt forpair elseNone, Rn, offset, fullstorewidth
STORES={0x1cf68:('W',1,None,0,8,4),0x1cf84:('pairS',10,9,20,0x44,8),0x1cf8c:('S',13,None,20,0x4c,4),0x1cf94:('S',11,None,20,0x38,4),0x1cfa4:('pairS',0,8,20,0x3c,8),0x1cfb0:('S',0,None,20,0x34,4),0x1cfe8:('S',0,None,20,0x30,4),0x1cfec:('W',19,None,20,0x28,4),0x1cff8:('pairS',1,0,20,0x50,8),0x1ed94:('W',1,None,0,8,4),0x1edb0:('pairS',9,8,20,0x3c,8),0x1edb8:('S',0,None,20,0x44,4),0x1edc4:('pairS',0,10,20,0x34,8),0x1ee18:('S',0,None,20,0x30,4),0x1ee1c:('W',19,None,20,0x28,4),0x1ee28:('pairS',1,0,20,0x48,8),0x20ce8:('W',1,None,0,8,4),0x20d04:('pairS',9,8,20,0x3c,8),0x20d0c:('S',0,None,20,0x44,4),0x20d18:('pairS',0,10,20,0x34,8),0x20d78:('S',0,None,20,0x30,4),0x20d7c:('W',19,None,20,0x28,4),0x20d88:('pairS',1,0,20,0x48,8)}
FIX={0x1cf54:0xaa0303f3,0x1cf58:0x4ea21c48,0x1cf5c:0x4ea11c29,0x1cf60:0x4ea01c0a,0x1cf64:0xaa0003f4,0x1cf74:0xf100005f,0x1cf78:0x9a820101,0x1cf7c:0x91004000,0x1cfb4:0x1f208160,0x1cfe4:0x1e25c000,0x1cff0:0x1e2a6920,0x1cff4:0x1e2a7921,0x1d010:0xd65f03c0,0x1ed80:0xaa0303f3,0x1ed90:0xaa0003f4,0x1eda0:0xf100005f,0x1eda4:0x9a820101,0x1eda8:0x91004000,0x1edc8:0x52802a08,0x1edcc:0x72a7d008,0x1edd8:0x529fac28,0x1eddc:0x72a7cfe8,0x1ede4:0x1e21b404,0x1edec:0x1e21c000,0x1ee04:0x1f010800,0x1ee08:0x1e25c000,0x1ee10:0x52a85008,0x1ee3c:0xd65f03c0,0x20cd4:0xaa0303f3,0x20ce4:0xaa0003f4,0x20cf4:0xf100005f,0x20cf8:0x9a820101,0x20cfc:0x91004000,0x20d1c:0x528010c8,0x20d20:0x72a7b008,0x20d2c:0x529fde88,0x20d30:0x72a7afe8,0x20d38:0x1e21b404,0x20d40:0x1e22c000,0x20d44:0x1e61c000,0x20d48:0x1e61c000,0x20d4c:0x1e624000,0x20d64:0x1f010800,0x20d68:0x1e25c000,0x20d70:0x52a85008,0x20d9c:0xd65f03c0}
def need(v,m):
 if not v:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def flow(pc,w):
 if w&0x7c000000==0x14000000:return {'pc':hex(pc),'kind':'BL'if w>>31 else'B','target':hex(pc+4*sx(w&0x3ffffff,26))}
 if w&0xff000010==0x54000000:return {'pc':hex(pc),'kind':'B.cond','cc':w&15,'target':hex(pc+4*sx(w>>5&0x7ffff,19))}
 if w&0xfffffc1f==0xd65f0000:return {'pc':hex(pc),'kind':'RET','Rn':w>>5&31}
 if w&0xfffffc1f in[0xd61f0000,0xd63f0000]:raise ValueError('unexpectedindirect')
 return None
def proof(W):
 for pc,(kind,rt,rt2,rn,off,width)in STORES.items():
  w=W[pc];need(w&31==rt and w>>5&31==rn,'storeregs')
  if kind=='pairS':need(w&0xffc00000==0x2d000000 and w>>10&31==rt2 and sx(w>>15&127,7)*4==off,'FPstorepair')
  else:need(w&0xffc00000=={'W':0xb9000000,'S':0xbd000000}[kind]and(w>>10&4095)*4==off,'scalarstorewidth/offset')
 for pc,w in FIX.items():need(W[pc]==w,'criticalform:'+hex(pc))
 for pc,t in DIRECT.items():need(flow(pc,W[pc])=={'pc':hex(pc),'kind':'BL','target':hex(t)},'all5calls')
 for pc in[0x1ed78,0x1ee2c,0x20ccc,0x20d8c]:
  w=W[pc];need((w&31,w>>10&31,w>>5&31,sx(w>>15&127,7)*8,w>>23&3)==(29,30,31,48,2),'malformed0lr48')
 for pc in[0x1cf6c,0x1ed98,0x20cec]:
  w=W[pc];need(w&0x9f000000==0x10000000 and w&31==8 and pc+sx((w>>5&0x7ffff)*4+(w>>29&3),21)==0x5579c,'unreadaddress5579c')
def claims(a,e):
 need(a['scope']=={'C_records':3,'C_bytes':3597,'C_lines':137,'warnings':0,'new_native_bytes':652,'new_native_rows':163,'new_data_bytes':0},'scope')
 need(a['carrier_limits']['callee_preserves_saved_GPR_FP_stack']=='premise-only','savedstatepremise')
 for k in['current_I_public_Q_E_R_table_binding','unread_string_log_effects_provider','full_helper_excludes_Q_firstword','formal_ABI_return_contract','FP_numeric_default_math_oracle']:need(a['carrier_limits'][k]=='unknown','unknownjoins')
 need(len(a['claims'])==8 and len(a['direct_state_writes'])==23 and a['required_status']=='U/OPEN unchanged'and a['new_readyX_grade_case_release_site_credit']==0 and a['no_successor_selected']and a['no_recursive_follow'],'noclosure')
 need(e['whole_set']==['1cf3c','1ed6c','20cc0']and e['status']=='NOT_CURRENTLY_READY_FOR_ORIGINAL_PURE_FUNCTION_X_BATCH'and e['not_infeasibility_or_public_failure']and not e['new_call_model_or_setup_authorized']and e['actual_original_or_math_model_execution']==0 and not e['automatic_successor'],'eligibility')
 need([x['pure_receiver_free']for x in e['body_classes']]==[False,False,False]and len(e['exact_missing_prerequisites'])==4,'whole3notpure')
def check():
 pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');p=json.loads(pb);need(p['ranges']==[{'start':hex(a),'end_exclusive':hex(a+n),'file_offset':a,'bytes':n,'words':n//4}for a,n in RANGES]and p['data_words']==[]and p['sole_independent_peer']=='automation_actual_review','fixedscopepeer')
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');need(len(before)==18 and before==[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]==after['files']and after['unchanged'],'18recordedcustody')
 for pin in p['pins']:
  q=Path(pin['path'])
  if q.parent==P:
   b=q.read_bytes();need(len(b)==pin['bytes']and H(b)==pin['sha256'],'ownedprecallpin')
 st=J('capture/status.json');need(st['error']is None and st['watch_unchanged']and not st['automatic_retry']and st['attempts']==st['children_started']==3 and st['selected_bytes_read']==st['validated_bytes']==652 and st['validated_words']==163 and st['selected_table_bytes_read']==st['native_original_instruction_execution']==0,'oncecapture')
 need(J('capture/table-words.json')['words']==[],'nodata')
 rd=J('analysis-read-receipt.json');need(p['frozen_utc']==rd['input_frozen_utc']<rd['C_semantic_read_started_utc']<=rd['C_semantic_read_finished_utc']<st['started_utc'],'freeze-before-analysis-beforecapture')
 src=(P/'source-context.jsonl').read_bytes().splitlines(keepends=True);meta=J('selected-metadata.json')['records'];need(len(src)==len(meta)==3 and sum(map(len,src))==4789,'rawC1scope');W={};flows=[];pairs=[];receipts=[];cb=cl=warnings=0
 for i,((a,n),line,mm)in enumerate(zip(RANGES,src,meta)):
  sm=mm['source'];need(len(line)==sm['raw_bytes']and H(line)==sm['raw_sha256'],'C1pin');d=json.loads(line);c=d.pop('code');need(d==sm['metadata']and d['body_ranges']==[[hex(a),hex(a+n-1)]]and d['body_bytes']==n,'Cmetadataextent');need(d['error']is None and not d['thunk']and not d['partial_code']and not d['timed_out']and not d['warnings']and d['state']=='exported','Cstatus');need(len(c.encode())==d['code_bytes']and len(c.splitlines())==sm['C_lines']and H(c.encode())==d['code_sha256'],'Cfull');cb+=len(c.encode());cl+=len(c.splitlines());warnings+=len(d['warnings'])
  name=hex(a)[2:];raw=(P/f'capture/{name}.bin').read_bytes();rows=J(f'capture/{name}.stdout.json');need(len(raw)==n and len(rows)==n//4 and J('capture/extraction.json')['ranges'][i]=={**p['ranges'][i],'sha256':H(raw)},'wholeextent')
  for j,r in enumerate(rows):
   pc=a+4*j;bb=raw[4*j:4*j+4];need(type(r['offset'])is int and r['offset']==pc and type(r['size'])is int and r['size']==4 and r['bytes']==bb.hex(),'163rawassociations');w=int.from_bytes(bb,'little');W[pc]=w;f=flow(pc,w)
   if f:
    if'target'in f:need(r.get('jump')==int(f['target'],16),'rawbrancharithmetic')
    flows.append(f)
   if w&0x3a000000==0x28000000:
    v=w>>26&1;opc=w>>30;scale=(4<<opc)if v else(8 if opc==2 else 4);pairs.append({'pc':hex(pc),'FP_SIMD':bool(v),'load':bool(w>>22&1),'Rt':w&31,'Rt2':w>>10&31,'Rn':w>>5&31,'element_bytes':scale,'byte_offset':sx(w>>15&127,7)*scale,'mode':w>>23&3})
  rc=J(f'capture/{name}.invocation-after.json');pr=J(f'capture/{name}.invocation-before.json');pid=J(f'capture/{name}.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(a),'-s',hex(a),'-q','-c','pdj '+str(n//4),str(P/f'capture/{name}.bin')]
  need(rc['argv']==pr['argv']==pid['argv']==argv and rc['pid']==pid['pid']==pid['pgid'],'argvpid');need(rc['started_utc']<=pid['spawned_utc']<=rc['finished_utc'],'times');need(rc['exit_code']==0 and rc['error']is None and not rc['timed_out']and(P/f'capture/{name}.stderr').read_bytes()==b''and rc['timeout_seconds']==30 and rc['stdin']=='DEVNULL'and rc['core_limit_bytes']==0 and rc['new_process_session']and rc['cleanup']=='process-group-already-gone','childpolicy');receipts.append(rc)
 need(cb==3597 and cl==137 and warnings==0 and len(W)==163 and len(flows)==12 and len(pairs)==35,'totals')
 for r,s in zip(receipts,receipts[1:]):need(r['finished_utc']<=s['started_utc'],'sequential')
 proof(W);a=J('assessment.json');e=J('eligibility.json');claims(a,e)
 for x,(pc,(kind,rt,rt2,rn,off,width))in zip(a['direct_state_writes'],STORES.items()):need(x['pc']==hex(pc)and x['incoming_I_byte_offset']==hex(off)and x['bytes']==width,'all23statewriteledger')
 neg=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError,TypeError):neg.append(n);return
  raise ValueError('acceptednegative:'+n)
 for name,pc,bit in[('Icarrierchanged',0x1cf64,16),('W3carrierchanged',0x1cf54,16),('stringX2selectionchanged',0x1cf78,16),('field8widthchanged',0x1cf68,30),('FPstore30madeinteger',0x1cfe8,26),('FRINTZmadeintegerconvert',0x1cfe4,16),('sqrtSformchanged',0x1edec,22),('thresholdFCCMPchanged',0x1ede4,5),('mixedprecisionlost',0x20d40,22),('secondDrootlost',0x20d48,22),('lastFPpairchanged',0x20d88,30),('malformedpair48changed',0x20ccc,15)]:
  z=W.copy();z[pc]^=1<<bit;reject(name,lambda z=z:proof(z))
 for name,k in[('currentQbinding','current_I_public_Q_E_R_table_binding'),('providerclosure','unread_string_log_effects_provider'),('transitiveexclusion','full_helper_excludes_Q_firstword'),('formalreturnABI','formal_ABI_return_contract'),('mathoracle','FP_numeric_default_math_oracle')]:
  z=copy.deepcopy(a);z['carrier_limits'][k]='proved';reject(name,lambda z=z:claims(z,e))
 z=copy.deepcopy(e);z['body_classes'][1]['pure_receiver_free']=True;reject('inlineSQRTpromotedpure',lambda:claims(a,z))
 z=copy.deepcopy(e);z['status']='READY';reject('newmodeladmissioninvented',lambda:claims(a,z))
 z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automaticfollow',lambda:claims(z,e))
 if(P/'manifest.json').exists():
  m=J('manifest.json');need({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and q.name!='manifest.json'}=={x['path']for x in m['files']},'sealedtree')
  for x in m['files']:
   b=(P/x['path']).read_bytes();need(len(b)==x['bytes']and H(b)==x['sha256'],'sealedpin')
 return {'status':'PASS-ownedpacket-only','C_records':3,'C_bytes':3597,'C_lines':137,'warnings':0,'new_native_bytes':652,'new_native_rows':163,'data_bytes':0,'recorded_custody_pairs':18,'receipts':receipts,'all_raw_flow_fields':flows,'all_GPR_FP_SIMD_pair_fields':pairs,'all23_direct_state_store_fields':[{'pc':hex(pc),'kind':v[0],'Rt':v[1],'Rt2':v[2],'Rn':v[3],'byte_offset':hex(v[4]),'full_store_bytes':v[5]}for pc,v in STORES.items()],'critical_carrier_FP_forms':len(FIX),'negative_controls':neg,'whole_set_pure_X_ready':False,'external_domain_reopens':0,'decoder_original_model_calls':0,'limits':'Narrowrawstaticfields only, nottotalISA/translatedmodel/runtimeFP/formalABI/class/currenttable/provider/oracleproof; no recursivefollow.'}
if __name__=='__main__':
 need(sys.argv[1:]==['--check'],'only --check')
 print(json.dumps(check(),indent=2))
