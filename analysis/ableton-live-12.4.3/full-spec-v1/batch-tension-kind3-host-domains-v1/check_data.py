"""Packet-only full finite class checks; never externalruntime/oldaudio/original calls."""
from datetime import datetime
import json,hashlib,copy,runpy,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=runpy.run_path(str(HERE/'data.py'),run_name='owned_data')
def load(n):return json.loads((HERE/n).read_text())
def check_record(row, receipt, c, stdout, stderr, raw):
    folder = HERE / 'attempts' / row['id']
    assert receipt['id'] == row['id'] and receipt['unique_vector'] == row['unique_vector']
    assert receipt['fresh_ordinal'] == row['fresh_ordinal'] and receipt['pid'] > 0
    assert receipt['argv'] == [c['executable']['path'], c['bundle_slice_expected']['path'], row['script']['path'], str(folder / 'output.f32'), '--imports']
    assert receipt['child_environment'] == c['environment']
    assert receipt['attempts'] == 1 and receipt['exit'] == 0 and not receipt['timeout']
    assert receipt['error'] is None and receipt['cleanup'] == [] and 'custody_error' not in receipt
    assert receipt['waveform_prediction'] is receipt['portable_comparator'] is receipt['portable_expected'] is receipt['candidate_grade'] is None
    assert stderr == b'' and len(raw) == 352800 and 0 < len(stdout) <= 4194304
    for k, b in [('stdout', stdout), ('stderr', stderr), ('output', raw)]:
        assert receipt[k]['bytes'] == len(b) and receipt[k]['sha256'] == hashlib.sha256(b).hexdigest()
    assert D['protocol'](stdout.decode('ascii'), row, c) == receipt['protocol']
    observed = D['metrics'](raw)
    assert observed == receipt['observed_output'] and observed['all_finite'] and observed['frames'] == 44100
    expected = list(c['runtime_expected']); image = c['bundle_slice_expected']
    expected.append({'path': image['path'], 'slice_offset': image['x86_64_offset'], 'bytes': image['x86_64_size'], 'sha256': image['x86_64_sha256']})
    expected += [D['identity'](HERE / n) for n in ('inputs.json', 'data.py', 'run_batch.py', 'check_data.py', 'launch.py')]
    expected.append(row['script'])
    assert receipt['custody_before'] == receipt['custody_after'] == expected
    times = [datetime.fromisoformat(receipt[k]) for k in ('utc_start', 'spawn_utc', 'child_end_utc', 'utc_end')]
    assert times == sorted(times) and 0 <= receipt['child_wall_seconds'] <= 20
    return observed


def check_parent(c, context, summary, launch):
    assert context['parent_launch_receipt'] == launch and launch['pid'] == context['outer_pid'] == summary['outer_pid']
    assert launch['exec_argv'] == c['parent_exec_argv'] and launch['exec_environment'] == c['environment'] and launch['core_limit'] == [0, 0]
    assert launch['launch_argv'] == c['parent_launch_argv'][3:] and context['outer_argv'] == c['parent_exec_argv'][3:]
    pre = (HERE / 'pre-call-manifest.json').read_bytes()
    assert launch['pre_call_manifest'] == {'bytes': len(pre), 'sha256': hashlib.sha256(pre).hexdigest()}
    assert datetime.fromisoformat(launch['utc']) <= datetime.fromisoformat(context['utc_start'])



def check():
 c=load('inputs.json');controls=D['selfchecks'](c);pre=load('pre-call-manifest.json')
 for x in pre['payloads']:
  got=D['identity'](HERE/x['path']);assert got['bytes']==x['bytes'] and got['sha256']==x['sha256']
 s,ctx,launch=[load(x) for x in ['execution-summary.json','execution-context.json','launch-receipt.json']];check_parent(c,ctx,s,launch)
 assert s['status']=='COMPLETE-106-ONCE' and s['attempted_children']==s['successful_protocols']==106 and s['error'] is None and s['retries']==0 and s['inherited_not_replayed']==11 and s['unattempted_ids']==[]
 assert s['selected_export_calls_with_valid_protocol']==23214 and s['CalcA_with_valid_protocol']==9222 and s['loader_initializer_entries_logged_separately']==106 and s['all_native_calls_count'] is None
 assert s['source_before']==s['source_after']==ctx['source_before']==c['source_pins']
 rs=[json.loads(x) for x in (HERE/'results.jsonl').read_text().splitlines()];fresh=[r for r in c['rows'] if r['disposition']=='fresh-planned'];assert len(rs)==len(fresh)==106 and len({r['pid'] for r in rs})==106
 points=[];fixture=None
 for row,r in zip(fresh,rs):
  folder=HERE/'attempts'/row['id'];assert sorted(x.name for x in folder.iterdir())==['output.f32','stderr.txt','stdout.txt']
  stdout,stderr,raw=[(folder/x).read_bytes() for x in ['stdout.txt','stderr.txt','output.f32']];observed=check_record(row,r,c,stdout,stderr,raw)
  points.append({'id':row['id'],'unique_vector':row['unique_vector'],'domain_index':row['domain_index'],'host_value':row['host_value'],'input_script':row['script'],'parameter_vector_sha256':row['parameter_vector_sha256'],'receipt_pointer':f"results.jsonl#line={row['fresh_ordinal']}",'pid':r['pid'],'output':r['output'],'observed_unsigned_summary':observed,'provenance':'fresh-once-only','prior_recipe_only_remains_historical_U':row.get('prior_recipe_only',False),'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
  if fixture is None:fixture=row,r,stdout,stderr,raw
 for prev,nxt in zip(rs,rs[1:]):assert prev['utc_end']<=nxt['utc_start']
 for row in c['rows']:
  if row['disposition']=='inherited-no-replay':points.append({'id':row['id'],'unique_vector':row['unique_vector'],'domain_index':row['domain_index'],'host_value':row['host_value'],'historical_input_reference':row['historical'],'provenance':'inherited-no-replay','fresh_pid':None,'fresh_receipt':None,'new_metrics':None,'waveform_prediction':None,'portable_expected':None,'portable_comparator':None,'candidate_grade':None})
 points.sort(key=lambda r:r['unique_vector']);assert len(points)==117 and [p['id'] for p in points]==[r['id'] for r in c['rows']]
 assert load('inherited-controls.json')=={'old_raw_audio_reads':0,'new_original_calls':0,'controls':[{'id':x['id'],'historical':x['historical']} for x in c['rows'] if x['disposition']=='inherited-no-replay']}
 row,r,stdout,stderr,raw=fixture;neg=[]
 for name,fn in [('inventbaselinefresh',lambda x:x.update(unique_vector=0)),('prior',lambda x:x.update(waveform_prediction='tone')),('exit',lambda x:x.update(exit=1)),('timeout',lambda x:x.update(timeout=True)),('argv',lambda x:x['argv'].__setitem__(2,'wrong.script')),('custody',lambda x:x['custody_after'][0].update(sha256='0'*64)),('flag',lambda x:x['protocol']['flags'][0].update(flag=4)),('rightsummary',lambda x:x['observed_output']['nonzero_sample_counts'].pop())]:
  bad=copy.deepcopy(r);fn(bad)
  try:check_record(row,bad,c,stdout,stderr,raw)
  except AssertionError:neg.append(name)
  else:raise AssertionError('acceptedreceipt '+name)
 for name,out,err,audio in [('stderr',stdout,b'fault',raw),('truncated',stdout,stderr,raw[:-8]),('changedraw',stdout,stderr,bytes([raw[0]^1])+raw[1:]),('changedlog',stdout+b'FAULT test\n',stderr,raw)]:
  try:check_record(row,r,c,out,err,audio)
  except AssertionError:neg.append(name)
  else:raise AssertionError('accepteddata '+name)
 parent=[]
 for name,fn in [('PID',lambda x:x.update(pid=1)),('env',lambda x:x['exec_environment'].update(XDEV_LIBM_ULP='1')),('preseal',lambda x:x['pre_call_manifest'].update(sha256='0'*64)),('execargv',lambda x:x['exec_argv'].__setitem__(3,'wrong.py'))]:
  bad=copy.deepcopy(launch);fn(bad);badctx=copy.deepcopy(ctx);badctx['parent_launch_receipt']=bad
  try:check_parent(c,badctx,s,bad)
  except AssertionError:parent.append(name)
  else:raise AssertionError('acceptedparent '+name)
 return {'status':'PASS packet-only finite-domain checks','controls':controls,'retained_negative_controls':neg,'parent_negative_controls':parent,'logical_alias_points':164,'unique_vectors':117,'fresh_children':106,'inherited_input_references_no_replay':11,'fresh_stereo_bytes':37396800,'selected_exports':23214,'CalcA':9222,'initializers_separate':106,'all_native_calls':None,'per_child_custody_pairs':len(rs[0]['custody_before']),'total_runtime_local_pairs':sum(len(r['custody_before']) for r in rs),'all_fresh_finite_both_channels':all(r['observed_output']['all_finite'] for r in rs),'all_fresh_stereo_byte_equal':all(r['observed_output']['channels_byte_identical'] for r in rs),'silent_fresh_ids':[r['id'] for r in rs if r['observed_output']['nonzero_sample_counts']==[0,0]],'points':points,'aliases':c['aliases'],'oldraw_audio_reads':0,'old_result_reads':0,'external_runtime_reads_by_checker':0,'checker_original_calls':0,'scope':'Declarednativehostdomains only,91=5notordinaryLiveemission/sign1at0/inactivegates/current/publicARMU;3recipeonlyoldbridgesremainU;NULLpriors/portablecriteria/grades/no f0/fit/newmetric/calibration/stability law.'}
if __name__=='__main__':
 assert sys.argv[1:]==['--check'];print(json.dumps(check(),indent=2,allow_nan=False))
