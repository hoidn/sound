import pathlib,json,hashlib,struct,shutil,ast,datetime
ROOT=pathlib.Path('/home/ollie/Documents/sound');B=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1';OLD=B/'batch-electric-note-keys-v1';P=B/'batch-electric-velocity-bytes-v1';P.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(path,offset=None,size=None):
 p=pathlib.Path(path).resolve()
 if offset is None:b=p.read_bytes()
 else:
  with p.open('rb') as f:f.seek(offset);b=f.read(size)
  assert len(b)==size
 x={'path':str(p),'bytes':len(b),'sha256':sha(b)}
 if offset is not None:x['offset']=offset
 return x
def save(n,d):(P/n).write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
reviewpath=B/'reviews/electric-transpose-integers-v1-review.json';rp=pin(reviewpath);assert rp['bytes']==365481 and rp['sha256']=='16783862180b314900c96762538313167874751f2fa68c5a867fdcbbf60a8e56'
r=json.loads(reviewpath.read_text());shared=r['approved_summary']['shared_input'];point=next(x for x in r['approved_summary']['approved_points'] if x['transpose_integer']==12)
assert point['provenance']=='inherited-approved-not-reexecuted' and point['fresh_receipt'] is None
words=[{'index':i,'token':t,'little_endian_hex':shared['baseline_parameter_f32_bits_le'][i],'reconstructed_binary64_le':struct.pack('<d',float(t)).hex()} for i,t in enumerate(shared['history']['baseline_parameter_tokens'])]
assert len(words)==33 and sha(b''.join(bytes.fromhex(w['little_endian_hex']) for w in words))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
history={'review_pin':rp,'review_pointer':'/approved_summary/approved_points/12','approved_point':point,'owner_case':'DEL-CS-001','release_case':'ELECTRIC-AUDIO-004','stored_aliases':[11.99999,12],'new_pid':None,'new_receipt':None,'scope':'One inherited velocity100 input at key60/P1 only; approved metadata, no prior audio/source/result/receipt opened or replayed.'}
d={'schema':'whole-Electric-P1-note-on-velocity-byte-v1','counts':{'logical':128,'inherited':1,'fresh_children':127,'direct_exports':18415,'CalcA':13843,'stereo_bytes':56249824},'words':words,'fixture':{'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'key':60,'on_velocity':'catalog_byte','off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'},'catalog':[],'plans':[]}
(P/'scripts').mkdir();(P/'protocol').mkdir()
for v in range(128):
 ev=[[11264,144,60,v],[33314,128,60,0]];d['catalog'].append({'velocity_byte':v,'events':ev,'packed16_events_le':[struct.pack('<qBBBB4x',*e,0).hex() for e in ev],'provenance':'inherited-no-replay' if v==100 else 'fresh-selected','historical':history if v==100 else None,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None})
 if v!=100:
  text='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in words]+[f'event 11264 0x90 60 {v}','event 33314 0x80 60 0','inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n';path=P/'scripts'/f'velocity-{v:03}.script';path.write_text(text);d['plans'].append({'velocity_byte':v,'script':str(path),'direct_exports':145,'CalcA':109,'output_bytes':442912})
save('inputs.json',d);save('approved-prior-summary.json',{'review_pin':rp,'shared_input':shared,'velocity100_ETI12':point,'scope':'Approved inherited input/control metadata only; old actual/audio/source/results/receipts not opened or replayed.'})
# Exact old host input declarations only, excluding all estimator/result expressions.
src=ROOT/'analysis/ableton-live-12.4.3/r2/t12-electric-v1/probes_events.py';raw=src.read_bytes();assert len(raw)==11205 and sha(raw)=='23d81d71b9f0d94aa921941f6e48957b6c8b9fdb4082df34d907ebbf3d888309';text=raw.decode();tree=ast.parse(text)
extracts=[]
for line in [63,66,190]:
 matches=[x for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and isinstance(x.func.value,ast.Name) and x.func.value.id=='el' and x.func.attr in ['render','note'] and x.lineno==line]
 # Prefer full render input call; no outer same()/reported result expression retained.
 x=next((x for x in matches if x.func.attr=='render'),matches[0]);s=ast.get_source_segment(text,x);extracts.append({'source_pin':pin(src),'line_start':x.lineno,'line_end':x.end_lineno,'column_start':x.col_offset,'column_end':x.end_col_offset,'text':s,'bytes':len(s.encode()),'sha256':sha(s.encode())})
for lo,hi in [(188,189),(197,197)]:
 s='\n'.join(text.splitlines()[lo-1:hi])+'\n';extracts.append({'source_pin':pin(src),'lines':[lo,hi],'text':s,'bytes':len(s.encode()),'sha256':sha(s.encode())})
olddecl=json.loads((OLD/'historical-input-declarations.json').read_text());recipe=[x for x in olddecl['extracts'] if pathlib.Path(x['source_pin']['path']).name=='el.py']
save('input-eligibility.json',{'schema':'bounded-Electric-P1-velocity-input-intersection-v1','extracts':extracts,'existing_owned_el_input_recipe':recipe,'old_class':{'FV':[0,.5,1],'SV':[0,.5,1],'note_on_velocities':[1,16,32,64,96,100,127],'logical_inputs':63,'host_indices':[9,6],'warmup':11264,'render':22050,'relative_off':13230,'absolute_off':24494,'absolute_end':33314},'selected_P1':{'warmup':11264,'render':44100,'relative_off':22050,'absolute_on':11264,'absolute_off':33314,'absolute_end':55364,'key':60,'on_velocity':'whole128'},'later_zero_event':{'prior_note_on_velocity':100,'render_relative_on':0,'render_relative_zero_velocity_note':13230,'absolute_zero_velocity_note':24494,'render':22050,'scope':'Later status90 velocity0 after100, not fresh-creation noteon0 P1 history.'},'exact_inherited_only':[100],'fresh_velocities':[v for v in range(128) if v!=100],'old_raw_reads':0,'scope':'Bounded selected host input declarations/protocol recipes only. No old estimators/results/audio/source-body execution or global historical-absence claim. Old63 and zero-event histories do not add exact P1 matches.'})
methods=[]
auth=json.loads((OLD/'authority-pins.json').read_text())
for f in sorted((OLD/'protocol').iterdir()):
 orig=next(x for x in auth['unchanged_method_sources'] if pathlib.Path(x['path']).name==f.name);b=f.read_bytes();assert len(b)==orig['bytes'] and sha(b)==orig['sha256'];shutil.copyfile(f,P/'protocol'/f.name);methods.append(orig)
oldctx=json.loads((OLD/'context.json').read_text());roles=[]
for x in oldctx['watched_roles']:
 expected=x['identity'];actual=pin(expected['path'],expected.get('offset'),expected['bytes'] if 'offset' in expected else None);assert actual==expected;roles.append(x)
save('authority-pins.json',{'prior_summary':rp,'unchanged_method_sources':methods,'method_semantics':'Inherited approved unchanged Electric xdev factory/rate/all33params/cumulativeevents/2processes/clock0/perexportMXCSR1f80/stubs; no new body/native/ABI/provider/model proof.','parent_method_packet_metadata':pin(OLD/'manifest.json'),'current_owner_asof_before_freeze':pin(ROOT/'wiki/specs/device-electric.md'),'source_origin':'Retained method bytes and endpoint hash identities, not historical or continuous loaded-provider closure.','old_modules_imported_or_compiled':False,'prior_actual_audio_results_reopened':False})
ctx={**oldctx,'sole_peer':'arrangement_map_review (Arr)','Root_scope':'Citation-only all new actual/code/source/raw/results; no duplicate review','host':{**oldctx['host'],'scope':'Inherited host metadata, no independent OSexec attestation; current recorder source binds planned executable paths and endpoint file hashes.'}}
ctx['watched_roles']=roles;save('context.json',ctx)
record=(OLD/'record.py').read_text().replace("'whole-Electric-P1-note-key-byte-v1'","'whole-Electric-P1-note-on-velocity-byte-v1'")
record=record.replace("['key']","['velocity_byte']").replace('["key"]','["velocity_byte"]').replace("{'key':v,","{'velocity_byte':v,")
record=record.replace("f'key-","f'velocity-").replace("print('key',","print('velocity',")
record=record.replace('f\'event 11264 0x90 {v} 100\',f\'event 33314 0x80 {v} 0\'',"f'event 11264 0x90 60 {v}','event 33314 0x80 60 0'")
record=record.replace("[v for v in range(128) if v!=60]","[v for v in range(128) if v!=100]")
record=record.replace("[[11264,144,r['velocity_byte'],100],[33314,128,r['velocity_byte'],0]]","[[11264,144,60,r['velocity_byte']],[33314,128,60,0]]")
record=record.replace("(r['velocity_byte']==60)","(r['velocity_byte']==100)")
record=record.replace("'on_velocity':100,","'key':60,'on_velocity':'catalog_byte',")
record=record.replace('.update(key=60)', '.update(velocity_byte=100)').replace("x['catalog'][60].update(historical=None)","x['catalog'][100].update(historical=None)")
record=record.replace("assert [r['velocity_byte'] for r in d['catalog']]==list(range(128))","assert [r['velocity_byte'] for r in d['catalog']]==list(range(128)) and all(type(r['velocity_byte']) is int for r in d['catalog'])")
record=record.replace("('on-key',lambda x:x['catalog'][0]['events'][0].__setitem__(2,1)),","('on-key',lambda x:x['catalog'][0]['events'][0].__setitem__(2,1)),('on-velocity',lambda x:x['catalog'][0]['events'][0].__setitem__(3,1)),")
(P/'record.py').write_text(record)
check=(OLD/'check-recorded.py').read_text().replace("['key']","['velocity_byte']").replace("{'key':c['velocity_byte']","{'velocity_byte':c['velocity_byte']")
check=check.replace("'event 11264 0x90 0 100','event 33314 0x80 0 0'","'event 11264 0x90 60 0','event 33314 0x80 60 0'")
check=check.replace("oldon=f'event 11264 0x90 {key} 100';oldoff=f'event 33314 0x80 {key} 0'","oldon=f'event 11264 0x90 60 {key}';oldoff='event 33314 0x80 60 0'")
check=check.replace("f'event 11264 0x90 {(key+1)%128} 100'","f'event 11264 0x90 60 {(key+1)%128}'").replace("f'event 33314 0x80 {(key+1)%128} 0'","'event 33314 0x80 61 0'").replace("f'event 33314 0x80 {key} 1'","'event 33314 0x80 60 1'")
check=check.replace("('on-key',text.replace(oldon,","('on-velocity',text.replace(oldon,")
check=check.replace("'key':c['velocity_byte']","'velocity_byte':c['velocity_byte']")
(P/'check-recorded.py').write_text(check)
for n in ['launch-once.py','freeze.py']:
 code=(OLD/n).read_text().replace('automation_actual_review (Auto)','arrangement_map_review (Arr)').replace('inherited_key60_only','inherited_velocity100_only').replace('historical_key60_no_replay','historical_velocity100_no_replay')
 (P/n).write_text(code)
(P/'assemble-inputs.py').write_bytes(pathlib.Path(__file__).read_bytes())
(P/'README.md').write_text('''# Electric whole P1 note-on velocity-byte class

Root selected all 128 typed note-on data2 bytes at the approved P1 fixture. Only 127 values 0–99 / 101–127 execute once. Velocity 100 is inherited from approved ETI-12 / DEL-CS-001 / ELECTRIC-AUDIO-004, both stored transpose aliases attached, with no extra logical point, old audio/source/results/receipt reads or fabricated fresh receipt.

Only note-on data2 changes. Key 60, all 33 ordered binary32 words (132-byte vector SHA 9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a), rate 44,100, zero input/flag 0, stopped transport 0/0/120, 11,264 warmup frames and 44,100 render frames in 512-frame blocks (last 68) remain fixed. On is absolute frame 11,264/status90/catalog data2; off is frame 33,314/status80/key60/data2=0; end is 55,364. Existing unchanged Electric xdev constructor/rate/all setters/cumulative events/two process calls/destroy, stubs, clock0 and per-export MXCSR1f80 model only. No new tool, provider, patch, build, construction, FP/libm override or state product.

The bounded input-only eligibility packet retains old FV/SV {0,.5,1} × velocities {1,16,32,64,96,100,127}: 63 histories used 22,050 render / off13,230 after warmup11,264. The older velocity-zero event follows velocity100 in that shorter history. These are not the current fresh P1 history; no global historical-absence claim or estimator/result replay. Quiet velocity0, endpoints, silent and nonfinite outputs are retained; nonfinite/failed children stop later execution without retry. No prior silence or productive velocity curve is asserted.

All new capture code INCLUDING parent launcher, inputs/scripts/packed events, methods/authority/context/environment are frozen before calls. The parent launcher records planned recorder argv/environment/preseal and PID; sys.argv/path strings and endpoint hashes are not independent OS exec/interpreter/provider/FP-state attestation. Custody is one common initial baseline compared with every child-after and final-after endpoint, NOT per-child-before snapshots. Imports are declarations versus counted code use, not data/global/transitive absence proof. 127 sequential once-only children imply 18,415 selected direct exports / 13,843 CalcA / 56,249,824 interleaved stereo bytes including warmup; logged initializers/nested native calls remain separate/unknown.

Read full record.py / launch-once.py / check-recorded.py / freeze.py / assemble-inputs.py before owned data-only checks. Only launch-once.py with frozen pre-call SHA starts the one original attempt. No retry/resume/fallback after attempts exist. Children use DEVNULL/minimal environment/new group/core0/20s CPU+wall/4MiB regular-file cap; first post-child detected error stops future children, not already queued calls within one child. Catchable cleanup can fail under SIGKILL/host loss/escaped descendants/IO failure. Recorder/launcher JSON request regular-file fsync; raw/log/audio are closed+hashed without explicit FD fsync. No directory/power-loss guarantee.

Safe data checks: python3 -I -B check-recorded.py --self-check, then after capture --check. NEVER rerun launcher/record --run-once/assemble-inputs or compile/import old method helpers. Rate return is an opaque signed integer; original supplied waveform priors, portable expected/comparator and grades remain NULL. Only size/finiteness/stereo-byte-identity/numeric warmup-zero/render zero counts are mechanical observations; no new f0/fit/metric/tolerance/calibration, productive velocity curve, general zero-event/dispatch/public clock/audio/lifecycle law, current receiver/A1/A2 or ARM/Apple equivalence. Required unknowns and product OPEN persist.

Arr is sole independent actual/source peer after final seal; author Auto does not review its own actual. Root adopts by citation only, without duplicate new source/code/raw/results review. Only canonical Electric research selection/status is updated by author; no shared routing, owner cases, grade or release changes.
''')
print(json.dumps({'folder':str(P),'code_written':True,'original_calls':0,'catalog':128,'scripts':127,'runtime_roles':len(roles)}))
