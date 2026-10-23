"""Read-only stdlib family packet integrity. No author modules or tool execution."""
from pathlib import Path
import collections
import copy
import hashlib
import json
import re
import struct
import sys

P = Path(__file__).resolve().parent
F = P.parent
D = F/'modulation-pitch-loop'
H = lambda b: hashlib.sha256(b).hexdigest()
OH = lambda x: H(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
J = lambda p: json.loads(Path(p).read_bytes())


def need(ok, message):
    if not ok:
        raise ValueError(message)


def pointer(obj, path):
    need(path.startswith('/'), 'JSON pointer root')
    for token in path.split('/')[1:]:
        token=token.replace('~1','/').replace('~0','~')
        obj=obj[int(token)] if isinstance(obj,list) else obj[token]
    return obj


def identity(p):
    path=Path(p['path'])
    need(path.stat().st_size==p['bytes'], 'selected input size')
    h=hashlib.sha256()
    with path.open('rb') as source:
        for raw in iter(lambda:source.read(1048576),b''):h.update(raw)
    need(h.hexdigest()==p['sha256'], 'selected input digest')


def historical_prefix(info):
    with Path(info['path']).open('rb') as source:raw=source.read(info['bytes'])
    need(len(raw)==15924 and H(raw)==info['sha256']=='21d2e4e5728019971132fa6779f810fe279b9e4b590b737492c205c5b3a07be5','complete research prefix')


def raw_row(row):
    with Path(row['provider']).open('rb') as source:
        if row['source_byte']:
            source.seek(row['source_byte']-1);need(source.read(1)==b'\n','row boundary')
        source.seek(row['source_byte']);raw=source.read(row['raw_bytes'])
    need(len(raw)==row['raw_bytes'] and raw.endswith(b'\n') and H(raw)==row['raw_sha256'],'exact raw selected row')
    original=json.loads(raw)
    if row['kind']=='table-data':
        expected=dict(original);size=len(original['slots'])
        expected.update(exported_prefix_slot_count=size,slots=original['slots'][:3] if size>16 else original['slots'],selection_policy='large leading3 construction/lifetime frontier only' if size>16 else 'whole small exported prefix',complete_native_table_class_function_or_processing_claim=False)
        need(row['record']==expected,'exact whole-small/leading3 table projection')
    else:need(row['record']==original,'exact selected metadata record')


def native_scope(rows, seeds, approval, proposal):
    counts=collections.Counter(r['kind'] for r in rows)
    need(counts=={'lexical-owner-data':120,'membership-data':133,'alias-data':133,'RTTI-data':32,'table-data':32,'store-data':67,'call-data':160,'indirect-data':27},'all704 selected row kinds')
    need(len({(r['provider'],r['source_byte']) for r in rows})==704,'no duplicate metadata row padding')
    aliases={r['record']['entry']:r for r in rows if r['kind']=='alias-data'}
    need(len(seeds['entries'])==133 and {r['entry'] for r in seeds['entries']}==set(aliases),'whole133 named alias frontier')
    chosen=set();excluded=set()
    name_group=re.compile(r'::(?:OnActiveViewCountChanged|OnActiveViewCount|OnAllowTextVisualizationUpdateTimer|OnUpdateDisplay|OnTimer)(?=>)')
    for s in seeds['entries']:
        a=rows[s['alias_native_data_line']-1]
        need(a['kind']=='alias-data' and a['record']['entry']==s['entry'] and a['record']['name']==s['name'],'seed alias identity')
        expected=not bool(name_group.search(s['name']))
        need(s['selected_outgoing_seed']==expected,'whole method-group seed predicate')
        (chosen if expected else excluded).add(s['entry'])
    need(excluded==set(approval['exact_seed_exclusions']) and len(chosen)==122,'exact11excluded/122selected')
    tables=[r['record'] for r in rows if r['kind']=='table-data']
    points={r['address_point']:r for r in tables}
    need({(r['literal_type_encoding'],r['address_point']) for r in tables}=={(r['type'],r['address_point']) for r in proposal['proposed_classes']['classes']},'approved class/addresspoint scope')
    need(sum(len(r['slots']) for r in tables)==102 and sum(r['exported_prefix_slot_count'] for r in tables)==1770 and sum(r['exported_prefix_slot_count']>16 for r in tables)==20,'102of1770slots20large/12small')
    rtti={r['record']['address']:r['record'] for r in rows if r['kind']=='RTTI-data'}
    for t in tables:
        need(t['offset_to_top']==0 and t['native_table_extent'] is None and not t['complete_native_table_class_function_or_processing_claim'],'qualified primary prefix')
        need(int(t['address_point'],16)==int(t['table_header'],16)+16 and t['address_point_file_offset']==t['header_file_offset']+16,'header point geometry')
        need(struct.unpack('<qQ',bytes.fromhex(t['raw_header16_hex']))==(0,int(t['typeinfo'],16)),'header raw16 values')
        ti=rtti[t['typeinfo']]
        need(ti['literal_type_encoding']==t['literal_type_encoding'] and bytes.fromhex(ti['name_NUL_hex'])==t['literal_type_encoding'].encode()+b'\0','RTTI literal identity')
        for i,s in enumerate(t['slots']):need(s['offset']==i*8 and int.from_bytes(bytes.fromhex(s['raw8_hex']),'little')==int(s['target'],16),'slot raw8 identity')
    scopes={r['record']['scope_id'] for r in rows if r['kind']=='lexical-owner-data'}
    for r in rows:
        d=r['record']
        if r['kind']=='membership-data':
            need(any(c[1] in scopes for c in d['candidates']) and d['entry'] in aliases,'lexical membership join')
            a=aliases[d['entry']]
            need(d['source']==[a['source_line'],a['source_byte'],a['raw_bytes']],'membership alias locator')
        elif r['kind']=='store-data':need(d['address_point'] in points and d['address_point'][2:] in d['quote'],'literal store metadata join')
        elif r['kind']=='call-data':need(d['caller'] in chosen,'outgoing ONLY selected seed; no incoming/transitive')
        elif r['kind']=='indirect-data':need((d.get('function') in chosen or d.get('caller') in chosen) and d['resolved_targets']==[],'unresolved selected indirect remainsU')
    return chosen


def owner_spans(spans,req,spec):
    need(len(spans)==106 and {s['requirement'] for s in spans}=={r['id'] for r in req},'all complete owner bodies')
    for i,s in enumerate(spans):
        r=pointer(req,s['catalog_pointer'])
        need(r['id']==s['requirement'] and OH(r)==s['record_sha256'] and H(r['contract'].encode())==s['contract_sha256'],'whole immutable contract record')
        for q in s['source_spans']:
            b=spec[q['byte_start']:q['byte_start']+q['byte_length']]
            need(len(b)==q['byte_length'] and H(b)==q['sha256'],'owner raw span')
            need(spec[:q['byte_start']].count(b'\n')+1==q['line_start'] and spec[:q['byte_start']+q['byte_length']].count(b'\n')+1==q['line_end'],'owner line geometry')
        if r['strength']=='D12':
            q=s['source_spans'][0]
            need(spec[q['byte_start']:q['byte_start']+q['byte_length']].decode()==r['contract'],'complete literal D12 contract')
        else:need(len(s['source_spans'])==2 and 'derived' in s['source_role'],'U derived catalog distinct from literal summary/matrix')


def ledger_check(ledger,req,cases):
    rows=ledger['required_outcomes']
    need(len(rows)==106 and len({r['id'] for r in rows})==106 and len({r['requirement'] for r in rows})==106,'one106whole-clause unit inventory')
    need(ledger['required_units']==106 and ledger['route_inventory']=={'X':0,'S':0,'no_established':106},'no file/helper/context padding')
    need(collections.Counter(r['source_annotation'] for r in rows)=={'D12':96,'U':10},'same106 source annotations')
    need(ledger['closure_gate']=='OPEN' and ledger['new_grade_spec_case_release_site_credit']==0,'coverage staysopen')
    for i,(r,q) in enumerate(zip(rows,req,strict=True)):
        need(r['requirement']==q['id'] and r['predicate']==q['contract'] and r['device']==q['device'] and r['source_annotation']==q['strength'],'whole clause limits/predicates unchanged')
        need(r['unit']=='whole complete current clause bundle; not atomic outcome' and r['owner_span_pointer']==f'owner-spans.json#/{i}','whole-clause unit not atomic facet claim')
        need(r['route']=='no-established-route' and r['actual_status']=='U' and r['exact_target_applicability']=='U' and r['public_binding']=='unknown' and not r['grade_changed'],'no D12/name/file/public promotion')
        need(r['related_cases_navigation_only']==[c['id'] for c in cases if q['id'] in c['requirements']] and r['related_cases_navigation_only'],'all current complete actions associated')
        need(r['missing_join'] and r['enumeration'],'required unsupported contexts explicit')
    need(len(ledger['auxiliary'])==10 and all(not a['required_outcome'] and a['route']=='S-route' and not a['raw_reopened'] for a in ledger['auxiliary']),'auxfileonly outside106')


def case_navigation(nav,cases,overlay,adoption):
    need(len(nav)==len(cases)==len(overlay)==208 and len(adoption)==22,'complete208/22 currentcase metadata')
    need(len({o['id'] for o in overlay})==208 and len({a['case_id'] for a in adoption})==22,'no duplicate references')
    for i,(n,c,o) in enumerate(zip(nav,cases,overlay,strict=True)):
        need(n['id']==c['id']==o['id'] and pointer(cases,n['pointer'])==c and n['pointer']==f'/{i}','case pointer dereference')
        need(n['record_sha256']==OH(c) and n['field_sha256']=={k:OH(v) for k,v in c.items()} and n['keys']==sorted(c),'all fullcase fields')
        need(pointer(cases,o['case_pointer'])['id']==o['id'] and o['case_pointer']==f'/{i}','actual R4 top-level list pointer')
        need(n['overlay_pointer']==f'/cases/{i}' and n['actual_record_sha256']==OH(o),'overlay dictionary pointer distinct from case list')
        need(c['expected'] is None and c['target_grade']=='U' and not c['executed'] and o['actual_expected'] is None and o['actual_comparison'] is None and o['target']=='U' and not o['executed'],'actualU not documentary result')
        if i>=186:need(c['documentary_expected'] is None and c['documentary_comparator'] is None and c['actual_comparison'] is None,'new oracles remainnull')
    for a in adoption:need(pointer(cases,a['case_pointer'])['id']==a['case_id'],'adoption R4 real list dereference')


def productive(prereq):
    need(all(w in prereq['common']['signal'] for w in ['NONEMPTY','NONZERO','EACH','BOTH','BEFORE']),'real independent signal baselines')
    need('remain U' in prereq['common']['lifecycle'],'lifecycle unknown not pass')
    for code,words in {'AS':['MIDI Off/Quantizer','latch/release','full wet'], 'PF':['EnvFol On','nonzero','BOTH'], 'SH':['Hertz','no ms/reciprocal','Internal'], 'SR':['Mono','GateOff','Poly','NONEMPTY'], 'ST':['Freezer On AND Freeze','NONZERO','Frz>Dly','Dly>Frz','X-Fade'], 'VO':['BOTH','EACH','Unvoiced'], 'BR':['RepeatOff','Chance100','BEFORE0'], 'LP':['NONZERO','Clear','BOTH InsertLooper','MonitorIn']}.items():
        need(all(w in prereq['devices'][code] for w in words),'device actual guard/context preserved '+code)


def file_auxiliary(auxiliary, packages, associations):
    need(len(auxiliary)==len(packages)==len(associations)==10,'ten bounded file observations')
    for i,aux in enumerate(auxiliary):
        p=pointer(packages,aux['pointer']);a=pointer(associations,aux['association_pointer'])
        need(aux['pointer']==aux['association_pointer']==f'/{i}' and OH(p)==aux['record_sha256'] and OH(a)==aux['association_sha256'],'file and reconciliation record pins')
        need(aux['historical_inventory_surface']==p['inventory_surface']==a['historical_inventory_surface'],'historical source ID kept distinct')
        need(aux['corrected_inventory_surface']==a['corrected_inventory_surface'] and aux['source_id_is_historical']==a['source_id_is_historical'],'corrected artifact association explicit')
        need(aux['class_name']==p['class']==a['class'] and aux['root_locator']==p['locator'] and p['file']==a['retained_preset'],'class/root/file association')
        need(not aux['required_outcome'] and not aux['raw_reopened'] and aux['route']=='S-route','artifact only not applicationS')


def source_geometry(geometry,audit,cases,html):
    need(len(geometry['blocks'])==len(audit['blocks'])==332,'332source geometry,not333')
    for i,(g,b) in enumerate(zip(geometry['blocks'],audit['blocks'],strict=True)):
        need(g['id']==b['id'] and g['audit_pointer']==f'/blocks/{i}' and g['local']==audit['local_owner_block_crosswalk'][b['id']],'exact source association')
        before=html[:g['character_start']]
        need(g['character_start']==b['raw_start'] and g['character_end']==b['raw_end'] and html[g['character_start']:g['character_end']]==b['raw_html'] and H(b['raw_html'].encode())==g['raw_utf8_sha256'],'raw source span')
        need(before.count('\n')+1==g['html_line']==b['html_line'] and len(before.rsplit('\n',1)[-1])==g['html_column']==b['html_column'],'Unicode line/column geometry')
    joins=geometry['current_case_source_block_joins']
    need(len(joins)==418 and len({x['case_pointer'] for x in joins})==418,'all418 distinctcase block associations')
    for x in joins:
        b=pointer(audit,x['audit_pointer'])
        need(pointer(cases,x['case_pointer'])==x['local']==audit['local_owner_block_crosswalk'][b['id']] and x['block']==b['id'] and x['text_sha256']==H(b['text'].encode()),'case-source exact local/global join')


def adoption_sources(adoption,cases,audit):
    for group in adoption:
        c=pointer(cases,group['case_pointer'])
        need(len(group['source_blocks'])==len(group['source_pointers'])==len(c['source_blocks']),'complete adopted source context')
        for global_id,path,local_id in zip(group['source_blocks'],group['source_pointers'],c['source_blocks'],strict=True):
            need(path.endswith('/text'),'adoption text pointer')
            block=pointer(audit,path[:-5])
            need(block['id']==global_id and audit['local_owner_block_crosswalk'][global_id]==local_id and pointer(audit,path)==block['text'],'adoption/case exact global-local source association')


def main():
    need(sys.argv[1:]==['--check'],'only inspected read-only --check mode; no writers/providers')
    need(H((P/'census-proposal.json').read_bytes())=='b29fadf8ccd7c7fa403aacf58a8d74312c971636e5ada50a2b1ddf6a11768430','immutable proposed scope')
    need(H((P/'scope-approval-root.json').read_bytes())=='bbecac079bb0aa6ca570a178f7f8a6d9c92e873fa348b289121352c513d888b9','immutable Root scope choice')
    pins=J(P/'source-pins.json')['files']
    need(len(pins)==39,'selected39pins')
    for p in pins:identity(p)
    req,cases=J(D/'requirements.json'),J(D/'cases-r3.json')
    need(len(req)==106 and cases[:186]==J(D/'cases.json'),'old106/186 unchanged')
    spec=(D/'spec-r4.md').read_bytes()
    spans,ledger=J(P/'owner-spans.json'),J(P/'route-ledger.json')
    owner_spans(spans,req,spec);ledger_check(ledger,req,cases)
    nav=J(P/'case-navigation.json')['cases'];overlay=J(D/'actual-overlay-r4.json')['cases'];adoption=J(D/'adoption-r4.json')['groups']
    case_navigation(nav,cases,overlay,adoption)
    rows=[json.loads(b) for b in (P/'native-data.jsonl').read_bytes().splitlines()]
    for row in rows:raw_row(row)
    seeds,approval,proposal=J(P/'named-seeds.json'),J(P/'scope-approval-root.json'),J(P/'census-proposal.json')
    native_scope(rows,seeds,approval,proposal)
    associations=J(P/'processor-associations.json')
    for field,kind,n in [('table_rows','table-data',32),('store_rows','store-data',67),('alias_rows','alias-data',133),('outgoing_call_rows','call-data',160),('indirect_rows','indirect-data',27)]:
        ids=[i for a in associations.values() for i in a[field]]
        need(len(ids)==len(set(ids))==n and all(rows[i-1]['kind']==kind for i in ids),'whole family association '+field)
    need(sum(len(a['selected_named_seed_rows']) for a in associations.values())==122 and sum(len(a['excluded_seed_rows']) for a in associations.values())==11,'seed family partition')
    need(all(not b['callable_X_leaves_established'] and b['status']=='NOT SELECTED / not execution-ready' for b in J(P/'batch-inputs.json').values()),'no invented callable leaf')
    prereq=J(P/'prerequisites.json');productive(prereq)
    geometry=J(P/'source-geometry.json');audit=J(F/'modulation-pitch-loop-source-audit/audit.json');html=Path(geometry['source']['path']).read_text()
    source_geometry(geometry,audit,cases,html)
    adoption_sources(adoption,cases,audit)
    historical_prefix(J(P/'research-prefix.json'))
    packages=J(D/'package-values.json');file_associations=J(D/'association-reconciliation.json')
    file_auxiliary(ledger['auxiliary'],packages,file_associations)
    negatives=[]
    def reject(label,operation):
        try:operation()
        except (ValueError,KeyError,IndexError,TypeError):negatives.append(label)
        else:raise ValueError('falsepromotion accepted: '+label)
    bad=copy.deepcopy(ledger);bad['required_outcomes'].pop()
    reject('missing complete clause',lambda:ledger_check(bad,req,cases))
    bad=copy.deepcopy(ledger);bad['required_outcomes'][1]['id']=bad['required_outcomes'][0]['id']
    reject('duplicate unit padding',lambda:ledger_check(bad,req,cases))
    for field,value,label in [('route','S-route','D12 promoted publicS'),('route','X-route','metadata name promoted callableX'),('actual_status','pass','actualU promoted pass'),('public_binding','established','unproved publicreceiver'),('enumeration','','unknown permutations omitted')]:
        bad=copy.deepcopy(ledger);bad['required_outcomes'][0][field]=value
        reject(label,lambda bad=bad:ledger_check(bad,req,cases))
    bad=copy.deepcopy(ledger);bad['required_outcomes'][0]['predicate']='Panning usesLFO'
    reject('subconditions stripped from wholeclause',lambda:ledger_check(bad,req,cases))
    bad=copy.deepcopy(ledger);bad['auxiliary'][0]['required_outcome']=True
    reject('fileS required denominator padding',lambda:ledger_check(bad,req,cases))
    for field in ['historical_inventory_surface','corrected_inventory_surface']:
        bad=copy.deepcopy(ledger['auxiliary']);bad[7][field],bad[8][field]=bad[8][field],bad[7][field]
        reject('swapped spectral '+field,lambda bad=bad:file_auxiliary(bad,packages,file_associations))
    bad=copy.deepcopy(spans);bad[0]['source_spans'][0]['byte_start']+=1
    reject('changed owner span',lambda:owner_spans(bad,req,spec))
    bad=copy.deepcopy(cases);bad[0]['setup_and_action']='inspect instead of actualaction'
    reject('changed fullcase action',lambda:case_navigation(nav,bad,overlay,adoption))
    bad=copy.deepcopy(overlay);bad[0]['actual_expected']=0
    reject('invented actual oracle',lambda:case_navigation(nav,cases,bad,adoption))
    for which in ['overlay','adoption']:
        for mutation in ['invalid-cases-prefix','wrong-valid-index','missing','duplicate','out-of-range']:
            o,a=copy.deepcopy(overlay),copy.deepcopy(adoption);target=o if which=='overlay' else a
            if mutation=='invalid-cases-prefix':target[0]['case_pointer']='/cases/0'
            elif mutation=='wrong-valid-index':target[0]['case_pointer']='/1'
            elif mutation=='missing':target.pop()
            elif mutation=='duplicate':target[1]=copy.deepcopy(target[0])
            else:target[0]['case_pointer']='/208'
            reject(which+' '+mutation,lambda o=o,a=a:case_navigation(nav,cases,o,a))
    o,a=copy.deepcopy(overlay),copy.deepcopy(adoption)
    for x in o+a:x['case_pointer']='/cases'+x['case_pointer']
    reject('joint historical invalid pointer agreement',lambda:case_navigation(nav,cases,o,a))
    bad=copy.deepcopy(next(r for r in rows if r['kind']=='table-data'));bad['record']['slots'][0]['target']='0x0'
    reject('arbitrary selected slot substitution',lambda:raw_row(bad))
    bad=copy.deepcopy(rows[0]);bad['source_byte']+=1
    reject('changed raw row offset',lambda:raw_row(bad))
    bad=copy.deepcopy(rows);next(r for r in bad if r['kind']=='call-data')['record']['caller']='0x0'
    reject('incoming or encountered callee seed expansion',lambda:native_scope(bad,seeds,approval,proposal))
    bad=copy.deepcopy(seeds);next(s for s in bad['entries'] if not s['selected_outgoing_seed'])['selected_outgoing_seed']=True
    reject('UI method-group outgoing selection broadened',lambda:native_scope(rows,bad,approval,proposal))
    bad=copy.deepcopy(geometry);bad['blocks'][0]['character_start']+=1
    reject('source geometry changed',lambda:source_geometry(bad,audit,cases,html))
    bad=copy.deepcopy(geometry);bad['current_case_source_block_joins'][0]['local']='wrong'
    reject('spectral/source association cannot be swapped',lambda:source_geometry(bad,audit,cases,html))
    bad=copy.deepcopy(adoption);bad[0]['source_pointers'][0]='/blocks/0/text'
    reject('wrong adopted primary paragraph association',lambda:adoption_sources(bad,cases,audit))
    bad=copy.deepcopy(prereq);bad['common']['signal']='Selected controls alone'
    reject('vacuous signal flag baseline',lambda:productive(bad))
    for code,replacement,label in [('AS','MIDI On inherited always','incompatible shared MIDI defaults'),('PF','EnvelopeAmount0 without baseline','missing envelope positive'),('SH','free delay means milliseconds','Hertz reciprocal repair'),('SR','Poly GateOff allowed','MonoGate generalized Poly'),('ST','Freeze flag proves capture; freezerfirst','flag capture and unconditional order'),('VO','one carrier channel enough','one Vocoder channel'),('BR','automatic RepeatOn','automatic Chance trial RepeatOn'),('LP','empty Clear and named taps enough','empty buffer/named InsertLooper positive')]:
        bad=copy.deepcopy(prereq);bad['devices'][code]=replacement
        reject(label,lambda bad=bad:productive(bad))
    bad=copy.deepcopy(J(P/'research-prefix.json'));bad['sha256']='0'*64
    reject('rewritten historical research prefix',lambda:historical_prefix(bad))
    bad=copy.deepcopy(pins[0]);bad['sha256']='0'*64
    reject('source pin changed',lambda:identity(bad))
    print(json.dumps(dict(status='PASS-data-only-author-integrity',whole_clauses=106,atomic_outcome_denominator=False,required_routes={'X':0,'S':0,'none':106},same_unit_annotations={'D12':96,'U':10},auxiliary_file_S=10,cases=208,old_exact=186,actual_null_U=208,current_pointer_dereferences=230,selected_DATA_rows=704,tables=32,selected_slots=102,stores=67,aliases_memberships=266,named_seeds=122,outgoing_direct=160,indirect_unresolved=27,pins=39,source_geometry=332,case_source_joins=418,negative_controls=negatives,new_C_bodies=0,new_native_windows=0,new_original_calls=0,new_site_grade_norm_case_release_credit=0,coverage_gate='OPEN',writes=False),indent=2))


if __name__=='__main__':
    main()
