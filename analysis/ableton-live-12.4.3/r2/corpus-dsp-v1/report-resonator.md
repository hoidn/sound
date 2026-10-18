# Corpus (Live 12.4.3) `ab_resonator`: DSP spec

Binary `Corpus.arm64` (sha256 29df4582…). `M+0xNNN` means a byte offset in the resonator object (FUN_0001e7cc mallocs 0x12728 bytes). Statements are read from code or data unless marked **Inf** (inference).

## 0. The graph around the resonator (FUN_00005ca8, FUN_000097e4)
- **Two instances.** `Resonator` is channel 0 and `Resonator_1` is channel 1. Each is built from the string `"<fs> 1024 <ch> Resonator"`, parsed with `sscanf("%f %d %d %63s")` at 0x1ec2c.
  - `%f` is stored at M+0x148 and is the sample rate.
  - The second `%d` is the channel index. `M+0x11d06 = (ch>0)` (set at 0x1f384) swaps the listening L/R parameters.
- **Linked pair.** `FUN_0001afa8` links the two instances. `FUN_00019370` delivers every parameter message to the module and then to its slaves (+0x118 list), calling module slot +0x18 = FUN_00020fc8 on each.
- **Ports and wiring** (0x5ca8 lines 815–819):

| Port | Role | Connected to |
|---|---|---|
| in1 | gate (≤0.1 means note-off) | Modulator (corpus_modulation_hub) out1 |
| in2 | audio excitation | Filters[ch] out1 (AudioIn → DryWet panpot out2 → Gain → Filters) |
| in3 | pitch, octaves relative to 261.62 Hz | Modulator out2 (ch0) / out3 (ch1) |
| in4 | exci_x mod | unconnected |
| in5 | exci_y / inharmonicity mod | unconnected |
| in6 | trigger | `constant1` (value 1) |
| out1 | output | StereoWidth (out2 unused) |

- **Values forced after graph build.** `FUN_000097e4` sends integer controllers to both instances:
  - frequency = 64 → 0
  - frequency_mod = 64 → 1.0
  - amp = 64 → 1.01098
  - decay_mod = 64 → 0
  - amp_mod = 64 → 0
  - mono_stero = 0 → **mono**, so each instance only uses its "L" pickup.

## 1. Parameters
**Controller curves** (c = 0..127; class constructors at 0xfc10, 0x10aac, 0x119ac, 0xf940; setters at 0xfcd8, 0x10b84, 0x11a88, 0xf354):

| Class | Curve |
|---|---|
| Linear | n = (c==64 ? 0.5 : c/127); v = min + n(max−min) |
| Exponential | v = min·(max/min)^(c/127) |
| Cubic | n = (c==64 ? 0.125 : (c/127)³) |
| Int | v = min + (int)(n·127 + 0.4); c=64 gives 63 |

**Quantisation matters for a faithful port.** The resonator's handler FUN_00020fc8 truncates every value with `fcvtzs` before calling the integer setters (0x21020–0x21420). All resonator params therefore land on integer controllers 0..127. Generic modules such as the Modulator keep float values (FUN_00018588 uses slot +0x40).

**Resonator parameters** (id: name / class / min..max / default / value offset / handler effect):

| id | Name | Class | Range | Default | Value at | Effect on set |
|---|---|---|---|---|---|---|
| 1 | frequency | lin | −2..2 | 0 | M+0x11d40 | — |
| 2 | inharmonicity | lin | −1..1 | 0 | M+0x11d90 | coef-dirty (0xdc6e) |
| 3 | frequency_mod | lin | 0..2 | 0 | M+0x11de8 | — |
| 10 | amp | exp | 0.25..4 | 1 | M+0x11e40 | coef-dirty + waveguide-dirty (0xdc72) |
| 11 | amp_freq | lin | ±1 | 0.6 | M+0x11e90 | coef-dirty |
| 12 | amp_mod | lin | ±1 | 0 | M+0x11ee0 | coef-dirty + waveguide-dirty |
| 15 | amp_hp | exp | 0.01..1 | 0.01 | M+0x11f38 | — |
| 20 | decay ("decay0") | exp | 0.05..35 | 1 | M+0x11f90 | coef-dirty + waveguide-dirty |
| 21 | decay_mod | lin | ±1 | 0 | M+0x12030 | coef-dirty + waveguide-dirty |
| 22 | tone ("gamma") | lin | ±1 | 0 | M+0x11fe0 | coef-dirty |
| 23 | decay_muted ("decay0_damped") | cubic | 0..1 | 0.2 (0x1ee40) | M+0x12080 | coef-dirty only if gate is low |
| 30 / 32 | list_l_x / list_r_x | lin | 0.01..0.99 | 0.5 | M+0x120d0 / M+0x12388 | starts a ramp; L and R swapped in Resonator_1 |
| 31 / 33 | list_l_y / list_r_y | lin | | 0.44375 | M+0x12138 / M+0x123f0 | **ignored by handler**, fixed |
| 34 | exci_x | lin | 0.05..0.95 | 0.5 | M+0x121a0 | exci-dirty (0xdc70) |
| 35 / 38 | exci_y / exci_y_mod | | | 0.44375 / 0 | | **ignored** |
| 36 | ratio | exp | 1..20 | 1.5 | M+0x12298 | table rebuild (0xdc6f), 2-D types only |
| 37 | exci_x_mod | | | | M+0x122e8 | — |
| 39 | exci_error | lin | 0..1 | 0 | M+0x12240 | — |
| 40 | mono_stero | int | | | M+0x12458 | — |
| 45 | quality | raw int | | 2 | M+0x160 | stored unclamped (0x212d0), rebuild |
| 60 | type | int | 0..8 | | M+0x124a8 | immediate `FUN_000243e8(M,1)` with state reset |
| 71 | tube_radius | exp | 0.005..0.4 | 0.02 | M+0x12508 | recompute reflection filter |
| 72 | tube_opening | lin | 0.005..1 | 1 | M+0x12558 | recompute reflection filter |
| 81–84 | manual_f1..f4 | | | | | type 8 only |
| 90 | inharm_opening_mod | lin | ±0.2 | | M+0x12708 | — |
| 0xffff | on/off | | | | | off → FUN_00024b14 (zeroes output) |

## 2. Live host index → resonator parameter
The wrapper table is at inst+0xe0078; conversions are in FUN_0000d75c and FUN_000050c0. The resonator then uses c = trunc(controller).

Conversion shorthands:
- `DEF(v)`: v' = min(v, 1); controller = 128v' if v' ≤ 0.5, else 126v' + 1.
- `BIP(v)`: v < 0 → 63.5 + 63.5v; otherwise 64 + 63v.
- `POS(v)`: 64 + 31.5v.

| Host | Param | Conversion | Live name (**Inf**) |
|---|---|---|---|
| 0 | 60 type | int table at 0x2a450 = [1,2,3,4,5,7,6]; out of range → 0 | ResonanceType |
| 33 | 45 quality | int min(v, 3) | ResonatorQuality |
| 1 | 20 decay | DEF → 0.05·700^(c/127) s | Decay |
| 2 | 22 tone | BIP | Material |
| 3 | 2 inharmonicity | BIP | Inharmonics |
| 4 | 36 ratio | DEF → 20^(c/127) | Ratio |
| 5 | 71 tube_radius | inverted: v ≥ 0.5 → 127(1−v); else 127−126v | Radius |
| 11 | 11 amp_freq | BIP | Brightness |
| 14 | 34 exci_x | POS | Hit |
| 15 | 30 list_l_x | POS | Listening L |
| 16 | 32 list_r_x | POS | Listening R |
| 34 | 23 decay_muted | DEF | Note-off decay |
| 35 | 72 tube_opening | DEF | Opening |
| 36 | 15 amp_hp | DEF → 0.01·100^(c/127) | Bleed |

Because of the swap flag, the left instance listens at host 15 and the right instance at host 16.

Pitch-related Modulator hosts (param setup FUN_00027278):
- 6 → fixed_pitch, linear −4..4 octaves, float, 1 ms ramp
- 7 → transpose, int −48..48 (controller = (int)v + 48)
- 8 → fine, ±0.5 semitone (controller = 63.5 + 1.27·cents)
- 9 → detune, ±1/12 octave (BIP)
- 10 → pitch-bend range 0..24 semitones
- 12 → tune_source (Param / MIDI)
- 13 → gate_source (Always On / MIDI Gate)

## 3. Types and quality (FUN_000243e8)
**Quality** sets the mode count only: N = [4, 16, 30, 70][quality] (table 0x2ab90; quality ≥ 4 gives 30). There is no oversampling. Quality and ratio changes rebuild at the next coefficient tick without resetting state (0x1f998).

| Internal | Live (via remap) | Ratios r_k | Mode shapes, grid size G |
|---|---|---|---|
| 0, 3 | String | k+1 | `T[k][j] = sin(π(k+1)j/(N+1))`, j = 0..N+1; G = N+2 |
| 1 | Beam | (β_k/β₀)², β = 4.730, 7.853, 10.996 (0x2aac4), then (k+1.5)π | same sine, G = N+2 |
| 2 | Marimba (0x24ee4) | (β_k/β₀)², β = 4.730, 9.413, 15.450, 20.710, 24.580 (0x2aab0), then (1.4142k + 2.1213)π | same sine, G = N+2 |
| 4 | Membrane (0x25210) | √(m² + (Rn)²) / √(1+R²) | `sin(πmi/(G−1))·sin(πnj/(G−1))`; G = ⌊√N⌋+3 |
| 5 | Plate (0x257b4) | (m² + (Rn)²) / (1+R²) | same 2-D shapes and G |
| 6 / 7 | Tube / Pipe | waveguide (§5) | — |
| 8 | manual (not reachable from Live) | — | — |

- **2-D grid construction:** R is the ratio param. Mx = ⌊√(RN)⌋ and My = ⌊√(N/R)⌋, each +1 if (x+1)² equals the argument. Enumerate m = 1..Mx+1 (outer) and n = 1..My+1 (inner), stable bubble sort ascending, keep the first N.
- **Grid sizes:** 1-D G = 6 / 18 / 32 / 72; 2-D G = 5 / 7 / 8 / 11 for quality 0..3.
- **Example ratios:**
  - Beam: 1, 2.756, 5.404, 8.933, 13.34, …
  - Marimba: 1, 3.96, 10.67, 19.17, 27.0, …
  - Membrane, R=1.5: 1(1,1), 1.387(2,1), 1.754(1,2), 1.861(3,1), 2(2,2), …
  - Plate, R=1.5: 1, 1.923, 3.077, 3.462, 4, …

## 4. Modal process (FUN_0001f3f8, types 0–5)
**Helpers:**
- `pow2(x)`: n = ⌊x⌋, t = (x−n)·ln2, result = ldexp(1 + t + t²(0.5 + 0.200064t), n). The constant 0.200064 is 0x3e4cdd94.
- Base angular frequency 1643.807 rad/s (0x44cd79d3) = 2π·261.62 Hz.

**Per-sample control:**
```
p = clamp(frequency + frequency_mod*in3, -5, 67/12)
gateLo = in1 <= 0.1;  trigLo = in6 <= 0.1;  rising = prevTrigLo && !trigLo
tick = cnt200 < 1 || rising
if (rebuildPending && tick)  { rebuild(no reset); exciDirty = coefDirty = true }
if (gateLo != prevGateLo || (tick && (|p - pPrev| > 0.00083 || coefDirty)))  recomputeCoefs()
if (rising || (cnt200 < 1 && exciDirty))  recomputeExcitation()
cnt200 = cnt200 > 0 ? cnt200 - 1 : 199            // initial 200
if (cnt20 < 1) { rampStep(); recomputePickups(); cnt20 = 20 }
cnt20--
```
Because in6 is a constant 1, `rising` happens only on the first sample after reset. Pitch and LFO changes therefore reach the filters at most every 200 samples.

**recomputeCoefs, per mode k:**
```
inh = clamp((inharmonicity + iom*in5)^3, -1, 1)    // recomputed only if dirty or rising, else cached at M+0x11da8
L = log2(r_k)
w = pow2(p) * 1643.807 * r_k * pow2(inh*L)
if (w >= fs*2.6179938) { activeN = k; bleedOn = false; stop }       // f >= 5/12 fs
if (k < oldActiveN) { s = Wold/w; y2 += y1*s - y1; y1 *= s } else { y1 = y2 = 0 }
e = tone >= 0 ? (5-L)*min(tone,1) - in3*decay_mod
              : -max(tone,-1)*L - in3*decay_mod
d = 8*pow2(e) / (gateLo ? 0.05 + (decay-0.05)*decay_muted : decay)
th = w/fs
alpha = (π/(π-th)) * sin(th) * d / w
tilt = pow2((L-2)*amp_freq + amp_mod*in3)
g  = alpha*amp*tilt / (2d(1+alpha))
a1 = -2cos(th)/(1+alpha)
a2 = (1-alpha)/(1+alpha)
```

**Bleed high-pass.** If all N modes pass the frequency check, a high-pass is designed from the last mode's W and r. It uses the same e, d, th and tilt, with:
- alphaH = 32·(π/(π−th))·sin(th)·d/w
- b0H = ((1+cos th)/2)·amp·tilt / ((1+alphaH)·w)
- a1H and a2H use the standard formulas above with alphaH
- its state is rescaled like the modes if it was active, otherwise zeroed

**Excitation and pickups:**
```
x = clamp(exci_x + exci_x_mod*in4, 0, 1)
// Gaussian jitter: sigma = 0.2*exci_error^2, Box-Muller from rand(), reflect at 0/1
x = clamp(x, 0.02, 0.98)
// 2-D only: y = clamp(exci_y + mod*in5, 0.05, 0.95)
shape1D(x): q = x*(G-1); i = floor(q); f = q - i
            value = 0.5*(T[i] + f*(T[i+1] - T[i]))
shape2D(x, y): bilinear on the same grid, also times 0.5
exc_k   = shape(k, x[, y])
pickL_k = shape(k, smoothed list_l_x[, list_l_y])
```
- In Live, exci_error and all y coordinates are unreachable, so there is no jitter and y = 0.44375.
- The shapes come from the coarse table plus linear interpolation, not analytic sines; a faithful port must replicate this.
- A new listening position ramps linearly over 200 steps of 20 samples each (4000 samples; constant 0x2a950). Table rebuilds snap the ramp (FUN_00025e6c).

**Filter bank, per sample:**
```
for k < activeN:
  y = exc_k*x + 1e-22 - (y1*a1 + y2*a2)
  v = (y - y2)*g
  sL += pickL_k*v
  y2 = y1; y1 = y
if bleedOn:
  w = x - (a1H*h1 + a2H*h2)
  sL += b0H*amp_hp*(w - 2*h1 + h2)
  h2 = h1; h1 = w
out = 3000*sL
```
**Inf:** the envelope is roughly exp(−d·t), so with e = 0 the level is about −69 dB after `decay` seconds.

## 5. Waveguide process (FUN_00023670; type 6 Tube, type 7 Pipe)
Two 2048-float delay lines: DL1 at M+0xdc78 and DL2 at M+0xfc78. `pipe` = M+0xdc73, latched into M+0xdc76.

**Recompute** happens when (|Δp| > 0.00083 or dirty) and (cnt10 == 0 or rising); cnt10 cycles every 10 samples. If only the gate changes, only `loss` is recomputed, using the previous pitch.
```
Td   = gateLo ? 0.05 + decay_muted*(decay - 0.05) : decay
loss = exp(-4 / (Td * 261.62 * pow2(decay_mod*in3) * pow2(p)))
gain = amp * pow2((amp_mod - 1)*in3)
Lf   = fs/(pow2(p) * (pipe ? 523.24 : 1046.48)) - 0.75
D = clamp((int)Lf, 2, 2046);  d = frac(Lf), set to 0 if D was clamped
// 5-tap Lagrange interpolation, taps at delays D..D+4
c0 =  (d-.5)(d-2.5)(d-1.5)(d+.5)/24
c1 = -(d-.5)(d-2.5)(d-1.5)(d+1.5)/6
c2 =  (d-2.5)(d-1.5)(d+1.5)(d+.5)/4
c3 = -(d-.5)(d-2.5)(d+1.5)(d+.5)/6
c4 =  (d-1.5)(d-.5)(d+1.5)(d+.5)/24
// then reload 4 taps from each line at write - D
```
**Per sample:**
```
read DL2 taps;  w = x - hpA*w1
DL1[++W1] = -0.999*Σ c·DL2taps + hpG*(w - w1);  w1 = w
read DL1 taps;  s = Σ c·DL1taps
yR = b0*s + b1*s_prev - a1*yR_prev               // reflection filter
v  = pipe ? yR : -yR
DL2[++W2] = v*loss
out = v*gain
```
- **Input DC blocker:** t = tan(94.24799/fs), i.e. 30 Hz; hpG = 1/(1+t), hpA = (t−1)/(t+1).
- **Reflection filter:** k = min(344/(fs·radius), 2.8274333) and o = (latched pipe ? opening : 1). With A = (k+o)o and B = (k−o)o:
  - a1 = (B−1)/(A+1)
  - b0 = (1−A)/(1+A)
  - b1 = −(B+1)/(A+1)
  - DC gain is −1; Nyquist gain is (1−o²)/(1+o²).
- **Inf from loop sign and length:**
  - Pipe, open: all harmonics of f0.
  - Pipe, closing the opening: the loop inverts and gives odd harmonics of f0/2.
  - Tube: odd harmonics of f0 (a quarter-wave tube).
- **Unused here:** tone, inharmonicity, amp_freq, hit/listening, bleed, quality. Output is the same on both channels.

## 6. Pitch and modulation inputs
- **Modulator** (FUN_0002764c): out2 = LFO_L + detune + P and out3 = LFO_R − detune + P.
  - P = fixed_pitch when tune_source is Param.
  - With MIDI, P = (note − 60)/12 + bend + (fine + transpose)/12, using highest-note priority (FUN_000279f4).
  - out1 (the gate) is 1 unless gate_source is MIDI Gate and no note is held.
- **Resonator:** f_k = 261.62·2^clamp(in3)·r_k^(1+inh).
  - in3 also drives decay_mod and amp_mod, but both are 0 in Corpus.
  - Modulation is held between ticks (every 200 samples modal, 10 samples waveguide).
  - On a pitch change, modal states are rescaled by W_old/W_new to avoid jumps.

## 7. Quirks (reproduce or skip deliberately)
1. All resonator params are truncated to integers 0..127.
2. Controller 64 has special cases: linear 0.5, cubic 0.125.
3. The int class maps controller 64 to 63; this hits Modulator transpose at +16 semitones.
4. Reset `FUN_00023464` (reached from `_ResetA` via engine slot +0x78 → FUN_0001bb44) writes 0x0101 at M+0xdc72 (0x235ac). This sets pipe = 1, so a Tube behaves like a Pipe until the type is sent again.
5. The reflection filter uses the latched pipe flag, so its coefficients stay stale after a type switch until Radius or Opening moves.
6. Bleed's minimum is 0.01, not 0. Bleed turns off whenever any mode exceeds 5/12·fs.

## 8. Uncertainties
- The host-index → Live-name mapping is inferred from what each parameter does; the binary contains no host names.
- Live's value ranges for hosts 14–16 are unknown. If v ∈ [−1, 1], positions span 0.277–0.723; if v ∈ [0, 1], they span 0.5–0.723.
- The ResonanceType order (Beam, Marimba, String, Membrane, Plate, Pipe, Tube) is assumed. The physics in each builder supports it, and Opening is used only by internal type 7.
- in4 and in5 are assumed to read zeros (port-buffer binding not traced).
- Input-path scaling was not traced. The output path is ×0.25 (FUN_00009300) then ×4 (FUN_000059d0), so unity.
- The Gain, Filters, DryWet and StereoWidth modules were not analysed.