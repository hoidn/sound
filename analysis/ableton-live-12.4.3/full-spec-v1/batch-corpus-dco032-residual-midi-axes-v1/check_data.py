"""Owned retained-packet-only checker: no original/runtime/provider acquisitions."""
from pathlib import Path
import argparse,copy,hashlib,json,runpy
P=Path(__file__).resolve().parent
D=runpy.run_path(str(P/'data.py'),run_name='owned_data_only_check')
def load(n):return json.loads((P/n).read_text())
def need(v,label):
 if not v:raise AssertionError(label)
def local(item):
 p=Path(item['path']);p=p if p.is_absolute() else P/p
 need(p.resolve().is_relative_to(P),'packet-only read')
 raw=p.read_bytes();need(len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],'local identity');return raw

def validate_receipt(r,row,c):
 need(r['id']==row['id'] and r['unique_vector']==row['unique_vector'] and r['fresh_ordinal']==row['fresh_ordinal'],'catalog join')
 need(r['exit']==0 and r['timeout'] is False and r['error'] is None and r.get('custody_error') is None and r['attempts']==1,'one success')
 need(type(r['pid']) is int and r['pid']>0 and r['child_environment']==c['environment'],'PID/env')
 need(r['argv']==[c['executable']['path'],c['bundle_slice_expected']['path'],row['script']['path'],str(P/'attempts'/row['id']/'output.f32'),'--imports'],'argv')
 need(r['resource_admission']['packet_bytes']<=c['resource_policy']['packet_stop_before_next_child_bytes'] and r['resource_admission']['free_bytes']>=c['resource_policy']['minimum_free_before_next_child_bytes'],'resource admission')
 need(r['custody_before']==r['custody_after'] and len(r['custody_before'])==16,'perchild custody')
 need(r['custody_before'][:8]==c['runtime_expected'],'recorded runtime identities')
 need(all(r[k] is None for k in ['waveform_prediction','portable_expected','portable_comparator','candidate_grade']),'NULL')
 out=local(r['output']);need(len(out)==131072,'shape')
 need(local(r['stderr'])==b'','stderr');log=local(r['stdout']).decode();prot=D['protocol'](log,row,c)
 need(prot==r['protocol'],'protocol exact');need(r['observed_output']==D['metrics'](out) and r['observed_output']['all_finite'],'unsigned bothchannel summary')
 return prot

def check():
 c=load('inputs.json');controls=D['selfchecks'](c);pre=load('pre-call-manifest.json')
 for it in pre['payloads']:local(it)
 need(any(x['path']=='launch.py' for x in pre['payloads']) and any(x['path']=='assemble-inputs.py' for x in pre['payloads']),'all newcode prebound')
 receipts=[json.loads(line) for line in (P/'results.jsonl').read_text().splitlines()];summary=load('execution-summary.json');context=load('execution-context.json');launch=load('launch-receipt.json');fresh=[x for x in c['rows'] if x['disposition']=='fresh-planned']
 need(summary['attempted_children']==len(receipts) and len(receipts)<=157,'bounded attempts')
 need(summary['source_before']==summary['source_after']==c['source_pins'],'recorded whole source custody')
 need(context['source_before']==summary['source_before'],'context custody')
 need(launch['pid']==context['outer_pid']==summary['outer_pid'] and launch['exec_argv']==c['parent_exec_argv'] and launch['exec_environment']==c['environment'],'parent exec bridge')
 raw=(P/'pre-call-manifest.json').read_bytes();need(launch['pre_call_manifest']=={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()},'precall receipt')
 D['parent_valid'](launch,c,context['outer_pid'],{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
 pids=[];valid=0;points=[]
 for i,row in enumerate(c['rows']):
  if row['disposition']=='inherited-no-replay':
   points.append({'id':row['id'],'provenance':'inherited-no-replay','history_sha256':row['history_sha256'],'events':row['events'],'first_alias':row['first_alias'],'historical':row['historical'],'fresh_pid':None,'fresh_receipt':None,'new_metrics':None,'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None});continue
  index=row['fresh_ordinal']-1
  if index>=len(receipts):points.append({'id':row['id'],'provenance':'unattempted-first-fault-stop','history_sha256':row['history_sha256'],'events':row['events'],'first_alias':row['first_alias'],'fresh_pid':None});continue
  r=receipts[index]
  if r['error'] is not None:
   need(index==len(receipts)-1 and summary['error'] is not None,'stop afterfirstfailure');points.append({'id':row['id'],'provenance':'failed-once-retained','receipt':r});continue
  validate_receipt(r,row,c);pids.append(r['pid']);valid+=1
  points.append({'id':row['id'],'provenance':'fresh-once-only','history_sha256':row['history_sha256'],'events':row['events'],'first_alias':row['first_alias'],'script':row['script'],'pid':r['pid'],'receipt_pointer':f'results.jsonl#line{index+1}','output':r['output'],'observed_unsigned_summary':r['observed_output'],'protocol':r['protocol'],'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
 need(len(pids)==len(set(pids)) and valid==summary['successful_protocols'],'distinctchildren')
 need(summary['selected_export_calls_with_valid_protocol']==73*valid and summary['CalcA_with_valid_protocol']==32*valid and summary['loader_initializer_entries_logged_separately']==0,'separatecallcounts')
 if summary['error'] is None:need(valid==157 and len(receipts)==157 and summary['status']=='COMPLETE-157-ONCE','completeclass')
 else:need(summary['status']=='STOPPED-NO-RETRY','partial retained')
 neg=[]
 if valid:
  row=fresh[0];r=receipts[0]
  for name,mut in [('missingPID',lambda x:x.update(pid=None)),('wronghistoryjoin',lambda x:x.update(id='CGR-U060')),('retry',lambda x:x.update(attempts=2)),('timeout',lambda x:x.update(timeout=True)),('inventprior',lambda x:x.update(waveform_prediction='fit')),('portablegrade',lambda x:x.update(candidate_grade='PASS')),('wrongenv',lambda x:x['child_environment'].update(XDEV_LIBM_ULP='1')),('wrongscript',lambda x:x['argv'].__setitem__(2,fresh[1]['script']['path'])),('changedcustody',lambda x:x['custody_after'][0].update(sha256='0'*64)),('wrongmetric',lambda x:x['observed_output'].update(frames=1)),('droppedusedimports',lambda x:x['protocol']['actual_used_code_import_counts'].clear()),('wrongrawpin',lambda x:x['output'].update(sha256='0'*64))]:
   bad=copy.deepcopy(r);mut(bad);need(bad!=r,'meaningful '+name)
   try:validate_receipt(bad,row,c)
   except (AssertionError,KeyError,IndexError):neg.append(name)
   else:raise AssertionError('accepted '+name)
 parentneg=[]
 for name,mut in [('wrongPID',lambda x:x.update(pid=0)),('wrongargv',lambda x:x['exec_argv'].append('--retry')),('wrongenvironment',lambda x:x['exec_environment'].update(XDEV_TIME='1')),('wrongprecall',lambda x:x['pre_call_manifest'].update(sha256='0'*64))]:
  bad=copy.deepcopy(launch);mut(bad);need(bad!=launch,name);need(not(bad['pid']==context['outer_pid'] and bad['exec_argv']==c['parent_exec_argv'] and bad['exec_environment']==c['environment'] and bad['pre_call_manifest']==launch['pre_call_manifest']),name);parentneg.append(name)
 if (P/'manifest.json').exists():
  final=load('manifest.json');need({str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}=={'manifest.json'}|{x['path'] for x in final['payloads']},'final exacttree')
  for it in final['payloads']:local(it)
 return {'status':'PASS retained data' if summary['error'] is None else 'RETAINED-PARTIAL-STOPPED','logical_aliases':160,'whole_histories':158,'fresh_valid':valid,'inherited':1,'dedup':'DCO032whole2eventhistory;160aliases158histories157fresh1inputref','controls':controls,'retained_negatives':neg,'parent_negatives':parentneg,'selected_direct_exports':valid*73,'CalcA':valid*32,'initializer_entries_separate':0,'all_native_calls':None,'fresh_stereo_bytes':valid*131072,'whole_source_pairs':len(c['source_pins']),'perchild_pairs':valid*16,'complete_catalog':points,'aliases':c['aliases'],'original_calls_by_checker':0,'external_runtime_reads_by_checker':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',required=True,action='store_true');p.parse_args();print(json.dumps(check(),indent=2))
