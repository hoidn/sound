#!/usr/bin/env python3
"""Additive POST-CAPTURE data-only control correction, NOT pre-call-bound capture code.

Frozen checker failure is retained unchanged. Only its in-memory negative-control
function is replaced; recorder, parser, inputs, raw results and original processes
are unchanged. No original/runtime/provider/old source read or call occurs here.
"""
import hashlib,importlib.util,inspect,json,os,pathlib,sys
H=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(n,d):
 with (H/n).open('x') as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def identity(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
assert sys.argv[1:] in (['--check-and-write'],['--check'])
writing=sys.argv[1:]==['--check-and-write']
assert not writing or not (H/'author-check.json').exists()
pre=json.loads((H/'pre-call-manifest.json').read_text())
for item in pre['frozen_files']:
 b=pathlib.Path(item['path']).read_bytes();assert len(b)==item['bytes'] and sha(b)==item['sha256']
s=importlib.util.spec_from_file_location('owned_frozen_checker',H/'check-recorded.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
d=json.loads((H/'inputs.json').read_text());results=json.loads((H/'results.json').read_text());plan=d['plans'][0];child=results['children'][0]
text=pathlib.Path(child['stdout']['path']).read_text();synthetic=C.synthetic(d,plan)
old=lambda t:t.replace('used synth_linux_0','used synth_data_0')
def data_mutation(t):
 used=next(x.split() for x in t.splitlines() if x.startswith('used '))
 data=next(x.split()[2] for x in t.splitlines() if x.startswith('import data '))
 before='used '+used[1]+' '+used[2];after='used '+data+' '+used[2]
 assert t.count(before)==1 and before!=after
 return t.replace(before,after,1)
assert old(text)==text and old(synthetic)!=synthetic
changed=data_mutation(text);assert changed!=text
C.R.parse_output(text,'',0,plan,d)
try:C.R.parse_output(changed,'',0,plan,d)
except AssertionError:corrected_rejected=True
else:raise AssertionError('actual data-as-code mutation accepted')
original_source=inspect.getsource(C.log_controls)
old_expression="text.replace('used synth_linux_0','used synth_data_0')"
assert original_source.count(old_expression)==1
corrected_source=original_source.replace(old_expression,'data_mutation(text)')
namespace=dict(C.__dict__);namespace['data_mutation']=data_mutation
exec(compile(corrected_source,str(H/'post-capture-check.py')+':additive-control','exec'),namespace)
C.log_controls=namespace['log_controls']
out=C.check()
assert out['status']=='PASS' and len(out['actual_protocol_negatives'])==20
out['frozen_original_checker_status']='FAIL: data_as_code was a no-op on actual stdout; exact original failure retained'
out['analysis_scope']='Full unchanged data checks with only documented in-memory negative-control substitution; this additive source was NOT pre-call-bound. No actual/capture/source/inputs repaired or retried.'
if writing:save('author-check.json',out)
else:assert json.loads((H/'author-check.json').read_text())==out
proof={'status':'PASS additive data-only correction','source':identity(H/'post-capture-check.py'),'not_pre_call_bound':True,'frozen_checker':identity(H/'check-recorded.py'),'old_expression':old_expression,'corrected_expression':'data_mutation(text)','old_mutation_equals_actual_input':old(text)==text,'old_mutation_changes_synthetic':old(synthetic)!=synthetic,'corrected_mutation_changes_actual':changed!=text,'corrected_mutation_rejected_by_unchanged_parser':corrected_rejected,'original_used_line':next(x for x in text.splitlines() if x.startswith('used ')),'new_data_used_line':next(x for x in changed.splitlines() if x.startswith('used ')),'positive_unmutated_actual_parser':'PASS','full_data_checks':out['totals'],'actual_negative_controls':out['actual_protocol_negatives'],'original_checker_success_claimed':False,'all_analysis_pre_call_bound_claimed':False,'capture_parent_recorder_input_edits':0,'original_retries':0,'original_calls_by_additive_checker':0,'external_runtime_reads':0}
if writing:save('post-capture-control-report.json',proof)
print(json.dumps({**{k:v for k,v in out.items() if k not in ['alias_catalog','vector_catalog']},'post_capture_control_proof':proof}))
