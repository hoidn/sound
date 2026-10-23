#!/usr/bin/env python3
"""Owned source/input/result metadata seals; never original execution."""
import pathlib,json,hashlib,os,sys
from datetime import datetime,timezone
H=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def inventory():
 return [{'path':p.relative_to(H).as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(H.rglob('*')) if p.is_file()]
if sys.argv[1:]==['--before']:
 assert not (H/'attempts').exists() and not (H/'pre-call-manifest.json').exists()
 files=[]
 for x in inventory():
  p=H/x['path'];files.append({**x,'path':str(p)});p.chmod(0o444)
 d={'schema':'whole-Corpus-native-integer-precall-v1','utc':datetime.now(timezone.utc).isoformat(),'sole_actual_source_peer':'Root','author':'automation_actual_review (Auto)','scope':{'aliases':69,'vectors':63,'fresh_children':57,'inherited_vectors':6,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104},'original_calls_before_freeze':0,'frozen_files':files,'attempt_policy':'Once whole57 sequential; first detected failure stops later children; no retry/oldcontrol replay/resume/extension','all_capture_code_including_parent_launcher_bound':True};save('pre-call-manifest.json',d);(H/'pre-call-manifest.json').chmod(0o444)
elif sys.argv[1:]==['--final']:
 assert not (H/'manifest.json').exists() and json.loads((H/'author-check.json').read_text())['status']=='PASS'
 files=inventory();d={'schema':'whole-Corpus-native-integer-actual-v1','utc':datetime.now(timezone.utc).isoformat(),'author':'automation_actual_review (Auto)','sole_actual_source_peer':'Root','files':files,'payload_count':len(files),'payload_bytes':sum(x['bytes'] for x in files),'scope':{'aliases':69,'vectors':63,'fresh_children':57,'inherited_vectors':6,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104},'precall_sha256':sha((H/'pre-call-manifest.json').read_bytes()),'safe_check':'Read entire new sources first; python3 -I -B check-recorded.py --check','never':'NEVER launch/record --run-once/assemble-inputs/assemble-code, oldhelper/import/build/native/provider/model execution again','status':'FROZEN author observations; sole Root actual/source review pending'};save('manifest.json',d)
 for p in H.rglob('*'):
  if p.is_file():p.chmod(0o444)
else:raise AssertionError('only --before or --final')
p=H/('pre-call-manifest.json' if sys.argv[1:]==['--before'] else 'manifest.json');print(json.dumps({'path':str(p),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes()),'files':len(d.get('files',d.get('frozen_files',[])))}))
