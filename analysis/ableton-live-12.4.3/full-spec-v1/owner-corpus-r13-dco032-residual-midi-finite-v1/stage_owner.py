from pathlib import Path
import json,hashlib,re,datetime
R=Path('/home/ollie/Documents/sound');F=R/'analysis/ableton-live-12.4.3/full-spec-v1';P=F/'owner-corpus-r13-dco032-residual-midi-finite-v1';assert not(P/'manifest.json').exists();P.mkdir(exist_ok=True)
def sh(b):return hashlib.sha256(b).hexdigest()
def enc(d):return json.dumps(d,sort_keys=True,separators=(',',':')).encode()
def pin(p):b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sh(b)}
def write(n,x):p=P/n;p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n'if not isinstance(x,str)else x)
RP=F/'reviews/corpus-dco032-residual-midi-axes-v1-review.json';b=RP.read_bytes();assert len(b)==9108938 and sh(b)=='a728173fc59cf176177bd3882f1da8027718b838be5dd5be9f0dbd39077d363f';rv=json.loads(b);S=rv['approved_summary'];assert rv['blocking_findings']==[]and rv['required_corrections']==[]
OP=R/'wiki/specs/device-corpus.md';before=OP.read_text();assert len(before.encode())==97341 and sh(before.encode())=='21087e2ebc735563b1d4f0451f3a6613342bb514b9591726b0a2c8c4ad4903d3'
PR=F/'reviews/corpus-owner-r12-dco032-midi-finite-v1-review.json';b=PR.read_bytes();assert sh(b)=='2446ac0dbdf15592e0a2561e28639ab2629f1d1319873c86b1206985e2ef1cbb';prior=json.loads(b);assert prior['approved_owner_target']['utf8_text']==before
points=S['approved_points'];hist=S['input_histories'];assert len(points)==len(hist)==158 and len(S['aliases'])==160
fresh=[];catalog=[];joins=[];seq=958
for i,(x,h)in enumerate(zip(points,hist)):
 assert x['id']==h['id']and x['history_sha256']==h['history_sha256']and x['events']==h['events']
 base=x['provenance']=='inherited-no-replay';cid=None
 if not base:seq+=1;cid=f'DCO-{seq:03d}'
 z={'id':h['id'],'case_id':cid,'existing_case_refs':['DCO-032']if base else[],'first_alias':h['first_alias'],'history_sha256':h['history_sha256'],'events':h['events'],'packed16_events_le':h['packed16_events_le'],'eligibility_history':h['eligibility_history'],'fixed_history_pointer':'#/shared_input/fixed_history','parameter_tokens':h['parameter_tokens'],'parameter_f32_bits_le':h['parameter_f32_bits_le'],'parameter_f64_reconstructed_le':h['parameter_f64_reconstructed_le'],'parameter_vector_sha256':h['parameter_vector_sha256'],'parameter_token_binary64_sha256':h['parameter_token_binary64_sha256'],'requirements':['REQ-DEVICE-CORPUS-013'],'new_application_predicate_proof':False,'approved_point_pointer':f'/approved_summary/approved_points/{i}','input_history_pointer':f'/approved_summary/input_histories/{i}','approved_point_sha256':sh(enc(x)),'input_history_sha256':sh(enc(h)),'provenance':x['provenance'],'native_observation':None if base else x,'historical':x if base else None,'new_pid':None if base else x['pid'],'new_receipt':None if base else x['receipt_pointer'],'new_metrics_for_inherited':None,'waveform_prior':None,'new_expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None,'old_modal_budget_transferred':False,'qualification_pointer':'#/review_qualifications'}
 catalog.append(z);joins.append({k:z[k]for k in ['id','case_id','existing_case_refs','history_sha256','approved_point_pointer','input_history_pointer']})
 if cid:fresh.append(z)
assert seq==1115 and len(fresh)==157 and[c['case_id']for c in fresh]==[f'DCO-{i:03d}'for i in range(959,1116)]
priorcatalog=prior['approved_complete_mapping']['catalog']['catalog'];priorhashes={x['history_sha256']for x in priorcatalog};newhashes={x['history_sha256']for x in fresh};assert not(newhashes&priorhashes)
C={'approved_review':pin(RP),'shared_input':S['shared_input'],'catalog':catalog,'aliases':S['aliases'],'logical_aliases':160,'whole_histories':158,'newcases':157,'inherited':1,'baseline_three_aliases_one_INPUT_reference':True,'review_qualifications':rv['qualifications'],'portable_admission':None}
J={'histories':joins,'aliases':[{'axis':a['axis'],'value':a['value'],'id':a['id'],'case_id':next(x['case_id']for x in catalog if x['id']==a['id']),'existing_case_refs':next(x['existing_case_refs']for x in catalog if x['id']==a['id']),'events':a['events'],'history_key':a['history_key']}for a in S['aliases']]}
write('catalog158.json',C);write('new-cases157.json',fresh);write('joins160.json',J)
def reqs(s):
 matches=list(re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n',s,re.M));out={}
 for i,m in enumerate(matches):
  ends=[x for x in [s.find('\n### ',m.end()),s.find('\n## ',m.end())]if x>=0];end=min(ends)if ends else len(s);out[m[1]]=s[m.start():end+1]
 return out
textids=sorted({int(x)for x in re.findall(r'\bDCO-(\d{3,4})\b',before)});assert max(textids)<=958 and all(1<=x<=958 for x in textids) and 'DCO-563–958' in before
assert prior['total_navigation_IDs']==958
oldids=list(range(1,959))
rows=[x for x in before.splitlines()if re.match(r'^\| DCO-\d{3} \|',x)];assert len(rows)==36
protected={name:sh(before[before.index(start):before.index(end,before.index(start))].encode())for name,start,end in [('old_acceptance','## Acceptance cases','## Open questions'),('metric','## Comparison metric','## Acceptance cases'),('open_questions','## Open questions','## Analyst evidence appendix'),('timing','## Timing and state','## R7 scope addition')]}
linkedobjects=sorted(set(re.findall(r'\]\(([^)]+/(?:new-cases\d+|catalog\d+|joins\d+)\.json)\)',before)))
B={'owner_before':pin(OP),'approved_prior_owner_review':pin(PR),'requirement_bodies':{k:{'bytes':len(v.encode()),'sha256':sh(v.encode())}for k,v in reqs(before).items()},'old_IDs':oldids,'old_case_rows':rows,'old_rows_sha256':sh(enc(rows)),'protected_sections':protected,'old_analysis_JSON_navigation_links':linkedobjects,'old_external_objects':'All R3–R12 objects and releases unchanged; inherited peer approval and unchanged navigation, no old provider payload or release fixture reopened. R12 embedded catalog/cases/joins compared as preservation INPUT metadata only.','R12_embedded_mapping_sha256':sh(enc(prior['approved_complete_mapping'])),'R12_embedded_catalog_count':len(priorcatalog),'prior_preservation':prior['preservation'],'release_groups':27,'release_evaluations':73,'no_actual_payload_reads':True}
write('baseline.json',B)
req='''- **X finite supplied residual two-event observations; U portable acceptance (revision 13).**
  [DCO-959–1115](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/new-cases157.json) add157 once-only histories at the fixed DCO-032 context:
  127 Off keys with On key60 fixed,15 On channel nibbles with Off status80
  fixed and15 Off channel nibbles with On status90 fixed, independently.
  Three baseline aliases share ONE old DCO-032 INPUT reference, without
  replay, new PID/receipt/metrics or transfer of its criterion. These are
  supplied-event observations, not matching-key/channel construction or a
  general release, voice, dispatch, current public receiver or Live/ARM law.
  All new waveform priors/expectations and portable expected/comparator/grade
  remain NULL; new application-predicate proofs remain false. All older
  clauses, criteria, general U and modal-budget scopes remain unchanged.

'''
annex='''## Finite supplied DCO032 residual MIDI observation annex — revision 13

The [complete catalog](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/catalog158.json) retains160 aliases and158 WHOLE histories at
one fixed38-word parameter vector. DCO-959–1115 are157 fresh observations:
Off key0–127 except60, On channel0–15 except0 and Off channel0–15 except0.
Each axis varies independently without a crossproduct. Off-key variation
keeps On key60 fixed; On-channel variation keeps Off status80 fixed;
Off-channel variation keeps On status90 fixed. They do not change paired
keys or channel nibbles together. The three baseline aliases share ONE
inherited DCO-032 INPUT approval, without replay, fresh PID/receipt/metrics,
new ID, output expectation, criterion or modal-budget transfer. The [160 joins](../../analysis/ableton-live-12.4.3/full-spec-v1/owner-corpus-r13-dco032-residual-midi-finite-v1/joins160.json)
use complete event/process/FP/environment history, not parameter-only dedup.
All new histories are distinct from the R12 four-axis catalog.

Only [Root's sole actual/source approval](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-dco032-residual-midi-axes-v1-review.json),
SHA-256 `a728173fc59cf176177bd3882f1da8027718b838be5dd5be9f0dbd39077d363f`,
supplies these finite observations. This owner maps that approved summary
without actual/source/raw/audio/numeric re-review. Each fresh record retains
exact script, two packed16-byte events, input/output identity, PID/receipt,
protocol and provenance pointers. The old735-byte baseline script remains
`2366eeac0a1f1e41a6b835fda19703e452d46002f14d45c48a0a2e6641b82fc3`;
it is an inherited input reference only. Bounded input intersections are
not global absence or proof of all MIDI histories.

The original38 decimal tokens and binary32 vector remain
`351eb39550097c4d432e53db67460f1e50b35533e34841a90438ab2e31256060`;
parsed binary64 token bytes remain
`1855a118565d354015e7ba29929bba2152a57f5a3507885ee1050e37b7ec8a6a`.
MidiPitch12=1/MidiGate13=1/LFO17=0/host34=positive zero. Literal script order
is MXCSR1f80/stopped transport0/0/120 BEFORE create/rate44100/38 ordered
parameters, On1537/status90/key60/velocity100 and Off3073/status80/key60/
velocity64, inputflag1/I1 impulse4096, render16384frames/block512/destroy.
Only the named event byte changes. No warmup/reset/extra event/host update,
new timing segmentation, construction, tool, patch, build or provider.
The original I1 path and bytes remain fixed; synthetic coordinates do not
prove Live frame origin, event admission or a current public receiver.

All157 approved outputs are finite/nonzero in both channels; none has
identical channel words, and two fresh output hashes are descriptive only.
These facts establish no key matching, channel filtering, voice release,
productive event admission, deterministic waveform or general MIDI law.
All new waveform priors/expectations, portable expected/comparator/grades
stay NULL; artifact hashes are native observation references, not portable
candidate waveform criteria. No f0, metric, fit, window, tolerance,
calibration, physical/ARM law or old modal-budget transfer is added.

Minimal environment retains XDEV_TIME0 and XDEV_LIBM_ULP UNSET, not explicit
LIBM0 or proof of the old whole ambient environment. Old source/default/
entryFP/ABI/OSexec and loaded-provider continuity gaps remain. All new
capture/data/checker/parent/initial-assembler source was pre-call-bound for
THIS batch; the assembler is historical materialization, not a final
regenerator. This does not repair earlier source/checker FAIL/additive
postcapture DATA/default/fsync or parent-binding history. Regular raw/log/
JSON/JSONL fsync requests do not prove directory/crash durability. Per-child
endpoints and samePID parent records do not attest OSexec, continuous
runtime/providers or native FP. Post-child protocol/import checks cannot
undo earlier within-child calls; group/direct-child cleanup does not exhaust
parent-loss/escaped-process paths. Declarations differ from counted use.
73 selected direct exports/32 CalcA per child and zero logged initializers
leave nested/all-native calls unknown; Rate's signed integer is opaque.
Resource guards were not triggered: before each call the recorded packet
was at most27,861,012 bytes and free space at least258,478,080 bytes.
Planning estimates are not filesystem reservations or general resource laws.

Only bounded REQ-013 wording is appended. All12 other whole requirements,
including ENTIRE R10 REQ-002, old013 R12 prefix,958 prior IDs/36 old rows,
all R3–R12 objects/catalogs, old NULL criteria/general U/timing/state/history,
released27groups/73evaluations, modal174+2 omissions, parked96 setup and old
Square phases/guard/prepare qualifications remain exact, with full reversal.
The resulting1115 navigation IDs are not passes or an application-outcome
denominator. New application-predicate proofs remain false; no release,
grade, public/ARM law or whole-product closure follows. Required U stays open.

'''
last=next(x+'\n'for x in before.splitlines()if x.startswith('| 12 |'))
rev='| 13 | 2026-10-21 | Add157 finite DCO032 residual observations DCO-959–1115/full160aliases158WHOLEhistories, three baseline aliases ONE inherited INPUT reference/no replay/newmetrics/criterion transfer. Append ONLY boundedREQ013; preserve12 other whole requirements incl ENTIRE R10 REQ002/old013 R12 prefix/958 prior IDs36rows/all R3–R12 objects/criteriaU/releases27groups73eval/modal176parked96/Squarehistory exact/fullreverse. Original decimal/f64/gate1/host34+0/LIBM_UNSET/single Offkey or Onchannel or Offchannel unchanged; NULL new priors/portable criteria/grades/newappFalse, no unmatched-key/release/publicARM/calibration law. |\n'
replacements=[{'old':'revision: 12\n','new':'revision: 13\n'},{'old':'## Timing and state\n','new':req+'## Timing and state\n'},{'old':'## Open questions\n','new':annex+'## Open questions\n'},{'old':last,'new':last+rev}]
after=before
for z in replacements:assert after.count(z['old'])==1;after=after.replace(z['old'],z['new'],1)
reverse=after
for z in reversed(replacements):assert reverse.count(z['new'])==1;reverse=reverse.replace(z['new'],z['old'],1)
assert reverse==before
rb,ra=reqs(before),reqs(after);assert len(rb)==13 and all(ra[k]==v for k,v in rb.items()if not k.endswith('013'))and ra['REQ-DEVICE-CORPUS-013'].startswith(rb['REQ-DEVICE-CORPUS-013'])
write('owner.delta.json',{'owner_before':pin(OP),'owner_after':{'path':'wiki/specs/device-corpus.md','bytes':len(after.encode()),'sha256':sh(after.encode())},'replacements':replacements,'status':'PROPOSED_R13_PENDING_ROOT_SOLE_OWNER_REVIEW','canonical_write':False})
write('README.md','''# Corpus R13 residual MIDI finite owner proposal

Root is the sole NEW wording/mapping/IDs/preservation peer. Actual evidence is inherited ONLY from Root's approved residual157 summary; never open the actual packet/source/raw or replay numeric proof. No canonical/shared/release write by author.

157 new IDs DCO-959–1115; full160aliases158WHOLEhistories. Three baseline aliases refer ONE old DCO032 INPUT approval only/no replay/newPIDmetrics/criterion. Single Off key, single On channel or single Off channel; no paired changes/crossproduct/timing/model change. All waveform priors/new expected/portable expected/comparator/grade NULL; no new application proof or general public/ARM/calibration law.

The exact four reversible replacements update revision, append only boundedREQ013, append an observation annex and revision row. Preserve all12 other whole requirements inclENTIRE R10REQ002, old013 R12prefix,958IDs36rows, old Acceptance prefix/all R3–R12 objects/catalogs/criteriaU/timing/state/history/modal176/parked96/Squarehistory and released27groups73eval. Full reversal reconstructs exact97341B/21087e2e…903d3 R12. No full owner snapshot is duplicated.

Read complete check.py before packet-only --check. Its only external reads are current canonical owner, approved Root actual summary and approved R12 owner report. It never reads actual payload, old proposal catalogs/code/raw, runtime/source/provider or released fixtures. R12 mapping preservation comes from that approved report's embedded mapping. Initial stage_owner.py is historical inert materialization; NEVER run/import it as a checker. Root applies only after approval; no automatic successor.
''')
write('stage_owner.py',Path(__file__).read_text());print(json.dumps({'directory':str(P),'target_bytes':len(after.encode()),'target_sha256':sh(after.encode()),'newcases':len(fresh)},indent=2))
