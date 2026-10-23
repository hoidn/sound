"""Historical initial authoring method using fixed retained DATA only.

Do not replay: the initial dense research append was edited into readable prose
within this unfrozen author task. Current research-change.json and read-receipt.json
describe the final artifacts. check.py --check is the read-only verification path.
No old imports or entrypoints are used here.
"""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import re

P=Path(__file__).resolve().parent
R=P.parents[3]
F=P.parent
D=F/'distortion'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def obj(path):return json.loads(path.read_bytes())
def canon(value):return sha(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())
def save(name,value):
    (P/name).write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def pin(path):
    raw=(R/path).read_bytes()
    return dict(path=path,bytes=len(raw),sha256=sha(raw))

def main():
    q=obj(D/'requirements.json');cases=obj(D/'cases-r3.json');old=obj(D/'cases.json')
    owner=(D/'spec-r3.md').read_text();current=R/'wiki/specs/distortion-devices.md'
    assert owner==current.read_text() and len(q)==67 and len(cases)==200 and cases[:190]==old
    overlay=obj(D/'actual-overlay-r3.json')['cases']
    assert [x['id'] for x in overlay]==[x['id'] for x in cases]
    assert all(x['actual_expected'] is x['actual_comparison'] is None and x['target']=='U' and not x['executed'] for x in overlay)
    census=obj(P/'query-census.json');assert census['within_caps']
    metadata=[json.loads(x) for x in (P/'metadata-rows.jsonl').read_text().splitlines()]
    assert len(metadata)==325
    def reqs(c):return list(dict.fromkeys([c['requirement'],*c.get('requirements',[])]))
    clauses=[];bundles=[];contexts=[]
    for i,r in enumerate(q):
        body=r['contract'];assert owner.count(body)==1
        start=owner.index(body);source=dict(path='wiki/specs/distortion-devices.md',immutable_provider='distortion/spec-r3.md',requirement_pointer=f'/{i}/contract',char_start=start,char_end=start+len(body),line=owner[:start].count('\n')+1,contract_sha256=sha(body.encode()))
        related=[c['id'] for c in cases if r['id'] in reqs(c)]
        clause=dict(id=r['id'],device=r['device'],provenance=r['provenance'],source=source,case_navigation=related,evidence=r['evidence'])
        clauses.append(clause)
        ident=f'DST-B{i+1:03}'
        bundles.append(dict(id=ident,requirement=r['id'],device=r['device'],unit='whole unchanged contract including every control/mode/unknown subcondition; not atomic denominator',source=source,case_navigation=related,provenance=r['provenance'],route='S-retained-file-only' if r['provenance']=='Dpkg' else 'no-established-route',whole_contract_qualifiers_mandatory=True))
        if r['provenance']=='D12':contexts.append(dict(id=ident+'-DOC',bundle=ident,requirement=r['id'],context='documentary',route='no-established-exact-target-route',basis='D12-source-annotation-not-extra-outcome',source_evidence=r['evidence'],actual=None,comparison=None,new_grade=None,native_PC=None))
        fileonly=r['provenance']=='Dpkg'
        contexts.append(dict(id=ident+'-FILE' if fileonly else ident+'-APP',bundle=ident,requirement=r['id'],context='retained-file' if fileonly else 'target-application',route='S-retained-file-only' if fileonly else 'no-established-route',basis='retained vocabulary/example only' if fileonly else 'exact target/control/receiver/effective output not established',missing_joins=[] if fileonly else ['actual admitted device/control and current value','same model/provider/entry/callback/processor receiver and native ABI','productive band/channel/stage/modulator/tail paths and host clock/output consumer','exact-target calibrated signal/UI/state/error/lifecycle oracle'],actual=None,comparison=None,new_grade=None,native_PC=None))
    save('clause-index.json',dict(requirements=clauses,count=67,owner_sha256=sha(owner.encode()),unit='67whole-clause navigation bundles; fullbody is normative source, no body copied'))
    nav=[]
    for i,c in enumerate(cases):
        nav.append(dict(id=c['id'],device=c['device'],source='distortion/cases-r3.json',pointer=f'/{i}',object_sha256=canon(c),input_sha256=canon(c['input']),requirements=reqs(c),provenance=c['provenance'],role='historical-file-only' if c['provenance']=='Dpkg' else 'application-U',history='old190-exact' if i<190 else 'newR3-null-history',actual_expected=None,actual_comparison=None,target='U',executed=False,actual_overlay_pointer=f'/cases/{i}',mapping='owning/explicit related requirement navigation,not eachcase proves every subcondition'))
    save('case-navigation.json',dict(records=nav,old_exact=190,new_null=10,current=200,artifact_roles=18,application_roles=182,all_actual_U=True))
    save('route-ledger.json',dict(owner_revision=3,bundle_count=67,unit='whole-clause bundles only;not atomic or wholefamily/product denominator',bundles=bundles,contexts=contexts,counts=dict(whole_clause_bundles=67,file_only_S=9,application_none=58,D12_annotations=47,total_context_records=114,X=0),counts_are_inventory_not_grades=True,new_native_sites=0,new_original_calls=0,new_grades=0,selected_successor=None,residuals=['Every exact transfer/filter/crossover/envelope/PRNG/feedback/mix/gain/aliasing/CPU/latency metric remains U.','Continuous controls/time/codec/error/legacy/automation/load/save/Undo/cancel/teardown inputs not exhausted by200finite cases.','Secondary/legacy/UI/other class and callback frontiers unselected,not absent.','Optional recipes/input instances/helper slots do not add required outcomes.']))
    audit=obj(F/'distortion-source-audit/audit.json');html=(F/'audio-utilities/manual-audio-effects-2026-10-19.html').read_text();assert len(audit['blocks'])==216
    blocks=[]
    for i,b in enumerate(audit['blocks']):
        assert html[b['raw_start']:b['raw_end']]==b['raw_html']
        blocks.append(dict(id=b['id'],pointer=f'/blocks/{i}',raw_start=b['raw_start'],raw_end=b['raw_end'],html_line=b['html_line'],html_column=b['html_column'],text_sha256=sha(b['text'].encode()),raw_sha256=sha(b['raw_html'].encode())))
    schema=obj(D/'schema-fields.json');packages=obj(D/'package-values.json');package=[]
    for i,s in enumerate(schema):
        j=next(j for j,x in enumerate(packages) if x['class']==s['class']);x=packages[j]
        assert x['locator']=='/Ableton/'+s['class'] and x['root_attributes']['Creator']=='Ableton Live 12.4d1' and x['root_attributes']['MinorVersion']=='12.0_12402'
        package.append(dict(class_name=s['class'],schema_pointer=f'/{i}',schema_line=s['line'],fields=len(s['fields']),package_pointer=f'/{j}',package_root=x['locator'],Creator=x['root_attributes']['Creator'],MinorVersion=x['root_attributes']['MinorVersion'],runtime_admission_default_or_DSP=False))
    save('source-scope.json',dict(source_version='OfficialVersion12/date2026-10-19/UTCunknown/exact12.4.3U',manual_path='analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html',source_bytes=588328,source_sha256=sha(html.encode()),inherited_semantic_review='216full blocks plus focused four-field sourceR2 correction;215other assessments/nineothergroups unchanged. Not fresh fullsemantic re-audit.',blocks=blocks,package_facts=package,source_R2_correction_path='distortion-source-audit/response-r2.json',corrected_Roar007_030_are_Frequency_gestures=False,R3_Roar037_explicit_Frequency_gesture_proposal=True,pixels_destinations_inspected=False,new_source_bodies=0,new_runtime_results=0))
    guards=dict(EACH_NONEMPTY_NONZERO_control_sensitive_positive=True,BOTH_relevant_channels_stages_modulators_targets_productive=True,UI_only_requires_audio=False,S0_proves_generator_or_tail_absence=False,settings_or_flags_prove_active_path=False,preset_is_constructor_default=False,file_schema_proves_live_admission=False,modern_legacy_algorithms_merged=False,Erosion_enabled_Width_before_modifier=True,Erosion_S1_first_second_only=True,Roar_filter_AND_shaper_positive=True,Roar007_030_imply_actual_gainstage_Frequency_edit=False,Roar037_explicit_gainstage_Frequency_action=True,Roar_analysis_feedback_Frequency_satisfy_gainstage=False,Roar_BOTH_manual_Feedback_controls_positive_before_MIDI=True,Roar_MIDI_both_Feedback_controls_inactive_D12_preserved=True,Listen_replacement_not_normal_mix=True,gate_tail_requires_sustaining_feedback=True,Waveshaper_Drive_distinct_from_main_Drive=True,Saturator_wet_clip_bound_applies_arbitrary_dry_mix=False,zero_envelope_only_follower_gate=True,optional_recipes_guaranteed_sound=False,graph_visualization_proves_audio_DSP=False,new_body_or_original_selection=False)
    save('semantic-guards.json',guards)
    edges=[('I07/I08 constructed InL/R/TrackOut','actual distortion processor/host audio','unknown','integration mix-structure I07/I08;approvedMix','current track/device instance,input/output buffer,clock/dispatch and hostconsumer'),('Stored class/fields/preset','active model/current control','unknown','retained schema/package','Live admission/default/domain/enum/provider'),('RTTI/addresspoint/store','putative class instance','observed-static-metadata','metadata-rows29tables35stores','constructor/nativeABI/normalcompletion/receiver/lifetime'),('Method/visualization aliases','same public control/processing receiver','inferred-lexical','41boundary/updatealiases','actual registration/currentcontrol/datum meaning/graph-to-audio join'),('41fixedseeds','62direct+22indirect index rows','observed-static-index','metadata-rows','actual invocation/arguments/results/provider;22indirecttargets stayunknown'),('Curve-helper data callbacks','numerical curve or audible processing','unknown','curve-frontiers','body/state/buffer/ABI/calibration and graph-to-audio proof'),('Automation/macro/sidechain/MIDI input','live distortion state','unknown','approvedAutomation and current clauses','provider/timebase/priority/receivedinput/currentreceiver'),('Operation/load/save/Undo/cancel/teardown','restored state/media/host output','unknown','current U clauses','transaction/ownership/error/continuity/default/legacy/currentvalues'),('D12 currentmanual','exact target result','unknown','source-scope','version and observable UI/signal/lifecycle oracle')]
    save('chain-edges.json',dict(integration=['I07','I08'],adjacent=['approved family-mix','approved family-automation'],selection='amendedrev4 item4 expectedwaveshaping/math leafyield;not proved selfcontained capability',edges=[dict(id=f'DS-E{i+1:02}',from_=a,to=b,classification=c,evidence=d,missing=e) for i,(a,b,c,d,e) in enumerate(edges)],new_native_sites=0,new_public_routes=0,new_traversal_credit=0,selected_successor=None))
    helper_req={'TRoarFilterCurveHelper':['REQ-DST-ROAR-004','REQ-DST-ROAR-006'],'TRoarLfoCurveHelper':['REQ-DST-ROAR-007'],'TRoarEnvelopeCurveHelper':['REQ-DST-ROAR-008'],'TRoarNoiseCurveHelper':['REQ-DST-ROAR-009'],'TRoarScopeCurveHelper':['REQ-DST-ROAR-004'],'TRoarShaperCurveHelper':['REQ-DST-ROAR-004','REQ-DST-ROAR-005'],'TSaturatorShaperCurveHelper':['REQ-DST-SATURATOR-002','REQ-DST-SATURATOR-004','REQ-DST-SATURATOR-006']}
    frontiers=[]
    for name,ids in helper_req.items():
        table=next(x for x in metadata if x['kind']=='table-prefix' and x['record']['literal_type_encoding']==str(len(name))+name)
        aliases=[x for x in metadata if x['kind']=='alias' and name+'::' in x['record']['name']]
        frontiers.append(dict(name=name,table_metadata_id=table['id'],selected_slots=table['record']['slots'],qualified_update_aliases=[dict(id=x['id'],entry=x['record']['entry'],name=x['record']['name']) for x in aliases],owner_clause_proofs=[next(x for x in clauses if x['id']==ident)['source'] for ident in ids],requirements=ids,relationship='Bounded lexical visualization/control-data candidate only;sourceclause supplies public control/curve role,notsame runtime/math algorithm.',body_math_or_DSP_proof=False,callable_input_state_ABI=False,graph_to_audio_join='unknown',no_named_update_alias_limit='Envelope/Noise prefixes have no selected update alias: no absence inference;Scope clause association is auxiliary navigation,not a newly required scope display.',selected_for_body_or_execution=False))
    save('curve-frontiers.json',dict(candidates=frontiers,small_prefix_targets='Whole20small processor/wrapper/helper prefixes only;not functions/algorithms/route denominator.',proof_gate='Need independently selected body semantics showing actual numeric function,valid owned input/state/ABI/providers/normal completion and calibrated observable join. Visualization names or graph samples are insufficient.',candidate_original_batch=None,selected_successor=None))
    save('input-sets.json',dict(retained=['distortion/fixture-signals.json#S0-S3/P-AUDIO','distortion/cases-r3.json#200','distortion/actual-overlay-r3.json#cases'],finite_inputs_not_outputs=True,actual_results=0,legal_call_state_or_oracle_established=False,candidate_original_batch=None,selected_successor=None,qualified_inputs=['Erosion uses only first1sS1;active Blend100/enabledWidth before modifier','EACH/BOTH productive controls/paths including sustainingfeedback/generator before loss','UI-only noaudio;separate dry/wet/return/Listen/Crackle/sidechain','all automation/load/save/Undo/malformed/cancel/transport/rate/teardown histories remainU']))
    paths=['component-resolution-v1/manifest.json','component-resolution-v1/packet-inputs.json','integration-structure-v1/manifest.json','integration-structure-v1/mix-structure.md','family-mix-routes-v1/manifest.json','family-mix-routes-v1/route-basis.json','family-automation-routes-v1/manifest.json','distortion/manifest-author-r3.json','distortion/spec-r3.md','distortion/requirements.json','distortion/cases-r3.json','distortion/cases.json','distortion/actual-overlay-r3.json','distortion/adoption-r3.json','distortion/fixture-signals.json','distortion/schema-fields.json','distortion/package-values.json','distortion/sources.json','distortion-source-audit/manifest.json','distortion-source-audit/manifest-r2.json','distortion-source-audit/audit.json','distortion-source-audit/response-r2.json','reviews/distortion-owner-r3-review.json','reviews/distortion-source-audit-review.json','reviews/distortion-source-audit-r2-review.json','audio-utilities/manual-audio-effects-2026-10-19.html']
    paths += ['distortion/manual-'+d+'-blocks.json' for d in sorted({x['device'] for x in q})]
    authority=[];component=obj(F/'component-resolution-v1/manifest.json');index=obj(F/'component-resolution-v1/packet-inputs.json')
    for name in ['class-tables.jsonl','class-stores.jsonl','symbol-memberships.jsonl']:
        x=next(x for x in component['files'] if x['path']==name);authority.append(dict(path=str(F/'component-resolution-v1'/name),bytes=x['bytes'],sha256=x['sha256'],scope='approvedfullidentityinherited;selectedrowhashesfresh'))
    for name in ['aliases.jsonl','calls.jsonl','indirect.jsonl']:
        x=next(x for x in index['retained_indexes_verified'] if x['path'].endswith('/'+name));authority.append(dict(path=x['path'],bytes=x['bytes'],sha256=x['sha256'],scope='approvedfullidentityinherited;selectedrowhashesfresh'))
    research=R/'wiki/research/distortion-devices.md';original=research.read_bytes();assert b'## Distortion family route map' not in original
    prefix=original.replace(b'updated: 2026-10-19',b'updated: 2026-10-20',1)
    append='\n## Distortion family route map — 2026-10-20\n\nPending independent structure review. The [new bounded map](../../analysis/ableton-live-12.4.3/full-spec-v1/family-distortion-routes-v1/structure.md) extends reviewed I07/I08 and approved Mix/Automation context under amended revision4 item4. It retains67whole-clause bundles (not atomic outcomes): nine retained-file-only S and58application bundles with no established route,0X.47D12 annotations mirror the same clauses;114context rows are not extra outcomes. All200actual results remain U,190old case objects exact andtennew histories null.\n\nRoot approved29primary table associations after324table/9695slot broad navigation exceededcap; a702alias+607membership census also exceededcap before raw retention. The selected semantic frontier has105of789slots,35store candidates,136aliases+41memberships,62call+22unresolvedindirect rows. Secondary/legacy/UI/other callbacks remain unselected/unknown. Seven curve-helper candidates retain visualization-data associations only, not audio transfer or self-contained math proof. No new body/native/provider/decoder/original/harness/model/comparator/fixture/build,site resolution,grade,requirement,case,release or successor. The corrected216block semantic audit is inherited; current67contracts/200input-actions and productive Erosion/Roar/Saturator/Crackle/return/load/lifecycle guards were read. Root owns seal,independent review,atlas/index/coverage/log adoption.\n'
    change=dict(path='wiki/research/distortion-devices.md',original_prefix_bytes=len(original),original_prefix_sha256=sha(original),prefix_bytes_after_date_update=len(prefix),prefix_sha256_after_date_update=sha(prefix),date_only_change=dict(from_='updated: 2026-10-19',to='updated: 2026-10-20'),append_start_byte=len(prefix),append_bytes=len(append.encode()),append_sha256=sha(append.encode()))
    save('research-change.json',change)
    save('pins.json',dict(providers=[pin(str((F/x).relative_to(R))) for x in paths],metadata_authority=authority,asof_context=[pin('wiki/specs/distortion-devices.md'),pin('wiki/research/full-live-specification-plan.md')],mutable_asof_not_future_live_gate=True,research_change=change,no_old_import_or_whole_predecessor_replay=True))
    save('read-receipt.json',dict(fresh='All67contract bodies,all200input/actions read through142exact-identical-input groups with everycaseID;all ten newpositive/limit fields;canonicalprerequisites andfixed29scope metadata. Oldunchangedcase expected/comparator and216source semantics inherited.',inherited='Corrected216block sourceR2/48literalresources/tenpartialgroups/sixquestions;R3ownerreview. No fullsource re-audit orpixels/destinations.',schema_probe_failure='First census aborted before output on a non-entry membership row;predicate changed to get(entry),manual rerun succeeded. No source rows retained by failed attempt.',cap_decisions='324table broad query then29table Root scope;1309alias/member broad census thenRootapproved41boundary/update semantic restriction,all caps passing before325rawrows retained.',all_actual_results='200nullU/unexecuted',writes='Only newfamilydir plus date-only/additive canonicalresearch;Rootsharedpages/manifest untouched'))
    research.write_bytes(prefix+append.encode())
    print(json.dumps(dict(status='author-data-built-pending-structure/check/Rootseal',clauses=len(clauses),contexts=len(contexts),metadata=len(metadata),pins=len(paths),research_prefix=len(original))))

if __name__=='__main__':main()
