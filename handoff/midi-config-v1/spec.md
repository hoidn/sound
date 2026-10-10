# MIDI configuration assignments — finite release revision 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS.
Feature: FEAT-MIDI-USER-MAPPING. Parent specification identity:
SPEC-MIDI-USER-MAPPING revision 1. Only the clauses explicitly included below
are approved for this handoff. No other clause of a listed requirement is
implicitly approved. This document is self-contained.

## What the contract means

A user supplies a text file named `UserConfiguration.txt` assigning MIDI
Control Change messages to master volume, cue/preview volume, and crossfader.
This contract describes the configured routing meaning of that input: which
assignments are enabled, which MIDI number/channel identifies each one, and
which of those three user targets it names. It does not specify parameter
values resulting from a CC data value, any audio result, or when a loaded
configuration takes effect.

All rules and expected results are **static-derived**, supported by reviewed
package evidence before sanitization, and not observed reference executions.
No compatibility result is established. The original application remains the
independent authority for a later comparison.

## Preconditions and bounded input grammar

Each fixture is a complete, independently authored ASCII text file with LF
newlines and the four exact sections `Globals`, `DeviceControls`,
`MixerControls`, and `TransportControls`. Keys use a colon followed by one
space. Numeric fields contain plain decimal integers with an optional minus
sign, or the exact malformed example `abc`; omitted fields are also covered.
There are no duplicate keys, duplicate sections, interpolation, default sections,
comments, unknown fields, continuation lines or encoding variants. Other lexical
forms have no expectation in this revision.

`GlobalChannel` appears in `Globals`. The supported fields in `MixerControls`
are listed below. `VolumeMapMode: Absolute` and
`CrossfaderMapMode: Absolute` are explicit in every fixture. The other sections
are empty. Controls outside this finite surface are unassigned. Assignments
have distinct MIDI addresses. All runtime interpretations assume a selected,
active profile and available targets, correct input-port routing and no competing
mapping or owner. Discovery and activation procedure remain outside the contract.

| CC number key | Optional channel key | User target |
| --- | --- | --- |
| `MasterVolumeSlider` | `MasterSliderChannel` | Master volume |
| `CueVolumeSlider` | `CueSliderChannel` | Cue/preview volume |
| `CrossfaderSlider` | `CrossfaderSliderChannel` | Crossfader |

## Selected requirement clauses

**REQ-MIDI-USER-002 — partial: the three ordinary CC assignments above.**
A present integer CC number from 0 through 127 enables that assignment.
A missing number, `-1`, any other out-of-range integer, or the ordinary
conversion failure `abc` disables it. A disabled assignment has no route in
the comparison representation. Interpolation failures, pad-note fields and
all other control fields are excluded. This is not a guarantee that a disabled
route prevents every possible effect of a message elsewhere in the application.

**REQ-MIDI-USER-003 — partial: global and the three channel fields above.**
An integer GlobalChannel from 0 through 15 supplies the ordinary global channel.
A missing, out-of-range or ordinarily noninteger global value supplies channel 0
for these controls. A per-control integer channel from 0 through 15 overrides
the global channel. A missing, `-1`, other out-of-range, or ordinarily noninteger
per-control value uses the effective global channel. A valid explicit channel
works even when the global value is invalid. These channel rules do not enable
an invalid CC number. No pad behavior is included.

**REQ-MIDI-USER-010 — partial: target association only.**
Each enabled assignment names the corresponding user target in the table.
Map mode is fixed to explicit Absolute as a precondition. This clause does not
establish numerical scaling, clipping, smoothing, feedback, takeover, audio
results, or other mode behavior.

**REQ-MIDI-USER-013 — partial: option-name case normalization only.**
Changing the ASCII letter case of a supported option name preserves its meaning.
The section spellings in the preconditions are exact. No behavior for malformed
syntax, unknown options, duplicate inputs, different section spellings or Boolean
settings is approved by this clause.

## Acceptance representation and comparison

[cases.json](cases.json) identifies each input and its complete expected set of
enabled assignments within the finite scope. Every assignment contains:

| Field | Comparison meaning |
| --- | --- |
| `control` | Canonical public CC-number key from the table |
| `target` | `master-volume`, `cue-volume`, or `crossfader` |
| `message_type` | `control-change` |
| `number` | Integer MIDI CC number, 0–127 |
| `channel` | Effective integer MIDI channel, 0–15 |

The assignment list is a **project comparison representation**, not a claimed
Live API or recovered internal structure. No parser entrypoint, data structure,
algorithm or module layout is prescribed. A candidate adapter may translate its
own configuration result into these labels. Compare exact sets: no missing or
extra assignments, and exact field values. List ordering has no meaning. An
empty set means none of the three controls is assigned.

Every case starts from fresh input; cases do not mutate a previous active
profile. Logical interpretation has no timing tolerance. It is inappropriate
to treat a short wait with no audible change as proof that an assignment is
disabled. A future reference probe must state how the profile became active,
how routing was observed, and which alternative mappings were eliminated.
The fixture set is not an executable original-application harness.

The cases cover all targets, both CC endpoints, disabled/missing/noninteger CCs,
channel endpoints and fallbacks, explicit-channel precedence, simultaneous
independent assignments and mixed-case options. Comparators apply only to these
logical expectations. Numerical or audio comparisons have no oracle here.

## Deferred obligations and exclusions

Before claiming reference compatibility, run a separately designed bounded probe
for the listed cases or an explicitly justified equivalent coverage set, pin the
original/candidate builds and configuration bytes, retain independent reference
observations and report mismatches. Static-derived expected results cannot stand
in for those observations. Candidate-only fixture success proves agreement with
this contract, not agreement with a running original.

Excluded or unknown: profile discovery, activation/reload timing, input ports,
missing-target and collision behavior; other controls; pad and device banking;
parameter response curves; alternate modes; MIDI feedback; UI presentation and
error recovery; note lifetime; undo; automation; persistence across save/reopen;
simultaneous-event ordering; real-time latency, cancellation and disconnect or
teardown with held controls. The finite interpretation operation has no specified
asynchronous lifecycle, so those cases are deferred rather than passed or
irrelevant. A future release must add requirements before implementing their
compatibility behavior.

## Fixture provenance and revision

All included text fixtures were authored for this candidate using the public
configuration field spellings needed to express the interface. They contain no
shipped comments, original configuration file content beyond those interface
names and simple values, executable code, recovered pseudocode or assets.
Expected JSON is newly authored static-derived behavioral data. No public-source
or dependency package is approved or included. Independent local sharing and
sanitization review passed for this scope. Revision 1 is the first release; no
prior release is superseded. See [the review disposition](REVIEW.md).
