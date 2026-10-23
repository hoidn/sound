#!/usr/bin/env python3
"""Packet-only retained data integrity; imports only this new inert stdlib recorder, never --run."""
import copy,importlib.util,json,pathlib,sys,hashlib
H=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('owned_record',H/'record.py');R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
def check():
 d=json.loads((H/'inputs.json').read_text());R.validate(d);neg=R.controls(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for p in pre['frozen_files']:assert R.ident(p['path'])==p
 a=json.loads((H/'results.json').read_text());assert a['status']=='COMPLETE-ONCE-NO-RETRY' and a['error'] is None and all(a['phases'].values())
 assert [c['velocity'] for c in a['children']]==[p['velocity'] for p in d['plans']]
 totals={'children':0,'direct_exports':0,'CalcA':0,'stereo_bytes':0};joins=[];data_controls=[]
 for c in a['children']:
  assert c['status']=='RECORDED' and c['exit']==0 and not c['timeout'] and c['pid']>0 and c['utc_start']<=c['utc_end']
  assert c['custody_after']==a['custody_before']
  for key in ['stdout','stderr','audio']:assert R.ident(c[key]['path'])==c[key]
  text=pathlib.Path(c['stdout']['path']).read_text();err=pathlib.Path(c['stderr']['path']).read_text()
  assert R.parse(text,err,c['exit'],c['velocity'],d)==c['parsed']
  assert R.audio(c['audio']['path'])==c['audio_summary'] and c['audio_summary']['all_finite']
  totals['children']+=1;totals['direct_exports']+=c['parsed']['direct_export_calls'];totals['CalcA']+=c['parsed']['CalcA'];totals['stereo_bytes']+=c['audio_summary']['bytes']
  joins.append({'velocity':c['velocity'],'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'results.json#/children/{len(joins)}','audio':c['audio'],'summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_comparator':None})
  if len(data_controls)==0:
   changes=[('exit-nonzero',text,'',2),('stderr',text,'unexpected',0),('trap',text+'\nTRAP test','',0),('wrong-on-velocity',text.replace(f'event 4096 0x90 60 {c["velocity"]}',f'event 4096 0x90 60 {(c["velocity"]+1)%128}'),'',0),('wrong-off-key',text.replace('event 26146 0x80 60 0','event 26146 0x80 61 0'),'',0),('wrong-rate-argument',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('rate-not-integer',text.replace('rate 44100 ret='+str(c['parsed']['Rate_return_opaque_integer']),'rate 44100 ret=unknown'),'',0),('create-null',text.replace('create ok','create NULL'),'',0),('wrong-blockcount',text.replace('blocks=87','blocks=86'),'',0),('CalcA-failure',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('wrong-input',text.replace('input zero','input signal'),'',0),('failbits',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('missing-param',text.replace('param 0 3\n',''),'',0),('wrong-param-bits',text.replace('param 0 3\n','param 0 2\n'),'',0),('omit-destroy',text.replace('destroy\n',''),'',0),('duplicate-export',text+'\nexport _CalcA 0x1','',0)]
   for name,t,e,rc in changes:
    try:R.parse(t,e,rc,c['velocity'],d)
    except (AssertionError,KeyError,IndexError,ValueError):data_controls.append(name)
    else:raise AssertionError('accepted '+name)
 assert totals=={'children':125,'direct_exports':27375,'CalcA':10875,'stereo_bytes':44100000}
 assert a['custody_after']==a['custody_before']
 byv={x['velocity']:x for x in joins};catalog=[]
 for row in d['catalog']:
  if row['historical'] is not None:catalog.append(row)
  else:catalog.append({**row,'actual':byv[row['velocity']]})
 assert [r['velocity'] for r in catalog]==list(range(128)) and sum('actual' in r for r in catalog)==125
 return {'status':'PASS','input_negative_controls':neg,'packet_negative_controls':data_controls,'totals':totals,'complete_catalog':catalog,'all_finite':True,'all_channels_bit_identical':all(c['audio_summary']['channels_bit_identical'] for c in a['children']),'all_silent_fresh_velocities':[c['velocity'] for c in a['children'] if c['audio_summary']['nonzero_samples']==[0,0]],'original_calls_by_checker':0,'external_runtime_reads_by_checker':0,'custody_scope':'Recorded endpoint arrays and packet-ownedbytes only; no live dependency/continuous custody proof.'}
if __name__=='__main__':
 assert sys.argv[1:] in (['--check'],['--write-report'])
 out=check()
 if sys.argv[1:]==['--write-report']:
  assert not (H/'author-check.json').exists();R.save(H/'author-check.json',out)
 print(json.dumps({k:v for k,v in out.items() if k!='complete_catalog'}))
