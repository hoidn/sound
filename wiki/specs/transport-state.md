---
id: SPEC-TRANSPORT-STATE
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3 / macOS arm64
---

# Transport state in Live Set documents

## Scope

Feature FEAT-TRANSPORT, with FEAT-PERSISTENCE, in the [feature map](feature-map.md).
User task: open a Live Set whose song tempo, time signature, arrangement loop
switch, loop start, loop length and playback position are stored in the document,
and save them back. This draft specifies how those six values are located in the
document, which value text is accepted, what a missing, duplicated or unknown item
does, how values are written on save, and the time-signature code.

Every requirement is a **proposed contract** supported by a static derivation, or
explicitly unknown. Nothing was run against Live.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a static-first
draft. Target: 12.4.3 arm64, documents with `MinorVersion="12.0_12402"`. The
gzip/XML envelope and root attributes belong to the draft
[SPEC-ALS-CONTAINER](als-container.md), a dependency of this spec. All document examples are fragments of the
decoded XML.

Excluded: older document versions and their migration, clip loop fields (same tag
names, different path), edits after load (UI, API or MIDI), scene launching,
playback, timing, undo, MIDI mapping of transport controls (`*KeyMidi`), Link and
external sync, and the exact text of error dialogs.

## Evidence labels

| Label | Meaning |
| --- | --- |
| D | Documented in a shipped manual or document. No clause in this revision is D |
| S | Static derivation from the 12.4.3 executable or shipped bytes; not an observed run |
| U | Unknown; no expected result. PRB IDs name the Phase 4 probe that would settle it |

Only S clauses may enter a release. U clauses block the behavior they name.

"The set does not open" means the document reader stops with a read error. The
container draft derives that such errors surface as the corrupt-document failure
class. How Live presents it is U
([REQ-ALS-CONTAINER-009](als-container.md#req-als-container-009--failure-presentation-and-state)).

## Requirements

### REQ-TRANSPORT-STATE-001 — field locations

- **S.** Below `/Ableton/LiveSet`, the six values are:
  `Transport/LoopOn/@Value` (Boolean), `Transport/LoopStart/@Value`,
  `Transport/LoopLength/@Value` and `Transport/CurrentTime/@Value` (64-bit
  floating point, arrangement time in beats),
  `MainTrack/DeviceChain/Mixer/Tempo/Manual/@Value` (32-bit floating point, beats
  per minute) and `MainTrack/DeviceChain/Mixer/TimeSignature/Manual/@Value`
  (integer code, REQ-010).
- **S.** The same tag names elsewhere (clip `Loop`, scenes, Simpler, grooves) are
  different fields. Only these paths carry the song transport state.
- **U.** The beat unit of the loop fields and the BPM unit of tempo are inferred
  from shipped files, not traced in code.

### REQ-TRANSPORT-STATE-002 — element shape and order on save

- **S.** Each `Transport` child is written as an empty element carrying exactly one
  `Value` attribute, for example `<LoopOn Value="false" />`. `Tempo` and
  `TimeSignature` write `Manual` the same way.
- **S.** `Transport` children are written in this order, each only if present:
  `PhaseNudgeTempo`, `LoopOn`, `LoopStart`, `LoopLength`, `LoopIsSongStart`,
  `CurrentTime`, `PunchIn`, `PunchOut`, `MetronomeTickDuration`, then any of the 23
  `*KeyMidi` children in schema order, then `DrawMode`.
- **U.** When a `*KeyMidi` child is written (believed to be: only when a key or
  MIDI assignment exists), whitespace and indentation, and whether the
  one-event tempo and time-signature envelopes are always written: PRB-N1-07.

### REQ-TRANSPORT-STATE-003 — loop switch text on load

- **S.** `LoopOn/@Value` text `true` or `1` loads loop on. `false` or `0` loads
  loop off. Matching is exact and case-sensitive, with no whitespace trimming.
- **S.** Any other text, including `TRUE`, `True`, an empty string and ` true`,
  makes the set not open.

### REQ-TRANSPORT-STATE-004 — loop and position number text on load

Applies to `LoopStart`, `LoopLength` and `CurrentTime`.

- **S.** The value is the longest leading prefix that C `strtod` accepts. The load
  succeeds when at least one character is consumed. Leading whitespace is skipped,
  and text after the prefix is ignored (`4.5abc` loads 4.5). Exponent, hexadecimal
  floating forms, `inf` and `nan` are accepted.
- **S.** `Invalid` loads the largest finite double. `#` followed by exactly 16 hex
  digits (17 characters) loads those IEEE-754 bits.
- **S.** Text with no numeric prefix (`abc`, an empty string) makes the set not open.
- **U.** Whether a locale decimal comma is honored.

### REQ-TRANSPORT-STATE-005 — tempo text on load

- **S.** `Tempo/Manual/@Value` follows REQ-004, except that `#` takes exactly 8 hex
  digits (9 characters) and `Invalid` loads the largest finite float. The result
  is rounded to 32-bit float: `93.3333333` is held as 93.33333587646484.

### REQ-TRANSPORT-STATE-006 — time-signature code text on load

- **S.** `TimeSignature/Manual/@Value` loads when it is ASCII decimal digits
  preceded by any number of U+0020 spaces and then at most one `+`, with nothing
  after the digits (`201`, ` 201`, `+201`, `  +201`), or ASCII digits followed
  only by spaces (`201 `). The part after leading spaces and `+`, not counting
  trailing spaces, must be at most 63 characters (corrected in review RV1-01 of
  transport-state-v1: the parser's length check excludes trailing spaces).
- **S.** An empty or all-space value, any byte outside ASCII, a `+` followed by
  `-`, and `201.0`, `2e2` or `0x10` make the set not open.
- **U.** Spaces on both sides of the digits, or a `+` and trailing spaces
  (` 201 `, `+201 `, ` +201 `). The trailing spaces reach the digit conversion,
  which is not traced; the static reading is that the set does not open. No N1
  probe covers it; PRB-N2-06 (case N2-014, ` +5 `) tests the same spelling in an
  envelope integer.
- **U.** A `-` sign (`-1`): PRB-N1-06.

### REQ-TRANSPORT-STATE-007 — missing fields

- **S.** A missing `LoopOn`, `LoopStart`, `LoopLength` or `CurrentTime` element, or
  one without its `Value` attribute, loads the new-document value: loop off, start
  8, length 16, position 0. A missing `Tempo/Manual` element or its `Value` loads
  120. None of these makes the set fail to open.
- **U.** The time-signature value when `TimeSignature/Manual` is missing (4/4 is
  expected but not established): PRB-N1-04. Whether a user default-set template
  supplies values instead: PRB-N1-02.

### REQ-TRANSPORT-STATE-008 — duplicated and unknown items

- **S.** Two elements with the same name directly under `Transport` (or under
  `Tempo` or `TimeSignature`) make the set not open. A repeated attribute is
  malformed XML and also prevents opening.
- **S.** An unknown child element of `Transport` is skipped together with its
  content. The set opens and a later save does not write it.
- **S.** An unknown attribute on a transport element is ignored. The exception
  is a versioned read whose `SchemaChangeCount` equals the ChangeCount of the
  schema named by `MinorVersion`; then the set does not open. B0
  (`SchemaChangeCount="1"`, schema ChangeCount 5) is not in that case.
- **U.** Whether Live Sets are read in versioned mode, the `SchemaChangeCount` a
  12.4.3 save writes (PRB-N1-07), and the outcomes above as seen by the user:
  PRB-N1-08.

### REQ-TRANSPORT-STATE-009 — out-of-range numbers

- **S.** Well-formed numbers outside the usual ranges do not make the set fail to
  open. This covers negative loop start, loop length below 1, negative position,
  tempo outside 20–999 and time-signature codes outside 0–494.
- **S.** On load, loop end becomes loop start plus loop length.
- **U.** The values Live then uses, displays and writes on the next save, including
  any clamping to start ≥ 0, length ≥ 1 or tempo 20–999: PRB-N1-03, PRB-N1-06.

### REQ-TRANSPORT-STATE-010 — time-signature code

- **S.** The code for numerator n and denominator d is `(n − 1) + 99 × log2(d)`,
  with n in 1–99 and d in {1, 2, 4, 8, 16}. Valid codes are 0–494. Examples: 4/4 =
  201, 6/8 = 302, 7/8 = 303, 99/16 = 494.

### REQ-TRANSPORT-STATE-011 — number text on save

- **S.** Booleans are written `true` or `false`, and integers as plain decimal.
- **S.** For 64-bit fields (REQ-004) and 32-bit fields (REQ-005), let P = 17 or 9.
  Positive zero is written `0`. For a nonzero x:
  - take k = ⌈log10|x|⌉ when |x| ≥ 1 and ⌊log10|x|⌋ when |x| < 1;
  - print x in fixed notation with max(0, P − k) decimals (a 32-bit value is first
    widened exactly to 64 bits);
  - if the text contains `.`, remove trailing `0`s and then a trailing `.`.
- **S.** The largest finite value is written `Invalid`. A non-finite value is
  written `#` followed by its IEEE bits in uppercase hex (8 or 16 digits).
- Examples: 120 → `120`; float 121.2 → `121.199997`; float 93.3333333 →
  `93.3333359`; double 0.3 → `0.299999999999999989`; double 3.3 →
  `3.2999999999999998`; 1e20 → `100000000000000000000`.
- **U.** Negative zero (for example loaded from `-0`). It takes the zero path,
  and fixed-point printing keeps the sign, so `-0` is expected but not
  established.

### REQ-TRANSPORT-STATE-012 — precedence between stored tempo and meter sources

- **U.** Which value applies on load when `Manual` disagrees with its one-event
  envelope (`FloatEvent`/`EnumEvent` at `Time="-63072000"`), or when a scene has an
  enabled tempo or time signature: PRB-N1-04, PRB-N1-05. Until settled, fixtures
  keep the envelope event equal to `Manual` and all scene overrides disabled.

## Timing and state

- Units: arrangement time in beats (REQ-001, inferred); tempo in BPM (inferred).
  Tempo is held in 32-bit precision after load (REQ-005).
- Persistent state: only the six values above. Loop end is derived on load
  (REQ-009). Playback state, undo and live edits are out of scope.
- Determinism: reading and writing are deterministic for a given document.
  REQ-011 defines the exact save text, so comparisons can be byte-exact per
  attribute value.
- Edits after load (UI, API, MIDI) are out of scope. Static evidence suggests that
  controlled edits clamp loop start ≥ 0 and loop length ≥ 1, but no requirement is
  made.

## Acceptance cases

Base document B0: the shipped `Core Library/Lessons/Sets/Recording Audio.als`
(SHA-256 `af57ff8f9eb1c2c51220ef6633a58838532350d53640df5f48dc01659023c043`,
`MinorVersion="12.0_12402"`, `SchemaChangeCount="1"`). It is decoded, changed only
as stated, and re-encoded as gzip. Its transport is
`<LoopOn Value="false" />`, `<LoopStart Value="8" />`, `<LoopLength Value="16" />`,
`<CurrentTime Value="0" />`, tempo `<Manual Value="120" />` with
`<FloatEvent Id="0" Time="-63072000" Value="120" />`, and time signature
`<Manual Value="201" />`. All expectations are static derivations; none has been
run. Case kinds: P positive, N negative/malformed, B boundary, M missing, S save.

| Case ID | Requirement | Kind | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- |
| TS-001 | 003 | P | `<LoopOn Value="true" />`; open, save | Opens; loop switch on; saved `<LoopOn Value="true" />` | B0 edit |
| TS-002 | 003 | P | `<LoopOn Value="1" />`; open | Opens; loop on | B0 edit |
| TS-003 | 003 | P | `<LoopOn Value="0" />`; open | Opens; loop off | B0 edit |
| TS-004 | 003 | N | `<LoopOn Value="TRUE" />`; open | Set does not open | B0 edit |
| TS-005 | 003 | N | `<LoopOn Value="" />`; open | Set does not open | B0 edit |
| TS-006 | 004, 011 | B | `<LoopStart Value="4.5abc" />`; open, save | Opens; loop start 4.5; saved `<LoopStart Value="4.5" />` | B0 edit |
| TS-007 | 004 | N | `<LoopLength Value="abc" />`; open | Set does not open | B0 edit |
| TS-008 | 005, 011 | P | Tempo `<Manual Value="93.3333333" />` and `FloatEvent` `Value="93.3333333"`; open, save | Opens; saved Manual `93.3333359`, and the event `93.3333359` if written (REQ-002) | B0 edit |
| TS-009 | 006 | N | Time signature `<Manual Value="201.0" />`; open | Set does not open | B0 edit |
| TS-010 | 006 | B | Time signature `<Manual Value=" +201 " />`; open | Static reading strengthened by review: the digit converter accepts no whitespace, so the kept trailing spaces make the set fail to open; still excluded from transport-state-v1 until a later revision grades it | B0 edit |
| TS-011 | 007 | M | Delete the `LoopStart` element; open | Opens; loop start 8 | B0 edit |
| TS-012 | 007 | M | Replace with `<LoopLength />`; open | Opens; loop length 16 | B0 edit |
| TS-013 | 007 | M | Delete the `CurrentTime` and `LoopOn` elements; open | Opens; position 0; loop off | B0 edit |
| TS-014 | 007 | M | Tempo `<Manual />` (no Value); event stays 120; open | Opens; tempo 120 | B0 edit |
| TS-015 | 008 | N | Two `LoopOn` elements (`false` then `true`) in `Transport`; open | Set does not open | B0 edit |
| TS-016 | 008 | B | Add `<Foo Value="1" />` inside `Transport`; open, save | Opens; saved `Transport` has no `Foo` | B0 edit |
| TS-017 | 009 | B | `<LoopLength Value="-4" />`; open | Opens; effective and saved values unresolved | B0 edit |
| TS-018 | 009 | B | Tempo Manual and event `2000`; open | Opens; effective tempo unresolved | B0 edit |
| TS-019 | 009, 010 | B | Time signature Manual and `EnumEvent` `495`; open | Opens; effective meter unresolved | B0 edit |
| TS-020 | 011 | S | Tempo Manual and event `121.2`; open, save | Saved Manual `121.199997`, and the event `121.199997` if written (REQ-002) | B0 edit |
| TS-021 | 011 | S | `<LoopStart Value="0.3" />`; open, save | Saved `<LoopStart Value="0.299999999999999989" />` | B0 edit |
| TS-022 | 002 | S | Open B0 unchanged, save | Saved `Transport` children in the REQ-002 order; values unchanged | B0 |
| TS-023 | — | — | Withdrawn in revision 2: it edited the time signature in the UI, which is out of scope | Not graded | — |

Comparators: "opens" and "does not open" are judged by whether the set finishes
loading. Value comparisons are exact text for saved attributes, and an exact
displayed value (loop start/length in beats, tempo to the displayed precision) for
loaded state. Cases whose expectation says "unresolved" must not be graded as
passes. No case checks a valid REQ-010 code: its effect on load depends on
REQ-012 (PRB-N1-04), and edits are out of scope. Cancellation and teardown kinds
are omitted: reading and writing these fields has no cancellable step or resource
defined in this scope.

## Open questions

[Q-012](../questions.md#q-012-transport-state-load-and-save-semantics) holds the
open items:

- the user-visible read-error outcome;
- REQ-012 precedence;
- the effective values for REQ-009;
- the missing time-signature default (REQ-007);
- REQ-006 spellings with spaces on both sides or `+` and trailing spaces (TS-010),
  and the `-` sign;
- negative zero on save (REQ-011);
- the current `SchemaChangeCount` and the KeyMidi and envelope presence on save (REQ-002, REQ-008).

The [probe batch](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/probe-batch.json)
(PRB-N1-01–08) supplies a minimal input, a discriminating observation and a stop
condition for each.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is
[transport-state native](../research/transport-state-native.md) and
[transport-state static](../research/transport-state-static.md), with retained run
`analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/` (image SHA-256
`3a99ceea…d1c383cfad`).

| Requirement | Evidence (function entry, query result) | Strength |
| --- | --- | --- |
| 001 | Schema `12.0_12402` paths and 376 shipped sets (s1-static-v1); member registry `0x10275dccc`; `Manual` class `0x1026f0390` | S; units inferred |
| 002 | Writer `0x101486cdc` (n1-0008); flag-4 attribute registration `0x101564330` etc.; registration order = schema order (`registry-order-check.txt`); KeyMidi slot `0x10260dde0` | S; KeyMidi predicate inferred |
| 003 | Text conversion `0x10152bfb8`, bool branch disassembly `0x10152c1c8`–`0x10152c988` (n1-0006); "0" at `0x105ab32f8` | S |
| 004, 005 | Same function, float/double branches `0x10152c2b0`–`0x10152c550`, `0x10152c8d4` (n1-0006) | S |
| 006 | Integer parser `0x1002fd908` (n1-0006): converted length `min(len − start, end index after trailing spaces)` at `0x1002fd97c`–`0x1002fd9a4`, `+-` check, ASCII check, 63-character limit; converter `0x1002fda78` untraced; the envelope integers use the same parser ([document container native](../research/document-container-native.md#corrections-to-the-packet-notes-and-cases), N2-014) | S; trailing spaces after a leading space or `+`, and `-`, U |
| 007 | Generic loader `0x101487310` (n1-0008); ATransport constructor `0x102760d88` constants at `0x102762778`, `0x102762eb8`, `0x102762f0c`, `0x102762f20` (n1-0008); tempo `0x1026f4d98` (n1-0008), `0x101568960`; time-signature L-layer `0x1026f7420` (order unresolved) | S / U |
| 008 | Add-member `0x101472624` (n1-0007); start element `0x1015299e0` (n1-0007); attributes `0x10152b77c` (n1-0006) | S; versioned-mode condition partly traced (see SPEC-ALS-CONTAINER) |
| 009 | Direct store in `0x101487310`; ATransport post-load `0x10276c6f4` (n1-0008); enum setter not on the load path `0x10156675c` (n1-0002); controllers `0x102770bac`/`0x102770c0c` | S / U |
| 010 | Encoder `0x101abea70`, list builder `0x1026e10a8` (n1-0008); shipped scene code 302 = 6/8 | S |
| 011 | Formatters `0x101520c70`, `0x101520dbc`, `0x101431584`, `0x101431788` (n1-0007); zero test `fcmp d0,#0.0` at `0x1014315b4`/`0x1014317b8` is also true for −0.0; `number-format-check.txt`: 376/376 per field, 149,716/149,716 FloatEvent | S, corroborated by 12.4d1/12.1d1 writes; negative zero U |
| 012 | Translator `0x101492afc` (single unautomated event at −63,072,000); time range `0x1055dba00` | U |

Contradictions: static candidate T-09 ("at most 9/17 significant digits") is
superseded by REQ-011. 4,803 shipped values below 1 match REQ-011 and not `%.9g`.
Revision 2 applies the corrections reported in the
[handoff plan](transport-state-handoff-plan.md#contradictions-and-corrections-for-the-draft-owner):
revision 1 accepted ` +201 ` by trimming both ends, which the parser's length
computation contradicts.
Limits: the top-level load and its exception handler were not traced.
Pseudocode was confirmed against disassembly only for the cited branches.

Probe IDs: the `requirements` lists in the N1 `probe-batch.json` predate
revision 1 and are left unchanged there. This spec cites probes in its own
numbering: PRB-N1-02 is 007 (file: 006); PRB-N1-06 is 006, 009 and 010 (file:
010); PRB-N1-07 is 002, 008 and 011 (file: 011 and a nonexistent 013); PRB-N1-08
is 008 (file: 007 and 008). PRB-N1-01, 03, 04 and 05 match. PRB-N1-04 has no
variant without `TimeSignature/Manual`, so the REQ-007 default needs one added.
The [Phase 4 batch](../research/phase4-probe-batch.md) follows the spec.

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from the S1 static half and the N1 native half; 12 requirements (5 S only, 6 S with U parts, 1 U only), 23 unexecuted cases |
| 2 | 2026-10-17 | Handoff-author corrections. REQ-006: trailing spaces accepted only without a leading space or `+`; both-sides and `-` spellings U. TS-010 relabelled B, unresolved. TS-023 withdrawn (UI edit, out of scope); edits after load added to the exclusions. REQ-011: "positive zero"; negative zero U. TS-008, TS-020: event text only if written. Probe references checked; appendix notes the probe file's older IDs. 12 requirements (3 S only, 8 S with U parts, 1 U only); 22 cases, 4 of them unresolved (TS-010, TS-017–019) |

Revision 2 itself is not reviewed. The released
[transport-state-v1](../../handoff/transport-state-v1/README.md) (approved with
narrowing; [handoff plan](transport-state-handoff-plan.md)) was built from
revision 1 with these corrections applied. It carries 18 cases: TS-001–009,
TS-011–016 and TS-020–022. TS-010, TS-017–019, REQ-009 and REQ-012 stay out
until probes settle them.
