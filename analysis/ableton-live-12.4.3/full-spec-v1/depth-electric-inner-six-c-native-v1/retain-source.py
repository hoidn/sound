#!/usr/bin/env python3
"""Exact six selected retained C1 ranges; no census, alias pass or callee follow."""
from pathlib import Path
import datetime,hashlib,json,os
HERE=Path(__file__).resolve().parent
CHUNK=Path('/var/tmp/sound-analysis/helpers/Electric/corpus/decomp/chunks/chunk-00002.jsonl')
EXPECTED=(120876,'d48dd1e67f127c4383fbadbb67a38c44d428fb802466504b75c11401af9ce26b')
REVIEW=HERE.parent/'reviews/electric-encoded-sites-v2-review.json'
ROWS=[('cb0c',12,11311,4333,'1771d37ab12a60a276832144b58f392193604d5c7c46f5326e38cc7fb8acd14a',800,3789,135,'c7008b4c5606866243fdbf098bde6e3b95a35dbf156a1bf31248d20aab4078b4'),('d2e0',20,23996,4486,'8ca556aa5921c57cabd870d63d0f4d0f36ae9447b415adabc05652969e1671b4',656,3748,113,'cf8add33d64a42b9aeaf83c34cb21d8b416b95ba3a14f225763554b9202ac9fa'),('d688',22,30789,3656,'5828ada7078f2a14404f7bf6ee8e31db7b780e459a5f93fac92818b92d2e2491',700,3069,98,'97a3eb9beb2a135f1bf78b20523753481cf5cd0d83cb9ecf34fb3ad1c8807f2c'),('d9b8',23,34445,758,'b4691c79d36886954a22fdf4c5657dadfb5a6b1f8aa897f15ef1b98ab1371ce4',16,263,10,'6b1679783e826b3e4db7520629478237c2af3b0220a3fe59e6e7ef9b9e9bcd1d'),('d9c8',24,35203,3570,'954cecbf335ab739f8d18d6da50ed709db2d56e79b0bd9da9e18e1ca60bbceba',540,3101,120,'738f50ee3fdf2e7cf6f09710f3e78dc286c494438fbfa22ab0ba4bb88cfb89da'),('dbe4',25,38773,957,'89847427e56f7e4178054f0294e8349cc80d746f37cfae21801d9dd03748b14b',108,586,24,'aeebdd468ee2c2019668132373545cc32730cabcf415af54a6d411acb47021f1')]
def sha(b):return hashlib.sha256(b).hexdigest()
def put(name,b):
 if not isinstance(b,bytes):b=(json.dumps(b,indent=2)+'\n').encode()
 with open(HERE/name,'xb')as f:f.write(b);f.flush();os.fsync(f.fileno())
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
review=identity(REVIEW);assert (review['bytes'],review['sha256'])==(3280,'653ce9bdd71c91a817a3c6166677f8f7065ea51ccd706c865e11b667ed9b375c')
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
assert sum(len(x)for x in raws)==17760 and sum(x['C1_metadata']['metadata']['code_bytes']for x in records)==14556 and sum(x['measured_C_lines']for x in records)==500 and sum(len(x['C1_metadata']['metadata']['warnings'])for x in records)==9
put('source-context.jsonl',b''.join(raws));put('whole-selected-C.txt',b''.join(text));put('selected-metadata.json',{'records':records,'raw_bytes':17760,'C_bytes':14556,'C_lines':500,'native_bytes':2820,'warnings':9,'navigation_history':'Earlier metadata-only alias-derived row guess mismatched and stopped; exact entry/range pins above replace navigation guesses. No source semantics were read during that metadata pass.'})
put('source-read-receipt.json',{'started_utc':start,'approval_verified_before_C_read_utc':verified,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'approval':review,'chunk_before':before,'chunk_after':after,'exact_record_ranges':[{k:x['C1_metadata'][k]for k in ['path','row_1based','byte_offset','raw_bytes','raw_sha256']}for x in records],'source_records':6,'raw_bytes':17760,'C_bytes':14556,'C_lines':500,'warning_occurrences':9,'original_or_native_execution':0,'alias_census_replayed':False,'automatic_retry':False})
print(json.dumps({'retained_records':6,'raw_bytes':17760,'C_bytes':14556,'C_lines':500,'warning_occurrences':9,'native_acquisition':0}))
