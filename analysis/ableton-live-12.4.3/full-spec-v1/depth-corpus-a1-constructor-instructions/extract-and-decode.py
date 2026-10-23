from pathlib import Path
import hashlib,json,struct,subprocess,datetime,shutil
root=Path('/home/ollie/Documents/sound')
out=root/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-a1-constructor-instructions'
assert not out.exists(), 'Exclusive destination exists'
image=root/'analysis/ableton-live-12.4.3/derived/Live.arm64'
tool=Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
factory=root/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-a1-factory-instructions'
parent=root/'analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-a1-current-module-construction-frontier-2026-10-20.json'
review=root/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-a1-factory-instruction-review.json'
def identity(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
providers=[image,tool,parent,review,*sorted(factory.iterdir())]
before=[identity(p) for p in providers]
assert before[0]['bytes']==149711904 and before[0]['sha256']=='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
assert before[1]['sha256']=='ab5614cf137608cffc5a3f4f471a91c995cfa7c0c35465bfb73876e5b95561ba'
with image.open('rb') as f:
 header=f.read(32)
 assert header.hex()=='cffaedfe0c000001000000000200000035000000201b00008580a10000000000'
 ncmds,sizeofcmds=struct.unpack_from('<II',header,16)
 commands=f.read(sizeofcmds);cursor=0;segments=[]
 for _ in range(ncmds):
  cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
   segments.append({'name':name.rstrip(b'\0').decode(),'vmaddr':va,'vmsize':vs,'fileoff':fo,'filesize':fs,'maxprot':mp,'initprot':ip})
  cursor+=size
 assert cursor==len(commands)
 start=0x1026e8e50;length=288
 mapping=[s for s in segments if s['vmaddr']<=start and start+length<=s['vmaddr']+s['filesize']]
 assert len(mapping)==1 and mapping[0]['name']=='__TEXT'
 segment=mapping[0];offset=segment['fileoff']+start-segment['vmaddr']
 f.seek(offset);raw=f.read(length);assert len(raw)==length
out.mkdir();shutil.copyfile(__file__,out/'extract-and-decode.py')
(out/'constructor-288.bin').write_bytes(raw)
argv=[str(tool),'-NN','-n','-x','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj 72',str(out/'constructor-288.bin')]
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(argv,capture_output=True,timeout=30,cwd=out,check=False)
(out/'constructor-288.stdout.json').write_bytes(r.stdout);(out/'constructor-288.stderr').write_bytes(r.stderr)
def save(name,value):
 with (out/name).open('x') as f:json.dump(value,f,indent=2);f.write('\n')
save('invocation.json',{'argv':argv,'started_utc':utc,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':r.returncode,'original_execution':False,'emulation':False,'analysis_pass':False,'control_repeated':False})
assert r.returncode==0
rows=json.loads(r.stdout);assert len(rows)==72
assert all(row['offset']==start+4*i and row['size']==4 for i,row in enumerate(rows))
assert b''.join(bytes.fromhex(row['bytes']) for row in rows)==raw
after=[identity(p) for p in providers];assert before==after
save('extraction.json',{'providers_before':before,'providers_after':after,'all_unchanged':True,'header_hex':header.hex(),'load_commands_bytes':len(commands),'load_commands_sha256':hashlib.sha256(commands).hexdigest(),'segments':segments,'selected_mapping':segment,'virtual_start':hex(start),'virtual_end_inclusive':hex(start+length-1),'file_offset':offset,'length':length,'raw_sha256':hashlib.sha256(raw).hexdigest(),'word_count':72,'tool_version_source':str(factory/'tool-version.stdout'),'tool_version':'rizin 0.9.1 @ linux-x86-64; c3a90e9226d977f58f4e9c75f78fa6b07afe13c7','static_decodes':1,'original_calls':0})
print(json.dumps({'packet':str(out),'raw_sha256':hashlib.sha256(raw).hexdigest(),'words':72,'providers_unchanged':len(before),'stderr_bytes':len(r.stderr)},indent=2))
