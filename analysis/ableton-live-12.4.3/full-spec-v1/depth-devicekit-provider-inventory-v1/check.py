#!/usr/bin/env python3
"""Read-only metadata integrity check. No imports of project helpers or native inputs."""
from pathlib import Path
import json, hashlib, collections, copy
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent

def load(name): return json.loads((HERE/name).read_text())
def selected(item):
 r=item.get('record') or {}
 return item.get('kind')=='call' and (r.get('callee_resolved') or '').startswith('EXTERNAL:') and 'ODeviceKitSampleRateProcessor<' in (r.get('callee_resolved_name') or r.get('callee_name') or '')

def validate(d,cache):
 rows=d['rows'];q=d['query'];a=d['associations'];sy=d['symbols'];m=d['missing'];b=d['budget']
 assert len(rows)==37 and len({r['id'] for r in rows})==37
 expected=[]
 for entry in q['input_census']:
  data=cache[entry['path']];offset=0;ks=collections.Counter();count=0
  for i,line in enumerate(data.splitlines(keepends=True)):
   item=json.loads(line);ks[item.get('kind')]+=1
   if selected(item):
    expected.append((entry['path'],i+1,offset,len(line),hashlib.sha256(line).hexdigest(),item));count+=1
   offset+=len(line)
  assert count==entry['selected_rows'] and dict(ks)==entry['kind_counts'] and sum(ks.values())==entry['total_rows']
 assert len(expected)==37
 for r,e in zip(rows,expected):
  assert (r['parent_path'],r['parent_line'],r['parent_byte_offset'],r['parent_line_bytes'],r['parent_line_sha256'],r['selected'])==e
  assert r['parent_index']==r['parent_line']-1 and r['binding_status']=='unknown' and r['actual_provider_path'] is None
  loc=r['selected']['locator'];assert loc.get('path') and loc.get('line',0)>0
  assert (loc.get('sha256') or loc.get('raw_sha256')) and loc.get('bytes',0)>0
 assert collections.Counter(r['family'] for r in rows)=={'filter-eq':22,'dynamics':3,'distortion':12}
 groups=collections.defaultdict(list);classes=collections.Counter()
 for row in rows:
  rr=row['selected']['record'];groups[rr['callee_resolved']].append(row['id']);name=rr.get('callee_resolved_name') or rr['callee_name'];classes[name.split('ODeviceKitSampleRateProcessor<',1)[1].split('>',1)[0]]+=1
 assert len(sy['symbols'])==len(groups)==27 and len(classes)==7 and dict(classes)==sy['class_occurrences']
 for s in sy['symbols']:
  assert s['boundary_rows']==groups[s['external_label']]
  first=next(r for r in rows if r['id']==s['boundary_rows'][0])['selected']['record']
  assert s['lexical_symbol']==(first.get('callee_resolved_name') or first['callee_name'])
  assert s['provider_path'] is None and s['macho_library_ordinal'] is None and s['binding_status']=='unknown'
 prefix='analysis/ableton-live-12.4.3/full-spec-v1/inventory/'
 dev=json.loads(cache[prefix+'devices.json']);dirs=json.loads(cache[prefix+'package-device-directories.json']);svc=json.loads(cache[prefix+'services-platforms.json'])
 assert len(a['current_device_profiles'])==7 and len(a['content_directories'])==14
 for p in a['current_device_profiles']:
  assert p['record']==dev[int(p['pointer'].rsplit('/',1)[1])] and p['scope']=='retained preset/schema profile, not native provider binding'
 for p in a['content_directories']:
  assert p['value']==dirs[int(p['pointer'].rsplit('/',1)[1])] and p['scope']=='content directory, not native library path'
 assert a['consumer_service']['record']==svc['services'][0]
 assert a['identified_devicekit_provider_images']==[] and a['provider_status']=='unknown; bounded metadata supplies no selected import/load binding'
 assert len(a['consumer_image_frontiers'])==2
 for p in a['consumer_image_frontiers']: assert 'consumer' in p['role'] and 'not identified provider' in p['role']
 assert len(a['legacy_helper_context'])==3
 for h in a['legacy_helper_context']:
  base='/var/tmp/sound-analysis/helpers/'+h['name']+'/'
  assert h['summary']==json.loads(cache[base+'summary.json']) and h['slice']==json.loads(cache[base+'slice.json'])
  assert h['source_image']==h['slice']['source'] and h['index_manifest_program']==json.loads(cache[base+'corpus/indexes/manifest.json'])['program']
  assert h['status']=='legacy-helper association only; no DeviceKit provider binding in these selected documents'
 assert len(m['missing_canonically_linked_inputs'])==5 and all(not p['exists'] for p in m['missing_canonically_linked_inputs'])
 assert m['scope']=='All are unknown; no provider absence or infeasibility conclusion.'
 proposal=m['proposal_not_selected'];assert proposal['read_now'] is False and proposal['maximum_bytes']==65568
 assert q['selected_call_occurrences']==37 and q['unique_external_symbols']==27 and q['lexical_class_families']==7
 assert q['identified_provider_images']==0 and q['candidate_provider_path_cap']==16
 assert q['selected_retained_rows']==68 and q['selected_retained_row_cap']==512
 assert q['outcome_or_site_credit']==0 and q['all_required_unsupported_behavior']=='U; coverage remains OPEN'
 assert b['cap_bytes']==4194304 and b['binary_bytes_read']==b['source_body_bytes_read']==b['old_helper_imports']==0
 assert b['author_read_bytes']==sum(x['bytes'] for x in b['author_reads'])==sum(len(x) for x in cache.values())
 assert b['planned_one_checker_pass_source_bytes']==b['author_read_bytes']
 assert b['total_reserved_bytes']==b['prior_conservative_document_bytes']+2*b['author_read_bytes']<=b['cap_bytes']

def main():
 pins=load('pins.json')['pins'];cache={}
 for p in pins:
  assert p['path'] not in cache
  path=Path(p['path']);path=path if path.is_absolute() else ROOT/path
  data=path.read_bytes();assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256'],p['path'];cache[p['path']]=data
 d=dict(rows=[json.loads(x) for x in (HERE/'boundary-rows.jsonl').read_text().splitlines()],query=load('query-census.json'),associations=load('package-associations.json'),symbols=load('symbols.json'),missing=load('missing-frontier.json'),budget=load('read-budget.json'))
 validate(d,cache)
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
 ('read-cap-overrun',lambda x:x['budget'].update(total_reserved_bytes=4194305))]
 negatives=[]
 for name,mutate in controls:
  changed=copy.deepcopy(d);mutate(changed)
  try:validate(changed,cache)
  except (AssertionError,KeyError,IndexError):negatives.append(dict(name=name,rejected=True))
  else:raise AssertionError('negative control passed: '+name)
 meta_paths=[p for p in cache if '/r2/' in p and p.endswith('.json')]+[p for p in cache if p.startswith('/var/tmp/')]
 exact_doc_queries=[dict(path=p,query='literal DeviceKit occurrence in this shallow retained document',matches=cache[p].count(b'DeviceKit'),interpretation='bounded lexical query only; zero is not provider absence') for p in meta_paths]
 print(json.dumps(dict(status='PASS',pin_count=len(pins),verified_metadata_bytes=sum(len(x) for x in cache.values()),reserved_total_document_bytes=d['budget']['total_reserved_bytes'],call_occurrences=37,unique_external_symbols=27,lexical_class_families=7,selected_raw_units=68,identified_provider_images=0,negative_controls=negatives,shallow_document_exact_queries=exact_doc_queries,original_or_provider_execution=0,binary_reads=0,scope='data-only; original source-index locators/full hash inherited, no original index/image/body reads; unsupported behavior U and coverage OPEN'),indent=2))
if __name__=='__main__':main()
