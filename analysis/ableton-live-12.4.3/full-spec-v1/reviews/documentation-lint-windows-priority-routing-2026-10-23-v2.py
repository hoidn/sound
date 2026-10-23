"""Focused routing-doc lint only; no source/native/guest proof checker or release payload reads."""
from pathlib import Path
from urllib.parse import unquote
import collections,datetime,hashlib,json,re,subprocess
R=Path('/home/ollie/Documents/sound');Q=R/'analysis/ableton-live-12.4.3/full-spec-v1/reviews'
names=['wiki/specs/feature-map.md','wiki/research/full-live-coverage-inventory.md','wiki/decisions/adr-0006-reference-observation-reopened.md','wiki/specs/device-analog.md','wiki/research/phase4-probe-batch.md','wiki/research/native-analysis-recovery.md','wiki/project.md','wiki/specs/device-tension.md','wiki/specs/device-corpus.md','wiki/specs/device-electric.md','wiki/research/device-collision-dsp.md','wiki/research/device-electric-dsp.md','wiki/specs/index.md','wiki/research/device-tension-dsp.md','wiki/research/corpus-dsp-static.md','wiki/research/device-analog-dsp.md','wiki/research/index.md','wiki/research/full-live-specification-plan.md','wiki/research/session-handoff.md','wiki/research/native-decompilation-roadmap.md','wiki/verification/coverage.md','wiki/log.md','wiki/research/full-live-specification-design.md','wiki/research/program-structure.md','wiki/research/automation-envelopes.md','wiki/research/clip-launch.md','wiki/research/midi-note-storage.md']
def slug(t):return re.sub(r'[^\w\- ]','',t.strip().lower()).replace(' ','-')
def broken(p,s):
    bad=[]
    for raw in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',s):
        target=raw.strip().split(' "',1)[0].strip('<>')
        if re.match(r'[a-zA-Z][\w+.-]*:',target):continue
        n,_,f=target.partition('#');dest=(p.parent/unquote(n)).resolve()if n else p
        if not dest.exists():bad.append(raw)
        elif f and dest.suffix=='.md':
            body=dest.read_text();anchors={slug(x)for x in re.findall(r'^#{1,6} (.+)$',body,re.M)};anchors.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)',body))
            if unquote(f)not in anchors:bad.append(raw)
    return sorted(set(bad))
base=json.loads((Q/'documentation-lint-2026-10-19-v1.json').read_bytes())['existing_broken_links'];errors=[];ids=[];pins=[]
for n in names:
    p=R/n;b=p.read_bytes();s=b.decode();m=re.match(r'^---\n(.*?)\n---\n',s,re.S);meta=dict(re.findall(r'^(\w+):\s*(.+)$',m[1],re.M))if m else{}
    if any(k not in meta for k in ['id','type','status','updated','access']):errors.append(n+': missing metadata');continue
    datetime.date.fromisoformat(meta['updated']);assert meta['access']in ['neutral','analysis','implementation','handoff']and '\x00'not in s;ids.append(meta['id'])
    bad=set(broken(p.resolve(),s))-set(base.get(n,[]))
    if bad:errors.append({'page':n,'new_broken':sorted(bad)})
    pins.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
assert len(names)==27 and len(ids)==len(set(ids))
a=(R/'wiki/research/full-live-specification-plan.md').read_text().split('### Current execution checkpoint',1)[1].split('#### Earlier checkpoint',1)[0].strip();b=(R/'wiki/research/session-handoff.md').read_text().split('## Current selection',1)[1].split('## Read first',1)[0].strip();assert a==b and '**24,051 new draft case IDs**'in a and '25,095 of 268,015'in a and '36 total / 19 current / 17 superseded'in a
for token in ['UNREVIEWED','PARKED','Session0','SessionA','reviewed O remains zero']:assert token in a
assert 'The latest user coordination assigns Claude guest boot/install ownership'not in a and 'Claude retains exclusive guest ownership pendingcompletionreport'not in a
design=(R/'wiki/research/full-live-specification-design.md').read_text();history=[]
for start,end,want in [('## Revision 15 proposal','## User-adopted revision 15 decision','7dd7bbf101a2ed2b5781b912b3c820d6dc8b1e94806a1a3af147b47039bd8431'),('## Revision 16 proposal','## Revision 16 DATA-policy review','ce691335946dfd360115b926f8f63d765eb557f7bb37603961cafddc81941a7a')]:
    span=design[design.index(start):design.index(end)];got=hashlib.sha256(span.encode()).hexdigest();assert got==want;history.append({'heading':start,'sha256':got,'unchanged':True})
log=(R/'wiki/log.md').read_bytes();prior=json.loads((Q/'windows-priority-routing-2026-10-23-pre-edit.json').read_bytes());assert len(log)>=prior['log_before_bytes']and hashlib.sha256(log[:prior['log_before_bytes']]).hexdigest()==prior['log_before_sha256'];assert log.startswith(subprocess.check_output(['git','show','HEAD:wiki/log.md'],cwd=R))
diff=subprocess.run(['git','diff','--check','--',*names],cwd=R,capture_output=True,text=True)
if diff.returncode:errors.append(diff.stdout+diff.stderr)
result={'status':'PASS'if not errors else'FAIL','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pages':len(names),'page_pins_before_log_entry':pins,'errors':errors,'checkpoint_equal':a==b,'current_static_queues_parked':True,'current_Root_guest_controller':True,'historical_proposals':history,'appendonly_log_against_pre_edit_and_HEAD':True,'scoped_git_diff_whitespace':diff.returncode,'source_native_guest_release_payload_proofs_replayed':0,'limits':'Metadata/date/local links against retained baseline, exact checkpoint and two historical MD proposal hashes only; no source/native/guest/runtime/compatibility proof, no released artifact hash audit. Log entry is appended only after this receipt exists.'}
assert not errors
out=Q/'documentation-lint-windows-priority-routing-2026-10-23-v2.json'
with out.open('x')as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items()if k!='page_pins_before_log_entry'},indent=2))
