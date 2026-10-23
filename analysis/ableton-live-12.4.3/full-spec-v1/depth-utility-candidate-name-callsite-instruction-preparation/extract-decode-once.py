"""AUTHOR-ONLY fixed nine128B staticDATA windows; no original code executed."""
from pathlib import Path
import datetime, hashlib, json, os, struct, subprocess, sys
PRE=Path(__file__).resolve().parent
DEST=PRE.with_name('depth-utility-candidate-name-callsite-instruction-data')
SITES=[0x1025c2058,0x1025c21f4,0x1025c2300,0x1025c2470,0x1025c2530,0x1025c2690,0x1025c2854,0x1025c28e0,0x1025c2a48]
TARGET=0x101482918

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
 if len(sys.argv)!=3 or sys.argv[1]!='--extract-decode-selected-once':raise SystemExit('Root-selected sealed digest required; no override/check/replay mode')
 if not sys.dont_write_bytecode:raise SystemExit('Use python3 -B')
 if DEST.exists():raise SystemExit('Exclusive destination exists; no reuse/retry')
 DEST.mkdir()
 outcomes=[dict(site=hex(s),start=hex(s-16),end_exclusive=hex(s+112),length=128,status='not_attempted',tool_attempts=0,pid=None,tool_exit=None,exception=None) for s in SITES]
 before=[];after=[];watched=[]
 state=dict(started_utc=utc(),argv=sys.argv,phase='preflight',exception=None,tool_attempts=0,original_calls=0,emulation=False)
 save('selection.json',state.copy());save('outcomes-initial.json',outcomes)
 try:
  seal=PRE/'manifest-preparation.json';assert sha(seal.read_bytes())==sys.argv[2]
  manifest=json.loads(seal.read_text());assert {r['path'] for r in manifest['files']}=={p.name for p in PRE.iterdir() if p.is_file() and p!=seal}
  for r in manifest['files']:
   row=ident(PRE/r['path']);assert (row['bytes'],row['sha256'])==(r['bytes'],r['sha256'])
  plan=json.loads((PRE/'plan.json').read_text())
  assert [int(w['site'],16) for w in plan['windows']]==SITES and plan['total_window_bytes']==1152
  assert all(int(w['start'],16)==s-16 and int(w['end_exclusive'],16)==s+112 and w['length']==128 for s,w in zip(SITES,plan['windows']))
  ranges=[(int(a,16),int(z,16)+1) for a,z in plan['caller_metadata']['body_ranges']]
  assert all(any(a<=s-16 and s+112<=z for a,z in ranges) for s in SITES)
  image=Path(plan['image']['path']);tool=Path(plan['tool']['path'])
  watched=sorted({image,tool,*[Path(r['path']) for r in plan['providers']],*[p for p in PRE.iterdir() if p.is_file()]})
  with (DEST/'before-identities.jsonl').open('xb') as f:
   for p in watched:
    row=ident(p);before.append(row);f.write((json.dumps(row)+'\n').encode());f.flush();os.fsync(f.fileno())
  save('before-map.json',before)
  for r in [plan['image'],plan['tool'],*plan['providers']]:
   row=next(x for x in before if x['path']==r['path']);assert (row['bytes'],row['sha256'])==(r['bytes'],r['sha256'])
  state['phase']='bounded-header-and-mapping'
  with image.open('rb') as f:
   header=f.read(32);assert header.hex()==plan['image_header_hex']
   magic,cpu,sub,kind,count,size,flags,reserved=struct.unpack('<IiiIIIII',header)
   assert magic==0xfeedfacf and cpu==0x100000c and count==53 and size==6944
   commands=f.read(size);assert sha(commands)==plan['load_commands_sha256']
   segments=[];pos=0
   for _ in range(count):
    cmd,n=struct.unpack_from('<II',commands,pos);assert n>=8 and pos+n<=size
    if cmd==0x19:
     assert n>=72
     name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,pos+8)
     segments.append(dict(name=name.rstrip(b'\0').decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
    pos+=n
   assert pos==size
  save('mapping.json',dict(header_hex=header.hex(),load_commands_sha256=sha(commands),segments=segments,selected_caller_ranges=plan['caller_metadata']['body_ranges']))
  for outcome,window in zip(outcomes,plan['windows']):
   stdout=b'';stderr=b'';site=int(outcome['site'],16);start=site-16;label=window['id'];outcome['started_utc']=utc()
   try:
    state['phase']='window-'+label;outcome['status']='extracting'
    maps=[s for s in segments if s['vmaddr']<=start and start+128<=s['vmaddr']+s['filesize']]
    assert maps==[plan['expected_segment']]
    offset=maps[0]['fileoff']+start-maps[0]['vmaddr'];assert offset==window['file_offset'] and offset+128<=plan['image']['bytes']
    with image.open('rb') as f:f.seek(offset);raw=f.read(128)
    assert len(raw)==128
    rawpath=DEST/(label+'.bin')
    with rawpath.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    outcome['raw_sha256']=sha(raw)
    # Retain actual raw/fields BEFORE rejecting a metadata-call mismatch; no decode retry.
    word=struct.unpack_from('<I',raw,16)[0];is_bl=word&0xfc000000==0x94000000
    imm=word&0x3ffffff;imm=imm-(1<<26) if imm&(1<<25) else imm
    target=site+4*imm if is_bl else None
    save(label+'.extraction.json',dict(va=hex(start),length=128,file_offset=offset,raw_sha256=sha(raw),callsite=hex(site),call_word=hex(word),is_bl=is_bl,call_target=hex(target) if target is not None else None,mapping=maps[0]))
    assert is_bl and target==TARGET
    argv=[str(tool),'-NN','-n','-x','-f','-a','arm','-b','64','-E','little','-m',hex(start),'-s',hex(start),'-q','-c','pdj 32',str(rawpath)]
    assert argv==window['decoder_argv']
    save(label+'.invocation-before.json',dict(argv=argv,started_utc=utc(),timeout_seconds=30,original_execution=False,analysis_or_emulation=False))
    outcome['tool_attempts']=1;state['tool_attempts']+=1;outcome['status']='decoder_attempted'
    child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=DEST);outcome['pid']=child.pid
    try:stdout,stderr=child.communicate(timeout=30)
    except subprocess.TimeoutExpired:
     child.kill();stdout,stderr=child.communicate();outcome['tool_exit']=child.returncode
     raise
    outcome['tool_exit']=child.returncode;assert child.returncode==0
    rows=json.loads(stdout);assert len(rows)==32
    assert all(r['offset']==start+4*i and r['size']==4 and r.get('type')!='ill' and r.get('opcode') not in [None,'invalid'] for i,r in enumerate(rows))
    assert b''.join(bytes.fromhex(r['bytes']) for r in rows)==raw
    outcome.update(status='decoded32byteexactrows',raw_sha256=sha(raw),rows=32)
   except Exception as error:
    outcome.update(status='failed',exception=type(error).__name__+': '+str(error));raise
   finally:
    with (DEST/(label+'.stdout.json')).open('xb') as f:f.write(stdout)
    with (DEST/(label+'.stderr')).open('xb') as f:f.write(stderr)
    outcome['finished_utc']=utc();save(label+'.receipt.json',outcome.copy())
  state['phase']='all9decoded-no-branch-association-conclusion'
 except Exception as error:
  state['exception']=type(error).__name__+': '+str(error)
  save('failure.json',dict(phase=state['phase'],exception=state['exception'],finished_utc=utc(),partial_outputs_retained=True,no_retry=True))
 finally:
  for outcome in outcomes:
   if outcome['status']=='not_attempted':outcome['status']='skipped_after_failure'
  save('outcomes-final.json',outcomes)
  for p in watched:
   try:after.append(ident(p))
   except Exception as error:after.append(dict(path=str(p),identity_error=type(error).__name__+': '+str(error)))
  unchanged=bool(before) and len(before)==len(watched) and before==after
  save('after-map.json',dict(files=after,unchanged=unchanged,ended_utc=utc()))
  state.update(finished_utc=utc(),watch_unchanged=unchanged,watched=len(watched),before_rows=len(before),completed_windows=sum(r['status']=='decoded32byteexactrows' for r in outcomes),all9outcomes_retained=True)
  save('status.json',state)
 print(json.dumps(state,indent=2))
 return 0 if state['exception'] is None and state['completed_windows']==9 and state['watch_unchanged'] else 1
if __name__=='__main__':raise SystemExit(main())
