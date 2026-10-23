"""Produce source-anchored analyst records from the fixed27 retained data only."""
from pathlib import Path
import collections
import hashlib
import json
import re

P = Path(__file__).resolve().parent
R = P.parents[3]
B = P.parent


def sha(b):
    return hashlib.sha256(b).hexdigest()


def save(name, data):
    with (P / name).open('x') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def pin(path, role):
    b = path.read_bytes()
    return dict(path=str(path), bytes=len(b), sha256=sha(b), role=role)


PREMISES = [
    'Recovered C projection only; signature, hidden arguments, register values and pointer types are not a validated native ABI.',
    'Normal flow with legal live receiver, valid complete storage, correct alignment/lifetimes, initialized callback and helper state.',
    'List/vector/count bounds and ownership invariants hold; no concurrency/reentrancy/memory-ordering guarantee is proved by LOAcquire/LORelease spellings.',
    'All unread direct helpers and indirect callbacks remain opaque, including their arguments, writes, exceptions and results.',
    'Weak section-defined declaration and same-address export navigation do not establish actual stub destination, interposition, provider or current runtime dispatch.',
    'Packed stack locals and word stores are recovered projections, not complete message layouts, channel identities, units, sample counts or audio laws.',
    'Warning-bearing paths establish no total native control-flow, public failure, throw, refusal or successful-return law.',
    'No actual current UI parameter, loaded engine/voice, scheduler clock, audio buffer, feedback reader or host consumer is bound.'
]

# Inclusive retained C-line ranges. Text below is analyst interpretation, never a copied body.
SPEC = {
 '0x101cba2bc': [
  (27,62,'base/handle','Calls opaque base/message helpers and writes a table candidate, manager-derived field and a refcounted handle projection; this/plVar4 identity and complete object ownership remain unproved.'),
  (63,81,'module','Manager-leading int is converted to float and passed with an allocated module-like pointer to opaque setup; that pointer is stored at this+0x80. No legal rate/default/constructor completion inferred.'),
  (82,124,'callback-fields','Stores named member-wrapper pointer candidates and this pointers at six embedded nodes. Their names suggest rate/tempo/transport/time-jump/prebuffer roles; no pointee bodies or delivery inspected.'),
  (125,146,'local-initialization','Initializes callback/cache/input-pointer/flag-like fields. These zeros are conditional local stores, not public bypass/default/audio semantics.'),
  (147,171,'capacity','Queries opaque manager state then conditionally reallocates/copies the 0x38/0x40/0x48 vector projection. Negative path carries a nonreturn warning; no allocation/error/lifetime law.')],
 '0x101d43638': [
  (30,63,'base/handle','Calls opaque base/message helpers, writes a table candidate and refcounted handle fields. ChannelEq handle refcount+0x14 differs from AutoFilter+0x3c; object identities remain conditional.'),
  (64,71,'module','Converts manager-leading int to float, allocates0x600 and delegates setup with local state, storing the returned word at this+0x80; no rate/default/receiver proof.'),
  (72,114,'callback-fields','Stores six named member-wrapper candidates and same-this field values; registration and later delivery are separate joins.'),
  (115,133,'local-initialization','Clears cache/input-pointer/flag-like fields and installs a local callback/table candidate; these are not public defaults or parameter delivery.'),
  (134,158,'capacity','Conditional vector-capacity allocation/copy follows opaque manager queries; warning-bearing failure path is not a public failure law.')],
 '0x101cbb4f0': [
  (20,36,'state-gates','this+0x1e9, lowbit+0x1e8, opaque helper result xor1 and cached+0x1ea gate early returns/transitions; no bypass/enable meaning adopted.'),
  (37,70,'transition','Delegates module+0x19e0 transition/configuration, optional0x38-stride callbacks and a local function pointer with words0x3f800000/0; pointer semantics and output remain opaque.'),
  (72,87,'publication','Conditionally clears selected handle payload words, updates selector/header under recovered lock spellings and clears+0x220. No reader, atomic protocol or audio silence proof.')],
 '0x101d447dc': [
  (20,36,'state-gates','Same field-shaped gates, with ChannelEq opaque predicate at module+0x3d0; field meaning remains unknown.'),
  (37,68,'transition','Delegates transition/configuration and optional0x38-stride callbacks, then invokes current function pointer with0x3f800000 or0; no callback target established.'),
  (70,81,'publication','Conditionally clears a selected two-byte payload and rewrites selector/header, then clears+0x220. Not the AutoFilter payload format or an audio result.')],
 '0x101cbb67c': [
  (32,100,'admission/tag-projection','Opaque admission helper precedes kind1/2/3/6/8 branches mapping to local tags0/1/2/2/3 and field words; only+0x1e9==1 proceeds. Native event/MIDI codec and carried register value remain unknown.'),
  (101,146,'queue-write','Uses0x38/0x40/0x48 pointers and32-byte recovered records, with conditional append/allocation/copy/free. Capacity legality and helper semantics are premises, not observed runtime.'),
  (149,161,'full/error-frontier','Full/nonempty projection overwrites selected final-record words with opaque DAT_10584f260/tag2; empty/failure paths delegate warning-bearing helpers. No observed note-off/all-notes-off/drop/error law.')],
 '0x101d4494c': [
  (31,98,'admission/tag-projection','Opaque admission followed by kind1/2/3/6/8 local tag projection and+0x1e9==1 gate; no public MIDI key/velocity/controller codec or ownership law.'),
  (99,144,'queue-write','Conditional32-byte record append/reallocation with recovered fields and carried register; no valid complete input recipe or same-instance consumer supplied.'),
  (147,159,'full/error-frontier','Nonempty/full last-record overwrite references unread DAT_10584f260; empty/error helpers include a nonreturn warning. No public failure or reset behavior.')]
}

INIT = {
 '0x101cbaf5c':(13,21,22,76,77), '0x101d44288':(13,21,22,76,77),
 '0x101df4630':(12,20,21,75,76), '0x101ec367c':(12,20,21,75,76),
 '0x101fafbe4':(12,20,21,75,76), '0x101fb2d28':(11,19,20,74,75),
 '0x101fb5aac':(12,20,21,75,76)
}
EXIT = ['0x101cbb1b0','0x101d444b4','0x101df485c','0x101ec38a8','0x101fafe10','0x101fb2f7c','0x101fb5cd8']
CALC = {
 # gate, callback-loop, device dispatch/cache/counter, publication, inactive/scheduling/tail
 '0x101cbb984':[(29,43),(44,58),(59,67),(68,85),(91,123)],
 '0x101d44c54':[(25,39),(40,52),(53,59),(60,74),(80,108)],
 '0x101df5080':[(23,37),(38,50),(51,55),(56,70),(76,103)],
 '0x101ec4054':[(28,41),(42,54),(55,59),(60,78),(84,118)],
 '0x101fb0634':[(23,36),(37,49),(50,54),(55,69),(75,100)],
 '0x101fb380c':[(60,72),(73,87),(88,97),(98,144),(150,238)],
 '0x101fb6490':[(25,39),(40,52),(53,59),(60,77),(83,115)]
}
for entry,(a,b,c,d,e) in INIT.items():
 SPEC[entry]=[
  (a,b,'configuration','Loads wrapper-shaped+0x80/+0x30, obtains scheduler-like state through opaque helpers and delegates leading-word/byte/opaque-clock arguments to device-offset helpers. No rate/tempo/playing semantics or units established.'),
  (c,d,'list-link','Projects five embedded nodes at+0x88/+0xb8/+0xe8/+0x118/+0x148 into manager lists+0x330/+0x270/+0x2a0/+0x2e8/+0x300 with link/tail stores. Valid initialized list ownership and no interfering mutation required.'),
  (e,e,'registration-frontier','Calls FUN_101ab1bfc(manager-like+0x30,node+0x178). Its body and scheduler execution/delivery are unread; recovered Init(OScheduler*) type does not validate native receiver ABI.')]
for entry in EXIT:
 end=174 if entry=='0x101fb2f7c' else 184
 SPEC[entry]=[
  (15,end,'list-unlink','Conditionally updates five lists and embedded-node neighbor/head/tail links, clears backpointers and delegates FUN_101ab1db0(manager,node+0x178). Requires valid membership/links/lifetime. Exit does not here prove destruction, resource release, host teardown completion or callback quiescence.')]
for entry,ranges in CALC.items():
 texts=[
  ('state-gates','Wrapper fields+0x1e9/+0x1e8/+0x1ea plus an opaque device predicate determine active/inactive paths. Names and booleans do not establish public enable, bypass, Freeze, silence or tail laws.'),
  ('callback-loop','Under the active projection, iterates an opaque module count in0x38-stride callback entries. Current code pointers, receiver/control units, valid count, arguments, ordering/reentrancy and side effects remain unbound.'),
  ('dispatch/cache','Dereferences selected input-like word pointers, delegates a device-specific opaque helper, stores two32-bit cached words at+0x1c8/+0x1cc and increments a module field. No channel/buffer/rate/sample-counter/DSP interpretation or legal domain is proved.'),
  ('feedback-publication','Obtains a helper-written packed stack projection and conditionally copies selected words into a handle-selected payload, updating header/selector under recovered lock spellings. Payload units, layout, consumer and concurrency remain unknown.'),
  ('inactive/schedule/tail','Inactive paths conditionally zero cache or selected feedback words and may enqueue a local node through FUN_101ab1648; the common projected tail rewinds+0x40 to+0x38. This is not public silence, flush, scheduling, reset or no-more-events proof.')]
 SPEC[entry]=[(a,b,k,t) for (a,b),(k,t) in zip(ranges,texts)]
 if entry=='0x101fb380c':
  SPEC[entry].append((88,93,'queued-record-forwarding','Roar alone in the selected seven CalcMain projections visibly walks+0x38..+0x40 by0x20 and calls FUN_10402fabc(module+0x5780,record), before FUN_10402f120. No public event codec, timing/order effect or absence in other device stages inferred.'))


def main():
 census=json.loads((P/'candidate-census.json').read_text())
 receipt=json.loads((P/'source-retention.json').read_text())
 rows=[json.loads(x) for x in (P/'sources.jsonl').read_bytes().splitlines()]
 assert set(SPEC)=={d['entry'] for d in rows}
 symbols=json.loads((B/'depth-devicekit-provider-inventory-v1/symbols.json').read_text())['symbols']
 actual=json.loads((B/'depth-devicekit-selected-symbols-v1/root-readback.json').read_text())['rows']
 claims=[];frontiers=[];declaration_joins=[]
 for i,(d,m) in enumerate(zip(rows,census['records']),1):
  entry=d['entry'];lines=d['code'].splitlines(keepends=True)
  ss=[x for x in symbols if x['lexical_symbol']=='<EXTERNAL>::'+m['alias_name']];assert len(ss)==1
  aa=[x for x in actual if x['raw_nlist_fields']['n_value']==int(entry,16)];assert len(aa)==1
  s,a=ss[0],aa[0]
  assert a['stub_address'] in s['stub_addresses'] and a['source_rows']==s['boundary_rows'] and a['external_labels']==[s['external_label']]
  declaration_joins.append(dict(entry=entry, retained_alias=m['alias_name'], stub_declaration=a['stub_address'], nlist_index=a['nlist_index'], n_type=a['raw_nlist_fields']['n_type'], n_desc=a['raw_nlist_fields']['n_desc'], boundary_rows=s['boundary_rows'], external_label=s['external_label'], actual_stub_destination=False, provider_binding=False, same_current_receiver=False, relation='reviewed retained declaration value -> exact selected retained export entry; conditional source navigation only'))
  statements=[]
  for j,(lo,hi,kind,text) in enumerate(SPEC[entry],1):
   assert 1<=lo<=hi<=len(lines)
   span=''.join(lines[lo-1:hi]).encode()
   statements.append(dict(id=f'DKS-{i:02}-{j:02}',kind=kind,C_start=lo,C_end=hi,span_utf8_bytes=len(span),span_sha256=sha(span),status='observed-static-projection',statement=text,premises=list(range(1,9)),public_route=False,complete_callable_leaf=False))
  claims.append(dict(entry=entry,alias=m['alias_name'],source_row=i,source_metadata=m,read_C_lines=[1,len(lines)],complete_C_read=True,warnings=d['warnings'],native_extent_basis='retained export metadata only; no fresh native bytes or PC/C pairing',statements=statements,legal_inputs=None,stub_recipe=None,expected_output=None,execution_ready=False,math_leaf=False))
  refs=[]
  for n,line in enumerate(lines,1):
   for call in re.finditer(r'\b((?:thunk_)?FUN_[0-9a-f]+)\s*\(',line):
    refs.append(dict(C_line=n,token=call[1],kind='lexical-direct-call',target_body_read=call[1].replace('thunk_FUN_','0x').replace('FUN_','0x') in SPEC,followed=False))
   if '(*(code *)' in line or '(**(code **)' in line or '(*pcVar2)' in line:
    refs.append(dict(C_line=n,token=line.strip(),kind='indirect-expression',target_body_read=False,followed=False))
  frontiers.append(dict(entry=entry,references=refs,scope='Lexical C expressions only, not independently indexed/native callsites. Encountered targets remain unselected; matching selected body identity, if any, does not authorize argument/edge composition.',legal_whole_function_X=False,missing=['native ABI and same current object','complete helper/callback contracts and effects','valid initialized storage/lifetime/counts','control/sample/clock and public consumer binding'],new_original_batch=None))
 save('claims.json',dict(schema='fixed27-source-claims-v1',claims=claims,premises=PREMISES,unit='conditional source statements, not required outcomes, grades or indirect-site resolutions'))
 save('call-frontiers.json',dict(schema='selected-C-frontiers-no-follow-v1',records=frontiers,encounter_follow=False,new_native_or_provider_reads=0,successor_selected=False))
 save('declaration-source-joins.json',dict(schema='conditional-declaration-export-navigation-v1',joins=declaration_joins,source_occurrences=sum(len(x['boundary_rows']) for x in declaration_joins),runtime_binding=False,new_resolved_sites=0))
 protected=[pin(P/n,'Root-owned frozen selection/census') for n in ['candidate-census.json','metadata-census-root.py','selection-metadata-only.json','selection-source-read.json']]
 predecessors=[('component-resolution-v1/manifest.json','approved component1a'),('integration-structure-v1/manifest.json','approved integration1b'),('depth-devicekit-provider-inventory-v1/manifest.json','approved37occurrence inventory'),('depth-devicekit-provider-inventory-v1/symbols.json','exact27symbol37boundary navigation'),('depth-devicekit-selected-symbols-v1/manifest.json','approved declarations capture'),('depth-devicekit-selected-symbols-v1/root-readback.json','reviewed declaration values only'),('reviews/devicekit-selected-symbols-actual-review.json','full fresh review read'),('reviews/devicekit-provider-inventory-v1-review.json','inherited inventory approval'),('family-filter-eq-routes-v1/manifest.json','inherited family cut'),('family-dynamics-routes-v1/manifest.json','inherited family cut'),('family-distortion-routes-v1/manifest.json','inherited family cut')]
 save('pins.json',dict(protected_root=protected,immutable=[pin(B/p,r) for p,r in predecessors],asof=[pin(R/'wiki/research/program-structure.md','canonical crossfamily context; as-of not futuregate'),pin(R/'wiki/research/full-live-specification-plan.md','amendedrev4 selector; as-of not futuregate')],source_chunks='Eight exact inherited chunk identities in census/retention; checker never reopens them. Selected raw ranges freshly hashed once.'))
 save('read-receipt.json',dict(schema='fixed27-fresh-source-read-v1',fresh_semantic_read=dict(records=27,C_utf8_bytes=121309,C_lines=3601,warning_records=4,whole_bodies=True,all_selected_metadata=True),fresh_data_read=dict(selected_raw_bytes=receipt['selected_raw_bytes'],retained_sha256=receipt['retained_sha256'],selected_ranges_once=True,chunk_full_rehash=False,root_selection_and_census=True,actual_review_complete=True,provider_inventory_structure_and_symbols=True),inherited='Prior1a/1b/family/manual/source-audit semantics, original chunk/index custody and original image identities. No full prior release/audit replay.',scope='All27 full C strings and record metadata freshly read in five bounded displays (6+6+6+6+3), with all four warnings; not a sourcegeometry-only claim. No fresh native extent/ABI proof.',source_read_successor=False,original_model_comparator_runs=0,canonical_or_shared_writes=0))
 save('assessment.json',dict(schema='whole27-source-frontier-assessment-v1',status='PENDING_INDEPENDENT_SOURCE_REVIEW',selection='whole27 records across seven DeviceKit template families',records=27,methods=dict(constructor_candidates=2,Init=7,Exit=7,UpdateOutX=2,OnMidi=2,CalcMain=7),conditional_source_relationships=['manager/list initialization and unlink patterns','module-offset opaque configuration and device dispatch','gated cache/feedback publication and scheduling','two event-tag/queue projections and Roar record forwarding'],complete_callable_math_leaves=0,complete_callable_X_leaves=0,ready_original_batches=0,legal_inputs=None,calibrated_metric=None,runtime_stub_binding=False,actual_provider_binding=False,actual_current_parameter_binding=False,actual_audio_or_host_delivery=False,new_site_credit=0,new_required_outcomes=0,new_case_grade_release=0,existing_inventory=dict(resolved_reference=25071,conditional_class=24,total=25095,all_indirect=268015),warning_limits='Four nonreturn warnings qualify error/control-flow claims. No observed throws/refusals/success, no exhaustive native/failure law.',body_limits='All27record/alias thunkfalse and retained native extents308..756B are metadata only; no native code or complete ABI proof.',setup_gate='Any future non-self-contained initialization/construction, patched/new-tool or full device execution requires separate selection and applicable preparation/review. No run selected here.',coverage_gate='OPEN',required_unsupported='U',documentary_fallback=False,successor_selected=False))
 print(json.dumps(dict(records=len(rows),claims=sum(len(x['statements']) for x in claims),references=sum(len(x['references']) for x in frontiers),joins=len(declaration_joins))))


if __name__=='__main__':
    main()
