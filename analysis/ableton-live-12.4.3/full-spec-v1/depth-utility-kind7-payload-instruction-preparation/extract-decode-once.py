"""AUTHOR-ONLY preparation: fixed200B static-data decode; never imports/executes image code."""
from pathlib import Path
import datetime, hashlib, json, os, struct, subprocess, sys
PRE=Path(__file__).resolve().parent
DEST=PRE.with_name('depth-utility-kind7-payload-instruction-data')
START=0x102323d98
LENGTH=200

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def save(name,value):
 with (DEST/name).open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
 if len(sys.argv)!=3 or sys.argv[1]!='--extract-decode-selected-once':
  raise SystemExit('Root-selected exact manifest digest required; no check/replay/caller override.')
 if not sys.dont_write_bytecode:raise SystemExit('Use python3 -B')
 if DEST.exists():raise SystemExit('Exclusive destination already exists; no reuse/retry')
 DEST.mkdir()
 before=[];after=[];watched=[];stdout=b'';stderr=b''
 state=dict(started_utc=utc(),argv=sys.argv,phase='preflight',tool_attempts=0,tool_returned_pid=None,tool_exit=None,exception=None,original_calls=0,emulation=False,caller_bytes=0)
 save('selection.json',state.copy())
 try:
  manifest_path=PRE/'manifest-preparation.json'
  assert sha(manifest_path.read_bytes())==sys.argv[2], 'Manifest identity mismatch'
  manifest=json.loads(manifest_path.read_text())
  assert {r['path'] for r in manifest['files']}=={p.name for p in PRE.iterdir() if p.is_file() and p!=manifest_path}
  for r in manifest['files']:
   actual=ident(PRE/r['path']);assert (actual['bytes'],actual['sha256'])==(r['bytes'],r['sha256'])
  plan=json.loads((PRE/'plan.json').read_text())
  assert plan['caller_window'] is None and plan['helper']['va']==hex(START) and plan['helper']['length']==LENGTH
  assert plan['helper']['body_start']=='0x102323d98' and plan['helper']['body_end_exclusive']=='0x102323e60'
  assert int(plan['helper']['body_start'],16)<=START and START+LENGTH<=int(plan['helper']['body_end_exclusive'],16)
  assert START+LENGTH==0x102323e60
  image=Path(plan['image']['path']);tool=Path(plan['tool']['path'])
  watched=sorted({image,tool,*[Path(r['path']) for r in plan['providers']],*[p for p in PRE.iterdir() if p.is_file()]})
  with (DEST/'before-identities.jsonl').open('xb') as log:
   for p in watched:
    row=ident(p);before.append(row);log.write((json.dumps(row)+'\n').encode());log.flush();os.fsync(log.fileno())
  save('before-map.json',before)
  for r in [plan['image'],plan['tool'],*plan['providers']]:
   actual=next(x for x in before if x['path']==r['path']);assert (actual['bytes'],actual['sha256'])==(r['bytes'],r['sha256'])
  state['phase']='header-mapping-and200B-extraction'
  with image.open('rb') as f:
   header=f.read(32);assert header.hex()==plan['image_header_hex']
   magic,cpu,sub,filetype,ncmds,sizeofcmds,flags,reserved=struct.unpack('<IiiIIIII',header)
   assert magic==0xfeedfacf and cpu==0x100000c and ncmds==53 and sizeofcmds==6944
   commands=f.read(sizeofcmds);assert len(commands)==6944 and sha(commands)==plan['load_commands_sha256']
   cursor=0;segments=[]
   for _ in range(ncmds):
    cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
    if cmd==0x19:
     assert size>=72
     name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,cursor+8)
     segments.append(dict(name=name.rstrip(b'\0').decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
    cursor+=size
   assert cursor==len(commands)
   maps=[s for s in segments if s['vmaddr']<=START and START+LENGTH<=s['vmaddr']+s['filesize']]
   assert len(maps)==1 and maps[0]==plan['expected_segment']
   offset=maps[0]['fileoff']+START-maps[0]['vmaddr'];assert offset==plan['helper']['file_offset'] and offset+LENGTH<=plan['image']['bytes']
   f.seek(offset);raw=f.read(LENGTH);assert len(raw)==LENGTH
  rawpath=DEST/'payload-200.bin'
  with rawpath.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  save('extraction.json',dict(image_header_hex=header.hex(),load_commands_sha256=sha(commands),selected_mapping=maps[0],va=hex(START),length=LENGTH,file_offset=offset,raw_sha256=sha(raw),words=[dict(va=hex(START+i),bytes=raw[i:i+4].hex(),word=hex(struct.unpack_from('<I',raw,i)[0])) for i in range(0,LENGTH,4)],caller_bytes=0))
  argv=[str(tool),'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(START),'-s',hex(START),'-q','-c','pdj 50',str(rawpath)]
  assert argv==plan['decoder_argv']
  save('invocation-before.json',dict(argv=argv,started_utc=utc(),timeout_seconds=30,analysis_or_emulation=False,original_instructions_executed=False))
  state['phase']='static-decoder';state['tool_attempts']=1
  child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=DEST)
  state['tool_returned_pid']=child.pid
  try:stdout,stderr=child.communicate(timeout=30)
  except subprocess.TimeoutExpired:
   child.kill();stdout,stderr=child.communicate();state['tool_exit']=child.returncode
   raise
  state['tool_exit']=child.returncode
  assert child.returncode==0
  decoded=json.loads(stdout)
  assert len(decoded)==50 and all(r['offset']==START+4*i and r['size']==4 and len(bytes.fromhex(r['bytes']))==4 and str(r.get('type','')).strip().lower() not in ('invalid','ill') and isinstance(r.get('opcode'),str) and r['opcode'].strip().lower() not in ('','invalid','ill','none') for i,r in enumerate(decoded))
  assert b''.join(bytes.fromhex(r['bytes']) for r in decoded)==raw
  state['phase']='decoded50byteexact-rows-no-semantic-conclusion'
 except Exception as error:
  state['exception']=type(error).__name__+': '+str(error)
  save('failure.json',dict(ended_utc=utc(),phase=state['phase'],exception=state['exception'],partial_files_retained=True,no_retry=True))
 finally:
  with (DEST/'decoder.stdout.json').open('xb') as f:f.write(stdout);f.flush();os.fsync(f.fileno())
  with (DEST/'decoder.stderr').open('xb') as f:f.write(stderr);f.flush();os.fsync(f.fileno())
  for p in watched:
   try:after.append(ident(p))
   except Exception as error:after.append(dict(path=str(p),identity_error=type(error).__name__+': '+str(error)))
  unchanged=bool(before) and len(before)==len(watched) and before==after
  save('after-map.json',dict(files=after,unchanged=unchanged,ended_utc=utc()))
  state.update(finished_utc=utc(),watched=len(watched),before_rows=len(before),watch_unchanged=unchanged,stdout_bytes=len(stdout),stderr_bytes=len(stderr))
  save('status.json',state)
 print(json.dumps(state,indent=2))
 return 0 if state['exception'] is None and state['phase']=='decoded50byteexact-rows-no-semantic-conclusion' and state['watch_unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
