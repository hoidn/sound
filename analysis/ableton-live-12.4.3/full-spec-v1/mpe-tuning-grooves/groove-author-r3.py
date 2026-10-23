"""Bounded Groove successor data; never imports source/vendor code or writes after seal."""
from pathlib import Path
import copy,json,re,sys
P=Path(__file__).resolve().parent;A=P.parent/'groove-source-audit'
load=lambda p:json.loads(p.read_text())
def original_requirements():
 rows=[]
 for line in (P/'groove-spec-before-r3.md').read_text().splitlines():
  if line.startswith('| REQ-GROOVE-'):
   cells=[x.strip() for x in line.strip('|').split('|')];assert len(cells)==4
   rows.append(dict(zip(['id','preconditions','contract','evidence'],cells)))
 assert len(rows)==14;return rows
def build():
 oldr=original_requirements();r=copy.deepcopy(oldr);oldc=[c for c in load(P/'cases.json') if c['id'].startswith('GRV-')];assert len(oldc)==24
 r[0]['preconditions']+=' Or select a pooled entry with the Clip Groove chooser.'
 r[0]['contract']+=' The Clip Groove chooser selects the groove for a clip from entries available in the Groove Pool.'
 r[0]['evidence']+='; CV:B062'
 r[9]['contract']+=' For a groove using positive velocity values, committing to an audio clip creates a volume clip envelope to represent that velocity information as audio volume changes, overwriting a volume clip envelope already in the clip. This named envelope relation supplies no velocity-to-gain, point/curve, marker, sample or timing law.'
 r[9]['evidence']+='; CV:B064'
 r[13]['contract']=r[13]['contract'].replace('replacement sharing','other-clip sharing/duplicate-entry behavior')+' After enabling Clip Hot-Swap, double-clicking the selected alternative groove or pressing Enter loads it onto the clip and replaces the previously loaded groove in the Groove Pool as well. The source does not specify how other clips or duplicate/shared entry identities change.'
 r[13]['evidence']+='; CV:B063'
 rows=[
 (25,3,'GSA-G01',['GRV:B006'],[],
 'Use independently admitted hidden pool and eligible main-window focus/layout. Actually invoke the browser view-control drop-down entry; reset separately for literal Ctrl+Alt+6(Win) or Cmd+Option+6(Mac). Begin from independently known visible state to test closing. Establish an ordinary productive visibility toggle first; absent input/control/working baseline remains U. Do not infer an open-only command or a default.',
 'The browser view-control entry and qualified shortcut toggle Groove Pool visibility.',False),
 (26,14,'GSA-G02',['GRV:B009'],[],
 'On disposable owned loaded groove with independently functioning offered Save and Hot-Swap controls and admitted destinations, actually click pool Save and pool Hot-Swap in separate reset histories. First establish genuinely successful ordinary operations with the same known assignments before an independently offered cancel/failure trial. Retain exact offered controls and assignment/destination identities; failed or absent operation stays U, not unchanged-state success.',
 'The buttons next to the pool groove name offer Save and Hot-Swap entrypoints; inspecting the button alone is not invoking it. File bytes/path/overwrite/cancel/rollback outcome remains U.',False),
 (27,4,'GSA-G03',['GRV:B011'],[],
 'Use independently valid known groove landmarks and nonempty clip notes away from ties/edges with actual supported event readout and independently productive groove effect. On separate reset copies explicitly set Base1/4 then Base1/8 with other controls retained. Preserve GRV004 exact aligned1/8 no-displacement case and retain event/grid observations without inventing correspondence or proportional arithmetic. Missing baseline/readout stays U.',
 'Base1/4 and Base1/8 provide distinct reference-grid contexts. All new event/numeric pairing or displacement comparisons remain null; the old aligned subset stays exact.',True),
 (28,6,'GSA-G04',['GRV:B009','GRV:B013','GRV:B015'],[],
 'Use valid owned nonempty notes/groove and independently confirm genuinely nonzero Timing influence with Quantize/Random/Velocity0 before changing only Timing to0 on matched original copies. Separately independently confirm genuine positive groove velocity emphasis on an active eligible source before actual+100/0/-100 Velocity trials. Retain actual transport, audible nonzero output, enabled source/instrument/routes and unchanged unrelated controls. An off-grid filename, nonzero flag, silent route or failed positive is U, never a no-effect pass.',
 'Timing and Velocity expose these source control contexts. No interpolation, velocity blending/audio-gain mapping, measured event/audio tolerance or immediate update law is supplied.',True),
 (29,2,'GSA-G05',['GRV:B004'],[],
 'Use independently valid nonempty Warp-enabled audio with genuinely confirmed groove timing effect and functioning unmuted nonzero routed output. Retain matched groove/controls/source and actual playback. Only then use reset Warp-off versus on copies, followed by a separate on-off-on history. Missing groove support, source/effect/output or failed positive stays U, never a passing no-effect observation. Preserve old GRV002 availability and GRV016 unknown interaction trials.',
 'Audio grooves require Warp. UI/refusal/auto-enable/restoration and exact signal/marker/timing outcomes remain U; a Warp flag alone is not a productive-effect baseline.',True),
 (30,9,'GSA-G06',['GRV:B016'],[],
 'Use valid assigned groove and independently functioning actual Global Amount control with known affected clips. Separately manipulate the pool Global Amount and the actually visible Control Bar Global Amount on reset copies; retain actual visible value/control/held-input state. Establish productive ordinary operation first and preserve GRV009100/130 endpoint context without changing its fields. Missing capability stays U.',
 'Assigned grooves expose Global Amount in the pool and Control Bar. Only named actual entrypoint roles are compared; no lower endpoint, composite/scaling equation or update deadline is added.',False),
 (31,11,'GSA-G07',['GRV:B021','GRV:B023','GRV:B024'],[],
 'Reset independently for a known valid groove dragged from browser versus Groove Pool into an admitted empty MIDI track. Establish the resulting clip is genuinely editable, make a supported nonidentity note edit and verify that edit before actual Extract Groove. Separately actually drag the edited clip into the pool. Retain playing portion and original material inside/outside it; preserve GRV012 existing two extraction routes. Failed operation or missing edit/source stays U, not an unchanged-content roundtrip pass.',
 'Both groove-to-MIDI routes create editable material, and an actually edited clip can be re-extracted. Exact detector, playing-boundary inclusion, bytes, normalization, naming and conversion defaults remain U.',False),
 (32,10,'GSA-G08',['GRV:B018','GRV:B019'],[2],
 'Use independently readable owned Warp-enabled audio and a valid assigned groove using positive velocity values with independently confirmed positive velocity influence, functioning routed unmuted nonzero output, and independently visible identifiable nonflat pre-existing clip-volume envelope. Establish a productive normal Commit/control baseline. Commit a disposable reset copy; retain original and resulting envelope/assignment/source identities. In a separate admitted no-existing-envelope history inspect creation only after the same positive prerequisite. Failed baseline/absent positive influence stays U. The old GRV010 Quantize100/Velocity0 MIDI and audio-assignment-only trials remain exact and are not this positive-velocity overwrite trial.',
 'With the stated positive-velocity source context, audio Commit creates a volume clip envelope and overwrites one already present. Compare only named envelope presence/overwrite relation and assignment; no point/value/curve/audio-gain/marker/PCM/RNG/file/timing oracle.',False),
 (33,1,'GSA-G10',['GRV:B003','GRV:B007'],[0],
 'With two independently valid distinct grooves already admitted in Groove Pool and an eligible editable owned clip, establish successful ordinary assignment. Actually select each pool entry through the Clip Groove chooser on reset histories and retain clip/entry/selection identities. Do not substitute browser double-click load for this chooser gesture; absent control/pool/working assignment stays U.',
 'Clip Groove chooser selects the clip groove from the pool. No duplicate import/default/entry identity or all-clips sharing law follows.',False),
 (34,14,'GSA-G10',['GRV:B003','GRV:B009'],[1],
 'Use a genuinely playing nonempty clip with valid assigned groove, functioning unmuted nonzero output and independently working normal Hot-Swap baseline. Keep two independently valid distinct alternatives and separately known sharing context. Enable Clip Hot-Swap, actually double-click the selected alternative; reset original clip/pool histories, then actually press Enter on the selected alternative. Retain old/new clip and Groove Pool entry identities before/after each gesture, and observations of any other sharing clip without grading its policy. Missing input/control/positive swap or failed playback stays U, not successful continuity or replacement.',
 'Both double-click and Enter load the selected alternative onto the clip and replace the previously loaded groove in the pool as well. Other-clip sharing/deletion/merge/reload/duplicate identity and disruption-free timing remain U.',False),
 ]
 new=[]
 for number,req,group,blocks,externals,action,claim,sensitive in rows:
  new.append(dict(id=f'GRV-{number:03}',requirement=f'REQ-GROOVE-{req:03}',kinds=['bounded-source-context'],setup='F-GRV-R3; owned reset data and admitted exact source/control/history prerequisites, not supplied reference fixtures.',action=action,expected=None,comparator=None,documentary_grade='D12',target_build_grade='U',execution='unexecuted',source_claim=claim,documentary_expected=None if sensitive else claim,documentary_comparator=None if sensitive else 'Named admitted input/control/selection/envelope-entry relationship only; no numeric/signal/file/timing/hidden-state comparator.',actual_expected=None,actual_comparison=None,audit_group=group,source_context=[dict(catalog='../groove-source-audit/audit.json',json_pointer=f'/blocks/{int(id[-3:])-1}',id=id) for id in blocks]+[dict(catalog='../groove-source-audit/audit.json',json_pointer=f'/external_contexts/{i}',id=['CV:B062','CV:B063','CV:B064'][i]) for i in externals]))
 new[3]['additional_requirements']=['REQ-GROOVE-008','REQ-GROOVE-003'];new[6]['additional_requirements']=['REQ-GROOVE-012']
 audit=load(A/'audit.json');correction=load(A/'correction-r2.json');effective=copy.deepcopy(audit)
 for patch in correction['patches']:
  field=patch['pointer'].rsplit('/',1)[1];assert effective['assessments'][27][field]==patch['before'];effective['assessments'][27][field]=patch['after']
 assert effective['assessments'][27]['requirement_refs']==effective['assessments'][27]['case_refs']==[]
 ledger=[dict(group=g['id'],title=g['title'],disposition='research-recommendation-only' if g['id']=='GSA-G09' else 'bounded-local-source-context',case_pointers=[dict(catalog='groove-cases-r3.json',json_pointer=f'/{24+i}',id=c['id']) for i,c in enumerate(new) if c['audit_group']==g['id']],limits=g['limits'],complete=False,coverage_credit=0) for g in effective['proposals']]
 fixture=dict(id='F-GRV-R3',role='Future owned unexecuted analyst recipes; no Set/AGR/audio/MIDI/controller or output supplied.',common='Independently valid owned nonempty groove/clip material and admitted exact controls, explicit Warp/transport/selection/focus/parameters/pool/assignment/route states; fresh reset original copies. Missing/failed capability or positive history is U.',positive='Genuinely productive relevant Timing/Velocity/audio/Save/Swap/control response and active unmuted nonzero output where relevant before zero/Warp/cancel/no-effect observations; flags and filenames are not real effect.',overwrite='Independently confirmed positive groove velocity influence plus identifiable nonflat prior clip-volume envelope before audio Commit overwrite; exact existing markers do not prove or require marker mutation.',random='GSA-G09 research only: no guaranteed distinct realization, independent stream/correlation/seed/distribution/threshold/texture grade; existing GRV007/023 U unchanged.',racks='Selected Racks022/RCK046 existing extraction remains as-of context, not new Groove extraction case. Effective audit clears only misleading primary Groove012/GRV012 chain references.',actual_expected=None,actual_comparison=None,target='U',executed=False)
 delta=dict(old_requirement_count=14,changed_requirement_records=[dict(index=i,id=r[i]['id'],fields={k:dict(before=oldr[i][k],after=r[i][k]) for k in r[i] if oldr[i][k]!=r[i][k]}) for i in range(14) if r[i]!=oldr[i]],new_requirement_IDs=[],unchanged_requirement_rows=11,old_Groove_records_verbatim=24,shared_original_records_verbatim=83,MPE_records_unchanged=27,tuning_records_unchanged=32,new_case_ids=[x['id'] for x in new],current_Groove_cases=34,current_Groove_documentary_D12=23,current_Groove_documentary_U=11,source_groups_bounded=9,Random_group_research_only='GSA-G09',actual_expected=None,actual_comparison=None,target='U',executed=False,complete_topics=0)
 status=dict(role='Current Groove-only catalog actual-status declaration; legacy expected/comparator are documentary proposals, not prior measurements. New fields likewise supply no executed results.',current_catalog='groove-cases-r3.json',current_cases=34,legacy_selected_records=24,shared_original_catalog='cases.json',shared_original_cases=83,MPE_original_cases=27,tuning_original_cases=32,new_source_contexts=10,new_named_documentary_relations=7,new_documentary_comparator_null=3,actual_expected=None,actual_comparison=None,target='U',executed=False,complete_topics=0)
 return {'groove-requirements-r3.json':r,'groove-cases-r3.json':oldc+new,'groove-adoption-r3.json':ledger,'groove-fixtures-r3.json':fixture,'groove-delta-r3.json':delta,'groove-actual-status-r3.json':status}
def main():
 assert sys.dont_write_bytecode and sys.argv[1:] in (['--write'],['--check'])
 writing=sys.argv[1:]==['--write']
 if writing:assert not (P/'groove-manifest-author-r3.json').exists(),'refuse write after seal'
 for name,value in build().items():
  if writing:
   assert not (P/name).exists(),'refuse overwrite current outputs';(P/name).write_text(json.dumps(value,indent=2)+'\n')
  else:assert load(P/name)==value,name
 print('GrooveR3 finite author '+('written before seal' if writing else 'readonly reconstruction matched'))
if __name__=='__main__':main()
