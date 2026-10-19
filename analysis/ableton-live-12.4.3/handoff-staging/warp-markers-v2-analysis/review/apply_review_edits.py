"""Reviewer's text edits to the warp-markers-v2 payload (analyst side; never shipped).

usage: python3 -I -B apply_review_edits.py [PACKAGE_DIR]   (run after build_v2.py build)
README.md, spec.md and AGENTS.md are the author's hand-written texts; a file that already carries the reviewed
status line is left alone. cases.json is rebuilt by build_v2.py and only its status is set here. Findings:
RVW2-01 (devices; case 018, REQ-001 clause 2 and REQ-004 withdrawn), RVW2-02 (REQ-009 unreleased), RVW2-03
(extracted-execution label), RVW2-04 (assumption 8), RVW2-05 (combined failures of an add), RVW2-07 (status).
"""
import json, sys
from pathlib import Path

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
PKG = Path(ARGS[0]).resolve() if ARGS else Path(__file__).resolve().parents[2] / "warp-markers-v2"
SENTINEL = {"README.md": "**Reviewed local release.**", "AGENTS.md": "This is a reviewed local release",
            "spec.md": "**Status: reviewed local release**"}


def edit(name, pairs):
    p = PKG / name
    t = p.read_text()
    if SENTINEL[name] in t:
        print(name, "already reviewed; unchanged")
        return
    for old, new in pairs:
        assert t.count(old) == 1, (name, old[:90])
        t = t.replace(old, new)
    p.write_text(t)


edit("README.md", [
    ("""**Unreviewed candidate.** Read [the contract](spec.md), [the cases](cases.json),
[the role instructions](AGENTS.md) and [the manifest](manifest.json). No
separate review has approved this package yet, and it is not an implementation
input until it is released. A fresh, restricted implementation workspace would
then still be required; this package does not provision one.""",
     """**Reviewed local release.** Read [the contract](spec.md),
[the cases](cases.json), [the role instructions](AGENTS.md),
[the manifest](manifest.json) and [the review disposition](REVIEW.md). The
stated partial scope, narrowed as recorded in the review, is approved as a
contract for a fresh, restricted implementation workspace. Such a workspace
has not been provisioned by this release."""),
    ("""The finite scope is how a decoded Live Set stores the warp markers and warp
settings of an audio clip, and the marker list of a Simpler sample: where they
are, how their text is read when a document is opened, the defaults of absent
settings and the stored codes. It also covers what the scripting interface's
conversions between sample time and beat time return for a warped clip, and
which edits of warp markers through the scripting interface are refused or
accepted, including the exact binary64 arithmetic at the edges of the edit
limits and of the beat grid. One statement is added about playback: a session
clip that is not warped does not use its warp markers. Requirement IDs are
retained with explicit partial clauses. Requirements 005, 006 and 014 are not
released, and 009 is released only as that statement. Nothing that is saved,
played or heard is graded.""",
     """The finite scope is how a decoded Live Set stores the warp markers and warp
settings of an audio clip: where they are, how their text is read when a
document is opened, the defaults of absent settings and the stored codes. It
also covers what the scripting interface's conversions between sample time and
beat time return for a warped clip, and which edits of warp markers through the
scripting interface are refused or accepted, including the exact binary64
arithmetic at the edges of the edit limits and of the beat grid. Requirement
IDs are retained with explicit partial clauses. Requirements 004, 005, 006, 009
and 014 are not released. Nothing that is saved, played or heard is graded,
and no device is part of the release."""),
    ("""The package has 64 cases over 21 XML documents""", """The package has 63 cases over 20 XML documents"""),
    ("""although 35 of their cases expect them to open (change 1). Within
warp-markers-v1's scope, both releases give the same expectations. Its 38 case
records are carried unchanged, with the same IDs and fixture names, and 26
cases are new, for 64 in total. [The manifest](manifest.json) records the
relationship and the superseded manifest digest.""",
     """although 35 of their cases expect them to open (change 1). Case
WARP-MARKERS-018 is withdrawn and has no expectation (change 11); do not use it
either. For every other case and clause of warp-markers-v1, both releases give
the same expectations. Its other 37 case records are carried unchanged, with
the same IDs and fixture names, and 26 cases are new, for 63 in total.
[The manifest](manifest.json) records the relationship and the superseded
manifest digest."""),
    ("""   - the rest of the base set: a MIDI track with a two-note MIDI clip and an
     instrument, a return track, one send per track mixer, the main and cue
     tracks, two scenes, the transport, the set-level values and the automation
     target identifiers. The audio track's identifier is now 2 (it was 0) and
     its second clip slot is empty;""",
     """   - the rest of the base set: a MIDI track with a two-note MIDI clip, a
     return track, one send per track mixer, the main and cue tracks, two
     scenes, the transport, the set-level values and the automation target
     identifiers. Every device list is empty. The audio track's identifier is
     now 2 (it was 0) and its second clip slot is empty;"""),
    ("""   | `simpler-empty-markers.xml` | A Simpler replaces the MIDI track's instrument; its sample part is the warp-markers-v1 one, and it also has the base set's `On` parameter. Unlike warp-markers-v1, the document also holds the clip, and the MIDI track's identifier is 1 (it was 0) | 018 |
""", ""),
    ("""8. **REQ-WARP-MARKERS-009** is partly released, as one statement without a
   case: a session audio clip that is not warped does not use its warp markers
   when it plays.""",
     """8. **REQ-WARP-MARKERS-009** stays unreleased, as in warp-markers-v1: no case
   of this release can observe playback."""),
    ("""The stated assumptions now
   also cover the base set opening, the sample rate and the arm64 build.""",
     """The stated assumptions now
   also cover the base set opening, the sample rate, the marker list a
   conversion uses and the arm64 build."""),
    ("""10. **Exclusions.** The fixtures' context, the structure rules that decide
    whether a Live Set opens, and how a document finds its sample are newly
    excluded. Conversion values, the cases named in changes 3, 4 and 7, and
    the three uncertainty bands are no longer excluded.
11. **Unchanged.** Every other clause, the 38 carried case records and the WAV
    are as in warp-markers-v1.""",
     """10. **Exclusions.** The fixtures' context, the structure rules that decide
    whether a Live Set opens, how a document finds its sample, devices and
    the sample parts of a Sampler or Simpler are newly excluded. Conversion
    values, the cases named in changes 3, 4 and 7, and the three uncertainty
    bands are no longer excluded.
11. **Withdrawn.** WARP-MARKERS-018, and with it REQ-WARP-MARKERS-001 clause 2
    and REQ-WARP-MARKERS-004. Its document needs a Simpler in the MIDI track's
    device list, and whether the target build accepts a device there is not
    established. `simpler-empty-markers.xml` is removed, and no fixture holds a
    device.
12. **Unchanged.** Every other clause, the 37 carried case records and the WAV
    are as in warp-markers-v1."""),
])

edit("AGENTS.md", [
    ("""This is an unreviewed candidate for a local release. It is not an
implementation input until a separate review approves and publishes it.
Application implementation then requires a fresh, restricted implementation
workspace that contains only permitted materials. Publication of this package
does not provision one. Do not begin clean implementation in an analyst
checkout.""",
     """This is a reviewed local release for its explicit partial scope. Application
implementation requires a fresh, restricted implementation workspace that
contains only permitted materials. Publication of this package does not
provision one. Do not begin clean implementation in an analyst checkout."""),
])

edit("spec.md", [
    ("""**Status: unreviewed candidate.** No separate review has approved this
contract yet. It is not an implementation input until it is released.""",
     """**Status: reviewed local release**, approved with listed narrowing. A separate
review approved the clauses below, narrowed as recorded in
[the review disposition](REVIEW.md)."""),
    ("""sample with a position in beats. Each sample of a Simpler carries a marker list
of the same kind. For one document format version, this contract describes:""",
     """sample with a position in beats. For one document format version, this
contract describes:"""),
    ("""- which edits of warp markers through the scripting interface are refused, and
  which are accepted;
- one statement about playback: a session clip that is not warped does not use
  its warp markers.""",
     """- which edits of warp markers through the scripting interface are refused, and
  which are accepted."""),
    ("""after an accepted edit, editing in the user interface, how a refused document
is reported, or the structure rules that decide whether a Live Set opens.""",
     """after an accepted edit, editing in the user interface, how a refused document
is reported, devices and the sample parts of a Sampler or Simpler, or the
structure rules that decide whether a Live Set opens."""),
    ("""  beat bounds that decide the outcome. The code ran on a Linux x86_64 host,
  outside the application, with the host's C library in place of the macOS
  system libraries. The macOS arm64 build is inferred to compute the same
  values. Opening, the call's other checks and the sample rate are
  static-derived.""",
     """  beat bounds that decide the outcome. For a conversion, that code computed
  the step between seconds and beats. The division of a position in frames by
  the sample rate, and the multiplication of a result by it, are
  static-derived; for every case with this label they are exact. The grid
  rounding ran in another part of the original program that rounds a beat
  with the same operations as the add and the marker lookup (static-derived).
  The code ran on a Linux x86_64 host, outside the application, with the
  host's C library in place of the macOS system libraries. The macOS arm64
  build is inferred to compute the same values. Opening, the comparisons of
  the deciding values, the call's other checks and the sample rate are
  static-derived."""),
    ("""1. the base set opens in the target build; its structure follows static-derived
   rules, which assume that a MIDI track's device list accepts the base set's
   instrument (in case WARP-MARKERS-018, the Simpler) and an audio track's
   device list its effect;""",
     """1. the base set opens in the target build; its structure follows static-derived
   rules, and its device lists are empty;"""),
    ("""7. the macOS arm64 build computes the conversions, the grid rounding and the
   beat bounds with the same binary64 operations as the x86_64 build.""",
     """7. the macOS arm64 build computes the conversions, the grid rounding and the
   beat bounds with the same binary64 operations as the x86_64 build;
8. a conversion made right after opening uses the marker list held after
   opening."""),
    ("""  transport and the set-level values. The MIDI track holds a MIDI clip of two
  notes and an instrument. The audio track's first clip slot holds the clip;
  its second slot is empty. Each audio and MIDI track has two clip slots and
  two empty freeze slots, and each track mixer has one send. The base set's
  structure is static-derived""",
     """  transport and the set-level values. The MIDI track holds a MIDI clip of two
  notes. Every device list is empty. The audio track's first clip slot holds
  the clip; its second slot is empty. Each audio and MIDI track has two clip
  slots and two empty freeze slots, and each track mixer has one send. The
  base set's structure is static-derived"""),
    ("""- The **sample part** of case WARP-MARKERS-018 is the only
  `SampleWarpProperties` element, at
  `Tracks/MidiTrack/DeviceChain/DeviceChain/Devices/OriginalSimpler/Player/MultiSampleMap/SampleParts/MultiSamplePart/SampleWarpProperties`.
  In that fixture a Simpler is the MIDI track's instrument.
""", ""),
    ("""- **Held after opening** means the values the clip or sample part holds once
  the document has been read.""",
     """- **Held after opening** means the values the clip holds once the document
  has been read."""),
    ("""2. A Sampler or Simpler sample stores a marker list of the same form, a
   `WarpMode`, the same eight settings and an `IsWarped` in
   `SampleWarpProperties`, a child of each `MultiSamplePart`.""",
     """2. Not released: how a Sampler or Simpler sample stores its warp state."""),
    ("""### REQ-WARP-MARKERS-004: empty marker list of a sample part (partial)

1. An empty `WarpMarkers` element (`<WarpMarkers />`) in
   `SampleWarpProperties` does not refuse the document. The sample part's
   marker list is empty after opening.

""", ""),
    ("""### REQ-WARP-MARKERS-009: playback of a clip that is not warped (partial, statement only)

1. A session audio clip whose `IsWarped` is `false` does not use its warp
   markers when it plays: its marker list has no effect on which positions of
   its sample it plays (static-derived). No case judges this clause, because it
   is observable only through playback, which this release does not grade. How
   such a clip plays, how a warped clip plays, and arrangement clips are
   outside this release.

""", ""),
    ("""Every case breaks at most one rule. A document or call that breaks more than
one rule of this release has no expectation.""",
     """Every case breaks at most one rule, with one exception: an `add_warp_marker`
call is refused for the first check of REQ-WARP-MARKERS-015 clauses 1 to 5 that
fails, whatever the later checks would give (the calls of WARP-MARKERS-023 to
027 also lie outside the beat bounds). Any other document or call that breaks
more than one rule of this release has no expectation."""),
    ("""[cases.json](cases.json) lists 64 cases.""",
     """[cases.json](cases.json) lists 63 cases. The identifier WARP-MARKERS-018 is
not used: that case of warp-markers-v1 is withdrawn
([README](README.md#supersession))."""),
    ("""under `AudioClip` (the clip) or `SampleWarpProperties` (the sample part). Each key""",
     """under `AudioClip` (the clip). Each key"""),
    ("""Requirements not released: **REQ-WARP-MARKERS-005** (one-marker, out-of-order
and equal-time audio clip marker lists), **REQ-WARP-MARKERS-006** (missing or
`Invalid` marker times) and **REQ-WARP-MARKERS-014** (codes and settings
outside their codes or ranges on load). **REQ-WARP-MARKERS-009** is released
only as the statement of its clause 1.""",
     """Requirements not released: **REQ-WARP-MARKERS-004** (empty marker lists),
**REQ-WARP-MARKERS-005** (one-marker, out-of-order and equal-time audio clip
marker lists), **REQ-WARP-MARKERS-006** (missing or `Invalid` marker times),
**REQ-WARP-MARKERS-009** (playback) and **REQ-WARP-MARKERS-014** (codes and
settings outside their codes or ranges on load). Clause 2 of
REQ-WARP-MARKERS-001 is not released."""),
    ("""- children of `AudioClip` or `SampleWarpProperties` other than those the
  fixtures carry, a child order other than the fixtures', and repeated
  children;""",
     """- children of `AudioClip` other than those the fixtures carry, a child order
  other than the fixtures', and repeated children;"""),
    ("""  children of REQ-WARP-MARKERS-001 clause 1 and the sample part's children,
  including the clip's sample reference, and the WAV file;""",
     """  children of REQ-WARP-MARKERS-001 clause 1, including the clip's sample
  reference, and the WAV file; any device in a device list, including a
  Sampler or Simpler and its sample parts (every device list of the fixtures
  is empty);"""),
    ("""- an audio clip whose marker list is empty, and what the user sees for any
  refused document;""",
     """- an empty marker list, in an audio clip or in a sample part, and what the
  user sees for any refused document;"""),
    ("""- which sample position plays at a given beat for a warped clip; how a clip
  that is not warped plays, beyond REQ-WARP-MARKERS-009 clause 1; arrangement
  clips; the audio output of every warp mode and setting;""",
     """- playback: which sample position plays at a given beat, whether a clip that
  is not warped uses its warp markers, and arrangement clips; the audio output
  of every warp mode and setting;"""),
    ("""- the warp mode a new or loaded clip or sample part gets when `WarpMode` is
  absent, and any default warp mode preference; defaults of sample-part
  settings;""",
     """- the warp mode a new or loaded clip gets when `WarpMode` is absent, and any
  default warp mode preference;
- Sampler and Simpler sample parts: how they store warp state, their marker
  lists, codes, settings and defaults; any device in a device list;"""),
    ("""All 21 XML fixtures""", """All 20 XML fixtures"""),
    ("""list is the base list. Each clip fixture is the base set, or the base set with
the one change that its case purpose states. The sample-part fixture is the
base set with a Simpler as the MIDI track's instrument, whose
`SampleWarpProperties` holds an empty marker list, `WarpMode` 0, `IsWarped`
false, `TransientEnvelope` 100 and the setting values of REQ-WARP-MARKERS-010.""",
     """list is the base list. Each fixture is the base set, or the base set with the
one change that its case purpose states. Every device list is empty."""),
    ("""Review
status is recorded in [the manifest](manifest.json).""",
     """Review
status is recorded in [the manifest](manifest.json) and
[the review disposition](REVIEW.md)."""),
])

p = PKG / "cases.json"
d = json.loads(p.read_text())
d["status"] = "released-reviewed"
p.write_text(json.dumps(d, indent=1, ensure_ascii=True) + "\n")
print("payload edits applied")
