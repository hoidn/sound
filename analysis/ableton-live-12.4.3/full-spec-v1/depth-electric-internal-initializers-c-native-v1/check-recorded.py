"""Fixed ownedpacket-only data checks; no external corpus/image/tool/provider opens, children, old imports or models."""
import copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent
PRE='cba2abb09132e6f2636333e6da75ac57d5a7250d16aa96dbb0e7794d0dee9004'
RANGES=[(0xa600,304),(0xcee4,396),(0xe1e8,432)]
CTX=[(0xcc80,0xcc98),(0xcd64,0xcd7c),(0xcd98,0xcdb0)]
CRITICAL={0xa610:0xaa0003f3,0xa614:0x91010014,0xa620:0xf9002e7f,0xa624:0xb9406268,0xa650:0xa9012a6a,0xa670:0x528002c1,0xa684:0xf9402a68,0xa688:0x9240f908,0xa68c:0xd1000501,0xa690:0xaa1403e0,0xa694:0x52800002,0xa6b4:0xa902d274,0xa6b8:0xf9001e68,0xa718:0x8b35c288,0xa720:0xa9427bfd,0xa728:0xa8c357f6,0xa72c:0xd65f03c0,0xcf04:0xf9400408,0xcf0c:0xaa0003f3,0xcf10:0x52800c08,0xcf14:0x72a001c8,0xcf1c:0xa94022ba,0xcf84:0xbd001901,0xcf8c:0xa94022ba,0xcfac:0x39402109,0xcfb4:0x39402508,0xcfbc:0xf9400268,0xcfc0:0xf9404d08,0xcfc4:0xaa1303e0,0xcfc8:0xaa1403e1,0xcfcc:0xd63f0100,0xcff4:0x1e207821,0xcffc:0x1e286800,0xd028:0x1f020c02,0xd034:0x1e22bc20,0xd058:0x2d420d02,0xd064:0x1f218800,0xd068:0xbd001900,0xe1fc:0xaa0103f4,0xe200:0xaa0003f3,0xe204:0xa940a808,0xe2d4:0xa9007d1f,0xe2d8:0xb900111f,0xe2e0:0xfc1f8160,0xe2f4:0xf9000668,0xe31c:0xa9007d3f,0xe320:0xb900113f,0xe324:0xfc014120,0xe334:0xa9402674,0xe354:0xa9005e75,0xe358:0xf9000a76,0xe360:0xaa1403e0,0xe364:0xa9437bfd,0xe370:0xa8c45ff8,0xe378:0xa9437bfd,0xe388:0xd65f03c0}
DIRECT={0xa61c:0x29288,0xa698:0x29258,0xe2ac:0x293d8,0xe350:0x2954c,0xe374:0x293c0,0xe390:0x291ec,0xe394:0xe170}
CTXFIX={0xcc80:0x52800108,0xcc84:0xb90093e8,0xcc88:0x910023e1,0xcc8c:0xaa1503e0,0xcc94:0x39c07fe8,0xcd64:0x9b0b7d4a,0xcd68:0xeb0a0001,0xcd6c:0x540000c9,0xcd70:0xaa0803e0,0xcd78:0x14000007,0xcd98:0xf9404508,0xcd9c:0xaa1403e0,0xcda0:0xd63f0100,0xcda4:0xaa1403e0,0xcdac:0x52800034}

def need(v,m):
 if not v:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def flow(pc,w):
 if w&0x7c000000==0x14000000:return {'pc':hex(pc),'kind':'BL'if w>>31 else'B','target':hex(pc+4*sx(w&0x3ffffff,26))}
 if w&0xff000010==0x54000000:return {'pc':hex(pc),'kind':'B.cond','cc':w&15,'target':hex(pc+4*sx(w>>5&0x7ffff,19))}
 if w&0x7e000000==0x34000000:return {'pc':hex(pc),'kind':'CBNZ'if w>>24&1 else'CBZ','Rt':w&31,'target':hex(pc+4*sx(w>>5&0x7ffff,19))}
 if w&0x7e000000==0x36000000:return {'pc':hex(pc),'kind':'TBNZ'if w>>24&1 else'TBZ','Rt':w&31,'bit':((w>>31)<<5)|(w>>19&31),'target':hex(pc+4*sx(w>>5&0x3fff,14))}
 op=w&0xfffffc1f
 if op in[0xd61f0000,0xd63f0000,0xd65f0000]:return {'pc':hex(pc),'kind':{0xd61f0000:'BR',0xd63f0000:'BLR',0xd65f0000:'RET'}[op],'Rn':w>>5&31}
 return None

def proof(W,C):
 for pc,w in CRITICAL.items():need(W[pc]==w,'criticalraw:'+hex(pc))
 for pc,t in DIRECT.items():
  f=flow(pc,W[pc]);need(f['target']==hex(t)and f['kind']==('B'if pc==0xe374 else'BL'),'directcall/tail')
 for pc,w in CTXFIX.items():need(C[pc]==w,'contextcarrier:'+hex(pc))
 for pc,t in[(0xcc90,0xa600),(0xcd74,0xe1e8),(0xcda8,0xcee4)]:need(flow(pc,C[pc])=={'pc':hex(pc),'kind':'BL','target':hex(t)},'threecontextcalls')
 for pc in[0xe1f4,0xe364,0xe378]:
  w=W[pc];need(w&0x3a000000==0x28000000 and(w&31,w>>10&31,w>>5&31,sx(w>>15&127,7)*8,w>>23&3)==(29,30,31,48,2),'malformed0lrraw48')
 for pc in[0xe2d0,0xe314]:
  w=W[pc];need(w&0xff000000==0x5c000000 and pc+4*sx(w>>5&0x7ffff,19)==0x2b328,'unreadDliteral')

def claims(a):
 need(a['scope']=={'C_records':3,'C_bytes':6011,'C_lines':208,'warnings':2,'new_native_bytes':1132,'new_native_rows':283,'existing_context_bytes':72,'existing_context_rows':18,'new_data_bytes':0},'scope')
 r=a['carrier_limits'];need(r['caller_X21_X8_X10_provenance']=='unknown-outside-fixed-windows'and r['callee_preservation_current_state']=='premise-only','contextpremises')
 for k in['a600_entry_A_equals_public_I_or_C0','producer_saved_S_current_C0_P_join','current_I_A_R_child_table_runtime_encoding','formal_ABI_loaded_import_provider','default_numeric_public_calibration_oracle']:need(r[k]=='unknown','unknownjoin')
 need(a['all_imported11_thunks_status']=='inherited-metadata-only/U; no loadedprovider/binding/content follow'and a['preserved_e1e8_warnings']==2,'imports/warnings')
 need(len(a['claims'])==8 and a['required_status']=='U/OPEN unchanged'and a['main_Live_inventory']=='25095 of268015 unchanged'and a['new_resolved_runtime_sites']==a['new_cases_grades_releases']==0 and a['no_successor_selected'],'noclosure')

def check():
 pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');p=json.loads(pb);need(p['ranges']==[{'start':hex(a),'end_exclusive':hex(a+n),'file_offset':a,'bytes':n,'words':n//4}for a,n in RANGES]and p['data_words']==[]and p['sole_independent_peer']=='arrangement_map_review','fixedscopepeer')
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');need(len(before)==22 and before==[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]==after['files']and after['unchanged'],'22recordedcustody')
 for pin in p['pins']:
  q=Path(pin['path'])
  if q.parent==P:
   b=q.read_bytes();need(len(b)==pin['bytes']and H(b)==pin['sha256'],'ownedprecallpin')
 st=J('capture/status.json');need(st['error']is None and st['watch_unchanged']and not st['automatic_retry']and st['attempts']==st['children_started']==3 and st['selected_bytes_read']==st['validated_bytes']==1132 and st['validated_words']==283 and st['selected_table_bytes_read']==st['native_original_instruction_execution']==0,'oncewholecapture')
 need(J('capture/table-words.json')['words']==[],'nodata')
 rd=J('analysis-read-receipt.json');need(p['frozen_utc']==rd['pre_call_frozen_utc']<rd['semantic_read_started_utc']<=rd['semantic_read_finished_utc']<st['started_utc'],'freeze-before-C-context-analysis-beforecapture')
 src=(P/'source-context.jsonl').read_bytes().splitlines(keepends=True);meta=J('selected-metadata.json')['records'];need(len(src)==len(meta)==3 and sum(map(len,src))==7372,'3rawC1');W={};flows=[];pairs=[];mem=[];receipts=[];Cbytes=Clines=warn=0
 for i,((a,n),line,mm)in enumerate(zip(RANGES,src,meta)):
  sm=mm['source'];need(len(line)==sm['raw_bytes']and H(line)==sm['raw_sha256'],'C1pin');d=json.loads(line);c=d.pop('code');need(d==sm['metadata']and d['body_ranges']==[[hex(a),hex(a+n-1)]]and d['body_bytes']==n,'Cmetaextent');need(not d['thunk']and not d['partial_code']and not d['timed_out']and d['error']is None,'Cstatus');need(len(c.encode())==d['code_bytes']and len(c.splitlines())==sm['C_lines']and H(c.encode())==d['code_sha256'],'Cfull');Cbytes+=len(c.encode());Clines+=len(c.splitlines());warn+=len(d['warnings'])
  name=hex(a)[2:];raw=(P/f'capture/{name}.bin').read_bytes();rows=J(f'capture/{name}.stdout.json');need(len(raw)==n and len(rows)==n//4 and J('capture/extraction.json')['ranges'][i]=={**p['ranges'][i],'sha256':H(raw)},'wholeextent')
  for j,r in enumerate(rows):
   pc=a+4*j;bb=raw[4*j:4*j+4];need(type(r['offset'])is int and r['offset']==pc and type(r['size'])is int and r['size']==4 and r['bytes']==bb.hex(),'283rawassociations');w=int.from_bytes(bb,'little');W[pc]=w;f=flow(pc,w)
   if f:
    if'target'in f:need(r.get('jump')==int(f['target'],16),'signedbranchfield')
    flows.append(f)
   if w&0x3a000000==0x28000000:
    v=w>>26&1;opc=w>>30;scale=(4<<opc)if v else(8 if opc==2 else 4);pairs.append({'pc':hex(pc),'FP_SIMD':bool(v),'load':bool(w>>22&1),'Rt':w&31,'Rt2':w>>10&31,'Rn':w>>5&31,'element_bytes':scale,'mode':w>>23&3,'byte_offset':sx(w>>15&127,7)*scale})
   if w&0x3b000000==0x39000000:
    v=w>>26&1;opc=w>>22&3;scale=16 if v and opc&2 else 1<< (w>>30);mem.append({'pc':hex(pc),'Rt':w&31,'Rn':w>>5&31,'FP_SIMD':bool(v),'opc':opc,'scale':scale,'byte_offset':(w>>10&4095)*scale})
  r=J(f'capture/{name}.invocation-after.json');pr=J(f'capture/{name}.invocation-before.json');pid=J(f'capture/{name}.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(a),'-s',hex(a),'-q','-c','pdj '+str(n//4),str(P/f'capture/{name}.bin')]
  need(r['argv']==pr['argv']==pid['argv']==argv and r['pid']==pid['pid']==pid['pgid'],'argvpid');need(r['started_utc']<=pid['spawned_utc']<=r['finished_utc'],'times');need(r['exit_code']==0 and r['error']is None and not r['timed_out']and(P/f'capture/{name}.stderr').read_bytes()==b''and r['timeout_seconds']==30 and r['stdin']=='DEVNULL'and r['core_limit_bytes']==0 and r['new_process_session']and r['cleanup']=='process-group-already-gone','childstatus');receipts.append(r)
 need(Cbytes==6011 and Clines==208 and warn==2 and len(W)==283,'aggregates');need(len(meta[2]['source']['metadata']['warnings'])==2 and meta[2]['source']['metadata']['warnings'][0]==meta[2]['source']['metadata']['warnings'][1],'twoidenticalnonreturnwarnings')
 for r,s in zip(receipts,receipts[1:]):need(r['finished_utc']<=s['started_utc'],'sequential')
 context=J('caller-context.json');need(context['old_selected_context_bytes']==72 and context['old_selected_context_words']==18 and context['new_image_context_bytes']==0 and len(context['windows'])==3,'contextbudget');C={};cf=[]
 for (a,z),window in zip(CTX,context['windows']):
  raw=(P/window['owned_excerpt']).read_bytes();need(window['start']==hex(a)and window['end_exclusive']==hex(z)and len(raw)==24 and H(raw)==window['sha256']and window['parent_byte_offset']==a-0xcb0c and len(window['rows'])==6,'exactcontextwindow')
  for j,r in enumerate(window['rows']):
   pc=a+4*j;bb=raw[4*j:4*j+4];need(r['offset']==pc and r['size']==4 and r['bytes']==bb.hex(),'18contextassociations');w=int.from_bytes(bb,'little');C[pc]=w;f=flow(pc,w)
   if f:
    if'target'in f:need(r.get('jump')==int(f['target'],16),'contexttarget')
    cf.append(f)
 need(context['source_parent_manifest']['sha256']=='d3720dc384db2df803cf790d923a3cc8dd8d1fa13a2c38cd174792e2a461ffb1'and context['parent_payload_pins'][0]['sha256']=='85498b1f9b7163f89d7d0417331648f73fee8bb883f75bac7e4a507836f234b6'and context['parent_payload_pins'][1]['sha256']=='835f7f8245635a862cbf0269a5815e4b728203001356c69327ce45adfd682261','approvedcontextcustodylineage')
 proof(W,C);a=J('assessment.json');claims(a);neg=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError,TypeError):neg.append(n);return
  raise ValueError('acceptednegative:'+n)
 for name,pc,bit in[('resize64carriertruncated',0xa68c,31),('stringreceiverchanged',0xa610,16),('cachebyteguardchanged',0xcfac,10),('virtual98slotchanged',0xcfc0,10),('FPfusedformchanged',0xd064,15),('descriptorreloadchanged',0xcf8c,5),('vectorNcarrierchanged',0xe1fc,16),('cellDnegativeoffsetchanged',0xe2e0,12),('headendstorechanged',0xe354,10),('deleteTAILmadeBL',0xe374,31),('malformedpair48changed',0xe1f4,15)]:
  z=W.copy();z[pc]^=1<<bit;reject(name,lambda z=z:proof(z,C))
 z=C.copy();z[0xcc8c]^=1<<16;reject('contextX21receiverchanged',lambda:proof(W,z))
 z=C.copy();z[0xcda0]^=1<<21;reject('opaquecontextcallchanged',lambda:proof(W,z))
 for name,key,v in[('publicI_A_C0join','a600_entry_A_equals_public_I_or_C0','proved'),('outsidecontextguessed','caller_X21_X8_X10_provenance','proved'),('producerP_C0join','producer_saved_S_current_C0_P_join','proved'),('runtimeclass','current_I_A_R_child_table_runtime_encoding','proved'),('loadedimports','formal_ABI_loaded_import_provider','proved'),('numericoracle','default_numeric_public_calibration_oracle','proved')]:
  z=copy.deepcopy(a);z['carrier_limits'][key]=v;reject(name,lambda z=z:claims(z))
 z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automaticfollow',lambda:claims(z))
 if(P/'manifest.json').exists():
  m=J('manifest.json');need({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and q.name!='manifest.json'}=={x['path']for x in m['files']},'sealedtree')
  for x in m['files']:
   b=(P/x['path']).read_bytes();need(len(b)==x['bytes']and H(b)==x['sha256'],'sealedpin')
 return {'status':'PASS-ownedpacket-only','C_records':3,'C_bytes':6011,'C_lines':208,'warnings':2,'new_native_bytes':1132,'new_native_rows':283,'old_context_bytes':72,'old_context_rows':18,'new_data_bytes':0,'recorded_custody_pairs':22,'receipts':receipts,'all_new_raw_flow_fields':flows,'all_new_GPR_FP_SIMD_pairs':pairs,'all_new_unsigned_memory_fields':mem,'exact_context_flow_fields':cf,'critical_raw_fields':len(CRITICAL),'negative_controls':neg,'external_domain_reopens':0,'decoder_original_model_calls':0,'limits':'Narrowstaticrawfields/contextonly, notfullISA/translatedmodel/mathoracle/formalABI/runtime/class/currentstate/publicproof; no contextexpansion or recursivefollow.'}
if __name__=='__main__':
 need(sys.argv[1:]==['--check'],'only --check')
 print(json.dumps(check(),indent=2))
