#!/usr/bin/env python3
"""HISTORICAL INITIAL ASSEMBLY ONLY; not final replay. Never execute after approval/freeze."""
import hashlib
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BATCH=HERE.parent/'batch-midi-user-relative-bytes-v1'
OWNER=ROOT/'wiki/specs/midi-user-mapping.md'
NAMES={1:'AccelSignedBit',2:'AccelBinaryOffset',3:'AccelTwoCompliment',4:'AccelSignedBit2',
       6:'LinearSignedBit',7:'LinearBinaryOffset',8:'LinearTwoCompliment',9:'LinearSignedBit2'}
PREFIX='../../analysis/ableton-live-12.4.3/full-spec-v1/'
PACKET='owner-midi-user-r7-relative-bytes-v1/'

def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(d):return json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def identity(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)}
def save(name,d):
    p=HERE/name;assert not p.exists(),name;p.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
def reqs(text):return {m[1]:m[0] for m in re.finditer(r'^### (REQ-MIDI-USER-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',text,re.M|re.S)}
def oldrows(text):return {m[1]:m[0] for m in re.finditer(r'^\| (MT-\d{2}) \|[^\n]*\n',text,re.M)}
def section(text,heading):
    start=text.index(heading);end=text.find('\n## ',start+len(heading));return text[start:end if end>=0 else len(text)]
def source_span(path,first,last):
    p=ROOT/path;b=p.read_bytes();lines=b.splitlines(keepends=True);start=sum(map(len,lines[:first-1]));end=sum(map(len,lines[:last]));raw=b[start:end]
    return {'source':identity(p),'line_span':[first,last],'offset':start,'bytes':len(raw),'sha256':sha(raw),'text':raw.decode()}

def main():
    assert sys.argv[1:]==['--stage-only']
    old=OWNER.read_text();assert sha(old.encode())=='c877decaa447ee773bf49fefd17b93f42c47e406354d6107883a940d32a85aea'
    data=json.loads((BATCH/'inputs.json').read_text());obs=json.loads((BATCH/'observations.json').read_text());results=json.loads((BATCH/'results.json').read_text())
    manifest=identity(BATCH/'manifest.json');assert manifest['sha256']=='2e37f16146ff4c91db95401b67e526db3d5e8a4fb4f62a94b8d7b88609bc0471'
    # The neutral names come from these existing reviewed dictionaries, not the new calls or table display order.
    binding={'entries':[{'native_code':k,'mode_name':v} for k,v in NAMES.items()],
       'source_spans':[source_span('analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/run_pilot.py',85,87),
                       source_span('analysis/ableton-live-12.4.3/r2/x2-midi-v1/run_x2.py',100,102)],
       'meaning':'Inherited reviewed X1/static mode-code association; numeric execution does not observe UI enum selection or actual mapped parameter receiver.',
       'new_calls_establish_UI_binding':False}
    save('mode-binding.json',binding)
    fresh=[];catalog=[];legacy=[];rawcalls={}
    for ci,c in enumerate(results['children']):
        stdout=Path(c['stdout']['path']);offset=0
        for line_number,line in enumerate(stdout.read_bytes().splitlines(keepends=True),1):
            if line.startswith(b'call '):
                call_index=int(line.split()[1]);rawcalls[(c['mode'],call_index)]={'path':str(stdout.relative_to(ROOT)),
                    'line':line_number,'offset':offset,'bytes':len(line),'sha256':sha(line)}
            offset+=len(line)
    child_index={c['mode']:i for i,c in enumerate(results['children'])}
    for i,(r,o) in enumerate(zip(data['rows'],obs)):
        assert r['id']==o['id'] and r['expected_low_xmm0_bits32']==o['low_xmm0_bits32']
        row={'mode_name':NAMES[r['mode']],'native_code':r['mode'],'byte':r['byte'],'batch_row_id':r['id'],
             'batch_input_pointer':f'/rows/{i}','batch_observation_pointer':f'/{i}',
             'expected_reference_x86_bits32':o['low_xmm0_bits32'],'provenance':r['provenance']}
        if r['provenance']=='fresh-selected':
            new_id=f'MUR-REL-{len(fresh)+1:04d}';ci=child_index[r['mode']];j=o['call_index']
            case={'id':new_id,'requirements':['REQ-MIDI-USER-005'],'kind':'H','label':'X',
                'scope':'One finite supplied-UNIT arithmetic evaluation; not an incoming application MIDI message.',
                'input':{'mode_name':NAMES[r['mode']],'native_code':r['mode'],'data_byte':r['byte'],
                    'current_bits32':'3f000000','minimum_bits32':'00000000','maximum_bits32':'3f800000',
                    'range_packed_bits64':'3f80000000000000','prior_bits32':'7f7fffff',
                    'sensitivity_bits32':'3f800000','quantized':False,'reversed':False,'record_bytes_le':r['buffer_le']},
                'action':'Recorded direct supplied-state value-function call after existing unit initialization.',
                'expected_reference_x86':{'low_XMM0_binary32_hex':o['low_xmm0_bits32'],'classification':'finite'},
                'portable_expected':None,'portable_comparator':None,'application_grade':'unknown','candidate_execution':'not-run',
                'prior_case_id':None,'prior_reference_observation':None,
                'precall_oracle':{'classification':r['oracle_class'],'bits32':r['expected_low_xmm0_bits32'],
                                 'meaning':'Existing current-clause static expectation, not a NULL-prior discovery or a fitted replacement.'},
                'source':{'batch_manifest':manifest,'batch_row_id':r['id'],'input_pointer':f'/rows/{i}',
                    'observation_pointer':f'/{i}','receipt_pointer':f'/children/{ci}',
                    'call_pointer':f'/children/{ci}/parsed/calls/{j}',
                    'buffer_pointer':f'/children/{ci}/parsed/buffers/{j-1}',
                    'raw_stdout_call':rawcalls[(r['mode'],j)],'return_projection':'low32 saved XMM0',
                    'mode_binding':'mode-binding.json; inherited existing reviewed X1/static dictionary, not newly observed selection'}}
            fresh.append(case);row['new_case_id']=new_id;row['historical_reference']=None
        else:
            row['new_case_id']=None;row['historical_reference']=r['historical'];legacy.append(row.copy())
        catalog.append(row)
    assert len(fresh)==1006 and len(catalog)==1024 and len(legacy)==18
    save('cases-added.json',{'schema':'finite-midi-relative-cases-v1','cases':fresh})
    save('complete-catalog.json',{'schema':'whole1024-relative-input-provenance-v1','rows':catalog})
    save('inherited-references.json',{'schema':'old18-no-duplicate-cases-v1','rows':legacy})
    release=ROOT/'handoff/midi-config-v4/cases.json';released=json.loads(release.read_text())['cases']
    before={'owner':identity(OWNER),'requirements':[{'id':k,'bytes':len(v.encode()),'sha256':sha(v.encode())} for k,v in reqs(old).items()],
        'MT_rows':[{'id':k,'bytes':len(v.encode()),'sha256':sha(v.encode())} for k,v in oldrows(old).items()],
        'preserved_sections':[{'heading':k,'bytes':len(section(old,k).encode()),'sha256':sha(section(old,k).encode())}
            for k in ['## Inputs and preconditions','## Timing and state','## Errors, cancellation and teardown','## Open questions']],
        'release':{'cases_file':identity(release),'case_count':len(released),'case_object_sha256':[sha(canonical(c)) for c in released]},
        'old_case_counts':'56 MT rows and55 configuration-navigation cases remain unchanged; released161objects immutable.'}
    save('before-identities.json',before)
    paragraph='''- **X (revision 7; finite supplied-state arithmetic only).** The
  [1,006 MUR-REL cases]('''+PREFIX+PACKET+'''cases-added.json)
  record the exact low-binary32 return bits of the supplied x86_64 value
  calculation for their enumerated relative-mode inputs. Every case starts
  independently at current 0.5, range [0,1], not stepped, sensitivity 1 and
  not reversed, with the recorded input data. The
  [complete 1,024-input catalog]('''+PREFIX+PACKET+'''complete-catalog.json)
  covers all eight relative modes and data bytes 0–127, including 18 older
  observations retained by reference rather than repeated as new cases.
  Code-to-mode-name association is inherited from the existing reviewed
  X1/static mapping; these calls do not observe UI enum selection or an
  application's parameter receiver. This finite X scope does not promote the
  general S relative law above, establish ARM/Apple bit equality, or supply
  a portable candidate comparator. See the finite annex below.

'''
    annex='''### Finite supplied-state relative-byte cases added in revision 7

[MUR-REL-0001–MUR-REL-1006]('''+PREFIX+PACKET+'''cases-added.json)
are separately identified H/X cases under REQ-005. The
[complete catalog]('''+PREFIX+PACKET+'''complete-catalog.json)
maps every relative-mode name/code and data byte to one new case or one of
the [18 inherited observations]('''+PREFIX+PACKET+'''inherited-references.json).
The numeric code-to-name association comes from the existing reviewed
[X1/static dictionaries]('''+PREFIX+PACKET+'''mode-binding.json),
not from observed selection of a UI enum or delivery to a mapped parameter.

Each new case records all supplied scalar and 16-byte record bits, exact
native x86_64 reference return bits, the frozen pre-call current-clause oracle
and exact input/observation/receipt/raw-output pointers in the
[whole batch]('''+PREFIX+'''batch-midi-user-relative-bytes-v1/manifest.json).
The action is the recorded direct arithmetic evaluation after its existing
unit initializer. The 1,006 fresh results agree with the frozen static
expectations; they are not NULL-prior discoveries or a repaired model. The
18 older observations gain no new case IDs or invented process receipts.

The expected binary32 bits describe those supplied x86_64 results only;
portable expected output and comparator are null. The existing application
value/τ, repeated-sequence and precision comparators do not become bit-exact
ARM/Apple comparators through this annex. No actual MIDI ingress, parameter
identity/current-value reader/setter, receiver accumulator, 14-bit pairing,
takeover, notification, deferred delivery, display/audio or lifecycle result
follows. Other current/range/stepped/sensitivity axes remain outside this finite
annex. All old S laws, U conditions, precision and history exclusions remain.
Input counts are not required-outcome counts, application grades or a family
denominator. All 56 old MT rows and 161 immutable released objects remain
unchanged; this annex makes no release or candidate compatibility claim.

'''
    evidence='''Revision 7 finite evidence: the [whole relative-byte batch]('''+PREFIX+'''batch-midi-user-relative-bytes-v1/manifest.json)
and its independent actual review (pinned in the owner packet after approval)
support only the enumerated supplied-state annex. The
[owner packet]('''+PREFIX+PACKET+'''README.md)
preserves its actual-review identity, mode-name lineage, complete provenance
catalog and unchanged predecessor clauses/cases. No second observation review
or source/body execution is part of owner assembly.

'''
    revision='| 7 | 2026-10-21 | Adds the fixed supplied-UNIT relative-byte X annex: 1,006 new MUR-REL draft IDs and18 inherited references complete the1,024 logical input catalog. General S laws,12other requirement bodies,56old MT rows,all U/precision/history limits and161released objects remain unchanged. Native x86 reference bits only; portable comparator null, no public/ARM promotion, new grade or release. |\n'
    ops=[{'old':'updated: 2026-10-19\n','new':'updated: 2026-10-21\n'},
         {'old':'revision: 6\n','new':'revision: 7\n'},
         {'old':'### REQ-MIDI-USER-006 — drum pads\n','new':paragraph+'### REQ-MIDI-USER-006 — drum pads\n'},
         {'old':'## Open questions\n','new':annex+'## Open questions\n'},
         {'old':'Case derivation: `scripts/derive_cases.py`','new':evidence+'Case derivation: `scripts/derive_cases.py`'},
         {'old':'| 6 | 2026-10-19 | applies','new':revision+'| 6 | 2026-10-19 | applies'}]
    proposed=old
    for op in ops:assert proposed.count(op['old'])==1;proposed=proposed.replace(op['old'],op['new'],1)
    save('owner-delta.json',{'schema':'staged-reversible-owner-delta-v1','status':'STAGED-NOT-APPLIED-NOT-FROZEN',
        'operations':ops,'proposed_owner':{'bytes':len(proposed.encode()),'sha256':sha(proposed.encode())},
        'review_note':'Actual review pin and exact final wording remain pending Root; no canonical owner writes performed.'})
    pins=[identity(BATCH/n) for n in ['manifest.json','manifest-before.json','inputs.json','observations.json','results.json','inherited-controls.json']]
    pins += [identity(ROOT/n) for n in ['wiki/specs/midi-user-mapping.md','handoff/midi-config-v4/manifest.json',
       'handoff/midi-config-v4/cases.json','handoff/midi-config-v4/REVIEW.md',
       'analysis/ableton-live-12.4.3/full-spec-v1/reviews/family-midi-user-routes-v1-review.json',
       'analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/manifest.json']]
    save('pins.json',{'pins':pins,'actual_review':None,'actual_review_status':'Root sole review pending; no invented approval/hash'})
    print(json.dumps({'status':'STAGED-ONLY','new_cases':len(fresh),'catalog':len(catalog),'historical':len(legacy),'canonical_unchanged':identity(OWNER),'proposed_owner_bytes':len(proposed.encode())}))

if __name__=='__main__':main()
