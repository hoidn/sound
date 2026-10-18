---
id: RESEARCH-ABLETON-STRUCTURE
type: research
status: current
updated: 2026-10-17
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Ableton package structure

This static pass establishes a native application with several separately
packaged subsystems and useful readable resources. It does not establish
runtime topology, signal processing behavior, or compatibility with a replacement.
All facts below refer to [SRC-ABLETON-12-4-3](sources/ableton-live-12.4.3.md).

## Bundle map

Browse [the artifact catalog](artifacts/index.md) for direct evidence and code
links. This simplified tree shows **package containment**, not runtime calls or
process communication. Its locations are recorded in INV/PKG and the resource
capture cited below.

```text
Ableton Live 12 Suite.app/Contents/
├── MacOS/Live                         Core native application
├── App-Resources/
│   ├── Extensions/                   Index, plugin scan and other helpers
│   ├── Devices/Mac/                  Bundled device binaries
│   ├── Max/Max.app/                  Nested Max subsystem and its dependencies
│   ├── MIDI Remote Scripts/          Controller bytecode and mapping docs
│   ├── Python/                       Bundled Python library bytecode
│   ├── Schema/                       Versioned XML structure descriptions
│   ├── Builtin/ + Core Library/      Sets, presets, clips and other content
│   ├── JS/                           WebView scripts
│   └── Database/                     Resource-map database
├── Helpers/Push3.app/                Push helper
├── Push2/Push2DisplayProcess.app/    Display executable and Push2 QML
├── Frameworks/                       Native dependencies
├── Qt/                               Qt libraries, plugins and QML
└── Resources/                        Engine bundle and other support binaries
```

## Native and process boundaries

Observed INV/PKG graph: 55,022 unique content nodes, 59,991 occurrences and
59,932 edges, with no reported integrity contradictions. These are graph counts,
not file or function counts. Native-format identification includes 1,093
occurrences across the whole package, including bundled third-party components;
format detection alone does not establish that each is executable code.

| Component | Observed evidence | Analysis implication |
| --- | --- | --- |
| `Contents/MacOS/Live` | Universal x86_64/arm64, 313,453,600 bytes; MACH has 48,780 merged export/symbol entries and 1,730 import entries | Core native analysis target; C++ names provide search seeds, not proof of behavior |
| `App-Resources/Extensions` | DYLD roots: AddOns, Index, Plugin Scanner, Web Connector, Swapper and xdelta3 | Separate executable candidates for focused lifecycle and IPC investigation |
| `Helpers/Push3.app` and `Push2/Push2DisplayProcess.app` | Distinct executable roots; Qt/QML dependencies in DYLD | Keep hardware/display behavior separate from core musical scheduling |
| `App-Resources/Max/Max.app` | Nested app, Chromium helpers and Node executable in DYLD | Analyze as a separate subsystem; its Node modules do not make Live an Electron app |
| `Frameworks` and `Qt` | Native dependencies include ONNX Runtime, libusb, REX and Qt frameworks | Dependency presence does not establish which features invoke them |

MACH's dependency list has 36 entries, including the dyld loader; do not call all
36 libraries. The arm64 load model examined 20 executable roots, 39 image records
and 444 dependency edges. Its coverage is partial: MakeAlias lacks the selected
architecture; four Java `.class` files share a header signature with universal
Mach-O and appear as unparsed candidates. System/shared-cache paths remain
undetermined. Four weak CEF loads were unresolved in the modeled helper contexts;
this is not evidence that Max fails to run. Exact findings and qualifications:
[DYLD result](../../analysis/ableton-live-12.4.3/dylib-resolution.json),
`normalized_result.coverage`, `.findings`, `.limitations`.

## Resources that can ground specifications

These observations are backed by hashed paths and parser results in
[resource evidence](../../analysis/ableton-live-12.4.3/resource-analysis.json);
[resource findings](../../analysis/ableton-live-12.4.3/resource-findings.txt)
provides detailed locators and per-sample limitations.

| Surface | Observed structure | What remains unknown |
| --- | --- | --- |
| `App-Resources/Schema` | All 203 `.txt` files parsed as XML; highest numbered `12.0_12402.txt` has 412 top-level entries and 7,943 child fields | Ranges, defaults, enum meanings and migration behavior; this is not an XSD |
| Core Library | 16,365 files, including 2,187 ADV, 1,071 ADG, 350 ALC and 25 ALS | Only named samples were format-parsed; counts do not prove uniform encoding |
| `Builtin/Templates/DefaultLiveSet.als` | Gzip XML; stored 2 MIDI, 2 audio, 2 return tracks and 8 scenes; tempo field 120 | User-template overrides, runtime initial state and enum/time semantics |
| Python and MIDI Remote Scripts | 888 plus 1,372 `.pyc`, no `.py` in those two trees; magic `a70d0d0a` | [Scoped follow-up](midi-user-mapping.md) decoded 17 modules as CPython 3.11; remaining module behavior unknown |
| MIDI `_Tools` | Readable INI configuration plus mapping documentation | Runtime validation, relative-encoder arithmetic and error behavior |
| Push2 QML | 153 readable QML files; Qt tree adds 192 | Native model bindings, controller correspondence and actual display behavior |
| `App-Resources/JS` | Three minified WebView scripts, 21,316 bytes | Native host endpoints and observed messaging lifecycle |
| `Database/filerefmap.db` | SQLite header and read-only schema inspection | Resource-resolution precedence and missing-file handling |
| GUI/Graphics/Languages ALP; sampled AGR | Opaque binary signatures | Container encoding/compression; encryption is not established |

The shipped default ALS identifies its creator as Live 12.1d1 even though the
installed executable is 12.4.3. Treat it as an older fixture bundled with this
build, not a capture produced by running this build. Sampled `.als/.adv/.adg/.alc`
decode as gzip XML; sampled `.agr` did not. All 219 `.agr` are plain XML (116)
or `AB1E` binary (103), never gzip ([document container](document-container-static.md)). Actual defaults are under
`Builtin/Templates` and `Core Library/Defaults`; top-level `Defaults` and
`Templates` only contain empty placeholders in this installation.

## Completion boundary

Target identity and package inventory: answered for the selected installation.
Static component/dependency structure: partially answered, with the limits above.
Decompilation readiness: proven for the smaller Push2 helper; core Live is
prepared and accepted by Ghidra but not deeply analyzed. Behavioral spec readiness:
concrete evidence seeds and acceptance-case plans exist; no behavior is verified
and no handoff has been released. See the [next-stage plan](ableton-decompilation-preparation.md).

## Serialization vocabulary strings and shipped documents — 2026-10-17

Observed on the Linux workstation against the re-derived `Live.arm64`
(SHA-256 `3a99cee…383cfad`) with `strings -n 4 | grep -x`: the image contains
exactly one null-terminated instance each of `LoopOn`, `LoopStart`, `LoopLength`,
`Tempo`, `SchemaChangeCount`, `MajorVersion`, `MinorVersion` and `Creator`,
four of `LiveSet` and five of `Transport`. These names match the schema and
ALS vocabulary in the [transport study](native-transport-study.md#evidence-already-available).
Their presence is a fact about bytes; which code references them, and whether
that code reads or writes documents, is unknown until cross-references are
resolved in an analyzed project.

Observed with `find` over `Contents/App-Resources`, excluding AppleDouble `._*`
companions: 26 `.als` sets, 350 `.alc` clips, 2,557 `.adv` presets, 1,072 `.adg`
racks, 219 `.agr` grooves, 3 `.alp` packs, 2,189 `.xml` and 580 `.txt` files.
Correction 2026-10-17: the first version of this paragraph counted the 56,603
`._*` companions too, doubling every figure; see the
[inventory correction](document-container-static.md#inventory-correction). `Schema/` holds 203 versioned
descriptions. Core Library and Builtin total about 4.3 GiB. Counts are file
inventory, not parsed or validated documents.
