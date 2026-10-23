#!/usr/bin/env python3
"""Own compact R4 checker; no old main/import/replay/adapter or vendor code."""
import argparse,ast,copy,hashlib,importlib.util,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parents[4];D=pathlib.Path(__file__).resolve().parent

def j(p):return json.loads(p.read_text())
def digest(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def safe(p,cases):
 assert len(cases)==101
 assert cases[:81]==j(D/'cases-r3.json')['cases'],'oldcasechanged'
 assert len(p['groups'])==20 and len(p['new_cases'])==20
 assert [c['id'] for c in cases]==[f'RCK-{n:03}' for n in range(1,102)]
 for c in cases[81:]:
  for k in ['actual_expected','actual_comparison','expected_comparator']:assert c[k] is None,'inventedoracle'
  assert c['execution']=='unexecuted' and c['exact_12_4_3_runtime_applicability']=='U'
  assert c['positive_guard']==p['guard'] and all(c['positive_guard'].values()),'guardlost'
  assert c['setup_action'].startswith(p['future_common']),'commonguardlost'
  assert (c['documentary_expected'] is None)==(c['documentary_comparator'] is None),'unpairedoracle'
 assert sum(c['documentary_expected'] is not None for c in cases[81:])==7
 actions={int(c['id'][4:]):c['setup_action'] for c in cases[81:]}
 # Essential actual actions/qualifiers, not just titles or flags.
 checks={82:['selected track','no-selected-track','return/Main','factory'],83:['DEVICE title','shown/expanded positive','focus chord separate'],84:['NAV079','right-arrow','Show Options'],85:['nonzero known input AND','independently nonmuted output','BOTH actual input/output'],86:['actually offered functioning','within-device triangle','Absent device/control is U','not a gesture inferred from the triangle icon'],87:['eligible built-in non-Rack','two genuinely distinguishable','Edit, device context and Show Options','(B)'],88:['active changing automation contribution','PARAMETER context','Global re-enable is not substitute'],89:['selected-A versus selected-B','BOTH slots','recognized ordinary save/load'],90:['factory/no-custom versus saved-custom','Explorer Windows/Finder Mac'],91:['no-selected-preset','first audio-effect AUDIO','instrument MIDI','No rollback'],92:['recognized EXISTING','no Options file is edited/created','string presence alone is not recognition','paired productive control'],93:['EXCEPT Sampler','EXPANDED Zone Editor','Drum Sampler','Impulse','sample-button, browser-X, Esc, Q'],94:['known custom Info View text','save AND reload','PMW026–028'],95:['ORIGINAL device name','recognized load','second default','context Delete versus selected browser Delete'],96:['parameter LIST only','NOT parameter VALUES','AU and VST','PH017'],97:['Default Audio Track/Default MIDI Track','correct-name recognition','Default Set/template'],98:['empty Sampler then separately Simpler','independently productive and distinct BEFORE','LAST ADDED'],99:['empty Sampler versus Simpler','genuinely productive controls','NONEMPTY generated notes'],100:['ATM036/037','single instrument OR Instrument Rack','nonnested Drum Rack','productive recognition BEFORE','NONEMPTY recognized notes'],101:['successful recognized but distinct','Default.appc-containing plugin FOLDER','Library destination','fileoperation/atomicity/path/codec/override failures null']}
 for n,phrases in checks.items():
  for phrase in phrases:assert phrase in actions[n],f'{n}missing:{phrase}'
 assert 'not automatically re-enable' in p['new_contracts'][1]['contract'],'autoenable'
 assert 'PARAMETER context' in p['new_contracts'][1]['contract'],'globalenable'
 assert 'LIST' in p['new_contracts'][4]['contract'] and 'VALUES' in p['new_contracts'][4]['contract'],'configvalues'
 assert 'single instrument OR an Instrument Rack' in p['new_contracts'][8]['contract'],'forcedrack'
 assert all(g['complete'] is False and g['coverage_credit']==0 for g in p['groups'])


def fixtures(p,c):
 mutations=[('erase-oldcase',lambda a,b:b[47].update(setup_action='label only')),('inventactual',lambda a,b:b[81].update(actual_expected='pass')),('meterflag-only',lambda a,b:b[84].update(setup_action=b[84]['setup_action'].replace('nonzero known input AND','enabled flag'))),('fold-tracktitle',lambda a,b:b[82].update(setup_action=b[82]['setup_action'].replace('DEVICE title','track title'))),('triangle-all-devices',lambda a,b:b[85].update(setup_action=b[85]['setup_action'].replace('actually offered functioning','universal'))),('triangle-inferredgesture',lambda a,b:b[85].update(setup_action=b[85]['setup_action'].replace('not a gesture inferred from the triangle icon','click triangle because icon'))),('AB-no-distinct-state',lambda a,b:b[86].update(setup_action=b[86]['setup_action'].replace('two genuinely distinguishable','two named'))),('global-reenable',lambda a,b:b[87].update(setup_action=b[87]['setup_action'].replace('PARAMETER context','global transport'))),('stored-envelope-only',lambda a,b:b[87].update(setup_action=b[87]['setup_action'].replace('active changing automation contribution','stored envelope'))),('autoreenable',lambda a,b:a['new_contracts'][1].update(contract=a['new_contracts'][1]['contract'].replace('not automatically re-enable','automatically re-enable'))),('all-samples-hover',lambda a,b:b[92].update(setup_action=b[92]['setup_action'].replace('EXCEPT Sampler','including Sampler'))),('Options-write',lambda a,b:b[91].update(setup_action=b[91]['setup_action'].replace('no Options file is edited/created','write Options file now'))),('config-values',lambda a,b:b[95].update(setup_action=b[95]['setup_action'].replace('NOT parameter VALUES','retained parameter VALUES'))),('timestamp-winner',lambda a,b:b[97].update(setup_action=b[97]['setup_action'].replace('LAST ADDED','newest timestamp'))),('empty-preview',lambda a,b:b[99].update(setup_action=b[99]['setup_action'].replace('NONEMPTY recognized notes','clip flag'))),('negative-before-recognition',lambda a,b:b[94].update(setup_action=b[94]['setup_action'].replace('recognized load','folder exists'))),('forced-pitchedrack',lambda a,b:a['new_contracts'][8].update(contract=a['new_contracts'][8]['contract'].replace('single instrument OR an Instrument Rack','Instrument Rack only'))),('newcompletion',lambda a,b:a['groups'][0].update(complete=True))]
 for name,change in mutations:
  a,b=copy.deepcopy(p),copy.deepcopy(c);change(a,b)
  try:safe(a,b)
  except AssertionError:continue
  raise AssertionError('mutation accepted:'+name)
 # Explicit retained positives reject erasing genuine old subsets by exact equality.
 for n in [48,49,50,51,52,66]:assert c[n-1]==j(D/'cases-r3.json')['cases'][n-1]
 return [x[0] for x in mutations]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true',required=True);ap.parse_args()
 inp=j(D/'inputs-r4.json');prior=j(D/'prior-files-r4.json');p=j(D/'adoption-r4.json');c=j(D/'cases-r4.json')['cases']
 paths={q['path'] for q in inp['files']+prior}|{str(x.relative_to(ROOT)) for x in D.iterdir() if x.is_file()}|{'wiki/specs/device-racks.md','wiki/research/device-racks.md'}
 before={q:digest(ROOT/q) for q in paths}
 for q in inp['files']+prior:assert digest(ROOT/q['path'])==q,q['path']
 assert len(prior)==49
 assert sum(x['criterion_domain']=='installed-document' for x in c)==3 and sum(x['criterion_domain']=='Live-12-documented' for x in c)==86 and sum(x['criterion_domain']=='unknown' for x in c)==12
 assert (D/'spec-before-r4.md').read_bytes()==(D/'spec-r3.md').read_bytes()
 assert (D/'research-before-r4.md').read_bytes()==(D/'research-r3.md').read_bytes()
 author=module(D/'author-r4.py','r4author')
 for n,b in author.build().items():assert (D/n).read_bytes()==b,n
 assert (ROOT/'wiki/specs/device-racks.md').read_bytes()==(D/'spec-r4.md').read_bytes()
 assert (ROOT/'wiki/research/device-racks.md').read_bytes()==(D/'research-r4.md').read_bytes()
 req=j(D/'requirements-r4.json');old=j(D/'requirements-r3.json');assert len(req)==38
 for i in range(28):
  if i not in [22,23,24,25]:assert req[i]==old[i]
  else:assert req[i]['contract'].startswith(old[i]['contract'].rstrip())
 assert [x['id'] for x in req]==[f'REQ-DEVICE-RACKS-{n:03}' for n in range(1,39)]
 safe(p,c);negative=fixtures(p,c)
 audit=j(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/device-chain-source-audit/audit.json');assert len(audit['blocks'])==153
 parser=module(ROOT/'analysis/ableton-live-12.4.3/full-spec-v1/clip-view-source-audit/source_parser.py','pinnedpureparser')
 blocks,res=parser.extract((D/'manual-devices-2026-10-19.html').read_text(),'DEVICES')
 assert blocks==audit['blocks'],'source changed'
 assert res==[{k:v for k,v in r.items() if k not in {'complete','pixels_or_destination_inspected','role','target'}} for r in audit['resources']],'resource projection changed'
 pointer_count=0
 for row in c[81:]+req[28:]:
  for ref in row['source_contexts']:
   value=audit
   for k in ref['json_pointer'].strip('/').split('/'):value=value[int(k)] if isinstance(value,list) else value[k]
   assert value['id']==ref['block'];pointer_count+=1
  if 'source_claim' in row:assert row['source_claim']==' '.join(audit['blocks'][int(ref['block'][-3:])-1]['text'] for ref in row['source_contexts'])
 for row in c:assert all(x in {q['id'] for q in req} for x in row['requirements'])
 status=j(D/'actual-status-r4.json')['cases'];assert len(status)==101
 assert all(x['actual_expected'] is None and x['actual_comparison'] is None and x['executed'] is False and x['target']=='U' and x['complete'] is False for x in status)
 # Actual existing Browser parser, AST-limited to four inspected pure functions.
 tree=ast.parse((ROOT/'tools/spec_browser.py').read_text());selected=[x for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name in {'anchor','frontmatter','cells','spec_rows'}]
 assert len(selected)==4;ns={'re':re};exec(compile(ast.Module(body=selected,type_ignores=[]),'inspected-browser-pure-functions','exec'),ns)
 found=ns['spec_rows'](ROOT/'wiki/specs/device-racks.md',(D/'spec-r4.md').read_text());assert {x['id'] for x in found}=={x['id'] for x in req} and len(found)==38
 links=0
 for n,base in [('spec-r4.md',ROOT/'wiki/specs'),('research-r4.md',ROOT/'wiki/research')]:
  for dest in re.findall(r'\]\(([^)\s]+)\)',(D/n).read_text()):
   if re.match(r'^[a-z]+:',dest) or dest.startswith('#'):continue
   assert (base/dest.split('#')[0]).exists(),dest;links+=1
 for n in [*author.build().keys(),'author-r4.py','check-r4.py','README-r4.md']:
  text=(D/n).read_text();assert all(line.rstrip()==line for line in text.splitlines()),n
 if (D/'manifest-author-r4.json').exists():
  m=j(D/'manifest-author-r4.json')
  for q in m['files']:assert digest(ROOT/q['path'])==q,q['path']
 after={q:digest(ROOT/q) for q in paths};assert before==after,'readonly mutation'
 print(json.dumps(dict(status='pass',prior_files=49,input_pins=len(inp['files']),requirements=38,cases=101,old_cases_exact=81,new_cases=20,criterion_classes={'installed':3,'D12':86,'U':12},new_named_UI_pairs=7,new_null_pairs=13,actual_nonnull=0,executed=0,complete=0,source_blocks=153,resources=140,source_pointers=pointer_count,groups=20,Browser_IDs=len(found),links=links,negative_fixtures=negative,retained_positive_subsets=[48,49,50,51,52,66],watched_paths=len(paths),all_unchanged=True,writes=False),indent=2))
if __name__=='__main__':main()
