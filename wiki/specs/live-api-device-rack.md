---
id: SPEC-LIVE-API-DEVICE-RACK
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public LOM index12.4.5 applicability U
---

# Public Live API device, rack and mixer members

## Scope and version boundary

This partial F-05/F-08 analyst draft selects exactly ten retained R1 public LOM
references: Device, Device.View, DeviceParameter, MixerDevice, RackDevice,
RackDevice.View, Chain, ChainMixerDevice, DrumChain and DrumPad. The requested
Chain.View is absent from that inventory and is not invented. SimplerDevice/View,
Track and other specialized classes remain separately owned; they are excluded.
[Research](../research/live-api-device-rack.md) records source limits;
[coverage design](../research/full-live-specification-design.md) governs closure.
This is not a released input, complete device/API family or compatibility result.

**D-current-public** means a bounded direct declaration/role in the immutable
publisher reference captures, not observed Live behavior. The original inventory
index explicitly declares **Live12.4.5**, later than target12.4.3; matching Max and
platform/member availability are not established. Source since-version prose is
retained without assuming target presence. Every target applicability is **U**.
All actual API, numeric, message, callback, signal and timing documentary oracles
are null, with source_claim context only. All target expected/comparison fields
are null, grades U, cases unexecuted and complete flags false.

## Exact direct-member denominator

The [denominator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/denominator.json) lists every selected original R1
reference/member identity. The [member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/member-ledger.json)
retains exact direct headings, categories, source types/access, spans/HTML locators,
explicit typed arguments, typed returns and units. It maps95 direct declarations
(25children/53properties/17functions) to95 requirements, with zero unlinked IDs.
There are94 bounded documentary roles and one heading-only semantic U:
DrumPad.delete_all_chains. **Zero unlinked IDs is not complete behavior**: all95
actual target member behaviors remain unclosed. Eight cross-cutting U obligations
bring this packet to103 requirements (94 D-current-public/9 U) and113 future cases.

This denominator is direct declarations only. Source base-class inheritance is
retained as context, without flattening duplicate members, assuming override
precedence or inventing Chain.View. The global R1 inventory has45 references and
588 explicit direct declarations, an overlapping discovery inventory. The selected
95 do not close the other493 or inherited semantics. Missing type/access/argument/
return information stays null/unknown. Undocumented function arguments never mean
zero arguments, nor does missing result documentation mean void/no output.

| Retained reference | Direct declarations | Bounded roles | Heading-only U |
| --- | --- | --- | --- |
| Device | 15 | 15 | 0 |
| Device.View | 1 | 1 | 0 |
| DeviceParameter | 15 | 15 | 0 |
| MixerDevice | 11 | 11 | 0 |
| RackDevice | 21 | 21 | 0 |
| RackDevice.View | 4 | 4 | 0 |
| Chain | 15 | 15 | 0 |
| ChainMixerDevice | 4 | 4 | 0 |
| DrumChain | 3 | 3 | 0 |
| DrumPad | 6 | 5 | 1 |

## Existing owners and future prerequisites

[API bridge](live-api-bridge-workflows.md) owns generic binding/navigation/IDs,
get/set/call/observe/remote/initialization and unresolved notification/mapping
contexts. These member declarations do not redefine those message grammars,
serialization, scheduler/threading or persistence laws. No source blank is filled
from bridge examples, another class, inherited name or memory.

[Device racks](device-racks.md) keeps device chains/zones/Macros/variations/pads and
UI workflows. [Bundled parameters](bundled-device-parameters.md),
[mixer values](mixer-values.md), [mix graph](mix-graph.md) and
[Set structure](live-set-structure.md) keep finite stored/native values, conditional
DSP/gains/units/ramps, device graph/storage and identifiers. An API float, type code,
name, min/max/default, GUI value, color or DeviceParameter identity does not expand
those laws. API IDs are not stored ALS Ids or native pointers.

[Automation envelopes](automation-envelopes.md), including unresolved REQ013, and
[automation workflows](automation-workflows.md) retain evaluator/edit/history/output
boundaries. [Mapping](midi-user-mapping.md), [transport](transport-state.md),
[project/media](project-media-workflows.md), [bundled hosting](bundled-device-hosting.md)
and [Max hosting](max-for-live-hosting.md) keep their existing protocols, timebase,
file/editor/device state and host admission. No new storage, Undo, direct-to-audio,
MIDI/choke/codec, RNG, palette-distance or arbitrary plug-in/Max compatibility law
is inferred from a member name. The Amp/Cabinet execution blocker is unchanged.

[Fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/fixtures.json) are future definitions only. No patch,
script, Max/API host, accepted binding, source Set/device, media, actual ID,
response/notification, controller or original/candidate result is supplied. Retain
exact build/Max/platform, source identities, actual available initialized context,
eligible existing same-context object/path/ID/member and separately admitted
read/write/observe/call capability before any later trial. Mutation/deletion applies
only to separately authorized owned disposable copies. No runtime action is
performed or newly authorized by a recipe.

Invalid/no-effect/source-loss probes require positive binding/readback/change/call
first. Audio/MIDI/remote comparisons additionally require nonempty eligible valid
source, enabled active processing/control/path, nonzero source/base/depth/amount/
gain/send, nonmuted wet/return/output and independently calibrated positive
source/return/output baseline, with correct Monitor/arm/receiver/clip/transport/
record/Automation Arm gates. Missing context/capability/hardware, a stale binding,
zero source, muted output or failed baseline is U, never a no-effect pass.

## Direct member contracts

Types/access/arguments/results below are publisher declarations, not wire formats,
actual accepted values or target runtime output. The same-number case provides
an individual future member observation; all documentary and target oracles remain
null. Each compound branch still requires separate evidence.

### REQ-LADR-001 — Device.parameters

**D-current-public/target-U.** Current public reference declares Device.parameters as child of printed type list of DeviceParameter, with access get, observe. Only automatable parameters are described as accessible; the child exposes their declared parameter identities, without a complete parameter set or ordering law.

Declaration: category `children`; printed type `list of DeviceParameter`; access `getobserve`. Original member `SURF-API-LOM-DEVICE--CHILDREN--parameters`.

Evidence: [C74-LOM-DEVICE B0008, B0009, B0010, HTML38:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#parameters).

### REQ-LADR-002 — Device.view

**D-current-public/target-U.** Current public reference declares Device.view as child of printed type Device.View, with access get. The view child is declared Device.View; no further child semantics are stated here.

Declaration: category `children`; printed type `Device.View`; access `get`. Original member `SURF-API-LOM-DEVICE--CHILDREN--view`.

Evidence: [C74-LOM-DEVICE B0011, B0012, HTML41:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#view).

### REQ-LADR-003 — Device.can_have_chains

**D-current-public/target-U.** Current public reference declares Device.can_have_chains as property of printed type bool, with access get. The source distinguishes a single device from a Rack by this capability flag; it is not a complete subclass or host-admission test.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--can_have_chains`.

Evidence: [C74-LOM-DEVICE B0014, B0015, B0016, HTML44:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#can_have_chains).

### REQ-LADR-004 — Device.can_have_drum_pads

**D-current-public/target-U.** Current public reference declares Device.can_have_drum_pads as property of printed type bool, with access get. The flag is described for Drum Racks; it is not an assertion that every rack exposes usable pads.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--can_have_drum_pads`.

Evidence: [C74-LOM-DEVICE B0017, B0018, B0019, HTML48:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#can_have_drum_pads).

### REQ-LADR-005 — Device.class_display_name

**D-current-public/target-U.** Current public reference declares Device.class_display_name as property of printed type symbol, with access get. The original display name is distinguished from the instance title and source class name.

Declaration: category `properties`; printed type `symbol`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--class_display_name`.

Evidence: [C74-LOM-DEVICE B0020, B0021, B0022, HTML51:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#class_display_name).

### REQ-LADR-006 — Device.class_name

**D-current-public/target-U.** Current public reference declares Device.class_name as property of printed type symbol, with access get. The device-type name examples are source context, not an exhaustive class enum or native storage identifier mapping.

Declaration: category `properties`; printed type `symbol`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--class_name`.

Evidence: [C74-LOM-DEVICE B0023, B0024, B0025, HTML54:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#class_name).

### REQ-LADR-007 — Device.is_active

**D-current-public/target-U.** Current public reference declares Device.is_active as property of printed type bool, with access get, observe. The source describes inactive state when either device or enclosing Rack is off; this does not prescribe audio silence, tail handling or a setter.

Declaration: category `properties`; printed type `bool`; access `getobserve`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--is_active`.

Evidence: [C74-LOM-DEVICE B0026, B0027, B0028, HTML57:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#is_active).

### REQ-LADR-008 — Device.name

**D-current-public/target-U.** Current public reference declares Device.name as property of printed type symbol, with access get, set, observe. The name is described as the device title-bar string; encoding, limits and saved identity are ungraded.

Declaration: category `properties`; printed type `symbol`; access `getsetobserve`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--name`.

Evidence: [C74-LOM-DEVICE B0029, B0030, B0031, HTML60:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#name).

### REQ-LADR-009 — Device.type

**D-current-public/target-U.** Current public reference declares Device.type as property of printed type int, with access get. The source lists undefined/instrument/audio-effect/MIDI-effect type codes; those API codes are not stored/native enum or host capability laws.

Declaration: category `properties`; printed type `int`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--type`.

Evidence: [C74-LOM-DEVICE B0032, B0033, B0034, HTML63:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#type).

### REQ-LADR-010 — Device.latency_in_samples

**D-current-public/target-U.** Current public reference declares Device.latency_in_samples as property of printed type int, with access get, observe. The source names device latency in samples; detector, rounding, rate conversion and actual compensation are ungraded.

Declaration: category `properties`; printed type `int`; access `getobserve`. Explicit source unit: samples. Original member `SURF-API-LOM-DEVICE--PROPERTIES--latency_in_samples`.

Evidence: [C74-LOM-DEVICE B0035, B0036, B0037, HTML66:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#latency_in_samples).

### REQ-LADR-011 — Device.latency_in_ms

**D-current-public/target-U.** Current public reference declares Device.latency_in_ms as property of printed type float, with access get, observe. The source names device latency in milliseconds; no equality or conversion with latency_in_samples is established.

Declaration: category `properties`; printed type `float`; access `getobserve`. Explicit source unit: milliseconds. Original member `SURF-API-LOM-DEVICE--PROPERTIES--latency_in_ms`.

Evidence: [C74-LOM-DEVICE B0038, B0039, B0040, HTML69:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#latency_in_ms).

### REQ-LADR-012 — Device.can_compare_ab

**D-current-public/target-U.** Current public reference declares Device.can_compare_ab as property of printed type bool, with access get. The source identifies AB Compare support and says available since Live12.3; target availability and eligible device set remain unknown.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--can_compare_ab`.

Evidence: [C74-LOM-DEVICE B0041, B0042, B0043, HTML72:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#can_compare_ab).

### REQ-LADR-013 — Device.is_using_compare_preset_b

**D-current-public/target-U.** Current public reference declares Device.is_using_compare_preset_b as property of printed type bool, with access get, set, observe. The source selects compare preset B, conditional on can_compare_ab, and describes errors otherwise; exact diagnostics and resulting processing remain unknown.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-DEVICE--PROPERTIES--is_using_compare_preset_b`.

Evidence: [C74-LOM-DEVICE B0044, B0045, B0046, HTML77:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#is_using_compare_preset_b).

### REQ-LADR-014 — Device.store_chosen_bank

**D-current-public/target-U.** Current public reference declares direct function Device.store_chosen_bank. The source supplies script_index and bank_index int inputs and relates the function to hardware control surfaces. No selection effect, return, bank table or hardware behavior is defined.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: script_index [int]; bank_index [int]. Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-DEVICE--FUNCTIONS--store_chosen_bank`.

Evidence: [C74-LOM-DEVICE B0048, B0049, HTML84:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#store_chosen_bank).

### REQ-LADR-015 — Device.save_preset_to_compare_ab_slot

**D-current-public/target-U.** Current public reference declares direct function Device.save_preset_to_compare_ab_slot. The source describes saving device state to the other AB compare slot when can_compare_ab is true, with errors otherwise and availability since12.3; identity, Undo and save/file outcomes stay unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-DEVICE--FUNCTIONS--save_preset_to_compare_ab_slot`.

Evidence: [C74-LOM-DEVICE B0050, B0051, HTML89:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device/#save_preset_to_compare_ab_slot).

### REQ-LADR-016 — Device.View.is_collapsed

**D-current-public/target-U.** Current public reference declares Device.View.is_collapsed as property of printed type bool, with access get, set, observe. The source describes device-chain collapsed presentation, without a geometry, focus, editor or saved-state law.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-DEVICE_VIEW--PROPERTIES--is_collapsed`.

Evidence: [C74-LOM-DEVICE_VIEW B0008, B0009, B0010, HTML38:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/device_view/#is_collapsed).

### REQ-LADR-017 — DeviceParameter.automation_state

**D-current-public/target-U.** Current public reference declares DeviceParameter.automation_state as property of printed type int, with access get, observe. The source distinguishes absent, active and overridden automation states; codes are source context without callback ordering or arbitration guarantees.

Declaration: category `properties`; printed type `int`; access `getobserve`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--automation_state`.

Evidence: [C74-LOM-DEVICEPARAMETER B0006, B0007, B0008, HTML34:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#automation_state).

### REQ-LADR-018 — DeviceParameter.default_value

**D-current-public/target-U.** Current public reference declares DeviceParameter.default_value as property of printed type float, with access get. The default is described only for nonquantized parameters; do not infer a default for quantized or unavailable members.

Declaration: category `properties`; printed type `float`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--default_value`.

Evidence: [C74-LOM-DEVICEPARAMETER B0009, B0010, B0011, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#default_value).

### REQ-LADR-019 — DeviceParameter.is_enabled

**D-current-public/target-U.** Current public reference declares DeviceParameter.is_enabled as property of printed type bool, with access get. The source describes whether user/API/automation/MIDI/keystroke changes are enabled, with macro/remote/other disabling contexts. It supplies no precedence, failure or audio-output law.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--is_enabled`.

Evidence: [C74-LOM-DEVICEPARAMETER B0012, B0013, B0014, HTML44:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#is_enabled).

### REQ-LADR-020 — DeviceParameter.is_quantized

**D-current-public/target-U.** Current public reference declares DeviceParameter.is_quantized as property of printed type bool, with access get. The source distinguishes booleans/enums from int/float parameters and warns visible stepping need not imply quantized state. No native value-class mapping follows.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--is_quantized`.

Evidence: [C74-LOM-DEVICEPARAMETER B0015, B0016, B0017, HTML48:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#is_quantized).

### REQ-LADR-021 — DeviceParameter.max

**D-current-public/target-U.** Current public reference declares DeviceParameter.max as property of printed type float, with access get. The source calls this the largest allowed value; units, rounding/clamping and actual parameter-domain admission need independent evidence.

Declaration: category `properties`; printed type `float`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--max`.

Evidence: [C74-LOM-DEVICEPARAMETER B0018, B0019, B0020, HTML53:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#max).

### REQ-LADR-022 — DeviceParameter.min

**D-current-public/target-U.** Current public reference declares DeviceParameter.min as property of printed type float, with access get. The source calls this the lowest allowed value; units and relation to stored/native domains remain ungraded.

Declaration: category `properties`; printed type `float`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--min`.

Evidence: [C74-LOM-DEVICEPARAMETER B0021, B0022, B0023, HTML56:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#min).

### REQ-LADR-023 — DeviceParameter.name

**D-current-public/target-U.** Current public reference declares DeviceParameter.name as property of printed type symbol, with access get. The source describes the short name in the closed automation chooser; localized labels and encoding remain unknown.

Declaration: category `properties`; printed type `symbol`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--name`.

Evidence: [C74-LOM-DEVICEPARAMETER B0024, B0025, B0026, HTML59:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#name).

### REQ-LADR-024 — DeviceParameter.original_name

**D-current-public/target-U.** Current public reference declares DeviceParameter.original_name as property of printed type symbol, with access get. The source describes a Macro parameter name before assignment, not every device instance name or a durable original identity.

Declaration: category `properties`; printed type `symbol`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--original_name`.

Evidence: [C74-LOM-DEVICEPARAMETER B0027, B0028, B0029, HTML62:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#original_name).

### REQ-LADR-025 — DeviceParameter.state

**D-current-public/target-U.** Current public reference declares DeviceParameter.state as property of printed type int, with access get, observe. The source distinguishes changeable active, changeable inactive and unchangeable states. Its no-audible-effect prose is contextual, requiring independently positive active output before any later no-effect investigation.

Declaration: category `properties`; printed type `int`; access `getobserve`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--state`.

Evidence: [C74-LOM-DEVICEPARAMETER B0030, B0031, B0032, HTML65:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#state).

### REQ-LADR-026 — DeviceParameter.value

**D-current-public/target-U.** Current public reference declares DeviceParameter.value as property of printed type float, with access get, set, observe. The source calls this the internal min-to-max value and distinguishes display_value. No stored/native/normalized conversion or output comparator is adopted.

Declaration: category `properties`; printed type `float`; access `getsetobserve`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--value`.

Evidence: [C74-LOM-DEVICEPARAMETER B0033, B0034, B0035, HTML71:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#value).

### REQ-LADR-027 — DeviceParameter.display_value

**D-current-public/target-U.** Current public reference declares DeviceParameter.display_value as property of printed type float, with access get, set, observe. The source calls this the GUI-visible value. No conversion, parsing, unit, display-text rounding or equivalence to value is supplied.

Declaration: category `properties`; printed type `float`; access `getsetobserve`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--display_value`.

Evidence: [C74-LOM-DEVICEPARAMETER B0036, B0037, B0038, HTML74:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#display_value).

### REQ-LADR-028 — DeviceParameter.value_items

**D-current-public/target-U.** Current public reference declares DeviceParameter.value_items as property of printed type StringVector, with access get. The source lists possible values only for quantized parameters. StringVector is preserved as the printed type, not a serialized vector/enum codec.

Declaration: category `properties`; printed type `StringVector`; access `get`. Original member `SURF-API-LOM-DEVICEPARAMETER--PROPERTIES--value_items`.

Evidence: [C74-LOM-DEVICEPARAMETER B0039, B0040, B0041, HTML77:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#value_items).

### REQ-LADR-029 — DeviceParameter.re_enable_automation

**D-current-public/target-U.** Current public reference declares direct function DeviceParameter.re_enable_automation. The source names re-enabling this parameter automation; arguments, return and effect timing are unspecified and existing automation owners retain their laws.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-DEVICEPARAMETER--FUNCTIONS--re_enable_automation`.

Evidence: [C74-LOM-DEVICEPARAMETER B0043, B0044, HTML82:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#re_enable_automation).

### REQ-LADR-030 — DeviceParameter.str_for_value

**D-current-public/target-U.** Current public reference declares direct function DeviceParameter.str_for_value. The source takes a float value and returns a symbol string representation. Exact formatting, locale, unit and bounds behavior remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: value [float]. Typed return: `symbol`. Original member `SURF-API-LOM-DEVICEPARAMETER--FUNCTIONS--str_for_value`.

Evidence: [C74-LOM-DEVICEPARAMETER B0045, B0046, HTML84:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#str_for_value).

### REQ-LADR-031 — DeviceParameter.__str__

**D-current-public/target-U.** Current public reference declares direct function DeviceParameter.__str__. The source returns a symbol string representation of the current value; arguments are not explicitly documented and output text/format remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `symbol`. Original member `SURF-API-LOM-DEVICEPARAMETER--FUNCTIONS--__str__`.

Evidence: [C74-LOM-DEVICEPARAMETER B0047, B0048, HTML86:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/deviceparameter/#__str__).

### REQ-LADR-032 — MixerDevice.sends

**D-current-public/target-U.** Current public reference declares MixerDevice.sends as child of printed type list of DeviceParameter, with access get, observe. The source describes one send per return track; return identity, order, gain/coefficient and graph behavior remain with existing owners.

Declaration: category `children`; printed type `list of DeviceParameter`; access `getobserve`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--sends`.

Evidence: [C74-LOM-MIXERDEVICE B0006, B0007, B0008, HTML34:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#sends).

### REQ-LADR-033 — MixerDevice.cue_volume

**D-current-public/target-U.** Current public reference declares MixerDevice.cue_volume as child of printed type DeviceParameter, with access get. The child is documented only in the source master-track context; modern Main naming is not silently substituted into API paths.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--cue_volume`.

Evidence: [C74-LOM-MIXERDEVICE B0009, B0010, B0011, HTML37:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#cue_volume).

### REQ-LADR-034 — MixerDevice.crossfader

**D-current-public/target-U.** Current public reference declares MixerDevice.crossfader as child of printed type DeviceParameter, with access get. The child is documented only in the source master-track context; crossfade DSP/curve behavior is not implied.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--crossfader`.

Evidence: [C74-LOM-MIXERDEVICE B0012, B0013, B0014, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#crossfader).

### REQ-LADR-035 — MixerDevice.left_split_stereo

**D-current-public/target-U.** Current public reference declares MixerDevice.left_split_stereo as child of printed type DeviceParameter, with access get. The source identifies the track left split-stereo pan parameter; eligibility, range and pan law remain ungraded.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--left_split_stereo`.

Evidence: [C74-LOM-MIXERDEVICE B0015, B0016, B0017, HTML43:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#left_split_stereo).

### REQ-LADR-036 — MixerDevice.panning

**D-current-public/target-U.** Current public reference declares MixerDevice.panning as child of printed type DeviceParameter, with access get. The heading/access declaration supplies the panning parameter role; no value range, unit, mode conversion or DSP law is stated.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--panning`.

Evidence: [C74-LOM-MIXERDEVICE B0018, B0019, HTML46:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#panning).

### REQ-LADR-037 — MixerDevice.right_split_stereo

**D-current-public/target-U.** Current public reference declares MixerDevice.right_split_stereo as child of printed type DeviceParameter, with access get. The source identifies the track right split-stereo pan parameter; eligibility, range and pan law remain ungraded.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--right_split_stereo`.

Evidence: [C74-LOM-MIXERDEVICE B0020, B0021, B0022, HTML48:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#right_split_stereo).

### REQ-LADR-038 — MixerDevice.song_tempo

**D-current-public/target-U.** Current public reference declares MixerDevice.song_tempo as child of printed type DeviceParameter, with access get. The child is documented only in the source master-track context; no tempo clock, precedence, range or scheduling law is added.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--song_tempo`.

Evidence: [C74-LOM-MIXERDEVICE B0023, B0024, B0025, HTML51:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#song_tempo).

### REQ-LADR-039 — MixerDevice.track_activator

**D-current-public/target-U.** Current public reference declares MixerDevice.track_activator as child of printed type DeviceParameter, with access get. The child declaration names the track activator parameter without defining its numeric domain, silence or tail behavior.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--track_activator`.

Evidence: [C74-LOM-MIXERDEVICE B0026, B0027, HTML54:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#track_activator).

### REQ-LADR-040 — MixerDevice.volume

**D-current-public/target-U.** Current public reference declares MixerDevice.volume as child of printed type DeviceParameter, with access get. The child declaration names a volume parameter without defining gain, default, stored-domain or output behavior.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-MIXERDEVICE--CHILDREN--volume`.

Evidence: [C74-LOM-MIXERDEVICE B0028, B0029, HTML56:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#volume).

### REQ-LADR-041 — MixerDevice.crossfade_assign

**D-current-public/target-U.** Current public reference declares MixerDevice.crossfade_assign as property of printed type int, with access get, set, observe. The source labels A/none/B codes and excludes the source master-track context; no finite stored/native enum or crossfade-output law is replaced.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-MIXERDEVICE--PROPERTIES--crossfade_assign`.

Evidence: [C74-LOM-MIXERDEVICE B0031, B0032, B0033, HTML59:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#crossfade_assign).

### REQ-LADR-042 — MixerDevice.panning_mode

**D-current-public/target-U.** Current public reference declares MixerDevice.panning_mode as property of printed type int, with access get, set, observe. The source distinguishes Stereo and Split Stereo modes; codes are context only and existing mixer pan laws remain unchanged.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-MIXERDEVICE--PROPERTIES--panning_mode`.

Evidence: [C74-LOM-MIXERDEVICE B0034, B0035, B0036, HTML62:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/mixerdevice/#panning_mode).

### REQ-LADR-043 — RackDevice.chain_selector

**D-current-public/target-U.** Current public reference declares RackDevice.chain_selector as child of printed type DeviceParameter, with access get. The source calls this a convenience accessor for the Rack chain selector; no zone, native unit or selection-to-sound law follows.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-RACKDEVICE--CHILDREN--chain_selector`.

Evidence: [C74-LOM-RACKDEVICE B0004, B0005, B0006, HTML32:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#chain_selector).

### REQ-LADR-044 — RackDevice.chains

**D-current-public/target-U.** Current public reference declares RackDevice.chains as child of printed type list of Chain, with access get, observe. The source describes the Rack chains as a list; no ordering/mutation/serialization or inherited-member expansion is inferred.

Declaration: category `children`; printed type `list of Chain`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--CHILDREN--chains`.

Evidence: [C74-LOM-RACKDEVICE B0007, B0008, B0009, HTML35:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#chains).

### REQ-LADR-045 — RackDevice.drum_pads

**D-current-public/target-U.** Current public reference declares RackDevice.drum_pads as child of printed type list of DrumPad, with access get, observe. The source describes128 pads for topmost Drum Racks and an empty list for inner racks. Counts are source claims only, not runtime or pad-MIDI-code oracles.

Declaration: category `children`; printed type `list of DrumPad`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--CHILDREN--drum_pads`.

Evidence: [C74-LOM-RACKDEVICE B0010, B0011, B0012, HTML38:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#drum_pads).

### REQ-LADR-046 — RackDevice.return_chains

**D-current-public/target-U.** Current public reference declares RackDevice.return_chains as child of printed type list of Chain, with access get, observe. The source describes Rack return chains; list identity, order, sends and graph behavior remain ungraded.

Declaration: category `children`; printed type `list of Chain`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--CHILDREN--return_chains`.

Evidence: [C74-LOM-RACKDEVICE B0013, B0014, B0015, HTML41:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#return_chains).

### REQ-LADR-047 — RackDevice.visible_drum_pads

**D-current-public/target-U.** Current public reference declares RackDevice.visible_drum_pads as child of printed type list of DrumPad, with access get, observe. The source describes16 visible pads for topmost Drum Racks and an empty list for inner racks. View/range/count correspondence remains ungraded.

Declaration: category `children`; printed type `list of DrumPad`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--CHILDREN--visible_drum_pads`.

Evidence: [C74-LOM-RACKDEVICE B0016, B0017, B0018, HTML44:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#visible_drum_pads).

### REQ-LADR-048 — RackDevice.can_show_chains

**D-current-public/target-U.** Current public reference declares RackDevice.can_show_chains as property of printed type bool, with access get. The source conditions the flag on a contained instrument capable of showing chains in Session View; do not generalize from Rack class alone.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--can_show_chains`.

Evidence: [C74-LOM-RACKDEVICE B0020, B0021, B0022, HTML48:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#can_show_chains).

### REQ-LADR-049 — RackDevice.has_drum_pads

**D-current-public/target-U.** Current public reference declares RackDevice.has_drum_pads as property of printed type bool, with access get, observe. The source limits this to Drum Racks and distinguishes a nested Drum Rack without pads. Root/topmost and member-availability predicates remain explicit.

Declaration: category `properties`; printed type `bool`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--has_drum_pads`.

Evidence: [C74-LOM-RACKDEVICE B0023, B0024, B0025, HTML51:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#has_drum_pads).

### REQ-LADR-050 — RackDevice.has_macro_mappings

**D-current-public/target-U.** Current public reference declares RackDevice.has_macro_mappings as property of printed type bool, with access get, observe. The source indicates whether any Macro is mapped to a parameter. Mapping encoding, eligible set and numerical effect remain with existing owners.

Declaration: category `properties`; printed type `bool`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--has_macro_mappings`.

Evidence: [C74-LOM-RACKDEVICE B0026, B0027, B0028, HTML55:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#has_macro_mappings).

### REQ-LADR-051 — RackDevice.is_showing_chains

**D-current-public/target-U.** Current public reference declares RackDevice.is_showing_chains as property of printed type bool, with access get, set, observe. The source conditions this on a contained instrument showing chains in Session View; actual view transitions and callback timing remain ungraded.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--is_showing_chains`.

Evidence: [C74-LOM-RACKDEVICE B0029, B0030, B0031, HTML58:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#is_showing_chains).

### REQ-LADR-052 — RackDevice.variation_count

**D-current-public/target-U.** Current public reference declares RackDevice.variation_count as property of printed type int, with access get, observe. The source counts currently stored Macro variations and dates availability to11.0; no exact count result or storage lifecycle is adopted.

Declaration: category `properties`; printed type `int`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--variation_count`.

Evidence: [C74-LOM-RACKDEVICE B0032, B0033, B0034, HTML61:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#variation_count).

### REQ-LADR-053 — RackDevice.selected_variation_index

**D-current-public/target-U.** Current public reference declares RackDevice.selected_variation_index as property of printed type int, with access get, set. The source selects the current variation and dates availability to11.0. No observation capability is declared here; index bounds/absence/recall effects remain unknown.

Declaration: category `properties`; printed type `int`; access `getset`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--selected_variation_index`.

Evidence: [C74-LOM-RACKDEVICE B0035, B0036, B0037, HTML66:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#selected_variation_index).

### REQ-LADR-054 — RackDevice.visible_macro_count

**D-current-public/target-U.** Current public reference declares RackDevice.visible_macro_count as property of printed type int, with access get, observe. The source counts visible Macros; admissible counts, layout, persistence and default are not established.

Declaration: category `properties`; printed type `int`; access `getobserve`. Original member `SURF-API-LOM-RACKDEVICE--PROPERTIES--visible_macro_count`.

Evidence: [C74-LOM-RACKDEVICE B0038, B0039, B0040, HTML71:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#visible_macro_count).

### REQ-LADR-055 — RackDevice.copy_pad

**D-current-public/target-U.** Current public reference declares direct function RackDevice.copy_pad. The source copies all pad content from source_index to destination_index, both Drum Rack pad indices. Index limits, replacement, shared references and audio/Undo outcomes remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: source_index [int]; destination_index [int]. Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--copy_pad`.

Evidence: [C74-LOM-RACKDEVICE B0042, B0043, HTML75:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#copy_pad).

### REQ-LADR-056 — RackDevice.add_macro

**D-current-public/target-U.** Current public reference declares direct function RackDevice.add_macro. The source increases visible Macro controls, available since11.0; count limits and result/Undo/persistence are unspecified.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--add_macro`.

Evidence: [C74-LOM-RACKDEVICE B0044, B0045, HTML80:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#add_macro).

### REQ-LADR-057 — RackDevice.insert_chain

**D-current-public/target-U.** Current public reference declares direct function RackDevice.insert_chain. The source attempts chain insertion at optional index, appending when absent, and reports an error if not possible; available since12.3. Valid predicates, exact errors, return and transactions are ungraded.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: index [int] optional. Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--insert_chain`.

Evidence: [C74-LOM-RACKDEVICE B0046, B0047, HTML84:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#insert_chain).

### REQ-LADR-058 — RackDevice.remove_macro

**D-current-public/target-U.** Current public reference declares direct function RackDevice.remove_macro. The source decreases visible Macro controls, available since11.0; lower bounds and mapping/value loss remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--remove_macro`.

Evidence: [C74-LOM-RACKDEVICE B0048, B0049, HTML90:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#remove_macro).

### REQ-LADR-059 — RackDevice.randomize_macros

**D-current-public/target-U.** Current public reference declares direct function RackDevice.randomize_macros. The source randomizes eligible Macro values, available since11.0; eligibility, distribution, seed, inequality and numeric outputs remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--randomize_macros`.

Evidence: [C74-LOM-RACKDEVICE B0050, B0051, HTML94:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#randomize_macros).

### REQ-LADR-060 — RackDevice.store_variation

**D-current-public/target-U.** Current public reference declares direct function RackDevice.store_variation. The source stores values of currently mapped Macros as a new variation, available since11.0; unbound/hidden exclusions, serialized values and ID/history behavior remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--store_variation`.

Evidence: [C74-LOM-RACKDEVICE B0052, B0053, HTML98:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#store_variation).

### REQ-LADR-061 — RackDevice.recall_selected_variation

**D-current-public/target-U.** Current public reference declares direct function RackDevice.recall_selected_variation. The source recalls the selected Macro variation, available since11.0; absent selection, partial mapping and parameter/output results remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--recall_selected_variation`.

Evidence: [C74-LOM-RACKDEVICE B0054, B0055, HTML102:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#recall_selected_variation).

### REQ-LADR-062 — RackDevice.recall_last_used_variation

**D-current-public/target-U.** Current public reference declares direct function RackDevice.recall_last_used_variation. The source recalls the most recently recalled Macro variation, available since11.0; selection identity and missing-history behavior remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--recall_last_used_variation`.

Evidence: [C74-LOM-RACKDEVICE B0056, B0057, HTML106:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#recall_last_used_variation).

### REQ-LADR-063 — RackDevice.delete_selected_variation

**D-current-public/target-U.** Current public reference declares direct function RackDevice.delete_selected_variation. The source deletes the selected variation and says nothing happens without selection, available since11.0; exact state/history/no-effect results remain ungraded.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-RACKDEVICE--FUNCTIONS--delete_selected_variation`.

Evidence: [C74-LOM-RACKDEVICE B0058, B0059, HTML110:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice/#delete_selected_variation).

### REQ-LADR-064 — RackDevice.View.selected_drum_pad

**D-current-public/target-U.** Current public reference declares RackDevice.View.selected_drum_pad as child of printed type DrumPad, with access get, set, observe. The source names the selected Drum Rack pad and limits availability to Drum Racks; pad identity, nested-rack predicates and selection effect remain ungraded.

Declaration: category `children`; printed type `DrumPad`; access `getsetobserve`. Original member `SURF-API-LOM-RACKDEVICE_VIEW--CHILDREN--selected_drum_pad`.

Evidence: [C74-LOM-RACKDEVICE_VIEW B0004, B0005, B0006, HTML32:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice_view/#selected_drum_pad).

### REQ-LADR-065 — RackDevice.View.selected_chain

**D-current-public/target-U.** Current public reference declares RackDevice.View.selected_chain as child of printed type Chain, with access get, set, observe. The source names the currently selected chain; absent selection and cross-rack IDs remain unresolved.

Declaration: category `children`; printed type `Chain`; access `getsetobserve`. Original member `SURF-API-LOM-RACKDEVICE_VIEW--CHILDREN--selected_chain`.

Evidence: [C74-LOM-RACKDEVICE_VIEW B0007, B0008, B0009, HTML36:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice_view/#selected_chain).

### REQ-LADR-066 — RackDevice.View.drum_pads_scroll_position

**D-current-public/target-U.** Current public reference declares RackDevice.View.drum_pads_scroll_position as property of printed type int, with access get, set, observe. The source identifies the lowest visible pad row and prints range0–28 for Drum Racks. No index-to-note, clipping/rounding or viewport geometry law is inferred.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-RACKDEVICE_VIEW--PROPERTIES--drum_pads_scroll_position`.

Evidence: [C74-LOM-RACKDEVICE_VIEW B0011, B0012, B0013, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice_view/#drum_pads_scroll_position).

### REQ-LADR-067 — RackDevice.View.is_showing_chain_devices

**D-current-public/target-U.** Current public reference declares RackDevice.View.is_showing_chain_devices as property of printed type bool, with access get, set, observe. The source describes whether devices in the selected chain are visible; it does not establish containing-rack view state, focus or durable layout.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-RACKDEVICE_VIEW--PROPERTIES--is_showing_chain_devices`.

Evidence: [C74-LOM-RACKDEVICE_VIEW B0014, B0015, B0016, HTML44:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/rackdevice_view/#is_showing_chain_devices).

### REQ-LADR-068 — Chain.devices

**D-current-public/target-U.** Current public reference declares Chain.devices as child of printed type Device, with access get, observe. The plural devices child is printed with type Device and get/observe access; no description clarifies cardinality. Preserve this exact declaration without inferring a list from its name or paths.

Declaration: category `children`; printed type `Device`; access `getobserve`. Original member `SURF-API-LOM-CHAIN--CHILDREN--devices`.

Evidence: [C74-LOM-CHAIN B0009, B0010, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#devices).

### REQ-LADR-069 — Chain.mixer_device

**D-current-public/target-U.** Current public reference declares Chain.mixer_device as child of printed type ChainMixerDevice, with access get. The source declares the chain mixer child as ChainMixerDevice; audio graph, initialization and missing-child behavior remain unknown.

Declaration: category `children`; printed type `ChainMixerDevice`; access `get`. Original member `SURF-API-LOM-CHAIN--CHILDREN--mixer_device`.

Evidence: [C74-LOM-CHAIN B0011, B0012, HTML42:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#mixer_device).

### REQ-LADR-070 — Chain.color

**D-current-public/target-U.** Current public reference declares Chain.color as property of printed type int, with access get, set, observe. The source describes RGB0x00rrggbb and nearest chooser color when set. Packing/arithmetic, palette/ties, distance metric and rendered pixels remain source context, not a numeric/codec comparator.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--color`.

Evidence: [C74-LOM-CHAIN B0014, B0015, B0016, HTML45:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#color).

### REQ-LADR-071 — Chain.color_index

**D-current-public/target-U.** Current public reference declares Chain.color_index as property of printed type long, with access get, set, observe. The source calls this the chain color index, printed long. Palette, bounds, API/native/stored type-width and equivalence to RGB remain unknown.

Declaration: category `properties`; printed type `long`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--color_index`.

Evidence: [C74-LOM-CHAIN B0017, B0018, B0019, HTML50:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#color_index).

### REQ-LADR-072 — Chain.is_auto_colored

**D-current-public/target-U.** Current public reference declares Chain.is_auto_colored as property of printed type bool, with access get, set, observe. The source describes inheriting the containing track/chain color while enabled; disabling/restoration, source identity and persistence remain ungraded.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--is_auto_colored`.

Evidence: [C74-LOM-CHAIN B0020, B0021, B0022, HTML53:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#is_auto_colored).

### REQ-LADR-073 — Chain.has_audio_input

**D-current-public/target-U.** Current public reference declares Chain.has_audio_input as property of printed type bool, with access get. The heading/access declaration names an audio-input capability flag; no extra direction, rack/type predicate, routing or signal behavior is supplied.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--has_audio_input`.

Evidence: [C74-LOM-CHAIN B0023, B0024, HTML56:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#has_audio_input).

### REQ-LADR-074 — Chain.has_audio_output

**D-current-public/target-U.** Current public reference declares Chain.has_audio_output as property of printed type bool, with access get. The heading/access declaration names an audio-output capability flag; no graph, route or silence result is implied.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--has_audio_output`.

Evidence: [C74-LOM-CHAIN B0025, B0026, HTML58:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#has_audio_output).

### REQ-LADR-075 — Chain.has_midi_input

**D-current-public/target-U.** Current public reference declares Chain.has_midi_input as property of printed type bool, with access get. The heading/access declaration names a MIDI-input capability flag; actual accepted event set, port and codec remain unknown.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--has_midi_input`.

Evidence: [C74-LOM-CHAIN B0027, B0028, HTML60:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#has_midi_input).

### REQ-LADR-076 — Chain.has_midi_output

**D-current-public/target-U.** Current public reference declares Chain.has_midi_output as property of printed type bool, with access get. The heading/access declaration names a MIDI-output capability flag; no routing, event scheduling or delivered-message law is implied.

Declaration: category `properties`; printed type `bool`; access `get`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--has_midi_output`.

Evidence: [C74-LOM-CHAIN B0029, B0030, HTML62:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#has_midi_output).

### REQ-LADR-077 — Chain.mute

**D-current-public/target-U.** Current public reference declares Chain.mute as property of printed type bool, with access get, set, observe. The source relates mute to Chain Activator off; tails, gain, other-chain interactions and numerical output remain ungraded.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--mute`.

Evidence: [C74-LOM-CHAIN B0031, B0032, B0033, HTML64:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#mute).

### REQ-LADR-078 — Chain.muted_via_solo

**D-current-public/target-U.** Current public reference declares Chain.muted_via_solo as property of printed type bool, with access get, observe. The source indicates mute because another chain is soloed; solo-domain membership, precedence and audible output remain unknown.

Declaration: category `properties`; printed type `bool`; access `getobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--muted_via_solo`.

Evidence: [C74-LOM-CHAIN B0034, B0035, B0036, HTML67:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#muted_via_solo).

### REQ-LADR-079 — Chain.name

**D-current-public/target-U.** Current public reference declares Chain.name as property of printed type unicode, with access get, set, observe. The source prints unicode with get/set/observe for the chain name but no encoding, limit, validation or durable-identity contract.

Declaration: category `properties`; printed type `unicode`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--name`.

Evidence: [C74-LOM-CHAIN B0037, B0038, HTML70:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#name).

### REQ-LADR-080 — Chain.solo

**D-current-public/target-U.** Current public reference declares Chain.solo as property of printed type bool, with access get, set, observe. The source describes the Solo switch and says it does not automatically switch other chains Solo off. No global exclusivity, output or history law follows.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-CHAIN--PROPERTIES--solo`.

Evidence: [C74-LOM-CHAIN B0039, B0040, B0041, HTML72:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#solo).

### REQ-LADR-081 — Chain.delete_device

**D-current-public/target-U.** Current public reference declares direct function Chain.delete_device. The source takes an int index to delete that device. Valid indices, return, dependent references, cleanup, error and history behavior are unspecified.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: index [int]. Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-CHAIN--FUNCTIONS--delete_device`.

Evidence: [C74-LOM-CHAIN B0043, B0044, HTML77:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#delete_device).

### REQ-LADR-082 — Chain.insert_device

**D-current-public/target-U.** Current public reference declares direct function Chain.insert_device. The source takes a UI device_name symbol and optional target_index int, appending when absent. It attempts native Live device insertion, excludes Max/plug-ins, and cites mouse-admission/type-order limits including no MIDI effect after an instrument. It dates availability to12.3; complete admission, errors, return and parameter defaults remain unknown.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: device_name [symbol]; target_index [int] optional. Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-CHAIN--FUNCTIONS--insert_device`.

Evidence: [C74-LOM-CHAIN B0045, B0046, HTML80:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chain/#insert_device).

### REQ-LADR-083 — ChainMixerDevice.sends

**D-current-public/target-U.** Current public reference declares ChainMixerDevice.sends as child of printed type list of DeviceParameter, with access get, observe. The source Rack-context wording is retained verbatim: [in Audio Effect Racks and Instrument Racks only] For Drum Racks, otherwise empty. Do not silently resolve its eligibility/emptiness predicate or infer a send/return graph.

Declaration: category `children`; printed type `list of DeviceParameter`; access `getobserve`. Original member `SURF-API-LOM-CHAINMIXERDEVICE--CHILDREN--sends`.

Evidence: [C74-LOM-CHAINMIXERDEVICE B0007, B0008, B0009, HTML36:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chainmixerdevice/#sends).

### REQ-LADR-084 — ChainMixerDevice.chain_activator

**D-current-public/target-U.** Current public reference declares ChainMixerDevice.chain_activator as child of printed type DeviceParameter, with access get. The child declaration names a chain activator DeviceParameter; no gate, numeric value, mute/tail or audio effect is established.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-CHAINMIXERDEVICE--CHILDREN--chain_activator`.

Evidence: [C74-LOM-CHAINMIXERDEVICE B0010, B0011, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chainmixerdevice/#chain_activator).

### REQ-LADR-085 — ChainMixerDevice.panning

**D-current-public/target-U.** Current public reference declares ChainMixerDevice.panning as child of printed type DeviceParameter, with access get. The source restricts panning to Audio Effect and Instrument Racks; absent/other-rack behavior and parameter units remain unknown.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-CHAINMIXERDEVICE--CHILDREN--panning`.

Evidence: [C74-LOM-CHAINMIXERDEVICE B0012, B0013, B0014, HTML42:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chainmixerdevice/#panning).

### REQ-LADR-086 — ChainMixerDevice.volume

**D-current-public/target-U.** Current public reference declares ChainMixerDevice.volume as child of printed type DeviceParameter, with access get. The source restricts volume to Audio Effect and Instrument Racks; gain, domains and other-rack behavior remain unknown.

Declaration: category `children`; printed type `DeviceParameter`; access `get`. Original member `SURF-API-LOM-CHAINMIXERDEVICE--CHILDREN--volume`.

Evidence: [C74-LOM-CHAINMIXERDEVICE B0015, B0016, B0017, HTML45:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/chainmixerdevice/#volume).

### REQ-LADR-087 — DrumChain.in_note

**D-current-public/target-U.** Current public reference declares DrumChain.in_note as property of printed type int, with access get, set, observe. The source selects the triggering MIDI note, with -1 described as All Notes and availability since12.3. This is source context only, not a note/codec/range or actual event-admission law.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-DRUMCHAIN--PROPERTIES--in_note`.

Evidence: [C74-LOM-DRUMCHAIN B0004, B0005, B0006, HTML33:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumchain/#in_note).

### REQ-LADR-088 — DrumChain.out_note

**D-current-public/target-U.** Current public reference declares DrumChain.out_note as property of printed type int, with access get, set, observe. The source selects the MIDI note sent to contained devices; full note domain, transformation, event codec and scheduling remain unknown.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-DRUMCHAIN--PROPERTIES--out_note`.

Evidence: [C74-LOM-DRUMCHAIN B0007, B0008, B0009, HTML38:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumchain/#out_note).

### REQ-LADR-089 — DrumChain.choke_group

**D-current-public/target-U.** Current public reference declares DrumChain.choke_group as property of printed type int, with access get, set, observe. The source selects the choke group; valid groups, voice/choke/release/audio behavior and stored encoding remain unknown.

Declaration: category `properties`; printed type `int`; access `getsetobserve`. Original member `SURF-API-LOM-DRUMCHAIN--PROPERTIES--choke_group`.

Evidence: [C74-LOM-DRUMCHAIN B0010, B0011, B0012, HTML41:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumchain/#choke_group).

### REQ-LADR-090 — DrumPad.chains

**D-current-public/target-U.** Current public reference declares DrumPad.chains as child of printed type Chain, with access get, observe. The plural chains child is printed Chain with get/observe and no clarifying description. Cardinality and pad/chain mapping remain unresolved rather than inferred from the name.

Declaration: category `children`; printed type `Chain`; access `getobserve`. Original member `SURF-API-LOM-DRUMPAD--CHILDREN--chains`.

Evidence: [C74-LOM-DRUMPAD B0006, B0007, HTML34:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#chains).

### REQ-LADR-091 — DrumPad.mute

**D-current-public/target-U.** Current public reference declares DrumPad.mute as property of printed type bool, with access get, set, observe. The source marks the pad muted; no contained-chain scope, voice termination, gain or silence oracle follows.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-DRUMPAD--PROPERTIES--mute`.

Evidence: [C74-LOM-DRUMPAD B0009, B0010, B0011, HTML37:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#mute).

### REQ-LADR-092 — DrumPad.name

**D-current-public/target-U.** Current public reference declares DrumPad.name as property of printed type symbol, with access get, observe. The source prints a get/observe symbol name without setter or naming semantics; generated labels, persistence and encoding remain unknown.

Declaration: category `properties`; printed type `symbol`; access `getobserve`. Original member `SURF-API-LOM-DRUMPAD--PROPERTIES--name`.

Evidence: [C74-LOM-DRUMPAD B0012, B0013, HTML40:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#name).

### REQ-LADR-093 — DrumPad.note

**D-current-public/target-U.** Current public reference declares DrumPad.note as property of printed type int, with access get. The note member is an int with get access and no stated domain or transformation; do not infer a MIDI wire codec or editable pad-note assignment.

Declaration: category `properties`; printed type `int`; access `get`. Original member `SURF-API-LOM-DRUMPAD--PROPERTIES--note`.

Evidence: [C74-LOM-DRUMPAD B0014, B0015, HTML42:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#note).

### REQ-LADR-094 — DrumPad.solo

**D-current-public/target-U.** Current public reference declares DrumPad.solo as property of printed type bool, with access get, set, observe. The source marks Solo on and says other chains Solo are not automatically switched off. Cross-pad/chain scope, exclusivity and sound remain unknown.

Declaration: category `properties`; printed type `bool`; access `getsetobserve`. Original member `SURF-API-LOM-DRUMPAD--PROPERTIES--solo`.

Evidence: [C74-LOM-DRUMPAD B0016, B0017, B0018, HTML44:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#solo).

### REQ-LADR-095 — DrumPad.delete_all_chains

**U/target-U.** Current public reference declares direct function DrumPad.delete_all_chains. Only the function heading is retained. Arguments, result, effect, eligibility, errors and lifecycle semantics are undocumented; do not infer deletion behavior from its name.

Declaration: category `functions`; printed type `not stated`; access `not stated`. Arguments: not stated (unknown). Typed return: `not stated (unknown)`. Original member `SURF-API-LOM-DRUMPAD--FUNCTIONS--delete_all_chains`.

Evidence: [C74-LOM-DRUMPAD B0020, HTML49:0](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/source-blocks.json); [publisher member](https://docs.cycling74.com/apiref/lom/drumpad/#delete_all_chains).

## Cross-cutting unknown obligations

### REQ-LADR-U-VERSION — Version and direct/inherited availability

**U/target-U.** Exact12.4.3/Max/platform/member availability, current12.4.5 source-index applicability and inherited member/alias/root reconciliation remain unknown. Chain.View is absent from R1 and receives no invented reference.

### REQ-LADR-U-SHAPES — Types cardinality arguments and returns

**U/target-U.** Plural Chain.devices and DrumPad.chains retain singular printed types. Missing function argument/return and type-width/nullable/list/order/encoding semantics remain U; absence of argument documentation never means zero arguments or void.

### REQ-LADR-U-CAPABILITY — Eligibility access and errors

**U/target-U.** Rack/topmost/nested/Drum/master-track/compare eligibility, contradictory ChainMixerDevice.sends context, absent/read-only/nonobservable/member and malformed/boundary/error outcomes remain unknown beyond stated source predicates.

### REQ-LADR-U-VALUES — Parameter and mixer value domains

**U/target-U.** API value/display_value/min/max/default/quantized/state/name/type roles do not define native/stored/gain/normalization/display conversion, actual latency, colors/MIDI codecs, clipping or numeric/signal results. Existing owners retain finite laws.

### REQ-LADR-U-MUTATION — Mutation automation and output ownership

**U/target-U.** Actual set/call effects, device insertion/admission, AB state, mute/solo/choke, automation override/re-enable/remote ownership, notification-time mutation and delivered audio/MIDI require independent evidence.

### REQ-LADR-U-MACROS — Macros variations and randomness

**U/target-U.** Eligible randomization, distributions/seeds, changed-value inequality, macro/mapping limits, visible-count/variation selection/last-used identity, copy replacement and unselected no-effect behavior remain unknown.

### REQ-LADR-U-STATE — History persistence and cancellation

**U/target-U.** Undo/Redo grouping, save/reopen/preset/editor moves, deleted/replaced object IDs, selection/layout/default/mapping durability, cancellation, concurrent edits and migration remain unknown.

### REQ-LADR-U-LIFECYCLE — Rate transport source loss and teardown

**U/target-U.** Rate/block/transport changes, observer invalidation, host/context/target/device/source loss, recovery and close/quit/pending-work teardown have null timing/output/cleanup outcomes. Missing Max/API/hardware or positive input is never a negative pass.

## Finite future cases

[Cases](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/cases.json) contain95 direct-member and18 cross-cutting
proposals. All113 have null documentary expected/comparison as well as null target
expected/comparison, target U and executed false. A source role or mapped member
count is not a returned value, API trace, acceptance pass or closed compound clause.

| Case | Requirement | Kind | Proposed member or boundary |
| --- | --- | --- | --- |
| LADR-001 | REQ-LADR-001 | message-role | Device.parameters |
| LADR-002 | REQ-LADR-002 | message-role | Device.view |
| LADR-003 | REQ-LADR-003 | message-role | Device.can_have_chains |
| LADR-004 | REQ-LADR-004 | message-role | Device.can_have_drum_pads |
| LADR-005 | REQ-LADR-005 | message-role | Device.class_display_name |
| LADR-006 | REQ-LADR-006 | message-role | Device.class_name |
| LADR-007 | REQ-LADR-007 | message-role | Device.is_active |
| LADR-008 | REQ-LADR-008 | message-role | Device.name |
| LADR-009 | REQ-LADR-009 | message-role | Device.type |
| LADR-010 | REQ-LADR-010 | message-role | Device.latency_in_samples |
| LADR-011 | REQ-LADR-011 | message-role | Device.latency_in_ms |
| LADR-012 | REQ-LADR-012 | message-role | Device.can_compare_ab |
| LADR-013 | REQ-LADR-013 | message-role | Device.is_using_compare_preset_b |
| LADR-014 | REQ-LADR-014 | message-role | Device.store_chosen_bank |
| LADR-015 | REQ-LADR-015 | message-role | Device.save_preset_to_compare_ab_slot |
| LADR-016 | REQ-LADR-016 | message-role | Device.View.is_collapsed |
| LADR-017 | REQ-LADR-017 | message-role | DeviceParameter.automation_state |
| LADR-018 | REQ-LADR-018 | message-role | DeviceParameter.default_value |
| LADR-019 | REQ-LADR-019 | message-role | DeviceParameter.is_enabled |
| LADR-020 | REQ-LADR-020 | message-role | DeviceParameter.is_quantized |
| LADR-021 | REQ-LADR-021 | message-role | DeviceParameter.max |
| LADR-022 | REQ-LADR-022 | message-role | DeviceParameter.min |
| LADR-023 | REQ-LADR-023 | message-role | DeviceParameter.name |
| LADR-024 | REQ-LADR-024 | message-role | DeviceParameter.original_name |
| LADR-025 | REQ-LADR-025 | message-role | DeviceParameter.state |
| LADR-026 | REQ-LADR-026 | message-role | DeviceParameter.value |
| LADR-027 | REQ-LADR-027 | message-role | DeviceParameter.display_value |
| LADR-028 | REQ-LADR-028 | message-role | DeviceParameter.value_items |
| LADR-029 | REQ-LADR-029 | message-role | DeviceParameter.re_enable_automation |
| LADR-030 | REQ-LADR-030 | message-role | DeviceParameter.str_for_value |
| LADR-031 | REQ-LADR-031 | message-role | DeviceParameter.__str__ |
| LADR-032 | REQ-LADR-032 | message-role | MixerDevice.sends |
| LADR-033 | REQ-LADR-033 | message-role | MixerDevice.cue_volume |
| LADR-034 | REQ-LADR-034 | message-role | MixerDevice.crossfader |
| LADR-035 | REQ-LADR-035 | message-role | MixerDevice.left_split_stereo |
| LADR-036 | REQ-LADR-036 | message-role | MixerDevice.panning |
| LADR-037 | REQ-LADR-037 | message-role | MixerDevice.right_split_stereo |
| LADR-038 | REQ-LADR-038 | message-role | MixerDevice.song_tempo |
| LADR-039 | REQ-LADR-039 | message-role | MixerDevice.track_activator |
| LADR-040 | REQ-LADR-040 | message-role | MixerDevice.volume |
| LADR-041 | REQ-LADR-041 | message-role | MixerDevice.crossfade_assign |
| LADR-042 | REQ-LADR-042 | message-role | MixerDevice.panning_mode |
| LADR-043 | REQ-LADR-043 | message-role | RackDevice.chain_selector |
| LADR-044 | REQ-LADR-044 | message-role | RackDevice.chains |
| LADR-045 | REQ-LADR-045 | message-role | RackDevice.drum_pads |
| LADR-046 | REQ-LADR-046 | message-role | RackDevice.return_chains |
| LADR-047 | REQ-LADR-047 | message-role | RackDevice.visible_drum_pads |
| LADR-048 | REQ-LADR-048 | message-role | RackDevice.can_show_chains |
| LADR-049 | REQ-LADR-049 | message-role | RackDevice.has_drum_pads |
| LADR-050 | REQ-LADR-050 | message-role | RackDevice.has_macro_mappings |
| LADR-051 | REQ-LADR-051 | message-role | RackDevice.is_showing_chains |
| LADR-052 | REQ-LADR-052 | message-role | RackDevice.variation_count |
| LADR-053 | REQ-LADR-053 | message-role | RackDevice.selected_variation_index |
| LADR-054 | REQ-LADR-054 | message-role | RackDevice.visible_macro_count |
| LADR-055 | REQ-LADR-055 | message-role | RackDevice.copy_pad |
| LADR-056 | REQ-LADR-056 | message-role | RackDevice.add_macro |
| LADR-057 | REQ-LADR-057 | message-role | RackDevice.insert_chain |
| LADR-058 | REQ-LADR-058 | message-role | RackDevice.remove_macro |
| LADR-059 | REQ-LADR-059 | message-role | RackDevice.randomize_macros |
| LADR-060 | REQ-LADR-060 | message-role | RackDevice.store_variation |
| LADR-061 | REQ-LADR-061 | message-role | RackDevice.recall_selected_variation |
| LADR-062 | REQ-LADR-062 | message-role | RackDevice.recall_last_used_variation |
| LADR-063 | REQ-LADR-063 | message-role | RackDevice.delete_selected_variation |
| LADR-064 | REQ-LADR-064 | message-role | RackDevice.View.selected_drum_pad |
| LADR-065 | REQ-LADR-065 | message-role | RackDevice.View.selected_chain |
| LADR-066 | REQ-LADR-066 | message-role | RackDevice.View.drum_pads_scroll_position |
| LADR-067 | REQ-LADR-067 | message-role | RackDevice.View.is_showing_chain_devices |
| LADR-068 | REQ-LADR-068 | message-role | Chain.devices |
| LADR-069 | REQ-LADR-069 | message-role | Chain.mixer_device |
| LADR-070 | REQ-LADR-070 | message-role | Chain.color |
| LADR-071 | REQ-LADR-071 | message-role | Chain.color_index |
| LADR-072 | REQ-LADR-072 | message-role | Chain.is_auto_colored |
| LADR-073 | REQ-LADR-073 | message-role | Chain.has_audio_input |
| LADR-074 | REQ-LADR-074 | message-role | Chain.has_audio_output |
| LADR-075 | REQ-LADR-075 | message-role | Chain.has_midi_input |
| LADR-076 | REQ-LADR-076 | message-role | Chain.has_midi_output |
| LADR-077 | REQ-LADR-077 | message-role | Chain.mute |
| LADR-078 | REQ-LADR-078 | message-role | Chain.muted_via_solo |
| LADR-079 | REQ-LADR-079 | message-role | Chain.name |
| LADR-080 | REQ-LADR-080 | message-role | Chain.solo |
| LADR-081 | REQ-LADR-081 | message-role | Chain.delete_device |
| LADR-082 | REQ-LADR-082 | message-role | Chain.insert_device |
| LADR-083 | REQ-LADR-083 | message-role | ChainMixerDevice.sends |
| LADR-084 | REQ-LADR-084 | message-role | ChainMixerDevice.chain_activator |
| LADR-085 | REQ-LADR-085 | message-role | ChainMixerDevice.panning |
| LADR-086 | REQ-LADR-086 | message-role | ChainMixerDevice.volume |
| LADR-087 | REQ-LADR-087 | message-role | DrumChain.in_note |
| LADR-088 | REQ-LADR-088 | message-role | DrumChain.out_note |
| LADR-089 | REQ-LADR-089 | message-role | DrumChain.choke_group |
| LADR-090 | REQ-LADR-090 | message-role | DrumPad.chains |
| LADR-091 | REQ-LADR-091 | message-role | DrumPad.mute |
| LADR-092 | REQ-LADR-092 | message-role | DrumPad.name |
| LADR-093 | REQ-LADR-093 | message-role | DrumPad.note |
| LADR-094 | REQ-LADR-094 | message-role | DrumPad.solo |
| LADR-095 | REQ-LADR-095 | source-context | DrumPad.delete_all_chains |
| LADR-U-01 | REQ-LADR-U-VERSION | source-context | Publication and inheritance |
| LADR-U-02 | REQ-LADR-U-SHAPES | malformed | Argument and cardinality gaps |
| LADR-U-03 | REQ-LADR-U-CAPABILITY | source-context | Rack send context |
| LADR-U-04 | REQ-LADR-U-CAPABILITY | negative | Invalid and unsupported access |
| LADR-U-05 | REQ-LADR-U-VALUES | numeric | Internal GUI and stored values |
| LADR-U-06 | REQ-LADR-U-VALUES | numeric | Latency color note domains |
| LADR-U-07 | REQ-LADR-U-MUTATION | boundary | Native device insertion boundaries |
| LADR-U-08 | REQ-LADR-U-MUTATION | automation | Automation remote and inactive path |
| LADR-U-09 | REQ-LADR-U-MUTATION | negative | AB comparison eligibility |
| LADR-U-10 | REQ-LADR-U-MACROS | persistence | Mapped variation and last used |
| LADR-U-11 | REQ-LADR-U-MACROS | boundary | Random and pad-copy boundaries |
| LADR-U-12 | REQ-LADR-U-STATE | undo | Undo and redo |
| LADR-U-13 | REQ-LADR-U-STATE | persistence | Save reopen and editor move |
| LADR-U-14 | REQ-LADR-U-STATE | cancel | Cancel and concurrent edits |
| LADR-U-15 | REQ-LADR-U-LIFECYCLE | sample-rate | Transport rate and automation |
| LADR-U-16 | REQ-LADR-U-LIFECYCLE | source-loss | Target source and context loss |
| LADR-U-17 | REQ-LADR-U-LIFECYCLE | recovery | Recovery and re-resolution |
| LADR-U-18 | REQ-LADR-U-LIFECYCLE | teardown | Close with pending work |

## Local questions

- **Q-LADR-001 — Current reference versus target:** The immutable inventory index declares12.4.5; exact12.4.3 and matching Max/platform/member availability remain U. Explicit since11.0/12.3 statements do not prove this target.
- **Q-LADR-002 — Direct and inherited cardinality:** RackDevice/RackDevice.View/DrumChain declare base-class inheritance in source context; the95-direct denominator is not flattened inheritance. Chain.View is absent from R1, not proved absent in Live. Chain.devices is printed Device and DrumPad.chains Chain despite plural names; cardinality remains unresolved.
- **Q-LADR-003 — Chain mixer sends predicate:** ChainMixerDevice.sends source says [in Audio Effect Racks and Instrument Racks only] For Drum Racks, otherwise empty. Preserve the exact source wording and determine eligibility/emptiness later; no repaired graph/predicate is adopted.
- **Q-LADR-004 — Parameter domains and flags:** DeviceParameter value/display_value/default/min/max and quantized/enabled/state/automation flags do not establish API-to-stored/native units, type widths, converters, precedence or numerical/no-audible-effect results. StringVector/unicode/long retain printed names only.
- **Q-LADR-005 — Missing arguments returns and sparse declarations:** Only six functions have explicit typed parameter declarations and two a typed return. Undocumented is not zero arguments/void. DrumPad.delete_all_chains is a heading only and semantic U; sparse capability/child headings do not justify behavior from their names.
- **Q-LADR-006 — Mixer roots units and colors:** Source master-track/API path naming is not silently changed to Main, nor are API enum codes equated to finite stored/native values. Samples/ms latency members supply no clock/conversion/compensation formula. RGB/nearest palette/MIDI note/choke descriptions give no new codec, distance metric or sound law.
- **Q-LADR-007 — Insertion and compare predicates:** 12.3 insertion and AB compare support/error roles retain native-only/type-order/optional-index and can_compare_ab conditions. Complete acceptance, invalid-index/no-object outcomes, exact errors, return and transactions remain unknown.
- **Q-LADR-008 — Macro variation and selection scope:** Visible counts, mapped Macros, selected versus last-recalled variation and eligible randomization remain distinct. No seed/distribution/mandatory change, copied-value equality, count limit, default, no-selection or persistence law follows.
- **Q-LADR-009 — Access history notification and lifecycle:** Declared get/set/observe is documentary access, not accepted runtime proof. Mutation-time callbacks, override/remote/re-enable, Undo, save/reopen/editor moves, cancellation/concurrency, transport/rate, target/source/context loss and teardown remain ungraded with positive active context required.

## Analyst evidence and immutable freeze

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/sources.json) reuses ten exact unchanged R1 publisher
HTML identities from [the immutable inventory](../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json).
Each record preserves original URL/final URL, capture UTC, bytes/SHA and version
scope; no recapture occurred. All315 selected text blocks were read. No figure,
linked source, script, patch, example, Max/API/original/native/candidate/hardware
runtime, emulator, installation or network-service operation was executed.
Private architecture, inheritance, alias, missing text or numeric laws are not
reconstructed from examples or names.

[Inventory pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/inventory-pins.json) protect original R1 artifacts
and the read-only validation also checks all65 original R1 payloads.
[Owner pins](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/owner-pins.json), [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/counts.json),
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/manifest-author-r1.json), two canonical snapshots and
[read-only validator](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-device-rack/validate.py) identify this partial author
revision. Run the validator with `python -B`; it prints stdout only and never
rewrites frozen sources, snapshots or reports. Independent review and exact-target
evidence remain required. Shared indexes/coverage/questions/log remain root-owned.
