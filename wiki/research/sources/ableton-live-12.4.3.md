---
id: SRC-ABLETON-12-4-3
type: source
status: current
updated: 2026-10-12
access: analysis
target: Ableton Live 12 Suite 12.4.3
---

# Ableton Live 12.4.3 installed package

Observed source: `/Applications/Ableton Live 12 Suite.app`, selected by the user.
Capture date: 2026-10-09 America/Los_Angeles (2026-10-10 UTC).
`Contents/Info.plist` reports `12.4.3 (2026-07-07_e3d8be4d07)`, bundle ID
`com.ableton.live`, executable `Live`, minimum macOS `11`.

The installed original remains external and can change on upgrade. REA retained
its content-addressed inventory, not a complete copy of all original bytes.
Selected arm64 executable slices are retained locally. Evidence under `analysis/`
is analyst-only local material, not a published handoff or portable backup.

## Identity and retained evidence

| Item | Exact identity / locator |
| --- | --- |
| Original universal Live executable SHA-256 | `52289af638f1b26590c84a9bc08eabdc35127883087057add909d2718a7a35ef` |
| REA directory root digest | `656c862441cd9bd7ec1e4cdf25e306998917576619362e7edddbd844a47618b1` (REA directory identity, not a DMG/archive file hash) |
| Inventory manifest | `agm_b0a8c5086f5ba5d4dbf10f5fb60d2f145090a952b37d9c6c0167bb08ebaff0f6` |
| Live arm64 slice SHA-256 | `3a99ceeabce62ccd069b6b55d99d186c9bdf8a6b80a7e3350dd0f9d1c383cfad` |
| Push2 arm64 slice SHA-256 | `5988ef09f5ff69ab916a7b399d81b28b401bb2a170fd1eb4505394f2527d5465` |

The [derivation manifest](../../../analysis/ableton-live-12.4.3/derived/manifest.json)
records both original hashes, `lipo` commands, offsets, sizes, and exact contiguous
byte equality with their universal parents. Live's slice starts at 163741696 and
contains 149711904 bytes. The original binaries were not modified.

The [static REA bundle](../../../analysis/ableton-live-12.4.3/evidence/static-evidence.json)
retains these records under `records`, selected by `operation` or `evidence_id`:

| Label | Operation | Evidence ID |
| --- | --- | --- |
| INV | inventory_artifact | `ev_0cd7fe48edae76531252472348f6b0854f4913be23498e4075b7b69247926035` |
| PKG | inspect_artifact | `ev_fbdd487039b9bb28634fca300b9d5bdea87d4f3d978cb8a04f1a16d1c41f7524` |
| MACH | inspect_macho | `ev_1be30a5bf2a8819891406299c7739659bcae681676ec358b4ec8f16021fe6667` |
| PLIST | inspect_plist | `ev_79cd69c298611d12df5ef77f465ef078bc93f68d708a3f81826cce8580d877f6` |
| DYLD | trace_dylib_resolution | `ev_a38cf53499a3ed84e441a823a39315d6ad2f2a38763decb6a9ca472da7d7b76e` |

The [decompilation bundle](../../../analysis/ableton-live-12.4.3/evidence/decompilation-evidence.json)
contains Push2 overview `ev_71a25f5c6cb7817ff0c7f4766a36b92f59f9068c005ca151ec85ee1e80a44a5d`
and entry-function dossier `ev_108344e4679384ae44fc7480aa7a4ee2b386980cba7dbb7b359f236059d89316`.
Its [snapshot](../../../analysis/ableton-live-12.4.3/evidence/push2-analysis-snapshot.json)
retains eligible query results; it is not a complete persistent Ghidra project.

Resource parsing, original paths, hashes and exact source/XML locators are in
[resource-analysis.json](../../../analysis/ableton-live-12.4.3/resource-analysis.json).
The [retained capture script](../../../analysis/ableton-live-12.4.3/capture_resources.py)
and [capture commands](../../../analysis/ableton-live-12.4.3/capture-commands.txt)
record the resource method and reconstruction limits; follow-up
[parser versions](../../../analysis/ableton-live-12.4.3/resource-parser-versions.json)
identify Python 3.14.6, ElementTree 1.3.0, Expat 2.6.3 and SQLite 3.53.4.
Parser versions were recorded during provenance follow-up, not instrumented in
the original capture. Running the script again writes mutable derived summaries;
preserve existing results or redirect its output before a new capture.
The [native index script](../../../analysis/ableton-live-12.4.3/summarize_native.py)
derives summaries from retained REA records and checks executable slice identity.
The [artifact checksums](../../../analysis/ableton-live-12.4.3/artifact-checksums.json)
identify local analysis payloads; they do not cover the complete installed package.
The [native summary](../../../analysis/ableton-live-12.4.3/native-summary.json),
[target inventory](../../../analysis/ableton-live-12.4.3/native-targets.json), and
[symbol index](../../../analysis/ableton-live-12.4.3/live-arm64-symbols.tsv) are
derived navigational views, not additional independent observations.

## Native-phase follow-up captures

The [owned-run preflight](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/)
records the retained main input identity and local REA/Ghidra/JDK configuration.
Actual native progress and limitations belong to the [execution ledger](../native-phase-execution.md).

The [transport-study resource recapture](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/sources-v1/manifest.json)
retains complete bytes for `12.0_12402.txt` and `DefaultLiveSet.als`, plus decoded
XML. All three digests match the earlier resource observations. The recapture
also resolves the earlier `Transport` line ambiguity: line 3807 is the field
inside `LiveSet`; line 8168 is the top-level class. Old capture bytes remain
unchanged. Exact paths, locator offsets, tool versions and fixture-generation
provenance are retained; the [study](../native-transport-study.md) owns findings
and unresolved behavioral questions. Proposed mutated fixtures are analyst inputs,
not observed load/save outcomes.

## Environment and limitations

[Host capture](../../../analysis/ableton-live-12.4.3/evidence/host-environment.json):
macOS 15.2 build 24C101, arm64; Apple LLVM 17.0.0. The `lipo -version` probe
was unsupported; its exact commands and byte-equality checks are retained instead.
[REA environment](../../../analysis/ableton-live-12.4.3/evidence/rea-session-environment.json)
records server identity and provider configuration. Ghidra 12.1.4 with JDK
21.0.12.1 completed the Push2 analysis through REA 6.3.0. Hopper is missing and
IDA is unconfigured.

Large REA results exceeded MCP response limits but were retained and exported;
they were not rerun. The package inventory is complete within its inventory
substep, not complete behavioral analysis. DYLD coverage is explicitly partial.
REA's signature command failed; [direct codesign display](../../../analysis/ableton-live-12.4.3/evidence/codesign-fallback.json)
successfully reported Ableton AG signing identity, runtime flag and entitlements.
Display does not verify signature validity. No `get-task-allow` entitlement was
displayed. [Tool failures](../../../analysis/ableton-live-12.4.3/evidence/tool-limitations.json)
remain retained. No application, packaged script, or Python bytecode was executed.

Canonical synthesis: [package structure](../ableton-package-structure.md).
Next work: [decompilation and specification preparation](../ableton-decompilation-preparation.md).

The selected native captures [v1](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/manifest.json),
[v2](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v2/manifest.json)
and [v3](../../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/manifest.json)
pin target identity, retained method and all output hashes. They use a bounded
no-autoanalysis profile; their pseudocode is generated analysis, not recovered
original C++ source. The [execution ledger](../native-phase-execution.md)
records these outcomes, the first default-analysis failure and the successful
full-analysis retry.

The [linker metadata index](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/summary.json)
decodes the pinned thin image's `LC_FUNCTION_STARTS` payload at file offset
137,089,496 (560,280 bytes). It contains 413,794 linker-declared start addresses
from `0x100002000` through `0x1054d20c4`. The
[sealed manifest](../../../analysis/ableton-live-12.4.3/derived/function-starts-v1/manifest.json)
retains the extractor copy and output hashes. Independent scope review streamed
all entries against the original payload. These are declared starts, not
Ghidra-discovered functions, body ranges or decompiled code; neighboring starts
do not define function sizes. The [design](../function-starts-design.md) records
format checks, resource measurement and review status.


## Main Live default-profile analysis

The [completion record](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/analysis-completion-v1.json)
pins the successful retry's full inventory bundle, analysis log and resource
observations. Inventory evidence ID:
`ev_e2ec1d6bec222974ebac6a973ec92c9453cbe2ac8e30217fa238db931f6211c8`.
The Ghidra 12.1.4 default profile digest is
`5b7927397d54a65b8e4ae3db210b45b6c649ea2022e950843c5906a01c2a487b`.
The complete [retained bundle](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/inventory-evidence.json)
is 121,206,515 bytes with SHA-256
`701547de1c5ba4b0f9b6f6b7e5b6ba67602874bcec015ebc92a0a5c394b5d60f`.
The MCP response was too large; the existing evidence was exported, not rerun.

The [execution ledger](../native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
owns counts, pilot selection and current export progress. Individual revisions
retain pseudocode and provenance; warnings are preserved. Analysis completion
is not complete control-flow recovery, and this profile does not supersede or
rewrite the separately sealed selected-entry captures. No original Live process
or compatibility scenario was executed by this static analysis.

The [session closure manifest](../../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/post-run/manifest-v1.json)
pins the final provider-neutral observation snapshot, close receipts and process
reconciliation. It preserves evidence, not a durable Ghidra database. The source
digest was reverified after shutdown; subsequent bulk work must satisfy the
capacity and recovery gates in the execution ledger.

The [compact mirror experiment](../native-compact-storage.md#measured-mirror--2026-10-10)
retains a separate hashed representation of committed default-profile artifacts
and source envelopes. All original member bytes and source files were unchanged;
its manifest and execution packet pin exact provenance. It adds no decompilation
coverage and does not replace the closed session with a persistent database.

The separately profiled [recovery route](../native-analysis-recovery.md#corrected-import-passes-reopen-capacity-stop--2026-10-12)
now retains actual target language/JVM verification and a saved import. Its first
reopen was refused by fresh-launch capacity, so neither incomplete job is an
accepted checkpoint. Source bytes and the default-profile exports remain
unchanged; these tool-side captures add no application behavior or compatibility
result. Use the linked report for exact commands, hashes and current next steps.
