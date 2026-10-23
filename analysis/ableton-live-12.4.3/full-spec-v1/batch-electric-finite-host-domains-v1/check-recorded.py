#!/usr/bin/env python3
"""Only owned synthetic/retaineddata checks; no original/runtime/provider subprocess or old imports."""
import importlib.util,json,pathlib,sys,tempfile,struct,collections
H=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('owned_record',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={'_CreateInstanceU':'0xc030','_DestroyInstanceU':'0xc0b0','_SetSampleRateU':'0xc120','_GetPlugInfoU':'0xc190','_CalcA':'0xc240','_SetParameterA':'0xc550','_ResetA':'0xc5d0'}
def synthetic(d,plan,rate=1):
 return '\n'.join(['slice offset=16384 size=267648']+[f'import linux synthetic_{i} slots=1'for i in range(133)]+[f'export {k} {v}'for k,v in EXPORTS.items()]+['create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {float(w["token"]):.9g}'for w in R.words(d,plan)]+['event 11264 0x90 60 100','event 33314 0x80 60 0','inflag 0','input zero','process 11264 512 flags: 22x(ret=0,flag=0) blocks=22','process 44100 512 flags: 87x(ret=0,flag=1) blocks=87','destroy','used synthetic_0 1','cxx-failbits 0'])+'\n'
def logcontrols(text,plan,d):
 i,v=plan['host_index'],plan['host_value'];param=f'param {i} {v}\n';assert param in text
 tests=[('exit',text,'',2),('stderr',text,'error',0),('trap',text+'\nTRAP x','',0),('bad-on',text.replace('event 11264 0x90 60 100','event 11264 0x90 61 100'),'',0),('bad-off',text.replace('event 33314 0x80 60 0','event 33314 0x80 60 64'),'',0),('rate-arg',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('create-null',text.replace('create ok','create NULL'),'',0),('blockcount',text.replace('blocks=87','blocks=86'),'',0),('calc-fault',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('flag-invalid',text.replace('flag=1','flag=2'),'',0),('input',text.replace('input zero','input signal'),'',0),('inflag',text.replace('inflag 0','inflag 1'),'',0),('cxxfail',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('wrongvarying',text.replace(param,f'param {i} {v+1}\n'),'',0),('missingvarying',text.replace(param,''),'',0),('destroy',text.replace('destroy\n',''),'',0),('duplicateexport',text+'export _CalcA 0xc240\n','',0),('unexpected-init',text+'init 0x314d0\n','',0),('wrongwarmup',text.replace('process 11264 512','process 0 512'),'',0),('badexport',text.replace('export _CalcA 0xc240','export _CalcA 0xc241'),'',0)];out=[]
 for n,t,e,rc in tests:
  try:R.parse(t,e,rc,plan,d)
  except(AssertionError,KeyError,IndexError,ValueError):out.append(n)
  else:raise AssertionError('negativeaccepted '+n)
 return out

def selfcheck(d):
 R.validate(d);n=R.controls(d);positive=[]
 for plan in[d['plans'][0],d['plans'][29],d['plans'][-1]]:
  for rate in[-7,0,1]:assert R.parse(synthetic(d,plan,rate),'',0,plan,d)['Rate_return_opaque_integer']==rate;positive.append([plan['id'],rate])
 logneg=logcontrols(synthetic(d,d['plans'][0]),d['plans'][0],d);audio=[]
 with tempfile.TemporaryDirectory(prefix='electric-finite-owned-')as t:
  p=pathlib.Path(t)/'audio';b=bytearray(442912);p.write_bytes(b);assert R.audio(p)['all_finite']and R.audio(p)['render_nonzero_samples']==[0,0];audio.append('silence-valid')
  struct.pack_into('<I',b,90112,0x80000000);p.write_bytes(b);assert R.audio(p)['render_negative_zero_samples']==[1,0];audio.append('signedzero-distinct')
  struct.pack_into('<I',b,90112,0x7fc00000);p.write_bytes(b);assert not R.audio(p)['all_finite'];audio.append('qNaN-detected')
  p.write_bytes(bytes(442911))
  try:R.audio(p)
  except AssertionError:audio.append('short-rejected')
  else:raise AssertionError('shortaccepted')
 return {'input_negatives':n,'protocol_negatives':logneg,'opaque_Rate_positives':positive,'audio_controls':audio,'original_calls':0,'external_runtime_reads':0}

def check():
 d=json.loads((H/'inputs.json').read_text());controls=selfcheck(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for x in pre['frozen_files']:assert R.ident(x['path'])==x
 o=json.loads((H/'outer-receipt.json').read_text());assert o['exit']==0 and o['interrupted']is None and not o['retry'] and o['precall_sha256']==o['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY'and a['error']is None and all(a['phases'].values());assert[c['id']for c in a['children']]==[p['id']for p in d['plans']]
 sums={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};joins=[];packetneg=[]
 for c,p in zip(a['children'],d['plans']):
  assert c['host_index']==p['host_index']and c['host_value']==p['host_value']and c['status']=='RECORDED'and c['exit']==0 and not c['timeout']and c['pid']>0 and c['utc_start']<=c['utc_end']and c['custody_after']==a['custody_before']
  for n in['stdout','stderr','audio']:assert R.ident(c[n]['path'])==c[n]
  text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert R.parse(text,err,c['exit'],p,d)==c['parsed'];assert R.audio(c['audio']['path'])==c['audio_summary']and c['audio_summary']['all_finite']
  sums['children']+=1;sums['direct_exports']+=c['parsed']['direct_export_calls'];sums['CalcA']+=c['parsed']['CalcA'];sums['stereo_bytes']+=c['audio_summary']['bytes']
  joins.append({'id':p['id'],'host_index':p['host_index'],'host_value':p['host_value'],'vector_sha256':p['vector_sha256'],'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'/children/{len(joins)}','audio':c['audio'],'summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
  if not packetneg:packetneg=logcontrols(text,p,d)
 assert sums=={'children':31,'direct_exports':4495,'CalcA':3379,'stereo_bytes':13730272}and a['custody_after']==a['custody_before']and len({c['pid']for c in a['children']})==31
 for p,n in zip(a['children'],a['children'][1:]):assert p['utc_end']<=n['utc_start']
 byhash={p['vector_sha256']:p for p in joins};vectors=[z if z['historical']is not None else{**z,'actual':byhash[z['vector_sha256']]}for z in d['vectors']];assert len(vectors)==56 and sum('actual'in z for z in vectors)==31
 assert len(d['aliases'])==58 and len({z['vector_sha256']for z in d['aliases']})==56
 return {'status':'PASS','controls':controls,'actual_protocol_negatives':packetneg,'totals':sums,'complete_vectors':vectors,'complete_aliases':d['aliases'],'all_finite':True,'all_warmup_numeric_zero':all(c['audio_summary']['warmup_numeric_zero']for c in a['children']),'all_channels_bit_identical':all(c['audio_summary']['channels_bit_identical']for c in a['children']),'silent_fresh_inputs':[c['id']for c in a['children']if c['audio_summary']['render_nonzero_samples']==[0,0]],'original_calls_by_checker':0,'external_runtime_reads_by_checker':0,'custody_scope':'Onecommonwholebatchbefore→each31after; not childbefore/continuousprovideridentity'}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 else:
  assert sys.argv[1:]in(['--check'],['--write-report']);out=check()
  if sys.argv[1:]==['--write-report']:assert not(H/'author-check.json').exists();R.save(H/'author-check.json',out)
 print(json.dumps({k:v for k,v in out.items()if k not in['complete_vectors','complete_aliases']}))
