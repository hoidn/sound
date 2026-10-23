"""Initial finite owner-context snapshots; no source/runtime imports or live pin replay."""
from pathlib import Path
from hashlib import sha256
import datetime,json,re,shutil
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert not (P/'manifest.json').exists(),'Frozen reconciliation; refuse overwrite'
OWNERS=[('keyboard','keyboard-navigation','keyboard-navigation.md'),('sync','synchronization','synchronization-workflows.md'),('routing','routing-monitoring','routing-monitoring-latency.md'),('remote','remote-control-workflows','remote-control-workflows.md'),('media','media-file-workflows','media-file-workflows.md'),('recording','recording','recording-comping.md'),('project','project-media','project-media-workflows.md'),('max','max-host','max-for-live-hosting.md'),('hosting','plugin-hosting','plugin-hosting.md'),('warp','warping-workflows','warping-workflows.md'),('session','session-workflows','session-view-workflows.md'),('launch','session-launch-workflows','session-launch-workflows.md'),('clip','clip-view','clip-view-workflows.md'),('settings','settings-learning','settings-learning-workflows.md')]
def digest(q):d=q.read_bytes();return dict(bytes=len(d),sha256=sha256(d).hexdigest())
def put(q,v):q.write_text(json.dumps(v,indent=2)+'\n')
def reqview(text):
 out=[];lines=text.splitlines(keepends=True);starts=[];offset=0
 for i,line in enumerate(lines):
  if re.match(r'^### REQ-[A-Z0-9-]+',line):starts.append((i,offset))
  offset+=len(line)
 for i,start in starts:
  rid=re.match(r'^### (REQ-[A-Z0-9-]+)',lines[i])[1];j=i+1
  while j<len(lines) and not re.match(r'^#{1,3} ',lines[j]):j+=1
  end=sum(map(len,lines[:j]));quote=text[start:end].rstrip();out.append(dict(id=rid,quote=quote,spec_character_span=[start,start+len(quote)],spec_line=i+1,role='exact canonical text transcription, not a new normative catalog'))
 offset=0
 for i,line in enumerate(lines):
  m=re.match(r'^\| (REQ-[A-Z0-9-]+) \|',line)
  if m:quote=line.rstrip('\n');out.append(dict(id=m[1],quote=quote,spec_character_span=[offset,offset+len(quote)],spec_line=i+1,role='exact canonical table-row transcription, not a new normative catalog'))
  offset+=len(line)
 assert len(out)==len({r['id'] for r in out});return out
bindings=[]
for key,packet,canonical in OWNERS:
 folder=P/'owners'/key;folder.mkdir(parents=True,exist_ok=True);spec=ROOT/'wiki/specs'/canonical;raw=spec.read_bytes();text=raw.decode();reused=None
 for q in sorted((B/packet).glob('spec-r*.md'),reverse=True):
  if q.read_bytes()==raw:reused=str(q.relative_to(ROOT));break
 origin=ROOT/reused if reused else spec
 (folder/'spec.md').write_bytes(raw)
 data=dict(owner=key,owner_packet=str((B/packet).relative_to(ROOT)),canonical_context=str(spec.relative_to(ROOT)),snapshot_capture_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),canonical_as_of_identity=digest(spec),spec_snapshot='owners/'+key+'/spec.md',spec_reused_immutable_source=reused,scope='as-of copied owner context only; evolving canonical path is not a new live replay pin',catalogs={})
 if (B/packet/'requirements.json').exists():
  q=B/packet/'requirements.json';shutil.copyfile(q,folder/'requirements.json');data['catalogs']['requirements']=dict(snapshot='owners/'+key+'/requirements.json',origin=str(q.relative_to(ROOT)),**digest(q),kind='exact existing JSON catalog bytes',predicate_field=('body' if key=='keyboard' else 'contract'))
 else:
  put(folder/'requirements.json',reqview(text));data['catalogs']['requirements']=dict(snapshot='owners/'+key+'/requirements.json',origin=None,kind='exact as-of canonical clauses/table transcription; owner has no original JSON requirement catalog',predicate_field='quote')
 if (B/packet/'cases.json').exists():
  q=B/packet/'cases.json';shutil.copyfile(q,folder/'cases.json');data['catalogs']['cases']=dict(snapshot='owners/'+key+'/cases.json',origin=str(q.relative_to(ROOT)),**digest(q),kind='exact existing JSON catalog bytes')
 else:
  assert key in ['recording','project'];cases=[];offset=0
  for i,line in enumerate(text.splitlines(keepends=True)):
   if re.match(r'^\| (RC|PMW)-[0-9]+ \|',line):
    cells=[c.strip() for c in line.strip().strip('|').split('|')];prefix='REQ-RECORDING-COMPING-' if key=='recording' else 'REQ-PROJECT-MEDIA-'
    cases.append(dict(id=cells[0],requirements=[prefix+n.strip().zfill(3) for n in cells[1].split(',')],kind=cells[2],action=cells[3],documentary_context=cells[4],raw_row=line.rstrip('\n'),spec_character_span=[offset,offset+len(line.rstrip('\n'))],spec_line=i+1,role='exact canonical table-cell transcription; not executed or a new owner case catalog'))
   offset+=len(line)
  assert cases;put(folder/'cases.json',cases);data['catalogs']['cases']=dict(snapshot='owners/'+key+'/cases.json',origin=None,kind='exact as-of canonical case-table transcription; owner has no original JSON case catalog')
 # Manifest is an identity/context snapshot, not permission to reinterpret any release.
 manifests=sorted((B/packet).glob('manifest-author-r*.json'));mf=manifests[-1] if manifests else B/packet/'manifest.json'
 if key in ['keyboard','media','hosting','recording','project'] and (B/packet/'manifest.json').exists():mf=B/packet/'manifest.json'
 shutil.copyfile(mf,folder/'origin-manifest.json');data['manifest_origin']=str(mf.relative_to(ROOT));data['manifest_snapshot']='owners/'+key+'/origin-manifest.json';data['manifest_as_of_identity']=digest(mf)
 data['case_field_semantics']='Legacy expected/predicate/comparator fields retain documentary proposal meanings under exact_target/exact_12_4_3 U and execution not-run; they are not actual passed outputs. Current expected/comparison-null schema retains its exact original fields. Transcribed tables retain documentary/U row text. This reconciliation executes none.'
 bindings.append(data)
put(P/'owner-bindings.json',bindings)
sourcepaths=[]
for folder,mname in [('settings-source-audit','manifest-r2.json'),('settings-learning','manifest-author-r1.json')]:
 q=B/folder/mname;m=json.loads(q.read_text());sourcepaths.append(q)
 fs=m['files'];sourcepaths +=[q.parent/n for n in fs]
sourcepaths +=[B/'reviews/settings-learning-workflows-review.json']
pins=[dict(path=str(q.relative_to(ROOT)),**digest(q)) for q in sorted(set(sourcepaths))]
assert not any(r['path'].startswith('wiki/') for r in pins);put(P/'source-input-pins.json',pins)
print(len(bindings),'owner snapshots;',len(pins),'immutable source pins; no live canonical replay pins')
