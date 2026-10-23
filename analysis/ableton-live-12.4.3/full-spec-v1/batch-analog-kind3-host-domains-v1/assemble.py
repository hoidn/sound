#!/usr/bin/env python3
"""One fixed selected338alias/254vector input materialization. No original execution/importoldhelper/build."""
import hashlib,json,pathlib,struct,shutil,sys,os
H=pathlib.Path(__file__).resolve().parent;F=H.parent;A=F.parent;ROOT=H.parents[3];OLD=F/'batch-analog-transpose-integers-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 p=pathlib.Path(p).resolve();b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with (H/n).open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def bits(v):return struct.pack('<f',float(v)).hex()
assert len(sys.argv)==3 and not(H/'inputs.json').exists();review=pathlib.Path(sys.argv[1]).resolve();rp=pin(review);assert rp['sha256']==sys.argv[2]
rr=json.loads(review.read_text());assert 'APPROVED'in rr['disposition'] and not rr.get('blocking_findings',[]) and not rr.get('required_corrections',[])
# Prerequisite is an external sealed approval, not this author's own assertion.
assert review.stat().st_mode&0o222==0
old=json.loads((OLD/'inputs.json').read_text());base=[w['little_endian_hex']for w in old['words']];words=old['words'];assert len(base)==203 and sha(bytes.fromhex(''.join(base)))=='18a94879168c2f73d621883d3a60b14de6f54a2b396fb8a0b11284c799926ed3'
summary=rr['approved_summary'];points=summary['approved_points'];assert len(points)==25
pointvalues=[p['transpose_integer']for p in points];assert pointvalues==list(range(25))
sp=A/'r2/t12-analog-v1/results/static_map.json';sm=json.loads(sp.read_text());domains=[{'host_index':r['index'],'kind':'kind3','maximum':int(r['range_or_max']),'baseline':int(struct.unpack('<f',bytes.fromhex(base[r['index']]))[0]),'source_pointer':f'/index_map/{r["index"]}'}for r in sm['index_map']if r['kind']=='kind3'];assert len(domains)==85 and sum(x['maximum']+1 for x in domains)==338
ap=F/'owner-analog-r3-finite-v1/case-aliases.json';aliases=json.loads(ap.read_text());mode={};mip=F/'batch-analog-envelope-modes-v1/inputs.json';mi=json.loads(mip.read_text());r3review=F/'reviews/batch-analog-envelope-modes-v1-review.json';assert pin(r3review)['sha256']=='46402c9f899684c5e105301c522894b43f44ee8b52acb2c501251213c338250f';assert mi['inputs'][0]['parameter_f32_bits_le']==base
modeprojection=[]
for ordinal,c in enumerate(aliases['cases']):
 if'mode_change'not in c:continue
 z=c['mode_change'];i,v=z['host_index'],z['host_value'];q=mi['inputs'][int(c['input_source']['pointer'].split('/')[-1])];wb=base.copy();wb[i]=bits(v);assert q['parameter_f32_bits_le']==wb and c['parameter_vector_sha256']==sha(bytes.fromhex(''.join(wb)))
 assert c['history']=={'rate':44100,'frames':44100,'block_frames':512,'transport':[0,0,120],'events':[[4400,144,60,100],[35270,128,60,64]],'index99':1,'process_requests':1,'post_start_param_changes':0}
 mode[(i,v)]={'source_case':c['source_case'],'id':c['id'],'owner_alias_pointer':f'/cases/{ordinal}','observation_review':c['observation_review'],'input_source':c['input_source'],'history':c['history'],'vector_sha256':c['parameter_vector_sha256']};modeprojection.append(mode[(i,v)])
assert len(mode)==20
hist=['create','rate 44100','event 4400 0x90 60 100','event 35270 0x80 60 64','inflag 0','input zero','process 44100 512','destroy'];dom={r['host_index']:range(r['maximum']+1)for r in domains}
def classify(ws,history):
 if history!=hist:return 'different-history',None
 if len(ws)!=203 or [i for i,b in ws]!=list(range(203)):return 'different-paramorder',None
 diff=[(i,b)for i,b in ws if b!=base[i]]
 if not diff:return 'baseline',None
 if len(diff)==1:
  i,b=diff[0];v=struct.unpack('<f',bytes.fromhex(b))[0]
  if i in dom and v in dom[i]:return 'one-kind3',[i,int(v)]
 return 'different-vector',None
om=A/'r2/t12-analog-v1/manifest.json';manifest=json.loads(om.read_text());scripts=[]
for p in sorted((A/'r2/t12-analog-v1/raw').glob('DAN-*.script')):
 raw=p.read_bytes();assert manifest['files']['raw/'+p.name]=={'bytes':len(raw),'sha256':sha(raw)};ws=[];history=[]
 for l in raw.decode().splitlines():
  z=l.split()
  if z and z[0]=='param':ws.append((int(z[1]),bits(z[2])))
  elif z:history.append(' '.join(z))
 status,pair=classify(ws,history);scripts.append({'pin':pin(p),'parameter_words':ws,'history':history,'classification':status,'pair':pair})
assert len(scripts)==47 and [(x['pin']['path'].split('/')[-1],x['pair'])for x in scripts if x['classification']=='one-kind3']==[('DAN-029.script',[100,0])]
cp=ROOT/'handoff/device-analog-v1/cases.json';cases=json.loads(cp.read_text());released=[]
for gi,g in enumerate(cases['cases']):
 for ei,e in enumerate(g['evaluations']):
  assert all(x['kind']in['note_on','note_off']for x in e['events']);ev=[f'event {x["frame"]} {(0x90 if x["kind"]=="note_on"else 0x80)+x["channel"]:#x} {x["key"]} {x["velocity"]}'for x in e['events']]
  history=['create',f'rate {e["sample_rate_hz"]}',*ev,'inflag 0','input zero',f'process {e["frames"]} {e["block_frames"]}','destroy'];ws=[(i,bits(e['parameters'][n]))for i,n in enumerate(e['parameter_order'])];status,pair=classify(ws,history)
  released.append({'id':e['id'],'source_pointer':f'/cases/{gi}/evaluations/{ei}','parameter_words':ws,'history':history,'classification':status,'pair':pair,'signal':e['signal']})
assert len(cases['cases'])==38 and len(released)==42 and [(x['id'],x['pair'])for x in released if x['classification']=='one-kind3']==[('ANALOG-AUDIO-029-01',[100,0])]
for rows,count in[(scripts,45),(released,40)]:assert sum(x['classification']=='different-history'for x in rows)==count and sum(x['classification']=='baseline'for x in rows)==1
save('historical-input-joins.json',{'scope':'47selected retainedscripts/42releasedinputdeclarations ONLY; no audio/metric/estimator/sourcebehavior read. Current sourceversion not independent historicalexecution/version attestation; no universalabsence.','old_manifest':pin(om),'script_rows':scripts,'released_cases_pin':pin(cp),'released_input_rows':released,'R3_input_pin':pin(mip),'R3_owner_alias_pin':pin(ap),'R3_review':pin(r3review),'R3_mode_input_projection':modeprojection,'old335_input_join':json.loads((OLD/'historical-input-declarations.json').read_text())})
(H/'scripts').mkdir();(H/'protocol').mkdir();vectors=[];av=[];plans=[];byhash={};events=[[4400,144,60,100],[35270,128,60,64]]
for row in domains:
 i=row['host_index']
 for v in range(row['maximum']+1):
  wb=base.copy();wb[i]=bits(v);key=sha(bytes.fromhex(''.join(wb)));ref=None
  if v==row['baseline']:prov='baseline';ref={'approved_review':rp,'approved_point_pointer':f'/approved_summary/approved_points/{pointvalues.index(12)}','case_refs':['AVB100','DAN-028','CONTROL-DAN028-P1']}
  elif(i,v)in mode:prov='R3-mode';ref=mode[(i,v)]
  elif i==4:prov='Transpose-approved';ref={'approved_review':rp,'approved_point_pointer':f'/approved_summary/approved_points/{pointvalues.index(v)}','host_index':4,'host_value':v}
  elif(i,v)==(100,0):prov='released-DAN029';ref={'script_pin':next(x['pin']for x in scripts if x['pair']==[100,0]),'released_cases_pin':pin(cp),'released_input_pointer':next(x['source_pointer']for x in released if x['pair']==[100,0]),'case_refs':['DAN-029','ANALOG-AUDIO-029-01']}
  else:prov='fresh-selected'
  av.append({'host_index':i,'host_value':v,'vector_sha256':key})
  if key in byhash:assert prov=='baseline';continue
  ws=[{**w,'token':str(v)+'.0','little_endian_hex':bits(v),'reconstructed_binary64_le':struct.pack('<d',v).hex()}if w['index']==i else w for w in words]
  z={'vector_sha256':key,'changed_host_index':None if prov=='baseline'else i,'changed_host_value':None if prov=='baseline'else v,'parameter_bits_le':wb,'parameter_binary64_le':[w['reconstructed_binary64_le']for w in ws],'events':events,'packed16_events_le':[struct.pack('<qBBBB4x',*e,0).hex()for e in events],'provenance':prov,'historical':None if ref is None else{**ref,'new_pid':None,'new_receipt':None},'measurement_only_auxiliary':i==99 and v==0,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None};vectors.append(z);byhash[key]=z
  if prov=='fresh-selected':
   id=f'i{i:03}-v{v:02}';script=H/'scripts'/(id+'.script');text='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}'for w in ws]+hist[2:])+'\n';script.write_text(text);plans.append({'id':id,'host_index':i,'host_value':v,'vector_sha256':key,'script':str(script),'direct_exports':293,'CalcA':87,'output_bytes':352800,'measurement_only_auxiliary':z['measurement_only_auxiliary']})
assert len(vectors)==254 and len(av)==338 and len(plans)==208
save('inputs.json',{'schema':'whole-Analog-P1-all-native-kind3-domains-v1','counts':{'alias_points':338,'unique_vectors':254,'inherited_unique_vectors':46,'fresh_children':208,'direct_exports':60944,'CalcA':18096,'stereo_bytes':73382400},'words':words,'fixture':old['fixture'],'domains':domains,'aliases':av,'vectors':vectors,'plans':plans})
save('approved-prior-summary.json',{'prerequisite_Transpose_approved_review':rp,'approved_summary':summary,'R3_review':pin(r3review),'R3_mode_input_projection':modeprojection,'DAN029':'Releasedinputmetadata only; no newPID/receipt/metrics. No historicalraw/code/resultreplay.'})
methods=[]
for p in sorted((OLD/'protocol').iterdir()):shutil.copyfile(p,H/'protocol'/p.name);methods.append(pin(p))
owner=ROOT/'wiki/specs/device-analog.md';save('authority-pins.json',{'Transpose_approval':rp,'Transpose_final_manifest':pin(OLD/'manifest.json'),'static_map':pin(sp),'baseline_input':pin(OLD/'inputs.json'),'R3_owner_aliases':pin(ap),'R3_review':pin(r3review),'old_script_manifest':pin(om),'release_input_manifest':pin(cp),'canonical_owner_asof':pin(owner),'canonical_revision_asof':int(next(l for l in owner.read_text().splitlines()if l.startswith('revision:')).split(':')[1])if any(l.startswith('revision:')for l in owner.read_text().splitlines())else'Exactfilepin controls; revisionlabel not parsed','unchanged_method_copies':methods,'new_original_source_acquisition':False})
ctx=json.loads((OLD/'context.json').read_text());ctx['stop_policy']='Once208sequential/firstfaultstop/retainpartial/no retry/resume/extension; queuedchildcalls can execute before outer detects. No provider/model/FP/seed change.';ctx['scope']='208missing whole203word one-native-kind3-index vectors. All338aliases retained; index99=0measurement-only.';save('context.json',ctx)
print(json.dumps({'status':'MATERIALIZED-ONCE-PREREQUISITE-SEALED','scripts':208,'aliases':338,'unique':254,'original_calls':0,'runtime_reads':0,'prerequisite_review':rp}))
