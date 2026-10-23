# D-02 released-case first action

Analyst-only schema/expectation census, frozen pending separate review as of
authoring. The [sole plan revision 3](../../../../wiki/research/full-live-specification-plan.md#revision-3--depth-before-breadth-2026-10-19)
selects this first action; this is not a new whole-product queue or source audit.

[census.json](census.json) inspects the 19 current immutable releases: 1,070
case rows, zero missing/unknown whole-case expectations in their three published
JSON forms. Every expectation/reference metric must exist; referenced device
captures and cases/specs verify against each release manifest. No comparator,
reference application or candidate runs. Case rows and device evaluations are
different dimensions; no coverage percentage follows.

[triage.json](triage.json) preserves the important limits. Five ALS refusal
outcomes remain specified while their refusal class is not compared. Analog's
32 null voice-end fields explicitly omit end comparisons; MIDI's 99 null bank
values and Structure's six empty slots are defined state. Existing narrower
comparison masks, excluded behaviors and inconclusive reference observations
remain. This does not declare all outcome properties graded.

The six Plugin Discovery and eight wholly/partly ungraded Playback scenarios
are **draft-only**, with exact raw rows and as-of providers. Their local numbers
must not be joined to similarly numbered release cases. No released case is
withdrawn or changed. Plan D-02's premise that those releases contain unknown
whole-case oracles needs this qualification. This first action closes no U,
changes no T1 exclusion, and supplies no new X/S grade.

The pinned `impl` commit has no IQ rows. Its old template statement about no
handoffs is stale; only absence of entries is used. No moving branch or draft
canonical hash is a future check dependency. Draft snapshots are necessary
as-of providers here. Candidate conformance remains unexecuted, with no fraction
reported. D-01/D-03 capability gates remain selectable under the sole plan.

Run the current read-only check:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/released-case-depth-census/check.py --check
```

It rejects eight absent/unknown expectation forms, checks exact census/provider
rows and the seal if present. Other arguments are refused before reading inputs.
[manifest.json](manifest.json) seals this packet; it does not release a contract.
No historical release scripts, source examples, plugins, original functions,
network/configuration operations or implementation work execute.
