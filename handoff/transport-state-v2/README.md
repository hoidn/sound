# Transport state in Live Set documents, release 2

**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, with the
clarifications recorded in the review, is approved as a contract for a fresh,
restricted implementation workspace. Such a workspace has not been provisioned
by this release.

The finite scope is the same as in transport-state-v1. It covers how the decoded
XML of one Live Set format version stores six values: the arrangement loop
switch, loop start, loop length, playback position, tempo and time-signature
code. For each it states where the value is, which text is accepted or refused
when a document is opened, what missing, duplicated and unknown items do, and
the exact text written on save. Existing requirement IDs are retained with
explicit partial clauses. Requirements 009 and 012 and every runtime effect
remain unreleased. No application source, shipped file or public dependency is
included.

The 33 cases use independently authored minimal XML fixtures. Each expected
output is labeled static-derived or extracted execution, as defined in the
contract. None is captured reference behavior. The representation is a
comparison convention, not an API claimed to exist in Live or a required
architecture. No compatibility claim is made. After publication the release is
immutable; corrections require a new revision.

## Supersession

This release supersedes transport-state-v1. transport-state-v1
stays immutable. It remains valid for its own scope, but its REQ-011 rule should
not be reused outside that scope (change 1). Its 18 cases keep their IDs,
records and fixture bytes, and 15 cases are new, for 33 in total.
[The manifest](manifest.json) records the relationship and the superseded
manifest digest.

## Changes from transport-state-v1

1. **REQ-011 step 1 corrected.** transport-state-v1 takes k from the exact
   base-10 logarithm. The original program takes it from its binary64
   logarithm, stated here as the logarithm rounded to the nearest binary64 value
   outside the band of change 5. The two differ only for binary64 values just above
   a power of ten 10ⁿ (n ≥ 1) or just below 10⁻ⁿ, for example 1000.0000000000001
   and 0.000001. transport-state-v1 gave no expectation for those values, so none
   of its cases is affected. The rule is now stated exactly. TS-024 to TS-027 are
   new cases.
2. **Negative zero.** REQ-011 writes negative zero as `-0`, and REQ-004 reads
   `-0` as negative zero. The transport-state-v1 exclusion of negative zero is
   removed. TS-028 is new.
3. **Time-signature text (REQ-006).** The rule is restated as five conditions:
   sign, spaces, length and range. Spellings that transport-state-v1 excluded are
   now decided: spaces on both sides, a `+` with trailing spaces, a `-` sign, and
   text longer than 63 characters that ends in a space. TS-010 and TS-029 to
   TS-033 are new. An accepted code outside 0 to 494 still has no expectation.
   transport-state-v1 gave no expectation for opening a document whose code is
   not 201; TS-030 now judges only that a document with code 0 (text `-0`)
   opens. Whether a code other than 201 takes effect stays excluded.
4. **`#` forms (REQ-004, REQ-005).** The `#` form with exactly 16 (tempo: 8)
   hexadecimal digits of either case reads as raw bits, most significant digit
   first. Other text starting with `#` is refused. That exclusion is removed.
   TS-034 to TS-037 are new; TS-034 and TS-035 exercise the existing sign and
   space reading.
5. **Exclusions.** The exclusion near integer logarithms is narrowed. Values
   whose logarithm lies within 1e-12 of an integer are no longer excluded; only
   values whose logarithm lies between 1/4 and 3/4 of a binary64 gap from an
   integer have no expectation. Accepted time-signature codes outside 0 to 494,
   which transport-state-v1 left without expectation through its value ranges,
   are now also listed as an exclusion.
6. **Provenance.** The extracted-execution label is new. Every new case carries
   it. Carried cases keep their records and the static-derived label. The
   contract states the assumptions the extracted-execution cases rest on.
7. **Unchanged.** Every other clause, case and fixture of transport-state-v1 is
   carried unchanged.
