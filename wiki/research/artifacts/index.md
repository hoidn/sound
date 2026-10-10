---
id: NAV-ABLETON-ARTIFACTS
type: index
status: active
updated: 2026-10-10
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Binary and decompilation artifacts

Start here to explore **Ableton Live 12 Suite 12.4.3**
(`2026-07-07_e3d8be4d07`). This is the analyst artifact catalog: readable entry
points first, exact retained evidence underneath. All paths are local to this
checkout. Original code and disassembly stay on the analysis side of the handoff.

**[Open the searchable artifact browser](../../../analysis/ableton-live-12.4.3/browse/index.html)**
— an offline HTML file with component filters, native-candidate search, direct
artifact links, Python-module links and an optional main Live function table.
Open it in a web browser; no server,
installation or internet connection is required. Markdown links below work
without the browser.

The browser is updated as retained artifacts are published. Its existing
[`#python` link](../../../analysis/ableton-live-12.4.3/browse/index.html#python)
remains stable. Selected main Live code is now available under
[`#selected-native`](../../../analysis/ableton-live-12.4.3/browse/index.html#selected-native);
the default-profile corpus retains its separate
[`#native`](../../../analysis/ableton-live-12.4.3/browse/index.html#native) section.
Refresh the browser after regeneration; it is a snapshot, not a live process
monitor. The [browser design and plan](browser-design-and-plan.md) describes
the update mechanism and navigation limits.

Read the [learning route](../learning/index.md), [method](../learning/method.md)
and [program atlas](../program-structure.md) alongside the artifacts. The
[next-phase roadmap](../native-decompilation-roadmap.md) and
[execution ledger](../native-phase-execution.md) distinguish planned work from
retained output.

## Choose a starting point

| I want to… | Open | What is available |
| --- | --- | --- |
| Understand the application bundle | [Package map and findings](../ableton-package-structure.md#bundle-map) | Core, helpers, dependencies and resource boundaries |
| Read default-profile main Live pseudocode | [Native corpus browser](../../../analysis/ableton-live-12.4.3/browse/index.html#native), [coverage ledger](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/coverage.json) | Retained exports appear immediately; optionally load all inventoried addresses for search |
| Compare bounded selected-entry captures | [Selected-entry browser](../../../analysis/ableton-live-12.4.3/browse/index.html#selected-native), [first selected ALoopOn factory](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/pseudocode.c) | Separate no-auto-analysis profile with code, assembly and metadata; failed attempts remain visible |
| Read helper pseudocode | [Push2 entry pseudocode](../../../analysis/ableton-live-12.4.3/push2-entry-pseudocode.c) | One Ghidra-decompiled helper entry, with warnings |
| Inspect that function's machine instructions | [Push2 assembly](../../../analysis/ableton-live-12.4.3/browse/push2-entry-assembly.txt) | 1,590 retained assembly lines with static addresses |
| Follow its calls or strings | [Callee table](../../../analysis/ableton-live-12.4.3/browse/push2-entry-callees.tsv), [string table](../../../analysis/ableton-live-12.4.3/browse/push2-entry-strings.tsv) | 77 callee records and 47 referenced strings; incomplete indirect-flow coverage |
| Find a Live C++ symbol | [Symbol index](../../../analysis/ableton-live-12.4.3/live-arm64-symbols.tsv) | Address, mangled name and demangled name; about 34 MB |
| Inspect linker-declared entry addresses | [Declared-starts browser shelf](../../../analysis/ableton-live-12.4.3/browse/index.html#declared-starts), [address TSV](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/addresses.tsv), [summary](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/summary.json) | 413,794 starts declared by `LC_FUNCTION_STARTS`; separate from analyzer inventory, bodies and code |
| Browse binaries by component | [Searchable browser](../../../analysis/ableton-live-12.4.3/browse/index.html), [native candidates JSON](../../../analysis/ableton-live-12.4.3/native-targets.json) | 1,093 format-detected occurrences, including unvalidated candidates |
| Read decoded controller logic | [Python module directory](#python-module-directory) | Seventeen bytecode disassemblies, organized by responsibility |
| Understand what that logic means | [MIDI research](../midi-user-mapping.md), [draft contract](../../specs/midi-user-mapping.md) | Evidence interpretations and proposed behavior; cases remain unexecuted |
| Find schemas, presets or GUI resources | [Resource findings](../../../analysis/ableton-live-12.4.3/resource-findings.txt) | Readable inventory, exact sample paths and source locators |
| Resume focused REA analysis | [Decompilation preparation](../ableton-decompilation-preparation.md#ready-native-inputs) | Inputs, snapshot reuse, symbol seeds and limitations |

## Read the coverage labels correctly

| Target | Retained work | What this does not establish |
| --- | --- | --- |
| Main Live default profile | Frozen Ghidra inventory of 420,472 addresses and retained pseudocode exports; browser reads the coverage ledger | Inventory size is not exported code coverage, recovered original source or demonstrated behavior |
| Main Live selected-entry profile | Sealed custom-script pseudocode/assembly and failed attempts; see browser for retained outcomes | Uses a no-auto-analysis profile, separate from the default-profile inventory and REA records |
| Push2 display helper | Ghidra inventory and one entry-function dossier with pseudocode, assembly and references | Not complete helper decompilation; 13,611 inventoried procedures are not 13,611 decompiled functions |
| MIDI user mapping | Seventeen CPython 3.11 modules disassembled and selected paths traced | Disassembly is opcode text, not recovered Python source; remaining modules untraced |
| Other native candidates | Package inventory and partial dependency model | Format labels are not validation: some Java `.class` headers resemble universal Mach-O |
| Schemas, QML, presets and other resources | Inventory and selected parsing/inspection | No complete runtime model, source recovery or compatibility result |

Native addresses belong to the pinned build and architecture. They are static
virtual addresses, not offsets into the universal file or current ASLR-adjusted
process addresses. Canonical identities and limitations are in the
[package source record](../sources/ableton-live-12.4.3.md) and
[MIDI source record](../sources/midi-user-mapping-12.4.3.md).

## Native evidence shelf

| Artifact | Format / approximate size | Use |
| --- | --- | --- |
| [Native summary](../../../analysis/ableton-live-12.4.3/native-summary.json) | JSON / 109 KB | Build identity, inventory totals, symbols and dependency-model overview |
| [Dependency model](../../../analysis/ableton-live-12.4.3/dylib-resolution.json) | JSON | Executable roots, image/dependency edges and unresolved loads |
| [Push2 function summary](../../../analysis/ableton-live-12.4.3/push2-decompilation-summary.json) | JSON | Entry address, body ranges, counts and warnings |
| [Push2 full dossier](../../../analysis/ableton-live-12.4.3/evidence/push2-entry-dossier.json) | JSON / 9.2 MB | Exact function evidence, including block/reference detail omitted from readable extracts |
| [Push2 analysis snapshot](../../../analysis/ableton-live-12.4.3/evidence/push2-analysis-snapshot.json) | JSON / 10.3 MB | Eligible cached queries for resuming REA; not a full Ghidra project |
| [Slice provenance](../../../analysis/ableton-live-12.4.3/derived/manifest.json) | JSON | Original hashes, extraction commands and slice byte identity |
| [Default-profile coverage](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/coverage.json), [analysis identity](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/run.json) | JSON | Frozen inventory identity, exact function states, retained revision IDs and profile; use the browser for direct code links |
| [Declared-starts summary](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/summary.json), [sealed provenance](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/manifest.json) | JSON and TSV | Linker metadata decoded with a captured extraction method; adjacent starts do not establish function sizes |
| [Live arm64 input](../../../analysis/ableton-live-12.4.3/derived/Live.arm64) | Mach-O binary / 149.7 MB | Prepared analyzer input, not a readable report |
| [Selected native run 1](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json), [manifest](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/manifest.json) | Custom Ghidra capture / JSON and code | First main Live selected entry; sealed identities, method and outcomes |
| [Selected native run 2](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/run-status.json), [manifest](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/manifest.json) | Custom Ghidra capture / JSON and code | Remaining selected pilot entries, including explicit failed body-recovery outcomes |
| [Selected native run 3](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/run-status.json), [manifest](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/manifest.json) | Custom Ghidra capture / JSON and code | Focused transport callees, retaining successful and failed outcomes separately |
| [Push2 arm64 input](../../../analysis/ableton-live-12.4.3/derived/Push2DisplayProcess.arm64) | Mach-O binary / 3.6 MB | Input used for the helper dossier |

The large [static export](../../../analysis/ableton-live-12.4.3/evidence/static-evidence.json)
(about 328 MB), [package export](../../../analysis/ableton-live-12.4.3/evidence/package-evidence.json)
(about 313 MB) and [decompilation export](../../../analysis/ableton-live-12.4.3/evidence/decompilation-evidence.json)
(about 5.3 MB) retain full REA records. Start with the summaries above; use these
exports when auditing an exact evidence ID. Sizes are decimal and rounded.

## Reviewed navigation and export methods

The [frozen export/browser v2 method](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/methods/export-and-browser-v2/manifest.json)
retains reviewed code, tests and design copies. The
[completed tool-validation record](../native-export-execution.md#completed-tool-validation)
links the 84-test combined suite and corrected grouped-ingestion reviews;
the [browser plan](browser-design-and-plan.md#full-inventory-publication-amendment)
links its 28-test scope/quality reviews and malformed-index recovery fixes.
Those reviews pin historical artifacts. The browser is regenerated from current
retained evidence, and the [phase ledger](../native-phase-execution.md) owns live
progress. Node DOM-stub checks do not establish visual or accessibility quality;
retained evidence and query snapshots do not establish cold database persistence.

## Python module directory

All links below open decoded opcode text. Search a file for a function name
from the findings; source-line metadata and bytecode offsets identify code
locations, not retained `.py` source lines. Companion findings:
[parser trace](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/parser-findings.json)
and [mapping trace](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/bytecode-mapping-findings.json).

| Module | Start here for |
| --- | --- |
| [_UserScript/__init__](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/__init__.dis.txt) | Configuration entry, integer/channel parsing and mode selection |
| [_UserScript/DeviceComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_UserScript/DeviceComponent.dis.txt) | One- versus two-bank width and bank navigation |
| [_Generic/GenericScript](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Generic/GenericScript.dis.txt) | Building and assigning device, mixer and transport controls |
| [_Generic/SpecialMixerComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Generic/SpecialMixerComponent.dis.txt) | Mixer specialization |
| [_Generic/SelectChanStripComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Generic/SelectChanStripComponent.dis.txt) | Channel selection and arming specialization |
| [_Framework/InputControlElement](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/InputControlElement.dis.txt) | Input control and mapping boundary |
| [_Framework/EncoderElement](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/EncoderElement.dis.txt) | Encoder modes and 14-bit identifier boundary |
| [_Framework/ButtonElement](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ButtonElement.dis.txt) | Button values and momentary classification |
| [_Framework/ButtonMatrixElement](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ButtonMatrixElement.dis.txt) | Control row order and width |
| [_Framework/DeviceComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/DeviceComponent.dis.txt) | Device parameters, bank buttons, activator and locking |
| [_Framework/ChannelStripComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ChannelStripComponent.dis.txt) | Mute, solo, arm and track state handlers |
| [_Framework/TransportComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/TransportComponent.dis.txt) | Transport assignments, tap and seek handlers |
| [_Framework/ToggleComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/ToggleComponent.dis.txt) | Press/release and Boolean control handling |
| [_Framework/MixerComponent](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/_Framework/MixerComponent.dis.txt) | Mixer channels and bank assignment |
| [ableton/v3/control_surface/__init__](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/ableton/v3/control_surface/__init__.dis.txt) | Exports connecting user scripts to control-surface helpers |
| [ableton/v3/control_surface/elements_base](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/ableton/v3/control_surface/elements_base.dis.txt) | Map-mode declarations |
| [stdlib/configparser](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly/stdlib/configparser.dis.txt) | INI sections, options, conversion and interpolation errors |

For the original interface text, open the retained
[configuration template](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source/_Tools/UserConfiguration.txt)
or [setup instructions](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/source/_Tools/InstantMappings-HowTo.txt).
The [46-group case plan](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/acceptance-cases.json)
has documentary/static expectations and explicit unknowns. It is not an
executable test suite or a reference execution record.

## Search without opening a large report

Run from the repository root. These commands read retained text only:

```sh
# Match C++ names; -m limits the output from the large symbol index.
rg -n -m 20 'ATransport|AAudioClip|ASongAgent' analysis/ableton-live-12.4.3/live-arm64-symbols.tsv

# Locate named functions in decoded MIDI modules, even though analysis/ is ignored.
rg --no-ignore -n -m 10 'parse_int|parse_map_mode|_bank_value' analysis/ableton-live-12.4.3/midi-user-mapping-v1/disassembly
```

## Provenance and local availability

The [package checksums](../../../analysis/ableton-live-12.4.3/artifact-checksums.json)
and [MIDI checksums](../../../analysis/ableton-live-12.4.3/midi-user-mapping-v1/artifact-checksums.json)
pin earlier retained evidence. New browser/extract files are derived navigation
views; their [manifest](../../../analysis/ableton-live-12.4.3/browse/manifest.json)
identifies their inputs and outputs. They add no new decompilation or behavior
observation. Rebuild only these views with the repository tool:

```sh
python3 tools/build_artifact_browser.py
```

Regeneration reads `native-live-arm64-v1/coverage.json` and adds actual function
states and searchable, paginated rows (100 per page) with direct
pseudocode, revision metadata and source-evidence links. No code is embedded in
the index. The full coverage ledger retains all attempt identities; displayed
links select a revision supporting the aggregate state, not necessarily the
newest attempt. Generation does not replace the exporter's integrity check.

The initial native search contains functions with retained attempts so available
code is easy to find. An explicit button loads the complete address index from a
local JavaScript file, including pending and external entries. Counts above the
table always describe the full ledger. Loading needs no server or fetch call;
a page left open across regeneration asks for a refresh if its inventory
snapshot no longer matches. The full index remains metadata, not embedded code.

The selected-entry shelf discovers sealed `native-live-arm64-targeted-v*`
captures independently. It verifies each manifest and clean process teardown
before publishing direct code/assembly links. Unsealed or corrupt captures are
listed without publishing their function artifacts. Run counts are selected
outcomes, and can repeat an address across captures; they never become a
whole-image discovery denominator. These custom-script artifacts are not
ingested into the REA default-profile corpus.

The optional declared-starts shelf validates its sealed capture, target and
method hashes, and TSV row count before linking the table. It keeps the large
address list outside the HTML. Declared starts never become an export-coverage
denominator or evidence that those functions were analyzed or decompiled.

`analysis/` is intentionally ignored by Git. Its artifact links resolve in this
workspace, but a fresh checkout will need the retained evidence copied back to
the same paths. The generator requires that evidence and does not reacquire it.
Do not move or rename captured payloads to tidy the directory: update this
catalog and generate new views while preserving source bytes and old manifests.
This catalog is not part of a clean implementation handoff.

The [2026-10-10 browser checkpoint](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/browser-checkpoint-2026-10-10-v1/report.json)
verifies the current generated files, local links, stable section anchors and
attempted/full inventory agreement. It is a structural check, not visual browser
QA. See the [phase report](../native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
for current export coverage and the capacity decision.
