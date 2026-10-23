"""Analyst-only public-document catalog; no API, patch, Max or example execution."""
from pathlib import Path
from collections import Counter
import json
import hashlib

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert not (P / 'manifest-author-r1.json').exists(), 'Do not regenerate sealed bytes'
requirements, cases = [], []


def dump(name, value):
    (P / name).write_text(json.dumps(value, indent=2) + '\n')


def refs(text):
    return [f'{a}:B{int(n):04d}' for a, n in (r.split(':') for r in text.split())]


def case(cid, rid, title, kind, action, claim, blocks):
    visible = kind == 'control' and '-U-' not in rid
    cases.append(dict(id=cid, requirements=[rid], title=title, kind=kind,
                      preconditions=['common', 'active-positive-guard'], setup_and_action=action,
                      source_blocks=blocks, source_claim=claim,
                      documentary_expected='The named Use Persistent Mapping Inspector option is offered for the indicated bridge object; binding and persistence outcomes remain ungraded.' if visible else None,
                      documentary_comparator='Inspect only the named visible option and actual selected setting; no ID, persistence, message, timing or runtime equivalence oracle.' if visible else None,
                      expected=None, comparison=None, target_grade='U', executed=False))


def add(section, title, evidence, contract, action, kind='message-role'):
    n = len(requirements) + 1
    rid = f'REQ-LAPI-BRIDGE-{n:03d}'
    blocks = refs(evidence)
    requirements.append(dict(id=rid, section=section, title=title, provenance='D-current-public', target_applicability='U', contract=contract, source_blocks=blocks))
    case(f'LAB-{n:03d}', rid, title, kind, action, contract, blocks)


add('Paths and identity', 'Reachable public hierarchy', 'OV:4 OV:5 OV:6',
    'The public overview describes a hierarchy of Live objects with single children and object lists, exposing only part of Live. Reachability, available members and types must be independently established; the inventory is not all application internals or complete API closure.',
    'F-OBJECT: on an independently initialized owned patch and available Live context, identify one eligible ordinary object and its documented child using independently accepted path/metadata. Retain target/source identity; missing member does not prove generic failure.')
add('Paths and identity', 'Path syntax and relative context', 'OV:8 OV:9 OV:10 OV:11',
    'Overview paths are unquoted navigation terms with zero-based list indices; more than one path may identify the same object. Relative paths begin from current hierarchy position. These source roles do not prescribe a complete argument grammar, quote parser or native index encoding.',
    'F-PATH: identify a valid nonempty list/member and known current position, then compare accepted absolute and relative routes on reset copies. Retain actual path/object identity; no numeric ID or parser-output oracle.')
add('Paths and identity', 'Root families', 'OV:13 OV:14 PATH:100',
    'The overview/path reference names live_app, live_set, control_surfaces with an index and this_device as root roles. Control-surface access depends on the controller; this_device is device-relative. Root availability, identity and lifetime are not universal constants.',
    'F-PATH: retain accepted device/Set/application context and independently available root for each actually offered category; controller root requires accepted controller setup. Navigate only valid known roots; absent capability remains U.')
add('Paths and identity', 'Canonical path and parent roles', 'OV:16 OV:17 OV:19',
    'Multiple paths can lead to one object; the overview describes a unique canonical path, returned by live.object getpath, and a get-only canonical_parent child. Its own-track example is not an unconditional parent-is-track law for nested devices or roots.',
    'F-PATH/F-OBJECT: independently identify one object through two eligible routes, request canonical path/parent, then repeat with nested rack/device context only if available. Capture returned identity/path; no parent topology or ordering oracle.')
add('Paths and identity', 'Object IDs and no-object sentinel', 'OV:21 OV:22 OV:23 OV:24 OV:25',
    'The overview describes id plus integer tokens, with id 0 denoting no object, device-scoped IDs assigned when navigated, normally stable while an object exists, and possible move-as-delete/create exceptions. Deletion/replacement and nonreuse/nonstorage prose are documentary contexts, not target ID allocation or durable identity laws.',
    'F-IDENTITY: retain a positively resolved owned object and separate no-object context; move/reorder, duplicate and delete/recreate only owned objects on separate copies. Record actual paths/IDs without exact numbers, monotonicity, reuse, persistence or lifetime comparator.')
add('Paths and identity', 'Children, properties and call roles', 'OV:27 OV:28 OV:30 OV:31 OV:32 OV:33 OV:35 OV:36 OV:38',
    'Types describe available children/properties/functions; children may be single, lists or absent. getcount applies to lists, while get/set and call access eligible state/functions. Not all children/properties are observable or settable. Individual LOM member capability remains separately unresolved.',
    'F-OBJECT: independently establish one list, one existing single child, one absent child, one readable property and separately writable/observable/callable member. Probe each only with known admissible inputs; no complete member capability table is supplied.')
add('Paths and identity', 'Notifications versus polling', 'OV:60 OV:61 OV:62',
    'The overview distinguishes explicit navigation/get/call polling from spontaneous notifications for path-object changes and property values. This supplies event roles only, not cadence, coalescing, delivery order, queue policy or a complete notification set.',
    'F-OBSERVE: establish a valid object/property and positive explicit lookup and change baseline. Separately poll and change state through an accepted UI action; retain spontaneous versus requested messages without timing or count equality.', 'notification')
add('Paths and identity', 'Notification mutation context', 'OV:63 OV:107 OBS:4',
    'Overview and observer prose says Live Set changes cannot be triggered directly while receiving notifications, and suggests deferred interaction in relevant contexts. This is a documented restriction/caution, not a prescribed candidate thread, queue architecture or guaranteed deferlow cure.',
    'F-OBSERVE: with independently productive observed changes and a separately valid writable owned target, compare read-only handling and an attempted supported mutation from notification versus an independently available deferred action. No error string, scheduling or success oracle.', 'notification')
add('live.path', 'Navigation and path following outlets', 'OV:76 OV:80 OV:81 PATH:4',
    'live.path selects objects for other bridges; its left output gives navigation identity and middle output follows the object currently at the path. A nonexistent path is described as yielding no-object IDs rather than an error. Path following is distinct from retaining one particular object.',
    'F-PATH: positively resolve owned object, bind another bridge from the appropriate output in an independently valid patch, then change a dynamic selection and separately remove the pointed-to object. Capture identities/messages without callback order or numeric expected ID.')
add('live.path', 'Initial path and absolute path message', 'PATH:7 PATH:99 PATH:100',
    'live.path accepts an optional initial path and a path message for root-starting absolute paths. Root/name acceptance and initialization readiness remain target U; the initial argument is not proof of a ready Live API during patch load.',
    'F-INIT/F-PATH: after independently confirmed initialization compare explicit path navigation with a declared initial path on reset owned patch instances. Keep valid root/member fixed; do not use loadbang as readiness proof.')
add('live.path', 'goto relative/up and list-member boundary', 'PATH:102 PATH:103',
    'goto is documented for absolute or relative paths and up, selecting individual list members rather than the list itself. Its root list omits this_device while other source contexts include it; the omission does not settle that root’s goto acceptance.',
    'F-PATH: valid nonempty current object/list and admitted member first, then compare relative child, up and list-container versus member requests in separate trials. Probe this_device only as unresolved context, no generic refusal or repair oracle.')
add('live.path', 'Count and child enumeration', 'PATH:63 PATH:64 PATH:69 PATH:72 PATH:73 PATH:78',
    'getcount reports a named list child’s count via the right outlet; getchildren reports available child names there. These are documented output roles, not stable list ordering, inherited-member closure or exact tuple/empty representation for target builds.',
    'F-OBJECT/F-PATH: known valid nonempty list and independent child inventory, then empty-list copy. Request count/children and retain raw output with actual source structure; no numeric count or order comparator.')
add('live.path', 'Current path response', 'PATH:80 PATH:81 PATH:86',
    'live.path getpath reports its current navigation path via the right outlet. This differs from live.object canonical getpath and does not require path spelling to match a canonical alias.',
    'F-PATH: identify two accepted aliases for same owned object and a valid relative navigation; request path and separately object canonical path on reset trials. Retain strings without quote, normalization or alias-equality oracle.')
add('live.path', 'Combined bang/getid documented role', 'PATH:88 PATH:89',
    'The combined bang, getid section describes emitting current-path identity through left and middle outputs, with no-object sentinel when absent. The separate standalone getid section is a placeholder and remains unsupported; no blank is filled from memory.',
    'F-PATH: independently valid current object then a known nonexistent path, invoke the explicitly documented combined-section context and retain outputs. Standalone placeholder interpretation and outlet sequencing are separate U probes.')
add('live.object', 'Select current object by ID', 'OBJ:4 OBJ:61 OBJ:62',
    'live.object operates on selected Live objects; id assignment is described for either inlet, with right-inlet use suggested for clarity and no assignment output described. This is not input routing, ID scope or rejection parity for arbitrary tokens.',
    'F-OBJECT: retain positive readable target resolved in same independently valid device context, bind through each actually supported inlet in separate copies, then inspect current binding via an independent query. Numeric/message-order/error outputs remain null.')
add('live.object', 'Current identity and type', 'OBJ:59 OBJ:60 OBJ:71 OBJ:72 OBJ:81 OBJ:82',
    'getid or bang/getid reports current identity and gettype its object class; getid describes no-object when unbound. These output roles do not specify every invalid/deleted-ID branch, exact names or message interleaving.',
    'F-OBJECT: independently valid bound target and separate unbound instance; request identity/type and capture raw responses. Delete only owned target in separate U trial; no expected numeric ID or type-completeness oracle.')
add('live.object', 'Canonical getpath and getinfo roles', 'OBJ:63 OBJ:64 OBJ:79 OBJ:80',
    'getpath reports canonical current-object path. getinfo describes identity/type/description/children/properties/functions and a terminating done role, with repeatable description lines. No fixed line order/cardinality or complete inherited-member specification follows.',
    'F-OBJECT: positive valid object, request path/info, retain full raw response and separately known identity. Repeat a second supported object type; do not compare against the 588 direct-heading inventory as a complete runtime surface.')
add('live.object', 'Read child versus child list', 'OBJ:115 OBJ:116 OBJ:121 OBJ:124 OBJ:125 OBJ:130',
    'get on an eligible list child reports element IDs; on a single child it reports that child ID. Source examples are not exact runtime IDs, alias names, empty-list formatting or universal child availability laws.',
    'F-OBJECT: valid object with independently known single child and nonempty list, query each then an empty/absent copy. Retain actual returned tokens only; no list order/count/ID expected value.')
add('live.object', 'Read value versus value list', 'OBJ:133 OBJ:134 OBJ:139 OBJ:142 OBJ:143 OBJ:148',
    'get reads single-value and list properties, with types and capabilities delegated to the LOM. Example routing labels, names and numbers do not override current native/domain owners or define a complete return grammar.',
    'F-OBJECT: independently readable scalar and list property on owned eligible objects; request each at two admitted states. Capture raw values/labels without native-enum, stored-unit, quoting or numeric equality oracle.')
add('live.object', 'Set child versus child list', 'OBJ:99 OBJ:100 OBJ:103 OBJ:104',
    'set has separate single-child and child-list roles accepting eligible object identities. Not all children are writable; no assignment response is described. Complete mutation, list ordering, cross-device IDs and rollback remain U.',
    'F-MUTATE: independently verified writable owned child/list capability and valid same-context identities, positive readback first; perform one admitted change then restore only through accepted actions. No hidden writable member or transaction/silence law is invented.')
add('live.object', 'Set property versus value list', 'OBJ:107 OBJ:108 OBJ:111 OBJ:112',
    'set writes eligible single/list property values; not all properties can be set and their types come from the LOM. No assignment response is described. Bounds, clamping, serialization, automation ownership and numerical conversion require separate evidence.',
    'F-MUTATE: separately admitted writable scalar/list property and independently valid values with positive target/readback baseline; attempt each on reset copies. Unavailable capability remains unmet prerequisite; no value, error or undo comparator.')
add('live.object', 'Function call role', 'OV:38 OBJ:89 OBJ:90 OBJ:95',
    'call names a current-object function and optional typed parameters, with result output described by the public source. Actual callable members, signatures, side effects, return types and errors are not completed by this generic bridge clause.',
    'F-MUTATE: independently known supported callable member on disposable owned object and admissible argument set, with observable positive baseline first. Capture return and owned before/after state, no source example executed or generic function semantics inferred.')
add('Persistence', 'Persistent Mapping Inspector option', 'OBJ:152 OBJ:153 OBS:123 OBS:124 REM:81 REM:82',
    'live.object, live.observer and live.remote~ references name an Inspector Use Persistent Mapping option. Its save/restore/editor-move association prose is retained separately from overview/JS dynamic-ID cautions; default, cross-run numeric ID and exact-target persistence remain U.',
    'F-PERSIST: independently available initialized bridge and valid binding; inspect named option for each of the three bridges and retain actual selected state. Save/reopen/editor-move effects are separate null probes, not this visible-option comparison.', 'control')
add('live.observer', 'Observe eligible property and changes', 'OBS:4 OBS:7 OBS:61 OBS:62',
    'live.observer selects an eligible object/property and describes initial/current value plus later change notifications through its left output. An optional argument selects property/child. Not all properties are observable and notification timing/count/order are unproven.',
    'F-OBSERVE: independently supported observable property and same-context valid object; positively read value, select observation and change property through admitted external UI action. Capture current/change output without immediate-delivery or exactly-once oracle.', 'notification')
add('live.observer', 'Observe single child versus child list', 'OBS:70 OBS:71 OBS:79 OBS:80',
    'Observer property selection can target an observable child ID or child list; single-child source mentions no-object and list source permits no output for an empty result. Capability and representation differ and are not generalized to every child.',
    'F-OBSERVE: independently eligible single child/list and positive nonempty observation, then separate empty/absent states through owned UI changes. Retain actual responses, not a universal silence, list or ID comparator.', 'notification')
add('live.observer', 'Binding and bang role', 'OBS:112 OBS:113 OBS:120 OBS:121',
    'Observer ID assignment accepts either inlet with right suggested; bang queries current selected property/object. The source describes no action without matching property/object, but invalid tokens, deleted objects and no-effect behavior remain target U.',
    'F-OBSERVE: establish active valid observation and nonzero positive changing target first, then separate no-property/no-object/mismatched context and bang. Retain matched positive response; missing baseline cannot prove no-effect.')
add('live.observer', 'Observer metadata outputs', 'OBS:88 OBS:89 OBS:96 OBS:97 OBS:104 OBS:105',
    'getproperty, gettype and getid describe current selection/type/identity through observer right output, distinct from value output left. Child-list type information is described as limited; no complete typed schema or cross-outlet order follows.',
    'F-OBSERVE: valid property, single child and list selections separately; query metadata while keeping independently positive observation. Capture raw right/left outputs without enum, type-union or event-order expected value.')
add('live.remote~', 'DeviceParameter binding and release', 'REM:4 REM:6 REM:75 REM:76 REM:78 REM:79',
    'live.remote~ binds a DeviceParameter identity through the right inlet, describes no effect for non-parameter IDs, reports mapped identity via getid, and uses id 0 to release control/re-enable parameter. Nonparameter rejection, release ordering and restoration stay U.',
    'F-REMOTE: independently eligible DeviceParameter with active nonzero input/base/output and known working remote response first; compare valid, separately known nonparameter and release contexts on reset copies. No hidden ID/class mapping or release-time/value oracle.', 'signal')
add('live.remote~', 'Parameter LOM path UI entry', 'REM:6',
    'The reference describes Copy LOM Path in a parameter context menu as available in Live 12, and live.path or live.map as ways to select a parameter. This does not specify the separate live.map object, exact path alias, menu eligibility for every control or target-build support.',
    'F-REMOTE: independently admitted editable/eligible parameter and initialized owned context; inspect actually offered Copy LOM Path and retain copied text separately from accepted binding. No clipboard grammar or full live.map contract is supplied.')
add('live.remote~', 'Message and signal control roles', 'REM:6 REM:63 REM:64 REM:66 REM:67 REM:73 REM:74',
    'Integer/float messages and signal input address the selected parameter through left inlet. Source prose distinguishes buffer/ramp scheduling from realtime signal application; sample-accurate/single-buffer claims are context, not target timing or candidate architecture requirements.',
    'F-REMOTE: active eligible parameter, independently valid nonzero signal/message path and positive source/output baseline. Compare each input family at two admitted values and actual supported rate/block settings separately; numeric/timing/signal responses null.', 'signal')
add('live.remote~', 'Ramp and smoothing controls', 'REM:10 REM:11 REM:69 REM:70',
    'smoothing describes event ramp time and signal temporal sampling; a value/time list requests a ramp and a new ramp overrides a current ramp. No source default/example is promoted to target interpolation, sample count, rate law or interruption arithmetic.',
    'F-REMOTE: known active positive remote path and admitted nonzero ramp settings; request one ramp then another during it, separately change actually offered smoothing. Capture control/audio traces with no linearity, latency, count or numerical output oracle.', 'signal')
add('live.remote~', 'Normalized-mode role', 'REM:12 REM:13',
    'normalized toggles between source-described automatic parameter-range scaling and caller-supplied parameter-domain values. This is not a conversion formula, native/stored-unit equivalence, valid range for every target or complete parameter behavior law.',
    'F-REMOTE: independently known eligible parameter and admitted input/base/depth in both actual offered modes, positive remote response and output first. Capture mode/values without assuming native min/max/enum/gain conversion or clipping.', 'signal')
add('live.remote~', 'Automation, undo and envelope context', 'OV:87 REM:6',
    'Remote control is described as disabling parameter interaction/automation without changing saved Set value or creating Undo steps, while reference prose also says envelopes remain active. Automation versus envelope identity and restoration are unresolved contexts, not a blanket disable-all law.',
    'F-REMOTE/F-AUTO: independently active eligible parameter with nonzero source/output and separately changing automation/modulation baseline, explicit transport and recording state. Bind/drive/release remote on reset copies, retain exposed state/history/output with no arbitration or persistence oracle.', 'signal')
add('live.thisdevice', 'Initialization and reload notification', 'OV:100 INIT:4 JS:4',
    'live.thisdevice describes left-outlet bang when the Max device/containing patcher is opened and completely initialized, including Live API in the JS/overview context, and again for preset load or device save/reload. Generic loadbang is not proof of Live API readiness.',
    'F-INIT: independently accepted owned device/patch and Live context; retain device load, preset load and save/reload as separate trials with readiness observation. No patch is created/executed here and no callback time/count/order oracle is supplied.', 'notification')
add('live.thisdevice', 'Enabled and preview state context', 'INIT:4 INIT:60 INIT:61',
    'Description distinguishes device-enabled middle output and preview right output in Live, with inactive state outputs when used in Max alone. getstate text says device state on rightmost output, leaving exact state meaning/context unresolved rather than merging enabled and preview.',
    'F-INIT: independently accepted in-Live device then separate valid editor/Max context if available, known enabled/preview state and positive output first. Change each state and request getstate; raw numeric/outlet/order outputs remain null.', 'notification')
add('live.thisdevice', 'Explicit bang and mouse entry', 'INIT:56 INIT:57 INIT:58 INIT:59 INIT:62 INIT:63',
    'Explicit bang, double-click and loadbang message roles describe left bang output. Those manual/message actions do not imply the device/API has reached the automatic complete-initialization condition.',
    'F-INIT: independently ready owned device first, then separate not-yet-established context only if observable. Compare explicit message and double-click to automatic load notification, retaining readiness separately without equating them.', 'notification')
add('live.thisdevice', 'Device width message and save caveat', 'INIT:64 INIT:65',
    'setwidth changes Max for Live device width and its source says this is not automatically saved in preset/Set; the reset setting returns width calculation from visible objects. Exact pixels/default sizing, persistence mechanism and unrelated layout behavior remain unknown.',
    'F-INIT: independently valid visible device with retained layout, use two actually admitted widths and offered reset separately, then save/reopen as U branch. No pixel, stored width or atomic resize comparator.')
add('JavaScript LiveAPI', 'Initialized JavaScript access context', 'JS:3 JS:4 JS:5 JS:6 OV:90',
    'LiveAPI offers js access to path/object/observer roles, with source cautions against global-code use and high-priority execution and a live.thisdevice readiness recommendation. Legacy constructor context is retained. No JS engine version, scheduler architecture or full runtime compatibility is imposed.',
    'F-JS/F-INIT: independently valid owned js-containing patch and accepted Max/Live configuration, initialized via accepted lifecycle context. Inspect offered API access separately from global/premature use; no script or example is executed in this packet.')
add('JavaScript LiveAPI', 'Constructor and callback roles', 'JS:31 JS:32 JS:33 JS:39 JS:42',
    'Constructor accepts optional callback and path or valid API identity; callback is described for referred-object or observed-property changes. Complete overload grammar, callback values/reentrancy and cross-instance ID acceptance are unresolved.',
    'F-JS: independently valid initialized owned patch with eligible path/object and positively changing observable property. In separate accepted instances compare callback/path/identity contexts, retaining invocation/data without constructing a source example or imposing order.', 'notification')
add('JavaScript LiveAPI', 'Follow-object versus follow-location modes', 'JS:109 JS:110 JS:111',
    'LiveAPI mode distinguishes following the particular referred object across movement from following the object occupying a hierarchy location. Source defaults/examples are not exact-target numeric mode, move-as-recreate, ID lifetime or bank-selection laws.',
    'F-JS/F-IDENTITY: two independently identified owned tracks/devices, accepted modes and positive binding before reorder. Compare object/location after each separate move and replacement; mode codes and callback/ID results stay null.')
add('JavaScript LiveAPI', 'Path, ID and validity properties', 'JS:96 JS:97 JS:105 JS:106 JS:114 JS:115 JS:116 JS:138 JS:139 JS:140 JS:141 JS:142',
    'goto navigates and reports object/no-object through callback; id is dynamic and not to be reused across runs per JS text. path and unquotedpath distinguish quoting and are Set-dependent; valid describes whether a Live object is referred to. Complete grammar, validity timing and persistent bindings remain U.',
    'F-JS/F-PATH: positive valid object/path, alternate quoted/unquoted representation and accepted nonexistent path in separate trials. Reopen Set and re-resolve as U branch; no stored-ID equality, raw grammar or transient-validity comparator.')
add('JavaScript LiveAPI', 'Children and info/type metadata', 'JS:58 JS:59 JS:72 JS:73 JS:107 JS:108 JS:112 JS:113 JS:135 JS:136',
    'children/getcount expose current-path child information; info/type describe object metadata and patcher identifies containing context. These bridge roles do not complete inherited member semantics, child cardinalities, source code architecture or exact class/type unions.',
    'F-JS/F-OBJECT: independently known valid object and separately nonempty/empty child lists, request supported metadata in accepted initialized context. Capture raw types/arrays/counts without full-schema or numeric expected result.')
add('JavaScript LiveAPI', 'get, getstring, set and call roles', 'JS:43 JS:44 JS:60 JS:61 JS:62 JS:84 JS:85 JS:86 JS:123 JS:124',
    'JS get/getstring read property values/lists with distinct described representations; set writes and call invokes eligible members. Printed get type annotation is narrower than the generic description; complete return unions, member signatures, type conversion and errors require separate evidence.',
    'F-JS/F-MUTATE: independently admissible readable scalar/list/symbol and separately writable/callable owned members, with positive baseline. Compare get/getstring and one accepted write/call on reset copies; no script, source example or generic type parser is invented.')
add('JavaScript LiveAPI', 'Observed property and type', 'JS:117 JS:118 JS:119 JS:120 JS:121 JS:122',
    'property selects an observed property, child or child list and proptype describes selected type; callback changes are documented roles only. Capabilities, initial callback timing, mutation while handling and stale targets remain unresolved.',
    'F-JS/F-OBSERVE: independently eligible observable property/child/list and positive binding/change baseline; select and externally mutate each separately. Capture callback/proptype without exactly-once, ordering or read/write-in-callback success oracle.', 'notification')

unknowns = [
 ('VERSION', 'Version, members and source contexts', 'Current LOM index declares Live12.4.5; bridge Max versions are unpinned. Exact12.4.3 applicability, complete 45-reference/588-direct-member/inherited capabilities, aliases, roots and source-context discrepancies remain U.'),
 ('IDENTITY', 'ID, root and persistence lifecycle', 'Overview/JS dynamic/nonstored IDs versus optional Persistent Mapping save/editor-move prose are not reconciled into one lifetime law. Root/device/Set scope, deletion/reorder, invalid/stale/cross-device IDs, path aliases and reopened bindings need evidence.'),
 ('GRAMMAR', 'Argument, type and error grammar', 'Malformed paths/quotes, unknown names, child/list capability, overloaded messages/functions, callback/result types, nonfinite/out-of-range values and read-only/nonobservable outcomes have no new complete parser, diagnostic or repair law.'),
 ('ORDER', 'Scheduling, notifications and reentrancy', 'Delivery/count/coalescing/order across outlets/callbacks, notification-time reads/mutations, initialization races, remote ramp/buffer/sample timing and rate/transport transitions remain unknown. No thread/queue architecture or latency mandate follows.'),
 ('REMOTE', 'Signal and parameter ownership', 'Remote normalization/smoothing/ramp, no-effect nonparameter tests, automation/modulation/manual control, saved value and release restoration need independently positive active paths and remain numerically ungraded.'),
 ('STATE', 'History, cancellation and durable state', 'Save/reopen, migration, preset/editor moves, Undo/Redo grouping, cancellation, concurrent mutations and persistent-mapping default/state consequences remain U beyond source roles.'),
 ('LOSS', 'Unavailable context and source loss', 'Object/property/device/track/Set/patcher/controller/media/engine disappearance, observer invalidation, unbinding/rebinding and recoverability require evidence. Missing API/Max capability is an unmet prerequisite, not a refusal or silence pass.'),
 ('TEARDOWN', 'Teardown and pending work', 'Device/patch/Set close, Live/editor transition or quit with active observer/callback/remote ramp/control has no established flush, cleanup, completion, crash or silence deadline.')
]
for suffix, title, contract in unknowns:
    requirements.append(dict(id=f'REQ-LAPI-BRIDGE-U-{suffix}', section='Unknown obligations', title=title, provenance='U', target_applicability='U', contract=contract, source_blocks=[]))
probes = [
 ('VERSION','placeholder','source-context','F-PATH: keep standalone live.path getid TEXT_HERE distinct from combined bang/getid section. Retain actual offered context only in independently valid future patch; no missing semantics inferred from memory or combined section.'),
 ('VERSION','root-context','source-context','F-PATH: independently valid this_device context and accepted ordinary root first; compare path versus goto and current/up in nested device/chain/root contexts. No own-track parent, universal root lifetime or omitted-root refusal is assumed.'),
 ('IDENTITY','persistence','persistence','F-PERSIST: positively bind each object/observer/remote separately, record actual Persistent Mapping on/off, save/reopen and editor/device moves in distinct copies; compare JS dynamic IDs separately. Capture association/path/ID without cross-run equality or nonstorage law.'),
 ('IDENTITY','move-delete','boundary','F-IDENTITY: two owned positive objects; reorder/move, duplicate, delete/recreate and replace at same path in separate trials, then re-resolve. Preserve device/Set/root/mode context; no exact ID allocation/reuse or callback-order comparator.'),
 ('GRAMMAR','invalid-input','malformed','F-PATH/F-OBJECT: after a valid positive request attempt abc/empty/quoted/incomplete paths, wrong arity/type and NaN/out-of-range values only through independently understood accepted interfaces on test-owned targets. No arbitrary LOM member or hidden input codec is invented.'),
 ('GRAMMAR','capability','negative','F-MUTATE/F-OBSERVE: retain independently valid writable/observable baseline, then separately inspect known read-only/nonobservable/unsupported member or absent child. Failed prerequisite or nonexistent feature cannot prove all-request no-effect; diagnostic/output null.'),
 ('ORDER','callback-mutation','notification','F-OBSERVE/F-JS: independent changing eligible observation and separately valid owned writable target with positive baseline; compare read/mutation in spontaneous callback versus accepted later action. No private-thread requirement, deferlow success, error text or event order oracle.'),
 ('ORDER','load-state','notification','F-INIT: compare initialized auto-load callback with manual bang/loadbang, save/preset reload and separate enabled/preview changes plus getstate. Retain actual Live versus editor/Max context; no outlet-state identity or immediate readiness guarantee.'),
 ('ORDER','transport-rates','sample-rate','F-REMOTE/F-OBSERVE: known valid nonzero positive signal/envelope/observer baseline, explicit running/stopped transport; compare stop/start/seek/tempo/loop and separately accepted 44.1/48/96kHz and64/512-frame contexts. No cadence, buffer latency, smoothing or phase equivalence law.'),
 ('REMOTE','ownership','automation','F-REMOTE/F-AUTO: known eligible parameter and active changing nonzero automation/modulation plus nonmuted source/wet output; drive then release and re-enable through owner controls on reset copies. Capture manual/automation/remote/undo/saved state without merging envelopes and automation or numerical identity.'),
 ('REMOTE','nonparameter-release','negative','F-REMOTE: independently productive DeviceParameter control with active nonzero source/base/depth/output first. Compare accepted nonparameter/invalid/unbound identities and id0 release separately, preserving paired positive baseline. No missing output or stale prior parameter proves no-effect.'),
 ('STATE','undo','undo','F-MUTATE: before-inventory of owned target/path/binding, perform one valid get/set/call/observer/remote or persistence change per reset copy then offered Undo/Redo. No generic history grouping or saved-value restoration law.'),
 ('STATE','cancel','cancel','F-MUTATE/F-REMOTE: begin actually offered parameter/patch edit, ramp or mapping selection and use supported cancellation/release before and after recorded commit in separate copies. No asynchronous API cancel command or rollback is invented.'),
 ('STATE','concurrency','concurrency','F-OBJECT/F-OBSERVE: independently valid object and positive observation/change, then overlapping external edit/reorder/selection while a request or ramp is pending in separate copies. No snapshot consistency, atomicity or caller priority law.'),
 ('LOSS','target-loss','source-loss','F-OBJECT/F-OBSERVE/F-REMOTE: established positive valid target/binding/output first, delete only owned parameter device, clip/track or replace Set while active. Retain path/ID/observations and other active paths; no observer-reset, restoration or silence deadline.'),
 ('LOSS','context-recovery','recovery','F-INIT: independently available accepted Live/editor context first; make only owned patch/context temporarily unavailable through supported controls, restore then re-resolve valid paths. No Max installation, fake host/API, recoverable-ID assumption or synthesized runtime is used.'),
 ('TEARDOWN','close-pending','teardown','F-REMOTE/F-OBSERVE: positive active callback/observer or nonzero remote ramp/output; separately close device/patch, save-and-edit transition, close/replace Set or quit through offered controls. Capture prompts/output/state if available; no flush/cleanup/transaction deadline.')
]
for suffix,label,kind,action in probes:
    case(f'LAB-U-{label.upper()}', f'REQ-LAPI-BRIDGE-U-{suffix}', label.replace('-',' ').capitalize(), kind, action, None, [])
assert len(requirements)==len({r['id'] for r in requirements})
assert len(cases)==len({c['id'] for c in cases})
dump('requirements.json',requirements)
dump('cases.json',cases)
counts=dict(requirements=len(requirements),requirement_grades=dict(Counter(r['provenance'] for r in requirements)),cases=len(cases),case_kinds=dict(Counter(c['kind'] for c in cases)),documentary_oracles=sum(c['documentary_expected'] is not None for c in cases),null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases),retained_sources=7,retained_blocks=893,target_oracles=0)
dump('counts.json',counts)
owners = ['max-for-live-hosting.md', 'automation-envelopes.md', 'automation-workflows.md', 'mix-graph.md', 'mixer-values.md', 'transport-state.md', 'playback-core.md', 'clip-view-workflows.md', 'session-view-workflows.md', 'routing-monitoring-latency.md', 'midi-user-mapping.md', 'device-racks.md', 'bundled-device-parameters.md', 'warp-markers.md', 'mpe-workflows.md', 'tuning-systems.md', 'live-set-structure.md']
pins=[]
for name in owners:
    path=ROOT/'wiki/specs'/name
    raw=path.read_bytes()
    pins.append(dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),purpose='Existing canonical owner unchanged; not API runtime or normalization evidence'))
dump('owner-pins.json',pins)
dump('fixtures.json',{
 'common':'Future finite contexts only: independently valid test-owned patch/device and actually available accepted Live/Max/editor configuration, exact versions/platform/entitlement and Live API initialization retained. No patch, JavaScript program, API execution or host capability is supplied. Reset copies of disposable valid owned Set with actual selected device/track/clip and source/binding before-state, transport/record/arm/monitor/automation and input ownership declared. Missing Live/Max/API or member capability leaves U, never pass.',
 'F-PATH':'Independently established valid roots and eligible object paths in accepted initialized same-device Live context, including known nonempty child list/member and separate existing/absent single child. Retain current navigation position, aliases and actual corresponding object identities. Control-surface root requires independently supported available controller; this_device needs actual device context. No source example, path spelling normalization or complete namespace is assumed.',
 'F-OBJECT':'Independently identified owned object with valid accepted same-context ID/path and actual readable metadata/property plus child/list capability established. Positive successful readable binding before no-object/invalid tests; names/types/capabilities are separately validated rather than guessed from 45 references or588 direct headings.',
 'F-IDENTITY':'Two independently identified owned nonempty objects with retained positive binding/path and before-order. Each move/reorder/duplicate/delete/recreate uses reset disposable copies; identify actual object versus position independently. No exact ID allocation, reuse, persistence or cross-device equality assumed.',
 'F-MUTATE':'Open prerequisite: independently known supported writable/callable member on disposable owned object with actually accepted type/arguments, positive readback/observable effect and valid binding first. Two admitted distinct values where applicable. No arbitrary child setter, hidden member, function/argument recipe or root mutation is invented. Read-only/unsupported cases need separate independently known capability status.',
 'F-OBSERVE':'Independently supported observable property, single child or child list and valid same-context object/ID; first retain current readable state and positive external UI change/notification baseline. Distinguish spontaneous from requested output and property versus ID/list values; no exactly-once or immediate delivery assumed. No monitor/patch is executed here.',
 'F-REMOTE':'Independently accepted DeviceParameter and initialized valid binding, enabled active eligible instrument/effect/mixer path, readable nonzero base and admitted nonzero source/control/signal/depth/amount/gain/send, correct track/receiver arm/monitor/clip and nonmuted positive wet/output baseline. Positive remote response confirmed independently before invalid/nonparameter/unbind tests. Numeric domains and normalization are established separately; no source0..1 volume example is imported as gain law.',
 'F-AUTO':'Independent active changing automation and separate modulation/manual-control baseline on actually supported parameter, nonzero source/base/depth/amount and positive nonmuted output. Explicit running/stopped transport and recording/Automation Arm state; re-enable and remote binding/release remain distinct accepted controls. Generic automation/stored/evaluator owners keep their existing conditions.',
 'F-INIT':'Independently valid owned Max device/patch and available Live API context, explicit device load/save/preset/editor mode and actually observed ready state. Compare automatic initialization versus manually triggered bang separately. Host/editor save/dependency behavior remains with Max hosting; no patch/code is produced or run.',
 'F-JS':'Open prerequisite: independently valid owned js-containing patch and accepted LiveAPI implementation/version in initialized Live context. Actually known eligible constructor/path/binding and observable/readable/writable/callable capability retained before probes. No example or new JavaScript/Max script is created, evaluated or executed, and unsupported JS context remains U.',
 'F-PERSIST':'Independent positive same-context binding for each offered object/observer/remote bridge; retain actual Use Persistent Mapping option/state and source target identity. Reset copies before Save/reopen, preset and editor/device moves; compare association, path and raw ID separately. JS dynamic IDs not equated with Inspector mapping. No constructor default or ID lifetime is assumed.',
 'active-positive-guard':'Require independently valid owned patch and actually available initialized Live/Max/API context, eligible existing object/path/ID and separately admitted readable/writable/observable/remote member before each relevant action. Establish positive binding/response and externally known state/change first. Audio/remote/no-effect probes additionally require active eligible parameter/section, nonzero source/base/depth/amount/gain/send and nonmuted positive wet/output with correct arm/monitor/receiver/clip and explicit transport/record state. Change only tested input after matched positive baseline. Missing context/object/capability, muted output, zero signal or stale prior binding cannot prove no-effect or pass. Future fixture requirements authorize no runtime, patch, API, hardware or installation.',
 'not_provided':['No original Live/Max application, API call, patch or JavaScript execution','No candidate, protocol emulator, private host shim or implementation','No retained API responses/audio/MIDI/notification traces or accepted host/patch','No ID numeric equality, message order, type grammar, gain/tempo/warp law, time/signal comparator or tolerance']
})
base='../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-bridge/'
spec='''---
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
not a pinned Live12.4.3/Max runtime. The source inventory's LOM index explicitly
declares **Live 12.4.5**, after the target; the overview and bridge pages do not
establish a matching Max version. Every new target applicability remains **U**.
All target expected/comparison fields are null, all target grades U and all cases
unexecuted. Message, ID, numeric, timing, signal and callback outcomes also have
null documentary expectations/comparators; source_claim is separate. Only the
named Inspector option has a visible-control proposal, without binding proof.

The [reviewed source inventory](../research/sources/cycling74-live-api.md) discovers
45 LOM references and588 explicit direct declarations; all member semantics,
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
and older finite/native enum scopes. Public examples of volume0..1, timing,
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
'''
for section in ['Paths and identity','live.path','live.object','Persistence','live.observer','live.remote~','live.thisdevice','JavaScript LiveAPI','Unknown obligations']:
    spec+=f'\n## {section}\n'
    for r in requirements:
        if r['section']!=section:continue
        spec+=f"\n### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
        if r['source_blocks']:
            spec+='Evidence: '+', '.join(f'[{ref}]({base}source-blocks.json)' for ref in r['source_blocks'])+'.\n'
        else:spec+='Evidence: unsupported outcome; ungraded investigation obligation.\n'
spec+=f'''
## Finite future cases

[{len(cases)} cases]({base}cases.json) map to [{len(requirements)} requirements]({base}requirements.json):
44 current-public documentary clauses and eight U obligations. One case compares
the named Inspector option only;60 have null documentary oracles. All61 target
outcomes/comparators are null/U/unexecuted. Even documented message formats are
source_claim context, not executable acceptance or complete argument grammar.
Each overloaded message, bridge/member/host branch needs its own retained result
before closure. No complete API entry or original-versus-candidate pass is claimed.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
'''
for c in cases:spec+=f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |\n"
spec+=f'''
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

[Sources]({base}sources.json) reuses the exact reviewed inventory HTML/UTC/URL/
size/SHA identities, with no recapture. [Inventory pins]({base}inventory-pins.json)
retain R1 manifest seal `67e24da58fb1d91d8c55659c65eb0779a3c3e8cc2424ddcf07915032d8637a73`,
its source catalog, blocks, parser and original source-page snapshot unchanged.
The mutable source-family page is a navigation route, not a frozen evidence pin.
[Owner pins]({base}owner-pins.json), [counts]({base}counts.json),
[manifest]({base}manifest-author-r1.json) and read-only [validator]({base}validate.py)
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

All893 blocks are retained unchanged with source-local block, HTML line/column,
tag, anchor and section. Only the requirement-cited Live-specific text is adopted
as documentary role; common-box attributes and examples remain data. No figures,
linked sources, patch/scripts or code examples are executed. Shared index/coverage/
question/log integration belongs to root after independent semantic review.
'''
spec=spec.replace('Live12.4.3','Live 12.4.3').replace('and588','and 588').replace('volume0..1','volume 0..1').replace('only;60','only; 60').replace('All61','All 61').replace('All893','All 893')
(ROOT/'wiki/specs/live-api-bridge-workflows.md').write_text(spec)
(P/'spec-r1.md').write_text(spec)
research=f'''---
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
is pinned to reviewed [R1 inventory]({base}../max-api/manifest-inventory-r1.json)
and its original immutable snapshot. That LOM index explicitly declares Live12.4.5,
after target12.4.3. Overview/bridge current Max versions do not establish a matching
runtime. D-current-public means publication text only; all new target applicability U.
The45 LOM references/588 direct headings, inherited members and full member/type/
event signatures remain separate; no complete API entry is claimed.

## Retained evidence and bounded reading

[Sources]({base}sources.json) reuses seven exact source identities from the
reviewed max-api catalog: overview and path/object/observer/remote~/thisdevice/
JavaScript LiveAPI. Original publisher URL/final URL, UTC capture, size and SHA
are retained without recapture. No max-api file or source-family canonical is
edited. [Inventory pins]({base}inventory-pins.json) retains five R1 artifact
identities and [blocks]({base}source-blocks.json) preserves893 exact source rows
with original block/HTML line/column/anchor/section. A [text view]({base}source-blocks.txt)
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

Public examples of0..1 volume, master_track, routing labels or time conversions
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

There are52 requirements:44 D-current-public and eight U, with61 proposed cases.
One visible option-presence proposal has a documentary comparator;60 are null,
including all message/ID/numeric/notification/timing/signal and wholly unknown
probes. Every target expected/comparison is null/U/unexecuted. source_claim is
retained separately, never an expected output or API call trace. No full bridge,
LOM member, hardware/profile or complete Max runtime is closed.

[Fixtures]({base}fixtures.json) require independently valid owned patch and
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

[Owner pins]({base}owner-pins.json) retain17 existing canonical boundary identities;
[manifest]({base}manifest-author-r1.json) seals this packet's source references,
derived blocks, catalogs, cases, fixtures, author/validator and canonical snapshots.
The [validator]({base}validate.py) is read-only before/after seal: all65 original
inventory R1 payload hashes, seven source identities,893 block equality/reproduction,
owner pins, exact requirement/case/browser IDs, null oracles, snapshots, local links/
anchors, manifest inventory and untracked-aware whitespace. It prints stdout only.
Later inventory/source-page revisions may coexist; frozen R1 bytes remain evidence.

Independent semantic review is required; no Max/API/runtime, implementation,
compatibility or complete feature claim follows from integrity checks. Root
integrates shared indexes, coverage, questions and log; this author edits none.
'''
for old,new in [('Live12.4.5','Live 12.4.5'),('target12.4.3','target 12.4.3'),('The45','The 45'),('preserves893','preserves 893'),('of0..1','of 0..1'),('are52','are 52'),(':44',': 44'),('with61','with 61'),(';60','; 60'),('retain17','retain 17'),('all65','all 65'),('identities,893','identities, 893')]:research=research.replace(old,new)
(ROOT/'wiki/research/live-api-bridge-workflows.md').write_text(research)
(P/'research-r1.md').write_text(research)
print(json.dumps(counts,indent=2))
