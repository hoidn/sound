"""Retained-index DATA census; no target/source function or provider execution."""
from pathlib import Path
from collections import Counter
import datetime,hashlib,json,sys
INDEX=Path('/var/tmp/sound-analysis/corpus/indexes')
OUT=Path(__file__).resolve().parent

def identity(path):
 h=hashlib.sha256();n=0
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return dict(path=str(path),bytes=n,sha256=h.hexdigest())

def rows(path):
 with path.open('rb') as f:
  line=0
  while True:
   offset=f.tell();raw=f.readline()
   if not raw:break
   line+=1;yield json.loads(raw),dict(path=str(path),line=line,byte_offset=offset,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest())

def census(source,functions):
 kinds=Counter();flows=Counter();nonempty=Counter();ref_types=Counter();availability=Counter();sources=set();sites=set();pairs=set();dups=0;refs=0;function_sites=Counter();examples={};target_functions=set();targets=set()
 for x,where in source:
  assert isinstance(x['resolved_targets'],list) and x['kind'] in ('call','jump')
  key=x['site'];dups+=key in sites;sites.add(key);pairs.add((x['function'],key));sources.add(x['function']);kinds[x['kind']]+=1;flows[x['flow']]+=1
  targets_here=x['resolved_targets'];nonempty[x['kind']]+=bool(targets_here)
  if any(t.get('function') is not None for t in targets_here):function_sites[x['kind']]+=1
  typ=x['kind']+('/nonempty' if targets_here else '/empty')
  if typ not in examples:examples[typ]=dict(locator=where,record=x)
  for t in targets_here:
   refs+=1;ref_types[t['ref_type']]+=1;targets.add(t['to']);tf=t.get('function')
   availability['function_field_present' if tf is not None else 'function_field_null']+=1
   availability['target_to_exact_function_entry' if t['to'] in functions else 'target_to_not_exact_function_entry']+=1
   if tf is not None:
    target_functions.add(tf);availability['function_field_in_alias_index' if tf in functions else 'function_field_missing_alias_entry']+=1
    if tf in functions:availability['function_field_external' if functions[tf] else 'function_field_internal']+=1
    availability['function_field_equals_to' if tf==t['to'] else 'function_field_differs_from_to']+=1
 return dict(rows=sum(kinds.values()),kinds=dict(kinds),flows=dict(flows),source_functions=len(sources),source_function_alias_available=sum(f in functions for f in sources),unique_sites=len(sites),unique_function_sites=len(pairs),duplicate_site_rows=dups,nonempty_target_sites_by_kind=dict(nonempty),nonempty_target_sites=sum(nonempty.values()),sites_with_function_field_target_by_kind=dict(function_sites),sites_with_function_field_target=sum(function_sites.values()),target_references=refs,unique_target_addresses=len(targets),unique_function_field_addresses=len(target_functions),reference_types=dict(ref_types),target_availability=dict(availability),examples=examples)

def selfcheck():
 def row(site,kind,ts):return dict(site=site,function='f',kind=kind,flow='COMPUTED_CALL' if kind=='call' else 'COMPUTED_JUMP',resolved_targets=ts)
 tf=dict(to='g',function='g',ref_type='COMPUTED_CALL');jump=dict(to='inside',function=None,ref_type='COMPUTED_JUMP')
 r=census([(row('a','call',[tf]),{}),(row('b','jump',[jump]),{}),(row('c','call',[]),{}),(row('c','call',[]),{})],{'f':False,'g':False})
 assert(r['rows'],r['unique_sites'],r['duplicate_site_rows'],r['nonempty_target_sites'],r['sites_with_function_field_target'])==(4,3,1,2,1)
 assert r['target_availability']['target_to_exact_function_entry']==1 and r['target_availability']['function_field_null']==1
 assert census([],{} )['rows']==0
 return dict(assertions='call/jump distinction, duplicate site, null-function interior target, alias membership, empty population',passed=True)

def main():
 if sys.argv[1:]!=['--derive']:raise SystemExit('Read-only retained data --derive only; no provider/runtime.')
 checks=selfcheck();files=[INDEX/'manifest.json',INDEX/'aliases.jsonl',INDEX/'indirect.jsonl'];before=[identity(p) for p in files];manifest=json.loads(files[0].read_text())
 for p,g in zip(files[1:],before[1:]):
  expected=manifest['files'][p.name];assert(g['bytes'],g['sha256'])==(expected['bytes'],expected['sha256'])
 functions={};alias_rows=0;alias_dups=0
 for x,_ in rows(INDEX/'aliases.jsonl'):
  alias_rows+=1;alias_dups+=x['entry'] in functions;functions[x['entry']]=x['external']
 result=census(rows(INDEX/'indirect.jsonl'),functions)
 assert result['rows']==manifest['files']['indirect.jsonl']['lines']
 assert before==[identity(p) for p in files]
 out=dict(schema='retained-indirect-index-census-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),program=manifest['program'],executable_sha256=manifest['executable_sha256'],source_index='c1-live-v1 retained /var/tmp projection',sources=before,alias_index=dict(rows=alias_rows,unique_entries=len(functions),duplicate_entry_rows=alias_dups,external_entries=sum(functions.values())),census=result,interpretation=['268015 denominator includes computed jump sites; it is not a virtual-call count.','Nonempty exported target references are an inventory baseline, not class dispatch/runtime/order/coverage proof.','Null target.function often accompanies interior jump destinations; exact alias-entry availability is reported separately.','Alias index membership is retained function metadata, not a claim that the complete target C body exists or has been reviewed.'],selfcheck=checks,preservation=dict(watched=len(files),unchanged=True),original_or_provider_execution=False)
 p=OUT/'indirect-baseline.json';p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(output=identity(p),census=result,alias_index=out['alias_index']),indent=2))
if __name__=='__main__':main()
