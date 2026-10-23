#!/usr/bin/env python3
"""Synthetic/input/recording bookkeeping; sole peer --check reopens retained actuals only."""
import importlib.util,json,pathlib,sys,tempfile,struct
H=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('owned_recorder',H/'record.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
EXPORTS={k:hex(0x1000+i*4)for i,k in enumerate(['_CreateInstanceU','_DestroyInstanceU','_SetSampleRateU','_GetPlugInfoU','_CalcA','_SetParameterA','_ResetA'])}
def synthetic(d,p,rate=1):
 imports=[f'import {kind} synthetic_{i} slots=1'for i,kind in enumerate(['linux']*96+['data']*7+['trap']*26)]
 return '\n'.join(['slice offset=16384 size=367488']+imports+[f'export {k} {v}'for k,v in EXPORTS.items()]+['create ok',f'rate 44100 ret={rate}']+[f'param {w["index"]} {float(w["token"]):.9g}'for w in R.variant(d,p)]+['inflag 0','input zero','process 11264 512 flags: 22x(ret=0,flag=0) blocks=22','event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512 flags: 87x(ret=0,flag=1) blocks=87','destroy','used synthetic_0 1','cxx-failbits 0'])+'\n'
def logcontrols(text,p,d):
 param='param '+str(p['index'])+' '+format(float(p['value']),'.9g')+'\n';assert param in text
 tests=[('exit',text,'',2),('stderr',text,'err',0),('trap',text+'TRAP x\n','',0),('fault',text+'FAULT x\n','',0),('bad-on-frame',text.replace('event 4096 ','event 4097 '),'',0),('bad-off-frame',text.replace('event 26146 ','event 7168 '),'',0),('bad-offkey',text.replace('0x80 60 0','0x80 61 0'),'',0),('bad-onstatus',text.replace('0x90 60 100','0x91 60 100'),'',0),('wrong-param',text.replace(param,'param '+str(p['index'])+' 999\n'),'',0),('Ratearg',text.replace('rate 44100 ret=','rate 48000 ret='),'',0),('createNULL',text.replace('create ok','create NULL'),'',0),('bad-warm',text.replace('process 11264 512','process 11263 512'),'',0),('bad-blockcount',text.replace('blocks=87','blocks=86'),'',0),('CalcAret',text.replace('ret=0,flag=','ret=-1,flag='),'',0),('ret1-stays-guardFAIL',text.replace('ret=0,flag=','ret=1,flag='),'',0),('CalcAflag',text.replace('flag=1','flag=2'),'',0),('input',text.replace('input zero','input signal'),'',0),('inflag',text.replace('inflag 0','inflag 1'),'',0),('destroy',text.replace('destroy\n',''),'',0),('CXXfail',text.replace('cxx-failbits 0','cxx-failbits 1'),'',0),('import-count',text.replace('import trap ','import linux ',1),'',0),('duplicateexport',text+'export _CalcA 0x1010\n','',0),('extra-command',text+'reset\n','',0)];out=[]
 for name,t,e,rc in tests:
  assert(t,e,rc)!=(text,'',0),'no-op '+name
  try:R.parse(t,e,rc,p,d)
  except(AssertionError,IndexError,KeyError,ValueError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out

def selfcheck(d):
 R.validate(d);neg=R.controls(d);positive=[]
 for p in[d['plans'][0],next(p for p in d['plans']if p['index']==59 and p['value']==5),d['plans'][-1]]:
  for rate in[-7,0,1]:assert R.parse(synthetic(d,p,rate),'',0,p,d)['Rate_return_opaque_integer']==rate;positive.append([p['id'],rate])
 logs=logcontrols(synthetic(d,d['plans'][0]),d['plans'][0],d);audio=[]
 with tempfile.TemporaryDirectory(prefix='collision-kind3-synthetic-')as t:
  p=pathlib.Path(t)/'audio';b=bytearray(442912);p.write_bytes(b);a=R.audio(p);assert a['all_finite']and a['render_nonzero_samples']==[0,0];audio.append('silence-valid')
  struct.pack_into('<I',b,90112,0x80000000);p.write_bytes(b);assert R.audio(p)['render_negative_zero_samples']==[1,0];audio.append('signedzero-preserved')
  struct.pack_into('<f',b,0,1.0);p.write_bytes(b);a=R.audio(p);assert a['all_finite']and not a['warmup_numeric_zero'];audio.append('nonzero-warmup-recorded-not-failure')
  struct.pack_into('<I',b,90112,0x7fc00000);p.write_bytes(b);assert not R.audio(p)['all_finite'];audio.append('qNaN-detected')
  struct.pack_into('<I',b,90112,0x7f800000);p.write_bytes(b);assert not R.audio(p)['all_finite'];audio.append('Infinity-detected')
  p.write_bytes(bytes(442911))
  try:R.audio(p)
  except AssertionError:audio.append('short-rejected')
  else:raise AssertionError('shortaccepted')
 return {'status':'PASS','input_negatives':neg,'synthetic_protocol_negatives':logs,'opaqueRate_boundaries':positive,'synthetic_audio_controls':audio,'original_calls':0,'actual_raw_reads':0,'runtime_reads':0}

def recorded(peer=False):
 d=json.loads((H/'inputs.json').read_text());R.validate(d);pre=json.loads((H/'pre-call-manifest.json').read_text())
 for x in pre['frozen_files']:assert R.ident(x['path'])==x
 o=json.loads((H/'outer-receipt.json').read_text());a=json.loads((H/'results.json').read_text());complete=a['status']=='COMPLETE-ONCE-NO-RETRY'
 assert not o['retry']and o['precall_sha256']==o['precall_sha256_after']==R.sha((H/'pre-call-manifest.json').read_bytes())
 assert[c['id']for c in a['children']]==[p['id']for p in d['plans'][:len(a['children'])]]and len(a['children'])<=69
 if complete:assert o['exit']==0 and o['interrupted']is None and a['error']is None and all(a['phases'].values())and len(a['children'])==69
 totals={'children_attempted':len(a['children']),'children_recorded':0,'direct_exports_recorded':0,'CalcA_recorded':0,'stereo_bytes_retained':0};actual=[];pneg=[]
 for c,p in zip(a['children'],d['plans']):
  assert(c['id'],c['index'],c['value'])==(p['id'],p['index'],p['value'])
  if peer:
   for k in['stdout','stderr','audio']:
    if k in c:assert R.ident(c[k]['path'])==c[k]
  totals['stereo_bytes_retained']+=c.get('audio',{}).get('bytes',0)
  if c['status']=='RECORDED':
   assert c['exit']==0 and not c['timeout']and c['pid']>0 and c['custody_after']==a['custody_before']and c['stderr']['bytes']==0 and c['audio']['bytes']==442912 and c['audio_summary']['all_finite']
   assert c['parsed']['direct_export_calls']==251 and c['parsed']['CalcA']==109
   if peer:
    txt=pathlib.Path(c['stdout']['path']).read_text();assert R.parse(txt,pathlib.Path(c['stderr']['path']).read_text(),c['exit'],p,d)==c['parsed']and R.audio(c['audio']['path'])==c['audio_summary']
    if not pneg:pneg=logcontrols(txt,p,d)
   totals['children_recorded']+=1;totals['direct_exports_recorded']+=251;totals['CalcA_recorded']+=109
   actual.append({'id':p['id'],'index':p['index'],'value':p['value'],'vector_sha256':p['vector_sha256'],'history_sha256':p['history_sha256'],'provenance':'fresh-once','pid':c['pid'],'utc_start':c['utc_start'],'utc_end':c['utc_end'],'receipt_pointer':f'/children/{len(actual)}','audio':c['audio'],'recorded_collector_output_summary':c['audio_summary'],'Rate_return_opaque_integer':c['parsed']['Rate_return_opaque_integer'],'CalcA_groups':c['parsed']['CalcA_groups'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
  elif complete:raise AssertionError('completed but unrecorded')
 if complete:
  assert totals=={'children_attempted':69,'children_recorded':69,'direct_exports_recorded':17319,'CalcA_recorded':7521,'stereo_bytes_retained':30560928}and a['custody_after']==a['custody_before']and len({c['pid']for c in a['children']})==69
 for c,n in zip(a['children'],a['children'][1:]):assert c['utc_end']<=n['utc_start']
 by={x['vector_sha256']:x for x in actual};catalog=[]
 for z in d['histories']:
  if z['local_disposition']!='SELECTED-NEVER-PREVIOUSLY-LAUNCHED':catalog.append(z)
  elif z['vector_sha256']in by:catalog.append({**z,'actual':by[z['vector_sha256']]})
  else:catalog.append({**z,'disposition':'attempted-incomplete-or-unlaunched','actual':None})
 return {'status':'PASS','batch_status':a['status'],'scope':'Solepeer retainedactual verification'if peer else'Author bookkeeping of collector records ONLY, not independent actualreview','actual_raw_reopened_by_this_check':peer,'totals':totals,'complete_catalog':catalog,'complete_aliases':d['aliases'],'actual_protocol_negative_controls':pneg,'custody_scope':'One common wholebatchbefore→eachafter, notperchildbefore/continuousproviderproof','prior_dispositions':'15approved+1guardFAIL+baselineinputONLY inheritedbysolepartialreview, none replayed; no semanticreinterpretation','original_calls_by_this_check':0,'runtime_reads_by_this_check':0}
if __name__=='__main__':
 if sys.argv[1:]==['--self-check']:out=selfcheck(json.loads((H/'inputs.json').read_text()))
 elif sys.argv[1:]==['--author-bookkeeping']:out=recorded(False);assert not(H/'author-check.json').exists();R.save(H/'author-check.json',out)
 else:assert sys.argv[1:]==['--check'];out=recorded(True)
 print(json.dumps({k:v for k,v in out.items()if k not in['complete_catalog','complete_aliases']}))
