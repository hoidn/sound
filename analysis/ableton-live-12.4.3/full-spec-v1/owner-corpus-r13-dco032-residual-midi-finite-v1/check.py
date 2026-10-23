"""Owner mapping/preservation only. External reads: current owner and two approved Root reviews. Never actual packet/code/raw or old proposal catalogs."""
from pathlib import Path
import json,hashlib,re,copy,sys
P=Path(__file__).resolve().parent;R=Path('/home/ollie/Documents/sound');F=R/'analysis/ableton-live-12.4.3/full-spec-v1'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_text())
def reqs(s):
 out={}
 for m in re.finditer(r'^### (REQ-DEVICE-CORPUS-\d{3})[^\n]*\n',s,re.M):
  ends=[v for v in [s.find('\n### ',m.end()),s.find('\n## ',m.end())]if v>=0];end=min(ends)if ends else len(s);out[m[1]]=s[m.start():end+1]
 return out

def verify(delta,C,N,J,B,before,S,rv,prior):
 assert len(before.encode())==B['owner_before']['bytes']==delta['owner_before']['bytes']==97341
 assert sha(before.encode())==B['owner_before']['sha256']==delta['owner_before']['sha256']=='21087e2ebc735563b1d4f0451f3a6613342bb514b9591726b0a2c8c4ad4903d3'
 assert delta['canonical_write']is False and len(delta['replacements'])==4
 out=before
 for z in delta['replacements']:assert out.count(z['old'])==1;out=out.replace(z['old'],z['new'],1)
 assert len(out.encode())==delta['owner_after']['bytes']and sha(out.encode())==delta['owner_after']['sha256']
 reverse=out
 for z in reversed(delta['replacements']):assert reverse.count(z['new'])==1;reverse=reverse.replace(z['new'],z['old'],1)
 assert reverse==before
 rb,ra=reqs(before),reqs(out);assert len(rb)==len(ra)==13 and all(ra[k]==v for k,v in rb.items()if not k.endswith('013'))and ra['REQ-DEVICE-CORPUS-013'].startswith(rb['REQ-DEVICE-CORPUS-013'])
 assert {k:{'bytes':len(v.encode()),'sha256':sha(v.encode())}for k,v in rb.items()}==B['requirement_bodies']
 rows=[x for x in out.splitlines()if re.match(r'^\| DCO-\d{3} \|',x)];assert rows==B['old_case_rows']and sha(enc(rows))==B['old_rows_sha256']and len(rows)==36
 assert B['old_IDs']==list(range(1,959))and prior['total_navigation_IDs']==958 and prior['approved_owner_target']['utf8_text']==before
 assert sha(enc(prior['approved_complete_mapping']))==B['R12_embedded_mapping_sha256']and len(prior['approved_complete_mapping']['catalog']['catalog'])==397
 def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
 for name,a,b in [('metric','## Comparison metric','## Acceptance cases'),('open_questions','## Open questions','## Analyst evidence appendix'),('timing','## Timing and state','## R7 scope addition')]:assert sha(section(out,a,b).encode())==B['protected_sections'][name]
 oldacc=section(before,'## Acceptance cases','## Open questions');assert section(out,'## Acceptance cases','## Open questions').startswith(oldacc)
 assert sha(oldacc.encode())==B['protected_sections']['old_acceptance']
 assert all(x in out for x in B['old_analysis_JSON_navigation_links'])and B['release_groups']==27 and B['release_evaluations']==73
 assert C['shared_input']==S['shared_input']and C['aliases']==S['aliases']and C['logical_aliases']==160 and C['whole_histories']==158 and C['newcases']==157 and C['inherited']==1 and C['portable_admission']is None
 assert C['baseline_three_aliases_one_INPUT_reference']is True and C['review_qualifications']==rv['qualifications']
 assert len(C['catalog'])==len(S['approved_points'])==len(S['input_histories'])==158 and len(N)==157 and len(J['histories'])==158 and len(J['aliases'])==160
 fresh=[];seq=958;seen=set()
 for i,(z,x,h)in enumerate(zip(C['catalog'],S['approved_points'],S['input_histories'])):
  base=x['provenance']=='inherited-no-replay'
  if not base:seq+=1
  cid=None if base else f'DCO-{seq:03d}'
  assert z['id']==x['id']==h['id']and z['case_id']==cid and z['existing_case_refs']==(['DCO-032']if base else[])
  assert z['history_sha256']==h['history_sha256']==x['history_sha256']and z['history_sha256']not in seen;seen.add(z['history_sha256'])
  assert z['events']==x['events']==h['events']and z['packed16_events_le']==h['packed16_events_le']and z['eligibility_history']==h['eligibility_history']and z['first_alias']==h['first_alias']
  for k in ['parameter_tokens','parameter_f32_bits_le','parameter_f64_reconstructed_le','parameter_vector_sha256','parameter_token_binary64_sha256']:assert z[k]==h[k]==S['shared_input'][k]
  assert z['requirements']==['REQ-DEVICE-CORPUS-013']and z['fixed_history_pointer']=='#/shared_input/fixed_history'and z['qualification_pointer']=='#/review_qualifications'
  assert z['approved_point_pointer']==f'/approved_summary/approved_points/{i}'and z['input_history_pointer']==f'/approved_summary/input_histories/{i}'and z['approved_point_sha256']==sha(enc(x))and z['input_history_sha256']==sha(enc(h))
  assert z['provenance']==x['provenance']and z['native_observation']==(None if base else x)and z['historical']==(x if base else None)
  assert z['new_pid']==(None if base else x['pid'])and z['new_receipt']==(None if base else x['receipt_pointer'])
  assert all(z[k]is None for k in ['new_metrics_for_inherited','waveform_prior','new_expected_waveform','portable_expected','portable_comparator','grade'])and z['new_application_predicate_proof']is False and z['old_modal_budget_transferred']is False
  assert J['histories'][i]=={k:z[k]for k in ['id','case_id','existing_case_refs','history_sha256','approved_point_pointer','input_history_pointer']}
  if not base:fresh.append(z)
 assert seq==1115 and fresh==N and[N['case_id']for N in fresh]==[f'DCO-{i:03d}'for i in range(959,1116)]
 assert not({z['history_sha256']for z in fresh}&{z['history_sha256']for z in prior['approved_complete_mapping']['catalog']['catalog']})
 byid={z['id']:z for z in C['catalog']}
 for a,j in zip(C['aliases'],J['aliases']):
  z=byid[a['id']];assert j=={'axis':a['axis'],'value':a['value'],'id':a['id'],'case_id':z['case_id'],'existing_case_refs':z['existing_case_refs'],'events':a['events'],'history_key':a['history_key']}
 assert sum(a['id']=='CGR-U060'for a in C['aliases'])==3 and sum(z['case_id']is None for z in C['catalog'])==1
 added=ra['REQ-DEVICE-CORPUS-013'][len(rb['REQ-DEVICE-CORPUS-013']):]
 for literal in ['127 Off keys with On key 60 fixed','15 On channel nibbles with Off status 80','15 Off channel nibbles with On status 90','ONE old DCO-032 INPUT reference','portable expected/comparator/grade','remain NULL','new application-predicate proofs remain false']:assert literal in added
 assert 'revision: 13\n'in out and '## Finite supplied DCO032 residual MIDI observation annex — revision 13'in out
 return out

def main():
 delta=load(P/'owner.delta.json');C=load(P/'catalog158.json');N=load(P/'new-cases157.json');J=load(P/'joins160.json');B=load(P/'baseline.json')
 before=(R/'wiki/specs/device-corpus.md').read_text();rp=R/C['approved_review']['path'];raw=rp.read_bytes();assert len(raw)==9108938 and sha(raw)=='a728173fc59cf176177bd3882f1da8027718b838be5dd5be9f0dbd39077d363f';rv=json.loads(raw);S=rv['approved_summary']
 pr=R/B['approved_prior_owner_review']['path'];raw=pr.read_bytes();assert sha(raw)=='2446ac0dbdf15592e0a2561e28639ab2629f1d1319873c86b1206985e2ef1cbb';prior=json.loads(raw)
 out=verify(delta,C,N,J,B,before,S,rv,prior);neg=[]
 for name,mut in [('omitHistory',lambda d,c,n,j,b:c['catalog'].pop()),('omitAlias',lambda d,c,n,j,b:c['aliases'].pop()),('omitNewCase',lambda d,c,n,j,b:n.pop()),('duplicateID',lambda d,c,n,j,b:c['catalog'][1].update(case_id='DCO-959')),('wrongEvents',lambda d,c,n,j,b:c['catalog'][0]['events'][1].__setitem__(2,1)),('wrongPacked',lambda d,c,n,j,b:c['catalog'][0]['packed16_events_le'].__setitem__(1,'0'*32)),('roundedToken',lambda d,c,n,j,b:c['catalog'][0]['parameter_tokens'].__setitem__(15,'0.10000000149011612')),('badF64',lambda d,c,n,j,b:c['catalog'][0]['parameter_f64_reconstructed_le'].__setitem__(15,'0'*16)),('wrongNative',lambda d,c,n,j,b:c['catalog'][0]['native_observation'].update(pid=0)),('inventBaselinePID',lambda d,c,n,j,b:c['catalog'][60].update(new_pid=1)),('baselineNewID',lambda d,c,n,j,b:c['catalog'][60].update(case_id='DCO-1116')),('prior',lambda d,c,n,j,b:c['catalog'][0].update(waveform_prior='fit')),('expectedWaveform',lambda d,c,n,j,b:c['catalog'][0].update(new_expected_waveform='exact')),('portable',lambda d,c,n,j,b:c['catalog'][0].update(portable_comparator='exact')),('grade',lambda d,c,n,j,b:c['catalog'][0].update(grade='PASS')),('applicationProof',lambda d,c,n,j,b:c['catalog'][0].update(new_application_predicate_proof=True)),('modalTransfer',lambda d,c,n,j,b:c['catalog'][0].update(old_modal_budget_transferred=True)),('joinID',lambda d,c,n,j,b:j['histories'][0].update(case_id='DCO-001')),('joinAlias',lambda d,c,n,j,b:j['aliases'][0].update(value=1)),('dropQualification',lambda d,c,n,j,b:c.update(review_qualifications=[])),('baselineAliasCount',lambda d,c,n,j,b:c.update(baseline_three_aliases_one_INPUT_reference=False)),('canonicalWrite',lambda d,c,n,j,b:d.update(canonical_write=True)),('badTarget',lambda d,c,n,j,b:d['owner_after'].update(sha256='0'*64)),('alterOldClause',lambda d,c,n,j,b:d['replacements'].append({'old':'## Scope','new':'## Changed Scope'})),('oldRow',lambda d,c,n,j,b:b['old_case_rows'].pop()),('oldIDs',lambda d,c,n,j,b:b['old_IDs'].pop()),('releaseBudget',lambda d,c,n,j,b:b.update(release_evaluations=74)),('oldR12Mapping',lambda d,c,n,j,b:b.update(R12_embedded_mapping_sha256='0'*64))]:
  args=copy.deepcopy([delta,C,N,J,B]);mut(*args);assert args!=[delta,C,N,J,B],name
  try:verify(*args,before,S,rv,prior)
  except(AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('accepted '+name)
 if(P/'manifest.json').exists():
  m=load(P/'manifest.json');assert{str(p.relative_to(P))for p in P.rglob('*')if p.is_file()}=={'manifest.json'}|{x['path']for x in m['payloads']}
  for x in m['payloads']:
   b=(P/x['path']).read_bytes();assert len(b)==x['bytes']and sha(b)==x['sha256']
 return {'status':'PASS owner wording/mapping/IDs/preservation','target_bytes':len(out.encode()),'target_sha256':sha(out.encode()),'new_IDs':['DCO-959','DCO-1115'],'newcases':157,'logical_aliases':160,'whole_histories':158,'inherited':1,'negative_controls':neg,'other_whole_requirements':12,'entire_R10_REQ002':True,'old013_R12_prefix':True,'old_IDs':958,'old_rows':36,'old_R3_R12_objects':'inherited approved metadata and navigation preserved; no provider replay','release_groups':27,'release_evaluations':73,'full_reverse_R12':True,'external_reads':['current canonical owner','approved Root residual157 review summary','approved Root R12 owner review embedded preservation/mapping'],'actual_packet_source_raw_or_numeric_reads':0,'original_calls':0,'canonical_write':False}
if __name__=='__main__':
 assert sys.argv[1:]==['--check'];print(json.dumps(main(),indent=2))
