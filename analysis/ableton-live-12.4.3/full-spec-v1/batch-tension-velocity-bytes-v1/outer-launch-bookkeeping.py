# Additive exact transcription of the inline launch code supplied in the tool call.
# This file was retained AFTER capture, NOT a pre-call-manifest member. Never rerun.
import pathlib,subprocess,json,os,time,hashlib
from datetime import datetime,timezone
h=pathlib.Path('analysis/ableton-live-12.4.3/full-spec-v1/batch-tension-velocity-bytes-v1').resolve();now=lambda:datetime.now(timezone.utc).isoformat();save=lambda d:(h/'outer-receipt.json').write_text(json.dumps(d,indent=2)+'\n')
assert not (h/'attempts').exists() and not (h/'outer.stdout').exists()
argv=[os.path.realpath('/home/ollie/miniconda3/bin/python3'),'-I','-B',str(h/'record.py'),'--run-once','836d76edb0b1ba3921944eeefc0de068c86ad63c08093736229c6bc9de4376c1'];env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'}
d={'argv':argv,'environment':env,'utc_start':now(),'pid':None,'exit':None,'retry':False,'original_child_policy':'record.py125sequential children/20sCPUwall/no retry; stop later children on detection'};save(d)
with (h/'outer.stdout').open('xb') as out,(h/'outer.stderr').open('xb') as err:
 p=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=env,start_new_session=True);d['pid']=p.pid;save(d);d['exit']=p.wait()
d['utc_end']=now();save(d);print(json.dumps(d))
