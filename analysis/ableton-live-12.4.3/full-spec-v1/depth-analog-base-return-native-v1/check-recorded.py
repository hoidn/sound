"""Fixed sealed owned-data check only. No outside pins, children, images, tools, old imports or models."""
import copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parent
PRE='8435a8b9f1fe11d9121bf80e0f650fd5b836ea417832cc2d00b269b39355bedf'
EXPECTED=[0x10172408,0xd503201f,0xf9000008,0x7900101f,0x3900281f,0x2901fc1f,0xd503201f,0x5c13fee0,0xfc014000,0x52802008,0x79003808,0xb900201f,0xa908fc1f,0xf900401f,0x6f00e400,0x3c828000,0x3c838000,0x3c848000,0x3c858000,0xf900341f,0x52800028,0x39027008,0x3903601f,0xd65f03c0]
def need(v,m):
 if not v:raise ValueError(m)
def H(b):return hashlib.sha256(b).hexdigest()
def J(n):return json.loads((P/n).read_bytes())
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def shape(W):
 need(W==EXPECTED,'all24rawforms/noX0assignment/helper/stack')
 w=W[0];need(w&0x9f000000==0x10000000 and w&31==8 and 0x2b990+sx(((w>>5&0x7ffff)<<2)|(w>>29&3),21)==0x59e10,'ADR59e10')
 w=W[7];need(w&0xff000000==0x5c000000 and w&31==0 and 0x2b9ac+4*sx(w>>5&0x7ffff,19)==0x53988,'D0literalnotGPRX0')
 for i,rt,rt2,offset,scale in[(5,31,31,12,4),(12,31,31,136,8)]:
  w=W[i];need(w&0x3a000000==0x28000000 and not(w>>26&1)and not(w>>22&1)and(w&31,w>>10&31,w>>5&31,sx(w>>15&127,7)*scale,w>>23&3)==(rt,rt2,0,offset,2),'exactpairfield')
 need(W[-1]==0xd65f03c0,'RET X30')
def claims(a):
 need(a['scope']=={'C_records':1,'C_bytes':700,'C_lines':29,'warnings':0,'native_bytes':96,'native_rows':24,'new_data_bytes':0},'scope')
 r=a['relation_status'];need(r['incoming_X0_to_normal_return_X0']=='equal-under-local-normal-return-premises'and r['inherited_B_equals_Q']=='conditional-local-composition-supported','localrelation')
 for k in['actual_public_entry_class_ABI','runtime_current_Q_table_continuity','callback_E_R_public_delivery','whole_Q_initialization_or_allocation']:need(r[k]=='unknown','unknownjoin')
 need(r['whole_Q_plus8_null_member']=='not-established','partialmembernotnullproof')
 need(len(a['claims'])==5 and len(a['claims'][3]['premises'])>=5 and a['new_resolved_runtime_sites']==0 and a['new_cases_grades_releases']==0 and a['main_Live_inventory']=='25095 of268015 unchanged'and a['required_status']=='U/OPEN unchanged'and a['no_successor_selected'],'noclosure')
def check():
 b=(P/'pre-call-manifest.json').read_bytes();need(H(b)==PRE,'precall');p=json.loads(b);need(p['ranges']==[{'start':'0x2b990','end_exclusive':'0x2b9f0','file_offset':178576,'bytes':96,'words':24}]and p['data_words']==[],'exactrange')
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');need(len(before)==17 and before==[p['image'],p['tool'],*p['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(b),'sha256':PRE}]==after['files']and after['unchanged'],'17recordedcustody')
 for pin in p['pins']:
  q=Path(pin['path'])
  if q.parent==P:
   d=q.read_bytes();need(len(d)==pin['bytes']and H(d)==pin['sha256'],'ownedpin')
 s=J('capture/status.json');need(s['attempts']==s['children_started']==1 and s['error']is None and s['watch_unchanged']and not s['automatic_retry']and s['selected_bytes_read']==s['validated_bytes']==96 and s['validated_words']==24 and s['selected_table_bytes_read']==s['native_original_instruction_execution']==0,'oncecapture')
 need(J('capture/table-words.json')['words']==[],'nodata')
 src=(P/'source-context.jsonl').read_bytes();m=J('selected-metadata.json')['source'];d=json.loads(src);c=d.pop('code');need(d==m['metadata']and len(src)==1078 and H(src)==m['raw_sha256'],'C1metadata');need(len(c.encode())==700 and len(c.splitlines())==29 and H(c.encode())==d['code_sha256'],'Cfull');need(d['body_ranges']==[['0x2b990','0x2b9ef']]and d['body_bytes']==96 and not d['thunk']and not d['partial_code']and not d['timed_out']and not d['warnings']and d['error']is None and d['state']=='exported','Cstatus')
 rr=J('source-read-receipt.json');need(rr['approval_verified_before_C_read_utc']<=rr['selected_C_retention_finished_utc']<s['started_utc'],'Cbeforecapture')
 raw=(P/'capture/2b990.bin').read_bytes();rows=J('capture/2b990.stdout.json');need(len(raw)==96 and len(rows)==24,'wholeraw');need(J('capture/extraction.json')['ranges']==[{**p['ranges'][0],'sha256':H(raw)}],'extracthash')
 W=[]
 for i,r in enumerate(rows):
  bb=raw[4*i:4*i+4];need(type(r['offset'])is int and r['offset']==0x2b990+4*i and type(r['size'])is int and r['size']==4 and r['bytes']==bb.hex(),'all24associations');W.append(int.from_bytes(bb,'little'))
 shape(W)
 rc=J('capture/2b990.invocation-after.json');pre=J('capture/2b990.invocation-before.json');pid=J('capture/2b990.pid.json');argv=[p['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m','0x2b990','-s','0x2b990','-q','-c','pdj 24',str(P/'capture/2b990.bin')]
 need(rc['argv']==pre['argv']==pid['argv']==argv and rc['pid']==pid['pid']==pid['pgid'],'argvpid');need(rc['exit_code']==0 and rc['error']is None and not rc['timed_out']and(P/'capture/2b990.stderr').read_bytes()==b'','status');need(rc['timeout_seconds']==30 and rc['stdin']=='DEVNULL'and rc['core_limit_bytes']==0 and rc['new_process_session']and rc['cleanup']=='process-group-already-gone','bounds');need(rc['started_utc']<=pid['spawned_utc']<=rc['finished_utc'],'times')
 a=J('assessment.json');claims(a);neg=[]
 def reject(n,f):
  try:f()
  except(ValueError,KeyError,TypeError):neg.append(n);return
  raise ValueError('acceptednegative:'+n)
 for name,i,bit in[('wrongaddressliteral',0,5),('storebaseX0changed',2,5),('partialhalfwordwidthchanged',3,30),('literalFPbankchanged',7,26),('unscaledstorebasechanged',8,5),('pairbaseregisterchanged',12,5),('SIMDstorewidthchanged',15,30),('RETregisterchanged',23,5)]:
  z=W.copy();z[i]^=1<<bit;reject(name,lambda z=z:shape(z))
 for name,key,value in[('publicentrypromoted','actual_public_entry_class_ABI','proved'),('stabletablepromoted','runtime_current_Q_table_continuity','proved'),('callbackbindingpromoted','callback_E_R_public_delivery','proved'),('partialmemberzero','whole_Q_plus8_null_member','provedzero'),('completeallocation','whole_Q_initialization_or_allocation','proved')]:
  z=copy.deepcopy(a);z['relation_status'][key]=value;reject(name,lambda z=z:claims(z))
 z=copy.deepcopy(a);z['no_successor_selected']=False;reject('automaticfollow',lambda:claims(z))
 if(P/'manifest.json').exists():
  m=J('manifest.json');need({str(q.relative_to(P))for q in P.rglob('*')if q.is_file()and q.name!='manifest.json'}=={x['path']for x in m['files']},'sealedtree')
  for x in m['files']:
   d=(P/x['path']).read_bytes();need(len(d)==x['bytes']and H(d)==x['sha256'],'sealedpin')
 return {'status':'PASS-packet-only','C_records':1,'C_bytes':700,'C_lines':29,'warnings':0,'native_rows':24,'native_bytes':96,'new_data_bytes':0,'recorded_custody_pairs':17,'receipts':[rc],'all_raw_forms_verified':[{'pc':hex(0x2b990+4*i),'word':hex(w)}for i,w in enumerate(W)],'normal_return_relation':'incomingX0=returnedX0 locally; no GPRX0assignment/helper/stackinstruction, conditionalactualentry/validstate/normalRET','literal_addresses_unread':['0x59e10 (addressonly)','0x53988 (Dliteralcontentsunread)'],'negative_controls':neg,'external_domain_reopens':0,'decoder_original_model_calls':0,'limits':'Fullraw24formmatch plusselectedfieldchecks, notgeneralISAdecoder/formalABI/runtime/class/publicorFPproof.'}
if __name__=='__main__':
 need(sys.argv[1:]==['--check'],'only --check')
 print(json.dumps(check(),indent=2))
