#!/usr/bin/env python3
"""Read-only, data-only checker. Never opens source chunks, indexes, images or helpers."""
from pathlib import Path
import hashlib,json,re,copy
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def read(name):return json.loads((HERE/name).read_text())
def digest(data):return hashlib.sha256(data).hexdigest()
def validate(d):
 census=d['census'];sel=d['selection'];raw=d['raw'];sm=d['source_map'];claims=d['claims']['claims'];a=d['assessment'];receipt=d['receipt']
 assert digest(d['census_raw'])=='602160bb7f19bc2d70922d2addf16ac2fd017e789dde2091d6959c78748bea3b'
 assert digest(d['selection_raw'])=='39f48a14ec8f6a51c75e2f29b2988db6c185be47e8b2b69c62784a1b4195c8d1'
 entries=sel['entries'];assert len(entries)==len(set(entries))==14
 records=[json.loads(x) for x in raw.splitlines()];assert len(records)==14
 assert [r['entry'] for r in records]==[r['entry'] for r in census['records']]==[r['entry'] for r in sm['records']]==[r['entry'] for r in claims]==entries
 offset=0;totalC=totalLines=warnings=0
 for record,meta,loc,claim in zip(records,census['records'],sm['records'],claims):
  segment=raw[offset:offset+meta['raw_bytes']];assert json.loads(segment)==record and digest(segment)==meta['raw_sha256']
  assert loc['retained_byte_start']==offset and loc['retained_bytes']==meta['raw_bytes'] and loc['raw_sha256']==meta['raw_sha256']
  for own,source in [('source_path','source_path'),('source_byte','source_byte'),('source_line','source_line')]:assert loc[own]==meta[source]
  code=record['code'];lines=code.splitlines(keepends=True)
  assert len(code.encode())==loc['code_utf8_bytes']==meta['code_utf8_bytes'] and digest(code.encode())==loc['code_sha256']==meta['code_sha256']==record['code_sha256']
  assert len(lines)==loc['code_lines']==meta['C_lines']<=1500
  assert record['warnings']==loc['warnings']==meta['warnings']==claim['warning_qualification']
  assert record['body_bytes']==loc['native_body_bytes']==meta['native_body_bytes'] and record['body_ranges']==loc['native_body_ranges']==meta['native_body_ranges']
  assert record['thunk']==loc['record_thunk']==meta['record_thunk']
  assert record['state']==meta['state'] and record['error']==meta['error'] and record['timed_out']==meta['timed_out'] and record['partial_code']==meta['partial_code']
  assert claim['evidence']=='observed-static recovered-C projection only' and claim['public_binding']=='unknown' and claim['whole_callable_X_leaf'] is False and claim['execution_or_grade_credit']==0
  assert len(claim['missing_prerequisites'])>0
  assert claim['direct_helper_tokens']==sorted(set(re.findall(r'\bFUN_[0-9a-f]+',code)))
  assert claim['global_tokens']==sorted(set(re.findall(r'\b(?:DAT|_DAT|UNK|_UNK)_[0-9a-f]+',code)))
  for span in claim['spans']:
   assert 1<=span['C_start']<=span['C_end']<=len(lines)
   assert digest(''.join(lines[span['C_start']-1:span['C_end']]).encode())==span['sha256']
  offset+=len(segment);totalC+=len(code.encode());totalLines+=len(lines);warnings+=bool(record['warnings'])
 assert offset==len(raw)==sm['raw_bytes']==a['raw_jsonl_bytes']==30164
 assert totalC==sm['code_bytes']==a['recovered_C_bytes']==21218<=196608
 assert totalLines==sm['code_lines']==a['recovered_C_lines']==634 and warnings==sm['warning_records']==a['warning_records']==5
 assert max(len(r['code'].splitlines()) for r in records)==a['max_C_lines']==213
 assert len({r['source_path'] for r in sm['records']})==a['selected_chunks']==6
 assert a['selected_set_records']==14 and a['fully_bounded_callable_math_leaves']==a['whole_callable_X_leaves']==[]
 assert a['four_byte_native_body_entries']==[r['entry'] for r in records if r['body_bytes']==4] and len(a['four_byte_native_body_entries'])==4
 control=a['conditional_control_candidates'];assert len(control)==1 and control[0]['entry']=='0x101bec394' and control[0]['status']=='source-only simple store candidate, not execution-ready' and len(control[0]['prerequisites'])==3
 frag=a['auxiliary_algebra_fragments'];assert len(frag)==1 and frag[0]['entry']=='0x102e027c0' and frag[0]['C_lines']==[61,74] and frag[0]['status']=='local expression only; enclosing callback not self-contained'
 assert all(x=='unknown' for x in a['public_chain'].values())
 assert a['required_predicate_contexts']==562 and a['required_routes_unchanged']=='562 no-established-route/U; no X/S promotion'
 assert a['actual_case_results']==176 and a['actual_results_unchanged']=='all null/U/unexecuted'
 assert a['unsupported_required']=='U;coverageOPEN' and a['no_documentary_fallback'] is True and a['required_inventory_is_not_grade'] is True
 assert a['site_or_grade_or_norm_case_release_changes']==a['original_or_native_or_provider_execution']==a['source_expansion_beyond_fixed14']==0 and a['successor_selected'] is False
 assert receipt['source_records_read']==14 and receipt['source_raw_bytes_read']==30164 and receipt['code_bytes']==21218 and receipt['code_lines']==634
 assert receipt['raw_source_reopens_after_materialization']==receipt['tool_original_provider_decoder_native_calls']==receipt['binary_bytes_read']==receipt['encountered_callee_global_slot_reads']==0
 assert receipt['inherited_chunk_pins']==census['selected_chunk_pins']

def main():
 cr=(HERE/'candidate-census.json').read_bytes();sr=(HERE/'selection-source-read.json').read_bytes()
 d=dict(census=json.loads(cr),census_raw=cr,selection=json.loads(sr),selection_raw=sr,raw=(HERE/'sources.jsonl').read_bytes(),source_map=read('source-map.json'),claims=read('claims.json'),assessment=read('whole-set-assessment.json'),receipt=read('read-receipt.json'))
 pins=read('pins.json');checked=[]
 for p in pins['pins']+pins['root_preservation_pins']:
  path=Path(p['path']);path=(HERE/path) if len(path.parts)==1 else (path if path.is_absolute() else ROOT/path)
  data=path.read_bytes();assert len(data)==p['bytes'] and digest(data)==p['sha256'],str(path);checked.append(p['path'])
 validate(d)
 controls=[
 ('source-byte-corruption',lambda x:x.update(raw=b' '+x['raw'][1:])),
 ('omit-selected-record',lambda x:x.update(raw=b''.join(x['raw'].splitlines(keepends=True)[:-1]))),
 ('unselected-source-entry',lambda x:x['source_map']['records'][0].update(entry='0x0')),
 ('bad-source-range',lambda x:x['source_map']['records'][0].update(source_byte=0)),
 ('bad-retained-hash',lambda x:x['source_map']['records'][0].update(raw_sha256='0'*64)),
 ('warning-erasure',lambda x:x['claims']['claims'][0].update(warning_qualification=[])),
 ('span-mislocation',lambda x:x['claims']['claims'][0]['spans'][0].update(C_start=1)),
 ('invented-global-free-leaf',lambda x:x['claims']['claims'][3].update(global_tokens=[])),
 ('invented-helper-free-leaf',lambda x:x['claims']['claims'][2].update(direct_helper_tokens=[])),
 ('promote-partial-wrapper',lambda x:x['claims']['claims'][6].update(whole_callable_X_leaf=True)),
 ('promote-store-to-X',lambda x:x['assessment']['whole_callable_X_leaves'].append('0x101bec394')),
 ('promote-expression-to-mathleaf',lambda x:x['assessment']['fully_bounded_callable_math_leaves'].append('0x102e027c0')),
 ('invent-store-legal-setup',lambda x:x['assessment']['conditional_control_candidates'][0].update(status='execution-ready')),
 ('close-public-receiver',lambda x:x['assessment']['public_chain'].update(same_callback_processor_receiver='known')),
 ('erase-native-fourbyte-gap',lambda x:x['assessment'].update(four_byte_native_body_entries=[])),
 ('invent-original-call',lambda x:x['assessment'].update(original_or_native_or_provider_execution=1)),
 ('expand-callee',lambda x:x['assessment'].update(source_expansion_beyond_fixed14=1)),
 ('select-successor',lambda x:x['assessment'].update(successor_selected=True)),
 ('invent-grade',lambda x:x['assessment'].update(site_or_grade_or_norm_case_release_changes=1)),
 ('close-unsupported',lambda x:x['assessment'].update(unsupported_required='complete')),
 ('documentary-fallback',lambda x:x['assessment'].update(no_documentary_fallback=False)),
 ('native-image-reopen',lambda x:x['receipt'].update(binary_bytes_read=4))]
 negatives=[]
 for name,mutate in controls:
  z=copy.deepcopy(d);mutate(z)
  try:validate(z)
  except (AssertionError,ValueError,KeyError,IndexError,json.JSONDecodeError):negatives.append(dict(name=name,rejected=True))
  else:raise AssertionError('negative not rejected: '+name)
 print(json.dumps(dict(status='PASS',checked_pins=checked,selected_records=14,raw_bytes=30164,recovered_C_bytes=21218,C_lines=634,warning_records=5,negative_controls=negatives,source_chunk_reopens=0,binary_original_provider_decoder_model_comparator_runs=0,scope='Read-only retained packet/selected predecessor metadata and canonical as-of pin integrity; no original source record reopening, no root builder execution, no semantic oracle or grade'),indent=2))
if __name__=='__main__':main()
