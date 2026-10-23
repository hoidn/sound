#!/usr/bin/env python3
"""Own R4 text/data renderer. --check never writes; --write refuses sealed R4."""
import argparse,json,pathlib,re,hashlib,difflib
ROOT=pathlib.Path(__file__).resolve().parents[4]
D=pathlib.Path(__file__).resolve().parent
SPEC=ROOT/'wiki/specs/device-racks.md';RESEARCH=ROOT/'wiki/research/device-racks.md'
def load(n):return json.loads((D/n).read_text())
def encoded(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
def requirements(text):
 out=[]
 for m in re.finditer(r'^### (REQ-DEVICE-RACKS-\d+) — ([^\n]+)\n(.*?)(?=^### |^## |\Z)',text,re.M|re.S):out.append(dict(id=m[1],title=m[2],contract=m[3]))
 return out

def build():
 p=load('adoption-r4.json');s=(D/'spec-before-r4.md').read_text();r=(D/'research-before-r4.md').read_text()
 s=s.replace('revision: 3\n','revision: 4\n',1);r=r.replace('revision: 3\n','revision: 4\n',1)
 before=requirements(s)
 for a in p['appended_contracts']:
  old=next(x for x in before if x['id']==a['id']);s=s.replace(old['contract'],old['contract'].rstrip()+'\n\n'+a['append']+'\n\n',1)
 new=''.join('### '+q['id']+' — '+q['title']+'\n'+q['contract'] for q in p['new_contracts'])
 s=s.replace('## Historical corrected R1 acceptance cases',new+'## Historical corrected R1 acceptance cases',1)
 # All previous current/pending catalog prose is an explicit historical as-of route.
 section='''
## R4 bounded Common Devices successor

All preceding R1–R3 catalog/status and narrower CommonDevices/A-B/default
exclusions are historical as-of those author freezes. This R4 section selects
current acceptance without rewriting their payloads, original predicates or
expected strings. The [approved full Common Devices source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/device-chain-source-audit/README.md)
and [independent review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-chain-source-audit-review.json)
retain153source contexts,153whole-context judgments,140literal resources,
20proposals and41selected neighboring records. Every full paragraph/list
qualifier, all28old contracts and81fullactions were read for this successor.
This is no atomic-facet/whole-group closure, image/link inspection or target run.

Common023–026 retain their old predicates plus bounded route/context appends.
Distinct029–031 own A/B slots, parameter-context automation and selected-state
copy/duplicate/preset relationships;032–038 own seven different default families.
The [20-group ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/adoption-r4.json)
records only actual adopted inputs and remaining unknowns. Browser/focus/stack/
generic-edit/monitoring/compensation/collection/API and current Conversion036/037
subsets stay with their existing owners. No duplicate DSP or whole neighboring
chapter contract is created.

[Current requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/requirements-r4.json)
contain38IDs. [Current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/cases-r4.json)
contain101records: all81R3records verbatim plus20RCK082–101. Criterion classes
are3installed assertions/86documentary proposals/12U. Seven new named UI-role
pairs are documentary only; thirteen new pairs and allnew legacy/numeric/audio/
MIDI/message/timing/RNG/fileoperation comparisons are null. [Actual status](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/actual-status-r4.json)
is null/U/unexecuted for every101case, including old nonnull documentary strings.
No target outcome/compatibility/coverage/family/source-topic completion follows.

[Future prerequisites](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/fixtures-r4.json)
require genuine productive controls, recognized successful save AND load before
absence/default/overwrite, eligible A/B and distinct states, actual parameter
contribution before switching, and PARAMETER-context Re-Enable rather than global
or automatic restoration. Sample HotSwap keeps the expanded Sampler exception.
Options data is inert; only independently recognized EXISTING configurations may
support future comparisons, with no file edits now. Plug-in defaults retain a
parameter LIST, not VALUES. Last-ADDED histories differ from timestamps/name sort.
Conversion preview needs genuinely NONEMPTY recognized notes and independently
nonzero active output; no arbitrary source is promised notes. UI-only needs no
hardware/audio. Failed/unavailable prerequisites remain U, never negative passes.
Existing R2positive guards and R3whole-zone movement clarification remain exact.

[Preserved identities](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/prior-files-r4.json)
retain all49old files and seals in place. Exact before/current canonical snapshots,
[immutable inputs](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/inputs-r4.json),
[delta](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/delta-r4.json) and
[historical consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/consumer-impact-r4.json)
are as-of providers, not future live canonical gates. No old author/checker/capture
main, consumer replay/adapter, file/configuration action, source recapture or
original/vendor/native/UI/hardware/network/example/candidate ran.
**AS-OF AUTHOR FREEZE:** independent R4 owner review pending; [spec index](index.md)
owns current disposition. DCA-Q01–04 and existingQ025/Q027 remain open. Source
Version12/publication/build/OS/reader/default-failure/lifecycle applicability,
DSP/headroom/CPU/latency/codec/RNG/timing/protocol/fileatomicity remain U.
'''
 s=s.rstrip()+'\n'+section
 r=r.rstrip()+'''

## R4 bounded Common Devices adoption

All earlier current/pending wording is historical as-of R1–R3. R3focused correction
was [independently approved](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/racks-owner-r3-review.json)
without widening the B044whole-zone movement predicate. The approved
[Common Devices full-source audit](../../analysis/ableton-live-12.4.3/full-spec-v1/device-chain-source-audit/README.md)
and [review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/device-chain-source-audit-review.json)
cover153fullsource paragraphs/list/headings,153whole-context judgments (not atomic
facets),20audit proposals and41selected actual neighboring predicates/actions.
All153texts/qualifiers,20proposals,41selected neighbors and current28contracts/
81fullactions were read. All140baseURL/caption/empty-alt roles were inspected;
responsive variants hashchecked only; no image pixels or linked destinations.
Verbose repeated-field outputs were reread in bounded projections where truncated.

The retained CommonDevicesHTML remains302488bytes, SHA256
6a783fde3de24178e1b1d4b8431ada1a1691a1c8f16a633f909bac347e72cd82,
original capture2026-10-19T20:01:52.371400Z, Version12current with precise
publication and target12.4.3 parity unknown. No recapture/date substitution.
R4refines only023–026 and adds029–038 for distinct A/B/default families.
[Current38requirements/101cases](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/README-r4.md)
keep all81R3records verbatim, including sourceclaims/oracles. Twenty new actions
are D12proposals; only seven named UI-role pairs have documentary criteria,
thirteen null and allactual/numeric/audio/message/time/RNG/filecomparisonsnullU.
No completion or reference/candidate run occurred.

The20-group ledger retains bounded missing inputs without completing entire
groups. True WORKSPACE009/CV001/NAV014/NAV079, RMLmonitor/compensation,
PluginHosting009/PH017, Project019/PMW026–028, Browser040 and APIA-B records
remain their own narrow scopes. Current ConversionATM036/037 already requires
factory/no-custom histories and actualNONEMPTYnotes plus genuinely nonzero active
preview; old029absence is not substituted. Pitched custom defaults may use a
single instrument OR Rack; Drums must use nonnested DrumRack. No arbitrary
conversion input is promised notes. Allold primaryRack laws, RR01sameunitAND
range and RR02factory qualifications remain exact.

A/Bautomation needs actualchangingparametercontribution, selected-state PARAMETER
context Re-Enable, and no automatic restoration or global substitute. Selected
copy/duplicate/preset state is documentary, not numeric/codec/fileequality.
Preset and sample HotSwap differ; expanded Sampler top-left button is always
visible while fourother contexts use hover. -EnableHotSwapOnSelection remains
inert source text; future tests require independently recognized EXISTING owned
configurations, no Options edits. Plug-in configuration saves LISTnotVALUES;
families keep factory/custom/lastADDED/Project contexts distinct. Recognized
successful save/load and genuinely productive controls precede absence/overwrite;
flags/names/folders alone fail that prerequisite. Editor controls need no audio.

[Preservation](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/prior-files-r4.json),
[exact delta](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/delta-r4.json) and
[consumer census](../../analysis/ableton-live-12.4.3/full-spec-v1/racks/consumer-impact-r4.json)
keep49old files/seals and oldconsumer as-of identities unchanged, no automatic
adapter or replay. Own immutable source/current-snapshot pins govern this draft;
no futuremutablewiki gate. DCA-Q01–04, target/default/Option parser/build/context,
failures/undo/persistence/transport/teardown, numerical/DSP/CPU/headroom/latency/
RNG/protocol/codec/fileatomicity stayU. No original/vendor/native/UI/audio/MIDI/
hardware/network/account/install/config/fileoperation/sourceexample ran.
**AS-OF AUTHOR FREEZE:** R4independent owner review pending; [spec index](../specs/index.md)
owns current disposition; this author does not self-approve or close coverage.
'''
 req=requirements(s);assert len(req)==38
 for i,g in enumerate([6,7,8,14,15,16,17,18,19,20],28):
  req[i]['source_contexts']=p['new_cases'][g-1]['source_contexts']
  req[i]['provenance']='D12';req[i]['target_applicability']='U';req[i]['complete']=False
 cases=load('cases-r3.json');cases['version']=4;cases['criterion_scope']='R4 keeps all81R3records exact and appends20CommonDevices documentary actions. Legacy expected strings are documentary only; all101actual outcomes null/U/unexecuted.';cases['cases']+=p['new_cases']
 delta=dict(role='Exact reconstructed before/current catalog differences; no oldcase edits',before_requirements=28,after_requirements=38,old_cases_exact=81,new_cases=20,appended_contracts=p['appended_contracts'],new_requirements=[x['id'] for x in p['new_contracts']],new_case_ids=[x['id'] for x in p['new_cases']],canonical_changes='revision3to4; four bounded contract appends; ten distinct headings; currentR4routing append. All earlier statuses qualified historical as-of.',complete=0)
 delta['requirement_field_deltas']=[dict(id=b['id'],field=k,before=b.get(k),after=a.get(k)) for b,a in zip(load('requirements-r3.json'),req[:28]) for k in b.keys()|a.keys() if b.get(k)!=a.get(k)]
 delta['canonical_patches']=[dict(kind=k,before_sha256=hashlib.sha256((D/f'{k}-before-r4.md').read_bytes()).hexdigest(),after_sha256=hashlib.sha256(t.encode()).hexdigest(),unified_diff=''.join(difflib.unified_diff((D/f'{k}-before-r4.md').read_text().splitlines(True),t.splitlines(True),fromfile=f'{k}-before-r4.md',tofile=f'{k}-r4.md'))) for k,t in [('spec',s),('research',r)]]
 status=dict(scope='Everycase actualoutcome unknown, including legacy installed/documentary strings. Installed cases are file-only assertions, never product execution.',cases=[dict(id=x['id'],actual_expected=None,actual_comparison=None,target='U',executed=False,complete=False) for x in cases['cases']])
 return {'spec-r4.md':s.encode(),'research-r4.md':r.encode(),'requirements-r4.json':encoded(req),'cases-r4.json':encoded(cases),'delta-r4.json':encoded(delta),'actual-status-r4.json':encoded(status)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--write',action='store_true');args=ap.parse_args();assert args.check!=args.write,'Choose --check or --write'
 if args.write and (D/'manifest-author-r4.json').exists():raise SystemExit('R4sealed; writes refused before build')
 out=build()
 for n,b in out.items():
  if args.write:(D/n).write_bytes(b)
  else:assert (D/n).read_bytes()==b,n
 for p,n in [(SPEC,'spec-r4.md'),(RESEARCH,'research-r4.md')]:
  if args.write:p.write_bytes(out[n])
  else:assert p.read_bytes()==out[n],str(p)
 print(json.dumps(dict(mode='write' if args.write else 'readonly',requirements=38,cases=101,oldcases_exact=81,newcases=20)))
if __name__=='__main__':main()
