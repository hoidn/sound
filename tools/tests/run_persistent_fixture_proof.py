#!/usr/bin/env python3
"""Actual bounded synthetic Ghidra proof; never imports or executes Live bytes."""
import argparse
import importlib.util
from pathlib import Path
import time
import traceback

SPEC=importlib.util.spec_from_file_location('persistent_native',Path(__file__).parents[1]/'run_persistent_native.py')
p=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p)


def script_fault(name,kind):
    def fault(stage,config):
        path=stage/'scripts'/name
        if kind=='compile':path.write_text('This intentionally is not valid Java.\n')
        elif kind=='constructor':
            path.write_text('import ghidra.app.util.headless.HeadlessScript; public class '+path.stem+' extends HeadlessScript {public '+path.stem+'(){if(System.nanoTime()>0)throw new IllegalStateException("Fixture constructor failure");} public void run() throws Exception {} }\n')
        elif kind=='execution':
            path.write_text('import ghidra.app.util.headless.HeadlessScript; public class '+path.stem+' extends HeadlessScript {public void run() throws Exception {enableHeadlessAnalysis(false);setHeadlessContinuationOption(HeadlessContinuationOption.ABORT);throw new IllegalStateException("Fixture execution failure");} }\n')
        elif kind=='missing-outcome':
            path.write_text('import ghidra.app.util.headless.HeadlessScript; public class '+path.stem+' extends HeadlessScript {public void run() throws Exception {enableHeadlessAnalysis(false);Thread.sleep(30000);} }\n')
    fault.__name__=kind+'-'+name
    return fault


def ack_fault(kind):
    def fault(ack):
        if kind=='absent':return None
        if kind=='late':time.sleep(11);return ack
        if kind=='nonce':ack['nonce']='0'*32
        if kind=='pid':ack['pid']+=1
        if kind=='hash':ack['gate_sha256']='0'*64
        return ack
    return fault


def run(output,*,positive_only=False):
    root=p.fresh(output);target=root/'fixture.bin';target.write_bytes(p.FIXTURE_BYTES)
    pins=p.method_pins();results=[]
    p.publish(root/'initial.json',{'schema':1,'methods':pins,'runner_sha256':p.sha(Path(__file__)),'target_sha256':p.FIXTURE_SHA,
              'free_bytes':p.shutil.disk_usage(root).free,'fixture_limit_bytes':p.GIB,'disk_floor_bytes':3*p.GIB})
    def case(name,fn):
        print('CASE '+name,flush=True);start=time.monotonic()
        value=fn();p.publish(root/(name+'.case.json'),{'schema':1,'status':'pass','duration_seconds':time.monotonic()-start,'result':str(value)})
        results.append({'case':name,'status':'pass'});return value
    baseline=case('baseline',lambda:p.import_job(root/'baseline',target,fixture=True))
    empty=case('empty-external-inventory',lambda:p.export_job(root/'empty-external',baseline,fixture=True))
    if p.read_inventory(empty)[1]['external']!=0:raise AssertionError('simple fixture external count')
    expanded=case('expanded-baseline',lambda:p.import_job(root/'expanded',target,fixture=True,fixture_expanded=True))
    inventory=case('expanded-inventory',lambda:p.export_job(root/'inventory',expanded,fixture=True))
    entries,summary=p.read_inventory(inventory,requested={'ram:0x0','ram:0x10','ram:0x20','ram:0x30','ram:0x40'})
    if (summary['ordinary'],summary['external'],summary['total'])!=(5,1,6):raise AssertionError('ordinary/external reconciliation')
    keys=[e['key'] for e in entries];keys.sort()
    one=case('export-one',lambda:p.export_job(root/'export-one',expanded,fixture=True,inventory=inventory,entries=['ram:0x0']))
    five=case('export-five',lambda:p.export_job(root/'export-five',expanded,fixture=True,inventory=inventory,entries=keys))
    for stage in (one,five):
        for metadata in (stage/'exports').glob('*/metadata.json'):
            record=p.read_json(metadata)
            if record['state'] not in ('exported','exported-with-warnings') or not record['native_children'] or not all(x['closed'] for x in record['native_children']):raise AssertionError('actual native decompiler closure/export')
            if 'return 0' not in (metadata.parent/'pseudocode.c').read_text():raise AssertionError('independent constant-return fixture code')
    finite=case('finite-analysis',lambda:p.analysis_job(root/'finite',expanded,fixture=True))
    if p.load_checkpoint(finite)['partial']:raise AssertionError('tiny finite pass unexpectedly timed out')
    partial=case('cooperative-timeout',lambda:p.analysis_job(root/'timeout',expanded,fixture=True,fixture_timeout=True))
    manifest=p.load_checkpoint(partial)
    if not manifest['partial']:raise AssertionError('cooperative timeout must be partial')
    timeout_out=p.read_json(root/'timeout/analysis/analysis-outcome.json')
    if timeout_out['fixture_timeout_marker']!=timeout_out['nonce']:raise AssertionError('scheduled timeout marker did not persist')
    partial_inventory=case('partial-inventory',lambda:p.export_job(root/'partial-inventory',partial,fixture=True))
    if p.read_inventory(partial_inventory)[1]['partial'] is not True:raise AssertionError('partial provenance lost')
    def finish():
        if p.method_pins()!=pins:raise AssertionError('production methods changed during final proof')
        if p.allocated_tree(root)>p.GIB:raise AssertionError('retained fixture suite exceeded 1 GiB')
        report={'schema':1,'status':'pass','scope':'positive-replay' if positive_only else 'positive-and-negative',
                'methods':pins,'runner_sha256':p.sha(Path(__file__)),'cases':results,'launches':len(list(root.rglob('stage-result.json'))),
                'allocated_bytes':p.allocated_tree(root),'logical_bytes':sum(x.stat().st_size for x in root.rglob('*') if x.is_file()),
                'native_bytes_executed':False,'target_live_imported':False,'limitations':['Synthetic persistence and failure proofs only; no target checkpoint or compatibility result.']}
        p.publish(root/'report.json',report);print('FINAL PASS '+str(root),flush=True)
        return report
    if positive_only:return finish()
    def negative(name,*,gate_name='RecoveryLaunchGate.java',outcome_name='RecoveryAnalysisOutcome.java',fault=None,ack=None,processing=False):
        job,_=p.prepare_job(root/name,target,fixture=True)
        if processing:
            parent=p.load_checkpoint(expanded);project=p.copy_project(expanded/'project',job/'project',parent['project'],budget_root=job,budget_limit=p.GIB)
        else:project=p.fresh(job/'project')
        try:
            p.run_stage(job/'stage',project,target,fixture=True,importing=not processing,mode='enable-analysis-after-ack' if processing else 'verify-only',
                fixture_timeout=processing,gate_name=gate_name,outcome_name=outcome_name,fixture_fault=fault,ack_fault=ack,allocation_root=job)
        except RuntimeError:
            result=p.read_json(job/'stage/stage-result.json')
            if result['status']!='fail' or result['closure']['closed'] is not True or not result['closure']['reaped'] or result['closure']['survivors']:raise AssertionError('negative case did not close owned processes')
            if (job/'checkpoint').exists():raise AssertionError('failed stage published checkpoint')
            if processing:p.verify_project(expanded/'project',parent['project'])
            return result['error']
        raise AssertionError('negative case accepted '+name)
    case('gate-missing',lambda:negative('gate-missing',gate_name='RecoveryMissingGate.java'))
    for kind in ('compile','constructor','execution'):
        case('gate-'+kind,lambda kind=kind:negative('gate-'+kind,fault=script_fault('RecoveryLaunchGate.java',kind)))
    for kind in ('absent','nonce','pid','hash','late'):
        case('ack-'+kind,lambda kind=kind:negative('ack-'+kind,ack=ack_fault(kind)))
    case('outcome-missing',lambda:negative('outcome-missing',processing=True,outcome_name='RecoveryMissingOutcome.java'))
    for kind in ('compile','constructor','execution','missing-outcome'):
        case('outcome-'+kind,lambda kind=kind:negative('outcome-'+kind,processing=True,fault=script_fault('RecoveryAnalysisOutcome.java',kind)))
    return finish()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--positive-only',action='store_true');args=parser.parse_args()
    import fcntl
    lock_path=Path(__file__).resolve().parents[2]/'analysis/ableton-live-12.4.3/.persistent-native-controller.lock'
    with lock_path.open('a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        run(args.output,positive_only=args.positive_only)
