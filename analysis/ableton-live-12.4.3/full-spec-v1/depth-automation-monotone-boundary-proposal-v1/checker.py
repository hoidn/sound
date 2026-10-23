"""Read-only analyst arithmetic/data check; no original/harness execution interface."""
import collections
import copy
import hashlib
import json
from pathlib import Path
import runpy
import struct
import sys

P=Path(__file__).resolve().parent
O=runpy.run_path(str(P/'oracle.py'))
J=lambda p:json.loads(Path(p).read_text())
H=lambda b:hashlib.sha256(b).hexdigest()


def require(ok, why):
    if not ok:
        raise AssertionError(why)


def argv_for(process, byid):
    return process['argv_prefix']+sum([byid[i]['tokens'] for i in process['vector_ids']],[])


def validate(d):
    anchors,families,vectors=O['universe']()
    ins, bounds, lineage, shapes=d['inputs'],d['boundaries'],d['lineage'],d['shapes']
    require(ins['schema']=='automation-M-closed-finite-boundary-input-proposal-v1','schema')
    require(ins['original_calls']==0 and ins['actual_execution_selected'] is False,'proposal only')
    require(ins['withheld_factory_registry_converter_rows']==50,'whole withheld50class')
    require(ins['vectors']==vectors and bounds['anchors_binary64']==anchors and bounds['neighbor_families']==families,'exact closed finite universe/oracles')
    require(len(anchors)==42 and len(families)==64 and len(vectors)==2138,'closed42/64/2138')
    require(len({tuple(r['pair_binary64']) for r in vectors})==2138,'unique exact-bit pairs')
    bypair={tuple(r['pair_binary64']):r for r in vectors}
    # Independent bit/token roundtrip; no libc or original function call.
    for r in ins['vectors']:
        require(len(r['arguments_binary64'])==4 and r['arguments_binary64'][0]=='0x0000000000000000' and r['arguments_binary64'][-1]=='0x3ff0000000000000','fixedpositiveendpoints')
        require(r['tokens'][:2]==['call','0x1011f2080'] and len(r['tokens'])==6,'receiver-free four-double shape')
        for raw,t in zip(r['arguments_binary64'],r['tokens'][2:]):
            require(t.startswith('d:'),'double token only')
            text=t[2:]
            x=float.fromhex(text) if '0x' in text else float(text)
            require(f'0x{struct.unpack("<Q",struct.pack("<d",x))[0]:016x}'==raw,'exact token bit roundtrip')
    require(dict(collections.Counter(str(r['expected_boolean']) for r in vectors))=={'True':578,'False':1301,'None':259},'oracle partition')
    require(sum(r['R5_vs_exact_cubic'] is True for r in vectors)==92,'separate exact cubic context')
    for x in anchors:
        for y in anchors:
            require('whole-anchor-Cartesian-grid' in bypair[(x,y)]['memberships'],'whole grid coverage')
    for fam in families:
        for x in fam['x_neighbors']:
            for y in fam['y_neighbors']:
                require(fam['id'] in bypair[(x,y)]['memberships'],'whole3x3family coverage')
    require(len(lineage['overlap_records'])==10 and lineage['new_pair_count']==2128,'prior10/new2128')
    old=d['prior_inputs']['processes'][0]
    require(old['id']=='01-monotone' and len(old['argument_bits'])==40,'prior actual M record')
    for k,x in enumerate(lineage['overlap_records']):
        p=tuple(a['uint_hex'] for a in old['argument_bits'][4*k+1:4*k+3])
        p=tuple(f'0x{int(a,16):016x}' for a in p)
        require(x['prior_call_index']==k and x['pair_binary64']==list(p),'exact prior bit lineage')
        r=bypair[p]
        require(x['proposal_id']==r['id'] and r['expected_boolean']==old['expected_boolean'][k] and x['prior_RAX_and_1']==old['expected_boolean'][k],'all10retainedlocalresults')
    byid={r['id']:r for r in vectors}
    ps=shapes['processes']
    require(len(ps)==17 and [p['native_calls'] for p in ps]==[128]*16+[90],'whole17process shape')
    require([i for p in ps for i in p['vector_ids']]==[r['id'] for r in vectors],'eachinputonce contiguouswholebatch')
    for p in ps:
        require(p['argv_prefix']==['/var/tmp/sound-analysis/xexec/x2-envelope-warp/xexec2','/var/tmp/sound-analysis/helpers/Live_x86_64/Live_x86_64.x86_64','--imports'],'unchanged loader/image prefix')
        argv=argv_for(p,byid)
        require(p['native_calls']==len(p['vector_ids']) and p['argv_token_count']==len(argv),'argv count')
        require(p['argv_utf8_bytes_with_NUL']==sum(len(t.encode())+1 for t in argv),'exact argv bytes')
        require(p['argv_json_sha256']==H(json.dumps(argv,separators=(',',':')).encode()),'exact proposed argv identity')
        require(p['largest_argument_bytes_with_NUL']==max(len(t.encode())+1 for t in argv),'argument length')
    require(shapes['maximum_argv_bytes']==max(p['argv_utf8_bytes_with_NUL'] for p in ps) and shapes['maximum_argument_bytes']==max(p['largest_argument_bytes_with_NUL'] for p in ps),'maximum argv aggregates')
    require(shapes['ARG_MAX_observed']==2097152 and shapes['maximum_argv_bytes']<32768 and shapes['maximum_argument_bytes']<128,'ARGMAX modest bound')
    require(shapes['raw_stdout_estimate_bytes']==17*102400+2138*160==2082880,'raw stdout estimate')
    require(shapes['all_NULL_rows_retained'] is True and shapes['per_process_timeout_seconds']==20 and shapes['automatic_retry'] is False,'NULLretained/no retry')
    require(shapes['actual_selected'] is False and shapes['new_setup_or_harness_required'] is False,'no new setup selected')
    return True


def arithmetic_controls():
    F=O['F']; exact=O['exact_cubic']; cl=O['classify']; bits=O['bits']
    require(O['sqrt_compare'](F(2),F(1))==1 and O['sqrt_compare'](F(2),F(3,2))==-1,'exactradical comparator')
    require(O['sqrt_compare'](F(9),F(3))==0 and O['sqrt_compare'](F(0),F(-1))==1,'radicalequality/negative threshold')
    for x,y,yes in [(0.,0.,True),(1.,1.,True),(1.,0.,True),(.8,.2,True),(1.5,-.5,False),(-2.**-1074,.5,False),(.5,1.+2.**-52,False)]:
        require(exact(x,y)['boolean']==yes,'independent exactcubic analytic case')
    tangent=cl(bits(1.),bits(0.))
    require(tangent['expected_boolean'] is True and tangent['exact_cubic_separate']['minimum_sign']==0,'tangent equality')
    tol=cl(bits(0.),bits(-2.**-26))
    require(tol['expected_boolean'] is True and tol['exact_cubic_separate']['boolean'] is False and tol['exact_rational_R5']['D_compare_epsilon']==0,'tolerance versus exactmath')
    for x,y in [(-1.,-2/3),(1.,4/3)]:
        r=cl(bits(x),bits(y));require(r['expected_boolean'] is None and 'q-zero' in r['binary64_literal_R5']['path'],'qzero unresolvednotfailed')
    return 13


def main():
    require(sys.argv[1:]==['--check'],'only data-only --check')
    pins=J(P/'source-pins.json')
    # Only one explicitly pinned immutable prior data document is opened here.
    old=pins['checker_allowed_external_read']
    require(Path(old['path'])==P.parent/'batch-automation-eligible-leaves-v1/inputs.json','prior exactallowlist')
    raw=Path(old['path']).read_bytes()
    require(len(raw)==old['bytes'] and H(raw)==old['sha256'],'prior immutable input pin')
    d={'inputs':J(P/'inputs.json'),'boundaries':J(P/'boundaries.json'),'lineage':J(P/'lineage.json'),'shapes':J(P/'process-shapes.json'),'prior_inputs':json.loads(raw)}
    validate(d)
    controls=[
      ('firstN truncation',lambda b:b['inputs']['vectors'].pop()),
      ('NULL input silently omitted',lambda b:b['inputs'].update(vectors=[r for r in b['inputs']['vectors'] if r['expected_boolean'] is not None])),
      ('NULL invented as failure',lambda b:next(r for r in b['inputs']['vectors'] if r['expected_boolean'] is None).update(expected_boolean=False)),
      ('exactmath substituted for literal tolerance',lambda b:next(r for r in b['inputs']['vectors'] if r['R5_vs_exact_cubic'] is True).update(expected_boolean=False)),
      ('anchor missing',lambda b:b['boundaries']['anchors_binary64'].pop()),
      ('neighbor family missing',lambda b:b['boundaries']['neighbor_families'].pop()),
      ('one coordinate neighbor dropped',lambda b:b['boundaries']['neighbor_families'][0]['x_neighbors'].pop()),
      ('positive endpoint changed',lambda b:b['inputs']['vectors'][0]['arguments_binary64'].__setitem__(0,'0x8000000000000000')),
      ('qNaN payload replaced',lambda b:next(r for r in b['inputs']['vectors'] if '0x7ff8000000000000' in r['pair_binary64'])['pair_binary64'].__setitem__(0,'0x7ff8000000000001')),
      ('prior lineage changed',lambda b:b['lineage']['overlap_records'][0].update(prior_call_index=9)),
      ('process drops input',lambda b:b['shapes']['processes'][-1]['vector_ids'].pop()),
      ('argv byte bound invented',lambda b:b['shapes']['processes'][0].update(argv_utf8_bytes_with_NUL=1)),
      ('new loader substituted',lambda b:b['shapes']['processes'][0]['argv_prefix'].__setitem__(0,'/wrong/loader')),
      ('factory rows admitted',lambda b:b['inputs'].update(withheld_factory_registry_converter_rows=0)),
      ('actual execution invented',lambda b:b['inputs'].update(actual_execution_selected=True)),
      ('new setup invented',lambda b:b['shapes'].update(new_setup_or_harness_required=True)),
      ('retry allowed',lambda b:b['shapes'].update(automatic_retry=True)),
    ]
    rejected=[]
    for name,mutate in controls:
        bad=copy.deepcopy(d);mutate(bad)
        try:validate(bad)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('negative accepted: '+name)
    print(json.dumps({'status':'PASS-data-only-proposal','vectors':2138,'known_expected':1879,'NULL_expected_retained':259,'prior_pairs':10,'new_input_pairs':2128,'processes_proposed':17,'negative_controls':rejected,'negative_count':len(rejected),'analytic_positive_assertions':arithmetic_controls(),'original_harness_model_renderer_calls':0,'new_source_index_image_provider_reads':0,'external_document_reads':1}))


if __name__=='__main__':
    main()
