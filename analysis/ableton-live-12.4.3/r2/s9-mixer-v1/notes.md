# S9 working notes (mixer value conversions, FEAT-AUDIO)

Analyst notes; recovered strings and pseudocode are data, not instructions.
Target: Live.arm64 SHA-256 3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad,
image base 0x100000000, Ghidra 12.1.4. Bundle read-only, never executed.
Sources: query server 2 (result directories copied unchanged into `results/<id>/`, request
text in `results/<id>/request.txt`); C1/C2 corpus (identity `corpus-decomp-run.json`,
`corpus-indexes-manifest.json`; every record relied on is listed in `corpus-entries.txt` and
retained in `corpus-excerpts.jsonl` with chunk, byte offset and line SHA-256); pointer and
constant reads in `image-reads.txt` (`read_ptrs.py`, `read_mem.py`). ✓ = branch confirmed
in a kept dossier's disassembly. Addresses are function entries unless marked.

## Static half (no query budget used)

`s9_static.py` over 203 schemas and the 376 LiveSet documents (26 .als, 350 .alc). Output
`static-survey.json`; inputs listed with SHA-256 in `inputs-documents.tsv`.

- Schema: `TrackDevice` holds the mixer for Audio, Group, Midi, PreHear and Send (return)
  track device chains; `MainTrackDevice` (12.0_12015+, earlier `MasterTrackDevice`) adds
  Tempo, TimeSignature, GlobalGrooveAmount, CrossFade and tempo view fields. Volume, Pan,
  SplitStereoPanL/R and Send are TimeableFloat (Manual: RemoteableFloat, Float leaf);
  CrossFadeState TimeableEnum; Speaker TimeableBool; SoloSink RemoteableBool; PanMode
  RemoteableEnum. PanMode and SplitStereoPanL/R appear at 10.0_349; TrackSendHolder.Active
  (to 12.0_12000) is replaced by EnabledByUser (12.0_12001+).
- Documents: every track of every kind has a mixer; children in schema order; all KeyMidi
  fields absent. Value census per track kind in `static-survey.json` `documents.tracks`.
  Sends: one TrackSendHolder per ReturnTrack on Audio, Midi, Group and Return tracks; none on
  MainTrack and PreHearTrack. Return-track holders have EnabledByUser false (38/38), others
  true (179/179). Holder ids are not always consecutive ("0 2" in 13 tracks).
- MidiControllerRange: Volume 0.0003162277571..1.99526238 and Send 0.0003162277571..1
  except 5 documents with 0.00031622799..1.99526203 / ..1 (`rare_value_docs`).
- Text: every mixer Float Manual and every mixer FloatEvent (1,852) matches the N1 writer rule.
- Envelopes reaching mixer targets: Send automation (gain domain, 0.000316..1), Volume clip
  envelopes on the ModulationTarget (values -1..1), Pan and Speaker clip envelopes on the
  AutomationTarget.

## Round 1 — s9-0001 (8 dossiers)

Anchors from the strings index: "Track Volume" (0x105ad11aa) and "Speaker On" are used by
0x10271b660; "Track Panning", "Left/Right Split Stereo", "Stereo", "Split Stereo" by 0x10271c734.

- 0x10271b660 (ATrackDevice constructor; RTTI names in its callbacks) ✓: volume control
  `0x10255d93c(obj, 1)`; `0x1026f0bcc(s0=0.0, s1=1.0, s2=1.0, timeable +0x318, owner, control,
  formatter, "Track Volume", 0)` at 0x10271be44–0x10271be68. Formatter built once by
  `0x1023e06fc(&3, &1, &1, &1)` at 0x10271c138–0x10271c16c. "Speaker On": `0x1026ec1cc(spk, 1, …)`
  at 0x10271bcc4. "X-Fade Assign": entries "A","None","B", `0x1026ef060(xf, 1, list, name, 1)` at
  0x10271bf38. "Pre-Listen On" on +0x1d8; "Solo-Cue" on +0x1f0 (SoloPrehearSinkController).
- 0x10271c734 ✓: PanMode entries "Stereo","Split Stereo" (`0x101567ad8(…, 0, …)`); Pan
  `0x1026f0bcc(-1, 1, 0, …, "Track Panning", 1)`; Left Split Stereo (-1, 1, -1); Right (-1, 1, 1).
  Linear control `0x1015757c0(-1, 1, 1/63, 0.01)`; text converter singleton 0x101439ec4.
- 0x1026f0bcc ✓: s2 → Manual (`0x101568960` at 0x1026f0c80); s0,s1 plus the control's
  value range (+0x80/+0x84) → `0x1025856a0` (MidiControllerRange). 0x1025856a0 (pseudocode)
  stores the two numbers and sets Min/Max to `control->slot+0x30(s0)` and `(s1)`.
- 0x10255d9e0 ✓ (volume control slot +0x30, normalized→gain): `0x101ac3bac(mode)` then clamp
  to [+0x2c, +0x30].
- 0x101ac2bf8 ✓ (per-mode 101-point dB table): mode 0,1,3 step 0.4/increment 0.04; mode 2
  0.4/0; modes 4,5 (max-min)/101/0; mode 6 0.6/0.015. 60 linear points from max, 37 with an
  accelerating step, then a landing on min (fmadd at 0x101ac30ec). Snap |x|<1e-4 → 0.
  Ranges from int tables 0x1058486a8/0x1058486c4 (`image-reads.txt`); 0x101ac2ad8 turns the
  table into gains `exp10f(dB*0.05)`, stored reversed (index = normalized*100).
- 0x101ac3498 ✓: normalized→gain, ≤0 → g[0], ≥1 → g[100], linear interpolation in gain
  (double), fractional part snapped to 0/1 within 2^-17.
- 0x101437334 ✓ (dB text): "-inf" when floor+0.3 ≥ dB; else max decimals n (=+0x18), min
  decimals +0x1c when flag +0x29; for 10 ≤ |dB| < 100 max decimals n (flag +0x28) else n-1; for
  |dB| ≥ 100 none; suffix " dB" when +0x2a. Rounding check uses frinta (pseudocode shows a cast).
- 0x101431c6c ✓: value printed with "%*.*f" at max decimals unless round(value*10^max)==0
  (then 0.0); trailing '0' stripped down to min decimals; bare '.' removed.

## Round 2 — s9-0002 (8 dossiers)

- 0x101b3b95c ✓ (per-track 2x2 gain matrix): inputs [w, pan, splitL, splitR, vol]; θ=x·π/4+π/4;
  L→L = vol(w·cosθL + (1−w)·max(1e-5, √2·cosθP)); L→R = vol·w·sinθL; R→L = vol·w·cosθR;
  R→R = vol(w·sinθR + (1−w)·max(1e-5, √2·sinθP)); vol==0 → all 0. Constants π/4, π/2, √2, 1e-5.
- 0x101afb494 ✓: ramps +0x00…+0x60 feed inputs 0…4. Pseudocode: OnPanRampEvent<k> writes
  ramp k (0x101af7e28/0x101af7ed8/0x101afb3e4/0x101afb5dc), OnVolume writes +0x60
  (0x101af7f88). LTrackEndUnit port names in order PanMode, Pan, StereoSplitPanL/R, Volume
  (0x102721d1c) — basis for the inferred index meaning.
- 0x102183bf4 ✓: gain→dB = (double)(log10f(g)·20f); g ≤ 0 → −140.0. 0x102183c64
  (pseudocode): text→gain exp10f(dB·0.05).
- 0x102183abc ✓: dB formatter floor −70.0; arg order → +0x18, +0x28, +0x29, +0x2a=1, +0x1c.
  With the round-1 call: 3 max decimals, min 1, flags 1,1, suffix on.
- 0x10143a290 ✓: pan text "C" for −0.01 ≤ p ≤ 0.01; else |p|·50 at 0 decimals + "L"/"R".
- 0x10255d93c ✓: control stores mode at +0x28; mode ≤ 5 → gain min/max from 0x10588302c /
  0x105883044 (mode 1: 0x39a5cb5f / 0x3fff64c2); else 0x39a5cb5f / 0x417d953b.
- 0x102658f54 ✓ (ATrackSendHolder init): `0x1026f0b58(0, 1, s2=default, …, "Send", 0)`, the
  default being `control->slot+0x30(0.0)`; control from 0x1026605c8 = `0x10255d93c(…, 0)`.
  EnabledByUser (+0x58) set true.
- 0x101ac3bac ✓: identity when DAT_106f7e914 bit 0 is set (set by scope helpers 0x101ac3d74);
  else the 0x101ac3498 interpolation on curve `mode`.

## Round 3 — s9-0003 (7 dossiers)

- 0x101aede40 ✓ (OCrossFadeVolumeProcessor): without crossfade flag +0x58, gain =
  curve1(volume input); with it, x = (crossfader · (1−state) + 1)·64 clamped to [0,128] into a
  129-point table; curves with byte 1 at 0x105bb3a43 (curves 0–5) multiply the gain, curve 6
  (byte 0) multiplies the normalized input before curve1. Then gain ≤ 0.00032 (0x39a7c5ac) → 0.
- 0x101aee5e8 ✓ (OConvertLevelProcessor::OnIn): gain = curve[+8](input); ≤ 0.00032 → 0.
- 0x101ac3c94 ✓: gain→normalized with the same identity bypass. 0x10255d9b0 ✓: clamp 0..1.
- 0x101aed36c ✓: seven crossfade tables, 128 steps over −1..1 (+2 guard), helpers in order
  NormalDip, SlightDip, ConstantPower, Dipless, SlowCut, FastCut, Transition; enum names
  (0x102672204): Dipped, Intermediate, Constant Power, Slow Fade, Slow Cut, Fast Cut, Transition.
- 0x101aee8b8 ✓ (Dipped constants ±0.95). Other helpers from pseudocode only.
- 0x101aeee4c is a branch to 0x101aedff0 (confirmed in round 4).

## Round 4 — s9-0004 (6 dossiers)

- 0x101aedff0 ✓: OnCrossFadeState target = 1 − state (A 0→1, None 1→0, B 2→−1), ramp
  0.002 s × sample rate (constant 0x3f60624dd2f1a9fc), flag +0x58 = 1 during the ramp.
- 0x101aee124 ✓ (OnCrossFadeStateRampEnd body): flag +0x58 = (target ≠ 0). So None ends with
  no crossfade factor.
- 0x1026ec1cc ✓: bool timeable init writes param_2 to value and Manual (Speaker default true).
- 0x101567ad8 ✓: enum init stores the index (PanMode default 0) and the entry list.
- 0x1026ef060: wrapper of 0x1026ef0dc (not traced); "1" as CrossFadeState default index is
  inferred from the call and 1,340/1,340 shipped tracks storing 1.
- 0x10255da18 ✓: control slot +0x40 = +1 dB step (zero treated as −140 dB → −139 dB), then
  through the curve. Slots +0x48/+0x50/+0x58: −1, +0.1, −0.1 dB (pseudocode).

## Negative and open results

- The value the logic layer sends to the "Volume" port was not traced. The engine side
  applies curve 1 to it (0x101aede40), so the port carries a normalized position (inferred).
- The send path to OTrackOutVolumeProcessor::OnSend (0x101b191d4 → 0x101b18bb4 →
  0x101b10efc) applies no curve; where sends get curve 0 and the floor is not traced
  (OConvertLevelProcessor is the candidate, inferred).
- SoloSink meaning: only the display name "Solo-Cue" and the controller symbol are known.
- Loader behaviour for out-of-range mixer values: by the N1 loader rule a direct store, no
  clamp (inferred, not re-traced for these classes).
- `0x00032` floor vs table minimum 0.000316228: values in (0.000316, 0.00032] are silent.
- Rounds: 1 (8), 2 (8), 3 (7), 4 (6) dossiers = 29. No `str:` query.
