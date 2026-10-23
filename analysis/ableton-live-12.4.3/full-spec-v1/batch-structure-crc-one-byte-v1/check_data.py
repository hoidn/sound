#!/usr/bin/env python3
"""Owned data-only whole-byte CRC validation; no external runtime/oldraw/source reads."""
import copy,hashlib,json,pathlib,re,sys
sys.dont_write_bytecode=True
import run_batch as rec
H=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((H/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def own_pin(p):
 q=pathlib.Path(p['path']);assert q.is_relative_to(H);b=q.read_bytes();assert len(b)==p['bytes'] and sha(b)==p['sha256']
def polynomial_remainder(b):
 # Independent integer polynomial long division of byte*x^16 by x^16+x^15+x^2+1.
 x=b<<16
 for bit in range(23,15,-1):
  if x&(1<<bit):x^=0x18005<<(bit-16)
 assert 0<=x<65536
 return x

def historical(d):
 p=H/'protocol/inherited-summary.json';raw=p.read_bytes();s=json.loads(raw);pins=load('authority-pins.json');pin=next(x for x in pins if x['path'].endswith('/out/x-crc.json'));assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256']
 for byte,index in [(0,2),(255,3),(183,4)]:
  r=d['rows'][byte];h=r['historical'];old=s['runs'][index]
  assert h['summary_pointer']==f'/runs/{index}' and h['summary_sha256']==sha(raw) and h['crc16']==old['x86_result']==old['rule']==polynomial_remainder(byte)
  assert old['bytes']==1 and old['sha256']==r['input_sha256']==sha(bytes([byte])) and old['calls']==1 and old['used_imports']=={} and old['ok'] and not old['trap'] and not old['fault']
  assert h['pid'] is None and h['utc'] is None and h['raw_receipt'] is None
 assert len({d['rows'][b]['input_sha256'] for b in rec.OLD})==3

def actual(d,a):
 assert a['status']=='COMPLETE-ONE-ATTEMPT-PER-CHILD' and a['error'] is None and len(a['children'])==2 and all(a['phases'].values())
 ctx=load('context.json');freeze=load('manifest-before.json');assert a['custody_before']==a['custody_after']==ctx['watched']+freeze['frozen_files'];byid={r['id']:r for r in d['rows']};allcalls={};imports=None
 for p,c in zip(d['plans'],a['children']):
  assert c['child']==p['child'] and c['pid']>0 and c['exit']==0 and not c['timeout'] and c['status']=='RECORDED'
  assert c['argv']==[ctx['loader'],ctx['image'],'--imports']+p['tokens'] and c['custody_after']==a['custody_before']
  for key in ('stdout','stderr'):own_pin(c[key])
  parsed=rec.parse_output(pathlib.Path(c['stdout']['path']).read_text(),pathlib.Path(c['stderr']['path']).read_text(),c['exit'],p,byid);assert parsed==c['parsed']
  if imports is None:imports=parsed['imports']
  else:assert imports==parsed['imports']
  for call in parsed['calls']:
   rid=call['row_id'];assert rid not in allcalls;allcalls[rid]={'child':c['child'],'pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'stdout':c['stdout'],'call':call}
 assert len(allcalls)==253 and len({c['pid'] for c in a['children']})==2
 rows=[]
 for r in d['rows']:
  assert r['expected_low16']==polynomial_remainder(r['byte'])
  out={k:r[k] for k in ('id','byte','payload_hex','input_sha256','entry','length','initial_seed_bytes_le','expected_low16','expected_low16_hex','expected_full32','portable_comparator','provenance')}
  if r['historical'] is not None:out.update(historical=r['historical'],fresh=None,observed_low16=r['historical']['crc16'],observed_full32=None,agrees=True)
  else:
   q=allcalls[r['id']];out.update(historical=None,fresh=q,observed_low16=q['call']['semantic_low16'],observed_full32=q['call']['result_u32_le'],agrees=q['call']['agrees'])
  rows.append(out)
 assert all(r['agrees'] for r in rows)
 return {'schema':'whole-crc-one-byte-observations-v1','counts':{'logical':256,'inherited':3,'fresh':253,'children':2,'direct_calls':253,'buffers_each':[254,252],'oracle_agreements_fresh':253},'import_declarations_each':{kind:sum(x['kind']==kind for x in imports) for kind in ('linux','linux-data','trap')},'used_imports_each':[c['parsed']['used_imports'] for c in a['children']],'all256':rows,'semantic':'Existing integer CRC16 rule low16 little-endian of4B output only; upper16 is retained observed data, no expectation or portable comparator. Saved RAX/RDX/XMM0/XMM1 not semantic CRC returns. Three old rows have no fabricated process/raw/fullword data. Local supplied byte buffers only; public/file/ARM/application binding unknown.'}

def controls(d,a):
 def reject(label,mut):
  x=copy.deepcopy(a);mut(x)
  try:actual(d,x)
  except (AssertionError,KeyError,IndexError,ValueError):return label
  raise AssertionError('negative accepted '+label)
 mutations=[('missing-child',lambda x:x['children'].pop()),('same-pid',lambda x:x['children'][1].update(pid=x['children'][0]['pid'])),('nonzero-exit',lambda x:x['children'][0].update(exit=1)),('timeout',lambda x:x['children'][0].update(timeout=True)),('custody-mismatch',lambda x:x['custody_after'][0].update(sha256='0'*64)),('raw-hash',lambda x:x['children'][0]['stdout'].update(sha256='0'*64)),('extra-argv',lambda x:x['children'][0]['argv'].append('call')),('wrong-low16',lambda x:x['children'][0]['parsed']['calls'][0].update(semantic_low16=0)),('changed-fullword',lambda x:x['children'][0]['parsed']['calls'][0].update(result_u32_le=0)),('changed-lane',lambda x:x['children'][0]['parsed']['calls'][0]['carriers64'].update(rax=f'{int(x["children"][0]["parsed"]["calls"][0]["carriers64"]["rax"],16)^1:016x}')),('wrong-buffer',lambda x:x['children'][0]['parsed']['calls'][0]['buffers_after'][1].update(index=0)),('missing-call',lambda x:x['children'][0]['parsed']['calls'].pop()),('invented-import',lambda x:x['children'][0]['parsed']['used_imports'].update(_malloc=1)),('false-completion',lambda x:x['phases'].update(all_children_completed=False))]
 passed=[reject(*m) for m in mutations]
 c=a['children'][0];p=d['plans'][0];byid={r['id']:r for r in d['rows']};text=pathlib.Path(c['stdout']['path']).read_text();firstdump=next(l for l in text.splitlines(keepends=True) if l.startswith('dump b1 '));firstout=next(l for l in text.splitlines(keepends=True) if l.startswith('out b1 '))
 tests=[('trap-output',text+'TRAP unbound\n','',0),('fault-stderr',text,'FAULT invalid',0),('counted-import',text+'used _malloc 1\n','',0),('failed-child',text,'',86),('missing-dump',text.replace(firstdump,'',1),'',0),('wrong-dump-index',text.replace('dump b1 ','dump b0 ',1),'',0),('input-byte-mutation',re.sub(r'out b0 (0x[0-9a-f]+) [0-9a-f]{2}',r'out b0 \1 ff',text,count=1),'',0),('CRC-disagreement',text.replace(firstout,firstout[:-9]+'00000000\n',1).replace(firstdump,firstdump[:-9]+'00000000\n',1),'',0)]
 for label,out,err,rc in tests:
  try:rec.parse_output(out,err,rc,p,byid)
  except (AssertionError,KeyError,IndexError,ValueError):passed.append(label)
  else:raise AssertionError('parser negative accepted '+label)
 # Positive controls: high output16 and RAX are not part of selected CRC16 oracle.
 oldhex=firstdump.split()[-1];altered=oldhex[:4]+'3412';positive=text.replace(firstout,firstout.replace(oldhex,altered),1).replace(firstdump,firstdump.replace(oldhex,altered),1)
 q=rec.parse_output(positive,'',0,p,byid);assert q['calls'][0]['upper16_observed']==0x1234 and q['calls'][0]['agrees']
 positive2=re.sub(r'(call 0 .*? rax=)0x[0-9a-f]+',r'\g<1>0xffffffffffffffff',text,count=1);q=rec.parse_output(positive2,'',0,p,byid);assert q['calls'][0]['carriers64']['rax']=='ffffffffffffffff' and q['calls'][0]['agrees']
 return passed,['upper16-not-oracle','rax-not-semantic-result','polynomial-long-division-all256']

def main():
 assert sys.argv[1:]==['--check'];d=load('inputs.json');rec.validate(d);historical(d)
 for p in load('manifest-before.json')['frozen_files']:own_pin(p)
 a=load('results.json');out=actual(d,a);negative,positive=controls(d,a)
 report={'status':'PASS','counts':out['counts'],'input_negatives':rec.input_controls(d),'recorded_negatives':negative,'positive_controls':positive,'original_calls_by_checker':0,'external_runtime_reads_by_checker':0,'old_raw_reads_by_checker':0}
 if (H/'manifest.json').exists():
  m=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in m['files']}
  for f in m['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
  assert load('observations.json')==out;print(json.dumps(report));return
 rec.save(H/'observations.json',out);rec.save(H/'author-check.json',report);print(json.dumps(report))
if __name__=='__main__':main()
