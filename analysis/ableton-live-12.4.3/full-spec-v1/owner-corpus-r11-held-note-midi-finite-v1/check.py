"""NEW owner wording/IDs/mapping/preservation only; no actual/source/raw/numeric rerun."""
from pathlib import Path
import argparse,copy,hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parents[3]
def need(v,s):
 if not v:raise AssertionError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def load(n):return json.loads((P/n).read_bytes())
def verify(x):
 p=(R/x['path']).resolve();s=str(p)
 need(p==R/'wiki/specs/device-corpus.md' or p==R/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/corpus-held-note-midi-axes-v1-review.json' or (('/full-spec-v1/owner-corpus-' in s or '/full-spec-v1/corpus-owner-' in s) and p.suffix=='.json') or p==R/'handoff/device-corpus-v5/manifest.json','owner/summary/manifest only')
 b=p.read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'pin');return b

def validate(c,n,j,s,quals):
 need(len(c['catalog'])==270 and len(n)==268 and len(c['aliases'])==272 and len(j['histories'])==270 and len(j['aliases'])==272,'whole units')
 need(c['shared_input']==s['shared_input'] and c['aliases']==s['aliases'] and c['review_qualifications']==quals,'shared exact authority/qualification')
 need(n==[x for x in c['catalog'] if x['case_id']] and [x['case_id'] for x in n]==[f'DCO-{i:03d}' for i in range(295,563)],'268new IDs')
 need(len({x['history_sha256'] for x in c['catalog']})==270 and {x['parameter_vector_sha256'] for x in c['catalog']}=={'613d0f49d678f947d847f2a4d56767881c63f370f07f2a8fdd2a172d4875b8a1'} and {x['parameter_token_binary64_sha256'] for x in c['catalog']}=={'1c0495901fdb45b2e3d8c47034fe9fa80fdabd375d2e945ec3a8e31d4fdf7863'},'wholehistory/originaltoken context')
 nid=295;refs=[]
 for i,(x,h,p) in enumerate(zip(c['catalog'],s['input_histories'],s['approved_points'])):
  need(x['id']==h['id'] and x['whole_history']==h['whole_history'] and x['history_sha256']==h['history_sha256'] and x['events']==h['events'] and x['packed16_event_le']==h['packed16_event_le'] and x['first_alias']==h['first_alias'],'complete history+event')
  need(x['parameter_tokens']==h['parameter_tokens'] and x['parameter_f32_bits_le']==h['parameter_f32_bits_le'] and x['parameter_f64_reconstructed_le']==h['parameter_f64_reconstructed_le'],'original38tokens/f32/f64')
  need(x['approved_point_pointer']==f'/approved_summary/approved_points/{i}' and x['input_history_pointer']==f'/approved_summary/input_histories/{i}' and x['approved_point_sha256']==obj(p) and x['input_history_sha256']==obj(h),'summary exactjoins')
  need(all(x[k] is None for k in ['waveform_prior','new_expected_waveform','portable_expected','portable_comparator','grade','new_metrics_for_inherited']) and x['new_application_predicate_proof'] is False and x['old_modal_budget_transferred'] is False and x['qualification_pointer']=='catalog270.json#/review_qualifications','NULLs/no modal or app promotion')
  need(x['provenance']==p['provenance'],'provenance')
  if p['provenance']=='fresh-once-only':
   need(x['case_id']==f'DCO-{nid:03d}' and x['existing_case_refs']==[] and x['historical'] is None and x['requirements']==['REQ-DEVICE-CORPUS-013'],'fresh ID/navigation');nid+=1
   need(x['native_observation']=={k:p[k] for k in ['script','pid','receipt_pointer','output','observed_unsigned_summary']} and x['new_pid']==p['pid'] and x['new_receipt']==p['receipt_pointer'],'copied facts')
  else:
   expected=h['historical']['existing_case_refs'];refs+=expected;need(x['case_id'] is None and x['existing_case_refs']==expected and x['native_observation'] is None and x['new_pid'] is x['new_receipt'] is None and x['historical']==p['historical'] and x['requirements']==[],'oldrefs no newfacts')
  need(j['histories'][i]=={'id':x['id'],'case_id':x['case_id'],'existing_case_refs':x['existing_case_refs'],'history_sha256':x['history_sha256'],'approved_point_pointer':x['approved_point_pointer'],'input_history_pointer':x['input_history_pointer']},'history joins')
 need(nid==563 and refs==['DCO-030','DCO-031'],'268new/two oldrefs')
 by={x['id']:x for x in c['catalog']}
 for a,z in zip(s['aliases'],j['aliases']):x=by[a['id']];need(z==dict(a,case_id=x['case_id'],existing_case_refs=x['existing_case_refs']),'272alias joins')
 need(len([x for x in j['aliases'] if x['existing_case_refs']==['DCO-030']])==3,'threebaselinealiases once')
 need('XDEV_LIBM_ULP' not in c['shared_input']['environment'],'LIBMUNSET')

def main():
 b=load('baseline.json');d=load('owner-delta.json');c=load('catalog270.json');n=load('new-cases268.json');j=load('joins272.json');r=json.loads(verify(b['approved_review']));s=r['approved_summary'];before=verify(b['owner_before']).decode();need(d['owner_before']==b['owner_before'],'base');after=before
 for x in d['replacements']:need(after.count(x['old'])==1,'uniqueold');after=after.replace(x['old'],x['new'])
 need(len(after.encode())==d['owner_after']['bytes'] and sha(after.encode())==d['owner_after']['sha256'],'target')
 rev=after
 for x in reversed(d['replacements']):need(rev.count(x['new'])==1,'uniquenew');rev=rev.replace(x['new'],x['old'])
 need(rev==before,'full reversal')
 bodies=lambda t:{m[1]:m[0] for m in re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n.*?(?=^### REQ-|^## |\Z)',t,re.M|re.S)}
 old=bodies(before);new=bodies(after);need(len(old)==len(new)==13,'13REQ')
 for k,v in old.items():need(sha(v.encode())==b['requirement_bodies'][k]['sha256'] and (new[k].startswith(v) if k.endswith('013') else new[k]==v),'12whole/013prefix')
 need(new['REQ-DEVICE-CORPUS-002']==old['REQ-DEVICE-CORPUS-002'],'entireR10REQ002 exact')
 need([x for x in after.splitlines() if re.match(r'^\| DCO-\d{3} \|',x)]==b['old_rows'] and len(b['old_rows'])==36 and b['old_IDs']==[f'DCO-{i:03d}' for i in range(1,295)],'294priorIDs36rows')
 secs=lambda t:{m[1]:m[0] for m in re.finditer(r'^## ([^\n]+)\n.*?(?=^## |\Z)',t,re.M|re.S)}
 for k,v in b['protected_sections'].items():need(sha(secs(after)[k].encode())==v,'protected '+k)
 for x in b['old_objects']:need(obj(json.loads(verify(x['pin'])))==x['json_object_sha256'],'R3–R10objects')
 rel=json.loads(verify(b['release_manifest']));need(obj(rel)==b['release_manifest_object_sha256'] and rel['case_count']==27 and rel['evaluation_count']==73,'release27g73e')
 validate(c,n,j,s,r['qualifications']);neg=[]
 for name,mut in [('omithistory',lambda a,z,m:a['catalog'].pop()),('omitalias',lambda a,z,m:a['aliases'].pop()),('duplicateID',lambda a,z,m:a['catalog'][1].update(case_id='DCO-295')),('inventoldID',lambda a,z,m:a['catalog'][60].update(case_id='DCO-563')),('inventoldPID',lambda a,z,m:a['catalog'][60].update(new_pid=1)),('parameteronlydedup',lambda a,z,m:a['catalog'][1].update(history_sha256=a['catalog'][0]['history_sha256'])),('wrongR10context',lambda a,z,m:a['catalog'][0].update(parameter_vector_sha256='9b98e8cab7aae28b01e18de3cd9570db62721f0ecdbf951bd5bd77d8b378e6e2')),('roundedtokens',lambda a,z,m:a['catalog'][0]['parameter_tokens'].__setitem__(15,'0.10000000149011612')),('binary64wrong',lambda a,z,m:a['catalog'][0]['parameter_f64_reconstructed_le'].__setitem__(15,'0'*16)),('addedOff',lambda a,z,m:a['catalog'][0]['events'].append([3073,128,0,64])),('matchingOffchannel',lambda a,z,m:a['catalog'][-1]['events'].append([3073,143,60,64])),('transfermodal',lambda a,z,m:a['catalog'][0].update(old_modal_budget_transferred=True)),('portableexpected',lambda a,z,m:a['catalog'][0].update(portable_expected=0)),('comparator',lambda a,z,m:a['catalog'][0].update(portable_comparator='modal')),('grade',lambda a,z,m:a['catalog'][0].update(grade='PASS')),('fitprior',lambda a,z,m:a['catalog'][0].update(waveform_prior='fit')),('newwaveformcriterion',lambda a,z,m:a['catalog'][0].update(new_expected_waveform='exact')),('newappproof',lambda a,z,m:a['catalog'][0].update(new_application_predicate_proof=True)),('wrongrawhash',lambda a,z,m:a['catalog'][0]['native_observation']['output'].update(sha256='0'*64)),('LIBM0notUNSET',lambda a,z,m:a['shared_input']['environment'].update(XDEV_LIBM_ULP='0')),('dropjoin',lambda a,z,m:m['histories'].pop())]:
  a,z,m=copy.deepcopy((c,n,j));mut(a,z,m)
  try:validate(a,z,m,s,r['qualifications'])
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('negative accepted '+name)
 for name,mut in [('R10REQ002',after.replace('### REQ-DEVICE-CORPUS-002','### REQ-DEVICE-CORPUS-202',1)),('old013prefix',after.replace('### REQ-DEVICE-CORPUS-013','### REQ-DEVICE-CORPUS-313',1)),('oldrow',after.replace('| DCO-001 |','| DCO-999 |',1)),('oldtiming',after.replace('**Latency.** None.','**Latency.** Changed.',1))]:
  need(mut!=after,'meaningful '+name)
  for x in reversed(d['replacements']):mut=mut.replace(x['new'],x['old'],1)
  need(mut!=before,'preservation '+name);neg.append(name)
 for x in d['replacements']:
  for link in re.findall(r'\]\(([^)]+)\)',x['new']):need((R/'wiki/specs'/link.split('#')[0]).resolve().exists(),'newlink')
 if (P/'manifest.json').exists():
  m=load('manifest.json');need({x.name for x in P.iterdir()}=={'manifest.json'}|{x['path'] for x in m['payloads']},'sealedtree')
  for x in m['payloads']:raw=(P/x['path']).read_bytes();need(len(raw)==x['bytes'] and sha(raw)==x['sha256'],'payload')
 return {'status':'PASS','owner_after':d['owner_after'],'newcases':268,'range':['DCO-295','DCO-562'],'wholehistories':270,'aliases':272,'oldrefs':['DCO-030','DCO-031'],'baselinealiases':3,'12otherwhole_includingR10REQ002_old013prefix_exact':True,'old294IDs36rows_exact':True,'R3R10objectproviders_exact':len(b['old_objects']),'criteriaU_modal176_parked96_history_release27g73e_exact':True,'fullreverse':True,'original_decimal_binary64_held_context_LIBMUNSET_exact':True,'negativecontrols':neg,'actual_packet_reads':0,'source_raw_numeric_rechecks':0,'original_calls':0}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',required=True,action='store_true');p.parse_args();print(json.dumps(main(),indent=2))
