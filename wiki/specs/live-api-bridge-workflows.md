---
id: SPEC-LIVE-API-BRIDGE-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public Max/Live API source applicability U
---

# Public Live API bridge and lifecycle workflows

## Scope, versions and evidence

This partial F-05/F-08 draft owns documentary navigation/identity, get/set/call,
observation/notification, parameter-remote and initialization roles from the
retained overview and six bridge references. [Research](../research/live-api-bridge-workflows.md)
preserves source contexts; [coverage design](../research/full-live-specification-design.md)
governs closure. This is not a complete API/Max contract, released implementation
input, executed patch or compatibility result.

**D-current-public** is text in the retained current Cycling74 public source,
not a pinned Live 12.4.3/Max runtime. The source inventory's LOM index explicitly
declares **Live 12.4.5**, after the target; the overview and bridge pages do not
establish a matching Max version. Every new target applicability remains **U**.
All target expected/comparison fields are null, all target grades U and all cases
unexecuted. Message, ID, numeric, timing, signal and callback outcomes also have
null documentary expectations/comparators; source_claim is separate. Only the
named Inspector option has a visible-control proposal, without binding proof.

The [reviewed source inventory](../research/sources/cycling74-live-api.md) discovers
45 LOM references and 588 explicit direct declarations; all member semantics,
inheritance, root/alias reconciliation and full bridge argument/event grammar
remain separate. Counts overlap other product surfaces. Generic Max common-box
attributes, source examples, live.map, scripts and arbitrary Max compatibility
are not newly specified here. No schema/storage field becomes an API behavior.

## Existing owners and prerequisites

[Max hosting](max-for-live-hosting.md) keeps device loading/editor/save/dependency/
template behavior. [Set structure](live-set-structure.md),
[racks](device-racks.md), [Clip View](clip-view-workflows.md),
[Session](session-view-workflows.md), [launch](clip-launch.md) and
[recording](recording-comping.md) retain target creation/edit/preset/record and
object-facing application behavior. A generic API call role does not complete
any individual method, child, property or external UI effect.

[Automation envelopes](automation-envelopes.md), especially REQ013, and
[automation workflows](automation-workflows.md) retain their finite evaluator
and unclosed editing/runtime. [Mix graph](mix-graph.md) and
[mixer values](mixer-values.md) retain conditional gains/units/ramps;
[routing](routing-monitoring-latency.md), [transport](transport-state.md),
[playback](playback-core.md), [Warp](warp-markers.md), [MPE](mpe-workflows.md),
[tuning](tuning-systems.md), [MIDI mapping](midi-user-mapping.md) and
[bundled parameters](bundled-device-parameters.md) retain numeric/codecs/defaults
and older finite/native enum scopes. Public examples of volume 0..1, timing,
master_track, input labels or list indices do not overwrite those owners.
Target API aliases/member capabilities and conversions need their own evidence.
[Project/media](project-media-workflows.md) owns generic save/history/media state.

The [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/fixtures.json)
require independently valid test-owned patch/device, actually available accepted
Live/Max/API context, initialization and eligible existing object/path/ID/member.
No patch, JS program, API call, accepted host or runtime result is supplied.
Read/write/call/observe capabilities must be independently established, with
positive binding/readback/state-change before invalid/no-effect probes.

Audio/remote observations additionally require active eligible parameter/section,
nonzero source/base/depth/amount/gain/send, correct arm/monitor/receiver/clip state,
explicit transport/record/automation context and positive nonmuted wet/output.
Retain matched positive control before changing one tested state. Absent context,
missing object, stale binding, unsupported member, zero signal or mute remains U,
never a no-effect pass. Missing firmware/ports/controllers are not simulated.

Publisher main-thread/defer, sample accuracy/single-buffer and smoothing examples
are source context only. No candidate threading, queue, scheduler architecture,
numerical interpolation, rate invariance, latency, tolerances or private mechanism
is prescribed. No source example/script/patch, Max, original/native/extracted code,
Live API, hardware, installation or independent application is executed.

## Requirements

## Paths and identity

### REQ-LAPI-BRIDGE-001 — Reachable public hierarchy

**D-current-public/target-U.** The public overview describes a hierarchy of Live objects with single children and object lists, exposing only part of Live. Reachability, available members and types must be independently established; the inventory is not all application internals or complete API closure.

Evidence: [OV:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0005](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-002 — Path syntax and relative context

**D-current-public/target-U.** Overview paths are unquoted navigation terms with zero-based list indices; more than one path may identify the same object. Relative paths begin from current hierarchy position. These source roles do not prescribe a complete argument grammar, quote parser or native index encoding.

Evidence: [OV:B0008](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0009](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0010](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0011](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-003 — Root families

**D-current-public/target-U.** The overview/path reference names live_app, live_set, control_surfaces with an index and this_device as root roles. Control-surface access depends on the controller; this_device is device-relative. Root availability, identity and lifetime are not universal constants.

Evidence: [OV:B0013](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0014](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0100](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-004 — Canonical path and parent roles

**D-current-public/target-U.** Multiple paths can lead to one object; the overview describes a unique canonical path, returned by live.object getpath, and a get-only canonical_parent child. Its own-track example is not an unconditional parent-is-track law for nested devices or roots.

Evidence: [OV:B0016](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0017](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0019](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-005 — Object IDs and no-object sentinel

**D-current-public/target-U.** The overview describes id plus integer tokens, with id 0 denoting no object, device-scoped IDs assigned when navigated, normally stable while an object exists, and possible move-as-delete/create exceptions. Deletion/replacement and nonreuse/nonstorage prose are documentary contexts, not target ID allocation or durable identity laws.

Evidence: [OV:B0021](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0022](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0023](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0024](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0025](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-006 — Children, properties and call roles

**D-current-public/target-U.** Types describe available children/properties/functions; children may be single, lists or absent. getcount applies to lists, while get/set and call access eligible state/functions. Not all children/properties are observable or settable. Individual LOM member capability remains separately unresolved.

Evidence: [OV:B0027](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0028](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0030](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0031](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0032](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0033](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0035](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0036](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0038](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-007 — Notifications versus polling

**D-current-public/target-U.** The overview distinguishes explicit navigation/get/call polling from spontaneous notifications for path-object changes and property values. This supplies event roles only, not cadence, coalescing, delivery order, queue policy or a complete notification set.

Evidence: [OV:B0060](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0061](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0062](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-008 — Notification mutation context

**D-current-public/target-U.** Overview and observer prose says Live Set changes cannot be triggered directly while receiving notifications, and suggests deferred interaction in relevant contexts. This is a documented restriction/caution, not a prescribed candidate thread, queue architecture or guaranteed deferlow cure.

Evidence: [OV:B0063](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0107](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## live.path

### REQ-LAPI-BRIDGE-009 — Navigation and path following outlets

**D-current-public/target-U.** live.path selects objects for other bridges; its left output gives navigation identity and middle output follows the object currently at the path. A nonexistent path is described as yielding no-object IDs rather than an error. Path following is distinct from retaining one particular object.

Evidence: [OV:B0076](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0080](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0081](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-010 — Initial path and absolute path message

**D-current-public/target-U.** live.path accepts an optional initial path and a path message for root-starting absolute paths. Root/name acceptance and initialization readiness remain target U; the initial argument is not proof of a ready Live API during patch load.

Evidence: [PATH:B0007](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0099](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0100](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-011 — goto relative/up and list-member boundary

**D-current-public/target-U.** goto is documented for absolute or relative paths and up, selecting individual list members rather than the list itself. Its root list omits this_device while other source contexts include it; the omission does not settle that root’s goto acceptance.

Evidence: [PATH:B0102](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0103](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-012 — Count and child enumeration

**D-current-public/target-U.** getcount reports a named list child’s count via the right outlet; getchildren reports available child names there. These are documented output roles, not stable list ordering, inherited-member closure or exact tuple/empty representation for target builds.

Evidence: [PATH:B0063](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0064](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0069](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0072](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0073](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0078](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-013 — Current path response

**D-current-public/target-U.** live.path getpath reports its current navigation path via the right outlet. This differs from live.object canonical getpath and does not require path spelling to match a canonical alias.

Evidence: [PATH:B0080](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0081](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0086](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-014 — Combined bang/getid documented role

**D-current-public/target-U.** The combined bang, getid section describes emitting current-path identity through left and middle outputs, with no-object sentinel when absent. The separate standalone getid section is a placeholder and remains unsupported; no blank is filled from memory.

Evidence: [PATH:B0088](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [PATH:B0089](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## live.object

### REQ-LAPI-BRIDGE-015 — Select current object by ID

**D-current-public/target-U.** live.object operates on selected Live objects; id assignment is described for either inlet, with right-inlet use suggested for clarity and no assignment output described. This is not input routing, ID scope or rejection parity for arbitrary tokens.

Evidence: [OBJ:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0061](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0062](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-016 — Current identity and type

**D-current-public/target-U.** getid or bang/getid reports current identity and gettype its object class; getid describes no-object when unbound. These output roles do not specify every invalid/deleted-ID branch, exact names or message interleaving.

Evidence: [OBJ:B0059](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0060](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0071](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0072](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0081](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0082](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-017 — Canonical getpath and getinfo roles

**D-current-public/target-U.** getpath reports canonical current-object path. getinfo describes identity/type/description/children/properties/functions and a terminating done role, with repeatable description lines. No fixed line order/cardinality or complete inherited-member specification follows.

Evidence: [OBJ:B0063](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0064](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0079](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0080](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-018 — Read child versus child list

**D-current-public/target-U.** get on an eligible list child reports element IDs; on a single child it reports that child ID. Source examples are not exact runtime IDs, alias names, empty-list formatting or universal child availability laws.

Evidence: [OBJ:B0115](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0116](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0121](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0124](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0125](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0130](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-019 — Read value versus value list

**D-current-public/target-U.** get reads single-value and list properties, with types and capabilities delegated to the LOM. Example routing labels, names and numbers do not override current native/domain owners or define a complete return grammar.

Evidence: [OBJ:B0133](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0134](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0139](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0142](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0143](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0148](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-020 — Set child versus child list

**D-current-public/target-U.** set has separate single-child and child-list roles accepting eligible object identities. Not all children are writable; no assignment response is described. Complete mutation, list ordering, cross-device IDs and rollback remain U.

Evidence: [OBJ:B0099](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0100](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0103](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0104](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-021 — Set property versus value list

**D-current-public/target-U.** set writes eligible single/list property values; not all properties can be set and their types come from the LOM. No assignment response is described. Bounds, clamping, serialization, automation ownership and numerical conversion require separate evidence.

Evidence: [OBJ:B0107](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0108](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0111](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0112](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-022 — Function call role

**D-current-public/target-U.** call names a current-object function and optional typed parameters, with result output described by the public source. Actual callable members, signatures, side effects, return types and errors are not completed by this generic bridge clause.

Evidence: [OV:B0038](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0089](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0090](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0095](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## Persistence

### REQ-LAPI-BRIDGE-023 — Persistent Mapping Inspector option

**D-current-public/target-U.** live.object, live.observer and live.remote~ references name an Inspector Use Persistent Mapping option. Its save/restore/editor-move association prose is retained separately from overview/JS dynamic-ID cautions; default, cross-run numeric ID and exact-target persistence remain U.

Evidence: [OBJ:B0152](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBJ:B0153](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0123](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0124](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0081](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0082](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## live.observer

### REQ-LAPI-BRIDGE-024 — Observe eligible property and changes

**D-current-public/target-U.** live.observer selects an eligible object/property and describes initial/current value plus later change notifications through its left output. An optional argument selects property/child. Not all properties are observable and notification timing/count/order are unproven.

Evidence: [OBS:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0007](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0061](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0062](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-025 — Observe single child versus child list

**D-current-public/target-U.** Observer property selection can target an observable child ID or child list; single-child source mentions no-object and list source permits no output for an empty result. Capability and representation differ and are not generalized to every child.

Evidence: [OBS:B0070](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0071](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0079](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0080](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-026 — Binding and bang role

**D-current-public/target-U.** Observer ID assignment accepts either inlet with right suggested; bang queries current selected property/object. The source describes no action without matching property/object, but invalid tokens, deleted objects and no-effect behavior remain target U.

Evidence: [OBS:B0112](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0113](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0120](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0121](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-027 — Observer metadata outputs

**D-current-public/target-U.** getproperty, gettype and getid describe current selection/type/identity through observer right output, distinct from value output left. Child-list type information is described as limited; no complete typed schema or cross-outlet order follows.

Evidence: [OBS:B0088](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0089](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0096](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0097](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0104](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OBS:B0105](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## live.remote~

### REQ-LAPI-BRIDGE-028 — DeviceParameter binding and release

**D-current-public/target-U.** live.remote~ binds a DeviceParameter identity through the right inlet, describes no effect for non-parameter IDs, reports mapped identity via getid, and uses id 0 to release control/re-enable parameter. Nonparameter rejection, release ordering and restoration stay U.

Evidence: [REM:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0075](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0076](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0078](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0079](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-029 — Parameter LOM path UI entry

**D-current-public/target-U.** The reference describes Copy LOM Path in a parameter context menu as available in Live 12, and live.path or live.map as ways to select a parameter. This does not specify the separate live.map object, exact path alias, menu eligibility for every control or target-build support.

Evidence: [REM:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-030 — Message and signal control roles

**D-current-public/target-U.** Integer/float messages and signal input address the selected parameter through left inlet. Source prose distinguishes buffer/ramp scheduling from realtime signal application; sample-accurate/single-buffer claims are context, not target timing or candidate architecture requirements.

Evidence: [REM:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0063](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0064](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0066](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0067](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0073](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0074](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-031 — Ramp and smoothing controls

**D-current-public/target-U.** smoothing describes event ramp time and signal temporal sampling; a value/time list requests a ramp and a new ramp overrides a current ramp. No source default/example is promoted to target interpolation, sample count, rate law or interruption arithmetic.

Evidence: [REM:B0010](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0011](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0069](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0070](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-032 — Normalized-mode role

**D-current-public/target-U.** normalized toggles between source-described automatic parameter-range scaling and caller-supplied parameter-domain values. This is not a conversion formula, native/stored-unit equivalence, valid range for every target or complete parameter behavior law.

Evidence: [REM:B0012](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0013](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-033 — Automation, undo and envelope context

**D-current-public/target-U.** Remote control is described as disabling parameter interaction/automation without changing saved Set value or creating Undo steps, while reference prose also says envelopes remain active. Automation versus envelope identity and restoration are unresolved contexts, not a blanket disable-all law.

Evidence: [OV:B0087](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [REM:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## live.thisdevice

### REQ-LAPI-BRIDGE-034 — Initialization and reload notification

**D-current-public/target-U.** live.thisdevice describes left-outlet bang when the Max device/containing patcher is opened and completely initialized, including Live API in the JS/overview context, and again for preset load or device save/reload. Generic loadbang is not proof of Live API readiness.

Evidence: [OV:B0100](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-035 — Enabled and preview state context

**D-current-public/target-U.** Description distinguishes device-enabled middle output and preview right output in Live, with inactive state outputs when used in Max alone. getstate text says device state on rightmost output, leaving exact state meaning/context unresolved rather than merging enabled and preview.

Evidence: [INIT:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0060](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0061](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-036 — Explicit bang and mouse entry

**D-current-public/target-U.** Explicit bang, double-click and loadbang message roles describe left bang output. Those manual/message actions do not imply the device/API has reached the automatic complete-initialization condition.

Evidence: [INIT:B0056](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0057](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0058](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0059](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0062](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0063](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-037 — Device width message and save caveat

**D-current-public/target-U.** setwidth changes Max for Live device width and its source says this is not automatically saved in preset/Set; the reset setting returns width calculation from visible objects. Exact pixels/default sizing, persistence mechanism and unrelated layout behavior remain unknown.

Evidence: [INIT:B0064](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [INIT:B0065](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## JavaScript LiveAPI

### REQ-LAPI-BRIDGE-038 — Initialized JavaScript access context

**D-current-public/target-U.** LiveAPI offers js access to path/object/observer roles, with source cautions against global-code use and high-priority execution and a live.thisdevice readiness recommendation. Legacy constructor context is retained. No JS engine version, scheduler architecture or full runtime compatibility is imposed.

Evidence: [JS:B0003](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0004](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0005](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0006](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [OV:B0090](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-039 — Constructor and callback roles

**D-current-public/target-U.** Constructor accepts optional callback and path or valid API identity; callback is described for referred-object or observed-property changes. Complete overload grammar, callback values/reentrancy and cross-instance ID acceptance are unresolved.

Evidence: [JS:B0031](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0032](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0033](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0039](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0042](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-040 — Follow-object versus follow-location modes

**D-current-public/target-U.** LiveAPI mode distinguishes following the particular referred object across movement from following the object occupying a hierarchy location. Source defaults/examples are not exact-target numeric mode, move-as-recreate, ID lifetime or bank-selection laws.

Evidence: [JS:B0109](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0110](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0111](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-041 — Path, ID and validity properties

**D-current-public/target-U.** goto navigates and reports object/no-object through callback; id is dynamic and not to be reused across runs per JS text. path and unquotedpath distinguish quoting and are Set-dependent; valid describes whether a Live object is referred to. Complete grammar, validity timing and persistent bindings remain U.

Evidence: [JS:B0096](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0097](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0105](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0106](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0114](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0115](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0116](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0138](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0139](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0140](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0141](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0142](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-042 — Children and info/type metadata

**D-current-public/target-U.** children/getcount expose current-path child information; info/type describe object metadata and patcher identifies containing context. These bridge roles do not complete inherited member semantics, child cardinalities, source code architecture or exact class/type unions.

Evidence: [JS:B0058](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0059](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0072](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0073](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0107](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0108](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0112](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0113](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0135](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0136](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-043 — get, getstring, set and call roles

**D-current-public/target-U.** JS get/getstring read property values/lists with distinct described representations; set writes and call invokes eligible members. Printed get type annotation is narrower than the generic description; complete return unions, member signatures, type conversion and errors require separate evidence.

Evidence: [JS:B0043](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0044](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0060](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0061](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0062](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0084](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0085](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0086](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0123](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0124](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

### REQ-LAPI-BRIDGE-044 — Observed property and type

**D-current-public/target-U.** property selects an observed property, child or child list and proptype describes selected type; callback changes are documented roles only. Capabilities, initial callback timing, mutation while handling and stale targets remain unresolved.

Evidence: [JS:B0117](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0118](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0119](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0120](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0121](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json), [JS:B0122](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/source-blocks.json).

## Unknown obligations

### REQ-LAPI-BRIDGE-U-VERSION — Version, members and source contexts

**U/target-U.** Current LOM index declares Live12.4.5; bridge Max versions are unpinned. Exact12.4.3 applicability, complete 45-reference/588-direct-member/inherited capabilities, aliases, roots and source-context discrepancies remain U.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-IDENTITY — ID, root and persistence lifecycle

**U/target-U.** Overview/JS dynamic/nonstored IDs versus optional Persistent Mapping save/editor-move prose are not reconciled into one lifetime law. Root/device/Set scope, deletion/reorder, invalid/stale/cross-device IDs, path aliases and reopened bindings need evidence.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-GRAMMAR — Argument, type and error grammar

**U/target-U.** Malformed paths/quotes, unknown names, child/list capability, overloaded messages/functions, callback/result types, nonfinite/out-of-range values and read-only/nonobservable outcomes have no new complete parser, diagnostic or repair law.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-ORDER — Scheduling, notifications and reentrancy

**U/target-U.** Delivery/count/coalescing/order across outlets/callbacks, notification-time reads/mutations, initialization races, remote ramp/buffer/sample timing and rate/transport transitions remain unknown. No thread/queue architecture or latency mandate follows.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-REMOTE — Signal and parameter ownership

**U/target-U.** Remote normalization/smoothing/ramp, no-effect nonparameter tests, automation/modulation/manual control, saved value and release restoration need independently positive active paths and remain numerically ungraded.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-STATE — History, cancellation and durable state

**U/target-U.** Save/reopen, migration, preset/editor moves, Undo/Redo grouping, cancellation, concurrent mutations and persistent-mapping default/state consequences remain U beyond source roles.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-LOSS — Unavailable context and source loss

**U/target-U.** Object/property/device/track/Set/patcher/controller/media/engine disappearance, observer invalidation, unbinding/rebinding and recoverability require evidence. Missing API/Max capability is an unmet prerequisite, not a refusal or silence pass.

Evidence: unsupported outcome; ungraded investigation obligation.

### REQ-LAPI-BRIDGE-U-TEARDOWN — Teardown and pending work

**U/target-U.** Device/patch/Set close, Live/editor transition or quit with active observer/callback/remote ramp/control has no established flush, cleanup, completion, crash or silence deadline.

Evidence: unsupported outcome; ungraded investigation obligation.

## Finite future cases

[61 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/cases.json) map to [52 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/requirements.json):
44 current-public documentary clauses and eight U obligations. One case compares
the named Inspector option only; 60 have null documentary oracles. All 61 target
outcomes/comparators are null/U/unexecuted. Even documented message formats are
source_claim context, not executable acceptance or complete argument grammar.
Each overloaded message, bridge/member/host branch needs its own retained result
before closure. No complete API entry or original-versus-candidate pass is claimed.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
| LAB-001 | REQ-LAPI-BRIDGE-001 | message-role | Reachable public hierarchy |
| LAB-002 | REQ-LAPI-BRIDGE-002 | message-role | Path syntax and relative context |
| LAB-003 | REQ-LAPI-BRIDGE-003 | message-role | Root families |
| LAB-004 | REQ-LAPI-BRIDGE-004 | message-role | Canonical path and parent roles |
| LAB-005 | REQ-LAPI-BRIDGE-005 | message-role | Object IDs and no-object sentinel |
| LAB-006 | REQ-LAPI-BRIDGE-006 | message-role | Children, properties and call roles |
| LAB-007 | REQ-LAPI-BRIDGE-007 | notification | Notifications versus polling |
| LAB-008 | REQ-LAPI-BRIDGE-008 | notification | Notification mutation context |
| LAB-009 | REQ-LAPI-BRIDGE-009 | message-role | Navigation and path following outlets |
| LAB-010 | REQ-LAPI-BRIDGE-010 | message-role | Initial path and absolute path message |
| LAB-011 | REQ-LAPI-BRIDGE-011 | message-role | goto relative/up and list-member boundary |
| LAB-012 | REQ-LAPI-BRIDGE-012 | message-role | Count and child enumeration |
| LAB-013 | REQ-LAPI-BRIDGE-013 | message-role | Current path response |
| LAB-014 | REQ-LAPI-BRIDGE-014 | message-role | Combined bang/getid documented role |
| LAB-015 | REQ-LAPI-BRIDGE-015 | message-role | Select current object by ID |
| LAB-016 | REQ-LAPI-BRIDGE-016 | message-role | Current identity and type |
| LAB-017 | REQ-LAPI-BRIDGE-017 | message-role | Canonical getpath and getinfo roles |
| LAB-018 | REQ-LAPI-BRIDGE-018 | message-role | Read child versus child list |
| LAB-019 | REQ-LAPI-BRIDGE-019 | message-role | Read value versus value list |
| LAB-020 | REQ-LAPI-BRIDGE-020 | message-role | Set child versus child list |
| LAB-021 | REQ-LAPI-BRIDGE-021 | message-role | Set property versus value list |
| LAB-022 | REQ-LAPI-BRIDGE-022 | message-role | Function call role |
| LAB-023 | REQ-LAPI-BRIDGE-023 | control | Persistent Mapping Inspector option |
| LAB-024 | REQ-LAPI-BRIDGE-024 | notification | Observe eligible property and changes |
| LAB-025 | REQ-LAPI-BRIDGE-025 | notification | Observe single child versus child list |
| LAB-026 | REQ-LAPI-BRIDGE-026 | message-role | Binding and bang role |
| LAB-027 | REQ-LAPI-BRIDGE-027 | message-role | Observer metadata outputs |
| LAB-028 | REQ-LAPI-BRIDGE-028 | signal | DeviceParameter binding and release |
| LAB-029 | REQ-LAPI-BRIDGE-029 | message-role | Parameter LOM path UI entry |
| LAB-030 | REQ-LAPI-BRIDGE-030 | signal | Message and signal control roles |
| LAB-031 | REQ-LAPI-BRIDGE-031 | signal | Ramp and smoothing controls |
| LAB-032 | REQ-LAPI-BRIDGE-032 | signal | Normalized-mode role |
| LAB-033 | REQ-LAPI-BRIDGE-033 | signal | Automation, undo and envelope context |
| LAB-034 | REQ-LAPI-BRIDGE-034 | notification | Initialization and reload notification |
| LAB-035 | REQ-LAPI-BRIDGE-035 | notification | Enabled and preview state context |
| LAB-036 | REQ-LAPI-BRIDGE-036 | notification | Explicit bang and mouse entry |
| LAB-037 | REQ-LAPI-BRIDGE-037 | message-role | Device width message and save caveat |
| LAB-038 | REQ-LAPI-BRIDGE-038 | message-role | Initialized JavaScript access context |
| LAB-039 | REQ-LAPI-BRIDGE-039 | notification | Constructor and callback roles |
| LAB-040 | REQ-LAPI-BRIDGE-040 | message-role | Follow-object versus follow-location modes |
| LAB-041 | REQ-LAPI-BRIDGE-041 | message-role | Path, ID and validity properties |
| LAB-042 | REQ-LAPI-BRIDGE-042 | message-role | Children and info/type metadata |
| LAB-043 | REQ-LAPI-BRIDGE-043 | message-role | get, getstring, set and call roles |
| LAB-044 | REQ-LAPI-BRIDGE-044 | notification | Observed property and type |
| LAB-U-PLACEHOLDER | REQ-LAPI-BRIDGE-U-VERSION | source-context | Placeholder |
| LAB-U-ROOT-CONTEXT | REQ-LAPI-BRIDGE-U-VERSION | source-context | Root context |
| LAB-U-PERSISTENCE | REQ-LAPI-BRIDGE-U-IDENTITY | persistence | Persistence |
| LAB-U-MOVE-DELETE | REQ-LAPI-BRIDGE-U-IDENTITY | boundary | Move delete |
| LAB-U-INVALID-INPUT | REQ-LAPI-BRIDGE-U-GRAMMAR | malformed | Invalid input |
| LAB-U-CAPABILITY | REQ-LAPI-BRIDGE-U-GRAMMAR | negative | Capability |
| LAB-U-CALLBACK-MUTATION | REQ-LAPI-BRIDGE-U-ORDER | notification | Callback mutation |
| LAB-U-LOAD-STATE | REQ-LAPI-BRIDGE-U-ORDER | notification | Load state |
| LAB-U-TRANSPORT-RATES | REQ-LAPI-BRIDGE-U-ORDER | sample-rate | Transport rates |
| LAB-U-OWNERSHIP | REQ-LAPI-BRIDGE-U-REMOTE | automation | Ownership |
| LAB-U-NONPARAMETER-RELEASE | REQ-LAPI-BRIDGE-U-REMOTE | negative | Nonparameter release |
| LAB-U-UNDO | REQ-LAPI-BRIDGE-U-STATE | undo | Undo |
| LAB-U-CANCEL | REQ-LAPI-BRIDGE-U-STATE | cancel | Cancel |
| LAB-U-CONCURRENCY | REQ-LAPI-BRIDGE-U-STATE | concurrency | Concurrency |
| LAB-U-TARGET-LOSS | REQ-LAPI-BRIDGE-U-LOSS | source-loss | Target loss |
| LAB-U-CONTEXT-RECOVERY | REQ-LAPI-BRIDGE-U-LOSS | recovery | Context recovery |
| LAB-U-CLOSE-PENDING | REQ-LAPI-BRIDGE-U-TEARDOWN | teardown | Close pending |

## Open source contexts and lifecycle

[Local research questions](../research/live-api-bridge-workflows.md#source-context-questions)
retain dynamic/nonstored versus optionally persistent IDs, standalone getid
placeholder versus combined section, root-list contexts, callback mutation/defer
and parameter automation versus active envelopes. They are not silently reconciled
into target laws or declared contradictions without matching preconditions/version.
getstate enabled/preview outlet meaning and JS return-type annotations stay U.

Malformed paths/types/member capabilities, invalid/no-object/deleted targets,
reorder/move/replace, observer callbacks, remote binding/ramp/release, initialization,
save/reopen/editor moves, Undo, cancel, concurrency, transport/rates, source/context
loss and teardown remain required outcomes. No blank source text is filled from
memory, example or a different input mode. Broad version applicability remains
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

## Analyst evidence appendix

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/sources.json) reuses the exact reviewed inventory HTML/UTC/URL/
size/SHA identities, with no recapture. [Inventory pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/inventory-pins.json)
retain R1 manifest seal `67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73`,
its source catalog, blocks, parser and original source-page snapshot unchanged.
The mutable source-family page is a navigation route, not a frozen evidence pin.
[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/owner-pins.json), [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/counts.json),
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/manifest-author-r1.json) and read-only [validator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/validate.py)
identify this partial author packet and canonical snapshots.

| Alias | Retained source | Blocks |
| --- | --- | --- |
| OV | Public API overview |126|
| PATH | live.path |130|
| OBJ | live.object |170|
| OBS | live.observer |141|
| REM | live.remote~ |101|
| INIT | live.thisdevice |83|
| JS | JavaScript LiveAPI |142|

All 893 blocks are retained unchanged with source-local block, HTML line/column,
tag, anchor and section. Only the requirement-cited Live-specific text is adopted
as documentary role; common-box attributes and examples remain data. No figures,
linked sources, patch/scripts or code examples are executed. Shared index/coverage/
question/log integration belongs to root after independent semantic review.
