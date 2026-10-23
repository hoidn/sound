#!/usr/bin/env python3
"""Packet-only Corpus checks. No outside runtime, source, old audio or original calls."""
import copy,hashlib,json,pathlib,struct,sys
sys.dont_write_bytecode=True
import record as rec
H=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((H/n).read_text())
def own(pin):
 p=pathlib.Path(pin['path']);assert p.is_relative_to(H);b=p.read_bytes();assert len(b)==pin['bytes'] and rec.sha(b)==pin['sha256']
def check(d,a):
 rec.validate(d);assert a['status']=='COMPLETE-ONCE-NO-RETRY' and a['error'] is None and all(a['phases'].values()) and len(a['children'])==3
 ctx=load('context.json');freeze=load('manifest-before.json');assert a['custody_before']==a['custody_after']==ctx['watched']+freeze['frozen_files']
 assert ctx['environment']=={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','XDEV_TIME':'0','XDEV_LIBM_ULP':'0'}
 ids=set();imports=None;exports=None;inits=None
 for p,c in zip(d['plans'],a['children']):
  assert c['shape']==p['shape'] and c['pid']>0 and c['pid'] not in ids;ids.add(c['pid'])
  assert c['exit']==0 and not c['timeout'] and c['status']=='RECORDED' and c['custody_after']==a['custody_before']
  assert c['argv']==[ctx['exe'],ctx['bundle'],p['script'],str(H/'attempts'/f'shape-{p["shape"]}'/'output.f32'),'--imports']
  for k in ('audio','stdout','stderr'):own(c[k])
  q=rec.parse_output(pathlib.Path(c['stdout']['path']).read_text(),pathlib.Path(c['stderr']['path']).read_text(),c['exit'],p,d);assert q==c['parsed']
  s=rec.audio(c['audio']['path']);assert s==c['audio_stats'] and all(x['finite'] for x in s['channels'])
  if imports is None:imports=q['imports'];exports=q['exports'];inits=q['initializers']
  else:assert imports==q['imports'] and exports==q['exports'] and inits==q['initializers']
 for r in d['catalog']:
  if r['historical'] is not None:assert r['historical']['new_pid'] is None and r['historical']['new_receipt'] is None and r['historical']['output_bytes']==131072
 # Exact input copy inspected as input DATA only; no old output opened.
 raw=(H/'input.f32').read_bytes();assert len(raw)==131072 and rec.sha(raw)==ctx['input_source']['sha256']
 vals=struct.unpack('<32768f',raw);assert [(i//2,i%2,v) for i,v in enumerate(vals) if v!=0]==[(4096,0,1.0),(4096,1,1.0)]
 pairs=[]
 for i,c in enumerate(a['children']):
  for other in a['children'][i+1:]:
   x=pathlib.Path(c['audio']['path']).read_bytes();y=pathlib.Path(other['audio']['path']).read_bytes();pairs.append({'shapes':[c['shape'],other['shape']],'byte_equal':x==y,'differing_binary32_words':sum(x[j:j+4]!=y[j:j+4] for j in range(0,len(x),4))})
 return {'schema':'Corpus-deterministic-Free-LFO-observations-v1','logical_catalog':d['catalog'],'counts':d['counts'],'fresh':[{'shape':c['shape'],'name':rec.NAMES[c['shape']],'output':c['audio'],'audio_stats':c['audio_stats'],'pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'stdout':c['stdout'],'receipt_pointer':f'results.json#/children/{i}','new_prior_expected':None,'portable_comparator':None,'used_imports':c['parsed']['used']} for i,c in enumerate(a['children'])],'fresh_pair_observations':pairs,'imports_declared_each':{kind:sum(x['kind']==kind for x in imports) for kind in ('linux','data','trap')},'export_addresses_recorded':exports,'limits':'NULL priors retained; finite supplied-host stereo observations, no shape fitting/internal LFO buffer/math law/public/ARM/seed-general/audio tolerance. Inherited0/3 outputs not opened or replayed; random5/6 separateU, not omitted deterministicmembers.'}
def negatives(d,a):
 out=[]
 changes=[('missing-child',lambda x:x['children'].pop()),('pid-reused',lambda x:x['children'][1].update(pid=x['children'][0]['pid'])),('nonzero-exit',lambda x:x['children'][0].update(exit=1)),('timeout',lambda x:x['children'][0].update(timeout=True)),('raw-hash',lambda x:x['children'][0]['audio'].update(sha256='0'*64)),('custody',lambda x:x['custody_after'][0].update(sha256='0'*64)),('wrong-shape',lambda x:x['children'][0].update(shape=0)),('extra-argv',lambda x:x['children'][0]['argv'].append('retry')),('invented-energy',lambda x:x['children'][0]['audio_stats']['channels'][0].update(post4096_energy=x['children'][0]['audio_stats']['channels'][0]['post4096_energy']+1)),('parsed-extra-import',lambda x:x['children'][0]['parsed']['used'].update(_unbound=1)),('false-completed',lambda x:x['phases'].update(all_children_completed=False))]
 for label,mut in changes:
  x=copy.deepcopy(a);mut(x)
  try:check(d,x)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(label)
  else:raise AssertionError('accepted '+label)
 c=a['children'][0];p=d['plans'][0];text=pathlib.Path(c['stdout']['path']).read_text()
 for label,outtext,err,rc in [('TRAP',text+'TRAP x\n','',0),('FAULT',text,'FAULT x',0),('bad-cxx',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('missing-param',text.replace(next(l for l in text.splitlines(keepends=True) if l.startswith('param 18 ')),''),'',0),('wrong-return-flags',text.replace('32x(ret=0,flag=1)','32x(ret=1,flag=1)'),'',0),('unexpected-command',text+'reset\n','',0),('wrong-rate',text.replace('rate 44100 ret=0','rate 48000 ret=0'),'',0)]:
  try:rec.parse_output(outtext,err,rc,p,d)
  except (AssertionError,KeyError,IndexError,ValueError,StopIteration):out.append(label)
  else:raise AssertionError('accepted '+label)
 return out

def main():
 assert sys.argv[1:]==['--check'];d=load('inputs.json');a=load('results.json')
 for pin in load('manifest-before.json')['frozen_files']:own(pin)
 observed=check(d,a);report={'status':'PASS','counts':d['counts'],'input_negatives':rec.input_controls(d),'recorded_negatives':negatives(d,a),'original_calls':0,'outside_runtime_source_oldraw_reads':0,'no_formula_or_tolerance_fitted':True}
 if (H/'manifest.json').exists():
  m=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in m['files']}
  for f in m['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and rec.sha(b)==f['sha256']
  assert load('observations.json')==observed and load('author-check.json')==report
 else:rec.save(H/'observations.json',observed);rec.save(H/'author-check.json',report)
 print(json.dumps(report))
if __name__=='__main__':main()
