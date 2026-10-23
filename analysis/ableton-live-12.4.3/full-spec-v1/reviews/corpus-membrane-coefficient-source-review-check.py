from pathlib import Path
import json,hashlib,copy,sys,datetime
ROOT=Path('/home/ollie/Documents/sound');REV=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/reviews'
QP=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/queries/corpus-membrane-coefficient-frontier-2026-10-20.json'
OUT=REV/'corpus-membrane-coefficient-source-review-evidence.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':digest(b)}
def array_data(p,prefix):
 t=p.read_text();assert t.startswith(prefix) and t.endswith(';\n');return json.loads(t[len(prefix):-2])
def good_span(span,code):
 raw=span['code'].encode();lo,hi=span['normalized_C_UTF8_byte_range_half_open'];a,b=span['lines_1_based_inclusive'];lines=code.splitlines(keepends=True)
 assert code.encode()[lo:hi]==raw and ''.join(lines[a-1:b]).encode()==raw
 assert len(raw)==span['bytes'] and digest(raw)==span['sha256']
 assert lo==len(''.join(lines[:a-1]).encode()) and hi==len(''.join(lines[:b]).encode())
assert sys.argv[1:]==['--check'] and not OUT.exists()
q=json.loads(QP.read_text());assert identity(QP)['sha256']=='170bdc1d42cc3668fe914e7ff194e479feb534ed99af15be175ac7488c9c2795'
roles={r['role']:Path(r['path']) for r in q['sources']}
watched={QP,*roles.values()}
for d in [ROOT/'handoff',ROOT/'analysis/ableton-live-12.4.3/handoff-staging/device-corpus-v5-final']:
 watched.update(p for p in d.rglob('*') if p.is_file())
before=[identity(p) for p in sorted(watched)]
for row in q['sources']:
 i=identity(Path(row['path']));assert (i['bytes'],i['sha256'])==(row['bytes'],row['sha256'])
manifest=json.loads(roles['browser_manifest'].read_text())
assert manifest['program']=='Corpus.arm64' and manifest['executable_sha256']==q['binary_identity']['sha256']
for role in ['modal_chunk','builder_chunk','browser_function_index']:
 p=roles[role];rel=str(p.relative_to(roles['browser_manifest'].parent));assert digest(p.read_bytes())==manifest['outputs'][rel]
bs=array_data(roles['builder_chunk'],'window.r2Chunks=window.r2Chunks||{};window.r2Chunks[5]=')
ms=array_data(roles['modal_chunk'],'window.r2Chunks=window.r2Chunks||{};window.r2Chunks[4]=')
b=bs[q['builder']['array_index']];m=ms[q['modal']['array_index']]
assert b==q['builder']['complete_previously_read_record'] and b['entry']=='0x25210' and m['entry']=='0x1f3f8'
assert b['partial_code']==False and m['partial_code']==False and b['warnings']==q['builder']['complete_previously_read_record']['warnings']
assert {k:v for k,v in m.items() if k!='code'}==q['modal']['metadata']
assert len(b['code'].encode())==q['builder']['code_bytes']==11041 and digest(b['code'].encode())==q['builder']['code_sha256']
assert len(m['code'].encode())==q['modal']['full_code_bytes']==31443 and digest(m['code'].encode())==q['modal']['full_code_sha256']
union=set()
for s in q['modal']['selected_spans']:
 good_span(s,m['code']);a,z=s['normalized_C_UTF8_byte_range_half_open'];union.update(range(a,z))
assert len(union)==q['modal']['new_C_unique_line_bytes']==15899 and len(union)<=16000
assert len(q['modal']['selected_spans'])==18 and len(q['modal']['incidental_locator_lines'])==11
for key in ['code','sha256','lines_1_based_inclusive','normalized_C_UTF8_byte_range_half_open']:
 s=copy.deepcopy(q['modal']['selected_spans'][1])
 if key=='code':s[key]=s[key].replace('fVar61','fVar60',1)
 elif key=='sha256':s[key]='0'*64
 else:s[key][0]+=1
 try:good_span(s,m['code'])
 except AssertionError:pass
 else:raise AssertionError('wrong association accepted: '+key)
for row in q['integer_address_identities_only'][1:]:
 assert row['coefficient_base']+4*row['coefficient_float_index']==row['address_offset']==row['recurrence_base']+4*row['recurrence_float_index']
assert 0x148+0x1c==0x164
for f in q['preservation'].values():assert f in (None,False,True,0)
assert q['preservation']['actual_expected'] is None and q['preservation']['actual_comparison'] is None and q['preservation']['candidate_or_application_grade'] is None
assert q['scope']['full_modal_body_semantically_read']==False and q['source_export_utc'] is None
assert len(q['claims'])==6 and all(c['predicate'] and c['not_proved'] for c in q['claims'])
assert 'NOT a proven rounded/runtime slot label from R>1 alone' in q['claims'][1]['conclusion']
assert 'same slot' in q['pole_derivation_design_only']['predicate'] or 'SAME slot' in q['pole_derivation_design_only']['predicate']
after=[identity(p) for p in sorted(watched)];assert before==after
result={'schema':'independent-corpus-membrane-source-association-check-v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'query':identity(QP),'source_pins':[identity(p) for p in roles.values()],'exact_builder_record_and_metadata':True,'builder_C_bytes':11041,'exact_modal_metadata_and_fullcode_hash_only':True,'full_modal_code_bytes':31443,'all18_selected_spans_exact':True,'unique_selected_modal_C_bytes':len(union),'cap':16000,'rejection_fixtures':['wrong retained C text','wrong span hash','wrong line start','wrong UTF8 byte start'],'integer_address_identities':q['integer_address_identities_only'],'pole_or_float_formula_executed':False,'source_functions_loaded_or_run':False,'new_source_bodies_instructions_or_words_read':False,'watch':{'paths':len(before),'scope':'query + 9 exact source pins + all published handoff files + exact v5 final staged tree, only this check interval','before_sha256':digest(json.dumps(before,sort_keys=True).encode()),'after_sha256':digest(json.dumps(after,sort_keys=True).encode()),'unchanged':True},'failures':[]}
with OUT.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'status':'PASS source/data only','evidence':identity(OUT),'watch':len(before)},indent=2))
