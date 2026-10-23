"""Owned packet serialization only; never imports collector or reads runtime files."""
from pathlib import Path
import sys,json,hashlib,datetime
P=Path(__file__).resolve().parent
assert sys.argv[1:]in(['--pre-call'],['--final'])
name='pre-call-manifest.json'if sys.argv[1:] ==['--pre-call']else'manifest.json'
assert not(P/name).exists()
if name=='pre-call-manifest.json':assert not(P/'attempts').exists()
else:assert(P/'author-check.json').exists()and(P/'assessment.json').exists()
rows=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  b=p.read_bytes();rows.append({'path':str(p.relative_to(P)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
d={'schema':'corpus-dco032-residual-midi-axes-'+('precall'if name.startswith('pre-')else'actual')+'-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Whole160aliases158histories157oncefresh+oneDCO032inherited-no-replay','payload_count':len(rows),'payload_bytes':sum(x['bytes']for x in rows),'payloads':rows,'actual_peer':'Root sole independent actual/source reviewer; author is automation_actual_review','new_waveform_priors':None,'portable_criteria':None,'safe_check':'Read complete new sources before packet-only check_data.py --check; NEVER launch/capture/assembler/freeze as check.'}
p=P/name;p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
for f in P.rglob('*'):
 if f.is_file():f.chmod(0o444)
b=p.read_bytes();print(json.dumps({'manifest':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'payload_count':len(rows),'payload_bytes':d['payload_bytes']},indent=2))
