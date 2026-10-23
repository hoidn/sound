from pathlib import Path
import json,hashlib,copy
ROOT=Path('/home/ollie/Documents/sound');F=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1';OLD=F/'batch-tension-kind3-host-domains-v1';P=F/'batch-tension-midi-axes-v1';P.mkdir(exist_ok=False)
def ident(p):b=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(n,x):p=P/n;p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n' if not isinstance(x,str) else x);return ident(p)
rp=F/'reviews/tension-note-keys-v1-review.json';review=json.loads(rp.read_text());s=review['approved_summary'];shared=s['shared_input'];baseline=s['approved_points'][60];assert baseline['note_key']==60 and baseline['provenance']=='inherited-no-replay'
write('inherited-controls.json',{'approved_review':ident(rp),'approved_pointer':'#/approved_summary/approved_points/60','control':baseline,'fresh_pid':None,'fresh_receipt':None,'new_metrics':None,'old_audio_reads':0,'historical_velocity_parent_gap':'Prior velocity launch binding gap remains historical; new prebound parent never repairs older evidence.'})
methods=[];(P/'protocol').mkdir()
for m in shared['method_sources']:
 old=Path(m['new_copy']['path']);raw=old.read_bytes();assert len(raw)==m['new_copy']['bytes'] and hashlib.sha256(raw).hexdigest()==m['new_copy']['sha256'];new=P/'protocol'/old.name;new.write_bytes(raw);methods.append({'historical_source':m['source_record'],'copy_provider':m['new_copy'],'owned_copy':ident(new),'scope':'inert same recorded method version; never imported/compiled/executed'})
write('method-sources.json',methods)
words=shared['words'];indices=[w['index'] for w in words];tokens=[w['token'] for w in words];bits=[w['little_endian_hex'] for w in words]
template=['create','rate 44100']+[f"param {w['index']} {w['token']}" for w in words]+['event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy'];write('baseline-template.script','\n'.join(template)+'\n')
rows=[];aliases=[];seen={};fresh=0;(P/'scripts').mkdir()
for axis,domain in [('channel',range(16)),('off_velocity',range(128))]:
 for val in domain:
  events=[[4096,(0x90|val) if axis=='channel' else 0x90,60,100],[26146,(0x80|val) if axis=='channel' else 0x80,60,val if axis=='off_velocity' else 0]]
  history={'rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':0,'input':'zero','input_flag':0,'transport':[0,0,120],'events':events,'time':0,'parameter_vector_sha256':shared['parameter_vector_sha256']}
  h=hashlib.sha256(json.dumps(history,sort_keys=True,separators=(',',':')).encode()).hexdigest()
  if h not in seen:
   i=len(rows);uid=f'TMA-U{i:03d}';seen[h]=uid;row={'id':uid,'unique_vector':i,'history_sha256':h,'history':history,'first_alias':{'axis':axis,'value':val},'parameter_tokens':tokens,'parameter_f32_bits_le':bits,'parameter_vector_sha256':shared['parameter_vector_sha256'],'events':events,'disposition':'inherited-no-replay' if i==0 else 'fresh-planned','waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None}
   if i==0:row['historical']={'approved_review':ident(rp),'approved_pointer':'#/approved_summary/approved_points/60','control':baseline,'fresh_pid':None,'fresh_receipt':None,'new_metrics':None,'old_audio_reads':0}
   else:
    fresh+=1;row['historical']=None;row['fresh_ordinal']=fresh;lines=list(template);lines[131:133]=[f'event {frame} 0x{status:02x} {key} {velocity}' for frame,status,key,velocity in events];row['script']=write('scripts/'+uid+'.script','\n'.join(lines)+'\n')
   rows.append(row)
  aliases.append({'axis':axis,'value':val,'unique_id':seen[h],'history_sha256':h,'shared_baseline_alias':val==0})
cold=json.loads((OLD/'inputs.json').read_text())
config={'schema':'tension-fixed-defaults44-two-independent-midi-axes-v1','parameter_indices':indices,'parameter_tokens':tokens,'parameter_f32_bits_le':bits,'parameter_vector_sha256':shared['parameter_vector_sha256'],'baseline_template':ident(P/'baseline-template.script'),'rows':rows,'aliases':aliases,'logical_aliases':144,'whole_histories':143,'fresh':142,'inherited':1,'environment':shared['environment'],'runtime_expected':shared['runtime_expected'],'executable':shared['runtime_expected'][0],'bundle_slice_expected':shared['bundle_slice_expected'],'approved_import_declarations':cold['approved_import_declarations'],'approved_export_declarations':cold['approved_export_declarations'],'declaration_authority_metadata':ident(OLD/'inputs.json'),'source_pins':[ident(rp)]+[m['owned_copy'] for m in methods],'limits':{'children':142,'wall_seconds':20,'cpu_seconds':20,'core':0,'file_size':4194304,'selected_export_calls_each':219,'selected_export_calls_total':31098,'CalcA_each':87,'CalcA_total':12354,'raw_bytes_each':352800,'new_stereo_bytes_total':50097600,'initializer_entries_separate':142,'all_native_calls':None},'parent_exec_argv':['/usr/bin/python3','-I','-B',str(P/'run_batch.py'),'--run-once'],'history':'Exactly two independent axes, matchingstatusnibbles0..15 and Offdata2 0..127; dedup by whole parameter+event+history identity, not parameter-only; baseline reused once/no replay. No crossproduct.'}
write('inputs.json',config)
# Copy only inert authored collector/launcher patterns into NEW owned source; never run/import old modules.
launcher=(OLD/'launch.py').read_text();write('launch.py',launcher)
runner=(OLD/'run_batch.py').read_text().replace('fixed106-child','fixed142-child').replace("'COMPLETE-106-ONCE'","'COMPLETE-142-ONCE'").replace("'inherited_not_replayed': 11","'inherited_not_replayed': 1")
write('run_batch.py',runner)
data=(OLD/'data.py').read_text().split('\ndef validate(c):')[0]
data=data.replace("== [('4096', '0x90', '60', '100'), ('26146', '0x80', '60', '0')]", "== [(str(f),hex(st),str(k),str(v)) for f,st,k,v in row['events']]")
write('data.py',data)
write('README.md','''# Tension defaults44 independent MIDI-axis whole batch

Root selected one existing unchanged xdev batch:144typedaliases/143complete event histories,142fresh (matchingchannels1..15 and Offvelocity1..127) plus ONE inherited shared baselineDTN001 from Root approved note-key summary only. No baseline replay, crossproduct, newmodel/patch/provider/build/tool, neweventtype, calibration or sourcefrontier. Fullhistory identity deduplicates the catalog, NEVER parameter vector alone. Fixed129words/44100/44100frames512last68/no warmup/zeroinputflag0/stopped0,0,120/key60/on4096vel100/off26146; vary only both matchingstatuslownibbles OR Offdata2, independently.

Freeze all inputs/scripts/newsource including parent, immutablemethodcopies/authority/model/runtimepins/FP-time environment/phases before once142children. Minimal explicit env/no inheritedLD/FP overrides;20sCPUwall/core0/4MiB/DEVNULL/newgroups; fullraw/stdoutstderr/PIDUTC/argv/imports/flags/cxx/beforeaftercustody; firstanomaly stops futurechildren, no retries.31,098selectedexports12,354CalcA50,097,600rawstereoB plus142initializer260c0 separately; nested/allnativeunknown. All0/edge/silent dispositions retained, NULLpriors/portableexpected/comparator/grade; no f0/fit/newmetric/tolerance/calibration/generalchannel/release/publicARM law.

Only new data.py modules run; inert previous authored pattern text was adapted, no oldhelper import/main execution. Protocol declarations inherited as approvedmethod metadata, actual counted use checked separately. Opaque Rate return remains literal, not success/samplerate law. Existing method defaults transport/FP/time premises remain not target-entry or OSexec proof. Earlier velocity-parentlaunch gap remains historical; thisnewparentpin does not repair it. Cleanup/post-child detection/escapeddescendant/crashdurability limits remain.

Root is SOLE actual/source peer after finalseal; no ownerproposal/grade/release admitted. Read allnewsource before ONLY check_data.py --check for retainedpacket data; NEVER launcher/run_batch --run-once again. Finalmanifest seals partialfailedhistory if any; no retry.
''')
write('phases.json',{'planned_order':['wholecatalog/script/code/materialization','inspectnewsource/dataonlyselfchecks','freezeallprecallpayloads','oneparentexec','142sequentialoncechildren:firstfaultstop','retainrawprotocolunsignedsummaries','authorpacketchecks','finalseal','Rootsoleactualreview'],'old_baseline_replay':False,'ownerproposal_selected':False})
print(P,len(rows),len(aliases),fresh)
