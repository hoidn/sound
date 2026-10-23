#!/usr/bin/env python3
"""Exact five selected retained C1 ranges; no census, alias pass or callee follow."""
from pathlib import Path
import datetime,hashlib,json,os
HERE=Path(__file__).resolve().parent
CHUNK=Path('/var/tmp/sound-analysis/helpers/Tension/corpus/decomp/chunks/chunk-00003.jsonl')
EXPECTED=(107467,'d498c48e0e0945a524197bfb3e4e0050fe540bc42a99d1a0f631c7eafe0f9be2')
REVIEW=HERE.parent/'reviews/tension-inner-five-words-v1-review.json'
ROWS=[('145c4', 66, 65312, 4489, '1a396e315dda070e43fbd5b8c2ac9f0579b62be14d17d0746180b140e7d57cd7', 656, 3748, 113, 'c56dedd874df2f84643c15c93823b1ed6a95a595a53d00a3706c3ede2c411642'), ('14a6c', 69, 74076, 3659, 'cd527903f07e33e3ff8d06c8bf4ac0234c4333010f968e6f683289bec5b468da', 700, 3069, 98, '7c965503c742aa028e49b9353a5315c43c64593b41a438712e09711c9a31205c'), ('14d9c', 70, 77735, 761, '95de4be28824d8e71daa7bef90714cc8798f72e82838bddce32e9719acbf130f', 16, 263, 10, 'ae45d2432c3160d1782dbf52d1431d79ec2a543c64480ba4e17b29a72682d774'), ('14dac', 71, 78496, 3573, '2eb26e132cc628b79745446700e4eff20bbdadf5e686b3ea685cd7e454943071', 540, 3101, 120, '6fcf1ddbfab1778399d9f4c71f744c8fb274d1ba28466cfadf1fe1c739eee10e'), ('14fc8', 72, 82069, 960, '67b958b0b23db8e7740df9956573aa47f2a80d0bcd2dc8c6b55a9a6cde8a568e', 108, 586, 24, '3a969fa4597e0cc7146e481e6d6448f689d1fd6b909c01665537dcd255f3e026')]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(name,b):
 if not isinstance(b,bytes):b=(json.dumps(b,indent=2)+'\n').encode()
 with open(HERE/name,'xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
review=identity(REVIEW);assert (review['bytes'],review['sha256'])==(1876,'982ec730731c3ffffb2063eaa876a7e432b043a5343554ca7573491ff468710e')
verified=datetime.datetime.now(datetime.timezone.utc).isoformat()
before=identity(CHUNK);assert(before['bytes'],before['sha256'])==EXPECTED
raws=[];records=[];text=[]
with open(CHUNK,'rb')as f:
 for entry,row,offset,size,rsha,native,cb,cl,csha in ROWS:
  f.seek(offset);raw=f.read(size);assert len(raw)==size and sha(raw)==rsha
  d=json.loads(raw);assert d['entry']=='0x'+entry and d['body_bytes']==native and d['body_ranges']==[['0x'+entry,hex(int(entry,16)+native-1)]]
  assert d['error']is None and not d['timed_out']and not d['partial_code']and not d['thunk']
  c=d.pop('code');assert len(c.encode())==cb==d['code_bytes']and sha(c.encode())==csha==d['code_sha256']and len(c.splitlines())==cl
  raws.append(raw);records.append({'C1_metadata':{'path':str(CHUNK),'row_1based':row,'byte_offset':offset,'raw_bytes':size,'raw_sha256':rsha,'metadata':d},'measured_C_lines':cl})
  text.append(('\n/* WHOLE SELECTED '+entry+'; original C follows unchanged */\n'+c).encode())
after=identity(CHUNK);assert before==after
assert sum(len(x)for x in raws)==13442 and sum(x['C1_metadata']['metadata']['code_bytes']for x in records)==10767 and sum(x['measured_C_lines']for x in records)==365 and sum(len(x['C1_metadata']['metadata']['warnings'])for x in records)==8
put('source-context.jsonl',b''.join(raws));put('whole-selected-C.txt',b''.join(text));put('selected-metadata.json',{'records':records,'raw_bytes':13442,'C_bytes':10767,'C_lines':365,'native_bytes':2020,'warnings':8,'navigation_history':'The selected five exact entries were projected as metadata only; code text was not displayed or semantically read in that pass. Exact record bytes and hashes now govern retention.'})
put('source-read-receipt.json',{'started_utc':start,'approval_verified_before_C_read_utc':verified,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'approval':review,'chunk_before':before,'chunk_after':after,'exact_record_ranges':[{k:x['C1_metadata'][k]for k in ['path','row_1based','byte_offset','raw_bytes','raw_sha256']}for x in records],'source_records':5,'raw_bytes':13442,'C_bytes':10767,'C_lines':365,'warning_occurrences':8,'original_or_native_execution':0,'alias_census_replayed':False,'automatic_retry':False})
print(json.dumps({'retained_records':5,'raw_bytes':13442,'C_bytes':10767,'C_lines':365,'warning_occurrences':8,'native_acquisition':0}))
