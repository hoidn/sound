---
id: LOG-WIKI
type: log
status: active
updated: 2026-10-09
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
