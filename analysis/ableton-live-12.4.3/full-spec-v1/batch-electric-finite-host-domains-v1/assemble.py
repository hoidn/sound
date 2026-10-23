#!/usr/bin/env python3
"""One fixed58alias/56vector selected input assembly, no original/oldmodule/provider/model execution."""
import hashlib,json,pathlib,struct,shutil,os
H=pathlib.Path(__file__).resolve().parent;F=H.parent;ROOT=H.parents[3];OLD=F/'batch-electric-note-keys-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):p=pathlib.Path(p).resolve();b=p.read_bytes();return{'path':str(p),'bytes':len(b),'sha256':sha(b)}
def save(n,d):
 with(H/n).open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def bits(v):return struct.pack('<f',float(v)).hex()
assert not(H/'inputs.json').exists();ep=F/'reviews/electric-fixed-p1-finite-host-domain-eligibility.json';assert pin(ep)['bytes']==30157 and pin(ep)['sha256']=='f7fb4a47d8728f5d24249973545c8e7a8ea514f933ab4620d281e711cb2e8d78';elig=json.loads(ep.read_text())
rp=F/'reviews/electric-transpose-integers-v1-review.json';assert pin(rp)['bytes']==365481 and pin(rp)['sha256']=='16783862180b314900c96762538313167874751f2fa68c5a867fdcbbf60a8e56';r=json.loads(rp.read_text());assert'APPROVED'in r['disposition']and not r['blocking_findings'];summary=r['approved_summary'];points=summary['approved_points'];assert[p['transpose_integer']for p in points]==list(range(25));shared=summary['shared_input'];words=[{'index':i,'token':tok,'little_endian_hex':shared['baseline_parameter_f32_bits_le'][i],'reconstructed_binary64_le':struct.pack('<d',float(tok)).hex()}for i,tok in enumerate(shared['history']['baseline_parameter_tokens'])];base=[w['little_endian_hex']for w in words];assert len(base)==33 and sha(bytes.fromhex(''.join(base)))=='9ef2b39d47ca833730a9bbfd9d26e3bdc08a847df0ead035bd14d948bc35a43a'
dom=[{'host_index':x['index'],'name':x['name'],'minimum':min(x['values']),'maximum':max(x['values']),'baseline':x['baseline']}for x in elig['domains']];assert[(d['host_index'],d['minimum'],d['maximum'],d['baseline'])for d in dom]==[(0,0,30,30),(23,0,1,0),(30,0,24,12)]
save('historical-input-joins.json',{'eligibility_pin':pin(ep),'complete_retained_metadata_assessment':elig,'scope':'All120selectedoldinputdeclarations onlydefaultP1match; old31voiceinputchangesindex28/multinotehistory. No globalabsence/originalexecutedversionproof/newvoicecount/stealing/labelproof.'});save('approved-prior-summary.json',{'review_pin':pin(rp),'approved_summary':summary,'scope':'All25Transposevectors inherited metadata only; no oldactual/code/raw/audio/metrics/control replay or newPID/receipt invented.'})
(H/'scripts').mkdir();(H/'protocol').mkdir();av=[];vectors=[];plans=[];seen={};events=[[11264,144,60,100],[33314,128,60,0]]
for row in dom:
 i=row['host_index']
 for v in range(row['minimum'],row['maximum']+1):
  ws=[{**w,'token':str(v)+'.0','little_endian_hex':bits(v),'reconstructed_binary64_le':struct.pack('<d',v).hex()}if w['index']==i else w for w in words];wb=[w['little_endian_hex']for w in ws];key=sha(bytes.fromhex(''.join(wb)));baseline=v==row['baseline'];inherited=baseline or i==30;av.append({'host_index':i,'host_value':v,'vector_sha256':key})
  if key in seen:assert baseline;continue
  tv=12 if baseline else v;reference=None
  if inherited:
   q=points[tv];assert q['parameter_f32_bits_le']==wb;reference={'approved_review':pin(rp),'approved_point_pointer':f'/approved_summary/approved_points/{tv}','transpose_integer':tv,'approved_point_id':q['id'],'case_refs':q.get('existing_owner_case_refs',[]),'new_pid':None,'new_receipt':None}
  z={'vector_sha256':key,'changed_host_index':None if baseline else i,'changed_host_value':None if baseline else v,'parameter_bits_le':wb,'parameter_binary64_le':[w['reconstructed_binary64_le']for w in ws],'events':events,'packed16_events_le':[struct.pack('<qBBBB4x',*e,0).hex()for e in events],'provenance':'approved-transpose'if inherited else'fresh-selected','historical':reference,'expected_waveform':None,'portable_expected':None,'portable_comparator':None,'grade':None};vectors.append(z);seen[key]=z
  if not inherited:
   id=f'i{i:02}-v{v:02}';p=H/'scripts'/(id+'.script');text='\n'.join(['create','rate 44100']+[f'param {w["index"]} {w["token"]}'for w in ws]+['event 11264 0x90 60 100','event 33314 0x80 60 0','inflag 0','input zero','process 11264 512','process 44100 512','destroy'])+'\n';p.write_text(text);plans.append({'id':id,'host_index':i,'host_value':v,'vector_sha256':key,'script':str(p),'direct_exports':145,'CalcA':109,'output_bytes':442912})
assert len(av)==58 and len(vectors)==56 and len(plans)==31
save('inputs.json',{'schema':'whole-Electric-P1-three-finite-host-domains-v1','counts':{'alias_points':58,'unique_vectors':56,'inherited_unique_vectors':25,'fresh_children':31,'direct_exports':4495,'CalcA':3379,'stereo_bytes':13730272},'words':words,'fixture':{'sample_rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':11264,'key':60,'on_velocity':100,'off_velocity':0,'input':'zero','inflag':0,'transport':[0,0,120],'MXCSR':'0x1f80','XDEV_TIME':'0 existing treatment','LIBM_ULP':'absent/unperturbed'},'domains':dom,'aliases':av,'vectors':vectors,'plans':plans})
methods=[]
for p in sorted((OLD/'protocol').iterdir()):shutil.copyfile(p,H/'protocol'/p.name);methods.append(pin(p))
owner=ROOT/'wiki/specs/device-electric.md';save('authority-pins.json',{'eligibility_metadata':pin(ep),'Transpose_approved_review':pin(rp),'family_manifest':pin(F/'family-electric-routes-v1/manifest.json'),'current_owner_asof':pin(owner),'asof_revision_label':6,'asof_scope':'Exactfilepin controls; laterdocumentation changes nongating/inputmodelunchanged','unchanged_inert_method_copies':methods,'prior_actual_packets_reopened':False,'new_original_source_acquisition':False})
ctx=json.loads((OLD/'context.json').read_text());assert ctx['watched_roles'][0]['identity']['sha256']=='6eb5dd284452960f623e0bb6ed26b8743bdf789b8eac09a48b4a9291995ed8e1';ctx['stop_policy']='Once31sequential/firstfaultstop/retainpartials/no retry/resume/extension. Childqueuedcalls mayalreadyexecute before outerdetects; no newreceiver/provider/model/FP/seed.';ctx['scope']='58aliases/56uniquevectors/31fresh, single-note fixedP1 NOT voicecount/stealing/labelproof.';save('context.json',ctx)
print(json.dumps({'status':'MATERIALIZED-ONCE','aliases':58,'vectors':56,'fresh':31,'original_calls':0,'runtime_reads':0}))
