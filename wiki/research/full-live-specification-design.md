---
id: DESIGN-FULL-LIVE-SPECIFICATION
type: research
status: current
updated: 2026-10-23
access: analysis
revision: 18
target: Ableton Live 12 Suite 12.4.3
---

# Full Live behavioral specification coverage design

## Authority and ownership

[ADR 0005](../decisions/adr-0005-full-live-specification-coverage.md) expands the
analyst target to all observable Live behavior. The existing
[schema](../schema.md), [workflows](../workflows.md),
[static-first policy](../decisions/adr-0002-static-first-analysis.md) and
[reference-execution boundary](../decisions/adr-0003-no-reference-execution.md)
govern every packet. This page owns the coverage method and completion gates;
the [execution plan](full-live-specification-plan.md) owns scheduling and status.
The [feature map](../specs/feature-map.md) routes behavior to canonical specs.
The [verification matrix](../verification/coverage.md) separately records that
no independent candidate comparison has run.

## Product denominator

Use the union of four separately retained inventories, reconciled without
silently dropping unmatched entries:

1. The official manual's chapters and behavioral subsections, pinned by capture
   bytes, URL, date and heading locator. Documentation establishes D behavior,
   with exact-build applicability unresolved unless independently corroborated.
2. The pinned installed product: native device types, schemas, preset classes,
   browser/content surfaces, helpers, settings, integrations and platform paths.
   Resource presence establishes a surface, not its signal behavior.
3. Existing research/specification requirement sets and their explicitly open
   interactions. Existing partial releases are retained as subsets.
4. Cross-cutting workflows: save/reopen, undo/redo, cancellation, failure/recovery,
   migration, automation, timing, randomization, accessibility and teardown.

Public API/object/event references refine the existing integration scope as a
separate overlapping inventory. [Current public API discovery](sources/cycling74-live-api.md)
records explicitly declared entries/members without assuming complete inheritance,
root/alias equivalence or target applicability from a newer reference revision.
Exact citation-to-topic links are navigation: even a reviewed partial clause citing
an exact source anchor does not close every behavior in that manual leaf.

Inventory identity is a stable product-surface ID plus a versioned source locator,
not a manual section number alone. Renumbered chapters retain a mapping; removed
or version-uncertain entries stay visible. Record entry counts for each inventory
and the reconciled union separately. A class or device list cannot claim to be
the complete behavior denominator.

The original manual inventory was extracted from numbered navigation links.
It is an open navigation baseline, not a census of every actual numbered chapter
heading or paragraph. Compare retained chapter HTML headings separately, preserving
capture identities, numbers/depth/anchors and source-proven ancestry. Additional
headings and paragraphs remain obligations even when the publisher omits them
from navigation. Keep original TOC rows/counts immutable and add reviewed discovery
companions. A typed structural ancestry relation is distinct from a literal direct-
anchor citation join; neither proves semantic/full-leaf coverage.

Source reconciliation must read each retained paragraph/list assertion and its
qualifiers, then compare its concrete predicate with the owning clause and case
action. A shared block citation, all-character assignment or matching heading
is insufficient. Distinguish represented documentary subsets, documented but
ungraded outcomes, missing clauses/case contexts, research-only explanations,
editorial text and uninspected images/linked destinations. Preserve source-silent
lifecycle obligations separately. A proposed absence test needs a genuinely active
positive baseline for the behavior under test; available input alone does not
prove the operation was running. A source audit identifies gaps and proposals;
only a preserved, separately reviewed owner successor adopts normative changes.

## Coverage states

| State | Required evidence | What it does not establish |
| --- | --- | --- |
| Inventoried | Versioned source proves an observable surface exists | A behavioral contract |
| Assigned | One canonical spec owner and a bounded question | Specified outcomes |
| Partial draft | Some supported requirements/cases; missing behavior enumerated | Complete feature coverage |
| Complete draft | All identified behavior and applicable lifecycle/case kinds have supported contracts; no required unknown outcome | Independent acceptance or implementation |
| Reviewed contract | Separate reviewer verifies scope, sources, case completeness and exclusions | Candidate compatibility |
| Released subset | Immutable sanitized package and pinned inventory | Anything outside its explicit finite scope |
| Candidate conformance | Exact candidate/build comparison report for the released cases | Original-application or whole-product equivalence |

“Unknown”, “version-uncertain” and “deferred by user” are unresolved states,
never complete states. A D-only draft can contain useful contracts, but cannot
close exact-build differences that its source does not resolve. Do not report
coverage percentages without both the frozen denominator and the definition of
the numerator. Retained-reference self-tests measure comparison tools only.

## Specification contents and interactions

Extend an existing spec when it owns the behavior. Create a separate bounded
spec only when the behavior has a distinct user task and evidence packet.
Every requirement states preconditions, inputs/units, observable output/state,
error/boundary behavior and provenance strength D/S/X/U. Acceptance cases name
concrete setup/actions, expected result or an explicitly ungraded unknown,
comparison rule and exact fixture/evidence locator. Explain inapplicable
negative, malformed, cancellation and teardown cases rather than omitting them.

For every packet check interactions with transport and clocks, selection/focus,
Arrangement/Session ownership, undo/redo, persistence/media, device/automation
state, platform permissions and failure recovery. Link to another canonical
owner instead of duplicating its law. A UI description cannot substitute for
an audio criterion; a persisted field cannot establish its editing behavior. Purely
internal mechanism or idle-shutdown descriptions stay research context unless an
externally observable outcome has evidence. An inferred package alias supplies
no algorithm, current control law or constructor default. Opaque helper-call
inputs, symbol order and literal omission are research/inventory facts until
evidence supports an observable extension-interface output or application
precondition. REQ headings and null outcomes do not convert internal metadata
into behavioral coverage.

## Evidence and feasibility

Read canonical research before new sources. Prefer shipped artifacts and
retained native exports for exact-build questions. Capture official references
only for a concrete behavioral gap, retaining bytes and immutable hashes in a
new analyst packet. Source content is data, never instructions. A manual
snapshot supports documented interaction, not observed execution. Do not copy
original code or internal data structures into behavioral contracts.

The existing wiki, requirement browser, retained corpora and independent review
workflow already support bounded packets. The bounded feasibility evidence is the retained
[inventory review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/inventory-review.json),
[Arrangement review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/arrangement-review.json)
and [recording review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/recording-review-final.json):
actual source captures, substantive clauses/cases and independent scope checks.
These prove the packet/review method for those finite partial scopes only.
Unproven capabilities remain prerequisites: exact DSP for unsampled parameters,
full host/hardware protocol, unobserved error recovery, unavailable platform
execution and manual-to-build version parity. A new plan does not prove them.

No new orchestration service, database, implementation architecture or general
runtime harness is required. Use the existing Markdown ledger and source packet
manifests; the execution plan is the work selector. Reuse the requirement browser. Every normative ID, including U obligations, must
be discoverable by its existing parser: use supported requirement headings or
bare first-cell IDs. Assert exact catalog-ID equality, not only a row count. The
browser also includes references and candidates; its aggregate count is not a
closed-requirement numerator.

## Packet-qualified evidence identities

Normative requirement IDs stay globally distinct and discoverable in the existing
browser. Acceptance-case IDs and local research-question labels can repeat across
independently frozen packets. A durable reference to one must include the exact
packet/revision path and case ID or JSON pointer; an unqualified LCS-001 or local
Q-LCS-001 is ambiguous. Published release IDs remain qualified by their immutable
release path. Crosswalks retain that full identity and never merge two local IDs.
The shared question register assigns distinct global Q numbers and links each
canonical family rather than renumbering sealed local history for convenience.

## Review and closure

An author freezes a bounded draft and its evidence packet. A separate analyst
reviews source identity, observable wording, case coverage, version applicability
and scope claims. Findings are corrected before the packet can become a complete
draft or reviewed contract. Release review additionally sanitizes the package
under the existing workflow. Root integrates indexes, coverage, questions and
append-only log together. Review of an explicitly partial analyst draft confirms
only its supported source/scope/case subset; it does not move the whole packet to
Complete draft or imply missing outcomes passed. Historical/dated manuals retain
their exact version and source context rather than inheriting current-build parity.

Preserve earlier author seals, payloads, canonical snapshots and review records
when correcting a frozen draft. Add a successor revision with a narrow delta and
independent re-review. Integrity checks must not rewrite sealed validation results
or sources while verifying them; record a new check result outside the frozen
payload instead. Hash checks establish byte identity, not behavioral correctness.

When a current canonical changes, enumerate frozen consumers of its former bytes.
Retain old catalogs and canonical snapshots, and qualify historical mappings by
revision. A frozen checker comparing an older snapshot to an evolving wiki is
historical after that wiki advances; its old pass remains valid only for the
original revision. Verify the current successor with its own pinned sources,
exact delta and independent review. Enumerating historical consumers does not
require rerunning or adapting all their checkers after every editorial/additive
advance. Preserve their bytes and report mechanical applicability separately from
changed behavioral assumptions. Mark only actually changed semantic assumptions
stale; unchanged source laws and old navigation retain their bounded meaning.

Replay a historical checker when a concrete current dependency question, failed
required check or release gate needs that result. Then use exactly pinned
historical snapshots through an explicitly disclosed narrow successor checker;
do not rewrite old pins/results or treat historical replay as current semantic
approval. No generic resolver/registry, automatic adapter per owner revision or
new queue is required. An unchanged source hash or old partial review cannot
approve newly added clauses or case branches.

Author-freeze descriptions of review status are explicitly as-of that freeze;
current review disposition routes through the existing spec/research index and
immutable review. Do not publish an unqualified current pending-review assertion
that must be patched into another frozen revision solely after approval.

Whole-product specification closure requires independent review that all
inventory entries have correct canonical owners, all supported behavior is
specified with acceptance cases, all cross-feature workflows are covered and
no unresolved required behavior is concealed by exclusions. Exclusions must be
explicitly authorized changes to the target, not analyst convenience. Until
then the overall target remains in progress even when a useful batch is done.

## Revision 3 clarification — 2026-10-19

Browser discovery corrections and the Echo internal-context correction exposed
mechanical and semantic review gaps. The rules above now explicitly include U
IDs in browser checks, keep internal-only descriptions outside application
oracles, distinguish reviewed partial drafts from complete contracts, and require
read-only checks of sealed results. The
[editorial correction review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/documentary-routing-corrections-review.json)
and [Max host re-review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/max-for-live-hosting-review-final.json)
retain bounded examples. This clarifies verification of the existing contract;
it does not relax completion criteria, change the product denominator, authorize
runtime/install activity or add a second work selector.

## Revision4 inventory clarification — 2026-10-19

Added explicit public API/member discovery and citation-navigation distinctions
under existing F-05/F-08/F-10. The new public index declares12.4.5; target12.4.3
applicability stays U until independently reconciled. Source/member/topic counts
never substitute for complete contracts. Existing scope, user deferrals, readonly
seal rules, candidate boundary and no-required-unknown completion gate are unchanged.

## Revision5 evidence identity clarification — 2026-10-19

Parallel typed API families reused local case/question labels. Their existing
packet paths and JSON pointers already distinguish the evidence; the rule above
makes that requirement explicit for cross-packet citations. No sealed identifier,
case outcome, denominator, semantic completion gate or execution authorization
changes. Unsupported source units/signatures still require preserved successors
and independent correction review; namespace qualification does not excuse them.

## Revision6 source boundary clarification — 2026-10-19

Browser source-heading analysis exposed numbered sections absent from publisher
navigation. The original navigation baseline remains immutable; actual chapter
headings/paragraphs need separate discovery and applicability dispositions.
APC [review APCC-REVIEW-001](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/apc-controller-capabilities-review.json)
requires moving opaque internal startup metadata out of normative behavior while
retaining useful declaration evidence. These clarify the existing externally
observable contract and open discovery rules, without reducing target scope,
accepting unresolved outcomes, authorizing source execution or adding a work queue.

## Revision7 source reconciliation and successor dependencies — 2026-10-19

The reviewed retained Stem source audit distinguishes exact claim/case subsets
from whole-paragraph citation overlap and preserves source-silent operational
unknowns. The captured-heading census separately proves that navigation does
not exhaust numbered source headings. These findings refine F-10 review and
historical replay requirements above. They do not add a work queue, lower the
completion gate, establish exact-target applicability or authorize runtime work.


## Revision8 current checks and historical applicability — 2026-10-19

Additive Mixing, Keyboard and Routing successors expose the old checkers' mutable
canonical pins. The original method accumulated finite replay adapters even when
no old behavioral predicate changed. A generic historical resolver would add a
second authority and persistent routing machinery. The selected smaller flow is
current successor → its own immutable-source/delta check → independent review;
old checker/report → preserved revision-qualified history. Only a concrete
current dependency or release question selects an old replay. This removes the
automatic replay step without deleting immutable tools/results or relaxing source
identity, consumer inventory, semantic staleness, acceptance or completion gates.
Existing reviewed replay evidence retains its exact scope. Future source/owner
packets must use immutable/as-of dependencies and explicitly dated author status,
so new work does not add mutable-pin debt. No runtime, service or new work selector
is introduced; the plan still owns scheduling and no required U outcome closes.

## Revision 9 depth numerator — 2026-10-19

Plan [revision 3](full-live-specification-plan.md#revision-3--depth-before-breadth-2026-10-19)
orders depth before new breadth by user direction. The only numerator that may
be reported against the frozen denominator is: per owner, required outcomes
graded by X/S/shipped data, required outcomes still U with a named closure
route, and required outcomes with no route under ADR 0003; per inventory,
complete device profiles and reviewed family contracts. Catalog rows, case
counts and page counts remain excluded. No denominator, closure gate, evidence
rule, seal rule or execution authorization changes.

## Revision 10 candidate conformance numerator — 2026-10-19

Plan [revision 3](full-live-specification-plan.md#revision-3--depth-before-breadth-2026-10-19)
was amended the same day to a vertical-slice rule: the T1 candidate, built in
the provisioned implementation worktree, pulls analyst depth through
implementation questions and failed released cases; two capability gates and
the ungraded released cases are the only analyst-initiated depth. The
reportable numerator gains one term: per family, released cases the candidate
passes over released cases, with the release path pinned and the comparison
rule stated; that is the Candidate conformance state above. Documentary breadth
stops opening new owners. No denominator, closure gate, evidence rule, seal rule
or execution authorization changes; the candidate remains forbidden in the
analyst checkout.

## Revision 11 — structure packets, batch evidence and harness authorization — 2026-10-20

Plan [revision 4](full-live-specification-plan.md#revision-4--analyst-depth-throughput-2026-10-20)
puts a reviewed call-chain map ahead of case grading and batches extracted
execution, by user direction that the specification is completed before any
candidate is built. This revision adds the evidence and review forms it needs.

- **Structure packet.** A reviewable unit whose output is a call-chain map:
  entry points, components, boundary state and data, and a route class per
  required behavior (X, S, none). The first call-chain map is the cross-component
  integration map of the T1 scenario, preceded by the amended component/indirect
  prerequisite packet1a below; family maps are cut from it and cite it,
  so no component is mapped before its integration context exists. Edges cite the retained call index or a
  function page and carry observed, inferred or unknown status as the atlas
  requires. A map supports route classification and batch enumeration only; it
  grades no outcome and does not turn internal mechanism into observable behavior.
- **Batch evidence packet.** One frozen manifest listing every harness call
  (slice sha256, address, inputs, stubs, harness source hash, timeout, result)
  and the grades it supports; one independent review covers the batch. Per-call
  evidence identity (revision 5) and the X label with its arm64 inference caveat
  (ADR 0003) are unchanged.
- **Standing authorization class.** Self-contained calls through the existing
  harness with recorded inputs and stubs. Anything that patches code, constructs
  original objects beyond the harness model or needs new tooling keeps per-run
  preparation and peer review.
- **Route ledger.** Per family, counts of required outcomes by route class. It
  is inventory, reported alongside the revision 9 numerator; it never closes an
  outcome.
- **Checks and pinning.** Checkpoint replays cover payloads changed since the
  last passing run, applying revision 8's rule to the mechanical checks; a full
  replay precedes a release. Successors pin the predecessor manifest hash rather
  than copying spec snapshots.

Completion rule confirmed by the user on2026-10-20: required behavior without
supporting evidence stays U and keeps family/product closure open. The
[ADR0005 confirmation](../decisions/adr-0005-full-live-specification-coverage.md#completion-rule-confirmation--2026-10-20)
owns this rule; a documentary inventory of unknowns grants no completion credit.
The formerly open disposition question is resolved in favor of the existing gate.
No denominator, seal rule, review requirement or execution authorization changes.

Amendment, 2026-10-20: a structure packet states the component layer it uses
(symbol clusters, vtables, type-name strings), the count of indirect call sites
with a resolved target at freeze, its hub-pruning rule and its search bounds;
every component edge carries its function-level evidence. The resolved count is
inventory reported alongside the route ledger and closes no outcome. See the
plan's [amendment](full-live-specification-plan.md#amendment--indirect-call-resolution-precedes-the-map-2026-10-20).

## Revision 12 — review-once batch adoption and authorization scope — 2026-10-21

Plan revision 4's [second amendment](full-live-specification-plan.md#second-amendment--batch-adoption-authorization-scope-and-x-count-ordering-2026-10-21)
measured nine hours of structure and batch work and found about 2,700 harness
calls with no adopted expectation, up to nine gate files per packet, and most
packets in families whose ledgers show no X route. This revision changes the
review and authorization forms so that evidence converts; it changes no
denominator, seal rule, closure gate or execution authorization.

- **Review once.** An observation is independently reviewed once, in its batch
  or structure packet. Later artifacts cite that review by manifest hash; they
  do not re-review the observation. A packet whose calls are all self-contained
  harness calls or static reads of retained bytes is one frozen manifest and
  one independent review; preflight, readiness, selection and receipt records
  are not created for it. The preparation and peer chain of revision 11 remains
  for patched code, original object construction beyond the harness model, or
  new tooling.
- **Batch adoption.** Approval of a batch review admits its observations into
  the owner's next revision: an agreement with the recorded oracle becomes that
  case's expectation with extracted-execution provenance; an evaluation without
  an oracle becomes the expectation of a new case with the same provenance and
  ADR 0003's arm64 inference caveat; a mismatch becomes a correction through
  the violated requirement. The owner-revision review covers only what the
  revision adds beyond the batch. Releases stay immutable and keep their review.
- **Ledger totals.** The route ledger of revision 11 is reported as totals
  across all family cuts (X, S, none) in every checkpoint, next to the
  resolved-indirect count; counts only, never a fraction. Under the confirmed
  completion rule a predicate without a route stays U and keeps closure open.
- **Yield ordering.** Batches and outside-scenario maps are selected by ledger
  X count; a family with no X route is not selectable for depth until a map
  revision adds one.


### Census schema qualification — 2026-10-21

The first amendment census did not read every required-unit schema. The corrected
32-family census passed independent review; its counts are
691 X, 1,076 S and 3,857 without a route. These are heterogeneous inventory units,
not an atomic behavior denominator. Analog's 199 X are predecessor-r1 context
under the approved v2 overlay, not current R2 admission. Selection must use the
reviewed per-family ledger and standing-harness eligibility; the amendment's
omitted schemas do not establish route absence. The [current checkpoint](full-live-specification-plan.md#current-execution-checkpoint)
owns the review disposition and corrected order. No authorization or closure rule
changes. Indirect resolution remains 25,071 baseline plus 24 conditional additions,
combined 25,095 of 268,015.

### Existing analyst artifact placement — 2026-10-21

Finite batch packets may use the already selected [G0.1 analyst store](native-analysis-recovery.md#existing-analyst-store-reuse-for-finite-batches--2026-10-21) through its existing repository link when checkout capacity does not cover full lifecycle artifacts. Packet manifests and receipts name exact lexical/resolved locations; packet-only checks stay within that resolved packet root. New pre-call code/input bindings, immutable final seals, sole actual reviews and owner-only mapping/preservation review apply identically. Normal artifact estimates include raw output, logs, custody, author/peer summaries and owner revisions, with concurrent headroom and recorded pre-child resource stop conditions. Estimates do not become reservations, per-file limits do not establish an aggregate bound, and a resource stop retains all partial evidence without replay. Existing evidence is not relocated or deleted. This adds no runtime model, provider/tool construction, release, implementation access or closure exception; current placement/selection belongs to the plan.

Placement clarification, 2026-10-21: large NEW peer summaries and staged owner proposals are evidence artifacts and may be created directly in the same existing analyst store (`full-spec-v1/reviews/` or sibling `owner-*` directories). Their reports retain exact lexical/resolved locations and standard repository citations through `r2-large`; owner-only checkers declare the checkout root separately from their artifact root. Small routing metadata and canonical spec Markdown remain in the checkout. Already sealed files retain their original locations and bytes. This uses the existing store; it adds no link, provider/model/tool or review gate.

## Revision 13 proposal — opaque return recording for unattempted Tension histories (2026-10-21)

**PROPOSED; NOT adopted or executable authorization.** The user has authorized continued whole-Live analyst execution, but this proposal changes the collector's frozen return-admission policy. Existing standing captures and owner reviews continue under revision12. No new native call, changed collector, retry or continuation is selected by this proposal.

The [partial batch review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/tension-stepped-controller-cells-v1-review.json) admits1388 observations, leaves one failed historyU and3960never-run historiesU. Its collector rejects a logged CalcA return other than0. The [retained-source conclusion](device-tension-dsp.md#calca-return-projection-and-retained-source-limits--2026-10-21) finds an analyst long-return cast and logging in the unchanged harness, without a vendor success/error contract. Retained ARM decompilation explicitly returns a conditional0/1 candidate; applicability and meaning for the failed x86 call remain unknown. Neither source justifies calling the value void/arbitrary, clipping or an error. Frozen failure bytes, source, guard and all published releases remain unchanged.

| Option | Execution and consequence |
| --- | --- |
| Keep zero-return admission | No changed collector. The failed history and3960unattempted histories remainU unless a separate supported route is selected. No new observations follow merely from this inventory. |
| Record opaque returns for only the never-run suffix (recommended) | One new prebound collector version and one frozen standing packet cover EXACTLY the3960unattempted IDs, without replaying the failed, successful or baseline histories. Parse each logged CalcA return as a signed64 integer projection through the existing analyst harness; preserve every value and run length without assigning success/error/flag meaning or requiring0/1. All exit, stderr, trap/fault, initializer, import-binding, event/parameter/order, frame/shape, output-flag, cxx, finite-unsigned-data, custody, timeout and resource guards stay enforced. First detected remaining guard failure stops later launches; retain partials/no retry. |

For the recommended option, native xdev/image/model/provider/FP, all129originaldecimal/f64setter words with index2 omitted, signed magnitude/sign pairing, On4096/Off26146/zeroinput/noWarm/TIME0/stopped transport/44100frames/block512 remain exact. This changes DATA admission, not the native binary, call construction or public API. It supplies no new vendor return ABI, success/error law, physical calibration, fitted metric or candidate criterion. A parser-valid retained report is not proof of native/public compatibility.

Before any new call the author must freeze all new source/parent/collector/checker/assembler/finalizer/context/scripts. Synthetic controls first accept mixed0/1 and signed64 extremes as opaque projections and reject malformed/overflow/duplicate/missing return fields, wrong run lengths, flags and other unchanged faults. The existing4GiB lifecycle+128MiB headroom estimate remains unreserved; a fresh parent snapshot and complete remaining raw+metadata/final floors must fit. The suffix has3960children/867240selecteddirectcalls/344520CalcA/1397088000rawstereo bytes before separate logged initializers/nested unknowns. No full native-call bound or storage reservation is claimed.

One independent actual/source reviewer reads ALL new source before the safe packet-only check and reviews the frozen suffix once. Its approved observations may enter the next owner directly; new owner wording/mapping/preservation review alone follows. Parent/resource/FDfsync/ABI/provider/FP/OS-exec/default/source/version qualifications remain explicit. The old failed return1 history remainsU and unnumbered; it is neither replayed nor repaired. Old1388observations and old0-return assertions keep their exact finite scope; original partial capture never becomes complete. All new priors/nativewaveform expectations/portablecriteria/grades remainNULL/applicationFalse. Required unsupported behavior staysU/whole-productOPEN.

Decision pending user review of this concrete proposal. No design commit is selected in this shared analyst checkout.

### User-adopted revision 13 decision — 2026-10-21

**USER ADOPTED.** The user explicitly approved the proposed opaque-return recording option. The preceding PROPOSED notice, alternatives and pending-decision sentence are preserved as the historical proposal; this decision supplies their current disposition. Adoption applies only to a new, pre-call-bound packet containing exactly the 3960 previously unlaunched Tension stepped-control histories, under the unchanged admitted native xdev/image/model/provider/FP and literal input context. The 1388 accepted observations, failed U1389 and qualified baseline are excluded from new calls. Their frozen source, return-zero guard, partial status and U/accepted dispositions remain immutable.

The sole policy delta is to record every CalcA return as the analyst harness's signed 64-bit opaque integer projection with exact run lengths, without requiring zero or a 0/1 domain and without assigning success, error, clipping, void, arbitrary-value or output-flag meaning. All other admission guards in the proposal remain enforced. New code/parent/collector/checker/assembler/finalizer/context/scripts must bind before once-only originals; first remaining guard failure stops later launches, retains partials and allows no retry. Native ABI/type/return-cause, public/ARM behavior, physical calibration and portable criteria remain unknown.

The full approved resource contract remains **4 GiB lifecycle plus 128 MiB headroom**, unreserved. A fresh parent snapshot and complete remaining-output/metadata/final floors must fit before originals and each launch. INPUT preparation does not reserve storage or authorize a smaller budget, deletion, relocation, new link, split packet or replay. The selected suffix has 3960 histories, 867240 selected exports, 344520 CalcA projections and 1397088000 raw stereo bytes, with initializer/nested work separate. Current execution selection and capacity observations belong to the plan and canonical Tension research; this design adoption alone does not certify a capture or observation.

One sole independent actual/source review must read all new source before the safe owned-data check; no duplicate actual review follows its approval. New owner wording/IDs/mapping/preservation is reviewed separately using only the approved summary. All fresh priors/native waveform expectations/portable criteria/grades remain NULL and application proof false. Required unsupported behavior stays U and whole-Live coverage OPEN.

## Revision 14 — reference observation evidence — 2026-10-21

[ADR 0006](../decisions/adr-0006-reference-observation-reopened.md) reopens whole-application observation of the
pinned build as evidence route O. This revision adds the evidence form; it
changes no denominator, seal rule, closure gate or adoption rule, and it is
independent of the revision 13 proposal above.

- **Label O (observed).** A value observed on the running reference application
  on a recorded host. It joins D, S and X. An O value is never derived from S or
  X and never replaces a retained S or X value; a disagreement between O and S
  or X is an open question on the owner, with both results preserved.
- **Observation packet.** One sitting is one frozen manifest: for each record
  the ADR 0002 escalation fields, the host and Live build identity, the input
  document and media hashes, the procedure as run, the raw capture hashes and
  the observed value or an explicit "not observed" with its reason. One
  independent review covers the sitting. Approval admits observed values into
  owners' next revisions under revision 12's adoption rule. Raw captures stay
  analyst-only; released cases carry the observed value with provenance O and
  the host identity.
- **Route class O.** Ledgers carry X, S, O and none; a unit with no X or S route
  is O-pending until an observation packet records it, and the totals reported
  under revision 12 state all four classes. O-pending is inventory, not
  evidence.
- **Host record.** No observation packet exists without the D-07 host record
  (machine, OS build, Live build hash, account isolation and authorization,
  evidence copy route). The record is a prerequisite, not evidence.

### Local virtualization host selection — 2026-10-22

The [recorded D-07 direction](../decisions/adr-0006-reference-observation-reopened.md#d-07-host-choice-local-virtualization--2026-10-22) chooses local virtualization, with readiness fields still open. This is a host-path decision authorizing setup, not an observed value. Distinguish physical-host identity, guest/hypervisor configuration, guest OS/build, exact Live executable/platform, authorization/isolation and evidence copy. Another platform's Live build requires its own provenance/profile and does not silently replace the pinned macOS source. Current X evidence/models and immutable releases stay unchanged. No O evidence or grade is admitted before the completed guest record and reviewed sitting.

#### Windows observation profile — 2026-10-22

D-07's [Windows guest choice](../decisions/adr-0006-reference-observation-reopened.md#windows-guest-profile-selected--2026-10-22) creates a distinct Windows/VM/build observation profile. Retain platform applicability explicitly: generic user scenarios may yield bounded Windows observations, while macOS/CoreAudio/AudioUnit/arm64/FP/timing associations require their own evidence. No presumed cross-platform identity, new denominator, grade or silent replacement of the pinned macOS source follows. The exact guest/executable/configuration/auth/copy record precedes the first observation packet.


#### Unactivated Windows capture profile — 2026-10-23

[D-07’s user-adopted profile](../decisions/adr-0006-reference-observation-reopened.md#unactivated-windows-profile-adopted--2026-10-23) is Windows11Pro installed withoutproductkey/notactivated. Windows activation/key is not a setup or observation prerequisite; record actual state as host metadata at Session0. Record watermark visibility/location in raw screen captures and lockedpersonalization as accepted expected guest conditions, not Live behavior. The declared profile is not evidence of an already installed guest. [The later D-07 supplied-media/guest-verification record](../decisions/adr-0006-reference-observation-reopened.md#live-media-supplied-windows-and-installed-live-identities-observed--2026-10-23) completes user boot-media inputs and binds the observedWindows11Pro26H2/signedLive12.4.3 profile. [The observed offline profile](../decisions/adr-0006-reference-observation-reopened.md#offline-profile-copy-route-and-hardware-code-observed--2026-10-23) adds guest EthernetDown, readonlyinput/writableexport private copies, and an exact32-byte export probe through normal guest eject/backend closure and same-image reattachment. This additive scoped copy method preserves the old frozen whole-VM-shutdown proposal. Actual hardware code is sent; user-fetched.auz file/path is pending, with no account credentials in guest/chat. Keep virtual hardware unchanged while awaiting AUZ. Live Save/ExportDisabled and audioengineOFF remain observed; authorization/capture/audio/MIDI/CPU/tool-version/input admission and the reviewed O sitting remain separate.


## Revision 15 proposal — opaque returns for two remaining declared device classes (2026-10-22)

**PROPOSED; NOT ADOPTED OR EXECUTABLE AUTHORIZATION.** D-08 is a new collector-policy decision. [User-adopted revision13](#user-adopted-revision-13-decision--2026-10-21) remains confined to its3960Tension stepped-control suffix. Current packets retain their frozen strictret0guards; this proposal changes no existing bytes, dispositions or release. Current scheduling and eventual exact remaining sets belong to the plan/canonical owners.

The [sole Electric12partial review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/electric-declared-protocol-unlaunched12-v1-partial-review.json) admits one activity_empty observation, rejects startup_0 under strictret0, and leaves ten startup histories unlaunched. The earlier activity_note failure remainsU. Literal ret1 with legalflag1 is a recorded guard violation, not proof of native success/error, benignness or a vendor return ABI. The Tension981 corrected-recorder packet is being sealed for its sole review; author counters are not evidence or policy authorization. Its exact unlaunched set must be established by that review before this proposal can select any Tension call.

| Option | Consequence |
| --- | --- |
| Keep zero-return admission | Preserve current collectors. Further eligible work may use the unchanged policy; remaining histories stayU until supported evidence. No opaque policy follows. |
| Record opaque returns for only the remaining two declared classes (recommended) | After explicit user adoption and the required sole partial reviews, one new prebound packet per family records every CalcA return as the analyst harness's signed64integer projection/RLE, without requiring0 or0/1 or assigning meaning. All other guards remain. Previously launched histories are excluded permanently from this selection. |

The second option is bounded to **Electric's ten startup members1024/2048/3072/4096/4224/4352/4400/4480/5000/11264** and **only the still-native-unlaunched members of Tension's981literal-script/985alias quantization class** as established by its corrected-recorder sole partial review. It excludes every child previously launched in either class, all earlier successes, both Electric failed histories, any new Tension failed history, baseline/old aliases, sine inputs, other device families and arbitrary parameter crossproducts. The final Tension ID/script/alias set and counts must be copied from the approved partial summary before a new call; if the whole remaining set cannot be bound/admitted, launch none. No old packet becomes complete and no failed original is replayed or repaired.

The sole DATA-policy delta parses and retains every signed64projection in[-9223372036854775808,9223372036854775807] with exact order/run lengths, assigning no success/error/void/clipping/flag/nativeABI meaning. Preserve all output flags0/1 and every existing exit/status/stderr/trap/fault/initializer/import-binding-versus-counted-use/CXX/input/parameter/event/order/frame/shape/unsigned-finite/channel/custody/timeout/resource/cleanup guard. First remaining fault stops future children, retaining failed/unattemptedU without retry. Opaque recording admits only a finite observation under recorded premises, not native/public correctness, a portable oracle or criterion.

Native xdev/image/model/provider/default-entryFP, literal decimal/f64/f32 words, source-event/warm/reset/rate/context order and Linux/source-version/OSexec qualifications remain unchanged. No new construction, build/patch/tool/provider, producer/helper/estimator execution, fitted metric or physical calibration. The earlier3960opaque packet supplies a reviewed recording precedent by citation only; it proves no native return contract for these classes. New collectors must establish their own compatibility and DATA controls, not infer applicability from that precedent.

Before any original, fully inert-read and freeze all new recording/control/checker/parent/assembler/finalizer/context/catalog/scripts. Controls must accept mixed0/1 and signed64extremes as opaque DATA and reject malformed/overflow/missing/duplicate fields, wrong run lengths, illegal flags and all unchanged protocol faults; retain positive runtime-schema and wrong lexical/resolvedpath/size/hash checks. Existing full unreserved resource contracts remain: **Electric1GiB+128MiB=1207959552B; Tension4GiB+128MiB=4429185024B**, with fresh fullremainingraw/futuremetadata/finalfloor/headroom before each child and unchanged child bounds. No storage deletion/move/split/budget reduction or provider mutation.

One frozen standing packet and one sole independent actual/source review per family; later owner review covers only new wording/IDs/mapping/preservation. No additional readiness gate. All new waveform priors/native expectations/portable expected/comparators/grades NULL/applicationfalse. FDfsync versus directory/crash durability, custody endpoints versus continuous provider/FP/OSexec, initializer/nested work and ARM/public applicability remain qualified. Unsupported required behavior staysU and whole-Live coverageOPEN. No implementation, release, observedO or closure credit follows. D-08 remains pending user decision; no new opaque collector or native call is selected here.
## User-adopted revision 15 decision — 2026-10-23

**USER ADOPTED.** The user explicitly approved opaque-return recording for the **771unlaunched Tensionquantization scripts and10Electricstartup histories**, retaining every other guard and excluding every previously launched/failed history. This decision supplies the disposition of the historical PROPOSED section above; it does not rewrite that proposal, design13's separate3960scope, old source/guards/failures or releases.

The exact scope is the [sole-summary remaining-set binding](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/design15-exact-unlaunched-remainders-binding.json),365520B/SHA256 `7d5f92b3bf23ecbb63b8b581b92d67c3c909699ca335068e072d620e965a1c57`: **781scripts/785aliases**, Tension771/775 and Electric10/10. Its authorities are the sole corrected-Tension981partial REPORT and sole Electric12partial REPORT. All210previously launched Tensionmembers, bothfailed Electric histories and every previously launched Electricmember/otherfamily/baseline stay excluded. Frozen original/partial/as-of/owner records retain their exact scope; no failed native original is replayed or retrospectively accepted.

Only the new collectors' CalcA return-admission policy changes: retain every logged signed64integer projection with exact values/order/run lengths, without requiring0 or0/1 or assigning success/error/benignness/void/clipping/flag/nativeABI meaning. All outputflag0/1 and exit/stderr/trap/fault/initializer/importbinding/CXX/INPUT/order/frames/shape/unsignedfinite/channel/custody/timeout/resource/cleanup guards remain. Native xdev/image/model/provider/defaultentryFP, literal words/events/warm/rate/context and all source/runtime/OSexec/publicARM qualifications stay unchanged. No new constructor/build/patch/tool/provider/inputgenerator/metric/oracle/physical calibration.

Each family gets one NEW pre-call-bound standing packet. Fully inert-read/freeze all new parent/collector/checker/assembler/finalizer/control/context/catalog/scripts before once-only originals. Synthetic controls accept mixed0/1/signed64extremes as opaqueDATA and reject malformed/overflow/missing/duplicate returns, wrongRLE/flags and every unchanged fault; retain runtimeidentityschema positives/wrong lexical/resolvedpath/size/hash checks. Fresh complete unreserved floors remain Tension4GiB+128MiB4429185024B and Electric1GiB+128MiB1207959552B, including remaining raw/futurelogsmetadata/final-review-owner/headroom before every child. No deletion/move/split/reducedbudget/provider mutation. First remaining fault stops futurechildren, retaining full failed/unlaunchedU without retry.

One sole independent actual/source review per family after immutable final seal; approval admits finite observations into the next owner, whose separate peer reviews only new wording/IDs/mapping/preservation. No extra readiness gate/second actualproof. FullFDfsync-versus-crashdurability/source/build/default/FP/provider/ABI/OSexec/initializer/nestedcall/resource limits remain explicit. All new waveformpriors/nativeexpectations/portableexpected/comparators/grades NULL/applicationfalse. Unsupported required behavior staysU/wholeLiveOPEN; no release, implementation, observedO or closure credit follows. Current selection/scheduling belongs to the plan/canonical owners, not this durable contract.


## Revision15 bounded execution outcome — 2026-10-23

The exact user-adopted scope now has sole actual approval and reviewed owner adoption: [TensionR14’s771histories/775aliases](device-tension-dsp.md#tension-owner-r14-opaque-quantization-annex-adoption--2026-10-23) and [ElectricR14’s tenstartup histories](device-electric-dsp.md#electric-owner-r14-startup-annex-adoption--2026-10-23). Every other guard and every previously launched/failed history remains unchanged. Opaque signed64 recording assigns no ABI/domain/success/flag meaning, public law or portable criterion. This outcome completes only D-08’s exact781scripts/785aliases; required unknowns keep whole-Live coverage OPEN. The selected later Electric dynamic-Polyphony class retains strict return0/flag0or1; revision15 does not transfer to it.


## Revision 16 proposal — opaque returns for four unlaunched Analog count histories (2026-10-23)

**PROPOSED; pending sole DATA-policy review and explicit user decision D-09. No collector change or native call is authorized by this proposal.** Revision15’s exact781-script decision is complete and does not extend to Analog. The [sole five-count partial](device-analog-dsp.md#five-count-remainder-partial-actual-adoption--2026-10-22) retained failed p05 with zero accepted observations and four unattempted members. Earlier p00–03 observations and failed p04 remain unchanged. Conditional recovered return construction supplies no native return ABI, success/error or benignness claim.

The proposed scope is exactly **ANALOG-COUNT-p06/p07/p08/p09**, the four members labeled UNATTEMPTED-U in the approved partial REPORT. The [exact sole-summary INPUT binding](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/design16-exact-analog-unlaunched-four-binding.json),119635bytes / SHA256 `2e70c511e86864ec96b255751389388acac20a69bf1e229bdc82324b17a64800`, copies every whole203-word vector, literal script, source event order, fixed context and admitted model metadata without changing historical guard labels. Its authority is361075bytes / SHA256 `7f933a3b796b4c3c62fb6f204e1aadeef6a0548db794c9178a7768831d3bf383`. The four-script planning totals are1652direct selected exports/828CalcA/3380800stereo raw bytes; these are projections, not observations or all nested work. They do not establish global never-run absence beyond the bounded sole-reported history.

| Option | Consequence |
| --- | --- |
| Keep current strict zero-return admission | No new policy. The four unattempted histories remain U until eligible evidence supports them. |
| Record opaque returns for only these four histories (recommended) | After sole DATA-policy review and explicit user adoption, one new prebound standing packet records signed64 CalcA return projections in order/RLE without requiring zero. Every other guard remains. |

The only proposed policy change is to retain all logged integer projections in[-9223372036854775808,9223372036854775807] as opaque values with exact order and run lengths. It assigns no success/error/void/clipping/flag/domain/nativeABI meaning. Output flags0or1, exit/status/stderr/trap/fault/initializer/import-binding-versus-counted-use/CXX/INPUT/203parameter/event/order/frame/shape/unsigned-finite/channel/custody/timeout/resource/cleanup guards stay exact. Previously launched p00–05 and all other histories/families are excluded; neither failed p04 nor p05 is replayed, reclassified or repaired. First remaining fault stops future children without retry and leaves failed/unlaunched U. All four exact inputs must be admitted before any call, otherwise launch none; no shortened or substituted count sequence.

Existing xdev149608bytes/SHA256 `3eec4ad1cfa0765c9e8267806cf02b7e664a07157043e3a170388cfa4d63cf14`, image/slice/import/default-entryFP/environment premises, literal words, rate44100/block512/process105650/event/input/context order remain unchanged and qualified. No rebuild, patch, new model/provider/tool/FP/construction, original producer/helper/module/NumPy/estimator execution, output prediction, calibration, metric or portable criterion. The old supplied-context strict-return text remains historical INPUT metadata; new recording policy must be a separate field, never a silent input-hash edit.

Before any native call, fully inert-read/prebind/freeze every new collector, parent, context, catalog/script, assembler/finalizer/checker/control source and all four inputs. Meaningful synthetic controls must accept mixed values and signed64 extremes as opaque DATA and reject overflow/malformed/missing/duplicate fields/wrong RLE/illegal flags and every unchanged protocol fault, with runtime-schema positives and wrong lexical/resolved-path/size/hash negatives. Retain Analog’s full **128MiB lifecycle+128MiB headroom=268435456bytes** unreserved parent and per-child floor, with exact full remaining raw, future logs/metadata, final review/owner and concurrent complete packet budgets. Preserve existing per-child CPU/wall20s, core0 and file-size limits; the earlier partial’s parent had no separate watchdog, so do not describe a parent bound that is absent. No deletion, movement, splitting or reduced budget.

One frozen standing packet gets one sole independent actual/source review; later owner review covers only new wording, IDs, mapping and preservation, without a second actual proof or extra readiness gate. Waveform priors/native expectations/portable expected/comparator/grade stay NULL/applicationfalse. Endpoint custody is not continuous provider/FP/OS-execution or source-to-compiled proof; FDfsync is not crash/directory durability; initializer versus nested work and public ARM behavior remain qualified. This proposal grants no release, implementation, O observation, compatibility grade or whole-product closure. Unsupported required behavior stays U and whole-Live coverage OPEN.
## Revision 16 DATA-policy review — 2026-10-23

[Mix’s sole NEW DATA-policy review](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/design16-analog-unlaunched-four-data-policy-v1-review.json),153198bytes / SHA256 `34197e872b61b2e1e25f00dd1940ab423052472cb7fbe268b57ded82c8d838f4`, APPROVES the proposal pending explicit user adoption, CLEAR with no blockers or corrections. The reviewed proposal section SHA256 is `ce691335946dfd360115b926f8f63d765eb557f7bb37603961cafddc81941a7a`; the immutable119635byte binding remains unchanged. All four selected records exactly equal sole-reported UNATTEMPTED-U p06–09, including full203word arrays, scripts,36event sequences and shared model/context metadata. Twenty-two independent mutations and mixed/extreme signed64 DATA positives passed. Allpreviously launched p00–05 remain excluded, every other guard/full268435456byte floor retained and the absent parent watchdog explicitly qualified. Review performs no runtime reservation or native selection and establishes no return meaning/ABI, current provider/FP/OS execution or compatibility.

The explicit user decision has been requested. **D-09 remains pending; no new collector or native call is selected.** Root authored the proposal/binding; Mix reviewed only new policy/INPUT binding and prior sole REPORT metadata, without a second actual/source/raw/provider proof review. The independent Tension and Corpus work continues.


## User-adopted revision 16 decision — 2026-10-23

**USER ADOPTED.** The user approved opaque-return recording for exactly Analog’s four sole-reported unattempted count histories **ANALOG-COUNT-p06/p07/p08/p09**, retaining every other guard and excluding failed p04/p05 and every previously launched p00–05 history. This decision supplies the disposition of the historical proposal and its sole DATA-policy review; neither frozen proposal/binding nor old source/guard/failure/owner/release is rewritten.

The exact119635byte binding/SHA256 `2e70c511e86864ec96b255751389388acac20a69bf1e229bdc82324b17a64800` retains full203word arrays, events, literal scripts and model/context metadata; sole review153198bytes/SHA256 `34197e872b61b2e1e25f00dd1940ab423052472cb7fbe268b57ded82c8d838f4` is the independent DATA-policy authority. Only the NEW collector’s CalcA return policy changes to retain every logged signed64 integer projection in exact order/RLE, without requiring zero or assigning meaning/ABI/domain/success/error/benignness. Historical strict-return INPUT labels stay exact, with new recording policy separate. Flags0or1 and all other protocol/input/resource/custody/cleanup/timeout guards remain exact. No transfer to another class follows.

One new standing packet must admit all four exact inputs before any native call, with full new code/catalog/context/scripts inert-read, controlled and prebound. Full268435456byte unreserved parent/per-child floor includes all remaining raw, future logs/metadata, final review/owner and concurrent complete packet budgets. Existing child20sCPU/wall/core0/file-size limits stay exact; absent parent watchdog remains qualified. No storage deletion/movement/splitting/reduced budget or native model/provider/tool/FP/construction change. Previously launched/failed histories stay excluded and unreplayed. First new fault stops future children with failed/unattempted U and no retry. One sole actual/source peer after frozen final seal, then separate new owner wording/ID/map/preservation review only. No extra readiness gate or repeated old proof. New waveform expectations/portable criteria/comparators/grades remain NULL/applicationfalse, all current execution/ABI/FP/provider/OS/publicARM limits remain explicit and unsupported required behavior stays U/whole-Live OPEN. Scheduling belongs to the plan/canonical owner.


## Revision16 bounded execution outcome — 2026-10-23

The exact user-adopted four-history scope now has [sole actual approval and reviewed AnalogR14owner adoption](device-analog-dsp.md#analog-owner-r14-four-count-annex-adoption--2026-10-23):fourp06–09/DAN1194–1197. Allotherguards and allpriorp00–05/failedp04-p05 remain unchanged and unreplayed. Only new signed64opaque return recording changed; literal638zero/190one assigns no ABI/domain/meaning/public law or portable criterion. This completes only D09’s exactfour scope, not Analog or whole-Live coverage. Tension’s new timing class remains strict return0/flag0or1 without policy transfer; required unknowns/productOPEN/O0/releases persist.

## Standing-harness supplied-input qualification — 2026-10-23

The coordinator selected [a new owned Electric sine stimulus and complete input-flag pair](device-electric-dsp.md#current-supplied-sine-input-flag-pair-selected--2026-10-23) under revision12. This is a routine INPUT selection within the existing harness: no patched code, original object construction beyond that model, new tooling, provider change, FP treatment or recording-guard change. The existing review-once authorization therefore applies; this is not a new opaque-return policy or an amendment to user16.

New provided input bytes are explicitly distinguished from the absent historical artifact and the original producer. Existing standard-library stimulus generation records its own recipe/version/rounding/custody limits, without claiming NumPy, historical file or executed-source equivalence. The original missing-file cases remain unknown; only the separately bound current supplied contexts may receive finite observation IDs after sole review and owner adoption. Exact experiment inputs, resources, author/peer roles and limits belong to the canonical Electric selection. No whole-application O or completion credit follows.

## Revision 17 proposal — opaque returns for333 retained unattempted members (2026-10-23)

**PROPOSED, pending sole DATA-policy review and explicit user decision D-10. No collector change or native call is authorized.** User13/15/16 decisions remain confined to their earlier exact sets. The newly sole-reviewed Analog469 partial admitted161 observations and left failedAPCS0162 plus307unattempted; earlier Tension remaining-check partial left24unattempted after failedTRCS0738, and Collision’s suffix left two unattempted after failed125. All strict failures and historical dispositions remain unknown and unreplayed.

The exact policy-membership authority is [the consolidated metadata nomination](../../analysis/ableton-live-12.4.3/r2-large/full-spec-v1/reviews/analog307-tension24-collision2-unlaunched-context-metadata-nomination-v1.json),586528bytes/SHA256 `24133545e2f49e09d8d4e729f7d9f04d9a5b8708e5bb948edf14ae185cd90ce4`. Its separate full333-member disposition list and detailed immutable INPUT-context digests/pointers bind **Analog307 members/316aliases, Tension24 members/24aliases, Collision MCI-001-126 and MCI-001-127 with their original explicit alias lists**. These are retained records across three namespaces, not333 newly proven eligible/unique/missing native histories. Those three counts remain NULL; cross-family deduplication is not claimed. All nine omitted-input Analog contexts/sixteen aliases are in the unattempted set, with only their existing conditional initial-input SOURCE/model premise. The metadata authority is not a new input reconstruction, fresh capacity statement or native acceptance proof.

| Option | Consequence |
| --- | --- |
| Keep strict zero-return recording | No policy change; all333 remain unknown until supported evidence is obtained under that rule. |
| Record opaque returns for exactly these333 retained members (recommended) | After sole review and explicit adoption, separately bind each whole family class to its existing admitted context and record signed64 CalcA return projections without requiring zero. All other guards remain. |

Only the new packet’s CalcA return guard changes: retain exact signed64 integers in[-9223372036854775808,9223372036854775807] with full order/run lengths as opaque DATA. No value is interpreted as success/error/void/benignness, a return domain, ABI, output law or public behavior. Historical strict-return fields and hashes remain exact; a separate new recording-policy field records this decision. No previous accepted or failed history is replayed, repaired or reclassified: all162 attempted Analog histories includingAPCS0162, all738 attempted Tension histories includingTRCS0738, Collision failed124/125 and every other known attempted/reference history are excluded. No opaque policy transfers to the independently selected strict Tension29 BRIGHT histories or any other class.

Every unchanged guard remains: flags0or1, exact process/RLE/frame/shape, signed/unsigned lexical/range checks, exit/status/stderr/trap/fault/CXX, initialization/import-binding versus counted use, full array/script/event/parameter/default/omission/context ordering, finite raw validation, custody/resources/timeouts/cleanup. Equality/nonzero/quiet/hash facts remain descriptive, with no productivity requirement or inferred waveform expectation. First remaining fault stops later children, preserving failed and unattempted U with no retry or automatic continuation. The policy does not cure any INPUT/admission/dependency gap. Before selecting a family’s native run, bind every member of its exact whole class against all then-current approved attempted/reference cuts, retaining aliases and all construction/model/provider/FP/source/current-consumption qualifications; if any member lacks admission, launch none of that class and record the gap, without substituting or shortening the class. Exact execution counts/resources belong to that subsequent concrete binding, not this333-record policy nomination.

Keep the already admitted executable/image/slice/model/constructor/provider/environment/default-entry-FP and all original bytes and omissions unchanged. No rebuild/patch/new tooling/model/provider/FP treatment, original producer/helper/module/NumPy/estimator execution, arbitrary parameter crossproduct, output prediction/formula/calibration/metric/portable criterion. Native initializer entries remain separate from selected exports and unknown nested work; source-to-compiled and current runtime/public ARM joins remain unknown.

Fully inert-read/control/prebind every new collector/parent/context/INPUT/assembler/finalizer/checker before one run per selected family. Synthetic controls must accept mixed signed64 values/extremes as opaque and reject overflow/malformed/missing/duplicate/incorrect run geometry/illegal flags and every unchanged fault. Preserve at least the complete latest family requirements: **Analog6991975856bytes; Tension4429185024floor+268435456concurrent=4697620480bytes; Collision671088640floor+268435456concurrent=939524096bytes**, or any larger complete current lifecycle projection. Fresh parent/everychild guards include actual-owned growth, all remaining raw, future worst8MiBstdout-stderr/adequate4MiBmetadata per child, full final review/owner, headroom and concurrent allowances. No storage move/delete/splitting/budget reduction. These remain unreserved estimates, without quotas, external-writer/escaped-descendant/within-child-finalization protection. Existing20sCPU/wall/core0/file bounds are child-only; absent parent watchdog stays explicit. Old endpoint/fsync/privacy and crash-durability qualifications remain exact.

One frozen family packet gets one sole independent actual/source review; its next owner gets only a NEW wording/ID/mapping/preservation review. No second actual proof, old proof replay or added readiness gate. New waveform priors/portable expected/comparator/grade remain NULL/applicationfalse. No release, implementation, O observation, compatibility percentage or whole-Live closure follows. Required unsupported behavior remains U and whole-product coverage OPEN. The current plan owns scheduling; this proposal selects no native continuation.

## Revision17 disposition — parked by user steering,2026-10-23

The user-directed Claude steering explicitly requires a new user decision before any opaque-return standing packet beyond adoptedD08/D09, and selects S work in ledger order after the currently selected X classes drain. Root parks the above unadopted proposal and its333-member metadata nomination: no DATA-policy review/question, collector change, new standing packet or native continuation is selected. The frozen6206byte proposal/SHA256 `62fe0354caedf34059ea13cdb1173b18921d607e63cab7282124cc4ef8f0bf9b` remains an unadopted historical proposal. D10 has no decision; all333 remain U, without transferring earlier approvals. Current strictTension29 execution and AnalogR15new-owner review continue independently. A future new user decision would require a concrete scope at that time, not inference from this nomination.

The same user steering selects one preparation packet for all137remaining Phase4 records in sessionsB–Q and a Session0Windows tool/version-record checklist, with no guest boot/install and one sole review. Applicability preparation is not an O observation, Windows/macOS equivalence or evidence that a tool is installed. See the [canonical preparation selection](phase4-probe-batch.md#remaining137-windows-triage-preparation-selected--2026-10-23).


[Latest D-07 coordination](../decisions/adr-0006-reference-observation-reopened.md#guest-operations-assigned-to-claude-concurrent-interaction-held--2026-10-23) assigns Claude guestboot/OSLiveinstallation; Root/workers hold QEMUlaunch, guest-v1 modification and all guest/QMP/UI/media/profile/AUZ interaction until its completion report. Earlier raw guest/software/copy/hardwarecode findings remain ASOF; no unchanged final profile or matching code is inferred. Readonly inventory commands were never launched; frozen focus-only partial adds no tool/capture capability. Static work continues; reviewedO0 and wholeLiveOPEN unchanged.


[Analog expanded native adoption](device-analog-dsp.md#expanded49-native-study-adopted-local-chains-and-complete-frontier--2026-10-23) carries21qualified local groups and the complete remaining dependency nomination, with no runtime/public/ABI/numerical/site-grade claim. The [next metadata cohort](device-analog-dsp.md#complete6415524-locator-cohort-selected--2026-10-23) follows the current S selection: all64destinations/155points/24sites/sixloadfields, one frozen packet/sole peer and RootCITEONLY. Existing inventory denominators, unknowns and closure rules remain unchanged; no further opaque-return scope or guest interaction is selected.


The [complete64locator metadata adoption](device-analog-dsp.md#complete64-locator-metadata-adopted-66-declarations-and-qualified-hint--2026-10-23) and [next complete66/67fragment native selection](device-analog-dsp.md#complete6667fragment-native-cohort-selected--2026-10-23) advance the existing S queue, preserving both gaps, runtime/object unknowns, one sole peer and RootCITEONLY. The newly encountered static hint authorizes only an explicitly selected target-locator lookup in the same packet, no target-body or automatic follow. [Primary-source Session0 methods](phase4-probe-batch.md#session0-capability-methods-primary-source-followup-adopted--2026-10-23) qualify future CPU/audio/video/MIDI measurements without a new approval/completeness gate, guest execution or readiness claim. Existing scope/denominators/opaquereturn limits and Claude guesthold remain unchanged; no new behavioral case, grade, site, O or closure.


[Complete66native adoption](device-analog-dsp.md#complete66-native-study-adopted-27-qualified-groups-and-cache-history--2026-10-23) preserves its27qualified groups, two return-identity refinements and failed peer cache-inspection history without bytecode-equivalence/runtime/grade proof. The [next combined63frontier/dispatch cohort](device-analog-dsp.md#complete63-frontier-and-known-dispatch-leg-selected--2026-10-23) groups the complete metadata frontier with the already admitted168-byte target body/112file-field bytes, under one freeze/sole peer and full unchanged budgets. New63destination/point/hint bodies and virtual/pointee prefixes remain unselected; raw candidates stay distinct from addresses/objects. Existing route/source denominators, case/release/site counts, unknown/closure and opaque-return limits remain unchanged.


The [combined frontier/dispatch cohort is adopted](device-analog-dsp.md#complete63-frontier-and-dispatch-adopted--2026-10-23); [complete67 native work](device-analog-dsp.md#complete67-native-frontier-selected--2026-10-23) is the current S selection. Host-only Windows archive/media preparation follows the [Phase4 record](phase4-probe-batch.md#host-only-tools-and-calibration-transfer-selected-and-adopted--2026-10-23). The existing one-packet/one-sole-review rule continues; no opaque-return, guest-operation or closure rule changes.


[Complete67 native findings](device-analog-dsp.md#complete67-native-study-adopted-with-two-semantic-refinements--2026-10-23) are adopted with two semantic refinements and retained author/resource history. [The next combined59 cohort](device-analog-dsp.md#complete59-frontier-and-admitted-dispatch-legs-selected--2026-10-23) selects the whole metadata frontier and only already admitted unread content, with full current concurrency from the first point. One freeze/sole review and Root citation-only remain; no opaque-scope, behavior or closure rule changes.


[The complete59 capacity stop](device-analog-dsp.md#complete59-resource-admission-gap-no-original-acquisition--2026-10-23) preserves the selected whole cohort and full allowances; its conservative bound is not a minimum actual requirement. No budget reduction or additional original-analysis approval gate follows. Independent next-family assessment may continue while capacity and Claude guest handoff are pending; no unknown is promoted or completion rule changed.


The [Automation whole caller frontier metadata selection](automation-envelopes.md#whole-immediate-m-caller-frontier-metadata-selected--2026-10-23) uses the existing one-packet/sole-peer rule and strict architecture attribution. Geometry unknowns permit a finite metadata census, never content or a guessed runtime binding. Full current resource terms are derived before original metadata reads; no budget reduction, opaque scope, grade or closure rule changes.


[One bounded Clip metadata-reader recovery](clip-launch.md#locator-reader-failure-retained-one-bounded-metadata-recovery-selected--2026-10-23) is explicitly selected after a typed external-entry handling bug. This instance amends Root’s own no-reader-retry execution choice while preserving the failed frozen packet, new-code controls/binding/full budget and sole review. It authorizes no failed original function/audio history, reference-process, provider/model or opaque-return retry, and creates no general standing retry policy or automatic third attempt. Geometry/behavior staysunknown until a separate successful approved result supports it.


The [Automationdependency native/hint cohort](automation-envelopes.md#whole-dependency-class-native-and-unread-hint-study-selected--2026-10-23) and [wholeACliphook native question](clip-launch.md#whole-aclip-post-load-native-declaration-selected--2026-10-23) follow sole metadata approval. Full class accounting excludes already-read overlaps by citation, retains architecture/public gaps and PREeligibility/currentconcurrency from the first point, with one finalfreeze/solepeer and RootCITEONLY. The original Clipfailure and recoveryclassifierU remainhistory, no original/audio history retry or broader opaque policy. Analog59remainswhole/capacity-pending; no behavioral/site/O/release/closure milestone advances.


[Automation’s first owned decoder toy stopped before original acquisition](automation-envelopes.md#pre-original-owned-toy-limit-failure-native-v2-selected--2026-10-23) on an inherited CPU-limit conflict. The failed v1is preserved, and one separately bound v2analysis-tool correction retains the entire class, budgets and unknowns before the first image/index read. This narrow Root-selected owned-tool recovery changes no user reference/X/audio-history retry permission or opaque policy; no behavior/release milestone advances.


The [owned raw-loader diagnostic](automation-envelopes.md#owned-raw-loader-diagnostic-first-original-scope-unchanged--2026-10-23) changes one prospective analysis-tool flag, using a retained failing owned test and one explicit diagnostic; it preserves all outputs and strict stderr guards, never reference/X/audio retry authority. The [whole MNS-053metadata class](midi-note-storage.md#all-four-mns-053-frontier-metadata-selected--2026-10-23) retains allfourvariants and treats slots as offsets/unknown providers, with onefreeze/solepeer/fullcurrentbudget and RootCITEONLY. No new closure or opaque policy is introduced.


[Whole AClip hook findings are adopted](clip-launch.md#whole-aclip-hook-native-findings-adopted--2026-10-23) as conditional local evidence only. [Automationv2 remains an unreviewed partial with a post-stop protocol breach](automation-envelopes.md#native-v2-partial-capture-and-protocol-breach-retained--2026-10-23); its explicitly selected owned344B diagnostic/static-tool recovery remains conditional and capacity-held. [Shared filesystem capacity](native-analysis-recovery.md#shared-filesystem-capacity-stop--2026-10-23) holds all new captures/diagnostics/checker-seals, including MNSprebinding, without smaller budgets/contracts or deleted evidence. One sole review, whole-class accounting, opaque limits and user-controlled guest handoff/closure rules remain unchanged.


[Host capacity was revalidated after user-directed cleanup](native-analysis-recovery.md#user-directed-disposable-cleanup-and-capacity-revalidation--2026-10-23), superseding the earlier blanketspacehold without reducing a packet contract. Existing whole-scope/one-sole-review/RootCITEONLY rules, first-fault and failed/unattempted dispositions, opaque decisions and Claude guest hold persist. Fresh complete resource admission remains required; no source/tool/native action or behavioral credit was produced by cleanup.


[The next whole AClip frontier](clip-launch.md#complete-aclip-dependency-metadata-and-two-constant-windows-selected--2026-10-23) explicitly selects ninecallee declarations/fiveunreadhintrecords/full17candidate and14runtimeclassaccounting plus only32admitted rawfilebytes. It is one standing static cohort/one sole peer/fullcurrentbudget/RootCITEONLY, with no newcallee body, runtime/FP/provider/opaque or guest action. Existing publicunknowns, completeAnalog59priority and product closure rules remainunchanged.


[The Automationv2partialrecord is adopted](automation-envelopes.md#native-v2-sole-partial-record-adopted--2026-10-23), preserving its protocolbreach and whole-classunknowns. The [explicitv3owneddiagnostic/static-tool recovery](automation-envelopes.md#native-v3-after-sole-handoff-exact-diagnostic-command-and-retained-semantic-scope--2026-10-23) records the exactcommand-expression/countunit change and permits onlyNEWwhole-class semanticclaims from retainedprojections, with oldguards/proof inherited rather thanrerun/reviewedagain. This changes no useropaque/reference/Xaudio retry, sourceacquisition, guest, scope or completionpolicy.


[The whole four-declaration MNS053 native question](midi-note-storage.md#whole-four-declaration-native-question-selected--2026-10-23) is now explicitly selected aftersolemetadataapproval:1180bytes/fourexactranges/295prospectiverows, with globalwidth/value/provider/runtime/publicjoinsU. Existing onefreeze/solepeer/RootCITEONLY/fullcurrentbudget/firstfault rules apply; new byte-countdecoder fixtures test the largest836Bcase, without oldproof/decoder replay. No opaque/runtime/provider/guest or scope/closure change.


Nextstaticclasses followsoleadoption and [boundedcross-cohortsharing](program-structure.md#cross-cohort-static-reference-reconciliation--2026-10-23):[wholeAnalog57](device-analog-dsp.md#whole57-class-after-shared-stub-reconciliation-selected--2026-10-23) carriesonealreadyguardedstub/reads56remaining7372B plusnewtail/29candidateMETADATA;[wholeClip9](clip-launch.md#whole-nine-callee-native-class-selected--2026-10-23) reads1032Bonly;[wholeAuto12-16-5-4-2-12](automation-envelopes.md#complete-recovered-method-frontier-metadata-and-five-cells-selected--2026-10-23) selectsmetadata+40rawcellbytes. Freshpre-moduleidentityreceipts/chronologicallyspecificeligibility/fullcurrentbudgets/firstfault/onefreeze-solepeer apply, oldproceduralgapsnotretrorepaired. No neworiginalruntime/FP/provider/opaque/guest, policydenominator or closure change.


The [complete MNS053 dependency metadata class](midi-note-storage.md#complete-four-body-dependency-metadata-class-selected--2026-10-23) is selected after current independent author/reviewer boundaries:four outside destinations, twenty indirect-site metadata questions, all73 typed candidates and six access classes. Carry known1054d56b4geometry and existing map/native/file evidence by citation; only three new callee declarations and twenty new site metadata queries, no file content or runtime follow. One packet/sole review/full current concurrency and resource guards; Root citation-only, Claude guest hold and all behavioral unknowns unchanged.


## Confirmed Windows handoff and sitting-first routing — 2026-10-23

[ADR0006's confirmed handoff/priority](../decisions/adr-0006-reference-observation-reopened.md#confirmed-handoff-and-windows-sitting-priority-supersede-static-queues--2026-10-23) and the [current plan checkpoint](full-live-specification-plan.md#current-execution-checkpoint), mirrored exactly in the [session handoff](session-handoff.md#current-selection), supersede earlier dated Claude-exclusive holds and active static-author/peer scheduling on this page. Root alone resumes the offline/no-NIC guest for **Session0 then all nine SessionA records**, with one sole NEW sitting-evidence/code review after freeze. Workers stay host-only; no new static follow, semantic work or queued static review runs ahead of Windows. Approved INPUT/tool/source proofs are inherited without a second proof review, and per-record unavailable prerequisites remain explicit not-observed/U rather than a new universal readiness gate.

Claude's authorized-offline Live12.4.3/build/hash, WindowsPro26300/unactivated observer profile and44.1kHz ich9HDA audio are reported handoff context, not reviewed current capability/results. The203924 authorization-session crash is separate setup history. Root records oldPID1588360 disappearing before first key and one supplied-script offline existing-disk relaunch, without reinstall/revert/duplicate process; newPID1590872/desktop is Root-reported, actual identity/results UNVERIFIED. No new Windows-key/AUZ/credentials request or NIC use is selected.

[Analog57](device-analog-dsp.md#windows-priority-parks-the-analog57-author-partial--2026-10-23) is a truthful frozen author partial; [Clip9](clip-launch.md#windows-priority-parks-the-nine-callee-review--2026-10-23) and [Automation frontier](automation-envelopes.md#windows-priority-parks-the-recovered-frontier-author-freeze--2026-10-23) are author-frozen UNREVIEWED, peers unbegun/parked. [MNS dependency](midi-note-storage.md#windows-priority-parks-the-once-census-terminal-record--2026-10-23) has a once-census terminal author freeze, with mapping/73-membership/synthesis/ordinary checker/sole peer and Automation peer unattempted. Frozen bytes, source scopes, full budgets and all failed/unattempted/ASOF histories remain unchanged; no automatic continuation. Current24,051draft additions, reviewedO0, main25,095of268,015, releases36total/19current/17superseded and wholeLiveOPEN stay exact. This scheduling amendment changes no behavioral criterion, case/grade/site/release, source denominator, opaque policy, failed-X/audio retry rule or completion rule.

## Revision 18 — paired observation and static analysis — 2026-10-23

User direction on 2026-10-23, simplified the same day: observation and static
analysis of the same component are two additive sources, not a synchronized
procedure. [Plan revision 6](full-live-specification-plan.md#revision-6--paired-observation-and-static-analysis-2026-10-23)
schedules them in parallel.

- Each source keeps its own label and adoption path: O under revision 14, S
  and X under revision 12. No joint packet or joint review exists.
- A unit may carry an O value, an S explanation such as the code location
  that produces it, and X values computed by that code, each with its own
  label. Amended 2026-10-23 by user direction to run X as a third concurrent
  source.
- Values read with gdb during a harness run, such as an intermediate value, the
  exit path taken or an indirect call target, are X evidence about the macOS
  slice. They carry the breakpoint address, the inputs and the gdb script
  hash, like any other X value. A diagnostic rerun of a failed history adds
  evidence and leaves the failed result in place. A coverage map describes the
  input set, not behaviour; it is reported with an X claim and is not a gate.
  The [gdb introspection method](extracted-execution.md#gdb-introspection--2026-10-23)
  is the how-to. An S prediction stays labelled S and never
  becomes O.
- A disagreement between O and S is an open question with both values kept,
  as revision 14 states.
- The S worker reads the pinned macOS source and the O worker observes the
  Windows profile, so the owner records platform applicability for any value
  that depends on the platform.


## Three-source Session0 and SessionA execution — 2026-10-23

The user-amended [plan revision6](full-live-specification-plan.md#revision-6--paired-observation-and-static-analysis-2026-10-23) supersedes the earlier sitting-only scheduling restriction: O, S and X run as three concurrent subagents on document container/save path, transport state, mixer values and MIDI note storage. O=tension_owner_finish alone drives the guest; S=tension_review_finish and X=o137_finish stay on the host. Root relinquished guest input after handing over the active first SessionA case. Already known authorization/identity facts are inherited; no repeated readiness confirmation delays the sitting. Each route adopts through its existing separate packet and sole review, with no combined packet, extra review, required ordering or platform-equivalence inference. Root solely reviews NEW S/X scope; o137 is the sole O reviewer after its own natural closed X boundary. Old unrelated static author freezes and their unbegun reviews remain parked; their bytes and unknowns are unchanged.
