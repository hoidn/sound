"""One-shot analyst RC-020 setup correction; no recording/source inspection code is run."""
from pathlib import Path
from hashlib import sha256
from html.parser import HTMLParser
import json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r3.json').exists(),'Unsealed explicit authoring only'
def load(q):return json.loads(q.read_text())
def info(q):
 b=q.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def save(n,x):
 q=P/n;assert not q.exists();q.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
sp=ROOT/'wiki/specs/recording-comping.md';rp=ROOT/'wiki/research/recording-comping.md'
assert info(P/'manifest.json')['sha256']=='0b1dd1222cfded8bdddad25a367eb7822c743a6bd783f8f183458cb9a97656c1'
oldfiles={str(q.relative_to(P)):info(q) for q in P.rglob('*') if q.is_file() and q.name!='author-r3.py'};assert len(oldfiles)==12
prior=load(P/'manifest.json')
for n,r in prior['files'].items():assert info(P/n)==r
oldtexts={str(q.relative_to(ROOT)):q.read_text() for q in [sp,rp]}
for q,n in [(sp,'spec-before-r3.md'),(rp,'research-before-r3.md')]:
 assert info(q)['sha256']==prior['canonical_documents'][str(q.relative_to(ROOT))];assert not (P/n).exists();(P/n).write_bytes(q.read_bytes())
targets=prior['canonical_documents'];rows=[]
def walk(x,ptr,q):
 if isinstance(x,dict):
  if x.get('path') in targets and 'sha256' in x:rows.append(dict(consumer=str(q.relative_to(ROOT)),pointer=ptr,target=x['path'],sha256=x['sha256'],matches_before=x['sha256']==targets[x['path']]))
  for k,v in x.items():
   e=k.replace('~','~0').replace('/','~1')
   if k in targets and isinstance(v,str) and len(v)==64:rows.append(dict(consumer=str(q.relative_to(ROOT)),pointer=ptr+'/'+e,target=k,sha256=v,matches_before=v==targets[k]))
   walk(v,ptr+'/'+e,q)
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,ptr+'/'+str(i),q)
for q in sorted(B.rglob('*.json')):
 try:walk(load(q),'',q)
 except (ValueError,UnicodeError):pass
for r in rows:
 r['consumer_pin']=info(ROOT/r['consumer']);r['historical_snapshot']=('spec-before-r3.md' if r['target']==str(sp.relative_to(ROOT)) else 'research-before-r3.md') if r['matches_before'] else None
save('impact-r3.json',dict(scope='Finite as-of JSON dict path/hash and path-keyed SHA identities under full-spec-v1; not all prose dependencies/semantic review; consumers untouched.',original_canonical_hashes=targets,records=rows))
fields=['id','requirement_suffix','kind','action','documentary_comparator_or_unknown','evidence'];trans=[];offset=0
for line_number,line in enumerate(oldtexts[str(sp.relative_to(ROOT))].splitlines(True),1):
 if line.startswith('| RC-'):
  cells=[x.strip() for x in re.split(r'(?<!\\)\|',line.strip().strip('|'))];assert len(cells)==6
  trans.append(dict(fields=dict(zip(fields,cells)),raw_row=line.rstrip('\n'),spec_line=line_number,spec_character_span=[offset,offset+len(line.rstrip('\n'))]))
 offset+=len(line)
assert len(trans)==81
save('case-transcription-before-r3.json',dict(role='New exact historical Markdown transcription, NOT an original JSON catalog or executed case result',canonical_snapshot='spec-before-r3.md',rows=trans))
records=[dict(**r['fields'],expected=None,comparison=None,target_grade='U',executed=False) for r in trans]
before=records[19]['action'];assert records[19]['id']=='RC-020' and before=='Default scene-record preference; launch scene with empty armed slots'
action='Use disposable copied Sets and independently offered Start Recording on Scene Launch, eligible record-enabled tracks, configured selected inputs, an active independently recordable owned source and known-empty slots in the scene being launched. Record the actual transport, arm, input and preference states. First explicitly enable the preference and launch the matched scene to establish the genuinely productive recording baseline of RC-021, observing new clips actually recording in those empty armed slots. In a separate matched history with fresh empty slots and the same eligible active source/track/transport conditions, explicitly set Start Recording on Scene Launch Off and record its actual value; launch the scene alone without an additional Session Record, slot Record or Arrangement Record trigger. Inspect whether the empty slots record under the unchanged documentary comparator. Do not treat unspecified defaults as Off evidence. An unavailable control, ineligible or inactive source/track, nonempty slot or missing genuine enabled recording baseline is U, never a passing no-recording observation.'
records[19]['action']=action
save('cases-r3.json',dict(role='First owner JSON view of existing Markdown scenarios; all documentary text unchanged except RC-020 action. Added expected/comparison null, target_grade U and executed false are explicit current status, not historical measurements. Four F rows remain artifact-only, not application tests.',historical_transcription='case-transcription-before-r3.json',records=records))
replacements=[]
for q in [sp,rp]:
 text=oldtexts[str(q.relative_to(ROOT))]
 if q==sp:
  pairs=[('revision: 1\n','revision: 3\n'),(before,action),('no asserted result. No generated fixture or captured execution is claimed.','no asserted result. No generated fixture or captured execution is claimed.\n\nThe [R3 case view](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/cases-r3.json)\nis an explicitly disclosed transcription of these Markdown scenarios. Only\nRC-020 now records explicit Off and a genuine matched enabled RC-021 recording\nbaseline with fresh empty eligible slots and active admitted input. All other\nactions and every documentary comparator remain unchanged. Its explicit actual\nexpectation/comparison fields are null, target grades U and executed flags false;\nthe four F rows remain static artifact-only scenarios, not application results.'),('| 1 (unreleased review corrections) | 2026-10-19 | Narrow REQ-031 to launched-scene names; broader scene-field branch U; single-owner links to Arrangement playback ownership; add RC-079–081 including recording format/depth. Now 81 cases: 65 D12, four artifact audits, 12 U |','| 1 (unreleased review corrections) | 2026-10-19 | Narrow REQ-031 to launched-scene names; broader scene-field branch U; single-owner links to Arrangement playback ownership; add RC-079–081 including recording format/depth. Now 81 cases: 65 D12, four artifact audits, 12 U |\n| 3 | 2026-10-19 | Q051: RC-020 explicitly selects Off with matched productive enabled RC-021 setup; original 32 clauses and all documentary comparators unchanged. Prior packet manifest revision2 and canonical revision1 preserved |')]
  appended=''
 else:
  pairs=[('access: analysis\n','access: analysis\nrevision: 3\n')]
  appended='\n## R3 explicit scene-recording Off history\n\nThe [approved Settings owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)\nidentified that RC-020 named a default preference state, while RC-021 named the\nenabled state. The retained [recording-into-session-slots source](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/manual-12-recording-new-clips-2026-10-19.html#recording-into-session-slots)\ndistinguishes ordinary scene launch from using Start Recording on Scene Launch\nto record empty record-enabled slots. R3 changes only RC-020\'s setup/action to\nexplicit Off, actual recorded preference/transport/input/arm states and a matched\ngenuinely productive enabled RC-021 baseline. Use separate copied histories with\nfresh empty slots, eligible record-enabled tracks and active admitted owned\ninput. Feature/source/track unavailability, occupied slots or a missing enabled\nrecording baseline cannot prove the negative. RC-021 itself is unchanged.\n\nThe original owner had no JSON requirement/case catalogs: its canonical\nMarkdown is the original case source. [Historical transcription](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/case-transcription-before-r3.json)\nretains all81 exact old rows and their line/character spans against\n[spec before R3](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/spec-before-r3.md).\n[Current case view](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/cases-r3.json)\ntranscribes those six documentary cells, changing only RC-020 action. Explicit\nactual expectation/comparison null, target-grade U and unexecuted fields are\nnew status fields, not assertions of historical measurement or grading.\nAll32 requirement clauses and all81 documentary comparators/evidence/kinds/IDs\nare unchanged, including four static artifact-only scenarios. No new default,\nconstructor, numeric, recording-gate, persistence, lifecycle or timing law is\nadopted. Existing explicit preference/source eligibility must be established;\nno actual audio, MIDI, recording or application operation was run.\n\nAll12 prior packet files, including the revision2 manifest and its11 payloads,\nremain unchanged in place; no whole archive is duplicated. Old canonical spec\nfrontmatter says revision1 and the old research page has no revision field.\nTheir exact bytes are preserved in the local before-R3 snapshots.\n[Impact identities](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/impact-r3.json)\nretain exact as-of JSON pointers and historical hashes. Frozen consumers remain\nunmodified and were not replayed against the changed current pages; root owns\nhistorical integration. Older first-review hashes remain historical mismatches.\n\n[Focused source context](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/source-context-r3.json),\n[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/delta-r3.json) and\n[read-only packet check](../../analysis/ableton-live-12.4.3/full-spec-v1/recording/README-r3.md)\nbound this correction. The retained section paragraphs/list items and RC-020/021\nwere read; unchanged requirements/actions are checked for exact preservation.\nThis is not a fresh semantic audit of all chapters, package inventories, figures,\nlinked destinations or downstream owners. Current public Version12 documentary\napplicability remains U for exact12.4.3. Focused independent review is pending.\n'
 for a,b in pairs:assert text.count(a)==1,(q,a);text=text.replace(a,b,1)
 text+=appended;q.write_text(text);name='spec-r3.md' if q==sp else 'research-r3.md';(P/name).write_text(text)
 replacements.append(dict(canonical=str(q.relative_to(ROOT)),old_snapshot='spec-before-r3.md' if q==sp else 'research-before-r3.md',new_snapshot=name,replacements=[dict(old=a,new=b) for a,b in pairs],appended=appended))
save('delta-r3.json',dict(scope='Q051 RC-020 action only; no other clause/action/comparator change',old_packet_files=oldfiles,prior_manifest=info(P/'manifest.json'),case_field_changes=[dict(pointer='/records/19/action',id='RC-020',old=before,new=action)],canonical_changes=replacements))
html=(P/'manual-12-recording-new-clips-2026-10-19.html').read_text();m=re.search(r'<h[1-6][^>]*id="recording-into-session-slots"[^>]*>',html);end=re.search(r'<h[1-6] ',html[m.end():]).start()+m.end();base=html[:m.start()].count('\n')
class Blocks(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.tag=None;self.parts=[];self.rows=[]
 def handle_starttag(self,t,a):
  if t in ['p','li']:self.tag=t;self.parts=[];self.pos=self.getpos()
 def handle_data(self,d):
  if self.tag:self.parts.append(d)
 def handle_endtag(self,t):
  if t==self.tag:self.rows.append(dict(tag=t,html_line=base+self.pos[0],text=' '.join(''.join(self.parts).split())));self.tag=None
parser=Blocks();parser.feed(html[m.start():end]);save('source-context-r3.json',dict(source=load(P/'sources.json')[0],anchor='recording-into-session-slots',blocks=parser.rows,figures_inspected=False,scope='Retained section text only; no exact-build runtime proof, images or linked contents.'))
paths=[B/'reviews/settings-owner-reconciliation-review.json',B/'reviews/recording-review-final.json',B/'settings-owner-reconciliation/manifest.json',B/'settings-owner-reconciliation/ledger.json',B/'settings-owner-reconciliation/owners/recording/spec.md',B/'settings-owner-reconciliation/owners/recording/cases.json',ROOT/'tools/spec_browser.py']+[ROOT/r['consumer'] for r in rows]
save('inputs-r3.json',[dict(path=str(q.relative_to(ROOT)),**info(q)) for q in sorted(set(paths))])
print('Authored one-action Recording R3 successor; inspect/check before seal.')
