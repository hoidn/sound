"""Bounded full retained Mixing chapter audit. No application/network execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json,re,runpy,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];M=P.parent/'mixing-workflows';R=P.parent/'routing-monitoring'
load=lambda p:json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def spans(s):
 a=0;o=[]
 for m in re.finditer(r'(?<=[.!?])\s+(?=[A-Z])',s):o.append((a,m.start()));a=m.end()
 return o+[(a,len(s))]
STATUS={'R':'represented-source-clause-and-action-subset','U':'documented-context-outcome-U','G':'missing-clause-action-or-context','M':'research-guidance-or-domain-context','E':'editorial','I':'image-chart-uninspected'}
ROUTES={'comp':[('routing-monitoring','REQ-RML-032','RML-050')],'meter':[('routing-monitoring','REQ-RML-035','RML-056')],'numeric':[],'solo':[],'arm':[],'group-route':[('routing-monitoring','REQ-RML-026','RML-042')],'group-slot':[('session-workflows','REQ-SESSION-VIEW-006','SV-006')],'return':[('routing-monitoring','REQ-RML-027','RML-043')],'tap':[('routing-monitoring','REQ-RML-028','RML-044'),('routing-monitoring','REQ-RML-028','RML-045')],'cue':[('routing-monitoring','REQ-RML-029','RML-046'),('routing-monitoring','REQ-RML-030','RML-047')],'delay':[('routing-monitoring','REQ-RML-034','RML-054'),('routing-monitoring','REQ-RML-034','RML-055')],'monitor':[('routing-monitoring','REQ-RML-007','RML-009')],'cpu':[('engine-resources','REQ-ER-006','ER-006'),('engine-resources','REQ-ER-007','ER-007')]}
def ref(packet,kind,id):
 q=P.parent/packet/(kind+'.json');rows=load(q);i=next(i for i,r in enumerate(rows) if r['id']==id);r=rows[i];field='contract' if kind=='requirements' else 'setup_and_action';x=dict(id=id,catalog=str(q.relative_to(ROOT)),json_pointer=f'/{i}/{field}',value_sha256=sha256(r[field].encode()).hexdigest())
 if kind=='cases':x.update(documentary_expected_is_null=r['documentary_expected'] is None,documentary_comparator_is_null=r['documentary_comparator'] is None,expected_is_null=r['expected'] is None,comparison_is_null=r['comparison'] is None,target_grade=r['target_grade'],executed=r['executed'])
 else:x.update(provenance=r.get('provenance',r.get('strength')),target_applicability=r['target_applicability'])
 return x

def build():
 bs=load(M/'source-blocks.json');source=load(M/'source.json');plan=load(P/'claim-plan.json');raw=Path(source['path']).read_text()
 assert digest(M/'manifest-author-r1.json')['sha256']=='7d1fd0bcb36be47060757b3055a8b25dbb633b7a497202306984a984b0c37e2b'
 # The retained analyst parser was inspected: its guarded writer main is never invoked.
 parser=runpy.run_path(str(R/'capture.py'));original=parser['Extract']('mixing');original.feed(raw)
 assert [dict(b,locator=f'mixing:B{i:03}') for i,b in enumerate(original.rows,1)]==bs
 parse=runpy.run_path(str(P/'source_parser.py'))['extract'];parsed,resources=parse(raw,'MIXA');assert len(parsed)==len(bs)==94
 claims=[];reconciliation=[]
 for i,(b,p) in enumerate(zip(bs,parsed),1):
  assert (b['kind'],b['text'],b['html_line'])==(p['kind'],p['text'],p['html_line'])
  ss=[(0,len(b['text']))] if b['kind'].startswith('h') else spans(b['text']);rows=plan.get(str(i),[[0,'E',[],[],[],'Literal heading/hierarchy retained; no completion credit.',None]])
  assert {x[0] for x in rows}==set(range(len(ss)));ids=[]
  for n,code,rr,cc,g,note,route in rows:
   a,z=ss[n];quote=b['text'][a:z];id=f'MIXA-C{len(claims)+1:03}';ids.append(id)
   reqs=[ref('mixing-workflows','requirements',f'REQ-MIXING-WORKFLOW-{x:03}' if isinstance(x,int) else 'REQ-MIXING-WORKFLOW-'+x) for x in rr];cases=[ref('mixing-workflows','cases',f'MXW-{x:03}' if isinstance(x,int) else 'MXW-'+x) for x in cc]
   routes=[dict(requirement=ref(packet,'requirements',rid),case=ref(packet,'cases',cid),role='selected source/action context only; not whole-owner completion or new audio law') for packet,rid,cid in ROUTES.get(route,[])]
   extra=[]
   if route=='arm':
    rec=load(P.parent/'recording/cases-r3.json')['records']
    for cid in ['RC-004','RC-005']:
     j=next(j for j,r in enumerate(rec) if r['id']==cid);extra.append(dict(id=cid,catalog=str((P.parent/'recording/cases-r3.json').relative_to(ROOT)),json_pointer=f'/records/{j}/action',value_sha256=sha256(rec[j]['action'].encode()).hexdigest(),role='Current R3 ordinary/modifier and multiselected arm actions, not ExclusiveArm/implicit-arm law'))
   claims.append(dict(id=id,block=b['locator'],sentence=n,disposition=STATUS[code],assessment=note,text_span=[a,z],source_excerpt=quote,source_excerpt_sha256=sha256(quote.encode()).hexdigest(),source_locator=dict(source_id=source['id'],source_path=str(Path(source['path']).relative_to(ROOT)),source_sha256=source['sha256'],source_version=source['version'],source_capture_utc=source['captured_utc'],source_url=source['url'],block_catalog=str((M/'source-blocks.json').relative_to(ROOT)),block_json_pointer=f'/{i-1}',html_line=b['html_line'],html_column=p['html_column'],literal_anchor=b['anchor'],literal_anchor_url=source['url']+'#'+b['anchor'] if b['anchor'] else None,heading_context=b['heading_context'],heading_context_url=source['url']+'#'+b['heading_context'][-1]['anchor'],anchor_role='Paragraph anchor remains literal null; ancestor heading is context, not its paragraph ID or TOC join.'),requirements=reqs,cases=cases,related_owner_routes=routes,related_recording_cases=extra,owner_context=route,case_action_sufficient_for_stated_subset=code=='R',related_context_not_sufficiency=code!='R',gaps=g,target='U',complete=False,behavioral_coverage_credit=0))
  reconciliation.append(dict(block=b,block_json_pointer=f'/{i-1}',raw_block=p,claim_ids=ids,all_nonwhitespace_text_accounted_for=True,target='U',complete=False))
 for i,r in enumerate(resources,1):r.update(id=f'MIXA-R{i:03}',source_sha256=source['sha256'],status='caption literal read, not image proof' if r['kind']=='caption' else 'image or linked destination uninspected',target='U',complete=False)
 props=[]
 for i,g in enumerate(load(P/'proposed-deltas.json')):
  x=dict(g);x.update(proposal_json_pointer=f'/{i}',claim_ids=[c['id'] for c in claims if g['id'] in c['gaps']],source_blocks=sorted({c['block'] for c in claims if g['id'] in c['gaps']}),status='audit proposal only; no current normative ID, owner change or adoption',positive_guard='Future proposal only, not execution authorization. Independently valid owned disposable backed-up Set, admitted controls and exact focus/platform/keymap/modifier/view/preferences; selected tracks/clips/devices/returns/scene/group hierarchy and before-state known. A silence/no-effect/unavailable-operation comparison requires genuine positive audible or control behavior for that exact source and receiver first: active nonzero source/send/return/wet/volume, valid monitor/arm/clip and ordinary routing, distinct Main/Cue/custom paths and isolated competing dry/hardware paths. Remote held-key tests require each mapped key to genuinely change an admitted value independently before a two-key sequence. Missing source, silent/zero/dry-only/muted/unsupported path, empty group, unavailable controller/output/recording or failed baseline stays U, never a negative pass. No hardware, media, account, install or destructive operation supplied.',documentary_expected=None,documentary_comparison=None,expected=None,comparison=None,target='U',executed=False,complete=False)
  assert x['claim_ids'];props.append(x)
 reverse={}
 for kind in ['requirements','cases']:
  reverse[kind]=[dict(id=r['id'],catalog=str((M/(kind+'.json')).relative_to(ROOT)),json_pointer=f'/{i}',claim_ids=[c['id'] for c in claims if any(x['id']==r['id'] for x in c[kind])],status='source/action subsets or related unknown context only',complete=False,target='U') for i,r in enumerate(load(M/(kind+'.json')))]
 questions=[dict(id='Q-046',state='open',snapshot='owner-snapshots/Q046.md',source_blocks=['mixing:B011','mixing:B014','mixing:B043','mixing:B053','mixing:B066','mixing:B067','mixing:B032','mixing:B033'],detail='ExclusiveArm/implicit arm, populated/empty GroupSlot control contexts, SendUI versus stored/active identity, unnamed halfcurve versus finite functions, multiunit/clamp/unqualifiedCtrl remain unresolved. No default curve/processor algorithm/arm gate/groupstop or field identity chosen; Stereo increase/decrease wording does not replace finite pan law.'),dict(id='MIXA-Q01',state='U',detail='Current Version12 body and controls/defaults do not prove target12.4.3. Ordinary selected/audio UI cases do not close arbitrary graphs, constructor/loading, exclusiveprefs, savedstate, nested/equal-time/disabled/modal/boundary histories.'),dict(id='MIXA-Q02',state='U',detail='Historical 18 owner input pins remain frozen author metadata. Only six immutable input identities replayed; selected current owner contexts copied as-of, RecordingR3/RC004005 explicit. No mutable canonical hashpin or silent historical redirect.'),dict(id='MIXA-Q03',state='U/uninspected',detail='Headroom32bit/private architecture, smoothness/perceived-loudness/CPU/sluggishness/clicks and waveform advice impose no candidate algorithms, numeric tolerance or universal inequality. Chart/figures and linked destinations uninspected; captions only read.'),dict(id='MIXA-Q04',state='U',detail='Old15 unresolved cases are three generic history templates pergroup. They remain unknown obligations, not concrete source-specific ExclusiveArm, populated-group-stop, each-key or default-history cases and not execution traces.')]
 summary=dict(scope='Full94-block retained Mixing chapter semantic audit only; no source-topic/product or owner completion',source_blocks=94,source_kinds=dict(Counter(b['kind'] for b in bs)),claim_context_records=len(claims),dispositions=dict(Counter(c['disposition'] for c in claims)),normalized_source_characters=sum(len(b['text']) for b in bs),resources=len(resources),resource_kinds=dict(Counter(r['kind'] for r in resources)),existing_requirements=23,existing_cases=33,proposed_delta_groups=len(props),new_normative_requirements=0,new_normative_cases=0,all_target_U=True,executed=0,behavioral_coverage_credit=0,complete_topics=0,read_scope='All94 retained paragraphs/list/headings, all23clauses/33actions/fixtures and independent R1review read. Selected RML/RecordingR3/Session/numeric/CPU clauses/actions read per owner-context.json; no whole-owner rereview. Facets/character accounting are omission checks, not semantic completion. Image pixels/chart and linked destinations uninspected.')
 return {'claims.json':claims,'block-reconciliation.json':reconciliation,'resources.json':resources,'proposed-deltas-derived.json':props,'existing-catalog-dispositions.json':reverse,'source-questions.json':questions,'summary.json':summary}

def main():
 assert sys.argv[1:] in (['--check'],['--write'])
 if sys.argv[1:]==['--write']:assert not (P/'manifest.json').exists(),'refuse overwrite after seal'
 result=build()
 for name,value in result.items():
  if sys.argv[1:]==['--check']:assert load(P/name)==value,name
  else:(P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps(result['summary.json'],indent=2))
if __name__=='__main__':main()
