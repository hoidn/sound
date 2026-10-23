#!/usr/bin/env python3
"""One-time fixed128catalog/127script generation; no original call or old helper import."""
import hashlib,json,pathlib,shutil,platform,sys,os,struct
H=pathlib.Path(__file__).resolve().parent;B=H.parent;T=B.parent/'r2/t12-electric-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,offset=None,size=None):
 p=pathlib.Path(p).resolve()
 if offset is None:raw=p.read_bytes();return {'path':str(p),'bytes':len(raw),'sha256':sha(raw)}
 with p.open('rb') as f:f.seek(offset);raw=f.read(size)
 assert len(raw)==size;return {'path':str(p),'bytes':len(raw),'sha256':sha(raw),'offset':offset}
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
assert not (H/'inputs.json').exists()
report=B/'reviews/electric-transpose-integers-v1-review.json';rp=pin(report);assert rp['bytes']==365481 and rp['sha256']=='16783862180b314900c96762538313167874751f2fa68c5a867fdcbbf60a8e56';r=json.loads(report.read_text());shared=r['approved_summary']['shared_input'];point=next(x for x in r['approved_summary']['approved_points'] if x['transpose_integer']==12)
assert point['provenance']=='inherited-approved-not-reexecuted' and point['fresh_receipt'] is None and point['portable_comparator'] is None
words=[{'index':i,'token':v,'little_endian_hex':shared['baseline_parameter_f32_bits_le'][i],'reconstructed_binary64_le':struct.pack('<d',float(v)).hex()} for i,v in enumerate(shared['history']['baseline_parameter_tokens'])]
assert len(words)==33 and sha(b''.join(bytes.fromhex(w['little_endian_hex']) for w in words))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
old={'review_pin':rp,'review_pointer':'/approved_summary/approved_points/12','approved_point':point,'owner_case':'DEL-CS-001','release_case':'ELECTRIC-AUDIO-004','stored_aliases':[11.99999,12],'new_pid':None,'new_receipt':None,'scope':'Approved summary/input metadata only; no prior actual/audio/source/receipt replay or fabricated new historical information'}
d={'schema':'whole-Electric-P1-note-key-byte-v1','counts':{'logical':128,'inherited':1,'fresh_children':127,'direct_exports':18415,'CalcA':13843,'stereo_bytes':56249824},'words':words,'fixture':{'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'on_velocity':100,'off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'},'catalog':[],'plans':[]}
(H/'scripts').mkdir();(H/'protocol').mkdir()
for key in range(128):
 events=[[11264,144,key,100],[33314,128,key,0]];d['catalog'].append({'key':key,'events':events,'packed16_events_le':[struct.pack('<qBBBB4x',*e,0).hex() for e in events],'provenance':'inherited-no-replay' if key==60 else 'fresh-selected','historical':old if key==60 else None,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
 if key!=60:
  text='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in words]+[f'event 11264 0x90 {key} 100',f'event 33314 0x80 {key} 0','inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n';path=H/'scripts'/f'key-{key:03}.script';path.write_text(text);d['plans'].append({'key':key,'script':str(path),'direct_exports':145,'CalcA':109,'output_bytes':442912})
save('inputs.json',d);save('approved-prior-summary.json',{'review_pin':rp,'shared_input':shared,'key60_ETI12':point,'scope':'Inherited approved context/control only. Prior actual/source/raw/results not opened; no duplicate prior observation review.'})
# Only already-selected input declarations, excluding estimators/numeric results.
extracts=[]
for name,ranges,expected in [('probes_events.py',[(21,21),(63,64),(72,73),(109,112),(119,126)],'23d81d71b9f0d94aa921941f6e48957b6c8b9fdb4082df34d907ebbf3d888309'),('el.py',[(30,31),(107,125),(142,150),(156,157)],'8b27fdfe5acea97b50116d70ac792bf6f22b8e9ceb1eb274ee35d9924e5d71a5')]:
 p=T/name;raw=p.read_bytes();assert sha(raw)==expected;lines=raw.decode().splitlines()
 for lo,hi in ranges:
  text='\n'.join(lines[lo-1:hi])+'\n';extracts.append({'source_pin':pin(p),'lines':[lo,hi],'utf8_bytes':len(text.encode()),'sha256':sha(text.encode()),'text':text})
save('historical-input-declarations.json',{'source_expression_only':True,'extracts':extracts,'intersection':{'P1_exact_inherited_keys':[60],'fresh_keys':list(range(60))+list(range(61,128)),'historical_all128_tuning':{'rate':44100,'warmup':11264,'block':512,'render_frames':17640,'render_on':0,'render_off':17640,'absolute_on':11264,'absolute_off':28904,'exclusive_end':28904},'historical_edge0_127_and_base60_A4_69':{'rate':44100,'warmup':11264,'block':512,'render_frames':22050,'render_on':0,'render_off':13230,'absolute_on':11264,'absolute_off':24494,'exclusive_end':33314},'selected_P1':{'rate':44100,'warmup':11264,'block':512,'render_frames':44100,'render_on':0,'render_off':22050,'absolute_on':11264,'absolute_off':33314,'exclusive_end':55364},'released_other_keys':'21/36/48/72/84/96/108 have22050render/off13230, notP1','scope':'Exact bounded selected declarations/input/release metadata; no global absence claim. Historical key domain already existed, but these complete histories differ. No numeric oldresults or estimator behavior used.'}})
methods=[]
for name in ['xdev.h','xdev.c','xdev_load.c','xdev_bind.c','xdev_cxx.c']:
 src=T/'harness'/name;shutil.copyfile(src,H/'protocol'/name);methods.append(pin(src))
# No whole el.py/probes_events.py copied; only inputrecipe excerpts above.
save('authority-pins.json',{'prior_summary':rp,'old_review':pin(B/'reviews/electric-control-seams-v1-review.json'),'owner_case_metadata':pin(B/'owner-electric-r3-finite-v1/cases.json'),'family_manifest':pin(B/'family-electric-routes-v1/manifest.json'),'release_input_metadata':pin(pathlib.Path('/home/ollie/Documents/sound/handoff/device-electric-v2/cases.json')),'source_origin':'Retained historical authority; copied source and hash identity do not repair historical custody','unchanged_method_sources':methods,'current_owner_asof_before_freeze':{**pin(pathlib.Path('/home/ollie/Documents/sound/wiki/specs/device-electric.md')),'revision':4,'scope':'Currentasofowneridentity; inputcontextunchanged'},'old_modules_imported_or_compiled':False,'prior_actual_packets_reopened':False})
roles=[]
expected=r['collector_semantics']['recorded_custody']['runtime_expected']
for role,item in zip(['loader','bundle','libm','libc','libstdcxx','libgcc','elf_interpreter','ld_cache','python'],expected):
 actual=pin(item['resolved_path']);assert actual['bytes']==item['bytes'] and actual['sha256']==item['sha256'];roles.append({'role':role,'identity':actual})
assert len(roles)==9 and roles[0]['identity']['bytes']==149688 and roles[0]['identity']['sha256']=='6eb5dd284452960f623e0bb6ed26b8743bdf789b8eac09a48b4a9291995ed8e1'
bundle=roles[1]['identity']['path'];sliceid=pin(bundle,16384,267648);assert sliceid['sha256']=='f121bb8d66ec1f3d8e9cb830e8081b25922cece6011cc12857c78180cd89dd32';roles.append({'role':'selected_x86_slice','identity':sliceid});assert pathlib.Path(sys.executable).resolve()==pathlib.Path(roles[8]['identity']['path'])
save('context.json',{'exe':roles[0]['identity']['path'],'bundle':bundle,'python':roles[8]['identity']['path'],'watched_roles':roles,'environment':shared['environment'],'host':{'uname':list(platform.uname()),'python':sys.version,'byteorder':sys.byteorder,'executable':sys.executable},'sole_peer':'automation_actual_review (Auto)','Root_scope':'Citation-only; no new source/code/raw/results peer replay','limits':{'CPU_seconds':20,'wall_seconds':20,'CORE':0,'FSIZE':4194304,'stdin':'DEVNULL','new_process_group':True,'retry':False},'phase_policy':'Existing per-callMXCSR1f80, XDEV_TIME0/unperturbed bindings; no new constructor/provider/FP/seed treatment. Rate signedint opaque.','stop_policy':'First detected anomaly stops later children. Childqueued calls may already have run; no retry/fallback/extension. SIGKILL/hostloss may leave partial status; no automatic resume.'})
print(json.dumps({'status':'MATERIALIZED-ONCE','scripts':127,'catalog':128,'watched_roles':len(roles),'original_calls':0}))
