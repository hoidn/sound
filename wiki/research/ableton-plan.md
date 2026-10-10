---
id: RESEARCH-ABLETON-PLAN
type: research
status: draft
updated: 2026-10-09
access: analysis
---

# Ableton investigation plan

The analysis method follows [ADR 0002](../decisions/adr-0002-static-first-analysis.md).
Subsystem ordering remains proposed, not verified Ableton behavior. Track full scope in the
[feature map](../specs/feature-map.md).

## Next major phase

The [native decompilation roadmap](native-decompilation-roadmap.md) is the
concrete draft for the next phase: systematic main-image code exports, a
human-readable method guide and evolving program atlas, focused native
behavior investigations and a first reviewed handoff. It proposes execution
gates and deliverables; no bulk analysis has started. This page continues to
own the general investigation method and its rationale.

## Reference identity

The first static pass now has a [durable source record](sources/ableton-live-12.4.3.md)
for Live 12.4.3, original and derived executable hashes, host/provider environment,
and exported REA evidence. The [structure findings](ableton-package-structure.md)
map the package. The [decompilation preparation](ableton-decompilation-preparation.md)
records a successful Push2 helper pipeline check and an accepted core Live arm64
input. Core Live deep analysis and runtime behavior remain unverified.

## Evidence channels

| Channel | Planned use | Boundary |
| --- | --- | --- |
| [Live manual](https://www.ableton.com/en/live-manual/12/welcome-to-live/) | Feature and workflow inventory | Confirm version-specific details against the pinned build |
| Shipped resources, schemas, scripts and saved fixtures | Default: recover contracts, defaults, formats and state relationships | Stored examples alone do not prove every loading or migration rule |
| REA/Ghidra | Default: targeted control/data-flow analysis and behavioral derivation | Resolve relevant paths and assumptions; static evidence does not establish execution |
| [Live Object Model](https://docs.cycling74.com/userguide/m4l/live_api_overview/) | Optional targeted state/control probes | Establish API coverage before use; notifications do not prove sample timing |
| [AbletonOSC](https://github.com/ideoforms/AbletonOSC) | Optional adapter if a specific probe warrants it | Pin/test only when needed; do not infer sample timing from OSC arrival |
| Audio/MIDI captures and file round trips | Targeted gap resolution and later compatibility comparisons | Record exact inputs, environment and variability; reuse captures |
| UI scenarios | Last-resort probe for questions requiring UI interaction | Keep scenarios minimal; establish tool coverage before assuming automation |

External URLs are discovery pointers, not archived sources. Ingest a versioned
source record when a claim depends on one.

## Investigation loop

1. Pick a bounded feature question from the map and consult existing findings.
2. Inspect the relevant versioned documents, resources, scripts and fixtures;
   trace native code where necessary to derive observable behavior.
3. Draft the behavioral contract and acceptance cases with exact evidence,
   static derivations, assumptions and unresolved details distinguished.
4. For material gaps, apply the [runtime escalation rule](../decisions/adr-0002-static-first-analysis.md#runtime-escalation-rule).
   Execute only a justified minimal probe; otherwise retain the gap as unknown.
5. Reconcile findings and submit the bounded contract through
   [handoff review](../workflows.md#release-a-handoff). Prior execution is not a
   universal release prerequisite; sufficient evidence and explicit scope are.
6. Retain targeted original-versus-candidate comparisons as later verification
   obligations. Static derivation alone does not close empirical compatibility.

Prioritize transport/project state, clip playback/routing, Session/Arrangement
interaction, editing/automation, persistence/hosting, then devices and ecosystem
compatibility. This is scheduling guidance; it does not remove later features
from the whole-app scope.

Keep original-side findings here and in specs. Independent implementation design
lives in its permitted workspace and receives only approved handoffs.

## Review of the proposed harness-first approach

Analyst assessment, 2026-10-09, of the user-supplied eight-part proposal in the
conversation (opening: “I’m assuming the goal is a native application with high
behavioral and GUI fidelity”). The proposal is a discussion input, not adopted
policy or evidence of Ableton behavior. The quotations and section numbers here
identify the reviewed claims; the full message is not independently archived.
[ADR 0002](../decisions/adr-0002-static-first-analysis.md) remains authoritative.

Keep its strongest elements: full-distribution identity, version/architecture
pinning, question-driven investigation, explicit contract provenance, GUI
interaction states, scoped tracing, end-to-end milestones and enforced separation
between analysis and implementation. Its instruction to measure supported
workflows instead of renamed functions is useful progress guidance.

Revise the sequencing. Section 2 (“Build the observation-and-replay harness
before deep reverse engineering”) and the final first-work-package requirement
make a replay harness, diagnostic plugin and instrumentation access universal
prerequisites. For this project those are conditional tools. First derive a
bounded contract from available evidence; build only the probe/adapter required
to resolve its material uncertainty, or when a small experiment is clearly
cheaper than further tracing. A full bundle inventory establishes artifact
identity, not a reproducible running installation. Keep those statuses separate.

The [MIDI mapping investigation](midi-user-mapping.md) provides a concrete
example: scoped bytecode work resolves parser, channel, bank and button branches
without a running reference. Its case matrix remains unexecuted. Section 5's
warning about tests and implementation sharing the same mistaken inference is
sound, but it does not imply reference execution is mandatory for every draft
or release. Independently review derivations and provenance; reserve empirical
compatibility claims for actual comparisons.

Additional methodological gaps and proposed corrections:

- Define compatibility dimensions before interpreting “high fidelity”: supported
  workflows, GUI geometry/interactions, file subset, audio metrics and timing
  tolerances. The opening native/GUI assumption is not a settled project target
  ([Q-001](../questions.md#q-001-compatibility-targets)).
- Preserve the action path. A semantic adapter can hide differences by doing
  extra operations or translating an unavailable command. Record concrete
  actions, preconditions, completion criteria and observable intermediate states.
  Treat UI and API invocation as distinct until their relevant effects agree.
- Separate observation channels and clocks. Cycling '74 documents that
  `live.object` messages are deferred to the main thread; it is unsuitable as
  a sample-accurate timing oracle. Steinberg marks many `ProcessContext` fields
  optional and does not require every host to split a processing block at a
  timeline jump. A plugin probe must check validity flags, define its graph
  position, record latency/configuration and test whether it perturbs results.
- Establish reference repeatability before comparing candidates. Use repeated
  baseline cases and explicit tolerances for nondeterministic paths; neither
  exact audio equality nor pixel equality is universally appropriate. Record
  build, project, media, plugin and environment identities with each case.
- Section 3's “one canonical analysis database” is an aspiration, not a verified
  property of REA. Our retained REA snapshot holds eligible query results, not
  a complete Ghidra project. Prefer one canonical evidence catalog with exported
  records and pinned tool settings; separately validate database persistence
  before depending on it. See [source limitations](sources/ableton-live-12.4.3.md#identity-and-retained-evidence).
- Frida overhead cautions in section 4 are supported by its documentation.
  Establish attach feasibility when it is a selected probe dependency; do not
  make arbitrary internal instrumentation a gate for unrelated static work.
- Separate first contract from first integrated application milestone. The
  proposed open/launch/edit/save/undo slice is a useful later integration target,
  but combines several currently unspecified contracts. Progress through small
  reviewed contracts and then test their interactions. Keep unknown file-data
  preservation and safe rejection explicit.
- Leave framework selection to an isolated implementer evaluating released
  requirements. JUCE is a candidate, not an outcome of reverse engineering.
  Role names alone do not enforce the clean handoff boundary; our current shared
  analyst checkout is unsuitable for independent implementation.

Recommended sequence: bounded question → retained static evidence → contract
and planned cases → minimal probe for material gaps → reviewed handoff → isolated
candidate → targeted differential comparisons. Grow reusable harness components
from proven cases; do not treat harness breadth as recovered behavior.

Technical sources consulted 2026-10-09 (live documentation; no exact installed
SDK/API version or retained page snapshot established):

- [Cycling '74 live.object reference](https://docs.cycling74.com/reference/live.object),
  description and main-thread/deferred-message limitation.
- [Steinberg ProcessContext reference](https://steinbergmedia.github.io/vst3_doc/vstinterfaces/structSteinberg_1_1Vst_1_1ProcessContext.html),
  detailed description, optional-field flags and loop/jump block guidance.
- [Frida JavaScript API](https://frida.re/docs/javascript-api/), Interceptor
  performance considerations, callback and `send()` overhead.

These sources constrain proposed measurement techniques; they establish no
observed behavior of the pinned Ableton build. The pasted generic “GitHub”
citation labels do not identify repositories or revisions and are insufficient
to choose between REA and a particular ghidra-rpc project.

## Linux analysis host versus reference host

Assessment, 2026-10-09: Linux is a suitable proposed host for static analysis and
specification work; the current REA/export pipeline has not been validated there.
Ghidra's [Getting Started guide](https://github.com/NationalSecurityAgency/ghidra/blob/master/GhidraDocs/GettingStarted.md),
"Platforms Supported" and "Headless (Batch) Mode", documents Linux support.
Its [Mach-O loader](https://raw.githubusercontent.com/NationalSecurityAgency/ghidra/master/Ghidra/Features/Base/src/main/java/ghidra/app/util/opinion/MachoLoader.java),
`findSupportedLoadSpecs` and `load`, parses target bytes into an analysis program.
Inference: analysis of the retained Mac arm64 image does not require running Live
or matching the analyst host's CPU to the target CPU. This is tool capability,
not evidence that our particular workload has succeeded on Linux.

Before migration, retain the required original bundle/resources and ignored
analysis artifacts with hashes, configure host-specific paths/tools, pin compatible
REA/Ghidra/JDK versions and validate a bounded import/export. A Git clone alone
is insufficient: the [source record](sources/ableton-live-12.4.3.md) identifies
external mutable resources and locally retained slices. The
[export design](native-export-design.md) also records an ephemeral provider DB;
copying exported evidence is not preserving a live analysis session. No migration,
installation or benchmark was performed for this assessment.

Recommend Linux for bulk work with occasional access to the pinned Mac reference
for justified probes and empirical comparisons under ADR 0002. Ableton's
[system requirements](https://help.ableton.com/hc/en-us/articles/115001663530-Live-Minimum-System-Requirements)
list Windows and macOS, not native Linux. A Windows reference is a distinct build
and platform; do not silently substitute it for the pinned Mac target. Fully
offline static work can proceed, but unavailable reference measurements remain
unknown. Independent candidate work still needs an isolated workspace; any
macOS-specific candidate integration requires appropriate target-platform checks.

External sources above were consulted 2026-10-09. Ghidra's live guide identifies
itself as 12.2, whereas the retained local source record names 12.1.4; repository
URLs are mutable and no source snapshot or exact commit was retained. These
references support host feasibility only, not version parity or a released spec.
