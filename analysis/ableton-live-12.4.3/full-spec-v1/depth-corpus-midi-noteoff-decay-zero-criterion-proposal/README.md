# Proposed finite host34-zero B waveform criterion

This private proposal chooses **at most 1% relative waveform RMS error in each
channel** for only the frozen B history: gate1, note60 On1537/Off3073, host34=0.
It is a new finite engineering choice. It is neither an adopted case nor a
general gate/decay law. Capture approval, criterion review, owner adoption and
handoff review remain separate. This author reviewed preparation readiness;
that did not approve actual captures or this new method.

[Criterion](criterion.json) fixes the proposed kind
`noteoff_decay_zero_waveform`, exact reference SHA and arithmetic. The budget
was fixed before this packet measured waveform distances, after the original
capture descriptions were available, and before any candidate result. All38
host inputs and their order, events and timing come from the pinned B script.
The input is a stereo unit impulse4096 at44100Hz,16384frames/block512; stopped
transport0/0/120,inputflag1,MXCSR1f80,time0,fresh instance. No warmup, reset,
second note, bend, sustain or parameter update occurs. Host34=0 is an input
label, not proof of stored/UI conversion, actual source binding or NoteOff law.

## Why a new finite rule

B is a nonstationary transient; direct waveform comparison needs no stationary
pole eligibility, envelope/decay fit, onset detector or new estimator. Every
frame4096..16383 is included independently on both channels. Exactly131072
bytes of stereo interleaved little-endian binary32 and full-file finiteness are
required; scored reference and candidate energy must be positive in EACH
channel. Decode to binary64, then compute
`sqrt(math.fsum((candidate-reference)**2)/math.fsum(reference**2))`.
Subtraction/products, `fsum`, division, `sqrt` and inclusive computed-binary64
`E <= 0.01` define rounding; there is no epsilon. No alignment, gain, phase,
offset fitting, channel mixing, transient deletion or alternate window occurs.

The mathematical budget is1e-4 error energy/reference energy per channel; the
defined rounded square-root comparison controls acceptance. This is an
explicit local engineering neighborhood, not recovered tolerance, inaudibility,
uncertainty calibration, native-pole accuracy, ULP/vendor/Apple/arm64 or mixed
library-error proof. No B-specific sensitivity or repeatability calibration
exists here. A correct future candidate on unmeasured libraries/architectures
is not proved to fall inside this budget.

Released `waveform`/`filter` use0.0001 for other fixed histories. That number's
existence does not establish its applicability to B. The approved Ramp method
has suitable arithmetic but its reference, musical history and sensitivity
evidence do not transfer. Its CLI deliberately rejects B's reference hash.
Thus this proposal requires its own named kind, exact B identity gate and
independent engineering-budget review. No published comparator is changed,
imported or run. This is not choosing a threshold from the observed wrong-output
distance, and the controls do not calibrate original variation.

## Measured controls and explicit limits

[Results](results.json) retain all quantities. B's scored energies are
0.04639744101570795 left and0.038413628080581796 right; self-error is zero.
Fresh A-held, fresh C-gate0-Off and old host34=1 B each fail the proposed rule
with errors9.147024433538633 left and9.104080744315864 right. Their FULL files
differ, but all three have identical scored bytes. They supply **one unique
wrong-waveform contrast**, not three independent behavioral controls, a
universal wrong-output detector or proof that a particular internal path ran.

Frames0..4095 receive length/finiteness validation only. Finite corruption there
can pass. Aggregate RMS can hide concentrated/onset/low-energy-tail defects;
it does not grade an exact silence time, envelope, tail floor or local decay.
Deliberately zeroing B's entire last8192frames still passes (errors about
2.04e-7 left/2.02e-7 right). That is a deliberate scope-limit control, not an
assertion that the tail is zero or unimportant. The complete captured reference
and every scored sample remain retained; no tail cutoff was added to the rule.

Twenty-one mathematical tests exercise the inclusive1%boundary and adjacent
binary32 samples, either-channel failure, gain/polarity algebra, first/last
window roles, finite-prefix exclusion, length/nonfinite/zero-energy rejection
and wrong reference identity. These are synthetic arithmetic data, not new
device runs or candidate implementations.

## Read-only reproduction and provenance

Read [measure.py](measure.py) before running `python3 -B measure.py --check` in
this directory. It reads exact [input pins](inputs.json), verifies both capture
inventories and the pinned B identity, runs only new stdlib arithmetic, checks
the retained results and prints JSON. After sealing it also checks its own
payload inventory/hashes. It never writes reports, imports old comparators or
invokes collectors/native code/models/fits/FFT. `--self-test` uses only synthetic
bytes. Unsupported modes refuse before source reads.

Capture manifests are verified mechanically; this is not an independent capture
review or source/harness certification. Current R5 was read against its existing
immutable snapshot; publishedv3 and the approved Ramp method are pinned as data
only. No mutable canonical future equality gate, duplicate source capture,
original run, owner/release edit, new normative ID/case/grade or coverage credit
is introduced. General MIDI/Live routing, source dispatch/application, all174old
modal omissions and both note72mode16 omissions remain unknown/ungraded.

Author readback retained the exact distances and controls. One data-output
retention attempt had too small a tool output budget, so its successful
measurement stdout was truncated and the outer JSON parser refused it; the
data-only check was repeated with sufficient output capacity. No native call,
failed numerical test, threshold change or discarded measurement occurred.
The first preseal link check also rejected relative links inside the quoted
as-of governance text in `inputs.json` by incorrectly treating them as current
packet navigation. Validation was restricted to this README's actual links;
the embedded source text remains byte-exact. No manifest had been created.

Independent review and any later adoption are pending. This packet is a
proposal for that review, not product compatibility or completion.
