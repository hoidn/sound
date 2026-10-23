#!/usr/bin/env python3
"""Retain only Root-approved metadata projections. No native/C/body traversal."""
from pathlib import Path
import hashlib, json, collections, datetime

HERE = Path(__file__).resolve().parent
COMP = HERE.parent/'component-resolution-v1'
INDEX = Path('/var/tmp/sound-analysis/corpus/indexes')
def sha(b): return hashlib.sha256(b).hexdigest()
def load(n): return json.loads((HERE/n).read_text())
approval_raw = (HERE/'scope-approval-root.json').read_bytes()
assert sha(approval_raw) == 'ca9060260a68e7f279a583aa0948058772fcd908f4a1af996e77882139893666'
approval = json.loads(approval_raw)
census_raw = (HERE/'metadata-scope-census.json').read_bytes()
assert sha(census_raw) == approval['census']['sha256']
census = json.loads(census_raw)
expected = {x['path']:x for x in census['metadata_provider_identities']}
points = {x['address_point']:x for x in approval['class_points']}
alias_entries = {x['entry'] for x in census['seed_metadata']}
call_entries = set(approval['exact_call_seed_entries'])
assert len(points)==32 and len(alias_entries)==153 and len(call_entries)==115
assert call_entries == {x['entry'] for x in census['seed_metadata'] if set(x['roles']) & {'small-prefix','large-construction-prefix','named-frontier'}}
rows=[]; providers=[]
def scan(path, kind, predicate, project=lambda x:x):
    before=path.stat(); digest=hashlib.sha256(); offset=0; selected=0
    with path.open('rb') as stream:
        for line,raw in enumerate(stream,1):
            digest.update(raw); record=json.loads(raw)
            if predicate(record):
                selected+=1
                loc=dict(path=str(path),line=line,byte=offset,bytes=len(raw),sha256=sha(raw))
                rows.append(dict(kind=kind,provider=loc,record=project(record)))
            offset+=len(raw)
    after=path.stat(); actual=dict(path=str(path),bytes=offset,lines=line,sha256=digest.hexdigest())
    assert (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)
    assert all(actual[k]==expected[str(path)][k] for k in ['bytes','lines','sha256'])
    providers.append(dict(actual,selected=selected,stat_unchanged=True))

def table_projection(record):
    ap=record['address_point']; point=points[ap]
    assert record['literal_type_encoding']==point['type'] and record['offset_to_top']==0
    slots=record['slots']; n=point['selected_slots']
    assert n==(len(slots) if len(slots)<=8 else 3)
    header={k:v for k,v in record.items() if k!='slots'}
    header.update(exported_prefix_slot_count=len(slots),selected_slot_count=n,
                  selection_scope='whole small exported prefix' if len(slots)<=8 else 'leading three construction/lifetime prefix only',
                  unselected_slot_count=len(slots)-n)
    return dict(header=header,selected_slots=slots[:n])

scan(COMP/'class-tables.jsonl','class-table',lambda d:d['address_point'] in points,table_projection)
# Split selected slots into explicit logical rows while keeping their one source-row locator.
split=[]
for row in rows:
    record=row['record'];split.append(dict(kind='class-table-header',provider=row['provider'],record=record['header']))
    for i,slot in enumerate(record['selected_slots']):
        split.append(dict(kind='class-slot',provider=dict(row['provider'],pointer='/slots/'+str(i)),
                          record=dict(address_point=record['header']['address_point'],slot_index=i,**slot)))
rows=split
scan(COMP/'class-stores.jsonl','literal-store-candidate',lambda d:d['address_point'] in points)
scan(INDEX/'aliases.jsonl','alias',lambda d:d['entry'] in alias_entries)
scan(COMP/'symbol-memberships.jsonl','alias-membership',lambda d:d['kind']=='alias_membership' and d['entry'] in alias_entries)
scan(INDEX/'calls.jsonl','outgoing-call',lambda d:d['caller'] in call_entries)
scan(INDEX/'indirect.jsonl','indirect',lambda d:d['function'] in call_entries)
counts=collections.Counter(x['kind'] for x in rows)
assert counts==dict({'class-table-header':32,'class-slot':124,'literal-store-candidate':50,
                     'alias':153,'alias-membership':22,'outgoing-call':246,'indirect':37})
assert len(rows)==664
raw=b''.join((json.dumps(dict(id='SM%04d'%i,**r),separators=(',',':'))+'\n').encode() for i,r in enumerate(rows,1))
with (HERE/'retained-metadata.jsonl').open('xb') as stream:stream.write(raw)
receipt=dict(schema='approved-synthesis-selected-metadata-retention-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             root_approval_sha256=sha(approval_raw),census_sha256=sha(census_raw),rows=len(rows),counts=dict(counts),
             retained=dict(path='retained-metadata.jsonl',bytes=len(raw),sha256=sha(raw)),
             providers=providers,source_chunks_or_C_bodies_read=0,native_binary_tool_provider_original_calls=0,
             incoming_transitive_or_callee_global_slot_following=0,
             limits='Selected retained index rows/projections only. Whole provider streams hashed for immutable metadata custody, not semantic source expansion. Thirty-eight additional store-only sources have no outgoing call retention. No class/ABI/full-native-extent/runtime/grade proof.')
with (HERE/'metadata-retention-receipt.json').open('x') as stream:json.dump(receipt,stream,indent=2);stream.write('\n')
print(json.dumps(receipt,indent=2))
