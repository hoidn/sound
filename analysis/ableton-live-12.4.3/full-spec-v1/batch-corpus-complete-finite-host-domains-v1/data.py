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
 assert len(commands)==48
 for i,line in enumerate(commands[5:43]):
  m=re.fullmatch(r'param (\d+) (\S+)',line);assert m and int(m[1])==i and struct.pack('<f',float(m[2])).hex()==row['parameter_f32_bits_le'][i]
 assert commands[43:45]==['inflag 1','input '+str(HERE/'input.f32')] and commands[46:]==['destroy','cxx-failbits 0']
 m=re.fullmatch(r'process 16384 512 flags:((?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+ blocks=32)',commands[45]);assert m
 groups=[{'blocks':int(n),'return':int(r),'flag':int(f)} for n,r,f in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)',commands[45])];assert sum(x['blocks'] for x in groups)==32 and all(x['return']==0 and x['flag'] in (0,1) for x in groups)
 return {'initializer_entries_logged':inits,'selected_direct_exports_from_script_protocol':73,'nested_original_calls':None,'rate_return_logged':rate,'flags':groups,'exports_declared_not_all_invoked':exports,'import_declarations':imports,'actual_used_code_import_counts':used,'cxx_failbits':0}

def planned(row):
 return '\n'.join(['mxcsr 0x1f80','transport 0 0 120','create','rate 44100']+[f'param {i} {t}' for i,t in enumerate(row['parameter_tokens'])]+['inflag 1','input '+str(HERE/'input.f32'),'process 16384 512','destroy'])+'\n'

def validate(c):
 e=json.loads((HERE/'eligibility.json').read_text());prior=json.loads((HERE/'approved-prior-summary.json').read_text())['approved_summary'];old={x['vector_sha256']:(i,x) for i,x in enumerate(prior['approved_vectors'])}
 assert len(old)==63 and len(c['rows'])==264 and len(c['aliases'])==277 and c['domains']==e['domains']
 assert [(x['host_index'],x['minimum'],x['maximum']) for x in c['domains']]==[(0,0,6),(7,-48,48),(8,-50,50),(10,0,24),(12,0,1),(13,0,1),(17,0,1),(18,0,6),(19,0,1),(21,0,21),(22,0,1),(27,0,1),(33,0,3),(37,0,1)]
 assert c['environment']=={'PATH':'/usr/bin:/bin','LC_ALL':'C','LANG':'C','TZ':'UTC','XDEV_TIME':'0','XDEV_LIBM_ULP':'0'} and c['shared_complete_history']==e['shared_complete_history']
 assert c['base_params']==e['base_params'] and c['baseline_vector_sha256']==e['base_vector_sha256']
 assert c['limits']['children']==201 and c['limits']['selected_export_calls_total']==14673 and c['limits']['CalcA_total']==6432 and c['limits']['new_stereo_bytes_total']==26345472
 assert identity(HERE/'input.f32')==c['input'] and c['input']['bytes']==131072 and c['input']['sha256']=='03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6'
 seen={};fresh=0;inherited=0
 for i,(row,ev) in enumerate(zip(c['rows'],e['catalog_vectors'])):
  assert row['id']==f'CFH-V{i:03d}' and row['unique_vector']==i and row['vector_sha256']==ev['vector_sha256'] and row['complete_history_sha256']==ev['complete_history_sha256'] and row['eligibility_pointer']==f'/catalog_vectors/{i}'
  assert row['alias_ids']==ev['alias_ids'] and row['first_alias']==ev['first_alias']
  expected=list(c['base_params']);expected[ev['first_alias']['host_index']]=float(ev['first_alias']['host_value'])
  assert row['parameter_tokens']==[repr(x) for x in expected] and [struct.pack('<f',float(t)).hex() for t in row['parameter_tokens']]==row['parameter_f32_bits_le']==ev['parameter_bits_le']
  assert [struct.pack('<d',float(t)).hex() for t in row['parameter_tokens']]==row['parameter_f64_reconstructed_le']
  h=hashlib.sha256(bytes.fromhex(''.join(row['parameter_f32_bits_le']))).hexdigest();assert h==row['vector_sha256']==row['parameter_vector_sha256'] and h not in seen;seen[h]=row['id']
  assert all(row[z] is None for z in ['waveform_prediction','portable_expected','portable_comparator','candidate_grade'])
  if h in old:
   inherited+=1;oi,p=old[h];ref=row['historical'];assert row['disposition']=='inherited-no-replay' and 'script' not in row and 'fresh_ordinal' not in row
   assert ref['approved_pointer']==f'/approved_summary/approved_vectors/{oi}' and ref['approved_vector_id']==p['id'] and ref['full_vector_sha256']==h
   assert ref['prior_point_sha256']==hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   assert ref['prior_shape5_qualification']==ev['prior_shape5_qualification'] and ref['prior_analysis_qualification']==ev['prior_analysis_qualification']
   assert ref['fresh_pid'] is ref['fresh_receipt'] is ref['new_metrics'] is None and ref['old_audio_reads']==0
   if p['id']=='CNI-V036':assert ref['prior_shape5_qualification']==prior['historical_shape5_qualification']
  else:
   fresh+=1;assert row['disposition']=='fresh-planned' and row['historical'] is None and row['fresh_ordinal']==fresh
   assert identity(row['script']['path'])==row['script'] and Path(row['script']['path']).read_text()==planned(row)
 assert fresh==201 and inherited==63 and set(old)<=set(seen)
 assert c['aliases']==[dict(a,unique_id=seen[a['vector_sha256']]) for a in e['catalog_aliases']]
 assert sum(a['vector_sha256']==c['baseline_vector_sha256'] for a in c['aliases'])==14

def synthetic(c,row,rate=1):
 return 'slice offset=16384 size=250352\n'+''.join(f"import {a['binding']} {a['symbol']} slots={a['slots']}\n" for a in c['approved_import_declarations'])+''.join(f'export {a} {v}\n' for a,v in c['approved_export_declarations'].items())+'mxcsr 0x1f80\ntransport 0 0 120\ncreate ok\n'+f'rate 44100 ret={rate}\n'+''.join(f'param {i} {t}\n' for i,t in enumerate(row['parameter_tokens']))+'inflag 1\ninput '+str(HERE/'input.f32')+'\nprocess 16384 512 flags: 32x(ret=0,flag=1) blocks=32\ndestroy\ncxx-failbits 0\n'+f"used {next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux')} 1\n"

def selfchecks(c):
 validate(c);neg=[]
 old=next(i for i,x in enumerate(c['rows']) if x['historical']);shape=next(i for i,x in enumerate(c['rows']) if x['historical'] and x['historical']['approved_vector_id']=='CNI-V036');fi=next(i for i,x in enumerate(c['rows']) if x['disposition']=='fresh-planned')
 for name,mut in [('omitalias',lambda x:x['aliases'].pop()),('omitvector',lambda x:x['rows'].pop()),('omitaxis',lambda x:x['domains'].pop()),('crossproduct',lambda x:x['rows'][fi]['parameter_tokens'].__setitem__(1,'0.0')),('nonintegerclass',lambda x:x['rows'][fi]['parameter_tokens'].__setitem__(7,'-47.5')),('f32wrong',lambda x:x['rows'][fi]['parameter_f32_bits_le'].__setitem__(7,'00000000')),('f64wrong',lambda x:x['rows'][fi]['parameter_f64_reconstructed_le'].__setitem__(7,'0000000000000000')),('inventprior',lambda x:x['rows'][fi].update(waveform_prediction='fit')),('portablecriteria',lambda x:x['rows'][fi].update(portable_comparator='exact')),('FPoverride',lambda x:x['environment'].update(XDEV_LIBM_ULP='1')),('wrongcount',lambda x:x['limits'].update(children=264)),('replayold',lambda x:x['rows'][old].update(disposition='fresh-planned')),('inventoldPID',lambda x:x['rows'][old]['historical'].update(fresh_pid=1)),('positionjoinwrong',lambda x:x['rows'][old]['historical'].update(approved_pointer='/approved_summary/approved_vectors/263')),('dropoldcheckerqualification',lambda x:x['rows'][old]['historical'].update(prior_analysis_qualification=None)),('shape5upgrade',lambda x:x['rows'][shape]['historical'].update(prior_shape5_qualification=None))]:
  bad=copy.deepcopy(c);mut(bad)
  try:validate(bad)
  except (AssertionError,KeyError,IndexError):neg.append(name)
  else:raise AssertionError('accepted '+name)
 row=c['rows'][fi];text=synthetic(c,row);protocol(text,row,c);pn=[]
 for name,a,b in [('rateformat','rate 44100','rate 48000'),('flags','ret=0,flag=1','ret=0,flag=7'),('processreturn','ret=0,flag=1','ret=1,flag=1'),('FPphase','mxcsr 0x1f80','mxcsr 0x3f80'),('transport','transport 0 0 120','transport 1 0 120'),('inputflag','inflag 1','inflag 0'),('cxx','cxx-failbits 0','cxx-failbits 1'),('events','destroy\n','event 1537 0x90 60 100\ndestroy\n')]:
  bad=text.replace(a,b);assert bad!=text
  try:protocol(bad,row,c)
  except (AssertionError,IndexError,KeyError):pn.append(name)
  else:raise AssertionError('acceptedprotocol '+name)
 code=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='linux');data=next(x['symbol'] for x in c['approved_import_declarations'] if x['binding']=='data');bad=text.replace(f'used {code} 1',f'used {data} 1');assert bad!=text
 try:protocol(bad,row,c)
 except AssertionError:pn.append('actualchanged_data_as_code')
 else:raise AssertionError('accepted data_as_code')
 for rate in [0,1,-2147483648]:assert protocol(synthetic(c,row,rate),row,c)['rate_return_logged']==rate
 assert metrics(struct.pack('<II',0,0))['all_finite'] and metrics(struct.pack('<II',0x80000000,0))['negative_zero_sample_counts']==[1,0]
 assert not metrics(struct.pack('<II',0,0x7f800001))['all_finite'] and not metrics(struct.pack('<II',0,1))['channels_byte_identical']
 return {'input_negatives':neg,'protocol_negatives':pn,'opaque_Rate_positives':[0,1,-2147483648],'unsigned_groups':['positivezero','negativezero','rightsignalingNaN','rightsubnormal'],'all63_inherited_byhash':True,'shape5_oldchecker_qualifications_preserved':True}
