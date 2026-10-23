from pathlib import Path
import ast,datetime,hashlib,json,subprocess,sys
B=Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'depth-utility-mute-x86-onmute-entry-preparation'
def pin(p):
 z=p.read_bytes();return dict(path=str(p),bytes=len(z),sha256=hashlib.sha256(z).hexdigest())
i=json.loads((P/'inputs.json').read_text());d=json.loads((P/'delta.json').read_text());m=json.loads((P/'manifest.json').read_text());paths=sorted({Path(x['path']) for x in i['pins']+d['preserved_parent_files']}|{p for p in P.iterdir() if p.is_file()});before=[pin(p) for p in paths]
assert pin(P/'manifest.json')['sha256']=='b21c536cc01d89bd839991015945cc65947efa4c9a99375f163216bb1449e8b4'
for row in i['pins']+d['preserved_parent_files']:assert pin(Path(row['path']))=={k:row[k] for k in ['path','bytes','sha256']}
assert {x['path'] for x in m['files']}=={p.name for p in P.iterdir() if p.is_file() and p.name!='manifest.json'}
for x in m['files']:
 q=pin(P/x['path']);assert(q['bytes'],q['sha256'])==(x['bytes'],x['sha256'])
for name,ops,parent in [('collect-once.py','collector_literal_operations','collector_before'),('check.py','checker_literal_operations','checker_before')]:
 s=(P/name).read_text()
 for op in reversed(d[ops]):assert s.count(op['after'])==op['occurrences'];s=s.replace(op['after'],op['before'])
 assert s.encode()==Path(d[parent]['path']).read_bytes()
current=ast.parse((P/'collect-once.py').read_text());old=ast.parse(Path(d['collector_before']['path']).read_text())
def selected(t):return next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='validate_prefix')
assert ast.dump(selected(current),include_attributes=False)==ast.dump(selected(old),include_attributes=False)
context=i['asof_context'];snapshot=pin(P/context['retained_provider']);assert(snapshot['bytes'],snapshot['sha256'])==(context['source_identity']['bytes'],context['source_identity']['sha256'])
metadata=json.loads(Path(next(x['path'] for x in i['pins'] if x['role']=='selected_symbol_metadata')).read_text());nom=metadata['selection']['rows']['StereoGainProcessor_AND_OnMute'];assert len(nom)==1 and nom[0]['nlist_index']==70756 and nom[0]['n_value_hex']=='0x10224e760'
header=json.loads((P/'header-map.json').read_text());assert header['image']==metadata['target']['thin'] and header['segments']==metadata['target']['segments'];assert header['slice_file_offset']==0x224e760 and header['length']==240
command=[sys.executable,'-B',str(P/'check.py'),'--check'];run=subprocess.run(command,capture_output=True,text=True);assert run.returncode==0 and not run.stderr;r=json.loads(run.stdout);assert r['valid_synthetic_prefixes']==3 and r['rejected_row_or_raw_controls']==29 and r['rejected_source_controls']==10
refusal=subprocess.run([sys.executable,'-B',str(P/'check.py'),'--write'],capture_output=True,text=True);assert refusal.returncode==1 and not refusal.stdout and 'Read-only --check only' in refusal.stderr
assert not P.with_name('depth-utility-mute-x86-onmute-entry-instructions').exists();after=[pin(p) for p in paths];assert before==after
out=B/'reviews/utility-mute-x86-onmute-code-preflight-review-evidence.json'
with out.open('x') as f:json.dump(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),manifest=pin(P/'manifest.json'),watch=before,watch_count=len(paths),unchanged=True,pins=len(i['pins']),parent_files=len(d['preserved_parent_files']),collector_literal_inverse=len(d['collector_literal_operations']),checker_literal_inverse=len(d['checker_literal_operations']),validate_prefix_AST_parent_exact=True,asof_snapshot_exact=True,nomination_exact=True,header_map_matches_reviewed_metadata=True,checker=dict(argv=command,exit=run.returncode,stdout=r,stderr=run.stderr),refusal=dict(exit=refusal.returncode,stderr=refusal.stderr),selected_window_read=False,collector_or_decoder_or_original_run=False),f,indent=2);f.write('\n')
print(json.dumps(dict(evidence=pin(out),watch=len(paths),result=r)))
