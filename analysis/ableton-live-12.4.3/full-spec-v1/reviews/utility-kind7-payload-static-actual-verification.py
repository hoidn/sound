"""Independent finite stdlib data assertions for the selected200 bytes; no tool replay."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-utility-kind7-payload-instruction-data';O=B/'reviews/utility-kind7-payload-selected-execution';PRE=B/'depth-utility-kind7-payload-instruction-preparation'
DEST=B/'reviews/utility-kind7-payload-static-actual-review-evidence.json'
assert not DEST.exists()
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def load(p):return json.loads(p.read_text())
def checkrow(r):
 got=ident(Path(r['path']));assert got==r;return got
inner=load(P/'before-map.json');outer=load(O/'before-map.json');pins=load(O/'pins.json')
assert len(inner)==127 and len(outer)==3222
assert inner==load(P/'after-map.json')['files'] and load(P/'after-map.json')['unchanged']
assert inner==[json.loads(s) for s in (P/'before-identities.jsonl').read_text().splitlines()]
assert outer==load(O/'after-map.json')
watch={Path(r['path']) for r in outer+inner+pins}
watch.update(p for d in [P,O,PRE] for p in d.iterdir() if p.is_file())
A=B/'reviews/utility-kind7-payload-author-actual-assessment.json';watch.add(A);watch.add(Path(__file__).resolve())
before=[ident(p) for p in sorted(watch)]
for r in inner+outer+pins:checkrow(r)
manifests=[]
for directory,name in [(P,'manifest.json'),(O,'manifest.json'),(PRE,'manifest-preparation.json')]:
 m=load(directory/name);assert {r['path'] for r in m['files']}=={p.name for p in directory.iterdir() if p.is_file() and p.name!=name}
 for r in m['files']:
  got=ident(directory/r['path']);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256'])
 manifests.append(ident(directory/name))
assessment=load(A)
for key in ['actual_manifest','outer_manifest','preparation','root_preflight','peer_preflight','wrapper_parent','wrapper']:checkrow(assessment[key])
wt=Path(assessment['wrapper']['path']).read_text()
for r in reversed(assessment['wrapper_literal_delta']):
 assert wt.count(r['new'])==r['count'];wt=wt.replace(r['new'],r['old'])
assert wt.encode()==Path(assessment['wrapper_parent']['path']).read_bytes()
state=load(P/'status.json');receipt=load(O/'receipt.json');inv=load(O/'invocation-before.json');selection=load(O/'selection.json')
assert state['tool_attempts']==1 and state['tool_returned_pid']==379880 and state['tool_exit']==0 and state['exception'] is None
assert state['original_calls']==0 and not state['emulation'] and state['caller_bytes']==0
assert receipt['attempted_collector_launches']==1 and receipt['returned_collector_pid']==379868 and receipt['outer_wrapper_pid']==379867
assert receipt['exit']==0 and receipt['exception'] is None and not receipt['timeout'] and not receipt['automatic_retry']
assert receipt['inherited_RLIMIT_CORE']==[0,0] and receipt['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8'}
assert inv['stdin']=='DEVNULL' and inv['timeout_seconds']==55 and inv['collector_timeout_seconds']==30 and inv['start_new_session']
assert inv['argv']==load(O/'attempt.json')['argv'] and load(O/'collector-pid.json')['pid']==379868
assert (O/'collector.stdout.json').read_bytes()==(P/'status.json').read_bytes()
assert (O/'collector.stderr').read_bytes()==(P/'decoder.stderr').read_bytes()==b''
assert state['started_utc']<load(P/'invocation-before.json')['started_utc']<state['finished_utc']<receipt['finished_utc']
plan=load(PRE/'plan.json');image=Path(plan['image']['path']);checkrow(plan['image'])
# Exact header/load commands and same fixed200B ONLY; no neighbor or target reads.
start=0x102323d98;end=0x102323e60
with image.open('rb') as f:
 header=f.read(32);h=struct.unpack('<IiiIIIII',header);assert h[0]==0xfeedfacf and h[1]==0x100000c and h[4:6]==(53,6944)
 commands=f.read(h[5]);assert header.hex()==plan['image_header_hex'] and hashlib.sha256(commands).hexdigest()==plan['load_commands_sha256']
 segments=[];cursor=0
 for i in range(h[4]):
  cmd,size=struct.unpack_from('<II',commands,cursor);assert size>=8 and cursor+size<=len(commands)
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,cursor+8);segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
  cursor+=size
 assert cursor==len(commands)
 matches=[s for s in segments if s['vmaddr']<=start and end<=s['vmaddr']+min(s['filesize'],s['vmsize'])]
 assert matches==[plan['expected_segment']]
 offset=matches[0]['fileoff']+start-matches[0]['vmaddr'];assert offset==36847000
 f.seek(offset);image200=f.read(200)
raw=(P/'payload-200.bin').read_bytes();assert raw==image200 and len(raw)==200
assert hashlib.sha256(raw).hexdigest()=='a556d03020b742ee66eddb9ea78adc1f2435018e42a375cbfd26785506c04b6c'
rows=load(P/'decoder.stdout.json');ex=load(P/'extraction.json');assert len(rows)==50 and ex['length']==200 and ex['file_offset']==offset and ex['selected_mapping']==matches[0]
assert b''.join(bytes.fromhex(r['bytes']) for r in rows)==raw
assert assessment['selected_rows']==[{k:r[k] for k in ['offset','size','bytes','opcode','type']} for r in rows]
# Explicit selected-word classes/operands, not a general decoder or execution model.
expected=[
 ('imm',31,31,64,True),('pair',False,20,19,31,32),('pair',False,29,30,31,48),('imm',29,31,48,False),('branch',True,0x10128ed98),('page',8,0x106796000),('imm',8,8,0xe00,False),('mem',False,8,0,0,8,0),('page',8,0x1064fe000),('mem',True,8,8,0x948,8,0),('ldaprb',8,8),('page',19,0x106537000),('mem',True,19,19,0x8f8,8,0),('tbz',8,0,0x102323e0c),('mem',True,8,19,0,8,0),('mem',False,8,0,0x18,8,0),('movz',8,1),('mem',False,8,0,0x20,1,0),('mem',False,31,0,0x28,8,0),('mem',False,31,0,0x30,4,0),('mem',False,31,0,0x38,8,0),('mem',False,31,0,0x40,4,0),('movi',0,0x55),('mem',False,0,0,0x48,4,1),('mem',False,31,0,0x4c,1,0),('pair',True,29,30,31,48),('pair',True,20,19,31,32),('imm',31,31,64,False),('ret',30),('page',8,0x1064fe000),('mem',True,8,8,0x948,8,0),('mem',False,0,31,8,8,0),('mov',0,8),('branch',True,0x1054d55d0),('mov',8,0),('mem',True,0,31,8,8,0),('cbz',8,0x102323dd0),('page',8,0x105aa9000),('imm',8,8,0xb90,False),('mem',False,8,31,16,8,0),('mem',False,31,31,24,1,0),('imm',0,31,16,False),('branch',True,0x101290f58),('mem',True,8,31,16,8,0),('mem',False,8,19,0,8,0),('page',0,0x1064fe000),('mem',True,0,0,0x948,8,0),('branch',True,0x1054d55dc),('mem',True,0,31,8,8,0),('branch',False,0x102323dd0)]
def signed(x,n):return x-(1<<n) if x&(1<<(n-1)) else x
fields=[]
for i,e in enumerate(expected):
 pc=start+4*i;w=struct.unpack_from('<I',raw,i*4)[0];r=rows[i];x=ex['words'][i]
 assert r['offset']==pc and r['size']==4 and len(bytes.fromhex(r['bytes']))==4
 assert x==dict(va=hex(pc),bytes=raw[i*4:i*4+4].hex(),word=hex(w))
 kind=e[0];d=dict(index=i,va=hex(pc),word=hex(w),class_name=kind)
 if kind=='imm':
  assert w&0x1f000000==0x11000000 and w>>31==1 and not(w>>29&1)
  got=(kind,w&31,w>>5&31,(w>>10&4095)<<(12 if w>>22&1 else 0),bool(w>>30&1))
 elif kind=='pair':
  assert w&0x3a000000==0x28000000 and w>>30==2 and not(w>>26&1) and w>>23&3==2
  got=(kind,bool(w>>22&1),w&31,w>>10&31,w>>5&31,signed(w>>15&127,7)*8)
 elif kind=='branch':
  assert w&0x7c000000==0x14000000;got=(kind,bool(w>>31),pc+signed(w&0x3ffffff,26)*4)
 elif kind=='page':
  assert w&0x9f000000==0x90000000;got=(kind,w&31,(pc&~4095)+(signed(((w>>5&0x7ffff)<<2)|(w>>29&3),21)<<12))
 elif kind=='mem':
  assert w&0x3b000000==0x39000000 and w>>22&3 in (0,1)
  size=1<<(w>>30&3);got=(kind,bool(w>>22&1),w&31,w>>5&31,(w>>10&4095)*size,size,w>>26&1)
 elif kind=='ldaprb':
  assert w&0xfffffc00==0x38bfc000;got=(kind,w&31,w>>5&31)
 elif kind=='tbz':
  assert w&0x7f000000==0x36000000;got=(kind,w&31,((w>>31)<<5)|(w>>19&31),pc+signed(w>>5&0x3fff,14)*4)
 elif kind=='cbz':
  assert w&0xff000000==0x34000000;got=(kind,w&31,pc+signed(w>>5&0x7ffff,19)*4)
 elif kind=='movz':
  assert w&0xff800000==0x52800000 and w>>21&3==0;got=(kind,w&31,w>>5&65535)
 elif kind=='movi':
  assert w&0xfff8fc00==0x2f00e400;got=(kind,w&31,((w>>16&7)<<5)|(w>>5&31))
  d['expanded_D_register_literal_hex']='0x'+format(sum((255 if got[2]>>j&1 else 0)<<(8*j) for j in range(8)),'016x')
 elif kind=='mov':
  assert w&0xffe0ffe0==0xaa0003e0;got=(kind,w&31,w>>16&31)
 elif kind=='ret':
  assert w&0xfffffc1f==0xd65f0000;got=(kind,w>>5&31)
 else:raise AssertionError(kind)
 assert got==e,(i,got,e)
 d['decoded_operand_tuple']=list(got);d['raw_fields_match_expected']=True;fields.append(d)
assert rows[2]['opcode']=='stp fp, lr, [sp, 0lr]' and rows[25]['opcode']=='ldp fp, lr, [sp, 0lr]'
assert rows[10]['type']=='null' and fields[10]['class_name']=='ldaprb'
after=[ident(p) for p in sorted(watch)];assert before==after
result=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS_INDEPENDENT_FINITE_STATIC_DATA_ASSERTIONS_ONLY',input_manifests=manifests,assessment=ident(A),method=ident(Path(__file__).resolve()),selected_range=[hex(start),hex(end)],raw_sha256=hashlib.sha256(raw).hexdigest(),unique_file_backed_mapping=matches[0],file_offset=offset,header_commands=53,header_command_bytes=6944,paired_inner_maps=127,paired_outer_maps=3222,outer_pins=len(pins),all_current_pins_match=True,all50_native_operand_rows=fields,wrapper_four_literal_inverse=True,accounting_confirmed=dict(collector_attempts=1,collector_pid=379868,decoder_pid=379880,exits=[0,0],core=[0,0],no_timeout_or_retry=True),display_notes=['Rows2/25 raw64bit pair fields baseSP/offset48, despite malformed display[sp,0lr]; no output patch/redecode.','Row10 exactLDAPRB encoding retained despite type null; classification is not a nop.'],read_scope='Whole current packet/outer receipts/assessment and wrapper as data; all50raw instruction fields. Whole image digest opaque; header/load commands and exactly same200B fresh data read only. No old/source827C/target/helper/global/suffix semantic read.',before=before,after_equal_before=True,watch_count=len(before),no_supplied_code_executed=True,no_decoder_or_original_execution=True,application_expected=None,comparison=None,new_grades=0,complete=False)
with DEST.open('x') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(evidence=ident(DEST),watch_count=len(before),all50_native_fields=True,inner=127,outer=3222,no_replay=True),indent=2))
