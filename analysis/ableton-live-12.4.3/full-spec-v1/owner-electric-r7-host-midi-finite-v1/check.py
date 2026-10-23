#!/usr/bin/env python3
"""Owner-only staged data, approved summary and explicit old owner/release metadata. No actual/raw access."""
import argparse,copy,hashlib,json,pathlib,re,struct
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[3]
ALLOWED={ROOT/n for n in ['wiki/specs/device-electric.md','analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-finite-host-domains-v1-review.json','analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-midi-axes-v1-review.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/cases.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r4-transpose-finite-v1/cases25.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r5-note-keys-finite-v1/cases128.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r6-velocity-finite-v1/cases128.json','handoff/device-electric-v2/manifest.json']}
def need(v,m):
 if not v:raise ValueError(m)
def read(p):
 p=pathlib.Path(p).resolve();need(p.parent==P or p in ALLOWED,'outside staged/approvedmetadata');return p.read_bytes()
def load(n):return json.loads(read(P/n))
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode()
def sig(s):return {'bytes':len(s.encode()),'sha256':sha(s.encode())}
def verify(pin):
 raw=read(ROOT/pin['path']);need(len(raw)==pin['bytes'] and sha(raw)==pin['sha256'],'identity '+pin['path']);return raw

def bodies(s):return {m[1]:m[0] for m in re.finditer(r'^### (REQ-DEVICE-ELECTRIC-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',s,re.M|re.S)}
def sections(s):return {m[1]:m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',s,re.M|re.S)}
def compose(text,delta,reverse=False):
 for item in (delta['replacements'][::-1] if reverse else delta['replacements']):
  old,new=(item['new'],item['old']) if reverse else (item['old'],item['new']);need(text.count(old)==1,'unique '+item['label']);text=text.replace(old,new,1)
 return text

def preserve(before,after,b):
 old,new=bodies(before),bodies(after);need(len(old)==len(new)==16 and old.keys()==new.keys(),'REQset');need({k:sig(v) for k,v in old.items()}==b['requirement_bodies'],'baselinebodies')
 for k in old:
  need(new[k].startswith(old[k]) if k in b['append_only_requirements'] else new[k]==old[k],'oldbody '+k)
 rows=lambda s:[x for x in s.splitlines() if x.startswith('| DEL-')];need(rows(before)==rows(after)==b['old_rows'] and len(rows(after))==40,'oldrows')
 oldsec,newsec=sections(before),sections(after)
 for k,v in b['protected_sections'].items():need(sig(oldsec[k])==sig(newsec[k])==v,'protected '+k)
 need(sig(oldsec['Acceptance cases'])==b['old_acceptance_prefix'] and newsec['Acceptance cases'].startswith(oldsec['Acceptance cases']),'oldAcceptanceprefix')
 need(new['REQ-DEVICE-ELECTRIC-006']==old['REQ-DEVICE-ELECTRIC-006'],'pitchcontextonly')


 need(sig(before[before.index('The [finite handoff plan]'):before.index('## Internal helper qualification')])==sig(after[after.index('The [finite handoff plan]'):after.index('## Internal helper qualification')])==b['release_prose'],'release prose exact')

def whole_history(bits, doubles, ev):
 return {'parameter_f32_bits_le':bits,'parameter_reconstructed_binary64_le':doubles,'events':ev,'sample_rate':44100,'process_frames':[11264,44100],'block':512,'input':'zero','inflag':0,'transport':[0,0,120],'XDEV_TIME':'0 existing treatment','MXCSR':'0x1f80','LIBM_ULP':'absent/unperturbed'}
def history_key(h):return sha(json.dumps(h,sort_keys=True,separators=(',',':')).encode())
def make_catalogs(host_review,midi_review,r4):
 hs,ms=host_review['approved_summary'],midi_review['approved_summary'];cases=[];hv=[];ha=[];mh=[];ma=[];joins=[];refs={};history_refs={};fresh_h=0;fresh_m=0
 trefs={x['transpose_integer']:x['case_id']or x['existing_case_refs'][0]for x in r4['catalog']}
 def case(cid,cl,req,z,pointer,key,actual):
  c={'case_id':cid,'kind':'finite-native-observation','source_class':cl,'requirements':[req],'approved_review':cl,'approved_review_pointer':pointer,'complete_history_sha256':key,'approved_point':z,'native_expected':{'original_output':actual['audio'],'observed_output_summary':actual['native_output_summary']},'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None,'owner_original_calls':0};cases.append(c)
  joins.append({'case_id':cid,'approved_review':cl,'approved_review_pointer':pointer,'complete_history_sha256':key,'owner_original_calls':0})
 for i,z in enumerate(hs['approved_vectors']):
  wh=whole_history(z['parameter_bits_le'],z['parameter_binary64_le'],z['events']);key=history_key(wh);new=None
  if z['historical']is None:
   new=f'DEL-CS-{285+fresh_h:03}';fresh_h+=1;ref=new;case(new,'host31','REQ-DEVICE-ELECTRIC-002',z,f'#/approved_summary/approved_vectors/{i}',key,z['actual'])
  else:ref=trefs[z['historical']['transpose_integer']]
  x={'parameter_vector_sha256':z['vector_sha256'],'complete_history_sha256':key,'host_index':z['changed_host_index'],'host_value':z['changed_host_value'],'case_ref':ref,'new_case_id':new,'approved_review_pointer':f'#/approved_summary/approved_vectors/{i}','provenance':z['provenance'],'inherited_reference_metadata':z['historical'],'whole_history':wh,'owner_original_calls':0,'new_inherited_receipt':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None};hv.append(x);refs[z['vector_sha256']]=x;history_refs[key]=ref
 for a in hs['approved_aliases']:
  x=refs[a['vector_sha256']];ha.append({**a,'case_ref':x['case_ref'],'new_case_id':x['new_case_id'],'complete_history_sha256':x['complete_history_sha256'],'owner_original_calls':0})
 for i,z in enumerate(ms['approved_histories']):
  key=z['history_sha256'];new=None
  if z['historical']is None:
   new=f'DEL-CS-{316+fresh_m:03}';fresh_m+=1;ref=new;case(new,'midi142','REQ-DEVICE-ELECTRIC-004',z,f'#/approved_summary/approved_histories/{i}',key,z['actual'])
  else:ref='DEL-CS-001';need(z['axis']=='baseline','only baseline inherited')
  if key in history_refs:need(history_refs[key]==ref=='DEL-CS-001','shared baseline only')
  history_refs[key]=ref
  mh.append({'axis':z['axis'],'value':z['value'],'complete_history_sha256':key,'parameter_vector_sha256':ms['shared_input']['parameter_vector_sha256'],'case_ref':ref,'new_case_id':new,'whole_history':z['whole_history'],'events':z['events'],'packed16_events_le':z['packed16_events_le'],'approved_review_pointer':f'#/approved_summary/approved_histories/{i}','provenance':z['provenance'],'inherited_reference_metadata':z['historical'],'owner_original_calls':0,'new_inherited_receipt':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
 mby={x['complete_history_sha256']:x for x in mh}
 for a in ms['approved_aliases']:
  x=mby[a['history_sha256']];ma.append({**a,'case_ref':x['case_ref'],'new_case_id':x['new_case_id'],'owner_original_calls':0})
 need(fresh_h==31 and fresh_m==142 and len(hv)==56 and len(ha)==58 and len(mh)==143 and len(ma)==144,'whole classes')
 need([x['case_id']for x in cases]==[f'DEL-CS-{i:03}'for i in range(285,458)],'173IDs')
 need(len(history_refs)==198 and len(set(x['parameter_vector_sha256']for x in mh))==1,'complete history distinct from parameter vector')
 return [{'schema':'electric-r7-combined173-native-finite-cases-v1','new_case_count':173,'shared_inputs':{'host31':hs['shared_input'],'midi142':ms['shared_input']},'cases':cases},
 {'schema':'electric-r7-whole58alias56vector-host-catalog-v1','logical_aliases':58,'unique_vectors':56,'fresh_cases':31,'inherited_vectors':25,'aliases':ha,'vectors':hv},
 {'schema':'electric-r7-whole144alias143history-midi-catalog-v1','logical_aliases':144,'unique_histories':143,'fresh_cases':142,'inherited_histories':1,'parameter_vectors':1,'aliases':ma,'histories':mh},
 {'schema':'electric-r7-complete173-review-joins-v1','new_cases':joins,'complete_history_references':[{'complete_history_sha256':k,'case_ref':v}for k,v in history_refs.items()],'unique_complete_histories':198,'owner_original_calls':0}]
def mapping(actual,expected):need(actual==expected,'all173cases/fullcatalogs/historydedup/joins/nativeNULLs')
def old_catalog(data,b):
 xs=data['catalog'];need(len(xs)==b['object_count']and {str(i):sha(enc(x))for i,x in enumerate(xs)}==b['object_digests'],'old full catalog objects');need([x['case_id']for x in xs if x['case_id']is not None]==b['case_IDs'],'old catalog IDs')
def wording(delta):
 s='\n'.join(x['new']for x in delta['replacements'])
 required=['not newly validate stored/UI conversion','not a new test of','complete event/process/FP-context history','All 143 MIDI histories share one','not a general channel or release-velocity invariance','**numerically zero**','comparators and candidate grades remain NULL','without actual/source/raw or numeric re-review','not\nindependent per-child-before','no success/sample-clock meaning','Author bookkeeping','coverage remains OPEN']
 # Capitalization is normalized only for these literal safety qualifications.
 need(all(x.lower()in s.lower()for x in required),'bounded new wording')
def controls(data,expected,before,after,b,old,delta):
 out=[]
 def reject(name,fn):
  try:fn()
  except(ValueError,KeyError,IndexError):out.append(name)
  else:raise AssertionError('negative accepted '+name)
 changes=[('omit native observation',lambda d:d[0]['cases'].pop()),('duplicate ID',lambda d:d[0]['cases'][1].update(case_id='DEL-CS-285')),('wrong MIDI startID',lambda d:d[0]['cases'][31].update(case_id='DEL-CS-315')),('native output hash',lambda d:d[0]['cases'][0]['native_expected']['original_output'].update(sha256='0'*64)),('native observed summary',lambda d:d[0]['cases'][0]['native_expected']['observed_output_summary'].update(all_finite=False)),('portable expected',lambda d:d[0]['cases'][0].update(portable_expected=0)),('portable comparator',lambda d:d[0]['cases'][0].update(portable_comparator='exact')),('candidate grade',lambda d:d[0]['cases'][0].update(candidate_grade='PASS')),('rewrite NULLprior',lambda d:d[0]['cases'][0].update(fresh_waveform_prior='fit')),('owner original call',lambda d:d[0]['cases'][0].update(owner_original_calls=1)),('wrong source review pointer',lambda d:d[0]['cases'][31].update(approved_review_pointer='#/unreviewed')),('wrong history identity',lambda d:d[0]['cases'][31].update(complete_history_sha256='0'*64)),('omit host alias',lambda d:d[1]['aliases'].pop()),('duplicate host vector',lambda d:d[1]['vectors'].__setitem__(1,copy.deepcopy(d[1]['vectors'][0]))),('reassign inherited transpose',lambda d:next(x for x in d[1]['vectors']if x['inherited_reference_metadata']).update(case_ref='DEL-CS-285')),('invent inherited hostreceipt',lambda d:next(x for x in d[1]['vectors']if x['inherited_reference_metadata']).update(new_inherited_receipt={'pid':1})),('omit channel15',lambda d:d[2]['aliases'].pop(15)),('omit off127',lambda d:d[2]['aliases'].pop()),('collapse sameparameter histories',lambda d:d[2].update(histories=d[2]['histories'][:1])),('matching channel pair mismatch',lambda d:d[2]['histories'][1]['events'][1].__setitem__(1,128)),('offvelocity crossproduct',lambda d:d[2]['histories'][1]['events'][1].__setitem__(3,127)),('invent baseline newID',lambda d:d[2]['histories'][0].update(new_case_id='DEL-CS-458')),('invent baseline receipt',lambda d:d[2]['histories'][0].update(new_inherited_receipt={'pid':1})),('wrong MIDI wholehistory',lambda d:d[2]['histories'][1]['whole_history'].update(process_frames=[44100])),('wrong reused baseline alias',lambda d:d[2]['aliases'][16].update(case_ref='DEL-CS-316')),('wrong shared history dedup',lambda d:d[3].update(unique_complete_histories=56)),('wrong join',lambda d:d[3]['new_cases'][0].update(case_id='DEL-CS-999'))]
 for name,change in changes:
  bad=copy.deepcopy(data);change(bad);need(bad!=data,'meaningful '+name);reject(name,lambda:mapping(bad,expected))
 for name,oldtext,newtext in [('other wholeREQ','all 33 host values of REQ-002','all 32 host values of REQ-002'),('old002 prefix','Live sends 33 host values.','Live sends 32 host values.'),('old004 prefix','All 128 keys sound.','Only 127 keys sound.'),('old row','| DEL-001 |','| DEL-999 |'),('old metric','0.05 dB (envelope)','0.5 dB (envelope)'),('oldR6annex','Fresh byte 0 has zero render samples;','Fresh byte 0 has one render sample;')]:
  need(oldtext in after,'control anchor '+name);reject(name,lambda oldtext=oldtext,newtext=newtext:preserve(before,after.replace(oldtext,newtext,1),b))
 for name,obj in old.items():
  bad=copy.deepcopy(obj);bad['catalog'].pop();reject('old '+name+' omitted',lambda:old_catalog(bad,b['old_catalogs'][name]))
 for token in ['complete event/process/FP-context history','**numerically zero**','comparators and candidate grades remain NULL','coverage remains OPEN']:
  bad=copy.deepcopy(delta)
  for x in bad['replacements']:x['new']=x['new'].replace(token,'')
  reject('remove '+token,lambda bad=bad:wording(bad))
 for folder in ['batch-electric-finite-host-domains-v1','batch-electric-midi-axes-v1']:
  reject('refuse actual '+folder,lambda folder=folder:read(P.parent/folder/'manifest.json'))
 return out

def check():
 b,delta=load('baseline.json'),load('owner-delta.json');before=verify(b['owner_before']).decode();reviews={k:json.loads(verify(v))for k,v in b['approved_reviews'].items()}
 need(all(r['blocking_findings']==[]and r['disposition']=='APPROVED_BOUNDED_ACTUAL_SOURCE'for r in reviews.values()),'approved summaries')
 r3=json.loads(verify(b['R3_cases_pin']));need(len(r3['cases'])==8 and {x['id']:sha(enc(x))for x in r3['cases']}==b['R3_objects'],'R3objects');need(len(r3['pair_relations'])==2 and {x['id']:sha(enc(x))for x in r3['pair_relations']}==b['R3_pair_relations'],'R3pairs')
 old={}
 for key,x in b['old_catalogs'].items():old[key]=json.loads(verify(x['pin']));old_catalog(old[key],x)
 oldids=[f'DEL-{i:03}'for i in range(1,33)]+[x['id']for x in r3['cases']]+sum((b['old_catalogs'][key]['case_IDs']for key in ['R4','R5','R6']),[])
 need(oldids==b['old_IDs']and len(set(oldids))==316,'316prior navigationIDs')
 release=json.loads(verify(b['release_manifest']));need(release['files']==b['release_inventory']and len(release['files'])==129 and release['case_count']==release['evaluation_count']==117,'release inventory')
 data=[load(n)for n in ['cases173.json','host-catalog58.json','midi-catalog144.json','joins173.json']];expected=make_catalogs(reviews['host31'],reviews['midi142'],old['R4']);mapping(data,expected)
 after=compose(before,delta);need(sig(after)=={k:delta['owner_after'][k]for k in ['bytes','sha256']},'composed target');need(compose(after,delta,True)==before,'full reverse toR6');preserve(before,after,b);wording(delta)
 negatives=controls(data,expected,before,after,b,old,delta)
 if (P/'manifest.json').exists():
  manifest=load('manifest.json');need({x.name for x in P.iterdir()if x.is_file()}=={'manifest.json'}|{x['path']for x in manifest['payloads']},'sealed tree')
  for x in manifest['payloads']:
   raw=read(P/x['path']);need(len(raw)==x['bytes']and sha(raw)==x['sha256'],'sealed payload')
 return {'status':'PASS','scope':'Only new wording/IDs/mapping/preservation; actual proof inherited from two approved summaries','target':delta['owner_after'],'reverse_to_R6_exact':True,'other_whole_bodies_exact':14,'old002004prefixes_exact':True,'oldREQ003and006_exact':True,'old_rows_exact':40,'old_IDs_exact':316,'new_IDs':173,'total_navigation_IDs':489,'R3objects_pairs':[8,2],'old_catalogs_exact':{'R4':25,'R5':128,'R6':128},'old_acceptance_prefix_exact':True,'release_evaluations_inventory':[117,129],'host_aliases_vectors':[58,56],'MIDI_aliases_histories':[144,143],'new_host_MIDI':[31,142],'shared_complete_history_references':198,'negative_controls':negatives,'actual_packet_reads':0,'numeric_recomputations':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args();print(json.dumps(check(),indent=2))
