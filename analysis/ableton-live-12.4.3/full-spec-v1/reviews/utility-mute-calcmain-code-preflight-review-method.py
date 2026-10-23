from pathlib import Path
import ast,copy,datetime,hashlib,json
R=Path('/home/ollie/Documents/sound');B=R/'analysis/ableton-live-12.4.3/full-spec-v1';P=B/'depth-utility-mute-calcmain-instruction-preparation'
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);n+=len(x)
 return dict(path=str(p),bytes=n,sha256=h.hexdigest())
plan=json.loads((P/'plan.json').read_text());delta=json.loads((P/'source-delta.json').read_text());manifest=json.loads((P/'manifest-preparation.json').read_text())
paths=sorted({Path(x['path']) for x in [plan['image'],plan['tool'],*plan['providers']]}|{p for p in P.iterdir() if p.is_file()})
before=[pin(p) for p in paths]
assert pin(P/'manifest-preparation.json')['sha256']=='d2cd8aa315205abc0770875ae5ddd1b6cb99bff17e23bab6df11314bc884eafb'
for v in [plan['image'],plan['tool'],*plan['providers']]:assert pin(Path(v['path']))==v
assert {v['path'] for v in manifest['files']}=={p.name for p in P.iterdir() if p.is_file() and p.name!='manifest-preparation.json'}
for v in manifest['files']:
 a=pin(P/v['path']);assert (a['bytes'],a['sha256'])==(v['bytes'],v['sha256'])
for v in delta['old_parent_files']:assert pin(Path(v['path']))==v
text=(P/'extract-decode-once.py').read_text();checker=(P/'check.py').read_text()
for current,key,parent in [(text,'literal_operations',Path(delta['before']['path'])),(checker,'checker_literal_operations',Path(delta['before']['path']).with_name('check.py'))]:
 restored=current
 for op in reversed(delta[key]):assert restored.count(op['after'])==op['occurrences'];restored=restored.replace(op['after'],op['before'])
 assert restored==parent.read_text()
assert len(delta['literal_operations'])==11 and len(delta['checker_literal_operations'])==23
start=0x1021658b0;length=72;end=0x1021658f8
assert end-start==length and plan['helper']['file_offset']==start-plan['expected_segment']['vmaddr']+plan['expected_segment']['fileoff']==35018928
segment=plan['expected_segment'];assert segment['vmaddr']<=start and end<=segment['vmaddr']+min(segment['vmsize'],segment['filesize'])
header=json.loads((P/'header-map.json').read_text());assert header['selected_segment']==segment and header['header_hex']==plan['image_header_hex'] and header['load_commands_sha256']==plan['load_commands_sha256']
anchor=plan['source_anchor'];provider=json.loads(Path(anchor['provider']['path']).read_text());assert pin(Path(anchor['provider']['path']))==anchor['provider']
a=provider['full_selected_records'][1];assert a['path']==anchor['source_provider'] and a['line_1based']==anchor['line_1based'] and a['raw_sha256_excluding_LF']==anchor['raw_sha256']
assert {k:v for k,v in a['record'].items() if k!='code'}==anchor['metadata']
raw=Path(a['path']).read_bytes().splitlines()[a['line_1based']-1];assert hashlib.sha256(raw).hexdigest()==anchor['raw_sha256'];assert json.loads(raw)==a['record']
tree=ast.parse(text);preds=[n.test for n in ast.walk(tree) if isinstance(n,ast.Assert) and ast.unparse(n.test).startswith('len(decoded)')];assert len(preds)==1
expr=compile(ast.Expression(preds[0]),'<reviewer synthetic-only row assertion>','eval')
# Only the source assertion is evaluated, with analyst-owned zero rows. No source functions/module/import/main.
def accepts(rows,n):
 try:
  ok=eval(expr,{'__builtins__':{},'len':len,'all':all,'enumerate':enumerate,'bytes':bytes,'str':str,'isinstance':isinstance,'START':start},{'decoded':rows})
  return bool(ok) and b''.join(bytes.fromhex(x['bytes']) for x in rows)==b'\0'*n
 except (ValueError,TypeError,KeyError):return False
base=[dict(offset=start+4*i,size=4,type='mov',opcode='synthetic valid',bytes='00000000') for i in range(18)]
results=[]
for case in json.loads((P/'guard-fixtures.json').read_text())['cases']:
 rows=copy.deepcopy(base);change=case['change']
 if 'row0' in change:rows[0].update(change['row0'])
 if 'allrows' in change:
  for row in rows:row.update(change['allrows'])
 if 'row0_remove' in change:rows[0].pop(change['row0_remove'])
 if 'row0_offset_delta' in change:rows[0]['offset']+=change['row0_offset_delta']
 if 'row_count' in change:
  c=change['row_count'];rows=rows[:c] if c<18 else rows+[dict(base[-1],offset=end)]
 if 'cancel3_5' in change:rows[0]['bytes']='000000';rows[1]['bytes']='0000000000'
 got=accepts(rows,72);assert got is case['expected_accept'];results.append(dict(label=case['label'],accepted=got))
for i in range(18):
 rows=copy.deepcopy(base);rows[i]['size']=0;assert not accepts(rows,72)
rows=copy.deepcopy(base);rows[0]['bytes']='00000001';assert not accepts(rows,72)
assert start+72<=end and not start+76<=end
calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess'];assert len(calls)==1 and calls[0].func.attr=='Popen'
assert "if DEST.exists():" in text and "child.communicate(timeout=30)" in text
assert text.index("save('invocation-before.json'")<text.index("state['tool_attempts']=1")<text.index('child=subprocess.Popen')<text.index("state['tool_returned_pid']=child.pid")
assert text.index("save('before-map.json'")<text.index('f.seek(offset)')
assert "START+LENGTH<=int(plan['helper']['body_end_exclusive'],16)" in text and "int(plan['helper']['body_end_exclusive'],16)>=START+72" in checker
assert not P.with_name('depth-utility-mute-calcmain-instruction-data').exists()
after=[pin(p) for p in paths];assert before==after
out=B/'reviews/utility-mute-calcmain-code-preflight-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mode='OWN stdlib metadata/opaque hashing/AST isolated synthetic row expression ONLY',manifest=pin(P/'manifest-preparation.json'),watch=before,unchanged=before==after,watch_count=len(paths),providers=len(plan['providers']),collector_inverse_operations=11,checker_inverse_operations=23,parent_files=len(delta['old_parent_files']),source_anchor_metadata_and_rawrow_exact=True,mapping='Plan/header-map metadata and arithmetic only; no fresh header or selected image window read. Full image identity opaque hashing only.',fixtures=results,extra_each_row_wrong_size_rejections=18,extra_wrongconcat_rejection=True,containment_controls=[dict(length=72,accepted=True),dict(length=76,accepted=False)],supplied_checker_or_collector_run=False,decoder_or_original_run=False,all38Utility='U/unexecuted'),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watched=len(paths),fixture_passes=len(results),positive=sum(v['accepted'] for v in results))))
