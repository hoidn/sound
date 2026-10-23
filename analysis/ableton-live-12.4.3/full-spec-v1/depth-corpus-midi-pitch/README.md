# Corpus MidiPitch: two finite extracted-event captures

Author freeze: 2026-10-19 Pacific / 2026-10-20 UTC. Root's observations are
retained; independent review is pending. No criterion or behavioral grade adopted.

Root executed exactly two new original x86_64 Corpus children at 06:31:45 UTC
on 2026-10-20, after the [independent preflight review](../reviews/corpus-midi-pitch-preflight-review.json).
The collector was authored by the Delay analyst and invoked once by Root.
No application or arm64 executable ran. The unchanged loader called the shipped
create/rate/parameter/process/destroy exports with the declared raw event.
This is finite bundle extracted execution, not Live's MIDI side-chain route.

Both children exited 0, each produced 131,072 bytes / 16,384 finite stereo
binary32 frames, and both channels had post-impulse peak and mean-square energy
above their pre-impulse floor. Stderr was empty, no trap/fault was hit, and
`cxx-failbits 0` was reported. Declared unused import trap slots are not hits.

| Case | Raw capture SHA-256 |
| --- | --- |
| note60 | `5866c6b9e4915336648da87bd92c38927cb3e532fe81ab38b5300664c7bb984f` |
| note72 | `f98b465f7186680830bc87c97f4a4096e1e53b2ad1b07aa5333ccccd6ea36ddc` |

The two complete scripts differ only in note number 60 versus 72. They preserve
the previous Sine baseline's 38 parameter inputs except enabling MidiPitch at
index 12 and disabling LFO at index 17. MidiGate stays off. Each child receives
one note-on, status `0x90`, velocity 100, at harness coordinate 1537, before the
same stereo unit impulse at frame 4096. No note-off, bend, sustain, additional
note, reset or warm-up is sent. The note remains held through destruction.
Both use 44.1 kHz, blocks 512, MXCSR `0x1f80`, stopped transport `{0,0,120}`,
input flag 1 and time seed 0. Full actual environment, limits, UTC/PID/status and
imports are retained; library/ULP/trace injection settings are absent. Core
limits were 0 and the child timeout was 30 seconds.

The inspected script parser stores a 16-byte event and forwards one event in
host block 1536 with local coordinate 1; other blocks receive zero count/null.
The Corpus report's nonzero-coordinate decrement is retained source context,
not a measured Live origin or onset-time rule. A queued command, nonempty audio
or merely different bytes alone does not establish correct note delivery.

The recorded `manifest-preflight.json` seals five preparation payloads. Its
`diagnostic.py` (1,650 bytes) remains as prepared and **was not executed**.
Root selected and ran Synth's separate `diagnostic-selected.py` (6,848 bytes,
SHA-256 `b6b80a9c04472e5627a48a464d36114af42aa434e957fc4bf9f077e3562559bf`).
`diagnostic-selection.json` records that choice; the proposal's future-analysis
text is historical preparation, not the actual method. The selected method uses
three predeclared full/half post-impulse windows, symmetric Hann, 8x FFT padding,
eight local peaks and fixed 261.62/523.24 +/-20 Hz descriptive bands. Padding
refines the displayed grid, not resolution or uncertainty. Spectral-bin magnitude
is not a calibrated component amplitude or fundamental-frequency estimate.
The method source/read/self-test selection preceded capture in the task history;
`diagnostic-selection.json` was written afterward and is not an earlier immutable
timestamp. Root's observations retain that distinction.

Root's `observations.json` preserves the interpretation separately from the
collector's earlier `results.json`: its `UNESTABLISHED` note-delivery field is an
as-of state before spectral analysis and is not overwritten. Root records several
prominent components shifting approximately an octave in both channels and all
three windows, consistent with the selected note-60-to-72 hypothesis. These are
coarse observations, not calibrated fundamentals or a note-identity criterion.
The illustrative first four A peaks are paired with retained B peaks nearest
twice their frequencies; those pairs are not unique mode correspondences.
Note 60 already has a substantial 523 Hz component, so band presence or the
largest peak alone cannot establish note identity. Small 261 Hz band values in
note 72 are finite leakage observations, not proof of absence. Spectra and this
interpretation add no note-identity acceptance threshold, phase/onset law or
general MIDI behavior. No Sine 0.2 Hz or Ramp 1% criterion is
transferred. Gate/release, bend, sustain, priority, other vectors/rates/boundaries,
Live routing/A1, arm64 behavior and all 174 omitted modal observations remain
ungraded. This packet adds no normative IDs/cases or release expectation.

The collector preserved all 530 watched historical/provider files. Full mutable
wiki contexts were embedded as of capture; future checking uses those snapshots
rather than requiring old live wiki hashes. Old captures, source bytes and both
Corpus releases remain unchanged. No old runner, collector, model, fit or
comparator was imported or replayed; there was no retry or extra original call.
The cumulative selected Corpus depth captures are six: two Ramp, two sensitivity,
and these two MIDI captures.

`check.py --check` is newly authored retained-data verification, fully read by
Root before execution. It checks exact preparation/source/input/vector bits, raw
outputs, logs, productive baselines and preservation, and reproduces only the
fully read selected **data-only** `describe` method. Root's illustrative component
pairing remains an explicitly qualified interpretation for independent review. It never calls either collector,
original code, the unselected diagnostic or old tools. Seven finite negative
fixtures cover malformed data, event/parameter changes, provider identity and
failed/productivity records. Write/replay arguments are rejected. Do not rerun
`capture-once.py`; its exclusive destination exists and these captures are final.
