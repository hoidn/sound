---
id: SRC-CYCLING74-LIVE-API
type: source
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Current Cycling74 public API reference; index declares Live12.4.5; target12.4.3 applicability unknown
---

# Cycling74 Live API source inventory

## Authority, capture and scope

Publisher: Cycling74. The current [Live Object Model index](https://docs.cycling74.com/apiref/lom/)
explicitly declares **Ableton Live12.4.5**. The project's target is12.4.3;
no object, member, signature, enum, event, default or lifecycle behavior becomes
target evidence merely because the publisher page or name matches. The
[API overview](https://docs.cycling74.com/userguide/m4l/live_api_overview/)
and six bridge/lifecycle references have no independently pinned matching Max
version here. Captured2026-10-19; exact URL/final URL/UTC/byte/hash identities
are in the [53-source catalog](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/all-sources-r1.json).

This source family adds a separate overlapping discovery dimension under
[the full-product inventory](../full-live-coverage-inventory.md) and
[plan](../full-live-specification-plan.md) F-05/F-08. It is source discovery,
not a draft API implementation contract, behavioral coverage, a complete Max
runtime scope or an independent review of every documented semantic claim.
[Max hosting](../../specs/max-for-live-hosting.md) retains its existing partial
scope; no host/device/template/release is expanded by retaining these sources.

## Finite discovered reference surface

| Dimension | Retained count | Limit |
| --- | ---: | --- |
| LOM index reference entries |45| Includes root/view/derived/reference roles; not45independent features or a guaranteed set of runtime class types |
| Explicit member declarations |588|64children/361properties/163functions from direct section headings only; inherited members and aliases not flattened |
| Bridge/lifecycle references |6|live.path, live.object, live.observer, live.remote~, live.thisdevice and JavaScript LiveAPI; signatures/events and generic Max attributes not yet reconciled |
| Source pages |53| Index, overview,45listed references and6bridge/lifecycle references |
| Derived blocks |2801| Article-scoped headings/paragraph/list/code/table cells with exact HTML line/column; extraction is not semantic approval |
| Complete API entries |0|Every entry/member has targetU and unresolved clause/case ownership |

These counts overlap manual/device/schema/controller surfaces; never add them to
those denominators or report a percentage of compatible API. No transitive closure,
complete inherited method surface, overload schema or supported-version matrix is
claimed. The index itself and bridge generic Max common-box attributes need explicit
disposition rather than automatic inclusion as Live-specific behavioral members.

[LOM entries](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/lom-entries.json),
[explicit member declarations](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/lom-members.json)
and [bridge entry points](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/bridge-entrypoints.json)
retain stable within-capture IDs and exact source/heading locations. Declared
member count below does not include inherited definitions or validate their types.

| Reference entry | Explicit member headings | Source |
| --- | ---: | --- |
| Application | 13 | [publisher reference](https://docs.cycling74.com/apiref/lom/application/) |
| Application.View | 10 | [publisher reference](https://docs.cycling74.com/apiref/lom/application_view/) |
| Chain | 15 | [publisher reference](https://docs.cycling74.com/apiref/lom/chain/) |
| ChainMixerDevice | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/chainmixerdevice/) |
| Clip | 77 | [publisher reference](https://docs.cycling74.com/apiref/lom/clip/) |
| Clip.View | 6 | [publisher reference](https://docs.cycling74.com/apiref/lom/clip_view/) |
| ClipSlot | 19 | [publisher reference](https://docs.cycling74.com/apiref/lom/clipslot/) |
| CompressorDevice | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/compressordevice/) |
| ControlSurface | 10 | [publisher reference](https://docs.cycling74.com/apiref/lom/controlsurface/) |
| CuePoint | 3 | [publisher reference](https://docs.cycling74.com/apiref/lom/cuepoint/) |
| Device | 15 | [publisher reference](https://docs.cycling74.com/apiref/lom/device/) |
| Device.View | 1 | [publisher reference](https://docs.cycling74.com/apiref/lom/device_view/) |
| DeviceIO | 5 | [publisher reference](https://docs.cycling74.com/apiref/lom/deviceio/) |
| DeviceParameter | 15 | [publisher reference](https://docs.cycling74.com/apiref/lom/deviceparameter/) |
| DriftDevice | 29 | [publisher reference](https://docs.cycling74.com/apiref/lom/driftdevice/) |
| DrumCellDevice | 1 | [publisher reference](https://docs.cycling74.com/apiref/lom/drumcelldevice/) |
| DrumChain | 3 | [publisher reference](https://docs.cycling74.com/apiref/lom/drumchain/) |
| DrumPad | 6 | [publisher reference](https://docs.cycling74.com/apiref/lom/drumpad/) |
| Eq8Device | 3 | [publisher reference](https://docs.cycling74.com/apiref/lom/eq8device/) |
| Eq8Device.View | 1 | [publisher reference](https://docs.cycling74.com/apiref/lom/eq8device_view/) |
| Groove | 6 | [publisher reference](https://docs.cycling74.com/apiref/lom/groove/) |
| GroovePool | 1 | [publisher reference](https://docs.cycling74.com/apiref/lom/groovepool/) |
| HybridReverbDevice | 8 | [publisher reference](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/) |
| LooperDevice | 16 | [publisher reference](https://docs.cycling74.com/apiref/lom/looperdevice/) |
| MaxDevice | 7 | [publisher reference](https://docs.cycling74.com/apiref/lom/maxdevice/) |
| MeldDevice | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/melddevice/) |
| MixerDevice | 11 | [publisher reference](https://docs.cycling74.com/apiref/lom/mixerdevice/) |
| PluginDevice | 3 | [publisher reference](https://docs.cycling74.com/apiref/lom/plugindevice/) |
| RackDevice | 21 | [publisher reference](https://docs.cycling74.com/apiref/lom/rackdevice/) |
| RackDevice.View | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/rackdevice_view/) |
| RoarDevice | 3 | [publisher reference](https://docs.cycling74.com/apiref/lom/roardevice/) |
| Sample | 28 | [publisher reference](https://docs.cycling74.com/apiref/lom/sample/) |
| Scene | 14 | [publisher reference](https://docs.cycling74.com/apiref/lom/scene/) |
| ShifterDevice | 2 | [publisher reference](https://docs.cycling74.com/apiref/lom/shifterdevice/) |
| SimplerDevice | 19 | [publisher reference](https://docs.cycling74.com/apiref/lom/simplerdevice/) |
| SimplerDevice.View | 1 | [publisher reference](https://docs.cycling74.com/apiref/lom/simplerdevice_view/) |
| Song | 91 | [publisher reference](https://docs.cycling74.com/apiref/lom/song/) |
| Song.View | 11 | [publisher reference](https://docs.cycling74.com/apiref/lom/song_view/) |
| SpectralResonatorDevice | 7 | [publisher reference](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/) |
| TakeLane | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/takelane/) |
| this_device | 0 | [publisher reference](https://docs.cycling74.com/apiref/lom/this_device/) |
| Track | 57 | [publisher reference](https://docs.cycling74.com/apiref/lom/track/) |
| Track.View | 4 | [publisher reference](https://docs.cycling74.com/apiref/lom/track_view/) |
| TuningSystem | 6 | [publisher reference](https://docs.cycling74.com/apiref/lom/tuningsystem/) |
| WavetableDevice | 20 | [publisher reference](https://docs.cycling74.com/apiref/lom/wavetabledevice/) |

## Method, review and required next evidence

The [capture helper](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/capture_classes.py)
reads only the45exact index article links and retains their HTML; no page script,
Max code, example, original application, patch, JavaScript LiveAPI or API call ran.
The [deriver](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/derive_inventory.py)
checks all53source hashes, extracts article-scoped blocks, and records h3members
only under Children/Properties/Functions. A small synthetic boundary/nesting/table
self-check guards against navigation/footer text entering the inventory. Replay
with `python -B .../derive_inventory.py --check` is read-only after sealing.

Author inspected index membership, overview headings/link structure and Application/
Clip declaration structure to establish the extraction method. The2801blocks were
mechanically retained, not all independently read for behavioral meaning. Source
figures/layout/examples are unexecuted and uninspected. Shared final review is still
pending for source inventory mechanics; it cannot approve all member semantics.
The [inventory seal](../../../analysis/ableton-live-12.4.3/full-spec-v1/max-api/manifest-inventory-r1.json)
pins current bytes and this source-page snapshot. No original source was overwritten.

Required next work: independently review inventory mechanics, retain inheritance/
alias/root and bridge/member applicability decisions, then author public path/ID,
get/set/call/observe/remote and initialization/notification/lifecycle contracts.
Missing, invalid, unavailable, read-only/nonobservable, deletion/reorder, persistence,
mutation during callback, malformed arguments, scheduling and teardown need finite
cases and evidence. Live12.4.5 claims and placeholder prose such as live.path's
standalone getid TEXT_HERE section stay unresolved; do not fill blanks from examples
or infer contradiction with its separately documented bang/getid section.

Runtime thread/defer descriptions are publisher context, not required candidate
architecture or a latency guarantee. Numeric transforms/coordinates/gain/tempo/
MIDI encodings from newer public API sources cannot silently replace the existing
finite/native owners. Actual object IDs, event order, message grammar, errors,
callback reentrancy, signal remote behavior and target outcomes remain unknown.
No application/candidate/compatibility test or clean implementation was performed.
