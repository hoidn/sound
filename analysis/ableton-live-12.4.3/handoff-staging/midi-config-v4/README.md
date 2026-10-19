# MIDI configuration interpretation and value transforms, release 4

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace has
not been provisioned by this release.

The finite scope is how a user configuration file is interpreted: which
assignments are enabled, their MIDI addresses, the device, mixer, transport and
drum-pad targets they name, map-mode labels, button kinds and the device
parameter bank span. It also covers the parameter value that each Control
Change message produces on an assigned continuous control, in each of the ten
map modes. New in this release are the Pick-Up and Value Scaling takeover
choices, reversed parameter ranges, the previous value of a 14-bit pair,
including the first pair after the input opens, and a value tolerance that
scales with the parameter's range. On/off parameters, the default takeover
choice and value timing are excluded. Existing requirement IDs are retained
with explicit partial clauses. Requirements 001 and 004 and every other runtime
effect remain unreleased. No application source, shipped file or public
dependency is included.

Each expected output is labeled static-derived or extracted execution, as
defined in the contract. None is captured reference behavior. The
representation is a comparison convention, not an API claimed to exist in Live
or a required architecture. No compatibility claim is made. After publication
the release is immutable; corrections require a new revision.

## Supersession

This release supersedes midi-config-v3. It carries every midi-config-v3 case
and clause and widens the scope, with two precision corrections to general
value clauses (changes 5 and 7): a value reached by several relative messages
in a row is compared within a tolerance that grows with their number, and a
stepped target value very close to a half-integer has no expectation. No
midi-config-v3 case is affected. Its 127 cases keep their IDs, records and
fixture bytes, and no expected value is corrected; 34 value cases are new, for
161 in total. midi-config-v3 stays immutable and valid for its own scope apart
from those two corrections. [The manifest](manifest.json) records the
relationship and the superseded manifest digest.

## Changes from midi-config-v3

1. **Takeover (REQ-MIDI-USER-005).** The `pick-up` and `value-scaling` choices
   are specified, with the record of previous data values, the previous value
   of a 14-bit pair, the sorted bounds and inclusive comparisons. The three
   choices are named `none`, `pick-up` and `value-scaling` and are selected by
   their entry's position in the preference. midi-config-v3 specified only
   `none` and the values exempt from takeover.
2. **Choice labels.** midi-config-v3 assumed that its `none` choice is the
   entry labelled None, inferred from the order of the entries. Which entry
   selects which choice is now static-derived. Only the displayed wording
   remains an assumption.
3. **Reversed ranges.** midi-config-v3 required *min* < *max*; now *min* ≠
   *max* is required. The `Absolute`, `Absolute14Bit` and relative rules and
   takeover hold for either order, and a stepped relative step moves toward
   *max* when *d* > 0, which is down for a reversed range. For *min* < *max*
   the rules are unchanged.
4. **Crossfader pairs (REQ-MIDI-USER-010).** Completed `Absolute14Bit` pairs of
   the crossfader are subject to takeover. midi-config-v3 gave them no
   expectation under the other two choices.
5. **Tolerance.** Values compare within τ = max(1e-6, 2⁻²² × max(|min|,
   |max|)) instead of 1e-6. τ is 1e-6 for every midi-config-v3 case, so no
   carried comparison changes. Rounding adds up over relative messages in a
   row on a parameter that is not stepped, so a value reached by *k* of them
   is compared within *k* × τ. Each step of the carried relative cases is
   exact in single precision, so their comparison is unchanged.
6. **Rounding.** A Value Scaling move is not rounded, even for a stepped
   parameter. Every other target value of a stepped parameter is rounded as
   before. A stepped parameter's value after a move has no expectation.
7. **Exclusions.** Removed: values subject to takeover under the choices other
   than `none`, and *min* above *max*. *min* equal to *max* stays excluded.
   Added: results near a bound, stepped target values near a half-integer and
   Value Scaling moves outside the listed cases, with the later values of
   their sequences, and anything that empties the record of previous data
   values. The stepped exclusion narrows the midi-config-v3 rounding rule,
   which gave such values an expectation; no midi-config-v3 case lies near a
   half-integer. The default choice stays excluded; the
   displayed wording of the choices and any takeover notification are now
   listed.
8. **Provenance.** The extracted-execution label is new, and every new case
   carries it. Carried cases keep their records and the static-derived label.
   The contract states the assumptions that the value cases rest on and the
   parts of the original code that did not run.
9. **Representation.** `takeover` gains `pick-up` and `value-scaling`. The
   initial value is stated to be a binary32 number. The values note and each
   new case's comparator state τ.
10. **Comparison obligations.** A reference comparison selects each case's
    choice by its entry's position and records the entry's wording, instead
    of confirming that the `none` choice is the one under which takeover
    never acts. The rule for a crossfader that reports another range now
    also covers MIDI-CONFIG-150.
11. **Cases.** MIDI-CONFIG-128 to 161 are new value cases.
12. **Unchanged.** Every other clause, case and fixture of midi-config-v3 is
    carried unchanged. Apart from the two precision corrections in changes 5
    and 7, nothing in midi-config-v3 is contradicted or narrowed. The
    sentences that left takeover unspecified now point to the new rules.
