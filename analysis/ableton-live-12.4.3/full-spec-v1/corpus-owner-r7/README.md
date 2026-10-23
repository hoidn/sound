# Private Corpus owner R7 proposal

This is a proposed owner successor, not an adopted canonical specification or
published handoff. The separate finite-method review is approved; independent
owner review and adoption remain pending. No candidate or application grade is
assigned. Root owns any later canonical adoption and handoff work.

[spec-r7.md](spec-r7.md) preserves the exact adopted
[R6 provider](../corpus-owner-r6/spec-r6.md), 58,472 bytes with SHA-256
`07a89f25de6b3c987d448e0e049bdd7dfaec52f479532b3aca3faddedcd511cd`.
[delta.json](delta.json) reconstructs R7 from that immutable provider: revision
metadata changes from 6 to 7; every normative change is an insertion. All 13
requirement IDs, all 32 old case rows, the complete REQ-013 body and all earlier
finite budgets remain literal. There is no redundant archive or historical
checker replay. The R7 proposal has 33 cases: 29 finite subsets and four U rows,
with only DCO-033 added under REQ-001/012. No release group/evaluation ID is
allocated here.

[cases-additions.json](cases-additions.json) contains the complete new fixture.
Its initial 38 binary32 values and order match old CORPUS-AUDIO-006-01. One fresh
instance processes two consecutive 8,192-frame segments, with ListeningXL host
index 15 set to exactly 0.75 between them. The rate is 44,100 Hz, block size 512,
and the existing stereo I1 impulse is at frame 4,096. Other parameters, including
the right pickup, remain unchanged; MIDI and LFO are off. The reference uses
stopped transport 0/0/120, input-present before each block, MXCSR 0x1f80 and time
zero, with no events, reset, warm-up or input restart. These environment facts
do not prescribe candidate architecture or establish new invariance.

The proposed dedicated waveform rule requires the exact step reference hash,
exact 131,072-byte stereo binary32 format and full-file finite samples. Four
checks score pre/post windows [4096,8192) and [8192,16384), independently for L/R.
Every reference and candidate region must have positive energy. Binary64
subtraction/products, `math.fsum`, division and square root give normalized RMS;
all four computed errors must be at most 0.01, inclusive without epsilon. There
is no alignment, gain/phase/offset fitting, pooling or transition exclusion.
Frames 0–4095 are finite-only. This is an explicit new finite engineering budget,
not calibrated uncertainty or transferred tolerance from an earlier case.

[provenance.json](provenance.json) retains exact pointers and all four error,
validity and outcome projections for every one of the 38 actual method controls:
152 axis records, 108 valid and 44 invalid, with all 89 required checks reported
passing. Ignoring the step fails postL at 0.8990030348930524. Four isolated 2%
corruptions fail their own axes while preserving the other three. A concentrated
last-right-sample error passes at 0.005000000371140732, and finite-prefix123
corruption passes. Artificial 1/512-frame splices and last-512 zeroing fail these
vectors, without proving physical timing, smoothing duration or a tail law.
The aggregate budget can hide localized defects. No 4,000-frame movement,
eight-frame latency, general right invariance, A1, application behavior or modal
omission is resolved. All 174 old modal omissions and two note72 mode16 omissions
remain unchanged.

[method-review-binding.json](method-review-binding.json) binds the full
[independent actual-method review](../reviews/corpus-pickup-step-method-actual-review.json),
15,881 bytes, SHA-256
`fad41d66e488702cff011632aedd712f422a9305a519b22038da38a7d2a8518d`.
Its approval is limited to the finite method and validation, not this owner
successor. [inputs.json](inputs.json) pins that review, the original capture and
review, effective design/addendum, actual validation, R6 and published v4. These
are immutable/as-of dependencies; no live canonical hash gate or consumer adapter
is introduced. Earlier R6 semantic review is carried, not freshly reapproved.
The new fixture, all 38 comparison projections and the complete actual-method
review were freshly read as data. No measurement was rerun for this proposal.

Read [check.py](check.py) before running:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/corpus-owner-r7/check.py --check
```

This read-only stdlib checker reconstructs the exact text delta, dereferences the
38 result pointers, verifies source/payload hashes, old rows, REQ-013, the new
fixture and review binding, checks links/whitespace, and rejects eleven unsafe
mutations. It watches its finite input/payload set before and after. It performs
no audio decoding, metric arithmetic, imports or replay of old tools, original
calls, model/FFT/fits, candidate execution, canonical adoption or publication.
Unsupported arguments are refused; frozen reports are never rewritten by replay.
