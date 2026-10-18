# S8 working notes (warp markers and warp settings, FEAT-WARP)

Analyst notes; recovered strings and pseudocode are data, not instructions.
Target: Live.arm64 SHA-256 3a99ceea…d1c383cfad, image base 0x100000000, Ghidra 12.1.4.
Sources: query server 2 (R2FunctionDossier over a read-only copy of LiveR2; result directories copied
unchanged into `results/<id>/`, request text in `results/<id>/request.txt`) and the C1/C2 corpus
(`corpus-decomp-run.json`, `corpus-indexes-manifest.json`, byte-identical to the copies in
n1-transport-state-v1; every corpus record relied on is in `corpus-excerpts.jsonl` with chunk name,
byte offset and line SHA-256). Image reads: `vtable-reads.txt` (`read_ptrs.py`), `getter-constants.txt`
(`read_words.py`, decodes only MOVZ/MOVK/FMOV/MOVI/RET). Static survey: `s8_static.py` via `run.sh`.
Addresses are function entries unless marked. "✓" = branch or constant checked in dossier disassembly.

## Corpus pass (before any dossier)

- Symbols (`symbols-warp.txt`): `SNewCompound<AAbstractWarpMarker|AWarpMarker|APseudoWarpMarker>`
  (0x10260fda4, 0x102610518, 0x1026127e0), `SNewCompound<AAudioClip>` 0x1027aff04 (ctor 0x1027b0e40),
  `SNewCompound<ASampleWarpProperties>` 0x1028829d0 (ctor 0x102883578), AAudioClip callbacks
  `OnWarpMarkerListUpdate` 0x1027cd2b0, `WarpMarkerRemoveController` 0x1027cd2b4, `WarpModeController`,
  `DisplayWarpModeController`, `IsWarpedController`; flip model `FWarpMarkerContainer::mWarpMarkers` and
  `::mTempoAfterLastMarker`; Python enum `NWarperTypes::TWarpMode`, `OWarperBeats::TTransientLoopMode`;
  engine classes `OWarperBeats|Tones|Texture|RePitch|Elastique|Rex|UnWarped`.
- Member registrations (`registrations.txt`, via `FUN_10147e954`):
  - 0x10260fdd8 (AAbstractWarpMarker): `mSecTime` +0x50 and `mBeatTime` +0x58, last argument
    0x4_fffffffc = flags 4, type −4 ✓ (s8-0001: `orr x8,xzr,#0xfffffffc; movk x8,#0x4,LSL #32`).
    Flag 4 = written as attribute (n1-transport-state-v1). Matches `<WarpMarker Id=… SecTime=… BeatTime=…/>`.
  - 0x1027aff6c (AAudioClip): SampleRef, Onsets, WarpMode, DisplayWarpMode, GranularityTones,
    GranularityTexture, FluctuationTexture, TransientResolution, TransientLoopMode, TransientEnvelope,
    ComplexProFormants, ComplexProEnvelope, Sync, HiQ, Fade, Fades, PitchCoarse, PitchFine, SampleVolume,
    WarpMarkers (+0x650), SavedWarpMarkersForStretched, MarkersGenerated, IsSongTempoLeader, RightTempo.
    Order equals the 12.0_12402 schema order with DisplayWarpMode and RightTempo inserted; those two are
    absent from all 2,878 shipped AudioClips. The flag argument is a computed value in the pseudocode; how
    the two are excluded from documents was NOT traced.
  - 0x102882a38 (ASampleWarpProperties) and 0x10285d098 (another sample-part holder) register the same set.
  - 0x102875ec0 (ASampleRef): `mDefaultDuration` +0xe8 and `mDefaultSampleRate` +0xec, `mov w8,#0xfffffffc`
    (flags 0, type −4) ✓ s8-0003 → child elements `<DefaultDuration Value=…/>`.
- No symbol or string names a sample-time→beat-time conversion routine. `sample_to_beat_time` and
  `beat_to_sample_time` are referenced only by the Python module initialisers 0x103abc6e8 (decompile
  `failed` in C1) and 0x103b70cf8; their implementations were not located. See "Negative results".

## Round 1 — s8-0001 (8 dossiers)

- 0x1027c1c7c = AAudioClip vtable 0x10680bea0 slot +0xd0 (post-load; `vtable-reads.txt`). ✓ `ldr x0,[x19,#0x658];
  bl 0x10156da34; cbnz w0,0x1027c1e14` → `Empty warp marker array.` (0x105bd150b) → `bl 0x101488e64` →
  0x10148229c (document-corrupt error, see n1/n2) → `bl 0x10017b398` (no return). So an AudioClip whose
  WarpMarkers list is empty fails the load (static-derived). Non-empty: sets list flags, calls 0x1027b3928
  (owner links + onset association 0x1027b7cf0), sampler/clip updates, pitch factor powf(2^(1/12)…).
- 0x10260fdd8 ✓ (above). 0x1026105ec (AWarpMarker ctor) ✓ `mov x8,#0x7fefffffffffffff; dup v0.2D,x8;
  str q0,[x19,#0x50]` → SecTime and BeatTime both DBL_MAX (written `Invalid`); +0x60 = INT_MIN (onset link
  index, cleared by 0x102610298); registers `AWarpMarker::OnValueChanged`. APseudoWarpMarker ctor 0x1026128ac
  is identical without the callback (corpus only).
- 0x10261093c ✓ segment tempo: `d = s2.Sec − s1.Sec; if d <= 0 → −60.0; else (s2.Beat − s1.Beat)/d × 60`.
  0x102610910 (corpus) is the beats-per-second form (−1 when degenerate).
- 0x102612464 ✓ append shadow marker: new AWarpMarker after the current last one with
  `Beat = q(last.Beat + 0.03125)` and `Sec = last.Sec + (p2 × 60 / p1) × 0.03125` (`fmul d1,d9,60; fdiv d1,d1,d8;
  fmadd d0,d1,0.03125,d0`), where p1 is a tempo in BPM. q() = round to the nearest 1/3,843,840 beat, half away
  from zero (`frintm` of |x ± q/2|·3843840), skipped for four special constants at 0x1055d9680 (not read).
- 0x1026102c0 ✓ "is shadow": true when the marker is the list's last element (`ldr x21,[x0,#0x20]` … `cmp x8,x19`).
- 0x1027b0e40 (AAudioClip ctor) ✓ call contexts: TransientResolution enum init `mov w1,#0x6` with list 0x10701b060;
  TransientLoopMode `mov w1,#0x2` with list 0x10701b078; float params `FUN_1015743b0(s0,s1,s2,…)` stores
  +0x80,+0x84,+0x88 and sets the value to s2 (corpus 0x1015743b0). Getter constants (`getter-constants.txt`):
  GranularityTones (12, 100, 30); GranularityTexture (2, 263, 65); FluctuationTexture (0, 100, 25);
  ComplexProFormants (0, 100, 100); ComplexProEnvelope (8, 256, 128) with an integer-step curve (0x101577e1c);
  TransientEnvelope (0, **1.0**, 100) while its curve gets (0, 100) — anomaly, see Unknowns. RightTempo
  (5, 999, 120) immediate. WarpMode: if 0x101849958 returns 0, default 0 (Beats); else default =
  table[pref index] (0x1026a9ec4, table 0x105889f90 = 0,1,2,3,4,6). Labels set on the remoteables:
  "Warped", "Warp Mode", "Granularity Tones", "Granularity Texture", "Fluctuation Texture",
  "Complex Pro spectral envelope factor" (Formants), "Complex Pro spectral envelope order" (Envelope),
  "Quality" (HiQ), "Fade", "Tempo Leader/Follower".
- 0x1033bf42c (API add_warp_marker) ✓: audio clip only; warped only; sample time valid iff
  0 ≤ t ≤ sample length (`fcmp d8,#0; fccmp d8,d0,#2,ge; b.hi error`; NaN fails); new beat must not be
  below the left neighbour's beat (`fccmp …; b.mi`) and not above the right neighbour's unless the right
  neighbour is the shadow; beat quantised with q(); segment tempo to each neighbour must stay within
  [5, 999] BPM via 0x1027afd40 ("Segment length out of range.").

## Round 2 — s8-0002 (8 dossiers)

- 0x1026a9ef8 ✓ stored WarpMode list, `mov w2,#0x7`: Beats, Tones, Texture, Re-Pitch, Complex, REX, Complex Pro.
- 0x1027b279c ✓ TransientResolution list (7): 1 Bar, 1/2, 1/4, 1/8, 1/16, 1/32, Transients.
- 0x1027b29e8 ✓ TransientLoopMode list (3): LoopOs, LoopFwd, LoopAlt. The C-string block at 0x105af67ac
  pairs them with "Off", "Loop Forward", "Loop Back-and-Forth" and then "Transient Loop Mode"
  (`vtable-reads.txt`); the long labels are referenced by test code 0x100718e6c and 0x102820654 (inferred
  display labels).
- 0x102610bc4 ✓ scale all marker beats about the first (`b' = b0 + (b − b0)·f`, quantised), then re-place the
  last marker at `q(prev.Beat + 0.03125)` with its seconds rescaled (shadow kept 1/32 beat after the last real marker).
- 0x1033bfa68 ✓ API remove: finds the marker by exact quantised beat (0x1027c79d0, linear scan assuming
  ascending order), refuses the shadow: "The shadow marker can't be deleted."
- 0x1027afd40 ✓ bounds: Δs = new.Sec − nb.Sec; returns min/max of nb.Beat + Δs·999/60 and nb.Beat + Δs·5/60
  (`0x408f380000000000` = 999, `0x4014000000000000` = 5; 0x1021862f0 = sec·bpm/60).
- 0x1027c724c ✓ recording path: after inserting a marker it deletes the previous one if that marker's seconds
  lie within 0.001 s (`0x3f50624dd2f1a9fc`) of the straight line through its neighbours — a marker on the
  line is redundant, consistent with piecewise-linear mapping.
- 0x10288538c ✓ ASampleWarpProperties post-load: owner links only, no empty-list check (4,244 shipped
  SampleWarpProperties have zero markers).

## Round 3 — s8-0003 (7 dossiers)

- 0x10156da34 ✓ `add x0,x0,#0x70; b 0x101467280`; 0x101467280 ✓ `ldr w8,[x0,#0x58]; cmp w8,#0; cset eq` → empty test.
- 0x101488e64 ✓ builds the message and calls 0x10148229c.
- 0x1026101b4 ✓ BeatTime setter quantises (`frintm`, 3843840) before `str d0,[x0,#0x58]`; SecTime setter
  0x1026101a0 (corpus) stores unquantised. The loader 0x101487310 stores base values directly (n1), so
  loaded BeatTime is not quantised by this setter (static-derived).
- 0x1026aa13c ✓ DisplayWarpMode list (6, no REX): Beats, Tones, Texture, Re-Pitch, Complex, Complex Pro.
  0x1026aa354 (corpus) is the short-label twin ("Pro"). 0x1026a9820/0x1026a9a08 (corpus) are 5- and
  4-entry lists (without Complex Pro, and without Complex too); their selection condition was not traced.
- 0x102875ec0 ✓ (above). 0x1033bfb94 ✓ API move refuses the shadow: "The shadow marker can't be moved."

Budget: three rounds, 23 dossiers (8 + 8 + 7). No `str:` query.

## Corpus-only findings (not disassembly-confirmed)

- ASampleWarpProperties ctor 0x102883578: same float ranges/defaults as AAudioClip, TransientResolution
  default 6 (0x1027b2794 = `movz w0,#6`), TransientLoopMode 2 (0x1027b29e0), WarpMode default via
  0x1026a9ec4(0x102676cf0()), IsWarped default false.
- 0x1027b7cf0: links each marker to the onset whose quantised time equals the marker's SecTime (+0x60), walking
  markers and onsets in order.
- 0x1027c28dc: segment for a marker = (previous, marker), or (marker, next) for the first marker; drives the
  "Segment BPM" value. 0x10261097c: minimum segment tempo over the list (DBL_MAX when fewer than 2 markers).
- 0x1027d304c: builds a (sec, beat) vector and appends `beat + 0.03125`, `sec + 0.03125 / slope(last segment)`.
- 0x102610fb0 re-creates a trailing marker at +0.03125 beat from the previous segment's slope.
- 0x1033bded8 (API set warp_mode): value must be in the list from 0x1033be004, else "Invalid warp mode".
  0x1033be004 returns {5} (REX) when the sample's type bit is in the mask at 0x105800c50/58, otherwise a list
  that starts 0, 1, 2 … (the rest of the pseudocode was not read; whether 6 is conditional is unknown).
- `FWarpMarkerContainer` assertion strings: `Constraints::kMinSegmentBpm <= tempoAfterLastMarker() <=
  Constraints::kMaxSegmentBpm` (values not read).

## Static survey highlights (`static-survey.json`)

See the wiki page; all counts come from `checks` and `distributions`. Shipped documents were written by
12.4d1/12.1d1, not by 12.4.3.

## Negative results and stops

- Sample-time ↔ beat-time conversion routine for playback or for the API (`sample_to_beat_time`) was not
  located; the Python registration function 0x103abc6e8 failed to decompile and was not requested as a dossier
  (large). Piecewise-linear interpolation is inferred from segment tempo, shadow construction and the 1 ms
  collinearity test, not from a traced conversion function.
- How the RemoteableList loader orders `WarpMarker` children (document order assumed; sorting unknown).
- Version translator 0x1014919c4 (uses `WarpMarkers`, `WarpMarker`, `SecTime`, `BeatTime` strings) not traced.
- DisplayWarpMode/RightTempo exclusion from the writer not traced.
- No out-of-range check for WarpMode or the UserFloat settings on load was found; the generic loader stores
  values directly (n1); ARemoteableEnum's setter range check (n1, 0x10156675c) is not on the load path.
