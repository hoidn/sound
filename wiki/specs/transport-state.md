---
id: SPEC-TRANSPORT-STATE
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 3
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

Every requirement is a **proposed contract** supported by a static derivation, by
extracted execution of the original x86_64 code, or explicitly unknown. Live itself
was never run. [ADR 0002](../decisions/adr-0002-static-first-analysis.md) permits a
static-first draft, and [ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)
adds extracted execution. Target: 12.4.3 arm64, documents with `MinorVersion="12.0_12402"`. The
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
| X | Extracted execution: the shipped x86_64 function was run on the given inputs, with glibc in place of Apple's libraries ([ADR 0003](../decisions/adr-0003-no-reference-execution.md#extracted-execution-of-original-code)). arm64 equivalence is inferred from a static comparison of the two slices. How Live reaches the function stays S |
| U | Unknown; no expected result. PRB IDs name the Phase 4 probe that would settle it |

Only S and X clauses may enter a release. U clauses block the behavior they name.
Where an X result depends on a substituted library, the clause says so.

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

- **S, X.** `LoopOn/@Value` text `true` or `1` loads loop on. `false` or `0` loads
  loop off. Matching is exact and case-sensitive, with no whitespace trimming.
- **S, X.** Any other text, including `TRUE`, `True`, an empty string, ` true`,
  `true `, `01` and `00`, makes the set not open. X: the text conversion refuses
  these by starting an exception; the open itself was not run.

### REQ-TRANSPORT-STATE-004 — loop and position number text on load

Applies to `LoopStart`, `LoopLength` and `CurrentTime`.

- **S, X.** The value is the longest leading prefix that C `strtod` accepts. The load
  succeeds when at least one character is consumed. Leading whitespace is skipped,
  and text after the prefix is ignored (`4.5abc` loads 4.5). Exponent, hexadecimal
  floating forms, `inf` and `nan` are accepted.
- **X.** These checks come before `strtod` and involve no library. Text that is exactly
  `Invalid` (7 characters, case-sensitive) loads the largest finite double. Text of
  exactly 17 characters, `#` and 16 hex digits of either case, loads those IEEE-754
  bits, most significant digit first: `#4012000000000000` is 4.5,
  `#3ff0000000000000` is 1, and `#8000000000000000` is −0. Any other text goes to
  `strtod`, so `Invalid `, ` Invalid`, `invalid`, and `#` with 15 or 17 digits or a
  non-hex digit make the set not open.
- **X (glibc `strtod`, C locale).** Signs and spaces are read as C specifies, so this reader
  does not behave like the REQ-006 integer reader. ` 4.5 `, `+4.5 `, ` +4.5 `,
  `-4.5` and ` -4.5` load 4.5 or −4.5, and `1e` and `1e+` load 1. `-0` and `-0.0` load −0.
  `- 4.5`, `+ 4.5`, `+-4.5`, `--4.5`, `+`, `-`, `.`, `abc`, and an empty or all-space
  value make the set not open. glibc also skips a leading tab or line feed. Inferred:
  Apple's `strtod` gives the same results in the C locale, whose grammar the C
  standard fixes.
- **S.** Text with no numeric prefix (`abc`, an empty string) makes the set not open.
- **U.** Whether a locale decimal comma or another white-space class is honored.

### REQ-TRANSPORT-STATE-005 — tempo text on load

- **S, X.** `Tempo/Manual/@Value` follows REQ-004, except that `#` takes exactly 8 hex
  digits (9 characters, either case: `#42f00000` is 120) and `Invalid` loads the
  largest finite float. The result is rounded to 32-bit float: `93.3333333` is held as
  93.33333587646484.
- **X.** The rounding is to nearest, ties to even, in the original code. A double
  above the largest float by half a float spacing or more becomes +∞: `3.4028236e38`
  and `1e39` give +∞, and `3.4028235e38` gives the largest finite float.

### REQ-TRANSPORT-STATE-006 — time-signature code text on load

- **X.** Split the value text into leading U+0020 spaces, at most one `+`, a body
  and trailing U+0020 spaces. The value loads when all five conditions hold.
  Otherwise the set does not open.
  1. Every byte is ASCII.
  2. The body is an optional `-` and then one or more ASCII digits, at most 63
     characters in all.
  3. A `+` is not followed by `-`.
  4. There are no trailing spaces when there are leading spaces or a `+`.
  5. The value lies in −2,147,483,648 to 2,147,483,647.

  Leading zeros are allowed: `00201` is 201, and `-0` is 0. Corrected in revision 3:
  the spellings with spaces on both sides, with `+` and trailing spaces, and with
  `-` were U. The conditions apply to the text after XML attribute-value decoding.
  That decoding turns a literal tab or line break into a space; only a character
  reference such as `&#9;` delivers one.
- **X.** Accepted spellings:
  - `201`, ` 201`, `+201`, `  +201`, `201 `, and `201` with 70 spaces before or after it;
  - `-201`, ` -201`, `-201 `, `-0`, `-01`, `-2147483648` and `2147483647`;
  - 63 characters `0…0201`, alone or with one leading space, one `+` or trailing spaces.
- **X.** Refused spellings:
  - spaces or `+` together with trailing spaces: ` 201 `, ` +201 `, `+201 `, ` -201 `, `   201 `;
  - signs: `- 201`, `+-201`, `+-0`, `-+201`, `--201`, `+`, `-`;
  - out of range: `2147483648`, `-2147483649`, `4294967497`;
  - other characters: a tab, line feed or carriage return before or after the digits,
    `2 01`, `201x`, `201.0`, `2e2`, `0x10`, `abc`, and a non-ASCII byte;
  - empty: an empty or all-space value;
  - too long: 64 characters `0…0201`, and `-` followed by 63 characters.
- **S.** A refused text stops the document read, as for the other values. X shows
  only that the text conversion starts an exception.
- **U.** What the loader does with an accepted code outside 0–494: REQ-009.

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
- **X.** The integer reader accepts codes outside 0–494, for example `-201`, `495` and
  `2147483647` (REQ-006). The loader stores them directly (S).
- **U.** The values Live then uses, displays and writes on the next save, including
  any clamping to start ≥ 0, length ≥ 1 or tempo 20–999: PRB-N1-03, PRB-N1-06.

### REQ-TRANSPORT-STATE-010 — time-signature code

- **S, X.** The code for numerator n and denominator d is `(n − 1) + 99 × log2(d)`,
  with n in 1–99 and d in {1, 2, 4, 8, 16}. Valid codes are 0–494. Examples: 4/4 =
  201, 6/8 = 302, 7/8 = 303, 99/16 = 494. X: the original encoder gives this for all
  495 pairs and no code for a denominator outside {1, 2, 4, 8, 16} or a numerator
  below 1. The original decoder maps code c in 0–494 back to n = (c mod 99) + 1 and
  d = 2^⌊c/99⌋.
- **X.** The time-signature value list has 495 entries. Entry c has the text `n/d`
  of code c: `1/1` for 0, `4/4` for 201, `99/16` for 494.
- **U.** Which display shows these texts. Inferred: they are the time-signature
  parameter's value names.
- **U.** The meter of a loaded code outside 0–494: PRB-N1-06. The decoder's
  arithmetic continues past 494 (495 gives 1/32; a negative code gives no meter), but
  nothing establishes that a loaded code reaches it.

### REQ-TRANSPORT-STATE-011 — number text on save

- **S.** Booleans are written `true` or `false`, and integers as plain decimal.
- **X.** For 64-bit fields (REQ-004) and 32-bit fields (REQ-005), let P = 17 or 9. A
  32-bit value is first widened exactly to 64 bits. Positive zero is written `0`, and
  negative zero `-0` (revision 3; was U). For any other finite x except the largest
  finite value:
  1. let L be log10|x| rounded to the nearest binary64 value, and k = ⌈L⌉ when L ≥ 0
     and ⌊L⌋ when L < 0 (corrected in revision 3: revision 2 took k from the exact
     logarithm);
  2. print x in fixed notation with max(0, P − k) decimals, rounded from its exact
     binary value to nearest;
  3. if the text contains `.`, remove trailing `0`s and then a trailing `.`.
- **X.** Rounding L matters only when L is an integer n but log10|x| is not. Then a
  64-bit x just above 10ⁿ (n ≥ 1) gets one decimal more than the exact logarithm
  would give it. An x just below 10⁻ⁿ (n ≥ 1) gets one decimal fewer, and that
  includes the nearest double to 10⁻ⁿ when it lies below 10⁻ⁿ. The text changes for
  n = 1 to 15 above and for every n below; larger values print no decimals either way.
  A 32-bit value other than an exact power of ten is never affected, and an exact
  power prints the same either way. X examples:
  - 100.00000000000001 → `100.000000000000014`
  - 1000.0000000000001 → `1000.00000000000011`
  - −1000.0000000000001 → `-1000.00000000000011`
  - 10.000000000000002 → `10.0000000000000018`
  - 0.09999999999999999 → `0.099999999999999992`
  - 0.000001 → `0.00000099999999999999995`
  - 1e-14 → `0.00000000000001`

  The exact logarithm would give `100.00000000000001`, `1000.0000000000001`,
  `-1000.0000000000001`, `10.000000000000002`, `0.0999999999999999917`,
  `0.000000999999999999999955` and `0.00000000000000999999999999999999`.
  0.9999999999999999 → `0.999999999999999889` is the same under both.
- **X.** The positive largest finite value is written `Invalid`. The most negative
  finite value follows the rule above (32-bit: `-340282346638528859811704183484516925440`).
  A non-finite value is written `#` and its IEEE bits in uppercase hex (16 or 8
  digits): `#7FF0000000000000`, `#FFF0000000000000` and `#7FF8000000000000` for +∞,
  −∞ and the default NaN; `#7F800000`, `#FF800000` and `#7FC00000` in 32 bits.
- Examples (S, and all X): 120 → `120`; float 121.2 → `121.199997`; float
  93.3333333 → `93.3333359`; double 0.3 → `0.299999999999999989`; double 3.3 →
  `3.2999999999999998`; 1e20 → `100000000000000000000`.
- **U.** The last bit of L where log10|x| lies about half a binary64 spacing from an
  integer. glibc's `log10` is not correctly rounded there. It differs from the
  correctly rounded L for 11 of 6,539 swept values, with offsets of 0.495 to 0.556
  spacings. Apple's `log10` was not run.
- **X (glibc formatter).** Exact decimal ties in step 2 round to even, for example
  tempo 120.0078125 → `120.007812` and 1 + 2⁻¹⁷ → `1.0000076293945312`. Inferred
  for Apple's formatter, as the transport-state-v1 review accepted; no case lies on a
  tie.

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
`<Manual Value="201" />`. No case has been run against Live. Case kinds: P positive,
N negative/malformed, B boundary, M missing, S save. Evidence: X means the case's
text conversion (reading or writing the value) ran as extracted execution and gave
the expected result. Locating the field, opening and saving remain S. S means a
static derivation only; U means unresolved.

| Case ID | Requirement | Kind | Evidence | Setup/action | Expected result/comparator | Fixture |
| --- | --- | --- | --- | --- | --- | --- |
| TS-001 | 003 | P | X | `<LoopOn Value="true" />`; open, save | Opens; loop switch on; saved `<LoopOn Value="true" />` | B0 edit |
| TS-002 | 003 | P | X | `<LoopOn Value="1" />`; open | Opens; loop on | B0 edit |
| TS-003 | 003 | P | X | `<LoopOn Value="0" />`; open | Opens; loop off | B0 edit |
| TS-004 | 003 | N | X | `<LoopOn Value="TRUE" />`; open | Set does not open | B0 edit |
| TS-005 | 003 | N | X | `<LoopOn Value="" />`; open | Set does not open | B0 edit |
| TS-006 | 004, 011 | B | X | `<LoopStart Value="4.5abc" />`; open, save | Opens; loop start 4.5; saved `<LoopStart Value="4.5" />` | B0 edit |
| TS-007 | 004 | N | X | `<LoopLength Value="abc" />`; open | Set does not open | B0 edit |
| TS-008 | 005, 011 | P | X | Tempo `<Manual Value="93.3333333" />` and `FloatEvent` `Value="93.3333333"`; open, save | Opens; saved Manual `93.3333359`, and the event `93.3333359` if written (REQ-002) | B0 edit |
| TS-009 | 006 | N | X | Time signature `<Manual Value="201.0" />`; open | Set does not open | B0 edit |
| TS-010 | 006 | N | X | Time signature `<Manual Value=" +201 " />`; open | Set does not open (graded in revision 3; was unresolved) | B0 edit |
| TS-011 | 007 | M | S | Delete the `LoopStart` element; open | Opens; loop start 8 | B0 edit |
| TS-012 | 007 | M | S | Replace with `<LoopLength />`; open | Opens; loop length 16 | B0 edit |
| TS-013 | 007 | M | S | Delete the `CurrentTime` and `LoopOn` elements; open | Opens; position 0; loop off | B0 edit |
| TS-014 | 007 | M | S | Tempo `<Manual />` (no Value); event stays 120; open | Opens; tempo 120 | B0 edit |
| TS-015 | 008 | N | S | Two `LoopOn` elements (`false` then `true`) in `Transport`; open | Set does not open | B0 edit |
| TS-016 | 008 | B | S | Add `<Foo Value="1" />` inside `Transport`; open, save | Opens; saved `Transport` has no `Foo` | B0 edit |
| TS-017 | 009 | B | U | `<LoopLength Value="-4" />`; open | Opens; effective and saved values unresolved | B0 edit |
| TS-018 | 009 | B | U | Tempo Manual and event `2000`; open | Opens; effective tempo unresolved | B0 edit |
| TS-019 | 009, 010 | B | U | Time signature Manual and `EnumEvent` `495`; open | Opens; effective meter unresolved | B0 edit |
| TS-020 | 011 | S | X | Tempo Manual and event `121.2`; open, save | Saved Manual `121.199997`, and the event `121.199997` if written (REQ-002) | B0 edit |
| TS-021 | 011 | S | X | `<LoopStart Value="0.3" />`; open, save | Saved `<LoopStart Value="0.299999999999999989" />` | B0 edit |
| TS-022 | 002 | S | S | Open B0 unchanged, save | Saved `Transport` children in the REQ-002 order; values unchanged | B0 |
| TS-023 | — | — | — | Withdrawn in revision 2: it edited the time signature in the UI, which is out of scope | Not graded | — |
| TS-024 | 011 | S | X | `<LoopStart Value="100.00000000000001" />`; open, save | Saved `<LoopStart Value="100.000000000000014" />` | B0 edit |
| TS-025 | 011 | S | X | `<LoopLength Value="1000.0000000000001" />`; open, save | Saved `<LoopLength Value="1000.00000000000011" />` | B0 edit |
| TS-026 | 011 | S | X | `<CurrentTime Value="0.09999999999999999" />`; open, save | Saved `<CurrentTime Value="0.099999999999999992" />` | B0 edit |
| TS-027 | 011 | S | X | `<LoopStart Value="0.000001" />`; open, save | Saved `<LoopStart Value="0.00000099999999999999995" />` | B0 edit |
| TS-028 | 004, 011 | B | X | `<LoopStart Value="-0" />`; open, save | Opens; saved `<LoopStart Value="-0" />` | B0 edit |
| TS-029 | 006 | N | X | Time signature `<Manual Value="+201 " />`; open | Set does not open | B0 edit |
| TS-030 | 006 | P | X | Time signature Manual and `EnumEvent` `-0`; open | Opens (code 0) | B0 edit |
| TS-031 | 006 | N | X | Time signature `<Manual Value="2147483648" />`; open | Set does not open | B0 edit |
| TS-032 | 006 | B | X | Time signature Manual `0…0201` (63 characters) followed by one space; open | Opens | B0 edit |
| TS-033 | 006 | N | X | Time signature Manual `-` followed by 63 `0`s; open | Set does not open | B0 edit |
| TS-034 | 004 | P | X | `<LoopLength Value=" +4.5 " />`; open | Opens; loop length 4.5 | B0 edit |
| TS-035 | 004 | N | X | `<LoopStart Value="- 4.5" />`; open | Set does not open | B0 edit |
| TS-036 | 004 | P | X | `<LoopStart Value="#4012000000000000" />`; open | Opens; loop start 4.5 | B0 edit |
| TS-037 | 005 | P | X | Tempo Manual and event `#42f00000`; open | Opens; tempo 120 | B0 edit |

TS-034 and TS-035 depend on glibc's `strtod` in place of Apple's. TS-024 to TS-027
depend on glibc's `log10` being correctly rounded at those values, which it is.
Their logarithms lie 0.02 to 0.17 binary64 spacings from an integer, so any
`log10` that errs by less than 0.8 spacing gives the same text.

Comparators: "opens" and "does not open" are judged by whether the set finishes
loading. Value comparisons are exact text for saved attributes, and an exact
displayed value (loop start/length in beats, tempo to the displayed precision) for
loaded state. Cases whose expectation says "unresolved" must not be graded as
passes. No case checks a valid REQ-010 code: its effect on load depends on
REQ-012 (PRB-N1-04), and edits are out of scope. TS-030 and TS-032 judge only
that the set opens. Cancellation and teardown kinds
are omitted: reading and writing these fields has no cancellable step or resource
defined in this scope.

## Open questions

[Q-012](../questions.md#q-012-transport-state-load-and-save-semantics) holds the
open items:

- the user-visible read-error outcome;
- REQ-012 precedence;
- the effective values for REQ-009;
- the missing time-signature default (REQ-007);
- the meter of a loaded code outside 0–494, and which display shows the meter
  texts (REQ-010);
- Apple's `log10` near half a spacing (REQ-011); Apple's formatter on exact ties and
  Apple's `strtod` for the REQ-004 sign and white-space spellings are inferred to
  match glibc;
- the current `SchemaChangeCount` and the KeyMidi and envelope presence on save (REQ-002, REQ-008).

Settled in revision 3 by extracted execution: the REQ-006 spellings with spaces on
both sides, with `+` and trailing spaces, and with `-` (TS-010); negative zero on
save (REQ-011).

The [probe batch](../../analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/probe-batch.json)
(PRB-N1-01–08) supplies a minimal input, a discriminating observation and a stop
condition for each.

## Analyst evidence appendix

Analysis-only. Do not copy into a handoff. The canonical evidence is
[transport-state native](../research/transport-state-native.md) and
[transport-state static](../research/transport-state-static.md), with retained run
`analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/` (image SHA-256
`3a99ceea…d1c383cfad`). X evidence is
[x2-transport-v1](../../analysis/ableton-live-12.4.3/r2/x2-transport-v1/manifest.json)
(x86_64 slice `1bae9a97…be999b0`; `sh run.sh`; results in `results/writer.json`,
`parse.json`, `meter.json`) and [x1-extracted-exec-v1](../../analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/manifest.json),
summarized on [transport-state native](../research/transport-state-native.md#extracted-execution-results-x2-2026-10-18).

| Requirement | Evidence (function entry, query result) | Strength |
| --- | --- | --- |
| 001 | Schema `12.0_12402` paths and 376 shipped sets (s1-static-v1); member registry `0x10275dccc`; `Manual` class `0x1026f0390` | S; units inferred |
| 002 | Writer `0x101486cdc` (n1-0008); flag-4 attribute registration `0x101564330` etc.; registration order = schema order (`registry-order-check.txt`); KeyMidi slot `0x10260dde0` | S; KeyMidi predicate inferred |
| 003 | Text conversion `0x10152bfb8`, bool branch disassembly `0x10152c1c8`–`0x10152c988` (n1-0006); "0" at `0x105ab32f8`. X2: x86 converter `0x10151b630`, 13 bool texts (`parse.json`) | S, X |
| 004, 005 | Same function, float/double branches `0x10152c2b0`–`0x10152c550`, `0x10152c8d4` (n1-0006). X2: x86 converter `0x10151b630` with glibc `strtod`, 67 double and 66 float texts (`parse.json`) | S, X; sign and white-space spellings rest on glibc `strtod` |
| 006 | Integer parser `0x1002fd908` (n1-0006): converted length `min(len − start, end index after trailing spaces)` at `0x1002fd97c`–`0x1002fd9a4`, `+-` check, ASCII check, 63-character limit; the envelope integers use the same parser ([document container native](../research/document-container-native.md#corrections-to-the-packet-notes-and-cases), N2-014). X2: x86 parser `0x100375650` and converter `0x10151b630` on 72 texts (`parse.json`); `from_chars` `0x100375790` ran, so no library is substituted | X |
| 007 | Generic loader `0x101487310` (n1-0008); ATransport constructor `0x102760d88` constants at `0x102762778`, `0x102762eb8`, `0x102762f0c`, `0x102762f20` (n1-0008); tempo `0x1026f4d98` (n1-0008), `0x101568960`; time-signature L-layer `0x1026f7420` (order unresolved) | S / U |
| 008 | Add-member `0x101472624` (n1-0007); start element `0x1015299e0` (n1-0007); attributes `0x10152b77c` (n1-0006) | S; versioned-mode condition partly traced (see SPEC-ALS-CONTAINER) |
| 009 | Direct store in `0x101487310`; ATransport post-load `0x10276c6f4` (n1-0008); enum setter not on the load path `0x10156675c` (n1-0002); controllers `0x102770bac`/`0x102770c0c` | S / U |
| 010 | Encoder `0x101abea70`, list builder `0x1026e10a8` (n1-0008); shipped scene code 302 = 6/8. X2: x86 encoder `0x101ae7a40` (655 pairs), decoder `0x101ae7a00` (arm64 `0x101abea38`; 3,405 codes), list builder `0x102812bf0` (495 texts) (`meter.json`) | S, X; display surface and out-of-range meaning U |
| 011 | Formatters `0x101520c70`, `0x101520dbc`, `0x101431584`, `0x101431788` (n1-0007); zero test `fcmp d0,#0.0` at `0x1014315b4`/`0x1014317b8` is also true for −0.0; `number-format-check.txt`: 376/376 per field, 149,716/149,716 FloatEvent. X2: x86 writers `0x10150f6a0`/`0x10150f7a0` (specials and case values) and formatters `0x10142b6c0`/`0x10142b980` (6,539-value sweep around every power of ten) with glibc `log10` and `vsnprintf` (`writer.json`) | S, X; L's last bit near half a spacing and exact ties rest on the substituted libraries |
| 012 | Translator `0x101492afc` (single unautomated event at −63,072,000); time range `0x1055dba00` | U |

Contradictions: revision 2's REQ-011 step 1 (k from the exact logarithm) is
contradicted by X for 825 of the 6,539 swept 64-bit values (all next to powers of
ten); revision 3 takes k from the rounded binary64 logarithm, which agrees with X
for 6,528 and with glibc's own `log10` for all 6,539. Static candidate T-09 ("at
most 9/17 significant digits") is superseded by REQ-011. 4,803 shipped values below 1 match REQ-011 and not `%.9g`.
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
| 3 | 2026-10-18 | Extracted execution (X2, ADR 0003); label X added. REQ-011 corrected: k comes from the binary64 logarithm, which differs from revision 2 next to powers of ten; negative zero is written `-0`; positive largest, most negative and non-finite texts X; ties to even X on glibc; the library-dependent last bit of L U. REQ-006 restated exactly (X): sign, spaces, 63-character body, int32 range. REQ-003, 004 and 005 checks X, with REQ-004's sign and space spellings on glibc `strtod`. REQ-009 notes the accepted out-of-range codes. REQ-010 encoder, decoder and the 495 meter texts X. TS-010 graded (refused). TS-024–037 added. 12 requirements (2 without U parts, 9 with U parts, 1 U only); 36 graded cases (26 X, 7 S, 3 U) |

Revisions 2 and 3 are not reviewed. Revision 3 is the source of the unreviewed
candidate transport-state-v2, with 33 cases: v1's 18 plus TS-010 and TS-024–037.
It would supersede transport-state-v1 ([v2 handoff plan](transport-state-v2-handoff-plan.md)).
The released [transport-state-v1](../../handoff/transport-state-v1/README.md)
(approved with narrowing; [handoff plan](transport-state-handoff-plan.md)) was
built from revision 1 with the revision 2 corrections applied. It carries 18
cases: TS-001–009, TS-011–016 and TS-020–022. TS-017–019, REQ-009 and REQ-012
stay out of both.

Status note, 2026-10-18 (editorial; requirements unchanged): under [ADR 0003](../decisions/adr-0003-no-reference-execution.md) the probes cited here (PRB-N1-01 to 08) will not run on a macOS host. Clauses waiting on them stay unknown until extracted execution of the original x86_64 code or further static work settles them.
