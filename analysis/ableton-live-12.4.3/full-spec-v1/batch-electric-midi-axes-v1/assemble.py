#!/usr/bin/env python3
"""One fixed144alias/143wholehistory catalog/142scripts, metadata only/no originals or old imports."""
import hashlib,json,pathlib,struct,shutil,os
H=pathlib.Path(__file__).resolve().parent;F=H.parent;ROOT=H.parents[3];OLD=F/'batch-electric-note-keys-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):p=pathlib.Path(p).resolve();b=p.read_bytes();return{'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with(H/n).open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def events(axis,value):
 if axis=='matching-channel':return[[11264,144+value,60,100],[33314,128+value,60,0]]
 return[[11264,144,60,100],[33314,128,60,value]]
assert not(H/'inputs.json').exists();rp=F/'reviews/electric-velocity-bytes-v1-review.json';assert pin(rp)['bytes']==1016304 and pin(rp)['sha256']=='7b89ba1553c6a5ebdf92b2931d09aae1095454aadc8a391c5bdde1b7dab55b66';review=json.loads(rp.read_text());assert review['disposition'].startswith('APPROVED')and not review['blocking_findings'];shared=review['approved_summary']['shared_input'];control=review['approved_summary']['approved_points'][100];assert control['events']==events('note-off-velocity',0)and control['fresh_pid']is None and control['fresh_receipt_pointer']is None
words=shared['words'];assert len(words)==33 and[w['index']for w in words]==list(range(33));assert sha(bytes.fromhex(''.join(w['little_endian_hex']for w in words)))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
save('approved-prior-summary.json',{'approved_review':pin(rp),'shared_input':shared,'inherited_velocity100_baseline':control,'scope':'ApprovedP1summarycontrol only/no actual/source/raw/numeric re-review/no oldPID/metrics fabricated'})
source=ROOT/'wiki/research/device-electric-dsp.md';page=source.read_text();heading='## Fixed P1 channel and release-byte eligibility — 2026-10-21';assert page.count(heading)==1;section=page[page.index(heading):].split('\n## ',1)[0];metap=F/'reviews/electric-fixed-p1-finite-host-domain-eligibility.json';meta=json.loads(metap.read_text());assert pin(metap)['sha256']=='f7fb4a47d8728f5d24249973545c8e7a8ea514f933ab4620d281e711cb2e8d78'
save('eligibility-context.json',{'canonical_research_asof_pin':pin(source),'canonical_section':heading,'canonical_section_text':section,'canonical_section_utf8_sha256':sha(section.encode()),'old120scriptpin_authority':pin(metap),'old120_script_pins':meta['historical_input_cut']['pins'],'inherited_metadata_disposition':'Onlydefaults_c4exactP1baseline. Oldchannel1/15/release127 ASTinputrecipes have22050render/off13230→absolute24494/end33314; P1off33314/end55364. Oldsecondnoteon90velocity0 historydifferent. HistoricalBool/source-executedversionbindinggap retained/no globalabsence; no reexecution/sourcebehavior/numeric/audio reads.'})
def whole(ev):return{'parameter_f32_bits_le':[w['little_endian_hex']for w in words],'parameter_reconstructed_binary64_le':[w['reconstructed_binary64_le']for w in words],'events':ev,'sample_rate':44100,'process_frames':[11264,44100],'block':512,'input':'zero','inflag':0,'transport':[0,0,120],'XDEV_TIME':'0 existing treatment','MXCSR':'0x1f80','LIBM_ULP':'absent/unperturbed'}
(H/'scripts').mkdir();(H/'protocol').mkdir();aliases=[];histories=[];plans=[];seen={}
for axis,count in[('matching-channel',16),('note-off-velocity',128)]:
 for value in range(count):
  ev=events(axis,value);wh=whole(ev);key=sha(json.dumps(wh,sort_keys=True,separators=(',',':')).encode());aliases.append({'axis':axis,'value':value,'history_sha256':key})
  if key in seen:assert axis=='note-off-velocity'and value==0;continue
  baseline=value==0;id='baseline-P1'if baseline else('channel-'+f'{value:02}'if axis=='matching-channel'else'offvel-'+f'{value:03}')
  old=None if not baseline else{'approved_review':pin(rp),'approved_point_pointer':'/approved_summary/approved_points/100','case_refs':['DEL-CS-001','P1','ETI-12','ELECTRIC-AUDIO-004'],'stored_aliases':[11.99999,12],'new_pid':None,'new_receipt':None}
  text='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}'for w in words]+[f'event {f} {s:#x} {k} {v}'for f,s,k,v in ev]+['inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n'
  h={'id':id,'axis':'baseline'if baseline else axis,'value':value,'history_sha256':key,'whole_history':wh,'events':ev,'packed16_events_le':[struct.pack('<qBBBB4x',*e,0).hex()for e in ev],'script_utf8_sha256':sha(text.encode()),'script_utf8_bytes':len(text.encode()),'historical':old,'provenance':'inherited-approved-summary-only'if baseline else'fresh-selected','expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None};histories.append(h);seen[key]=h
  if not baseline:
   p=H/'scripts'/(id+'.script');p.write_text(text);plans.append({'id':id,'axis':axis,'value':value,'history_sha256':key,'script':str(p),'direct_exports':145,'CalcA':109,'output_bytes':442912})
assert len(aliases)==144 and len(histories)==143 and len(plans)==142
save('inputs.json',{'schema':'whole-Electric-P1-matching-channel-and-offvelocity-v1','counts':{'alias_points':144,'unique_histories':143,'inherited_histories':1,'fresh_children':142,'direct_exports':20590,'CalcA':15478,'stereo_bytes':62893504},'words':words,'fixture':{'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'key':60,'on_frame':11264,'off_frame':33314,'on_velocity':100,'baseline_off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'},'aliases':aliases,'histories':histories,'plans':plans})
methods=[]
for p in sorted((OLD/'protocol').iterdir()):shutil.copyfile(p,H/'protocol'/p.name);methods.append(pin(p))
owner=ROOT/'wiki/specs/device-electric.md';save('authority-pins.json',{'approved_baseline':pin(rp),'eligibility_source':pin(metap),'canonical_eligibility_section':pin(source),'owner_asof_nongating':pin(owner),'unchanged_inert_method_copies':methods,'actual_semantics_not_rereviewed':True,'prior_actual_raw_audio_reopened':False,'new_original_source_acquisition':False})
ctx=json.loads((OLD/'context.json').read_text());assert ctx['watched_roles'][0]['identity']['sha256']=='6eb5dd284452960f623e0bb6ed26b8743bdf789b8eac09a48b4a9291995ed8e1';ctx['scope']='TwoindependentMIDIaxes/no crossproduct/full144aliases143histories142fresh; full-event/history dedup NOT parameter-only';ctx['stop_policy']='Once142sequential/firstdetectedfaultstopsfuturechildren/retainpartials/no retry/resume/extension; queuedchildcalls mayalreadyexecute. No model/provider/FP/clock/seed change.';save('context.json',ctx)
print(json.dumps({'status':'MATERIALIZED-ONCE','aliases':144,'whole_histories':143,'fresh_scripts':142,'original_calls':0,'runtime_reads':0}))
