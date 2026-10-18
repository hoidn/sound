# MIDI configuration interpretation and value transforms, release 3

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace has
not been provisioned by this release.

The finite scope is how a user configuration file is interpreted: which
assignments are enabled, their MIDI addresses, the device, mixer, transport and
drum-pad targets they name, map-mode labels, button kinds and the device
parameter bank span. New in this release is the parameter value that each
Control Change message produces on an assigned continuous control, in each of
the ten map modes. Takeover is specified only for the choice under which it
never acts and for the values exempt from it. On/off parameters, Pick-Up,
Value Scaling and value timing are excluded. Existing requirement IDs are
retained with explicit partial clauses. Requirements 001 and 004 and every
other runtime effect remain unreleased. No application source, shipped file or
public dependency is included.

All expected outputs are static-derived and unexecuted, not captured reference
behavior. The representation is a comparison convention, not an API claimed to
exist in Live or a required architecture. No compatibility claim is made.
After publication the release is immutable; corrections require a new revision.

## Supersession

This release supersedes midi-config-v2 as a strict superset.
midi-config-v2 stays immutable and valid for its narrower scope. Its 109 cases
keep their IDs, records and fixture bytes; 18 value cases are new, for 127 in
total. [The manifest](manifest.json) records the relationship and the
superseded manifest digest.

## Changes from midi-config-v2

1. REQ-MIDI-USER-005 gains the value transforms: `Absolute`, `Absolute14Bit`
   pairing, the eight relative decode tables and step rules, rounding on
   stepped parameters, the takeover choice `none` and the values exempt from
   takeover.
2. REQ-MIDI-USER-010 gains master, cue and crossfader values, with the
   crossfader's `Absolute` values exempt from takeover.
3. The midi-config-v2 exclusion of numeric transforms, 14-bit pairing, relative
   arithmetic, pickup and takeover narrows to the value exclusions listed in
   the contract.
4. Value cases add a `stimulus` (takeover, parameter, messages) and
   `expected.values`. The other case fields are unchanged.
5. Cases MIDI-CONFIG-110 to 127 are new value cases.
6. Every midi-config-v2 clause, case and fixture is carried unchanged, and
   nothing in midi-config-v2 is contradicted. The sentences that left value
   behavior unspecified, in the contract summary, REQ-MIDI-USER-005,
   REQ-MIDI-USER-010 and the exclusions, now point to the new section.
