---
id: SPEC-PROJECT-MEDIA-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; documented Live 12 workflows with exact-build applicability unknown
---

# Sets, projects and media-reference workflows

## Scope and authority

FEAT-PERSISTENCE and FEAT-PROJECT-MANAGEMENT. User tasks: create/save and merge
Sets, use templates, inspect/repair/collect referenced assets, manage unused
files and create/restore project Packs. This is a partial documented-domain
contract. The current official Live 12 chapter was captured 2026-10-19; it names
no exact patch revision. **Every D12 behavioral clause retains exact 12.4.3
applicability U.** No original program, candidate, codec, project mutation or
file-operation acceptance scenario was executed.

[ALS container](als-container.md) owns the file envelope/version checks;
[Live Set structure](live-set-structure.md) owns its existing reader subset;
[browser index](browser-index.md) owns indexed content/sidecars and
[browser workflows](browser-workflows.md) owns search/navigation. This page owns
user-facing project/media lifecycle, not a replacement serializer or dependency
resolution algorithm. [Arrangement editing](arrangement-editing.md) owns edit
transactions still unknown there; generic Undo History presentation below does
not establish any particular edit's undo grouping or rollback behavior.

D12 = documented in the retained chapter, with target-build parity U. U = no
supported outcome. Requirement suffixes refer to this page's REQ prefix. Source
keys E1–E14 resolve to exact HTML anchors in the appendix. Concrete scenarios
are authored definitions, not original-side captures or ready-made ALS files.

## Preconditions and state

Use fresh, valid, editable Sets and explicitly identified test projects. Reset
preferences and open Set state between cases. Sources are readable unless a
case changes that property. Set names, active project, referenced logical asset,
missing/online status, selected dependency-location classes, template contents
and Undo History are separate observable state. Compare named state only;
never assume filename identity proves equal content.

Use copies of test-owned assets for replace/delete/collect operations. This is
a fixture isolation requirement, not a claimed Live safety feature. No broad
unchanged-file/hash/atomicity guarantee follows from a successful UI operation.
Runtime-dependent failures, overwrite prompts and partially completed writes
remain U unless a requirement explicitly says otherwise.

## Requirements

| Requirement ID | Preconditions/input | Observable documentary result | Source |
| --- | --- | --- | --- |
| REQ-PROJECT-MEDIA-001 | New/Open/Open Recent or browser Set open | Create or open the selected Set through the named command. | D12/E1 |
| REQ-PROJECT-MEDIA-002 | Save current Set; Save As; Save a Copy | Save current content; the latter commands support a different name/location. Active-document identity after Save a Copy remains U here. | D12/E1 |
| REQ-PROJECT-MEDIA-003 | Open Undo History for an editable Set | Actions appear newest first; selecting an earlier action undoes later actions, which become dimmed; selecting an undone action reapplies it and intervening earlier undone actions. | D12/E2 |
| REQ-PROJECT-MEDIA-004 | Close and reopen a Set | Undo History starts afresh; creating/opening is its initial non-undoable action. | D12/E2 |
| REQ-PROJECT-MEDIA-005 | Drag a source Set onto a track header/drop area | Reconstruct its tracks, Session/Arrangement clips, devices and automation, excluding source return tracks. Specific routing/ID/collision transformations U. | D12/E3 |
| REQ-PROJECT-MEDIA-006 | Unfold a source Set in browser | Expose individual tracks, nested groups, devices, grooves and Session clips for the documented selective import actions. | D12/E3 |
| REQ-PROJECT-MEDIA-007 | Drag selected Session clips into Current Project/user folder | Export a newly named Set containing that selection. Other retained content/defaults and file-reference transforms U. | D12/E4 |
| REQ-PROJECT-MEDIA-008 | Save current Set as default | New Sets use its configured state; a browser template can also be chosen as default. | D12/E5 |
| REQ-PROJECT-MEDIA-009 | Save Set as Template, then load it | List template in Templates/User Library; load its configuration as an untitled Set. | D12/E5 |
| REQ-PROJECT-MEDIA-010 | Manage Files → Manage Set → View Files | List referenced files and expandable usages; indicate missing/User Library/Project/external location. | D12/E6 |
| REQ-PROJECT-MEDIA-011 | Replace an entry with a readable new sample | Redirect every Set clip using that sample. For audio clips retain clip properties and retain Warp Markers when replacement length is at least original, discard when shorter. | D12/E6 |
| REQ-PROJECT-MEDIA-012 | Edit a referenced sample externally | Keep it offline while Edit is engaged; retain audio-clip Warp Markers only when sample length is unchanged. Non-sample Edit availability and external-editor failures U. | D12/E6 |
| REQ-PROJECT-MEDIA-013 | Save outside existing projects versus within one | Outside creates a new project; within an existing project shares that project. Save As alone does not collect external samples. | D12/E7 |
| REQ-PROJECT-MEDIA-014 | Open an older-major-version Set and try ordinary overwrite | Require Save As instead of overwriting it. Exact accepted versions remain owned by the container spec. | D12/E7 |
| REQ-PROJECT-MEDIA-015 | Referenced sample unavailable | Mark affected clip/instrument sample slot offline and substitute silence for that sample; effect/instrument tails and whole-mix silence are not implied. | D12/E8 |
| REQ-PROJECT-MEDIA-016 | Drop a readable candidate on a missing reference | Accept manual reassignment without proving it is the original missing file. Compatibility/type rejection and saved-path rules U. | D12/E9 |
| REQ-PROJECT-MEDIA-017 | Automatic search over explicitly enabled locations | No candidate: unresolved; one: accept; several: offer user selection via Hot-Swap. Matching/ranking/tie identity and search timing U. | D12/E10 |
| REQ-PROJECT-MEDIA-018 | Collect and Save selected external-location classes | Copy selected dependencies into project Samples or Presets and use project-contained references. Include files outside project, even those in Packs/User Library/other projects, as external. | D12/E11 |
| REQ-PROJECT-MEDIA-019 | Move/save a clip, preset or track from an open Set into a supported Places folder, with collection preference | Always copies; Never keeps original references; Ask offers Copy/Don't Copy/Cancel. Filename confirmation precedes dependent copying in the documented Ask/Copy path. Partial writes and cancel atomicity U. | D12/E12 |
| REQ-PROJECT-MEDIA-020 | Find unused project files | Judge use by that project's Sets/clips/presets, even when another project uses the file. Deletion can break those other references; no global safe-delete guarantee. | D12/E13 |
| REQ-PROJECT-MEDIA-021 | Create project Pack; install it later | Write an ALP without automatically collecting external files; restore the packed project folder on install. Original project remains available. Compression ratio/bytes/version safety U. | D12/E14 |
| REQ-PROJECT-MEDIA-022 | Malformed media/project, permission/disk/network failure, cancel or teardown | U: precise refusal/repair, diagnostics, overwrite decisions, partial output, transaction recovery, cleanup, undo grouping and stale references. | U |

## Timing and interactions

No file-operation deadlines, audio substitution latency, search completeness
bound, deterministic candidate ranking or total transaction order is specified.
Equal versus shorter replacement lengths are observable media-duration conditions;
no tolerance or rounding rule for almost-equal durations is invented. File-byte
interchange still requires the existing container/structure contracts and their
explicit gaps; these UI rules cannot approve arbitrary malformed ALS or ALP input.

Collecting and packing are distinct: a Pack's creation does not resolve omitted
external dependencies. A template is not a saved undo history. Changing every
reference to a sample can affect multiple clips; no per-clip replacement promise
is inferred. A stopped/cancelled operation need not imply rolled-back disk state.

## Acceptance cases

F1: fresh Set A, project P, two warped audio clips referencing valid PCM WAV X,
and compatible PCM WAV Y variants at the same sample rate. X has 100,000 frames;
Y variants have 80,000/100,000/120,000 frames. Give both clips distinguishable
nondefault Warp Markers and valid nondefault clip properties; record their
pre-operation marker/property state. Chosen loop/extents must fit even the shorter
replacement so this test does not rely on an unknown out-of-source clamp.
The [declarative fixture](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/fixtures.json)
defines mandatory nonempty marker/state controls. F2: source Set S with one audio,
one MIDI, one return and a nested group, distinguishable clips/devices/automation.
F3: projects P/Q with test asset X inside P but used by Q only; project-owned
and external samples from each selectable location class. Operations use copies.
Choose an undoable documentary action with an independently known transaction
boundary for history cases; this page does not define an edit's transaction.

| Case ID | Requirement | Kind | Action/setup | Documentary comparator / limit |
| --- | --- | --- | --- | --- |
| PMW-001 | 001 | Positive | Create A, then open named S. | Named current Set changes; content according to its existing format contract. |
| PMW-002 | 002 | Positive | Save A, then Save As to distinct test name. | Named destination receives saved Set; byte format out of this case. |
| PMW-003 | 002 | Boundary | Save a Copy to distinct destination. | New named copy exists; current identity U. |
| PMW-004 | 003 | History | Perform three known undoable actions; choose earliest history action. | Later actions dim/undo; newest-to-oldest ordering. |
| PMW-005 | 003 | History | Select a later dimmed action. | Relevant undone action sequence reapplied; edit grouping independently controlled. |
| PMW-006 | 004 | Teardown/reopen | Close/reopen saved A. | Fresh history; initial opening not undoable. |
| PMW-007 | 005 | Positive/negative | Drag S into target Set drop area. | Import non-return tracks and described content; source return excluded; remapping U. |
| PMW-008 | 006 | Selection | Unfold S/nested group and import one track, then one Session clip. | Only chosen imported object scope; merge remapping/extra context U. |
| PMW-009 | 007 | Positive | Export two selected Session clips to test user folder. | New named Set for selection; exact extra contents U. |
| PMW-010 | 008 | State | Save a distinguishable default, create new Set. | Configured default state represented; exact coverage of every device/plugin setting U. |
| PMW-011 | 009 | State | Save/load named template. | Templates listing and configured untitled instance. |
| PMW-012 | 010 | References | View A's X references and expand usage. | Listed reference shows both clip usages and location class. |
| PMW-013 | 011 | Equal-length boundary | Replace X with equal-length Y in reference list. | Both references redirect; Warp Markers retained. |
| PMW-014 | 011 | Longer boundary | Replace X with longer Y. | Both references redirect; Warp Markers retained. |
| PMW-015 | 011 | Shorter boundary | Replace X with shorter Y. | Warp Markers discarded; other applicable clip properties retained. |
| PMW-016 | 012 | External edit | Engage Edit; keep X duration unchanged. | Offline while engaged; markers retained on documented return; exact refresh timing U. |
| PMW-017 | 012 | Changed duration | External edit changes X duration. | Old Warp Markers not retained; replacement/default marker state U. |
| PMW-018 | 013 | Project boundary | Save fresh A outside projects, then Save As inside existing P. | New project versus shared project; no automatic external collection asserted. |
| PMW-019 | 014 | Version boundary | Open valid older-major Set, attempt overwrite. | Save As required; unsupported file versions remain separate. |
| PMW-020 | 015 | Missing input | Make X unavailable before loading A. | Affected usages offline; missing sample contributes silence; unrelated/tail output ungraded. |
| PMW-021 | 016 | Reassignment | Use different valid audio Y to repair missing X. | Manual reassignment accepted without original-identity requirement. |
| PMW-022 | 017 | No candidate | Search controlled empty folder only. | Missing reference unresolved. |
| PMW-023 | 017 | One candidate | Supply exactly one matching candidate by independently established search criteria. | Candidate accepted; matching algorithm outside comparator. |
| PMW-024 | 017 | Several candidates | Supply two matching candidates under same controlled criteria. | User candidate selection offered; ordering U. |
| PMW-025 | 018 | Collection | Select one external-location class, Collect and Save. | Selected dependencies copied/referenced within P; omitted classes not graded. |
| PMW-026 | 019 | Always/Never | Export sample-bearing preset under each preference. | Copy versus original-reference behavior; exact destination layout U. |
| PMW-027 | 019 | Ask/Copy | Confirm Copy, then confirm item filename. | Dependent copying follows filename confirmation. |
| PMW-028 | 019 | Cancellation | Choose Cancel at Ask prompt. | Export process quit; atomicity/partial filesystem state U. |
| PMW-029 | 020 | Cross-project boundary | Inspect X in P used only by Q. | X considered unused in P despite Q usage. |
| PMW-030 | 021 | Pack | Pack P containing uncollected external X; install to fresh location. | Packed project restored; external X not automatically collected; original P remains. |
| PMW-031 | 022 | Malformed | Corrupt ALS/ALP/media or ambiguous candidate identity. | U beyond existing narrower format refusals. |
| PMW-032 | 022 | Failure | Deny destination access or exhaust space during collect/save/pack. | U diagnostics, partial output, rollback and recovery. |
| PMW-033 | 022 | Cancellation | Cancel collect/pack/search/external editor mid-operation. | U accepted cancellation points and preserved state. |
| PMW-034 | 022 | Undo/teardown | Undo file replacement, or close/replace Set mid-write. | U undo grouping, save prompts, reference restoration and cleanup. |

All 34 cases are unexecuted. PMW-001–030 have bounded documented-domain criteria,
with additional ungraded limits as shown; PMW-031–034 are wholly ungraded. Exact
12.4.3 behavior is U throughout. There is no graded byte/audio equality test.

## Open questions

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns manual/build applicability. Narrower unresolved questions: copy versus
active-document identity; ID/routing/automation remapping during merge; nearly
equal replacement duration; search criteria/ranking; collection collisions and
location naming; missing plugin/Max dependencies; Save As/version migration;
ALP format/install boundaries; cancel/failure atomicity, rollback/recovery,
permission handling, undo grouping and external edit refresh/reclamation.

Audio/video/MIDI render/export settings, decoding cache/ASD behavior, codec
support, destructive clip editing, file-format bytes and filesystem-watch
latency remain separate unclosed F-07 obligations. The manual has relevant
sections; citing the whole chapter does not specify those omitted contracts.

## Analyst evidence appendix

Canonical [research owner](../research/project-media-workflows.md). Retained
[source metadata](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/source.json)
and [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/project-media/manual-files-2026-10-19.html)
identify the inspected source. These exact heading IDs, within those bytes,
own each documentary claim. Only text was inspected, not chapter illustrations.

| Key | HTML heading ID |
| --- | --- |
| E1 | `creating-opening-and-saving-sets` |
| E2 | `accessing-a-sets-undo-history` |
| E3 | `merging-sets` |
| E4 | `exporting-session-clips-as-new-sets` |
| E5 | `template-sets` |
| E6 | `viewing-and-changing-a-live-sets-file-references` |
| E7 | `projects-and-live-sets` |
| E8 | `locating-missing-files` |
| E9 | `manual-repair` |
| E10 | `automatic-repair` |
| E11 | `collecting-external-files` |
| E12 | `collect-files-on-export` |
| E13 | `finding-unused-files` |
| E14 | `packing-projects-into-packs` |

## Revision and handoff

Revision 1: 22 requirements and 34 acceptance scenarios, partial D12 contract
with exact-build and lifecycle unknowns. Independent review pending. No release.
