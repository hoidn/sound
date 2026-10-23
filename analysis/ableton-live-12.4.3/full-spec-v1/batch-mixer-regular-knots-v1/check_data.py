#!/usr/bin/env python3
"""Owned packet-only checker/analyzer. Never launches a child or opens runtime images."""
import copy,hashlib,json,math,pathlib,struct,sys
sys.dont_write_bytecode=True
import run_batch as rec
H=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((H/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def same_file(pin):
 p=pathlib.Path(pin['path']);assert p.is_relative_to(H);b=p.read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256']
def bits_info(bits):
 i=int(bits,16);v=struct.unpack('<f',struct.pack('<I',i))[0]
 return {'bits32':bits,'binary32_hex':v.hex(),'class':'NaN' if math.isnan(v) else ('Inf' if math.isinf(v) else ('zero' if v==0 else 'finite')),'sign':i>>31}
def historical(d):
 b=(H/'inherited-records.jsonl').read_bytes();idx=load('inherited-index.json');records={}
 assert len(idx)==21
 for x in idx:
  raw=b[x['selected_offset']:x['selected_offset']+x['bytes']];assert sha(raw)==x['sha256'];records[x['original_index']]=(x,json.loads(raw))
 assert sum(x['bytes'] for x in idx)==len(b)
 for r in d['rows']:
  if r['historical'] is None:continue
  h=r['historical'];x,old=records[h['input_row_index']]
  assert h['result_raw_sha256']==x['sha256'] and h['result_raw_bytes']==x['bytes'] and h['result_byte_offset']==x['original_byte_offset']
  assert old['id']==h['input_id'] and old['rc']==0 and not old['timeout'] and not old['stderr'] and h['pid'] is None
  # Historical argv is exact existing scalar protocol; no new PID or receipt.
  argv=old['argv'];start=argv.index('call');t=argv[start:];j=h['input_tokens_offset'];assert t[j:j+3]==['call',r['function'],r['token']]
  line=next(x for x in old['stdout'].splitlines() if x.startswith(f'call {h["call_index"]} '));assert line==h['call_line']
  assert f'{int(line.split(" xmm0=")[1].split()[0],16)&0xffffffff:08x}'==r['expected_bits32']==h['bits32']
 return records
def verify_actual(d,a):
 assert a['status']=='COMPLETE-ONE-ATTEMPT-PER-CURVE' and a['error'] is None and len(a['children'])==7
 assert all(a['phases'].values());assert a['custody_before']==a['custody_after']
 ctx=load('context.json');freeze=load('manifest-before.json');assert a['custody_before']==ctx['watched']+freeze['frozen_files']
 assert len(a['host_parser'])==903
 for p,r in zip(a['host_parser'],d['rows']):assert p['id']==r['id'] and p['token']==r['token'] and p['argument_bits32_le']==bytes.fromhex(r['input_bits32'])[::-1].hex()
 byid={r['id']:r for r in d['rows']};observed={};common=None
 for p,c in zip(d['plans'],a['children']):
  assert c['curve']==p['curve'] and c['pid']>0 and c['exit']==0 and not c['timeout'] and c['status']=='RECORDED'
  assert c['argv']==[ctx['loader'],ctx['image'],'--imports']+p['tokens'];assert c['custody_after']==a['custody_before']
  for k in ('stdout','stderr'):same_file(c[k])
  parsed=rec.parse_output(pathlib.Path(c['stdout']['path']).read_text(),pathlib.Path(c['stderr']['path']).read_text(),c['exit'],p,byid)
  assert parsed==c['parsed']
  if common is None:common=parsed['imports']
  else:assert common==parsed['imports']
  for call in parsed['calls']:
   rid=call['row_id'];assert rid not in observed;observed[rid]={'call':call,'pid':c['pid'],'curve':c['curve'],'stdout':c['stdout'],'call_index':call['index']}
 assert len(observed)==826 and len({c['pid'] for c in a['children']})==7
 out=[]
 for r in d['rows']:
  z={k:r[k] for k in ('id','curve','name','k','i','function','token','input_bits32','provenance','expected_bits32','oracle_class','portable_comparator')}
  if r['historical'] is not None:z.update(observation=bits_info(r['historical']['bits32']),historical=r['historical'],fresh=None)
  else:
   q=observed[r['id']];z.update(observation=bits_info(q['call']['low_xmm0_bits32']),historical=None,fresh=q)
  out.append(z)
 return {'schema':'mixer-903-logical-observations-v1','counts':{'logical':903,'inherited':77,'fresh':826,'children':7,'direct_calls':826,'buffers':0},'classification':{cl:sum(z['observation']['class']==cl for z in out) for cl in ('finite','zero','Inf','NaN')},'fresh_classification':{cl:sum(z['observation']['class']==cl and z['fresh'] is not None for z in out) for cl in ('finite','zero','Inf','NaN')},'all903':out,'used_imports':[{'curve':c['curve'],'used':c['parsed']['used']} for c in a['children']],'import_declarations':{k:sum(x['kind']==k for x in common) for k in ('linux','linux-data','trap')},'interpretation':'Fresh expectations were NULL. Output low32 bits are retained finite local x86 observations only; no fitted law, portable comparator, runtime table read, actual entry register or fenv proof, interpolation/public/ARM/audio/track/ramp assertion.'}
def controls(d,a):
 def reject(label,mut):
  x=copy.deepcopy(a);mut(x)
  try:verify_actual(d,x)
  except (AssertionError,KeyError,ValueError,IndexError):return label
  raise AssertionError('accepted invalid '+label)
 mutations=[('missing-child',lambda x:x['children'].pop()),('duplicated-child-pid',lambda x:x['children'][1].update(pid=x['children'][0]['pid'])),('nonzero-status',lambda x:x['children'][0].update(exit=1)),('timeout',lambda x:x['children'][0].update(timeout=True)),('custody-change',lambda x:x['custody_after'][0].update(sha256='0'*64)),('invented-expected',lambda x:x['children'][0]['parsed']['calls'][0].update(precall_expected='00000000')),('wrong-saved-lane',lambda x:x['children'][0]['parsed']['calls'][0].update(low_xmm0_bits32='ffffffff')),('output-omission',lambda x:x['children'][0]['parsed']['calls'].pop()),('extra-setup-argv',lambda x:x['children'][0]['argv'].append('poke')),('parser-endian',lambda x:x['host_parser'][1].update(argument_bits32_le='00000000')),('unrecorded-import-use',lambda x:x['children'][0]['parsed']['used'].update(_malloc=1)),('raw-hash',lambda x:x['children'][0]['stdout'].update(sha256='0'*64)),('false-all-completed',lambda x:x['phases'].update(all_children_completed=False))]
 passed=[reject(*m) for m in mutations]
 c=a['children'][0];p=d['plans'][0];byid={r['id']:r for r in d['rows']};text=pathlib.Path(c['stdout']['path']).read_text()
 for label,altered,err,rc in [('trap-output',text+'TRAP missing\n','',0),('fault-stderr',text,'FAULT unexpected',0),('unexpected-used',text+'used _malloc 1\n','',0),('nonzero-child',text,'',86),('extra-buffer',text+'out b0 0x1 00\n','',0),('wrong-header',text.replace(rec.HEADER,'loaded invalid',1),'',0),('missing-call',text.replace(next(z for z in text.splitlines(keepends=True) if z.startswith('call 0 ')),'',1),'',0)]:
  try:rec.parse_output(altered,err,rc,p,byid)
  except (AssertionError,KeyError,IndexError):passed.append(label)
  else:raise AssertionError('parser accepted '+label)
 return passed
def main():
 assert sys.argv[1:]==['--check'];d=load('inputs.json');rec.validate(d);historical(d)
 for pin in load('manifest-before.json')['frozen_files']:same_file(pin)
 a=load('results.json');out=verify_actual(d,a);negative=controls(d,a)
 report={'status':'PASS','input_negatives':rec.input_controls(d),'recorded_negatives':negative,'counts':out['counts'],'classification':out['classification'],'fresh_classification':out['fresh_classification'],'original_calls_by_checker':0,'runtime_external_reads_by_checker':0,'partial_null_history_preserved':True}
 if (H/'manifest.json').exists():
  manifest=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in manifest['files']}
  for f in manifest['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
  assert load('observations.json')==out;print(json.dumps(report));return
 rec.save(H/'observations.json',out);rec.save(H/'author-check.json',report);print(json.dumps(report))
if __name__=='__main__':main()
