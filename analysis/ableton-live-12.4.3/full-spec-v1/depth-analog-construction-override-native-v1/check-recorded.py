"""Owned packet-only raw/custody/claim checks; no external provider or original reads."""
from pathlib import Path
import json,hashlib,copy
P=Path(__file__).resolve().parent

def B(n):return (P/n).read_bytes()
def J(n):return json.loads(B(n))
def H(b):return hashlib.sha256(b).hexdigest()
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def flow(w,pc):
 if w&0x7c000000==0x14000000:return {'kind':'BL' if w>>31 else 'B','target':pc+4*sx(w&0x3ffffff,26)}
 if w&0xff000010==0x54000000:return {'kind':'Bcond','condition':w&15,'target':pc+4*sx((w>>5)&0x7ffff,19)}
 if w&0x7e000000==0x34000000:return {'kind':'CBNZ' if w&(1<<24) else 'CBZ','rt':w&31,'target':pc+4*sx((w>>5)&0x7ffff,19)}
 if w&0xfffffc1f==0xd65f0000:return {'kind':'RET','register':(w>>5)&31}

def rows_check(rs,raw,s,n):
 assert len(rs)==n and len(raw)==4*n
 for i,r in enumerate(rs):assert type(r['offset']) is int and r['offset']==s+4*i and type(r['size']) is int and r['size']==4 and bytes.fromhex(r['bytes'])==raw[4*i:4*i+4]
def main():
 pre=B('pre-call-manifest.json');plan=json.loads(pre);status=J('capture/status.json')
 assert H(pre)==status['pre_call_manifest_sha256']=='60a1deb2a419e5ef4ba2e378bb3cf7d0bec7edde39e5168e5376bc5937b5ae02'
 assert status['attempts']==status['children_started']==4 and status['validated_words']==95 and status['selected_bytes_read']==388 and status['validated_bytes']==380 and status['error'] is None and status['watch_unchanged']
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');assert len(before)==16 and before==after['files'] and after['unchanged']
 assert before==[plan['image'],plan['tool'],*plan['pins'],{'path':str(P/'pre-call-manifest.json'),'bytes':len(pre),'sha256':H(pre)}]
 for pin in plan['pins']:
  q=Path(pin['path'])
  if q.parent==P:assert len(B(q.name))==pin['bytes'] and H(B(q.name))==pin['sha256']
 mapping=J('retained-map.json');assert mapping['code_section']=={'addr':'0x15e0','name':'__text','offset':5600,'size':324100} and mapping['data_section']=={'addr':'0x580b0','name':'__const','offset':360624,'size':9672}
 W={};flows=[];associations=[];receipts=[]
 for r in plan['ranges']:
  s=int(r['start'],16);key=f'{s:x}';raw=B(f'capture/{key}.bin');rs=J(f'capture/{key}.stdout.json');rows_check(rs,raw,s,r['words'])
  assert r['file_offset']==s and len(raw)==r['bytes']==int(r['end_exclusive'],16)-s
  for i,row in enumerate(rs):
   pc=s+4*i;w=int.from_bytes(raw[4*i:4*i+4],'little');W[pc]=w;associations.append({'pc':hex(pc),'raw':raw[4*i:4*i+4].hex(),'opcode':row['opcode']});f=flow(w,pc)
   if f:
    if 'target' in f:assert row.get('jump')==f['target']
    flows.append({'pc':hex(pc),**f})
  a=J(f'capture/{key}.invocation-after.json');b=J(f'capture/{key}.invocation-before.json');pid=J(f'capture/{key}.pid.json')
  assert a['argv']==b['argv']==pid['argv']==[plan['tool']['path'],'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(s),'-s',hex(s),'-q','-c',f'pdj {len(rs)}',str(P/'capture'/f'{key}.bin')]
  assert a['pid']==pid['pid']==pid['pgid'] and a['exit_code']==0 and a['error'] is None and not a['timed_out'] and a['cleanup']=='process-group-already-gone' and not B(f'capture/{key}.stderr')
  assert a['stdin']=='DEVNULL' and a['core_limit_bytes']==0 and a['new_process_session'] and a['timeout_seconds']==30 and a['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
  receipts.append(a)
 assert len(W)==95
 assert W[0x1ac20]==0xaa0003f3 and W[0x1aca8]==0xaa1303e0 and W[0x1acb4]==0xd65f03c0
 assert W[0x1b06c]==0xaa0003f3 and W[0x1b068]==0xaa0103f4 and W[0x1b070]==0xb9800c16
 assert W[0x1b0fc]==0xb9001001 and W[0x1b100]==0xd65f03c0
 w=W[0x1b138];assert w&0x9f00001f==0x10000008 and 0x1b138+sx((((w>>5)&0x7ffff)<<2)|((w>>29)&3),21)==0x59710
 src=B('source-context.jsonl').splitlines(keepends=True);meta=J('selected-metadata.json')['records'];cb=cl=0
 for raw,r in zip(src,meta):
  d=json.loads(raw);c=d.pop('code');assert len(raw)==r['raw_bytes'] and H(raw)==r['raw_sha256'] and d==r['metadata'] and len(c.encode())==d['code_bytes'] and H(c.encode())==d['code_sha256'];cb+=len(c.encode());cl+=len(c.splitlines())
 assert len(src)==len(meta)==4 and cb==3007 and cl==108 and not any(r['metadata']['warnings'] for r in meta)
 words=J('capture/data-words.json');raw=B('capture/word-58150.bin');assert len(words)==1 and words[0]['address']=='0x58150' and len(raw)==8 and H(raw)==words[0]['sha256'] and int.from_bytes(raw,'little')==words[0]['little_endian_raw_integer']==0x2c34
 a=J('assessment.json');assert a['runtime_target_resolved'] is False and a['callback_C_addresspoint']=='unknown' and a['R_equals_A']=='conditional-chain-only' and a['successor_selected'] is False
 controls=[]
 def claim(x):assert x
 def reject(n,f):
  try:f()
  except (AssertionError,ValueError,KeyError):controls.append(n);return
  raise AssertionError('negative accepted '+n)
 rs=copy.deepcopy(J('capture/1b138.stdout.json'));rs[0]['offset']+=4;reject('row PC shifted',lambda:rows_check(rs,B('capture/1b138.bin'),0x1b138,11))
 rs=copy.deepcopy(J('capture/1b138.stdout.json'));rs[0]['bytes']='00000000';reject('row bytes replaced',lambda:rows_check(rs,B('capture/1b138.bin'),0x1b138,11))
 reject('whole two-word body truncated',lambda:rows_check(J('capture/1b0fc.stdout.json')[:-1],B('capture/1b0fc.bin'),0x1b0fc,2))
 reject('leaf store uses callback slot+8',lambda:claim(((W[0x1b0fc]>>10)&4095)*4==8))
 reject('helper saved incoming pointer instead of return role',lambda:claim(W[0x1ac20]!=0xaa0003f3))
 reject('current counter load unsigned64',lambda:claim(W[0x1b070]&0xffc00000==0xf9400000))
 reject('big endian word promoted',lambda:claim(int.from_bytes(raw,'big')==0x2c34))
 reject('word treated runtime target proof',lambda:claim(a['runtime_target_resolved']))
 reject('callback addresspoint invented',lambda:claim(a['callback_C_addresspoint']!='unknown'))
 reject('R=A unconditional',lambda:claim(a['R_equals_A']=='proved'))
 reject('missing custody record',lambda:claim(before[:-1]==after['files']))
 reject('automatic target follow',lambda:claim(a['successor_selected']))
 print(json.dumps({'status':'PASS-packet-only','native_rows':95,'native_bytes':380,'data_bytes':8,'C_bytes':cb,'C_lines':cl,'warnings':0,'raw_associations':associations,'raw_flow_fields':flows,'child_receipts':receipts,'custody_pairs':16,'word_raw_integer_only':hex(int.from_bytes(raw,'little')),'negative_controls':controls,'external_reads':0,'original_or_decoder_calls':0},indent=2))
if __name__=='__main__':main()
