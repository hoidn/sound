#!/usr/bin/env python3
"""Owned retained/synthetic-data checks only. No oldmodule/helper/provider/runtime execution/read."""
import importlib.util,json,pathlib,sys,tempfile,struct
H=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('owned_record',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={'_CreateInstanceU':'0x1fd70','_DestroyInstanceU':'0x1fdf0','_SetSampleRateU':'0x1fe60','_GetPlugInfoU':'0x1fed0','_CalcA':'0x1ff80','_SetParameterA':'0x20290','_ResetA':'0x20310'}
def synthetic(d,v=0,rate=1):
 return '\n'.join(['init 0x314d0','slice offset=16384 size=500880']+[f'import linux synthetic_{i} slots=1' for i in range(132)]+[f'export {k} {v}' for k,v in EXPORTS.items()]+['create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {float(w["token"]):.9g}' for w in R.words(d,v)]+['event 4400 0x90 60 100','event 35270 0x80 60 64','inflag 0','input zero','process 44100 512 flags: 87x(ret=0,flag=1) blocks=87','destroy','used synthetic_0 1','cxx-failbits 0'])+'\n'
def log_controls(text,v,d):
 param=f'param 4 {v}\n';tests=[('exit',text,'',2),('stderr',text,'unexpected',0),('trap',text+'\nTRAP x','',0),('on-key',text.replace('event 4400 0x90 60 100','event 4400 0x90 61 100'),'',0),('off-key',text.replace('event 35270 0x80 60 64','event 35270 0x80 61 64'),'',0),('off-velocity',text.replace('event 35270 0x80 60 64','event 35270 0x80 60 0'),'',0),('Rateargument',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('createNULL',text.replace('create ok','create NULL'),'',0),('blockcount',text.replace('blocks=87','blocks=86'),'',0),('CalcAfailure',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('input',text.replace('input zero','input signal'),'',0),('inflag',text.replace('inflag 0','inflag 1'),'',0),('failbits',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('wrongvaryingword',text.replace(param,f'param 4 {(v+1)%25}\n'),'',0),('wrongfixed99',text.replace('param 99 1\n','param 99 0\n'),'',0),('missingparam4',text.replace(param,''),'',0),('destroy',text.replace('destroy\n',''),'',0),('duplicateexport',text+'\nexport _CalcA 0x1ff80','',0),('initializer',text.replace('init 0x314d0','init 0x314d4'),'',0),('missinginitializer',text.replace('init 0x314d0\n',''),'',0),('wrongexport',text.replace('export _CalcA 0x1ff80','export _CalcA 0x1ff81'),'',0)];out=[]
 for name,t,e,rc in tests:
  try:R.parse(t,e,rc,v,d)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 return out

def selfcheck(d):
 R.validate(d);n=R.controls(d);positive=[]
 for v in [0,24]:
  for rate in [-7,0,1]:assert R.parse(synthetic(d,v,rate),'',0,v,d)['Rate_return_opaque_integer']==rate;positive.append([v,rate])
 logneg=log_controls(synthetic(d),0,d);audio=[]
 with tempfile.TemporaryDirectory(prefix='analog-owned-data-') as t:
  p=pathlib.Path(t)/'data.f32';raw=bytearray(352800);p.write_bytes(raw);assert R.audio(p)['all_finite'] and R.audio(p)['nonzero_samples']==[0,0];audio.append('zeroaudio-retained-valid')
  struct.pack_into('<I',raw,0,0x80000000);p.write_bytes(raw);assert R.audio(p)['negative_zero_samples']==[1,0];audio.append('signedzero-distinguished-not-normalized')
  struct.pack_into('<I',raw,0,0x7fc00000);p.write_bytes(raw);assert not R.audio(p)['all_finite'];audio.append('qNaN-detected')
  p.write_bytes(bytes(352799))
  try:R.audio(p)
  except AssertionError:audio.append('short-output-rejected')
  else:raise AssertionError('shortaccepted')
 return {'input_negatives':n,'synthetic_protocol_negatives':logneg,'opaqueRate_endpoint_positives':positive,'synthetic_audio_controls':audio,'original_calls':0,'external_runtime_reads':0}

def check():
 d=json.loads((H/'inputs.json').read_text());controls=selfcheck(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for x in pre['frozen_files']:assert R.ident(x['path'])==x
 outer=json.loads((H/'outer-receipt.json').read_text());assert outer['exit']==0 and outer['interrupted'] is None and not outer['retry'] and outer['precall_sha256']==outer['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY' and a['error'] is None and all(a['phases'].values());assert [c['transpose_integer'] for c in a['children']]==[p['transpose_integer'] for p in d['plans']]
 sums={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};joins=[];packetneg=[]
 for c in a['children']:
  v=c['transpose_integer'];assert c['status']=='RECORDED' and c['exit']==0 and not c['timeout'] and c['pid']>0 and c['utc_start']<=c['utc_end'] and c['custody_after']==a['custody_before']
  for name in ['stdout','stderr','audio']:assert R.ident(c[name]['path'])==c[name]
  text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert R.parse(text,err,c['exit'],v,d)==c['parsed'];assert R.audio(c['audio']['path'])==c['audio_summary'] and c['audio_summary']['all_finite']
  sums['children']+=1;sums['direct_exports']+=c['parsed']['direct_export_calls'];sums['CalcA']+=c['parsed']['CalcA'];sums['stereo_bytes']+=c['audio_summary']['bytes']
  joins.append({'transpose_integer':v,'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'results.json#/children/{len(joins)}','audio':c['audio'],'summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
  if not packetneg:packetneg=log_controls(text,v,d)
 assert sums=={'children':24,'direct_exports':7032,'CalcA':2088,'stereo_bytes':8467200} and a['custody_after']==a['custody_before'];assert len({c['pid'] for c in a['children']})==24
 for p,n in zip(a['children'],a['children'][1:]):assert p['utc_end']<=n['utc_start']
 byv={p['transpose_integer']:p for p in joins};catalog=[row if row['historical'] is not None else {**row,'actual':byv[row['transpose_integer']]} for row in d['catalog']];assert [r['transpose_integer'] for r in catalog]==list(range(25)) and sum('actual' in r for r in catalog)==24
 return {'status':'PASS','controls':controls,'actual_protocol_negatives':packetneg,'totals':sums,'complete_catalog':catalog,'all_finite':True,'all_channels_bit_identical':all(c['audio_summary']['channels_bit_identical'] for c in a['children']),'silent_fresh_integers':[c['transpose_integer'] for c in a['children'] if c['audio_summary']['nonzero_samples']==[0,0]],'original_calls_by_checker':0,'external_runtime_reads_by_checker':0,'custody_scope':'Onecommonwholebatchbefore→each24after, not independentchildbefore/continuousprovideridentity'}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 else:
  assert sys.argv[1:] in (['--check'],['--write-report']);out=check()
  if sys.argv[1:]==['--write-report']:assert not (H/'author-check.json').exists();R.save(H/'author-check.json',out)
 print(json.dumps({k:v for k,v in out.items() if k!='complete_catalog'}))
