#!/usr/bin/env python3
"""Owned wording/mapping checker. Reads staged data, canonical owner and Root review ONLY."""
import copy,hashlib,json,pathlib,re,sys
H=pathlib.Path(__file__).resolve().parent
ROOT=H.parents[3]
def load(n):return json.loads((H/n).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def requirement_hashes(text):
 out=[]
 for m in re.finditer(r'^### (REQ-LIVE-SET-STRUCTURE-\d{3})[^\n]*\n',text,re.M):
  end=text.find('\n### ',m.end());end=end if end!=-1 else text.index('\n## T1 limits',m.end());b=text[m.start():end].encode();out.append({'id':m[1],'bytes':len(b),'sha256':sha(b)})
 return out

def old_rows(text):return [{'id':l.split('|')[1].strip(),'bytes':len(l.encode()),'sha256':sha(l.encode())} for l in text.splitlines(keepends=True) if re.match(r'^\| LSS-\d{3} \|',l)]
def compose(text,delta,fragments):
 for op in delta['operations']:
  if op['kind']=='replace-once':
   assert text.count(op['before'])==1;text=text.replace(op['before'],op['after'],1)
  else:
   assert op['kind']=='insert-before-once' and text.count(op['anchor'])==1
   s=fragments[op['fragment']]+('\n' if op.get('trailing_newline') else '');text=text.replace(op['anchor'],s+op['anchor'],1)
 return text

def reverse(text,delta,fragments):
 for op in reversed(delta['operations']):
  if op['kind']=='replace-once':
   assert text.count(op['after'])==1;text=text.replace(op['after'],op['before'],1)
  else:
   s=fragments[op['fragment']]+('\n' if op.get('trailing_newline') else '');assert text.count(s+op['anchor'])==1;text=text.replace(s+op['anchor'],op['anchor'],1)
 return text

def pointer(obj,p):
 assert p.startswith('/')
 for item in p[1:].split('/'):
  k=item.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
 return obj

def polynomial(b):
 x=b<<16
 for bit in range(23,15,-1):
  if x&(1<<bit):x^=0x18005<<(bit-16)
 return x

def basic_catalog(cat,cases):
 assert len(cat)==256 and [r['byte'] for r in cat]==list(range(256)) and len(cases)==253
 fresh=[r for r in cat if r['byte'] not in (0,183,255)];old=[r for r in cat if r['byte'] in (0,183,255)]
 assert [r['draft_id'] for r in fresh]==[f'LSS-CRC-{i:03d}' for i in range(1,254)]
 assert all(r['draft_id'] is None and r['historical'] is not None and r['historical']['pid'] is None and r['historical']['raw_receipt'] is None for r in old)
 for r in cat:
  assert r['payload_hex']==f'{r["byte"]:02x}' and r['input_sha256']==sha(bytes([r['byte']])) and r['length']==1 and r['initial_seed_le']=='00000000'
  assert r['requirement']=='REQ-LIVE-SET-STRUCTURE-008' and r['native_x86_expected_crc16']==polynomial(r['byte']) and r['native_x86_expected_crc16_hex']==f'{polynomial(r["byte"]):04x}'
  assert r['expected_full32'] is None and r['portable_expected'] is None and r['portable_comparator'] is None
 for r,c in zip(fresh,cases):
  assert c['id']==r['draft_id'] and c['requirement']==r['requirement'] and c['scope']=='local-initial0-one-byte-CRC16-memory'
  assert c['input']=={k:r[k] for k in ('byte','payload_hex','input_sha256','length','initial_seed_le')}
  assert c['expected']=={'native_x86_crc16':r['native_x86_expected_crc16'],'native_x86_crc16_hex':r['native_x86_expected_crc16_hex'],'expected_full32':None,'portable_expected':None,'portable_comparator':None}
  assert c['grade'] is None and c['release'] is None and c['approved_review_join']==r['approved_review_join']

def preserve(base,after,before):
 assert sha(base.encode())==before['owner']['sha256'] and len(base.encode())==before['owner']['bytes']
 required=[{k:r[k] for k in ('id','bytes','sha256')} for r in before['requirements']]
 assert len(required)==18 and requirement_hashes(base)==requirement_hashes(after)==required
 assert old_rows(base)==old_rows(after)==before['canonical_case_rows'] and len(old_rows(after))==40
 assert before['released_case_count']==len(before['released_case_object_hashes'])==34
 assert len({r['id'] for r in before['released_case_object_hashes']})==34
 # Release inventory is inherited immutable metadata; never reopen/replay fixtures or cases.
 assert next(x for x in before['release_inventory_inherited_pins'] if x['path']=='cases.json')['sha256']==before['released_cases_file']['sha256']
 assert 'revision: 3\n' in after and 'updated: 2026-10-21\n' in after

def approved_joins(cat,cases,review,pin):
 assert review['disposition']==pin['required_disposition']=='APPROVED_253_FRESH_CRC16_AGREEMENTS_AND_3_INHERITED_SUMMARY_JOINS'
 assert not review['blocking_findings'] and not review['required_corrections']
 assert review['frozen_packet']['manifest']==pin['batch_manifest']
 points=review['approved_summary']['approved_points'];assert len(points)==256
 assert review['approved_summary']['portable_expected'] is None and review['approved_summary']['portable_comparator'] is None
 fields=pin['observation_fields'];bycase={c['id']:c for c in cases}
 for r,q in zip(cat,points):
  b=r['byte'];j=r['approved_review_join'];assert j['report_sha256']==pin['report']['sha256'] and j['point_pointer']==f'/approved_summary/approved_points/{b}'
  assert pointer(review,j['point_pointer'])==q and j['point_canonical_sha256']==sha(json.dumps(q,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
  assert q['byte']==b and q['id']==f'CRC-{b:02x}' and q['payload_hex']==r['payload_hex'] and q['input_sha256']==r['input_sha256'] and q['entry']=='0x101191310' and q['length']==1 and q['initial_seed_bytes_le']=='00000000'
  assert q['agrees'] and q['expected_low16']==q['observed_low16']==r['native_x86_expected_crc16'] and q['expected_low16_hex']==r['native_x86_expected_crc16_hex']
  assert q['expected_full32'] is None and q['portable_comparator'] is None
  assert r['observation_provenance']=={k:q[k] for k in fields if k in q}
  if b in (0,183,255):
   assert r['draft_id'] is None and r['provenance']=='inherited-summary-no-new-id' and r['historical']==q['historical']
   assert q['pid'] is None and q['utc_start'] is None and q['utc_end'] is None and q['observed_full32'] is None and q['output4_hex'] is None and q['carriers64'] is None
  else:
   assert r['provenance']=='fresh-approved-review' and r['historical'] is None and q['pid']>0 and q['provenance']=='fresh-once-only-original-call'
   assert bycase[r['draft_id']]['approved_review_join']==j
 # No raw/source/receipts followed: exact review summaries are inherited facts, not fresh actual validation.

def negative_controls(cat,cases,review,pin,base,after,before):
 out=[]
 def check(label,mut):
  x,y,z=copy.deepcopy(cat),copy.deepcopy(cases),copy.deepcopy(review);mut(x,y,z)
  try:basic_catalog(x,y);approved_joins(x,y,z,pin)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(label);return
  raise AssertionError('negative accepted '+label)
 tests=[('missing-byte',lambda x,y,z:x.pop()),('duplicate-id',lambda x,y,z:x[2].update(draft_id=x[1]['draft_id'])),('historical-new-id',lambda x,y,z:x[0].update(draft_id='LSS-CRC-999')),('invented-old-pid',lambda x,y,z:x[0]['historical'].update(pid=123)),('nonzero-seed',lambda x,y,z:x[1].update(initial_seed_le='01000000')),('wrong-length',lambda x,y,z:x[1].update(length=2)),('wrong-byte-input',lambda x,y,z:x[1].update(payload_hex='02')),('changed-rule',lambda x,y,z:x[1].update(native_x86_expected_crc16=0)),('fullword-as-criterion',lambda x,y,z:x[1].update(expected_full32=98309)),('portable-comparator',lambda x,y,z:x[1].update(portable_comparator='exact')),('portable-expected',lambda x,y,z:x[1].update(portable_expected=32773)),('case-input-mismatch',lambda x,y,z:y[0]['input'].update(byte=2)),('case-expectation-mismatch',lambda x,y,z:y[0]['expected'].update(native_x86_crc16=0)),('missing-fresh-case',lambda x,y,z:y.pop()),('case-grade-invented',lambda x,y,z:y[0].update(grade='X')),('point-wrong-byte',lambda x,y,z:x[1]['approved_review_join'].update(point_pointer='/approved_summary/approved_points/2')),('point-hash',lambda x,y,z:x[1]['approved_review_join'].update(point_canonical_sha256='0'*64)),('receipt-mismatch',lambda x,y,z:x[1]['observation_provenance'].update(receipt_pointer='results.json#/children/1/parsed/calls/0')),('carrier-mismatch',lambda x,y,z:x[1]['observation_provenance']['carriers64'].update(rax='0'*16)),('unapproved-review',lambda x,y,z:z.update(disposition='PENDING'))]
 for t in tests:check(*t)
 for label,altered in [('prior-requirement-edit',after.replace('### REQ-LIVE-SET-STRUCTURE-001 — reading model','### REQ-LIVE-SET-STRUCTURE-001 — changed model',1)),('prior-case-edit',after.replace('| LSS-001 |','| LSS-099 |',1))]:
  try:preserve(base,altered,before)
  except AssertionError:out.append(label)
  else:raise AssertionError('prior preservation accepted '+label)
 return out

def main():
 assert sys.argv[1:]==['--check'];before=load('owner-before.json');delta=load('delta.json');pin=load('review-pin.json');fragments={n:(H/n).read_text() for n in ('annex.md','revision-row.md')}
 canonical=ROOT/'wiki/specs/live-set-structure.md';assert str(canonical)==before['owner']['path'];text=canonical.read_text()
 composition=load('composition.json')
 if sha(text.encode())==before['owner']['sha256']:base=text;after=compose(base,delta,fragments)
 else:
  assert sha(text.encode())==composition['owner_after_sha256'];after=text;base=reverse(after,delta,fragments)
 assert compose(base,delta,fragments)==after and reverse(after,delta,fragments)==base
 preserve(base,after,before);assert len(after.encode())==composition['owner_after_bytes'] and sha(after.encode())==composition['owner_after_sha256']
 assert delta['base_sha256']==before['owner']['sha256'] and delta['owner_path']=='wiki/specs/live-set-structure.md'
 assert len(delta['operations'])==4 and [op['kind'] for op in delta['operations']]==['replace-once','replace-once','insert-before-once','insert-before-once']
 assert [op.get('fragment') for op in delta['operations'][2:]]==['annex.md','revision-row.md']
 p=pathlib.Path(pin['report']['path']);assert p==ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/reviews/structure-crc-one-byte-v1-review.json'
 raw=p.read_bytes();assert len(raw)==pin['report']['bytes'] and sha(raw)==pin['report']['sha256'];review=json.loads(raw)
 cat=load('catalog.json');cases=load('new-cases.json');basic_catalog(cat,cases);approved_joins(cat,cases,review,pin);controls=negative_controls(cat,cases,review,pin,base,after,before)
 report={'status':'PASS','requirements_exact':18,'old_canonical_rows_exact':40,'released_case_object_hashes_preserved':34,'logical':256,'fresh_ids':253,'historical_no_ids':3,'portable_comparators_null':256,'negative_controls':controls,'canonical_writes':0,'actual_source_raw_or_tool_reads':0,'original_calls':0,'review_summary_only':True,'composed_owner_bytes':len(after.encode()),'composed_owner_sha256':sha(after.encode())}
 if (H/'manifest.json').exists():
  m=load('manifest.json');assert {p.relative_to(H).as_posix() for p in H.rglob('*') if p.is_file()}=={'manifest.json'}|{f['path'] for f in m['files']}
  for f in m['files']:
   b=(H/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
  assert load('author-check.json')==report
 else:
  with (H/'author-check.json').open('w') as f:json.dump(report,f,indent=2);f.write('\n')
 print(json.dumps(report))
if __name__=='__main__':main()
