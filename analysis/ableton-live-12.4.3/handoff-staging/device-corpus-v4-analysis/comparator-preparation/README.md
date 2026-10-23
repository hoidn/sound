# Private comparator preparation — not release4

This reversible preparation adds only the proposed
`noteoff_decay_zero_waveform` kind and its exact B-reference guard to a copy of
releasedv3. Method, owner and eventual release approval are separate gates;
this directory adopts nothing and can be discarded. It is not a public handoff.
No source/canonical/released file or evaluation object was edited.

[Patch](patch.diff) adds nine lines for the new branch and four for its separate
reference-SHA guard. Removing only those insertions reconstructs the7795Bv3
source byte-exact. The private8830B [candidate](compare.py) has SHA
`9964de11da79eb61c0624d34e402d238cd5c466093d15ccc91fd630ac4c54110`.
All earlier branches, labels, errors and the Ramp reference guard remain literal.
The new guard requires B SHA
`a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829`;
it neither bypasses nor broadens the existing Ramp hardpin.

The new branch has fixed full4096..16383 per-channel `math.fsum` waveform RMS
arithmetic, positive reference/candidate energy, inclusive0.01 and no options,
fitting/alignment/gain/phase normalization. Full-file size/finiteness remains
the existing `audio()` gate. Direct `compare()` calls support mathematical
fixtures; actual evaluation must use the case-specific reference gate in the
NEW data-only run driver. Reference identity cannot establish candidate input
provenance; any later case/harness must supply its exact38host values/history.

## Actual preparation results

[Full numerical report](numeric-results.json) retains every old measurement
and new test; [summary](summary.json) gives counts. Using only this NEW private
candidate's measurement functions, all71old evaluations passed4793/4793
measurements against their own references. B self passed2/2, giving4795actual
self-measurements, not a number inferred before running. The report retains311
small nonzero old-self errors; it does not claim all errors are zero. The largest
raw number3.2476120812840545e-15 spans heterogeneous old metric units and is
not an uncertainty estimate or new tolerance. No candidate device DSP ran.

Wrong freshA, freshC and oldhost34=1B fail with9.147024433538633 left and
9.104080744315864 right. They duplicate one scored waveform and are not three
independent contrasts. The same pinned criterion-proposal results reproduce
exactly. Fifteen arithmetic controls exercise inclusive/adjacent boundaries,
either-channel failure, gain/polarity, zero-energy failure and first/last window
roles. Eight actual new-run driver scenarios test correct Ramp+B references,
separate wrong-reference rejection, short/extra/NaN/Inf and finite-zero inputs.
Both independent reference guards retain their own failure labels.

Finite-prefix corruption and deliberately zeroed lateB both pass as explicit
scope limits. Aggregate RMS does not grade exact tail/silence, local decay,
NoteOff admission, timing, public gate behavior or Live/source binding. No
unmeasured rate/block/history/repeatability/architecture or original sensitivity
claim follows. Newkind is still proposed; all old requirement/case/omission
scopes remain as-of and unchanged.

## Executed code and preservation

The [current preparation checker](check.py) was fully inspected before its one
26.08second data-only run. It disables bytecode writing before loading ONLY the
NEW private comparator with a non-main name, then restores that setting. Old
measurement functions copied into this new candidate include the already
authorized fits/FFT needed by71old cases; no released comparator, old CLI/main,
private fit/model, collector, original/native device or candidate DSP executes.
Its new `run()` driver is exercised only on synthetic data fixtures with a
temporarily replaced private `HERE`, restored in `finally`.

The checker writes/removes only its own temporary synthetic files under this
private directory; measurements go to stdout. It does not rewrite retained
reports or published files. Inspect it before any rerun; a numerical rerun is
unnecessary unless a new concern warrants it. [Receipt](execution-receipt.json)
retains exact command/time/exit0/empty stderr and full stdout hash.

All269watched paths stayed unchanged during that run, including every payload
of Corpus releasesv1/v2/v3, the exact71evaluation provider and canonical bytes
watched as-of. This is not a future live-canonical equality gate. Immutable
input pins are [here](inputs.json); current inspection does not renew semantic
approval of every prior case. Native/original/candidateDSP calls: zero.

Only private preparation files exist here. No finalv4manifest, owner adoption,
shared routing, publication or implementation is supplied by this preparation.
