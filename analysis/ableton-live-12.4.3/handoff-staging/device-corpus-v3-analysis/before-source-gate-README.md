# Corpus audio comparison, draft release3

**Unreviewed draft.** The finite method has separate approval; proposed parent
revision5 and this handoff await independent approval. This directory is not a released implementation target.
Read [the contract](spec.md), [cases](cases.json), [unchanged measurement tool](compare.py),
[draft manifest](manifest.json), [role instructions](AGENTS.md) and
[pending review](REVIEW.md). Prior release2 approval does not approve this extension.

The draft preserves all69 prior evaluations,78 input/reference fixture bytes and
measurement code, adding group025 with held note60/72 vectors and two references.
There are25groups/71evaluations,71reference files/64distinct reference byte streams,
and nine generated signals. Every output is16384stereo frames, little-endian
binary32 without a header. Parameters are complete named binary32 comparison
inputs, not a claimed stored-value mapping or device API. The two events use an
explicit host/test coordinate, not an inferred Live frame base.

Reference outputs come from original x86_64 device-code execution with substituted
Linux libraries. No original application, arm64 device or candidate ran here.
025-01 uses a literal scored-region match to an existing fixed-pitch reference;
it cannot alone detect ignored MIDI.025-02 proposes30fixed modal points as an
explicit finite engineering eligibility decision; both mode16 estimates remain
ungraded and no tolerance was widened. Prefix0–4095 is finite-format-only.
All general MIDI routing/handling and broader compatibility remain excluded.

The measurement dependency remains Python, NumPy and SciPy; their availability
does not authorize installation. A future approved package would compare one
headerless stereo file named `<evaluation-id>.f32` per listed evaluation through
`python compare.py /absolute/path/to/candidate-outputs`. Exit0 means its listed
finite measurements pass; missing, malformed, nonfinite or unmeasurable output
fails. Author data-only self checks pass98+92measurements for the two additions;
the wrong-note control fails64/92 as expected. These are measurement checks,
not executions of a candidate or original device. The prior4603measurements
are carried from release2 approval, not rerun here. Independent owner and
handoff review remain necessary before any local publication.
