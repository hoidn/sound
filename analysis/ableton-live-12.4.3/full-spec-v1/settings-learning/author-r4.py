"""Create only two bounded Settings configuration bridges. No runtime or source capture."""
from pathlib import Path
from hashlib import sha256
from copy import deepcopy
import json,datetime,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[3];B=P.parent
assert sys.argv[1:]==['--write'] and not (P/'manifest-author-r4.json').exists(),'Unsealed explicit authoring only'
def load(q):return json.loads(q.read_text())
def pin(q):
 b=q.read_bytes();return dict(path=str(q.relative_to(ROOT)),bytes=len(b),sha256=sha256(b).hexdigest())
def put(n,v):
 assert not (P/n).exists(),n
 (P/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
prior=load(P/'manifest-author-r3.json');assert pin(P/'manifest-author-r3.json')['sha256']=='4570f813d2908468657d937aed206ea04dae2b801edaa1839d04c1797a60adb6'
for n,r in prior['files'].items():assert all(pin(P/n)[k]==r[k] for k in ['bytes','sha256'])
assert (ROOT/'wiki/specs/settings-learning-workflows.md').read_bytes()==(P/'spec-r3.md').read_bytes()
assert (ROOT/'wiki/research/settings-learning-workflows.md').read_bytes()==(P/'research-r3.md').read_bytes()
req=deepcopy(load(P/'requirements.json'));cases=deepcopy(load(P/'cases-r3.json'));assert len(req)==21 and len(cases)==31
bs=load(P/'source-blocks.json')
def ev(n):
 b=bs[n-1];assert b['id']==f'SET-B{n:03}';return dict(block=b['id'],anchor=b['anchor'],html_line=b['html_line'])
new=[dict(id='REQ-SETTINGS-LEARNING-020',title='Sample Editor application choice',contract='File & Folder settings provide a Sample Editor setting for choosing an external audio-editing program. This is the configuration frontend only. The already configured Edit launch, shared/destructive sample effects and lifecycle stay with Clip View023 and Project/Media012. Exact picker labels, application/path grammar, defaults, acceptance of an arbitrary application, persistence and launch/failure results remain unknown.',strength='D12',target_applicability='U',evidence=[ev(59)]),dict(id='REQ-SETTINGS-LEARNING-021',title='Plug-in folder configuration choices',contract='Plug-Ins settings allow configuring plug-in folder locations and specifying which folders Live uses. This adds the documented configuration frontend only. Existing SPEC-PLUGIN-DISCOVERY002 retains native system/custom source-switch search effects and custom-path predicates; plug-in hosting retains window preferences. Exact labelled control-to-native-switch mapping, picker/path grammar, defaults, scan transactions, immediate effects and arbitrary plug-in acceptance remain unknown.',strength='D12',target_applicability='U',evidence=[ev(66)])]
req+=new
for r,action,contexts in [(new[0],'In an independently admitted exact-build/platform Settings context, identify the offered Sample Editor application-choice control and a separately established compatible already available editor choice. Select that admitted offered choice and retain the visible configured selection only. Do not invoke Edit, launch the program or process a sample. Missing chooser/application capability remains U; arbitrary application/path acceptance, persistence, cancellation and failures require separate unknown probes.',['offered Sample Editor application-choice control','independently admitted existing editor selection; no launch']),(new[1],'In an independently admitted Settings/platform context with a separately known working folder-configuration baseline and owned existing readable folder identities, inspect the offered plug-in folder location control and separately the offered folder-use choices. Select only independently admitted offered configuration values and retain visible setting/location and use-choice states. No scan, instantiation, editor launch or resulting plug-in listing is executed or graded here. Keep native search effects with discovery002, and exact labels/path grammar/defaults/scan transitions/arbitrary plug-in acceptance U.',['offered folder-location configuration','offered which-folders-used configuration'])]:
 cases.append(dict(id='SET-'+r['id'].split('-')[-1],requirements=[r['id']],kind='control',fixture='fixtures-r2.json#SET-OWNED',setup_and_action=action,source_claim=r['contract'],documentary_expected='Named offered configuration control and selected visible state only.',documentary_comparator='Compare only explicitly documented frontend choice roles; no exact label/path grammar, file bytes, editor launch, discovery listing, signal, timing, persistence or transaction grade.',expected=None,comparison=None,target_grade='U',executed=False,evidence=r['evidence'],finite_contexts=contexts,prerequisites='Future independently admitted exact build/platform, offered supported Settings control and genuine working positive configuration baseline. Editor/folder choices must be independently eligible and already available; no installation, external program launch, plug-in scan or hardware operation is performed. Missing capability/input is U, never a successful absence test.'))
put('requirements-r4.json',req);put('cases-r4.json',cases)
# Preserve current discovery text as dated owner context instead of introducing a mutable cross-owner pin.
q=ROOT/'wiki/specs/plugin-discovery.md';snap=P/'plugin-discovery-context-r4.md';assert not snap.exists();snap.write_bytes(q.read_bytes())
review=B/'reviews/settings-owner-reconciliation-review.json';assert pin(review)['sha256']=='7cb939ffccb397dba402a4ffa74f2b907704793cf5c8748e61ad37cdbe835172'
comp=B/'settings-owner-reconciliation';assert pin(comp/'manifest.json')['sha256']=='057f3c360b605d3f8d876d9f9b187bca5c15abd4a5f3c6628de870a9fc9d4b67'
inputs=[P/'manifest-author-r3.json']+[P/n for n in prior['files']]+[comp/'manifest.json']+[comp/n for n in load(comp/'manifest.json')['files']]+[review,B/'reviews/settings-learning-owner-r3-review.json',ROOT/'tools/spec_browser.py',ROOT/'tools/build_artifact_browser.py',ROOT/load(P/'dependencies.json')[0]['path']]
inputs +=[ROOT/r['path'] for r in load(comp/'source-input-pins.json')]
put('inputs-r4.json',[pin(q) for q in sorted(set(inputs))])
put('delta-r4.json',dict(prior_manifest=pin(P/'manifest-author-r3.json'),previous_requirements_catalog='requirements.json',previous_cases_catalog='cases-r3.json',old_requirement_records_verbatim=21,old_case_records_verbatim=31,new_requirement_ids=[r['id'] for r in new],new_case_ids=['SET-020','SET-021'],new_source_blocks=['SET-B059','SET-B066'],reconciliation_manifest=pin(comp/'manifest.json'),reconciliation_review=pin(review),adopted_local_facets=['SOR-022','SOR-031','SOR-032'],G09_status='two local configuration frontends adopted only; remaining owner gaps/qualifiers not closed',native_search_owner='SPEC-PLUGIN-DISCOVERY / REQ-PLUGIN-DISCOVERY-002',discovery_context=dict(snapshot=snap.name,origin_path=str(q.relative_to(ROOT)),as_of_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=snap.stat().st_size,sha256=pin(snap)['sha256'],role='historical as-of canonical context only; not current canonical replay pin'),no_new_search_or_Edit_lifecycle_law=True,no_prior_source_case_or_oracle_changes=True))
oldspec=(P/'spec-r3.md').read_text();spec=oldspec[:oldspec.index('## Requirements')].replace('revision: 3\n','revision: 4\n',1)
spec+='''R4 adds only two documented Settings configuration frontends: choosing an
external Sample Editor application and configuring plug-in folder locations/use.
[Reviewed owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-owner-reconciliation/README.md)
remains a historical scoped mapping, not all-G09 closure. Existing Edit and native
discovery laws remain with their owners; no runtime effect is inferred from UI.

## Requirements

'''
for r in req[:19]+new+req[19:21]:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact source](#analysis-only-evidence).\n\n'
spec+=oldspec[oldspec.index('## Source-context question'):oldspec.index('## Finite acceptance proposals')]
spec+='''## Finite acceptance proposals

[Current33 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r4.json)
retain all31 R3 case records verbatim and add two bounded configuration-control
proposals for23 requirements (21D12/2U). Twenty named visible documentary roles
are source proposals only; one timing and twelve operational U documentary
outcomes/comparators remain null. Every actual outcome/comparator is null/U/
unexecuted. Missing offered control, eligible editor/folder or genuine positive
configuration baseline is U. No editor launch, scan or hardware operation ran.
Existing lifecycle probes remain unknown; no path/picker/default/acceptance law
or scan transaction is added. G09 is only partially adopted, not closed.

'''+oldspec[oldspec.index('## Analysis-only evidence'):oldspec.index('## Preserved source-audit successor')]
spec=spec.replace('[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements.json)','[Current R4 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements-r4.json)')
spec+='''## Preserved history and ownership

The [R4 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/delta-r4.json)
retains21 prior clauses and31 R3 cases unchanged before the two new records.
[Clip View023](clip-view-workflows.md) and [Project/Media012](project-media-workflows.md)
retain configured editor use/destructive edits; [discovery002](plugin-discovery.md)
already owns native system/custom folder search effects. No global absence or
new search law follows from the narrower hosting-owner gap. Picker labels,
label-to-native-switch mapping and defaults remain U. Image/linked contents are
uninspected; exact12.4.3 applicability is unknown.

All R1/R2/R3 payloads/seals/snapshots remain unchanged in place, with the existing
R1 archive retained. R4/SOR/source-audit historical inputs stay as-of; no old
consumer, pin or report is rewritten. Root owns shared navigation and combined
historical replay. The [R4 read-only checker](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/validate-r4.py)
and [R4 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r4.json)
freeze this partial successor for focused independent review. No topic is complete.
'''
research=(P/'research-r3.md').read_text().replace('revision: 3\n','revision: 4\n',1)
research=research.replace('Current case contexts are listed in the R2 section below.','These are historical R1 counts; current R4 catalogs are described below.')
research=research.replace('## R2 case-context adoption retained in R3','## Historical R2 case adoption retained through R3')
research=research.replace('one of the21original requirement records unchanged in requirements.json; current\n[cases-r2](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r3.json)','one of the21original requirement records unchanged in requirements.json. Its R3\n[case successor](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r3.json)')
research=research.replace('color/operational contexts. G09 external-owner reconciliation remains pending,\nincluding Sample Editor choice, hardware resync, plug-in folders and Max edition\nconditions; those are not covered merely because the chapter routes to an owner.','color/operational contexts. At that revision G09 external-owner reconciliation\nwas pending. R4 below adopts only two local configuration frontends from the\nsubsequently reviewed companion; owner links still do not establish full coverage.')
research=research.replace('Current cases-r3 and R3 snapshots require focused\nindependent review; G09 and all target/lifecycle unknowns remain open.','The preserved cases-r3/R3 snapshots were subsequently\n[focused-reviewed](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-learning-owner-r3-review.json).\nTheir partial scope remains historical; remaining G09 and target/lifecycle gaps stay open.')
research+='''
## R4 two configuration frontends and bounded G09 adoption

[Reviewed owner reconciliation](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-owner-reconciliation/README.md)
and [its independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-owner-reconciliation-review.json)
retain13 specified paragraphs/40 facets against historical/as-of owner snapshots,
including Settings R1. They are not current all-owner or product coverage. R4
adopts only SOR022 Sample Editor choice (SET-B059) and SOR031/032 plug-in folder
location/use (SET-B066), adding020/021 frontend clauses and two bounded cases.
[Current requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements-r4.json)
retain21 prior records verbatim plus two (23total,21D12/2U).
[Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r4.json)
retain31 prior records verbatim plus two (33total,20visible documentary proposals,
one timing/twelve operational U). Every actual result remains null/U/unexecuted.

Choosing an external editor is distinct from invoking an already configured
editor. ClipView023/Project012 retain Edit launch, stopped playback, shared source,
marker preservation and unknown destructive/lifecycle effects. No editor runs here.
For plug-in folders, the scoped hosting gap is not repository-wide absence:
SPEC-PLUGIN-DISCOVERY002 already owns independent system/custom source-switch
search effects and custom-folder predicates. The new frontend clause does not
repeat those laws or resolve exact labels, label-to-native-switch mapping, path
syntax/defaults, immediate scan/visibility, transactions or arbitrary plug-ins.
An explicitly dated [discovery context](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/plugin-discovery-context-r4.md)
retains that existing authority without a mutable cross-owner replay pin.

Remaining G09 qualifications stay explicit. SOR028 contrasts SET-B061 Standard
summary with MaxHost001's Standard plus Max for Live add-on source qualification;
Suite inclusion and edition wording give no legal/entitlement/installed-runtime
proof. MaxHost002 retains restart before the chosen Max editor becomes effective.
SOR021 Creation On paired history is still a case gap: MF011 uses default analysis
options, while MF015 explicitly sets creation Off. Causal On/Off work needs fresh
no-ASD owned copies and explicit other analysis settings, without a file oracle.
SOR038/recording:RC-020 uses a default scene-record preference, not explicit Off;
RC-021 enables it. Any causal On/Off refinement must record actual preference
state, armed/eligible empty slots and a productive recording baseline. Neither
old action supplies a target constructor default or a passing negative result.
SOR012/013 hardware Resync remains a separate unresolved Sync/Routing action gap;
port Sync enable, ordinary clock traffic and drift prose are not the missing
Resync command, payload, correction law or timing guarantee. Q031 clip-color
preference/version/creation history remains open; no random inequality or
unconditional inheritance correction is adopted. No all-G09 closure follows.

[R4 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/delta-r4.json)
and [R4 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r4.json)
preserve all prior R1/R2/R3 bytes/seals/snapshots without another whole archive.
Current R4 pages/catalogs await focused review; historical R4 crosswalk, SOR and
Settings source-audit records remain as-of and are not rewritten. No new source,
original function/UI/runtime, network/account/editor launch, scan/install/hardware
or candidate operation was performed. Root owns shared Q051/maps/log/browser and
combined historical replay; source images/captions/linked destinations and all
exact-target numerical/lifecycle results remain unknown.
'''
for name,text,target in [('spec-r4.md',spec,ROOT/'wiki/specs/settings-learning-workflows.md'),('research-r4.md',research,ROOT/'wiki/research/settings-learning-workflows.md')]:
 assert not (P/name).exists();(P/name).write_text(text);target.write_text(text)
