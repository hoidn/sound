#!/usr/bin/env python3
"""Owned retained/synthetic data only; no original, runtime, old-helper or source reads."""
import copy,importlib.util,json,pathlib,struct,sys,tempfile
H=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('owned_corpus_record',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={'_CreateInstanceU':'0x23b0','_DestroyInstanceU':'0x1','_SetSampleRateU':'0x1','_GetPlugInfoU':'0x1','_CalcA':'0x29c0','_SetParameterA':'0x1','_ResetA':'0x1'}
def synthetic(d,p,rate=1):
 u=next(x for x in d['vectors'] if x['id']==p['vector_id'])
 lines=['slice offset=16384 size=250352']+[f'import {kind} synth_{kind}_{i} slots=1' for kind,n in [('trap',21),('linux',99),('data',7)] for i in range(n)]+[f'export {k} {v}' for k,v in EXPORTS.items()]
 lines+=['mxcsr 0x1f80','transport 0 0 120','create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {w["token"]}' for w in u['words']]+['inflag 1','input '+str(H/'input.f32'),'process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy','used synth_linux_0 1','cxx-failbits 0']
 return '\n'.join(lines)+'\n'
def log_controls(text,p,d):
 param0=next(x for x in text.splitlines() if x.startswith('param 0 '))
 tests=[('exit',text,'',87),('stderr',text,'fault',0),('TRAP',text+'TRAP x\n','',0),('mxcsr',text.replace('mxcsr 0x1f80','mxcsr 0x9fc0'),'',0),('transport',text.replace('transport 0 0 120','transport 1 0 120'),'',0),('rate_argument',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('createNULL',text.replace('create ok','create NULL'),'',0),('wrong_param0',text.replace(param0,'param 0 999'),'',0),('missing_param',text.replace(param0+'\n',''),'',0),('inputflag',text.replace('inflag 1','inflag 0'),'',0),('inputpath',text.replace('input '+str(H/'input.f32'),'input wrong.f32'),'',0),('blockcount',text.replace('blocks=32','blocks=31'),'',0),('CalcAfailure',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('wrongflag',text.replace('flag=1','flag=4'),'',0),('CXXfailure',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('destroy',text.replace('destroy\n',''),'',0),('duplicateexport',text+'export _CalcA 0x29c0\n','',0),('wrongexport',text.replace('export _CalcA 0x29c0','export _CalcA 0x29c4'),'',0),('data_as_code',text.replace('used synth_linux_0','used synth_data_0'),'',0),('newreset',text+'reset\n','',0)]
 out=[]
 for name,t,e,rc in tests:
  try:R.parse_output(t,e,rc,p,d)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out
def selfcheck(d):
 R.validate(d);inputs=R.input_controls(d);R.validate_roles(json.loads((H/'context.json').read_text()));p=d['plans'][0];rates=[]
 for ret in [-7,0,1]:assert R.parse_output(synthetic(d,p,ret),'',0,p,d)['rate_return_observed']==ret;rates.append(ret)
 negatives=log_controls(synthetic(d,p),p,d);audio=[]
 with tempfile.TemporaryDirectory(prefix='corpus-owned-data-') as t:
  pth=pathlib.Path(t)/'data.f32';raw=bytearray(131072);pth.write_bytes(raw);a=R.audio(pth);assert all(c['finite'] and c['nonzero']==0 for c in a['channels']);audio.append('silence_valid_no_prediction')
  struct.pack_into('<f',raw,4096*8,1.0);pth.write_bytes(raw);a=R.audio(pth);assert a['channels'][0]['post4096_energy']==1.0 and a['channels'][1]['post4096_energy']==0.0;audio.append('both_channels_and_window_retained')
  struct.pack_into('<I',raw,0,0x7fc00000);pth.write_bytes(raw);assert not R.audio(pth)['channels'][0]['finite'];audio.append('left_qNaN_detected')
  struct.pack_into('<I',raw,0,0);struct.pack_into('<I',raw,4,0x7f800000);pth.write_bytes(raw);assert not R.audio(pth)['channels'][1]['finite'];audio.append('right_Inf_detected')
  pth.write_bytes(bytes(131071))
  try:R.audio(pth)
  except AssertionError:audio.append('short_stereo_rejected')
  else:raise AssertionError('short accepted')
 return {'input_negatives':inputs,'synthetic_protocol_negatives':negatives,'opaqueRate_positive_values':rates,'synthetic_audio_controls':audio,'original_calls':0,'external_runtime_reads':0}
def check():
 d=json.loads((H/'inputs.json').read_text());controls=selfcheck(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for x in pre['frozen_files']:assert R.ident(x['path'])==x
 outer=json.loads((H/'outer-receipt.json').read_text());assert outer['exit']==0 and outer['interrupted'] is None and outer['retry'] is False and outer['precall_sha256']==outer['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY' and a['error'] is None and all(a['phases'].values());assert [c['vector_id'] for c in a['children']]==[p['vector_id'] for p in d['plans']]
 byid={u['id']:u for u in d['vectors']};actual={};sums={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};negative=[]
 for p,c in zip(d['plans'],a['children']):
  assert c['status']=='RECORDED' and c['exit']==0 and not c['timeout'] and c['cleanup'] is None and c['pid']>0 and c['utc_start']<=c['utc_end'] and c['custody_after']==a['custody_before']
  assert c['argv']==[json.loads((H/'context.json').read_text())['exe'],json.loads((H/'context.json').read_text())['bundle'],p['script']['path'],str(H/'attempts'/p['vector_id']/'output.f32'),'--imports']
  for name in ['stdout','stderr','audio']:assert R.ident(c[name]['path'])==c[name]
  text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert R.parse_output(text,err,c['exit'],p,d)==c['parsed'];assert R.audio(c['audio']['path'])==c['audio_stats'] and all(s['finite'] for s in c['audio_stats']['channels'])
  sums['children']+=1;sums['direct_exports']+=c['parsed']['direct_export_calls'];sums['CalcA']+=c['parsed']['CalcA'];sums['stereo_bytes']+=c['audio_stats']['bytes']
  actual[c['vector_id']]={'receipt_pointer':f'results.json#/children/{sums["children"]-1}','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'argv':c['argv'],'audio':c['audio'],'audio_stats':c['audio_stats'],'parsed':c['parsed'],'new_expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
  if not negative:negative=log_controls(text,p,d)
 assert sums=={'children':57,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104} and len({c['pid'] for c in a['children']})==57 and a['custody_after']==a['custody_before']
 for prev,nxt in zip(a['children'],a['children'][1:]):assert prev['utc_end']<=nxt['utc_start']
 vectors=[{**u,'actual':actual[u['id']]} if u['id'] in actual else u for u in d['vectors']];assert len(vectors)==63 and sum('actual' in u for u in vectors)==57
 return {'status':'PASS','controls':controls,'actual_protocol_negatives':negative,'totals':sums,'logical_aliases':69,'unique_vectors':63,'inherited_vectors':6,'all_finite_both_channels':True,'custody_scope':'Common whole-batch before→each57after/final; NOT perchildbefore/continuous loaded state','alias_catalog':d['catalog'],'vector_catalog':vectors,'original_calls':0,'external_runtime_reads':0,'new_metrics_or_comparators':False}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 else:
  assert sys.argv[1:] in (['--check'],['--write-report']);out=check()
  if sys.argv[1:]==['--write-report']:assert not (H/'author-check.json').exists();R.save(H/'author-check.json',out)
 print(json.dumps({k:v for k,v in out.items() if k not in ['alias_catalog','vector_catalog']}))
