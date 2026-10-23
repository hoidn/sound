# Automation-envelope owner: bounded structure and route inventory

Authored 2026-10-20; **pending independent structure review**. Owner:
[SPEC-AUTOMATION-ENVELOPES revision 5](../../../../wiki/specs/automation-envelopes.md),
requirements 001–013. The broader automation-workflows owner is outside this
packet. No requirement, case, release or grade changes here.

The cut uses approved integration I-05/I-06, manifest
`7dddd59650ca3395d10e1b3c8aded3cda01d66b522dda4973a08f32e7bfb8f83`, and the
approved [mix-family map](../family-mix-routes-v1/structure.md), manifest
`c4ad95bef8e44db6c01c654f471347c6d666305894a104f3f5e3bff3d06fdab9`, with its
[independent review](../reviews/family-mix-routes-v1-review.json). The review’s
editorial note about float32 send products and binary64 accumulation does not
change any automation outcome. Predecessors are pinned, not replayed wholesale.

## Bounded inventory

The [ledger](route-ledger.json) enumerates **129 required semantic predicates**:
22 X-route, 69 S-route, 38 no-established-route. These are route inventory
counts, not passes, grades, a completed family or a frozen whole-product denominator.
[Clause decomposition](clauses.tsv) retains 136 formulations; seven repeated
summaries/general-rule specializations are cross-references rather than duplicate
outcomes. Every row has an exact owner clause/algorithm span and context, related
case navigation, evidence basis, qualified route and concrete missing join.

Shipped counts, unique-Id/NextPointeeId statistics, leading-value distributions,
helper-only dependencies, numeric examples and excluded-input fault controls are
auxiliary. They do not enlarge the required-outcome count or impose new load
requirements. Owner exclusions remain: dangling/wrong/cross-track target relations,
logic evaluation before the first event, three-or-more coincident-event fixtures,
and older migration. In particular a retained fault is not a required crash.
All owner D/S/X/U labels and the 33 case dispositions remain unchanged, including
the two withdrawn cases. The partial current release still has 21 cases and
releases no evaluator/playback values.

An X-route identifies an established local original-function computation route;
it does not say every prospective branch vector was run. S-route identifies the
qualified static/schema predicate. No-established-route means no complete route
at the stated unknown/public/state boundary under ADR 0003 and this evidence
scope, not global impossibility or an exclusion. A helper return cannot close
actual UI reading, loaded parameter application, song-time drive or audio output.

## Keep the value and time boundaries separate

| Boundary | What retained evidence supports | What it does not establish |
| --- | --- | --- |
| Stored document values | Target-kind schema, typed event values, Time/curve attributes, target Id lookup and member lexical/writer rules. | Shipped uniqueness is not duplicate-Id refusal; a stored target Id is not the actual active converter/provider. |
| Logic evaluator E(t) | Supplied list/provider/mode at explicit envelope time. X2 identity/full-range results cover Pan’s identity conversion; Float hold/event/equal/linear/curve and discrete getters are separate branches. | Which UI/LOM/other consumer reads E(t), which mode it passes, or whether a loaded owner is the parameter target. E(t) is not playback output. |
| Parameter conversion | Conditional owner-at-`+130` cast/provider `102687e00`, target slot `+8` at `10281abe0`, parameter conversion step `101565810`. Pan is identity; Volume/Send gain values map to fader positions when that target owns the envelope. | Actual loaded owner/provider is mix A3. A separate null-converter construction cannot prove ordinary envelopes use stored units. No general exact gain roundtrip follows. |
| Ideal playback P(t) | Float point-list construction and engine segment arithmetic at supplied envelope time: 15 Bezier interior points/16 straight pieces; Float first time `−1e7`; later event at a step. Discrete lookup uses mode 1. | Actual loaded settings/segment-update behavior remains mix A6; these are not ramped output samples. Do not infer a Bool/Enum first-time rewrite. |
| Clip/song time and delivery | Static scheduler/event/offset/index landmarks identify the missing boundaries. | Clip start/loop/warp timebase, song offset, initial Arrangement/Session index and transitions, actual event/player receiver, parameter units/processor delivery and ramped samples remain conditional or U (mix A3/A6/A8). No zero offset is assumed. |

P(t) can define a value before an original first event at 0 through its point-list
rule; this does not remove E(t)’s excluded pre-first-event domain. Exact E(t)
comparators and ideal P(t) columns must not be used on samples held/shortened by
automation ramps. Ramps/settings/sample delivery stay owned by mix graph.

## Removal, normalization and validation

The current owner/release corrections govern over earlier research statements:
member parsing and enabled member post-load steps, then root post-load discard,
then the unconditional survivor validation walk. Discard does not repair a lexical
parse error that already stopped member reading.

- A clip envelope with exactly one event is removed; an empty clip envelope survives
  that count test and reaches the empty-list refusal.
- Track envelopes on the scoped Speaker/Pan/CrossFadeState targets with fewer than
  two events are removed. Main tempo/meter exceptions remain; other targets can opt
  out. The target’s own-device relation and unchanged application-start discard
  setting remain premises accepted by RA2.
- Removed envelopes cannot trigger survivor empty-list/invalid-first-time refusals.
  Surviving first times are compared after binary64 parsing against L or 0, including
  signed zero. Later times do not fail that particular check.
- T11 establishes the Live Set post-load context enabled. Surviving curve controls
  are retained if both coordinate pairs satisfy M; otherwise all four reset to 0.5.
  The local writer then omits those default control attributes. Actual public Save
  binding/Id handling retains A5.
- Timeline lists are a separate class/context. The no-other-owner-check premise of
  AEN-033 remains; this packet does not infer complete Arrangement/take-lane behavior.

## Retained call-chain cut

[Sources](sources.json) retain 67 selected JSONL rows and 24 dossiers, exact row
byte/hash/C locators, native call PCs and original warnings. C is available in all
91 selected entries; unlocated appendix nominations and historical scratch slot
reads remain explicitly unlocated, not invented C. Approved mix route-basis/source
locators supply the inherited T14 converter, point, segment, settings and drive
boundaries without copying their old bodies. Source names are inferred roles;
observed-static references/expressions are not runtime execution or delivery.

| Component boundary | Exact retained locator | Qualification |
| --- | --- | --- |
| Root load/post-load → walk | S6 `101486fe4@101487124 → 101487198`, AE-E01; T11 `traces/a1a2/trace.txt` lines19–34 records context `+2c`, root `+d0` before unconditional walk and member post-load enablement. | Static call/order and traced app-entry premises; no whole Live run. |
| Root post-load → discard | Reviewed removal rows: `102695f78 → 102711584`; clip `102456e98 → 1024559b8`, track `102406378`; count helpers `1025619e0`/`1025654e8`, relation `1024dd434`, gate `10185138c`. Exact C spans/original byte-row locators in catalog. | Inherited RA2/T11 conditional semantic chain; own-device relation, gate stability and target opt-out remain qualified. |
| Envelope wrappers → survivor check | Wrapper C at `1024050d8` and `10245194c` uses virtual `+1e8` at native PCs `102405108`/`102451980`. S6 retained vtable line112 has operand `1067d08a0 → 102561a28` at address point `1067d06b8`. | Conditional AListAutomation receiver/address-point association, not a direct call or new unconditional indirect resolution. Unrecovered indirect-jump warnings retained. |
| Curve normalization → M | `102778870@102778894` and `@1027788ac → 1012132d8`, AE-E02/03, with exact dossier reference pointers and C lines. | Surviving-event/reset semantics use enabled context; M has an independently callable scalar route. |
| Float evaluator → conversion | `1024095b4 → 101574bb0` at PCs `10240973c`, `1024097dc`, `10240997c`, `1024099c8`, `1024099e4` (AE-E04–08). | Conversion applies across branches, not only linear interpolation. Actual loaded provider/converter remains unbound; full-range X remains local. |
| Parameter owner → unit provider | Approved mix `route-basis.json#/q019` and `/automation-points`; T14 `notes-q019.txt` §1d, `notes-automation.txt` §1. | Owner cast/target converter chain is conditional. Earlier stored-unit prose does not override current r5/mix r2. |
| Logic point list → command | Integration source record7 `1026f1e4c` C43–48 constructs descriptor `106e522b0` and sends count/time/value pointers; inherited mix point basis identifies x86 `102823cb0`, iterator `102518360`, Bezier subiterator `102520a60`. | Local array/message construction only. Actual ARM descriptor-handler/provider and parameter application remain unjoined. |
| Scheduler → event/player | Integration record1 `101ab5cec` C101/C172 dispatches virtual `+10`; mix bases `/automation-points`, `/segment`, `/automation-rate`, `/automation-drive` distinguish lookup, local segment and scheduling/drive state. | Concrete event receiver, callback order, lane/index/offset, ramp/sample and host delivery remain unknown. OSend receiver proof cannot transfer here. |

No new graph traversal, binary read/decoder or indirect resolution occurred.
The inherited layer uses packet1a symbol clusters, type names and constructor/
vtable candidates. Baseline 25,071 nonempty-reference sites of 268,015 is separate
from 24 conditional additions (combined inventory 25,095). Integration bounds
remain depth 3, top 1,000 hubs pruned except explicit seeds, 80 nodes/200 edges
per direction/level, with unknown and terminal frontiers retained. Those counts
are navigation units, not automation outcome coverage.

## Finite inputs and method limits

[Batch inputs](batch-inputs.json) compactly select **80 historical input/result
rows**, not call counts or outcomes: 22 Float evaluator values, 22 discrete values,
6 Pan-converter values, 4 M controls, 17 Bezier points (15 interior) and 9 ideal
segment results. Original event lists, explicit times/modes/provider records and
call tokens remain in the pinned drivers/raw results. Three historical fault
controls stay outside the required domain. Six prospective nonfinite/overflow M
vectors are enumerated without claiming execution or complete branch/NaN coverage.

The X2 evaluator setup used original factories, subset registries and extended
library bindings; 295 of 3,322 historical initializers stopped at imports/faults
and were abandoned. That setup is not automatically within today’s standing
harness class. Future construction/patches need their applicable gate. No future
batch is selected or authorized by this map.

X2 is x86_64/Linux with substituted libraries and supplied object graphs. The
linear evaluator uses glibc `fma` with fused operation order matching both slices
statically. Arm64 curve bisection/M use fused operations where x86 uses separate
multiply/add; the claimed below-1e−6 curve difference is inferred, not measured
or proved at every threshold. Ideal segment helpers do not establish a sample
trajectory. Current mix-r2 signed32 overflow/shortening rules take precedence over
older T14 generic clamp prose.

## Checks and review boundary

Run `python analysis/ableton-live-12.4.3/full-spec-v1/family-automation-routes-v1/author-check.py`
from the repository root. [Author results](author-check.json) check selected pins,
owner clause/context hashes, source C/PC/pointer locators, bounded clause/outcome/
case/input accounting, local links and the full protected research prefix. They
are mechanical checks, not independent semantic review or compatibility proof.
Root seals and separately reviews this packet and owns shared atlas/index/coverage/
log updates and next selection. No original function/instruction, provider, decoder,
harness, installation, candidate or original application ran in this packet.
