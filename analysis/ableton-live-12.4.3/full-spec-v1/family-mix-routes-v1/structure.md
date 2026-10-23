# Mix graph family route map — 2026-10-20

Author packet, pending one independent structure review. Analyst/spec-author
work only. Current authority is [SPEC-MIX-GRAPH revision 2](../../../../wiki/specs/mix-graph.md),
REQ-MIX-GRAPH-001–016. Its 34 case IDs and the partial 28-case released
[mix-graph-v1 manifest](../../../../handoff/mix-graph-v1/manifest.json) remain unchanged.
This packet neither revises their contracts nor grades their outcomes.

## Integration cut and method

This is a cut from approved integration packet 1b, manifest SHA256
`7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`,
and its [independent review](../reviews/integration-structure-v1-review.json).
Atlas revision 10 I-07/I-08 supplies local construction and processor-wrapper
context. I-05/I-06 supplies scheduling/automation boundaries; I-12 supplies the
unjoined render delivery boundary. The source of the cut is
[mix-structure.md](../integration-structure-v1/mix-structure.md) and
[nine construction edges plus execution interfaces](../integration-structure-v1/mix-component-edges.json).
Exact source/index locators already retained there are inherited through the
pinned manifest, rather than duplicated as another source graph.

Component layer: approved packet 1a, manifest SHA256
`392a738005f7d776dca96d7c78220cb94091081ef7086ec45b9397afccbe438b`,
uses symbol clusters, qualified aliases, RTTI/type names and constructor/vtable
evidence. At its freeze it has 25,071 exported-reference resolved indirect
sites of 268,015; 21,685 have function targets. Its 24 additional conditional
class-slot sites yield 25,095 exported-or-conditional sites. These are distinct
inventory units, neither mix coverage nor actual receiver resolution. The
OSendThreadMessage receiver proof does not apply to TrackOut endpoints.

No new graph traversal, binary read, decoder/provider/harness child, original
execution or tool installation occurred. This map reads selected retained
packet bodies and T14/X2 sources, then indexes current requirement predicates.
Inherited integration search: three depths in each direction, top 1,000
incoming-row destinations pruned except explicit seeds, at most 80 nodes and
200 accepted edges per direction/level. Mix forward rows were 97/18/9,
new nodes 20/10/9, hub omissions 501/42/56, no node/edge-budget omissions,
zero backward intersections, and 15 considered-function unresolved indirect
associations. Final frontier nodes were not expanded; zero backward references
does not prove unreachable wrappers. The inherited common wiring helpers were
partly read despite hub pruning. No new indirect resolution is credited here.

## State, data and call-chain boundaries

Observed-static means present in a retained projection or index, not an observed
run. Inferred names/owners retain the original donor/port interpretation.
Unknown means a concrete join is missing; a shared label or matching offset
does not supply it.

| Cut | Retained locator and state/data | Classification and missing boundary |
| --- | --- | --- |
| Device chain → output unit | Builder `0x102731438`, C1482–1489 and1898–1903: unit InL/R fields `+0x168/+0x170` connect to constructed TrackOut member `+0x428`; MIX-E06 | Observed-static unit-local helper arguments; named-port role inferred. Instantiated clip/instrument/device-chain output supplying these unit inputs unknown. |
| Switch control | Same builder C1683–1698, MIX-E01: Speaker/SoloPrehear → Switches/Split → MainOn/SendsOn/PrehearOn ramp nodes | Observed-static construction. T14 gate arithmetic X; load notifications, runtime dispatch and delivery order unknown. |
| Pan and volume control | Builder C1712–1750, MIX-E02/03: PanMode ramp/Pan/split controls, Group controls/transaction and Volume → Volumes | Observed-static arguments. Ungrouped T1 uses group identity; group transaction synchronization is unknown and outside scope. |
| Send control | Builder C1751–1814, MIX-E04: PrePostState → splitter → IsPost ramps; send controls → Volumes | Observed-static local construction. Twelve iterations are a local source bound, not a global Live maximum. T14 `0x1027bde00` separately gives a 12-bit reader/13th-entry error; whole-app load admission remains unknown. |
| Matrix → processor construction | Builder C1815–1891, MIX-E05: named main/meter/send matrix outputs → TrackOut inputs | Observed-static helper arguments, interpreted as ports under the inherited helper semantics. It does not bind an actual running processor. |
| Connection registration | Name lookups `0x102321f5c/0x102321e6c/0x102322044` → `0x102312ed0(a,b,c,d)` → `0x102312604(b,a,c,d,1)` | Observed-static. Valid lookups/object lifetimes/ABI are premises. Core obtains endpoint representations using virtual `+0x50/+0x58` or fallbacks and calls current virtual `+0x40`; actual methods and processing consequences unknown. No table-only class target attached. |
| Main wrapper | `0x101b1c114`, execution interface1: float input references `+8/+0x10`, local packed matrix values/steps `+0x320…+0x358`, outputs `+0x38/+0x40/+0x48` | Observed-static reads/updates/stores; TrackOut association inferred from named source/T14. Reached receiver, dispatch site and final buffer owner unknown. |
| Send wrapper | `0x101b1afbc`, interface2: referenced inputs, destination indices signed bytes `+0x2f0/+0x2f1`, table `+0x50`, gain/step state and accumulation | Observed-static local updates. Actual return bus, callback ordering and global sum ownership unknown. T14 x86 disassembly separately supports float32 products into binary64 send accumulators. |
| Local destinations → delivery | Builder C1907–2016, MIX-E07–09: main/routing/prehear/send/meter output helper arguments | Observed-static local destinations only. Main bus and export/host buffer association unknown. No rendered mix was observed. |
| Loaded solo → runtime gates | T14 notes-solo §1/§3, `0x10285cf50`, `0x10284d180`; ARM `0x102719f88` retained by 1b | Static/inferred logic; A2 loaded SoloSink notification and saved Solo/Cue copy unknown. A7 send activity (`mpActive`) is derived state, not automatically EnabledByUser. X switch-word/split computations use explicitly supplied states. |
| Envelope → point list | T14 notes-automation §1, `0x102823cb0` → iterator `0x102518360`; Float time/value arrays | Static sender writes f64 beats/f32 values and replaces first Float time with−1e7. Curves become15 interior points. Concrete loaded provider/consumer delivery remains conditional. Bool/Enum first-time rewriting is not inferred. |
| Owner → value units | T14 notes-q019 §1d: `AListAutomation+0x130` → cast/provider `0x102687e00` → target slot+8 `0x10281abe0` | Static conditional chain. A3 actual loaded owner=parameter automation target remains unjoined. Old automation-r3 A1 stored-unit generalization and T14 exact-roundtrip prose are superseded by current owner corrections. |
| Engine automation → scheduled ramps | T14 notes-automation §1b/§2/§3; `0x141110`, `0x16a240`/Live `0x101b39550`, `0x169c00` | Static segment selection/default inference. A6 parameter settings, actual offset, event receiver and callback order remain premises/gaps. Current R2 signed32 overflow rule takes precedence over old generic clamp prose. |
| Arrangement/Session state → Manual | `OAsyncTrack` index−1/k/−2, `0x13d800` automation selection and virtual slot0x38→`0x13de60` Manual | Static/inferred local state behavior. A8 initial index and stop transition remain unproved; Session envelope start/loop/warp timebase unknown. Override/re-enable/AutomationMode stay U. |

`route-basis.json` gives exact retained note line ranges, JSON pointers and
function nominations per route basis. `source-locators.json` gives 51 selected
retained JSONL row identities, byte offsets, original chunk/offset/hash and C
hashes without copying function bodies. `pins.json` binds the 47 selected inputs
and predecessor manifests/reviews. It is not a replay of their entire universes.

## Route inventory and completeness limits

[route-ledger.json](route-ledger.json) enumerates110 predicates explicitly
required by the current16 requirements:17 X routes,70 S routes and23 with no
established route. These are bounded route inventory counts, not new grades,
passes, coverage percentages or a frozen whole-product denominator.
Requirement IDs and the34 case rows are cross-reference units, not outcomes.
Numeric examples stay attached to their general predicates rather than creating
an outcome for every input. Required matrix tuples remain coherent outputs.
Source spans include the exact parent clause, an exact anchor line and a hash;
compound clauses split into independently meaningful timing/state/output facets.
Two auxiliary records retain the old-spec correction and a repeated drive
summary without counting them as additional observable outcomes.

X identifies a harness route for an explicitly required computation and retained
original results for recorded inputs. S identifies a bounded static/conditional
predicate, including the project render convention. Both retain their application
binding gaps. No-established-route identifies the required observable or U
boundary without a complete established route in this evidence. It does not
mean static recovery is impossible. Thirteen separate excluded/unresolved scope
records keep broader routing, group, delay, cue, clip-timebase, lifecycle and
pre-first-discrete contexts visible without pretending to enumerate all Live.

Cases remain12 X computations,11 conditional composed renders,10 U and one
withdrawn. MG-008 is withdrawn because its internal predicate lacks a behavioral
observable; it contributes no required outcome. MG-029 remains load-U.
MG-032–036 remain song-time U despite their retained envelope-time arithmetic.
MG-038 remains excluded/unresolved at the app boundary, even though the selected
SendsPre reader has a known local error. MG-039/040/041 remain U. The release
still narrows to28 cases and does not acquire draft-only drive/offset clauses.

All public render factors in MG-020–028/030 are attached to the required Main
delivery predicate and its unresolved receiver/bus/host join, alongside their
conditional arithmetic dependencies. T14 and X2 helper evidence alone supplies
no new public waveform credit. ADR0003 excludes whole-application observation;
the open no-route disposition has not been adopted.

## Preserved premises and batch candidates

A1 is the settled T1 render convention from ADR0004, not Live start behavior.
A2 is solo-on-load. A3 is loaded-envelope provider identity. A4 is send level
converter→Send port. A5 is the unresolved track virtual branch for crossfade.
A6 is default automation settings. A7 is EnabledByUser→active for T1. A8 is
Arrangement/Session index initialization and transitions. Each applicable row
retains these premises; no static port construction silently discharges them.

Q019 remains conditionally settled: A3/A4/A5, identity bypass unset, and missing
ARM envelope/send-path comparison. Correct ARM functions are position→gain
`0x101ac3bac`, gain→position `0x101ac3c94`. No general exact roundtrip is claimed.
ARM per-sample wrappers are not shown equivalent to x86; pan-law/crossfade and
interpolator FMA caveats remain. Reused X includes its original stub/import and
owned-input limitations, including glibc cos replacement where called.

[candidate-batches.json](candidate-batches.json) enumerates five retained call-set
candidates: matrices; interpolator/panner histories; switches/split/default fade;
Bezier/segment arithmetic; and the existing fader/crossfade dependency sweep.
Related outcomes link to these finite input records. Candidate batches are
unexecuted proposals for the post-review batch queue, not additional outcomes.
Their per-call slice, harness, inputs, stubs, timeout and results would be frozen
by the later batch. `retained-callsets.json` supplies173 exact raw command-row
locators, including complete original argument/setup/stub references. Panner
recompute is an internal dependency of the recorded setters, not a directly
called leaf. The selected return-only stub at `0x101b0ee93` is carried in the
owned T14 switch call shapes, never counted as a required outcome.

Readiness is mixed:36 X2 conversion rows patch original allocator sites while
constructing curve objects, so replay retains the preparation/peer-review gate
for patched original code. The63 scalar crossfade rows in that candidate have no
patches. No past patched success creates standing permission for another patched
run. T14 selected rows and the nine selected X2 direct pan-matrix rows have no
recorded patches; only their existing recorded harness setup/stub shapes are
nominated for standing calls. Scalar ratio values do not make the object-bearing automation
player, scheduler or TrackOut runtime graph self-contained. Three separate
not-yet-enumerable gaps preserve those receiver/clock/state boundaries. New
object construction beyond the existing harness model retains preparation/review.

## Author checks and next gate

Run `python analysis/ableton-live-12.4.3/full-spec-v1/family-mix-routes-v1/author-check.py`.
It checks selected pins, exact owner spans, all top-level normative-clause
associations, all34 case identities/dispositions, route/batch references, retained
source rows and JSON pointers. Synthetic mutations must reject an omitted
requirement, orphaned clause, duplicate ID, bad span, bad case and unknown basis.
The saved result describes these integrity checks, not independent semantic
review, original execution or an exhaustive source interpretation proof.

Root owns atlas/catalog/plan/coverage/log changes, packet seal and the one
independent review. Batch grading follows that review. No normative clause,
acceptance object, release, coverage grade or implementation artifact was edited.
