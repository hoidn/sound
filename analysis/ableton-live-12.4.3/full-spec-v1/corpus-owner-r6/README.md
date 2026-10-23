# Private Corpus R6 draft: one host34-zero Off history

AS-OF AUTHOR FREEZE: the finite criterion has independent approval; this owner
review/adoption remains pending. Nothing here adopts a canonical page, release
or candidate grade. Current disposition is routed through the shared spec index. Root assigned
DCO-032; no new requirement or release evaluation/group ID is allocated.

`spec-before-r5.md` is the exact51,090-byte canonical R5 snapshot, SHA-256
`aba64f5c420091617c16d28c9f0d2437c0eacf67ed1940bfe27250644038eecf`.
The immutable old [R5 owner](../corpus-owner-r5/README.md) and all its payloads
remain unchanged. [Delta](delta.json) reconstructs [spec-r6.md](spec-r6.md)
without changing any of the complete clauses001–012, all13requirement IDs or
31old anchored case rows. The only new row is DCO-032: proposed32cases,
28finite/fourU. DCO-026, A1,174oldmodal omissions, both note72mode16 omissions,
general MIDI/Live/UI routing and the earlier finite case scopes stay open.

[Cases](cases-additions.json) contains ONE complete38-value HOST fixture:
B gate1, note60 On1537/Off3073, host34=positivezero, LFOoff, I1at4096,
44100Hz/16384frames/block512; stopped0/0/120,inputflag1, referenceMXCSR1f80,
time0,fresh instance and no reset/warm-up/other event/update. No extra adapter
subtraction is allowed. Host34=0 is not a decoded stored/UI/unit conversion.
The exact captured reference SHA is
`a378ac6de6c04041a21aee501094be643fdb6615d3fc212ebbcc32afdf76d829`.
The [capture](../depth-corpus-midi-noteoff-decay-zero/CAPTURE.md) and separate
[actual review](../reviews/corpus-midi-noteoff-decay-zero-capture-review.json)
approve observations only. This author reviewed those captures and does not
self-approve this owner; a separate owner reviewer must assess the proposal.

The [criterion proposal](../depth-corpus-midi-noteoff-decay-zero-criterion-proposal/README.md)
selects `noteoff_decay_zero_waveform`: fullfinite/exactlength, positive scored
reference/candidate energy in EACHchannel, ALL4096..16383 frames, per-channel
`sqrt(fsum(error**2)/fsum(reference**2)) <= 0.01` with computedbinary64 rounding,
no epsilon/alignment/fitting/mixing/window substitution. This is a new finite
engineering budget, not transferred Ramp applicability/sensitivity or a recovered
native/Apple/arm64/ULP/inaudibility uncertainty guarantee. Prefix0..4095finite-only;
finite prefix corruption and deliberate late-tailzero can pass the aggregate
budget. B's actual tail is nonzero. No silence, timing, decay, general gate or
output-flag/scheduling law is adopted. No comparator is authored or changed here.

[Inputs](inputs.json) binds immutable owner/capture/criterion payloads as-of;
`criterion_review_binding` pins the separate [independent method approval](../reviews/corpus-midi-noteoff-decay-zero-criterion-review.json)
(15,328bytes, SHA47ff51b4bc0987444506f925cd4c6e58cd6d3ca8955ab237edbd40989c1d55ad).
[Binding history](method-review-binding.json) retains the former unsealedpending
state; no threshold, reference, input or numerical operation changed.
[Historical consumers](historical-consumers.json) records a bounded39-file R5hash
search:38immutable historicalfiles plus one active parallel comparator-prep
input, which is AS-OFONLY and excluded from future identity gates. No consumer,
old checker, published payload or root adapter is rewritten/replayed. Snapshot
links inside spec-r6 resolve in the original `wiki/specs/` context; README links
resolve here. This is an analyst draft, not a clean implementation input.

`check.py --check-draft` is a read-only stdlib text/JSON/raw-metadata integrity
check, not a waveform comparator or original/model/old-tool invocation. It checks
exactdelta/IDs/oldrows/001–012, fixedreference/vector/events/format/scoredwindow,
nullgrades and meaningful rejection fixtures. `--check` additionally requires a
bound independent approved method review; unsupported write/seal/capture modes
refuse. The final manifest binds this private owner proposal only, after method
approval. Actual Root adoption and separate owner/handoff review remain later
decisions. The author invokes no comparator, estimator, model, capture or native code.
