---
id: RESEARCH-DOCUMENT-CONTAINER-STATIC
type: research
status: draft
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Document container and version envelope: static evidence

Packet S2, static half, from [roadmap revision 2](native-decompilation-roadmap.md#revision-2-proposal--2026-10-17).
Question: which container, encoding, root attributes and version identifiers do
the documents shipped with 12.4.3 use, and how do they relate to the 203 shipped
schema versions? Everything here was derived from bytes on disk. Nothing was
executed and no loader code was analyzed. The accepted range, error handling and
values written on save stay **unknown** until the native half is done.

## Evidence

Source: [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md), local copy
`/home/ollie/Ableton Live 12 Suite.app`, `Contents/Info.plist` SHA-256
`9b804aa1…ffda29b6d` (`12.4.3 (2026-07-07_e3d8be4d07)`). Image:
`analysis/ableton-live-12.4.3/derived/Live.arm64`, 149,711,904 bytes, SHA-256
`3a99ceea…d1c383cfad`. Retained run: [s2-static-v1](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/manifest.json)
(Python 3.13.9 standard library, `python3 -I`). The manifest lists every command
and the SHA-256 of every script and output. [inputs.jsonl](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/inputs.jsonl)
gives path, size and SHA-256 for all 4,723 parsed files.

| Output | Content |
| --- | --- |
| [documents.jsonl](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/documents.jsonl) | One row per document: magic, gzip header, payload hash, XML declaration, ordered root attributes, root line/byte, first child, well-formedness |
| [summary.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/summary.json) | Per-extension distributions (key = extension) |
| [magic_scan.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/magic_scan.json) | Magic class of every non-AppleDouble file under `App-Resources`, by extension; AppleDouble counts |
| [schemas.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/schemas.json) | All 203 schema headers, ranges, gaps, duplicates, document-to-schema cross-check |
| [binary_headers.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/binary_headers.json) | Byte-level probes of `.alp`, AB1E binaries and one `.amxd` |
| [strings_queries.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/strings_queries.json) | `anchors`: exact C-string and byte anchors with thin-slice offset, section and vmaddr; `phrases`: loader-message search |

Offsets are into the thin arm64 slice. Add 163,741,696 to get offsets in the
universal `Contents/MacOS/Live`. Vmaddrs are unslid: section address plus the
offset delta.

## Inventory correction

Observed: `App-Resources` holds 105,425 regular files. 56,603 of them are
AppleDouble `._*` companions, and each has a real file or directory of the same name. The
[earlier counts](ableton-package-structure.md#serialization-vocabulary-strings-and-shipped-documents--2026-10-17)
included these companions and so doubled every figure. The real counts are 26 `.als`,
350 `.alc`, 2,557 `.adv`, 1,072 `.adg`, 219 `.agr`, 3 `.alp`, 2,189 `.xml` and
580 `.txt` ([magic_scan.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/magic_scan.json)
`appledouble_skipped_by_ext`). Also, no `.agr` is gzip: each one is plain XML or AB1E binary.

## Containers by extension

Observed ([summary.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/summary.json)):

| Ext | Files | Container | Root / first child | MajorVersion · MinorVersion · Creator (count) |
| --- | --- | --- | --- | --- |
| `.als` | 26 | gzip 26 | `Ableton`/`LiveSet` | 5 · `12.0_12402` · 12.4d1 (25); 5 · `12.0_12117` · 12.1d1 (1, `Builtin/Templates/DefaultLiveSet.als`) |
| `.alc` | 350 | gzip 350 | `Ableton`/`LiveSet` | 5 · `12.0_12402` · 12.4d1 (350) |
| `.adv` | 2,557 | gzip 2,556; AB1E1234 1 (`Misc/MidiPreHear.adv`) | `Ableton`/device element (70 names) | 5 · `12.0_12402` · 12.4d1 (2,187); 4 · `9.0_305` · 9.2b1 (369, under `Max/`) |
| `.adg` | 1,072 | gzip 1,072 | `Ableton`/`GroupDevicePreset` | 5 · `12.0_12402` · 12.4d1 (1,071); 4 · `8.1_226` · 8.2.2b4 (1, `Misc/Metronome/Classic.adg`) |
| `.agr` | 219 | plain XML 116; AB1E5678 103 | `Ableton`/`Groove` | 5 · `10.0_377`/`11.0_423`/`11.0_428`/`11.0_432`/`11.0_11300` · 10.1.6–11.3.12 (116) |
| `.ask` | 18 | plain XML 18 | `Ableton`/`Theme` | 5 · `12.0_12120` · 12.1d1 (18) |
| `.cfg` | 3 of 182 | plain XML 2; AB1E5678 1 (`Metadata.cfg`) | `Ableton`/`FallbackLocationsConfig`, `VirtualFolderConfig` | 4 · `9.0_302`/`9.0_299` · 9.0b37/9.0b36 |
| `.alp` | 3 | unidentified | — | — |
| `.amxd` | 110 | `ampf` chunked (not XML) | — | — |
| `.xmp` | 162 | plain XML, no declaration | `x:xmpmeta`/`rdf:RDF` (not the Ableton envelope) | — |

Creator strings are recorded as `Ableton Live <version>`. No other file under
`App-Resources` has gzip magic and decompresses to an `Ableton` root.

**Gzip envelope (all 4,004 members).** Observed: each file is one RFC 1952 member
with CM=8 and no trailing bytes. Python `zlib` (wbits 31) checked CRC32 and ISIZE
on every member, and every check passed. No reserved FLG bits are set. Header
variants:

| Header | Files |
| --- | --- |
| FLG=0, MTIME=0, XFL=2, OS=19 | 3,633: all 12.4d1 content |
| FLG=0, MTIME=0, XFL=2, OS=3 | 369: Max presets |
| FLG=0, MTIME=0, XFL=0, OS=11 | 1: the 8.2.2b4 metronome rack |
| FLG=FNAME (`DefaultLiveSet.als`), MTIME=1737549441 (2025-01-22T12:37:21Z), XFL=0, OS=3, 29-byte header | 1: the default set |

OS=19 is outside the values RFC 1952 defines. Which writer produced it is unknown.

**XML envelope (4,140 `Ableton`-rooted documents).** Observed: none has a BOM.
Line 1 is the declaration and line 2 is the root element. All parse as well-formed
with Expat, and all end in a newline. Every gzip document, every `.ask` and every
`.cfg` uses `<?xml version="1.0" encoding="UTF-8"?>`. The 116 plain `.agr` use single
quotes: `<?xml version='1.0' encoding='UTF-8'?>`. Two files use CRLF:
`Misc/Metronome/Classic.adg` and `FallbackLocations.cfg`. Root attribute order:

- All gzip documents and all `.ask` use `MajorVersion, MinorVersion, SchemaChangeCount, Creator, Revision`.
- The 8.2.2b4 rack and both `.cfg` lack `Revision`.
- `.agr` uses three orders: the canonical order (52), the same order without
  `SchemaChangeCount` (48), and `Creator, MajorVersion, MinorVersion, Revision, SchemaChangeCount` (16).

`Revision` is 40 lowercase hex digits wherever it is present, except in `.ask`,
where it is the empty string. All 3,633 documents from 12.4d1 share
`Revision="42bc084cd8152e4fb737ef3fefd04b2bea5320e7"` and `SchemaChangeCount="1"`.
No other root attributes occur.

## Schema directory and version cross-check

Observed ([schemas.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/schemas.json)):

- **Naming.** All 203 names match `^\d+\.\d+_\d+\.txt$`, written `<family>_<translator>`.
  Families and counts: 8.1 (8), 8.2 (10), 8.3 (1), 9.0 (28), 9.5 (14), 10.0 (25), 11.0 (37), 12.0 (80).
- **Header.** Every file starts with the double-quoted UTF-8 declaration and the
  root `AbletonSchema`.
- **`Version`.** The value is `4` from 8.1_220 through 10.0_348 (63 files) and
  `5` from 10.0_349 on (140 files).
- **Translator attribute.** `TranslatorCount` runs to 11.0_435 (119 files) and
  `TranslatorNumber` starts at 11.0_436 (84 files). In all 203 files the value
  equals the filename suffix.
- **`ChangeCount`.** Present in 129 files and absent in 74.
- **Translator numbers repeat across families.** 270 appears in 8.1, 8.2 and 8.3
  (byte-identical files), 274 in 8.1 and 9.0, 305 in 9.0 and 9.5, and 326 in 9.5 and 10.0.
  In family order the numbers are not monotonic (8.1_274 comes before 8.2_260).
- **Number jumps.** 11.0 jumps from 436 to 11201, and 12.0 numbers run 12000–12402 with gaps.
- **Newest schema.** `12.0_12402` is newest by both orderings: 441,285 bytes, SHA-256 `b7c9d4c7…13789d0f299`,
  412 classes and 7,943 fields. This matches the [earlier capture](native-transport-study.md#evidence-already-available).
- **Document-to-schema match.** Shipped documents use 12 distinct MinorVersions,
  and each one matches a schema file name exactly: `8.1_226`, `9.0_299`, `9.0_302`,
  `9.0_305`, `10.0_377`, `11.0_423`, `11.0_428`, `11.0_432`, `11.0_11300`,
  `12.0_12117`, `12.0_12120`, `12.0_12402`. No document has a MinorVersion without
  a schema; 191 schemas have no shipped document.
- **MajorVersion.** Every document's MajorVersion equals its schema's `Version`
  (17 of 17 (MinorVersion, extension, SchemaChangeCount) groups).
- **SchemaChangeCount.** In all 14 groups where both values exist, the document's
  SchemaChangeCount is at most the schema's ChangeCount. Shipped 12.4d1 content
  has 1 and schema `12.0_12402` has 5. The default set has 10 against 23.

Inferred: MinorVersion is the schema-file key, combining format family and
translator number. MajorVersion tracks the schema `Version` generation. The
`12.0` family prefix spans Live 12.1 and 12.4, so it does not encode the app's
minor version. Unknown: whether 12.4.3 reads `Schema/*.txt` at runtime, and how it
orders versions given that translator numbers repeat across families.

## Non-XML containers (header identification only)

Observed ([binary_headers.json](../../analysis/ableton-live-12.4.3/r2/s2-static-v1/out/binary_headers.json)):

- **`.alp` (`GUI.alp`, `Graphics.alp`, `Languages.alp`).**
  - No recognized signature.
  - Bytes 0–7 vary; bytes 8–11 are zero in all three.
  - All three end with the same 64-byte trailer layout: nonzero bytes only at 61,
    27 and 23 bytes from the end, then 22 zero bytes.
  - Whole-file entropy is 7.24–7.76 bits/byte. Some `Graphics.alp` 64 KiB blocks
    drop to 2.2.
  - Neither zlib nor raw deflate starts at offsets 0–31, and no embedded
    zip/gzip/PNG/XML signatures appear.
  - Interpretation: a proprietary container. Whether it is compressed or
    encrypted is unknown.
- **AB1E binary.**
  - `AB 1E 56 78` begins 103 `.agr` and `Core Library/Ableton Folder Info/Metadata.cfg`.
    `AB 1E 12 34` begins `Misc/MidiPreHear.adv`.
  - Bytes 4–7 of the AB1E5678 files are `03 99 00 00` (64), `03 93` (28),
    `03 8a`/`03 8d` (5 each), `03 8e` (1) and `05 b4 01 00` (Metadata.cfg).
  - Class names follow as 1-byte-length ASCII strings; field names are u32-length
    UTF-16LE strings.
  - Hypothesis, not established: byte 4 is a major version and the next u16 (LE)
    is a translator number. That reads `05 b4 01` as 5/436, which coincides with
    schema 11.0_436. No shipped schema has `Version` 3.
  - The raw-inflate hit at offset 13 of one `.agr` is a false positive, because
    the payload holds plain ASCII names.
- **`.amxd`.**
  - Header: `ampf`, u32 4, a 4-byte type code (`aaaa` 76, `iiii` 20, `mmmm` 10,
    `nagg` 2, `natt` 2), then a `meta` chunk and a `ptch` chunk holding JSON.
  - In the one probed file the `ptch` length equals the file size minus 32.
  - These are Max devices outside the Ableton XML envelope.

The image has both AB1E magics side by side at `__TEXT,__const` `0x105815848`
(offset 92,362,824). They are followed by `Ableton#` in UTF-16BE and then
UTF-16LE. No shipped file starts with `Ableton#`.

## Native string anchors

Observed: every anchor below appears exactly once as a NUL-delimited C string in
`__TEXT,__cstring`. A query starts at each address. Presence shows the bytes
exist; it does not show that the code runs or which code uses them. Because
identical strings are pooled, `Creator` and `Ableton` may also be referenced by
unrelated code: `Creator` sits among browser strings and `Ableton` among
device-loading strings. Tail-merged references are possible, since `Ableton`
occurs as a substring 626 times and `Creator` 543 times.

| Anchor (vmaddr · thin offset) | Text | Query should establish |
| --- | --- | --- |
| `0x105b916e7` · 96016103 | `MajorVersion` | Reader acceptance test; value written on save |
| `0x105b916f4` · 96016116 | `MinorVersion` | Parsing of `<family>_<n>`; comparison with the current translator; value written |
| `0x105b91701` · 96016129 | `SchemaChangeCount` | Whether it is optional (no "missing" message exists, and 48 `.agr` lack it); value written (5?) |
| `0x105b91713` · 96016147 | `Revision` | Value written; whether it is read |
| `0x105be933e` · 96375614 | `Creator` | Value written; whether it is compared |
| `0x105bc92f0` · 96244464 | `Ableton` | Root-name check and emission |
| `0x105b916e0`, `0x105b914eb` · 96016096, 96015595 | `Binary`; `Unknown Compound Stream Type` | Stream-type dispatch (binary, XML, gzip) |
| `0x105b91508` · 96015624 | `Can't read a gzip'ed document from a non-file` | Gzip detection; whether plain XML is accepted for `.als` |
| `0x105b9167e`, `0x105b916a0`, `0x105b9b373`, `0x105b916c1` | `sErrorDocumentCorruptWhileReading`, `sErrorDocumentIsFromNewerVersion`, `sErrorDocumentIsFromSpecificNewerVersion`, `sErrorClassesMissingFromSchema` | Conditions behind each user-facing error key. The localized text is unknown because `Languages.alp` is opaque |
| `0x105b9b360` · 96056160 | `TXmlCompoundParser` | Root of the XML reader call graph |
| `0x105b9b39c` … `0x105b9b596` · 96056220–96056726 | `No document found`; `The document hasn't been created by "`; `MajorVersion attribute missing from 'Ableton' root node`; `MinorVersion attribute missing from 'Ableton' root node`; `Unsupported MajorVersion (`; `Unsupported MinorVersion ($1)`; `Illegal tag format '$1'`; `More than one document in one stream`; `Expected 'Ableton' root node, got '$1' instead`; `Unknown class '$1' encountered`; `The document appears to be corrupt.`; `Unknown attribute '$1'` | Each error's trigger and whether it aborts the load. Per-string offsets are in `anchors` |
| `0x105b9b2b2` · 96055986 | `<?xml version="1.0" encoding="UTF-8"?>` | Declaration written on save |
| `0x105b9af5b`, `0x105b9af69`, `0x105b9b793`, `0x105b9af7a` | `AbletonSchema`, `TranslatorNumber`, `TranslatorCount`, `ChangeCount` | Schema reader; whether both translator attribute forms are accepted |
| `0x105b9af14`, `0x105b9af37`, `0x105b9b719`, `0x105b9b778` | `Live: Finding schema file failed: `, `Live: Reading schema files failed: `, `No schema found`, `Unsupported schema version` | Whether the shipped schema files are read at runtime, and how a MinorVersion selects one |
| `0x105ab0307`, `0x105ab030e` · 95093511, 95093518 | `12.4.3`, `12.0` (adjacent, after `Live`) | Source of the Creator version and the MinorVersion family |
| `0x105bc5587` · 96228743 | `Ableton Live ` | Creator prefix |
| `0x105b6b99b`, `0x105b6b9b2` | `Init: BuildRevisions: `, `e3d8be4d07c71dbd4de9e4183bf90652f680375b` | Candidate `Revision` value. Its prefix matches the Info.plist build `e3d8be4d07` |
| `0x105bac62d`, `0x105bac63f` | `Loading document `, `Loaded document was created by ` | Load logging; the Creator read path |
| `0x105815848`, `0x10581584c` (`__TEXT,__const`) | bytes `ab1e1234`, `ab1e5678` | Whether legacy binary streams are still decoded |

Observed absences: the strings `newer version`, `older version`, `12.0_12402` and
`%d.%d_%d` do not occur, and there is no "missing" message for
`SchemaChangeCount`, `Creator` or `Revision`. These absences show nothing about
behavior.

## Candidate requirements for SPEC-ALS-CONTAINER

Proposed. These are statements about externally observable document bytes, and
each is supported only to the extent stated. "Ships" means the file is present
in 12.4.3. It does not mean 12.4.3 loads that file successfully; that remains a
Phase 4 observation.

| Candidate | Statement | Evidence | Strength |
| --- | --- | --- | --- |
| C-01 | `.als`, `.alc`, `.adv` and `.adg` documents ship as a single gzip member (deflate) holding a UTF-8 XML document | 4,004 of 4,004 gzip files; one AB1E `.adv` exception | Observed for shipped files |
| C-02 | A reader of shipped content must tolerate gzip FLG 0 or FNAME, any MTIME, XFL 0 or 2, and OS 3, 11 or 19 | Header table above | Observed variety |
| C-03 | `.agr`, `.ask` and `Ableton`-rooted `.cfg` documents ship as uncompressed XML | 116 + 18 + 2 files | Observed |
| C-04 | The envelope is an XML 1.0 declaration with encoding UTF-8 and no BOM, then root `Ableton`, whose first child names the document kind (`LiveSet`, `GroupDevicePreset`, a device element, `Groove`, `Theme`, `*Config`) | 4,140 documents | Observed |
| C-05 | Root attributes are MajorVersion, MinorVersion, SchemaChangeCount, Creator and Revision. Shipped documents vary their order and sometimes omit SchemaChangeCount (48) or Revision (3) | `root_attr_order` | Observed. Reader tolerance is inferred and needs native evidence |
| C-06 | MinorVersion has the form `<major>.<minor>_<translator>`, and every shipped value names a file in `Schema/`. MajorVersion equals that schema's `Version` | 12 of 12; 17 of 17 groups | Observed |
| C-07 | Shipped 12.4-era documents carry `5`, `12.0_12402`, `1`, `Ableton Live 12.4d1` and a 40-hex `Revision` | 3,633 files | Observed for content. It is not a 12.4.3 save |
| C-08 | Error taxonomy: missing MajorVersion or MinorVersion, unsupported MajorVersion or MinorVersion, wrong root, multiple documents, illegal tag, unknown class or attribute, corrupt document, newer version, classes missing from schema | Anchor strings | Proposed taxonomy only; triggers and user-visible results are unknown |

Unknown, pending the native loader half and Phase 4:

- Accepted MajorVersion and MinorVersion ranges, including the oldest accepted version.
- Behavior on uncompressed `.als`/`.alc`/`.adv`/`.adg`.
- Behavior on a newer MinorVersion (refuse, warn or load) and the message shown.
- Behavior on a missing or malformed SchemaChangeCount, Creator or Revision, and
  on malformed MajorVersion or MinorVersion.
- Whether Creator is checked, and what `The document hasn't been created by "` tests.
- Whether legacy AB1E and MajorVersion 4 documents load. Two app resources,
  `Misc/Metronome/Classic.adg` and `Misc/MidiPreHear.adv`, suggest they do; this
  is inferred, not observed.
- Values written on save: the gzip header bytes, the declaration, the attribute
  order, and the MajorVersion, MinorVersion, SchemaChangeCount, Creator and
  Revision values. The candidates are `5`, `12.0_12402`, 5,
  `Ableton Live 12.4.3` and `e3d8be4d…`, all unverified.
- The `.alp` structure.

## Native follow-up queries

These run in a persistent Ghidra project of `Live.arm64`, and only after G0.3
saves one. Each query is a reference lookup on an address from the anchors table
followed by decompilation of the caller. Stop a chain at an indirect dispatch and
record it.

1. For `MajorVersion` and `MinorVersion`, list the readers, then follow the
   comparison that leads to `Unsupported MajorVersion (` and
   `Unsupported MinorVersion ($1)`. This gives the accepted range and how
   `<family>_<n>` is parsed.
2. Trace callers of `sErrorDocumentIsFromNewerVersion` and
   `…SpecificNewerVersion` to find the newer-version condition and whether the
   load continues.
3. Trace callers of `Can't read a gzip'ed document from a non-file` and
   `Unknown Compound Stream Type` to find the detection order: gzip magic, XML
   text, and the AB1E table at `0x105815848`.
4. Find the save path from the `<?xml …?>` writer constant and the writers of
   all five root attributes. This gives the emitted order and values, the
   Creator source (`Ableton Live ` with `12.4.3`) and the Revision source
   (`e3d8be4d…`).
5. Find the comparator behind `The document hasn't been created by "`.
6. Trace callers of `SchemaChangeCount`, checking whether a missing value is
   tolerated and how it is compared with the schema ChangeCount.
7. Trace callers of `Live: Finding schema file failed: ` and `No schema found`
   to learn whether `Schema/*.txt` is consulted at runtime and how the file name
   is formed.

## Limitations

Only shipped files were examined. There is no user-saved 12.4.3 document, and
no runtime capture exists. Expat well-formedness was the only check; files were
not validated against the schemas. Text inside documents and strings is treated
as data. The `.alp` probe was bounded to headers and trailers.
