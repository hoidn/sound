#!/usr/bin/env python3
"""EXPLICIT POST-CAPTURE metadata readback only; not pre-call code or original execution."""
import pathlib,json,hashlib,os
H=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
d=json.loads((H/'inputs.json').read_bytes());a=json.loads((H/'results.json').read_bytes());o=json.loads((H/'outer-receipt.json').read_bytes());pre=(H/'pre-call-manifest.json').read_bytes()
assert a['status']=='STOPPED-NO-RETRY'and a['error']['type']=='AssertionError'and o['exit']==1 and not o['retry']
assert sha(pre)==o['precall_sha256']==o['precall_sha256_after']
by={c['id']:c for c in a['children']};catalog=[]
for z in d['histories']:
 c=by.get(z['id']);item={'id':z['id'],'index':z['changed_index'],'value':z['value'],'history_sha256':z['history_sha256'],'vector_sha256':z['vector_sha256'],'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
 if z['historical_input']is not None:item.update(disposition='HISTORICAL-INPUT-ONLY-NOT-APPROVED-ACTUAL',pid=None,new_receipt=None,new_metrics=None)
 elif c is None:item.update(disposition='NEVER-LAUNCHED',pid=None,new_receipt=None,new_metrics=None)
 else:
  item.update(disposition='COLLECTOR-RECORDED-PENDING-SOLE-PEER'if c['status']=='RECORDED'else'ATTEMPTED-EXIT0-GUARD-REJECTED-RETAINED-UNCLASSIFIED',pid=c['pid'],exit=c['exit'],timeout=c['timeout'],retained_status_label=c['status'],receipt_pointer='/children/'+str(a['children'].index(c)),retained_stdout=c.get('stdout'),retained_stderr=c.get('stderr'),retained_audio=c.get('audio'),native_return_flag_interpretation=None)
 catalog.append(item)
counts={k:sum(x['disposition']==k for x in catalog)for k in sorted({x['disposition']for x in catalog})}
assert counts=={'HISTORICAL-INPUT-ONLY-NOT-APPROVED-ACTUAL':1,'NEVER-LAUNCHED':69,'COLLECTOR-RECORDED-PENDING-SOLE-PEER':15,'ATTEMPTED-EXIT0-GUARD-REJECTED-RETAINED-UNCLASSIFIED':1}
assert len(catalog)==86 and len(d['aliases'])==105 and len({c['pid']for c in a['children']})==16 and all(c['exit']==0 and not c['timeout']and c['stderr']['bytes']==0 and c['audio']['bytes']==442912 for c in a['children'])
out={'status':'PARTIAL-ONCE-STOPPED-NO-RETRY','scope':'Postcapture JSONmetadata only, NOT independentactual/source/raw/audio review','not_pre_call_source':True,'precall_sha256':sha(pre),'attempted_children':16,'collector_recorded_children':15,'guard_rejected_retained_child':'i058-v01','never_launched_children':69,'stereo_bytes_retained':sum(c['audio']['bytes']for c in a['children']),'selected_direct_call_budget_attempted_scripts':16*251,'selected_CalcA_budget_attempted_scripts':16*109,'native_call_count_qualification':'These are script-derived direct budgets for16exit0 children, not independentallcommand proof for rejectedchild; nested/initializers unknown.','recorded_success_direct_exports':15*251,'recorded_success_CalcA':15*109,'parent_exit':o['exit'],'recorder_error':a['error'],'phases':a['phases'],'failure_custody_recorded_equal':a['custody_after_failure']==a['custody_before'],'preserved_guard':'Frozen record.py91 requiresret0/flag0or1.16thchildguardrejected; literalreturns/flags remainSOLEpeerclassification, not silently repaired or fitted.','stale_running_label':'LastchildstatusRUNNING retained verbatim because postwaitparserfailed before RECORDED assignment. Its recorded exit0/end/byteidentities distinguish this from a livechild.','catalog':catalog,'aliases':d['aliases'],'capture_retries':0,'additional_original_calls':0,'raw_audio_log_or_runtime_bytes_opened_by_this_readback':0}
p=H/'partial-readback.json';assert not p.exists()
with p.open('x')as f:json.dump(out,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps({k:v for k,v in out.items()if k not in['catalog','aliases']}))
