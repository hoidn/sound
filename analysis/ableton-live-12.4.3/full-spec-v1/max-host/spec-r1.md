---
id: SPEC-MAX-FOR-LIVE-HOSTING
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documentary Version 12 applicability unknown
---

# Max for Live host and template workflows

## Scope and authority

This partial F-05/F-08 draft owns documented Max editor selection, device/tool
editing and save/discovery/dependency workflows, plus individual documentary
roles and retained identity for five inventoried templates. It establishes no
arbitrary Max compatibility, full Live API/object/event protocol, AMXD codec,
patch algorithm, DSP/MIDI engine or complete host coverage. **D12** is captured
Version 12 prose; **every runtime clause has exact 12.4.3 applicability U**.
**Dpkg** is supplied-file identity only. U outcomes have null expectations and
comparators; no original application/patch/function, external editor or candidate
ran. This is an analyst draft, not a released implementation input.

[Coverage design](../research/full-live-specification-design.md) and
[research](../research/max-for-live-hosting.md) own method/source interpretation.
[Device racks](device-racks.md) owns common chains/presets, [browser](browser-workflows.md)
and [project/media](project-media-workflows.md) own their bounded file/discovery
operations, [automation](automation-envelopes.md) and [mapping](midi-user-mapping.md)
own their finite contracts. [MIDI editing/tools](midi-editing-tools.md) owns
Euclidean/VelocityShaper algorithms (REQ-MIDI-EDIT-043/038) and tool note editing;
this page adds no algorithmic or occupied-region oracle. [Clip View](clip-view-workflows.md)
owns shared panels. Twenty shipped Max devices in the
[inventory boundary](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/inventory-boundary.json) remain separately pending;
this host packet does not cover their controls, maps or sound. Third-party
[plug-in host](plugin-hosting.md) and [bundled host](bundled-device-hosting.md)
contracts do not imply Max ABI or arbitrary patch support.

## Input and acceptance boundaries

[Finite future setups](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/fixtures.json) require owned file copies,
explicit edition/Max version, application path and restart state, selected
instance/tool, save identity, dependencies, panel/focus and actual accepted
controls. No fixture patch or executable is supplied. The five AMXD copies are
immutable analyst sources: content unparsed, no executable use. Missing Max,
patch support, controls, dependencies or positive response leaves a case U.

Audio/MIDI/no-effect observations need active nonzero input/depth/route, unmuted
output and independently functioning paired positive baseline. A nominally
empty template is not assigned silence, pass-through, notes or audio from its
name. A public default audio-flow description is not a numerical unity/bit/phase
oracle. Save-confirmation UI does not prove rollback, identity, shared-instance
state or file atomicity beyond its documented predicate. Device freeze differs
from track Freeze; no private patch graph/process/API architecture is prescribed.

## Host requirements

All following rows are D12/target-U. Exact retained blocks include source HTML
lines and numbered heading context. The same-number MAX-H-NNN case provides
finite actions. Timing or signal obligations stay ungraded.

| Requirement | Documented contract and limits | Source blocks |
| --- | --- | --- |
| REQ-MAX-HOST-001 — Bundled setup context | The manual describes Max for Live as included with Suite and Standard plus the Max for Live add-on, without separate installation. Entitlement/activation/platform failure behavior is not specified. | `MAX:B006` |
| REQ-MAX-HOST-002 — Selected editor application | File & Folder settings can select a specific Max application path instead of bundled editor; changing path takes effect after Live restart, when opening editor launches chosen Max. | `MAX:B007`, `MAX:B008` |
| REQ-MAX-HOST-003 — Device browser surfaces | Core Library Max instruments/effects appear in Instruments, Audio Effects, MIDI Effects and Modulators; Max for Live label includes installed third-party/user devices and MIDI Tools. This is discovery UI, not proof every arbitrary AMXD works. | `MAX:B010`, `MAX:B011` |
| REQ-MAX-HOST-004 — Modulator role | Modulators are documented as controlling Live parameters with modulation signals. Specific mappings, ranges, parameter ownership, timing and device algorithms are not supplied. | `MAX:B010` |
| REQ-MAX-HOST-005 — Preset workflow | Max devices can have supplied presets and user-created/edited presets similar to ordinary device presets. Exact patch-definition versus parameter-state identity and sharing rules remain U. | `MAX:B012` |
| REQ-MAX-HOST-006 — Open device editor | For Max devices, Edit in Max in title-bar context or Show Options launches Max and opens selected device in editor/patcher. | `MAX:B016`, `MAX:B017` |
| REQ-MAX-HOST-007 — Developer edit button context | The manual distinguishes pre-12.2 device-title Edit button from current Edit in Max command. It documents -MaxForLiveDeveloperMode in Options.txt as restoring button functionality. Exact 12.4.3 option parsing/effective restart/default behavior is U. | `MAX:B018` |
| REQ-MAX-HOST-008 — Device Save instance scope | After editing a device, Max File Save updates all instances of the same device in the Set. Meaning of same-device identity versus preset copies, dirty state and atomicity is not established. | `MAX:B019` |
| REQ-MAX-HOST-009 — Device Save As confirmation | Device Save As opens confirmation asking whether changes apply only to edited preset or all instances. | `MAX:B019` |
| REQ-MAX-HOST-010 — Default device save folders | Max device default save location is the User Library folder appropriate to type, including Max Audio Effect and Max MIDI Effect. The chapter does not enumerate the exact folder name for every other type. | `MAX:B020` |
| REQ-MAX-HOST-011 — Separate AMXD references | Max devices are separate AMXD files rather than embedded in Set. Moving/renaming referenced AMXD can break path; File Manager offers location repair. Exact relocation/search/copy behavior remains U. | `MAX:B021` |
| REQ-MAX-HOST-012 — Existing tool editor route | An existing Max for Live MIDI Tool can be a starting point. Selected tool/template Edit button launches Max editor; this tool UI is distinct from current device-title Edit in Max. | `MAX:B025`, `MAX:B026` |
| REQ-MAX-HOST-013 — Tool saving | Max MIDI Tools are saved with patcher File Save or Save As. The device Save all-instances rule is not automatically transferred to tool selections. | `MAX:B027` |
| REQ-MAX-HOST-014 — Tool default folders | Documented default tool directories are ~/Music/Ableton/User Library/MIDI Tools/Max Transformations and .../Max Generators. User Library relocation/platform path resolution remains U. | `MAX:B028`, `MAX:B029`, `MAX:B030` |
| REQ-MAX-HOST-015 — Tool discovery locations | Tools stored in default folders or browser Places appear in corresponding tool dropdowns; elsewhere they are not found by Indexer and do not appear there. Timing, cache invalidation, recursion and ambiguous duplicate resolution are U. | `MAX:B031`, `MAX:B032` |
| REQ-MAX-HOST-016 — Dependencies and device freeze | Max devices may depend on samples, images or other patches. Device freezing packages files needed to use device; it is distinct from Freeze Track. Exact dependency discovery, supported file types, package grammar and portability are not specified. | `MAX:B035`, `MAX:B036`, `MAX:B037` |
| REQ-MAX-HOST-017 — Reference entry points | Max Help Reference opens built-in documentation with a Max for Live category; MIDI Tools guide is routed through category Guides. Availability/documentation versions and full API/object contracts are not captured here. | `MAX:B033`, `MAX:B039` |

## Five individually scoped templates

### Max Audio Effect

Surface `SURF-MAX-TEMPLATE-MAX-AUDIO-EFFECT`. **REQ-MAX-TEMPLATE-AE-ROLE (D12/target-U):** The named default Max Audio Effect is a starting point dragged from browser into Set for editing. The manual describes incoming chain audio being passed onward to subsequent devices. This documentary default role supplies no measured unity gain, bit identity, channel/latency/bypass law or arbitrary edited-patch behavior.

Evidence: `MAX:B014`, `MAX:B015`, `MAX:B016`, `MAX:B017`. **REQ-MAX-TEMPLATE-AE-FILE (Dpkg):** retained `max-audio-effect.amxd`, 4478 bytes, SHA-256 `ee9b5ced0f11ab098a24fd7b867a36b3980fda83119ab56c9e774cd62f2bf3e1`. [Template file ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json) retains original/copy paths and prefixes; no source content was parsed.

**REQ-MAX-TEMPLATE-AE-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.

### Max Instrument

Surface `SURF-MAX-TEMPLATE-MAX-INSTRUMENT`. **REQ-MAX-TEMPLATE-IN-ROLE (D12/target-U):** The named Max Instrument default can be dragged from browser into Set as a new editable Max device. This text does not specify its default note/audio behavior, voice model or channel mapping.

Evidence: `MAX:B015`, `MAX:B016`, `MAX:B017`. **REQ-MAX-TEMPLATE-IN-FILE (Dpkg):** retained `max-instrument.amxd`, 3800 bytes, SHA-256 `737dec1026106a33ec88f6fd3f246bae8b402dfa84f7ec633298c5f8b8d87d97`. [Template file ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json) retains original/copy paths and prefixes; no source content was parsed.

**REQ-MAX-TEMPLATE-IN-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.

### Max MIDI Effect

Surface `SURF-MAX-TEMPLATE-MAX-MIDI-EFFECT`. **REQ-MAX-TEMPLATE-ME-ROLE (D12/target-U):** The named Max MIDI Effect default can be dragged from browser into Set as a new editable Max device. Template presence/name supplies no MIDI pass-through, ordering, translation or output-message law.

Evidence: `MAX:B015`, `MAX:B016`, `MAX:B017`. **REQ-MAX-TEMPLATE-ME-FILE (Dpkg):** retained `max-midi-effect.amxd`, 3350 bytes, SHA-256 `1e3153f762eadbf967850fbd22a021dcab940035c3608a4f2edeeab03ac2efe2`. [Template file ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json) retains original/copy paths and prefixes; no source content was parsed.

**REQ-MAX-TEMPLATE-ME-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.

### Max MIDI Generator

Surface `SURF-MAX-TEMPLATE-MAX-MIDI-GENERATOR`. **REQ-MAX-TEMPLATE-GE-ROLE (D12/target-U):** Max MIDI Generator is the default tool starting point in Generative Tools panel/tab; selected template Edit opens patcher and Save/Save As saves tool. No default generated notes, randomness, seed or generation range is established.

Evidence: `MAX:B024`, `MAX:B026`, `MAX:B027`, `MAX:B028`, `MAX:B030`. **REQ-MAX-TEMPLATE-GE-FILE (Dpkg):** retained `max-midi-generator.amxd`, 3185 bytes, SHA-256 `8f8f6945b4b8864774cf29d34ae74c3826aa1ca4b5ff5dbc4980ddf96ed93c3c`. [Template file ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json) retains original/copy paths and prefixes; no source content was parsed.

**REQ-MAX-TEMPLATE-GE-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.

### Max MIDI Transformation

Surface `SURF-MAX-TEMPLATE-MAX-MIDI-TRANSFORMATION`. **REQ-MAX-TEMPLATE-TR-ROLE (D12/target-U):** Max MIDI Transformation is the default tool starting point in Transformation panel/tab; selected template Edit opens patcher and Save/Save As saves tool. No default note/expression transformation, pass-through or selection scope is established.

Evidence: `MAX:B024`, `MAX:B026`, `MAX:B027`, `MAX:B028`, `MAX:B029`. **REQ-MAX-TEMPLATE-TR-FILE (Dpkg):** retained `max-midi-transformation.amxd`, 3212 bytes, SHA-256 `3407d0f478ce625023494274827199f7a6d74077f0c8b8d9141ebc5fb83be014`. [Template file ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/template-files.json) retains original/copy paths and prefixes; no source content was parsed.

**REQ-MAX-TEMPLATE-TR-RUNTIME (U):** five concrete cases cover I/O, save/reopen/reference loss, malformed AMXD/dependency, cancel/undo and teardown/transport. No default behavior or lifecycle output is inferred from the template name or bytes.

## Required unknown host behavior

| Requirement | Required missing outcomes | Concrete U cases |
| --- | --- | --- |
| REQ-MAX-HOST-U-APP | Application selection/availability and editor coordination remain unknown. | `MAX-U-APP-LOSS`, `MAX-U-EDITOR-RACE` |
| REQ-MAX-HOST-U-SAVE | Save/save-as/preset/shared-reference transactions remain unknown beyond documented confirmation scope. | `MAX-U-SAVE-CANCEL`, `MAX-U-SAVE-FAIL` |
| REQ-MAX-HOST-U-DEPENDENCY | Dependency discovery, freeze/unfreeze and dependency-loss outcomes remain unknown. | `MAX-U-DEPENDENCY-LOSS`, `MAX-U-FREEZE-CANCEL` |
| REQ-MAX-HOST-U-TOOLS | Tool indexing and clip apply/select/editor interactions remain unknown. | `MAX-U-INDEX-BOUNDARY`, `MAX-U-TOOL-APPLY` |
| REQ-MAX-HOST-U-ENGINE | Host DSP/MIDI/clock/performance/API behavior remains unknown. | `MAX-U-ENGINE`, `MAX-U-API` |
| REQ-MAX-HOST-U-STATE | Automation/mapping/history/persistence and teardown ownership remain unknown. | `MAX-U-AUTOMATION`, `MAX-U-TEARDOWN` |

Cases retain invalid app path, lost/unwritable AMXD/User Library, same-device and
copy identity, Save As cancellation/overwrite, dependency source loss and freeze
interruption, duplicate/outside-location tool indexing, clip Apply/selection/undo,
rate/block/transport, automation/mapping and device/editor/Set teardown. Malformed
inputs use disposable truncated copies, never source evidence. These are required
unknowns, not inapplicable omissions. Missing prerequisites are not a pass.

## Case catalog and source limits

[Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/requirements.json) contain **38 clauses: 22 D12, 5 Dpkg,
11 U**. [64 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/cases.json) include 22 documentary proposals, 5 package
identity checks and 37 U lifecycle/runtime obligations. All 64 have
`executed:false`, `target_grade:U`, `expected:null` and `comparison:null`.
A separate documentary field proposes only source-supported named visible state;
signal/timing obligations have no documentary comparator. There are zero target
oracles or compatibility grades. Positive/negative/boundary cases accompany
malformed/cancel/save/undo/source-loss/transport/rate/teardown/automation/API gaps.
Compound cases remain bounded investigation recipes, not exhaustive closure.

The chapter's device Edit in Max versus pre-12.2 Edit button statement is scoped
to device-title controls. MIDI Tools keep their own Edit button context. They are
not asserted contradictory. Editor selection affects launch after restart but
supplies no supported Max-version matrix. Device Save updates same-device
instances as documented; tool Save propagation is left U. Default-location or
Places discovery needs known valid tool and indexing readiness; no immediate
refresh guarantee. Device freezing packages dependencies as documented, while
file-type closure, external objects, licenses, search paths and platform binaries
remain unsupported. No dependency-free, portable, sandboxed or security-isolation
claim follows. Full API protocol needs its own retained versioned sources.

## Analyst evidence appendix

Official [Max for Live chapter](https://www.ableton.com/en/live-manual/12/max-for-live/),
Version 12, captured 2026-10-19. [Source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/source.json) retains exact
UTC/URL/250,005-byte capture; HTML SHA-256
`2f771ab26d3e08d4c7df737fbf2a2f95e62cc501739ba65a4531de90d0de69dc`.
[42 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manual-blocks.json) retain paragraphs/headings, HTML lines
and full context for §§32–32.6, excluding sidebar/footer. [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manual-max-for-live-2026-10-19.html)
is immutable source and [normalized text](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manual-text.txt) navigation.
Figures were not inspected; source links to Max docs are not retained API evidence.

[Sources](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/sources.json) pin manual, inventory/TOC and five inventoried
AMXD template copies. [Inventory boundary](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/inventory-boundary.json)
contains 20 max-device, 2 max-midi-tool and 5 max-template records; twenty individual
patches were neither parsed nor executed, and no compatibility follows.
[Author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/manifest-author-r1.json) freezes exact payloads and
canonical snapshots. [Validation](../../analysis/ableton-live-12.4.3/full-spec-v1/max-host/validation-author-r1.json) checks
source/hash/catalog/link/whitespace scope only. These analysis links require
sanitization and review before any handoff. No profile/host family is complete.

## Revision and handoff

Revision1 is author-frozen for separate semantic review. No handoff, public
publication, installation or implementation workspace is created by this draft.
