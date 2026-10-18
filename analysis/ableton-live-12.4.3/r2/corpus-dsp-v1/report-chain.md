# Corpus (Live 12.4.3, `Corpus.arm64`): the signal chain except the resonator core

This is static reading of the Ghidra pseudocode, with rizin disassembly for the constants that matter. Nothing was run. Addresses are vmaddr, which equals the file offset. **[obs]** = the code shows it directly; **[inf]** = an inference.

Terms:
- `ctl` is the engine's controller-scale value, 0..127, held as a float.
- `n` is a normalized position.
- "oct" means octaves relative to C4 = 261.62 Hz. The resonator multiplies by 1643.807 rad/s = 2π·261.62 inside FUN_0001f3f8.

## 0. The host wrapper and how it calls the engine

- **SetParameterA path.** `_SetParameterA` goes to CorpusWrapper vtable slot 0 at 0x2cb88, which is **FUN_0000d75c(float v, inst, idx)**.
  - The raw value is stored at `inst+0xe0090+idx*0x1c` and replayed when the sample rate changes.
  - Vtable slot 2 (FUN_0000d98c) returns −1, which disables the program-change special case in FUN_000050c0.
- **Host table.** It is at `inst+0xe0078`, 37 entries, stride 0x1c, built in FUN_0000c40c. Layout:
  - +0: module handle
  - +4: param id
  - +8: enabled flag
  - +0xc: kind (3 = int)
  - +0x14: max (float)
  - +0x18: last value
- **Engine API.** This is the synth vtable at 0x2c358. [obs]
  - +200 (FUN_0001ca00) posts a type-2 (float ctl) message; +0xd0 (FUN_0001caa8) posts a type-1 (int ctl) message.
  - Messages travel FUN_00015f08 → FUN_00019370 and are applied to the module **and to every linked module in its +0x118 list**.
  - In the default handler FUN_00018588: type 1 calls param vtable +0x20 (int-ctl setter), type 2 calls +0x40 (float-ctl setter), type 7 calls +0x30 (sets the physical value).
  - When a value changes, the handler calls module+0x90, which becomes processor vtable +0x20 `(paramId, mode 2 = smooth)`.
- **Timing.** Messages are drained **once per host block** at the top of FUN_00009300. [obs]

### 0.1 Parameter "drivers": converting ctl to a physical value [obs]

| Driver (vtable) | Mapping. `c` = ctl. |
|---|---|
| Linear float (0x2c898; setters 0xfcd8 int, 0xfd8c float) | `n = (63.9999<c<64.0001) ? 0.5 : c/127`; `v = min + n·(max−min)` |
| Exponential (0x2c5f8; 0x10b84, 0x10c78) | The code computes `min + (max−min)(r^(c/127)−1)/(r−1)` with r = max/min, which is exactly **`v = min·r^(c/127)`**. No special case at 64. |
| Int/Enum (0x2c518 and 0x2ce88; 0xf354 int, 0xf3e0 float) | `c' = min(c, max−min)` (a float ctl is first rounded via `(int)(c+0.499)`); then `v = min + (int)((c'==64 ? 0.5 : c'/127)·127 + 0.4)` = `min + c'`, **except c'=64 gives min+63** (verified at 0xf398–0xf3cc) |
| Cube (0x2cf68; 0x11ba4, 0x11c10) | `n = ((int)c==64) ? 0.125 : (c/127)³` |
| SmoothParameter Lin/Exp (0x2c6d8 / 0x2c9c8) | Target computed as above, then a linear ramp over N samples |

The resonator's own message handler (FUN_00020fc8) truncates a float ctl to int with `fcvtzs`, for example at 0x210c4 and 0x21128. Resonator parameters are therefore quantized to 128 steps. [obs]

### 0.2 Conversion functions from the host value to ctl, in FUN_0000d75c and FUN_000050c0 [obs]

- **`D(v)`**, the default path in FUN_000050c0:
  - `v = min(v,1)`.
  - `ctl = v≤0.5 ? 128v : 126v+1`. The constants (0x43000000 and 0x42fc0000) are at 0x51c4–0x51d8. The value is sent as a float.
  - When the entry's kind is 3, the path is instead `(int)min(v,max)`, sent as an int.
- **`B(v)`**, bipolar, for idx 2, 3, 9, 11: `v<0 ? 63.5v+63.5 : 63v+64`.
- **`Rinv(v)`**, for idx 5: `u=1−v; u≤0.5 ? 127u : 126u+1`.
- **`Deg(v)`**, for idx 24 and 25: `v<180 ? v·127/360 : 0.35v+1`.

### 0.3 The 37 host indices

The (module, id) pairs come from FUN_0000c40c. The Live names are assigned by elimination and name or semantic match. [inf] Indices 17–26 (LFO) and 27–29 (filter) follow the Live schema order exactly. For resonator rows, the curve is applied inside the resonator, after the ctl is truncated to int.

| idx | Live | Target (module:id name, driver, range) | host → ctl | ctl → physical |
|---|---|---|---|---|
| 0 | ResonanceType | Res:60 type (int 0..8) | int `T[(int)v]`, T = {1,2,3,4,5,7,6} @0x2a450 (v≥7 → 0) | type id |
| 1 | Decay | Res:20 decay (Exp 0.05..35) | D | 0.05·700^(c/127) |
| 2 | FreqDamping | Res:22 tone (Lin −1..1) | B | |
| 3 | Inharmonics | Res:2 inharmonicity (Lin −1..1) | B | |
| 4 | Ratio | Res:36 ratio (Exp 1..20) | D | |
| 5 | Radius | Res:71 tube_radius (Exp 0.005..0.4) | Rinv (inverted) | |
| 6 | Frequency | Mod:4 fixed_pitch (SmoothLin −4..4 oct, N=sr/1000) | D | −4+8n oct |
| 7 | Transpose | Mod:5 transpose (int −48..48) | int `(int)v+48` | −48+c (**c=64 → +15**) |
| 8 | FineTranspose | Mod:6 fine_transpose (SmoothLin ±0.5 st) | 1.27v+63.5 | |
| 9 | Detune | Mod:7 detune (SmoothLin ±1/12 oct) | B | |
| 10 | PitchBendRange | Mod:3 pitch_bend_range (enum 0..23 st, "2 octaves") | int min(v,24) | semitones |
| 11 | AmpFreq | Res:11 amp_freq (Lin −1..1, default 0.6) | B | |
| 12 | MidiPitch | Mod:2 tune_source (enum Param / MIDI) | D | |
| 13 | MidiGate | Mod:1 gate_source (enum Always On / MIDI Gate) | D | |
| 14/15/16 | ExcitationX / ListeningXL / ListeningXR | Res:34 exci_x (0.05..0.95), Res:30 list_l_x, Res:32 list_r_x (0.01..0.99) | 31.5v+64 | |
| 17 | LfoOnOff | Lfo:0xffff on_off | int | |
| 18 | LfoType | Lfo:1 waveform | int min(v,6) | |
| 19 | LfoSync | Lfo:3 sync | D | |
| 20 | LfoRate | Lfo:2 rate (Exp 0.01..10 Hz) | D | 0.01·1000^(c/127) |
| 21 | LfoSyncRate | Lfo:4 sync_rate (enum of 22) | int min(v,21) | |
| 22 | LfoStereoMode | Lfo:6 stereo_mode (enum 0 = Spin, 1 = Phase) | int `v≠0 ? 0 : 1` (Live 0 = Phase) | |
| 23 | LfoSpin | Lfo:7 relative_spin (Lin 0..1) | v≤0.5 ? 127v : 126v+1 | |
| 24 | LfoPhase | Lfo:8 relative_phase (Lin 0..1) | Deg | cycles |
| 25 | LfoOffset | Lfo:9 phase (Lin 0..1) | Deg | cycles |
| 26 | LfoAmount | Lfo:5 amount (SmoothLin 0..1, N=sr/1000) | D | |
| 27 | FilterOn | Filters:0xffff on_off | int | |
| 28 | FilterMidFreq | Filters:1 mid_freq (Exp 50..18000) | D (Live must send a normalized value) | 50·360^(c/127) |
| 29 | FilterBandWidth | Filters:2 bandwidth (Lin 0.5..9 oct) | 14.941176v−7.470588 | 0.5+8.5n |
| 30 | Drive | Gain:1 gain (SmoothExp 0.17783..5.6234, N=sr/100) | D | dB = −15+30c/127 |
| 31 | StereoWidth | StereoWidth:1 crossfade (SmoothLin 0..1, N=sr/100) | D | |
| 32 | DryWet | DryWet panpot:1 angle | D | a = c/127 (its own handler FUN_0001e244, no special case at 64) |
| 33 | ResonatorQuality | Res:45 quality | int min(v,3) | |
| 34 | DecayOnNoteOff | Res:23 decay_muted (Cube 0..1) | D | n³ |
| 35 | TubeOpening | Res:72 tube_opening (Lin 0.005..1) | D | |
| 36 | Bleed | Res:15 amp_hp (Exp 0.01..1) | D | 0.01·100^(c/127) |

- **Not sent through SetParameterA:** only MidiMode. Live has 38 parameters; the host table has 37.
- **Defaults applied at state load.** FUN_000097e4 sends int-ctl messages to the Resonator, which the link copies to Resonator_1:
  - frequency = 0 (ctl 64)
  - frequency_mod = 1.0 (ctl 64)
  - amp = 1.011 (ctl 64)
  - decay_mod = 0
  - amp_mod = 0
  - mono_stero = 0

## 1. The module graph

The graph is built in FUN_00005ca8 (CorpusSynth vtable +0xf0) using FUN_000182f8 calls. The data at 0x2a278/0x2a2f4 is an identity table, not a netlist. Per-channel modules come in pairs named "X" and "X_1".

| Module | Type | Ports (in/out) |
|---|---|---|
| constant1 | constant, value 1.0 | |
| StereoAudioIn | stereo_audio_in | |
| StereoLfo | ab_stereo_lfo | 0/2 |
| Modulator | corpus_modulation_hub (derived from MidiInModule) | 2/3 |
| DryWet, DryWet_1 | **panpot** (FUN_0001dcf0) | 2/2 |
| Gain, Gain_1 | corpus_gain | 1/1 |
| Filters, Filters_1 | corpus_filter | 1/1 |
| Resonator, Resonator_1 | ab_resonator (channel index passed as an argument) | 6/2 |
| StereoWidth | **corpus_stereo_crossfade** | 2/2 |
| left_mix, right_mix | plus | 2 inputs |
| StereoAudioOut | stereo_audio_out | |

```
In.out1→DryWet.in1, In.out2→DryWet_1.in1
DryWet_c.out2 (WET) → Gain_c → Filters_c → Resonator_c.in2
Mod.out1 (gate) → Res_c.in1;  Mod.out2 → Res.in3;  Mod.out3 → Res_1.in3 (pitch, oct);  constant1(1.0) → Res_c.in6
LFO.out1/out2 → Mod.in1/in2
Res.out1 → Width.in1;  Res_1.out1 → Width.in2
Width.out1 + DryWet.out1 (DRY) → left_mix;  Width.out2 + DryWet_1.out1 → right_mix → Out
```

Resonator in4, in5 and out2 are unconnected; unconnected inputs read as zero [inf]. The links set up by FUN_0001afa8 (DryWet, Gain, Filters, Resonator, left → right) copy every message from the left instance to the right one.

**Processing order per sub-block.** A sub-block is at most 512 samples (FUN_00009300):

In, LFO, Mod, DryWet, Gain, Filters, Res, DryWet_1, Gain_1, Filters_1, Res_1, Width, left_mix, right_mix.

**Output and gain.** The output is ×0.25, copied in place to the host buffers, then ×4 in FUN_000059d0, so the net gain is unity. A clip flag is set if any |x| > 0.7 before the ×4. `plus` computes `in1 + 1e-22 + in2`.

**Bleed** is the resonator's `amp_hp`.
- In FUN_0001f3f8 (decompile lines ~764–771), when flag 0x11cec is set, a two-pole high-pass of in2 (numerator x−2x₁+x₂) is computed.
- It is scaled by gain·amp_hp and added to out1 before the resonator's ×3000 output scaling.
- The filter's coefficients belong in the resonator report.

**Resonator pitch** is `clamp(frequency + frequency_mod·in3, −5, 5.5833)` oct. With the load-time defaults this is just in3.

## 2. Engine framework details the port needs [obs]

- **Smoother struct** `{cur, tgt, step, count, N}`.
  - Retargeting sets `step = (tgt−cur)/N` and `count = N`.
  - Each sample: `count--`, then `cur = count ? cur+step : tgt`.
- **Reset** (synth vtable +0x78, FUN_0001bb44) only snaps parameter smoothers. It does not clear biquad states.
- **Sample-rate change** (FUN_00004878): rebuild the synth, reload state, then replay all 37 stored host values.
- **Dead state:** the `{2·sr, 1e-5}` structures at inst+0xe04a8 and +0xe04d0 are never read.

## 3. DSP of each module [obs]

### DryWet (panpot; process FUN_0001dfec)

The targets are recomputed every 100 samples, and each gain ramps over 100 samples. Both gains start at 0.

```
P(t) = t·(10.392633 − 31.177902t + 20.785267t²)    // = 6√3·t(1−t)(1−2t)
x = a/4    // modulation term m·in2·min(a, 1−a) is zero here
wet = P(x);  dry = P(0.25 − x)
out1 (dry) = gDry·in;   out2 (wet) = gWet·in
```

| a | 0 | 0.25 | 0.5 | 0.75 | 1 |
|---|---|---|---|---|---|
| wet | 0 | 0.533 | 0.853 | 0.990 | 0.974 |
| dry | 0.974 | 0.990 | 0.853 | 0.533 | 0 |

### Gain (FUN_000271cc)

`out = g·in`, with g in −15..+15 dB, linear in dB, and a 10 ms ramp. There is **no saturation**.

### Filter (FUN_00026a5c, FUN_00026d70)

An RBJ low-pass (FUN_00027e3c) feeds an RBJ high-pass (FUN_00028260). Both have Q = 0.707 (0x3f34fdf4).

```
k  = P2(bw/2)    // P2(x) = ldexp(1 + y + (0.200064y + 0.5)·y², ⌊x⌋), y = frac(x)·ln2
fH = clamp(f0·k, 50, 18000);   fL = clamp(f0/k, 50, 18000)
w  = clamp(2πf/sr, 0.0006π, 0.9π)
α  = sin(w)/1.414
LPF: b0 = b2 = (1−cos)/2,  b1 = 1−cos
HPF: b0 = b2 = (1+cos)/2,  b1 = −(1+cos)
a0 = 1+α,  a1 = −2cos,  a2 = 1−α
y = (b0·(x+1e-22) + b1·x1 + b2·x2 − a1·y1 − a2·y2) / a0
```

- **Coefficient smoothing:** each coefficient ramps linearly over 30 samples after a frequency or bandwidth change.
- **On/off:** a mix ramp over ⌊sr/100⌋ samples, `out = x + g·(y−x)`. Once fully off, the output is a straight copy and the biquad states are frozen, not cleared.

### StereoWidth (FUN_00027040)

```
A = 0.5 + 0.5w;   B = 0.5 − 0.5w
L' = A·L + B·R;   R' = A·R + B·L
```

There is a 10 ms ramp. This applies to the wet (resonated) signal only.

### LFO (FUN_0001d1b4, FUN_0001d550, FUN_0001d74c)

Waveform mapping (Live LfoType → shape):

| LfoType | Name | Output |
|---|---|---|
| 0 | Sine | `6.094263p + 6.094263p² − 85.31969p³ + 121.88526p⁴ − 48.754105p⁵` (approximates sin 2πp) |
| 1 | Square | `p<0.5 ? −1 : 1` |
| 2 | Triangle | `p<0.5 ? 4p−1 : 3−4p` |
| 3 | Ramp Up | `2p−1` |
| 4 | Ramp Down | `1−2p` |
| 5 | S&H | current random, with the phase running at **×2 rate** |
| 6 | Random Ramp | `prev + p·(cur−prev)` |

Random values are uniform on [−1,1] and are redrawn when the phase wraps.

- **Outputs:** `out = amount·wave`.
- **Free-running rate:** `inc = rate/sr`.
  - **Spin mode:** `incR = incL·(1+spin)`.
  - **Phase mode:** `phR = frac(phL + relPhase)` and `incR = incL`; in this mode the right channel's random value copies the left's.
- **Sync:** `inc = BPM/(240·bars·sr)`.
  - The phases reset only on the transport-start edge: `phL = offset`, `phR = offset + relPhase`.
  - Spin is disabled while synced.
- **Offset change:** `phL += new − old`.
- **Rate change while synced:** ignored.
- **LfoOnOff off:** outputs zero and the phases freeze.
- **What it modulates:** pitch in octaves, through the Modulator, so LfoAmount 1 means ±1 octave.

### Modulator (FUN_0002764c, FUN_000279f4)

```
pL = lfoL + detune;   pR = lfoR − detune
Param mode:  p += fixedPitch
MIDI mode:   p += (note−60)/12 + bend + (fine + transpose)/12
gate = (AlwaysOn || heldCount ≥ 1) ? 1 : 0
```

- **Note priority:** highest note (`cmp; b.ge` at 0x27b04). When the current note is released, the code searches downward for the next held note.
- **Sustain (CC64)** is supported. CC123 is all notes off; CC120 also releases sustain.
- **Pitch bend** maps to b·PBR/12 oct, with b = 14-bit value ÷8192 (negative) or ÷8191 (positive), ramped over 1 ms.
- **Initial MIDI pitch** is −5 oct.
- There is no glide.

### CalcA (_CalcA 0x4cb8, FUN_000059d0, FUN_0000dff8)

1. MIDI events are queued with `frame − 1`.
2. The sync port is updated from CalcA's argument 7.
3. If no input is flagged, the engine reads zeros.
4. The engine renders the block, then applies ×4 and the clip check.
5. **End-of-block fade:** if CC120 (All Sound Off) arrived in this block (flag at offset 0x4010, set by FUN_0000e7c4):
   - the synth is reset after rendering,
   - and the block is multiplied by `1 − k/N`.
6. **Activity flag:** set to 0 after sr/10 consecutive samples with |out| ≤ 1e-5 on both channels.

## 4. Tables

- **Sync rates** (bars, at 0x2a8c4), index 0..21:
  - 8, 6, 4, 3, 2, 1.5, 1, 3/4, 1/2, 3/8, 1/3, 5/16, 1/4, 3/16, 1/6, 1/8, 1/12, 1/16, 1/24, 1/32, 1/48, 1/64.
  - Rate in Hz = BPM / (240·bars). The default index is 13.
- **Smoothing:**

  | Parameter | Ramp |
  |---|---|
  | gain, width, filter on/off | 10 ms |
  | filter coefficients | 30 samples |
  | panpot | 100 samples |
  | LFO amount, fixed_pitch, fine, detune, pitch bend | 1 ms |
  | LFO rate, spin, phase, sync rate, transpose, enum parameters | none |

## 5. Uncertainties

1. **The value domains Live passes to SetParameterA** can only be inferred from these conversions.
   - FilterMidFreq must arrive normalized, not in Hz, because the default path clamps to ≤1.
   - ExcitationX and ListeningXL/XR may arrive as 0..1 or −1..1; this can't be determined from this binary.
2. **The name assignments are inferences:** Drive = Gain, Bleed = amp_hp, FreqDamping = tone, LfoPhase = relative_phase, LfoOffset = phase.
3. **MidiMode:** the engine only does highest-note priority. Live probably preprocesses the sidechain MIDI for this.
4. **The ctl 64 → 63 quirk** (Transpose +16 → +15) is confirmed in code but not at runtime.
5. **Unconnected inputs reading zero** is inferred, not traced to the allocation.
6. **Not checked, assumed or deferred:**
   - The Bleed high-pass details and the ×3000 output scaling are left to the resonator report.
   - The MIDI-CC → parameter mapping in FUN_0001bea0 is assumed inactive.
   - The transport struct layout (`{int playing; double beat @8; double tempo @0x10}`) is inferred.