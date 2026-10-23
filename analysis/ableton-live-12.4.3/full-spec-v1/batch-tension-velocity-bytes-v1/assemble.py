#!/usr/bin/env python3
"""One-time complete fixed input materialization. No original calls/imported old helpers."""
import hashlib,json,pathlib,shutil,platform,sys,os
H=pathlib.Path(__file__).resolve().parent;B=H.parent;T=B.parent/'r2/t12-tension-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,offset=None,size=None):
 p=pathlib.Path(p).resolve()
 if offset is None:
  raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':sha(raw)}
 with p.open('rb') as f:f.seek(offset);raw=f.read(size)
 assert len(raw)==size;return {'path':str(p),'bytes':len(raw),'sha256':sha(raw),'offset':offset}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not (H/'inputs.json').exists()
source=B/'batch-tension-retained-checks-v1/baseline-links.json';sp=pin(source);assert sp['sha256']=='ec5a9bc093e5e37750bf0b34b4ed2d9111b55ad3166cc3f56f5ab5b2f3baf14c';base=json.loads(source.read_text())['defaults_44']
report=B/'reviews/tension-uncalibrated-sensitivity-v1-review.json';rp=pin(report);assert rp['sha256']=='001b2b6993c0aa7784e1af9325a4c193aa6685bac67dc4695010dad86a0d62d5';review=json.loads(report.read_text());vel1=review['per_setting_reviewed_summary'][34];assert vel1['name']=='vel_1' and vel1['baseline_exact_historical_stereo']
runs_path=T/'results/runs.json';runpin=pin(runs_path);assert runpin['sha256']=='130e46681cc80c24a7f0d4587e42d193dae9a877e16171715c94baad204b7f9f';runs=json.loads(runs_path.read_text())['runs']
selected={1:'vel_1',100:'defaults_44',127:'vel_127'};old={}
for v,name in selected.items():
 r=runs[name];assert r['changes']=={} and r['preset'] is None and r['fs']==44100 and r['frames']==44100 and r['events']==[[4096,144,60,v],[26146,128,60,0]]
 old[v]={'tag':name,'input_metadata_pin':runpin,'input_pointer':'/runs/'+name,'input_projection':{k:r[k] for k in ['changes','preset','fs','frames','events','process']},'output_wav_sha256':r['wav_sha256'],'output_raw_f32_sha256':r['raw_f32_sha256'],'new_pid':None,'new_receipt':None,'source':'inherited approved evidence; no old raw opened or new receipts fabricated'}
 if v==1:old[v]['approved_summary']={'review_pin':rp,'pointer':'/per_setting_reviewed_summary/34','summary':vel1}
 else:old[v]['released_evaluation']={'path':str(B/'family-tension-routes-v1/released-evaluations.json'),'pointer':'/evaluations/'+str(0 if v==100 else 4),'id':'TENSION-AUDIO-001' if v==100 else 'TENSION-AUDIO-005'}
d={'schema':'whole-Tension-default-velocity-byte-v1','counts':{'logical':128,'inherited':3,'fresh_children':125,'direct_exports':27375,'CalcA':10875,'stereo_bytes':44100000},'words':base['parameters_binary32'],'fixture':{'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'key':60,'off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'warmup':0,'MXCSR':'0x1f80','XDEV_TIME':'absent -> existing fixed0','LIBM_ULP':'absent/unperturbed'},'catalog':[],'plans':[]}
(H/'scripts').mkdir();(H/'protocol').mkdir()
for v in range(128):
 d['catalog'].append({'velocity':v,'events':[[4096,144,60,v],[26146,128,60,0]],'provenance':'inherited-no-replay' if v in old else 'fresh-selected','historical':old.get(v),'expected_waveform':None,'portable_comparator':None})
 if v not in old:
  script='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in d['words']]+[f'event 4096 0x90 60 {v}','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy'])+'\n';path=H/'scripts'/f'velocity-{v:03}.script';path.write_text(script);d['plans'].append({'velocity':v,'script':str(path),'direct_exports':219,'CalcA':87,'output_bytes':352800})
save('inputs.json',d)
save('approved-prior-summary.json',{'review_pin':rp,'whole_finite_universe':review['whole_finite_universe'],'input_and_phase_review':review['input_and_phase_review'],'runtime_expected_identity_records':review['custody']['runtime_expected_identity_records'],'imports':review['imports'],'velocity1':vel1,'scope':'Selected approved-summary context only. Prior actual packet/source/raw/results not reopened; no duplicate review.'})
methods=[]
for name in ['xdev.h','xdev.c','xdev_load.c','xdev_bind.c','xdev_cxx.c']:
 src=T/'harness'/name;shutil.copyfile(src,H/'protocol'/name);methods.append(pin(src))
for name in ['tension.py','xdevpy.py']:
 src=T/name;shutil.copyfile(src,H/'protocol'/name);methods.append(pin(src))
authorities=[source,report,runs_path,B/'family-tension-routes-v1/manifest.json',B/'family-tension-routes-v1/released-evaluations.json',B/'reviews/family-tension-routes-v1-review.json',B/'batch-tension-retained-checks-v1/manifest.json',B/'reviews/tension-retained-checks-v1-review.json']
save('authority-pins.json',{'retained_documents':[pin(p) for p in authorities],'unchanged_method_sources':methods,'original_method_modules_executed':False,'prior_actual_packet_opened':False,'source_origin':'retained historical authority; fresh copying/hashes do not repair original custody'})
roles=[{'role':'loader','identity':x} for x in []]
for i,item in enumerate(review['custody']['runtime_expected_identity_records']):
 actual=pin(item['path']);assert actual==item
 roles.append({'role':['loader','bundle','libc','libm','libstdcxx','libgcc','elf_interpreter'][i],'identity':actual})
assert roles[0]['identity']['bytes']==155680 and roles[0]['identity']['sha256']=='e4e184894fc7e91f8661b7df548ec338ac441372d30adbdc862425c5fe4fb8be'
bundle=roles[1]['identity']['path'];sliceid=pin(bundle,16384,501392);assert sliceid['sha256']=='63dd07171e76e20427045cc0269e124d67e94e6cddb42cab82c77cec7e6ed05d';roles.append({'role':'selected_x86_slice','identity':sliceid});roles.append({'role':'python','identity':pin(sys.executable)})
save('context.json',{'exe':roles[0]['identity']['path'],'bundle':bundle,'watched_roles':roles,'environment':{'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC'},'host':{'uname':list(platform.uname()),'python':sys.version,'byteorder':sys.byteorder},'sole_peer':'Root','limits':{'CPU_seconds':20,'wall_seconds':20,'CORE':0,'FSIZE':4194304,'stdin':'DEVNULL','new_process_group':True,'retry':False},'phase_policy':'MXCSR default1f80 for each call, no explicit script/environment perturbation; XDEV_TIME absent is existing fixed0. libm wrappers unperturbed. Rate return opaque, CalcA status checked. Init/nested calls separately retained, not direct count.','stop_policy':'First detected anomaly stops future children. Already executed calls inside child cannot be retracted; no retry/fallback/extension. SIGKILL/host loss may leave partial status; no automatic resume.'})
print(json.dumps({'status':'MATERIALIZED-ONCE','scripts':125,'logical':128,'runtime_roles':len(roles),'original_calls':0}))
