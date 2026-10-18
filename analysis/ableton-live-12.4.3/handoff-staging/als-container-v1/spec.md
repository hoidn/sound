# Live Set container and version envelope, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Feature: FEAT-PERSISTENCE. Parent specification identity:
SPEC-ALS-CONTAINER revision 1. Release: als-container-v1. Only the clauses
explicitly included below are in scope. No other clause of a listed requirement
is implicitly approved. This document is self-contained.

**Status: unreviewed candidate.** This document is not an implementation input
until a separate review approves it and it is published as a release.

## What the contract means

A user opens a Live Set file, or is told that it cannot be opened. This
contract describes how the outer layer of the file decides whether the file is
refused, and how a refusal is classified. It covers:

- recognition of a gzip or an uncompressed XML container from the first bytes;
- the root element;
- the presence, integer syntax and range of the version attributes;
- refusal of documents from a newer version of the application;
- the check that MinorVersion names a shipped schema;
- optional and ignored root attributes.

It does not specify whether a document whose envelope is accepted then opens,
what the user sees after a refusal, or what the application writes on save.

All rules and expected outcomes are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison.

## Terms

| Term | Meaning |
| --- | --- |
| File bytes | The complete stored content of the file |
| gzip file | File bytes whose first two bytes are `1F 8B` |
| Plain XML | Bytes whose first two bytes are `3C 3F` (`<?`) |
| Envelope | The XML declaration, the root element and the root attributes `MajorVersion`, `MinorVersion`, `SchemaChangeCount`, `Creator` and `Revision` |
| Document element | The first child element of the root. In every case of this release it is an empty `LiveSet` element |
| Schema name | A value `<a>.<b>_<c>` in which a, b and c are groups of one to nine ASCII decimal digits, for example `12.0_12402`. The pair (a, b) is its family and c its translator number |
| S | The set of schema names shipped with the target build |

This release does not supply S. The cases rely only on these facts about the
target build: `12.0_12402` and `12.0_12117` are in S, and the largest
translator number among the names of family 12.0 in S is 12402.

## Outcomes and comparison convention

Each case in [cases.json](cases.json) gives one input file and its expected
outcome. The input is read as a Live Set document in a fresh state. The result
is described with two labels:

| Label | Values |
| --- | --- |
| `outcome` | `envelope-accepted`: no rule in this release refuses the file. `refused`: no Live Set document is read from the file |
| `refusal_class` | Only when refused. `corrupt-document`: the document is reported as damaged or unreadable. `newer-version`: the document is reported as created by a newer version of the application. `unspecified`: this release does not specify the class |

Comparison rules:

- `outcome` compares exactly.
- `refusal_class` compares exactly unless the expected value is `unspecified`.
  For `unspecified`, any class or no report matches, provided the file is
  refused.
- Message text, wording, dialogs, logs, named versions and the state after a
  refusal are not compared.
- `envelope-accepted` does not mean that the set opens. Whether a document with
  an accepted envelope opens depends on content outside this release. A
  candidate adapter reports its envelope result separately from any later
  loading of content.
- Each case is independent and starts from a fresh state. No timing applies.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for the
original application.

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-ALS-CONTAINER-001: container recognition (partial)

1. The container is decided from the file bytes, not from the file name or
   extension. All fixtures use the `.als` extension; filtering of files by
   name in a user command is excluded.
2. A gzip file is decompressed. The decompressed content is classified again
   by these same rules, so a gzip file whose content starts with a byte order
   mark is refused like the equivalent uncompressed file. Expectations exist
   only for single-member gzip files with the fixtures' header (see
   [fixture provenance](#fixture-provenance)) and a valid trailer.
3. Plain XML is parsed as XML and then checked against the envelope rules
   below.
4. These files are refused, with an unspecified class:
   - fewer than two bytes;
   - first byte U+0020 space, tab, line feed or carriage return;
   - first byte `<` followed by any byte other than `?`, as when the file
     starts directly with the root element;
   - a UTF-8 byte order mark (`EF BB BF`) followed by `<`.
5. Plain XML content that is not well-formed is refused as `corrupt-document`.
   This also applies when the error comes after a valid envelope and the start of
   the document element, as in a document truncated before the root's end tag.

### REQ-ALS-CONTAINER-002: root element (partial)

1. The root element must be named exactly `Ableton`, with the same letter case.
   Any other name is refused as `corrupt-document`; `Live` and `ableton` are
   refused.
2. A root element with valid attributes and no child element is refused as
   `corrupt-document`.

### REQ-ALS-CONTAINER-003: version attributes and MajorVersion range (partial)

Root attributes are found by their exact, case-sensitive names, in any order.
An attribute whose name differs only in letter case counts as absent.

**Integer attributes.** `MajorVersion` and `SchemaChangeCount` are integer
attributes. Let D be the single digit `0`, or one to nine ASCII digits that do
not start with `0`. A present value is read as follows:

| Present value | Result |
| --- | --- |
| D | the integer D |
| `+` immediately followed by D | the integer D |
| one or more U+0020 spaces, then D | the integer D |
| D, then one or more U+0020 spaces | the integer D |
| empty, or only U+0020 spaces | illegal |
| any character outside ASCII, anywhere in the value | illegal |
| after any leading spaces, `+` immediately followed by `-` | illegal |
| more than 63 characters, all ASCII digits | illegal |
| any ASCII letter, anywhere in the value | illegal |
| any other value | no expectation |

An illegal value of either integer attribute refuses the document as
`corrupt-document`.

**MajorVersion.**

| MajorVersion | Result |
| --- | --- |
| absent | refused, `corrupt-document` |
| illegal | refused, `corrupt-document` |
| integer 0 | refused, `corrupt-document` |
| integer 1 to 3 | refused, `corrupt-document` |
| integer 4 or 5 | passes this check |
| integer 6 or more | refused, `newer-version` (REQ-ALS-CONTAINER-004) |

A MajorVersion of 4 passes with MinorVersion `12.0_12402`.

**MinorVersion presence.** An absent or empty MinorVersion refuses the
document as `corrupt-document`.

### REQ-ALS-CONTAINER-004: newer-version refusal (partial)

1. An integer MajorVersion of 6 or more is refused as `newer-version`, not as
   `corrupt-document`.
2. A MinorVersion that is a schema name not in S is refused as `newer-version`
   when S contains names of its family (a, b) and its translator number c is
   larger than the largest translator number of that family in S. Example:
   `12.0_12403`.

### REQ-ALS-CONTAINER-005: MinorVersion names a shipped schema (partial)

1. A MinorVersion that is in S passes, including the names of older families
   in S. Example: `12.0_12117` with MajorVersion 5.
2. A MinorVersion that consists only of ASCII letters names no schema and is
   refused as `corrupt-document`. Example: `garbage`.

### REQ-ALS-CONTAINER-006: optional and ignored root attributes (partial)

1. `Creator` and `Revision` are optional. Their presence, absence and value do
   not change the outcome; `Creator` may name another application and
   `Revision` need not be hexadecimal.
2. `SchemaChangeCount` is optional. When present it must follow the integer
   rule of REQ-ALS-CONTAINER-003; an illegal value refuses the document as
   `corrupt-document`. A legal value does not by itself cause a refusal.
3. Root attributes with other names are ignored.

### Combined failures

Every case breaks at most one rule. A document that breaks more than one rule
of this release has no expectation.

## Exclusions and deferred obligations

These inputs have **no expectation** in this release:

- leading bytes other than those in REQ-ALS-CONTAINER-001, including the
  formats of other Live documents;
- gzip files other than a single member with the fixtures' header, a valid
  trailer and no trailing bytes; damaged or truncated compressed data; header
  flags and optional header fields;
- plain XML other than the fixtures' form: a declaration other than
  `<?xml version="1.0" encoding="UTF-8"?>`, other encodings, a processing
  instruction in place of the declaration, document type declarations, entity
  or character references in root attributes, namespaces, carriage returns;
- a document element other than `LiveSet`, a second child element of the root,
  and any content inside `LiveSet`;
- integer values marked "no expectation" above, including values with both
  leading and trailing decoration (` 5 `, `+5 `, ` +5 `), a `-` sign not
  preceded by `+`, leading zeros, and ten or more digits within 63 characters;
- MinorVersion values not covered by REQ-ALS-CONTAINER-003 to 005, including
  schema names of a family absent from S (for example `13.0_13000`), schema
  names below the largest translator number of their family but not in S (for
  example `12.0_12050`), digit groups of ten or more digits, and values that
  contain characters other than ASCII letters but are not schema names;
- documents that break more than one rule.

Excluded behavior:

- what the application shows after a refusal: texts, dialogs, any detail or
  named version, logging, and whether a previously open set stays open
  (REQ-ALS-CONTAINER-009, unreleased);
- what is written on save, compressed or not, and the envelope values written
  (REQ-ALS-CONTAINER-007 and 008, unreleased);
- whether a document with an accepted envelope opens, its content, and the
  conversion of older documents;
- which commands (File > Open, the browser, drag and drop) read a file, and any
  filtering by those commands by file name, extension or container, including
  whether they read an uncompressed file at all;
- any effect of `Creator` that does not refuse a document;
- comparison of `SchemaChangeCount` with the named schema, and unknown element
  names inside a document;
- progress, cancellation, timing and undo.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Two obligations are specific
to this release. An `envelope-accepted` observation must show that the file
was not refused by these rules, which may need more than whether the set
opens. A refusal of the uncompressed case ALS-CONTAINER-002 by a command,
before the file is read, is inconclusive rather than a mismatch.
Candidate-only success proves agreement with this contract, not with the
running original.

## Fixture provenance

All 35 fixtures were authored for this release from a template written for it.
The template is a four-line document: the declaration, the root start tag, an
empty `LiveSet` element, and the root end tag. Its root attributes are
`MajorVersion="5" MinorVersion="12.0_12402" SchemaChangeCount="1"
Creator="Ableton Live 12.4.3"` and an invented forty-digit hexadecimal
`Revision`. Each fixture is the template, or the template with the one change
that its purpose states, stored in the container its `container` field names.
Text is UTF-8 with line-feed line endings and a tab before `<LiveSet />`.

gzip fixtures are single-member files. The 10-byte header is
`1F 8B 08 00 00 00 00 00 02 13`: deflate, no flags, zero modification time,
maximum-compression marker and operating-system byte 19. The header is
followed by raw deflate data at maximum compression and the CRC-32 and length
trailer. Nothing follows the trailer.

No fixture contains shipped file content, program code, schema content or
assets. Expected outcomes are newly authored static-derived behavioral data.
No public source or dependency is approved or included. Review status is
recorded in [the manifest](manifest.json).
