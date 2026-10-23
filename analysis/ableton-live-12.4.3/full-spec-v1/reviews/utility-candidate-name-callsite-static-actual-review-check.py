"""Independent fixed1152B/hash/selectedARM64bitfields. No original or decoder invocation."""
from pathlib import Path
import datetime,hashlib,json,struct
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1')
P=B/'depth-utility-candidate-name-callsite-instruction-data';PRE=B/'depth-utility-candidate-name-callsite-instruction-preparation'
ROOT=B/'reviews/utility-candidate-name-callsite-static-root-execution'
E=B/'reviews/utility-candidate-name-callsite-static-actual-review-evidence.json'
R=B/'reviews/utility-candidate-name-callsite-static-actual-review.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def ident(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
def verify(p,r):
 got=ident(p);assert (got['bytes'],got['sha256'])==(r['bytes'],r['sha256']),str(p)
def signed(x,n):return x-(1<<n) if x&(1<<(n-1)) else x
assert not E.exists() and not R.exists()
ib=load(P/'before-map.json');ia=load(P/'after-map.json');ob=load(ROOT/'before.json');oa=load(ROOT/'after.json')
assert len(ib)==14 and ib==ia['files'] and ia['unchanged']
assert len(ob)==139 and ob==oa
assert len({x['path'] for x in ib})==14 and len({x['path'] for x in ob})==139
assert [json.loads(s) for s in (P/'before-identities.jsonl').read_text().splitlines()]==ib
watch={Path(x['path']) for x in ib+ob}|set(P.iterdir())|set(ROOT.iterdir())|{Path(__file__).resolve()}
before=[ident(p) for p in sorted(watch)]
m=load(P/'manifest.json');assert sha((P/'manifest.json').read_bytes())=='978259139eaf3ade7fe247b924fb978c2ec8a47cd2129f9692fab5cebdb0b60c'
assert len(m['files'])==64 and {x['path'] for x in m['files']}|{'manifest.json'}=={p.name for p in P.iterdir()}
for x in m['files']:verify(P/x['path'],x)
for x in ib:verify(Path(x['path']),x)
for x in ob:
 if '/wiki/' not in x['path']:verify(Path(x['path']),x)
plan=load(PRE/'plan.json');sel=load(ROOT/'selection.json');receipt=load(ROOT/'receipt.json');status=load(P/'status.json')
assert sel['argv']==['python3','-B',*status['argv']]
assert sel['selected_utc']<status['started_utc']<status['finished_utc']<receipt['finished_utc']
for k in ['manifest','full_source_read']:verify(Path(sel[k]['path']),sel[k])
for k in ['stdout','stderr']:verify(Path(receipt[k]['path']),receipt[k])
assert receipt['exit']==0 and (ROOT/'stderr').read_bytes()==b'' and load(ROOT/'stdout.json')==status
assert status['tool_attempts']==status['completed_windows']==9 and status['exception'] is None
assert receipt['original_children_after']==sel['original_children_before']==17
final=load(P/'outcomes-final.json');initial=load(P/'outcomes-initial.json');assert len(final)==len(initial)==9 and len({x['pid'] for x in final})==9
image=Path(plan['image']['path']);verify(image,plan['image']);verify(Path(plan['tool']['path']),plan['tool'])
with image.open('rb') as f:
 header=f.read(32);assert header.hex()==plan['image_header_hex']
 magic,cpu,sub,kind,count,size,flags,res=struct.unpack('<IiiIIIII',header);assert count==53 and size==6944
 commands=f.read(size);assert sha(commands)==plan['load_commands_sha256']
 segments=[];pos=0
 for _ in range(count):
  cmd,n=struct.unpack_from('<II',commands,pos);assert n>=8 and pos+n<=size
  if cmd==0x19:
   name,va,vs,fo,fs,mp,ip,ns,sf=struct.unpack_from('<16sQQQQiiII',commands,pos+8)
   segments.append(dict(name=name.rstrip(b'\0').decode(),vmaddr=va,vmsize=vs,fileoff=fo,filesize=fs,maxprot=mp,initprot=ip))
  pos+=n
 assert pos==size
 raws={}
 for w in plan['windows']:
  start=int(w['start'],16);maps=[s for s in segments if s['vmaddr']<=start and start+128<=s['vmaddr']+s['filesize']];assert maps==[plan['expected_segment']]
  offset=maps[0]['fileoff']+start-maps[0]['vmaddr'];assert offset==w['file_offset']
  f.seek(offset);raw=f.read(128);assert raw==(P/(w['id']+'.bin')).read_bytes();raws[w['site']]=raw
# Encoding masks/operand arithmetic are independent of retained opcode text.
def bl(w,pc):
 assert w&0xfc000000==0x94000000
 return pc+4*signed(w&0x3ffffff,26)
def add64(w):
 assert w&0xff800000==0x91000000
 return (w&31,(w>>5)&31,((w>>10)&4095)<<(12 if w&(1<<22) else 0))
def mov64(w):
 assert w&0xffe0ffe0==0xaa0003e0
 return (w&31,(w>>16)&31)
def adrp(w,pc):
 assert w&0x9f000000==0x90000000
 imm=signed(((w>>5)&0x7ffff)*4+((w>>29)&3),21)
 return w&31,(pc&~4095)+(imm<<12)
def mem(w,tag,scale):
 assert w&0xffc00000==tag
 return (w&31,(w>>5)&31,((w>>10)&4095)*scale)
def cond_target(w,pc):
 if w&0xff000000==0xb4000000:
  return 'cbz64',w&31,pc+4*signed((w>>5)&0x7ffff,19)
 assert w&0xff000010==0x54000000
 return 'b.cond',w&15,pc+4*signed((w>>5)&0x7ffff,19)
assert add64(0x910103e8)==(8,31,64) and mov64(0xaa1c03e0)==(0,28)
assert bl(0x97bb012a,0x1025c2470)==0x101482918
assert adrp(0xf00210e8,0x1025c24b4)==(8,0x1067e1000)
results=[];typed=[];rows_count=0;allwords={}
for i,(w,outcome,init) in enumerate(zip(plan['windows'],final,initial)):
 site=int(w['site'],16);start=site-16;raw=raws[w['site']];words=struct.unpack('<32I',raw);label=w['id']
 assert init['site']==outcome['site']==w['site'] and init['status']=='not_attempted'
 assert outcome['status']=='decoded32byteexactrows' and outcome['tool_attempts']==1 and outcome['tool_exit']==0 and outcome['exception'] is None
 assert load(P/(label+'.receipt.json'))==outcome and (P/(label+'.stderr')).read_bytes()==b''
 inv=load(P/(label+'.invocation-before.json'));assert inv['argv']==w['decoder_argv'] and outcome['started_utc']<=inv['started_utc']<outcome['finished_utc']
 ex=load(P/(label+'.extraction.json'));assert ex['va']==hex(start) and ex['length']==128 and ex['raw_sha256']==sha(raw) and outcome['raw_sha256']==sha(raw) and ex['file_offset']==w['file_offset'] and ex['call_target']=='0x101482918'
 rows=load(P/(label+'.stdout.json'));assert len(rows)==32
 for j,row in enumerate(rows):
  assert row['offset']==start+4*j and row['size']==4 and bytes.fromhex(row['bytes'])==raw[4*j:4*j+4]
  allwords[row['offset']]=words[j]
 rows_count+=len(rows)
 assert bl(words[4],site)==0x101482918
 assert add64(words[2])==(8,31,64) and mov64(words[3])==(0,22 if i==0 else 28)
 literals=[]
 for j in range(31):
  if words[j]&0x9f000000!=0x90000000:continue
  reg,page=adrp(words[j],start+4*j)
  if words[j+1]&0xff800000!=0x91000000:continue
  rd,rn,imm=add64(words[j+1])
  if rd==rn==reg:
   entry=dict(va=hex(start+4*j),register=reg,address=hex(page+imm));literals.append(entry)
   if page+imm==0x1067e1d18:typed.append((w['site'],start+4*j))
 results.append(dict(site=w['site'],raw_sha256=sha(raw),all32rows_byteexact=True,entry_helper_X8='SP+0x40',entry_helper_X0='X22' if i==0 else 'X28',adjacent_ADRP_ADD_literals=literals))
assert rows_count==288 and typed==[('0x1025c2470',0x1025c24b4)]
assert sum(len(r['adjacent_ADRP_ADD_literals']) for r in results)==17
assert sum(e['address']=='0x1067e18f8' for r in results for e in r['adjacent_ADRP_ADD_literals'])==8
assert results==load(P/'findings.json')['window_results']
def at(va):return allwords[va]
assert mem(at(0x1025c24bc),0xf9000000,8)==(8,25,0)
assert mem(at(0x1025c24c0),0xf9400000,8)==(8,28,0)
assert mem(at(0x1025c24c4),0xf9400000,8)==(8,8,0x330)
assert mov64(at(0x1025c24c8))==(0,28)
assert at(0x1025c24cc)&0xfffffc1f==0xd63f0000 and (at(0x1025c24cc)>>5)&31==8
assert mem(at(0x1025c24d0),0x39000000,1)==(0,25,0x28)
assert cond_target(at(0x1025c249c),0x1025c249c)==('cbz64',0,0x1025c24b4)
assert cond_target(at(0x1025c24ac),0x1025c24ac)==('b.cond',1,0x1025c24b4)
assert mem(at(0x1025c24a0),0xb9400000,4)==(8,0,0)
subs=at(0x1025c24a4);assert subs&0xff800000==0x71000000 and (subs&31,(subs>>5)&31,(subs>>10)&4095)==(8,8,1)
assert mem(at(0x1025c24a8),0xb9000000,4)==(8,0,0)
assert bl(at(0x1025c24b0),0x1025c24b0)==0x101449efc
assert bl(at(0x1025c2478),0x1025c2478)==0x10128ed98 and bl(at(0x1025c248c),0x1025c248c)==0x1012908d8
assert mem(at(0x1025c2490),0xf9000000,8)==(0,25,24) and mem(at(0x1025c2494),0x39000000,1)==(1,25,32)
# Four finite operand/literal rejection controls, not executed instructions.
assert adrp(at(0x1025c24b4),0x1025c24b4)[1]+add64(0x9135c108)[2]!=0x1067e1d18
assert mem(at(0x1025c24bc)^(1<<5),0xf9000000,8)!=(8,25,0)
assert mem(at(0x1025c24c4)^(1<<10),0xf9400000,8)!=(8,8,0x330)
assert cond_target(at(0x1025c24ac)^1,0x1025c24ac)!=('b.cond',1,0x1025c24b4)
source=load(B/'depth-utility-mute-model-routing/records.json')['functions'][26]['record']['code'].splitlines();context='\n'.join(source[460:474])+'\n'
assert 'PTR_thunk_FUN_10128edf8_1067e1d18' in context and '0x330' in context
# Readback of selected old C context only; no additional body or callee retrieval.
after=[ident(Path(r['path'])) for r in before];assert before==after
with E.open('x') as f:json.dump(dict(checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checker=ident(Path(__file__).resolve()),before=before,after=after,unchanged=True,window_results=results,selected_bool_source_context=dict(provider=str(B/'depth-utility-mute-model-routing/records.json'),pointer='/functions/26/record/code',lines_1based_inclusive=[461,474],text=context,sha256=sha(context.encode())),independent_operand_checks='All9centralBL,9ADDSP/MOV,17adjacentADRPADD pairs; selectedtypedstore/330loads/BLR/byte-store and2branchjoin/load/subs/store/directcall fields; four rejection variants',actual_new_original_or_decoder_invocations=0),f,indent=2);f.write('\n')
report=dict(reviewed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),disposition='APPROVED_CONDITIONAL_SELECTED_WINDOW_REGISTER_AND_SOURCE_CORRELATION_ONLY',required_findings=[],packet=ident(P/'manifest.json'),reviewer_evidence=ident(E),reviewer_checker=ident(Path(__file__).resolve()),relationship='Reviewer authored preparation and flagged sharedvptr ambiguity, but not Root selection/execution/findings. This review freshly independently verifies actualbytes/bitfields/correlation; it is not selfapproval of my own method or any behavior criterion.',fresh_scope='All288address/byte/opcode rows read in two untruncated compact projections, all9outcomes and64payload identities/65actualtreefiles checked, allRootreceipts and14/139pairedmaps assessed. Independent rawbitfields cover the significant claims listed in evidence, not a new general ARMdecoder for everyopcode. Exact7910Bpreparation source/readiness carried at pinned identity; relevantC461–474context reread only. ESIL strings not evaluated. No outofwindow instruction/source/body/callee/targetword or decoder/runner/native invocation.',integrity=dict(payloads=64,tree_files=65,windows=9,selected_bytes=1152,byteexact_rows=288,decoder_attempts=9,returned_pids=[r['pid'] for r in final],decoder_exits=[r['tool_exit'] for r in final],stderr_bytes=0,inner_paired_paths=14,outer_paired_paths=139,outer_scope='Newprep5+33publishedmanifests+R7canonical/adoption+frozenR1v5stage89/preflight10, not allreleasepayloads. Mutablecanonical evaluated asof; otherfrozen rows directlychecked.',original_children_before_after=17,own_watch_paths=len(before),own_watch_unchanged=True),results=dict(all9_local_setup='AllcentralBLtarget101482918; ADDX8,SP,40 andMOVX0,X22 at2058, X28 atother8. This identifies localnative arguments, not actualcandidate provenance.',literal_discriminator='All17adjacentADRP/ADDpairs independently reconstructed. Shared1067e18f8 occurs8times and providesno boolidentity. Onlyselected2470window builds1067e1d18 at24b4/24b8 andSTRX8,[X25] at24bc.',typed_context='24c0LDRX8,[X28];24c4LDRX8,[X8+330];24c8MOVX0,X28;24ccBLRX8;24d0STRBW0,[X25+28]. With existingCtypedvptr/virtual330/+28context, this conditionally associates2470withthat descriptorbranch without ordinalmatching.',local_control='249cCBZX0 and24acB.NE eachtarget24b4. The nonzero path loads/decrements/stores a32bitcounter; zero decrement calls101449efc at24b0 before normalreturnfallthrough. Under normalcallee-saveX25/X28/validstack/pointer/nointerference premises, these local representedpaths converge into the typedstore/330sequence. No callee body or branch outside selectedwindows followed.',name_storage='Afternamehelpercall, localbasehelpercall2478 andcommonvptrstore2484 precede2488ADD X0,SP,40 and248cBL1012908d8; returnedX0/W1 storedintoX25+18/+20 at2490/2494. This narrows stack/descriptor carrier layout, not actualnamecontents or hidden target output semantics.',helper_composition='Previouslyreviewedhelper16preservesentryX8 locally and tails to loadedobject(entryX0+18). Combined with new localcallsetup, conditionalreached2470suppliesX28 andSP+40. No actualD358 or target return/outputproof follows.'),premises_and_limits=['Normalreturn/callee-saveX25/X28, stablevalidobjects/stack, successfulallocation and nointerferinghelper/reentrancy effects. Caller non-return projectionwarnings do not establish runtimebehavior.','Unique association only within these9selectedwindows and this literal/control pattern, not wholeprogram/globaluniqueness or actualpathreachability. All9results retained, no suppressed mismatch and no ordinals.','X28origin/actualD358/admission, currenttype/name/key/map contents, emittedunit/samemodel/processorP/publicgesture remainU. SP+40 is a local outputcarrier candidate, not proof delegatedtarget writes it or returns a specificstring.','No scheduling/latency/timing/numericDSP/default/invariance/compatibility/absence/no-route or completion claim. All38Utilityapplicationoutcomes remainU/unexecuted; no requirements/cases/grades.'],image_scope=dict(image=plan['image'],header_sha256=sha(header),load_commands_sha256=sha(commands),unique_segment=plan['expected_segment'],extraction='Freshonlysame9fixed128Bwindows/1152Bafterfullidentity/headerchecks; nohelper16reread or otherimageword'),negative_controls='Four meaningful valid-encoding perturbations fail the selectedtypedliteral/storebase/330offset/NEcondition predicates. No suppliedchecker/decoder replay.',application_expected=None,comparison=None,grade=None,new_requirements=0,new_cases=0,new_grades=0,original_instructions_executed=0)
with R.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(dict(review=ident(R),evidence=ident(E),watch=len(before),status=report['disposition'])))
