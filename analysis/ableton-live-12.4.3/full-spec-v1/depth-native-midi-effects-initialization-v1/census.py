"""Census fixed seeds as retained data only; print metadata, no C bodies or source writes."""
import pathlib,json,re,hashlib,collections
R=pathlib.Path(__file__).resolve().parents[4];F=R/'analysis/ableton-live-12.4.3/full-spec-v1';M=F/'family-native-midi-effects-routes-v1';rows=[json.loads(l)for l in (M/'native-data.jsonl').read_text().splitlines()];names={'OMidi'+s+'Processor'for s in ['Arpeggiator','CcControl','Chord','NoteLength','Pitcher','Random','Scale','Velocity']};roles=collections.defaultdict(list)
for index,row in enumerate(rows,1):
 d=row['record']
 if row['kind']=='literal-store-candidate':roles[d['entry']].append({'kind':'literal-store-candidate','address_point':d['address_point'],'native_map_line':index})
 if row['kind']=='table-prefix-data':
  for slot in d['slots']:roles[slot['target']].append({'kind':'class-prefix-slot-target','type':d['literal_type_encoding'],'address_point':d['address_point'],'slot_offset':slot['offset']})
 if row['kind']=='selected-alias-data'and any(re.search(re.escape(n)+r'::(?:Init|Exit|Reset|OnOn)(?:>|\()',d['name'])for n in names):roles[d.get('thunk_target')or d['entry']].append({'kind':'named-lifecycle-wrapper','alias_entry':d['entry'],'name':d['name'],'normalized_known_thunk_target':d.get('thunk_target')})
assert len(roles)==74
eligible=0;loc={};aliasmeta={}
for raw in pathlib.Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl').open('rb'):
 d=json.loads(raw)
 if not d['external']:
  if d['entry']in roles:loc[d['entry']]=eligible//100;aliasmeta[d['entry']]=d
  eligible+=1
assert eligible==418417 and len(loc)==74
cpins=json.loads((F/'component-resolution-v1/class-inputs.json').read_text())['decomp_chunk_pins'];cp={p['path']:p for p in cpins};chunks=collections.defaultdict(set)
for entry,n in loc.items():chunks[n].add(entry)
census=[];missing=[];chunkpins=[]
for number,selected in sorted(chunks.items()):
 path=pathlib.Path('/var/tmp/sound-analysis/corpus/decomp/chunks')/f'chunk-{number:05}.jsonl';data=path.read_bytes();pin=cp.get(str(path));assert pin is not None,str(path);assert len(data)==pin['bytes']and hashlib.sha256(data).hexdigest()==pin['sha256'];chunkpins.append(pin)
 off=0;found=set()
 for i,raw in enumerate(data.splitlines(keepends=True),1):
  m=re.search(br'"entry"\s*:\s*"([^\"]+)"',raw[:100]);entry=m[1].decode()if m else''
  if entry in selected:
   d=json.loads(raw);code=d.get('code')or'';b=code.encode();found.add(entry)
   census.append({'entry':entry,'roles':roles[entry],'alias_name':aliasmeta[entry]['name'],'alias_thunk':aliasmeta[entry]['thunk'],'alias_thunk_target':aliasmeta[entry].get('thunk_target'),'source_path':str(path),'source_line':i,'source_byte':off,'raw_bytes':len(raw),'raw_sha256':hashlib.sha256(raw).hexdigest(),'code_bytes':len(b),'C_lines':len(code.splitlines()),'code_sha256':hashlib.sha256(b).hexdigest(),'native_body_bytes':d.get('body_bytes'),'native_body_ranges':d.get('body_ranges'),'record_thunk':d.get('thunk'),'state':d.get('state'),'warnings':d.get('warnings'),'error':d.get('error'),'timed_out':d.get('timed_out'),'partial_code':d.get('partial_code')})
  off+=len(raw)
 missing.extend(sorted(selected-found))
summary={'unique_selected_entries':len(roles),'located':len(census),'missing':missing,'total_C_utf8_bytes':sum(r['code_bytes']for r in census),'max_C_lines':max(r['C_lines']for r in census),'total_C_lines':sum(r['C_lines']for r in census),'records_exceeding_1500_lines':[{'entry':r['entry'],'C_lines':r['C_lines'],'code_bytes':r['code_bytes']}for r in census if r['C_lines']>1500],'native_extent_bytes_sum_over_unique_entries':sum(r['native_body_bytes']or 0 for r in census),'record_thunks':sum(bool(r['record_thunk'])for r in census),'distinct_range_sets':len({json.dumps(r['native_body_ranges'])for r in census}),'selected_chunks':len(chunkpins)}
summary['within_caps']=not missing and len(census)<=96 and summary['total_C_utf8_bytes']<=262144 and summary['max_C_lines']<=1500
out={'schema':'native-midi-initialization-seed-census-v1','fixed_selection':'All27literalstore entries+35prefix targets+known-metadata-thunk-normalized Init/Exit/Reset/OnOn wrappers (elsealiasentry); no callee expansion.','caps':{'records':96,'C_utf8_bytes':262144,'C_lines_per_record':1500},'omissions':[],'locator_method':'Nonexternal alias ordinal nominates C1 chunk100; exact selected entry confirms locator and every selected chunk matches approved1a class-inputs pin. No old cache/script imported, no nonselected body parsed or semantic body output.','summary':summary,'records':sorted(census,key=lambda r:int(r['entry'],16)),'approved_chunk_pins':chunkpins,'source_materialized':False,'semantic_bodies_read':False}
print(json.dumps(out,indent=2))
