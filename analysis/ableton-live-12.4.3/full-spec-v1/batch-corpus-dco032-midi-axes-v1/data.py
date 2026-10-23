"""Owned DCO032 four independent MIDI-axis Corpus inputs/protocol/unsigned data; no oldmodule imports."""
import collections,copy,hashlib,json,re,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
def identity(path):
 p=Path(path);b=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def metrics(raw):
    # Already used unsigned finite/zero/channel representation summary; no float estimator.
    assert len(raw) > 0 and len(raw) % 8 == 0
    pairs = list(struct.iter_unpack('<II', raw))
    nonfinite = sum((v & 0x7f800000) == 0x7f800000 for pair in pairs for v in pair)
    return {'frames': len(pairs), 'all_finite': nonfinite == 0, 'nonfinite_scalar_count': nonfinite,
            'channels_byte_identical': all(l == r for l, r in pairs),
            'nonzero_sample_counts': [sum((pair[c] & 0x7fffffff) != 0 for pair in pairs) for c in (0, 1)],
            'negative_zero_sample_counts': [sum(pair[c] == 0x80000000 for pair in pairs) for c in (0, 1)]}


def protocol(log,row,c):
 assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)',log)
 imports=[];exports={};used={};inits=[];commands=[]
 for line in log.splitlines():
  if line.startswith('init '):assert re.fullmatch(r'init 0x[0-9a-f]+',line);inits.append(line.split()[1])
  elif line.startswith('import '):
   m=re.fullmatch(r'import (linux|data|trap) (\S+) slots=(\d+)',line);assert m;imports.append({'binding':m[1],'symbol':m[2],'slots':int(m[3])})
  elif line.startswith('export '):
   m=re.fullmatch(r'export (\S+) (0x[0-9a-f]+)',line);assert m and m[1] not in exports;exports[m[1]]=m[2]
  elif line.startswith('used '):
   m=re.fullmatch(r'used (\S+) ([1-9][0-9]*)',line);assert m and m[1] not in used;used[m[1]]=int(m[2])
  else:commands.append(line)
 assert imports==c['approved_import_declarations'] and len(imports)==len({x['symbol'] for x in imports})==127
 assert dict(collections.Counter(x['binding'] for x in imports))=={'linux':99,'trap':21,'data':7}
 assert exports==c['approved_export_declarations'] and used and all(x in {y['symbol'] for y in imports if y['binding']=='linux'} for x in used)
 assert inits==c['approved_initializer_entries']
 assert commands[:4]==['slice offset=16384 size=250352','mxcsr 0x1f80','transport 0 0 120','create ok']
 m=re.fullmatch(r'rate 44100 ret=(-?\d+)',commands[4]);assert m;rate=int(m[1])
 assert len(commands)==50
 for i,line in enumerate(commands[5:43]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and struct.pack('<f',float(m[2])).hex()==row['parameter_f32_bits_le'][i]
 for j,(fr,st,k,v) in enumerate(row['events']):assert commands[43+j]==f'event {fr} {hex(st)} {k} {v}'
 assert commands[45:47]==['inflag 1','input '+c['input_source']['path']] and commands[48:]==['destroy','cxx-failbits 0']
 m=re.fullmatch(r'process 16384 512 flags:((?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+ blocks=32)',commands[47]);assert m
 groups=[{'blocks':int(n),'return':int(r),'flag':int(f)} for n,r,f in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',commands[47])];assert sum(x['blocks'] for x in groups)==32 and all(x['return']==0 and x['flag'] in (0,1) for x in groups)
 return {'initializer_entries_logged':inits,'selected_direct_exports_from_script_protocol':73,'nested_original_calls':None,'rate_return_logged':rate,'flags':groups,'exports_declared_not_all_invoked':exports,'import_declarations':imports,'actual_used_code_import_counts':used,'cxx_failbits':0}

def planned(row,c):
 return '\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {i} {t}' for i,t in enumerate(c['parameter_tokens'])]+[f'event {fr} {hex(st)} {k} {v}' for fr,st,k,v in row['events']]+['inflag 1','input '+c['input_source']['path'],'process 16384 512','destroy'])+'\n'

def validate(c):
 e=json.loads((HERE/'eligibility.json').read_text())
 assert len(c['rows'])==397 and c['aliases']==e['aliases'] and len(c['aliases'])==400
 assert [(a['axis'],a['value']) for a in c['aliases']]==[(axis,v) for axis,n in [('on_key',128),('on_velocity',128),('matching_channel',16),('off_velocity',128)] for v in range(n)]
 assert c['full_ordered38_words']==e['full_ordered38_words'] and c['fixed_history']==e['fixed_history']
 assert c['parameter_tokens']==[w['token'] for w in e['full_ordered38_words']]
 assert [struct.pack('<f',float(t)).hex() for t in c['parameter_tokens']]==c['parameter_f32_bits_le']
 assert [struct.pack('<d',float(t)).hex() for t in c['parameter_tokens']]==c['parameter_f64_reconstructed_le']
 assert hashlib.sha256(bytes.fromhex(''.join(c['parameter_f32_bits_le']))).hexdigest()==c['parameter_vector_sha256']=='351eb39550097c4d432e53db67460f1e50b35533e34841a90438ab2e31256060'
 assert hashlib.sha256(bytes.fromhex(''.join(c['parameter_f64_reconstructed_le']))).hexdigest()==c['parameter_token_binary64_sha256']=='1855a118565d354015e7ba29929bba2152a57f5a3507885ee1050e37b7ec8a6a'
 assert c['environment']=={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','XDEV_TIME':'0'}
 assert c['limits']=={'children':396,'wall_seconds':20,'cpu_seconds':20,'core':0,'file_size':4194304,'selected_export_calls_total':28908,'CalcA_total':12672,'new_stereo_bytes_total':51904512,'all_native_calls':None}
 assert identity(HERE/'input.f32')==c['input'] and c['input']['sha256']==e['I1_input']['sha256'] and c['input_source']==e['I1_input']
 assert c['parent_exec_argv']==['/home/ollie/miniconda3/bin/python3.13','-I','-B',str(HERE/'run_batch.py'),'--run-once']
 seen=set();fresh=old=0
 for i,(row,h) in enumerate(zip(c['rows'],e['histories'])):
  assert row['id']==f'C32-U{i:03d}' and row['unique_vector']==i and row['eligibility_history']==h and row['history_sha256']==h['history_sha256'] and row['first_alias']==f"{h['first_axis']}:{h['first_value']}"
  assert row['events']==h['events'] and len(row['events'])==2 and row['packed16_events_le']==h['packed16_events_le']
  assert [struct.pack('<qBBBBI',f,s,k,v,0,0).hex() for f,s,k,v in row['events']]==row['packed16_events_le']
  assert row['history_sha256'] not in seen;seen.add(row['history_sha256'])
  for field in ['parameter_tokens','parameter_f32_bits_le','parameter_f64_reconstructed_le','parameter_vector_sha256','parameter_token_binary64_sha256']:assert row[field]==c[field]
  assert all(row[k] is None for k in ['waveform_prediction','portable_expected','portable_comparator','candidate_grade']) and row['new_application_predicate_proof'] is False
  if h['existing_case_refs']:
   old+=1;r=row['historical'];assert row['disposition']=='inherited-no-replay' and 'script' not in row and 'fresh_ordinal' not in row and r['eligibility_row']==h and r['existing_case_refs']==['DCO-032'] and r['input_approval_only'] is True and r['no_old_modal_budget_transfer'] is True and r['old_audio_reads']==0
   assert r['fresh_pid'] is r['fresh_receipt'] is r['new_metrics'] is None
  else:
   fresh+=1;assert row['disposition']=='fresh-planned' and row['historical'] is None and row['fresh_ordinal']==fresh
   raw=planned(row,c).encode();assert Path(row['script']['path']).read_bytes()==raw and identity(row['script']['path'])==row['script'] and len(raw)==h['script_utf8_bytes'] and hashlib.sha256(raw).hexdigest()==h['script_utf8_sha256']
 assert fresh==396 and old==1 and len(seen)==397
 assert [r['id'] for r in c['rows'] if r['historical']]==['C32-U060']
 assert len([a for a in c['aliases'] if a['history_sha256']==e['baseline_history_sha256']])==4
 assert {a['history_sha256'] for a in c['aliases']}==seen

def parent_valid(r,c,pid,pre):
 assert type(r['pid']) is int and r['pid']>0 and r['pid']==pid and r['exec_argv']==c['parent_exec_argv'] and r['exec_environment']==c['environment'] and r['pre_call_manifest']==pre and r['core_limit']==[0,0]

def synthetic(c,row,rate=1):
 return 'slice offset=16384 size=250352\n'+''.join(f"import {a['binding']} {a['symbol']} slots={a['slots']}\n" for a in c['approved_import_declarations'])+''.join(f'export {a} {v}\n' for a,v in c['approved_export_declarations'].items())+'mxcsr 0x1f80\ntransport 0 0 120\ncreate ok\n'+f'rate 44100 ret={rate}\n'+''.join(f'param {i} {t}\n' for i,t in enumerate(row['parameter_tokens']))+''.join(f'event {f} {hex(s)} {k} {v}\n' for f,s,k,v in row['events'])+'inflag 1\ninput '+c['input_source']['path']+'\nprocess 16384 512 flags: 32x(ret=0,flag=1) blocks=32\ndestroy\ncxx-failbits 0\n'+f"used {next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux')} 1\n"

def selfchecks(c):
 validate(c);neg=[]
 for name,mut in [('omitHistory',lambda x:x['rows'].pop()),('omitAlias',lambda x:x['aliases'].pop()),('parameterOnlyDedup',lambda x:x['rows'].__setitem__(1,copy.deepcopy(x['rows'][0]))),('roundedOwnerTokens',lambda x:x['parameter_tokens'].__setitem__(15,repr(struct.unpack('<f',bytes.fromhex(x['parameter_f32_bits_le'][15]))[0]))),('wrongF64',lambda x:x['parameter_f64_reconstructed_le'].__setitem__(15,'0'*16)),('wrongHeldVector',lambda x:x.update(parameter_vector_sha256='613d0f49d678f947d847f2a4d56767881c63f370f07f2a8fdd2a172d4875b8a1')),('LIBMnotUnset',lambda x:x['environment'].update(XDEV_LIBM_ULP='0')),('wrongOnFrame',lambda x:x['rows'][0]['events'][0].__setitem__(0,1536)),('falseMatchingOffKey',lambda x:x['rows'][0]['events'][1].__setitem__(2,0)),('wrongOffFrame',lambda x:x['rows'][0]['events'][1].__setitem__(0,3072)),('dropOff',lambda x:x['rows'][0]['events'].pop()),('crossproduct',lambda x:x['rows'][0]['events'][0].__setitem__(3,1)),('wrongPacking',lambda x:x['rows'][0]['packed16_events_le'].__setitem__(1,'0'*32)),('inventPrior',lambda x:x['rows'][0].update(waveform_prediction='law')),('portableCriterion',lambda x:x['rows'][0].update(portable_comparator='modal')),('newApplicationProof',lambda x:x['rows'][0].update(new_application_predicate_proof=True)),('inventOldPID',lambda x:x['rows'][60]['historical'].update(fresh_pid=1)),('replayBaseline',lambda x:x['rows'][60].update(disposition='fresh-planned')),('transferModalBudget',lambda x:x['rows'][60]['historical'].update(no_old_modal_budget_transfer=False)),('wrongChildCount',lambda x:x['limits'].update(children=397)),('changedParentArgv',lambda x:x['parent_exec_argv'].append('--retry'))]:
  bad=copy.deepcopy(c);mut(bad);assert bad!=c
  try:validate(bad)
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('accepted '+name)
 row=c['rows'][0];text=synthetic(c,row);protocol(text,row,c);pn=[]
 for name,a,b in [('wrongOn','event 1537','event 1536'),('wrongOnStatus','0x90 0 100','0x91 0 100'),('wrongOnKey','0x90 0 100','0x90 1 100'),('wrongOnVelocity','0x90 0 100','0x90 0 0'),('wrongOffKey','0x80 60 64','0x80 0 64'),('wrongOffVelocity','0x80 60 64','0x80 60 0'),('missingOff','event 3073 0x80 60 64\n',''),('FP','mxcsr 0x1f80','mxcsr 0x3f80'),('transport','transport 0 0 120','transport 1 0 120'),('flag','ret=0,flag=1','ret=0,flag=4'),('cxx','cxx-failbits 0','cxx-failbits 1')]:
  bad=text.replace(a,b);assert bad!=text
  try:protocol(bad,row,c)
  except (AssertionError,IndexError,KeyError):pn.append(name)
  else:raise AssertionError('accepted protocol '+name)
 code=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux');data=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='data');bad=text.replace(f'used {code} 1',f'used {data} 1');assert bad!=text
 try:protocol(bad,row,c)
 except AssertionError:pn.append('dataAsCodeChanged')
 else:raise AssertionError('accepted data-as-code')
 for rate in [-2147483648,0,2147483647]:assert protocol(synthetic(c,row,rate),row,c)['rate_return_logged']==rate
 for axis,value in [('on_key',127),('on_velocity',0),('matching_channel',15),('off_velocity',127)]:
  h=next(a['history_sha256'] for a in c['aliases'] if a['axis']==axis and a['value']==value);r=next(r for r in c['rows'] if r['history_sha256']==h);protocol(synthetic(c,r),r,c)
 pre={'bytes':123,'sha256':'a'*64};r={'pid':123,'exec_argv':c['parent_exec_argv'],'exec_environment':c['environment'],'pre_call_manifest':pre,'core_limit':[0,0]};parent_valid(r,c,123,pre);parentneg=[]
 for name,mut in [('wrongPID',lambda x:x.update(pid=0)),('wrongArgv',lambda x:x['exec_argv'].append('--retry')),('wrongEnv',lambda x:x['exec_environment'].update(XDEV_TIME='1')),('wrongPreSeal',lambda x:x['pre_call_manifest'].update(sha256='b'*64)),('coreEnabled',lambda x:x.update(core_limit=[1,1]))]:
  bad=copy.deepcopy(r);mut(bad);assert bad!=r
  try:parent_valid(bad,c,123,pre)
  except AssertionError:parentneg.append(name)
  else:raise AssertionError('accepted parent '+name)
 assert metrics(struct.pack('<II',0,0))['all_finite'] and metrics(struct.pack('<II',0x80000000,0))['negative_zero_sample_counts']==[1,0]
 assert not metrics(struct.pack('<II',0,0x7f800001))['all_finite'] and not metrics(struct.pack('<II',0,1))['channels_byte_identical']
 for raw in [b'',b'1234']:
  try:metrics(raw)
  except AssertionError:pass
  else:raise AssertionError('accepted malformed stereo')
 return {'input_negatives':neg,'protocol_negatives':pn,'precall_parent_negatives':parentneg,'opaque_Rate_positives':[-2147483648,0,2147483647],'edge_protocols':['Onkey127','Onvelocity0','matchingchannel15','Offvelocity127'],'unsigned_groups':['positivezero','negativezero','rightsignalingNaN','rightsubnormal','emptyshape','halfstereoshape'],'400aliases397wholehistories':True,'fourBaselineAliasesOneInputReferenceNoReplay':True,'original_decimal_f64_exact':True,'LIBM_ULP_UNSET':True}
