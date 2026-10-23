"""Independent selected16B image/hash/bitfields only. No decoder or original invocation."""
from pathlib import Path
import datetime, hashlib, json, struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-utility-candidate-name-instruction-data'
PRE=B/'depth-utility-candidate-name-instruction-preparation'
ROOT=B/'reviews/utility-candidate-name-static-root-execution'
OUT=B/'reviews/utility-candidate-name-static-actual-review.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def check(p,row):
 r=ident(p);assert (r['bytes'],r['sha256'])==(row['bytes'],row['sha256']),str(p)
assert not OUT.exists()
inner=load(P/'before-map.json');inner_after=load(P/'after-map.json')
outer=load(ROOT/'before.json');outer_after=load(ROOT/'after.json')
assert len(inner)==20 and len({r['path'] for r in inner})==20 and inner==inner_after['files'] and inner_after['unchanged']
assert len(outer)==41 and len({r['path'] for r in outer})==41 and outer==outer_after
assert [json.loads(line) for line in (P/'before-identities.jsonl').read_text().splitlines()]==inner
watched={Path(r['path']) for r in inner+outer}|set(P.iterdir())|set(ROOT.iterdir())|{Path(__file__).resolve()}
before=[ident(p) for p in sorted(watched)]
manifest=load(P/'manifest.json');assert sha((P/'manifest.json').read_bytes())=='2f4fc7ec18694b0b4a04e464d10ce180d3af4ee9b31a2baa1236eadb479e0e3e'
assert len(manifest['files'])==12 and {r['path'] for r in manifest['files']}|{'manifest.json'}=={p.name for p in P.iterdir()}
for r in manifest['files']:check(P/r['path'],r)
for r in inner:check(Path(r['path']),r)
# Root's mutable canonical row remains historical; published/preparation identity is checked directly.
for r in outer:
 if '/wiki/' not in r['path']:check(Path(r['path']),r)
plan=load(PRE/'plan.json');assert plan['caller_window'] is None and plan['helper']['length']==16
sel=load(ROOT/'selection.json');receipt=load(ROOT/'receipt.json');status=load(P/'status.json');inv=load(P/'invocation-before.json')
check(Path(sel['manifest']['path']),sel['manifest']);check(Path(sel['full_source_read']['path']),sel['full_source_read'])
assert sel['argv']==['python3','-B',*status['argv']]
assert sel['selected_utc']<status['started_utc']<inv['started_utc']<status['finished_utc']<receipt['finished_utc']
assert receipt['exit']==0 and status['tool_exit']==0 and status['tool_attempts']==1 and status['tool_returned_pid']==297066 and status['exception'] is None
assert receipt['original_Corpus_children_after']==sel['original_Corpus_children_before']==17
assert status['original_calls']==status['caller_bytes']==manifest['caller_bytes']==0
for k in ['stdout','stderr']:check(Path(receipt[k]['path']),receipt[k])
assert load(ROOT/'stdout.json')==status and (ROOT/'stderr').read_bytes()==b'' and (P/'decoder.stderr').read_bytes()==b''
assert inv['argv']==plan['decoder_argv']
image=Path(plan['image']['path']);check(image,plan['image']);check(Path(plan['tool']['path']),plan['tool'])
with image.open('rb') as f:
 header=f.read(32);assert header.hex()==plan['image_header_hex']
 magic,cpu,sub,kind,count,size,flags,reserved=struct.unpack('<IiiIIIII',header)
 assert magic==0xfeedfacf and cpu==0x100000c and count==53 and size==6944
 commands=f.read(size);assert sha(commands)==plan['load_commands_sha256']
 segments=[];pos=0
 for _ in range(count):
  cmd,n=struct.unpack_from('<II',commands,pos);assert n>=8 and pos+n<=size
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,pos+8)
   segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
  pos+=n
 assert pos==size
 start=0x101482918;maps=[s for s in segments if s['vmaddr']<=start and start+16<=s['vmaddr']+s['filesize']]
 assert maps==[plan['expected_segment']]
 offset=maps[0]['fileoff']+start-maps[0]['vmaddr'];assert offset==21506328
 f.seek(offset);raw=f.read(16)
assert raw==(P/'helper-16.bin').read_bytes() and len(raw)==16 and sha(raw)=='cba624727e9ea81fcbe9f5555fc72ab773fa2b504f5b69a66fd02efc5d2378f5'
words=struct.unpack('<4I',raw)
def ldr64_unsigned(w):
 assert w&0xffc00000==0xf9400000,'not unsigned-offset 64-bit integer LDR'
 return dict(target_register=w&31,base_register=(w>>5)&31,unsigned_offset_bytes=((w>>10)&4095)*8)
def br_register(w):
 assert w&0xfffffc1f==0xd61f0000,'not BR register (nonlink)'
 return (w>>5)&31
# Synthetic bit patterns only; nothing is executed as an instruction.
assert ldr64_unsigned(0xf9400528)==dict(target_register=8,base_register=9,unsigned_offset_bytes=8)
assert br_register(0xd61f03c0)==30
rejected=0
for w in [0xd63f0020,0xd65f03c0,0x14000000]:
 try:br_register(w)
 except AssertionError:rejected+=1
assert rejected==3
loads=[dict(va=hex(start+4*i),**ldr64_unsigned(w)) for i,w in enumerate(words[:3])]
assert [(r['target_register'],r['base_register'],r['unsigned_offset_bytes']) for r in loads]==[(0,0,24),(9,0,0),(1,9,24)]
assert br_register(words[3])==1
found=load(P/'findings.json');assert found['load_fields']==loads
assert found['last_instruction']==dict(va='0x101482924',kind='BR register, non-linking',register=1)
rows=load(P/'decoder.stdout.json');assert len(rows)==4
opcodes=['ldr x0, [x0, 0x18]','ldr x9, [x0]','ldr x1, [x9, 0x18]','br x1']
for i,r in enumerate(rows):assert r['offset']==start+4*i and r['size']==4 and bytes.fromhex(r['bytes'])==raw[4*i:4*i+4] and r['opcode']==opcodes[i]
ex=load(P/'extraction.json');assert ex['raw_sha256']==sha(raw) and ex['file_offset']==offset and ex['selected_mapping']==maps[0] and ex['length']==16
for i,row in enumerate(ex['words']):assert row==dict(va=hex(start+4*i),bytes=raw[4*i:4*i+4].hex(),word=hex(words[i]))
after=[ident(Path(r['path'])) for r in before];assert before==after
report=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),disposition='APPROVED_CONDITIONAL_STATIC_DATA_REGISTER_RESULT_ONLY',required_findings=[],packet=ident(P/'manifest.json'),raw=ident(P/'helper-16.bin'),checker=ident(Path(__file__).resolve()),relationship='Reviewer authored the sealed preparation/metadata stop, not Root execution/findings. This review independently validates actualselected bytes/mapping/bitfields and records; it is not independent approval of my own preparation method or a runtime/behavior criterion.',fresh_scope='All13actualpacketfiles and6Rootexecutionfiles read asdata, exactsealed preparation/pins carried. Full4decoded address/byte/opcode rows read; ESIL strings neither evaluated nor used as semantic evidence. Freshsame16imagebytes/header/loadcommands/fullidentity checked. No other imageword/caller/callee/body, decoder/script/model/original/ESIL/emulator invocation.',integrity=dict(payloads=12,tree_files=13,inner_paired_paths=20,outer_paired_paths=41,outer_scope='Six prepfiles+33publishedmanifests+canonicalCorpus/adoption, not allreleasepayloads. Mutablecanonical row evaluated historically; immutablepublished/prep directly checked.',tool_attempts=1,returned_tool_pid=297066,tool_exit=0,stderr_bytes=0,original_children_before_after=17,caller_bytes=0),image_verification=dict(image=plan['image'],header_hex=header.hex(),load_commands_sha256=sha(commands),selected_mapping=maps[0],file_offset=offset,selected_length=16,selected_raw_sha256=sha(raw)),independent_bitfields=dict(load_mask='word & 0xffc00000 == 0xf9400000',load_fields=loads,branch_mask='word & 0xfffffc1f == 0xd61f0000',branch_register=1,synthetic_controls='Two positive fieldcontrols; three negativeBLR/RET/immediateB patterns rejected. Data-bit arithmetic only.'),result='Under ordinary ARM64 instruction semantics and validstable reachable pointers: X0=load64(entryX0+24); X9=load64(X0); X1=load64(X9+24); nonlink BR X1. Thus the loaded subordinateobject is passed inX0 to the target fetched fromits vptr+24. Local destinationwrites are onlyX0/X9/X1; these fourinstructions do notwriteX8/X30/LR,SP,NZCV ormemory. EntryX1 is overwritten, so no allargumentpreservation claim. Targetexecution/preservation/return remainsunknown.',limits=['The nineexactdirectcallmetadata sites remainunmapped to the desired conditionalbooldescriptor branch; no callerbytes were selected. EntryX0 cannot be equated with projected&local90/plVar21 or actualD358 withouta callsite/ABIjoin.','LocalX8preservation doesnotproveX8containsan indirectresult pointer, local90, orany outputstorage; no returnvalue/signature proof fordelegatedtarget.','No virtualslotword/target/type/name/key content, mpMute==Mute, currentmapadmission, sameunit/model/processorP orpublicMute delivery. Cindirectjumpwarnings remainhistorical projectionlimits; actualfourlocalinstructions nowhave independentbyte-backed registerdescription.','All38Utilityapplicationoutcomes remainU/unexecuted. No requirement/case/signal/default/compatibilitygrade or no-route/completion claim.'],preservation=dict(scope='Own75orotherreportedcount selectedfiles watched after initialrecordreads, before selectedimage/bitfieldverification. Not awhole-session watch.',watched=len(before),before=before,after=after,unchanged=True),root_receipts=[ident(p) for p in sorted(ROOT.iterdir())],application_expected=None,comparison=None,grade=None,new_requirements=0,new_cases=0,new_grades=0,original_instructions_executed=0)
report['preservation']['scope']='Selected scopedfiles watched after initialrecordreads, before own selectedimage/bitfieldverification; not whole-session/workspace proof.'
with OUT.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(disposition=report['disposition'],review=ident(OUT),watched=len(before),unchanged=True)))
