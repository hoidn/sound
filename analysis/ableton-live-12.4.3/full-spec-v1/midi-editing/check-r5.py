"""Read-only focused source-role correction. No old main/writer/source execution."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'midi-tools-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def pointer(v,s):
 for k in s.strip('/').split('/'):v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def replace_pointer(v,s,b,a):
 bits=s.strip('/').split('/');parent=v
 for k in bits[:-1]:parent=parent[int(k)] if isinstance(parent,list) else parent[k]
 k=int(bits[-1]) if isinstance(parent,list) else bits[-1];assert parent[k]==b;parent[k]=a

def semantic_roles(plan):
 r,s,e=[plan['groups'][i] for i in [11,13,20]]
 assert 'The Dimension chooser selects Position, Pitch, Duration or Velocity.' in r['clause_append']
 assert 'by dragging across the display columns and by Rotate Step Down/Up buttons' in r['action']
 assert 'Explicitly select Position in the Dimension chooser before toggling Rotate on Grid.' in r['action']
 assert 'select Position before using Rotate on Grid' in r['clause_append']
 assert 'each Position/Pitch/Duration/Velocity column' not in r['clause_append'] and 'Velocity columns separately' not in r['action']
 assert 'Low and High can each be edited by its respective Strum Position display breakpoint or computer-keyboard value entry.' in s['clause_append']
 assert 'Separately admitted Tension changes do not imply those same gestures.' in s['clause_append']
 assert 'respective Low and High Strum Position display breakpoints' in s['action'] and 'without assuming breakpoint or keyboard-entry equivalence' in s['action']
 assert 'one middle randomization button that sets the Rotation sliders value for each voice' in e['clause_append']
 assert 'individual voice-enable toggles and Rotation sliders' in e['clause_append']
 assert 'press the one randomization button in the middle of the pattern visualization' in e['action']
 assert 'No separately targeted per-voice randomize control or guaranteed changed realization is inferred.' in e['action']

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only'
 prior=load(P/'prior-files-r5.json');oldmf=load(P/'manifest-author-r4.json');assert len(prior)==55 and set(prior)==set(oldmf['files'])|{'manifest-author-r4.json'}
 inherited=load(P/'inputs-r4.json');extra=load(P/'inputs-r5.json');assert len(inherited)==59 and len(extra)==1
 watch={q for q in P.iterdir() if q.is_file()}|{ROOT/r['path'] for r in inherited+extra}|{ROOT/'wiki/specs/midi-editing-tools.md',ROOT/'wiki/research/midi-editing-tools.md'};before={str(q):dg(q) for q in watch}
 for n,v in prior.items():assert dg(P/n)==v
 for r in inherited+extra:assert dg(ROOT/r['path'])=={k:r[k] for k in ['bytes','sha256']}
 assert dg(P/'manifest-author-r4.json')['sha256']=='046c33658b5ca1949eda7d71e94f458a142ab3bfe3d4f0970772fd2a3a6785f6'
 review=load(ROOT/extra[0]['path']);assert extra[0]['sha256']=='4359641325a097e2c68d1b87c60ce99fa7a0f9e649eb0058eaa266da638fda5a' and review['disposition']=='required-corrections'
 correction=load(P/'correction-r5.json');assert correction['resolves']==[f'MIDI-TOOLS-R4-REVIEW-{i:03}' for i in [1,2,3]]
 assert correction['review']=={k:extra[0][k] for k in ['path','bytes','sha256']}
 assert len(correction['plan_replacements'])==6 and {r['pointer'] for r in correction['plan_replacements']}=={f'/groups/{i}/{k}' for i in [11,13,20] for k in ['clause_append','action']}
 plan=load(P/'tools-increment-r4.json')
 for r in correction['plan_replacements']:replace_pointer(plan,r['pointer'],r['before'],r['after'])
 assert plan==load(P/'tools-increment-r5.json');semantic_roles(plan)
 cat=load(P/'acceptance-cases-r4.json');assert len(correction['case_replacements'])==5
 assert {r['pointer'] for r in correction['case_replacements']}=={'/cases/83/setup_action','/cases/85/setup_action','/cases/92/setup_action','/format_revision','/provenance'}
 for r in correction['case_replacements']:replace_pointer(cat,r['pointer'],r['before'],r['after'])
 assert cat==load(P/'acceptance-cases-r5.json') and cat['cases'][:72]==load(P/'acceptance-cases-r3.json')['cases']
 oldcat=load(P/'acceptance-cases-r4.json');oldplan=load(P/'tools-increment-r4.json')
 for i in [11,13,20]:
  before_action=oldcat['cases'][72+i]['setup_action'];old_suffix=oldplan['groups'][i]['action'];assert before_action.endswith(old_suffix)
  assert cat['cases'][72+i]['setup_action']==before_action[:-len(old_suffix)]+plan['groups'][i]['action'],'common prerequisites unchanged'
 for r in correction['requirement_rows']:
  i=next(j for j,g in enumerate(plan['groups']) if g['requirement']==r['id']);prior_clause=oldplan['groups'][i]['clause_append'];assert r['before'].count(prior_clause)==1
  assert r['after']==r['before'].replace(prior_clause,plan['groups'][i]['clause_append'],1),'only precise appended clause changes'
 for i,(o,n) in enumerate(zip(oldcat['cases'],cat['cases'])):
  assert set(o)==set(n)
  assert {k for k in o if o[k]!=n[k]}==({'setup_action'} if i in [83,85,92] else set())
  if i>=72:assert n['setup_action'].endswith(plan['groups'][i-72]['action'])
 assert len(cat['cases'])==93 and Counter(c['documented_domain_grade'] for c in cat['cases'])=={'D12':77,'U':16}
 for f in ['spec','research']:
  assert (P/f'{f}-before-r5.md').read_bytes()==(P/f'{f}-r4.md').read_bytes();text=(P/f'{f}-before-r5.md').read_text()
  if f=='spec':
   assert {r['id'] for r in correction['requirement_rows']}=={f'REQ-MIDI-EDIT-{i:03}' for i in [34,36,43]}
   for r in correction['requirement_rows']:assert text.count(r['before'])==1;text=text.replace(r['before'],r['after'],1)
  for r in correction[f'editorial_{f}_replacements']:assert text.count(r['before'])==1;text=text.replace(r['before'],r['after'],1)
  text+=correction[f'{f}_suffix'];assert text==(P/f'{f}-r5.md').read_text()
  assert (ROOT/f'wiki/{"specs" if f=="spec" else "research"}/midi-editing-tools.md').read_bytes()==(P/f'{f}-r5.md').read_bytes()
 # Inspect/extract only the old pure safety guard, never old module imports/main.
 oldtree=ast.parse((P/'validate-r4.py').read_text());defs=[n for n in oldtree.body if isinstance(n,ast.FunctionDef) and n.name=='safety'];assert len(defs)==1 and not defs[0].decorator_list
 env=dict(P=P,ROOT=ROOT,A=A,load=load,pointer=pointer,Counter=Counter);exec(compile(ast.Module(body=defs,type_ignores=[]),'<pinned R4 pure safety>','exec'),env);safety=env['safety'];safety(cat,plan)
 rejected=[]
 for name in ['old-gesture-erased','actual-oracle','generator-flag-only','zero-without-positive','offline-hardware','wrong-source','C1-resolved','numeric-new-oracle','Strum-baseline-erased','lost-generator-output']:
  c,g=deepcopy(cat),deepcopy(plan)
  if name=='old-gesture-erased':c['cases'][71]['setup_action']='changed'
  elif name=='actual-oracle':c['cases'][72]['actual_expected']='measured'
  elif name=='generator-flag-only':c['cases'][89]['positive_guard']['actual_nonempty_output_before_generator_bounds_capacity_origin_absence']=False
  elif name=='zero-without-positive':c['cases'][85]['positive_guard']['productive_matched_operation_before_negative']=False
  elif name=='offline-hardware':c['cases'][73]['positive_guard']['hardware_required_for_editor_data']=True
  elif name=='wrong-source':c['cases'][76]['source_contexts'][0]['json_pointer']='/blocks/0'
  elif name=='C1-resolved':c['cases'][72]['documented_domain_grade']='D12'
  elif name=='numeric-new-oracle':c['cases'][76]['documentary_expected']=g['groups'][4]['documentary_expected']='exact numeric output';c['cases'][76]['documentary_comparator']=g['groups'][4]['documentary_comparator']='numeric'
  elif name=='Strum-baseline-erased':c['cases'][85]['setup_action']=c['cases'][85]['setup_action'].replace('NONZERO','zero');g['groups'][13]['action']=g['groups'][13]['action'].replace('NONZERO','zero')
  else:c['cases'][89]['setup_action']=c['cases'][89]['setup_action'].replace('NONEMPTY','flag');g['groups'][17]['action']=g['groups'][17]['action'].replace('NONEMPTY','flag')
  try:safety(c,g)
  except AssertionError:rejected.append(name)
  else:raise AssertionError('Unsafe retained fixture accepted '+name)
 focused=[]
 for name in ['dimension-chooser-as-columns','RotateGrid-without-Position','Tension-gets-LowHigh-gestures','individual-Euclidean-randomize']:
  g=deepcopy(plan)
  if name=='dimension-chooser-as-columns':g['groups'][11]['clause_append']=g['groups'][11]['clause_append'].replace('The Dimension chooser selects Position, Pitch, Duration or Velocity.','Each dimension has its own column.')
  elif name=='RotateGrid-without-Position':g['groups'][11]['action']=g['groups'][11]['action'].replace('Explicitly select Position in the Dimension chooser before toggling Rotate on Grid.','Toggle Rotate on Grid for any dimension.')
  elif name=='Tension-gets-LowHigh-gestures':g['groups'][13]['clause_append']=g['groups'][13]['clause_append'].replace('Low and High can each','Low, High and Tension can each')
  else:g['groups'][20]['action']=g['groups'][20]['action'].replace('press the one randomization button in the middle of the pattern visualization','press each voice randomize button')
  try:semantic_roles(g)
  except AssertionError:focused.append(name)
  else:raise AssertionError('Source-role conflation accepted '+name)
 audit=load(A/'audit.json');raw=(P/'manual-12-midi-tools-2026-10-19.html').read_text();selected=list(range(74,81))+list(range(90,95))+list(range(141,147))
 for n in selected:
  b=audit['blocks'][n-1];assert raw[b['raw_start']:b['raw_end']]==b['raw_html'] and raw.count('\n',0,b['raw_start'])+1==b['html_line']
 assert 'Dimension chooser' in audit['blocks'][74]['text'] and 'When Position is selected' in audit['blocks'][78]['text']
 assert 'both parameters' in audit['blocks'][92]['text'] and 'middle of the pattern visualization' in audit['blocks'][142]['text']
 browserdefs=[n for n in ast.parse((ROOT/'tools/spec_browser.py').read_text()).body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(browserdefs)==4 and all(not n.decorator_list for n in browserdefs);be={'re':re};exec(compile(ast.Module(body=browserdefs,type_ignores=[]),'<owned Browser read functions>','exec'),be)
 spec=(P/'spec-r5.md').read_text();ids={r['id'] for r in be['spec_rows'](ROOT/'wiki/specs/midi-editing-tools.md',spec)};assert ids=={f'REQ-MIDI-EDIT-{i:03}' for i in range(1,44)}
 links=0
 for n,base in [('README-r5.md',P),('spec-r5.md',ROOT/'wiki/specs'),('research-r5.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)]+)\)',(P/n).read_text()):
   if re.match(r'^[A-Za-z]+:',dest):continue
   target=base/dest.split('#')[0];assert target.exists(),dest;links+=1
   if '#' in dest and target.suffix=='.md':assert dest.split('#',1)[1] in {be['anchor'](l.lstrip('#').strip()) for l in target.read_text().splitlines() if l.startswith('#')}
 for p in P.iterdir():
  if p.is_file() and p.name not in prior:
   b=p.read_bytes();assert b.endswith(b'\n') and b'\x00' not in b and all(l.rstrip(b' \t')==l for l in b.splitlines())
 if (P/'manifest-author-r5.json').exists():
  mf=load(P/'manifest-author-r5.json');assert set(mf['files'])=={p.name for p in P.iterdir() if p.is_file()}-{'manifest-author-r5.json'}
  for n,v in mf['files'].items():assert dg(P/n)==v
 assert before=={str(p):dg(p) for p in watch}
 print(json.dumps(dict(status='pass',prior_files=55,input_pins=60,requirements=43,cases=93,precise_clause_rows=3,precise_setup_actions=3,source_claims_oracles_guards_unchanged=True,earlier_records_exact=72,documentary_D12=77,documentary_U=16,actual_nonnull=0,executed=0,complete_topics=0,focused_source_contexts=len(selected),retained_mutation_fixtures=rejected,focused_mutation_fixtures=focused,Browser_IDs=len(ids),links=links,watched_paths=len(watch),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
