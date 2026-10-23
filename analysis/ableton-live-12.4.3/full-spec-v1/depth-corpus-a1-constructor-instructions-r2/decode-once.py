from pathlib import Path
import hashlib,json,subprocess,datetime,shutil
root=Path('/home/ollie/Documents/sound')
old=root/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-a1-constructor-instructions'
out=root/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-a1-constructor-instructions-r2'
assert not out.exists(), 'Exclusive destination exists'
tool=Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
receipt=root/'analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-a1-constructor-instruction-frontier-2026-10-20.json'
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
oldmanifest=json.loads((old/'manifest.json').read_bytes())
assert identity(old/'manifest.json')['sha256']=='9f92836d51b6313c73cfcafb4a65647864fc737bdc66849e605519330fa3ac00'
assert set(x.name for x in old.iterdir())==set(oldmanifest['files'])|{'manifest.json'}
for name,pin in oldmanifest['files'].items():
 actual=identity(old/name);assert {k:actual[k] for k in ['bytes','sha256']}==pin
raw=(old/'constructor-288.bin').read_bytes()
assert len(raw)==288 and hashlib.sha256(raw).hexdigest()=='3c36b423c1a6cd8f194ec973135ba170c4e764194419e27642161f0475123885'
assert identity(tool)['sha256']=='ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba'
providers=[*sorted(old.iterdir()),tool,receipt]
before=[identity(p) for p in providers]
out.mkdir();shutil.copyfile(__file__,out/'decode-once.py')
def save(name,value):
 with (out/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
(out/'constructor-288.bin').write_bytes(raw)
save('before-map.json',{'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'providers':before})
oldargv=json.loads((old/'invocation.json').read_bytes())['argv']
argv=oldargv.copy();argv.insert(4,'-f');argv[-1]=str(out/'constructor-288.bin')
assert argv==[str(tool),'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m','0x1026e8e50','-s','0x1026e8e50','-q','-c','pdj 72',str(out/'constructor-288.bin')]
invocation={'argv':argv,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'change_from_first':'Only -f added; destination raw path changed to this exclusive byte-identical sibling.','original_execution':False,'reextraction':False,'control_repeated':False,'automatic_retry':False}
save('invocation-before.json',invocation)
status={'exit':None,'exception':None};stdout=b'';stderr=b''
try:
 result=subprocess.run(argv,capture_output=True,timeout=30,cwd=out,check=False)
 stdout=result.stdout;stderr=result.stderr;status['exit']=result.returncode
except subprocess.TimeoutExpired as error:
 stdout=error.stdout or b'';stderr=error.stderr or b'';status['exception']='TimeoutExpired after30seconds'
except Exception as error:
 status['exception']=type(error).__name__+': '+str(error)
finally:
 (out/'constructor-288.stdout.json').write_bytes(stdout)
 (out/'constructor-288.stderr').write_bytes(stderr)
 status['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 save('status.json',status)
 after=[identity(p) for p in providers]
 save('after-map.json',{'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'providers':after,'unchanged':before==after})
assert before==after
assert status['exit']==0 and status['exception'] is None
rows=json.loads(stdout)
assert len(rows)==72 and all(row['offset']==0x1026e8e50+4*i and row['size']==4 for i,row in enumerate(rows))
assert b''.join(bytes.fromhex(row['bytes']) for row in rows)==raw
save('decode-validation.json',{'status':'PASS complete72-row static decode','rows':72,'size4_and_mapped_offsets':True,'full_raw_byte_roundtrip':True,'stderr_bytes':len(stderr),'providers_unchanged':len(before),'tool_retries':0,'original_calls':0})
print(json.dumps({'status':'PASS','rows':72,'providers_unchanged':len(before),'stderr_bytes':len(stderr),'raw_sha256':hashlib.sha256(raw).hexdigest()},indent=2))
