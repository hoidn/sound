# Proposed five-profile synthesis metadata scope

Pending Root scope choice. Metadata census/proposal only; no map or raw-row materialization.

Census: `analysis/ableton-live-12.4.3/full-spec-v1/family-synthesis-instruments-routes-v1/metadata-scope-census.json`, 71024 bytes, SHA256 `337dca125b2672cf8c5b9d53ff03bcb9862b2dda54f9bd644179a18e2ada5ad3`.

Broad case-insensitive tokens match793 address-point candidates/657 literal encodings/15,302 exported-prefix slots/1,530 store annotations and15,913 alias entries. Exact core class tokens still match636 aliases. Nested wrappers/UI and unrelated Operator expressions make these discovery counts, not actual family class/function counts. Exploratory broad metadata displays were truncated; no raw rows were retained or adopted. An exploratory membership query met an exported-vtable-label record without candidates; final census explicitly selects alias memberships. No C/native body read.

Propose all24 exact primary core classes below plus ALL8 exact typed WavetableUnisonOscillator specializations:32 primary address points,124selected slots,50actual lexical-store rows. Fourteen large prefixes retain leading3 construction/lifetime entries only;18small prefixes retain whole2/3/6/8exported entries. No prefix proves complete class/vtable/ABI/native extent.

| Family | Exact proposed class/type | AP | Exported | Selected |
| --- | --- | --- | ---: | ---: |
| Operator | `OInstrumentOperatorProcessor` | `0x10675d638` | 3 | 3 |
| Drift | `ODriftProcessor` | `0x1067627e0` | 3 | 3 |
| Wavetable | `OInstrumentWavetableProcessor` | `0x106765c80` | 3 | 3 |
| Meld | `OMeldProcessor` | `0x10676a340` | 3 | 3 |
| Operator | `OInstrumentOperatorFilterProcessor` | `0x10676ded0` | 3 | 3 |
| Operator | `OOperatorLfoControlProcessor` | `0x10676def8` | 3 | 3 |
| Operator | `OOperatorOperatorVoiceProcessor` | `0x10676df20` | 3 | 3 |
| Operator | `OOperatorVoiceManagementProcessor` | `0x10676df68` | 8 | 8 |
| Drum Sampler | `ODrumSamplerProcessor` | `0x106776760` | 3 | 3 |
| Drum Sampler | `ODrumSamplerSampleHolder` | `0x106777f50` | 2 | 2 |
| Drift | `ADriftModule` | `0x1068573c0` | 89 | 3 |
| Drum Sampler | `ADrumSampler` | `0x106859028` | 65 | 3 |
| Drum Sampler | `LDrumSampler` | `0x106859758` | 128 | 3 |
| Drum Sampler | `ADrumSamplerModule` | `0x106859ea0` | 89 | 3 |
| Drift | `ADrift` | `0x10686ae20` | 65 | 3 |
| Drift | `LDrift` | `0x10686b628` | 128 | 3 |
| Meld | `AInstrumentMeld` | `0x10686e0d0` | 65 | 3 |
| Meld | `LInstrumentMeld` | `0x10686e8a8` | 128 | 3 |
| Meld | `AInstrumentMeldModule` | `0x10686f080` | 89 | 3 |
| Operator | `AOperator` | `0x106871028` | 128 | 3 |
| Wavetable | `AInstrumentWavetable` | `0x106875198` | 65 | 3 |
| Wavetable | `LInstrumentWavetable` | `0x106875ad0` | 128 | 3 |
| Wavetable | `AInstrumentWavetableModule` | `0x1068768d8` | 89 | 3 |
| Operator | `AOperatorSynthesisModule` | `0x10688eba8` | 89 | 3 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS3_6PhasorIfLNS3_9DirectionE0EEELNS4_13InterpolationE1EEEEE` | `0x106af73a0` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS3_6PhasorIfLNS3_9DirectionE0EEELNS4_13InterpolationE0EEEEE` | `0x106af7658` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_24FrequencyModulatedPhasorIfLNS4_9SineModelE0EEELNS4_13InterpolationE0EEEEE` | `0x106af7700` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_15ClassicPdPhasorIfEELNS4_13InterpolationE0EEEEE` | `0x106af77b8` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_14ModernPdPhasorIfEELNS4_13InterpolationE0EEEEE` | `0x106af7860` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_24FrequencyModulatedPhasorIfLNS4_9SineModelE1EEELNS4_13InterpolationE1EEEEE` | `0x106af7908` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_15ClassicPdPhasorIfEELNS4_13InterpolationE1EEEEE` | `0x106af79b0` | 6 | 6 |
| Wavetable | `N7ableton7devices9wavetable25WavetableUnisonOscillatorINS_6blocks9wavetable19WavetableOscillatorINS4_14ModernPdPhasorIfEELNS4_13InterpolationE1EEEEE` | `0x106af7a58` | 6 | 6 |

The full table/store/named union has153sources and542one-hop rows, over128seeds/512rows. **Stop before raw retention of that union.**

Proposed call scope: complete selected-slot-target plus12named-wrapper union,115sources/246direct+37indirect=283rows. Keep32table headers/124slots/50stores and153alias+22membership rows (=175) as metadata. Do not follow38additional store-only source entries; their constructor/receiver/ABI/effects remain explicit frontiers. This preserves construction continuity and whole small processor/typed-oscillator prefixes, not arbitrary first-N selection.

The alternative complete small-prefix+named set is86sources/212direct+27indirect=239rows, but115fits and retains large construction continuity. Root chooses; neither alternative silently adopted.

The exact named selector yields twelve Operator-qualified wrappers only. Missing matches for other profiles are unknown symbol frontiers, not native absence. Nine outermost Wavetable LFO/oscillator/envelope/filter lexical owners have144memberships but are outside this fixed wrapper selector; do not guess direct native main-processing names. Nested generic InvokeFunctionFactory/RealtimeModel matches are not actual processors.

Unselected: secondary/adjusted APs, UI/control/RealtimeModel/observer wrappers, generic DeviceKit buffer-rate wrapper tables, Drum sample-manager/service/browser frontiers, extra Operator shaper/wavetable/aux-envelope classes and all encountered/incoming/transitive callees/globals/slots. Required cross-owner behavior remains in the later ledger with unknown delivery. Schema/package classnames are not inverted into runtime binding.

All110IDs/190actualU unchanged;567-source semantics inherited, later geometry mechanical only. No fullspec snapshot/case-body copies, canonical edit, finalmanifest, original/provider/native/decoder/harness/model/comparator/fixture/build or oldmodule execution. Root owns scope/finalmanifest/shared pages. Later map extends approved I07/I08+Mix/Automation/sample boundaries; requiredunsupportedU/coverageOPEN/no documentaryfallback, no successor/grade/site.
