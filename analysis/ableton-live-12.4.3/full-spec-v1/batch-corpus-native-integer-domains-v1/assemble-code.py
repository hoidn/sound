import pathlib
B=pathlib.Path('/home/ollie/Documents/sound/analysis/ableton-live-12.4.3/full-spec-v1');P=B/'batch-corpus-native-integer-domains-v1';OLD=B/'batch-corpus-deterministic-free-lfo-continuation-v1'
source=(OLD/'record.py').read_text();source=source.replace('Fixed two-child continuation Corpus recording.','Whole57-child native integer-domain Corpus recording.').replace("NAMES={0:'Sine',1:'Square',2:'Triangle',3:'Ramp Up',4:'Ramp Down'}",'')
start=source.index('def validate(d):');end=source.index('def parse_output(')
validation='''def planned_script(u):
 return '\\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {w["index"]} {w["token"]}' for w in u['words']]+['inflag 1','input '+str(H/'input.f32'),'process 16384 512','destroy'])+'\\n'
def vector_sha(params):return sha(b''.join(struct.pack('<f',float(x)) for x in params))
def validate(d):
 e=json.loads((H/'eligibility.json').read_text());prior=json.loads((H/'approved-prior-summary.json').read_text())
 assert d['schema']=='whole-Corpus-native-integer-domains-v1' and d['domains']==e['domains'] and d['base_params']==e['base_params']
 assert d['counts']=={'aliases':69,'unique_vectors':63,'inherited_vectors':6,'fresh_children':57,'direct_exports':4161,'CalcA':1824,'stereo_bytes':7471104}
 assert [(x['index'],int(x['max'])) for x in d['domains']]==[(0,6),(10,24),(17,1),(18,6),(21,21),(27,1),(33,3)]
 assert d['fixture']=={'rate':44100,'frames':16384,'block':512,'last_block':512,'inflag':1,'I1_impulse_frame':4096,'transport':[0,0,120],'MXCSR':'0x1f80','warmup':0,'XDEV_TIME':'0','XDEV_LIBM_ULP':'0'}
 assert d['baseline_vector_sha256']==vector_sha(d['base_params'])=='9b98e8cab7aae28b01e18de3cd9570db62721f0ecdbf951bd5bd77d8b378e6e2'
 assert ident(H/'input.f32')==d['input'] and d['input']['bytes']==131072 and d['input']['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
 assert len(d['catalog'])==69 and len(d['vectors'])==63 and len(d['plans'])==57
 expected_pairs=[(x['index'],v) for x in d['domains'] for v in range(int(x['max'])+1)];assert [(r['index'],r['value']) for r in d['catalog']]==expected_pairs
 seen={};aliases={};hist={}
 for p in prior['approved_summary']['approved_points']:
  params=d['base_params'].copy();params[18]=p['shape'];h=vector_sha(params)
  assert [bits(x) for x in params]==p['parameter_bits32'];hist[h]=('approved-summary-no-replay',p)
 params=d['base_params'].copy();params[18]=5.;hist[vector_sha(params)]=('qualified-historical-shape5-metadata-only',prior['shape5_qualified_reference'])
 for i,(row,erow) in enumerate(zip(d['catalog'],e['catalog'])):
  assert row['id']==f'CNI-A{i:03}' and row['index']==erow['index'] and row['value']==erow['value'] and type(row['value']) is int
  params=d['base_params'].copy();params[row['index']]=float(row['value']);h=vector_sha(params);assert row['vector_sha256']==h==erow['vector_sha256']
  if h not in seen:seen[h]=f'CNI-V{len(seen):03}'
  assert row['vector_id']==seen[h];aliases.setdefault(row['vector_id'],[]).append(row['id'])
  assert all(row[k] is None for k in ['new_expected_waveform','portable_expected','portable_comparator','grade'])
 assert [u['id'] for u in d['vectors']]==list(seen.values()) and len(set(u['vector_sha256'] for u in d['vectors']))==63
 fresh=[]
 for u in d['vectors']:
  assert u['alias_ids']==aliases[u['id']] and [w['index'] for w in u['words']]==list(range(38))
  params=[float(w['token']) for w in u['words']];assert vector_sha(params)==u['vector_sha256']
  i=u['first_alias']['index'];v=u['first_alias']['value'];expected=d['base_params'].copy();expected[i]=float(v);assert [bits(x) for x in params]==[bits(x) for x in expected]
  assert all(w['binary32_le']==struct.pack('<f',float(w['token'])).hex() and w['host_reconstructed_binary64_le']==struct.pack('<d',float(w['token'])).hex() for w in u['words'])
  assert all(u[k] is None for k in ['new_expected_waveform','portable_expected','portable_comparator','grade'])
  if u['vector_sha256'] in hist:
   assert u['disposition']=='inherited-no-replay' and 'script' not in u and u['inherited'] is not None
   h=u['inherited'];assert h['kind']==hist[u['vector_sha256']][0] and h['fresh_pid'] is h['fresh_receipt'] is h['new_metrics'] is None
   if h['kind']=='approved-summary-no-replay':assert h['approved_point']==hist[u['vector_sha256']][1]
   else:assert h['historical']==hist[u['vector_sha256']][1] and h['qualification']==h['historical']['qualification']
  else:
   assert u['disposition']=='fresh-selected' and u['inherited'] is None;fresh.append(u['id']);assert ident(u['script']['path'])==u['script'];assert pathlib.Path(u['script']['path'])==H/'scripts'/(u['id']+'.script') and pathlib.Path(u['script']['path']).read_text()==planned_script(u)
 assert [p['vector_id'] for p in d['plans']]==fresh and len(hist)==6
 byid={u['id']:u for u in d['vectors']}
 for p in d['plans']:assert p=={'vector_id':p['vector_id'],'vector_sha256':byid[p['vector_id']]['vector_sha256'],'script':byid[p['vector_id']]['script'],'direct_exports':73,'CalcA':32,'output_bytes':131072}

def input_controls(d):
 tests=[('omit-alias',lambda x:x['catalog'].pop()),('omit-vector',lambda x:x['vectors'].pop()),('omit-plan',lambda x:x['plans'].pop()),('domain-missing',lambda x:x['domains'].pop()),('domain-crossproduct',lambda x:x['domains'][0].update(max=7)),('domain-virtual',lambda x:x['domains'][0].update(virtual=True)),('alias-duplicate',lambda x:x['catalog'][1].update(value=0)),('alias-fractional',lambda x:x['catalog'][0].update(value=.5)),('wrong-vector-link',lambda x:x['catalog'][0].update(vector_id='CNI-V002')),('baseline-dropped',lambda x:x['catalog'][2].update(vector_sha256='0'*64)),('word38-missing',lambda x:x['vectors'][0]['words'].pop()),('fixed-other-word',lambda x:x['vectors'][0]['words'][1].update(token='0.0')),('wrong-f32',lambda x:x['vectors'][0]['words'][0].update(binary32_le='0000803f')),('wrong-f64',lambda x:x['vectors'][0]['words'][0].update(host_reconstructed_binary64_le='000000000000f03f')),('invented-prior',lambda x:x['vectors'][0].update(new_expected_waveform='law')),('portable-expected',lambda x:x['catalog'][0].update(portable_expected='law')),('portable-comparator',lambda x:x['vectors'][0].update(portable_comparator='exact')),('grade',lambda x:x['catalog'][0].update(grade='PASS')),('seed',lambda x:x['fixture'].update(XDEV_TIME='1')),('inflag',lambda x:x['fixture'].update(inflag=0)),('impulse',lambda x:x['fixture'].update(I1_impulse_frame=0)),('rate',lambda x:x['fixture'].update(rate=48000)),('count',lambda x:x['counts'].update(fresh_children=63))]
 old=next(i for i,u in enumerate(d['vectors']) if u['inherited'] is not None);sah=next(i for i,u in enumerate(d['vectors']) if u['inherited'] and u['inherited']['kind']=='qualified-historical-shape5-metadata-only')
 tests += [('replay-inherited',lambda x:x['plans'][0].update(vector_id=x['vectors'][old]['id'])),('invent-old-PID',lambda x:x['vectors'][old]['inherited'].update(fresh_pid=1)),('drop-shape5-qualification',lambda x:x['vectors'][sah]['inherited'].update(qualification='proved'))]
 out=[]
 for name,mut in tests:
  x=copy.deepcopy(d);mut(x)
  try:validate(x)
  except (AssertionError,KeyError,IndexError,ValueError):out.append(name)
  else:raise AssertionError('accepted '+name)
 return out

'''
source=source[:start]+validation+source[end:]
source=source.replace("vector=d['base_params'].copy();vector[18]=p['shape']","vector=[float(w['token']) for w in next(u for u in d['vectors'] if u['id']==p['vector_id'])['words']]")
source=source.replace("assert commands[43:]==['inflag 1',next(l for l in commands if l.startswith('input ')),'process 16384 512 flags: 32x(ret=0,flag=1) blocks=32','destroy','cxx-failbits 0']\n assert commands[44]=='input '+d['base_script'].split('\\ninput ')[1].splitlines()[0]", "assert commands[43:45]==['inflag 1','input '+str(H/'input.f32')] and commands[46:]==['destroy','cxx-failbits 0']\n m=re.fullmatch(r'process 16384 512 flags:((?: [1-9][0-9]*x\\(ret=-?\\d+,flag=-?\\d+\\))+ blocks=32)',commands[45]);assert m\n groups=[list(map(int,g)) for g in re.findall(r'(\\d+)x\\(ret=(-?\\d+),flag=(-?\\d+)\\)',commands[45])];assert sum(g[0] for g in groups)==32 and all(g[1]==0 and g[2] in (0,1) for g in groups)")
source=source.replace("'shape':p['shape']","'vector_id':p['vector_id'],'CalcA_groups':groups")
source=source.replace("(H/'manifest-before.json')","(H/'pre-call-manifest.json')")
source=source.replace('def run(d):','def run(d,prehash):\n assert sha((H/\'pre-call-manifest.json\').read_bytes())==prehash')
source=source.replace("directory=H/'attempts'/f'shape-{plan[\"shape\"]}'","directory=H/'attempts'/plan['vector_id']")
source=source.replace("plan['script'],str(output)","plan['script']['path'],str(output)")
source=source.replace("{'shape':plan['shape'],","{'vector_id':plan['vector_id'],")
source=source.replace("print('shape',plan['shape'],","print('vector',plan['vector_id'],")
source=source.replace("else:assert sys.argv[1:]==['--run-once'];run(d)","else:assert len(sys.argv)==3 and sys.argv[1]=='--run-once';run(d,sys.argv[2])")
source=source.replace("assert rc==0 and stderr=='';imports=[]","assert rc==0 and stderr=='' and not re.search(r'\\b(TRAP|FAULT)\\b',text);imports=[]")
(P/'record.py').write_text(source)
# Reuse the fully reviewed ordinary launcher source only; new file freezes before calls.
(P/'launch-once.py').write_bytes((B/'batch-electric-velocity-bytes-v1/launch-once.py').read_bytes())
print({'record_lines':len(source.splitlines()),'original_calls':0})
