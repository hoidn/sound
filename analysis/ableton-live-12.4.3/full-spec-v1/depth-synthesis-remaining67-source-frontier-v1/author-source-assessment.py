"""Author anchored conditional assessments from the owned fixed67 retained source only."""
from pathlib import Path
import collections
import hashlib
import json
import re

P=Path(__file__).resolve().parent


def sha(b):return hashlib.sha256(b).hexdigest()


def save(n,d):
    with (P/n).open('x') as f:json.dump(d,f,indent=2);f.write('\n')


SPEC={
0:('indirect-dispatch','Recovered virtual+0x20 then+8 expressions with jump-table/indirect-as-call warnings; actual receiver/targets/order/failure behavior unknown.'),
4:('expanded-init-projection','Expanded4B Init wrapper projection stores scheduler-like pointers and delegates subobject initialization/conversion/cache/registration helpers. All operations belong to recovered expanded C, not proven4Bnative implementation or inspected target body.'),
5:('exit-helper-wrapper','Delegates repeated object-offset helper calls and final+0x888 cleanup-shaped helper; no complete destruction, quiescence or public lifecycle result.'),
6:('expanded-reset-projection','Expanded4B Reset projection clears local fields, invokes opaque helpers and unresolved callbacks with condition/history gates. WarningPCs differ from selected wrapperentry; no full native target/CFG/reset/audio law.'),
7:('expanded-note-on-projection','Expanded4B OnNoteOn projection sets flags, branches on controls, delegates helpers/callbacks and contains tanf/coefficient-shaped arithmetic under field gates. Parameter domains/units/receiver, target extent, FP/library and consumer unknown; no standalone filter/math/audio law.'),
8:('expanded-note-off-projection','Expanded4B OnNoteOff projection gates helper calls and forwards to an unresolved callback; event codec/latch/release/audio and native target behavior remain unknown.'),
15:('event-helper-wrapper','Delegates cache/object-offset helpers under a field flag and forwards object/event-like arguments. Named cache/OnNote context does not prove admitted MIDI, note ownership, current voice or audio.'),
16:('event-helper-wrapper','Delegates cache/conditional state helpers and named stopTracking; opaque helper predicate/receiver/event history prevent a full note-off/voice/lifecycle rule.'),
17:('control-dispatch-projection','Branches on input+0x18 kind-like values -2/-1/1/0x40/0x78, opaque conversion helpers and callbacks; conditional loop over flags. Unrecovered jump tables/indirect-as-call warnings preclude repaired native control/MIDI/ordering/error law.'),
18:('control-cache-wrapper','Tests input kind-like -2/-1/0x4a, uses opaque sentinel conversion and named per-note cache method, conditional callback and final helper. Public controller codec, state ownership and output remain unknown.'),
28:('expanded-filter-reset-projection','Expanded4B filter Reset projection selects local flag stores0x101 and helper paths under field/tag gates. Underlying targetbody/ABI/helper/state/filter mode and effect unknown; no native reset/algorithm inference.'),
29:('filter-note-on-wrapper','A byte+0x41b0 gates two opaque helpers; no legal receiver/note codec or audible/filter/envelope behavior established.'),
31:('lfo-init-copy-wrapper','Delegates scheduler-like helper and copies returned object+0x1c word into receiver+8. Word units/current rate/clock/lifetime and consumer are unknown.'),
32:('voice-exit-wrapper','Calls one opaque helper on receiver+0xc88; name/offset supplies no voice destruction or host teardown result.'),
33:('voice-reset-wrapper','Writes zero through linked pointer+0xc60/+0x24 and calls named per-note cache reset with recovered omitted arguments. Legal current storage/history/ABI and full reset result unknown.'),
34:('voice-enable-projection','Stores0.001<input into+0xc78; lower branch combines opaque predicate, count/flag iteration and callback. Threshold is local source expression, not public On/automation/voice allocation or note-off law.')}
DELETE={3,10,21,25,27}
CLEANUP={11,12,13,14,22,23,35,36,37,38,39,40}
SIZED={42,44,46,48,50,52,54,56,58}
SPECIAL_ANCHORS={0:[(5,8)],4:[(16,24),(25,46)],5:[(9,18)],6:[(14,48),(49,84)],7:[(17,57),(58,136),(137,143)],8:[(9,24)],17:[(12,28),(30,73)],18:[(8,18)],28:[(13,65)],29:[(9,14)],30:[(9,9)],31:[(11,13)],32:[(9,10)],33:[(9,12)],34:[(13,26)]}
PREMISES=[
 'Conditional retained decompiler projection only; no new native bytes, instruction/C pairing, validated ABI or complete targetfunction extent.',
 'Expanded4B false-thunk projections are not operations proved inside that4Bbody; metadataflags and mismatches remain literal.',
 'Legal live initialized receiver/storage/counts/linked ownership/alignment/history and no interfering mutation are required, not supplied.',
 'All unread direct helpers/library/global/table and dynamic callback targets/effects remain opaque; no callee/slot/native follow.',
 'Warning paths are not total native CFG, observed errors/refusals/crashes/successes or repaired nonreturn/jumptable semantics.',
 'No actual loaded device/current parameter/media/voice/eventcodec/clock/rate/reset/output/host binding is proved.',
 'Arithmetic fragments have no admitted legal argument partition, calibrated oracle, FP/library/ARM-x86 transfer or independent callable recipe.'
]


def main():
    c=json.loads((P/'candidate-census.json').read_text())
    rows=[json.loads(x) for x in (P/'selected-records.jsonl').read_bytes().splitlines()]
    assert len(rows)==67
    records=[];front=[];read=[]
    for i,(r,m) in enumerate(zip(rows,c['records'])):
        assert r['entry']==m['entry'];lines=r['code'].splitlines(keepends=True)
        if i in SPEC:role,obs=SPEC[i]
        elif r['thunk']:
            role,obs='marked-thunk','Shallow marked thunk delegates a named unread target. Tiny4Bextent and rendered C do not inspect fullcallee, prove arguments/ABI, lifecycle role or public behavior.'
        elif i in [1,30]:role,obs='return-only','Complete selected C projection is return-only. No public behavior, destructor/lifecycle meaning or proof of global inactivity follows.'
        elif i in DELETE:role,obs='delete-wrapper','Calls an opaque helper and passes its recovered returned word to operator_delete. No validated receiver/hidden arguments, helper/deallocator body or complete lifecycle law.'
        elif i in SIZED:role,obs='sized-release-wrapper','Calls an unread helper then passes its recovered result plus a literal size to FUN_1012d9770. Size is a callargument, not established allocation/class extent, ABI or deletion law.'
        elif i in CLEANUP:role,obs='cleanup-shaped-projection','Writes table candidates and/or clears/releases linked fields through opaque direct/indirect helpers. Cleanup purpose is inferred; current object identity, complete constructor/destructor, lifetime/error/quiescence and public result unknown.'
        elif i>=59:role,obs='warned-breakpoint-projection','4Bmetadata/nonreturn projection contains SoftwareBreakpoint and indirect call. No observed trap/crash/error/lifecycle law or repaired native CFG; neighboring literal PC is not automatically a selected callee edge.'
        else:raise AssertionError(i)
        body_start=next(n for n,l in enumerate(lines,1) if l.strip()=='{')
        spans=SPECIAL_ANCHORS.get(i,[(body_start+1,len(lines)-2)])
        anchors=[]
        for lo,hi in spans:
            b=''.join(lines[lo-1:hi]).encode();anchors.append(dict(C_start=lo,C_end=hi,span_utf8_bytes=len(b),span_sha256=sha(b)))
        expanded=r['body_bytes']==4 and not r['thunk'] and len(lines)>11
        records.append(dict(id=f'SR{i+1:03}',entry=r['entry'],alias=m['alias_record']['name'],alias_metadata_id=m['alias_metadata_id'],census_pointer=f'candidate-census.json#/records/{i}',source_record=i+1,code_sha256=sha(r['code'].encode()),whole_C_lines=[1,len(lines)],fresh_full_C_read=True,role=role,observation=obs,anchors=anchors,warning_texts=r['warnings'],native_body_bytes=r['body_bytes'],native_body_ranges=r['body_ranges'],record_thunk=r['thunk'],expanded_4B_false_thunk=expanded,extent_basis='retained metadata only; no native instruction/ABI/full-target proof',premises=list(range(1,8)),complete_callable_math_leaf=False,complete_callable_X_leaf=False,public_route=False,legal_inputs=None,expected_result=None))
        references=[]
        for n,l in enumerate(lines,1):
            if n<=body_start:continue
            for match in re.finditer(r'\b((?:thunk_)?FUN_[0-9a-f]+)\s*\(',l):references.append(dict(C_line=n,kind='lexical-FUN-call',token=match[1],followed=False))
            if '(**(code **)' in l or '(*(code *)' in l or '(*pcVar1)' in l:references.append(dict(C_line=n,kind='indirect-expression',token=l.strip(),followed=False))
        front.append(dict(entry=r['entry'],references=references,legal_complete_function_X=False,missing=['same actual receiver/native ABI/extent','complete helper/callback/library/global contracts','legal initialized storage/history/FP domains','current parameter/voice/event/clock/audio/output binding'],new_execution=None))
        read.append(dict(entry=r['entry'],C_lines=[1,len(lines)],C_utf8_bytes=len(r['code'].encode()),code_sha256=sha(r['code'].encode()),method='direct complete numbered C projection; all warning text read',source_semantics='expanded projection only' if expanded else 'conditional retained projection'))
    save('source-assessment.json',dict(schema='fixed67-source-assessment-v1',status='PENDING_INDEPENDENT_SOURCE_REVIEW',records=records,premises=PREMISES,role_counts=dict(collections.Counter(x['role'] for x in records)),complete_callable_math_leaves=0,complete_callable_X_leaves=0,ready_original_batches=0,legal_inputs=None,calibrated_metric=None,existing_inventory=dict(required_clauses=110,actual_U_cases=190,required_predicate_inventory=585,X=0,S=0,no_established_route=585,resolved_indirect_inventory=25095,total_indirect_inventory=268015),new_required_outcome_site_grade_case_release=0,required_unsupported='U',coverage_gate='OPEN',successor_selected=False))
    save('source-read-map.json',dict(schema='fixed67-fresh-full-source-read-v1',records=read,complete_records=67,C_utf8_bytes=29288,C_lines=1231,warning_records=13,warning_occurrences=20,method='All67complete bodies read directly in three numbered displays,indices0..17/18..40/41..66; no lossless representative shortcut or truncation.',fresh='Selected67raw ranges/source semantics/warnings and exact perbody anchors.',inherited='Parent115seed/component/integration/family/owner/manual semantics; completed48Wavetable and23chunk custody; no re-audit/replay.',new_alias_chunk_hash_passes=0,source_expansion=False))
    save('call-frontiers.json',dict(schema='fixed67-lexical-source-dependencies-v1',records=front,references=sum(len(x['references']) for x in front),scope='Lexical FUN/indirect C expressions inside selected bodies only. Functionheaders excluded. Not native/indexed callsites or target resolution; every encountered dependency unselected/unread.',callee_global_slot_native_provider_follow=False,new_original_batch=None,successor_selected=False))
    save('whole-set-claims.json',dict(claims=[
     dict(id='SRC01',scope='all67',claim='Complete remaining reviewed115-minus48 frontier read; no arbitrary omission or class/function completeness claim.'),
     dict(id='SRC02',scope='15markedthunks/30fourBmetadata',claim='Shallow delegation, return-only and warned breakpoint fragments add no native destructor/constructor/callee/ABI or public proof.'),
     dict(id='SRC03',scope='fiveexpanded4Bfalse-thunkrecords',claim='Init/Reset/OnNote projections retain expanded source operations conditionally; no fulltargetbody or alloperations-inside4Bbody claim.'),
     dict(id='SRC04',scope='Operator-qualified initialization/control/event/voicefrontiers',claim='Concrete conditional field/callback/helper relationships and localthreshold/filter-shaped arithmetic remain source-only; no public codec/units/voice/history/timing/filter law.'),
     dict(id='SRC05',scope='cleanup/release-shapedcohort',claim='Table stores/refcounts/linked clearing/helperresult release provide conditional structure only; no complete cleanup/currentobject/quiescence/host result.'),
     dict(id='SRC06',scope='all13warnedrecords/20warnings',claim='Jumptable/indirect-as-call/nonreturn projections are preserved, no nativeCFG/failure/success law repaired.'),
     dict(id='SRC07',scope='whole67 and inheritedfiveprofileowner',claim='No complete callablemath/Xleaf, admitted input/oracle/calibration/currentengine/publicoutput join;0newsite/grade/case/release/outcome,requiredU/OPEN unchanged.')],frontiers=[
     dict(id='SF01',status='OPEN',missing='Legal actual instance/layout/native ABI/lifetime/ownership/history; expanded projection-to-target/native join.'),
     dict(id='SF02',status='OPEN',missing='Unread helper/library/global/table and dynamic callback target contracts; no encountered follow.'),
     dict(id='SF03',status='OPEN',missing='Current control/eventcodec/media/note/voice/count/FP inputs and productive EACH/BOTH/nonzero path before any negative.'),
     dict(id='SF04',status='OPEN',missing='Rate/clock/phase/reset/filter mode/history/Loop-Beat-Sync/publichost and audio consumer/oracle; existingOperator/Meld ambiguities unchanged.'),
     dict(id='SF05',status='OPEN',missing='Error/cleanup/quiescence/teardown/controlflow and fourB/nonreturn target behavior; sourcewarnings not execution.')],new_selection=False))
    print(json.dumps(dict(records=67,anchors=sum(len(x['anchors']) for x in records),roles=dict(collections.Counter(x['role'] for x in records)),lexical_references=sum(len(x['references']) for x in front))))


if __name__=='__main__':main()
