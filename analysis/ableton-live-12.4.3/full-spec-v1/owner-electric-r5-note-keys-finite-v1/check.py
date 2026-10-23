#!/usr/bin/env python3
"""Owner-only staged data, approved summary and explicit old owner/release metadata. No actual/raw access."""
import argparse,copy,hashlib,json,pathlib,re,struct
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[3]
ALLOWED={ROOT/n for n in ['wiki/specs/device-electric.md','analysis/ableton-live-12.4.3/full-spec-v1/reviews/electric-note-keys-v1-review.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r3-finite-v1/cases.json','analysis/ableton-live-12.4.3/full-spec-v1/owner-electric-r4-transpose-finite-v1/cases25.json','handoff/device-electric-v2/manifest.json']}
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

def item(point,key,caseid):
 fresh=key!=60;native={'original_output':point['audio'],'observed_output_summary':point['native_output_summary']} if fresh else {'approved_inherited_reference':point['inherited_approved_summary'],'no_new_measurement':True}
 return {'note_key':key,'case_id':caseid,'existing_case_refs':[] if fresh else ['DEL-CS-001','P1','ELECTRIC-AUDIO-004','ETI-12'],'stored_aliases':[] if fresh else [11.99999,12],'kind':'finite-native-observation' if fresh else 'inherited-reference-only','requirements':['REQ-DEVICE-ELECTRIC-004'],'context_requirement':'REQ-DEVICE-ELECTRIC-006 unchanged; no new pitch formula or f0 validation','approved_review_pointer':f'#/approved_summary/approved_points/{key}','approved_point':point,'native_expected':native,'fresh_waveform_prior':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None,'limits':'Only exact33wordP1/44100Hz/warm11264/render44100/512/zeroinputflag0/stopped0-0-120/on11264v100/off33314v0 bothmatchingkeys. No general range/onset/pitch/public/ARM/calibration/portable criterion.'}
def mapping(catalog,joins,review):
 s=review['approved_summary'];need(catalog['shared_input']==s['shared_input'],'sharedinput');need([x['note_key'] for x in s['approved_points']]==list(range(128)),'approveddomain');need(len(catalog['catalog'])==len(joins['joins'])==128,'wholecatalog')
 need(catalog['logical_points']==128 and catalog['fresh_cases']==127 and catalog['inherited_ref_count']==1,'counts')
 ordinal=0
 for key,p in enumerate(s['approved_points']):
  fresh=key!=60;caseid=f'DEL-CS-{31+ordinal:03}' if fresh else None
  if fresh:ordinal+=1
  expected=item(p,key,caseid);need(catalog['catalog'][key]==expected,'case '+str(key));need(joins['joins'][key]=={'note_key':key,'case_id':caseid,'existing_case_refs':expected['existing_case_refs'],'approved_review_pointer':expected['approved_review_pointer'],'fresh_observation':fresh,'owner_original_calls':0},'join '+str(key))
  for e,frame,status,vel in zip(p['events'],[11264,33314],[144,128],[100,0]):need(e==[frame,status,key,vel],'eventbytes')
  need(p['packed16_events_le']==[struct.pack('<qBBBB4x',*e,0).hex() for e in p['events']],'packed words')
  need(p['fresh_waveform_prior'] is None and p['portable_expected'] is None and p['portable_comparator'] is None and p['grade'] is None,'originalNULLs')
 need(ordinal==127,'127new')

def old_r4(data,b):
 xs=data['catalog'];need(len(xs)==b['object_count']==25 and {str(i):sha(enc(x)) for i,x in enumerate(xs)}==b['object_digests'],'old25objects');need([x['case_id'] for x in xs if x['case_id'] is not None]==b['case_IDs'],'old22IDs')
def wording(delta):
 s='\n'.join(x['new'] for x in delta['replacements']);required=['do not newly\nvalidate the broader note-range','REQ-006 remains pitch context','**numerically zero**','not a new positive-zero','without actual/source/raw or\nnumeric re-review','154 common whole-batch-before','not independent\nper-child-before','Rate returned the opaque integer 1','Portable expected\noutputs, comparators and candidate grades remain NULL','No new release, candidate result, site or whole-product closure','ADR 0003']
 need(all(t in s for t in required),'bounded wording')

def negatives(catalog,joins,review,before,after,baseline,r4,delta):
 out=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,struct.error):out.append(name)
  else:raise AssertionError('negativeaccepted '+name)
 def mutate(name,fn):
  x,y=copy.deepcopy(catalog),copy.deepcopy(joins);fn(x,y);reject(name,lambda:mapping(x,y,review))
 mutate('omit key127',lambda x,y:x['catalog'].pop())
 mutate('duplicate key',lambda x,y:x['catalog'].__setitem__(2,copy.deepcopy(x['catalog'][1])))
 mutate('wrong first ID',lambda x,y:x['catalog'][0].update(case_id='DEL-CS-030'))
 mutate('inherited60 new ID',lambda x,y:x['catalog'][60].update(case_id='DEL-CS-091'))
 mutate('lost aliases',lambda x,y:x['catalog'][60].update(stored_aliases=[12]))
 mutate('fabricated fresh60 PID',lambda x,y:x['catalog'][60]['approved_point'].update(fresh_pid=1))
 mutate('wrong output hash',lambda x,y:x['catalog'][0]['native_expected']['original_output'].update(sha256='0'*64))
 mutate('wrong native summary',lambda x,y:x['catalog'][0]['native_expected']['observed_output_summary'].update(warmup_numeric_zero=False))
 mutate('positivezero extrapolation',lambda x,y:x['catalog'][0]['native_expected']['observed_output_summary'].update(warmup_positivezero=True))
 mutate('off key mismatch',lambda x,y:x['catalog'][0]['approved_point']['events'][1].__setitem__(2,1))
 mutate('wrong packed event',lambda x,y:x['catalog'][0]['approved_point']['packed16_events_le'].__setitem__(0,'00'*16))
 mutate('changed fixed word',lambda x,y:x['shared_input']['parameters'][0].update(token='29'))
 mutate('portable expected',lambda x,y:x['catalog'][0].update(portable_expected='audio'))
 mutate('portable comparator',lambda x,y:x['catalog'][0].update(portable_comparator='exact'))
 mutate('candidate grade',lambda x,y:x['catalog'][0].update(candidate_grade='PASS'))
 mutate('rewrite NULL prior',lambda x,y:x['catalog'][0].update(fresh_waveform_prior='fit'))
 mutate('wrong review join',lambda x,y:y['joins'][0].update(approved_review_pointer='#/unapproved'))
 mutate('owner original call',lambda x,y:y['joins'][0].update(owner_original_calls=1))
 reject('old body changed',lambda:preserve(before,after.replace('all 33 host values of REQ-002','all 32 host values of REQ-002',1),baseline))
 reject('old004 changed',lambda:preserve(before,after.replace('All 128 keys sound.','Only 127 keys sound.',1),baseline))
 reject('old row changed',lambda:preserve(before,after.replace('| DEL-001 |','| DEL-999 |',1),baseline))
 reject('old R4 annex changed',lambda:preserve(before,after.replace('The 22 fresh output hashes are distinct.','The 21 fresh output hashes are distinct.',1),baseline))
 reject('old pitch changed',lambda:preserve(before,after.replace('440.329 Hz','440.0 Hz',1),baseline))
 bad=copy.deepcopy(r4);bad['catalog'].pop();reject('old R4 object omitted',lambda:old_r4(bad,baseline['R4_catalog']))
 for token in ['**numerically zero**','154 common whole-batch-before','Rate returned the opaque integer 1','REQ-006 remains pitch context']:
  bad=copy.deepcopy(delta)
  for x in bad['replacements']:x['new']=x['new'].replace(token,'')
  reject('remove wording '+token,lambda bad=bad:wording(bad))
 reject('actual payload access',lambda:read(P.parent/'batch-electric-note-keys-v1/manifest.json'))
 return out

def check():
 b,d,c,j=[load(n) for n in ['baseline.json','owner-delta.json','cases128.json','joins128.json']];before=verify(b['owner_before']).decode();need(b['approved_review']==c['approved_review']==j['approved_review'],'reviewpins');r=json.loads(verify(b['approved_review']));need(r['blocking_findings']==[] and r['disposition'].startswith('APPROVED'),'actualauthority')
 after=compose(before,d);need(sig(after)=={k:d['owner_after'][k] for k in ['bytes','sha256']},'target');need(compose(after,d,reverse=True)==before,'reverse');preserve(before,after,b);mapping(c,j,r);wording(d)
 r3=json.loads(verify(b['R3_cases_pin']));need(len(r3['cases'])==8 and {x['id']:sha(enc(x)) for x in r3['cases']}==b['R3_objects'],'R3objects');need(len(r3['pair_relations'])==2 and {x['id']:sha(enc(x)) for x in r3['pair_relations']}==b['R3_pair_relations'],'R3pairs')
 r4=json.loads(verify(b['R4_catalog']['pin']));old_r4(r4,b['R4_catalog']);oldids=[f'DEL-{i:03}' for i in range(1,33)]+[x['id'] for x in r3['cases']]+b['R4_catalog']['case_IDs'];need(oldids==b['old_IDs'] and len(set(oldids))==62,'62oldIDs')
 release=json.loads(verify(b['release_manifest']));need(release['files']==b['release_inventory'] and len(release['files'])==129 and release['evaluation_count']==release['case_count']==117,'release metadata')
 neg=negatives(c,j,r,before,after,b,r4,d)
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir() if x.is_file()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'sealed tree')
  for x in m['payloads']:raw=read(P/x['path']);need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'sealedpayload')
 return {'status':'PASS','scope':'Only newowner wording/mapping/IDs/preservation, approvedactualsummary inherited','target':d['owner_after'],'reverse_to_R4_exact':True,'other_whole_bodies_exact':15,'old004prefix_exact':True,'REQ006_exact':True,'old_rows_exact':40,'old_IDs_exact':62,'new_IDs':127,'total_navigation_IDs':189,'R3_objects':8,'R3_pairs':2,'R4_catalog_exact':25,'release_evaluations':117,'release_manifest_inventory':129,'logical_catalog':128,'inherited_ref_only':1,'negative_controls':neg,'actual_packet_reads':0,'numeric_recomputations':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);p.parse_args();print(json.dumps(check(),indent=2))
