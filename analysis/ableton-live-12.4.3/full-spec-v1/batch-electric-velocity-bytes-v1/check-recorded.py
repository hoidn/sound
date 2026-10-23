#!/usr/bin/env python3
"""New packet-only checker; safe synthetic/input controls, no subprocess/runtime/helper calls."""
import importlib.util,json,pathlib,sys,struct,tempfile
H=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('owned_record',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={'_CreateInstanceU':'0xc030','_DestroyInstanceU':'0xc0b0','_SetSampleRateU':'0xc120','_GetPlugInfoU':'0xc190','_CalcA':'0xc240','_SetParameterA':'0xc550','_ResetA':'0xc5d0'}
def synthetic(d,rate=1):
 lines=['slice offset=16384 size=267648']+[f'import linux synthetic_{i} slots=1' for i in range(133)]+[f'export {k} {v}' for k,v in EXPORTS.items()]+['create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {float(w["token"]):.9g}' for w in d['words']]+['event 11264 0x90 60 0','event 33314 0x80 60 0','inflag 0','input zero','process 11264 512 flags: 22x(ret=0,flag=1) blocks=22','process 44100 512 flags: 87x(ret=0,flag=1) blocks=87','destroy','used synthetic_0 1','cxx-failbits 0']
 return '\n'.join(lines)+'\n'
def log_controls(text,key,d):
 oldon=f'event 11264 0x90 60 {key}';oldoff='event 33314 0x80 60 0'
 tests=[('exit',text,'',2),('stderr',text,'unexpected',0),('trap',text+'\nTRAP symbol','',0),('on-velocity',text.replace(oldon,f'event 11264 0x90 60 {(key+1)%128}'),'',0),('on-key',text.replace(oldon,f'event 11264 0x90 61 {key}'),'',0),('off-key',text.replace(oldoff,'event 33314 0x80 61 0'),'',0),('off-velocity',text.replace(oldoff,'event 33314 0x80 60 1'),'',0),('rate-argument',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('create-null',text.replace('create ok','create NULL'),'',0),('warmup-blockcount',text.replace('blocks=22','blocks=21'),'',0),('render-blockcount',text.replace('blocks=87','blocks=86'),'',0),('CalcA-failure',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('input',text.replace('input zero','input signal'),'',0),('input-flag',text.replace('inflag 0','inflag 1'),'',0),('failbits',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('omit-param',text.replace('param 0 30\n',''),'',0),('param-bits',text.replace('param 0 30\n','param 0 29\n'),'',0),('destroy',text.replace('destroy\n',''),'',0),('duplicate-export',text+'\nexport _CalcA 0xc240','',0),('initializer',text+'\ninit 0x1','',0),('wrong-export',text.replace('export _CalcA 0xc240','export _CalcA 0xc241'),'',0)];out=[]
 for name,t,e,rc in tests:
  try:R.parse(t,e,rc,key,d)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out
def selfcheck(d):
 R.validate(d);inputs=R.controls(d);positives=[]
 for rate in [-7,0,1]:
  parsed=R.parse(synthetic(d,rate),'',0,0,d);assert parsed['Rate_return_opaque_integer']==rate;positives.append(rate)
 negatives=log_controls(synthetic(d),0,d);audio=[]
 with tempfile.TemporaryDirectory(prefix='electric-owned-data-') as t:
  p=pathlib.Path(t)/'synthetic.f32';raw=bytearray(442912);p.write_bytes(raw);a=R.audio(p);assert a['all_finite'] and a['warmup_numeric_zero'];audio.append('all-positive-zero-valid')
  struct.pack_into('<f',raw,0,1);p.write_bytes(raw);a=R.audio(p);assert a['all_finite'] and not a['warmup_numeric_zero'];audio.append('warmup-nonzero-detected')
  struct.pack_into('<f',raw,0,0);struct.pack_into('<I',raw,90112,0x7fc00000);p.write_bytes(raw);assert not R.audio(p)['all_finite'];audio.append('render-qNaN-detected-not-normalized')
  p.write_bytes(bytes(442911))
  try:R.audio(p)
  except AssertionError:audio.append('short-output-rejected')
  else:raise AssertionError('short output accepted')
 return {'input_negatives':inputs,'synthetic_protocol_negatives':negatives,'opaque_Rate_positive_integers':positives,'synthetic_audio_controls':audio,'original_calls':0,'runtime_reads':0}
def check():
 d=json.loads((H/'inputs.json').read_text());controls=selfcheck(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for p in pre['frozen_files']:assert R.ident(p['path'])==p
 outer=json.loads((H/'outer-receipt.json').read_text());assert outer['exit']==0 and outer['interrupted'] is None and outer['retry'] is False and outer['precall_sha256']==outer['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY' and a['error'] is None and all(a['phases'].values())
 assert [c['velocity_byte'] for c in a['children']]==[p['velocity_byte'] for p in d['plans']]
 totals={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};joins=[];packet_controls=[]
 for c in a['children']:
  assert c['status']=='RECORDED' and c['exit']==0 and not c['timeout'] and c['pid']>0 and c['utc_start']<=c['utc_end']
  assert c['custody_after']==a['custody_before']
  for name in ['stdout','stderr','audio']:assert R.ident(c[name]['path'])==c[name]
  text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text();assert R.parse(text,err,c['exit'],c['velocity_byte'],d)==c['parsed'];assert R.audio(c['audio']['path'])==c['audio_summary']
  assert c['audio_summary']['all_finite'] and c['audio_summary']['warmup_numeric_zero']
  totals['children']+=1;totals['direct_exports']+=c['parsed']['direct_export_calls'];totals['CalcA']+=c['parsed']['CalcA'];totals['stereo_bytes']+=c['audio_summary']['bytes']
  joins.append({'velocity_byte':c['velocity_byte'],'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'results.json#/children/{len(joins)}','audio':c['audio'],'summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
  if not packet_controls:packet_controls=log_controls(text,c['velocity_byte'],d)
 assert totals=={'children':127,'direct_exports':18415,'CalcA':13843,'stereo_bytes':56249824} and a['custody_after']==a['custody_before']
 assert len({c['pid'] for c in a['children']})==127
 for prev,nxt in zip(a['children'],a['children'][1:]):assert prev['utc_end']<=nxt['utc_start']
 bykey={x['velocity_byte']:x for x in joins};catalog=[row if row['historical'] is not None else {**row,'actual':bykey[row['velocity_byte']]} for row in d['catalog']]
 assert [r['velocity_byte'] for r in catalog]==list(range(128)) and sum('actual' in r for r in catalog)==127
 return {'status':'PASS','controls':controls,'actual_protocol_negatives':packet_controls,'totals':totals,'complete_catalog':catalog,'all_finite':True,'all_channels_bit_identical':all(c['audio_summary']['channels_bit_identical'] for c in a['children']),'all_warmup_numeric_zero':True,'silent_fresh_velocities':[c['velocity_byte'] for c in a['children'] if c['audio_summary']['render_nonzero_samples']==[0,0]],'original_calls_by_checker':0,'external_runtime_reads_by_checker':0,'custody_scope':'Recorded endpoint arrays/ownedbytes only; no liveprovider/continuous custody proof.'}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 else:
  assert sys.argv[1:] in (['--check'],['--write-report']);out=check()
  if sys.argv[1:]==['--write-report']:assert not (H/'author-check.json').exists();R.save(H/'author-check.json',out)
 print(json.dumps({k:v for k,v in out.items() if k!='complete_catalog'}))
