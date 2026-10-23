#!/usr/bin/env python3
"""Owned synthetic/input/bookkeeping checks; --check is sole-peer retainedactual verification, never originals."""
import importlib.util,json,pathlib,sys,tempfile,struct
H=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('owned_record',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={'_CreateInstanceU':'0xc030','_DestroyInstanceU':'0xc0b0','_SetSampleRateU':'0xc120','_GetPlugInfoU':'0xc190','_CalcA':'0xc240','_SetParameterA':'0xc550','_ResetA':'0xc5d0'}
def synthetic(d,p,rate=1):
 return '\n'.join(['slice offset=16384 size=267648']+[f'import linux synthetic_{i} slots=1'for i in range(133)]+[f'export {k} {v}'for k,v in EXPORTS.items()]+['create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {float(w["token"]):.9g}'for w in d['words']]+[f'event {f} {st:#x} {k} {v}'for f,st,k,v in R.eventpair(p['axis'],p['value'])]+['inflag 0','input zero','process 11264 512 flags: 22x(ret=0,flag=0) blocks=22','process 44100 512 flags: 87x(ret=0,flag=1) blocks=87','destroy','used synthetic_0 1','cxx-failbits 0'])+'\n'
def logcontrols(text,p,d):
 on,off=R.eventpair(p['axis'],p['value']);ontext=f'event {on[0]} {on[1]:#x} 60 100';offtext=f'event {off[0]} {off[1]:#x} 60 {off[3]}';assert ontext in text and offtext in text
 tests=[('exit',text,'',2),('stderr',text,'err',0),('trap',text+'TRAP x\n','',0),('bad-on-status',text.replace(ontext,f'event {on[0]} {on[1]+1:#x} 60 100'),'',0),('bad-off-status',text.replace(offtext,f'event {off[0]} {off[1]+1:#x} 60 {off[3]}'),'',0),('bad-off-velocity',text.replace(offtext,f'event {off[0]} {off[1]:#x} 60 {(off[3]+1)%128}'),'',0),('bad-off-key',text.replace(offtext,f'event {off[0]} {off[1]:#x} 61 {off[3]}'),'',0),('wrong-fixed-param',text.replace('param 0 30\n','param 0 29\n'),'',0),('Rateargument',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('createNULL',text.replace('create ok','create NULL'),'',0),('warmup',text.replace('process 11264 512','process 0 512'),'',0),('renderblocks',text.replace('blocks=87','blocks=86'),'',0),('CalcAret',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('CalcAflag',text.replace('flag=1','flag=2'),'',0),('inflag',text.replace('inflag 0','inflag 1'),'',0),('input',text.replace('input zero','input signal'),'',0),('destroy',text.replace('destroy\n',''),'',0),('CXXfail',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('duplicateexport',text+'export _CalcA 0xc240\n','',0),('wrongexport',text.replace('export _CalcA 0xc240','export _CalcA 0xc241'),'',0),('unexpectedinitializer',text+'init 0x314d0\n','',0)];out=[]
 for n,t,e,rc in tests:
  try:R.parse(t,e,rc,p,d)
  except(AssertionError,KeyError,IndexError,ValueError):out.append(n)
  else:raise AssertionError('negativeaccepted '+n)
 return out

def selfcheck(d):
 R.validate(d);n=R.controls(d);pos=[]
 for p in[d['plans'][0],d['plans'][14],d['plans'][-1]]:
  for rate in[-7,0,1]:assert R.parse(synthetic(d,p,rate),'',0,p,d)['Rate_return_opaque_integer']==rate;pos.append([p['id'],rate])
 protocol=logcontrols(synthetic(d,d['plans'][0]),d['plans'][0],d);audio=[]
 with tempfile.TemporaryDirectory(prefix='electric-axes-synthetic-')as t:
  p=pathlib.Path(t)/'audio';b=bytearray(442912);p.write_bytes(b);assert R.audio(p)['all_finite']and R.audio(p)['render_nonzero_samples']==[0,0];audio.append('silence-valid')
  struct.pack_into('<I',b,90112,0x80000000);p.write_bytes(b);assert R.audio(p)['render_negative_zero_samples']==[1,0];audio.append('signedzero-preserved')
  struct.pack_into('<I',b,90112,0x7fc00000);p.write_bytes(b);assert not R.audio(p)['all_finite'];audio.append('qNaN-detected')
  p.write_bytes(bytes(442911))
  try:R.audio(p)
  except AssertionError:audio.append('short-rejected')
  else:raise AssertionError('shortaccepted')
 return{'input_negatives':n,'synthetic_protocol_negatives':protocol,'opaqueRate_boundaries':pos,'synthetic_audio_controls':audio,'original_calls':0,'actual_raw_reads':0,'runtime_reads':0}

def recorded(peer=False):
 d=json.loads((H/'inputs.json').read_text());R.validate(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for x in pre['frozen_files']:assert R.ident(x['path'])==x
 o=json.loads((H/'outer-receipt.json').read_text());assert o['exit']==0 and o['interrupted']is None and not o['retry']and o['precall_sha256']==o['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY'and a['error']is None and all(a['phases'].values());assert[c['id']for c in a['children']]==[p['id']for p in d['plans']]
 totals={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};actual=[];pneg=[]
 for c,p in zip(a['children'],d['plans']):
  assert(c['id'],c['axis'],c['value'])==(p['id'],p['axis'],p['value'])and c['exit']==0 and not c['timeout']and c['status']=='RECORDED'and c['custody_after']==a['custody_before']and c['pid']>0
  assert c['audio']['bytes']==442912 and c['stderr']['bytes']==0 and c['parsed']['direct_export_calls']==145 and c['parsed']['CalcA']==109 and c['audio_summary']['all_finite']and c['audio_summary']['warmup_numeric_zero']
  if peer:
   for k in['stdout','stderr','audio']:assert R.ident(c[k]['path'])==c[k]
   text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert R.parse(text,err,c['exit'],p,d)==c['parsed'];assert R.audio(c['audio']['path'])==c['audio_summary']
   if not pneg:pneg=logcontrols(text,p,d)
  totals['children']+=1;totals['direct_exports']+=c['parsed']['direct_export_calls'];totals['CalcA']+=c['parsed']['CalcA'];totals['stereo_bytes']+=c['audio']['bytes']
  actual.append({'id':c['id'],'axis':c['axis'],'value':c['value'],'history_sha256':p['history_sha256'],'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'/children/{len(actual)}','audio':c['audio'],'recorded_collector_output_summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
 assert totals=={'children':142,'direct_exports':20590,'CalcA':15478,'stereo_bytes':62893504}and a['custody_after']==a['custody_before']and len({c['pid']for c in a['children']})==142
 for c,n in zip(a['children'],a['children'][1:]):assert c['utc_end']<=n['utc_start']
 byhash={c['history_sha256']:c for c in actual};histories=[z if z['historical']is not None else{**z,'actual':byhash[z['history_sha256']]}for z in d['histories']];assert len(histories)==143 and sum('actual'in z for z in histories)==142
 return{'status':'PASS','scope':'Solepeer retainedactual verification'if peer else'Author bookkeeping/recordedcollectorstatus ONLY, not independentactualreview','actual_raw_reopened_by_this_check':peer,'totals':totals,'complete_histories':histories,'complete_aliases':d['aliases'],'collector_recorded_allfinite':True,'collector_recorded_warmup_numeric_zero':True,'collector_recorded_all_channels_equal':all(c['audio_summary']['channels_bit_identical']for c in a['children']),'collector_recorded_silent_inputs':[c['id']for c in a['children']if c['audio_summary']['render_nonzero_samples']==[0,0]],'actual_protocol_negative_controls':pneg,'custody_scope':'Onecommonwholebatchbefore→each142after/notperchildbefore/continuousproviderproof','original_calls_by_this_check':0,'runtime_reads_by_this_check':0}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 elif sys.argv[1:]==['--author-bookkeeping']:
  out=recorded(False);assert not(H/'author-check.json').exists();R.save(H/'author-check.json',out)
 else:assert sys.argv[1:]==['--check'];out=recorded(True)
 print(json.dumps({k:v for k,v in out.items()if k not in['complete_histories','complete_aliases']}))
