from pathlib import Path
import json,hashlib,re,datetime,collections
R=Path.cwd();B=R/'analysis/ableton-live-12.4.3/full-spec-v1';P=B/'depth-delay-reverb-source-frontier-v1';assert not P.exists();P.mkdir()
fixed=['101bd6ac4','101bd6b4c','101bd6cd0','101bec250','101bec2ec','101bec394','101bec498','102164918','102164b90','102164d6c','102ad733c','102b2cf14','102b2d090','102e027c0'];wanted={'0x'+x for x in fixed}
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(n,x):
 with (P/n).open('x') as f:json.dump(x,f,indent=2);f.write('\n')
mp=B/'family-delay-reverb-routes-v1/manifest.json';rv=B/'reviews/family-delay-reverb-routes-v1-review.json';assert pin(mp)['sha256']=='3731962df358df06c2c4c763e87b4fd2237a563745f93bf80c40f876a5463498' and pin(rv)['sha256']=='f0fb530aeb26d25ec5917274fbcdb69ea54bc9ae470129f9bbefebd455a58ce7'
selection=dict(schema='root-fixed-fourteen-delay-source-metadata-selection-v1',selected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),authority='User continuous analyst whole-Live execution;amendedrev4 after independently approved familymap.',map=pin(mp),review=pin(rv),entries=sorted(wanted),selection='Exactly14 method nominees from approved structure frontier,not encountered callees. Retained export metadata census only before Root size/scope approval for semantic source reading.',caps=dict(records=14,total_C_utf8_bytes=196608,C_lines_per_record=1500),excluded=['encounteredcallee','newbinary/native','original/harness','slot/global','sourcebodysemanticread','norm/case/grade/release/sitecredit'],unsupported_required='U;coverageOPEN')
save('selection-metadata-only.json',selection)
a=Path('/var/tmp/sound-analysis/corpus/indexes/aliases.jsonl');offset=ordinal=0;found={};metahash=hashlib.sha256()
for line,raw in enumerate(a.open('rb'),1):
 metahash.update(raw);d=json.loads(raw)
 if d['entry'] in wanted:
  assert d['entry'] not in found and not d['external'];found[d['entry']]=dict(alias_record=d,alias_source=dict(path=str(a),line=line,byte=offset,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),chunk_number=ordinal//100)
 if not d['external']:ordinal+=1
 offset+=len(raw)
assert ordinal==418417 and set(found)==wanted and metahash.hexdigest()=='6f05d75085ffb5f74826b4d44f3708fe89466b0b14581e538d912944f8167fcb'
cp=B/'component-resolution-v1/class-inputs.json';pins={x['path']:x for x in json.loads(cp.read_text())['decomp_chunk_pins']};groups=collections.defaultdict(set)
for e,x in found.items():groups[x['chunk_number']].add(e)
records=[];chunkpins=[]
for n,entries in sorted(groups.items()):
 path=Path('/var/tmp/sound-analysis/corpus/decomp/chunks')/f'chunk-{n:05}.jsonl';data=path.read_bytes();p=pins[str(path)];assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256'];chunkpins.append(p);byte=0;seen=set()
 for line,raw in enumerate(data.splitlines(keepends=True),1):
  m=re.search(br'"entry"\s*:\s*"([^\"]+)"',raw[:100]);e=m[1].decode() if m else ''
  if e in entries:
   d=json.loads(raw);code=d.get('code') or '';x=found[e];records.append(dict(entry=e,alias_name=x['alias_record']['name'],alias_thunk=x['alias_record']['thunk'],alias_thunk_target=x['alias_record'].get('thunk_target'),alias_source=x['alias_source'],source_path=str(path),source_line=line,source_byte=byte,raw_bytes=len(raw),raw_sha256=hashlib.sha256(raw).hexdigest(),code_utf8_bytes=len(code.encode()),C_lines=len(code.splitlines()),code_sha256=hashlib.sha256(code.encode()).hexdigest(),native_body_bytes=d['body_bytes'],native_body_ranges=d['body_ranges'],state=d['state'],warnings=d['warnings'],error=d['error'],timed_out=d['timed_out'],partial_code=d['partial_code'],record_thunk=d['thunk']));seen.add(e)
  byte+=len(raw)
 assert seen==entries
records.sort(key=lambda x:int(x['entry'],16));size=sum(x['code_utf8_bytes'] for x in records);maxlines=max(x['C_lines'] for x in records)
r=dict(schema='fixed-fourteen-delay-source-metadata-census-v1',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),selection=pin(P/'selection-metadata-only.json'),records=records,summary=dict(records=len(records),code_utf8_bytes=size,C_lines=sum(x['C_lines'] for x in records),max_C_lines=maxlines,chunks=len(chunkpins),warning_records=sum(bool(x['warnings']) for x in records),within_caps=len(records)==14 and size<=196608 and maxlines<=1500),selected_chunk_pins=chunkpins,metadata_scan=dict(alias_bytes=offset,alias_sha256=metahash.hexdigest(),nonexternal_ordinal=ordinal),read_scope='All aliases are metadata. Only exactselected records parsed in pinned relevant chunks for code lengths/hash/warnings;wholechunk hashing is custody-only,unselected code not printed/retained/semantically reviewed. No C body output or semantics read. No callee/global/native/tool/original/grade.',semantic_source_selection='pending separate Root cap decision')
save('candidate-census.json',r);print(json.dumps(r['summary']));print(json.dumps([dict(entry=x['entry'],name=x['alias_name'],C_bytes=x['code_utf8_bytes'],C_lines=x['C_lines'],warnings=x['warnings']) for x in records],indent=2))
