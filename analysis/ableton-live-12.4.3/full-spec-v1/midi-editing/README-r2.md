# MIDI Interval case successor R2

Same43requirement rows,60cases: all57old case records remain verbatim and only
three Interval branches are appended. They exercise selected-note slider addition,
no-selection slider alone, and no-selection Add Interval for all original notes.
Existing MED011 only exercises Fit to Scale. The actual source distinction was
already in MIDI011; no new law or requirement ID is introduced.

`expected` and optional `comparator` remain legacy documentary proposal fields,
not original/target results. The added wrapper status explicitly describes all
current actual results as null/U/unexecuted, without pretending it was present in
old records. New rows also carry explicit actual-null fields. There are46D12 and
14Udocumentary cases, all60exact-target gradesU/not-run. The no-addition trial
requires a genuinely productive matched Add Interval button baseline, then an
original reset with actual no selection. Failed prerequisites remainU.

[Source context](source-context-r2.json) points to the retained exact raw query,
five complete Intervals/Humanize subsection records and two Clip paragraphs.
MIDI capture is date-only; queryUTC is not captureUTC. Humanize half-grid versus
quarter-before/after staysQ053. No total-span equivalence,RNG,NoteId/count,
clipping,repeat accumulation,codec,timing,default or generic button-selected law.
Original C1/C2/C3 and nonblocking R1 generator/Chop notes remain open.

All11old files, including old validation report and manifest, remain exact.
[Prior hashes](prior-files-r2.json),[delta](delta-r2.json),[before spec](spec-before-r2.md)
and[before research](research-before-r2.md) preserve those original identities.
Old manifest wiki entries are checked against exact before snapshots. No old
validator/consumer runs and no automatic historical adapter is added. The
[consumer inventory](consumer-impact-r2.json) is a finite hash-occurrence search,
including as-of/review/archive metadata; one actively authored ClipView input
file is explicitly as-of, not a mutable immutable-pin dependency.

Inspect `validate-r2.py`, then run from repository root:

```sh
python3 -B analysis/ableton-live-12.4.3/full-spec-v1/midi-editing/validate-r2.py --check
```

It verifies immutable sources, exact case-only delta, source/selection association,
five rejection fixtures, actual nulls, snapshot identities, exact Browser IDs,
local links and authored whitespace without writing. Source parser and four
Browser functions are inspected pure analyst helpers; vendor code never runs.
No original/UI/OS/tool/MIDI/audio/hardware/account/network/candidate operation ran.
**AS-OF AUTHOR FREEZE:** independent R2 review pending; the
[spec index](../../../../wiki/specs/index.md) owns current disposition. This is a
narrow partial case increment, not a whole MIDI source/owner review or completion.
