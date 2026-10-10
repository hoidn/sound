---
id: RESEARCH-NATIVE-TRANSPORT-STUDY
type: research
status: draft
updated: 2026-10-09
access: analysis
target: Ableton Live 12 Suite 12.4.3 arm64
---

# Native transport investigation design

The first two native studies will ask how one loop-enable field survives
loading and saving, and how a start request followed by a stop request changes
transport state. These bounded questions connect readable project data to
exported native code without requiring an explanation of the whole audio engine.
The design supports M5 of the [roadmap](native-decompilation-roadmap.md);
actual execution and resource limits belong to the
[phase ledger](native-phase-execution.md).

This preparation inspected retained resource observations and symbol entries,
then retained the two matching original resources and constructed twelve input
candidates. The first main-image export now exposes four direct calls and
setup-like writes in the `ALoopOn` factory. Its connection to persisted state,
load/save behavior and command semantics remains unknown. These bounded native
findings do not yet support a behavioral specification.

## Evidence already available

The [retained selection](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/retained-seeds-v1.json)
pins its three input summaries and exact symbol rows. Its
[checksum manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/artifact-checksums.json)
protects this selection. It adds navigation, not an independent observation.
Executable identity and the source capture's limitations remain canonical in
[the installed-source record](sources/ableton-live-12.4.3.md).

| Observed evidence | Exact retained locator | What it can establish |
| --- | --- | --- |
| `LiveSet` declares a `Transport` field with `Class=Transport`, `Type=0` | Resource JSON: `evidence.latest_numbered_schema.selected_classes.LiveSet.fields`, matching `name=Transport` | A relationship in the shipped schema vocabulary |
| `Transport` declares `LoopOn`, `Class=LoopOn`, `Type=0` | Same JSON: `selected_classes.Transport.fields`, matching `name=LoopOn`; schema XPath `/AbletonSchema/Transport/LoopOn` | The declared field name and class, not its default or parser rules |
| Default ALS stores `LoopOn/@Value=false` | `evidence.format_samples[0].seed_values.transport.LoopOn`; fixture XPath `/Ableton/LiveSet/Transport/LoopOn/@Value` | One stored value in the bundled fixture |
| Default ALS identifies Live 12.1d1 and schema `12.0_12117` | `evidence.format_samples[0].root_attributes` | The fixture predates the installed 12.4.3 build; it is not a save captured from that executable |
| Highest numbered shipped schema is `12.0_12402.txt` | `evidence.latest_numbered_schema.artifact`, SHA-256 `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` | The selected schema identity; executable use and migration rules remain unknown |

All JSON paths above refer to
[resource-analysis.json](../../analysis/ableton-live-12.4.3/resource-analysis.json).
The default ALS compressed hash is
`aeec3f07599da0a61cc86fd9ddeb78a5ce61fe473f676d50c1ae3e281c289a1f`;
decoded hash is `6ccfa96df1e7a7fbdcd48fc40641ace19bd5e798acc23117c45fda64a78d4783`.
The original capture retained parsed observations and hashes rather than these
complete resource bytes. The follow-up [resource capture manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/sources-v1/manifest.json)
now retains the complete schema (441,285 bytes), compressed default ALS
(13,657 bytes) and decoded XML (182,528 bytes). All three hashes match the earlier
capture. This adds durable local bytes without changing the earlier evidence.

The earlier JSON records `Transport.line=3807`, while
[resource-findings.txt](../../analysis/ableton-live-12.4.3/resource-findings.txt)
names top-level `Transport` at line 8168. The matching-byte recapture resolves
this: line 3807 is `/AbletonSchema/LiveSet/Transport`; line 8168 is
`/AbletonSchema/Transport`. Its `LoopOn` field is line 8170. The manifest records
Expat-derived paths, lines and byte offsets. Earlier records remain unchanged.
This corrects a locator; it does not change a behavioral expectation.

The retained schema's top-level `LoopOn` at line 3925 contains
`<Value Class="Bool" Type="-4" />` on line 3926. This strengthens the declared
boolean-type observation, while accepted tokens, defaults and conversion
behavior still require the native reader or a reference observation. The
default XML's selected `LoopOn` occurs at line 5084, byte offset 159862.

## Native query seeds

The following rows were checked in the
[arm64 symbol index](../../analysis/ableton-live-12.4.3/live-arm64-symbols.tsv).
Addresses are static virtual addresses for the pinned arm64 image, not runtime
addresses or evidence that Ghidra recognizes an eligible function there.

| Seed | Address | TSV line | Initial question |
| --- | --- | --- | --- |
| `SNewCompound<ATransport>()` | `0x10275dc64` | 88 | Which constructor and registration paths does this factory reach? |
| `SNewCompound<ALoopOn>()` | `0x10276e5d4` | 2602 | Which state/type registration can connect the schema field to reader/writer code? |
| Callback wrapper naming `ATransport::OnStart` | `0x102770a58` | 26626 | Does the wrapper branch to a body, and what is that body's actual address? |
| Callback wrapper naming `ATransport::OnStop` | `0x102770a64` | 26625 | Which state writes or requests does the resolved body make? |
| Callback wrapper naming `ATransport::OnCurrentTimeChanged` | `0x102770994` | 26610 | Is there a demonstrable relationship to position changes? |
| Callback wrapper naming `ATransport::OnLoopIsSongStart` | `0x102770c70` | 26606 | Could this affect the selected loop-enable question? |
| Callback wrapper naming `ATransport::ClearLoopIsSongStart` | `0x102771394` | 26600 | Is it relevant to start/stop or merely adjacent? |
| `SNewCompound<ASongAgent>()` | `0x10269c558` | 77 | Fallback document/transport connection if direct seeds are unproductive |

The full demangled names in the retained selection identify the callback
templates. A wrapper bearing `OnStart` is not automatically the handler body or
the path taken by a GUI Play action. Resolve both connections separately.

## First native findings

The selected `ALoopOn` factory at `0x10276e5d4` now has retained
[pseudocode](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/pseudocode.c),
[assembly](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/assembly.txt)
and [metadata](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/functions/0x10276e5d4/metadata.json).
The [findings record](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/loop-factory-findings-v1.json)
pins seven source artifacts against the sealed run manifest and records the
exact excerpt used by the [first-code lesson](learning/walkthroughs/first-native-loop-factory.md).

This export uses `ghidra-selected-entry-noanalysis-v1`, Ghidra 12.1.4, on the
pinned Live arm64 SHA-256 from the source record. It disables automatic and
incremental analysis, recovers a selected body within a 4,096-byte window and
requests its decompilation with a 60-second limit. The actual recovered body is
104 bytes/26 instructions, and pseudocode is 391 bytes. The
[run status](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v1/run-status.json)
records exit 0, export success and cleanup without survivors. This custom-script
output is not a REA evidence record or a default-profile whole-image inventory.
The default analysis encountered its
[disk stop](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/transport-pilot-v2/RESOURCE_STOP.json);
the fallback's narrower profile must remain visible beside its output.

| Finding | Directly supported observation | Interpretation boundary |
| --- | --- | --- |
| LOOP-FACTORY-01 | Four `bl` calls target `0x1012d9734`, `0x1015644d4`, `0x101486414`, `0x101482718` | Callee behavior and prototypes unexamined |
| LOOP-FACTORY-02 | Before the first call, `w0` receives `0x78`; returned `x0` is retained in `x20` | Allocation is a hypothesis; the constant does not establish a musical value |
| LOOP-FACTORY-03 | After the second call, address values `0x106803d50` and `0x106803fc0` are stored through its result at offsets 0 and `0x58` | Table identity and semantic field meanings are unknown |
| LOOP-FACTORY-04 | The 32-bit word at retained pointer plus 8 is incremented; the retained pointer is passed to the fourth call and written through saved incoming `x8` | Reference counting and source-level return conventions remain hypotheses |

The full address locators are in the findings record. No exact matches for
these four callees or two stored addresses were found in the retained symbol
TSV. There is no inferred name to promote to a fact. Pseudocode omits parameters
for calls whose register inputs remain live, and its displayed parameter list
differs from metadata's recovered signature. Inspect instructions and callees
before relying on either type description. Empty provider warnings do not
establish complete recovery.

The follow-up selected run inspected `0x1015644d4` and `0x101486414`; the next
section records the result. An initialization write still needs a demonstrated
connection to serialized `LoopOn`, plus load/migration behavior, before it
supports a default rule. The P1 expectation matrix therefore remains unknown.

## Persistence packet after the callee follow-up

The [second findings revision](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/native-packets-findings-v2.json)
pins eleven v3 assembly, metadata and pseudocode artifacts, including exact
excerpts. The same target and selected no-analysis profile were used. This
revision adds evidence; it does not replace the first factory observations.

| Callee | Observed result | Interpretation and remaining gap |
| --- | --- | --- |
| [`0x1015644d4`](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x1015644d4/pseudocode.c) | Exported 76-byte body/19 instructions. Calls `0x10156e5e0`; writes two address values; writes a 16-bit zero at returned pointer plus `0x60`; stores a named default-controller pointer and a zero at `0x68`/`0x70`; calls `0x101486414`; returns the original incoming pointer | Consistent with boolean-related setup, supported by the displayed `ARemoteableBool`/`SDefaultController` symbol. Which bytes encode the serialized loop field remains unknown |
| [`0x101486414`](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x101486414/pseudocode.c) | Exported 116-byte body/29 instructions. Makes an indirect call through slot `0x170`, traverses entries, and conditionally writes an entry pointer to a computed destination | Setup/registration is plausible. The indirect return object's meaning, entry layout and relationship to the file reader/writer remain unresolved |

The zero store is corroborated by `strh wzr,[x0, #0x60]` at `0x1015644fc` in
[the actual assembly](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x1015644d4/assembly.txt).
It is not yet a `LoopOn=false` requirement: two bytes are cleared in an
unresolved layout, later setup/load code can alter state, and the input path
has not been joined to the schema field. The shipped fixture's stored false
value does not independently prove that join.

P1 is now a partial native packet with positive code evidence, concrete file
inputs, competing interpretations and an explicit missing connection. All
P1-A–F expected behavioral outcomes remain unknown. The next useful evidence
would identify the relevant field's reader/writer and state location, rather
than export more nearby setup functions without a discriminating question.

## Study P1 Loop enable persistence

**Question:** for a narrowly declared set format, how does the stored loop-enable
value affect the loaded state, and what value does saving produce? Start with
`LoopOn` because its candidate boolean meaning offers a smaller investigation
than tempo or loop bounds with unresolved units. That meaning still needs proof.

The minimum useful derivation joins five pieces: field-name/type registration;
the reader's lexical conversion and missing-field path; the receiving state;
the writer's extraction and encoding; and a supported external observation of
the resulting state. Schema declarations and a factory name supply only search
seeds. A generic boolean parser becomes relevant only after proving this field
uses it. Constructor initialization alone does not prove missing-field behavior,
since loading or migration may override it.

1. Resolve the transport and loop factories against the actual function inventory.
   Read their exported pseudocode and corroborate significant branches or calls
   with instructions/references where available.
2. Follow only calls, registration records and field-string references needed to
   identify the field's reader and writer. Record data-flow joins as observed
   edges or explicit hypotheses. Do not guess object layout from nearby fields.
3. Trace normal conversion, absent-element and absent-attribute paths, then one
   invalid token. Establish version dispatch before applying results to the older
   default fixture. If no relevant path is found, record which seeds were tried.
4. Build a candidate field contract only for resolved cases. Name the supported
   input format and externally readable output; avoid promising whole-ALS
   compatibility or byte-identical saves.

The proposed inputs for P1-A through P1-D have been constructed from the matching
default bytes; their [fixture manifest](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/fixtures-v1/manifest.json)
lists twelve cases, exact byte patches and XML/ALS digests. Each changes only the
selected element or adjacent insertion, preserving all bytes outside that patch
and the older fixture's root metadata. P1-A0 retains the original decoded XML
with deterministic recompression. P1-E/F remain workflow plans. XML parsing and
gzip round trips passed; none of the files has been submitted to Live, and all
reference behavioral expectations remain unknown.

The [retained preparation script](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/prepare_fixtures_v1.py)
was run as `python3 prepare_fixtures_v1.py` in its containing directory. It uses
Python's gzip writer with `mtime=0`, an empty filename and compression level 9;
tool versions and the script hash are in the source manifest. Repeating
compression in that process produced identical bytes. It refuses to overwrite
existing revisions. The [capture and fixture checksums](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/resource-fixture-checksums-v1.json)
cover 29 resource, fixture and manifest files totaling 2,996,096 bytes. Matching
XML syntax is not proof of Live acceptance, migration behavior or save fidelity.

| Case family | Controlled change | Expected behavior to derive |
| --- | --- | --- |
| P1-A | Original `false`; replace with `true` | Accepted token mapping and saved representation |
| P1-B | Delete `LoopOn`; separately delete its `Value` attribute | Default, inherited value or failure path; do not equate the two omissions |
| P1-C | `Value=""`, `TRUE`, `0`, `1`, `invalid` in separate cases | Accepted token set and rejection/coercion behavior |
| P1-D | Duplicate `LoopOn` with conflicting values; unknown adjacent field | Precedence, rejection and preservation behavior |
| P1-E | Change loop enable, save, reopen; repeat save | Persisted state and any normalization |
| P1-F | Change loop enable through a supported control, then undo/redo | Whether undo applies and its interaction with persisted state |

An optional bounded reference probe should discriminate the first material
ambiguity, such as whether a missing field preserves initialization or triggers
migration. Capture load outcome, independently observable loop-enable state and
saved XML. If observation requires an exposed API or GUI control, validate that
surface first. The probe's preconditions must name version, preferences and
external synchronization state. No original-side execution has been performed
by this preparation.

## Study T1 Start followed by stop

**Question:** from a stopped, non-recording document, what externally observable
state changes follow one Start request and one Stop request? Separate command
acceptance, requested playback state, effective playback and visible feedback.
A write that requests playback does not establish when the audio thread acts.

Begin with the two named callback wrappers. Resolve their actual branches and
any relevant update-event guard, then trace the state writes or downstream
requests. Follow their registration or callers until the input is connected to
an externally describable action. Stop at the first unresolved indirect call or
asynchronous boundary and state the missing proof. Nearby functions and symbol
names alone cannot supply an event-order diagram.

| Case family | Proposed precondition and action | Question to resolve |
| --- | --- | --- |
| T1-A | Stopped, then one Start; playing, then one Stop | Which state changes and position effects are supported? |
| T1-B | Start twice; Stop twice | Idempotence, restart or distinct second-action behavior |
| T1-C | Start immediately followed by Stop | Request ordering, cancellation and effective playback |
| T1-D | Loop disabled versus enabled, same position | Whether the selected state transition depends on looping |
| T1-E | Saved state before and after the sequence | Which changes persist, and which are transient? |
| T1-F | Close document with a pending request | Teardown scope and unresolved ownership boundary |

Keep external sync, Link, count-in, armed recording, tempo following, keyboard
modifiers and clip launching outside the first contract unless a traced branch
requires them. Document exclusions as preconditions rather than assume identical
behavior. Timing, audio output and GUI repaint claims require appropriate
observations; static call order cannot establish a real-time latency tolerance.
Check whether transport actions participate in undo instead of assuming they do.

## Transport wrapper findings

The selected v2 export retained assembly for the named Start and Stop callback
wrappers but rejected both bodies as incomplete/ambiguous under its acceptance
rule. The [wrapper findings](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/transport-wrapper-findings-v1.json)
pin both assembly/metadata pairs against the sealed run manifest. Profile and
target are unchanged from the first selected export.

| Seed | Observed instructions | Accepted result and next boundary |
| --- | --- | --- |
| `0x102770a58`, wrapper naming `OnStart` | Set `w1=1`, `w2=1`; branch at `0x102770a60` to `0x10276a7b0` | Failed pseudocode export: non-call transfer leaves recovered body; target semantics unresolved |
| `0x102770a64`, wrapper naming `OnStop` | Branch to `0x102767b70` | Same failure class; target semantics unresolved |

These are demonstrated static transfer targets. A forwarding/tail-transfer
interpretation is plausible, but the values' meanings and external
action-to-wrapper paths are not established. Neither excerpt proves a
playing-state change. The follow-up below inspected those two targets; it does
not erase the wrappers' failed export status. The
[second native lesson](learning/walkthroughs/transport-wrapper-boundary.md)
explains this boundary using the complete small assembly excerpts.

## Transport packet after the destination follow-up

V3 exported the Start-wrapper destination
[`0x10276a7b0`](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x10276a7b0/pseudocode.c)
(552-byte body, 138 instructions, 3,157-byte pseudocode). Stop's destination
[`0x102767b70`](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x102767b70/assembly.txt)
retained 75 instructions across 300 bytes but failed pseudocode acceptance:
computed transfers at `0x102767c60` and `0x102767c98` remain unresolved.
[Metadata](../../analysis/ableton-live-12.4.3/native-live-arm64-targeted-v3/functions/0x102767b70/metadata.json)
preserves that failure. The second findings revision pins these artifacts.

Both destinations contain a conditional direct call to `0x101a4abd8`:

| Path | Call instruction | Observed register values before the call |
| --- | --- | --- |
| Start-wrapper destination | `0x10276a8e8` | `w1=0x100500`, `w2=1`, `w3=0`, `x4` copied from saved incoming `x2` |
| Stop-wrapper destination | `0x102767be4` | `w1=0x100500`, `w2=0`, `w3=1`, `w4=0` |

Start's selected section is bypassed when the byte at incoming object plus
`0x8b0` is not one, or when bit zero of the result from `0x101a48488` is set.
Stop's path also tests that callee's result bit before the common call. This is
an observed shared code boundary with different argument patterns, not a
validated description of Play/Stop state or command flags. Both paths contain
other calls and conditional behavior, so the shared call cannot stand for the
whole operation.

Stop's two unresolved branches load their destinations from a pointer table
slot at `0x248`, then use `br x2` or `br x1`. Resolving the receiver and target is
required before claiming the full path. The common callee `0x101a4abd8` is the
highest-value next transport query once native analysis resumes; identifying
its state effect would distinguish a dispatch request from a direct state write.
No further native queries were issued by this study.

T1 is a partial native packet: two wrapper edges, a readable destination, a
shared guarded call and a precise computed-transfer boundary. External input
routing, meaningful state names, request ordering, effective playback, timing,
persistence and undo remain unresolved. None of the T1 case outcomes is a pass.

## Native contract assessment

The current evidence supports internal observations but no useful finite
external persistence or transport contract. P1 lacks a proven serialized-field
reader/writer/state connection; T1 lacks a complete external-action-to-observable
transition. Do not release the internal zero store as a default rule or the
argument differences as playback semantics.

The proposed first release should therefore use the roadmap's explicit
[MIDI fallback](native-decompilation-roadmap.md#default-first-handoff), subject
to its own reviewed requirements and fixtures. This is not a native-backed
release and does not complete the two native packets' evidence-review gate.
Keep these packets, candidate cases and unresolved connections active for the
next native analysis pass.

## Query budget and stopping conditions

The coordinator owns the active native session. Investigators read completed
exports and return exact queries for missing evidence; they do not open another
analysis session. First inspect the four primary seeds already in the pilot
queue or request them after inventory validation. For each study, allow one
round of at most eight additional directly relevant function dossiers and
bounded reference queries, then review what was resolved before expanding.
This is a semantic-investigation budget, not a restriction on systematic corpus
export. Do not label the study complete simply because the budget was consumed.

A successful packet records a supported path from selected input to observable
output, its branch conditions, evidence IDs/addresses/profile, and case outcomes
classified as statically derived, observed or unresolved. An inconclusive packet
records the last supported edge, competing explanations and the smallest next
query or probe. Two packets alone do not satisfy the phase's native evidence
review or handoff gate.

## Teaching and review deliverables

Write one walkthrough showing how a schema field led to native code and one
showing why a callback name did or did not explain a transport action. Use real
small excerpts linked to immutable exports; retain warnings and provisional
names. Explain in ordinary language where the evidence stops. Add demonstrated
relationships to the [program atlas](program-structure.md), labeling package
containment separately from code/data-flow relationships.

An independent reader should be able to locate the exact `LoopOn` observation,
explain why `false` in one bundled file is not proof of the runtime default,
follow a real wrapper into its resolved body, and identify a remaining boundary.
Before a handoff, an evidence reviewer must check every proposed expectation
against the retained path or observation. Recovered internals and these teaching
notes stay in the analyst workspace; only reviewed external contracts cross the
[handoff boundary](../workflows.md#release-a-handoff).

## Execution status

| Step | Status |
| --- | --- |
| Inspect canonical research and retained resources | Complete; source hashes and selected observations retained |
| Validate symbol seeds against TSV | Complete for eight entries; discovered-function validation pending |
| First selected native factory | Exported and inspected; four call edges retained under the no-analysis profile |
| Native reader/writer and handler tracing | Four follow-up destinations inspected: three exports and one computed-transfer failure; shared guarded transport call identified; field/action connections remain unresolved |
| Fixture byte retention and mutations | Complete for 12 P1-A–D inputs; both original resources match prior hashes; XML syntax/gzip round trips checked; reference acceptance unknown |
| Native walkthroughs, evidence review and contracts | Two native lessons written; reader review pending; behavioral contracts unresolved |
| Reference comparison | Unknown; no candidate or comparison run |

The [independent preparation review](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/independent-review-v1.json)
verified the resource hashes, locators, all twelve exact patches, gzip/XML checks
and retained manifests. It found no material issues. This review approves the
prepared static inputs and their provenance; behavioral expectations remain
unknown pending tracing or reference observations.

## Linker metadata cross-check

A [retained membership check](../../analysis/ableton-live-12.4.3/native-live-arm64-v1/behavior-preparation/function-start-membership-v1.json)
found all 24 selected-entry addresses in the independently reviewed
`LC_FUNCTION_STARTS` index. This corroborates their presence as declared start
locations, including the failed wrappers. It does not validate a recovered body,
resolve a computed transfer, or change any failed export to success. The
[source page](sources/ableton-live-12.4.3.md) owns the whole index's identity and
limits. No new native analysis or runtime call was required for this comparison.
