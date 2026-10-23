"""Fixed Root-selected retained metadata materialization; no body/native/provider imports."""
from pathlib import Path
import json,hashlib,re,sys,collections
P=Path(__file__).resolve().parent;C=P.parent/'component-resolution-v1';I=Path('/var/tmp/sound-analysis/corpus/indexes')
PROPOSAL='2dba9910d2676fa51d785c04efcc3d5f43828fdaae08f808516b02489229c60f'
APPROVAL='5e17b4a1d5003acf06588a91636fce052303c3cb4639de4969f23ae24028fb69'
def query(path,kind,predicate,projection=lambda x:x):
 result=[];offset=0
 with path.open('rb') as source:
  for number,raw in enumerate(source,1):
   row=json.loads(raw)
   if predicate(row):result.append(dict(kind=kind,provider=str(path),source_line=number,source_byte=offset,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),record=projection(row)))
   offset+=len(raw)
 return result
def table_projection(row):
 d=dict(row);n=len(d['slots']);d.update(exported_prefix_slot_count=n,slots=d['slots'][:3] if n>16 else d['slots'],selection_policy='large leading3 construction/lifetime frontier only' if n>16 else 'whole small exported prefix',complete_native_table_class_function_or_processing_claim=False);return d
def main():
 if sys.argv[1:]!=['--rows']:raise SystemExit('Only approved --rows stdout materialization; no source/body/runtime path')
 qr=(P/'scope-census-proposal.json').read_bytes();ar=(P/'scope-approval-root.json').read_bytes()
 assert hashlib.sha256(qr).hexdigest()==PROPOSAL and hashlib.sha256(ar).hexdigest()==APPROVAL
 q=json.loads(qr);a=json.loads(ar);assert q['classes']==a['classes'] and q['proposed_all_208_seed_entries']==a['all_208_seed_entries']
 pairs={(r['type'],r['address_point']) for r in a['classes']};types={r['type'] for r in a['classes']};pat=re.compile(q['scope_regex'])
 tables=query(C/'class-tables.jsonl','table-data',lambda r:(r['literal_type_encoding'],r['address_point']) in pairs and r['offset_to_top']==0,table_projection)
 rtti=query(C/'class-rtti.jsonl','RTTI-data',lambda r:r['literal_type_encoding'] in types)
 points={r['record']['address_point'] for r in tables}
 stores=query(C/'class-stores.jsonl','store-data',lambda r:r['address_point'] in points)
 owners=query(C/'symbol-owners.jsonl','lexical-owner-data',lambda r:bool(pat.search(r.get('lexical_owner') or '')) and not (r.get('lexical_owner') or '').startswith(('boost::','std::','flip::')))
 scopes={r['record']['scope_id'] for r in owners}
 members=query(C/'symbol-memberships.jsonl','membership-data',lambda r:any(c[1] in scopes for c in r.get('candidates',[])))
 entries={r['record']['entry'] for r in members}
 aliases=query(I/'aliases.jsonl','alias-data',lambda r:r['entry'] in entries)
 assert [r['record']['entry'] for r in aliases]==a['all_208_seed_entries'] and len(aliases)==208
 calls=query(I/'calls.jsonl','call-data',lambda r:r['caller'] in entries)
 indirect=query(I/'indirect.jsonl','indirect-data',lambda r:r.get('function') in entries or r.get('caller') in entries)
 counts=[len(owners),len(members),len(aliases),len(rtti),len(tables),len(stores),len(calls),len(indirect)]
 assert counts==[207,208,208,32,32,56,256,12]
 assert sum(len(r['record']['slots']) for r in tables)==96 and sum(r['record']['exported_prefix_slot_count'] for r in tables)==1855
 assert len(tables)<=a['caps']['primary_tables'] and 96<=a['caps']['selected_slots'] and len(stores)<=a['caps']['stores'] and len(aliases)+len(members)<=a['caps']['aliases_plus_memberships'] and len(entries)<=a['caps']['call_seeds'] and len(calls)+len(indirect)<=a['caps']['outgoing_plus_indirect']
 for r in owners+members+aliases+rtti+tables+stores+calls+indirect:print(json.dumps(r,separators=(',',':'),ensure_ascii=False))
if __name__=='__main__':main()
