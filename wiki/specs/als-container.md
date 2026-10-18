---
id: SPEC-ALS-CONTAINER
type: spec
status: draft
updated: 2026-10-18
access: analysis
revision: 2
target: Ableton Live 12 Suite 12.4.3 arm64 (macOS)
---

# Live document container and version envelope

## Scope

Feature: FEAT-PERSISTENCE in the [feature map](feature-map.md); this draft
covers only the outer layer of a Live Set file. The user task is to open a
`.als` file, or be told why it cannot be opened, and to save one. The draft
covers:

- how the file's bytes are recognized as compressed or plain XML;
- the root element and its attributes;
- which version values are accepted, refused as corrupt, or refused as newer;
- what is known about the envelope written on save.

Excluded: the content of the set below the root's first child, upgrading older
documents, legacy binary and UTF-16 text documents, presets, clips and other
document kinds, media references and crash recovery. Dependencies: the shipped
schema directory (`Contents/App-Resources/Schema/*.txt`) and the running
application's version, 12.4.3.

The requirements are **proposed behavioral contracts** derived from static
reading of the 12.4.3 program and its shipped files. No requirement was observed
in a running Live. No requirement is documented by Ableton: no user
documentation was consulted for this packet. Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) a static derivation
can support a draft, but the derivation is never a measured result.

## Evidence labels

| Label | Meaning |
| --- | --- |
| Documented | Stated in shipped documentation. No clause in this revision has this label |
| Static-derived | Follows from the program's code and shipped files as read, without execution; any assumption is stated beside the clause, by ID when it is one of I1–I6 below |
| Unknown | Not decided by the evidence. Has no expected output and blocks release of that clause; the probe ID names the planned Phase 4 observation |

## Assumptions

Several derivations rest on an assumption that the evidence supports but does
not establish. A clause that rests on one names it, for example
"Static-derived (assumes I1)". If an assumption fails, the clauses naming it
become unknown. The IDs match the analyst traceability records (appendix).

Review update 2026-10-17 (als-container-v1, RVA-01): the separate reviewer established I1
statically (a handler-level catch of the thrown type stores the message, stops the parser,
sets the error flag and leads to the post-parse classification) and confirmed I3 (the
converter is a base-10 conversion that stops at the first non-digit). I2, I4, I5 and I6
remain assumptions.

| ID | Assumption | What rests on it |
| --- | --- | --- |

| I1 | A refusal raised while the root element or the document element is read stops parsing there and is classified after parsing, by the same decision that reports XML errors | The class of each such refusal (corrupt-document or newer-version); never whether the file is refused |
| I2 | A Live Set's document element is subject to the version checks of REQ-ALS-CONTAINER-003 | Refusals by checks 1–4 (REQ-ALS-CONTAINER-003 to 005) |
| I3 | After the space and sign handling of REQ-ALS-CONTAINER-003, an integer value is converted as a whole-string base-10 integer | Accepted integer spellings; refusal of values such as `five` |
| I4 | With MinorVersion absent, the schema check completes normally and finds no schema | Refusal of an absent MinorVersion |
| I5 | The schema-file lookup and the largest-translator scan both use the shipped schema directory | Clauses that name schema files or a family's largest translator |
| I6 | A gzip file is inflated as one standard member with the header form of the shipped sets (FLG 0) | Every gzip clause and case |

## Inputs and preconditions

Input is a file opened as a Live Set. A file is *gzip* if its first two bytes
are `1F 8B`; *plain XML* if its first two bytes are `<?`. The *envelope* is the
XML declaration, the root element and the root's attributes `MajorVersion`,
`MinorVersion`, `SchemaChangeCount`, `Creator` and `Revision`. A *document
element* is the root's first child, `LiveSet` for a Live Set.

A *schema name* has the form `<a>.<b>_<c>` with decimal a, b and c, for example
`12.0_12402`. The pair (a, b) is its *family* and c its *translator number*. The
shipped schema directory holds 203 such files. The newest is `12.0_12402`, and
the 12.0 family has gaps (for example, no `12.0_12050`). The running
application's version pair is (12, 4), from 12.4.3.

The program reads documents along two paths that differ only in a few clauses
below. The *general reading path* recognizes every stream kind but does not
supply the running version to its newer-family comparison, so that comparison
is undetermined. The *version-aware reading path* knows
the running version and the application-name prefix of `Creator`, but returns
no document, without an error, for unrecognized bytes. Which path File > Open
uses is unknown (PRB-N2-05). Clauses that depend on it say so.

Precondition for every case: a fresh application launch with no unsaved set,
opening the case file with File > Open Live Set. The cases in this draft were
built from two shipped sets. A *minimal document* has an XML declaration, a root
with the listed attributes and one empty `LiveSet` child. A *full set* is the
decompressed shipped lesson set `Recording Audio.als` with its root attributes
edited.

Two failure classes are distinguished:

- **corrupt-document**: names the document and carries a detail;
- **newer-version**: names the document, either alone or with a version text.

The detail kinds below are labels; the appendix maps each to the recovered
message text. Whether the text is shown to the user is REQ-ALS-CONTAINER-009.

| Detail | Meaning |
| --- | --- |
| stream-type | The bytes are not a recognized document stream |
| wrong-root | The root element is not `Ableton`; names the element found |
| major-missing | MajorVersion is absent or zero |
| minor-missing | MinorVersion is absent or empty |
| illegal-integer | An integer attribute's value is not an integer; quotes the value |
| major-unsupported | MajorVersion is not supported; names the number |
| minor-unsupported | MinorVersion names no known schema; quotes the value |
| xml | The XML is not well-formed; the XML parser's message |
| no-document | The root has no document element |

## Requirements

### REQ-ALS-CONTAINER-001 — container recognition

The application recognizes a Live Set by its first bytes, not its file name. A gzip file is decompressed and its content recognized again. Content whose first two bytes are `<?` is parsed as XML. Other starts of an XML document are refused.

- **Static-derived (assumes I6).** A gzip file read from disk is decompressed
  and its content is recognized by the same rule. Gzip content cannot be read
  from a source without a file path.
- **Static-derived.** Content starting with `<?` is parsed as XML whatever the
  file extension.
- **Static-derived (refusal; class unspecified).** These are refused: XML
  preceded by a UTF-8 byte order mark, XML preceded by whitespace, XML with no
  declaration (the root element first), content shorter than two bytes, and
  content starting with bytes that match none of the recognized starts (gzip,
  `<?`, and legacy formats this draft excludes). On the general reading path
  the expected class is corrupt-document with detail stream-type, but the step
  that raises it was not traced; if it does not raise, a different error
  follows at once, so the file is refused either way. On the version-aware
  reading path content shorter than two bytes is refused as corrupt-document
  with detail stream-type; the other inputs yield no document and no error,
  and counting that as a refusal assumes that no set is opened from no
  document (PRB-N2-05). The class is therefore not specified.
- **Static-derived.** XML that is not well-formed is refused as corrupt-document
  with detail xml, even after a valid envelope.
- **Unknown.** Whether File > Open accepts an uncompressed `.als` at the command
  level, and whether a later save keeps it uncompressed (PRB-N2-02).
- **Unknown.** Handling of truncated or corrupt gzip data, multiple gzip
  members and gzip header flags (PRB-N2-07). Shipped sets use FLG 0, or FNAME in
  the default template, and are expected to open.

### REQ-ALS-CONTAINER-002 — root element

The root element must be named exactly `Ableton`, case-sensitive; otherwise the document is refused as corrupt-document with detail wrong-root naming the element found.

- **Static-derived (class assumes I1).** The name comparison is exact: `Live`
  and `ableton` are refused as corrupt-document. A wrong root is refused before
  any root attribute is read.
- **Static-derived (no constructed case).** A root with no child element is
  refused as corrupt-document with detail no-document.
- **Unknown.** Whether a second child of the root is always refused (the check
  depends on when the first document is registered), and what happens when the
  document element is of a kind other than `LiveSet`.

### REQ-ALS-CONTAINER-003 — version attribute presence and MajorVersion range

MajorVersion must be an integer 4 or 5 and MinorVersion must be present and non-empty; otherwise the document is refused, as corrupt-document for these failures or as newer-version for MajorVersion 6 or more when no earlier check refuses (REQ-ALS-CONTAINER-004).

- **Static-derived.** Attributes are found by exact, case-sensitive name. Their
  order does not matter.
- **Static-derived.** The integer rule below is applied to MajorVersion and
  SchemaChangeCount when the parser reads the root element, MajorVersion
  first. A value that fails it is refused there, before the document element
  is read and before any of the numbered checks. This holds whatever the
  document kind.
- **Static-derived (assumes I2; classes assume I1).** The numbered checks are
  made when the parser reaches the document element. The first failing check
  decides the detail:
  1. MajorVersion absent or `0`: major-missing.
  2. MinorVersion absent or empty: minor-missing (see the next bullet).
  3. MajorVersion below 6 and other than 4 or 5: major-unsupported naming the
     value, for example `3`.
  4. MinorVersion names no schema: REQ-ALS-CONTAINER-005.
- **Static-derived (detail unknown; assumes I1, I2).** An empty MinorVersion
  is refused as corrupt-document. An absent MinorVersion is refused as
  corrupt-document, assuming I4 as well. The detail is either minor-missing or
  minor-unsupported with an empty value; which one is unknown for each of the
  two inputs.
- **Static-derived (class assumes I1).** An integer attribute value is refused
  as corrupt-document with detail illegal-integer, quoting the raw value, when
  any of these holds:
  - it is empty or only spaces;
  - it contains a byte outside ASCII;
  - it has a `+` followed by `-`;
  - the part to convert, after leading spaces and a leading `+`, is longer
    than 63 characters;
  - it is not a decimal integer, for example `five` (assumes I3).
- **Static-derived (assumes I3).** Accepted spellings include `5`, `+5`, ` 5`
  and `5 ` (spaces are U+0020 only).
- **Unknown.** Values with spaces on both sides, or with `+` and a trailing
  space (` 5 `, `+5 `, ` +5 `). The traced code passes the trailing space on to
  the digit conversion. Under I3 these values are refused with illegal-integer
  (PRB-N2-06).
- **Unknown.** Whether a set with MajorVersion 4 and a current MinorVersion
  loads beyond the envelope (PRB-N2-06).
- **Unknown.** Which document kinds skip the numbered checks. Live Sets are
  assumed to be checked (I2) because every shipped set carries the attributes.

### REQ-ALS-CONTAINER-004 — newer-version refusal

A document whose version values are newer than the application's is refused with the newer-version class when the check that detects them is reached; a refusal reached earlier is reported as corrupt-document.

- **Static-derived (assumes I1, I2, I3).** MajorVersion 6 or above is refused
  as newer-version.
- **Static-derived (assumes I1, I2, I5).** A MinorVersion `<a>.<b>_<c>` with no
  schema file is refused as newer-version when the schema directory has family
  (a, b) and its largest translator number is below c. Example: `12.0_12403`.
- **Unknown (static-derived on the version-aware reading path only).** A
  MinorVersion whose family is newer than the running version is refused as
  newer-version on the version-aware path: a > 12, or a = 12 and b > 4, for
  example `13.0_13000`. On the general reading path the outcome is
  undetermined statically and may be corrupt-document (PRB-N2-05).
- **Static-derived (version-aware reading path).** The version text, when
  present, comes from `Creator`: the remainder after the application-name
  prefix, assuming surrounding spaces are removed (`12.4d1` for
  `Ableton Live 12.4d1`). For a newer family with no usable Creator remainder,
  the version text is `<a>.<b>`. Otherwise, with no remainder, the message names
  no version.
- **Unknown.** The message text, and whether the general reading path uses the
  whole Creator as the version text (PRB-N2-04).
- **Static-derived (assumes I1).** Reading stops at the first refusal. There
  is no general precedence of newer-version over corrupt-document: the result
  is newer-version only when the refusal that stopped reading is itself a
  newer condition. Those are MajorVersion 6 or more at check 3 of
  REQ-ALS-CONTAINER-003, a MinorVersion that is newer by the clauses above at
  check 4, and the unknown-element condition of REQ-ALS-CONTAINER-006. Content
  after that point is not examined, so a later XML error does not change the
  class. A refusal reached first is corrupt-document even when the document
  also carries a newer MajorVersion or MinorVersion:
  - malformed XML before the document element, or a wrong root;
  - an illegal integer in MajorVersion or SchemaChangeCount, refused when the
    root is read (REQ-ALS-CONTAINER-003);
  - an absent or zero MajorVersion together with a newer MinorVersion;
  - a MajorVersion below 6 other than 4 or 5 together with a newer MinorVersion;
  - a root without a document element, where no version check runs.

  Example: `MajorVersion="6"` with `SchemaChangeCount="x"` is refused as
  corrupt-document with detail illegal-integer.
- **Unknown.** `MajorVersion="6"` with an empty or absent MinorVersion. The
  MinorVersion check (check 2) comes first: if it refuses, the class is
  corrupt-document; if the value reaches check 3, newer-version. This is the
  detail question of REQ-ALS-CONTAINER-003; for an absent value, see also I4.

### REQ-ALS-CONTAINER-005 — MinorVersion selects a shipped schema

MinorVersion must name a file `<MinorVersion>.txt` in the application's schema directory; a value that names none and is not newer (REQ-ALS-CONTAINER-004) is refused as corrupt-document with detail minor-unsupported quoting the value.

- **Static-derived (assumes I5).** Any of the 203 shipped schema names passes
  this check, including older families back to `8.1`. Example: the shipped
  default template with `12.0_12117`.
- **Static-derived.** The check looks up the file `<MinorVersion>.txt` in the
  schema directory at run time. It tests only whether that file exists; it
  does not test the value's form.
- **Static-derived (assumes I1, I2, I5).** A value made only of letters, for
  example `garbage`, is refused as corrupt-document. The shipped directory
  holds no such file, and the value is not of the schema-name form, so it
  cannot be newer.
- **Unknown.** Other values not of the schema-name form, such as values that
  contain a path separator or that name another `.txt` file reachable from the
  schema directory. They are not established as refused.
- **Unknown.** A missing translator inside the current family, for example
  `12.0_12050`. This is corrupt-document on the version-aware reading path and
  undetermined on the general path (PRB-N2-05).
- **Unknown.** Whether older documents are converted correctly after this check.
  That is out of this draft's scope.

### REQ-ALS-CONTAINER-006 — optional and ignored root attributes

`Creator`, `Revision` and `SchemaChangeCount` are optional, other root attributes are ignored, and none of them changes whether a valid document opens; a present `SchemaChangeCount` must be a valid integer.

- **Static-derived.** `Revision` is never read; any value or absence is
  accepted.
- **Static-derived.** `Creator` is free text. A missing Creator, or one that
  does not name Ableton, is accepted. It is used only for the version text in
  REQ-ALS-CONTAINER-004.
- **Static-derived (class assumes I1).** `SchemaChangeCount` may be absent
  (taken as 0). If present, it must pass the integer rule of
  REQ-ALS-CONTAINER-003; otherwise the document is refused as corrupt-document
  with illegal-integer when the root is read. This happens before the version
  checks, so it applies even when MajorVersion is newer (REQ-ALS-CONTAINER-004).
- **Static-derived.** Root attributes with other names are ignored.
- **Static-derived (no constructed case; assumes I1, I2).** When an element
  name unknown to the named schema occurs, the refusal is newer-version if
  SchemaChangeCount exceeds that schema's change count, and corrupt-document
  otherwise.
- **Unknown.** Any non-refusing effect of a non-Ableton Creator on the user
  interface.

### REQ-ALS-CONTAINER-007 — container written on save

Unknown: whether a Live Set saved by 12.4.3 is gzip-compressed, and its gzip header bytes.

- **Static-derived (conditional).** The envelope writer compresses with gzip at
  a level chosen by its caller. The default is 6 or a configured value limited
  to 0–9; level 0 writes plain XML. The caller and level used for a Live Set
  were not identified.
- **Unknown.** Compression on save, the XFL, OS and MTIME header bytes, and
  whether saving a set opened from a plain file writes plain or gzip
  (PRB-N2-01, PRB-N2-02).

### REQ-ALS-CONTAINER-008 — envelope written on save

A saved Live Set's envelope, as far as derived: declaration `<?xml version="1.0" encoding="UTF-8"?>`, root `Ableton`, attributes in the order MajorVersion, MinorVersion, SchemaChangeCount, Creator, Revision, with MajorVersion `5`.

- **Static-derived (conditional).** This assumes the set is written by the
  application's single envelope writer, the only code that writes these
  attribute names. Then:
  - MajorVersion is `5`;
  - SchemaChangeCount is written only when positive;
  - the attribute order is as stated.
- **Static-derived with an assumption.** From the application's version data,
  and assuming the newest registered translator is 12402: MinorVersion
  `12.0_12402`, Creator `Ableton Live 12.4.3` and Revision
  `e3d8be4d07c71dbd4de9e4183bf90652f680375b`.
- **Unknown.** The SchemaChangeCount value (candidate 5), indentation,
  whitespace and line endings, and the complete first lines byte-for-byte
  (PRB-N2-01).

### REQ-ALS-CONTAINER-009 — failure presentation and state

Unknown: the dialog text for each failure class, whether the detail is shown, and whether the previously open set remains open after a refused document.

- **Static-derived.** The program distinguishes the two failure classes. A
  corrupt-document detail produced while parsing XML carries the line and
  column at which parsing stopped; details for unrecognized streams and missing
  documents carry no position. For errors raised while reading the root or the
  document element this assumes I1.
- **Unknown.** The localized texts, the dialog layout, log lines and the state
  after failure (PRB-N2-03, PRB-N2-04).

## Timing and state

No timing, ordering or tolerance applies beyond the order of checks stated in
REQ-ALS-CONTAINER-003 and REQ-ALS-CONTAINER-004. Loading is treated as one
operation whose outcome is "opened", "refused as corrupt-document", "refused
as newer-version" or, where the class is unspecified, "refused". Whether it
runs synchronously, and whether progress is shown, is unknown.

Persistent state: the schema directory is read-only input. State after a
refusal is unknown (REQ-ALS-CONTAINER-009). What a successful open does to the
previously open set, and whether open or save interact with undo, were not
examined in this packet.
Interaction with transport and audio is out of scope. Round-trip (open, save,
reopen) is unknown until REQ-ALS-CONTAINER-007 and REQ-ALS-CONTAINER-008 are
observed.

## Errors, cancellation and teardown

Every refusal with a specified class is one of the two failure classes; the
start refusals of REQ-ALS-CONTAINER-001 have no specified class. The detail
strings are candidate observables only; comparators below grade the class, not
the text, until REQ-ALS-CONTAINER-009 is resolved. No cancel affordance during
loading is established, so no cancellation case is defined. Teardown (the state
left after a refused open) is REQ-ALS-CONTAINER-009 and is unknown.

## Acceptance cases

None of these cases has been run against Live or a candidate. "Expected" is a
static derivation or explicitly unknown; it is not an observation. The
comparator is the outcome class: opens, corrupt-document or newer-version, or
"refused" in any class where the class is unspecified. The detail kind is
recorded but not graded. Fixtures are the case files named in the last column
(location and SHA-256 in the appendix).

Fixture container. Only N2-001, N2-021 and N2-027 are gzip. N2-002 to N2-020
and N2-022 to N2-026 are uncompressed plain XML, so under File > Open each of
their expectations also depends on PRB-N2-02. Storing the envelope cases as
gzip with the shipped sets' header form removes that dependency and rests on
I6 instead; the staged handoff candidate does this.

| Case ID | Requirement | Case kind | Setup/action | Expected result | Label | Fixture |
| --- | --- | --- | --- | --- | --- | --- |
| N2-001 | 001 | positive | Shipped lesson set, unchanged gzip | Opens | Static-derived (assumes I6 and that the shipped set loads past the envelope) | `N2-001.als` |
| N2-002 | 001 | positive | Same set, decompressed to plain XML | Recognized as XML and passes the envelope; acceptance by File > Open unknown | Static-derived (recognition); unknown (PRB-N2-02) | `N2-002.als` |
| N2-003 | 001 | malformed | N2-002 with a UTF-8 byte order mark prepended | Refused, class unspecified (corrupt-document, stream-type expected on the general path) | Static-derived (refusal) | `N2-003.als` |
| N2-004 | 001 | malformed | N2-002 with a leading newline | Refused, class unspecified (corrupt-document, stream-type expected on the general path) | Static-derived (refusal) | `N2-004.als` |
| N2-005 | 001 | malformed | N2-002 without the XML declaration | Refused, class unspecified (corrupt-document, stream-type expected on the general path) | Static-derived (refusal) | `N2-005.als` |
| N2-026 | 001 | malformed | First half of N2-002 | Corrupt-document, xml | Static-derived | `N2-026.als` |
| N2-027 | 001 | malformed | First half of N2-001's compressed bytes | Unresolved | Unknown (PRB-N2-07) | `N2-027.als` |
| N2-006 | 002 | negative | Minimal document with root `Live` | Corrupt-document, wrong-root naming `Live` | Static-derived (assumes I1) | `N2-006.als` |
| N2-007 | 002 | negative | Minimal document with root `ableton` | Corrupt-document, wrong-root naming `ableton` | Static-derived (assumes I1) | `N2-007.als` |
| N2-008 | 003 | negative | Minimal document without MajorVersion | Corrupt-document, major-missing | Static-derived (assumes I1, I2) | `N2-008.als` |
| N2-009 | 003 | boundary | Minimal, `MajorVersion="0"` | Corrupt-document, major-missing | Static-derived (assumes I1, I2, I3) | `N2-009.als` |
| N2-010 | 003 | malformed | Minimal, `MajorVersion="five"` | Corrupt-document, illegal-integer quoting `five` | Static-derived (assumes I1, I3) | `N2-010.als` |
| N2-011 | 003 | boundary | Minimal, `MajorVersion="3"` | Corrupt-document, major-unsupported naming 3 | Static-derived (assumes I1, I2, I3) | `N2-011.als` |
| N2-012 | 003 | boundary | Full set, `MajorVersion="4"` | Passes the envelope; whole-set load unresolved | Static-derived (envelope, assumes I3); unknown (PRB-N2-06) | `N2-012.als` |
| N2-014 | 003 | boundary | Full set, `MajorVersion=" +5 "` | Unresolved; static reading suggests corrupt-document, illegal-integer | Unknown (PRB-N2-06) | `N2-014.als` |
| N2-015 | 003 | negative | Minimal document without MinorVersion | Corrupt-document; detail minor-missing or minor-unsupported (empty) | Static-derived (class, assumes I1, I2, I4); detail unknown | `N2-015.als` |
| N2-016 | 003 | boundary | Minimal, `MinorVersion=""` | Corrupt-document; detail minor-missing or minor-unsupported (empty) | Static-derived (class, assumes I1, I2); detail unknown | `N2-016.als` |
| N2-013 | 004 | boundary | Minimal, `MajorVersion="6"` | Newer-version | Static-derived (assumes I1, I2, I3) | `N2-013.als` |
| N2-019 | 004 | boundary | Minimal, `MinorVersion="12.0_12403"` | Newer-version | Static-derived (assumes I1, I2, I5) | `N2-019.als` |
| N2-020 | 004 | boundary | Minimal, `MinorVersion="13.0_13000"` | Newer-version on the version-aware path; unresolved for File > Open | Unknown (PRB-N2-05) | `N2-020.als` |
| N2-017 | 005 | malformed | Minimal, `MinorVersion="garbage"` | Corrupt-document, minor-unsupported quoting `garbage` | Static-derived (assumes I1, I2, I5) | `N2-017.als` |
| N2-018 | 005 | negative | Minimal, `MinorVersion="12.0_12050"` | Corrupt-document or newer-version, depending on reading path | Unknown (PRB-N2-05) | `N2-018.als` |
| N2-021 | 005 | positive | Shipped default template (gzip with stored file name, `12.0_12117`) | Opens | Static-derived (assumes I5, I6, that the gzip file-name field is skipped (PRB-N2-07) and that the shipped template loads) | `N2-021.als` |
| N2-022 | 006 | positive | Full set without Creator and Revision | Opens | Static-derived | `N2-022.als` |
| N2-023 | 006 | positive | Full set, `Creator="Somebody Else 1.0"`, `Revision="not-hex"` | Opens | Static-derived | `N2-023.als` |
| N2-024 | 006 | positive | Full set without SchemaChangeCount, plus `Extra="1"` | Opens | Static-derived | `N2-024.als` |
| N2-025 | 006 | malformed | Minimal, `SchemaChangeCount="x"` | Corrupt-document, illegal-integer quoting `x` | Static-derived (assumes I1, I3) | `N2-025.als` |

Counts: REQ-001 7, REQ-002 2, REQ-003 8, REQ-004 3, REQ-005 3, REQ-006 4;
27 in total. 23 have a static-derived expectation (N2-002 and N2-012 only
up to the envelope; N2-003 to N2-005 refusal only, class unspecified; N2-015
and N2-016 without their detail) and 4 are unknown (N2-014, N2-018, N2-020,
N2-027). Every graded refusal class except N2-026's rests on I1. REQ-007 to
REQ-009 have no case files; their probes are the cases. Positive "opens" expectations for full sets
assume the unchanged set content loads, which this packet did not trace.
Omitted kinds: cancellation (no affordance established) and teardown
(REQ-ALS-CONTAINER-009, unknown).

## Open questions

| Item | Requirements | Missing evidence | Next step |
| --- | --- | --- | --- |
| PRB-N2-01 | 007, 008 | Bytes of a fresh 12.4.3 save | One save captured and hashed |
| PRB-N2-02 | 001, 007; every uncompressed fixture | File > Open of a plain-XML set, then Save | One open, one save |
| PRB-N2-03 | 001–003, 005, 009 | Dialog text, detail display, state after refusal | Ten corrupt cases |
| PRB-N2-04 | 004 | Newer-version text and version named | Three newer cases |
| PRB-N2-05 | 001, 004, 005 | Which reading path File > Open uses | N2-018 and N2-020 |
| PRB-N2-06 | 003, 005, 006 | Whether accepted envelope variants open as sets; N2-014 | Six opens |
| PRB-N2-07 | 001 | Truncated gzip outcome | N2-027 |

Canonical gaps: [Q-006](../questions.md#q-006-native-analysis-and-resource-decoding)
(native analysis and resource decoding) and
[Q-012](../questions.md#q-012-transport-state-load-and-save-semantics) (the
exact format 12.4.3 writes). Several unknowns can still be narrowed statically
before any probe; see the research page's remaining-unknowns section.

## Analyst evidence appendix

Analysis-only. Remove or review before any handoff. Canonical findings:
[native research](../research/document-container-native.md) and
[static research](../research/document-container-static.md). Evidence run:
`analysis/ableton-live-12.4.3/r2/n2-container-v1/`
([manifest](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/manifest.json),
SHA-256 `8faab9dccf6a…`, 247 files, all hashes matched 2026-10-17). Image
`Live.arm64` SHA-256 `3a99ceea…d1c383cfad`, Ghidra 12.1.4. Fixtures:
`cases/N2-001.als` … `N2-027.als`, listed with SHA-256 in
[cases.json](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/cases.json)
(SHA-256 `ab9d6dbd3ae2…`). They were built by `make_cases.py` from
`Core Library/Lessons/Sets/Recording Audio.als` (`af57ff8f…`) and
`Builtin/Templates/DefaultLiveSet.als` (`aeec3f07…`). Probes:
[probe-batch.json](../../analysis/ableton-live-12.4.3/r2/n2-container-v1/probe-batch.json).

| Requirement | Function entries (result id) | Basis |
| --- | --- | --- |
| 001 | `0x10148389c` (n2-0002), `0x10146c258` (n2-0002), `0x10146c0d4` (n2-0005), `0x101483cec` (n2-0001 reference only), `0x1012475a8`, `0x101247760`, `0x101247828` (corpus) | Dispatcher disassembly; stream-type error class inferred for the general path; gzip object `0x10146208c` untraced |
| 002 | `0x1015299e0` (n2-0002; disassembly `0x101529c5c`–`0x101529c8c`), `0x1015289c8` (n2-0003) | Root compare; no-document step |
| 003 | `0x10152a900`, `0x10152ab04` (n2-0003), `0x1002fd908` (n2-0005 disassembly), `0x101529024` (n2-0002 disassembly), `0x101429854`, `0x101432520`, `0x1011cb734` (corpus) | Integer rule; check order; empty-string layout inferred; converter `0x1002fda78` untraced |
| 004 | `0x101529024`, `0x1015289c8` (n2-0003 disassembly), `0x101528c84` (n2-0005), `0x101528e2c` (n2-0002), `0x101514e30` (n2-0005), `0x101514f7c`, `0x1011c1c24`, `0x1011c2bb0` (corpus) | Newer flag and post-parse order; current pair (12, 4) inferred; general path leaves the pair uninitialized (`0x101484108`, n2-0003) |
| 005 | `0x101514c6c` (n2-0003), `0x101514954` (n2-0005), `0x101514864`, `0x10152a570` (n2-0005) | Runtime file lookup `<MinorVersion>.txt` |
| 006 | `0x1015299e0`, `0x10152a570`, `0x101573d24` (corpus), n2-0001 `Revision` reference report | Attributes read; Revision unread; Creator only in newer paths and an internal event |
| 007 | `0x101485240` (n2-0002), `0x1014338b0` (n2-0005 disassembly), `0x1014339e4`, `0x101485c50` (n2-0005), `0x1018ed778`, `0x102971090` (corpus) | Level handling; Live Set caller not identified |
| 008 | `0x101485240`, `0x1015170a8`, `0x101515508`, `0x1011c2bb0`, `0x1002ea094`, `0x101470ef4` (corpus); index-lookups string rows | Single writer, order, literal 5; translator registry `0x10148ec98` not in kept evidence |
| 009 | `0x10148229c`, `0x101488e64`, `0x101488ec0` (corpus), `0x10148e4cc`, `0x101535400` (n2-0002), `0x101529970`, `0x101247760` (corpus) | Error identities; catch step from handler exception to stored detail inferred |

Detail labels and the recovered message texts:

| Detail | Recovered text |
| --- | --- |
| stream-type | `Unknown Compound Stream Type` |
| wrong-root | `Expected 'Ableton' root node, got '$1' instead` |
| major-missing | `MajorVersion attribute missing from 'Ableton' root node` |
| minor-missing | `MinorVersion attribute missing from 'Ableton' root node` |
| illegal-integer | `Illegal value for int attribute: $1` |
| major-unsupported | `Unsupported MajorVersion (` + number + `)` |
| minor-unsupported | `Unsupported MinorVersion ($1)` |
| xml | Expat error string |
| no-document | `No document found` |

Inferred: thrown details are formatted as `{} (at line {}, column {})`.
Corrupt-document is localized key `sErrorDocumentCorruptWhileReading`.
Newer-version is `sErrorDocumentIsFromNewerVersion`, or
`sErrorDocumentIsFromSpecificNewerVersion` when it names a version. The
localized texts are in the opaque `Languages.alp`. The general reading path is
`0x10148389c` → `0x101484108`; the version-aware path is `0x10146c0d4` →
`0x10146c258`.

Revision 2 re-check (2026-10-17), against the N2 run and the
[handoff plan](als-container-handoff-plan.md#findings-while-staging), whose
findings F1 to F5 and inference links I1 to I6 this revision applies:

- F1, F2: `0x1015299e0` disassembly calls `0x10152a900` for MajorVersion at
  `0x101529ca0` and for SchemaChangeCount at `0x101529de8`, in the root branch
  after the name compare (`0x101529c5c`–`0x101529c8c`). The version check
  `0x101529024` is called only for the first child (`0x101529e88`). Its
  disassembly (`0x101529038`–`0x101529130`) orders checks 1–3 and sets the
  newer flag `+0x29` only when MajorVersion ≥ 6; check 4 stores MinorVersion
  at `+0x38`. `0x1015289c8` disassembly (`0x101528a04`–`0x101528a98`) reads
  `+0x29`, `+0x38`, `+0x60`, then `+0x28` and `+0xa0`.
- F1 example with `MinorVersion=""`: left unknown, because whether an empty
  value fails check 2 depends on the string layout inferred from `0x101429854`
  and `0x101432520`; the allocator `0x101449848` is untraced.
- F3: first bytes of `cases/N2-*.als` read 2026-10-17: `1F 8B` for N2-001,
  N2-027 (FLG 0) and N2-021 (FLG 8, FNAME); plain text for the rest.
  [documents.jsonl](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/documents.jsonl):
  25 of 26 shipped `.als` have FLG 0, XFL 2, OS 19, MTIME 0; the default
  template has FNAME.
- F4: n2-0005 `0x101514954.c` forms `<MinorVersion>.txt` and tests existence
  through the resource location (vtable `+0x28`) with no form check. The local
  `Contents/App-Resources/Schema` holds the 203 schema-name files and 203
  AppleDouble `._*.txt` companions (listing 2026-10-17), probably a copy
  artifact; no other entries.
- F5: n2-0002 `0x10148389c` disassembly `0x101483b8c`–`0x101483c1c`: the call
  to `0x101483cec` falls through to a throw of `Can't read a gzip'ed document
  from a non-file` (string `0x105b91508`). The body of `0x101483cec` is not in
  the kept evidence.
- I1 to I6 carry the plan's evidence: I1 the untraced Expat callback catch
  site; I2 the class flag `+0xbe`; I3 converter `0x1002fda78`; I4 shared empty
  string `0x106e0ca98`; I5 the base of `0x101514864` and `0x101514f7c`; I6
  gzip stream object `0x10146208c`.

Corrections relative to the packet's `cases.json`:

- N2-014 is relabelled unknown (was "opens", static-derived), because the
  disassembly of `0x1002fd908` keeps the trailing space.
- N2-015's detail is relabelled unknown (was static-derived).

## Revision and handoff

| Revision | Date | Change |
| --- | --- | --- |
| 1 | 2026-10-17 | First draft from packet N2, written from the retained evidence after the investigator was interrupted; 9 requirements, 27 unexecuted cases |
| 2 | 2026-10-17 | Handoff-author corrections (F1 to F5). REQ-004: general precedence clause replaced by first-refusal-wins with the newer conditions listed; `MajorVersion="6"` with an empty or absent MinorVersion unknown. REQ-003: integer refusals at the root, before the numbered checks. REQ-005: the check is a file-existence lookup; only letters-only values are refused, other non-schema values unknown. REQ-001: start refusals have no specified class (N2-003 to N2-005). Uncompressed fixtures depend on PRB-N2-02. Assumptions I1 to I6 named beside each clause and case that rests on them. Same 27 cases |

Revision 2 itself is not reviewed. The released
[als-container-v1](../../handoff/als-container-v1/README.md) (approved with
narrowing, 35 cases; [handoff plan](als-container-handoff-plan.md)) was built
from revision 1 with these corrections carried. It releases partial
REQ-ALS-CONTAINER-001 to 006 only. REQ-ALS-CONTAINER-007 to 009 and the unknown
clauses stay unreleased until PRB-N2-03 and PRB-N2-05, or equivalent static
traces, settle them.
