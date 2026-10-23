---
id: SPEC-LIVE-API-SPECIALIZED-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current public API applicability U
---

# Specialized device API declarations

Partial direct-member roles for14 exact current-public references/108declarations.
The publisher index states12.4.5; all exact12.4.3 outcomes/applicability remain U.
Raw publication role text is retained in each clause as documentary data with its
own type/access/context caveats, never an executed result, guessed ABI or complete
branch contract. No original application/function/API/Max/JS/patch/example,
candidate, audio/MIDI/hardware or service operation ran.

[Bridge](live-api-bridge-workflows.md) and [control/routing](live-api-control-tuning.md)
retain generic message/bus roles. [Dynamics](dynamics-devices.md),
[synthesis](synthesis-instruments.md), [filter/EQ](filter-eq-devices.md),
[delay/reverb](delay-reverb-devices.md), [modulation](modulation-pitch-loop-devices.md),
[distortion](distortion-devices.md), [Max hosting](max-for-live-hosting.md),
[plug-in hosting](plugin-hosting.md), [routing](routing-monitoring-latency.md),
[MPE](mpe-workflows.md), [tuning](tuning-systems.md) and [racks](device-racks.md)
retain their workflow, processing, values/storage and lifecycle laws. Generic
Device/View API members are a separate owner: no inheritance is flattened here.

## Documentary direct-member contracts

### REQ-LAPI-SPECIALIZED-001 — CompressorDevice.available_input_routing_channels

**D-current-public/target-U.** For CompressorDevice.available_input_routing_channels, the published declaration is dict with getobserve. Documentary role: The list of available source channels for the compressor's input routing in the sidechain. It's represented as a dictionary with the following key: available_input_routing_channels [list] The list contains dictionaries as described in input_routing_channel. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/compressordevice/#available_input_routing_channels), `C74-LOM-COMPRESSORDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-002 — CompressorDevice.available_input_routing_types

**D-current-public/target-U.** For CompressorDevice.available_input_routing_types, the published declaration is dict with getobserve. Documentary role: The list of available source types for the compressor's input routing in the sidechain. It's represented as a dictionary with the following key: available_input_routing_types [list] The list contains dictionaries as described in input_routing_type. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/compressordevice/#available_input_routing_types), `C74-LOM-COMPRESSORDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-003 — CompressorDevice.input_routing_channel

**D-current-public/target-U.** For CompressorDevice.input_routing_channel, the published declaration is dict with getsetobserve. Documentary role: The currently selected source channel for the compressor's input routing in the sidechain. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the compressor's available_input_routing_channels. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/compressordevice/#input_routing_channel), `C74-LOM-COMPRESSORDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-004 — CompressorDevice.input_routing_type

**D-current-public/target-U.** For CompressorDevice.input_routing_type, the published declaration is dict with getsetobserve. Documentary role: The currently selected source type for the compressor's input routing in the sidechain. It's represented as a dictionary with the following keys: display_name [symbol] identifier [symbol] Can be set to all values found in the track's available_input_routing_types. The setter cross-reference says track available_input_routing_types, while the class also declares its own compressor availability list. Preserve this context question; do not silently repair the owning object. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/compressordevice/#input_routing_type), `C74-LOM-COMPRESSORDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-005 — DriftDevice.mod_matrix_filter_source_1_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_filter_source_1_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating the Filter Frequency for the first modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_filter_source_1_index), `C74-LOM-DRIFTDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-006 — DriftDevice.mod_matrix_filter_source_1_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_filter_source_1_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating the Filter Frequency for the first modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_filter_source_1_list), `C74-LOM-DRIFTDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-007 — DriftDevice.mod_matrix_filter_source_2_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_filter_source_2_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating the Filter Frequency for the second modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_filter_source_2_index), `C74-LOM-DRIFTDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-008 — DriftDevice.mod_matrix_filter_source_2_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_filter_source_2_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating the Filter Frequency for the second modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_filter_source_2_list), `C74-LOM-DRIFTDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-009 — DriftDevice.mod_matrix_lfo_source_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_lfo_source_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating the LFO Amount. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_lfo_source_index), `C74-LOM-DRIFTDEVICE` B0016, B0017, B0018.

### REQ-LAPI-SPECIALIZED-010 — DriftDevice.mod_matrix_lfo_source_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_lfo_source_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating the LFO Amount. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_lfo_source_list), `C74-LOM-DRIFTDEVICE` B0019, B0020, B0021.

### REQ-LAPI-SPECIALIZED-011 — DriftDevice.mod_matrix_pitch_source_1_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_pitch_source_1_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating the Pitch for the first modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_pitch_source_1_index), `C74-LOM-DRIFTDEVICE` B0022, B0023, B0024.

### REQ-LAPI-SPECIALIZED-012 — DriftDevice.mod_matrix_pitch_source_1_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_pitch_source_1_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating the Pitch for the first modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_pitch_source_1_list), `C74-LOM-DRIFTDEVICE` B0025, B0026, B0027.

### REQ-LAPI-SPECIALIZED-013 — DriftDevice.mod_matrix_pitch_source_2_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_pitch_source_2_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating the Pitch for the second modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_pitch_source_2_index), `C74-LOM-DRIFTDEVICE` B0028, B0029, B0030.

### REQ-LAPI-SPECIALIZED-014 — DriftDevice.mod_matrix_pitch_source_2_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_pitch_source_2_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating the Pitch for the second modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_pitch_source_2_list), `C74-LOM-DRIFTDEVICE` B0031, B0032, B0033.

### REQ-LAPI-SPECIALIZED-015 — DriftDevice.mod_matrix_shape_source_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_shape_source_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for modulating Shape. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_shape_source_index), `C74-LOM-DRIFTDEVICE` B0034, B0035, B0036.

### REQ-LAPI-SPECIALIZED-016 — DriftDevice.mod_matrix_shape_source_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_shape_source_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for modulating Shape. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_shape_source_list), `C74-LOM-DRIFTDEVICE` B0037, B0038, B0039.

### REQ-LAPI-SPECIALIZED-017 — DriftDevice.mod_matrix_source_1_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_1_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for the first custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_1_index), `C74-LOM-DRIFTDEVICE` B0040, B0041, B0042.

### REQ-LAPI-SPECIALIZED-018 — DriftDevice.mod_matrix_source_1_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_1_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for the first custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_1_list), `C74-LOM-DRIFTDEVICE` B0043, B0044, B0045.

### REQ-LAPI-SPECIALIZED-019 — DriftDevice.mod_matrix_source_2_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_2_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for the second custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_2_index), `C74-LOM-DRIFTDEVICE` B0046, B0047, B0048.

### REQ-LAPI-SPECIALIZED-020 — DriftDevice.mod_matrix_source_2_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_2_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for the second custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_2_list), `C74-LOM-DRIFTDEVICE` B0049, B0050, B0051.

### REQ-LAPI-SPECIALIZED-021 — DriftDevice.mod_matrix_source_3_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_3_index, the published declaration is int with getsetobserve. Documentary role: The index of the available sources for the third custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_3_index), `C74-LOM-DRIFTDEVICE` B0052, B0053, B0054.

### REQ-LAPI-SPECIALIZED-022 — DriftDevice.mod_matrix_source_3_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_source_3_list, the published declaration is StringVector with get. Documentary role: The list of the available sources for the third custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_source_3_list), `C74-LOM-DRIFTDEVICE` B0055, B0056, B0057.

### REQ-LAPI-SPECIALIZED-023 — DriftDevice.mod_matrix_target_1_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_1_index, the published declaration is int with getsetobserve. Documentary role: The index of the available targets for the first custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_1_index), `C74-LOM-DRIFTDEVICE` B0058, B0059, B0060.

### REQ-LAPI-SPECIALIZED-024 — DriftDevice.mod_matrix_target_1_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_1_list, the published declaration is StringVector with get. Documentary role: The list of the available targets for the first custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_1_list), `C74-LOM-DRIFTDEVICE` B0061, B0062, B0063.

### REQ-LAPI-SPECIALIZED-025 — DriftDevice.mod_matrix_target_2_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_2_index, the published declaration is int with getsetobserve. Documentary role: The index of the available targets for the second custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_2_index), `C74-LOM-DRIFTDEVICE` B0064, B0065, B0066.

### REQ-LAPI-SPECIALIZED-026 — DriftDevice.mod_matrix_target_2_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_2_list, the published declaration is StringVector with get. Documentary role: The list of the available targets for the second custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_2_list), `C74-LOM-DRIFTDEVICE` B0067, B0068, B0069.

### REQ-LAPI-SPECIALIZED-027 — DriftDevice.mod_matrix_target_3_index

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_3_index, the published declaration is int with getsetobserve. Documentary role: The index of the available targets for the third custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_3_index), `C74-LOM-DRIFTDEVICE` B0070, B0071, B0072.

### REQ-LAPI-SPECIALIZED-028 — DriftDevice.mod_matrix_target_3_list

**D-current-public/target-U.** For DriftDevice.mod_matrix_target_3_list, the published declaration is StringVector with get. Documentary role: The list of the available targets for the third custom modulation slot. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#mod_matrix_target_3_list), `C74-LOM-DRIFTDEVICE` B0073, B0074, B0075.

### REQ-LAPI-SPECIALIZED-029 — DriftDevice.pitch_bend_range

**D-current-public/target-U.** For DriftDevice.pitch_bend_range, the published declaration is int with getsetobserve. Documentary role: The amount for the MIDI Pitch Bend range in semitones. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#pitch_bend_range), `C74-LOM-DRIFTDEVICE` B0076, B0077, B0078.

### REQ-LAPI-SPECIALIZED-030 — DriftDevice.voice_count_index

**D-current-public/target-U.** For DriftDevice.voice_count_index, the published declaration is int with getsetobserve. Documentary role: The index of the voice count parameter. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#voice_count_index), `C74-LOM-DRIFTDEVICE` B0079, B0080, B0081.

### REQ-LAPI-SPECIALIZED-031 — DriftDevice.voice_count_list

**D-current-public/target-U.** For DriftDevice.voice_count_list, the published declaration is StringVector with get. Documentary role: The list of available voice count settings. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#voice_count_list), `C74-LOM-DRIFTDEVICE` B0082, B0083, B0084.

### REQ-LAPI-SPECIALIZED-032 — DriftDevice.voice_mode_index

**D-current-public/target-U.** For DriftDevice.voice_mode_index, the published declaration is int with getsetobserve. Documentary role: The index of the voice mode utilized by Drift. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#voice_mode_index), `C74-LOM-DRIFTDEVICE` B0085, B0086, B0087.

### REQ-LAPI-SPECIALIZED-033 — DriftDevice.voice_mode_list

**D-current-public/target-U.** For DriftDevice.voice_mode_list, the published declaration is StringVector with get. Documentary role: The list of available voice modes. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/driftdevice/#voice_mode_list), `C74-LOM-DRIFTDEVICE` B0088, B0089, B0090.

### REQ-LAPI-SPECIALIZED-034 — DrumCellDevice.gain

**D-current-public/target-U.** For DrumCellDevice.gain, the published declaration is float with getsetobserve. Documentary role: The sample gain, as normalized value. Normalized is the only range description here; no zero-to-one domain or gain-to-amplitude mapping is supplied. The class description identifies Drum Sampler; its public class spelling is retained. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/drumcelldevice/#gain), `C74-LOM-DRUMCELLDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-035 — Eq8Device.edit_mode

**D-current-public/target-U.** For Eq8Device.edit_mode, the published declaration is bool with getsetobserve. Documentary role: Access to EQ Eight's edit mode, which toggles the channel currently available for editing. The available edit modes depend on the global mode (see global_mode) and are encoded as follows: In L/R mode: 0 = L, 1 = R In M/S mode: 0 = M, 1 = S In Stereo mode: 0 = A, 1 = B (inactive) Channel encoding depends on global_mode: L/R0L1R, M/S0M1S, Stereo0A1B(inactive). No new channel-processing law or inactive-write result follows. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/eq8device/#edit_mode), `C74-LOM-EQ8DEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-036 — Eq8Device.global_mode

**D-current-public/target-U.** For Eq8Device.global_mode, the published declaration is int with getsetobserve. Documentary role: Access to EQ Eight's global mode. The modes are encoded as follows: 0 = Stereo 1 = L/R 2 = M/S This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/eq8device/#global_mode), `C74-LOM-EQ8DEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-037 — Eq8Device.oversample

**D-current-public/target-U.** For Eq8Device.oversample, the published declaration is bool with getsetobserve. Documentary role: Access to EQ Eight's Oversampling parameter. 0 = Off, 1 = On. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/eq8device/#oversample), `C74-LOM-EQ8DEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-038 — Eq8Device.View.selected_band

**D-current-public/target-U.** For Eq8Device.View.selected_band, the published declaration is int with getsetobserve. Documentary role: The index of the currently selected filter band. No band-index base, accepted interval or out-of-range policy is supplied. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/eq8device_view/#selected_band), `C74-LOM-EQ8DEVICE_VIEW` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-039 — HybridReverbDevice.ir_attack_time

**D-current-public/target-U.** For HybridReverbDevice.ir_attack_time, the published declaration is float with getsetobserve. Documentary role: The attack time of the amplitude envelope for the impulse response, in seconds. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_attack_time), `C74-LOM-HYBRIDREVERBDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-040 — HybridReverbDevice.ir_category_index

**D-current-public/target-U.** For HybridReverbDevice.ir_category_index, the published declaration is int with getsetobserve. Documentary role: The index of the selected impulse response category. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_category_index), `C74-LOM-HYBRIDREVERBDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-041 — HybridReverbDevice.ir_category_list

**D-current-public/target-U.** For HybridReverbDevice.ir_category_list, the published declaration is StringVector with get. Documentary role: The list of impulse response categories. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_category_list), `C74-LOM-HYBRIDREVERBDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-042 — HybridReverbDevice.ir_decay_time

**D-current-public/target-U.** For HybridReverbDevice.ir_decay_time, the published declaration is float with getsetobserve. Documentary role: The decay time of the amplitude envelope for the impulse response, in seconds. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_decay_time), `C74-LOM-HYBRIDREVERBDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-043 — HybridReverbDevice.ir_file_index

**D-current-public/target-U.** For HybridReverbDevice.ir_file_index, the published declaration is int with getsetobserve. Documentary role: The index of the selected impulse response files from the current category. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_file_index), `C74-LOM-HYBRIDREVERBDEVICE` B0016, B0017, B0018.

### REQ-LAPI-SPECIALIZED-044 — HybridReverbDevice.ir_file_list

**D-current-public/target-U.** For HybridReverbDevice.ir_file_list, the published declaration is StringVector with getobserve. Documentary role: The list of impulse response files from the selected category. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_file_list), `C74-LOM-HYBRIDREVERBDEVICE` B0019, B0020, B0021.

### REQ-LAPI-SPECIALIZED-045 — HybridReverbDevice.ir_size_factor

**D-current-public/target-U.** For HybridReverbDevice.ir_size_factor, the published declaration is float with getsetobserve. Documentary role: The relative size of the impulse response, 0.0 to 1.0. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_size_factor), `C74-LOM-HYBRIDREVERBDEVICE` B0022, B0023, B0024.

### REQ-LAPI-SPECIALIZED-046 — HybridReverbDevice.ir_time_shaping_on

**D-current-public/target-U.** For HybridReverbDevice.ir_time_shaping_on, the published declaration is bool with getsetobserve. Documentary role: Enables transforming the current selected impulse response with an amplitude envelope and size parameter. 1 = enabled. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/hybridreverbdevice/#ir_time_shaping_on), `C74-LOM-HYBRIDREVERBDEVICE` B0025, B0026, B0027.

### REQ-LAPI-SPECIALIZED-047 — LooperDevice.loop_length

**D-current-public/target-U.** For LooperDevice.loop_length, the published declaration is float with getobserve. Documentary role: The length of Looper's buffer. The unit and valid empty/recording context are unspecified; do not infer beats, seconds or samples. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#loop_length), `C74-LOM-LOOPERDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-048 — LooperDevice.overdub_after_record

**D-current-public/target-U.** For LooperDevice.overdub_after_record, the published declaration is bool with getsetobserve. Documentary role: 1 = Looper will switch to overdub after recording, when recording a fixed number of bars. 0 = switch to playback without overdubbing. This is scoped to recording a fixed number of bars; do not generalize it to every stop or free-length recording. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#overdub_after_record), `C74-LOM-LOOPERDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-049 — LooperDevice.record_length_index

**D-current-public/target-U.** For LooperDevice.record_length_index, the published declaration is int with getsetobserve. Documentary role: Access to the Record Length chooser entry index. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#record_length_index), `C74-LOM-LOOPERDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-050 — LooperDevice.record_length_list

**D-current-public/target-U.** For LooperDevice.record_length_list, the published declaration is StringVector with get. Documentary role: Access to the list of Record Length chooser entry strings. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#record_length_list), `C74-LOM-LOOPERDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-051 — LooperDevice.tempo

**D-current-public/target-U.** For LooperDevice.tempo, the published declaration is float with getobserve. Documentary role: The tempo of Looper's buffer. The body supplies no explicit unit, accuracy, setter or detector law. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#tempo), `C74-LOM-LOOPERDEVICE` B0016, B0017, B0018.

### REQ-LAPI-SPECIALIZED-052 — LooperDevice.clear

**D-current-public/target-U.** For LooperDevice.clear, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Erase Looper's recorded content. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#clear), `C74-LOM-LOOPERDEVICE` B0020, B0021.

### REQ-LAPI-SPECIALIZED-053 — LooperDevice.double_speed

**D-current-public/target-U.** For LooperDevice.double_speed, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Double the speed of Looper's playback. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#double_speed), `C74-LOM-LOOPERDEVICE` B0022, B0023.

### REQ-LAPI-SPECIALIZED-054 — LooperDevice.half_speed

**D-current-public/target-U.** For LooperDevice.half_speed, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Halve the speed of Looper's playback. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#half_speed), `C74-LOM-LOOPERDEVICE` B0024, B0025.

### REQ-LAPI-SPECIALIZED-055 — LooperDevice.double_length

**D-current-public/target-U.** For LooperDevice.double_length, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Double the length of Looper's buffer. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#double_length), `C74-LOM-LOOPERDEVICE` B0026, B0027.

### REQ-LAPI-SPECIALIZED-056 — LooperDevice.half_length

**D-current-public/target-U.** For LooperDevice.half_length, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Halve the length of Looper's buffer. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#half_length), `C74-LOM-LOOPERDEVICE` B0028, B0029.

### REQ-LAPI-SPECIALIZED-057 — LooperDevice.record

**D-current-public/target-U.** For LooperDevice.record, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Record incoming audio. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#record), `C74-LOM-LOOPERDEVICE` B0030, B0031.

### REQ-LAPI-SPECIALIZED-058 — LooperDevice.overdub

**D-current-public/target-U.** For LooperDevice.overdub, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Play back while adding additional layers of incoming audio. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#overdub), `C74-LOM-LOOPERDEVICE` B0032, B0033.

### REQ-LAPI-SPECIALIZED-059 — LooperDevice.play

**D-current-public/target-U.** For LooperDevice.play, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Play back without overdubbing. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#play), `C74-LOM-LOOPERDEVICE` B0034, B0035.

### REQ-LAPI-SPECIALIZED-060 — LooperDevice.stop

**D-current-public/target-U.** For LooperDevice.stop, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Stop Looper's playback. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#stop), `C74-LOM-LOOPERDEVICE` B0036, B0037.

### REQ-LAPI-SPECIALIZED-061 — LooperDevice.undo

**D-current-public/target-U.** For LooperDevice.undo, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Erase everything that was recorded since the last time Overdub was enabled. Calling a second time will restore the material erased by the previous undo operation. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#undo), `C74-LOM-LOOPERDEVICE` B0038, B0039.

### REQ-LAPI-SPECIALIZED-062 — LooperDevice.export_to_clip_slot

**D-current-public/target-U.** For LooperDevice.export_to_clip_slot, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameter: clip_slot [ClipSlot] The target clip slot. Given a valid LOM ID of an empty clip slot on a non-frozen audio track, will export Looper's content to a clip in that slot. This is similar to using the Drag Me! control on the Looper device, and the same restrictions apply: the audio engine must be turned on, the Looper must actually hold audio content, the content must have a fixed length (i.e. Looper must not be recording), etc. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/looperdevice/#export_to_clip_slot), `C74-LOM-LOOPERDEVICE` B0040, B0041.

### REQ-LAPI-SPECIALIZED-063 — MaxDevice.audio_inputs

**D-current-public/target-U.** For MaxDevice.audio_inputs, the published declaration is list of DeviceIO with getobserve. Documentary role: List of the audio inputs that the MaxDevice offers. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#audio_inputs), `C74-LOM-MAXDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-064 — MaxDevice.audio_outputs

**D-current-public/target-U.** For MaxDevice.audio_outputs, the published declaration is list of DeviceIO with getobserve. Documentary role: List of the audio outputs that the MaxDevice offers. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#audio_outputs), `C74-LOM-MAXDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-065 — MaxDevice.midi_inputs

**D-current-public/target-U.** For MaxDevice.midi_inputs, the published declaration is list of DeviceIO with getobserve. Documentary role: List of the midi inputs that the MaxDevice offers. Available since Live 11.0. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#midi_inputs), `C74-LOM-MAXDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-066 — MaxDevice.midi_outputs

**D-current-public/target-U.** For MaxDevice.midi_outputs, the published declaration is list of DeviceIO with getobserve. Documentary role: List of the midi outputs that the MaxDevice offers. Available since Live 11.0. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#midi_outputs), `C74-LOM-MAXDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-067 — MaxDevice.get_bank_count

**D-current-public/target-U.** For MaxDevice.get_bank_count, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Returns: [int] the number of parameter banks. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#get_bank_count), `C74-LOM-MAXDEVICE` B0017, B0018.

### REQ-LAPI-SPECIALIZED-068 — MaxDevice.get_bank_name

**D-current-public/target-U.** For MaxDevice.get_bank_name, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameters: bank_index [int] Returns: [list of symbols] The name of the parameter bank specified by bank_index. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#get_bank_name), `C74-LOM-MAXDEVICE` B0019, B0020.

### REQ-LAPI-SPECIALIZED-069 — MaxDevice.get_bank_parameters

**D-current-public/target-U.** For MaxDevice.get_bank_parameters, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameters: bank_index [int] Returns: [list of ints] The indices of the parameters contained in the bank specified by bank_index. Empty slots are marked as -1. Bank index -1 refers to the "Best of" bank. Empty slots use -1; bank index -1 denotes Best of. These are parameter indices, not LOM IDs or native storage IDs; list ordering and unsupported bank policy remain ungraded. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/maxdevice/#get_bank_parameters), `C74-LOM-MAXDEVICE` B0021, B0022.

### REQ-LAPI-SPECIALIZED-070 — MeldDevice.selected_engine

**D-current-public/target-U.** For MeldDevice.selected_engine, the published declaration is int with getsetobserve. Documentary role: Meld's oscillator engine selector. The modes are encoded as follows: 0 = Engine A 1 = Engine B This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/melddevice/#selected_engine), `C74-LOM-MELDDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-071 — MeldDevice.unison_voices

**D-current-public/target-U.** For MeldDevice.unison_voices, the published declaration is int with getsetobserve. Documentary role: Selects the Unison voice count. The modes are encoded as follows: 0 = off 1 = two 2 = three 3 = four This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/melddevice/#unison_voices), `C74-LOM-MELDDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-072 — MeldDevice.mono_poly

**D-current-public/target-U.** For MeldDevice.mono_poly, the published declaration is int with getsetobserve. Documentary role: Selects the polyphony mode. The modes are encoded as follows: 0 = mono 1 = poly This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/melddevice/#mono_poly), `C74-LOM-MELDDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-073 — MeldDevice.poly_voices

**D-current-public/target-U.** For MeldDevice.poly_voices, the published declaration is int with getsetobserve. Documentary role: Selects the polyphony voice count. The modes are encoded as follows: 0 = two 1 = three 2 = four 3 = five 4 = six 5 = eight 6 = twelve This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/melddevice/#poly_voices), `C74-LOM-MELDDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-074 — PluginDevice.is_editor_open

**D-current-public/target-U.** For PluginDevice.is_editor_open, the published declaration is bool with getsetobserve. Documentary role: The opened state of the plug-in's editor window. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/plugindevice/#is_editor_open), `C74-LOM-PLUGINDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-075 — PluginDevice.presets

**D-current-public/target-U.** For PluginDevice.presets, the published declaration is StringVector with getobserve. Documentary role: Get the list of the plug-in's presets. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/plugindevice/#presets), `C74-LOM-PLUGINDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-076 — PluginDevice.selected_preset_index

**D-current-public/target-U.** For PluginDevice.selected_preset_index, the published declaration is int with getsetobserve. Documentary role: Get/set the index of the currently selected preset. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/plugindevice/#selected_preset_index), `C74-LOM-PLUGINDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-077 — RoarDevice.routing_mode_index

**D-current-public/target-U.** For RoarDevice.routing_mode_index, the published declaration is int with getsetobserve. Documentary role: The index of the routing mode utilized by Roar. The class introduction repeats Roar Device as its parent type; no recursive or repaired inheritance is flattened here. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/roardevice/#routing_mode_index), `C74-LOM-ROARDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-078 — RoarDevice.routing_mode_list

**D-current-public/target-U.** For RoarDevice.routing_mode_list, the published declaration is StringVector with get. Documentary role: The list of available routing modes. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/roardevice/#routing_mode_list), `C74-LOM-ROARDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-079 — RoarDevice.env_listen

**D-current-public/target-U.** For RoarDevice.env_listen, the published declaration is bool with getsetobserve. Documentary role: Get, set and observe the Envelope Input Listen toogle. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/roardevice/#env_listen), `C74-LOM-ROARDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-080 — ShifterDevice.pitch_bend_range

**D-current-public/target-U.** For ShifterDevice.pitch_bend_range, the published declaration is int with getsetobserve. Documentary role: The pitch bend range used in MIDI Pitch Mode. Unlike Drift, this member body does not explicitly supply semitone units; keep the MIDI Pitch Mode context without borrowing units. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/shifterdevice/#pitch_bend_range), `C74-LOM-SHIFTERDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-081 — ShifterDevice.pitch_mode_index

**D-current-public/target-U.** For ShifterDevice.pitch_mode_index, the published declaration is int with getsetobserve. Documentary role: The current pitch mode index: 0 = Internal, 1 = MIDI This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/shifterdevice/#pitch_mode_index), `C74-LOM-SHIFTERDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-082 — SpectralResonatorDevice.frequency_dial_mode

**D-current-public/target-U.** For SpectralResonatorDevice.frequency_dial_mode, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Freq control's mode. 0 = Hertz, 1 = MIDI note values. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#frequency_dial_mode), `C74-LOM-SPECTRALRESONATORDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-083 — SpectralResonatorDevice.midi_gate

**D-current-public/target-U.** For SpectralResonatorDevice.midi_gate, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the MIDI gate switch's state. 0 = Off, 1 = On. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#midi_gate), `C74-LOM-SPECTRALRESONATORDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-084 — SpectralResonatorDevice.mod_mode

**D-current-public/target-U.** For SpectralResonatorDevice.mod_mode, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Modulation Mode. 0 = None, 1 = Chorus, 2 = Wander, 3 = Granular. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#mod_mode), `C74-LOM-SPECTRALRESONATORDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-085 — SpectralResonatorDevice.mono_poly

**D-current-public/target-U.** For SpectralResonatorDevice.mono_poly, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Mono/Poly switch's state. 0 = Mono, 1 = Poly. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#mono_poly), `C74-LOM-SPECTRALRESONATORDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-086 — SpectralResonatorDevice.pitch_mode

**D-current-public/target-U.** For SpectralResonatorDevice.pitch_mode, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Pitch Mode. 0 = Internal, 1 = MIDI. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#pitch_mode), `C74-LOM-SPECTRALRESONATORDEVICE` B0016, B0017, B0018.

### REQ-LAPI-SPECIALIZED-087 — SpectralResonatorDevice.pitch_bend_range

**D-current-public/target-U.** For SpectralResonatorDevice.pitch_bend_range, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Pitch Bend Range.\ The printed body supplies no unit/range. Do not import Drift semitone units or a MIDI bend transform. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#pitch_bend_range), `C74-LOM-SPECTRALRESONATORDEVICE` B0019, B0020, B0021.

### REQ-LAPI-SPECIALIZED-088 — SpectralResonatorDevice.polyphony

**D-current-public/target-U.** For SpectralResonatorDevice.polyphony, the published declaration is int with getsetobserve. Documentary role: Get, set and observe the Polyphony. 0 = 2, 1 = 4, 2 = 8, 3 = 16 voices. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/spectralresonatordevice/#polyphony), `C74-LOM-SPECTRALRESONATORDEVICE` B0022, B0023, B0024.

### REQ-LAPI-SPECIALIZED-089 — WavetableDevice.filter_routing

**D-current-public/target-U.** For WavetableDevice.filter_routing, the published declaration is int with getsetobserve. Documentary role: Access to the current filter routing. 0 = Serial, 1 = Parallel, 2 = Split. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#filter_routing), `C74-LOM-WAVETABLEDEVICE` B0004, B0005, B0006.

### REQ-LAPI-SPECIALIZED-090 — WavetableDevice.mono_poly

**D-current-public/target-U.** For WavetableDevice.mono_poly, the published declaration is int with getsetobserve. Documentary role: Access to Wavetable's Poly/Mono switch. 0 = Mono, 1 = Poly. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#mono_poly), `C74-LOM-WAVETABLEDEVICE` B0007, B0008, B0009.

### REQ-LAPI-SPECIALIZED-091 — WavetableDevice.oscillator_1_effect_mode

**D-current-public/target-U.** For WavetableDevice.oscillator_1_effect_mode, the published declaration is int with getsetobserve. Documentary role: Access to oscillator 1's effect mode. 0 = None, 1 = Fm, 2 = Classic, 3 = Modern. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_1_effect_mode), `C74-LOM-WAVETABLEDEVICE` B0010, B0011, B0012.

### REQ-LAPI-SPECIALIZED-092 — WavetableDevice.oscillator_2_effect_mode

**D-current-public/target-U.** For WavetableDevice.oscillator_2_effect_mode, the published declaration is int with getsetobserve. Documentary role: Access to oscillator 2's effect mode. The oscillator2 body supplies no enum. Do not transfer oscillator1 Fm/Classic/Modern indexes by analogy. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_2_effect_mode), `C74-LOM-WAVETABLEDEVICE` B0013, B0014, B0015.

### REQ-LAPI-SPECIALIZED-093 — WavetableDevice.oscillator_1_wavetable_category

**D-current-public/target-U.** For WavetableDevice.oscillator_1_wavetable_category, the published declaration is member type not declared here with getsetobserve. Documentary role: Access to oscillator 1's wavetable category selector.  The published selector heading omits a type; do not fill int from similar selectors. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_1_wavetable_category), `C74-LOM-WAVETABLEDEVICE` B0016, B0017, B0018.

### REQ-LAPI-SPECIALIZED-094 — WavetableDevice.oscillator_2_wavetable_category

**D-current-public/target-U.** For WavetableDevice.oscillator_2_wavetable_category, the published declaration is member type not declared here with getsetobserve. Documentary role: Access to oscillator 2's wavetable category selector.  The published selector heading omits a type; do not fill int from similar selectors. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_2_wavetable_category), `C74-LOM-WAVETABLEDEVICE` B0019, B0020, B0021.

### REQ-LAPI-SPECIALIZED-095 — WavetableDevice.oscillator_1_wavetable_index

**D-current-public/target-U.** For WavetableDevice.oscillator_1_wavetable_index, the published declaration is member type not declared here with getsetobserve. Documentary role: Access to oscillator 1's wavetable index selector.  The published selector heading omits a type; do not fill int from similar selectors. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_1_wavetable_index), `C74-LOM-WAVETABLEDEVICE` B0022, B0023, B0024.

### REQ-LAPI-SPECIALIZED-096 — WavetableDevice.oscillator_2_wavetable_index

**D-current-public/target-U.** For WavetableDevice.oscillator_2_wavetable_index, the published declaration is member type not declared here with getsetobserve. Documentary role: Access to oscillator 2's wavetable index selector.  The published selector heading omits a type; do not fill int from similar selectors. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_2_wavetable_index), `C74-LOM-WAVETABLEDEVICE` B0025, B0026, B0027.

### REQ-LAPI-SPECIALIZED-097 — WavetableDevice.oscillator_1_wavetables

**D-current-public/target-U.** For WavetableDevice.oscillator_1_wavetables, the published declaration is StringVector with getobserve. Documentary role: List of names of the wavetables currently available for oscillator 1. Depends on the current wavetable category selection (see oscillator_1_wavetable_category). This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_1_wavetables), `C74-LOM-WAVETABLEDEVICE` B0028, B0029, B0030.

### REQ-LAPI-SPECIALIZED-098 — WavetableDevice.oscillator_2_wavetables

**D-current-public/target-U.** For WavetableDevice.oscillator_2_wavetables, the published declaration is StringVector with getobserve. Documentary role: List of names of the wavetables currently available for oscillator 2. Depends on the current wavetable category selection (see oscillator_2_wavetable_category). This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_2_wavetables), `C74-LOM-WAVETABLEDEVICE` B0031, B0032, B0033.

### REQ-LAPI-SPECIALIZED-099 — WavetableDevice.oscillator_wavetable_categories

**D-current-public/target-U.** For WavetableDevice.oscillator_wavetable_categories, the published declaration is StringVector with get. Documentary role: List of the names of the available wavetable categories. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#oscillator_wavetable_categories), `C74-LOM-WAVETABLEDEVICE` B0034, B0035, B0036.

### REQ-LAPI-SPECIALIZED-100 — WavetableDevice.poly_voices

**D-current-public/target-U.** For WavetableDevice.poly_voices, the published declaration is int with getsetobserve. Documentary role: The current number of polyphonic voices. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#poly_voices), `C74-LOM-WAVETABLEDEVICE` B0037, B0038, B0039.

### REQ-LAPI-SPECIALIZED-101 — WavetableDevice.unison_mode

**D-current-public/target-U.** For WavetableDevice.unison_mode, the published declaration is int with getsetobserve. Documentary role: Access to Wavetable's unison mode parameter. 0 = None 1 = Classic 2 = Shimmer 3 = Noise 4 = Phase Sync 5 = Position Spread 6 = Random Note This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#unison_mode), `C74-LOM-WAVETABLEDEVICE` B0040, B0041, B0042.

### REQ-LAPI-SPECIALIZED-102 — WavetableDevice.unison_voice_count

**D-current-public/target-U.** For WavetableDevice.unison_voice_count, the published declaration is int with getsetobserve. Documentary role: Access to the number of unison voices. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#unison_voice_count), `C74-LOM-WAVETABLEDEVICE` B0043, B0044, B0045.

### REQ-LAPI-SPECIALIZED-103 — WavetableDevice.visible_modulation_target_names

**D-current-public/target-U.** For WavetableDevice.visible_modulation_target_names, the published declaration is StringVector with getobserve. Documentary role: List of the names of modulation targets currently visible in the modulation matrix. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#visible_modulation_target_names), `C74-LOM-WAVETABLEDEVICE` B0046, B0047, B0048.

### REQ-LAPI-SPECIALIZED-104 — WavetableDevice.add_parameter_to_modulation_matrix

**D-current-public/target-U.** For WavetableDevice.add_parameter_to_modulation_matrix, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameter: parameter_to_add [DeviceParameter] Add an instrument parameter to the modulation matrix. Only works for parameters that can be modulated (see is_parameter_modulatable). This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#add_parameter_to_modulation_matrix), `C74-LOM-WAVETABLEDEVICE` B0050, B0051.

### REQ-LAPI-SPECIALIZED-105 — WavetableDevice.get_modulation_target_parameter_name

**D-current-public/target-U.** For WavetableDevice.get_modulation_target_parameter_name, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameter: index [int] Return the modulation target parameter name at index in the modulation matrix as a [symbol]. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#get_modulation_target_parameter_name), `C74-LOM-WAVETABLEDEVICE` B0052, B0053.

### REQ-LAPI-SPECIALIZED-106 — WavetableDevice.get_modulation_value

**D-current-public/target-U.** For WavetableDevice.get_modulation_value, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameters: modulation_target_index [int] modulation_source_index [int] Return the amount of the modulation of the parameter at modulation_target_index by the modulation source at modulation_source_index in Wavetable's modulation matrix. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#get_modulation_value), `C74-LOM-WAVETABLEDEVICE` B0054, B0055.

### REQ-LAPI-SPECIALIZED-107 — WavetableDevice.is_parameter_modulatable

**D-current-public/target-U.** For WavetableDevice.is_parameter_modulatable, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameter: parameter [DeviceParameter] 1 = parameter can be modulated. Call this before add_parameter_to_modulation_matrix. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#is_parameter_modulatable), `C74-LOM-WAVETABLEDEVICE` B0056, B0057.

### REQ-LAPI-SPECIALIZED-108 — WavetableDevice.set_modulation_value

**D-current-public/target-U.** For WavetableDevice.set_modulation_value, the published declaration is function role; formal argument/result declarations only where printed with function-call role; no property access line. Documentary role: Parameters: modulation_target_index [int] modulation_source_index [int] Set the amount of the modulation of the parameter at modulation_target_index by the modulation source at modulation_source_index in Wavetable's modulation matrix. The printed parameter list contains only target/source indices, although prose describes setting an amount. The missing amount argument/type is U; do not invent a third argument. This publication role supplies no complete signature/error/lifecycle or target numerical/signal/timing law.

Exact [publication member](https://docs.cycling74.com/apiref/lom/wavetabledevice/#set_modulation_value), `C74-LOM-WAVETABLEDEVICE` B0058, B0059.

### REQ-LAPI-SPECIALIZED-U-VERSION — Versions, class names and inherited surface

**U/target-U.** Exact12.4.3 applicability and inherited Device/View/root/alias closure remain unknown. DrumCellDevice maps by publisher description to Drum Sampler; Roar introduction repeats its own device name, not a reviewed parent hierarchy.

### REQ-LAPI-SPECIALIZED-U-TYPES — Types, ranges and omitted signatures

**U/target-U.** Wavetable selector types, oscillator2 enum, setter amount signature, Looper buffer units, bend units, dictionary serialization, index bounds and function returns remain unresolved where omitted. No type/default/void or analogue inference.

### REQ-LAPI-SPECIALIZED-U-CONTEXT — Routing, categories, banks and presets

**U/target-U.** Compressor setter track/device cross-reference, category/list dependency, plugin editor/preset capabilities, Max banks/IDs, source changes and invalid/stale/member capability interactions remain unknown.

### REQ-LAPI-SPECIALIZED-U-PROCESSING — Composed numeric, signal, timing and recording outcomes

**U/target-U.** Modulation routing, voice allocation, pitch/MPE/tuning, filtering, normalized gain, IR shaping, speed/length, buffer capture/overdub and export audio remain separate device/workflow owners; no algorithm or tolerance follows.

### REQ-LAPI-SPECIALIZED-U-LIFECYCLE — Undo, persistence, initialization and teardown

**U/target-U.** Malformed values, observer/event sequencing, ownership/source loss, cancellation, save/reopen, Undo except its scoped Looper content role, device reordering and teardown remain unknown.

## Acceptance proposals and source limits

[123 future proposals](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/cases.json)
cover108 source roles and15 U probes across113 requirements. Property actions use
capability-conditioned positive setups and member-specific source context; function
actions retain particular content/routing/modulation/bank/identity prerequisites.
They are partial discovery proposals, not all branches or executable fixture files.
Every actual documentary/target result/comparator is null/U/unexecuted. Published
role text stays in source_claim, not a fabricated API or numeric/signal oracle.

## Analysis-only evidence and denominator

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/sources.json)
retain unchanged original URL/UTC/size/hash and paths relative to max-api inventory.
[Blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/source-blocks.json)
and [direct-member ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/member-ledger.json)
retain exact locators/types/access/argument/result prose and omission flags. All108
map to a partial clause/action; none is semantically complete. Typed schema,
inherited/root/alias closure, numeric/audio/timing and exact-target obligations
remain open. [Research](../research/live-api-specialized-devices.md) owns the
source-context questions. The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/live-api-specialized-devices/manifest-author-r1.json)
freezes only this partial scope for independent review.
