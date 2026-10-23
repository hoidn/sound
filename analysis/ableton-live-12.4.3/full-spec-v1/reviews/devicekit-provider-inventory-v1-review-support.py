"""Independent fixed metadata review; no author main/helper/provider/source-index execution."""
from pathlib import Path
import collections
import copy
import datetime
import hashlib
import json

ROOT=Path('/home/ollie/Documents/sound')
BASE=ROOT/'analysis/ableton-live-12.4.3/full-spec-v1'
PACK=BASE/'depth-devicekit-provider-inventory-v1'
OUT=BASE/'reviews/devicekit-provider-inventory-v1-review.json'
READ_CAP=4194304
PRIOR_CONSERVATIVE_PAYLOAD_READS=268890
reads=[]

def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):
    data=path.read_bytes()
    reads.append(dict(path=str(path),bytes=len(data),sha256=sha(data)))
    assert PRIOR_CONSERVATIVE_PAYLOAD_READS+sum(x['bytes'] for x in reads)<=READ_CAP
    return data

def ptr(doc,pointer):
    for token in pointer.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        doc=doc[int(token)] if isinstance(doc,list) else doc[token]
    return doc

manifest_bytes=read(PACK/'manifest.json')
assert len(manifest_bytes)==2133 and sha(manifest_bytes)=='6c4dc1ff7027408242c876d8a7208b85e477feed62d62d664cf9e1994f096934'
manifest=json.loads(manifest_bytes)
assert {f.name for f in PACK.iterdir() if f.is_file()}=={'manifest.json'}|{r['path'] for r in manifest['files']}
payload={}
for row in manifest['files']:
    data=read(PACK/row['path'])
    assert len(data)==row['bytes'] and sha(data)==row['sha256']
    payload[row['path']]=data
assert len(payload)==11 and sum(len(x) for x in payload.values())==113131
pins=json.loads(payload['pins.json'])['pins']
assert len(pins)==34 and len({p['path'] for p in pins})==34
cache={};exact=[];drifts=[]
for pin in pins:
    path=Path(pin['path']);path=path if path.is_absolute() else ROOT/path
    assert path.suffix in ('.md','.json','.jsonl')
    data=read(path);cache[pin['path']]=data
    same=len(data)==pin['bytes'] and sha(data)==pin['sha256']
    if pin['path'].startswith('wiki/'):
        if not same:drifts.append(dict(path=pin['path'],role=pin['role'],author_asof=dict(bytes=pin['bytes'],sha256=pin['sha256']),current=dict(bytes=len(data),sha256=sha(data))))
    else:assert same,pin['path']
    if same:exact.append(pin['path'])
assert len(drifts)==1 and drifts[0]['path']=='wiki/research/index.md'
rows=[json.loads(x) for x in payload['boundary-rows.jsonl'].splitlines()]
d=dict(rows=rows,query=json.loads(payload['query-census.json']),symbols=json.loads(payload['symbols.json']),associations=json.loads(payload['package-associations.json']),missing=json.loads(payload['missing-frontier.json']),budget=json.loads(payload['read-budget.json']))

def independent_validate(d):
    rows,q,sy,a,m,b=(d[k] for k in ['rows','query','symbols','associations','missing','budget'])
    assert len(rows)==37 and len({r['id'] for r in rows})==37
    expected=[]
    for source in q['input_census']:
        offset=0;counts=collections.Counter();picked=0
        for index,line in enumerate(cache[source['path']].splitlines(keepends=True)):
            item=json.loads(line);counts[item.get('kind')]+=1;r=item.get('record') or {}
            if item.get('kind')=='call' and (r.get('callee_resolved') or '').startswith('EXTERNAL:') and 'ODeviceKitSampleRateProcessor<' in (r.get('callee_resolved_name') or r.get('callee_name') or ''):
                expected.append((source['path'],index+1,index,offset,len(line),sha(line),item));picked+=1
            offset+=len(line)
        assert dict(counts)==source['kind_counts'] and sum(counts.values())==source['total_rows'] and picked==source['selected_rows']
    assert len(expected)==37
    for row,original in zip(rows,expected,strict=True):
        assert tuple(row[k] for k in ['parent_path','parent_line','parent_index','parent_byte_offset','parent_line_bytes','parent_line_sha256','selected'])==original
        assert row['binding_status']=='unknown' and row['actual_provider_path'] is None
        loc=row['selected']['locator'];assert loc['path']=='/var/tmp/sound-analysis/corpus/indexes/calls.jsonl'
        assert type(loc['line']) is int and loc['line']>0 and type(loc['byte_start']) is int and loc['byte_start']>=0 and loc['bytes']>0 and len(loc.get('sha256') or loc.get('raw_sha256'))==64
        rr=row['selected']['record'];assert rr['kind'] in ('call','tail-jump')
        assert rr['to']==rr['callee'] and int(rr['site'],16)%4==int(rr['callee'],16)%4==0
    assert collections.Counter(r['family'] for r in rows)=={'filter-eq':22,'dynamics':3,'distortion':12}
    groups=collections.defaultdict(list);classes=collections.Counter()
    for row in rows:
        r=row['selected']['record'];groups[r['callee_resolved']].append(row)
        classes[(r.get('callee_resolved_name') or r['callee_name']).split('ODeviceKitSampleRateProcessor<',1)[1].split('>',1)[0]]+=1
    assert len(groups)==len(sy['symbols'])==27 and len(classes)==7 and dict(classes)==sy['class_occurrences']
    assert {s['external_label'] for s in sy['symbols']}==set(groups)
    for group in sy['symbols']:
        members=groups[group['external_label']]
        assert group['boundary_rows']==[r['id'] for r in members]
        assert set(group['stub_addresses'])=={r['selected']['record']['callee'] for r in members}
        assert all(group['lexical_symbol']==(r['selected']['record'].get('callee_resolved_name') or r['selected']['record']['callee_name']) for r in members)
        assert group['provider_path'] is None and group['macho_library_ordinal'] is None and group['binding_status']=='unknown'
    assert len(a['current_device_profiles'])==7 and len(a['content_directories'])==14
    for p in a['current_device_profiles']:
        assert ptr(json.loads(cache[p['source_path']]),p['pointer'])==p['record']
        assert p['scope']=='retained preset/schema profile, not native provider binding'
    for p in a['content_directories']:
        assert ptr(json.loads(cache[p['source_path']]),p['pointer'])==p['value']
        assert p['scope']=='content directory, not native library path'
    service=a['consumer_service'];assert ptr(json.loads(cache[service['source_path']]),service['pointer'])==service['record']
    assert a['identified_devicekit_provider_images']==[] and a['provider_status']=='unknown; bounded metadata supplies no selected import/load binding'
    assert len(a['consumer_image_frontiers'])==2 and all('consumer' in p['role'] and 'not identified provider' in p['role'] for p in a['consumer_image_frontiers'])
    assert len(a['legacy_helper_context'])==3
    for h in a['legacy_helper_context']:
        prefix='/var/tmp/sound-analysis/helpers/'+h['name']+'/'
        assert h['summary']==json.loads(cache[prefix+'summary.json']) and h['slice']==json.loads(cache[prefix+'slice.json'])
        assert h['source_image']==h['slice']['source'] and h['summary']['executable_sha256']==h['slice']['slice_sha256']
        assert h['index_manifest_program']==json.loads(cache[prefix+'corpus/indexes/manifest.json'])['program']==h['summary']['program']
        assert h['status']=='legacy-helper association only; no DeviceKit provider binding in these selected documents'
    assert len(m['missing_canonically_linked_inputs'])==5 and all(p['exists'] is False for p in m['missing_canonically_linked_inputs'])
    assert m['scope']=='All are unknown; no provider absence or infeasibility conclusion.'
    assert m['proposal_not_selected']['read_now'] is False and m['proposal_not_selected']['maximum_bytes']==65568
    assert q['selected_call_occurrences']==37 and q['unique_external_symbols']==27 and q['lexical_class_families']==7 and q['identified_provider_images']==0
    assert q['selected_retained_rows']==37+7+14+1+9==68<=q['selected_retained_row_cap']==512 and q['candidate_provider_path_cap']==16
    assert q['outcome_or_site_credit']==0 and q['all_required_unsupported_behavior']=='U; coverage remains OPEN'
    assert b['cap_bytes']==READ_CAP and b['binary_bytes_read']==b['source_body_bytes_read']==b['old_helper_imports']==0
    assert b['author_read_bytes']==sum(r['bytes'] for r in b['author_reads'])==sum(p['bytes'] for p in pins)==882628
    assert b['planned_one_checker_pass_source_bytes']==882628
    assert b['total_reserved_bytes']==b['prior_conservative_document_bytes']+2*882628==3642836<=READ_CAP
    assert b['post_pass_locator_check_bytes']==sum(r['bytes'] for r in b['post_pass_locator_check_reads'])==78640
    assert b['final_conservative_document_bytes']==b['total_reserved_bytes']+b['post_pass_locator_check_bytes']==3721476<=READ_CAP

independent_validate(d)
controls=[
 ('external-label-is-provider',lambda x:x['rows'][0].update(actual_provider_path='/imagined/DeviceKit.dylib')),
 ('invented-provider-image',lambda x:x['associations']['identified_devicekit_provider_images'].append('/imagined/DeviceKit.dylib')),
 ('invented-ordinal',lambda x:x['symbols']['symbols'][0].update(macho_library_ordinal=1)),
 ('changed-selected-call',lambda x:x['rows'][0]['selected']['record'].update(site='0x0')),
 ('bad-parent-hash',lambda x:x['rows'][0].update(parent_line_sha256='0'*64)),
 ('omitted-boundary-row',lambda x:x['rows'].pop()),
 ('namespace-to-library',lambda x:x['symbols']['symbols'][0].update(provider_path='ableton::devices')),
 ('content-as-binary',lambda x:x['associations']['content_directories'][0].update(scope='native provider')),
 ('consumer-as-provider',lambda x:x['associations']['consumer_image_frontiers'][0].update(role='actual provider')),
 ('helper-as-devicekit',lambda x:x['associations']['legacy_helper_context'][0].update(status='DeviceKit provider confirmed')),
 ('missing-means-absence',lambda x:x['missing'].update(scope='provider absent')),
 ('execute-unselected-proposal',lambda x:x['missing']['proposal_not_selected'].update(read_now=True)),
 ('inventory-as-grade',lambda x:x['query'].update(outcome_or_site_credit=37)),
 ('close-unsupported-coverage',lambda x:x['query'].update(all_required_unsupported_behavior='complete')),
 ('read-cap-overrun',lambda x:x['budget'].update(total_reserved_bytes=4194305)),
 ('wrong-symbol-stub',lambda x:x['symbols']['symbols'][0].update(stub_addresses=['0x0'])),
 ('bad-list-root-pointer',lambda x:x['associations']['current_device_profiles'][0].update(pointer='/devices/1'))]
negatives=[]
for name,mutate in controls:
    altered=copy.deepcopy(d);mutate(altered)
    try:independent_validate(altered)
    except (AssertionError,KeyError,IndexError,ValueError,TypeError):negatives.append(dict(name=name,rejected=True))
    else:raise AssertionError('negative accepted '+name)
# Verify absence and size using stat only; never open a binary or missing path.
for row in d['missing']['missing_canonically_linked_inputs']:assert not (ROOT/row['path']).exists()
consumer_stats=[]
for row in d['associations']['consumer_image_frontiers']:
    path=Path(row['path']);path=path if path.is_absolute() else ROOT/path
    st=path.stat();assert st.st_size==row['bytes']
    consumer_stats.append(dict(path=str(path),bytes=st.st_size,method='stat-only; no binary open/hash'))
# Final verification rereads only the owned frozen packet.
for row in manifest['files']:
    data=read(PACK/row['path']);assert len(data)==row['bytes'] and sha(data)==row['sha256']
assert read(PACK/'manifest.json')==manifest_bytes
assert {f.name for f in PACK.iterdir() if f.is_file()}=={'manifest.json'}|set(payload)
report=dict(schema='independent-devicekit-provider-inventory-review-v1',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/utility_x86_capture_prep',author='/root/mix_routes',disposition='approved-bounded-retained-metadata-provider-frontier-with-asof-context-qualification',findings=[dict(id='DKP-REVIEW-NOTE-001',severity='nonblocking',topic='Mutable canonical routing context is historical',detail='Current research index differs from author as-of pin after Root adopted Delay29. Other three canonical research pins are exact. Packet manifest/structure explicitly label these as historical context, not future gates. Author check.py main blanket-hashes all34pins and was intentionally not rerun. Independent validation freshly checked the frozen packet and30non-wiki immutablepins, separately qualified four wiki context identities, and used current cached documents only where metadata verification requires them. No frozen rewrite or successor revision required.',identities=drifts)],required_findings=[],manifest=dict(path=str((PACK/'manifest.json').relative_to(ROOT)),bytes=2133,sha256=sha(manifest_bytes)),inventory=dict(payloads=11,payload_bytes=113131,selected_call_occurrences=37,external_names=27,lexical_class_families=7,selected_raw_units=68,exact_frozen_tree_and_payload_hashes=True),source_scope=dict(complete_source_read_before_execution=['structure.md','check.py including main/validate/all15authorcontrols','all authored JSON/JSONL payload data'],execution='Only this independently authored stdlib support script. No author main, pure function, old helper, provider or native module imported/executed.',fresh='34listed metadata documents read once and cached;30non-wiki pins exact,three canonical research pins exact,one historical index pin drift qualified;three complete parent metadata documents re-queried for exact target-only37records/parent byte geometry and grouping.',inherited='Original431MBcall-index bytes/fullhash/locators, parent family complete requirement/case semantics/class associations, original source/package capture methodology, binary hashes and publicbinding unknowns remain inherited; no original index/image/sourcebody replay.'),checks=dict(status='PASS',immutable_nonwiki_pins_exact=30,canonical_context_exact=3,canonical_context_qualified_drift=1,parent_metadata_rows=865,parent_selected_rows_by_family={'filter-eq':22,'dynamics':3,'distortion':12},all37parent_fullrecords_geometry_locators_exact=True,grouping_27external_names_and_all_stub_sets_exact=True,profile_pointers=7,directory_pointers=14,service_pointers=1,list_root_JSON_pointers_verified=True,helper_contexts=3,shallow_helper_documents=9,five_missing_paths_freshly_statted=True,consumer_frontiers=consumer_stats,negative_controls=negatives,author_controls_reproduced=15,additional_independent_controls=2,original_or_provider_calls=0,binary_header_symbol_bind_body_bytes=0),budget=dict(cap_bytes=READ_CAP,author_final_conservative_document_bytes=3721476,author_remaining_bytes=READ_CAP-3721476,author_budget_arithmetic_freshly_verified=True,author_historical_IO_observation='Retained read-budget receipts only; not a historical audit of author system calls.',review_prefight_conservative_payload_bytes=PRIOR_CONSERVATIVE_PAYLOAD_READS,review_driver_document_bytes=sum(x['bytes'] for x in reads),review_total_conservative_document_bytes=PRIOR_CONSERVATIVE_PAYLOAD_READS+sum(x['bytes'] for x in reads),review_driver_read_receipts=reads,all_review_reads_listed_metadata_or_frozen_payloads=True),limits=['No DeviceKit provider image or consumer import/library ordinal/bind/install-name/rpath/provider-body association established.','Names/EXTERNAL labels, seven preset/schema profiles and14contentdirectories do not bind actual native providers or public behavior.','Two consumer paths were stat-only; three helper summary/slice/index-manifests are legacy associations, not an exhaustive package/library inventory or DeviceKit bindings.','Five missing paths are retained-input gaps; no provider absence/infeasibility conclusion.','Proposed65568-byte header/loadcommand acquisition remainsUNSELECTED; no target/header/symbol/bind/rawcode/sourcebody read or decoder/original/model/comparator/harness/fixture/build/network/install.','Independent selected query verifies bounded retained parent documents, not the original431MBsourceindex or prior family semantic audits.'],downstream=dict(actual_provider_bindings=0,new_sites=0,new_grades=0,new_normative_cases_releases=0,required_unsupported='U',coverage='OPEN',whole_product_gate='OPEN',documentary_fallback=False,selected_successor=None),write_scope='Only external independent review JSON and its focused stdlib support script. All frozen/canonical/shared payloads untouched; Root owns adoption and successor selection.')
with OUT.open('x') as stream:json.dump(report,stream,indent=2);stream.write('\n')
b=OUT.read_bytes()
print(json.dumps(dict(status='PASS',review_bytes=len(b),review_sha256=sha(b),report=str(OUT),conservative_review_document_bytes=report['budget']['review_total_conservative_document_bytes'],immutable_nonwiki_pins=30,exact_canonical_context=3,qualified_context_drift=drifts,negative_controls=len(negatives))))
