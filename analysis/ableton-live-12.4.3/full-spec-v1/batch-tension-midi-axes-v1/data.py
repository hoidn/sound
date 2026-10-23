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
    assert re.findall(r'^event (\d+) (0x[0-9a-f]+) (\d+) (\d+)$', log, re.M) == [(str(f),hex(st),str(k),str(v)) for f,st,k,v in row['events']]
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



def history_hash(h):
 import json
 return hashlib.sha256(json.dumps(h,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def validate(c):
 assert c['parameter_indices']==INDICES and len(c['rows'])==143 and len(c['aliases'])==144
 assert c['logical_aliases']==144 and c['whole_histories']==143 and c['fresh']==142 and c['inherited']==1
 assert c['environment']=={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC','XDEV_TIME':'0'}
 assert c['limits']['children']==142 and c['limits']['selected_export_calls_total']==31098 and c['limits']['CalcA_total']==12354 and c['limits']['new_stereo_bytes_total']==50097600
 bits=[struct.pack('<f',float(x)).hex() for x in c['parameter_tokens']]
 assert bits==c['parameter_f32_bits_le'] and hashlib.sha256(bytes.fromhex(''.join(bits))).hexdigest()==c['parameter_vector_sha256']=='e00185698bafd4531b3562012e001afa759556d27405928685f07bf2f5c97eb8'
 assert identity(HERE/'baseline-template.script')==c['baseline_template'];template=(HERE/'baseline-template.script').read_text().splitlines()
 assert len(template)==137 and template[:2]==['create','rate 44100'] and template[131:]==['event 4096 0x90 60 100','event 26146 0x80 60 0','inflag 0','input zero','process 44100 512','destroy']
 seen={};fresh=0
 for i,row in enumerate(c['rows']):
  assert row['id']==f'TMA-U{i:03d}' and row['unique_vector']==i
  assert row['parameter_tokens']==c['parameter_tokens'] and row['parameter_f32_bits_le']==bits and row['parameter_vector_sha256']==c['parameter_vector_sha256']
  assert row['waveform_prediction'] is row['portable_expected'] is row['portable_comparator'] is row['candidate_grade'] is None
  h=row['history'];assert h=={'rate':44100,'frames':44100,'block':512,'last_block':68,'warmup':0,'input':'zero','input_flag':0,'transport':[0,0,120],'events':row['events'],'time':0,'parameter_vector_sha256':c['parameter_vector_sha256']}
  digest=history_hash(h);assert row['history_sha256']==digest and digest not in seen;seen[digest]=row['id']
  if i==0:
   assert row['events']==[[4096,144,60,100],[26146,128,60,0]] and row['disposition']=='inherited-no-replay' and 'script' not in row and 'fresh_ordinal' not in row
   old=row['historical'];assert old['fresh_pid'] is old['fresh_receipt'] is old['new_metrics'] is None and old['old_audio_reads']==0
  else:
   fresh+=1;assert row['disposition']=='fresh-planned' and row['fresh_ordinal']==fresh and row['historical'] is None
   expected=[[4096,144+i,60,100],[26146,128+i,60,0]] if i<=15 else [[4096,144,60,100],[26146,128,60,i-15]]
   assert row['events']==expected
   lines=list(template);lines[131:133]=[f'event {fr} 0x{st:02x} {key} {vel}' for fr,st,key,vel in expected]
   assert identity(row['script']['path'])==row['script'] and Path(row['script']['path']).read_text()=='\n'.join(lines)+'\n'
 assert fresh==142
 expected_aliases=[]
 for axis,values in [('channel',range(16)),('off_velocity',range(128))]:
  for v in values:
   i=v if axis=='channel' else 0 if v==0 else 15+v;r=c['rows'][i]
   expected_aliases.append({'axis':axis,'value':v,'unique_id':r['id'],'history_sha256':r['history_sha256'],'shared_baseline_alias':v==0})
 assert c['aliases']==expected_aliases and sum(x['shared_baseline_alias'] for x in c['aliases'])==2
 # Parameter vectors are intentionally all equal; event histories MUST NOT collapse to one.
 assert len({r['parameter_vector_sha256'] for r in c['rows']})==1 and len(seen)==143

def synthetic(c,row,rate=1):
 text='init 0x260c0\nslice offset=16384 size=501392\n'+''.join(f"import {r['binding']} {r['symbol']} slots={r['slots']}\n" for r in c['approved_import_declarations'])+''.join(f'export {n} {v}\n' for n,v in c['approved_export_declarations'].items())+f'create ok\nrate 44100 ret={rate}\n'+''.join(f'param {i} {t}\n' for i,t in zip(c['parameter_indices'],row['parameter_tokens']))+''.join(f'event {f} {hex(s)} {k} {v}\n' for f,s,k,v in row['events'])+'inflag 0\ninput zero\nprocess 44100 512 flags: 87x(ret=0,flag=1) blocks=87\ndestroy\ncxx-failbits 0\n'
 linux=next(r['symbol'] for r in c['approved_import_declarations'] if r['binding']=='linux');return text+f'used {linux} 1\n'

def selfchecks(c):
 validate(c);negative=[]
 for name,fn in [('omitwholehistory',lambda x:x['rows'].pop()),('omitaxisalias',lambda x:x['aliases'].pop()),('parameteronlydedup',lambda x:x.update(whole_histories=1)),('duplicatehistory',lambda x:x['rows'].__setitem__(1,copy.deepcopy(x['rows'][0]))),('unmatchedchannel',lambda x:x['rows'][1]['events'][1].__setitem__(1,128)),('statecrossproduct',lambda x:x['rows'][1]['events'][1].__setitem__(3,1)),('onvelocitychange',lambda x:x['rows'][1]['events'][0].__setitem__(3,99)),('offframechange',lambda x:x['rows'][1]['events'][1].__setitem__(0,26147)),('inventprior',lambda x:x['rows'][1].update(waveform_prediction='fitted')),('portablecriterion',lambda x:x['rows'][1].update(portable_comparator='exact')),('inventoldPID',lambda x:x['rows'][0]['historical'].update(fresh_pid=1)),('replaybaseline',lambda x:x['rows'][0].update(disposition='fresh-planned')),('FPoverride',lambda x:x['environment'].update(XDEV_LIBM_ULP='1')),('wrongparameter',lambda x:x['parameter_f32_bits_le'].__setitem__(0,'00000000')),('omitedge127',lambda x:x['aliases'][-1].update(value=126)),('extraalias',lambda x:x['aliases'].append(dict(x['aliases'][0])) )]:
  bad=copy.deepcopy(c);fn(bad)
  try:validate(bad)
  except (AssertionError,KeyError,IndexError):negative.append(name)
  else:raise AssertionError('accepted '+name)
 row=c['rows'][1];text=synthetic(c,row);protocol(text,row,c);pn=[]
 for name,a,b in [('wrongchannel','0x91','0x90'),('unmatchedoff','0x81','0x80'),('offvelocity','0x81 60 0','0x81 60 127'),('key','0x91 60 100','0x91 61 100'),('onvelocity','0x91 60 100','0x91 60 99'),('offframe','26146','26147'),('initializer','0x260c0','0x1'),('cxx','cxx-failbits 0','cxx-failbits 1'),('flag','ret=0,flag=1','ret=0,flag=4'),('return','ret=0,flag=1','ret=1,flag=1'),('extrareset','destroy\n','destroy\nreset\n')]:
  bad=text.replace(a,b);assert bad!=text
  try:protocol(bad,row,c)
  except (AssertionError,IndexError,KeyError):pn.append(name)
  else:raise AssertionError('accepted protocol '+name)
 data_symbol=next(r['symbol'] for r in c['approved_import_declarations'] if r['binding']=='data')
 linux_symbol=next(r['symbol'] for r in c['approved_import_declarations'] if r['binding']=='linux')
 bad=text.replace(f'used {linux_symbol} 1',f'used {data_symbol} 1');assert bad!=text
 try:protocol(bad,row,c)
 except AssertionError:pn.append('data_as_code')
 else:raise AssertionError('accepted data_as_code')
 positives=[]
 for rate in [0,1,-2147483648]:assert protocol(synthetic(c,row,rate),row,c)['rate_return_logged']==rate;positives.append(rate)
 for row in [c['rows'][15],c['rows'][16],c['rows'][-1]]:protocol(synthetic(c,row),row,c)
 assert metrics(struct.pack('<II',0,0))['all_finite'];assert metrics(struct.pack('<II',0x80000000,0))['negative_zero_sample_counts']==[1,0]
 assert not metrics(struct.pack('<II',0,0x7f800001))['all_finite'];assert not metrics(struct.pack('<II',0,1))['channels_byte_identical']
 return {'input_negatives':negative,'synthetic_protocol_negatives':pn,'opaque_rate_positive_controls':positives,'edge_protocols':['channel15','offvelocity1','offvelocity127'],'unsigned_groups':['positivezero','negativezero','rightsignalingNaN','rightsubnormal'],'parameter_only_dedup_refused':True,'baseline_shared_once_no_replay':True}
