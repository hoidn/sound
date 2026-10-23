import pathlib,json,hashlib,struct,shutil,platform,sys
ROOT=pathlib.Path('/home/ollie/Documents/sound');B=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1';OLD=B/'batch-corpus-deterministic-free-lfo-continuation-v1';P=B/'batch-corpus-native-integer-domains-v1';P.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p,offset=None,size=None):
 p=pathlib.Path(p).resolve()
 if offset is None:b=p.read_bytes()
 else:
  with p.open('rb') as f:f.seek(offset);b=f.read(size)
  assert len(b)==size
 d={'path':str(p),'bytes':len(b),'sha256':sha(b)}
 if offset is not None:d['offset']=offset
 return d
def save(n,d):(P/n).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
ep=B/'reviews/corpus-whole-native-integer-domain-eligibility.json';e=json.loads(ep.read_text());assert pin(ep)['bytes']==34772 and pin(ep)['sha256']=='3886b9df1831aa755f9ed2ef43c24f09968b9fb82baa444ff92b9ae87e57ee12'
rp=B/'reviews/corpus-deterministic-free-lfo-continuation-v1-review.json';r=json.loads(rp.read_text());assert pin(rp)['sha256']=='6427a0e75470c0758dbfd4ea4afae49d6c6b3261c43d854fa705f69d0bc58f6b' and r['blocking_findings']==[]
save('eligibility.json',e);save('approved-prior-summary.json',{'review_pin':pin(rp),'approved_summary':r['approved_summary'],'history':r['history'],'limits':r['limits'],'shape5_qualified_reference':e['extra_historical_shape5'],'scope':'Only approved summary and Root bounded metadata; no old output/raw/audio, PID/receipt invention, source/estimator replay or original retry.'})
oldinputs=json.loads((OLD/'inputs.json').read_text());assert oldinputs['base_params']==e['base_params'];base=e['base_params'];b32=lambda x:struct.pack('<f',float(x)).hex();vecsha=lambda v:sha(b''.join(struct.pack('<f',float(x)) for x in v))
inherited={}
for point in r['approved_summary']['approved_points']:
 v=base.copy();v[18]=float(point['shape']);assert [f'{struct.unpack("<I",struct.pack("<f",x))[0]:08x}' for x in v]==point['parameter_bits32'];inherited[vecsha(v)]={'kind':'approved-summary-no-replay','review_pin':pin(rp),'review_pointer':f'/approved_summary/approved_points/{point["shape"]}','approved_point':point,'fresh_pid':None,'fresh_receipt':None,'new_metrics':None}
v=base.copy();v[18]=5.;inherited[vecsha(v)]={'kind':'qualified-historical-shape5-metadata-only','eligibility_pin':pin(ep),'pointer':'/extra_historical_shape5','historical':e['extra_historical_shape5'],'fresh_pid':None,'fresh_receipt':None,'new_metrics':None,'qualification':e['extra_historical_shape5']['qualification']}
assert len(inherited)==6
catalog=[];unique=[];byhash={}
(P/'scripts').mkdir();(P/'protocol').mkdir()
# Exact supplied I1 bytes are input data, not any old original output.
inputsource=ROOT/'analysis/ableton-live-12.4.3/r2/t12-device-dsp-v1/inputs/impulse44.f32';raw=inputsource.read_bytes();assert len(raw)==131072 and sha(raw)=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6';(P/'input.f32').write_bytes(raw)
def script(words):return '\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in words]+['inflag 1','input '+str(P/'input.f32'),'process 16384 512','destroy'])+'\n'
for i,row in enumerate(e['catalog']):
 v=base.copy();v[row['index']]=float(row['value']);h=vecsha(v);assert h==row['vector_sha256']
 if h not in byhash:
  uid=f'CNI-V{len(unique):03}';byhash[h]=uid;words=[{'index':j,'token':repr(float(x)),'binary32_le':b32(x),'host_reconstructed_binary64_le':struct.pack('<d',float(x)).hex()} for j,x in enumerate(v)]
  u={'id':uid,'first_alias':{'index':row['index'],'value':row['value']},'vector_sha256':h,'words':words,'alias_ids':[],'disposition':'inherited-no-replay' if h in inherited else 'fresh-selected','inherited':inherited.get(h),'new_expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None}
  if h not in inherited:
   path=P/'scripts'/(uid+'.script');path.write_text(script(words));u['script']=pin(path)
  unique.append(u)
 uid=byhash[h];aid=f'CNI-A{i:03}';unique[next(j for j,x in enumerate(unique) if x['id']==uid)]['alias_ids'].append(aid);catalog.append({'id':aid,'index':row['index'],'value':row['value'],'vector_id':uid,'vector_sha256':h,'new_expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
assert len(catalog)==69 and len(unique)==63 and sum(x['disposition']=='fresh-selected' for x in unique)==57
plans=[{'vector_id':u['id'],'vector_sha256':u['vector_sha256'],'script':u['script'],'direct_exports':73,'CalcA':32,'output_bytes':131072} for u in unique if u['disposition']=='fresh-selected']
save('inputs.json',{'schema':'whole-Corpus-native-integer-domains-v1','domains':e['domains'],'base_params':base,'baseline_vector_sha256':vecsha(base),'catalog':catalog,'vectors':unique,'plans':plans,'input':pin(P/'input.f32'),'fixture':{'rate':44100,'frames':16384,'block':512,'last_block':512,'inflag':1,'I1_impulse_frame':4096,'transport':[0,0,120],'MXCSR':'0x1f80','warmup':0,'XDEV_TIME':'0','XDEV_LIBM_ULP':'0'},'counts':{'aliases':69,'unique_vectors':63,'inherited_vectors':6,'fresh_children':57,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104}})
oldctx=json.loads((OLD/'context.json').read_text());roles=[]
for x in oldctx['watched_roles']:
 expected=x['identity'];actual=pin(expected['path'],expected.get('offset'),expected['bytes'] if 'offset' in expected else None)
 assert {k:expected[k] for k in actual}==actual
 # Preserve selected-slice role annotation used by existing recorded method.
 roles.append(x)
assert len(roles)==9
py=next(x['identity']['path'] for x in roles if x['role']=='python');assert pathlib.Path(sys.executable).resolve()==pathlib.Path(py)
context={**oldctx,'python':py,'host':{'uname':list(platform.uname()),'python':sys.version,'byteorder':sys.byteorder,'sys_executable':sys.executable},'watched_roles':roles,'sole_peer':'Root','Root_role':'Sole independent actual/source peer; Auto is author and cannot approve own actual','parent_launch_argv_template':[py,'-I','-B',str(P/'launch-once.py'),'{sha256(pre-call-manifest.json)}'],'recorder_argv_template':[py,'-I','-B',str(P/'record.py'),'--run-once','{sha256(pre-call-manifest.json)}'],'input_copy':pin(P/'input.f32'),'custody_scope':'One common initial whole-batch endpoint baseline compared with every child-after/final-after; NOT per-child-before/continuous/provider/OSexec/FP attestation.','history':'Previous Square failure/partial phases/unusedprepare and historical initialgeneration qualifications retained only by approved review citation; not repaired or rerun. Parked96bytes and174+2modalomissions untouched.'};save('context.json',context)
oldmanifest=json.loads((OLD/'manifest.json').read_text());methodpins=[]
for x in oldmanifest['files']:
 if x['path'].startswith('protocol/'):
  f=OLD/x['path'];b=f.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256'];shutil.copyfile(f,P/x['path']);methodpins.append({'historical_path':str(f),'owned_path':x['path'],'bytes':len(b),'sha256':sha(b)})
save('authority-pins.json',{'eligibility':pin(ep),'approved_review':pin(rp),'old_input_recipe':pin(OLD/'inputs.json'),'copied_method_pins':methodpins,'current_owner_asof':pin(ROOT/'wiki/specs/corpus-device.md') if (ROOT/'wiki/specs/corpus-device.md').exists() else None,'no_oldmodules_imported_compiled_or_called':True,'no_old_output_audio_read':True,'scope':'Only retained old input/model/approved summary/Root metadata; no new source/native/provider/constructor or version-binding repair.'})
(P/'assemble-inputs.py').write_bytes(pathlib.Path(__file__).read_bytes())
print(json.dumps({'folder':str(P),'aliases':69,'vectors':63,'fresh':57,'inherited':6,'original_calls':0,'method_files':len(methodpins)}))
