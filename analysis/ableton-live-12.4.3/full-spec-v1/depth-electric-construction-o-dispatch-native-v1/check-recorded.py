"""Packet-only fixed25-row/six-word custody and raw-claim checks. No external reads."""
from pathlib import Path
import json,hashlib,copy
P=Path(__file__).resolve().parent

def read(n):
 p=P/n
 assert p.is_relative_to(P)
 return p.read_bytes()
def J(n):return json.loads(read(n))
def H(b):return hashlib.sha256(b).hexdigest()
def sx(v,n):return (v^(1<<(n-1)))-(1<<(n-1))
def branch(w,pc):
 assert w&0xfc000000==0x14000000
 return pc+4*sx(w&0x3ffffff,26)
def adr(w,pc):
 assert w&0x9f000000==0x10000000
 return pc+sx((((w>>5)&0x7ffff)<<2)|((w>>29)&3),21),w&31
def rows_check(rows,raw,start,n):
 assert len(rows)==n and len(raw)==4*n
 for i,r in enumerate(rows):
  assert type(r['offset']) is int and r['offset']==start+4*i
  assert type(r['size']) is int and r['size']==4
  assert bytes.fromhex(r['bytes'])==raw[i*4:i*4+4]

def main():
 plan=J('pre-call-manifest.json');status=J('capture/status.json')
 assert H(read('pre-call-manifest.json'))==status['pre_call_manifest_sha256']=='cd5ff3c503499960fa6db688e18c9f963ffbc559ae9a75b92bec5bdef16c0bc0'
 assert status['attempts']==status['children_started']==2 and status['selected_bytes_read']==148 and status['validated_words']==25 and status['validated_bytes']==100 and status['error'] is None and status['watch_unchanged']
 before=J('capture/before-identities.json');after=J('capture/after-identities.json');assert len(before)==14 and before==after['files'] and after['unchanged']
 for p in plan['pins']:
  q=Path(p['path'])
  if q.parent==P:
   b=read(q.name);assert len(b)==p['bytes'] and H(b)==p['sha256']
 mapping=J('retained-map.json');assert mapping['code_section']=={'addr':'0x3d74','name':'__text','offset':15732,'size':152672} and mapping['data_section']=={'addr':'0x300a0','name':'__const','offset':196768,'size':5752}
 rawwords={};rows=[];receipts=[]
 for start,n in [(0x4db0,1),(0x1b124,24)]:
  key=f'{start:x}';raw=read(f'capture/{key}.bin');rs=J(f'capture/{key}.stdout.json');rows_check(rs,raw,start,n)
  for i,r in enumerate(rs):rawwords[r['offset']]=int.from_bytes(raw[4*i:4*i+4],'little');rows.append({'pc':hex(r['offset']),'raw':raw[4*i:4*i+4].hex(),'opcode':r['opcode']})
  b=J(f'capture/{key}.invocation-before.json');a=J(f'capture/{key}.invocation-after.json');pid=J(f'capture/{key}.pid.json')
  assert b['argv']==a['argv']==pid['argv'] and a['argv'][-2:]==[f'pdj {n}',str(P/'capture'/f'{key}.bin')]
  assert a['pid']==pid['pid']==pid['pgid'] and a['exit_code']==0 and a['error'] is None and not a['timed_out'] and a['cleanup']=='process-group-already-gone' and not read(f'capture/{key}.stderr')
  assert a['stdin']=='DEVNULL' and a['timeout_seconds']==30 and a['core_limit_bytes']==0 and a['new_process_session'] and a['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
  receipts.append(a)
 assert branch(rawwords[0x4db0],0x4db0)==0x4500
 expected=[0x100b0ba8,0xd503201f,0xf9000008,0x7900101f,0x3900281f,0x2901fc1f,0xd503201f,0x5c0801c0,0xfc014000,0x52802008,0x79003808,0xb900201f,0xa908fc1f,0xf900401f,0x6f00e400,0x3c828000,0x3c838000,0x3c848000,0x3c858000,0xf900341f,0x52800028,0x39027008,0x3903601f,0xd65f03c0]
 assert [rawwords[0x1b124+4*i] for i in range(24)]==expected
 assert adr(rawwords[0x1b124],0x1b124)==(0x31298,8)
 w=rawwords[0x1b140];assert w&0xff00001f==0x5c000000 and 0x1b140+4*sx((w>>5)&0x7ffff,19)==0x2b178
 # Exact whitelist is interpreted in assessment: X8 destinations and SIMD0, receiver-based stores, NOP/RET; never an X0 destination, BL or stack operation.
 data=J('capture/data-words.json');assert [int(x['address'],16) for x in data]==[0x30d20,0x30d48,0x30d60,0x30d68,0x30d70,0x30d78]
 for x in data:
  b=read('capture/word-'+x['address'][2:]+'.bin');assert len(b)==8==x['bytes'] and H(b)==x['sha256'] and int.from_bytes(b,'little')==x['little_endian_raw_integer'] and x['file_offset']==int(x['address'],16)
 src=json.loads(read('source-context.jsonl'));assert src['entry']=='0x1b124' and len(src['code'].encode())==700 and len(src['code'].splitlines())==29 and H(src['code'].encode())==src['code_sha256']=='39e0646406b0d8b6803159462416987d909cf39d08f6f8b57087ab9de3254ffa'
 meta=J('selected-metadata.json')['records'];assert len(meta)==2 and meta[0]['metadata']['entry']=='0x4db0' and not meta[0]['C_retained'] and meta[0]['metadata']['body_bytes']==4 and meta[1]['C_retained']
 for x in meta:assert x['metadata']['state']=='exported' and x['metadata']['error'] is None and not x['metadata']['timed_out'] and not x['metadata']['partial_code'] and not x['metadata']['warnings']
 controls=[]
 def claim(value):assert value
 def reject(name,f):
  try:f()
  except (AssertionError,ValueError,KeyError):controls.append(name);return
  raise AssertionError('accepted negative '+name)
 r=copy.deepcopy(J('capture/1b124.stdout.json'));r[0]['offset']+=4;reject('shifted row address',lambda:rows_check(r,read('capture/1b124.bin'),0x1b124,24))
 r=copy.deepcopy(J('capture/1b124.stdout.json'));r[0]['bytes']='00000000';reject('wrong raw row bytes',lambda:rows_check(r,read('capture/1b124.bin'),0x1b124,24))
 reject('expanded thunk is separate550-row native body',lambda:rows_check(J('capture/4db0.stdout.json'),read('capture/4db0.bin'),0x4db0,550))
 reject('4db0 branch has different target',lambda:claim(branch(rawwords[0x4db0],0x4db0)==0x4504))
 reject('helper literal is newly read global content',lambda:claim('capture/2b178.bin' in [str(x.relative_to(P)) for x in P.rglob('*')]))
 reject('one nominated word omitted',lambda:claim(len(data[:-1])==6))
 reject('little endian word interpreted big endian',lambda:claim(int.from_bytes(read('capture/word-30d20.bin'),'big')==data[0]['little_endian_raw_integer']))
 reject('expanded4db0 C retained',lambda:claim(meta[0]['C_retained']))
 reject('missing custody pair',lambda:claim(before[:-1]==after['files']))
 reject('source helper signature proves returnvoid',lambda:claim(expected[-1]!=0xd65f03c0))
 print(json.dumps({'status':'PASS-packet-only','rows':rows,'data_words':data,'raw_branch_4db0_target':'0x4500','raw_1b124_ADR':'0x31298','raw_1b124_literal_address_only':'0x2b178','conditional_X0_input_equals_RET_X0':True,'source_C_bytes':700,'source_C_lines':29,'recorded_custody_pairs':14,'child_receipts':receipts,'negative_controls_rejected':controls,'external_reads':0,'original_calls':0,'proof_limit':'Exact raw fields/recorded custody plus qualified local interpretation, not runtime pointer binding or public ABI.'},indent=2))

if __name__=='__main__':main()
