"""One selected linker-start membership and immediate neighbors; metadata only."""
from pathlib import Path
import bisect, datetime, hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
IMAGE=Path('/home/ollie/Ableton Live 12 Suite.app/Contents/App-Resources/Devices/Mac/Corpus.bundle/Contents/MacOS/Corpus')
OUT=B/'queries/corpus-x86-3820-linker-start-metadata-2026-10-20.json'
PRIOR=B/'queries/corpus-x86-selected-export-metadata-2026-10-20.json'
METHOD=B/'queries/corpus-x86-selected-export-metadata-2026-10-20.py'
TRIAGE=B/'reviews/corpus-x86-state-next-edge-triage-2026-10-20.json'
def sha(v): return hashlib.sha256(v).hexdigest()
def identity(p):
 v=p.read_bytes();return dict(path=str(p),bytes=len(v),sha256=sha(v))
def bounded(o,n,limit): assert 0<=o<=limit and 0<=n<=limit-o
assert not OUT.exists()
providers=[Path(__file__).resolve(),IMAGE,PRIOR,METHOD,TRIAGE]
before=[identity(p) for p in providers]
assert before[2]['sha256']=='192b70a230dc6c6ba74adaee1f1f8e9694a42a78a8f1204c0ba9d598a2af0034'
assert before[3]['sha256']=='85af6b26e28c7af7bf28566e8fe593d8666eecd71cf4c3df7296cb42b9ab6b1d'
prior=json.loads(PRIOR.read_bytes());fat=IMAGE.read_bytes()
assert len(fat)==527152 and sha(fat)=='2164ec08805b35f1571687a08b7ce7df9831102981f0e2fdbd07719dbf3ef422'
magic,count=struct.unpack_from('>II',fat);assert magic==0xcafebabe
bounded(8,20*count,len(fat));arches=[]
for i in range(count):
 cpu,sub,o,n,alignment=struct.unpack_from('>5I',fat,8+20*i)
 bounded(o,n,len(fat));assert alignment<64 and o%(1<<alignment)==0
 if cpu==0x1000007: arches.append((o,n,sub))
assert arches==[(16384,250352,3)]
s=fat[16384:266736];assert sha(s)=='03be50fae8abee39dcaafec743d82ab4c908d548977354528aa1b8dd3919b00d'
h=struct.unpack_from('<8I',s);assert list(h)==prior['slice']['header_fields'] and h[4:6]==(14,1696)
assert sha(s[32:1728])==prior['slice']['load_commands_sha256']
cursor=32;segments=[];starts=[];commands=[]
for i in range(h[4]):
 bounded(cursor,8,1728);cmd,n=struct.unpack_from('<II',s,cursor)
 assert n>=8 and n%8==0;bounded(cursor,n,1728)
 commands.append(dict(index=i,command=hex(cmd),slice_file_offset=cursor,bytes=n))
 if cmd==0x19:
  assert n>=72
  name,va,vs,fo,fs,mp,ip,ns,flags=struct.unpack_from('<16sQQQQiiII',s,cursor+8)
  assert n==72+80*ns and fs<=vs and va+vs<=1<<64 and ip&~mp==0
  bounded(fo,fs,len(s))
  segments.append(dict(name=name.split(b'\0')[0].decode('ascii'),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip,nsects=ns,flags=flags))
 if cmd==0x26:
  assert n==16
  _,_,o,z=struct.unpack_from('<4I',s,cursor);bounded(o,z,len(s))
  starts.append((i,o,z,s[cursor:cursor+n].hex()))
 cursor+=n
assert cursor==1728 and commands==prior['slice']['load_command_records'] and segments==prior['slice']['segments']
assert starts==[(11,219920,768,'2600000010000000105b030000030000')]
_,off,size,rawcmd=starts[0]
links=[x for x in segments if x['name']=='__LINKEDIT' and x['fileoff']<=off and off+size<=x['fileoff']+x['filesize']]
assert len(links)==1
blob=s[off:off+size];assert sha(blob)==prior['function_starts']['payload_sha256']=='892e54633bc1c5c782810969033822c114d722bcb22ebda2e6daa0c46f8aa86d'
texts=[x for x in segments if x['name']=='__TEXT'];assert len(texts)==1 and texts[0]['vmaddr']==0
pos=0;address=0;rows=[];terminated=False
while pos<len(blob):
 begin=pos;delta=0
 for j in range(10):
  assert pos<len(blob);v=blob[pos];pos+=1
  assert j!=9 or v<=1
  delta|=(v&127)<<(7*j)
  if not v&128:
   assert j==0 or v!=0
   break
 else: raise AssertionError('overlong ULEB')
 if delta==0:
  assert all(v==0 for v in blob[pos:]);terminated=True;terminator=begin;break
 assert address+delta<1<<64;address+=delta
 maps=[x for x in segments if x['vmaddr']<=address<x['vmaddr']+x['filesize'] and x['initprot']&4]
 assert len(maps)==1
 rows.append(dict(index=len(rows),address=hex(address),uleb_blob_offset=begin,uleb_slice_offset=off+begin,uleb_hex=blob[begin:pos].hex()))
assert terminated and len(rows)==534==prior['function_starts']['declared_start_count']
addresses=[int(r['address'],16) for r in rows];i=bisect.bisect_left(addresses,0x3820)
exact=i<len(rows) and addresses[i]==0x3820
selected=dict(exact_membership=exact,previous=None if i==0 else rows[i-1],selected=rows[i] if exact else None,next=rows[i+int(exact)] if i+int(exact)<len(rows) else None)
after=[identity(p) for p in providers];assert before==after
q=dict(schema='one-corpus-x86-linker-start-navigation-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='FROZEN METADATA ONLY; Root review/any source selection separate',providers=before,selection='Exact0x3820 membership and immediate predecessor/successor only; no symbols, instructions or body read',fat=dict(bytes=len(fat),sha256=sha(fat),header8_hex=fat[:8].hex(),selected_slice_offset=16384,selected_slice_bytes=len(s),selected_slice_sha256=sha(s)),header=dict(raw32_hex=s[:32].hex(),load_commands=14,load_command_bytes=1696,load_command_sha256=sha(s[32:1728]),all_command_bounds_and_segments_equal_reviewed_provider=True),function_starts=dict(command_index=11,command_hex=rawcmd,payload_slice_offset=off,payload_bundle_offset=16384+off,payload_bytes=size,payload_sha256=sha(blob),unique_LINKEDIT_mapping=True,declared_start_count=534,termination_blob_offset=terminator,trailing_padding_bytes=len(blob)-pos),result=selected,limits=['534 linker starts are not a proved function count.','Immediate neighbors are metadata navigation only; no gap is body size, no executable byte was decoded/retained, no source/body extent inferred.','Full fat/slice bytes hashed as data; only headers/load commands/LC_FUNCTION_STARTS metadata interpreted.','No old parser replay/import, decoder/Ghidra/original/native or numerical work.','No actual instance/model/coefficient identity, runtime invocation, physical frequency, observation or grade is established.'],recommendation='Use exact0x3820 as the next separately selected metadata/entry nomination. Any prospective export cap must be an explicit Root read limit, not the difference to its next linker start. Reuse current immutable Java only if its fixed scope permits that nomination; no exporter or fixture authored here.',watch=dict(paths=len(before),scope='five exact providers before/after this metadata query; no broad historical watch claim',unchanged=True),actual_expected=None,comparison=None,new_grade=0,complete=False)
with OUT.open('x') as f:json.dump(q,f,indent=2);f.write('\n')
print(json.dumps(dict(query=identity(OUT),result=selected,declared_start_count=len(rows),watch_unchanged=True),indent=2))
