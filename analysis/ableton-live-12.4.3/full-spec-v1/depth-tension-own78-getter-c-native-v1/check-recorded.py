#!/usr/bin/env python3
"""Packet-only validation: no external files, imports of collectors, or target execution."""
import argparse,copy,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
def need(x,m):
 if not x:raise ValueError(m)
def load(n):return json.loads((P/n).read_bytes())
def local(raw,rows,source):
 need(len(raw)==8 and len(rows)==2,'whole-body')
 for i,r in enumerate(rows):need(r['offset']==0x3ddc+4*i and r['size']==4 and r['bytes']==raw[4*i:4*i+4].hex(),'association')
 w=int.from_bytes(raw[:4],'little');t=int.from_bytes(raw[4:],'little')
 need(w&0xff800000==0x52800000,'W-MOVZ')
 need((w&31)==0 and ((w>>21)&3)==0 and ((w>>5)&65535)==32,'MOVZ-register-shift-value')
 need(t&0xfffffc1f==0xd65f0000 and ((t>>5)&31)==30,'RET-X30')
 need(source['entry']=='0x3ddc' and source['body_ranges']==[['0x3ddc','0x3de3']] and source['body_bytes']==8,'source-extent')
 need(source['code_bytes']==52 and len(source['code'].splitlines())==7 and hashlib.sha256(source['code'].encode()).hexdigest()==source['code_sha256'],'source-projection')
 need(not source['warnings'] and source['error'] is None and not any(source[k] for k in ['thunk','partial_code','timed_out']),'source-status')
 return {'MOVZ_sf':0,'destination_W':0,'imm16':32,'shift':0,'RET_Rn':30,'conditional_X0_return':32,'instruction_count':2,'calls':0,'memory_accesses':0,'stack_accesses':0}
def main():
 raw=(P/'capture/3ddc.bin').read_bytes();rows=load('capture/3ddc.stdout.json');src=load('source-context.jsonl');facts=local(raw,rows,src)
 status=load('capture/status.json');inv=load('capture/invocation-after.json');outer=load('outer-invocation.json');plan=load('input-plan.json')
 need(status['error'] is None and status['attempts']==1 and not status['automatic_retry'] and status['children_started']==1 and status['native_original_execution']==0,'capture-status')
 need(status['selected_content_bytes_read']==8 and status['validated_rows']==2,'capture-counts')
 need(not inv['timed_out'] and inv['exit_code']==0 and not outer['timed_out'] and outer['exit_code']==0,'process-status')
 need((P/'capture/3ddc.stderr').stat().st_size==0 and (P/'outer.stderr').stat().st_size==0,'stderr')
 need(hashlib.sha256((P/'input-plan.json').read_bytes()).hexdigest()==status['input_plan_sha256'],'input-hash')
 before=load('capture/before-identities.json');after=load('capture/after-identities.json')
 need(before==plan['pins']==after['files'] and after['unchanged'] and status['recorded_custody_pairs']==11,'recorded-custody-only')
 for pin in plan['pins']:
  f=Path(pin['path'])
  if f.parent==P:
   b=f.read_bytes();need(len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256'],'local-frozen-input')
 controls=[]
 def reject(n,b=raw,r=rows,s=src):
  try:local(b,r,s)
  except ValueError:controls.append(n)
  else:raise AssertionError(n)
 reject('short-body',raw[:4]);reject('missing-row',r=rows[:1]);q=copy.deepcopy(rows);q[0]['offset']+=4;reject('wrong-PC',r=q)
 q=copy.deepcopy(rows);q[0]['bytes']='ffffffff';reject('wrong-byte-association',r=q)
 for name,word in [('X-width',0xd2800400),('wrong-register',0x52800401),('wrong-shift',0x52a00400),('wrong-literal',0x52800020)]:
  b=word.to_bytes(4,'little')+raw[4:];q=copy.deepcopy(rows);q[0]['bytes']=b[:4].hex();reject(name,b,q)
 b=raw[:4]+(0xd65f0020).to_bytes(4,'little');q=copy.deepcopy(rows);q[1]['bytes']=b[4:].hex();reject('return-other-register',b,q)
 q=copy.deepcopy(src);q['body_bytes']=12;reject('expanded-extent',s=q)
 q=copy.deepcopy(src);q['partial_code']=True;reject('partial-source',s=q)
 q=copy.deepcopy(src);q['warnings']=['warning'];reject('hidden-warning',s=q)
 print(json.dumps({'status':'PASS','facts':facts,'negative_controls':controls,'control_count':len(controls),'external_reads':0,'ESIL_used':False,'fresh_original_or_native_execution':0,'custody':'retained before/after records only'},indent=2))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',required=True,action='store_true');ap.parse_args();main()
