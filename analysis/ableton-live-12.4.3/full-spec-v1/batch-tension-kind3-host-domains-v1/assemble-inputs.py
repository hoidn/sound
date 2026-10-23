from pathlib import Path
import json,hashlib,struct,csv,copy,re,os
from datetime import datetime,timezone
ROOT=Path('/home/ollie/Documents/sound');A=ROOT/'analysis/ableton-live-12.4.3';F=A/'full-spec-v1';P=F/'batch-tension-kind3-host-domains-v1';P.mkdir(exist_ok=False);(P/'scripts').mkdir();(P/'protocol').mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':sha(b)}
def save(n,x):(P/n).write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
rp=F/'reviews/tension-note-keys-v1-review.json';review=json.loads(rp.read_text());assert ident(rp)['sha256']=='537ab1e99b8e7a7a50bbefb09453135508316c7f442521aaf09b89dc25597c06'
s=review['approved_summary']['shared_input'];prior=json.loads((F/'batch-tension-note-keys-v1/inputs.json').read_text());base=(F/'batch-tension-note-keys-v1/baseline-template.script').read_bytes();words=s['words'];inds=[w['index'] for w in words];bits=[w['little_endian_hex'] for w in words];tokens=[w['token'] for w in words];byindex={w['index']:w for w in words}
h4p=A/'r2/h4-devices-v1/out/param_tables.json';h4=json.loads(h4p.read_text())['Tension']['rows'];domains=[{k:r[k] for k in ['index','kind','min','max','virtual','setter']} for r in h4 if r['kind']==3 and not r['virtual']];assert len(domains)==48
n6p=A/'r2/n6-device-tables-v1/out/live_index_map.tsv';names={int(x['index']):x for x in csv.DictReader(n6p.open(),delimiter='\t') if x['device']=='StringStudio'}
oldmp=A/'r2/t12-tension-v1/manifest.json';manifest=json.loads(oldmp.read_text());hits={};oldbase=None;scan=[]
for p in sorted((A/'r2/t12-tension-v1/raw').glob('*.script')):
 raw=p.read_bytes();scan.append(ident(p));lines=raw.decode().splitlines();params=[l.split() for l in lines if l.startswith('param ')]
 if len(lines)!=137 or lines[:2]!=['create','rate 44100'] or lines[131:]!=base.decode().splitlines()[131:] or [int(x[1]) for x in params]!=inds:continue
 vbits=[struct.pack('<f',float(x[2])).hex() for x in params];diff=[i for i,x in enumerate(vbits) if x!=bits[i]]
 ref={'tag':p.stem,'script':ident(p),'old_manifest':ident(oldmp),'manifest_script_pointer':'#/files/raw~1'+p.name,'historical_WAV_metadata_only':manifest['files']['raw/'+p.stem+'.wav'],'old_audio_reads':0,'fresh_receipt':None,'fresh_pid':None,'new_metrics':None,'reference_scope':'Exact retained input script + manifestoutputidentity only; not new rawaudio/receipt/result proof.'}
 assert manifest['files']['raw/'+p.name]=={'bytes':len(raw),'sha256':sha(raw)}
 if not diff:oldbase=ref
 elif len(diff)==1:
  idx=inds[diff[0]];v=struct.unpack('<f',bytes.fromhex(vbits[diff[0]]))[0]
  if idx in [x['index'] for x in domains] and v.is_integer() and 0<=v<=next(x['max'] for x in domains if x['index']==idx):hits[(idx,int(v))]=ref
assert len(scan)==68 and len(hits)==10 and oldbase
(P/'baseline-template.script').write_bytes(base)
rows=[{'id':'TK3-U000','unique_vector':0,'domain_index':None,'host_value':None,'disposition':'inherited-no-replay','historical':oldbase,'parameter_tokens':tokens,'parameter_f32_bits_le':bits,'parameter_vector_sha256':s['parameter_vector_sha256'],'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None}];aliases=[];fresh=0
for domain in domains:
 i=domain['index'];domain['N6_name']=names[i]['name'];domain['N6_mode']=names[i]['mode'];domain['N6_second']=names[i]['second'];domain['baseline']=int(float(byindex[i]['token']))
 domain['role_qualification']='Nativehostdomain only. No ordinaryLiveemission/currentvalue/public path; inactive/sign/magnitude gates remain qualified.'
 for v in range(int(domain['max'])+1):
  if v==domain['baseline']:uid='TK3-U000'
  else:
   unique=len(rows);uid=f'TK3-U{unique:03d}';tt=list(tokens);bb=list(bits);pos=inds.index(i);tt[pos]=str(float(v));bb[pos]=struct.pack('<f',float(v)).hex();ref=hits.get((i,v));row={'id':uid,'unique_vector':unique,'domain_index':i,'host_value':v,'disposition':'inherited-no-replay' if ref else 'fresh-planned','historical':ref,'parameter_tokens':tt,'parameter_f32_bits_le':bb,'parameter_vector_sha256':sha(bytes.fromhex(''.join(bb))),'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None}
   if ref is None:
    fresh+=1;row['fresh_ordinal']=fresh;lines=base.decode().splitlines();lines[2+pos]=f'param {i} {tt[pos]}';p=P/'scripts'/(uid+'.script');p.write_text('\n'.join(lines)+'\n');row['script']=ident(p)
   row['prior_recipe_only']=([13,1],[36,0],[6,2]).__contains__([i,v]);rows.append(row)
  aliases.append({'domain_index':i,'host_value':v,'unique_id':uid,'inherited_shared_baseline':v==domain['baseline']})
assert len(rows)==117 and len(aliases)==164 and fresh==106
methods=[]
for src in sorted((F/'batch-tension-note-keys-v1/protocol').iterdir()):
 (P/'protocol'/src.name).write_bytes(src.read_bytes());methods.append({'copy':'protocol/'+src.name,'identity':ident(src)})
sourcepaths=[rp,h4p,n6p,oldmp,F/'batch-tension-retained-checks-v1/input-selectors.json']+[Path(x['historical']['script']['path']) for x in rows if x['disposition']=='inherited-no-replay']
sourcepaths=list(dict.fromkeys(sourcepaths))
c={k:copy.deepcopy(prior[k]) for k in ['environment','runtime_expected','bundle_slice_expected','executable','approved_import_declarations','approved_export_declarations','limits']}
c.update({'schema':'whole-Tension-kind3-nonvirtual-host-domains-v1','author':'/root/arrangement_map_review','sole_actual_source_peer':'/root','frozen_input_utc':datetime.now(timezone.utc).isoformat(),'baseline_template':ident(P/'baseline-template.script'),'parameter_indices':inds,'parameter_tokens':tokens,'parameter_f32_bits_le':bits,'parameter_vector_sha256':s['parameter_vector_sha256'],'domains':domains,'excluded_virtual_kind3':[0,7,122,124,126,128],'aliases':aliases,'rows':rows,'history':s['history'],'source_pins':[ident(x) for x in sourcepaths],'source_input_scan':scan,'parent_launch_argv':['/usr/bin/python3','-I','-B',str(P/'launch.py'),'--run-once'],'parent_exec_argv':['/usr/bin/python3','-I','-B',str(P/'run_batch.py'),'--run-once'],'limits':{**c['limits'],'children':106,'selected_export_calls_total':23214,'CalcA_total':9222,'new_stereo_bytes_total':37396800,'loader_initializer_count_separate':106},'historical_scope':'11exacthistoricalinputreferences, nooldaudio/resultJSON/receipt/sourcebehavior reads. Three recipe-only freshmembers13=1/36=0/6=2 doNOTrepairoldunknownbridge.','domain_scope':'48nonvirtualdeclared0..maxdomains/164logicalaliases/117uniquevectors. Onehostwordonly, no crossproduct.91=5notordinaryLiveemission;sign1mag0/inactivegate/current/public/ARM unknown.','method_scope':'Existing129worddefaults44Tensionxdev/method only. No model/build/patch/provider/tool/newmetric/f0/fit/calibration/stability/publiclaw. Copiedmethodsourceinert, oldAuto222citation-only.'})
save('inputs.json',c);save('inherited-controls.json',{'old_raw_audio_reads':0,'new_original_calls':0,'controls':[{'id':x['id'],'historical':x['historical']} for x in rows if x['disposition']=='inherited-no-replay']});save('method-sources.json',{'sources':methods,'scope':'Exact copied preexisting methodsource bytes, retained/inert only, no import/build or new sourcebehavior audit.'})
# Owned new recorder source derived as inert text from our standing capture pattern, never imported/run.
code=(F/'batch-tension-note-keys-v1/run_batch.py').read_text().replace('123-child','106-child').replace("'note_key'","'unique_vector'").replace("[36, 48, 60, 72, 84]","[x['id'] for x in config['rows'] if x['disposition']=='inherited-no-replay']").replace('COMPLETE-123-ONCE','COMPLETE-106-ONCE').replace("'inherited_not_replayed': 5","'inherited_not_replayed': 11")
(P/'run_batch.py').write_text(code);(P/'launch.py').write_bytes((F/'batch-tension-note-keys-v1/launch.py').read_bytes())
# Protocol and unsigned output classes copied as new owned source; adaptive inputs use row-specific vectors, fixed C4events.
old=(F/'batch-tension-note-keys-v1/data.py').read_text();protocol=old[old.index('def protocol('):old.index('def selfchecks(')];protocol=protocol.replace("c['parameter_f32_bits_le']","row['parameter_f32_bits_le']").replace("str(row['note_key'])","'60'")
header='''"""Owned fixed finite host-domain inputs/protocol and unsigned stereo data only."""\nimport collections,copy,hashlib,re,struct\nfrom pathlib import Path\nHERE=Path(__file__).resolve().parent\ndef identity(path):\n p=Path(path);raw=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}\n'''
(P/'data.py').write_text(header+'\n'+protocol)
(P/'README.md').write_text('''# Tension complete nonvirtual kind-3 host domains\n\nRoot-selected unchanged standing harness class:54kind3 minus6virtual=48domains,allintegers0..declaredmax,164logicalaliases/117uniquevectors.106fresh and11exacthistoricalinputreferences(sharedbaseline+10), no replay. All129worddefaults44/event/rate/history unchanged exceptonehostword. Metadata legalhostdomain is not ordinaryLiveemission:91=5 exceeds N6ordinary0..4; sign1at0/inactiveLFO/gates/currentreceiver/publicARM remain unknown.\n\nThreefresh13=1/36=0/6=2 also have prior recipe-only relations; old missingchangedvector/process/raw bridge remainshistoricalU, never repaired by this capture. Historical11references keep only exactinputscript+oldmanifestWAVmetadata, no new raw/PID/receipt/metrics. Baselinealiasdedup exact.\n\nAllnewlaunch/data/recorder/checker/scripts/context/metadata/methodcopies freezeBEFORE once106children. ExistingTensionxdev/exactbundle/init260c0/model/environment/FP/time0 only.219selectedexports/87CalcA each →23214exports/9222CalcA/37396800stereoB;106initentriesseparate,nested/allnativeunknown.20sCPUwall/core0/4MiB/DEVNULL/newgroup/minimalenv,noLD/FPoverride; firstpostchildanomalystop/no retry/extension. Raw/log/JSONfilefsyncrequested;nodirectory/powerloss guarantee. Perchild16endpointpairsnotcontinuous/transitive/OSexec/fenv proof; plannedparentexec/sourcePIDrecordsnotOSattestation.\n\nUnsignedbothchannelfinite/identity/nonzero/negativezero summary class only. Allquiet/edge/nonfinite dispositions retained; nonfinite/shape/protocol/custodyfaultstopslaterchildren. NULLfreshpriors/portableexpected/comparator/grade,nof0/fit/newmetric/window/tolerance/calibration/stability/generalDSP/publicARMlaw. PriorAuto222citationonly,no oldsource/raw/metric replay.\n\nReadowneddata.py/run_batch.py/launch.py/check_data.py before data-only inputs/check. NEVER rerunlaunch/--run-once afterattempts exist. RootSOLEnewactual/sourcepeer afterfinalseal; onepacket/onereview/no readinesschain. Canonicalselection/statusonly,no owner/release/sharedroutingedit.\n''')
print(json.dumps({'dir':str(P),'rows':len(rows),'aliases':len(aliases),'fresh':fresh,'sources':len(sourcepaths)},indent=2))
