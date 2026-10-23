from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-mute-core-prefix-instruction-preparation'
def pin(p):
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x);size+=len(x)
 return dict(path=str(p),bytes=size,sha256=h.hexdigest())
plan=json.loads((P/'plan.json').read_text());delta=json.loads((P/'source-delta.json').read_text());manifest=json.loads((P/'manifest-preparation.json').read_text())
paths=sorted({Path(x['path']) for x in [plan['image'],plan['tool'],*plan['providers']]}|{x for x in P.iterdir() if x.is_file()});before=[pin(x) for x in paths]
assert pin(P/'manifest-preparation.json')['sha256']=='69393610d01e0035f0a4b1d13a56009e11d7c1b45dd42c2133f1f5bf245a410b'
for x in [plan['image'],plan['tool'],*plan['providers']]:assert pin(Path(x['path']))==x
assert {x['path'] for x in manifest['files']}=={x.name for x in P.iterdir() if x.is_file() and x.name!='manifest-preparation.json'}
for x in manifest['files']:
 a=pin(P/x['path']);assert(a['bytes'],a['sha256'])==(x['bytes'],x['sha256'])
text=(P/'extract-decode-once.py').read_text();checker=(P/'check.py').read_text()
for current,key,parent in [(text,'literal_operations',Path(delta['before']['path'])),(checker,'checker_literal_operations',Path(delta['before']['path']).with_name('check.py'))]:
 restored=current
 for op in reversed(delta[key]):assert restored.count(op['after'])==op['occurrences'];restored=restored.replace(op['after'],op['before'])
 assert restored==parent.read_text()
for x in delta['old_parent_files']:assert pin(Path(x['path']))==x
assert len(delta['literal_operations'])==11 and len(delta['checker_literal_operations'])==23
anchor=plan['source_anchor'];record=json.loads(Path(anchor['provider']['path']).read_text())['full_selected_record'];assert record['path']==anchor['source_provider'] and record['line_1based']==anchor['line_1based'] and record['raw_sha256']==anchor['raw_sha256'];assert {k:v for k,v in record['record'].items() if k!='code'}==anchor['metadata']
raw=Path(record['path']).read_bytes().splitlines()[record['line_1based']-1];assert hashlib.sha256(raw).hexdigest()==anchor['raw_sha256'] and json.loads(raw)==record['record']
start=0x1047bd790;metadata_end=0x1047bda78;selected_end=0x1047bd7b0
assert metadata_end-start==744 and selected_end-start==32 and plan['helper']['end_exclusive']==hex(selected_end) and plan['helper']['body_end_exclusive']==hex(metadata_end)
assert plan['helper']['file_offset']==start-plan['expected_segment']['vmaddr']+plan['expected_segment']['fileoff']==75224976
assert start+32<=metadata_end and start+36<=metadata_end and start+744<=metadata_end and not start+748<=metadata_end
# Full supplied read-only checker inspected before this sole invocation. It reads header/load-command metadata, no selected window or tool launch.
cmd=[sys.executable,'-B',str(P/'check.py'),'--check'];run=subprocess.run(cmd,capture_output=True,text=True);assert run.returncode==0 and not run.stderr;result=json.loads(run.stdout);assert result['fixtures']==29 and result['valid_controls']==2 and result['rejections']==27 and result['containment_controls']==3 and result['source_mutation_rejections']==7
refusal=subprocess.run([sys.executable,'-B',str(P/'check.py'),'--write'],capture_output=True,text=True);assert refusal.returncode==1 and not refusal.stdout and 'Read-only --check only' in refusal.stderr
assert not P.with_name('depth-utility-mute-core-prefix-instruction-data').exists()
after=[pin(x) for x in paths];assert before==after
out=B/'reviews/utility-mute-core-prefix-code-preflight-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest=pin(P/'manifest-preparation.json'),watch=before,watch_count=len(paths),unchanged=True,providers=len(plan['providers']),old_parent_files=len(delta['old_parent_files']),collector_literal_inverse=11,checker_literal_inverse=23,single_source_anchor_rawrow_metadata_exact=True,range=dict(start=hex(start),selected_end=hex(selected_end),metadata_end=hex(metadata_end),selected=32,metadata=744,length36_fits_metadata_but_not_fixed_selection=True),checker=dict(argv=cmd,exit=run.returncode,stdout=result,stderr=run.stderr),refusal=dict(exit=refusal.returncode,stderr=refusal.stderr),no_collector_import_main_decoder_original_or_native_run=True),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),result=result)))
