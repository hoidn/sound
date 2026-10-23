# Proposed finite Corpus held-note-60 case

Unadopted author proposal. No normative ID, acceptance result or release is assigned. The companion JSON supplies the complete vector, all 32 frozen mode entries and exact input identities. Independent capture, method, owner and handoff review remain separate gates.

## Exact input and expected output

Begin with a fresh state, set 44,100 Hz, and apply the companion's 38 named comparison values once in their listed order, rounding decimals to binary32. Process exactly 16,384 stereo frames in blocks of 512. Supply the existing unit impulse at frame 4096 in both channels (`signals/input-01.f32`, SHA-256 `03a7d8daa68e79547578a53d7fed8e6cc872e0e81a22368615f0fa61b7b083f6`), flag input present each block, and hold transport stopped at position 0 and tempo 120. No reset, warm-up or parameter changes occur.

Supply exactly one event: `{"frame":1537,"kind":"note_on","channel":0,"key":60,"velocity":100}`. Channel numbers are zero based. Following the existing Analog comparison convention, deliver it in the block containing its absolute host/test coordinate: block start 1536, local offset 1. There is no additional adapter subtraction or alignment. Send no note-off or other event before the capture ends; the held note's destruction/release tail is not compared.

MidiPitch is 1, MidiGate and LFO are 0; the vector includes LfoRate binary32 0.8 and LfoAmount binary32 0.3 even though LFO is off. Host strike/listening positions are 0.5/0.1/0.9, with String/Low/Decay1 and wet output. These are exact comparison inputs, not stored-value or insertion-default claims.

The reference is the actual note60 capture: 131,072 bytes, SHA-256 `5866c6b9e4915336648da87bd92c38927cb3e532fe81ab38b5300664c7bb984f`. Future packaging should retain that full file rather than describe its prefix as equal to an older reference. Reference MXCSR `0x1f80`, time seed 0 and substituted libraries describe its capture environment, not a required candidate architecture.

## Unchanged modal comparison

Use the released `CORPUS-AUDIO-013-04` metric object without changing any of its 16 centers/cutoffs per channel, estimator or threshold. Both channels must satisfy the initial waveform relative RMS limit 0.002 on frames 4096–4351 and every existing frequency, per-frame log-radius and complex-amplitude check. The companion records the exact formulas. No fitting/alignment correction, new epsilon or tolerance is introduced. Invalid lengths, nonfinite samples anywhere, zero reference denominators and missing or unmeasurable required modes fail.

The reuse basis is literal data identity: all interleaved bytes from frame 4096 through 16383 equal the released 013-04 reference. Its existing pole/reference eligibility therefore need not be re-derived for this identical scored data. Every cutoff is 100 Hz, giving 1455 FIR taps; fits use frames 5551–16383 and depend only on input frame 4097 onward. The existing code unwraps phase only inside that fit segment. The initial waveform window is also inside the identical region. No fit or comparator was executed to prepare this proposal.

Frames 0–4095 are validated only for full-file format and finiteness. They have no error budget, equality, silence/floor, onset, startup, phase or event-time expectation. Finite corruption there can pass. No general startup, Sine, LFO or Ramp row additionally applies. The selected modal checks also leave omitted modes and arbitrary additional long-term energy incompletely constrained.

## Scope that must remain explicit

The released fixed-pitch 013-04 output itself satisfies all proposed scored windows. This single case cannot reject an implementation that ignores the MIDI note or MidiPitch. It is one event-bearing finite input/output obligation, not proof of note admission, note identity, transposition or the entire MIDI side chain.

The reference driver encoded a 16-byte record and forwarded local coordinate 1. The old report's bundle offset-minus-one observation remains private source context; neither that internal layout nor decrement is a candidate requirement, and neither proves Live's event origin. Do not change the declared event input to frame 1536 to imitate an inferred mechanism.

Note72 remains ungraded and needs its own justified pole centers and reference-mode eligibility. Gate, note-off/release, sustain, bend, priority, velocity scaling, channels, boundaries, other vectors and histories, Live routing, A1 and arm64 behavior remain unknown. No invariance, general pitch formula, Ramp 1% or Sine 0.2 Hz criterion transfers.

If independently approved later, assign one new case ID and an exact exception to the current event-free protocol; preserve all 69 released evaluations, fixtures and numerical rules. The existing modal evaluator needs no new measurement algorithm for this object. No canonical, packet or release was changed here, and no native code, old comparator, fit, model, FFT or candidate was executed.
