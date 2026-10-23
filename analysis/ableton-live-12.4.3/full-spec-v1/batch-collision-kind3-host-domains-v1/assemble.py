#!/usr/bin/env python3
"""One selected Collision metadata materialization; no old imports/originals/runtime reads."""
import pathlib,json,hashlib,struct,os,shutil
H=pathlib.Path(__file__).resolve().parent;F=H.parent;R=H.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):p=pathlib.Path(p).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,v):
 with (H/n).open('x') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not(H/'inputs.json').exists() and not(H/'attempts').exists()
ep=F/'reviews/collision-kind3-host-domain-eligibility.json';assert pin(ep)['sha256']=='706b599ba68670b8faa1139f64f192c270d2a14b18cdfdd0f653f0389d05c5d9';e=json.loads(ep.read_bytes());source=R/e['baseline_script']['path'];bp=pin(source);assert all(bp[k]==e['baseline_script'][k]for k in ['bytes','sha256']);text=source.read_text();words=e['baseline_words'];assert len(words)==139 and [w['index']for w in words]==list(range(139))
assert sha(bytes.fromhex(''.join(w['f32_le']for w in words)))=='1a61d31521973c8eaa9167ca184704b787cda790d43db0c82a459d28caf0d0bc'
(H/'scripts').mkdir();(H/'protocol').mkdir();histories=[];plans=[];byhash={}
fixed={'rate':44100,'warmup_before_event_queue':11264,'render_frames':44100,'block':512,'last_render_block':68,'events':[[4096,144,60,100],[26146,128,60,0]],'input':'zero','inflag':0,'transport':[0,0,120],'XDEV_TIME':'0','MXCSR':'0x1f80 source policy; no register trace','LIBM_ULP':'absent/unperturbed','process_commands':e['history_commands']}
for v in e['vectors']:
 i=v['changed_index'];value=v['value'];w=[dict(x)for x in words]
 if i is not None:w[i].update(token=f'{value}.0',f32_le=struct.pack('<f',value).hex(),reconstructed_f64_le=struct.pack('<d',value).hex())
 key=sha(bytes.fromhex(''.join(x['f32_le']for x in w)));assert key==v['vector_sha256'];id='baseline-preset-c4'if i is None else f'i{i:03d}-v{value:02d}';script=text if i is None else text.replace(f'param {i} {words[i]["token"]}\n',f'param {i} {value}.0\n',1)
 history={**fixed,'parameter_vector_sha256':key,'parameter_tokens':[x['token']for x in w],'parameter_f32_le':[x['f32_le']for x in w],'parameter_reconstructed_f64_le':[x['reconstructed_f64_le']for x in w]};hk=sha(json.dumps(history,sort_keys=True,separators=(',',':')).encode())
 z={'id':id,'changed_index':i,'value':value,'vector_sha256':key,'history_sha256':hk,'whole_history':history,'script_bytes':len(script.encode()),'script_sha256':sha(script.encode()),'provenance':'historical-retained-input-only-NOT-approved-actual'if i is None else'fresh-selected-once','historical_input':{'script':bp,'approved_actual':None,'new_pid':None,'new_receipt':None,'new_metrics':None}if i is None else None,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None};histories.append(z);byhash[key]=z
 if i is not None:
  p=H/'scripts'/(id+'.script');p.write_text(script);plans.append({'id':id,'index':i,'value':value,'vector_sha256':key,'history_sha256':hk,'script':str(p),'direct_exports':251,'CalcA':109,'stereo_bytes':442912})
aliases=[dict(a,id=byhash[a['vector_sha256']]['id'],history_sha256=byhash[a['vector_sha256']]['history_sha256'])for a in e['aliases']]
save('inputs.json',{'schema':'Collision-native-nonvirtual-kind3-preset-c4-v1','counts':{'domains':20,'aliases':105,'unique_histories':86,'historical_input_only':1,'fresh_children':85,'direct_exports':21335,'CalcA':9265,'stereo_bytes':37647520},'baseline_words':words,'domains':e['domains'],'excluded_virtual_kind3_indices':e['excluded_virtual_kind3_indices'],'fixed_history':fixed,'baseline_script_utf8':text,'aliases':aliases,'histories':histories,'plans':plans})
old=R/'analysis/ableton-live-12.4.3/r2/t12-collision-v1';m=json.loads((old/'manifest.json').read_bytes());methods=[]
for name,expected in e['admitted_existing_model']['method_source_manifest_pins'].items():
 p=old/name;got=pin(p);assert all(got[k]==expected[k]for k in ['bytes','sha256']);dest=H/'protocol'/p.name;shutil.copyfile(p,dest);methods.append({'historical_source':got,'owned_copy':pin(dest),'never_compile_import_execute':True})
prior=F/'batch-collision-resonator-enable-histories-v1/pre-call-manifest.json';pre=json.loads(prior.read_bytes());roles=['loader','bundle','elf-interpreter','libc','libm','libstdcxx','libgcc'];watch=[]
for role,x in zip(roles,pre['runtime_expected']):watch.append({'role':role,'identity':{k:x[k]for k in ['path','bytes','sha256']}})
# Current Python/cache expected identities inherited from admitted other current standing contexts; not new provider selection.
ctxold=json.loads((F/'batch-electric-midi-axes-v1/context.json').read_bytes())
for role in ['python','ld_cache']:
 x=next(x for x in ctxold['watched_roles']if x['role']==role);watch.append(x)
bun=e['admitted_existing_model']['bundle'];watch.append({'role':'selected-x86-slice','identity':{'path':bun['path'],'offset':bun['x86_64']['offset'],'bytes':bun['x86_64']['size'],'sha256':bun['x86_64']['sha256']}})
save('context.json',{'exe':watch[0]['identity']['path'],'bundle':bun['path'],'python':'/usr/bin/python3','environment':e['admitted_existing_model']['environment_inherited'],'watched_roles':watch,'limits':{'sequential_once_children':85,'wall_seconds':20,'CPU_seconds':20,'core_bytes':0,'FSIZE_each':4194304,'stdin':'DEVNULL','new_process_group':True},'sole_actual_source_peer':'automation_actual_review','Root_role':'Citation-only all new source/code/actual/raw/results','phase_limits':'First detected fault stops later children/no retry/resume; childend guards cannot retract queued calls; cleanup limits escapeddescendants/uncatchableparent unknown.'})
reviewp=F/'reviews/collision-resonator-enable-histories-v1-review.json';assert pin(reviewp)['sha256']=='e899873b4bd4335aedc83013739fd8875d9d465db32d6daa929e70601131d086'
save('authority-pins.json',{'eligibility':pin(ep),'native_domain_authority':e['native_domain_authority'],'H4_manifest':e['H4manifest'],'N6_metadata_only':e['N6metadata'],'baseline_input':bp,'prior_model_protocol_review':pin(reviewp),'prior_pre_call_metadata_only':pin(prior),'old_manifest':pin(old/'manifest.json'),'owner_asof_nongating':pin(R/'wiki/specs/device-collision.md'),'method_sources':methods,'source_version_and_execution_binding':'Historical retainedsource identity, not originalexecutedversion attestation','historical_baseline_actual_approval':None,'new_native_source_provider_acquisition':False})
save('eligibility-context.json',{'eligibility_pin':pin(ep),'selected_whole_class':{'domains':20,'aliases':105,'histories':86,'fresh':85,'baseline':'retainedinput-only NOT approved observation; no PID/metrics/oracle fabricated and not rerun'},'old41_input_classifications':e['old41_input_classifications'],'released_input_projections':e['released_input_projections'],'approved12_input_projections':e['approved12_input_projections'],'approved12_protocol':e['approved12_protocol'],'approved12_exact_history_intersections':0,'limits':e['limits'],'old_source_binding_unknown':True})
print(json.dumps({'status':'MATERIALIZED-ONCE','domains':20,'aliases':105,'histories':86,'fresh_scripts':85,'baseline_approved_actual':False,'original_calls':0,'runtime_reads':0}))
