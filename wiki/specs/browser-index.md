---
id: SPEC-BROWSER-INDEX
type: spec
status: draft
updated: 2026-10-17
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3 / macOS
---

# Browser content index and tag sidecars

## Scope

Features: FEAT-UI (browser content) and FEAT-PERSISTENCE (tag and color-label
sidecars) in the [feature map](feature-map.md). The user task is to browse files
in the application's content locations and in user-added folders, see previews,
tag items and give them color labels, and keep those tags when the browser's
index is rebuilt or the folder is copied elsewhere. The draft covers:

- which files are offered as browser content, by extension and content kind;
- the location kinds that are indexed;
- the tag sidecar file (`Ableton Folder Info/*.xmp`): which files are read, their
  format, how entries bind to items, and where user edits are written;
- how a preview file is associated with an item;
- reactions to added, renamed, deleted, moved, unavailable and unsupported files;
- rebuilding the index.

Excluded: search matching, sound-similarity and automatic tags, use counts as a
displayed value, folder property files (`Properties.cfg`), virtual folders,
pack installation, plug-in discovery (see SPEC-PLUGIN-DISCOVERY), and
redirection of sample references when a Live Set loads (FEAT-PERSISTENCE media
references). The index's own storage is internal: an implementation need not
read, write or reproduce it. The sidecar file is an interchange format and is in
scope.

The requirements are **proposed behavioral contracts** derived from static
reading of the 12.4.3 program and its shipped files. No requirement was observed
in a running Live, and no Ableton documentation was consulted for this draft, so
no clause is labeled documented. Under
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) a static derivation
can support a draft, but it is never a measured result.

## Evidence labels

| Label | Meaning |
| --- | --- |
| Documented | Stated in shipped documentation. No clause in this revision has this label |
| Static-derived | Follows from the program's code and shipped files as read, without execution; any assumption is stated beside the clause |
| Unknown | Not decided by the evidence. Has no expected output and blocks release of that clause; the probe ID names the planned observation |

## Terms and common preconditions

- *Location*: a root the browser indexes (REQ-BROWSER-INDEX-002).
- *User folder F*: a folder on a local APFS volume added to the browser's places,
  containing only the entries a case lists. Unless a case says otherwise the
  application starts with no index, no sidecar in F, and an existing User
  Library.
- *Item*: a file or folder inside a location.
- *Listed*: shown as an entry when F is selected in the browser.
- *Sidecar folder*: a folder named exactly `Ableton Folder Info`.
- *Folder sidecar name*: `dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp`.
- *Tag*: a text path whose levels are separated by `|`, for example
  `Character|Bright`.
- *Color label*: one of seven numbered labels, 1 to 7, that an item may carry in
  any combination. Their presentation in the browser is unknown.

**Fixture A** (a folder sidecar; cases name changes relative to it):

```xml
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:ablFR="https://ns.ableton.com/xmp/fs-resources/1.0/">
   <dc:format>application/vnd.ableton.folder</dc:format>
   <ablFR:resource>folder</ablFR:resource>
   <ablFR:platform>mac</ablFR:platform>
   <ablFR:items>
    <rdf:Bag>
     <rdf:li rdf:parseType="Resource">
      <ablFR:filePath>a.wav</ablFR:filePath>
      <ablFR:keywords>
       <rdf:Bag><rdf:li>Character|Bright</rdf:li></rdf:Bag>
      </ablFR:keywords>
     </rdf:li>
    </rdf:Bag>
   </ablFR:items>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
```

Media files in cases are valid files of the named type unless the case says
otherwise; their content does not matter except in REQ-BROWSER-INDEX-012.

## Requirements

### REQ-BROWSER-INDEX-001 — content kind by extension

Each file in a location is classified by its extension into one content kind, or into none; a file with no content kind is not offered as browser content.

| Content kind | Extensions |
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
| others | `.als`, `.abl`, `.ablbundle`, `.alp`, `.mid`, `.midi`, `.scl`, `.ascl`, `.stacks`, `.appc`, `.sf`, `.sf2`, `.gig`, `.exs`, `.nki`, `.toast`, `.iso` |
| no kind | `.asd`, `.xmp`, `.cfg`, `.txt`, `.json`, `.xml`, `.ini`, `.zip`, `.gz`, `.py`, `.log`, `.lng`, `.ask`, `.fxp`, `.fxb`, `.ablpresetbundle`, `.auz`, `.idx`, `.db`, `.lock`, `.dmp`, `.aad`, `.ard`, `.band`, `.exe`, `.com` |

Folders are classified separately as device folders or other folders; plug-ins
form their own kind without an extension.

- **Static-derived.** The table above, for the registered extensions.
- **Static-derived (assumes the browser lists files through a content-kind
  filter, inferred from named kind sets in the program).** Files of no kind are
  not listed. This includes `.fxp`, `.fxb` and `.ablpresetbundle`, which a
  reader may not expect; PRB-BI-01 should confirm it.
- **Static-derived.** The program's named default content set contains every
  file kind above and excludes device folders, other folders and plug-ins. Which
  set each browser view uses is unknown (PRB-BI-01).
- **Unknown.** Whether the four audio kinds, video and images are listed in a
  user folder; extension case (`A.WAV`); files without an extension; files with
  an unregistered extension; `.ablx`, which is registered but has no kind
  (PRB-BI-01, PRB-H2-09).
- **Unknown.** Which sidebar categories list which kinds (PRB-BI-02).

### REQ-BROWSER-INDEX-002 — indexed locations

The browser indexes built-in content, factory packs (including the Core Library), the User Library, user-added folders, the current project, managed folders, legacy pack data and a cloud folder; a location that cannot be reached is remembered as unavailable instead of being removed.

- **Static-derived.** The list of location kinds and the record of unavailable
  locations.
- **Unknown.** Names, order and presentation in the browser; when the current
  project location changes; how an unavailable location is shown (PRB-BI-02,
  PRB-H2-05).

### REQ-BROWSER-INDEX-003 — which sidecar files are read

A file with extension `.xmp` is read as a tag sidecar when its parent folder is named `Ableton Folder Info`, or when it lies in the User Library's override folder (REQ-BROWSER-INDEX-007); a sidecar in `<R>/Ableton Folder Info/` describes items of `<R>`.

- **Static-derived.** The parent-name test. An `.xmp` elsewhere is not read as a
  sidecar, and `.xmp` files are never listed (REQ-BROWSER-INDEX-001).
- **Static-derived (assumes the files of a sidecar folder are enumerated; the
  enumeration was not traced).** A sidecar with the folder sidecar name in
  `F/Ableton Folder Info/` is read. All three shipped naming families (built-in,
  Core Library, legacy packs; appendix) pass the parent-name test.
- **Unknown.** Whether every `.xmp` in a sidecar folder is read or only the
  expected names; whether a sidecar folder below a location root applies;
  case sensitivity of `Ableton Folder Info`; whether the sidecar folder itself is
  listed (PRB-BI-03, PRB-BI-01).

### REQ-BROWSER-INDEX-004 — sidecar format

A sidecar is an XMP document (RDF/XML in `x:xmpmeta`) whose single `rdf:Description` uses the namespace `ablFR = https://ns.ableton.com/xmp/fs-resources/1.0/` with these properties:

| Property | Level | Value |
| --- | --- | --- |
| `ablFR:resource` | document | `folder`, `pack`, `plugin` or `app-builtin` |
| `dc:format` | document | `application/vnd.ableton.folder`, `.factory-pack`, `.plugin-device` or `.app-builtin`, paired with the resource in that order |
| `ablFR:platform` | document | `mac`, `win` or `linux` |
| `ablFR:packUniqueId`, `ablFR:packVersion` | document, packs | text |
| `ablFR:deviceId` | document, plug-ins | text |
| `ablFR:items` | document | `rdf:Bag` of items, each `rdf:parseType="Resource"` |
| `ablFR:filePath` | item | relative path (REQ-BROWSER-INDEX-005) |
| `ablFR:keywords` | item | `rdf:Bag` of tags |
| `ablFR:hideKeywords` | item | `rdf:Bag` of tags |
| `ablFR:colors` | item | `rdf:Bag` of color-label numbers |
| `ablFR:assetId`, `ablFR:contentHash` | item | text; meaning unknown |
| `xmp:CreatorTool`, `xmp:CreateDate`, `xmp:MetadataDate` | document | informational |

- **Static-derived.** The property set, the value sets and the pairing of
  resource and format. All 162 shipped sidecars conform. They carry no
  `<?xpacket?>` wrapper, and none uses `colors`, `assetId` or `contentHash`.
- **Static-derived.** A sidecar that cannot be parsed contributes no tags.
  Other effects, such as a message, are unknown (PRB-BI-03).
- **Unknown.** Effects of `platform` `win` or `linux` (for example on path
  separators); acceptance of an `xpacket` wrapper; unknown properties; a
  resource that does not match its format; tags or colors at document level
  (PRB-BI-03).

### REQ-BROWSER-INDEX-005 — item binding

An item's `filePath` is relative to the folder that contains the sidecar folder, uses `/` separators, and may name a file or a folder at any depth; an entry naming nothing on disk is ignored.

- **Static-derived.** The resolution rule. In shipped content, 7,084 of 7,085
  entries in active locations resolve. The 85 built-in entries name folders.
- **Static-derived (assumes the shipped built-in sidecar, which has one
  unresolved entry, loads without error).** Unresolved entries are ignored
  without an error.
- **Unknown.** Case-insensitive matching; absolute paths, `..` segments and `\`
  separators (PRB-BI-03).

### REQ-BROWSER-INDEX-006 — tag and color values

Each `keywords` entry gives the item that tag; each `colors` entry with a decimal value 1 to 7 gives the item that color label, and other numeric or empty entries are ignored.

- **Static-derived.** The color rule. A writer emits one entry per label, in
  ascending order, as `"1"` to `"7"`.
- **Static-derived (shipped content).** Factory tags have 2 or 3 levels. Their
  first levels are `Drums`, `Sounds`, `Type`, `Character`, `Key`, `Genres`,
  `Clips`, `Devices`, `Grooves` and `Tunings`.
- **Unknown.** Whether an item tagged `A|B` is found under `A`; tags of 1 or of 4
  or more levels; duplicate tags; a non-numeric color value, which may reject the
  whole sidecar; the meaning of `hideKeywords` (PRB-BI-02, PRB-BI-03,
  PRB-BI-04).

### REQ-BROWSER-INDEX-007 — where user edits are written

When the user changes an item's tags or color labels, the application records the item's complete tag state in a sidecar: for an item in a user folder F, in `F/Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp`; for an item in factory or built-in content, in the User Library and never in the factory content.

- **Static-derived.** The user-folder sidecar's name and location. A new
  sidecar has `ablFR:resource` `folder`, `dc:format`
  `application/vnd.ableton.folder` and an `ablFR:platform` value (`mac` on macOS
  is inferred). The item
  entry's `keywords`, `hideKeywords`, `colors`, `assetId` and `contentHash` are
  replaced as a whole. A color label is written as in REQ-BROWSER-INDEX-006.
- **Static-derived.** Factory and built-in edits go to
  `<User Library>/Ableton Folder Info/<n>/<name>.xmp`. For a pack, `<name>` is
  the name-based UUID (version 5) of the pack's `packUniqueId` under the
  namespace UUID `c55d131f-2661-5add-aece-29afb7099dfa`; for the Core Library
  (`www.ableton.com/0`) this is `b17d447d-894d-5b3e-96e9-a81dbf4d431c`. For
  built-in content `<name>` is `b769aafb-73f9-57e9-8dba-740d64be2541`. These
  edits are not written when no User Library exists. Plug-in tags use the same
  folder with a name derived from the plug-in's identity.
- **Unknown.** `<n>`, a decimal number the application supplies. When the write
  happens (on each edit, batched, or at quit). Whether a nested item `F/sub/a.wav`
  is recorded in F's sidecar or in `F/sub`'s. Whether other entries in an
  existing sidecar are kept unchanged. Behavior on a read-only volume. What the
  user sees when nothing can be written. (All PRB-H2-04.)

### REQ-BROWSER-INDEX-008 — tags survive an index rebuild

Tags and color labels recorded in sidecars reappear after the index is rebuilt and when a folder with its sidecar folder is added on another installation, because building the index reads sidecars (REQ-BROWSER-INDEX-003 to 006).

- **Static-derived.** Building the index includes reading sidecars. A folder
  copied with its sidecar folder therefore keeps its tags (case BI-071).
- **Unknown.** Whether an edit made before a rebuild has always reached its
  sidecar (REQ-BROWSER-INDEX-007 timing). Whether data kept only in the index,
  such as use counts, survives (PRB-H2-04, PRB-H2-06).

### REQ-BROWSER-INDEX-009 — preview association

The preview of an item at relative path `p` in location `R` is the first existing file among `R/Ableton Folder Info/Previews/p.aif`, `p.wav`, `p.ogg` and `p.mp3`, where `p` keeps the item's own extension.

- **Static-derived.** The rule and its order. Shipped content follows it: 2,563
  previews in the Core Library, all `.ogg` (893 `.adg`, 1,101 `.adv`, 219 `.agr`
  and 350 `.alc` items), each with a `.ogg.asd` companion. Every one names an
  existing item.
- **Unknown.** Whether `R` is the location root or the nearest folder holding a
  sidecar folder; whether the browser plays the preview file instead of the item
  itself, and for which kinds; the role of the `.asd` companion (PRB-BI-05).

### REQ-BROWSER-INDEX-010 — changes while running

Files added, renamed or deleted in a location while the application runs are reflected in the browser without a restart; locations on volumes that do not deliver file-system change events are rescanned in full.

- **Static-derived.** Change notification per folder; handling of volume mount
  and unmount; the full-rescan fallback.
- **Unknown.** Latency, coalescing and ordering; whether a rename keeps tags;
  when a full rescan runs (PRB-H2-03, PRB-H2-05).

### REQ-BROWSER-INDEX-011 — missing, moved and unavailable items

An item that no longer exists is removed from the browser, together with everything under it if it is a folder, rather than shown as missing; an unreachable location is kept as unavailable (REQ-BROWSER-INDEX-002).

- **Static-derived.** Removal on detection, with descendants.
- **Unknown.** When detection happens for changes made while the application was
  not running; whether tags and color labels follow a moved or renamed item (its
  sidecar entry keeps the old path unless rewritten; the role of `contentHash` is
  unknown); presentation of an unavailable location (PRB-H2-05).

### REQ-BROWSER-INDEX-012 — unsupported and undecodable files

No browser behavior is established for files with an unregistered extension or for files of a content kind whose content cannot be decoded.

- **Unknown (static reading suggests: unregistered extensions not listed,
  undecodable files listed because classification uses the extension).** The
  listing and error presentation of truncated, zero-length or corrupt files, and
  of unregistered extensions (PRB-H2-09, PRB-BI-01).

### REQ-BROWSER-INDEX-013 — index rebuild

The index is a rebuildable cache: it is created when missing, recreated when it records a newer or unrecognized version or another platform, upgraded in place from an older version, and rebuilt at the next start after corruption is detected; a rebuilt index is derived from the files on disk and their sidecars.

- **Static-derived.** The five outcomes. If the application cannot record that
  corruption was found, the index is not rebuilt at the next start.
- **Unknown.** Messages, progress display and duration; whether a truncated
  index found at start is treated as corrupt; whether anything other than
  sidecar data survives (PRB-H2-06).

## Timing and state

No timing is established. Latencies of change reflection (REQ-BROWSER-INDEX-010)
and of sidecar writes (REQ-BROWSER-INDEX-007) are unknown and have no tolerance
yet. Persistent state in scope is the sidecar file. The index is a cache
(REQ-BROWSER-INDEX-013), and its loss must not lose sidecar data. Whether tag
and color edits are undoable is unknown. Interactions:

- Live Set saving does not write sidecars (no evidence links them).
- A preview is associated by path only (REQ-BROWSER-INDEX-009).
- Editing a sidecar while the application runs is not covered (no evidence).

## Errors, cancellation and teardown

An unreadable sidecar contributes no tags (REQ-BROWSER-INDEX-004). A missing
User Library suppresses factory-content tag writes (REQ-BROWSER-INDEX-007). Index
corruption leads to a rebuild at the next start (REQ-BROWSER-INDEX-013). No
cancellation affordance for tag edits is established; quitting right after an edit
is the teardown case BI-067.

## Acceptance cases

None of these cases has been run against Live or a candidate. "Expected" is a
static derivation or is explicitly unresolved; it is not an observation.
Comparators:

- Listings are compared as sets of names.
- An item's tags and color labels are compared as sets.
- Sidecar files are compared as RDF graphs: Bag entries as multisets, ignoring
  whitespace, namespace prefixes, `xmp:CreatorTool`, `xmp:CreateDate` and
  `xmp:MetadataDate`. They are not compared as bytes.

Fixtures are the folder layouts and sidecar texts in the setup column; Fixture A
is above.

| Case ID | Requirement | Case kind | Setup/action | Expected result | Label |
| --- | --- | --- | --- | --- | --- |
| BI-001 | 001 | positive | F: `a.wav`, `b.aif`, `c.alc`, `d.adg`, `e.adv`, `f.agr`, `g.amxd`, `h.rx2`, `i.mid`, `j.als` | All ten listed | Static-derived (kinds); listing assumes the folder view shows these kinds (PRB-BI-01) |
| BI-002 | 001 | negative | F: `k.txt`, `l.json`, `m.asd`, `n.xmp`, `o.cfg`, `p.zip` | None listed | Static-derived (assumes kind filtering) |
| BI-003 | 001 | negative | F: `q.fxp`, `r.fxb`, `s.ablpresetbundle` | None listed | Static-derived (assumes kind filtering); confirm with PRB-BI-01 |
| BI-004 | 001 | boundary | F: `t.mp3`, `u.ogg`, `v.flac`, `w.m4a`, `x.wma`, `y.mov`, `z.png` | Unresolved | Unknown (PRB-BI-01) |
| BI-005 | 001 | boundary | F: `A.WAV`, `B.Wav` | Unresolved | Unknown (PRB-BI-01) |
| BI-006 | 001, 012 | malformed | F: `noext` (a WAV without extension), `x.xyz` | Unresolved; static reading suggests `x.xyz` is not listed | Unknown (PRB-BI-01, PRB-H2-09) |
| BI-020 | 003 | positive | F: `a.wav`; `F/Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` = Fixture A | `a.wav` has tags {`Character\|Bright`}; the `.xmp` is not listed | Static-derived (assumption in REQ-003) |
| BI-021 | 003 | negative | As BI-020, but the sidecar is at `F/Tags/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` | `a.wav` has no tags; the `.xmp` is not listed | Static-derived |
| BI-022 | 003 | boundary | As BI-020, sidecar named `my-tags.xmp` | Unresolved | Unknown (PRB-BI-03) |
| BI-023 | 003 | boundary | F: `sub/a.wav`; Fixture A at `F/sub/Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` | Unresolved | Unknown (PRB-BI-03) |
| BI-024 | 003 | boundary | As BI-020, sidecar folder named `ableton folder info` | Unresolved | Unknown (PRB-BI-03) |
| BI-030 | 004 | positive | As BI-020; Fixture A adds `xmlns:xmp="http://ns.adobe.com/xap/1.0/"` with `xmp:CreatorTool`, `xmp:CreateDate` and `xmp:MetadataDate` | Same as BI-020 | Static-derived |
| BI-031 | 004 | malformed | As BI-020; the sidecar is the first half of Fixture A | `a.wav` has no tags; other effects unresolved | Static-derived (no tags); unknown (PRB-BI-03) |
| BI-032 | 004 | boundary | As BI-020; `ablFR:platform` = `win` | Unresolved | Unknown (PRB-BI-03) |
| BI-033 | 004 | boundary | As BI-020; Fixture A inside `<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>` … `<?xpacket end="w"?>` | Unresolved | Unknown (PRB-BI-03) |
| BI-040 | 005 | positive | F: `sub/b.wav`; F's sidecar has one item, `sub/b.wav`, tags {`Sounds\|Pad`} | `b.wav` has tags {`Sounds\|Pad`} | Static-derived |
| BI-041 | 005 | positive | F: `kit/k.wav`; F's sidecar has one item, `kit`, tags {`Drums\|Kick`} | Folder `kit` has tags {`Drums\|Kick`}; `k.wav` none | Static-derived (binding); display unknown (PRB-BI-02) |
| BI-042 | 005 | negative | As BI-020; Fixture A adds an item `gone.wav` with tags {`Type\|Loop`}; no such file | `a.wav` as BI-020; no entry or error for `gone.wav` | Static-derived (assumption in REQ-005) |
| BI-043 | 005 | boundary | F: `a.wav`; Fixture A with `filePath` `A.WAV` | Unresolved | Unknown (PRB-BI-03) |
| BI-044 | 005 | malformed | F: `a.wav`; Fixture A with `filePath` `./../F/a.wav` | Unresolved | Unknown (PRB-BI-03) |
| BI-050 | 006 | positive | As BI-020; item adds `ablFR:colors` Bag {`2`, `5`} | `a.wav` has labels {2, 5} | Static-derived |
| BI-051 | 006 | boundary | As BI-020; colors Bag {`0`, `8`, `3`, an empty entry} | Labels {3} | Static-derived |
| BI-052 | 006 | malformed | As BI-020; colors Bag {`red`} | Unresolved, including whether the item keeps its tags | Unknown (PRB-BI-03) |
| BI-053 | 006 | positive | As BI-020; keywords {`Character\|Bright`, `Character\|Warm`, `Genres\|Ambient`} | Tags are exactly these three; grouping in the browser unresolved | Static-derived (set); unknown (PRB-BI-02) |
| BI-054 | 006 | boundary | As BI-020; keywords {`Favorites`, `A\|B\|C\|D`} | Unresolved | Unknown (PRB-BI-02) |
| BI-055 | 006 | boundary | As BI-020; adds `ablFR:hideKeywords` {`Character\|Bright`} | Unresolved | Unknown (PRB-BI-04) |
| BI-060 | 007 | positive | F: `a.wav`; the user assigns tag `Character\|Warm` to `a.wav`, then quits | `F/Ableton Folder Info/dc66a3fa-0fe1-5352-91cf-3ec237e9ee90.xmp` exists and equals Fixture A with tags {`Character\|Warm`}; nothing else in F changes | Static-derived (name, content); timing unknown (PRB-H2-04) |
| BI-061 | 007 | positive | As BI-060, but the user assigns color label 3 | Item `a.wav` has `colors` {`3`} and no `keywords` | Static-derived (encoding); timing unknown (PRB-H2-04) |
| BI-062 | 007 | positive | F: `a.wav`, `b.wav`; F's sidecar: `a.wav` {`Character\|Bright`}, `b.wav` {`Sounds\|Pad`}; the user adds `Character\|Warm` to `a.wav` | `a.wav` {`Character\|Bright`, `Character\|Warm`}; `b.wav` entry unchanged | Unknown (PRB-H2-04) |
| BI-063 | 007 | boundary | F: `sub/a.wav`; the user tags `a.wav` | Which folder's sidecar is written is unresolved | Unknown (PRB-H2-04) |
| BI-064 | 007 | positive | The user tags one Core Library item | `<User Library>/Ableton Folder Info/<n>/b17d447d-894d-5b3e-96e9-a81dbf4d431c.xmp` holds the item's entry; no Core Library file changes | Static-derived (name, location); `<n>` and timing unknown (PRB-H2-04) |
| BI-065 | 007 | positive | The user tags one built-in device folder | `<User Library>/Ableton Folder Info/<n>/b769aafb-73f9-57e9-8dba-740d64be2541.xmp` holds it; built-in content unchanged | Static-derived (name, location); `<n>` and timing unknown (PRB-H2-04) |
| BI-066 | 007 | negative | F on a read-only volume; the user tags `a.wav` | Unresolved | Unknown (PRB-H2-04) |
| BI-067 | 007 | teardown | As BI-060, quitting within 1 s of the edit | Unresolved | Unknown (PRB-H2-04) |
| BI-070 | 008 | positive | After BI-060: quit, remove the index (for a candidate, its own index), start | `a.wav` has tags {`Character\|Warm`} | Unknown; expected if REQ-007 holds (PRB-H2-04, PRB-H2-06) |
| BI-071 | 008 | positive | Copy F from BI-020, with its sidecar folder, to a second installation; add it as a user folder | `a.wav` has tags {`Character\|Bright`} | Static-derived (assumption in REQ-003) |
| BI-080 | 009 | positive | F: `c.adg`; `F/Ableton Folder Info/Previews/c.adg.ogg` | Preview of `c.adg` is that file | Static-derived (association); playback unknown (PRB-BI-05) |
| BI-081 | 009 | boundary | As BI-080, plus `Previews/c.adg.wav` | Preview is `c.adg.wav` | Static-derived |
| BI-082 | 009 | negative | F: `c.adg`; only `Previews/c.ogg` | No preview file associated | Static-derived |
| BI-083 | 009 | boundary | F: `sub/d.adg`; `F/Ableton Folder Info/Previews/sub/d.adg.ogg` | Preview of `d.adg` is that file | Static-derived (assumes `R` is F) |
| BI-084 | 009 | boundary | F: `sub/d.adg`; `F/sub/Ableton Folder Info/Previews/d.adg.ogg` | Unresolved | Unknown (PRB-BI-05) |
| BI-090 | 010 | positive | Running, F: `a.wav`; copy `n.wav` into F | `n.wav` listed without restart; latency unresolved | Unknown (PRB-H2-03) |
| BI-091 | 010 | positive | Running; rename `a.wav` to `a2.wav` | Listing {`a2.wav`} | Unknown (PRB-H2-03) |
| BI-092 | 010 | positive | Running, F: `a.wav`, `b.wav`; delete `b.wav` | Listing {`a.wav`} | Unknown (PRB-H2-03) |
| BI-100 | 011 | negative | F: `a.wav`, `b.wav`; quit; delete `b.wav`; start | Listing {`a.wav`}; nothing shown as missing | Static-derived (removal); detection time unknown |
| BI-101 | 011 | boundary | BI-020 state; quit; move `a.wav` to `F/sub/a.wav`; start | Tags of `sub/a.wav` unresolved | Unknown (PRB-H2-05) |
| BI-102 | 011 | boundary | F on a removable volume; eject while running; remount | Unresolved presentation; F returns after remount | Unknown (PRB-H2-05) |
| BI-103 | 011 | negative | Running, F: `sub/x.wav`, `sub/y.wav`; delete `sub` | `sub` and its contents are no longer listed | Static-derived (removal with descendants); latency unknown |
| BI-110 | 012 | malformed | F: `t.wav` holding only the first 44 bytes of a valid WAV | Unresolved | Unknown (PRB-H2-09) |
| BI-111 | 012 | malformed | F: zero-length `z.als` | Unresolved | Unknown (PRB-H2-09) |
| BI-112 | 012 | malformed | F: `r.wav` holding 4,096 random bytes | Unresolved | Unknown (PRB-H2-09) |
| BI-120 | 013 | boundary | BI-020 state; quit; make the index unreadable (for the original: truncate its index file to half its size); start | Browser content and `a.wav`'s tags return; any message unresolved | Unknown (PRB-H2-06) |

Counts:

| Requirement | Cases |
| --- | --- |
| 001 | 6 |
| 003 | 5 |
| 004 | 4 |
| 005 | 5 |
| 006 | 6 |
| 007 | 8 |
| 008 | 2 |
| 009 | 5 |
| 010 | 3 |
| 011 | 4 |
| 012 | 3 |
| 013 | 1 |

BI-006 counts under 001. The total is 52 cases. 24 have a static-derived
expected result, some only in part: BI-001, BI-041, BI-053, BI-060, BI-061,
BI-064, BI-065 and BI-080 leave the noted part unknown, and BI-031 leaves other
effects unknown. 28 are unknown.

Omitted kinds:

- REQ-002 has no case, because no location configuration is constructible
  without the unknown UI; PRB-BI-02 covers it.
- REQ-013's version outcomes have no candidate case, because they concern the
  original's internal storage; PRB-H2-06 covers them on the reference side.
- No case covers cancellation, because no cancel affordance for tag edits is
  established.

## Open questions

PRB-H2-xx records are in the H2 probe batch (appendix). PRB-BI-xx records are
**proposed** here and not yet filed in any probe-batch file.

| Item | Requirements | Missing evidence | Minimal input and observation |
| --- | --- | --- | --- |
| PRB-BI-01 | 001, 003, 012 | Which kinds a user-folder view lists; case; no extension; `.fxp`; sidecar folder visibility | One folder with the BI-001 to BI-006 files and an `Ableton Folder Info`; record the listing once |
| PRB-BI-02 | 001, 002, 006 | Sidebar categories per kind and per tag level; location presentation | BI-041, BI-053, BI-054 folders; record where each item appears |
| PRB-BI-03 | 003–006 | Sidecar edge cases | One user folder per case BI-022–024, BI-031–033, BI-043, BI-044 and BI-052; record the tags shown after one start |
| PRB-BI-04 | 006 | Meaning of `hideKeywords` | BI-055, plus one shipped Core Library item that has `hideKeywords`; compare the displayed tags |
| PRB-BI-05 | 009 | Preview root and playback | BI-080 to BI-084, each preview a distinct tone; record which plays |
| PRB-H2-03 | 010 | Add, rename and delete latency | BI-090 to BI-092 |
| PRB-H2-04 | 007, 008 | Write location, `<n>`, timing, nesting | BI-060 to BI-067, BI-070 |
| PRB-H2-05 | 002, 010, 011 | Moves, unmount, tag retention | BI-101, BI-102 |
| PRB-H2-06 | 008, 013 | Corrupt, newer and foreign index | BI-070, BI-120 and the probe's variants |
| PRB-H2-09 | 001, 012 | Unsupported and corrupt media | BI-006, BI-110 to BI-112 |

Canonical gap: [Q-014](../questions.md#q-014-browser-index-behavior).

## Analyst evidence appendix

Analysis-only. Remove or review before any handoff. Canonical research:
[browser index](../research/browser-index-static.md) and
[helper launch, Live side](../research/helper-launch-live-side.md#index).

Kept evidence:

- `analysis/ableton-live-12.4.3/r2/h2-index-v1/`
  ([manifest](../../analysis/ableton-live-12.4.3/r2/h2-index-v1/manifest.json)),
  including `out/code/*.c`, `out/file-type-registry.tsv`,
  `out/shipped-inventory.json`, `out/sql-strings.jsonl`,
  `out/strings-xmp-region.tsv` and `probe-batch.json` (PRB-H2-01 to 09).
- `analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/` (result `n4-0003`).

Helper identity: `Ableton Index` arm64 slice SHA-256 `3390bd4b…a289b62`.

**Not retained (read 2026-10-17 for this draft).** The helper corpus at
`/var/tmp/sound-analysis/helpers/Ableton_Index/corpus/` (coverage `run_sha256`
`858745e5…6cf8c1f`, strings index `95733c86…4ac6`, calls index `7349b6c0…c903`).
Pseudocode of the functions marked † below came from chunks 00062, 00277 and
00282 to 00284. No disassembler for the helper exists on this host, so these
rest on Ghidra pseudocode plus string-reference records. No query-server rounds
were used; the server serves only `Live.arm64`. These reads should be retained
in a kept addendum before review.

| Requirement | Locators | Basis and limits |
| --- | --- | --- |
| 001 | Registry `0x10029bb10` (80 rows, `file-type-registry.tsv`); kind map `0x10016b758`† (the target of callback `0x100289f8c`, whose symbol names `TFileDatabase::MapFileTypeToFileKind`); kind names and named sets `0x10016b3e8` (`browser-default` = 31999 = `0x7CFF`) | The map compares four-character type codes, as traced by hand. Unmapped codes, including `ablx`, log `Unknown file typeId:` and return 0. Kind filtering by the browser is inferred. Live also contains `browser-default` (`0x105b2468a`, from `0x100ddf904`) |
| 002 | `Library.cfg` keys `0x100153650`/`0x100131a44`; `unavail_places`, `folder_kind` 13 (`sql-strings.jsonl`) | The configuration file is internal; only the location kinds are used |
| 003 | `0x1006e6d40`† (parent name equals `Ableton Folder Info`, or the parent equals the override folder `0x1006e5d68`†); constants `0x100237a58` (`Ableton Folder Info` `0x100c22278`, `Legacy Pack Data` `0x100c22290`, `Previews` `0x100c222bb`); reader `0x1006d2624`† (gate first, then a branch per resource kind 1 to 4, the folder branch at its second dispatch) | How the reader enumerates sidecars is not traced. `0x1006e71c8` (name patterns `0x100c5c2e8`, `0x100c5c326`) classifies sidecars under `Legacy Pack Data/Ableton Folder Info`; its effect is not traced |
| 004 | Value tables at `0x100dbd650` (format), `0x100dbd678` (resource), `0x100dbd698` (platform), decoded with `read_ptrs.py` to the strings `0x100c5c648`…`0x100c5c6b2`, `0x100c5c4c4`…`0x100c5c4d7`, `win`/`mac`/`linux`; header writer `0x1006f09d8`†; platform parse `0x1006e188c`†; `Updated by ` `0x100c5c2bc` (`0x1006e5140`); parse error `Error reading xmp file: ` `0x100c5bd91` in `0x1006d2624` | Shipped sidecars: 162 (`shipped-inventory.json` `xmp`); Live has the same message (`0x105ba2231`, `0x101697908`) |
| 005 | Items `0x1006e34b4`†, item read `0x1006ee124`†; `per_file` resolution counts; this draft checked that all 85 built-in items are folders and all 7,000 Core Library items are files | Unresolved entries: one built-in, 59,227 in `Legacy Pack Data` (not active locations) |
| 006 | Colors read `0x1006ed324`† (`stoul` base 10, 1 to 7 set a bit); colors write `0x1006edbbc`† (bits 1 to 7 → `"1"`…`"7"`); keyword arrays `0x1006ed554`†; per-item writer `0x1006ef218`† (deletes then writes `colors`, `keywords`, `hideKeywords`, `assetId`, `contentHash`); document-level writer `0x1006ed9b4`† | Exception handling for a non-numeric color is not traced |
| 007 | Folder path `0x1006e637c`† (`folder` `0x100c5c4c4` at `0x1006e64ec`, `.` `0x100c5437c` at `0x1006e63c8`; called with mode 1 by folder writer `0x1006d03b8` at `0x1006d0428`); UUID text plus file type 68 (`.xmp`) `0x1006e60e4`† → `0x1002a1a40`; UUIDv5 `0x1006efb30`† and `0x1006f02dc`† (Boost SHA-1 name generator: 16 namespace bytes, then the name, then the version-5 and variant bits); factory pack `0x1006e5f48`† (writer `0x1006cf838`, `No UserLibrary.  Can't write factory pack metadata` `0x100c5bc51`); pack-folder variant `0x1006e61d8`† (caller `0x1006e7928`, not traced); built-in `0x1006e67dc`† (`app-resource` `0x100c5c63b`, `builtin` `0x100c5c2e0`); plug-in `0x1006e6640`† (writer `0x1006cec4c`); `<n>` from `0x1001c2380`† (a field of a static product object, not resolved) | Name rule checked by computation (below). The base folder being the User Library is inferred from the refusal message |
| 008 | Work queue `0x100140bac` (`Push xmp import task`); pending export `flags \| 32` (research page) | Export timing not traced |
| 009 | `0x1006c0e04`† (location root path, then `Ableton Folder Info`, then `Previews`, then the relative path plus `.aif`, `.wav`, `.ogg`, `.mp3`, first existing); shipped preview counts (this draft, excluding AppleDouble `._*` files) | This is the index's association; Live's playback path was not traced. Live has the same constants (`0x10121f0e4`, `Previews` `0x105b6a71b`) |
| 010–011 | OsEvents strings, `Folders to be scanned fully…` `0x100c1ca96`, `Index: Observed File is gone:`, the descendant `DELETE` (`sql-strings.jsonl`) | Research page; latency unknown |
| 012 | `audio_decoding_failed`, `corrupt_document`; registry | Presentation untraced |
| 013 | `0x10023344c`, `0x100232eb4`, `0x1002336e0`, `0x1002301ac`, `0x10023a970`; version `0x300c` (`0x100735594`) | Internal storage; outcomes only |

**Sidecar name check (computation, reproducible).** With Python
`uuid.uuid5(namespace, name)` and the nil namespace `N`:

- `uuid5(N, "app-resource")` = `b20da5c2-8ad7-5c68-866e-e0618da1d528`, the
  shipped built-in sidecar's name.
- `uuid5(N, "factory-pack")` = `c55d131f-2661-5add-aece-29afb7099dfa`, the
  shipped Core Library sidecar's name.
- `uuid5(N, "folder")` = `5f319382-…`; `uuid5` of that and `"."` =
  `dc66a3fa-0fe1-5352-91cf-3ec237e9ee90`.
- `uuid5(c55d131f…, packUniqueId)` matches 159 of 160 `Legacy Pack Data`
  sidecar names. The exception, `a1c28bb1…`, is a second file for
  `www.ableton.com/280`, whose matching file `0845588d…` also exists.
- The derived names `b17d447d…` (Core Library) and `b769aafb…` (built-in) apply
  the code's construction; no shipped file confirms them.

This resolves the research page's unknown "namespace and name used for the
UUIDv5 file names". The shipped factory sidecars use the bare namespace UUIDs as
names, while user overrides use the derived names.

**Live-side context (internal, not in the spec body).** Live starts the helper
with an options file and restarts it up to 100 times (`0x1002b4b14`,
`0x1002b56c4`, n4-0003). Both binaries contain the XMP and kind-name code. Which
process performs each step does not affect the observable contract above.

Corrections relative to the research page:

- The kind map was located, so the type-to-kind mapping is no longer unknown.
- The `browser-default` set also excludes plug-ins.
- Items may carry `ablFR:colors` and `ablFR:assetId`, which the research page
  does not list.
- The sidecar naming unknown is resolved, as described above.

## Dropped and deferred candidates

| Candidate | Disposition |
| --- | --- |
| BI-C01 | REQ-BROWSER-INDEX-003 to 005 |
| BI-C02 | REQ-BROWSER-INDEX-006. The 10 first levels are a shipped-content fact, not a requirement on the tag tree; grouping unknown |
| BI-C03 | REQ-BROWSER-INDEX-009, refined: extension order, `p` keeps its extension |
| BI-C04 | Deferred: `Properties.cfg` effects are inferred only |
| BI-C05 | REQ-BROWSER-INDEX-001, now with the static type-to-kind map. "Default excludes device and other folders" narrowed to a named set whose use is unknown |
| BI-C06 | REQ-BROWSER-INDEX-002 |
| BI-C07 | REQ-BROWSER-INDEX-010 |
| BI-C08 | REQ-BROWSER-INDEX-007 and 008; location and name now static-derived; timing unknown |
| BI-C09 | REQ-BROWSER-INDEX-013, restated without internal storage details |
| BI-C10 | Deferred to FEAT-PERSISTENCE media references; the Live-side consumer is unknown (PRB-H2-07) |
| BI-C11 | Split: color labels in REQ-BROWSER-INDEX-006 and 007 (sidecar-backed); use count dropped as unknown (REQ-013) |
| BI-C12 | Deferred: matching rules unknown; the tokenizer is internal |

## Revision and handoff

Revision 1, 2026-10-17: first draft from packet H2, the N4 Index section and a
bounded re-read of the helper corpus. Not reviewed; no handoff exists. A
handoff candidate would need, at minimum:

- the corpus reads marked † retained in kept evidence;
- PRB-BI-01 (listing);
- PRB-H2-04 (write location and timing).

Until then REQ-BROWSER-INDEX-001, 007 and 008 can release only their read-side
and naming clauses.
