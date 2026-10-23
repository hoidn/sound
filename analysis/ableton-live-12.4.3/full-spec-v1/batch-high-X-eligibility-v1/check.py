"""Data-only checks of this planning packet. No runtime/image/source-function reads."""
import copy,json,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parent

def validate(e,s,x):
    assert e['common']['execution_selected'] is False
    assert e['common']['new_original_calls']==0
    assert e['priority_decision'].startswith('DEFERRED')
    assert x['counts']==dict(analog=199,electric=149,tension=71,corpus=49,playback=43)
    assert len(x['rows'])==511
    assert all(not r['public_credit'] for r in x['rows'])
    p=s['analog']['P1_whole_expansion'];v=p['new_single_control_vectors']
    assert len(v)==20 and p['total_renders']==21
    assert len({(r['host_index'],r['host_value']) for r in v})==20
    assert len({r['host_index'] for r in v})==12
    assert {r['host_index'] for r in v}=={89,90,91,101,102,103,172,173,174,184,185,186}
    assert all(r['baseline_host_value']==0 for r in v)
    assert 'BLOCKED PHYSICAL ORACLE' in e['families'][3]['whole_classes'][2]['eligibility']
    assert '176' in e['families'][3]['whole_classes'][2]['class']
    assert 'WITHHELD' in e['families'][4]['whole_classes'][2]['eligibility']
    assert e['families'][0]['P1_protocol']['direct_export_calls_per_child']==293
    assert e['families'][0]['P1_protocol']['output_bytes_per_child']==352800

def main():
    e=json.loads((P/'eligibility.json').read_text());s=json.loads((P/'finite-class-selectors.json').read_text());x=json.loads((P/'mapped-X-contexts.json').read_text());validate(e,s,x)
    mutations=[lambda a,b,c:a['common'].__setitem__('execution_selected',True),lambda a,b,c:a.__setitem__('priority_decision','SELECTED'),lambda a,b,c:c['counts'].__setitem__('analog',0),lambda a,b,c:c['rows'][0].__setitem__('public_credit',True),lambda a,b,c:b['analog']['P1_whole_expansion']['new_single_control_vectors'].pop(),lambda a,b,c:a['families'][3]['whole_classes'][2].__setitem__('eligibility','ready'),lambda a,b,c:a['families'][4]['whole_classes'][2].__setitem__('eligibility','eligible'),lambda a,b,c:a['families'][0]['P1_protocol'].__setitem__('direct_export_calls_per_child',256)]
    for m in mutations:
        a,b,c=copy.deepcopy((e,s,x));m(a,b,c)
        try:validate(a,b,c)
        except AssertionError:pass
        else:raise AssertionError('false promotion accepted')
    print(json.dumps({'status':'PASS','negative_controls':len(mutations),'scope':'owned planning data only; no original/image/loader read or invocation'}))
if __name__=='__main__':main()
