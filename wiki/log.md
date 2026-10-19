---
id: LOG-WIKI
type: log
status: active
updated: 2026-10-17
access: analysis
---

# Wiki activity log

Append analyst/maintainer entries at the end. Candidate-only work has its own
implementation log. Existing entries are corrected by later entries.

## [2026-10-09] ingest | User supplied LLM Wiki pattern

Retained [selected verbatim excerpts](../raw/public/2026-10-09-llm-wiki-excerpts.md)
and wrote the [source summary](research/sources/llm-wiki.md). The capture is partial;
author and external publication identity were not supplied.

## [2026-10-09] decision | Establish documentation practices

Adopted [ADR 0001](decisions/adr-0001-documentation.md), [schema](schema.md),
[routing](../AGENTS.md), and [workflows](workflows.md). Separated original-side
research/draft specs from reviewed handoffs and implementation docs. Isolation
is a future environment requirement, not an established property of this checkout.

## [2026-10-09] maintenance | Seed project navigation and coverage

Created the [feature map](specs/feature-map.md), [investigation plan](research/ableton-plan.md),
[architecture candidates](implementation/architecture.md), [verification coverage](verification/coverage.md),
and [templates](../templates/index.md). Earlier conversation findings are labeled
as reports without retained raw evidence. All behavioral specifications,
implementation work, and compatibility results remain pending.

## [2026-10-09] ingest | Register existing Ableton analysis outputs

An `analysis/ableton-live-12.4.3/` output tree appeared during documentation setup.
Registered it in the [analysis intake](research/sources/ableton-analysis-intake.md),
classified `analysis/` as analyst-only and Git-ignored, and reconciled current
project status and Q-002. The earlier entry's absence of retained evidence is
superseded by this discovery. Only the derived manifest and native summary were
read during intake; other files are inventoried, not substantively reviewed.
Existing analysis files were not modified.

## [2026-10-09] ingest | Ableton Live 12.4.3 package preparation

Captured [reference identity and evidence](research/sources/ableton-live-12.4.3.md),
[package structure](research/ableton-package-structure.md) and
[decompilation/spec preparation](research/ableton-decompilation-preparation.md).
REA completed inventory, plist/Mach-O inspection and partial arm64 dependency
modeling; oversized responses were recovered by evidence export. Universal Mach-O
was not accepted by explicit Ghidra selection, so byte-identical arm64 slices were
prepared. Ghidra completed Push2 analysis and one entry dossier; its snapshot was
saved. Core Live thin input was accepted without deep analysis. Sessions closed.
REA signature inspection failed; direct codesign display recovered signing metadata,
not signature verification. Resource analysis was delegated and independently
reviewed; 2,941 unique hashes/sizes, nine scope counts and eleven schema locators
matched installed files. Updated Q-002, added Q-006/Q-007 and static coverage.
No original application execution, runtime compatibility claim, implementation
or handoff release occurred. Original resources remain external mutable files.

## [2026-10-09] lint | Initial documentation validation

Checked 38 Markdown documentation files, 26 unique metadata IDs,
172 relative file/heading links, and the matching 13 feature-family IDs
in the spec and verification maps. Required metadata, ISO dates, index coverage,
source excerpt SHA-256, two intake-file digests, implementation link boundaries,
and generated-evidence ignore rules passed. A direct whitespace scan covered
untracked Markdown; `git diff --check` also passed.

The initial pass found three new research pages without index entries; their
catalog links are now present. The initial intake record is superseded by the
canonical package source. Routing and status language were reviewed to distinguish
research, draft specs, implementation, and verification. These checks validate
documentation structure, not binary-analysis correctness, runtime equivalence,
or clean-room environment isolation. Git was initialized without a commit or
remote; application implementation and handoff releases remain pending.

## [2026-10-09] lint | Package-preparation research and evidence

Resource scope review and final evidence-quality review passed after retaining
capture provenance and the universal-Ghidra rejection. Checked 26 wiki/catalog
pages and 144 relative links, required metadata, unique IDs, dates, access labels,
heading targets and inbound catalog links: no unresolved findings. Explicit
whitespace checks and `git diff --check` passed; the documentation is currently
untracked, so the explicit checks cover more than Git's diff. Analysis evidence
and executable slices are ignored. No commit or external publication occurred.
Local checksum manifest records the retained analysis artifacts. These checks
establish documentation/evidence integrity within scope, not runtime compatibility.

## [2026-10-09] decision | Make analysis static-first

User directed that runtime interaction be demoted as much as reasonably possible.
Adopted [ADR 0002](decisions/adr-0002-static-first-analysis.md), updated the
[investigation plan](research/ableton-plan.md),
[spec preparation](research/ableton-decompilation-preparation.md),
[workflows](workflows.md), [milestones](project.md),
[questions Q-006/Q-007](questions.md), research/decision indexes and
[coverage next-evidence priorities](verification/coverage.md).
Static contracts can proceed to review without a blanket runtime prerequisite;
execution is reserved for material gaps, cheaper bounded probes and measured
compatibility obligations. This supersedes the earlier runtime-first loop.
No original execution, new behavior finding, implementation or release occurred;
all compatibility results remain unknown. This is a user-authorized process
choice, not a finding that LLM clean-room projects universally follow this method.

## [2026-10-09] lint | Static-first policy reconciliation

Focused checks passed for ten affected pages: required metadata/date fields,
75 relative file/heading links, whitespace, 26 unique wiki IDs, the new decision's
index entry, unchanged prior log content and all 13 unknown feature verification
states. `git diff --check` passed; direct whitespace checks also covered the
untracked documentation. Reviewed runtime/static wording across the affected
plan, preparation, workflow, coverage and question pages. This pass did not
recheck binary/source hashes, execute Live or establish compatibility/isolation.

## [2026-10-09] ingest | MIDI user mapping static evidence

Captured nineteen documents/bytecode source files from the pinned Live 12.4.3
package; [source record](research/sources/midi-user-mapping-12.4.3.md) links exact
manifests and decoder provenance. Used isolated xdis 6.3.0 to decode seventeen
CPython 3.11 modules without importing/executing target code. Separate tracing
and specification subagents produced [research findings](research/midi-user-mapping.md),
a [13-requirement draft](specs/midi-user-mapping.md), and planned acceptance cases.
Scope review requested narrower malformed-number claims and unmasked channel
cases; fixes and review dispositions are retained with the analysis artifacts.
Updated source/spec indexes, feature map, coverage, project status and Q-006/008–010.
No runtime, clean handoff release, candidate implementation or compatibility pass.

## [2026-10-09] query | Review the proposed reverse-engineering approach

Retained the critique in the canonical [investigation plan](research/ableton-plan.md#review-of-the-proposed-harness-first-approach).
Keep scoped contracts, independent evidence review, GUI interaction coverage,
artifact identity and clean boundaries. Recommend conditional probe/harness
construction rather than upfront replay/plugin/instrumentation prerequisites;
separate static contract confidence from empirical compatibility. Recorded
adapter masking, optional timing context, observation clocks, reference
repeatability and database persistence caveats, with primary technical sources.
This is an assessment of the supplied proposal; ADR 0002 and existing scope
remain unchanged. No harness, diagnostic plugin or runtime tracer was launched.

## [2026-10-09] lint | MIDI draft, method review and evidence integrity

Independent scope recheck and separate quality review approved the bounded
analyst draft after two corrections. A subsequent editorial correction preserved
ADR 0002's cheaper-probe exception; requirements and 46 case groups did not change.
Checked 30 wiki/catalog pages, 219 relative file/heading links, unique metadata
IDs, dates/access labels, inbound indexes and whitespace: passed. All 48 source
and disassembly digest checks passed (some sources intentionally checked twice).
All 46 case IDs are unique, reference the 13 requirement IDs, have not-run/null
actual results, and retain unresolved comparators for unknown expectations.
The local 50-file artifact inventory has SHA-256
`8b3987efb9417ae28b7124afc63780d4dfd0b2091af5fa3f7f3d9a6f4d52cd36`;
it excludes tooling and itself. `git diff --check` passed; direct checks covered
untracked documentation, and the captured bytecode remains ignored. No commit,
publication, reference run, executable fixture validation or handoff release.

## [2026-10-09] maintenance | Make binary artifacts discoverable

Added the [artifact catalog](research/artifacts/index.md) with task-based links,
coverage labels, a complete directory of seventeen Python disassemblies and
native evidence sizes. Linked it from the README, wiki/research indexes and
local analysis READMEs; added a package-containment tree to the canonical
[structure page](research/ableton-package-structure.md#bundle-map). Reconciled
stale Python-decoding status in structure and decompilation preparation with the
completed MIDI investigation. Coverage records navigation-only changes.

Added an offline searchable artifact browser and reproducible analyst generator
at `tools/build_artifact_browser.py`. It indexes retained native-format candidates
and extracts small assembly/callee/string views from the Push2 dossier. A separate
derived-view manifest pins inputs/outputs. Existing captured evidence and checksum
manifests are preserved. A separate navigation reviewer approved clarity and
scope labels. No new binary analysis, target execution or compatibility claim.

## [2026-10-09] lint | Artifact catalog and offline views

Checked 31 wiki/catalog pages and 282 relative file/heading links, required
metadata, unique IDs, dates/access labels, inbound catalogs and whitespace;
all passed. Also checked 22 README links and all 79 hashes in the earlier
package/MIDI inventories: no missing files or changed evidence. The standard
48 source/disassembly checks and `git diff --check` passed. Untracked docs were
covered by direct checks; no commit or external publication occurred.

The browser author verified deterministic regeneration, JavaScript syntax,
41 local HTML links, 1,093 candidate rows, seventeen module links, input/output
digests and 1,590/77/47 assembly/callee/string extraction counts. A headless
Chrome file-URL smoke test timed out after 30 seconds; its launched process was
terminated. Browser rendering and interactive filter execution remain unverified.
The Markdown catalog and direct artifact links provide a noninteractive route.
These checks concern navigation and faithful extraction, not reverse-engineered
behavior or clean implementation readiness.

## [2026-10-09] query | Draft the next major phase

Drafted the [native decompilation roadmap](research/native-decompilation-roadmap.md)
with main Live pseudocode as the first tangible deliverable, systematic batched
export across a pinned discovered-function inventory, resumable evidence storage,
source browsing, focused native behavior studies and a first reviewed handoff.
User additionally requested a pedagogical dimension: the plan now includes an
accessible method guide, evidence-based walkthroughs, a continuously updated
program-structure atlas and independent reader-review gates throughout the phase.

Read-only tool-metadata review identified unpaged procedure inventory, explicit
batch addresses, snapshot/persistence limits and the need to validate a real
controller-to-provider transport. Separate roadmap review requested resource
preflight before main analysis and an explicit first-handoff choice; both are
incorporated. Linked the roadmap from project/research/preparation/artifact pages,
updated planning coverage, and added Q-011 for main-image capacity and recovery.
All phase milestones remain proposed. No binary analysis, installation, runtime
execution, application implementation or handoff release occurred in this task.

## [2026-10-09] lint | Next-phase roadmap and pedagogical design

[Roadmap re-review](../analysis/ableton-live-12.4.3/phase-2-plan/roadmap-recheck.json)
and [technical review](../analysis/ableton-live-12.4.3/phase-2-plan/technical-review.json)
passed for planning. Both identify the exact reviewed draft SHA-256
`f6816729d4945d50aee725fc355329e884ccd0325716a0d45b70c21407604c3b`;
a retained snapshot and checksums preserve that revision. The roadmap stays
`draft`, and review does not establish main-image capacity or execution approval.

Checked 32 wiki/catalog pages, 304 relative file/heading links, frontmatter,
unique IDs, dates/access labels, inbound catalogs, whitespace and the existing
48 source/disassembly hash checks: passed. `git diff --check` passed; direct
checks covered the untracked documentation. New proposed paths are explicitly
marked as future files. No milestone or compatibility status was advanced.

## [2026-10-09] query | Linux analysis host feasibility

Added the [host assessment](research/ableton-plan.md#linux-analysis-host-versus-reference-host)
to the canonical investigation plan. Official Ghidra platform/loader documentation
supports Linux static-analysis feasibility; local pipeline portability is untested.
Recorded transfer/pinning needs, external resources, ephemeral provider state and
the recommendation to retain occasional pinned Mac reference access. No migration,
Live execution or compatibility claim occurred; verification coverage is unchanged.

## [2026-10-09] lint | Linux host assessment

Focused checks passed for the two changed pages: required metadata/dates,
relative file/heading links, direct whitespace scan, existing research index
coverage and unchanged prior log prefix. No source hashes, Linux execution,
provider portability or empirical compatibility were tested.

## [2026-10-09] maintenance | Execute native-phase designs and tooling

User authorized associated designs and execution. Created the [execution
ledger](research/native-phase-execution.md), [export design](research/native-export-design.md)
and [task plan](research/native-export-execution.md), plus the [learning design](research/learning/design-and-plan.md).
Implemented owned REA transport, immutable evidence ingestion and resource/log
monitoring. Scope review followed by independent quality review passed; 18
synthetic integrity/lifecycle tests passed. Reviews and source digests are retained
under `analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/`.

Metadata-only transport smoke passed. The first native open rejected absent
Ghidra configuration; its result was retained and the session closed. A fresh
transport with explicit installed Ghidra/OpenJDK paths accepted the pinned main
arm64 image and started its first deep inventory analysis. It remains in flight
at this entry; no main pseudocode or function count is claimed. Resource samples
and bounded provider logs are being retained. No original Live execution or
candidate implementation occurred.

Published the initial [learning route](research/learning/index.md), method,
bytecode example and program atlas. Independent reader review checked 52
links/anchors and three verbatim bytecode excerpts with no findings. This review
covers the initial materials, not the planned main-code lessons. The existing
artifact browser is being extended; the user explicitly requested continued
updates and preservation of its `#python` entry point. Compatibility remains
unknown, and the phase ledger keeps unfinished gates visible.

## [2026-10-09] maintenance | Living artifact browser and native study preparation

Executed the [browser design](research/artifacts/browser-design-and-plan.md):
retained `#python`, linked the learning materials and program atlas, and added
`#native` as a paginated projection of committed corpus coverage. Code and full
evidence stay in linked files. Scope/quality review found and corrected excluded
function attempts, unsupported success rows, and a coverage/manifest publication
race. Nine focused tests pass, including pagination/filter script execution in a
DOM stub and lock contention. Fifty-one browser links/anchors and 26 manifest
digests pass. A bounded Chrome attempt timed out; real rendering and large-corpus
performance remain unverified. No native outputs existed at browser generation.

Prepared the [transport study](research/native-transport-study.md) from pinned
resource observations and exact symbol rows. Loop-enable persistence and
Start/Stop are scoped questions with proposed cases; semantics await native code.
The study preserves a schema line-locator conflict instead of silently rewriting
prior evidence. Main analysis remains in flight under its owned resource monitor.

## [2026-10-09] lint | Execution designs, learning materials and browser

Full documentation checks passed: 42 pages, 417 relative file/heading links,
metadata/indexes/whitespace and 48 existing source/disassembly hash checks.
Transport/export and browser reviews record exact source digests. These are
tooling/navigation checks; no original-versus-candidate comparison was performed.

## [2026-10-09] maintenance | Neovim Markdown reading

User selected Neovim and authorized navigation plus rendering. Installed pinned
render-markdown.nvim and Mkdnflow plugins in the user's existing vim-plug setup;
added the separate dotfiles `lua/markdown_reading.lua` configuration and plugin
entries in `init.lua`. Reused bundled parsers. Documented controls, portability
and scope in [editor navigation](editor-navigation.md), linked from the wiki index
and README. Real-config smoke checks passed for relative links, heading anchors,
back navigation and rendering decorations. The existing fuzzy.nvim startup warning
remains unrelated. No application code, reference evidence or compatibility
coverage changed; plain Vim was not modified.

## [2026-10-09] lint | Editor navigation documentation

Focused checks passed for the four changed documentation files: required wiki
metadata/dates, relative file/heading links, whitespace, new page index entry and
append-only log prefix. Project `git diff --check` passed; direct scans covered
untracked Markdown. No binary evidence or compatibility coverage was revalidated.

## [2026-10-09] ingest | Retain loop-state study sources and proposed inputs

Retained the exact shipped schema/default ALS and decoded XML with hashes
matching prior resource observations. The [transport study](research/native-transport-study.md)
now resolves the nested `LiveSet/Transport` line 3807 versus top-level `Transport`
line 8168; the older summaries remain immutable. Generated twelve proposed
loop-field mutations using exact byte patches and deterministic gzip settings.
Independent review checked 29 resource/fixture files, locator offsets, XML
parsing, round trips and deterministic recompression with no material findings.
All reference-load and behavioral expectations remain unknown. Updated the
canonical installed-source page with retention and corrected-locator provenance.

## [2026-10-09] maintenance | Restore Leap s/S navigation

Diagnosed the existing Leap legacy setup helper skipping s/S because `hasmapto`
matched plugin compatibility aliases. Added two explicit normal/visual mappings
in the separate dotfiles `init.lua`; Markdown mappings were not the cause.
Updated [editor navigation](editor-navigation.md) with the diagnosis, bindings
and startup-validation scope. A post-VimEnter reproduction failed before the fix
and passed afterward, including real forward/backward jumps and Markdown mapping
coexistence. Existing fuzzy.nvim warning remains. No compatibility coverage changed.

## [2026-10-09] lint | Leap navigation repair

Focused documentation checks passed: changed-page whitespace, existing index
entry and the new local log link. Metadata and earlier log entries were preserved.
Project and dotfiles whitespace diffs were checked separately. The runtime smoke
check covers editor behavior only; no Ableton evidence or application was tested.

## [2026-10-09] maintenance | Preserve native address-space identities

Installed provider source inspection established that procedure inventory includes
external functions with space-qualified addresses such as `EXTERNAL:0x1`.
Corrected the corpus importer and browser to preserve address-space identity,
encoded names and numeric offset ordering. External records remain excluded from
the decompilation queue. Scope review identified the local volume's case-insensitive
path collision risk; the inventory now rejects case-colliding addresses before
writes rather than merging distinct entries. Scope and quality re-reviews passed;
31 tests pass across exporter, browser and transport. Exact code/provider hashes
and limitations are retained in the two address-space review records.

Added a reviewed method explanation distinguishing open/inventory/export/interpret/
comparison states, and advanced the atlas with the declared loop-field schema
relationship. Native object relationships remain unknown. Main Ghidra analysis
is still in flight; process diagnostics show advancement from constant propagation
to operand-reference analysis. No main function count or pseudocode is claimed.

## [2026-10-09] ingest | Main analysis stop and selected native code

The default main inventory attempt stopped after 39.5 minutes at the 3 GiB disk
floor. Retained the failed response, resource samples, analyzer logs and
identity-checked cleanup record. No default inventory was produced. A reviewed
bounded no-autoanalysis route then exported 17 of 24 selected entries over three
sealed runs; seven body-validation failures remain explicit. Independently
verified each run manifest. Updated execution, source, preparation, coverage and
Q-011. The user freed disk space; a scoped pool-sizing probe and aggregate-RSS
watchdog amendment prepare a changed-condition retry. Compatibility remains
unknown; no original Live runtime scenario or candidate implementation ran.

## [2026-10-09] maintenance | Selected code shelf and monitored retry

Independent scope then quality reviews passed the selected-code browser:
20 tests, 17 exports and seven failed outcomes from three sealed captures.
Direct pseudocode/assembly/metadata links and both native lessons are published;
`#python` remains stable. Real-browser rendering remains unverified. The revised
aggregate-RSS monitor passed both reviews; retained a fresh preflight and
launched one full-analysis retry with two-worker default pools, a 4 GiB heap,
one-second resource samples and the existing disk reserve. No default
inventory has yet returned. Native packets still do not establish externally
observable transport contracts; a finite MIDI configuration handoff candidate
is being prepared under the roadmap fallback.

## [2026-10-09] query | Native teaching packets reviewed

Two native investigations now retain the selected call paths, assembly and
pseudocode: loop-related construction and Start/Stop wrapper destinations.
Updated the program atlas, method guide and two walkthroughs. Independent
reader review verified eight page hashes, 195 links/anchors, eleven packet
artifact hashes and the quoted excerpts. Teaching acceptance passed; persisted
loop defaults and transport effects remain unresolved. These findings support
the explicit MIDI fallback for the first finite handoff, not an invented native
behavioral contract.

## [2026-10-09] query | Actual launch did not retain requested pool settings

Correction to the retry entry above: a standalone JVM accepted the two pool
settings, but the active REA-launched JVM did not retain them. Its captured
command line lacks ActiveProcessorCount and sets cpu.core.override to empty;
the process sampler observed nine native decompiler children. Retained actual
command/properties/thread captures under transport-retry-v3/diagnostics. The
new disk capacity and aggregate monitor remain effective changed conditions;
the two-worker intention is not an achieved property of this run. Corrected
the execution ledger and requested a bounded installed-launch source trace.

## [2026-10-09] release | Finite MIDI configuration handoff

Published immutable local handoff `midi-config-v1` after independent scope,
quality and final isolated-package checks. The four partial clauses cover only
master/cue/crossfader assignment interpretation. All 54 fixtures and substantive
case expectations are unchanged from the reviewed candidate; 60 final files and
59 payload hashes verified. Catalog records manifest SHA-256
`9e3ab46efba170f61bcd7b9fce5d579c263aefd90097dc06695339594308b6ee`.
Updated project/spec/research/verification navigation and implementation-side
release metadata. Reference and candidate executions remain not-run, wider MIDI
requirements remain draft, and no implementation workspace is provisioned.
This is the native roadmap's explicit fallback; it does not close native
transport/persistence semantics or whole-binary export gates.

## [2026-10-09] ingest | Linker-declared function-start navigation

Added a strict, bounded metadata extractor and a sealed index of 413,794
linker-declared main-image starts. Actual extraction took 1.04 seconds with
31.5 MB process peak RSS; twelve tests and independent scope/quality reviews
passed. Independent review decoded the complete table against the retained
binary. Updated source, atlas and design; all 24 selected entries also occur in
this metadata, without changing their export outcomes. A separate browser shelf
provides count and direct table/provenance links. This index is not the missing
Ghidra inventory, body coverage, original source or a new export denominator.

## [2026-10-09] lint | Reviewed tooling and local release checkpoint

The combined analyst-tool suite passed all 71 tests; exact tool/test hashes and
output are retained in native-live-arm64-v1/preflight/tool-suite-v1.json and its
text capture. Regenerated the offline browser after reviewed changes. Full wiki
check passed 47 pages, 606 relative links and 48 earlier source/disassembly
hashes; the new metadata/native/release manifests have separate retained checks.
No real-browser rendering pass or original-versus-candidate compatibility is
claimed. Full native inventory remains in flight.

## [2026-10-09] maintenance | Preserve reviewed draft versions

Publication updates advanced two mutable wiki pages pinned by the handoff's
analyst traceability. Retained exact reviewed copies by reversing the recorded
publication-only edits and matching their pre-existing SHA-256 pins; recorded
that reconstruction explicitly. Independent focused retention review verified
both snapshots, the other ten unchanged source pins and every published release
file. Corrected the plan's stale pending-review disposition. No behavior, fixture,
case expectation or released payload changed.

## [2026-10-09] query | Persistent native recovery design

Drafted the [recovery design](research/native-analysis-recovery.md) while the
single full REA retry remains active. Installed source establishes that ordinary
headless processing restarts analysis scheduling and can run an extra untimed
pass after post-scripts. The proposed route therefore separates a saved import,
a bounded analysis stage and exports with analysis disabled. Actual JVM gates,
closed-project verification and storage admission remain unimplemented/unproven.
Linked the research index, export design and phase ledger. Independent design
review is pending; no additional analyzer was launched.

## [2026-10-09] ingest | Full main-image inventory and default pilot

After the user freed disk space, the single retry completed Ghidra analysis in
3,016 reported seconds. The [completion record](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/analysis-completion-v1.json)
pins full retained evidence exported after the MCP size limit, without repeating
the query. The [phase ledger](research/native-phase-execution.md#full-analysis-checkpoint)
records the frozen inventory and twenty successful pilot exports with warnings.
The two original Start/Stop wrapper seeds were absent as exact discovered entries;
their known branch destinations were verified and substituted for the pilot.
Updated source, preparation, questions and coverage; runtime compatibility remains
unknown. The selected-profile failures remain unchanged. Actual full-scale costs
require grouped ingestion and attempted-first browser loading before bulk work.

The [recovery design](research/native-analysis-recovery.md) received independent
[design review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/native-recovery-quality-review-v1.json)
after correcting gate-load failure handling. It is a contingency, not implemented
persistence. The current provider remains open; no competing analyzer was started.

## [2026-10-09] query | Shared transport helper and profile comparison

The [native study](research/native-transport-study.md#default-profile-comparison-and-shared-helper)
now records the default-profile Stop warnings at the same computed transfers
that failed the selected profile. A focused follow-up established memory access
widths in a shared record-building path and a small byte getter. Its large caller
list caused an MCP size limit; retained evidence was exported without repeating
the query. Updated the wrapper lesson and atlas revision 6. The
[independent semantic review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/default-transport-packet-review-v1.json)
verified source hashes, assembly and careful observed/inferred/unknown wording.
The indirect consumer and external behavior remain unresolved; released handoff
bytes and compatibility coverage are unchanged.


## [2026-10-10] maintenance | Reviewed exports, browser checkpoints and capacity closure

The [phase report](research/native-phase-execution.md#stratified-checkpoint-and-phase-report--2026-10-10)
records two completed 1,000-function stages and the remaining export gate. The
first stage was contiguous; the second used independently checked address strata.
Both retain exact requests, source hashes, method copies, resource checks and
checkpoint results. The independent final stage review verified new revisions
and unchanged prior payloads, then recommended stopping further bulk work until
a durable storage budget or reviewed compact format provides adequate margin.
These sample-derived scenarios are not whole-program size or timing forecasts.

Grouped ingestion and attempted-first/lazy-full browsing passed independent
scope and quality reviews. The [84-test tool suite](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/tool-suite-v2.json)
pins final source hashes; [frozen methods](../analysis/ableton-live-12.4.3/native-live-arm64-v1/methods/export-and-browser-v2/manifest.json)
preserve those tools and design snapshots. Updated export/browser designs and
execution pages. The [final browser check](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/browser-checkpoint-2026-10-10-v1/report.json)
verified generated hashes, local links and stable anchors, including `#python`.
No real-browser visual pass or original-versus-candidate test was performed.

Saved the provider-neutral analysis snapshot and closed the owned provider,
controller and monitor. The [closure manifest](../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-retry-v3/post-run/manifest-v1.json)
pins receipts, logs and identity reconciliation: no owned survivors or temporary
Ghidra directory remain. This preserves observations, not the ephemeral native
database. Updated sources, questions and coverage; all compatibility results
remain unknown. Reverified the released MIDI handoff's unchanged manifest and
59 payloads; its 54 comparison cases remain unexecuted.


## [2026-10-10] lint | Final native checkpoint documentation

The [final validation record](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v4/report.json)
retains the wiki checker, output and whitespace check, and rechecks final tool
source pins, frozen methods, stage-summary pins, session-closure pins and released
handoff bytes. The separate browser and stage reviews establish their explicitly
named scopes; none is a runtime compatibility pass.

The preceding v3 validation attempt retained an error for its not-yet-written
report link, while the old checker returned exit zero despite a nonempty error
list. That attempt's pass label is superseded by v4. The retained v4 checker
returns nonzero on documentation errors, and the runner also inspects the error
list explicitly. Earlier captures remain unchanged.


## [2026-10-10] query | Continuation capacity and exact compact archives

The user requested continuation after the prior capacity checkpoint. Reverified
the retained arm64 source and captured fresh free disk, host state and allocated
payload sizes in [continuation preflight](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/continuation-v1/host-and-storage.json).
No native analyzer or old transport lock was present. Drafted the canonical
[compact archive and continuation plan](research/native-compact-storage.md),
assigned one tooling author, and commissioned a separate read-only audit of
the persistent design. Updated recovery design activation and added the
[storage/recovery lesson](research/learning/walkthroughs/artifact-storage-and-recovery.md).
New compressed storage savings and cold native recovery remain unproven until
actual round-trip and save/reopen captures exist.

## [2026-10-10] query | Compact archive failure review and reader clarity

The initial scope review exposed a failed-rename publication window; author
revision 2 fixed it. Separate quality review reproduced a later output-directory
sync failure after the completion marker had been removed, and internally
consistent archive changes which disagreed with unchanged source envelopes.
The retained [publication reproduction](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v1/publication-tail-reproduction.stdout.txt)
and [source-agreement reproduction](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v1/source-authority-reproduction.stdout.txt)
cover synthetic fixtures, not changes to Live captures. Returned both findings
to the same author for corrections and scope/quality rereview before real use.

A separate reader review identified ambiguous storage wording and missing
navigation/counts. Updated the [storage lesson](research/learning/walkthroughs/artifact-storage-and-recovery.md)
with direct browser links, code-versus-metadata sizes, the retained/pending counts
and the fact that a mirror neither exports more functions nor frees space while
old evidence remains. Expanded the canonical plan with concrete viewer limits,
revision selection and exact-byte download criteria.

The [reader rereview](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/storage-learning-review-v2/report.md)
passed the revised lesson's clarity for its exact retained page hash. Root
reverified all five payload pins, and all 27 sealed quality-review payload pins.
These are documentation/review results, not archive execution, database recovery
or behavioral compatibility results.

## [2026-10-10] query | Compact tool approved; execution wrapper corrected

Author revision 3 passed independent [scope](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-scope-review-v3/scope-review.json)
and [quality](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-quality-review-v2/quality-review.json)
rereviews, including the shared evidence authority and explicit completion commit.
The 63 compact/exporter tests and independently replayed failure/contradiction
cases name their exact method pins. Root verified the 23 scope and 37 quality
payload pins. No real-corpus mirror has run yet.

A narrow [execution-wrapper review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-runner-review-v1/runner-review.json)
found missing cleanup on monitoring exceptions and wrapper-exit ambiguity. Root
retained that method and authored a separate `run-mirror-v2.py` using a direct
Python child and finally-based closure, now awaiting rereview. Fresh target/host
capture remains distinct from earlier capacity records. Assigned a fresh offline
viewer author with fixture-only execution; real generation stays under root after
both reviews. Existing source captures and handoff releases remain unchanged.


## [2026-10-10] query | Real compact mirror and preserved source evidence

The execution wrapper required a further revision after repeated interruption
could abandon cleanup. Retained revision 3 passed independent
[scope](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-runner-review-v3/runner-review.json)
and [quality](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-runner-quality-v1/quality-review.json)
replays. Root reverified 225 review payload pins before fresh admission.

The [actual mirror packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-mirror-v1/manifest-v1.json)
records successful build, check and named extraction. All 6,135 members match
original bytes; source hashes, sizes, modification times and allocation remain
unchanged. The [canonical storage page](research/native-compact-storage.md#measured-mirror--2026-10-10)
owns the measured representation sizes and resource limits. Originals were
retained: the experiment adds storage and generates no additional code. All
three owned workers closed without survivors.

Updated the phase ledger, source record, artifact catalog, storage lesson, Q-011
and coverage distinction. The offline viewer author passed 43 synthetic browser
tests and entered fresh scope review; actual viewer generation and durable
native database recovery remain pending. Compatibility remains unknown.


## [2026-10-10] query | Compact reader scope pass and quality type gap

The [independent scope review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v1/scope-review.json)
passed revision 1, including exact payload comparisons, publication failure
windows and Node DOM callback/download cases. Separate quality review then
reproduced malformed array profile/identity values accepted by JavaScript while
Python rejected them. Returned the finding to the same author for explicit type
validation and regression cases, then scope/quality rereview on new pins.
Actual viewer generation remains pending; original artifacts and archive remain
unchanged. These are analyst tooling results, not application behavior results.


## [2026-10-10] query | Real reader build rejects composed-workflow provenance

Final reader revision 2 passed [scope](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v2/scope-review.json)
and [quality](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v2/quality-review.json)
rereviews, including 44 browser tests. Root verified 435 final review payload
pins and admitted real generation from fresh host measurements. The build
rejected a valid composed-workflow profile because the reader compared original
revision profile metadata directly with the resolved native run profile.

The [sealed failure](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v1/manifest-v1.json)
retains the exact metadata/member locator, command, resources and closure.
Source, archive and prior browser bytes/mtimes were reverified unchanged. The
worker exited cleanly, and no reader was published. Returned the mismatch to
the same author for source-authority alignment, original/effective profile
provenance and representative regressions. Paused the new persistent-driver
author to keep coding ownership sequential; no JVM fixtures had launched.

## [2026-10-11] query | Reader source profiles and scalar-type correction

Reader revision 3 preserves the original workflow profile and derives the native
profile from the exact retained record provider. Its
[scope review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v3/scope-review.json)
passed 48 browser tests and independent source-binding cases. Root verified all
23 author and 99 scope payload pins. A bounded
[real-schema projection](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/real-profile-projection.json)
passed all 2,028 revisions without viewer publication or inventory parsing.

Separate [quality review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v3/quality-review.json)
found that Python profile equality accepts a boolean replaced by numeric `1`
against unchanged source data. Root verified its 418 sealed payload pins and
returned the blocker to the same author for typed JSON equality and paired
regressions. The completed test session was confirmed closed; the unrelated REA
MCP server remained untouched. Actual publication and Task 3 coding remain
pending. The [storage lesson](research/learning/walkthroughs/artifact-storage-and-recovery.md)
documents the real workflow-profile failure; an independent pedagogy review is
checking its frozen bytes and navigation.

## [2026-10-11] query | Offline native code reader published and checked

Final reader revision 4 passed independent
[scope](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-scope-v4/scope-review.json)
and [quality](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-quality-v4/quality-review.json)
rereviews, with 51 browser tests and independently reproduced correction of the
raw-profile boolean/number gap. Root reverified all 152 final author/review
payload pins before fresh admission. The
[actual execution](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/compact-viewer-execution-v2/manifest-v1.json)
passed build, independent check and main-browser regeneration. All monitored
workers and verifier sessions closed. Original source/archive bytes and
modification times remained unchanged.

The [canonical publication record](research/native-compact-storage.md#measured-reader--2026-10-11)
owns sizes, resource measurements, 2,239 hash checks, 6,223 local links and all
2,028 exact code downloads under the DOM stub. The main browser preserves its
`#python` and other native anchors and links the new reader. Actual browser
rendering/accessibility remains untested; no additional code or compatibility
coverage is claimed.

The [pedagogy review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/storage-learning-review-v3/report.md)
found no misleading claim in its frozen lesson/navigation snapshot. Root verified
its nine payload pins, then applied the optional first-function example and
current-status link, and added actual publication evidence. Its review does not
certify the later page bytes. Updated the catalog, browser plan, learning index,
phase ledger, Q-011, source date and coverage distinction. The persistent-driver
author resumed as sole code author; fixture launches are conditional on fresh
four-GiB admission and the verified closure of reader workers. Live target
admission remains root-owned after code/fixture scope and quality reviews.

## [2026-10-11] query | Historical recovery fixtures and teaching review

The [recovery design](research/native-analysis-recovery.md#preparation-observations--2026-10-11)
now records actual historical JDK-version/attach failures and tiny baseline/finite
analysis save-reopen successes under their captured method revisions. Controller
acceptance rules are still being hardened; these runs do not certify final tools
or a Live checkpoint. The design accounts for all four retained project
representations and retains the original resource minimums. No Live target stage
has been launched.

The [storage/recovery lesson](research/learning/walkthroughs/artifact-storage-and-recovery.md)
explains the small raw fixture, measured JVM settings, closed source checkpoint,
disposable copies and the separate coverage obligations. The independent
[first readability review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/recovery-learning-review-v1/report.md)
found stale blanket pending wording despite historical successes. Its own first
path-check failure is retained as a reviewer-method error, not a pipeline failure.
Root corrected the wording and labeled the earlier source-only review.
The [narrow rereview](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/recovery-learning-review-v2/report.md)
passed 60 locators and 112 current input pins. Root reverified all ten rereview
payloads and all 112 current pins; the nine-payload first packet remains unchanged.
This is documentation/evidence review, not final controller, target, browser or
application certification.

## [2026-10-11] query | Persistent driver frozen for independent review

The [canonical recovery design](research/native-analysis-recovery.md#frozen-driver-and-proof-packet--2026-10-11)
now links the readable author guide, exact CLI and proof matrix. Root reverified
all 4,766 sealed payloads and 11 current source captures. The retained proofs
distinguish the historical full suite, publication replay and affected final-code
replays; no complete historical suite is claimed under the final controller.
Independent scope review is underway; separate quality review and actual Live
admission remain required. Production methods are frozen.

The [immutable artifact recheck](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/immutable-artifact-check-v2.json)
passed 6,135 original corpus files, 12 archive files, 59 released handoff payloads
and the retained arm64 source. Its first comparison incorrectly treated an extra
measured allocation field as an archive mismatch; that failed method record is
preserved. The corrected comparison checks each recorded field exactly and
found no changed field. Updated the artifact catalog, tools guide, phase ledger,
compact plan and Q-011. No Live target stage, new default export, installation or
application implementation occurred.

## [2026-10-11] query | Recovery scope review blocks target launch

Independent scope review reproduced two failures against the frozen v1 controller:
[unregistered launch after identity lookup failure](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/results/launch-identity-failure.json)
and [successful checkpoint commit after the whole-job deadline](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/results/expired-checkpoint-commit.json).
The first probe uses a mocked termination-ignoring child; the second uses a
retained fixture checkpoint and a mocked expired clock while exercising its
actual evidence/commit validation. Neither probe launched a JVM or Live.
The 43 frozen tests pass but do not cover these failures. Returned both blockers
to the sole author for regression tests and a new immutable packet. Live launch
remains blocked pending fresh scope and separate quality reviews. The
[recovery page](research/native-analysis-recovery.md#frozen-driver-and-proof-packet--2026-10-11)
records these failures without rewriting the successful historical fixture cases.

The [failed scope packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v1/scope-review.json)
is now sealed; root verified all 259 payload pins. Its 27 passing offline checks
cover accepted historical checkpoints/inventories/exports, negative acceptance
cases and resource-formula boundaries, alongside the two reproduced blockers.
The narrow [teaching clarification](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/recovery-learning-review-v4/report.md)
passes documentation readability while explicitly retaining failed tooling
approval and unknown Live persistence. Root verified all 15 payloads across its
v3/v4 packets. Later status edits are not covered by those page-snapshot hashes.

## [2026-10-12] query | Cancellation during process construction

Before sealing the corrected recovery driver, a scoped
[actual Python probe](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/popen-interrupt-probe/result.json)
reproduced cancellation after a child was created but before its `Popen`
constructor returned and ownership was registered. The owner incorrectly
reported empty clean closure; the probe's cleanup safely killed and reaped the
exact child. This is a concrete failure under the captured candidate methods,
not a Live failure. The sole author is adding deferred cancellation across
process creation/registration and retaining new regression proofs. Earlier
51-test and positive-replay successes remain historical for their methods.
No Live stage is admitted before the final correction and fresh scope/quality
reviews. The [recovery page](research/native-analysis-recovery.md) tracks the gap.

## [2026-10-12] query | Corrected recovery driver and final fixture replay

The [author-v2 packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v2/README.md)
is sealed; root verified all 2,635 payloads and the final controller/test pins.
It retains the original review failures, intermediate positive replays, actual
constructor-interruption failure and final corrections without rewriting v1.
The final controller passes 52 tests and nine actual synthetic Ghidra launches;
three actual constructor-cancellation children were tracked and closed/reaped.
The existing-output ownership regression and non-JVM cancellation/late-publication
proofs are retained separately. No complete historical negative JVM matrix is
claimed under the final methods.

Updated the [canonical recovery page](research/native-analysis-recovery.md#corrected-driver-ready-for-review--2026-10-12),
tools guide and artifact catalog. Fresh scope review is underway; separate
quality and root target admission remain pending. The
[post-fixture host check](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/host-after-fixtures.json)
found no native analyzer processes and reverified the target bytes. Its free disk
is a timestamped observation, not permission for a later analysis stage.

## [2026-10-12] query | Recovery deadline still paused during reporting

Fresh scope review of the frozen v2 controller reproduced a
[paused non-cleanup tail](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v2/results/paused-stage-tail.json).
After mocked process cleanup completed, a real 0.3-second job alarm could not
cancel a 1.1-second injected target-hashing wait because the guard remained
paused through hashing and stage publication. No JVM ran, no success was accepted
and the incomplete marker remained, but the job exceeded its cancellation bound.
Returned this concrete remaining deadline gap to the same author for a narrow
correction, regression and concise new immutable packet. V2 successful tests
and fixture captures remain valid for their recorded cases; Live launch remains
blocked pending fresh scope and separate quality review.

## [2026-10-12] maintenance | Recovery deadline correction sealed

The same author froze the [revision-3 delta packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v3/README.md).
Root rehashed all 253 payloads and all 45 sealed scope-v2 payloads. The new
controller passes 54 tests and three actual fixture import/reopen launches;
real alarm probes cancel delayed hashing and failure reporting within their
0.3-second bounds. Prior v2 workflow proofs retain their original method lineage.
Updated the canonical recovery page and tools guide. Fresh scope review is
underway; separate quality and Live admission remain pending.

## [2026-10-12] query | Recovery scope passes; complete tooling suite passes

The independent [scope-v3 review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v3/scope-review.json)
passes the frozen controller, two independently reproduced real-alarm probes and
retained final fixture import/reopen evidence. Root rehashed all 42 review
payloads. A fresh separate quality reviewer is auditing the public route before
Live admission. Root also ran the full analyst-tool suite: 196 tests pass;
[command receipt and logs](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/full-tool-suite-command.json)
retain the actual invocation. Added the rejection-versus-cancellation distinction
to the storage/recovery lesson; earlier documentation reviews apply only to their
captured versions. No application compatibility status changed.

## [2026-10-12] query | Reviewed first Live import rejected its language assumption

The sealed [quality-v1 review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-quality-v1/README.md)
passes revision 3 with 54 tests and 22 additional checks. Root verified all 39
review payloads, then freshly rehashed the target and installed methods, checked
host resources and obtained both writer locks nonblocking before admission.
The direct CLI imported the pinned target with analysis disabled; the loader
selected AppleSilicon while the profile expected generic v8A. The strict gate
rejected the mismatch. [Execution evidence](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v1/README.md)
and the failed job are sealed; root verified seven packet and 57 failed-job
payloads. Owned identities are closed/reaped with no survivors, target bytes
unchanged; incomplete output and failed project locks remain intact.

Updated canonical recovery, plan, phase ledger, catalog and coverage. Returned
the concrete target-versus-fixture profile error to the sole author for a narrow
revision, installed-source evidence, regression and three fixture launches.
New reviews precede a fresh-directory retry. No target checkpoint, bounded
analysis, new pseudocode or application compatibility result was accepted.

## [2026-10-12] maintenance | Loader-matched profile correction frozen

Root verified all 255 payloads in the [author-v4 delta packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-author-v4/README.md).
Installed loader opinions and language/compiler definitions explain the observed
AppleSilicon choice. Immutable target and raw-fixture profiles now have distinct
IDs and canonical hashes; exact Java checks and original budgets are unchanged.
The new controller passes 56 tests and three actual raw-fixture import/reopen
launches. The config-only target routing case is explicitly digest-stubbed,
not a positive Live proof. Fresh scope is underway, then quality before root
retry. Updated canonical profile/design status, tools guide, artifact catalog
and lesson; first failed target evidence remains immutable.

## [2026-10-12] query | Loader correction scope passes

The [scope-v4 packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-scope-v4/scope-review.json)
passes 56 tests, installed-source agreement, config routing and checkpoint
profile binding. Root verified its 46 payloads and all 11 current method source
pins. The final full tooling suite passes 198 tests; [receipt](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/full-tool-suite-v4-command.json)
retains the rerun required by the profile code change. Separate narrow quality
review is underway. The first failed target job remains sealed and untouched;
no retry, accepted checkpoint, new pseudocode or application compatibility pass.

## [2026-10-12] query | Actual target settings and save pass; reopen capacity stops

The [quality-v2 review](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-quality-v2/quality-review.json)
passes the narrow profile correction with 56 tests and 18 cases. Root rehashed
all 27 review payloads, rechecked fresh host/method/target hashes and writer locks,
then used the original direct CLI into a new output. The actual Live import stage
passes exact AppleSilicon/default language, external JVM/pool diagnostics,
controller acknowledgment, save and normal owned closure. Its closed project is
345,047,040 allocated bytes. First reopen is refused before JVM startup at
6,116,376,576 free bytes against 6,442,450,944 required. No accepted checkpoint,
analysis or new pseudocode results. Both incomplete jobs and all evidence remain.

The [second execution packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/persistent-execution-v2/README.md)
is sealed; root verified nine packet and 81 failed-job payloads, copied-project
byte agreement and absence of every retained owned identity. A root verifier
initially passed a job path to a child-path helper; its setup error is retained,
and the correctly addressed public checkpoint reader rejects incomplete output.
No production code changed. Updated canonical recovery/resource/next-step status,
plan, phase ledger, artifact catalog, source guidance, lesson, coverage and Q-011.
Recommended 10 GiB fresh import headroom is additional planning capacity; tool
limits stay unchanged. The provisional analysis reserve is 13.54 GiB after an
accepted baseline, which remains unproved. No further retry or repair is authorized
by unchanged available capacity. All application compatibility rows remain unknown.

## [2026-10-12] lint | Reviewed continuation closed at the capacity gate

The [final validation packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/README.md)
records scope/quality PASS, final 198-test tooling PASS, two real static target
attempts and the blocked cold-reopen milestone. Root verified current installed
methods and source pins, retained failed-job manifests, 6,135 default payloads,
12 compact files, 59 released handoff payloads, 24 reader and six main-browser
outputs, target bytes and 48 legacy source/disassembly pins. Recorded metadata
fields agree where checked. No code/browser output or application compatibility
coverage was added. Existing #python navigation remains byte-identical.

Mechanical lint covered 50 live pages, frontmatter/IDs/index coverage, relative
file/heading links and evidence paths, with no errors; git diff --check is clean.
Final lint output after this entry is retained in the packet. Semantic review
keeps observed fixture/import/save facts separate from unknown reopen/analyzed
recovery and every application compatibility row. Raw captures and the released
handoff remain unchanged; logs were appended. The final host snapshot contains
no analyzer and 6.70 GiB free, below proposed 10 GiB fresh-import headroom.
More capacity precedes a fresh import; B's 13.54 GiB estimate is provisional
until a baseline is accepted and remeasured. No commit or external publication.

## [2026-10-12] maintenance | Final continuation evidence sealed

The [final packet manifest](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5/manifest-v1.json)
is SHA `2e3ca1c9cd905f1929be619ba64d9616ff3ed13c2d836c99e273b16e875fb771`;
root independently verified all 66 payloads. It includes 17 exact documentation
snapshots, final 198-test logs, current method/target pins, review/actual-execution
checks, preserved-artifact checks and the 50-page/878-link zero-error lint.
This seal entry follows that snapshot; it does not silently revise the packet.
The [independent manifest receipt](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/final-validation-v5-manifest-check.json)
records the final hash check. Current target status remains import/save proved,
first cold reopen capacity-blocked, no new pseudocode or accepted checkpoint.

## [2026-10-12] maintenance | Read revisions now reveals its code

The [reader interaction repair](research/native-compact-storage.md#read-revisions-interaction-fix--2026-10-12)
records the actual local-file reproduction: code loaded below the visible
viewport. Added focus/scroll, reader height before asynchronous loading, code
before collapsed provenance and return navigation. Published a fresh v2 and
regenerated the main browser with existing anchors; v1 and compact archive remain
byte/hash/mtime unchanged. No code exports or compatibility coverage were added.
Three regressions were first observed failing; the initial 54-test browser suite
passed and the final CSS-inclusive 26-test independent scope review passed.
Chrome 153.0.8010.53 at 1280x900 verifies mouse/Enter selection, visible code, focus,
return link and exact 134-byte Blob download for one case. Root inspected its
screenshot and verified 38 review payloads, 37 original archive/reader files,
seven previous-browser backup files and 2,239 main-browser input/output hashes.
Earlier candidate and harness failures remain retained in the repair packet.
Updated canonical storage page, artifact guide/design, learning lesson, phase
ledger, research index, analyst navigation coverage and tool instructions.

## [2026-10-12] query | Disk cleanup candidates with Trash excluded

The [read-only storage inventory](research/native-analysis-recovery.md#disk-cleanup-inventory--2026-10-12)
records Downloads, separate Live Trial and tool-managed caches as capacity
candidates. User explicitly forbids emptying Trash; revised recommendations
exclude it. Root verified 23 initial and two revised audit payloads. No user
files were moved/deleted, no cleanup command ran, and protected reference/evidence
remains intact. Directory allocation is an upper bound, not exclusive reclaim.
Capacity remains below proposed 10 GiB fresh-import headroom; existing launch and
analysis gates are unchanged. Updated Q-011 and the canonical recovery page.

## [2026-10-12] query | Incoming register in the first browsed function

The [incoming-register lesson](research/learning/walkthroughs/incoming-registers.md)
answers why FUN_100002000 declares and tests in_w5. A bounded LLVM decode of
seven instructions in the pinned arm64 image confirms an incoming w5 test,
subsequent x5 address setup and direct branches to two targets. The C-like
capture omits that setup and displays inferred void/no-argument interfaces.
Caller/prototype/target semantics remain unknown; no Live or decompiler launch,
original capture edit, new pseudocode or compatibility claim. Linked the lesson
from the learning index and method guide, with retained command/assembly and
primary Ghidra/ARM references. Empty retained warnings are not completeness proof.

## [2026-10-12] query | Decompilation-to-specification progress

The [phase ledger](research/native-phase-execution.md#decompilation-to-specification-status--2026-10-12)
now distinguishes retained code counts from semantic findings and reviewed
contracts. Native default exports remain 2,028/418,418 eligible entries; no native
handoff is released. The earlier MIDI work has 13 broader draft IDs/46 unexecuted
groups and one four-partial-clause/54-unexecuted-case release. No candidate or
reference compatibility result exists. The next milestone is a finite native
behavior contract, not a larger toolkit. Saved-import/cold-reopen and capacity
gaps remain explicit. Updated the program atlas with a link to the new register
study; facts remain canonical in its lesson rather than copied into a spec.

## [2026-10-12] lint | Reader repair and teaching updates

The pre-log mechanical pass covered 51 pages, 914
relative links and 48 retained MIDI source/disassembly pins with
zero errors; git diff --check passed. The [repair packet](../analysis/ableton-live-12.4.3/native-live-arm64-v1/preflight/read-revisions-fix-v1/README.md)
retains final reader/archive checks, browser case and independent scope review.
No binary behavior or compatibility pass is inferred from navigation/tool tests.
The final post-log lint is retained separately in that packet before sealing.

## [2026-10-17] maintenance | Record current location of the Ableton bundle

The [installed source page](research/sources/ableton-live-12.4.3.md) now records
that the reference bundle lives at `/home/ollie/Ableton Live 12 Suite.app` on the
Linux analyst workstation. The historical `/Applications` capture path is kept as
the observation it was. The copy's `Live` executable matches the recorded original
SHA-256 and its `Info.plist` version string is unchanged. The REA directory digest
was not recomputed, no retained evidence under `analysis/` was edited, and nothing
was executed. Lint: wiki-internal links on both edited pages resolve and
`git diff --check` is clean. Gap: the `analysis/` evidence directory is absent
from this workstation, so every evidence link on the source page and in earlier
log entries is unresolved here. This predates the change; the source page now
states it. Evidence hash checks against `analysis/` are `unknown` on this host.

## [2026-10-17] maintenance | Linux analysis workstation provisioned

Installed Ghidra 12.1.4, Temurin JDK 21.0.12.1+1 and REA 6.5.0 under the user
home without root, verified archive digests, and re-derived both arm64 slices
byte-identically from the local bundle. REA doctor accepts the Ghidra provider;
a Push2 `rea analyze` smoke test reproduced the macOS procedure and string
counts. Recorded in the [execution ledger](research/native-phase-execution.md#linux-workstation-provisioning--2026-10-17),
[source page](research/sources/ableton-live-12.4.3.md), [export guide](research/native-export-execution.md#coordinator-commands),
[recovery page](research/native-analysis-recovery.md#linux-workstation-paths--2026-10-17),
[Q-011](questions.md#q-011-main-live-export-capacity-and-recovery) and
[project status](project.md). Added `.gitignore` for `analysis/`. Gaps: the
macOS `analysis/` evidence tree is absent, persistent-project storage is
undecided, REA 6.5.0 source is uninspected, and no Live analysis ran.
Lint: relative links on all edited pages resolve except the pre-existing
`analysis/` references noted on 2026-10-17; `git diff --check` clean.

## [2026-10-17] maintenance | Roadmap revision 2 proposal

Appended a proposed, not adopted, [revision 2](research/native-decompilation-roadmap.md#revision-2-proposal--2026-10-17)
to the decompilation roadmap: restart gates (storage, evidence restoration,
persistent project), corpus export as one measured batch, outside-in
specification packets anchored on document vocabulary strings and shipped
documents, handoffs, and a macOS-only probe batch. Recorded the supporting
[string and document observations](research/ableton-package-structure.md#serialization-vocabulary-strings-and-shipped-documents--2026-10-17).
Updated the research index, [project status](project.md) and Q-011. Revision 1
remains authorized; frontmatter revision is unchanged. Lint: relative links and
anchors on edited pages resolve; `git diff --check` clean.

## [2026-10-17] maintenance | REA provider routing and analyzer dependencies

Query: does roadmap revision 2 invoke REA analyzers, and should it? Observed:
revision 2 named no REA operation. G0.3 and C1/C2 call `analyzeHeadless` and
repository scripts directly, and Phase 2 kept the dossier budget without a
route. Added a [provider routing](research/native-decompilation-roadmap.md#proposed-sequencing)
paragraph: bulk stays on direct Ghidra; Phase 2 dossiers use REA native
operations only if the coordinator's query-route check (planned
`wiki/research/r2-query-route.md`) shows REA can serve the saved project
affordably; non-native REA analyzers serve outside-in anchors. At user request,
installed Hopper 6.4.2 demo, Node 24.22.0 and rizin 0.9.1 without root under
`/var/tmp/sound-tools` and added `tools/rea-env.sh`. Recorded in the
[execution ledger](research/native-phase-execution.md#rea-analyzer-dependencies--2026-10-17).
GNU multiarch objdump lacks Mach-O and was removed. IDA needs a licensed
installer. No Live analysis ran; Hopper was not exercised on any target. Lint:
relative links and anchors on edited pages resolve; `git diff --check` clean.

## [2026-10-17] ingest | S2 document container static evidence

Recomputed from the local bundle (read-only) into `analysis/ableton-live-12.4.3/r2/s2-static-v1/`
and filed [document container static](research/document-container-static.md): container, gzip
header and XML envelope for 4,140 documents, all 203 schema headers, document-to-schema
cross-check (12 of 12 MinorVersions match a schema file), `.alp`/`AB1E` headers, and exact
`Live.arm64` loader string anchors with offsets for the native half. Corrected the
AppleDouble-doubled document counts on [package structure](research/ableton-package-structure.md)
and the roadmap; the coordinator re-counted and confirmed. Gaps: accepted version range,
error handling and save-time values remain unknown pending the saved Ghidra project;
`.alp` encoding unknown. Lint: links resolve; `git diff --check` clean.

## [2026-10-17] query | MIDI user-mapping closure assessment (S4)

Re-established the MIDI evidence from the local bundle into `analysis/ableton-live-12.4.3/r2/s4-midi-v1/`.
Both shipped documents and the Live slice match their recorded digests; the 17 bytecode
digests are unknown because their v1 manifests are absent here. Re-decoded 18 modules with
CPython 3.11.13 `dis` via `marshal.loads` only (no import or execution); every locator the
draft cites reproduced. The embedded interpreter is inferred to be 3.11.6. Classified every
clause in [the closure page](research/midi-closure-r2.md): the configuration-interpretation
layer of all 13 requirements is statically supportable; discovery, host errors, numeric
transforms, pad playback, feedback and timing need native tracing or Phase 4 probes.
Drafted 55 unexecuted v2 cases and 16 probe records. No spec or handoff page was edited.
Next: spec revision 2 and a midi-config-v2 candidate for separate review.

## [2026-10-17] ingest | S1 transport-state static evidence

Recomputed from the read-only bundle into `analysis/ableton-live-12.4.3/r2/s1-static-v1/`
(deterministic `run.sh`, outputs identical over two runs) and filed
[transport-state static](research/transport-state-static.md): Transport evolution over
203 schemas; tempo and time signature live on the main-track mixer, never under
Transport; values across 376 shipped sets and clips; 9 candidate statements; native
anchors and 10 follow-up queries. All four prior hashes matched. Corrected the
`LiveSet`/`Transport` string counts on [package structure](research/ableton-package-structure.md);
the coordinator re-checked by Mach-O section. Opened [Q-012](questions.md#q-012-transport-state-load-and-save-semantics).
Gaps: defaults, malformed and out-of-range handling, precedence and the 12.4.3
write format remain unknown. Lint: links and anchors resolve; `git diff --check` clean.

## [2026-10-17] maintenance | Learning pages updated for revision 2

Method guide: added the outside-in route (shipped artifacts, declared schema
structure, string anchors) with S1/S2 examples and three cautions (AppleDouble
counts, pooled strings, shipped is not loaded), marked the REA session paragraph
as revision 1, and added three glossary terms. [Learning index](research/learning/index.md):
a revision 2 section and a note that most lesson evidence links point into the
absent macOS tree. [MIDI lesson](research/learning/walkthroughs/midi-integer-parsing.md):
pointed to the S4 re-decode, which reproduces every quoted offset, plus S4's
`int()` spellings and PRB-S4-03. [Atlas](research/program-structure.md)
revision 8: document-to-schema correspondence and the 12.0_12402 tempo field
path. Two edges were checked directly against `12.0_12402.txt` lines 4116 and
4177. [Learning plan](research/learning/design-and-plan.md) row L6. No packet walkthrough was written:
each waits for its packet's native half. Not reader-reviewed. Lint: relative
links and anchors on edited pages resolve except 14 pre-existing links into the
absent macOS `analysis/` tree; `git diff --check` clean.

## [2026-10-17] query | Investigator query route (e-rea)

Inspected REA 6.5.0 installed source: it has no saved-project open path, every
session re-imports, and `--snapshot` replays exact queries only. Measured on Push2:
REA cold 80.9 s, exact replay 1.35 s, a different function 79.4 s; our MCP transport
handshake and function calls still work on 6.5.0. Added
`tools/ghidra/R2FunctionDossier.java` (read-only dossiers, reference and string
queries, deterministic manifests, spool server). A second read-only open is blocked
by the project lock; hard-linked copies cost about 0 bytes. Recommended one query
server on a hard-linked LiveR2 copy; filed as [query route](research/r2-query-route.md)
and recorded the decision in the roadmap's provider-routing paragraph, the export
guide and the provisioning table. Evidence: `analysis/ableton-live-12.4.3/r2/e-rea-v1/`.
Gaps: Live open time, RAM and project size; `str:` scan cost on Live.

## [2026-10-17] spec | MIDI user mapping revision 2 and midi-config-v2 candidate

Applied the S4 closure assessment to [spec revision 2](specs/midi-user-mapping.md),
re-checking each new clause against the S4 listings. Each requirement is split into
documented, static, static-conditional and unknown clauses with locators and probe
IDs. The check rejected draft case S4-MIDI-030: send knobs are compacted per strip,
so a lone Send2 knob reaches Send A; recorded as an unreviewed refinement and noted
on the [closure page](research/midi-closure-r2.md). Staged the
[midi-config-v2 candidate](specs/midi-config-v2-handoff-plan.md): 109 unexecuted
cases (54 restated from v1, 55 new), a draft manifest of 113 files, exclusions and
the supersession change list. Author checks passed: model cross-check, hashes,
isolated links, sanitization. Updated the feature-map and coverage rows and
Q-008 to Q-010 progress. Gaps: separate review pending; bytecode digest match to
the v1 pins unknown until G0.2; no reference or candidate run.

## [2026-10-17] ingest | Helper executables analyzed in parallel

Ran `tools/r2_helper_batch.sh` to use idle CPUs while the serial Live analysis
continues: 16 Ableton-authored helper executables analyzed in separate projects,
eight at a time, results in the [package structure](research/ableton-package-structure.md#helper-executables-analyzed--2026-10-17)
section and the helper manifest. The `Ableton Live Engine` bundle is x86_64-only
in substance (35 KB arm64 stub). Editing the batch script while its first run was
still executing caused a bash parse error after the last job; no job was lost, and
running scripts are no longer edited in place. Started a full analysis of Live's
x86_64 slice (SHA-256 `1bae9a97…be999b0`) as a second compile of the same source
for cross-checking arm64 readings; this is a revision 1 backlog item using spare
capacity, not a revision 2 gate. No behavior or compatibility claim.

## [2026-10-17] maintenance | R2 C1/C2 corpus tooling

Added `tools/ghidra/R2BulkDecompile.java`, `tools/ghidra/R2ExportIndexes.java`,
`tools/r2_corpus.py` with 10 tests, and a tools README section; filed
[corpus tooling](research/r2-corpus-tooling.md) with evidence in
`analysis/ableton-live-12.4.3/r2/c-tooling-v1/`. On Push2 (`5988ef09…`): 12,626
eligible functions, one 60 s timeout failure, output byte-identical across 11
thread, instance, JVM and kill-and-resume configurations; C2 deterministic. A single
program instance serializes on the program lock (35% of 16-thread samples); separate
instances in one JVM remove it. Chunked JSONL chosen (0.62 GB projected versus 9.4 GB
per-function layout); the roadmap's C1 ingest line was revised. The coordinator
re-ran the tests and compiled all R2 scripts against Ghidra 12.1.4. The agent's
report of a renamed roadmap heading was checked and is wrong; the anchor resolves.
Gaps: not yet run on Live; scaling measured under load 12 to 36; hard-linked project
copies share `project.prp` and `user/~index.dat`, so query copies must privatize them.

## [2026-10-17] release | midi-config-v2

A separate review subagent reviewed the staged midi-config-v2 (109 cases) and
approved it with listed narrowing: RV2-01 excludes pad integer text over 640
characters; RV2-02 excludes tabs and other ASCII control characters. Editorial
fixes RV2-03 to RV2-05 were applied in the payload. Evidence identity: the decoded
modules and both documents are bound to the pinned Live executable `52289af6…`
through its code signature and `CodeResources` hashes; the v1 pin comparison
remains unknown and does not block, so G0.2 is not required. Checks: all 55 new
cases read by hand; reviewer and author models each agree 109 of 109; isolated
copy verified. The coordinator copied the payload into
[handoff/midi-config-v2](../handoff/midi-config-v2/README.md), re-verified all 114
payload hashes and the manifest SHA-256 `889b52fa…12eb4d7`, added the catalog row,
and reconciled [spec revision 2](specs/midi-user-mapping.md) with RV2-01 to RV2-03.
Review evidence: `analysis/ableton-live-12.4.3/handoff-staging/midi-config-v2-analysis/review/`.
Open: no reference or candidate execution; RV2-07 coverage notes; isolated
implementation workspace not provisioned.

## [2026-10-17] maintenance | Revision 2 corpus browsers (C3) and doc refresh

Added [`tools/r2_browser.py`](../tools/r2_browser.py) and seven unit tests. It
builds one offline browser per verified C1 corpus plus C2 indexes and refuses
unverified or mismatched inputs. Function code and relations load per chunk.
Generated 16 browsers under the ignored `analysis/ableton-live-12.4.3/browse/r2/`
(Push2 tooling corpus plus 15 helper corpora, 395,764 functions, 1.2 GB), with
an `r2-index.html` catalog. Observed: snap Chromium cannot open `file:///var/tmp`
pages, so output stays under `/home`. Headless Chromium navigation check on Push2
(callee link and caller back-link) passed. Recorded in the
[browser design amendment](research/artifacts/browser-design-and-plan.md#revision-2-corpus-browser-amendment--2026-10-17),
[artifact catalog](research/artifacts/index.md) and `tools/README.md`. Learning
pages: the method guide now cites the [query route](research/r2-query-route.md)
decision (Ghidra dossier server, not REA); the learning index links midi-config-v2
and the browsers. The C1–C3 gate row is left to the coordinator. The Live
browser waits on the Live corpus. Lint: links and anchors on edited pages
resolve; `git diff --check` clean; `test_r2_*.py` 17 tests pass.

## [2026-10-17] ingest | x86_64-only bundles (H3)

Identified the [x86_64-only bundles](research/x86-only-bundles.md) from their
helper corpora and Mach-O headers, without executing anything: the Live Engine
bundle is a ReWire device build of the audio engine; ReWire.bundle is
Propellerhead ReWire 1.8.7; MultiF0 is an audio-to-note library. arm64 Live has
no ReWire install or loader strings, and it carries MultiF0 built in. The engine's
x86_64 slice names 297 `OEngine` methods that Live leaves unnamed, a candidate
symbol donor for S3. Updated the package-structure helper section and feature map;
opened [Q-013](questions.md#q-013-x86_64-only-rewire-and-multif0-paths).
Evidence: `analysis/ableton-live-12.4.3/r2/h3-x86-bundles-v1/`. No behavior claim.

## [2026-10-17] query | Browser index helper (H2)

Filed [browser index (static)](research/browser-index-static.md) from the index
helper's corpus and project (slice `3390bd4b…`) and the shipped metadata: launch
modes and option keys, the `ipc://` channel with 25 Live-to-helper commands and 12
helper events, the SQLite files-database schema with FTS4 search, version 12300 with
upgrade and rebuild rules, an 80-entry file-type table, file-event-driven updates,
162 XMP tag sidecars and 2,563 previews, and the read-only `filerefmap.db` with 37,617
sample-path mappings. Updated the feature map and the package-structure database row;
opened [Q-014](questions.md#q-014-browser-index-behavior). Evidence:
`analysis/ableton-live-12.4.3/r2/h2-index-v1/`. The agent also confirmed that
`decomp.time` is created at job start and is not a completion signal; the coordinator
had already corrected that rule. Gaps: Live-side spawn and queries; runtime probes.

## [2026-10-17] query | Push 3 helper interfaces (H5)

Filed [Push 3 helper (static)](research/push3-helper-static.md) with evidence in
`analysis/ableton-live-12.4.3/r2/h5-push3-v1/` (12 self-checks pass). The helper
(arm64 `8a2b77c9…`) is the Push application: embedded Python 3.11 running its own
`Push2` script, Skia display, libusb with vendor `0x2982` and Push 3 product
`0x1969`, CoreMIDI, and three nanomsg channels plus a document-sync model and
shared memory linking it to Live. Added a Q-005 evidence line. Static only; socket
roles, message bytes and pixel format remain open; probes P5-01 to P5-09 need a
Push 3 on the macOS host.

## [2026-10-17] ingest | Web connector, add-ons, swapper (H6)

Filed [web, add-ons, swapper (static)](research/web-addons-swapper-static.md) from
three verified helper corpora and 45 shipped Python modules decoded statically;
evidence in `analysis/ableton-live-12.4.3/r2/h6-web-v1/` (64 outputs, deterministic).
The web connector is an embedded Python auto-updater and usage uploader talking to
Live over nanomsg; updates are `.asu` ZIPs whose `.alp` files are patched with
xdelta3; the swapper renames the app with rollback after Live exits; add-ons serves
the Extensions and Splice backends, not Packs. No service was contacted and no
credential value is recorded. Updated the feature map and opened
[Q-015](questions.md#q-015-helper-launch-and-update-handling-in-live).

## [2026-10-17] maintenance | G0.3 passed; next stage started

The persistent Live project passed G0.3: full analysis 1:14:30, saved project
2.03 GB, cold read-only reopen 2:54, 418,417 non-external functions; recorded in the
[gate table](research/native-phase-execution.md#gate-ledger) with evidence in
`analysis/ableton-live-12.4.3/r2/g03-v1/`. A hard-linked query copy with private
non-database files now serves dossiers to three native investigators (N1 transport
state, N2 document container, N3 transport transitions), and the bulk decompile is
running on the main project. The coordinator's automatic launcher failed because its
`pgrep -f` pattern matched its own command line; the stage was launched by hand.

## [2026-10-17] query | Plug-in scanner (H1)

Filed [plug-in scanner (static)](research/plugin-scanner-static.md) from the scanner's
corpus (slice `6ce847b0…`; 36,873 of 36,879 functions decompiled) with evidence in
`analysis/ableton-live-12.4.3/r2/h1-plugin-scanner-v1/`. Recovered the option set,
`ID=PATH` scan-root syntax, VST3-then-VST2 enumeration rules, a size-and-mtime
fingerprint, a five-state scan database, the per-session limit and three message
topics to Live. No Audio Unit or CLAP scanning code is in the scanner. The crash
handling and limit behavior are derivations that need probes before release. Updated
the FEAT-HOSTING row; opened [Q-016](questions.md#q-016-plug-in-discovery-live-side-contract).
Nothing executed.

## [2026-10-17] maintenance | Interactive Corpus resonator demo

Added the [Corpus resonator demo](research/learning/demos/corpus-resonator.md),
built by `tools/corpus_demo.py` and `tools/corpus_demo.html` into the ignored
`analysis/ableton-live-12.4.3/demos/corpus/`. Controls, ranges and the 26 presets
come from the Corpus class of `Schema/12.0_12402.txt` and the shipped `.adv`
presets. The sound is a labelled textbook modal-resonator stand-in, not decompiled
code. Resonance type labels are assumed; two preset titles agree with the order.
Checks: 3 unit tests pass. A headless Chromium offline self-test found the String
peak at 220.0 Hz and a membrane ratio of 1.59334, and the normal page rendered
26 presets and 38 controls. Live audio in a desktop browser was not checked.
Linked from the [learning index](research/learning/index.md) and learning plan
row L7. Gap: tracing `SetParameterA`/`CalcA` for a faithful version.
Lint: links and anchors resolve; `git diff --check` clean.

## [2026-10-17] maintenance | Track analysis evidence and browsers in Git

By user direction, the `analysis/` tree is now tracked in Git: evidence directories,
scripts, staged handoff payloads, the helper and Push2 corpus browsers, and the
Corpus demo output. Excluded by `.gitignore`: extracted binaries (`derived/`,
`*.arm64`, `*.x86_64`), the raw Push2 corpus and index dumps, and the `r2-large`
link to `/var/tmp/sound-analysis` (Ghidra projects and corpora). A credential
pattern scan found nothing. Statements that `analysis/` is ignored were corrected
on the artifact catalog, tools README, installed-source page and Q-002. Evidence
directories of agents still running (H4, N1 to N4) were committed as snapshots and
will change. The `origin` remote is public; nothing was pushed.

## [2026-10-17] decision | Clean-room separation waived for the Corpus demo

User direction: "ignore the rule for now". The [AGENTS.md](../AGENTS.md) separation
between analyst contexts and implementation is waived for the Corpus device DSP
demo being built in this checkout from decompiled Corpus code. That demo is
therefore decompilation-derived and is not a clean input to the independent
application. The waiver is temporary and covers only this work; the rule is
otherwise unchanged. Nothing has been pushed to the public `origin` remote.

## [2026-10-17] maintenance | Live corpus complete (C1, C2)

The bulk decompile of `Live.arm64` finished in 13:13 with 14 program instances in
one JVM: all 418,417 eligible functions have an outcome (320,967 exported, 97,387
with warnings, 63 failed), and the C2 indexes verify. The short A/B samples had
favored one instance, but the full run sustained about 848 functions per second.
Recorded in the [gate table](research/native-phase-execution.md#gate-ledger) and
[corpus tooling](research/r2-corpus-tooling.md#measured-on-live--2026-10-17), with
evidence in `analysis/ableton-live-12.4.3/r2/c1-live-v1/`. The corpus and indexes
stay on `/var/tmp/sound-analysis/corpus` and are not in Git. The four native
investigators were told the indexes are ready.

## [2026-10-17] query | Native device bundles (H4)

Filed [device bundles (static)](research/device-bundles-static.md) from the bundle
plists and Mach-O headers, the seven helper corpora and 3,634 shipped documents,
without executing anything. All seven bundles export one 7-function C interface
with three implementations (Softube Amp and Cabinet, which check for the Live bundle
ID; four Tassman-based instruments; Corpus). Live holds every parameter name and
stored domain; bundles receive only an index and a float. 502-parameter inventory
over 1,064 shipped occurrences; Corpus `ResonanceType` 5 and 6 confirmed from two
presets, the full label order still inferred. Updated FEAT-DEVICES, Q-005 and Q-006,
and linked the page from the [Corpus demo](research/learning/demos/corpus-resonator.md).
Evidence: `analysis/ableton-live-12.4.3/r2/h4-devices-v1/`. Gaps: Live-side index
mapping and value conversion; labels; defaults for Amp, Cabinet and Corpus.

## [2026-10-17] maintenance | Requirements browser and spec index catalog

The user could not find the requirements derived from the static and decompilation
work: they existed only as candidate tables in five research pages. Added
`tools/spec_browser.py` (2 unit tests), which generates the
[requirements browser](../analysis/ableton-live-12.4.3/browse/specs/index.html):
66 rows, made up of 13 draft REQs from SPEC-MIDI-USER-MAPPING and 53 candidates (C-, T-, PD-, BI-C,
DEV-C), each linked to its source section. Added a one-row-per-target
"Candidate specifications" table and the browser link to the
[spec index](specs/index.md). README now routes to the learning
route, requirements browser and corpus browsers, and corrects three stale claims:
the current release is midi-config-v2, there is a public `origin`, and `analysis/`
tracks decompiled code. Lint: links and anchors on edited pages resolve, the 67
generated-page links resolve, and `git diff --check` is clean.

## [2026-10-17] query | Transport transitions, native (S3, N3)

Filed [transport transitions](research/transport-transitions-native.md) and the
[dispatch lesson](research/learning/walkthroughs/transport-dispatch.md). The indirect
call at `0x101a4ac58` is `OSendThreadMessage::Finish` (`0x101ab7898`; RTTI-named vtable
`0x106756188`), queuing `OSetPlayingCommand` to handler `0x101a524b8`. Start and Stop
post requests; the interface mirrors engine reports through
`TransportEngineStateChanged`. Static transition table T-01 to T-13; 31 engine-donor
symbol matches (26 high confidence). Updated the atlas edge, transport study,
learning index and FEAT-TRANSPORT in the same change. Evidence:
`analysis/ableton-live-12.4.3/r2/n3-transitions-v1/`. Gaps: position after Stop,
report timing, control-to-entry routing, undo; runtime escalation record filed.
Each `str:` dossier query took about 4 to 6 minutes on Live; the strings index is
the faster route.

## [2026-10-17] spec | Transport-state native half (N1); SPEC-TRANSPORT-STATE r1

Filed [transport-state native](research/transport-state-native.md), the draft
[SPEC-TRANSPORT-STATE](specs/transport-state.md) revision 1 (12 requirements, 23
unexecuted cases) and the [reader walkthrough](research/learning/walkthroughs/transport-state-reader.md).
Four query rounds (34 dossiers) plus corpus reads. Derived: Boolean token
acceptance, constructor defaults, duplicate and unknown-element handling, the save
number format (reproduces all 149,716 shipped float values) and the time-signature
code; static candidate T-09 is superseded. Updated the spec index (candidate row
replaced), feature map, coverage, Q-012, atlas and learning index; the spec
browser is regenerated after the container draft lands. Evidence: `analysis/ableton-live-12.4.3/r2/n1-transport-state-v1/`.
Gaps: precedence, post-load clamping, time-signature default, error presentation;
PRB-N1-01 to 08.

## [2026-10-17] spec | Document container native half (N2) and SPEC-ALS-CONTAINER r1

A fresh writer produced [document container native](research/document-container-native.md),
the draft [SPEC-ALS-CONTAINER](specs/als-container.md) revision 1 (9 requirements, 27
unexecuted cases, 7 probes) and the [version-check walkthrough](research/learning/walkthroughs/document-version-check.md)
from the N2 evidence after the investigator was interrupted. Nothing was executed.
12.4.3 reads `Schema/<MinorVersion>.txt` on the version-check path; MajorVersion 4 and 5
are accepted, 6 and above gives the newer-version error, other values the
corrupt-document error; `Revision` is never read. The writer's check against the
disassembly relabelled case N2-014 unknown and N2-015's message inferred; notes
claims missing from the kept evidence are listed on the page. Updated the spec index
(candidate row replaced), feature map, coverage, Q-006, Q-012, atlas and learning
index, and regenerated the spec browser. Gaps: Live Set save call site and
compression level, which reading path File > Open uses, dialog texts.

## [2026-10-17] spec | Corpus signal chain traced from the decompiled bundle

Traced Corpus.bundle (arm64, `29df4582…`) from Live's parameter call down to each
output sample, under the user's waiver of the analyst/implementation separation
for this work (recorded earlier in this log). Two read-only subagents traced the
resonator and the rest of the chain; their reports are retained in
`analysis/ableton-live-12.4.3/r2/corpus-dsp-v1/`. New page:
[Corpus DSP (decompiled)](research/corpus-dsp-static.md), covering 37 host
parameters with conversions, the module graph, five modal and two waveguide
resonator models, quirks, and candidates CD-C01–CD-C08 (listed in the
[spec index](specs/index.md) and the requirements browser, rerun at 95 rows).
It confirms the ResonanceType order the demo had assumed. A JavaScript port with
an interactive page lives outside the repository in
`~/Documents/sound-local/corpus-faithful/` and is not committed, because the
remote is public. Its checks: 8 Node tests pass, a headless Chromium AudioWorklet
self-test puts String at 261.5 Hz, and it uses at most 9% of one core. The
[Corpus demo](research/learning/demos/corpus-resonator.md) gained a
stand-in-versus-traced comparison. Gaps: Live-side value conversion (N5),
inferred Live names for three host indices, and no runtime comparison.
Lint: links and anchors on edited pages resolve; `git diff --check` clean.

## [2026-10-17] maintenance | Traced Corpus demo published in the repository

By the user's direction, the built traced-engine page now lives at
`analysis/ableton-live-12.4.3/demos/corpus-traced/index.html` and is committed
and pushed to the public origin. It embeds the JavaScript port of Corpus's
decompiled signal chain. This reverses the earlier choice to keep the port out of
the repository. The page banner, [Corpus DSP page](research/corpus-dsp-static.md),
[Corpus demo](research/learning/demos/corpus-resonator.md) and
[learning index](research/learning/index.md) now say so. The page is labelled as
derived from recovered code, never to seed the reimplementation. Its sources
(engine, tests, build script) stay in `~/Documents/sound-local/corpus-faithful/`.
Checks before commit: 8 Node tests pass; the repository copy passes its headless
Chromium self-test (String peak at 261.5 Hz through an AudioWorklet).

## [2026-10-17] query | Device bundles: Live-side mapping (N5)

Traced bundle loading, `GetPlugInfoU` use and the parameter path in Live 12.4.3 and
filed [device parameter mapping](research/device-parameter-mapping-native.md) with
evidence in `analysis/ableton-live-12.4.3/r2/n5-device-mapping-v1/`. Complete index and
value-conversion tables for Amp, Cabinet, Electric and Corpus (82 rows): every stored
range equals Live's constructor range, and the Corpus bundle's setter override confirms
the index map. Corrections: the [device bundles](research/device-bundles-static.md)
"XML-only ranges" statement is qualified, and Corpus index 37 is sent but ignored, not
never sent. Open contradiction: the three Corpus position parameters arrive as 0..1 on
Live's traced side, while the bundle's mapping fits -1..1 (probe P4-N5-01). Gaps:
Analog, Tension and Collision tables; the document reader; `Defaults` presets.

## [2026-10-17] maintenance | Corpus port and page updated with N5's Live-side mapping

Applied the [device parameter mapping](research/device-parameter-mapping-native.md)
(N5, 7b611bd) to the Corpus work.
- **Conversions confirmed:** Live passes stored values unchanged, and
  FilterMidFreq's log10 Hz to 0–1 conversion matches the earlier assumption. The
  host names for indices 0–36 are confirmed.
- **Corrections:** MidiMode is sent as index 37 and ignored, not "never sent".
  The three position controls now follow Live's traced pass-through of 0–1.
  Their range stays open (probe P4-N5-01): the device's 64+31.5v fits a −1–1
  input.
- **Pages updated:** the [Corpus DSP page](research/corpus-dsp-static.md),
  including CD-C02 and CD-C08, the research index row, and the
  [learning index](research/learning/index.md). The rebuilt
  traced-engine page (`analysis/ableton-live-12.4.3/demos/corpus-traced/index.html`)
  now shows 37 controls traced, 3 unresolved and 1 ignored.
- **Checks:** 8 Node tests pass; the repository copy's headless self-test passes.

## [2026-10-17] query | Live-side helper contracts (N4)

Traced Live arm64's launch and supervision of six helpers from the C2 indexes and 46
dossiers and filed [helper launch, Live side](research/helper-launch-live-side.md) with
evidence in `analysis/ableton-live-12.4.3/r2/n4-helper-contracts-v1/`. One process
controller supervises the index, scanner, add-ons and Push 3 (20 s launch timeout,
60 s unsynced kill); Live binds every channel except `live-to-push-midi`; named events
use a type-byte, length-prefixed frame. Per-helper arguments, start conditions and
restart caps are recorded; Live exits with code 42 if the swapper is running at start.
Added progress to Q-013 through Q-016 and Live-side cross-links on the five helper
pages; the Push 3 page's emulator-flag guess is superseded. Gaps: Audio Unit handler,
debug-option names (stored as digests), index database naming, ReWire (x86_64 pending).

## [2026-10-17] maintenance | Traced Corpus demo: key status, default preset, output limiter

The on-screen MIDI keys only act through MidiPitch or MidiGate. Only one of the
26 presets (Pipe Resonator, the previous default) turns on MidiGate, and none
turns on MidiPitch. With MidiGate on and no note held, a click's ring fell to
−60 dB in 56 ms instead of 1.2 s.

The page now shows below the keys whether they do anything with the current
settings. It opens on Metallic Rezo (Membrane, MidiGate off, 0.43 s ring), and a
safety limiter on the page output protects against presets that peak far above
full scale (Loop Move about 22×). The limiter is labelled as page-only, not part
of Corpus.

Whether Live itself gates Corpus when no MIDI is routed to it is not established.
Checks: 8 Node tests pass; the headless self-test passes; the default loads as
type 3.

## [2026-10-17] query | Phase 4 probe batch prepared

Merged every probe and escalation record into `analysis/ableton-live-12.4.3/r2/phase4-batch-v1/`
(batch, fixture plan, manifest, builder) and the run sheet
[Phase 4 probe batch](research/phase4-probe-batch.md): 79 records (75 original IDs, 4
assigned), 7 merge groups, 3 incomplete, about 24 h of sessions; the handoff blockers
take about 7 h. Found that the requirement IDs in N1's probe file predate spec r1; the
batch follows the spec. Gaps: no probe covers TS-010 or P1-F; an N2-019 variant without
`Creator` is missing; the LOM, debugger, USB-capture and MIDI-sender tools are
unverified. Nothing was run. The run sheet lists decisions for the user (sitting length,
isolation, debugging, hardware, test plug-ins, network, evidence transfer).

## [2026-10-17] decision | Phase 2 scope extended

By user direction, eight more agents started: draft SPEC-PLUGIN-DISCOVERY and
SPEC-BROWSER-INDEX; the remaining device tables with SPEC-BUNDLED-DEVICE-PARAMETERS;
MIDI numeric transforms (Q-009); and new outside-in packets S6 automation, S7 MIDI
notes, S8 warp, S9 mixer values. Recorded in the
[roadmap](research/native-decompilation-roadmap.md#scope-extension--2026-10-17) and
gate table. A second hard-linked query copy and server were started for S6 to S9.

## [2026-10-17] spec | transport-state-v1 handoff candidate staged

Staged a finite candidate from SPEC-TRANSPORT-STATE r1 under
`analysis/ableton-live-12.4.3/handoff-staging/transport-state-v1/` (18 cases, authored
XML fixtures, draft manifest `45c60b41…ac4202`); plan and traceability in
[transport-state handoff plan](specs/transport-state-handoff-plan.md). Partial
REQ-001, 002, 004 to 008, 010 and 011 and full REQ-003; REQ-009 and REQ-012 unreleased;
TS-010, TS-017 to 019 and TS-023 withheld. Found: REQ-006 and TS-010 contradict the
container reading of the integer parser (trailing space kept); TS-023 conflicts with
the draft's own exclusion of edits; TS-008 and TS-020 narrowed to `Manual`. Checks:
cross-check model 18 of 18, hashes and links in an exported copy, deny lists clean.
Not reviewed, not released, nothing executed.

## [2026-10-17] spec | als-container-v1 handoff candidate staged

Staged an unreviewed candidate from SPEC-ALS-CONTAINER r1 at
`analysis/ableton-live-12.4.3/handoff-staging/als-container-v1/` (35 cases, 35 authored
fixtures, draft manifest `62da834b…`) and filed the [plan](specs/als-container-handoff-plan.md).
Scope: partial REQ-001 to 006; 007 to 009 unreleased. Outcomes are envelope-accepted or
refused with a class; all 23 static-derived r1 cases kept (some narrowed), 4 unknown
cases excluded, 12 new cases for clauses without one. Refusal classes for root-attribute
errors rest on an inferred catch step (I1). Findings F1 to F5 propose r2 corrections,
including an overbroad precedence clause. Hashes and links verified in an export copy.

## [2026-10-17] spec | SPEC-TRANSPORT-STATE revision 2

Applied the transport-state-v1 handoff author's corrections to
[SPEC-TRANSPORT-STATE](specs/transport-state.md). REQ-006 narrowed: spellings with spaces
on both sides, `+` with trailing spaces, and the `-` sign are unknown. TS-010 is
unresolved; TS-023 is withdrawn as out of scope. REQ-011 says positive zero; negative
zero is unknown. TS-008 and TS-020 judge the automation event text only if it is
written. The appendix maps the N1 probe file's older requirement IDs. Corrected the
integer row on [transport-state native](research/transport-state-native.md). Gaps: no
N1 probe covers TS-010 or a missing `TimeSignature/Manual`. Nothing executed.

## [2026-10-17] maintenance | Live x86_64 cross-check corpus complete

Live's x86_64 slice finished analysis (1:39:43, 414,791 functions) and bulk decompile
(17:17; 317,021 exported, 97,725 with warnings, 45 failed; indexes verified), recorded in
[corpus tooling](research/r2-corpus-tooling.md#live-x86_64-cross-check-corpus--2026-10-17)
with evidence in `analysis/ableton-live-12.4.3/r2/c1-live-x86-v1/`. It is a cross-check
build; specifications stay derived from arm64. Investigator N8 now uses it for the
ReWire and MultiF0 questions in Q-013 and to cross-check the arm64 transport readings.

## [2026-10-17] spec | SPEC-PLUGIN-DISCOVERY r1 (D1)

Drafted [SPEC-PLUGIN-DISCOVERY](specs/plugin-discovery.md) revision 1 from the H1
scanner and N4 Live-side evidence: 16 requirements, 42 unexecuted cases (6 unresolved).
Nothing was executed. Every static clause was rechecked against retained pseudocode.
New: the VST2 system folders, case-insensitive `.vst` matching, deletion of a changed
module's old plug-ins on re-examination, and host answers defaulting to 0. The crash-state
update runs once per format pass, which corrects the scanner page's crash timing
(outcome unchanged); correction notes added there and on the helper-launch page. PD-10
and PD-12 stay unknown pending PRB-H1-02 and PRB-H1-04. Updated the spec index (candidate
row replaced), feature map, coverage and Q-016, and regenerated the spec browser.

## [2026-10-17] ingest | S5 clip launch settings and quantization

Filed [clip launch](research/clip-launch.md) with evidence in
`analysis/ableton-live-12.4.3/r2/s5-clip-launch-v1/` (four rounds of 8 dossiers).
Enumerations, defaults (global quantization 1 Bar; a new clip's launch values from
preferences), follow-chance normalization, six translators, the quantization grid
function and the launch-boundary rule, read in disassembly with two corpus misreadings
corrected. Candidates CL-01 to CL-23 and probes PRB-S5-01 to 11. Updated the feature map,
coverage, spec index (candidate row), gate table and the Phase 4 page; opened
[Q-017](questions.md#q-017-clip-launch-timing-and-launch-modes). Gaps: boundary offset,
stopped launch, launch modes, legato, velocity law, follow-action timing. Nothing executed.

## [2026-10-17] spec | SPEC-ALS-CONTAINER revision 2

Applied the als-container-v1 handoff author's findings F1 to F5 to
[SPEC-ALS-CONTAINER](specs/als-container.md). REQ-004: the first refusal wins, and earlier
refusals (illegal integer at the root, wrong root, absent or zero MajorVersion, no
document) are corrupt-document even with newer versions. REQ-003 and 006: integer
refusals happen when the root is read. REQ-005: a file-existence lookup; letters-only
values are refused, other non-schema values unknown. REQ-001: start refusals have an
unspecified class. Uncompressed fixtures depend on PRB-N2-02. Assumptions I1 to I6 are
labelled per clause. Gap: `MajorVersion="6"` with an empty or absent MinorVersion is
unknown; the candidate's 12 new cases are not yet added to the draft. Nothing executed.

## [2026-10-17] spec | SPEC-BROWSER-INDEX revision 1 (D2)

Drafted [SPEC-BROWSER-INDEX](specs/browser-index.md) r1 from packet H2, the N4 index
section and a bounded re-read of the helper corpus (no query-server rounds): 13
requirements, 52 unexecuted cases (24 static-derived, 28 unknown). New static results:
sidecar file names are UUIDv5 under the nil namespace, the fixed user-folder sidecar name,
factory and built-in edits written to the User Library, the type-to-kind map, `colors` and
`assetId` item fields, and the preview lookup order. The coordinator retained the cited
helper-corpus records (43 functions) in `analysis/ableton-live-12.4.3/r2/d2-browser-index-v1/`
and added an update note to [browser index](research/browser-index-static.md). Deferred
BI-C04, C10 and C12; dropped the use count. PRB-BI-01 to 05 proposed but not yet in the
Phase 4 batch. Not reviewed; nothing executed.

## [2026-10-17] release | transport-state-v1

A separate review subagent approved transport-state-v1 with narrowing (RV1-01: the REQ-006
length refusal applies only to text not ending in a space, because the parser's length check
excludes trailing spaces). It also clarified the TS-009 embedding event and the full-set root
attributes, aligned the manifest exclusions, and confirmed the author's residual inferences by
reading the uncited vtables, the default-tempo store, the digit converter, the report sink and
the save formatter. The coordinator copied the payload into
[handoff/transport-state-v1](../handoff/transport-state-v1/README.md), re-verified all 23 payload
hashes against manifest `b2fdf029…5baba`, added the catalog row, and carried RV1-01 and the
strengthened TS-010 reading into [SPEC-TRANSPORT-STATE](specs/transport-state.md) r2. 18 cases,
static-derived and unexecuted; no compatibility claim. Isolated implementation workspace still
unprovisioned. Not pushed.

## [2026-10-17] query | MIDI note storage in clips (S7)

Surveyed note storage in 203 schemas and 1,368 shipped clips (235,756 notes) and traced the
12.4.3 reader and writer in four rounds of 8 dossiers; filed
[MIDI note storage](research/midi-note-storage.md) with evidence in
`analysis/ableton-live-12.4.3/r2/s7-midi-notes-v1/`. Notes sit in one KeyTrack per key;
12.4d1 omits VelocityDeviation 0, Probability 1 and IsEnabled true. The reader reuses one
note object per KeyTrack, so an absent Time, Duration, Velocity, OffVelocity or NoteId repeats
the previous note's value; it rounds times to 1/3,843,840 beat, clamps velocities and
probability, fails on repeated non-zero NoteIds, numbers NoteId-0 notes from NextId, and cleans
or rejects per-note expression lists and probability groups. Candidates MN-01 to MN-24 and
PRB-S7-01 to 10. Opened [Q-018](questions.md#q-018-midi-note-key-range-and-ordering-after-load)
for the unchecked key-table store and ordering after load. Nothing executed.

## [2026-10-17] query | MIDI map-mode transforms, native (N7)

Filed [MIDI map-mode transforms](research/midi-transforms-native.md) with evidence in
`analysis/ableton-live-12.4.3/r2/n7-midi-transforms-v1/` (27 dossiers, n7-0001 to n7-0004).
Static only; every material branch was checked in disassembly. Traced the native path from
the user script's mapping call to the parameter value for all ten map modes: absolute scaling,
14-bit pairing in either order, relative step size (max − min) × d/256, one-step moves for
quantized parameters, round-half-away-from-zero (the decompiler's truncating cast was wrong),
the two acceleration tables with three confirmed oddities, on/off thresholds, and the takeover
arithmetic for None, Pick-Up and Value Scaling. Proposed SPEC-MIDI-USER-MAPPING revision 3
clauses with cases MT-01 to MT-23; PRB-N7-01 to 05 refine PRB-S4-05. Gaps: takeover preference
default, prior-table reset trigger, registry gate, the parameter setter, delivery timing.

## [2026-10-17] query | Mixer value conversions (S9)

Filed [mixer values](research/mixer-values.md) with evidence in
`analysis/ableton-live-12.4.3/r2/s9-mixer-v1/` (29 dossiers in four rounds, 90 corpus records).
Static: mixer fields and history over 203 schemas and a per-track-type census of 1,340 mixers
in 376 shipped sets; volume and sends are stored as linear gain. Native: constructor defaults
and ranges, seven 101-point fader curves (0 dB at position 0.85), dB and pan text rules, the
engine silence floor (gain ≤ 0.00032 becomes 0), the pan law and crossfade assign. Candidates
MX-01 to MX-15 and probes PRB-S9-01 to 08. Opened
[Q-019](questions.md#q-019-mixer-volume-and-send-values-sent-to-the-engine) for the
logic-to-engine port values. No audio claim is measured. Nothing was run.

## [2026-10-17] release | als-container-v1

A separate review subagent approved als-container-v1 (SPEC-ALS-CONTAINER r1, partial REQ-001 to
006, 35 static-derived unexecuted cases) with narrowing: RVA-02 excludes gzip content that is
itself gzip, and RVA-03 excludes plain-XML differences outside `LiveSet` that no rule names.
The reviewer established I1 statically (handler-level catch, stored message, error flag,
post-parse classification), so refusal classes stay graded, and confirmed I3; I2, I4, I5 and
I6 are now named in the contract. All 12 new cases accepted; excluding entry-dependent outcomes
was accepted in place of PRB-N2-03 and 05 for this static release only. The coordinator copied
the payload into [handoff/als-container-v1](../handoff/als-container-v1/README.md), re-verified
all 40 payload hashes against manifest `f5ca758d…62d1de`, added the catalog row, and recorded
the I1 and I3 outcome in [SPEC-ALS-CONTAINER](specs/als-container.md) r2. No compatibility
claim; isolated implementation workspace still unprovisioned. Not pushed.

## [2026-10-17] query | Automation envelopes (S6)

Filed [automation envelopes](research/automation-envelopes.md) with evidence in
`analysis/ableton-live-12.4.3/r2/s6-automation-v1/` (24 dossiers in three rounds, 72 corpus
records). In 4,365 shipped envelopes every target resolves, events are time-ordered (at most two
per time) and start at −63,072,000 with the next event's value. Natively: a post-load walk
rejects empty envelopes and a first event at neither −63,072,000 nor 0; non-monotone curves reset
to linear; 0.5 curve controls are not written; a dangling `PointeeId` aborts on access; float
evaluation is hold, constant, cubic Bezier or linear (float32), and Bool and Enum envelopes step.
Also found the generic create-and-load entry point, which narrows the transport-state page's
"top-level load not traced" gap. Candidates AE-C01 to C17 and PRB-S6-01 to 07. Opened
[Q-020](questions.md#q-020-automation-envelope-load-robustness). Nothing executed.

## [2026-10-17] query | Warp markers and settings (S8)

Read 203 schemas and 4,005 shipped documents and traced Live arm64's warp-marker reader, helpers
and enumerations (23 dossiers); filed [warp markers](research/warp-markers.md) with evidence in
`analysis/ableton-live-12.4.3/r2/s8-warp-v1/`. Markers are SecTime and BeatTime attributes. The
last marker is a shadow marker 1/32 beat after the last real marker, carrying the tempo after it.
An empty AudioClip list is a load error. Edits keep segment tempo within 5 to 999 BPM and snap
beats to the 1/3,843,840-beat grid. The seven warp-mode codes and labels, the transient
enumerations and the setting ranges and defaults are recorded; the piecewise-linear mapping is
inferred. Candidates WM-01 to WM-16; probes PRB-S8-01 to 11. Gaps: the conversion routine, load
handling of malformed lists and values, the Transient Envelope range, and the stretching
algorithms. Nothing executed.

## [2026-10-17] spec | SPEC-CLIP-LAUNCH r1 (D3)

Drafted [SPEC-CLIP-LAUNCH](specs/clip-launch.md) revision 1 from the S5 evidence: 23 requirements,
56 unexecuted cases (4 not graded, 2 without a fixture). No query was issued; every static clause
was rechecked against the retained s5 dossiers, and the grid jump table, migration table and
lattice sentinels were re-read from the image. Clauses that rest on uninterpreted steps name
assumptions A1 to A6. Correction added to [clip launch](research/clip-launch.md): the default set
falls under scene migration step 12203. REQ-017's near-boundary clause stays unknown until
PRB-S5-01. Updated the spec index (candidate row replaced), feature map, coverage and Q-017.

## [2026-10-17] query | x86_64 ReWire, MultiF0 and transport cross-check (N8)

Filed [Live x86_64 paths](research/x86-live-paths.md) with evidence in
`analysis/ableton-live-12.4.3/r2/n8-x86-paths-v1/` (dossiers n8-0001 and n8-0002 on the x86_64
project). The ReWire install and host open are unreachable in 12.4.3 (constant-false predicates in
Live and the Engine), which supersedes the [x86_64-only bundles](research/x86-only-bundles.md)
inference that ReWire works under Rosetta. The x86_64 MultiF0 default is built-in; Convert Drums
uses a separate drum task; MultiF0 record fields are mapped. The x86_64 transport code corroborates
the [transport transitions](research/transport-transitions-native.md) readings, including both
Stop transfers, and adds a reflection branch present in both builds. Updated Q-013 and the
helper-launch page. Gaps: user-visible ReWire remnants, the Engine arm64 stub, MultiF0 time units;
PRB-N8-01 to 05.

## [2026-10-17] spec | SPEC-MIDI-USER-MAPPING revision 3 (N7 transforms)

[SPEC-MIDI-USER-MAPPING](specs/midi-user-mapping.md) REQ-005 gains static clauses (value mapping,
Absolute, Absolute14Bit, the relative step table, takeover exemptions) and static-conditional
clauses (Pick-Up and Value Scaling, on/off parameters); REQ-010 points at the crossfader's takeover
opt-out; evidence labels E10 to E14 added; cases MT-01 to MT-23 (18 static, 5 static-conditional).
Clauses were rechecked against kept dossiers n7-0001 to 0004 and re-read image constants;
`derive_cases.py` reproduced the cases byte for byte and 12 cases were recomputed exactly. One
clause is weaker than the packet: "no previous value keeps the current value" applies only to
Absolute. Updated the spec index, feature map, coverage and Q-009. A narrow midi-config-v3
candidate is justified but was not started, because no new work is being dispatched. Gaps:
PRB-N7-01 to 05.

## [2026-10-17] spec | SPEC-MIDI-NOTE-STORAGE revision 1 (D4)

Drafted [SPEC-MIDI-NOTE-STORAGE](specs/midi-note-storage.md) r1 from packet S7 (MN-01 to MN-24)
and query round d4-0001 (2 dossiers): 17 requirements, 60 unexecuted cases (45 gradable, 6
blocked by the unknown group shape, 9 unresolved). Missing note attributes are an explicit
exclusion, except NoteId absent from every note; MidiKey range and duplicate keys are excluded
(Q-018). New static result: the reader adjusts per-note lists with events at or before offset 0
or at or after the note's Duration (semantics untraced) and removes lists left empty; this affects
most lists in one shipped demo. Corrections: integer trailing spaces, the MN-20 drop rule, and the
PRB-S7-02 variant B expectation. The coordinator retained d4-0001 in
`analysis/ableton-live-12.4.3/r2/d4-midi-notes-v1/`. Not reviewed; nothing executed.

## [2026-10-17] spec | SPEC-BUNDLED-DEVICE-PARAMETERS r1 (N6)

Recovered the Analog, Tension and Collision parameter vectors (472 entries) by reading the
builders under both branch assumptions, naming members from class registrations and resolving two
virtual getters through vtables (24 dossiers, n6-0001 to 0003). Constructor defaults for 417
parameters; 412 of 426 calls re-read from disassembly. Cross-check against the bundles' own tables:
402 exact, 65 within range, 3 Collision mismatches, 1 unused index, 1 unrecovered row. Filed
[device tables](research/device-tables-native.md) and drafted
[SPEC-BUNDLED-DEVICE-PARAMETERS](specs/bundled-device-parameters.md) r1 (15 requirements, tables
for all 502 stored parameters of the seven devices, 37 cases). Collision's position parameters show
the same half-range pattern as Corpus (P4-N6-01). Updated the spec index (candidate row replaced),
feature map, coverage, Q-006, the device-bundles page and the Phase 4 note. Gaps: enumeration labels
for three devices, the device create path on load, Amp and Cabinet DryWet ranges. Nothing executed.

## [2026-10-17] spec | SPEC-AUTOMATION-ENVELOPES revision 1 (D6)

Drafted [SPEC-AUTOMATION-ENVELOPES](specs/automation-envelopes.md) from S6 (AE-C01 to C17, PRB-S6-01
to 07, Q-020): 13 requirements, 31 unexecuted cases (20 gradable, 10 unresolved, 1 partly). Dropped
AE-C09 (replaced by an exclusion), AE-C12 (now unknown) and AE-C16 (out of scope). Excluded dangling
targets and evaluation before the first event (Q-020). No new queries; claims rechecked against the
retained s6 dossiers and corpus excerpts. Corrected [automation envelopes](research/automation-envelopes.md):
the path without a converter does not clamp. Proposed PRB-S6-08 to 11 and a Pan variant of PRB-S6-04;
not yet in the Phase 4 batch. Updated the spec index (candidate row replaced), feature map, coverage
and Q-020. Nothing executed.

## [2026-10-17] maintenance | Traced Corpus demo: playable keys

The user reported that the on-screen MIDI keys did nothing. Root cause: the keys
only sent bare MIDI notes. Those act only through MidiPitch or MidiGate, which
are off in 25 of 26 presets. A note also makes no sound on an effect without an
input. The engine path itself works: with MidiPitch on, note 72 moves a String's
ring from 261.5 Hz to 523 Hz.

Fix: a "Keys play notes" page feature, on by default. A key press turns on
MidiPitch (shown in the MIDI section), sends the note and strikes the resonator
10 ms later, after its coefficients retune. Release sends note-off. The computer
keys A S D F G H J K map to the eight notes. Unticking the option restores bare
MIDI notes.

The page self-test now checks this wiring against the offline node and passes
3 of 3 runs; the 8 Node tests pass.

## [2026-10-17] spec | SPEC-WARP-MARKERS revision 1 (D7)

Drafted [SPEC-WARP-MARKERS](specs/warp-markers.md) r1 from packet S8 (WM-01 to WM-16) plus query
rounds d7-0001 and d7-0002 (16 dossiers): 16 requirements, 35 unexecuted cases (28 gradable, 7
unresolved). New static result: the scripting sample/beat conversion is piecewise linear over the
stored list, extending the first segment and the shadow segment, unclamped; playback mapping stays
unknown (PRB-S8-08). Edit limits are narrowed to the scripting add. WM-04 and WM-15 dropped, WM-16
excluded. The coordinator retained the d7 queries in `analysis/ableton-live-12.4.3/r2/d7-warp-v1/`,
added an update note to [warp markers](research/warp-markers.md), and opened
[Q-021](questions.md#q-021-warp-playback-mapping-and-load-handling). Updated the spec index
(candidate row replaced), feature map and coverage. Nothing executed.

## [2026-10-17] spec | SPEC-MIXER-VALUES revision 1 (D8)

Drafted [SPEC-MIXER-VALUES](specs/mixer-values.md) from MX-01 to MX-15 and two query rounds
(d8-0001 with 8 dossiers, d8-0002 with 6): 15 requirements, 45 unexecuted cases (11 audio renders
need measurement). Q-019 narrowed: volume consumers apply the volume curve and the silence floor on
every traced path; the gain-to-position conversion and the send path remain open. Upgraded to
static: the pan input order and the crossfade-assign default of 1. Corrections added to
[mixer values](research/mixer-values.md): pan 0.33 displays as `17R` for float32, and the −69.7 dB
boundary is excluded as rounding-sensitive. The coordinator retained the d8 queries in
`analysis/ableton-live-12.4.3/r2/d8-mixer-v1/`. Updated the spec index (candidate row replaced),
feature map, coverage, Q-019 and the gate table.

## [2026-10-17] maintenance | Dispatch paused; query servers stopped

By user direction, no further work was dispatched after the running agents returned. All agents
have returned and their results are committed. Both dossier query servers were stopped; the
hard-linked query copies remain under `/var/tmp/sound-analysis/query*` and can be served again
with the commands in [query route](research/r2-query-route.md). Natural next steps, not started:
separate reviews and handoff candidates for the new drafts, a midi-config-v3 candidate, merging the
post-consolidation probes into the Phase 4 batch, and the Phase 4 sitting on the macOS host.

## [2026-10-17] maintenance | Bundled audio samples for the traced Corpus demo

Added `tools/demo_samples.py` and six clips as sources for the traced demo: bongos
and a funk drum loop (both seamless loops), djembe, acoustic guitar, piano chords
and a LibriVox reading. All are CC0 or public domain on Wikimedia Commons; the
script refuses other licences and checks each download's SHA-1. The clips are
packaged as `analysis/ableton-live-12.4.3/demos/corpus-traced/samples.js`
(801 KB) with `samples-manifest.json`. No Ableton content is included.

The page gained a Sample menu, a Play/Stop button and credits. Checks: a
real-time headless Chromium run over CDP passes the full self-test (all six
clips decode at the expected lengths, key wiring, String at 261.5 Hz), and the
8 Node tests pass.

Finding: headless virtual time skips past off-thread audio decoding, so the
self-test needs real time (or a pending timer) to finish.

## [2026-10-18] analysis | Phase 4 batch extended with the post-consolidation probes

The user resumed work after the dispatch pause. The
[Phase 4 batch](research/phase4-probe-batch.md) now merges 67 newer records:
S5 11, S6 7 plus proposals 08 to 11, S7 10, S8 11, S9 8, N6 1, N7 5, N8 5 and
PRB-BI 5. That makes 146 records, 142 with their original IDs, in sessions
totalling about 39 h (2,325 min). New sessions K to Q run after I; J stays last.
There are two new merge groups, M-MIDI-ABS and M-WARP-RENDER, and M-SAVE now also
takes S9-07 and S7-09. Deferred as incomplete: S6-08 to 11, BI-01 to 05 and
S8-11. Eleven records cite requirements that disagree with their specs (for
example S9-04 still says 16R, against the corrected 17R). These are flagged on
the page, not fixed. `batch.json` still holds the original 79 records. Source
hashes are in `analysis/ableton-live-12.4.3/r2/phase4-batch-v1/sources-2026-10-18.json`.

Separately, the spec index and the transport-state and container specs now
record the two releases (cc64caf). Nine handoff candidates are being staged in
parallel, each followed by a separate review.

## [2026-10-18] release | Nine handoffs released from the revision 1 drafts and MIDI r3

Each candidate was staged by an author agent and checked by a separate review
agent that did not author it and will not implement. The coordinator verified
every payload hash, checked that the target directory did not already exist,
copied the staging package to `handoff/`, and scanned it for restricted links and
code identifiers. All cases remain unexecuted against Live.

| Release | Cases (staged) | Disposition | Main narrowing |
| --- | --- | --- | --- |
| [midi-config-v3](../handoff/midi-config-v3/README.md) | 127 (127) | Approved | None. Supersedes v2; its 109 cases are carried byte-identical |
| [clip-launch-v1](../handoff/clip-launch-v1/README.md) | 50 (50) | Approved with narrowing | REQ-015 removed; read-back limited to six significant digits |
| [midi-note-storage-v1](../handoff/midi-note-storage-v1/README.md) | 67 (67) | Approved with narrowing | Key-track order precondition; the d4-0001 cases were re-established from the corpus |
| [mixer-values-v1](../handoff/mixer-values-v1/README.md) | 37 (37) | Approved with corrections | Wording only |
| [automation-envelopes-v1](../handoff/automation-envelopes-v1/README.md) | 21 (29) | Approved with narrowing | The 8 value cases removed (assumption A1 untraced) |
| [bundled-device-parameters-v1](../handoff/bundled-device-parameters-v1/README.md) | 82 (82) | Approved with narrowing | Cabinet microphone labels found reversed and excluded; graded values of the position parameters removed |
| [browser-index-v1](../handoff/browser-index-v1/README.md) | 26 (28) | Approved with narrowing | Sidecars bind only to files directly in their folder; 2 cases removed |
| [plugin-discovery-v1](../handoff/plugin-discovery-v1/README.md) | 35 (35) | Approved with clarifications | Plain-file candidates named in the comparison obligation |
| [warp-markers-v1](../handoff/warp-markers-v1/README.md) | 38 (38) | Approved with narrowing | Values graded as read; tolerance bands widened; inferred labels removed |

Manifest digests are in the [catalog](../handoff/index.md). The corrections owed to
each draft spec are on its handoff plan, under Review outcome. They are not
applied yet: each spec page notes that its text is unchanged. One research
correction was applied. In
[device parameter mapping](research/device-parameter-mapping-native.md), the
Cabinet `MicrophoneTypeSwitch` labels were reversed: true shows Dynamic. The
index, feature map, coverage, project, gate table and catalog are updated. The
two release-status lines for transport-state and the container went in at
cc64caf. A link check of the changed pages and all release packages found no
new broken links. The 33 it reports are older links into the macOS-host
analysis tree, which is absent here (G0.2). The untracked
`r2/n1-transport-state-v1/.entry-map.pickle` (11 MB) is a cache and is left
uncommitted.

## [2026-10-18] decision | ADR 0003: no Mac observation; extracted execution instead

User direction: "mac observation not possible; we are finishing the proj on this
x86 machine". A follow-up added: "integration test style observation is still
possible if you can compile portions of the original program on this machine".
[ADR 0003](decisions/adr-0003-no-reference-execution.md) records both. Live as a
whole will not run, and the Phase 4 batch will not run as planned. The shipped
x86_64 machine code can still be loaded on this host and individual
self-contained functions called. That counts as a new evidence class, X
(extracted execution). Its limits are that the harness supplies setup and
stubs, results bind to the x86_64 slice, and equivalence with the arm64 target
is inferred. ADR 0002 points to it. The probe batch, roadmap, project milestones,
coverage, gate table, transport-state and container specs carry the change.

The same day, nine agents began applying the review findings to the draft
specs, and a pilot agent began building the harness. The harness is checked
against released mixer, MIDI and browser-index or transport cases.

## [2026-10-18] spec | Review findings applied to the nine draft specs

At the user's request ("fix such errors"), nine agents each applied the
staging and review findings to one draft spec. Each rejection gives a
reason. Where a finding and the draft disagreed, the agent re-checked the
cited evidence. Clauses that waited on a probe now cite ADR 0003 and name the
static route that remains, if any. Requirement and case IDs are stable;
withdrawn cases are marked, not deleted.

| Spec | Revision | Main corrections | Rejected |
| --- | --- | --- | --- |
| [MIDI user mapping](specs/midi-user-mapping.md) | 4 | Crossfader exemption limited to Absolute values; reversed-range stepped rule stated; reversed-range takeover unknown | RV3-07 (adds cases, no error) |
| [Clip launch](specs/clip-launch.md) | 2 | F1 to F9 and seven review findings; REQ-015 to 018 release proposal dropped; new assumption A7 | None |
| [MIDI note storage](specs/midi-note-storage.md) | 2 | A1 widened and established; key-order precondition; 64-bit signed; A3 for integer reading; MNS-061 to 071 | Copying d4-0001 (review excerpts cited instead) |
| [Mixer values](specs/mixer-values.md) | 2 | REQ-008 and 009 citations; REQ-002 upper bound; MV-020 to 022 and 027 ungraded; MV-046 (pan 0.33 gives 17R) | None |
| [Automation envelopes](specs/automation-envelopes.md) | 2 | A1 covers every Float value; AEN-001 and 002 withdrawn; AEN-003 reworded; AEN-032 and 033 | Probe route for Bool and Enum |
| [Bundled device parameters](specs/bundled-device-parameters.md) | 2 | Cabinet microphone labels corrected; DryWet 0..1; unstored Collision fields removed; Corpus side-chain fields; tables in document order | None |
| [Browser index](specs/browser-index.md) | 2 | Sidecars bind to direct files only (BI-040 and 041 withdrawn, BI-045 and 046 added); low-32-bit colour rule; unmatched entries dropped | F7 (narrows the candidate, not an error) |
| [Plug-in discovery](specs/plugin-discovery.md) | 2 | F1 to F7; release cases adopted as PD-043 to 062 | None |
| [Warp markers](specs/warp-markers.md) | 2 | A2 split into opening (A2) and saving (A4); REQ-015 inclusive bounds; tie band; WMK-036 | F2 (the review showed TransientEnvelope is created at 100) |

Research pages carry dated correction notes. The handoff plans record what each
revision applied. Released payloads are unchanged. The question register
(Q-006, 009, 014, 016 to 021), spec index, feature map, coverage and project
page are updated. Two gaps were found. First, the automation spec's claim that
Bool and Enum values skip conversion rests partly on scratch lookups that were
not retained; the spec says so, and the claim should be re-established and
retained. Second, the note-storage review found that the integer reader
accepts a leading `-`. REQ-TRANSPORT-STATE-006 still marks `-` as unknown, so
check whether it is the same reader.

## [2026-10-18] analysis | X1 extracted-execution pilot passes

[Extracted execution](research/extracted-execution.md) records the method,
limits and results. `tools/xexec/xexec.c` maps the Mach-O segments of the
original x86_64 slice into a Linux process and applies its fixups. It binds 57
libm functions and a few libc functions to glibc, and traps every other import.
It then calls one function with System V arguments. `xexec.py` runs each call
in a subprocess. Evidence, with `run.sh` and a manifest, is in
`analysis/ableton-live-12.4.3/r2/x1-extracted-exec-v1/`.

There were 476 runs with no trap or fault. Results against released cases:

| Target | Agreement |
| --- | --- |
| Mixer dB and pan text | 44 of 44 released texts and 23 spec examples |
| MIDI map-mode values | 18 of 18 midi-config-v3 value cases, all ten modes, 14-bit pairing via gdb |
| Transport number writer and time-signature parser | 8 of 8 checks and 22 examples |

The colour parse lives in the index helper and was not run. Findings:

- REQ-TRANSPORT-STATE-011 step 1 is imprecise next to powers of ten. The code
  takes k from the binary64 `log10`, so 1000.0000000000001 is written
  `1000.00000000000011`. Released transport-state-v1 states that rule, so it
  needs a corrected release.
- Negative zero is written `-0`.
- The integer parser accepts `-201` and refuses padded or signed-padded forms.
- Pan ties round to even: 0.25 gives `12R`.
- arm64 computes the Absolute map mode with a fused multiply-add. Results
  differ from x86_64 by one binary32 ulp when min is not 0. No released case is
  affected, but the 1e-6 tolerance is too tight for wide ranges.
- Maths and formatting come from glibc, not Apple's libraries. This is
  recorded as a limit.

The page lists the probes and questions this route can settle.

## [2026-10-18] analysis | X2: open clauses settled by extracted execution

Five agents used the [harness](research/extracted-execution.md) to run the
original x86_64 functions that decide open clauses. Each revised its specs. The
evidence is in `analysis/ableton-live-12.4.3/r2/x2-*`, each directory with
`run.sh` and a manifest.

| Topic | Spec revision | Settled (X) | Errors corrected | Still open |
| --- | --- | --- | --- | --- |
| Mixer | [mixer-values](specs/mixer-values.md) r3 | Fader curves both ways (exact round trip), pan law, seven crossfade curves, `On`/`Off` | Model rounding in `derive_curves.py` | Engine-port values (Q-019) |
| MIDI | [midi-user-mapping](specs/midi-user-mapping.md) r5 | Pick-Up and Value Scaling takeover, reversed ranges, first 14-bit pair; 34 X cases | 1e-6 tolerance replaced; reversed-range takeover formula | Master-volume display, PRB-N7-04 and 05 |
| Transport | [transport-state](specs/transport-state.md) r3 | REQ-011 rule, negative zero, REQ-006 integer spellings, meter codes | REQ-011 next to powers of ten | REQ-009, REQ-012; Apple's `log10` near half a spacing |
| Notes | [midi-note-storage](specs/midi-note-storage.md) r3 | Value limits, time-grid rounding, saved number text | None; no MidiKey guard exists, so REQ-011 is permanently excluded | Re-sorting, list adjustment |
| Clip launch | [clip-launch](specs/clip-launch.md) r3 | Grid and boundary arithmetic, chance rescaling and limits, follow-time rounding | REQ-016 (stored −99 launches as Global), REQ-017 (triplet grid lines) | Scheduler call (A1), near-boundary offset |

Harness defect: the loader's 256-slot return array had no bounds check. It now
stops with an error at the 257th call in one process. The X1 runs and four of
the five X2 sets stayed under the limit. The MIDI set went over it in ten
processes; those were re-run, and no value changed. The harness page also
corrects its claim that glibc's `log10` is correctly rounded: it is not for 108
of 6,539 inputs.

transport-state-v2, which corrects released REQ-011, is staged and under
separate review. Automation and warp work is still running. The question
register, spec index, feature map and coverage are updated.

## [2026-10-18] release | transport-state-v2 corrects REQ-011 and supersedes v1

[transport-state-v2](../handoff/transport-state-v2/README.md) was staged by the X2
transport agent and approved by a separate review agent. The review made four
clarifications, RV2-01 to RV2-04, and changed no case. The manifest SHA-256 is
`398a88a62114552595830f99ba2fc1bc4d8c0e1f0d2ae65a70d21aa2324c17c8`.

The release carries v1's 18 cases byte-identical and adds 15. TS-010 and TS-024
to 037 come from extracted execution. It replaces v1's REQ-011 rule, which
gave the wrong text next to powers of ten. Values whose logarithm lies 1/4 to
3/4 of a binary64 spacing from an integer are excluded. The reading of `-0` and
the exact save text are marked as depending on glibc.

[SPEC-TRANSPORT-STATE](specs/transport-state.md) revision 4 applies the review's
clarifications. The coordinator verified every hash and scanned the published
copy for restricted links and addresses. The catalog, spec index, feature map,
coverage, project page and gate table (new X2 row) are updated.

## [2026-10-18] analysis | X2 automation and warp

Automation envelopes and warp markers are both at revision 3 (evidence:
`r2/x2-envelope-warp-v1`). Every run matches its spec case bit for bit.

Envelopes:
- Float evaluation is now X: holds, values at event times, equal values,
  linear segments, the ramp and curves. At a step, mode 0 gives the left value
  and mode 1 the right.
- Envelopes evaluate in stored units. The conversion step applies a converter
  only if one is present, and none is (static).
- The Bool and Enum no-conversion claim is now X, with retained evidence.
- Evaluating before the first event crashes, so that input stays excluded.
- Unknown: whether song position drives the evaluator, and which caller picks
  which mode.

Warp:
- The beat and sample conversion, the shadow marker (it reproduces the shipped
  shadows) and the REQ-015 and 016 edges are X.
- Revision 2's tolerance bands are replaced by the exact binary64 operation
  order.
- Playback stays unknown, because no caller connects these functions to it.

Errors fixed:
- The discrete path crashes before the first event; revision 2 said it
  returned the list head.
- A negative-zero beat rounds to +0.

No process exceeded 22 calls. The agent used a private bounds-checked loader
copy, and one run failed when a rebuild replaced its binary; it produced no
values. Questions Q-019 to 021, the spec index, feature map, coverage and gate
table are updated.

## [2026-10-18] decision | ADR 0004 target T1; roadmap revision 3

The user asked whether spec generation was complete. It is not: three of 14
families have no spec, and the other eleven each cover a narrow slice. The user
accepted the recommendation to choose a bounded target ("proceed"), and asked
for the plans to be updated.

[ADR 0004](decisions/adr-0004-target-scope-t1.md) defines T1:
- open and save Live Sets for the T1 fields;
- offline-rendered playback: transport, Trigger launches, MIDI and unwarped
  audio clips, the mixer, automation and the seven bundled devices;
- MIDI control.

It also sets the acceptance dimensions, which answers Q-001 for T1.
[Roadmap revision 3](research/native-decompilation-roadmap.md#revision-3--t1-completion-plan-2026-10-18)
plans workstreams T1.1 to T1.7, with gate rows added.

Checks made for the plan: the seven device bundles are universal binaries with
x86_64 slices, so their DSP can be run under the harness; bubblewrap is installed
and proposed for the isolated implementation workspace (T1.6, which needs the
user's decision).

## [2026-10-18] spec | T1.1 structure and T1.4 mix graph; released fixtures found invalid

The T1.1 and T1.4 drafts are in:
- [SPEC-LIVE-SET-STRUCTURE](specs/live-set-structure.md) r1: 18 requirements and
  40 cases, plus the minimal set T11-MIN;
- [SPEC-MIX-GRAPH](specs/mix-graph.md) r1: 16 requirements and 34 cases.

Every open route runs the reader's validation walk (A1), traced in both corpora
with the key branches read in x86_64 disassembly. That walk refuses two kinds of
set:
- a set with no audio or MIDI track;
- a track that has clip slots but no freeze sequencer (A2).

An audit
(`r2/t11-structure-v1/released-fixture-audit.json`) finds 204 fixtures that would
be refused, contradicting 178 cases:

| Release | Fixtures | Cases |
| --- | --- | --- |
| transport-state-v1 | 18 | 13 |
| transport-state-v2 | 33 | 23 |
| automation-envelopes-v1 | 21 | 13 |
| clip-launch-v1 | 49 | 43 |
| midi-note-storage-v1 | 66 | 51 |
| warp-markers-v1 | 17 | 35 |

als-container-v1 is unaffected. For mixer-values-v1, the effect of the missing
SendsPre is unknown. The catalog now carries a defect note. Superseding releases
with fixtures rebuilt on T11-MIN are next. Both briefs now require a fixture
validity check: the first review round had none, which is how these got through.

T1.4 also settled Q-019, with conditions: Live sends fader positions, not gains,
to the engine. Its follow-up wrote two revisions:
- automation r4 separates evaluator values from playback: a 16-piece polyline,
  a first point at −10⁷ beats, and the later event at a step;
- mixer r4 narrows REQ-011 to 015.

Neither contradicts a release. ADR 0004 gains a render convention: rendering
starts from a settled state. New questions are Q-022 (structure load rules) and
Q-023 (mix-graph conditions). The T1.3 playback-core draft is filed with its
corrections still in progress.

## [2026-10-18] spec | T1.3 playback core; clip launch r4 and warp r4

[SPEC-PLAYBACK-CORE](specs/playback-core.md) r1 has 23 requirements and 68 cases, with
evidence in `r2/t13-playback-v1`. It covers transport, launch timing, note
emission and unwarped audio playback. Launch timing (clip-launch A1) is settled
for Trigger launches. Eight cases accept either P or P+1 at 48 kHz, because the
engine's sample counter decides which; this is Q-024.

Corrections:
- **Clip launch r4.** REQ-017's offset is the track player's pre-delay: 0 for
  MIDI, the audio crossfade length otherwise. REQ-018 and 019 are corrected.
  Sample-exact timing replaces the ±1/64-beat tolerance.
- **Warp markers r4.** REQ-009 named no playback caller; one exists. Warped
  playback uses the scripting mapping, and unwarped session clips ignore
  markers.
- **Transport transitions.** T-01's first played sample is exactly the start
  beat.

None of these contradicts a released handoff.

## [2026-10-18] analysis | T1.2 device audio gate passes

A copy of the harness loader loads a device bundle's own x86_64 slice. The
bundles are universal binaries in the app, and the copy renders audio through
them. Evidence is in `r2/t12-device-dsp-v1`, and the method is described in
[device DSP](research/device-dsp-extracted.md).

Corpus results:
- renders are bit-identical across 25 determinism checks;
- every difference from the static model and from the traced demo port is
  explained.

[SPEC-DEVICE-CORPUS](specs/device-corpus.md) r1 has 13 requirements and 28 cases
(24 graded against retained renders). Its proposed metric is per-mode
frequency, decay and amplitude bounds, plus third-octave levels for broadband
output. A one-ulp libm change moves a 66 Hz mode measurably, so the metric does
not use maximum absolute error.

Corrections to research pages: Pipe and Tube frequencies are 251.271 and
241.687 Hz, not 251.0 and 241.2, and output starts after a 100-frame silence.
The traced demo port ramps from frame 0 and skips DecayOnNoteOff's 1 − v.

Effort for the other devices:
- Analog, Tension and Electric already render;
- Collision is silent with Live's defaults;
- Amp and Cabinet need CoreFoundation and Objective-C emulation and a fake
  host identity. That is held for the user (Q-025).

## [2026-10-18] release | midi-config-v4 supersedes v3

[midi-config-v4](../handoff/midi-config-v4/README.md) has 161 cases: v3's 127 carried
byte-identical, and 34 from extracted execution covering Pick-Up and Value Scaling
takeover, reversed ranges and the first 14-bit pair. A separate review agent
approved it with one narrowing: a stepped value within 8τ of a half-integer has
no expectation. Relative message runs are compared within k×τ.

The manifest SHA-256 is
`0911e9b57730b9d41c143cd18a5bacc80d8439ce51b202201820bef9ff8cef65`. The review's
two precision corrections, and its correction of the Value Scaling error figure
(96 to 408τ, not 3.8τ), are owed to spec revision 6.

## [2026-10-18] release | transport-state-v3 corrects the fixture defect

[transport-state-v3](../handoff/transport-state-v3/README.md) carries v2's 33 cases,
with records unchanged. Each fixture gains a MIDI track so that the reader
opens it. A separate review agent approved it with two clarifications: the
refusal rule covers no audio, MIDI or group track, and v2's fixtures judge no
case. The manifest SHA-256 is
`2cd4320ac3e6cefab257d8f8ab6bc627284c87ca4b0b7c06e5ea22ae172d329d`. The catalog's
defect note now states the rule precisely. New REQ-012 evidence for the next
spec revision: on open, a tempo Manual value that disagrees with its automation
envelope is replaced by the envelope's value.

## [2026-10-18] release | midi-note-storage-v2 corrects the fixture defect

[midi-note-storage-v2](../handoff/midi-note-storage-v2/README.md) has 72 cases: v1's
67, each with a freeze slot and a scene added to its fixture, plus 5 new cases
from extracted execution. A separate review agent approved it with listed
clarifications: positive-zero `Duration`, `TimeOffset` negative zero excluded, and
a completed change list. No expectation changed. The manifest SHA-256 is
`697f09ffc4951d5f3b6d67c20b8f851d68671078a0b3d730a220383f94d2dd15`.

## [2026-10-18] spec | SPEC-DEVICE-ELECTRIC r1

[Electric](specs/device-electric.md) audio is specified from extracted execution of the
bundle's x86_64 code: 16 requirements and 32 cases, 23 graded against 120 retained
renders. Polyphony is settled: index p allows p + 2 voices, which settles the
labels SPEC-BUNDLED-DEVICE-PARAMETERS REQ-014 left unknown. KeyboardStretch acts
as a ±7.2-cent detune.

Corrections:
- The T1.2 gate's Electric probe used a rounded Volume and played during the
  start-up ramp; its peak should be 0.296, not 0.32.
- The N5 conversion table prints Volume's default rounded; it is 0.7047892213.

Open, under Q-025: grid phase, the event frame base, stop-processing, and the
block in which an automated value arrives.

## [2026-10-18] release | mixer-values-v2

[mixer-values-v2](../handoff/mixer-values-v2/README.md) has 80 cases: v1's 37 on
rebuilt fixtures, plus 43 computed cases from extracted execution. A separate review
agent approved it with narrowing. The review confirmed that the gain-to-position
round trip is not exact: 765 of 1,601 random gains, run through the original code,
come back up to 2 steps off. The earlier "bit-exact" claim in the mixer and
mix-graph specs and in Q-019 is therefore wrong, and is listed for correction. The
manifest SHA-256 is
`a79d427a2266ec637d18aad9cbd690c1656ddeea629b4c04501f6817389a6ae8`.

## [2026-10-18] release | mix-graph-v1

[mix-graph-v1](../handoff/mix-graph-v1/README.md) is the first release of SPEC-MIX-GRAPH.
It has 28 cases: 17 computations and 11 composed renders, labelled as spec
conformance under ADR 0004. A separate review agent approved it with narrowing:
automation application holds under the default settings only, the main track's
one-event envelopes are exempt, and the timing sentence is moved out of the
released clause. The review confirmed the spec errors the author found.

## [2026-10-18] release | live-set-structure-v1

[live-set-structure-v1](../handoff/live-set-structure-v1/README.md) is the first
release of SPEC-LIVE-SET-STRUCTURE, with 34 cases. A separate review agent approved
it with narrowing. Devices are removed from T11-MIN and every fixture, because
device placement (REQ-012, Q-022) is not established. The track rule reads "no
audio, MIDI or group track", and the path fallback is limited to codes 0 and 1. The
open-path and freeze-slot rules held under review. The staged warp-markers-v2 puts
a device on a track, and its reviewer has been told to remove it.

## [2026-10-18] release | automation-envelopes-v2

[automation-envelopes-v2](../handoff/automation-envelopes-v2/README.md) has 21 cases on
openable fixtures. A separate review agent confirmed, in both builds, a removal
step on open that runs before the checks. It deletes clip envelopes that have
exactly one event, and Speaker, Pan and CrossFadeState envelopes with fewer than
two. That makes v1 cases 003, 004 and 011 wrong. They are withdrawn, and the
change list says so. No evaluated or playback values are released. The manifest
SHA-256 is
`267554cb2edc6c9960bfd5d67bcf996b833de15b9375063edfce4232c09d3791`.
