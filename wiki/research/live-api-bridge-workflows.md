---
id: RESEARCH-LIVE-API-BRIDGE-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public API/Max source applicability U
specs: SPEC-LIVE-API-BRIDGE-WORKFLOWS
---

# Public API bridge source roles and unresolved contexts

## Question, ownership and versions

Which public bridge/lifecycle roles can be stated from retained text without
promoting a newer publisher reference to target runtime proof? The
[canonical draft](../specs/live-api-bridge-workflows.md) owns proposed clauses;
[coverage design](full-live-specification-design.md) and
[plan](full-live-specification-plan.md) govern the partial F-05/F-08 scope.
This analyst context cannot implement. No original/Max/JS/patch/API/native/
candidate/hardware runtime, installation, emulator or source example was executed.

The [source-family page](sources/cycling74-live-api.md) is a mutable route; evidence
is pinned to reviewed [R1 inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/../max-api/manifest-inventory-r1.json)
and its original immutable snapshot. That LOM index explicitly declares Live 12.4.5,
after target 12.4.3. Overview/bridge current Max versions do not establish a matching
runtime. D-current-public means publication text only; all new target applicability U.
The 45 LOM references/588 direct headings, inherited members and full member/type/
event signatures remain separate; no complete API entry is claimed.

## Retained evidence and bounded reading

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/sources.json) reuses seven exact source identities from the
reviewed max-api catalog: overview and path/object/observer/remote~/thisdevice/
JavaScript LiveAPI. Original publisher URL/final URL, UTC capture, size and SHA
are retained without recapture. No max-api file or source-family canonical is
edited. [Inventory pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/inventory-pins.json) retains five R1 artifact
identities and [blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json) preserves 893 exact source rows
with original block/HTML line/column/anchor/section. A [text view](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.txt)
is derived, not source bytes. Generic Max box attributes remain retained data,
not adopted Live-specific protocol requirements.

Read all overview paragraphs including examples as data, and all relevant
description/arguments/Live-specific attributes/messages/Inspector and JS headings,
paragraphs and tables in the six references. Examples were not executed or converted
into fixtures/algorithms. Common-box appearance attributes and See Also links are
outside the adopted role scope. Figures and linked sources were not inspected.

## Source-supported roles and exclusions

OV B0004–B0038 describes hierarchy, paths/roots/canonical parents, device-scoped
IDs and get/set/call/observation. Paths and API IDs are distinct from ALS Ids,
native pointers, list storage indices and generic user mapping tokens. Canonical
parent examples do not prove every nested device parent is a Track. Child lists
versus single children and read/write/observable capabilities need independent
per-member evidence rather than inference from a name or getinfo listing.

PATH B0063–B0113 describes list counts, names, current path, combined bang/getid
and absolute/relative/up navigation. OBJ B0059–B0153 separates binding, metadata,
four get/set categories, callable members and persistence option. OBS B0004 and
B0061–B0124 separates observed values, child IDs/lists, metadata output and explicit
bang from spontaneous notifications. Generic message roles leave actual byte/token
grammar, error/no-object representation, ID numbers and output/callback order null.

REM B0006/B0011/B0013/B0064–B0082 describes eligible DeviceParameter binding,
release, message/signal/ramp/smoothing/normalized controls, UI path copy and
parameter/automation/history interaction. Single-buffer/sample-accurate prose,
default smoothing and normalization examples are not target scheduling or a
native/stored/gain conversion. Unknown parameter eligibility/units/automation
ownership requires active nonzero source/base/depth and paired positive output.

INIT B0004/B0057–B0065 describes complete-initialization/reload versus manual
bang/loadbang, enabled/preview and width save caveat. JS B0003–B0142 gives initialized
constructor/callback/follow modes/path/get/set/call/observation/metadata roles,
with global/high-priority-use cautions. These sources do not mandate candidate
threading, defer objects or scheduler internals; neither manual bang nor a nominal
constructor proves a ready accepted Live/Max API. JS source types are not all LOM
property/type unions or arbitrary JavaScript compatibility.

Public examples of 0..1 volume, master_track, routing labels or time conversions
are not adopted numeric laws. Existing finite/native mixer/gain/enum/transport/
Warp/automation/mapping owners retain their versions/conditions; no oldest native
enum or current canonical is overwritten. Examples' child spelling and selected
object prose are not a complete path grammar. All compound member operations stay
partial until individually evidenced.

## Source context questions

| Local ID | Exact source contexts | Treatment |
| --- | --- | --- |
| Q-LAB-001 | OV:B0023–B0024 says device-scoped/usually-stable IDs are not stored; JS:B0106 warns dynamic IDs should not span runs. OBJ:B0153/OBS:B0124/REM:B0082 describes optional Persistent Mapping and historical cross-launch persistence. | Retain feature/object/version contexts separately. Compare actual association, path and ID under mapping on/off and JS independently; no universal nonpersistence, cross-run equality or precedence law. |
| Q-LAB-002 | PATH:B0061–B0062 standalone getid is TEXT_HERE; PATH:B0088–B0089 combined bang,getid describes lookup/no-object outputs. | Adopt combined-section role only with explicit context; standalone placeholder stays U, not filled from memory or claimed a contradiction without same mode/preconditions. |
| Q-LAB-003 | OV:B0013/B0019 and PATH:B0100 includes this_device root use; PATH:B0103 goto absolute-root list omits it. | Record omission/context without concluding unsupported root. Valid nested/root/relative/up and root lifetimes need independent accepted contexts. |
| Q-LAB-004 | OV:B0063/B0107 and OBS:B0004 prohibit mutation during notifications and describe deferred follow-up; JS callback roles JS:B0039/B0097/B0119 do not supply reentrancy guarantees. | Preserve spontaneous/requested distinction and version/context. No global mutation-success law, exact error, callback ordering, deferlow cure or candidate threading mechanism. |
| Q-LAB-005 | OV:B0087 and REM:B0006 describe automation disabled, no new Undo/saved-value change; REM:B0006 also says envelopes remain active. | Automation/modulation/envelope identities and remote release restoration remain U; no blanket disable-all, numeric value equality or old finite envelope-law replacement. |
| Q-LAB-006 | INIT:B0004 uses middle enabled/right preview states; INIT:B0061 calls getstate rightmost output device state. | Keep enabled/preview/Live/editor contexts separate; no conflated state or outlet-order numeric oracle. |
| Q-LAB-007 | JS:B0061 generic value/list description and B0062 printed number/number-array annotation versus getstring B0085–B0086 string representation; individual LOM types remain outside this packet. | Complete return unions/coercion/serialization U; no type grammar reconstructed from examples. |

These are unresolved source contexts, not asserted runtime contradictions without
same object/mode/feature/version/preconditions. Root owns shared question register;
broader publication/build applicability stays with
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

## Cases and evidence gates

There are 52 requirements: 44 D-current-public and eight U, with 61 proposed cases.
One visible option-presence proposal has a documentary comparator; 60 are null,
including all message/ID/numeric/notification/timing/signal and wholly unknown
probes. Every target expected/comparison is null/U/unexecuted. source_claim is
retained separately, never an expected output or API call trace. No full bridge,
LOM member, hardware/profile or complete Max runtime is closed.

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/fixtures.json) require independently valid owned patch and
available initialized accepted Live/Max context, existing eligible object/path/ID,
actual read/write/call/observe capability and positive binding/state-change first.
Remote/audio additionally needs active parameter/path with nonzero source/base/
amount/depth/gain/send, correct arm/monitor/clip/receiver and nonmuted positive wet/
output baseline. Explicit transport/record/Automation Arm applies where relevant.
Missing object/capability/host or a silent/inactive path remains U, never pass.
No patch/script/media/accepted runtime is supplied and none is fabricated.

Finite unknown probes cover source/version roots/placeholders, ID/mapping
persistence/move/delete, malformed/readonly/nonobservable input, callback mutation,
load/readiness, enabled/preview state, automation/remote arbitration, rates and
transport, Undo/cancel/concurrency, target/context loss/recovery and teardown.
They do not invent a universal asynchronous cancel or rollback/cleanup rule.

## Author freeze and checks

[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/owner-pins.json) retain 17 existing canonical boundary identities;
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/manifest-author-r1.json) seals this packet's source references,
derived blocks, catalogs, cases, fixtures, author/validator and canonical snapshots.
The [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/validate.py) is read-only before/after seal: all 65 original
inventory R1 payload hashes, seven source identities, 893 block equality/reproduction,
owner pins, exact requirement/case/browser IDs, null oracles, snapshots, local links/
anchors, manifest inventory and untracked-aware whitespace. It prints stdout only.
Later inventory/source-page revisions may coexist; frozen R1 bytes remain evidence.

Independent semantic review is required; no Max/API/runtime, implementation,
compatibility or complete feature claim follows from integrity checks. Root
integrates shared indexes, coverage, questions and log; this author edits none.
