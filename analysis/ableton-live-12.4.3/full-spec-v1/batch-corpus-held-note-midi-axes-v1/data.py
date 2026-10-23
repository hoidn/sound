"""Owned complete14axis Corpus inputs/protocol/unsigned data; no oldmodule imports."""
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
 assert len(commands)==49
 for i,line in enumerate(commands[5:43]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and struct.pack('<f',float(m[2])).hex()==row['parameter_f32_bits_le'][i]
 assert commands[43]==f"event {row['events'][0][0]} {hex(row['events'][0][1])} {row['events'][0][2]} {row['events'][0][3]}"
 assert commands[44:46]==['inflag 1','input '+c['input_source']['path']] and commands[47:]==['destroy','cxx-failbits 0']
 m=re.fullmatch(r'process 16384 512 flags:((?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+ blocks=32)',commands[46]);assert m
 groups=[{'blocks':int(n),'return':int(r),'flag':int(f)} for n,r,f in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',commands[46])];assert sum(x['blocks'] for x in groups)==32 and all(x['return']==0 and x['flag'] in (0,1) for x in groups)
 return {'initializer_entries_logged':inits,'selected_direct_exports_from_script_protocol':73,'nested_original_calls':None,'rate_return_logged':rate,'flags':groups,'exports_declared_not_all_invoked':exports,'import_declarations':imports,'actual_used_code_import_counts':used,'cxx_failbits':0}

def planned(row,c):
 f,st,k,v=row['events'][0]
 return '\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {i} {t}' for i,t in enumerate(c['parameter_tokens'])]+[f'event {f} {hex(st)} {k} {v}','inflag 1','input '+c['input_source']['path'],'process 16384 512','destroy'])+'\n'

def validate(c):
 e=json.loads((HERE/'eligibility.json').read_text());needkeys=[(a['axis'],a['value']) for a in c['aliases']]
 assert needkeys==[('note_key',i) for i in range(128)]+[('note_on_velocity',i) for i in range(128)]+[('channel_nibble',i) for i in range(16)]
 assert len(c['rows'])==270 and len(c['aliases'])==272 and c['aliases']==e['aliases']
 assert c['full_ordered38_words']==e['full_ordered38_words'] and c['fixed_history']==e['fixed_history']
 assert c['parameter_tokens']==[w['token'] for w in e['full_ordered38_words']]
 assert [struct.pack('<f',float(x)).hex() for x in c['parameter_tokens']]==c['parameter_f32_bits_le'] and [struct.pack('<d',float(x)).hex() for x in c['parameter_tokens']]==c['parameter_f64_reconstructed_le']
 assert hashlib.sha256(bytes.fromhex(''.join(c['parameter_f32_bits_le']))).hexdigest()==c['parameter_vector_sha256']=='613d0f49d678f947d847f2a4d56767881c63f370f07f2a8fdd2a172d4875b8a1'
 assert hashlib.sha256(bytes.fromhex(''.join(c['parameter_f64_reconstructed_le']))).hexdigest()==c['parameter_token_binary64_sha256']=='1c0495901fdb45b2e3d8c47034fe9fa80fdabd375d2e945ec3a8e31d4fdf7863'
 assert c['environment']=={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC','XDEV_TIME':'0'} and 'XDEV_LIBM_ULP' not in c['environment']
 assert c['limits']['children']==268 and c['limits']['selected_export_calls_total']==19564 and c['limits']['CalcA_total']==8576 and c['limits']['new_stereo_bytes_total']==35127296
 assert identity(HERE/'input.f32')==c['input'] and c['input']['sha256']==e['fixed_history']['input']['sha256'] and c['input_source']==e['fixed_history']['input']
 seen=set();fresh=0;old=0
 for i,(row,h) in enumerate(zip(c['rows'],e['histories'])):
  assert row['id']==h['id']==f'CHM-U{i:03d}' and row['unique_vector']==i and row['first_alias']==h['first_alias'] and row['history_sha256']==h['history_sha256'] and row['whole_history']==h['whole_history']
  assert row['events']==[h['event']] and len(row['events'])==1 and row['packed16_event_le']==h['packed16_event_le']
  fr,st,k,v=row['events'][0];assert fr==1537 and st in range(144,160) and k in range(128) and v in range(128)
  assert struct.pack('<qBBBBI',fr,st,k,v,0,0).hex()==row['packed16_event_le']
  assert row['parameter_tokens']==c['parameter_tokens'] and row['parameter_f32_bits_le']==c['parameter_f32_bits_le'] and row['parameter_f64_reconstructed_le']==c['parameter_f64_reconstructed_le'] and row['parameter_vector_sha256']==c['parameter_vector_sha256'] and row['parameter_token_binary64_sha256']==c['parameter_token_binary64_sha256']
  assert row['history_sha256'] not in seen;seen.add(row['history_sha256']);assert all(row[z] is None for z in ['waveform_prediction','portable_expected','portable_comparator','candidate_grade'])
  if h['existing_case_refs']:
   old+=1;ref=row['historical'];assert row['disposition']=='inherited-no-replay' and 'script' not in row and 'fresh_ordinal' not in row and ref['eligibility_row']==h and ref['existing_case_refs']==h['existing_case_refs'] and ref['no_old_modal_budget_transfer'] is True
   assert ref['fresh_pid'] is ref['fresh_receipt'] is ref['new_metrics'] is None and ref['old_audio_reads']==0
  else:
   fresh+=1;assert row['disposition']=='fresh-planned' and row['fresh_ordinal']==fresh and row['historical'] is None
   script=planned(row,c).encode();assert identity(row['script']['path'])==row['script'] and Path(row['script']['path']).read_bytes()==script and len(script)==h['script_utf8_bytes'] and hashlib.sha256(script).hexdigest()==h['script_utf8_sha256']
 assert fresh==268 and old==2 and len(seen)==270 and len({r['parameter_vector_sha256'] for r in c['rows']})==1
 assert len([a for a in c['aliases'] if a['id']=='CHM-U060'])==3
 assert [(r['id'],r['historical']['existing_case_refs']) for r in c['rows'] if r['historical']]==[('CHM-U060',['DCO-030']),('CHM-U072',['DCO-031'])]

def synthetic(c,row,rate=1):
 fr,st,k,v=row['events'][0]
 return 'slice offset=16384 size=250352\n'+''.join(f"import {a['binding']} {a['symbol']} slots={a['slots']}\n" for a in c['approved_import_declarations'])+''.join(f'export {a} {v}\n' for a,v in c['approved_export_declarations'].items())+'mxcsr 0x1f80\ntransport 0 0 120\ncreate ok\n'+f'rate 44100 ret={rate}\n'+''.join(f'param {i} {t}\n' for i,t in enumerate(row['parameter_tokens']))+f'event {fr} {hex(st)} {k} {v}\n'+'inflag 1\ninput '+c['input_source']['path']+'\nprocess 16384 512 flags: 32x(ret=0,flag=1) blocks=32\ndestroy\ncxx-failbits 0\n'+f"used {next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux')} 1\n"

def selfchecks(c):
 validate(c);neg=[]
 for name,mut in [('omithistory',lambda x:x['rows'].pop()),('omitalias',lambda x:x['aliases'].pop()),('paramonlydedup',lambda x:x['rows'].__setitem__(1,copy.deepcopy(x['rows'][0]))),('roundedownertokens',lambda x:x['parameter_tokens'].__setitem__(15,repr(struct.unpack('<f',bytes.fromhex(x['parameter_f32_bits_le'][15]))[0]))),('binary64wrong',lambda x:x['parameter_f64_reconstructed_le'].__setitem__(15,'0'*16)),('wrongvector201',lambda x:x.update(parameter_vector_sha256='9b98e8cab7aae28b01e18de3cd9570db62721f0ecdbf951bd5bd77d8b378e6e2')),('libmoverride0notunset',lambda x:x['environment'].update(XDEV_LIBM_ULP='0')),('wrongonframe',lambda x:x['rows'][0]['events'][0].__setitem__(0,1536)),('addedOff',lambda x:x['rows'][0]['events'].append([3073,128,0,64])),('crossproduct',lambda x:x['rows'][0]['events'][0].__setitem__(3,1)),('packedwrong',lambda x:x['rows'][0].update(packed16_event_le='0'*32)),('inventprior',lambda x:x['rows'][0].update(waveform_prediction='law')),('portablecriterion',lambda x:x['rows'][0].update(portable_comparator='modal')),('inventoldPID',lambda x:x['rows'][60]['historical'].update(fresh_pid=1)),('replayold',lambda x:x['rows'][60].update(disposition='fresh-planned')),('transfermodalbudget',lambda x:x['rows'][60]['historical'].update(no_old_modal_budget_transfer=False)),('wrongcount',lambda x:x['limits'].update(children=270))]:
  bad=copy.deepcopy(c);mut(bad);assert bad!=c
  try:validate(bad)
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('accepted '+name)
 row=c['rows'][0];text=synthetic(c,row);protocol(text,row,c);pn=[]
 for name,a,b in [('wrongon','event 1537','event 1536'),('wrongstatus','0x90 0 100','0x91 0 100'),('wrongkey','0x90 0 100','0x90 1 100'),('wrongvelocity','0x90 0 100','0x90 0 0'),('addedOff','destroy\n','event 3073 0x80 0 64\ndestroy\n'),('FP','mxcsr 0x1f80','mxcsr 0x3f80'),('transport','transport 0 0 120','transport 1 0 120'),('flag','ret=0,flag=1','ret=0,flag=4'),('cxx','cxx-failbits 0','cxx-failbits 1')]:
  bad=text.replace(a,b);assert bad!=text
  try:protocol(bad,row,c)
  except (AssertionError,IndexError,KeyError):pn.append(name)
  else:raise AssertionError('acceptedprotocol '+name)
 code=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux');data=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='data');bad=text.replace(f'used {code} 1',f'used {data} 1');assert bad!=text
 try:protocol(bad,row,c)
 except AssertionError:pn.append('changed_data_as_code')
 else:raise AssertionError('accepted data_as_code')
 for rate in [0,1,-2147483648]:assert protocol(synthetic(c,row,rate),row,c)['rate_return_logged']==rate
 for row in [c['rows'][127],c['rows'][128],c['rows'][-1]]:protocol(synthetic(c,row),row,c)
 assert metrics(struct.pack('<II',0,0))['all_finite'] and metrics(struct.pack('<II',0x80000000,0))['negative_zero_sample_counts']==[1,0]
 assert not metrics(struct.pack('<II',0,0x7f800001))['all_finite'] and not metrics(struct.pack('<II',0,1))['channels_byte_identical']
 return {'input_negatives':neg,'protocol_negatives':pn,'opaque_Rate_positives':[0,1,-2147483648],'edge_protocols':['key127','velocity0','channel15'],'unsigned_groups':['positivezero','negativezero','rightsignalingNaN','rightsubnormal'],'270wholehistories_notparameteronly':True,'threebaselinealiases_onecontrol_no_replay':True,'originaldecimal_binary64_tokens_exact':True,'LIBM_ULP_unset':True}
