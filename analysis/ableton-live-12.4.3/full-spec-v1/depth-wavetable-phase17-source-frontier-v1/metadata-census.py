from pathlib import Path
import json,hashlib,re,datetime,collections
import sys

def guard_selection(s):
 assert s['stage']=='SELECTED-retained-export-metadata-only'
 entries=s['entries'];assert len(entries)==len(set(entries))==17 and entries==sorted(entries,key=lambda x:int(x,16))
 assert all(re.fullmatch(r'0x[0-9a-f]+',x) for x in entries)
 assert len(s['parents'])==8 and {a['target'] for p in s['parents'] for a in p['anchors']}==set(entries)
 assert s['proposed_source_caps']==dict(records=17,C_bytes=1048576,C_lines=30000)
 assert s['semantic_source_selection'].startswith('PENDING')

def guard_code(r):
 c=r.get('code');assert c is None or isinstance(c,str)
 return c or ''

def selfcheck():
 import copy
 s=json.loads((Path(__file__).resolve().parent.parent/'reviews/wavetable-phase17-root-metadata-selection.json').read_text());guard_selection(s)
 assert len(guard_code(dict(code='λ\nx')).encode())==4 and len(guard_code(dict(code='λ\nx')).splitlines())==2 and guard_code(dict(code=None))==''
 controls=[]
 for label,fn in [('drop',lambda q:q['entries'].pop()),('duplicate',lambda q:q['entries'].__setitem__(1,q['entries'][0])),('order',lambda q:q['entries'].reverse()),('lost-parent',lambda q:q['parents'].pop()),('source-promote',lambda q:q.update(semantic_source_selection='SELECTED')),('caps',lambda q:q['proposed_source_caps'].update(records=18))]:
  q=copy.deepcopy(s);fn(q)
  try:guard_selection(q)
  except AssertionError:controls.append(label)
  else:raise AssertionError(label+' accepted')
 for value in [[],{},1,False,b'C']:
  try:guard_code(dict(code=value))
  except AssertionError:controls.append('nontext-'+type(value).__name__)
  else:raise AssertionError('nontext accepted')
 print(json.dumps(dict(status='PASS',negative_controls=controls,negative_count=len(controls),positive_assertions=4,original_reads=0)))

def census():
 R=Path.cwd();B=R/'analysis/ableton-live-12.4.3/full-spec-v1';V=B/'reviews';P=B/'depth-wavetable-phase17-source-frontier-v1'
 selection_path=V/'wavetable-phase17-root-metadata-selection.json'
 selection=json.loads(selection_path.read_text());assert selection['stage']=='SELECTED-retained-export-metadata-only'
 review_path=Path(selection['actual_review']['path']);rawreview=review_path.read_bytes();assert hashlib.sha256(rawreview).hexdigest()==selection['actual_review']['sha256']
 assert not (P/'candidate-census.json').exists();wanted=set(selection['entries']);guard_selection(selection)

 def save(n,d):
  with (P/n).open('x') as f:json.dump(d,f,indent=2);f.write('\n')

 def pin(p):
  b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 save('selection-metadata-only.json',selection)
 a=Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl');offset=ordinal=0;found={};digest=hashlib.sha256()
 for line,raw in enumerate(a.open('rb'),1):
  digest.update(raw);d=json.loads(raw)
  if d['entry'] in wanted:
   assert d['entry'] not in found and not d['external'];found[d['entry']]=dict(alias_record=d,alias_source=dict(path=str(a),line=line,byte=offset,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),chunk_number=ordinal//100)
  if not d['external']:ordinal+=1
  offset+=len(raw)
 assert ordinal==418417 and digest.hexdigest()=='6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb'
 missing=sorted(wanted-set(found));groups=collections.defaultdict(set)
 for e,x in found.items():groups[x['chunk_number']].add(e)
 pins={x['path']:x for x in json.loads((B/'component-resolution-v1/class-inputs.json').read_text())['decomp_chunk_pins']};records=[];chunkpins=[]
 for n,entries in sorted(groups.items()):
  p=Path('/var/tmp/sound-analysis/corpus/decomp/chunks')/f'chunk-{n:05}.jsonl';data=p.read_bytes();fixed=pins[str(p)];assert len(data)==fixed['bytes'] and hashlib.sha256(data).hexdigest()==fixed['sha256'];chunkpins.append(fixed);byte=0;seen=set()
  for line,raw in enumerate(data.splitlines(keepends=True),1):
   match=re.search(br'"entry"\s*:\s*"([^\"]+)"',raw[:100]);e=match[1].decode() if match else ''
   if e in entries:
    d=json.loads(raw);assert d['entry']==e;code=guard_code(d);x=found[e];records.append(dict(entry=e,alias_name=x['alias_record']['name'],alias_thunk=x['alias_record']['thunk'],alias_thunk_target=x['alias_record'].get('thunk_target'),alias_source=x['alias_source'],source_path=str(p),source_line=line,source_byte=byte,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),code_utf8_bytes=len(code.encode()),C_lines=len(code.splitlines()),code_sha256=hashlib.sha256(code.encode()).hexdigest(),native_body_bytes=d['body_bytes'],native_body_ranges=d['body_ranges'],state=d['state'],warnings=d['warnings'],error=d['error'],timed_out=d['timed_out'],partial_code=d['partial_code'],record_thunk=d['thunk']));seen.add(e)
   byte+=len(raw)
  assert seen==entries
 records.sort(key=lambda x:int(x['entry'],16));size=sum(x['code_utf8_bytes'] for x in records);maxlines=max((x['C_lines'] for x in records),default=0)
 summary=dict(selected_values=17,records_found=len(records),missing_values=missing,code_utf8_bytes=size,C_lines=sum(x['C_lines'] for x in records),max_C_lines=maxlines,chunks=len(chunkpins),warning_records=sum(bool(x['warnings']) for x in records),within_proposed_source_caps=len(records)==17 and size<=1048576 and sum(x['C_lines'] for x in records)<=30000)
 result=dict(schema='root-whole17-wavetable-phase-helper-export-metadata-census-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selection=pin(selection_path),records=records,summary=summary,selected_chunk_pins=chunkpins,metadata_scan=dict(alias_bytes=offset,alias_sha256=digest.hexdigest(),nonexternal_ordinal=ordinal),read_scope='Exact17lexicaltargets metadata lookup only;selected C strings measured/hashed but not semantically read/printed/retained. Full relevantchunk hash custody only,unselectedC not parsed. No originalimage/native/provider/stub/n_value-memory/callee/bodysemanticfollow.',semantic_source_selection='pending separate Root coherent size/scope decision',required_unsupported='U;coverageOPEN')
 save('candidate-census.json',result);print(json.dumps(summary));print(json.dumps([dict(entry=x['entry'],name=x['alias_name'],C_bytes=x['code_utf8_bytes'],C_lines=x['C_lines'],native_body_bytes=x['native_body_bytes'],warnings=x['warnings']) for x in records],indent=2))

if __name__=='__main__':
 if sys.argv[1:]==['--check']:selfcheck()
 elif sys.argv[1:]==['--census']:census()
 else:raise SystemExit('usage: metadata-census.py --check | --census')
