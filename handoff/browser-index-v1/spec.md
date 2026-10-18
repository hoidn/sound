# Browser content kinds and tag sidecars, release 1

Target: Ableton Live 12 Suite 12.4.3 (2026-07-07_e3d8be4d07), macOS, Apple
silicon (arm64). Features: FEAT-UI (browser content) and FEAT-PERSISTENCE (tag
sidecars). Parent specification identity: SPEC-BROWSER-INDEX revision 1.
Release: browser-index-v1. Only the clauses explicitly included below are in
scope. No other clause of a listed requirement is implicitly approved. This
document is self-contained.

**Status: reviewed local release.** A separate review approved the clauses
below with the narrowing recorded in [the review disposition](REVIEW.md).

## What the contract means

A user adds a folder of their own to the browser, tags its files and folders,
gives them color labels, and expects the tags to stay with the folder when it
is copied to another computer. This contract describes:

- the content kind that the application assigns to a file from its extension;
- the tag sidecar file of a user folder: which files are read as sidecars, the
  sidecar form covered, how entries bind to the files directly inside the
  folder, and how tags and color labels are read from it;
- the name, location and content of the sidecar that the application writes
  when the user tags an item of a user folder;
- the file names of the sidecars that record the user's tags for items of the
  Core Library and of the built-in content.

It does not specify whether or how files are listed or offered in the browser,
how tags and color labels are presented, when a sidecar is written, previews,
reactions to changes on disk, or the application's own index.

All rules and expected results are **static-derived**: they were derived for
the target build without running it. None is an observed execution of the
original application, and none was run against a candidate. No compatibility
result is established. The original application remains the authority for a
later comparison. Some derived steps rest on assumptions that were not traced
to the end:

- the application reads the sidecar files in a user folder's sidecar folder
  when it indexes that folder, and applies them to the files directly inside
  that folder that it has indexed;
- a file's content kind follows from its lowercase extension alone;
- the tags and color labels of an item are those assigned to that item, not
  ones it shows because of the folder that contains it;
- the sidecars that record the user's tags for factory and built-in content
  are written below the User Library, and for a factory pack the name is
  computed from the pack identifier recorded in that pack's own sidecar;
- sidecar file names are written in lowercase hexadecimal.

The comparison obligations below cover them.

## Terms

| Term | Meaning |
| --- | --- |
| User folder F | A folder on a local APFS volume that the user adds to the browser's places. In each case it contains exactly the entries of the case's fixture folder |
| Item | A file or folder inside F, named by its path relative to F with `/` between levels |
| Sidecar folder | A folder named exactly `Ableton Folder Info`, in this letter case |
| User-folder sidecar name | `dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` |
| F's sidecar | The file `F/Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` |
| Tag | A text whose levels are separated by `\|`, for example `Character\|Bright`. Every tag in this release has two levels |
| Color label | One of seven numbered labels, 1 to 7, which an item may carry in any combination |
| Content kind | The class of browser content that the application assigns to a file. The kind labels in this release are project labels, not names used by the application |
| User Library | The application's User Library folder |
| Core Library | The library of factory content installed with the target build |
| Built-in content | The application's built-in devices as they appear in the browser, for example a device folder |

Namespaces, identified by URI and not by prefix:

| Prefix used here | Namespace URI |
| --- | --- |
| `x` | `adobe:ns:meta/` |
| `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` |
| `dc` | `http://purl.org/dc/elements/1.1/` |
| `ablFR` | `https://ns.ableton.com/xmp/fs-resources/1.0/` |
| `xmp` | `http://ns.adobe.com/xap/1.0/` |

## Preconditions

For every case with a fixture folder: the application has not indexed F
before, the User Library exists, and F is added as a user folder after its
fixture content is in place. Results are observed after the application has
finished indexing F. No timing applies. Each case is independent and starts
from this state.

## Results and comparison convention

Each case in [cases.json](cases.json) gives its input, any user action, and
the expected result, described with these labels:

| Label | Values |
| --- | --- |
| `content_kind` | For each file name, one kind label of REQ-BROWSER-INDEX-001, or `none` (no content kind) |
| `tags` | For each listed item, the set of tags assigned to it |
| `labels` | For each listed item, the set of color label numbers assigned to it |
| `sidecar` | The data model of a written sidecar, defined below |

The identifiers BROWSER-INDEX-016 and 017 are not used in this release.

**Sidecar data model.** The data model of a sidecar consists of:

- its document-level properties in the `dc` and `ablFR` namespaces other than
  `ablFR:items`, each with its text;
- the multiset of its item entries. An item entry consists of its
  `ablFR:filePath` text and the multisets of its `ablFR:keywords`,
  `ablFR:colors` and `ablFR:hideKeywords` entries.

An absent property and an empty `rdf:Bag` are equivalent. Whitespace,
prefixes, the order of properties and of Bag entries, the serialization form,
any packet wrapper or XML declaration, attributes of `x:xmpmeta`, properties
in any other namespace (such as `xmp:CreatorTool`, `xmp:CreateDate` and
`xmp:MetadataDate`), and the item fields `ablFR:assetId` and
`ablFR:contentHash`, if present, are not part of the data model.

Comparison rules:

- `content_kind` compares exactly for each file name.
- `tags` and `labels` compare as sets, for the items a case lists. Items a case
  does not list are not judged.
- For a write case, the data model of the file at `sidecar_path`, relative to
  F, compares exactly with the expected data model. The case's
  `expected-sidecar.xmp` is one serialization of that data model, in the form
  of REQ-BROWSER-INDEX-004.
- For the two cases on factory and built-in content, the file name compares
  exactly, and the file must lie directly inside a folder that is directly
  inside `<User Library>/Ableton Folder Info/`. The name of that folder and
  the file's content are not compared. No sidecar file inside the Core
  Library or the built-in content, as the case names, is created or changed.
- A write case in which the expected file is absent when observed is
  inconclusive, because write timing is outside this release.
- Message text, dialogs, logs and listings are not compared.

This is a **project comparison representation**, not an API claimed to exist
in Live and not a required design. A candidate adapter may translate its own
result into these labels. The fixture set is not an executable harness for the
original application.

## Selected requirement clauses

Each clause below is included only as stated.

### REQ-BROWSER-INDEX-001: content kind by extension (partial)

1. A file's content kind is decided by its extension. For the lowercase
   extensions in this table, the kind is:

   | Kind label | Extensions |
   | --- | --- |
   | clips | `.alc` |
   | live presets | `.adv`, `.adg` |
   | grooves | `.agr` |
   | Max devices | `.amxd`, `.amp` |
   | REX files | `.rex`, `.rcy`, `.rx2` |
   | other audio | `.wav`, `.aif`, `.aiff`, `.ams`, `.sd2`, `.mp7`, `.eflac`, `.wv`, `.bwf`, `.rf64` |
   | encoded audio | `.mp3`, `.ogg`, `.flac` |
   | Windows Media audio | `.wma` |
   | MPEG-4 audio | `.m4a` |
   | video | `.mov`, `.avi`, `.dv`, `.mp4`, `.m4v`, `.wmv`, `.mpg`, `.m2v` |
   | images | `.bmp`, `.pcx`, `.tif`, `.tiff`, `.jpg`, `.jpeg`, `.png` |
   | plug-in presets | `.aupreset`, `.vstpreset` |
   | other files | `.als`, `.abl`, `.ablbundle`, `.alp`, `.mid`, `.midi`, `.scl`, `.ascl`, `.stacks`, `.appc`, `.sf`, `.sf2`, `.gig`, `.exs`, `.nki`, `.toast`, `.iso` |
   | none | `.asd`, `.xmp`, `.cfg`, `.txt`, `.json`, `.xml`, `.ini`, `.zip`, `.gz`, `.py`, `.log`, `.lng`, `.ask`, `.fxp`, `.fxb`, `.ablpresetbundle`, `.auz`, `.idx`, `.db`, `.lock`, `.dmp`, `.aad`, `.ard`, `.band`, `.exe`, `.com` |

2. A file with an extension in the `none` row has no content kind. This
   includes `.fxp`, `.fxb` and `.ablpresetbundle`.
3. The file's content does not take part. The classification cases therefore
   give file names only.

Whether a file with or without a kind is listed or offered in any browser view
is not part of this release.

### REQ-BROWSER-INDEX-003: which sidecar files are read (partial)

1. A file inside F whose parent folder is not named exactly
   `Ableton Folder Info` is not read as a sidecar, whatever its name and
   extension.
2. F's sidecar is read when F is indexed. It describes the files directly
   inside F (REQ-BROWSER-INDEX-005).

User folders inside the User Library are outside this release.

### REQ-BROWSER-INDEX-004: sidecar form (partial)

1. The form covered is an XMP document of this shape: a root element
   `x:xmpmeta` containing `rdf:RDF`, which contains a single
   `rdf:Description` with `rdf:about=""`. Its document-level properties are
   `dc:format` with the text `application/vnd.ableton.folder`,
   `ablFR:resource` with the text `folder`, `ablFR:platform` with the text
   `mac`, and `ablFR:items`. `ablFR:items` holds one `rdf:Bag`. Each of its
   `rdf:li` entries has `rdf:parseType="Resource"` and contains
   `ablFR:filePath` and, optionally, `ablFR:keywords` and `ablFR:colors`, each
   holding one `rdf:Bag` of `rdf:li` text entries. Properties are written as
   elements. The text is UTF-8, with line feeds, without an XML declaration
   and without a packet wrapper. The sidecar of case BROWSER-INDEX-012 is an
   example.
2. Document-level properties in the `xmp` namespace, such as `xmp:CreatorTool`,
   `xmp:CreateDate` and `xmp:MetadataDate`, are informational. They do not
   change any item's tags or color labels.
3. A sidecar that is not well-formed XML gives no tags and no color labels.
   Other effects, such as a message, are not part of this release.
4. A sidecar that the application writes for a user folder has the
   document-level properties of clause 1 (REQ-BROWSER-INDEX-007).

### REQ-BROWSER-INDEX-005: item binding (partial)

1. An entry whose `ablFR:filePath` is exactly the name of a file directly
   inside F, the folder that contains the sidecar folder, applies to that
   file.
2. An entry whose path names nothing in F is skipped. It does not change the
   tags or color labels of other items.

Entries whose path contains `/` or names a folder, and the tags of items
inside a subfolder of F, are outside this release.

### REQ-BROWSER-INDEX-006: tag and color label values (partial)

1. Each `ablFR:keywords` entry of an item's entry gives the item that tag, with
   its exact text. The item's tags are the set of these texts.
2. Each `ablFR:colors` entry whose text is exactly one of `1`, `2`, `3`, `4`,
   `5`, `6` or `7` gives the item the color label of that number. Entries
   whose text is `0` or `8`, and empty entries, are ignored.
3. When the application writes an item's color labels, it writes one
   `ablFR:colors` entry per label, with the decimal text `1` to `7`, in
   ascending order. The comparison does not judge the order.

### REQ-BROWSER-INDEX-007: where the user's tags are written (partial)

1. When the user sets the tags or color labels of an item that lies directly
   inside F, and F has no sidecar folder, the application records the item's
   complete tag and color label state in F's sidecar. It creates the sidecar
   folder.
2. The written sidecar's data model has the document-level properties
   `dc:format` = `application/vnd.ableton.folder`, `ablFR:resource` = `folder`
   and `ablFR:platform` = `mac`, and one item entry. The entry's
   `ablFR:filePath` is the item's name. Its `ablFR:keywords` entries are the
   item's tags and its `ablFR:colors` entries are its color labels, written as
   in REQ-BROWSER-INDEX-006. A property whose set is empty is absent or an
   empty `rdf:Bag`.
3. When the user sets the tags of an item of the Core Library, the application
   records them in a file named `b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp`.
   The file lies in a folder that is directly inside
   `<User Library>/Ableton Folder Info/`, and that folder's name is the
   decimal text of an integer that this release does not specify. No sidecar
   is written inside the Core Library. The name follows a general rule for an
   installed factory pack whose own sidecar records the pack identifier P in
   `ablFR:packUniqueId`: the name-based UUID of version 5 (SHA-1, as defined
   in RFC 9562) of the UTF-8 text P in the namespace UUID
   `c55d131f-2661-5add-aece-29afb7099dfa`, in lowercase hexadecimal with
   hyphens, followed by `.xmp`. The Core Library's pack identifier is
   `www.ableton.com/0`. Only the Core Library has a case.
4. When the user sets the tags of an item of the built-in content, the
   application records them in a file named
   `b769aafb-73f9-57e9-8dba-740d64be2541.xmp`, in a folder of the kind
   described in clause 3. No sidecar is written inside the built-in content.

### REQ-BROWSER-INDEX-008: tags travel with a copied folder (partial)

1. A folder copied together with its sidecar folder and added as a user folder
   on another installation, which has not indexed it, has the tags and color
   labels that its sidecar records, by the rules of REQ-BROWSER-INDEX-003 to
   006.

### Combined conditions

Each fixture folder has at most one sidecar, and each case exercises one rule
of this release beside those every read case relies on. Inputs that combine
conditions this release excludes have no expectation.

## Exclusions and deferred obligations

Requirements not released: **REQ-BROWSER-INDEX-002** (the kinds of indexed
locations and unavailable locations), **REQ-BROWSER-INDEX-009** (previews),
**REQ-BROWSER-INDEX-010** (changes while the application runs),
**REQ-BROWSER-INDEX-011** (missing, moved and unavailable items),
**REQ-BROWSER-INDEX-012** (unsupported and undecodable files) and
**REQ-BROWSER-INDEX-013** (the index and its rebuild).

These inputs have **no expectation** in this release:

- extensions not in the REQ-BROWSER-INDEX-001 table, including other extensions
  the application recognizes; extensions with upper-case letters; names without
  an extension; folders, device folders and plug-ins;
- sidecar folders with another letter case; sidecar folders below F; files
  with any other name in F's sidecar folder; any other location of a sidecar;
- sidecar text in another form than REQ-BROWSER-INDEX-004 clause 1: a packet
  wrapper, an XML declaration, another encoding, attribute or other
  alternative RDF forms, carriage returns, unknown properties, document-level
  tags or labels, and `ablFR:hideKeywords`, `ablFR:assetId` or
  `ablFR:contentHash` in input;
- a resource, format or platform other than `folder`,
  `application/vnd.ableton.folder` and `mac`;
- a `filePath` that differs from an item only in letter case, absolute paths,
  `.` or `..` levels, `\` separators, or a trailing `/`; a `filePath` that
  contains `/` or names a folder; the tags and labels of items inside a
  subfolder of F;
- color entries other than exactly `1` to `7`, `0`, `8` or empty; keyword
  entries that are empty, repeated, of one level, or of four or more levels;
  leading or trailing spaces in any value;
- the tags and labels of items inside a tagged folder; more than one sidecar
  for the same folder;
- edits to items inside a subfolder of F; edits when F already has a sidecar
  folder; edits that leave an item with no tags and no labels; read-only
  volumes; a missing User Library.

Excluded behavior:

- whether and how files and folders are listed or offered in any browser view
  or category, including files without a content kind and the sidecar folder
  itself;
- how tags and color labels are presented, grouped, searched or filtered;
- when a sidecar is written after an edit, any batching, and what happens on
  quit;
- the name of the folder between `Ableton Folder Info` and the sidecars for
  factory and built-in content, their content, and how they are read;
- whether other entries of an existing sidecar are kept when it is rewritten,
  and whether the application rewrites a sidecar after reading it, for example
  without the entries that name no file;
- previews, changes on disk, missing or moved items, unavailable locations,
  unsupported or undecodable files, and the application's index
  (requirements not released, above);
- messages, logs and dialogs, undo, progress and timing.

Before claiming reference compatibility, a separately designed bounded probe
must run these cases, or a justified equivalent set, against the original. It
must pin the original and candidate builds and the fixture bytes, retain
independent observations, and report mismatches. Obligations specific to this
release:

- A `content_kind` observation must show which kind the original assigns to
  each file, through a channel that distinguishes the kinds of this release,
  such as a browser view or filter that selects files by kind. Designing that
  channel is part of the probe. A comparison that the chosen channel cannot
  decide is inconclusive. Absence of a file from a view is not an observation
  of `none`, because whether files are listed is outside this release.
- A `tags` or `labels` observation must read the tags and labels assigned to
  the item itself, and must identify each color label by its number. If the
  presentation does not identify the number, that comparison is inconclusive.
  If the original does not present the item, the comparison is inconclusive;
  absence from a view is not an observation of an empty set.
- A write case is observed after the edit and after the application has quit
  normally. If the original does not offer the item for the edit, the case
  is inconclusive. An absent file is inconclusive; a present file whose data
  model differs is a mismatch.
- The cases on factory and built-in content use the target's own installed
  Core Library and built-in content. They do not need, and this package does
  not supply, any copy of that content.

Candidate-only success proves agreement with this contract, not with the
running original.

## Fixture provenance

All fixtures were authored for this release. Each case with a fixture folder
has its own folder `fixtures/<case ID>/F`, which is copied as F. The
classification cases 001 to 011 have no fixture files.

- Every `.wav` file is a 60-byte RIFF/WAVE file: PCM, one channel,
  44,100 Hz, 16 bits, eight zero samples.
- Every sidecar comes from one template written for this release, in the form
  of REQ-BROWSER-INDEX-004 clause 1, with one space of indentation per level.
  The **base sidecar** has one item entry, `a.wav`, with the tag
  `Character|Bright`. The sidecar fixtures are:

  | Cases | Location in F | Content |
  | --- | --- | --- |
  | 012, 028 | F's sidecar | the base sidecar |
  | 013 | `Tags/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` | the base sidecar |
  | 014 | F's sidecar | the base sidecar plus `xmp:CreatorTool`, `xmp:CreateDate` and `xmp:MetadataDate` |
  | 015 | F's sidecar | the first half of the base sidecar's bytes |
  | 018 | F's sidecar | the base entry plus an entry `gone.wav`, tag `Type\|Loop` |
  | 019 | F's sidecar | the base entry with colors `2`, `5` |
  | 020 | F's sidecar | the base entry with colors `0`, `8`, `3` and an empty entry |
  | 021 | F's sidecar | the base entry with colors `1` to `7` |
  | 022 | F's sidecar | one entry, `a.wav`, tags `Character\|Bright`, `Character\|Warm`, `Genres\|Ambient` |
- In the write cases 023 to 025, F holds only `a.wav`, and
  `expected-sidecar.xmp` is one serialization of the expected data model in
  the same form.

Tag texts are short words chosen for the cases; some also occur as tag names
in factory content, and no expectation depends on the text. The three sidecar
file names and the Core Library's pack identifier are values used by the
target build. No fixture contains shipped file content, program code or
assets. Expected results are newly authored static-derived behavioral data.
No public source or dependency is approved or included; RFC 9562 is named only
to identify the UUID version. Review status is recorded in
[the manifest](manifest.json) and [the review disposition](REVIEW.md).
