"""Owned fixed finite host-domain inputs/protocol and unsigned stereo data only."""
import collections,copy,hashlib,re,struct
from pathlib import Path
HERE=Path(__file__).resolve().parent
INDICES=[i for i in range(130) if i!=2]
def identity(path):
 p=Path(path);raw=p.read_bytes();return {'path':str(p),'resolved_path':str(p.resolve()),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def protocol(log, row, c):
    assert not re.search(r'(?im)^(?:TRAP|FAULT|xdev:)', log)
    assert re.findall(r'^init (0x[0-9a-f]+)$', log, re.M) == ['0x260c0']
    assert re.findall(r'^slice offset=(\d+) size=(\d+)$', log, re.M) == [('16384', '501392')]
    assert re.findall(r'^create (\S+)$', log, re.M) == ['ok']
    assert re.findall(r'^destroy$', log, re.M) == ['destroy']
    assert re.findall(r'^cxx-failbits (\S+)$', log, re.M) == ['0']
    rate = re.findall(r'^rate 44100 ret=(-?\d+)$', log, re.M); assert len(rate) == 1
    params = re.findall(r'^param (\d+) (\S+)$', log, re.M)
    assert [int(i) for i, _ in params] == INDICES
    assert [struct.pack('<f', float(x)).hex() for _, x in params] == row['parameter_f32_bits_le']
    assert re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M) == [('4096', '0x90', '60', '100'), ('26146', '0x80', '60', '0')]
    assert re.findall(r'^inflag (-?\d+)$', log, re.M) == ['0']
    assert re.findall(r'^input (\S+)$', log, re.M) == ['zero']
    assert not re.search(r'(?m)^(?:reset|transport|mxcsr|info)\b', log)
    process = re.findall(r'^process 44100 512 flags:(.*) blocks=87$', log, re.M)
    assert len(process) == 1 and re.fullmatch(r'(?: [1-9][0-9]*x\(ret=-?\d+,flag=-?\d+\))+', process[0])
    flags = [{'blocks': int(n), 'return': int(r), 'flag': int(f)} for n, r, f in re.findall(r'(\d+)x\(ret=(-?\d+),flag=(-?\d+)\)', process[0])]
    assert sum(x['blocks'] for x in flags) == 87 and all(x['return'] == 0 and x['flag'] in (0, 1) for x in flags)
    exports = re.findall(r'^export (\S+) (0x[0-9a-f]+)$', log, re.M)
    assert len(exports) == len(dict(exports)) == 7 and dict(exports) == c['approved_export_declarations']
    imports = re.findall(r'^import (trap|linux|data) (\S+) slots=(\d+)$', log, re.M)
    assert len(imports) == len({n for _, n, _ in imports}) == 142
    assert dict(collections.Counter(k for k, _, _ in imports)) == {'trap': 26, 'linux': 109, 'data': 7}
    declarations = [{'binding': k, 'symbol': n, 'slots': int(s)} for k, n, s in imports]
    assert declarations == c['approved_import_declarations']
    bindings = {n: k for k, n, _ in imports}
    used = re.findall(r'^used (\S+) ([1-9][0-9]*)$', log, re.M)
    assert used and len(dict(used)) == len(used) and all(bindings.get(n) == 'linux' for n, _ in used)
    return {'initializer_entries_logged': ['0x260c0'], 'selected_direct_exports_from_script_protocol': 219,
            'nested_original_calls': None, 'rate_return_logged': int(rate[0]), 'flags': flags,
            'exports_declared_not_all_invoked': dict(exports), 'import_declarations': declarations,
            'actual_used_code_import_counts': {n: int(v) for n, v in used}, 'cxx_failbits': 0}


def metrics(raw):
    # Same retained bit-summary class as approved Tension velocity captures: no float estimator.
    assert len(raw) > 0 and len(raw) % 8 == 0
    pairs = list(struct.iter_unpack('<II', raw))
    nonfinite = sum((v & 0x7f800000) == 0x7f800000 for pair in pairs for v in pair)
    return {'frames': len(pairs), 'all_finite': nonfinite == 0, 'nonfinite_scalar_count': nonfinite,
            'channels_byte_identical': all(l == r for l, r in pairs),
            'nonzero_sample_counts': [sum((pair[c] & 0x7fffffff) != 0 for pair in pairs) for c in (0, 1)],
            'negative_zero_sample_counts': [sum(pair[c] == 0x80000000 for pair in pairs) for c in (0, 1)]}



def validate(c):
 domains=c['domains'];rows=c['rows'];aliases=c['aliases'];indices=c['parameter_indices'];base=c['parameter_f32_bits_le']
 assert len(domains)==48 and len(rows)==117 and len(aliases)==164
 assert c['excluded_virtual_kind3']==[0,7,122,124,126,128]
 assert len(indices)==129 and indices==[i for i in range(130) if i!=2]
 assert c['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC','XDEV_TIME':'0'}
 assert c['limits']['children']==106 and c['limits']['selected_export_calls_total']==23214 and c['limits']['CalcA_total']==9222 and c['limits']['new_stereo_bytes_total']==37396800
 assert identity(HERE/'baseline-template.script')==c['baseline_template']
 template=(HERE/'baseline-template.script').read_text().splitlines()
 assert len(template)==137 and template[:2]==['create','rate 44100'] and template[131:]==['event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy']
 assert base==[struct.pack('<f',float(t)).hex() for t in c['parameter_tokens']]
 assert hashlib.sha256(bytes.fromhex(''.join(base))).hexdigest()==c['parameter_vector_sha256']=='e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8'
 pairs=[];seen=set();fresh=0;old=0
 for i,row in enumerate(rows):
  assert row['id']==f'TK3-U{i:03d}' and row['unique_vector']==i
  assert row['waveform_prediction'] is row['portable_expected'] is row['portable_comparator'] is row['candidate_grade'] is None
  actualbits=[struct.pack('<f',float(t)).hex() for t in row['parameter_tokens']];assert actualbits==row['parameter_f32_bits_le']
  vector=''.join(actualbits);assert vector not in seen;seen.add(vector);assert hashlib.sha256(bytes.fromhex(vector)).hexdigest()==row['parameter_vector_sha256']
  diff=[indices[j] for j,x in enumerate(actualbits) if x!=base[j]]
  if i==0:assert diff==[] and row['domain_index'] is row['host_value'] is None
  else:
   assert diff==[row['domain_index']];d=next(x for x in domains if x['index']==row['domain_index']);assert row['host_value'] in range(int(d['max'])+1) and row['host_value']!=d['baseline'];assert actualbits[indices.index(d['index'])]==struct.pack('<f',row['host_value']).hex()
  if row['disposition']=='fresh-planned':
   fresh+=1;assert row['fresh_ordinal']==fresh and row['historical'] is None and identity(row['script']['path'])==row['script']
   lines=list(template);idx=row['domain_index'];lines[2+indices.index(idx)]=f"param {idx} {row['parameter_tokens'][indices.index(idx)]}";assert (HERE/'scripts'/(row['id']+'.script')).read_text()=='\n'.join(lines)+'\n'
  else:
   old+=1;assert row['disposition']=='inherited-no-replay' and 'script' not in row and 'fresh_ordinal' not in row
   ref=row['historical'];assert ref['fresh_receipt'] is ref['fresh_pid'] is ref['new_metrics'] is None and ref['old_audio_reads']==0
 for d in domains:
  assert d['kind']==3 and not d['virtual'] and d['min']==0 and type(d['baseline']) is int and d['baseline'] in range(int(d['max'])+1)
  for v in range(int(d['max'])+1):
   target=rows[0] if v==d['baseline'] else next(x for x in rows if x['domain_index']==d['index'] and x['host_value']==v)
   pairs.append({'domain_index':d['index'],'host_value':v,'unique_id':target['id'],'inherited_shared_baseline':v==d['baseline']})
 assert aliases==pairs and sum(x['inherited_shared_baseline'] for x in aliases)==48 and fresh==106 and old==11
 assert [(r['domain_index'],r['host_value']) for r in rows if r.get('prior_recipe_only')]==[(6,2),(13,1),(36,0)]

def selfchecks(c):
 validate(c);negative=[]
 for name,fn in [('omitclass',lambda x:x['domains'].pop()),('omitvector',lambda x:x['rows'].pop()),('omitalias',lambda x:x['aliases'].pop()),('virtualdomain',lambda x:x['domains'][0].update(virtual=True)),('wrongbaseline',lambda x:x['domains'][0].update(baseline=6)),('dupalias',lambda x:x['aliases'].__setitem__(1,dict(x['aliases'][0]))),('newprior',lambda x:x['rows'][1].update(waveform_prediction='tone')),('portable',lambda x:x['rows'][1].update(portable_comparator='exact')),('wronghostvalue',lambda x:x['rows'][1].update(host_value=7)),('newstatecrossproduct',lambda x:x['rows'][1]['parameter_f32_bits_le'].__setitem__(10,'0000803f')),('inventoldPID',lambda x:x['rows'][0]['historical'].update(fresh_pid=1)),('replayold',lambda x:x['rows'][0].update(disposition='fresh-planned')),('wrongcount',lambda x:x['limits'].update(children=107)),('FPoverride',lambda x:x['environment'].update(XDEV_LIBM_ULP='1'))]:
  bad=copy.deepcopy(c);fn(bad)
  try:validate(bad)
  except (AssertionError,KeyError,IndexError,StopIteration):negative.append(name)
  else:raise AssertionError('accepted '+name)
 row=next(r for r in c['rows'] if r['disposition']=='fresh-planned')
 text='init 0x260c0\nslice offset=16384 size=501392\n'+''.join(f"import {r['binding']} {r['symbol']} slots={r['slots']}\n" for r in c['approved_import_declarations'])+''.join(f'export {n} {v}\n' for n,v in c['approved_export_declarations'].items())+'create ok\nrate 44100 ret=1\n'+''.join(f'param {i} {t}\n' for i,t in zip(c['parameter_indices'],row['parameter_tokens']))+'event 4096 0x90 60 100\nevent 26146 0x80 60 0\ninflag 0\ninput zero\nprocess 44100 512 flags: 87x(ret=0,flag=1) blocks=87\ndestroy\ncxx-failbits 0\n'
 linux=next(r['symbol'] for r in c['approved_import_declarations'] if r['binding']=='linux');text+=f'used {linux} 1\n';protocol(text,row,c);pn=[]
 for name,a,b in [('initializer','0x260c0','0x1'),('key','0x90 60 100','0x90 61 100'),('velocity','0x90 60 100','0x90 60 1'),('offframe','26146','26147'),('flag','ret=0,flag=1','ret=0,flag=4'),('return','ret=0,flag=1','ret=1,flag=1'),('cxx','cxx-failbits 0','cxx-failbits 1'),('extrareset','destroy\n','destroy\nreset\n')]:
  try:protocol(text.replace(a,b),row,c)
  except (AssertionError,IndexError,KeyError):pn.append(name)
  else:raise AssertionError('accepted protocol '+name)
 assert metrics(struct.pack('<II',0,0))['all_finite'];assert metrics(struct.pack('<II',0x80000000,0))['negative_zero_sample_counts']==[1,0]
 assert not metrics(struct.pack('<II',0,0x7f800001))['all_finite'];assert not metrics(struct.pack('<II',0,1))['channels_byte_identical']
 return {'input_negatives':negative,'synthetic_protocol_negatives':pn,'unsigned_groups':['positivezero','negativezero','rightsignalingNaN','rightsubnormal']}
