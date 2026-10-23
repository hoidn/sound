"""Read-only bounded Delay/Reverb R3 owner check. No old tool/source execution/decode."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
from copy import deepcopy
import ast,json,re,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];A=P.parent/'delay-reverb-source-audit'
load=lambda p:json.loads(p.read_text())
def dg(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def ptr(v,path):
 for k in path.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def audit_view():
 a=load(A/'audit.json');row=load(A/'response-r2.json')['changes'][0];assert row['json_pointer']=='/assessments/8/assessment';assert a['assessments'][8]['assessment']==row['before'];a['assessments'][8]['assessment']=row['after'];return a

def validate(req,cases,fixtures,adoption,audit):
 oldr=load(P/'requirements.json');oldc=load(P/'cases.json')
 assert req[:92]==oldr and cases[:149]==oldc and len(req)==93 and len(cases)==176
 assert len({r['id'] for r in req})==93 and len({c['id'] for c in cases})==176
 assert req[-1]['id']=='REQ-DR-HYBRID-REVERB-022' and req[-1]['provenance']=='D12' and req[-1]['exact_target_applicability']=='unknown'
 assert 'Reverb and EQ tabs' in req[-1]['text'] and 'yellow' in req[-1]['text'] and 'blue' in req[-1]['text'] and 'not a required RGB/pixel palette' in req[-1]['text']
 assert Counter(c['provenance'] for c in oldc)=={'D12':77,'Dpkg':7,'U':65}
 echo=next(c for c in cases if c['id']=='DR-ECHO-014');assert echo['provenance']=='U' and echo['expected'] is echo['exact_target_expected'] is None and 'no application-observable oracle' in echo['comparison']
 ids={r['id'] for r in req};new=cases[149:];groups={g['id']:g for g in audit['proposals']}
 for c in new:
  assert c['requirement'] in ids and c['provenance']=='U' and c['exact_target_applicability']=='unknown' and c['execution']=='unexecuted; no Live, extracted-original or candidate result'
  assert all(c[k] is None for k in ('expected','comparison','exact_target_expected','documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
  assert c['fixture']=='fixtures-r3.json#/current_version_overlay' and c['documented_predicate'] and 'NONEMPTY' in c['setup'] and 'BOTH' in c['setup'] and 'UI-only gestures need no audio/hardware' in c['setup']
  src=['FX:B318'] if c['adoption_group']=='DRA-G00' else groups[c['adoption_group']]['source_blocks']
  refs=[dict(path=str((A/'audit.json').relative_to(ROOT)),pointer=f'/blocks/{i}',block_id=b['id'],quote=b['text']) for i,b in enumerate(audit['blocks']) if b['id'] in src];assert c['source_references']==refs and len(refs)==len(src)
  expected=[]
  for rr in refs:
   b=ptr(audit,rr['pointer']);assert b['id']==rr['block_id'] and b['text']==rr['quote']
   section=[x for x in audit['blocks'] if any(h['level']==2 and h['anchor']==c['device'] for h in x['heading_context'])];pos=next(i for i,x in enumerate(section) if x['id']==b['id']);local=load(P/f'manual-{c["device"]}-blocks.json')[pos];assert all(b[k]==local[k] for k in ('kind','text','html_line'));expected.append(f'manual-{c["device"]}-blocks.json#{local["locator"]}')
  assert c['evidence']==expected
 by={c['id']:c for c in new};required={
 'DR-DELAY-023':['actually click and drag','along display X','along Y','not these drags'],
 'DR-DELAY-024':['actually move the Freq slider','Width slider','inspection never counts'],
 'DR-DELAY-025':['RIGHT delay time','LEFT Offset'],
 'DR-DELAY-026':['RIGHT-only','LEFT identity','Ping Pong OFF','nonzero'],
 'DR-DELAY-027':['EACH offered','EACH seven','enumeration'],
 'DR-DELAY-028':['Repitch, Fade and Jump','Filter depth zero','Delay depth zero'],
 'DR-ECHO-027':['EACH side','LEFT and RIGHT Offset'],
 'DR-ECHO-028':['drag the waveform display','Freq with Sync OFF','Rate with Sync ON'],
 'DR-ECHO-029':['EACH LFO-only','changing-envelope-only','Only after BOTH positives'],
 'DR-ECHO-030':['EACH Release','above-to-below threshold'],
 'DR-ECHO-031':['BOTH independently productive/distinct','actually move Dry/Wet'],
 'DR-FILTER-DELAY-017':['EACH of three lines','actually move its Pan','toggle that line'],
 'DR-FILTER-DELAY-018':['line2 then line3','drag X then Y','old002 actual line1'],
 'DR-FILTER-DELAY-019':['Volume of EACH3','nonmuting'],
 'DR-GRAIN-DELAY-018':['Pitch row for X','Spray row for Y','unavailable retain U'],
 'DR-GRAIN-DELAY-019':['Pitch then Spray','jointly nonzero Pitch and RandomPitch'],
 'DR-HYBRID-REVERB-030':['switch Reverb then EQ then Reverb','yellow Convolution','blue Algorithm'],
 'DR-HYBRID-REVERB-031':['BOTH dry and wet','change Send','Predelay in Time then Beat'],
 'DR-HYBRID-REVERB-032':['first item','backward arrow','nonempty adjacent categories'],
 'DR-HYBRID-REVERB-033':['Freeze OFF','EACH five algorithms','Decay, Size and additional Delay','not count this case as new Freeze'],
 'DR-HYBRID-REVERB-034':['productive Shimmer','change Damping, Mod, Diffusion and Size','old012 actual'],
 'DR-HYBRID-REVERB-035':['Wave0/50/100','Phase0/180','Triplet/16th/Dotted','BOTH independently identifiable'],
 'DR-HYBRID-REVERB-036':['actually toggle EQ and PreAlgo','6 and96dB/oct','Convolution-only inactive-algorithm branch is UI-only'],
 'DR-HYBRID-REVERB-037':['move Vintage','Subtle/Old/Older/Extreme'],
 'DR-RESONATORS-019':['EACH admitted context','EACH II-V Pitch and Fine'],
 'DR-RESONATORS-020':['BOTH I and EACH tested II/III/IV/V','disable only I','EACH I-V individual Gain'],
 'DR-REVERB-022':['Stereo minimum','120degree','Sparse and High','BOTH independently productive']}
 for ident,parts in required.items():assert all(s.casefold() in ' '.join(str(v) for v in by[ident].values()).casefold() for s in parts),ident
 # Same-text/same-HTMLline Damping paragraphs require actual source-section ordinal.
 assert 'manual-hybrid-reverb-blocks.json#hybrid-reverb:B053' in by['DR-HYBRID-REVERB-034']['evidence'] and 'manual-hybrid-reverb-blocks.json#hybrid-reverb:B062' in by['DR-HYBRID-REVERB-035']['evidence']
 f=fixtures['current_version_overlay'];assert f['actual_oracles']==[dict(id=c['id'],expected=None,comparison=None,target='U',executed=False) for c in cases]
 assert 'NONEMPTY' in f['policy'] and 'NONZERO' in f['policy'] and 'BOTH independent' in f['policy']
 assert 'NONZERO tail' in f['hybrid_and_freeze'] and 'recognized valid owned nonidentity IR' in f['hybrid_and_freeze'] and 'Serial algorithm is fed by Convolution' in f['hybrid_and_freeze'] and 'public routing/Blend isolation' in f['hybrid_and_freeze']
 assert 'old DR-HYBRID-REVERB-006 and007' in f['IR_reset_refinement'] and 'NONZERO Convolution wet response' in f['IR_reset_refinement']
 assert fixtures['source_questions']==audit['source_questions'] and 'retained file identity/field presence only' in f['historical_Dpkg']
 assert len(adoption['groups'])==26
 for i,(g,sg) in enumerate(zip(adoption['groups'],audit['proposals'])):
  assert g['id']==sg['id'] and g['audit_pointer']==f'/proposals/{i}' and g['source_blocks']==sg['source_blocks']
  assert g['new_cases']==[c['id'] for c in new if c['adoption_group']==g['id']] and g['overlay_refinement_only']==(g['id']=='DRA-G18') and not g['complete'] and not g['coverage_credit'] and not g['executed']
  assert all(g[k] is None for k in ('documentary_expected','documentary_comparison','actual_expected','actual_comparison'))
 assert sum(bool(g['new_cases']) for g in adoption['groups'])==25 and adoption['extra_source_association']['new_cases']==['DR-DELAY-023','DR-DELAY-024'] and not adoption['complete']
 return True

def main():
 assert sys.dont_write_bytecode and sys.argv[1:]==['--check'],'Read-only --check only; no writer, oldtools or replay'
 inp=load(P/'inputs-r3.json');oldpaths={Path(p) if Path(p).is_absolute() else ROOT/p for p in inp['files']};wiki={ROOT/p for p in inp['canonical_before']};paths=oldpaths|wiki|{p for p in P.rglob('*') if p.is_file()};before={str(p):dg(p) for p in paths}
 assert len(inp['old_packet_files'])==72 and len(inp['files'])==95
 for path,row in inp['files'].items():assert dg(Path(path))==row,path
 for path,row in inp['old_packet_files'].items():assert dg(ROOT/path)==row,path
 for canonical,provider in inp['canonical_before'].items():assert dg(P/provider)==inp['old_packet_files'][str((P/provider).relative_to(ROOT))]
 audit=audit_view();req=load(P/'requirements-r3.json');cases=load(P/'cases-r3.json');f=load(P/'fixtures-r3.json');ad=load(P/'adoption-r3.json');validate(req,cases,f,ad,audit)
 mutations=[('oldreq',lambda r,c,f,a:r[0].update(text='changed')),('oldcase',lambda r,c,f,a:c[0].update(action='changed')),('neworacle',lambda r,c,f,a:c[149].update(documentary_expected='pass')),('actualoracle',lambda r,c,f,a:f['current_version_overlay']['actual_oracles'][0].update(expected='pass')),('display-inspection',lambda r,c,f,a:c[149].update(action='Inspect X/Y')),('slider-inspection',lambda r,c,f,a:c[150].update(action='Inspect sliders')),('source-same-text-alias',lambda r,c,f,a:c[169]['evidence'].__setitem__(0,'manual-hybrid-reverb-blocks.json#hybrid-reverb:B036')),('same-quote-wrong-pointer',lambda r,c,f,a:c[169]['source_references'][0].update(pointer='/blocks/123')),('no-tail',lambda r,c,f,a:f['current_version_overlay'].update(hybrid_and_freeze='Enabled Freeze is enough')),('raw-algorithm-Serial',lambda r,c,f,a:f['current_version_overlay'].update(hybrid_and_freeze='Serial gives raw algorithm and common Freeze')),('no-IR-positive',lambda r,c,f,a:f['current_version_overlay'].update(IR_reset_refinement='Listed filename enough')),('no-positive',lambda r,c,f,a:f['current_version_overlay'].update(policy='Enabled flags enough')),('group-complete',lambda r,c,f,a:a['groups'][0].update(complete=True)),('old-idle-promoted',lambda r,c,f,a:next(x for x in c if x['id']=='DR-ECHO-014').update(provenance='D12',expected='Shuts down')),('file-runtime',lambda r,c,f,a:next(x for x in c if x['provenance']=='Dpkg').update(exact_target_expected='Runtimepass')),('no-both-voices',lambda r,c,f,a:c[174].update(setup='I enabled enough'))]
 bad=[]
 for name,fn in mutations:
  rr,cc,ff,aa=deepcopy((req,cases,f,ad));fn(rr,cc,ff,aa)
  try:validate(rr,cc,ff,aa,audit)
  except (AssertionError,KeyError,IndexError):bad.append(name)
  else:raise AssertionError('Unsafe mutation accepted '+name)
 spec=(P/'spec-r3.md').read_text();research=(P/'research-r3.md').read_text();assert spec==(ROOT/'wiki/specs/delay-reverb-devices.md').read_text() and research==(ROOT/'wiki/research/delay-reverb-devices.md').read_text()
 for name,text in [('spec',spec),('research',research)]:assert text.startswith((P/f'{name}-r2.md').read_text().replace('revision: 2\n','revision: 3\n',1))
 assert all(r['text'] in spec for r in req)
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'anchor','frontmatter','cells','spec_rows'}];assert len(defs)==4;env={'re':re};exec(compile(ast.Module(body=defs,type_ignores=[]),'four-pure-analyst-browser-defs','exec'),env);assert {r['id'] for r in env['spec_rows'](P/'spec-r3.md',spec)}=={r['id'] for r in req}
 links=0;pending=[]
 for p in [ROOT/'wiki/specs/delay-reverb-devices.md',ROOT/'wiki/research/delay-reverb-devices.md',P/'README-r3.md']:
  for dest in re.findall(r'\]\(([^)\s]+)\)',p.read_text()):
   if re.match(r'(https?://|#|mailto:)',dest):continue
   target=(p.parent/dest.split('#')[0]).resolve()
   if not target.exists() and not (P/'manifest-author-r3.json').exists() and target in {P/'manifest-author-r3.json',P/'validation-r3.json'}:pending.append(str(target));continue
   assert target.exists(),(p,dest);links+=1
 oldnames=set(inp['old_packet_files']);current=[p for p in P.rglob('*') if p.is_file()]
 for p in current:
  if str(p.relative_to(ROOT)) not in oldnames:
   data=p.read_bytes();assert data.endswith(b'\n') and all(x.rstrip(b' \t')==x for x in data.splitlines()),p
   if p.suffix=='.json':load(p)
 sealed=(P/'manifest-author-r3.json').exists()
 if sealed:
  m=load(P/'manifest-author-r3.json');assert set(m['payloads'])=={str(p.relative_to(ROOT)) for p in current if p.name!='manifest-author-r3.json'}
  for path,row in m['payloads'].items():assert dg(ROOT/path)==row,path
 assert before=={str(p):dg(p) for p in paths}
 print(json.dumps(dict(status='pass' if sealed else 'pass-unsealed-preflight',sealed=sealed,pending_declared_artifacts=pending,requirements=93,old_requirement_objects_exact=92,cases=176,old_case_objects_exact=149,old_files_exact=72,new_documentary_null=27,current_actual_null_U=176,historical_Dpkg_file_only=7,old_U_cases=65,Echo014_internalidle_U=True,partial_casegroups=25,overlay_only_groups=1,extra_actual_Delay_gestures=2,unsafe_fixtures_rejected=bad,browser_exact_IDs=93,links=links,input_pins=95,watched_unchanged=len(paths),writes=False,complete=False,scope='Partial current owner integrity only; independent root semantic review pending. No original/code/archive/preset decode/runtime/coverage.'),indent=2))
if __name__=='__main__':main()
