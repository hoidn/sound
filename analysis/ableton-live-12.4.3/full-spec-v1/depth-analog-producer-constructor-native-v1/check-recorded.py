"""Owned currentpacket-only custody/rawfield checker; no external opens/oldimports/decoder."""
import argparse,hashlib,json,copy
from pathlib import Path
P=Path(__file__).resolve().parent
PRE='d36ca4e80e1b41faff456c71aef012079917a987a3b8649c050aef350b171955'
RANGES=[('4448',0x4448,4),('3b18',0x3b18,2292)]
def J(n):return json.loads((P/n).read_bytes())
def H(b):return hashlib.sha256(b).hexdigest()
def need(v,n):
 if not v:raise ValueError(n)
def sx(v,n):return v-(1<<n) if v&(1<<(n-1)) else v
def branch(w,pc):
 if w&0x7c000000==0x14000000:return ('BL' if w>>31 else 'B',pc+4*sx(w&0x3ffffff,26))
 if w&0xfffffc1f==0xd65f0000:return ('RET',w>>5&31)
 return None
def u64(w,rt,rn,off):need(w&0xffc00000==0xf9000000 and (w&31,w>>5&31,8*(w>>10&4095))==(rt,rn,off),'u64store')
def pair(w):
 need(w&0x3a000000==0x28000000,'pairfamily');v=w>>26&1;opc=w>>30
 scale=(4<<opc) if v else (8 if opc==2 else 4)
 return {'rt':w&31,'rt2':w>>10&31,'rn':w>>5&31,'mode':w>>23&3,'load':bool(w>>22&1),'vector':bool(v),'element_bytes':scale,'offset':sx(w>>15&127,7)*scale}
def semantic(w):
 need(branch(w[0x4448],0x4448)==('B',0x3b18),'thunkbranch')
 need(w[0x3b2c]==0xaa0003f3 and w[0x43f4]==0xaa1303e0,'incomingQ-returnQ')
 need(branch(w[0x3b30],0x3b30)==('BL',0x2b990),'firsthelper')
 need(branch(w[0x3b50],0x3b50)==branch(w[0x3b5c],0x3b5c)==('BL',0x1006c),'twointeriorsamehelper')
 u64(w[0x3b3c],8,0,0);need(pair(w[0x3b44])=={'rt':8,'rt2':31,'rn':0,'mode':2,'load':False,'vector':False,'element_bytes':8,'offset':0xe0},'Bsecondstore')
 need(w[0x3b48]==0x9103c014 and w[0x3b54]==0x910ea275,'Bplusf0-vsQplus3a8')
 need(branch(w[0x3bc0],0x3bc0)==branch(w[0x3fa4],0x3fa4)==('BL',0x509e8),'twoallocation-shapedcalls')
 need(w[0x3bbc]==w[0x3fa0]==0x5280a000,'two500constants')
 u64(w[0x3e9c],0,22,0);u64(w[0x428c],0,19,0x22f8)
 for pc in [0x3b24,0x43f8]:
  z=pair(w[pc]);need((z['rt'],z['rt2'],z['rn'],z['offset'],z['mode'])==(29,30,31,48,2),'malformed0lr-raw48')
 need(w[0x4408]==0xd65f03c0,'lastRET')
def check():
 pb=(P/'pre-call-manifest.json').read_bytes();need(H(pb)==PRE,'precall');plan=json.loads(pb)
 before,after=J('capture/before-identities.json'),J('capture/after-identities.json')
 need(len(before)==13 and before==[plan['image'],plan['tool'],*plan['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pb),'sha256':PRE}]==after['files'] and after['unchanged'],'13recordedcustody')
 for x in plan['pins']:
  p=Path(x['path'])
  if p.parent==P:
   b=p.read_bytes();need(len(b)==x['bytes'] and H(b)==x['sha256'],'ownedprecallpin')
 st=J('capture/status.json');need(st['error'] is None and st['watch_unchanged'] and st['attempts']==st['children_started']==2 and not st['automatic_retry'] and st['selected_bytes_read']==st['validated_bytes']==2296 and st['validated_words']==574 and st['selected_table_bytes_read']==st['native_original_instruction_execution']==0,'actualsuccess')
 need(J('capture/table-words.json')['words']==[] and J('capture/table-words.json')['total_bytes']==0,'nodata')
 src=(P/'source-context.jsonl').read_bytes();md=J('selected-metadata.json');d=json.loads(src);c=d['code'].encode()
 need(len(src)==21775 and H(src)==md['source']['raw_sha256'] and len(c)==20807 and len(d['code'].splitlines())==616 and H(c)==d['code_sha256'],'actualcompleteC')
 need(d['entry']=='0x3b18' and d['body_bytes']==2292 and d['state']=='exported' and not d['thunk'] and not d['warnings'] and d['error'] is None and not d['partial_code'] and not d['timed_out'],'actualsource-status')
 need(not md['thunk']['expanded_C_retained'] and not md['thunk']['expanded_C_semantic_read'] and md['no_expanded_thunk_implementation_credit'],'expandedCexcluded')
 W={};assocs=[];flows=[];pairs=[];mem=[];addresses=[];receipts=[]
 for i,(name,start,n) in enumerate(RANGES):
  raw=(P/f'capture/{name}.bin').read_bytes();rows=J(f'capture/{name}.stdout.json');need(len(raw)==n and len(rows)==n//4,'wholephysicalextent')
  need(J('capture/extraction.json')['ranges'][i]['sha256']==H(raw),'extraction')
  for j,r in enumerate(rows):
   pc=start+4*j;bb=raw[4*j:4*j+4];need((r['offset'],r['size'],r['bytes'])==(pc,4,bb.hex()),'all574rawassociations');w=int.from_bytes(bb,'little');W[pc]=w;assocs.append({'pc':hex(pc),'bytes':bb.hex()})
   f=branch(w,pc)
   if f:
    if f[0]!='RET':need(r.get('jump')==f[1],'rawtarget')
    flows.append({'pc':hex(pc),'form':f[0],('rn' if f[0]=='RET' else 'target'):(f[1] if f[0]=='RET' else hex(f[1]))})
   if w&0x3a000000==0x28000000:pairs.append({'pc':hex(pc),**pair(w)})
   if w&0x3b000000==0x39000000:
    v=w>>26&1;size=w>>30;opc=w>>22&3;scale=16 if v and opc&2 else 1<<size
    mem.append({'pc':hex(pc),'rt':w&31,'rn':w>>5&31,'vector':bool(v),'opc':opc,'width_or_scale':scale,'offset':(w>>10&4095)*scale})
   if w&0x9f000000==0x10000000:addresses.append({'pc':hex(pc),'form':'ADR','rd':w&31,'address':hex(pc+sx((w>>5&0x7ffff)*4+(w>>29&3),21))})
   elif w&0x3b000000==0x18000000:addresses.append({'pc':hex(pc),'form':'literal','rt':w&31,'address':hex(pc+4*sx(w>>5&0x7ffff,19))})
  b=J(f'capture/{name}.invocation-before.json');a=J(f'capture/{name}.invocation-after.json');pid=J(f'capture/{name}.pid.json')
  argv=[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(n//4),str(P/f'capture/{name}.bin')]
  need(a['argv']==b['argv']==pid['argv']==argv and a['pid']==pid['pid']==pid['pgid'],'childargvpid');need(a['exit_code']==0 and a['error'] is None and not a['timed_out'] and (P/f'capture/{name}.stderr').read_bytes()==b'','childstatus');need(a['started_utc']<=pid['spawned_utc']<=a['finished_utc'],'childclock');receipts.append(a)
 need(len(W)==574 and len(flows)==7,'fullrawflow');semantic(W)
 # Both32-element backpointer/value blocks are checked whole, not firstN.
 links=[]
 for begin,constreg in [(0x3ea0,23),(0x4290,9)]:
  for i in range(32):
   pc=begin+8*i;u64(W[pc],22,0,0x10+0x28*i);u64(W[pc+4],constreg,0,0x28*i)
   links.append({'pc':hex(pc),'record':i,'head_pointer_register':22,'field_offset':hex(0x10+0x28*i),'value_pc':hex(pc+4),'literal_offset':hex(0x28*i)})
 neg=[]
 for label,pc,bit in [('wrongthunk',0x4448,0),('wrongQcarrier',0x3b2c,16),('returnBnotQ',0x43f4,16),('firsthelper',0x3b30,0),('Bvptrstorebase',0x3b3c,5),('Bsecondaryoffset',0x3b44,15),('Binterior',0x3b48,10),('Qinterior',0x3b54,10),('first500',0x3bbc,5),('second500',0x3fa0,5),('firstheadslot',0x3e9c,5),('secondheadslot',0x428c,10),('malformedpair-offset',0x3b24,15),('wrongRET',0x4408,5)]:
  bad=dict(W);bad[pc]^=1<<bit
  try:semantic(bad)
  except ValueError:neg.append(label)
  else:raise AssertionError(label)
 need(len(neg)==14,'controlcount')
 return {'status':'PASS-currentpacketonly','rows':574,'code_bytes':2296,'actual_C_bytes':20807,'actual_C_lines':616,'warnings':0,'newdata_bytes':0,'recorded_custody_pairs':13,'all_raw_associations':assocs,'all_raw_flow_fields':flows,'all_GPR_SIMD_pair_fields':pairs,'all_unsigned_memory_fields':mem,'ADR_literal_addresses':addresses,'all64_backpointer_value_record_pairs':links,'negative_controls':neg,'negative_control_count':14,'receipts':receipts,'malformed_renderings':'Original0lr retainedat3b24/43f8;rawimm7=6*8=48=0x30 reconstructed separately.','limits':'No totalISA/ABI/runtime/class/allocation/currentvptr/publicproof;expanded4448Cexcluded;ESILunused;externalreopens0.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',required=True);ap.parse_args();print(json.dumps(check(),indent=2))
