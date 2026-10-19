"""Apply the reviewer's payload edits to the mixer-values-v2 staging copy (analyst side; never shipped).

usage: python3 -I -B apply_review_edits.py      (idempotent; run before finalize_manifest.py)
Text edits only: status lines, the REQ-005 round-trip claim, REQ-013 and REQ-014 wording, the exclusion paragraph,
the scene description and the change-list cue-track exception. No case record, fixture or expectation changes
(cases.json changes only in its top-level status string).
"""
from pathlib import Path

PKG = Path(__file__).resolve().parents[2] / "mixer-values-v2"


def swap(name, old, new):
    p = PKG / name
    t = p.read_text()
    if new in t:  # already applied
        return
    assert t.count(old) == 1, (name, old[:60])
    p.write_text(t.replace(old, new))


swap("README.md", """**Staged candidate; not reviewed; not released.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md) and
[the manifest](manifest.json). This package is not an implementation input
until a separate review approves it and it is published.""",
     """**Reviewed local release.** Read [the contract](spec.md), [cases](cases.json),
[role instructions](AGENTS.md), [the manifest](manifest.json) and
[the review disposition](REVIEW.md). The stated partial scope, with the
narrowing recorded in the review, is approved as a contract for a fresh,
restricted implementation workspace. Such a workspace has not been provisioned
by this release.""")

swap("README.md", """   - each track gains `Name`, `Color`, `AutomationEnvelopes` (empty, except
     the main track's tempo and time-signature envelopes), `TrackGroupId` −1
     (not on the main track) and `AudioOutputRouting`;""",
     """   - each track except the cue track gains `Name`, `Color`,
     `AutomationEnvelopes` (empty, except the main track's tempo and
     time-signature envelopes), `TrackGroupId` −1 (not on the main track) and
     `AudioOutputRouting`;""")

swap("AGENTS.md", """This is a staged, unreviewed handoff candidate. It is not an implementation
input. Only a release that a separate review approved and published may be used
for implementation, in a fresh, restricted implementation workspace that
contains only permitted materials. Do not begin clean implementation in an
analyst checkout.""",
     """This is a reviewed local release for its explicit partial scope. Application
implementation requires a fresh, restricted implementation workspace containing
only permitted materials. Publication of this package does not provision one.
Do not begin clean implementation in an analyst checkout.""")

swap("spec.md", """**Status: staged candidate; not reviewed; not released.** Do not implement from
it. A separate review must approve it first.""",
     """**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).
Implementation requires a fresh, restricted implementation workspace.""")

swap("spec.md", """  exactly. This does not hold for every gain: between −6 dB and 0 dB on the
  volume curve there are about 2.5 million binary32 positions for about 8.4
  million binary32 gains, so most gains between curve points cannot return
  unchanged. Other gains have no round-trip expectation.""",
     """  exactly. This does not hold for every gain. On the volume curve, from the
  point at position 0.7 (about −6 dB) to the point at 0.85 (0 dB), there are
  about 8.4 million binary32 gains but only about 2.5 million binary32
  positions, so most gains in that range cannot return unchanged. Other gains
  have no round-trip expectation: neither an exact return nor a bound on the
  difference is released.""")

swap("spec.md", """  to four binary32 gains. With θ(x) = (x + 1)·π/4:""",
     """  to four binary32 gains named L→L, L→R, R→L and R→R. With
  θ(x) = (x + 1)·π/4:""")

swap("spec.md", """  Output left = L→L·input left + R→L·input right, and output right =
  L→R·input left + R→R·input right. The formula is static-derived. The
  original program's code for it was run by extracted execution at the inputs
  of the cases, and every result agrees with it within the comparison.
- Consequences: with w = 0 the pan is a balance control without cross-feed;
  at p = −1, L→L is √2 (+3.01 dB) and R→R is 10^−5 (−100 dB), not 0. With
  w = 1 and split pans −1 and 1 the matrix is the identity; with split pans 0
  and 0 every gain is 0.7071068 (−3.01 dB). With v = 0 every gain is 0.
- The original computes the cosines in binary64. Where the formula gives 0 at
  a quarter turn, it gives about 6·10^−17 instead (MIXER-VALUES-070); the
  comparison absorbs this.""",
     """  The names are labels for the four computed values. Which signal each gain
  scales, and whether, where and when the audio path applies the gains, are
  not released. The formula is static-derived. The original program's code
  for it was run by extracted execution at the inputs of the cases, and every
  result agrees with it within the comparison.
- Consequences: with w = 0, L→R and R→L are 0; at p = −1, L→L is √2
  (+3.01 dB) and R→R is 10^−5 (−100 dB), not 0. With w = 1 and split pans −1
  and 1, L→L and R→R are 1, and L→R and R→L are 0 within the comparison; with
  split pans 0 and 0 every gain is 0.7071068 (−3.01 dB). With v = 0 every gain
  is 0.
- In MIXER-VALUES-070 the original gives about 6·10^−17 for L→R and R→L,
  where the formula gives 0. The comparison's bound of 10^−12 absorbs this.""")

swap("spec.md", """  REQ-MIXER-VALUES-009 has a level T_c(x), a binary32 value, at a curve
  position x from −1 to 1. MIXER-VALUES-074 to 080 list each curve's level at
  x = −1, −0.5, −0.25, 0, 0.25, 0.5 and 1.""",
     """  REQ-MIXER-VALUES-009 gives a level T_c(x), a binary32 value, at each of the
  curve positions x = −1, −0.5, −0.25, 0, 0.25, 0.5 and 1. MIXER-VALUES-074
  to 080 list these levels. No level is released for any other position, and
  the listed levels do not define one, for example by interpolation.""")

swap("spec.md", """Parts of released requirements that are not released: in REQ-MIXER-VALUES-005,
any binding of the curves to faders, controls or audio, and inputs other than
those of the cases; in REQ-MIXER-VALUES-013, the inputs the audio path supplies,
ramps, other inputs, and the application to audio; in REQ-MIXER-VALUES-014,
levels at other positions, the crossfader and assignment mapping, ramps and the
application to audio.""",
     """Parts of released requirements that are not released: in REQ-MIXER-VALUES-005,
any binding of the curves to faders, controls or audio, inputs other than
those of the cases, and the round trip of other gains; in
REQ-MIXER-VALUES-013, the inputs the audio path supplies, ramps, other inputs,
which signal each gain scales, and the application to audio; in
REQ-MIXER-VALUES-014, levels at other positions, the crossfader and assignment
mapping, ramps and the application to audio.""")

swap("spec.md", """- `Scenes`, with two scenes (`Id` 0 and 1, named `Scene 1` and `Scene 2`,
  colour −1, tempo 120 and time signature 201, both disabled).""",
     """- `Scenes`, with two scenes (`Id` 0 and 1, named `Scene 1` and `Scene 2`,
  colour −1, tempo 120 and time signature 201, both disabled, and a follow
  action that is not enabled).""")

swap("spec.md", """approved or included. Review status is recorded in
[the manifest](manifest.json).""",
     """approved or included. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).""")

swap("README.md", "When published, this release supersedes mixer-values-v1, which stays",
     "This release supersedes mixer-values-v1, which stays")

swap("cases.json", '"status": "staged candidate; not reviewed; not released",', '"status": "released-reviewed",')
print("edits applied")
