#!/usr/bin/env python3
"""Owned metadata seals only. No subprocess, original, image/tool/provider read or code import."""
import json,pathlib,hashlib,os,sys
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,d):
 with (H/name).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def inventory():
 out=[]
 for p in sorted(H.rglob('*')):
  if p.is_file():
   b=p.read_bytes();out.append({'path':p.relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b)})
 return out
if sys.argv[1:]==['--before']:
 assert not (H/'pre-call-manifest.json').exists() and not (H/'attempts').exists()
 files=[]
 for x in inventory():
  p=H/x['path'];files.append({**x,'path':str(p)});p.chmod(0o444)
 d={'schema':'standing-whole-class-precall-freeze-v1','frozen_utc':datetime.now(timezone.utc).isoformat(),'sole_actual_source_peer':'automation_actual_review (Auto)','Root_role':'Citation-only, no new source/code/raw/results review','original_calls_before_freeze':0,'frozen_files':files,'scope':{'domains':20,'alias_points':105,'unique_histories':86,'historical_input_only':1,'fresh_children':85,'direct_exports':21335,'CalcA':9265,'stereo_bytes':37647520},'attempt_policy':'Exclusive attempts/outerreceipt/logs; no retry/reuse/resume. ALLnewcode including parentlauncher is file-bound before calls.'};save('pre-call-manifest.json',d);(H/'pre-call-manifest.json').chmod(0o444)
elif sys.argv[1:]==['--final']:
 assert not (H/'manifest.json').exists();a=json.loads((H/'author-check.json').read_text());assert a['status']=='PASS'
 files=inventory();d={'schema':'standing-whole-class-actual-batch-v1','packet':H.name,'sealed_utc':datetime.now(timezone.utc).isoformat(),'sole_actual_source_peer':'automation_actual_review (Auto)','Root_role':'Citation-only adoption, no duplicate newactual/source/code/raw/results review','files':files,'payload_count':len(files),'payload_bytes':sum(x['bytes'] for x in files),'universe':{'domains':20,'alias_points':105,'unique_histories':86,'historical_input_only_no_approved_actual':1,'fresh_children':85,'direct_exports':21335,'CalcA':9265,'stereo_bytes':37647520},'precall_sha256':sha((H/'pre-call-manifest.json').read_bytes()),'historical_baseline':'RetainedinputONLY/notapprovedactual; no replay/newPID/receipt/metrics', 'review_entry':['README.md','record.py','launch-once.py','check-recorded.py','assemble.py','context.json','inputs.json','assessment.json','results.json','author-check.json','eligibility-context.json'],'safe_check':'SOLEPEERONLYafterfullsourceread: /usr/bin/python3 -I -B check-recorded.py --check. Authoronly--author-bookkeeping, no actualraw reopen.','original_reexecution':'Forbidden; NEVER launch-once/--run-once/assemble/oldhelper/build again'};save('manifest.json',d)
 for p in H.rglob('*'):
  if p.is_file():p.chmod(0o444)
else:raise AssertionError('only --before or --final')
p=H/('manifest.json' if sys.argv[1:] == ['--final'] else 'pre-call-manifest.json');b=p.read_bytes();print(json.dumps({'path':str(p),'bytes':len(b),'sha256':sha(b),'files':len(d.get('files',d.get('frozen_files',[])))}))
