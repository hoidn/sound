from pathlib import Path
import hashlib,json,struct,subprocess,datetime,shutil
root=Path('/home/ollie/Documents/sound')
out=root/'analysis/ableton-live-12.4.3/full-spec-v1/depth-corpus-a1-factory-instructions'
assert not out.exists(), 'Exclusive destination already exists'
image=root/'analysis/ableton-live-12.4.3/derived/Live.arm64'
tool=Path('/var/tmp/sound-tools/rizin-v0.9.1/bin/rizin')
parents=[root/'analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-a1-current-module-construction-frontier-2026-10-20.json',root/'analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-a1-current-module-vtable-metadata-frontier-2026-10-20.json']
def identity(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return {'path':str(p),'bytes':p.stat().st_size,'sha256':h.hexdigest()}
before=[identity(p) for p in [image,tool,*parents]]
assert before[0]['bytes']==149711904 and before[0]['sha256']=='3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad'
with image.open('rb') as f:
 header=f.read(32)
 assert header.hex()=='cffaedfe0c000001000000000200000035000000201b00008580a10000000000'
 magic,cpu,sub,filetype,ncmds,sizeofcmds,flags,reserved=struct.unpack('<IiiIIIII',header)
 commands=f.read(sizeofcmds)
 assert len(commands)==sizeofcmds
 segments=[];cursor=0
 for i in range(ncmds):
  cmd,size=struct.unpack_from('<II',commands,cursor)
  assert size>=8 and cursor+size<=len(commands)
  if cmd==0x19:
   name,va,vsize,fo,fs,maxprot,initprot,nsects,segflags=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
   segments.append({'name':name.rstrip(b'\0').decode('ascii'),'vmaddr':va,'vmsize':vsize,'fileoff':fo,'filesize':fs,'maxprot':maxprot,'initprot':initprot})
  cursor+=size
 assert cursor==len(commands)
 start=0x1024f415c; length=100
 mapping=[s for s in segments if s['vmaddr']<=start and start+length<=s['vmaddr']+s['filesize']]
 assert len(mapping)==1 and mapping[0]['name']=='__TEXT'
 segment=mapping[0];offset=segment['fileoff']+start-segment['vmaddr']
 assert offset+length<=before[0]['bytes']
 f.seek(offset); raw=f.read(length);assert len(raw)==length
out.mkdir()
shutil.copyfile(__file__,out/'extract-and-decode.py')
(out/'factory-100.bin').write_bytes(raw)
(out/'synthetic-ret.bin').write_bytes(bytes.fromhex('c0035fd6'))
def save(name,d):
 with (out/name).open('x') as f:json.dump(d,f,indent=2);f.write('\n')
version=subprocess.run([str(tool),'-NN','-v'],capture_output=True,timeout=30,check=False)
(out/'tool-version.stdout').write_bytes(version.stdout);(out/'tool-version.stderr').write_bytes(version.stderr)
assert version.returncode==0 and b'rizin 0.9.1' in version.stdout
runs=[]
for label,count in [('synthetic-ret',1),('factory-100',25)]:
 argv=[str(tool),'-NN','-n','-x','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj '+str(count),str(out/(label+'.bin'))]
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=subprocess.run(argv,capture_output=True,timeout=30,check=False,cwd=out)
 (out/(label+'.stdout.json')).write_bytes(result.stdout);(out/(label+'.stderr')).write_bytes(result.stderr)
 runs.append({'label':label,'argv':argv,'started_utc':utc,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exit':result.returncode})
 save(label+'.invocation.json',runs[-1])
 assert result.returncode==0
 decoded=json.loads(result.stdout)
 assert len(decoded)==count and all(x['offset']==start+4*i and x['size']==4 for i,x in enumerate(decoded))
 assert b''.join(bytes.fromhex(x['bytes']) for x in decoded)==(out/(label+'.bin')).read_bytes()
 if label=='synthetic-ret':assert decoded[0]['opcode']=='ret'
after=[identity(p) for p in [image,tool,*parents]]
assert before==after
save('extraction.json',{'retained_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'providers_before':before,'providers_after':after,'unchanged':True,'image_header_hex':header.hex(),'load_commands_bytes':len(commands),'load_commands_sha256':hashlib.sha256(commands).hexdigest(),'segments':segments,'selected_mapping':segment,'virtual_start':hex(start),'virtual_end_inclusive':hex(start+length-1),'file_offset':offset,'length':length,'raw_sha256':hashlib.sha256(raw).hexdigest(),'words_little_endian':[{'address':hex(start+i),'bytes':raw[i:i+4].hex(),'word':hex(struct.unpack_from('<I',raw,i)[0])} for i in range(0,length,4)],'tool_version_argv':[str(tool),'-NN','-v'],'tool_version_exit':version.returncode,'runs':runs,'original_instruction_execution':False,'analysis_or_emulation':False})
print(json.dumps({'out':str(out),'raw_sha256':hashlib.sha256(raw).hexdigest(),'tool':before[1],'words':25,'all_4_providers_unchanged':True},indent=2))
