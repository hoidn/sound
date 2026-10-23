"""One-shot analyst case-history correction; never opens or operates media."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
import json, sys

P=Path(__file__).resolve().parent; ROOT=P.parents[3]; B=P.parent
assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r4.json').exists(), 'Unsealed explicit authoring only'
def load(p):return json.loads(p.read_text())
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def save(n,x):
 p=P/n;assert not p.exists(),p;p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
sp=ROOT/'wiki/specs/media-file-workflows.md';rp=ROOT/'wiki/research/media-file-workflows.md'
old={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file() and q.name!='author-r4.py'}
assert info(P/'manifest.json')['sha256']=='3f6a1d3c3265181023a55aaca5badd80ce45504320e285d1e87dacf2bf418843'
for r in load(P/'manifest.json')['payloads']:assert info(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
oldtexts={str(q.relative_to(ROOT)):q.read_text() for q in [sp,rp]}
for q,n in [(sp,'spec-before-r4.md'),(rp,'research-before-r4.md')]:
 assert not (P/n).exists();(P/n).write_bytes(q.read_bytes())
# Freeze only exact JSON path/hash identities present before the correction.
targets={str(q.relative_to(ROOT)):info(q)['sha256'] for q in [sp,rp]};rows=[]
def walk(x,ptr,p):
 if isinstance(x,dict):
  if x.get('path') in targets and 'sha256' in x:rows.append(dict(consumer=str(p.relative_to(ROOT)),pointer=ptr,target=x['path'],sha256=x['sha256'],matches_before=x['sha256']==targets[x['path']]))
  for k,v in x.items():
   esc=k.replace('~','~0').replace('/','~1')
   if k in targets and isinstance(v,str) and len(v)==64:rows.append(dict(consumer=str(p.relative_to(ROOT)),pointer=ptr+'/'+esc,target=k,sha256=v,matches_before=v==targets[k]))
   walk(v,ptr+'/'+esc,p)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,ptr+'/'+str(i),p)
for p in sorted(B.rglob('*.json')):
 try:walk(load(p),'',p)
 except (ValueError,UnicodeError):pass
for r in rows:
 r['consumer_pin']=info(ROOT/r['consumer'])
 r['historical_snapshot']=('spec-before-r4.md' if r['target']==str(sp.relative_to(ROOT)) else 'research-before-r4.md') if r['matches_before'] else None
save('impact-r4.json',{'scope':'As-of exact JSON dict path+sha256 and path-keyed SHA identities under full-spec-v1; not all prose/dependency references or consumer semantic review. Historical identities only; no consumer rewritten or replayed.','original_canonical_hashes':targets,'records':rows})
cases=load(P/'cases.json');updated=json.loads(json.dumps(cases));changes=[]
actions={
 'MF-011':'F3: independently establish an offered Create Analysis Files control, an admitted owned source and a writable disposable directory. Explicitly select On and record the actual value, source identity, no-ASD initial inventory and all other analysis/Auto-Warp settings. Use a fresh never-analyzed copy eligible for this ordinary-add analysis path; add it to a copied Set and independently confirm completed productive analysis as the positive baseline before inspecting the sibling sidecar. Pair with MF-015 using a separate fresh same-source copy, initially no ASD, the same independently admitted path and other settings, and explicit Off; retain separate before/load/completion/after histories for both. Do not use default settings as On evidence or Save Default Clip. Missing control, ineligible source, unwritable directory, suppressed/incomplete/failed analysis or an unavailable positive baseline is U, never a passing absence test.',
 'MF-015':'F3: pair with the genuinely completed productive explicit-On MF-011 baseline using a separate fresh owned same-source copy in a writable disposable directory, initially no ASD. Explicitly select Create Analysis Files Off and record the actual value and the same other analysis/Auto-Warp settings and applicable ordinary-load path; load, independently establish completed analysis, then load again with the same settings and record the second applicable analysis history and sidecar inventory. Do not invoke Save Default Clip or reuse an existing ASD. An unavailable control, ineligible source, failed/suppressed/incomplete analysis or missing matched positive baseline is U, never evidence that Off successfully suppressed a sidecar.'}
for i,c in enumerate(updated):
 if c['id'] in actions:
  changes.append({'pointer':f'/{i}/action','id':c['id'],'old':c['action'],'new':actions[c['id']]});c['action']=actions[c['id']]
assert len(changes)==2;save('cases-r4.json',updated)
replacements=[]
for q in [sp,rp]:
 t=oldtexts[str(q.relative_to(ROOT))];pairs=[('revision: 2\n','revision: 4\n')]
 if q==sp:
  pairs.append(('media-file-workflows/cases.json)','media-file-workflows/cases-r4.json)'))
  for c in cases:
   if c['id'] in actions:pairs.append((c['action'],actions[c['id']]))
  pairs.append(('are unexecuted and ungraded for target compatibility. Unknown probes have null\npredicates. File manipulation', 'are unexecuted and ungraded for target compatibility. MF-011 and MF-015 now\nrecord explicit On/Off histories with separate fresh copies and a completed-analysis\npositive baseline; no initial preference value is inferred. Legacy `predicate`\nfields are documentary proposals, not actual results. Actual target expectations\nand comparisons are absent from this legacy schema and remain unknown/ungraded,\nnot populated by this revision. Unknown probes have null predicates. File\nmanipulation'))
 else:
  pairs.append(('Separate source/scope/predicate review remains required.', 'The unchanged clauses retain their prior independent partial review; the R4\ncase-history correction requires focused independent review.'))
  t+='\n## R4 explicit creation-On/Off history correction\n\nThe [approved owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)\nidentified that historical MF-011 used unspecified default analysis options,\nwhereas MF-015 explicitly selected Off. [SET-B058](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json)\nstates that Create Analysis Files determines creation on import. The retained\n[analysis-files-asd source](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html#analysis-files-asd)\nseparately describes first-add creation, analysis completion, existing ASD,\nAuto-Warp Long Samples Off, creation Off and Save Default Clip exceptions.\n\n[Current cases R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/cases-r4.json)\nchange only the MF-011 and MF-015 action fields: explicit On and explicit Off\nwith separate fresh initially no-ASD owned copies, writable directories, an\nindependently admitted analysis path, recorded other settings and genuinely\ncompleted productive analysis. Unavailable controls, ineligible sources or failed,\nsuppressed or incomplete analysis cannot establish a passing no-sidecar observation. The paired histories\nare future prerequisites, not executed results or a sidecar codec/transaction law.\nThe legacy documentary predicates/basis/unknown fields and exact-target U/not-run\nmetadata are unchanged; no actual expectation, comparison or pass was introduced.\nNo constructor default or complete option-interaction matrix is inferred.\n\nAll original sources, catalogs, IDs, predicates and old packet bytes/seals remain\nin place. Only the two old canonical pages needed new exact historical copies:\n[spec before R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/spec-before-r4.md)\nand [research before R4](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/research-before-r4.md).\nThe prior packet manifest is revision3 after a whitespace-only correction while\nthe prior canonical frontmatter says revision2; R4 preserves both identities.\n[Impact identities](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/impact-r4.json)\nrecord exact as-of JSON pointers. Other frozen consumers were not edited or\nreplayed against changed pages; root owns historical redirection/integration.\nRecording RC-020 default-versus-explicit-Off remains a separate Q051 gap.\n\n[Delta](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/delta-r4.json),\n[read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/validate-r4.py)\nand [R4 packet](../../analysis/ableton-live-12.4.3/full-spec-v1/media-file-workflows/README-r4.md)\nbound the correction. Focused source reading covers the ASD section paragraphs\nand SET-B058, both changed actions, all unchanged case records for exact equality,\nand prior review identities; it is not a fresh semantic audit of the whole\nManaging Files chapter or all downstream owners. All target outcomes remain U.\n'
 for a,b in pairs:
  assert t.count(a)==1,(q,a,t.count(a));t=t.replace(a,b,1)
 # Store exact old-to-current reconstruction, including the appended research section.
 replacements.append({'canonical':str(q.relative_to(ROOT)),'old_snapshot':'spec-before-r4.md' if q==sp else 'research-before-r4.md','new_snapshot':'spec-r4.md' if q==sp else 'research-r4.md','replacements':[{'old':a,'new':b} for a,b in pairs],'appended':t[t.index('\n## R4 explicit'): ] if q==rp else ''})
 q.write_text(t);(P/('spec-r4.md' if q==sp else 'research-r4.md')).write_text(t)
save('delta-r4.json',{'scope':'Q051 explicit creation-On paired history only; no new requirement or documentary/actual oracle','old_packet_files':old,'prior_manifest':info(P/'manifest.json'),'requirement_IDs_unchanged':17,'case_IDs_unchanged':32,'case_field_changes':changes,'canonical_changes':replacements,'source_versions':'Current retained Version12 documentary only; exact12.4.3 U','actual_schema':'Legacy exact_target U/execution not-run; no actual expectation/comparison fields. predicate is documentary, not measured.','no_recording_change':True})
paths=[B/'project-media/manual-files-2026-10-19.html',B/'project-media/source.json',B/'settings-learning/manual-first-steps-2026-10-19.html',B/'settings-learning/source.json',B/'settings-learning/source-blocks.json',B/'settings-owner-reconciliation/manifest.json',B/'settings-owner-reconciliation/ledger.json',B/'reviews/settings-owner-reconciliation-review.json',B/'reviews/media-file-workflows-review-final.json',ROOT/'tools/spec_browser.py']
paths+= [ROOT/r['consumer'] for r in rows]
save('inputs-r4.json',[{'path':str(q.relative_to(ROOT)),**info(q)} for q in sorted(set(paths))])
html=(B/'project-media/manual-files-2026-10-19.html').read_text();start=html.index('<h3 data-number="5.1.2" id="analysis-files-asd">');end=html.index('<h3 ',start+1);segment=html[start:end]
class Paragraphs(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.active=False;self.text=[];self.rows=[]
 def handle_starttag(self,tag,attrs):
  if tag=='p':self.active=True;self.text=[];self.pos=self.getpos()
 def handle_data(self,data):
  if self.active:self.text.append(data)
 def handle_endtag(self,tag):
  if tag=='p' and self.active:self.rows.append({'html_line':html[:start].count('\n')+self.pos[0],'text':' '.join(''.join(self.text).split())});self.active=False
parser=Paragraphs();parser.feed(segment)
source=load(B/'project-media/source.json');settings=load(B/'settings-learning/source.json');block=next(x for x in load(B/'settings-learning/source-blocks.json') if x['id']=='SET-B058')
save('source-context-r4.json',{'ASD':{'path':str((B/'project-media/manual-files-2026-10-19.html').relative_to(ROOT)),'metadata':source,'anchor':'analysis-files-asd','paragraphs':parser.rows,'figures_inspected':False},'Settings':{'path':str((B/'settings-learning/manual-first-steps-2026-10-19.html').relative_to(ROOT)),'metadata':settings,'block':block},'limits':'Exact retained text context only, not runtime, images, linked destinations, ASD layout, defaults or complete option interactions.'})
print('Authored R4 documents and exact two-action delta; inspect/check before sealing.')
