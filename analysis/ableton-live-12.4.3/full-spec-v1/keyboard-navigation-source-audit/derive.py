"""Finite semantic reconciliation of two retained keyboard chapters; static reads only."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];K=P.parent/'keyboard-navigation'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
STATUS={'R':'represented-source-clause-and-action-subset','U':'documented-context-outcome-U','G':'missing-clause-action-or-context','M':'research-guidance-or-domain-context','E':'editorial-or-table-structure','D':'binding-discovery-not-command-contract'}
def spans(s):
 out=[];a=0
 for m in re.finditer(r'(?<=[.!?])\s+(?=[A-Z])',s):out.append((a,m.start()));a=m.end()
 return out+[(a,len(s))]
def ref(kind,n):
 rows=load(K/(kind+'.json'));id=f'REQ-KEYBOARD-NAV-{n:03}' if kind=='requirements' else f'NAV-{n:03}';i=next(i for i,r in enumerate(rows) if r['id']==id);r=rows[i];field='body' if kind=='requirements' else 'action'
 result=dict(id=id,catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}/{field}',value_sha256=sha256(r[field].encode()).hexdigest(),basis=r['basis'])
 if kind=='cases':result.update(kind=r['kind'],legacy_documentary_expected_is_null=r['expected'] is None,exact_target=r['exact_target'],execution=r['execution'],actual_target_oracle=None,schema_note='Legacy expected is a documentary proposal, not an executed target oracle; no original schema field is rewritten.')
 return result

def build():
 sources=load(K/'sources.json');parse=runpy.run_path(str(P/'source_parser.py'))['extract'];blocks=[];resources=[]
 for si,s in enumerate(sources,1):
  assert digest(ROOT/s['path'])=={k:s[k] for k in ['bytes','sha256']}
  b,rs=parse((ROOT/s['path']).read_text(),f'KN{si}');blocks.extend(b)
  for i,r in enumerate(rs,1):
   rid=f'KN{si}:R{i:03}';r.update(id=rid,source_id=f'KN{si}',source_sha256=s['sha256'],status='caption literal read; no pixel proof' if r['kind']=='caption' else 'resource destination or pixels uninspected',target='U',complete=False)
   if rid in {'KN1:R021','KN1:R023','KN1:R025','KN1:R027'}:r['related_gap']='K20' if rid=='KN1:R021' else 'K21'
   resources.append(r)
 plan=load(P/'claim-plan.json');bindings=load(K/'shortcut-bindings.json');claims=[];ledger=[]
 def append(b,a,z,code,rr,cc,g,note,facet=None,binding=None):
  s=sources[int(b['source_id'][-1])-1];heading=b['heading_context'][-1];literal=b['attributes'].get('id');quote=b['text'][a:z]
  c=dict(id=f'KNA-C{len(claims)+1:03}',block=b['id'],facet=facet or quote,disposition=STATUS[code],assessment=note,text_span=[a,z],source_excerpt=quote,source_excerpt_sha256=sha256(quote.encode()).hexdigest(),source_locator=dict(source_id=s['id'],source_catalog=str((K/'sources.json').relative_to(ROOT)),source_json_pointer=f'/{int(b["source_id"][-1])-1}',source_path=s['path'],source_sha256=s['sha256'],source_version=s['version'],source_capture_utc=s['captured_utc'],source_url=s['url'],block_catalog='source-blocks.json',block_json_pointer=f'/{blocks.index(b)}',html_line=b['html_line'],html_column=b['html_column'],literal_anchor=literal,literal_anchor_url=s['url']+'#'+literal if literal else None,heading_context= b['heading_context'],heading_context_url=s['url']+'#'+heading['anchor'],anchor_role='Literal paragraph/row anchor is preserved; ancestor heading is context, never an inherited paragraph ID or TOC join.'),requirements=[ref('requirements',n) for n in rr],cases=[ref('cases',n) for n in cc],gaps=g,case_action_represents_only_stated_subset=code=='R',related_context_not_sufficiency=code!='R',target='U',complete=False,behavioral_coverage_credit=0)
  c['excerpt_representation']='Normalized decoded HTML prose text; raw HTML retained separately.' if b['kind']!='tr' else 'Ordered normalized source cells joined by audit-only | delimiters; pipe characters are not claimed literal source text.'
  if b['kind']=='tr':c['source_cell_quotes']=[cell['text'] for cell in b['cells']]
  if binding is not None:c['discovery_binding']=binding
  claims.append(c);return c
 for b in blocks:
  if b['kind']=='tr':
   if b['cells'][0]['kind']=='th':append(b,0,len(b['text']),'E',[],[],[],'Platform header/column structure retained; not a command or behavioral case.');continue
   id=f'BIND-T{b["table"]:02}-R{b["row"]-1:03}';i=next(i for i,r in enumerate(bindings) if r['id']==id);r=bindings[i]
   assert [c['text'] for c in b['cells']]==[r['command'],r['windows_source'],r['macos_source']]
   assert b['raw_html_sha256']==r['cell_html_sha256'] and b['html_line']==r['html_line'] and b['heading_context'][-1]['anchor']==r['section']
   binding=dict(id=id,catalog=str((K/'shortcut-bindings.json').relative_to(ROOT)),json_pointer=f'/{i}',raw_row_sha256=r['cell_html_sha256'])
   contexts={3:['KN2:B037'],7:['KN2:B081'],11:['KN2:B110'],26:['KN2:B336'],27:['KN2:B350','KN2:B351']}.get(b['table'],[])
   c=append(b,0,len(b['text']),'D',[19],[34],[],'Exact command/platform cell syntax and raw row identity only. NAV034 is documentary extraction, not command dispatch, per-row canonical ownership, numeric result or context/OS/reader/target proof. No shortcut grammar invented.',binding=binding)
   ledger.append(dict(binding=binding,source_block=b['id'],source_block_json_pointer=f'/{blocks.index(b)}',source_cells=b['cells'],explicit_context_blocks=contexts,context_scope='Only listed literal source prerequisites; not exhaustive enabled/focus/selection/IME/reader/mapping conditions.',discovery_claim=c['id'],normative_command_contract=False,command_owner_reconciled=False,dispatch_tested=False,complete=False,target='U',actual_expected=None,actual_comparison=None))
   if id=='BIND-T02-R009':append(b,0,len(b['text']),'G',[9,19],[14,34],['K24'],'Alt/Option8 selected Clip Panel is in discovery, but clause009/case014 only enumerate0..7 and case022 other panel chord. No selected-panel focus case or context history. Preserve inventory; propose bounded owner reconciliation.',facet='Selected Clip Panel focus is not the existing0..7 set')
   continue
  if b['kind'].startswith('h'):
   if b['source_id']=='KN1' and int(b['id'][-3:]) in {48,51,61,81,110,121,129,132}:append(b,0,len(b['text']),'R',[9],[14],[],'Literal platform focus chord in source heading matches actual separate0..7 focus actions with applicable views present. No hidden-view/reader guarantee.')
   else:append(b,0,len(b['text']),'E',[],[],[],'Exact heading/subsection retained, no semantic completion credit.')
   continue
  ss=spans(b['text']);rows=plan[b['id']];assert [r[0] for r in rows]==list(range(len(ss)))
  for i,code,rr,cc,g,note in rows:
   a,z=ss[i];append(b,a,z,code,rr,cc,g,note)
  if b['id'] in {'KN1:B021','KN2:B373'}:
   a,z=ss[0];append(b,a,z,'U',[20],[36],[],'Source stopping contrast retained alongside enabled Wrap subset. Existing wrap-off boundary case stays null/U; no universal off-mode boundary or scope guessed.',facet='Enabled wrapping versus stopping contrast')
  if b['id']=='KN1:B139':
   a,z=ss[1];append(b,a,z,'G',[16],[28],['K20'],'Case028 says move pending point, but does not explicitly name left/right keyboard movement before confirmation. Refine that specific input route; no step/bounds/interpolation law.',facet='Explicit keyboard movement of pending new point')
  if b['id']=='KN1:B075':
   # This raw paragraph embeds a dash list; preserve each independent command facet too.
   start=0
   for i,chunk in enumerate(b['text'].split(' - ')):
    a=b['text'].index(chunk,start);z=a+len(chunk);start=z
    append(b,a,z,'E' if i==0 else 'G',[],[],[] if i==0 else ['K12'],'Embedded heading' if i==0 else 'Individual content-selection/edit dispatch is not a navigation edge-edit action; reconcile domain owner. No clipboard format, displacement or compound edit result inferred.',facet='Embedded content command: '+chunk)
 props=[]
 for i,g in enumerate(load(P/'proposed-deltas.json')):
  x=dict(g);x.update(proposal_json_pointer=f'/{i}',claim_ids=[c['id'] for c in claims if g['id'] in c['gaps']],source_blocks=sorted({c['block'] for c in claims if g['id'] in c['gaps']}),status='audit only; no normative requirement/case or current owner change',positive_guard='Future proposal only, no execution authorization. Independently admitted exact build/feature, correct recorded OS/layout/IME/modifier keys, focus/view/selection/editor/modal state and navigation preferences; main-window Tab ON except explicit OFF view-switch/Settings exception. Establish genuinely working enabled-control input and selected target before variant/absence/failure; supported OS+reader must produce independently functioning baseline for relevant controls before reader-context comparisons. Audio/MIDI, export or edit proposals require independently accepted owned nonempty source, valid selected notes/points/locator/device, accepted parameter values and independently positive audible/nonzero routed output where relevant. Unavailable feature/content/reader/device/permissions or failed baseline stays U, never a negative pass. No account/download/install/driver/reader execution or source modification supplied.',documentary_expected=None,documentary_comparison=None,expected=None,comparison=None,target='U',executed=False,behavioral_coverage_credit=0)
  assert x['claim_ids'];props.append(x)
 reverse={}
 for kind in ['requirements','cases']:
  reverse[kind]=[]
  for i,r in enumerate(load(K/(kind+'.json'))):
   matching=[c for c in claims if any(a['id']==r['id'] for a in c[kind])]
   reverse[kind].append(dict(id=r['id'],catalog=str((K/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}',claim_ids=[c['id'] for c in matching],represented_subset_claims=[c['id'] for c in matching if c['case_action_represents_only_stated_subset']],status='partial or context-only source/action reconciliation; no completion',target='U',complete=False))
 questions=[dict(id='KNA-Q01',topic='Version/platform/focus/default provenance',state='U',detail='Current Version12 source and discovered post-target commands do not prove12.4.3. Declared default enabled/hidden/source about500ms are not constructor, OS key dispatch, strict threshold or migration laws.'),dict(id='KNA-Q02',topic='Export chord source difference',state='unresolved-source-context',sources=['KN1:B079','BIND-T04-R007','BIND-T06-R008'],detail='Accessibility text gives CtrlR/CmdR for export; shortcuts give CtrlShiftR/CmdShiftR for export and CtrlR/CmdR rename. Preserve distinct text; no unqualified export/rename implementation or key dispatch choice.'),dict(id='KNA-Q03',topic='Windows MIDI next/previous note source difference',state='unresolved-source-context',sources=['KN1:B093','KN1:B094','BIND-T15-R019','BIND-T15-R020'],detail='Accessibility text WindowsCtrl differs from shortcut table WindowsAlt, while MacOption aligns. Same-pitch/context/selection roles require reconciliation; do not choose one from label similarity.'),dict(id='KNA-Q04',topic='Reader/protocol/context unknowns',state='U',detail='Support restrictions remain current documentary limitations, not permissions to omit features. No exact tree, utterance, palette/animation frame, OS/reader recovery, language fallback or allcommand focus restoration supplied.'),dict(id='KNA-Q05',topic='Lifecycle and domain owners',state='U',detail='Old NAV035-042 conflict/boundary/malformed/layout/protocol/undo/persistence/teardown obligations remain unknown; they do not close concrete source histories. Existing command-owner links in preserved canonical scope require separate reconciliation before adopting new domain/UI predicates.'),dict(id='KNA-Q06',topic='Resources uninspected',state='uninspected',detail='All literal captions/links/attributes read. Five images and24 destinations not viewed or fetched; ComputerMIDI keyboard note layout cannot be reconstructed from uninspected figure or octave/velocity labels.')]
 for q in questions:
  if 'sources' not in q:continue
  q['evidence']=[]
  for sid in q['sources']:
   i=next(i for i,c in enumerate(claims) if c['block']==sid or c.get('discovery_binding',{}).get('id')==sid);c=claims[i]
   q['evidence'].append(dict(claim_id=c['id'],claim_catalog='claims.json',claim_json_pointer=f'/{i}',source_block=c['block'],block_catalog='source-blocks.json',block_json_pointer=c['source_locator']['block_json_pointer'],source_locator=c['source_locator'],source_excerpt=c['source_excerpt'],source_cell_quotes=c.get('source_cell_quotes'),binding=c.get('discovery_binding')))
 summary=dict(scope='Full two retained chapters, prose/list/heading/table reconciliation only; no command, source-topic or application completion',source_chapters=2,source_blocks=len(blocks),block_kinds=dict(Counter(b['kind'] for b in blocks)),claim_context_records=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),source_text_characters=sum(len(b['text']) for b in blocks),shortcut_tables=27,shortcut_data_rows=len(ledger),shortcut_header_rows=27,resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),existing_requirements=21,existing_cases=42,proposed_delta_groups=len(props),new_normative_requirements=0,new_normative_cases=0,all_target_U=True,executed=0,behavioral_coverage_credit=0,complete_topics=0,read_scope='All541 source blocks including every prose/list assertion/qualifier and all292 command/Windows/Mac cell rows manually read against all21 clauses/all42 actions/fixtures and both independent reviews. Facets may share sentence spans. Full textual accounting and extraction are not semantic completion. Only audited owner canonicals snapshotted; external domain-owner clauses not newly audited. Image pixels and linked destinations uninspected.')
 return {'source-blocks.json':blocks,'resources.json':resources,'claims.json':claims,'binding-reconciliation.json':ledger,'proposed-deltas-derived.json':props,'existing-catalog-dispositions.json':reverse,'source-questions.json':questions,'summary.json':summary}

def main():
 assert sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 result=build()
 for name,value in result.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==value,name
  else:(P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result['summary.json'],indent=2))
if __name__=='__main__':main()
