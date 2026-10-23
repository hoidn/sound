---
id: SPEC-BROWSER-CONTENT-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version12 feature/service applicability U
---

# Browser content, tagging and service entrypoints

## Scope and canonical boundaries

This partial F-07/F-08 draft owns additional text-supported filter/tag/collection,
content view and service entrypoints. **D12** is retained current Version12 prose;
every exact12.4.3 feature/option/default/output remains U. It is not a release,
complete Browser/online-service/Push3 contract or compatibility result.
[Coverage design](../research/full-live-specification-design.md) governs closure;
[research](../research/browser-content-workflows.md) owns interpretation/questions.

[Browser Workflows](browser-workflows.md) retains ordinary word-search/clear/find,
history, color-membership, folder registration/missing-view, generic preview and
Session sample load. This page adds only distinct predicates and entrypoints.
[Browser Index](browser-index.md) and [browser-index-v1](../../handoff/browser-index-v1/README.md)
retain finite kind/sidecar/read/write/binding/label laws. UI tag edits supply no
new sidecar bytes or private index/model architecture. [Keyboard/navigation](keyboard-navigation.md)
owns general focus/arrows/global shortcuts; chapter-specific gestures need actual
Browser focus/layout/preferences, not universal dispatch.

[Project/media](project-media-workflows.md) retains Set import/save/template,
missing references, collect/export and project-Pack create/restore; this page's
downloadable content Pack views do not redefine that operation. [Media files](media-file-workflows.md)
owns eligible codecs/cache/ASD/Live Clips; [Clip View](clip-view-workflows.md) owns
source replacement and Clip View Show Similar Files042. [Settings](settings-learning-workflows.md)
018 owns default Library/Pack locations, dependent copying and Places visibility.
[Racks](device-racks.md), [Simpler](device-simpler.md), [synthesis instruments](synthesis-instruments.md),
[plug-in discovery](plugin-discovery.md), [tuning](tuning-systems.md),
[grooves](groove-workflows.md), [MIDI tools](midi-editing-tools.md) and
[routing/cue](routing-monitoring-latency.md) retain their bounded sound/file/control laws.
Folder names, sample metadata and remote listings do not broaden them.

Browser Push file entrypoints do not close Push3 Standalone/firmware/controller
or the149 controller-directory inventory. Cloud/Splice/Pack labels, marketing and
license information do not supply service codecs, accounts, legal rights or
entitlement behavior. Search with Sound and local Similarity Search are distinct.
No embedding, model, scoring, threshold, search ranking, RNG, numeric scale,
default, credential or private data structure is invented.

## Inputs and null outcomes

[Future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/fixtures.json) require independently valid owned eligible
content, completed indexing/analysis, actual capability/catalog/account/hardware,
known focus/key preferences and a paired working positive baseline. Unavailable
content/control/account/hardware is U, never a negative pass. Audible/reference
paths require valid nonzero source, active eligible processing, nonzero gain/amount
and nonmuted cue/return/output. Empty results do not establish failed indexing,
and a visible label does not establish a connected service.

All target expected/comparison fields are null, grade U and executed false.
Only named visible control/entry/selection/membership roles have documentary
proposals. Signal/timing/protocol/numeric/RNG/similarity/file/analysis outcomes
have null documentary expected/comparator and source_claim context only.
All compound branches and online/hardware prerequisites remain partial.
No Browser/runtime/native/candidate was run; no account/login/cloud/Splice,
download/upload/Pack installation/transfer/network service action occurred.
Public retained documentation only was reused; figures were not inspected.

## Documentary clauses

### REQ-BROWSER-CONTENT-001 — Browser sizing contexts

**D12/target-U.** Dragging Browser dividers resizes panels; dragging its bottom edge closes Info and the active Clip/Device View. Full-Height Browser instead expands while those views remain open. Geometry limits and focus restoration remain U.

Evidence: `BC-B012` (#working-with-the-browser, HTML302), `BC-B013` (#working-with-the-browser, HTML302).

### REQ-BROWSER-CONTENT-002 — Content columns and sorting entrypoints

**D12/target-U.** Name is always shown; Content Options offers extra columns and file-extension visibility. Headers can be reordered and clicked for ascending/descending sorting. Sort keys, Unicode comparison, missing values and ties remain U.

Evidence: `BC-B016` (#content-pane, HTML316), `BC-B017` (#content-pane, HTML330), `BC-B018` (#content-pane, HTML330), `BC-B019` (#content-pane, HTML330).

### REQ-BROWSER-CONTENT-003 — Tag-query entry and suggestions

**D12/target-U.** Typing # followed by a tag name exposes tag auto-complete suggestions. Ordinary word matching/clear/global-find behavior stays with Browser Workflows001..004; tag parser, matching, suggestion ranking and boolean algebra remain U.

Evidence: `BC-B023` (#search-bar, HTML344), `BC-B024` (#search-bar, HTML358).

### REQ-BROWSER-CONTENT-004 — Custom result-label editing

**D12/target-U.** Add Label saves a search/filter result label in Library. Its context menu removes a custom label; factory/custom labels offer rename and icon choice. Dynamic versus snapshot membership and durable storage are not established.

Evidence: `BC-B033` (#saving-search-results-as-custom-labels, HTML386), `BC-B034` (#saving-search-results-as-custom-labels, HTML400), `BC-B035` (#saving-search-results-as-custom-labels, HTML414), `BC-B036` (#saving-search-results-as-custom-labels, HTML414), `BC-B037` (#saving-search-results-as-custom-labels, HTML414), `BC-B053` (#filter-groups, HTML486).

### REQ-BROWSER-CONTENT-005 — Per-label filter presentation

**D12/target-U.** Filter View can be shown/hidden, with label-specific groups shown through its menu or hidden by group context. Enabled filter state is recalled between Library labels; Ctrl Windows/Cmd Mac permits multiple tags in a group. Reset Filter Groups to Default restores visible groups, not a new search algebra.

Evidence: `BC-B007` (#working-with-the-browser, HTML302), `BC-B046` (#filters-and-tags, HTML456), `BC-B048` (#filter-groups, HTML456), `BC-B049` (#filter-groups, HTML470), `BC-B050` (#filter-groups, HTML470), `BC-B051` (#filter-groups, HTML486), `BC-B052` (#filter-groups, HTML486).

### REQ-BROWSER-CONTENT-006 — Factory tag edit restrictions

**D12/target-U.** The chapter distinguishes factory/default tags and groups from user additions: factory-item default tags and default groups/tags cannot be removed or edited, while added user tags are allowed. Exact permissions, error presentation and serialization stay U or with Browser Index.

Evidence: `BC-B056` (#tags, HTML486), `BC-B057` (#tags, HTML486), `BC-B072` (#tag-editor, HTML562), `BC-B079` (#quick-tags, HTML604).

### REQ-BROWSER-CONTENT-007 — Automatic analysis and plug-in metadata tags

**D12/target-U.** Current documentation describes periodic sound analysis assigning a best-matching tag to user samples up to60 seconds, and VST3 metadata tags when a subcategory maps to a Live category. Analysis timing, duration-boundary admission, classification/model, category mapping and accuracy remain U; native index fields provide no algorithm.

Evidence: `BC-B058` (#tags, HTML486), `BC-B060` (#tags, HTML486).

### REQ-BROWSER-CONTENT-008 — Auto Tags controls

**D12/target-U.** Enable Auto Tags is offered in Filter View. Tag Editor can remove auto tags or change them to user tags. Source provenance conversion, future rescans, durability and classification remain U.

Evidence: `BC-B059` (#tags, HTML486).

### REQ-BROWSER-CONTENT-009 — Tag Editor assignment and custom creation

**D12/target-U.** Filter View opens Tag Editor; it shows selected-item tags, foldable groups and assigned-group emphasis. Checkbox edits can tag one or Shift-selected multiple files; Add Tag and Add Group create custom entries, with a group exposed in Filter View after one of its tags is assigned.

Evidence: `BC-B062` (#tag-editor, HTML486), `BC-B063` (#tag-editor, HTML486), `BC-B064` (#tag-editor, HTML502), `BC-B065` (#tag-editor, HTML518), `BC-B066` (#tag-editor, HTML530), `BC-B067` (#tag-editor, HTML530), `BC-B068` (#tag-editor, HTML540), `BC-B069` (#tag-editor, HTML550).

### REQ-BROWSER-CONTENT-010 — Nested and custom tag editing

**D12/target-U.** Add Subtag in creates a nested tag under a parent; Creator-group tags do not permit subtags. Parent tags fold/unfold; custom tags/groups offer rename/delete. Editor closes through X or its Filter View entry; default-item restrictions remain separate.

Evidence: `BC-B070` (#tag-editor, HTML550), `BC-B071` (#tag-editor, HTML550), `BC-B072` (#tag-editor, HTML562), `BC-B073` (#tag-editor, HTML562).

### REQ-BROWSER-CONTENT-011 — Quick Tags creation

**D12/target-U.** Quick Tags Add offers existing-tag auto-complete or Create new tag followed by parent/group selection. An unrecognized parent/group name offers creation of a parent tag or group. No arbitrary nesting, collision or text grammar is specified.

Evidence: `BC-B075` (#quick-tags, HTML562), `BC-B076` (#quick-tags, HTML576), `BC-B077` (#quick-tags, HTML576), `BC-B078` (#quick-tags, HTML590).

### REQ-BROWSER-CONTENT-012 — Quick Tags selection presentation

**D12/target-U.** Quick Tags shows assigned tags, with additions described in alphabetical order. Multi-selection shows the union and marks nonshared tags with an asterisk; selecting a tag shows its group in Status Bar. X removes user assignments, and Filter View can hide the section. Exact collation and saved visibility remain U.

Evidence: `BC-B076` (#quick-tags, HTML576), `BC-B079` (#quick-tags, HTML604), `BC-B080` (#quick-tags, HTML604), `BC-B081` (#quick-tags, HTML616), `BC-B082` (#quick-tags, HTML616).

### REQ-BROWSER-CONTENT-013 — Collection assignment entrypoints

**D12/target-U.** Selected items, including mixed types/folders or multiple items, can receive Collections colors through context or keys1..7;0 resets assignments. This is Browser-focused UI assignment, not a global shortcut or new sidecar color encoding. Existing collection-membership and sidecar owners remain authoritative.

Evidence: `BC-B084` (#collections, HTML632), `BC-B085` (#collections, HTML632), `BC-B086` (#collections, HTML632).

### REQ-BROWSER-CONTENT-014 — Collection item presentation

**D12/target-U.** Collection folders can unfold. Content-pane color icons represent assignments, with at most three displayed even when an item has more colors. Collection membership itself remains Browser Workflows006; no color palette or chosen-color truncation order is established.

Evidence: `BC-B087` (#collections, HTML632), `BC-B088` (#collections, HTML632).

### REQ-BROWSER-CONTENT-015 — Collection label name and visibility

**D12/target-U.** Collection labels support context rename or Browser-focused Ctrl/Cmd-R, and header Edit exposes Show/Hide Label with Done. Assigning a hidden previously unassigned color reveals its label; removing all assignments does not automatically hide a visible label.

Evidence: `BC-B089` (#collections, HTML646), `BC-B090` (#collections, HTML646), `BC-B091` (#collections, HTML668), `BC-B092` (#collections, HTML668).

### REQ-BROWSER-CONTENT-016 — Library label presentation

**D12/target-U.** Library presents type-oriented labels and header Edit/Done visibility selection. Their described contents are discovery roles, not a new extension-kind, plug-in admission, ranking or index algorithm. Source-described default visibility is not exact-target observation.

Evidence: `BC-B094` (#library, HTML668), `BC-B095` (#library, HTML668), `BC-B096` (#library, HTML668), `BC-B097` (#library, HTML668), `BC-B098` (#library, HTML668), `BC-B099` (#library, HTML668), `BC-B100` (#library, HTML668), `BC-B101` (#library, HTML668), `BC-B102` (#library, HTML668), `BC-B103` (#library, HTML668), `BC-B104` (#library, HTML668), `BC-B105` (#library, HTML668), `BC-B106` (#library, HTML668), `BC-B107` (#library, HTML668), `BC-B108` (#library, HTML668), `BC-B109` (#library, HTML668), `BC-B110` (#library, HTML688).

### REQ-BROWSER-CONTENT-017 — Places content entry roles

**D12/target-U.** Places exposes configured Packs, Splice, Cloud, Push, User Library, Current Project and user-folder entrypoints. Its actual labels depend on configuration; settings-owned Show Splice/Cloud/Push controls do not prove available services or hardware.

Evidence: `BC-B112` (#places, HTML688), `BC-B113` (#places, HTML688), `BC-B114` (#places, HTML688), `BC-B115` (#places, HTML688), `BC-B116` (#places, HTML688), `BC-B117` (#places, HTML688), `BC-B118` (#places, HTML688), `BC-B119` (#places, HTML688), `BC-B120` (#places, HTML688), `BC-B121` (#places, HTML688).

### REQ-BROWSER-CONTENT-018 — Installed Pack presentation

**D12/target-U.** Installed Packs appear as expandable folders under Packs, with their presets/samples/Live Clips also exposed in appropriate Library labels. This is a known installed-catalog view, not an ALP codec, install transaction or universal content-admission law.

Evidence: `BC-B123` (#downloading-and-installing-packs-in-the-browser, HTML688), `BC-B124` (#downloading-and-installing-packs-in-the-browser, HTML688).

### REQ-BROWSER-CONTENT-019 — Pack updates and available catalog

**D12/target-U.** Packs Updates exposes available updates for installed Packs; Available Packs exposes owned uninstalled Packs. Ownership/catalog validity, refresh ordering, stale state and entitlement protocol remain U.

Evidence: `BC-B125` (#downloading-and-installing-packs-in-the-browser, HTML702), `BC-B126` (#downloading-and-installing-packs-in-the-browser, HTML716).

### REQ-BROWSER-CONTENT-020 — Pack download controls

**D12/target-U.** The source describes download/progress, pause/resume/cancel and corresponding context commands, including selected multiple Packs. These are workflow roles only; bytes, authentication, queue order, retry, progress scale, cancellation and partial-file outcomes remain U.

Evidence: `BC-B127` (#downloading-and-installing-packs-in-the-browser, HTML730), `BC-B128` (#downloading-and-installing-packs-in-the-browser, HTML742), `BC-B129` (#downloading-and-installing-packs-in-the-browser, HTML754), `BC-B130` (#downloading-and-installing-packs-in-the-browser, HTML754), `BC-B131` (#downloading-and-installing-packs-in-the-browser, HTML768).

### REQ-BROWSER-CONTENT-021 — Pack install and delete roles

**D12/target-U.** After download the source offers Install with a progress dialog. Installed Pack context/Delete removes it and makes it available again. This is distinct from project-Pack creation/restore under Project Media021; atomicity, dependencies, rights, deletion extent and service refresh remain U.

Evidence: `BC-B130` (#downloading-and-installing-packs-in-the-browser, HTML754), `BC-B132` (#downloading-and-installing-packs-in-the-browser, HTML768), `BC-B133` (#downloading-and-installing-packs-in-the-browser, HTML780), `BC-B135` (#downloading-and-installing-packs-in-the-browser, HTML796).

### REQ-BROWSER-CONTENT-022 — Pack size and downloadable visibility

**D12/target-U.** Content Options can expose Pack size in Updates/Available Packs. Library settings Show Downloadable Packs hides/shows those sections. Size units/accuracy, capacity prediction and default visibility are not new numerical laws.

Evidence: `BC-B134` (#downloading-and-installing-packs-in-the-browser, HTML780), `BC-B136` (#downloading-and-installing-packs-in-the-browser, HTML796).

### REQ-BROWSER-CONTENT-023 — Pack Info entrypoints

**D12/target-U.** Installed Packs can expose Show Pack Info, and Help Pack Overview opens installed Pack Info pages. Content may include creator/summary/tutorial; the Core Library is documented without a Pack Info page. No external tutorial or content decoder is specified.

Evidence: `BC-B138` (#pack-info, HTML812), `BC-B139` (#pack-info, HTML824).

### REQ-BROWSER-CONTENT-024 — Splice Home and connection prerequisite

**D12/target-U.** The Splice label Home exposes navigation/search, Search with Sound and category entrypoints, with login/signup entries. Viewing its content requires an active Internet connection. Settings-owned label visibility and account/service availability remain distinct.

Evidence: `BC-B142` (#splice, HTML838), `BC-B143` (#splice, HTML838), `BC-B144` (#splice, HTML838), `BC-B145` (#splice, HTML854).

### REQ-BROWSER-CONTENT-025 — Splice device-confirmation login role

**D12/target-U.** Login/Try free opens an OS browser for Splice device confirmation and then account entry; the source describes matching confirmation codes in browser and Live. This supplies no credential, token, code-generation, security, entitlement or login-success law.

Evidence: `BC-B147` (#logging-into-splice, HTML854), `BC-B148` (#logging-into-splice, HTML868).

### REQ-BROWSER-CONTENT-026 — Splice account-dependent capabilities

**D12/target-U.** The source distinguishes unauthenticated browse/preview from logged-in Set insertion, library saving and Search with Sound. Logged-in Home exposes Library and rearranged browse/search areas. Free/paid catalog contents, counts, rights and subscription behavior remain unknown.

Evidence: `BC-B147` (#logging-into-splice, HTML854), `BC-B149` (#logging-into-splice, HTML882), `BC-B155` (#searching-for-splice-samples, HTML922).

### REQ-BROWSER-CONTENT-027 — Splice search and result controls

**D12/target-U.** Splice has its own category/query suggestions, Samples/Packs view, tag/filter expansion and sorting options including Random/shuffle. Selected category scopes subsequent text search. Exact result matching, ranking, RNG, counts and history retention remain U; native Browser matching is not borrowed.

Evidence: `BC-B151` (#searching-for-splice-samples, HTML896), `BC-B152` (#searching-for-splice-samples, HTML908), `BC-B153` (#searching-for-splice-samples, HTML922), `BC-B154` (#searching-for-splice-samples, HTML922), `BC-B156` (#searching-for-splice-samples, HTML936), `BC-B159` (#working-with-splice-samples, HTML964), `BC-B160` (#working-with-splice-samples, HTML964).

### REQ-BROWSER-CONTENT-028 — Splice Search with Sound

**D12/target-U.** Logged-in Search with Sound accepts a dragged clip or captured time selection; the source describes compatible results and reference replay/replacement/removal. Its reported50-result list is source context, not a target count or quality oracle. Model, upload, scoring, rights and rendering remain U.

Evidence: `BC-B147` (#logging-into-splice, HTML854), `BC-B157` (#searching-for-splice-samples, HTML950).

### REQ-BROWSER-CONTENT-029 — Splice sample-row entrypoints

**D12/target-U.** Sample rows expose pack navigation, sample-type/name/tags and context actions for Likes/Collections or pack view. Hover/selection can expose Like and expanded pane shows Time/Key/BPM columns. Display metadata does not establish audio analysis, source type or stored service identity.

Evidence: `BC-B161` (#working-with-splice-samples, HTML976), `BC-B165` (#working-with-splice-samples, HTML976), `BC-B166` (#working-with-splice-samples, HTML976).

### REQ-BROWSER-CONTENT-030 — Splice preview settings

**D12/target-U.** Splice preview has its own play/name entry, loop/timestretch/original-tempo, selected-key/Live-scale and loudness options. Source defaults and preview synchronization supply no waveform, gain, pitch, scale, render or timing law; native Browser Preview remains a separate owner.

Evidence: `BC-B162` (#working-with-splice-samples, HTML976), `BC-B163` (#working-with-splice-samples, HTML976), `BC-B164` (#working-with-splice-samples, HTML976).

### REQ-BROWSER-CONTENT-031 — Splice import Warp context

**D12/target-U.** Splice samples have service-specific drag/double-click/Enter/device destinations. The source describes Complex Warp overriding the ordinary default for clips using Splice samples; this is unverified source context, not a new Warp algorithm, decode result or guaranteed preview identity.

Evidence: `BC-B167` (#working-with-splice-samples, HTML994), `BC-B168` (#working-with-splice-samples, HTML994).

### REQ-BROWSER-CONTENT-032 — Splice sample registration and location

**D12/target-U.** The source describes Set insertion as licensing/registering a sample in the Splice library and storing downloads under User Library/Samples/Splice, Current Project/Samples/Splice or Custom Folder. These are source workflow/location roles, not a legal-rights conclusion, default-build promise, file transaction or service codec.

Evidence: `BC-B169` (#working-with-splice-samples, HTML994), `BC-B170` (#working-with-splice-samples, HTML994), `BC-B171` (#working-with-splice-samples, HTML994), `BC-B172` (#working-with-splice-samples, HTML994), `BC-B173` (#working-with-splice-samples, HTML994).

### REQ-BROWSER-CONTENT-033 — Splice Library and Collections controls

**D12/target-U.** Splice Library presents Likes, Collections and previously loaded/downloaded samples. Its Collections page/menu offers creation, name/description edit, private/share-link and delete controls. This is separate from Browser color Collections; publication, privacy enforcement and saved server state remain U.

Evidence: `BC-B175` (#splice-library, HTML1010), `BC-B176` (#splice-library, HTML1024).

### REQ-BROWSER-CONTENT-034 — Splice Settings information routes

**D12/target-U.** Splice Settings offers subscription/display, usage-log download, certified-license information, Knowledge Base/feedback and logged-out Login entrypoints. No subscription, usage-log format, legal validity, support service or credential behavior is specified.

Evidence: `BC-B178` (#splice-settings, HTML1024), `BC-B179` (#splice-settings, HTML1024).

### REQ-BROWSER-CONTENT-035 — Ableton Cloud authorization entry

**D12/target-U.** Cloud label offers a Sign In browser route to authorize Ableton Cloud, after which synced Move/Note Sets appear. The published up-to-eight Set description is source context, not an exact-target quota, sync protocol, account entitlement or version-compatibility promise.

Evidence: `BC-B181` (#using-ableton-cloud, HTML1038), `BC-B182` (#using-ableton-cloud, HTML1038), `BC-B183` (#using-ableton-cloud, HTML1052).

### REQ-BROWSER-CONTENT-036 — Cloud assets and direction boundary

**D12/target-U.** Synced Set assets require an accessible User Library; ABL Assets stores Move/Note assets. The chapter describes Move/Note-to-Live sync rather than Live-to-source and recommends Collect All and Save for developed Sets. Existing project/media collection and missing-reference owners retain their laws.

Evidence: `BC-B184` (#using-ableton-cloud, HTML1066), `BC-B185` (#using-ableton-cloud, HTML1066), `BC-B205` (#abl-assets, HTML1138).

### REQ-BROWSER-CONTENT-037 — Push3 standalone pairing entry

**D12/target-U.** Browser Push transfer requires Push3 Standalone and the same Wi-Fi network. Named-device selection/Connect precedes a code displayed on Push and entered in Live. The six-digit description is not a wire or pairing-code algorithm; Push1/2/controller mode cannot substitute.

Evidence: `BC-B189` (#transferring-files-from-push-3-in-standalone-mode, HTML1082), `BC-B190` (#transferring-files-from-push-3-in-standalone-mode, HTML1096).

### REQ-BROWSER-CONTENT-038 — Paired Push file-view controls

**D12/target-U.** After successful pairing, saved Standalone Project folders and Push User Library appear. Switching away/back refreshes the list; Push-label Disconnect unpairs. These are Browser file-view entrypoints, not file-transfer integrity, discovery timing or Push3 standalone/controller compatibility.

Evidence: `BC-B191` (#transferring-files-from-push-3-in-standalone-mode, HTML1096), `BC-B192` (#transferring-files-from-push-3-in-standalone-mode, HTML1108), `BC-B193` (#transferring-files-from-push-3-in-standalone-mode, HTML1108).

### REQ-BROWSER-CONTENT-039 — Push continuity prerequisites

**D12/target-U.** The chapter describes Standalone Set transfer/open on computer and transfer back using native devices, frozen plug-in tracks and collected Project samples. These are prerequisites/guidance, not an arbitrary Set/device codec, plugin parity, successful transfer or full Push3 contract.

Evidence: `BC-B188` (#transferring-files-from-push-3-in-standalone-mode, HTML1082).

### REQ-BROWSER-CONTENT-040 — User Library folder entry roles

**D12/target-U.** User Library exposes user-saved content and custom folders; source folder roles include ABL Assets, Chord Banks, Clips, Defaults, Grooves, Presets, Samples and Templates. Existing owners retain save/default/Stacks/groove/media/template and dependent-copy semantics; folder names do not establish codecs or constructor contents.

Evidence: `BC-B197` (#user-library, HTML1124), `BC-B202` (#user-library, HTML1124), `BC-B203` (#user-library, HTML1138), `BC-B205` (#abl-assets, HTML1138), `BC-B207` (#chord-banks, HTML1138), `BC-B209` (#clips-folder, HTML1138), `BC-B210` (#clips-folder, HTML1138), `BC-B211` (#clips-folder, HTML1138), `BC-B213` (#defaults-folder, HTML1138), `BC-B217` (#grooves-folder, HTML1138), `BC-B218` (#grooves-folder, HTML1138), `BC-B221` (#presets-folder, HTML1138), `BC-B222` (#presets-folder, HTML1138), `BC-B225` (#samples-folder, HTML1138), `BC-B226` (#samples-folder, HTML1138), `BC-B228` (#templates-folder, HTML1138).

### REQ-BROWSER-CONTENT-041 — User Library manager and Project reveal

**D12/target-U.** File Manage Files then Manage User Library opens that Library overview; Current Project context Show in Explorer/Finder reveals its folder. Project Media retains Set file management and reference operations, and Settings retains location selection.

Evidence: `BC-B231` (#managing-files-in-the-user-library, HTML1138), `BC-B239` (#current-project, HTML1178).

### REQ-BROWSER-CONTENT-042 — Current Project Backup presentation

**D12/target-U.** The chapter describes a Backup folder after repeated saves, timestamped prior Sets and bounded retention with old backups moved to trash; unsaved Sets use a temporary Project without Backup. Its twice-saved/last-ten wording remains source context, not a new recovery, retention-timing, filesystem or restore law.

Evidence: `BC-B233` (#current-project, HTML1150), `BC-B234` (#current-project, HTML1164), `BC-B235` (#current-project, HTML1164), `BC-B236` (#current-project, HTML1178), `BC-B237` (#current-project, HTML1178), `BC-B238` (#current-project, HTML1178).

### REQ-BROWSER-CONTENT-043 — Folder scan, locate and removal entrypoints

**D12/target-U.** A Places scan has a spinning progress indicator. For a registered folder, Locate Folder and Remove from Sidebar are offered; removal also applies to an available folder. Existing Browser Workflows007/008 owns nonrelocating registration and dimmed unavailable entries; retry/index timing and deletion effects remain U.

Evidence: `BC-B243` (#user-folders, HTML1178), `BC-B244` (#user-folders, HTML1188), `BC-B245` (#user-folders, HTML1188), `BC-B246` (#user-folders, HTML1188), `BC-B247` (#user-folders, HTML1188).

### REQ-BROWSER-CONTENT-044 — Multi-folder expansion modifier

**D12/target-U.** Opening another folder normally closes previously open folders; Ctrl Windows/Cmd Mac while opening overrides that behavior. Generic arrows/focus remain Keyboard Navigation-owned; selection, layout/IME, hidden folders and persistence require their own contexts.

Evidence: `BC-B252` (#navigating-in-the-browser, HTML1188).

### REQ-BROWSER-CONTENT-045 — Native preview Raw and scrubbing context

**D12/target-U.** Beyond existing generic preview, the chapter describes waveform scrubbing except unwarped saved clips, Raw original-tempo/unlooped versus non-Raw next-bar/looped preview, and no scrubbing in Raw. Cue/routing owns output selection; all sound, loop, onset and tempo algorithms remain U.

Evidence: `BC-B258` (#previewing-files, HTML1202), `BC-B259` (#previewing-files, HTML1216), `BC-B260` (#previewing-files, HTML1216), `BC-B261` (#previewing-files, HTML1216), `BC-B262` (#previewing-files, HTML1226).

### REQ-BROWSER-CONTENT-046 — Explicit preview gesture without toggle

**D12/target-U.** Shift-Enter or right arrow on a selected eligible Browser item can request preview even with Preview toggle off. Existing Browser Workflows009 owns generic preview; focus conflict, actual sound and cancellation/timing remain U.

Evidence: `BC-B257` (#previewing-files, HTML1202).

### REQ-BROWSER-CONTENT-047 — Browser Similarity Search entry

**D12/target-U.** Compatible selected Browser files offer Show Similar Files icon/context and Ctrl-Shift-F Windows/Cmd-Shift-F Mac entry. This owns Browser entrypoints only; Clip View042 retains its corresponding entry and sample-file management.

Evidence: `SIM-B003` (#sound-similarity, HTML338), `SIM-B004` (#sound-similarity, HTML350).

### REQ-BROWSER-CONTENT-048 — Similarity source and ranking role

**D12/target-U.** Concepts describes comparing a reference against Core/User Library samples up to60 seconds, instrument/drum presets, then listing results from most to least similar. Similar Sample Swapping names Drum Rack, Simpler and Drum Sampler targets. No embedding/model, scoring, threshold, exact result/order, boundary admission or replacement algorithm is supplied.

Evidence: `SIM-B002` (#sound-similarity, HTML338), `SIM-B004` (#sound-similarity, HTML350).

### REQ-BROWSER-CONTENT-049 — Similarity background-analysis status

**D12/target-U.** The Concepts source says similarity needs analysis, with new-user-file background work reported in Status Bar and a Pause control; Core Library is described as pre-analyzed. This clause owns status/Pause affordances, not a scan trigger, completion deadline, resume law, index lifecycle or generated features.

Evidence: `SIM-B006` (#sound-similarity, HTML364).

### REQ-BROWSER-CONTENT-050 — Similarity custom-label reference presentation

**D12/target-U.** For a custom User Label saved from Similarity Search results, the reference sound is shown at the top. General custom-label editing stays above; reference identity is distinct from any numerical similarity rank or successful sample replacement.

Evidence: `SIM-B005` (#sound-similarity, HTML364).

### REQ-BROWSER-CONTENT-U-QUERY — Query, tags and result algebra

**U/target-U.** Tag/query grammar, boolean combination, collation/Unicode/IME, hierarchy/sort ties, filter counts, dynamic label refresh and index-to-UI result identity remain unknown.

### REQ-BROWSER-CONTENT-U-ANALYSIS — Automatic classification and similarity algorithms

**U/target-U.** Sound-analysis eligibility,60-second boundaries, models/features/scoring, periodic scheduling, CPU behavior, rankings/thresholds/RNG and swap sound/state outcomes remain unknown.

### REQ-BROWSER-CONTENT-U-SERVICE — Accounts, catalogs and legal/service boundaries

**U/target-U.** Online capability, credentials/tokens/device confirmation, free/paid entitlements/catalogs/quotas, sample rights, logs/licenses, privacy/sharing, availability and server protocols remain unknown. No legal interpretation follows from marketing or registration prose.

### REQ-BROWSER-CONTENT-U-TRANSFER — Cloud and Push file identity

**U/target-U.** Cloud/Push versions, pairing/discovery, permissions, codecs, dependency/device portability, synchronization/conflict order, partial copies and direction/capacity limits remain unknown; no Push3 standalone or controller profile is completed.

### REQ-BROWSER-CONTENT-U-STORAGE — Content transactions and saved state

**U/target-U.** Pack install/update/delete, Library reconfiguration, backup retention, downloads/paths/collisions, tagging side effects, Undo/cancel, saved browser state and migration remain unknown beyond existing finite owners.

### REQ-BROWSER-CONTENT-U-LIFECYCLE — Input admission and cross-cutting lifecycle

**U/target-U.** Malformed/unavailable content, focus/preferences, unsupported controls, transport/automation/rate changes, source loss, concurrency and teardown retain null outcomes; missing capability or positive input is never a negative pass.

## Finite cases and open obligations

[71 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/cases.json) cover56 requirements (50 D12/6 U).
No future recipe is a result or exhaustive feature/profile coverage.

| Case | Requirement | Kind / finite action |
| --- | --- | --- |
| BC-001 | REQ-BROWSER-CONTENT-001 | control: With Info and Clip View explicitly open, resize a divider/bottom edge, then restore and choose Full-Height Browser. Repeat Device View separately; inspect named visibility only, no pixel tolerance. |
| BC-002 | REQ-BROWSER-CONTENT-002 | control: Use owned entries with known distinct names/metadata; show an offered extra column, move its header, toggle sort direction and extensions. Inspect controls/order choice, without a new exact result-ranking comparator. |
| BC-003 | REQ-BROWSER-CONTENT-003 | control: With independently known assigned custom tags and completed indexing, type # plus a partial known tag and choose an offered suggestion. Retain query/selection and compare an unassigned tag only as an unknown result probe. |
| BC-004 | REQ-BROWSER-CONTENT-004 | control: After a productive known search/filter baseline, Add Label, revisit it, rename/change its offered icon and remove the owned custom label on separate copies. Inspect label identity only; membership refresh/save/restart remains U. |
| BC-005 | REQ-BROWSER-CONTENT-005 | control: Use two labels with known available groups and positive content; vary visible groups and Ctrl/Cmd-selected tags, switch labels/back, then reset group visibility. Retain result-bar count as display context; exact result sets/count arithmetic remain U. |
| BC-006 | REQ-BROWSER-CONTENT-006 | control: Use an independently identified unmodified factory item plus an owned custom tag; inspect offered edit/removal commands and add the custom tag separately. Compare custom-only item; do not infer write protection from a failed source/index baseline. |
| BC-007 | REQ-BROWSER-CONTENT-007 | analysis: Use independently valid owned nonzero samples of retained duration and a known metadata-bearing plug-in only if separately available. Establish completed positive analysis/indexing context before observing tags; no deadline, exact classification or subcategory transform is predicted. |
| BC-008 | REQ-BROWSER-CONTENT-008 | control: With an independently retained actual auto-tag assignment and active index, inspect Enable Auto Tags and the offered editor removal/user-conversion routes in reset copies. Missing analyzed tags remain an unmet prerequisite, not an empty-result pass. |
| BC-009 | REQ-BROWSER-CONTENT-009 | control: Use two owned indexed files with different known tags, open editor, fold/unfold, assign a tag to one then Shift-select both. Create an owned group/tag and assign it; inspect entries and group visibility, not sidecar bytes or transaction grouping. |
| BC-010 | REQ-BROWSER-CONTENT-010 | control: Create an owned parent/subtag, fold it, rename/delete custom entries on reset copies and inspect a Creator tag without presuming a particular disabled/hidden presentation. Close/reopen editor; deletion cascade and cancellation remain U. |
| BC-011 | REQ-BROWSER-CONTENT-011 | control: Select an owned tagged file, add an existing offered tag, then type a distinct new tag and choose a known parent. Separately use an unrecognized parent/group name and inspect the offered creation choice; invalid/collision outcomes remain U. |
| BC-012 | REQ-BROWSER-CONTENT-012 | control: Use two indexed owned items with shared tag A and distinct B/C; select one then both, inspect shared/nonshared marks, select a tag for group status, remove an owned assignment and toggle section visibility. No Unicode/tie order or serialization oracle. |
| BC-013 | REQ-BROWSER-CONTENT-013 | control: With Browser focus, declared key/layout/preferences and two owned different-type entries, assign via context then an offered number key in reset copies; reset with0. Inspect assignment presentation; do not reinterpret released sidecar values or global dispatch. |
| BC-014 | REQ-BROWSER-CONTENT-014 | control: Use an owned collection folder and item with independently confirmed multiple assignments; unfold the folder and inspect assignment icons versus retained actual assignments. Do not infer omitted assignments from icon count or exact pixels. |
| BC-015 | REQ-BROWSER-CONTENT-015 | control: On owned assignments rename a label, explicitly hide an unassigned color, assign it to an indexed item and inspect visibility; remove that assignment separately. Retain prior hidden/visible state and key focus; no factory-default inference. |
| BC-016 | REQ-BROWSER-CONTENT-016 | control: With an independently known positive local catalog, inspect offered Library labels, hide/show one via Edit/Done and revisit. Existing Browser Index and device/media owners determine content admission; missing unavailable products are not a negative compatibility result. |
| BC-017 | REQ-BROWSER-CONTENT-017 | control: Retain actual configured local Library/Project/folders and independently available service/hardware capability. Inspect corresponding Places entries without enabling accounts or transferring files; label absence alone is not service failure. |
| BC-018 | REQ-BROWSER-CONTENT-018 | control: Use a separately retained valid installed test Pack/catalog and known eligible contents; expand its folder and inspect offered Library entries. No Pack is downloaded/installed here; existing import/format owners remain prerequisites. |
| BC-019 | REQ-BROWSER-CONTENT-019 | control: Only with independently valid authorized account/catalog snapshots, inspect known installed-update and owned-uninstalled entries separately. An offline or unavailable account/catalog is inconclusive, not proof that no update/Pack exists. |
| BC-020 | REQ-BROWSER-CONTENT-020 | protocol: For separately authorized future service tests only, require a known permitted Pack/catalog and working positive download baseline; retain offered start/pause/resume/cancel states for one then two selections. No service request or download is performed by this packet. |
| BC-021 | REQ-BROWSER-CONTENT-021 | file: Future authorized disposable Pack copy and separately validated completed download/install baseline required. Retain offered install/delete and catalog states without performing them here; project references, disk effects and cancellation are separate unknowns. |
| BC-022 | REQ-BROWSER-CONTENT-022 | control: With a valid known Pack catalog inspect the size-column option and Show Downloadable Packs on/off. Compare section/control presence only; no byte-size, required-space or installation-success comparator. |
| BC-023 | REQ-BROWSER-CONTENT-023 | control: Use independently known installed Pack Info content and Core Library as separate contexts; inspect Help/context entrypoints and available content identity. Missing known info is not silently interpreted as download/format failure. |
| BC-024 | REQ-BROWSER-CONTENT-024 | control: Use an independently authorized available catalog/connection fixture and known version capability before inspecting Home entries and internal back/forward navigation. This packet makes no connection; offline/unavailable content remains U. |
| BC-025 | REQ-BROWSER-CONTENT-025 | protocol: Only in separately authorized future account/service investigation retain offered redirect/confirmation stages and independently valid account capability. No account/login/code/credential is acquired, submitted or simulated here; failure/cancel outcomes stay U. |
| BC-026 | REQ-BROWSER-CONTENT-026 | protocol: Use independently authorized known logged-out/logged-in and account-tier contexts only in future tests. Inspect offered capabilities and catalog labels without asserting a fixed sample count, legal entitlement, accepted authentication or server response. |
| BC-027 | REQ-BROWSER-CONTENT-027 | control: With independently valid account/catalog and known sample category, inspect suggestions, Samples/Packs, offered filters and sort choices, then category-scoped query. Record controls only; relevance, popularity, random ordering and returned sets are ungraded. |
| BC-028 | REQ-BROWSER-CONTENT-028 | similarity: Use separately authorized account/catalog plus independently owned valid nonzero clip/time selection and positive search capability. Retain reference identity and offered replay/replace/delete controls only in future investigation; no audio upload or ranking/count criterion here. |
| BC-029 | REQ-BROWSER-CONTENT-029 | control: With a separately known permitted sample/catalog inspect row/context, pack entry, Like control and expanded columns. No account write, published collection or metadata accuracy is established by icon/text presence. |
| BC-030 | REQ-BROWSER-CONTENT-030 | signal: Future independently permitted nonzero preview source, active cue/monitor output and paired audible baseline required. Retain actually offered preview options separately; no audio/service request, sample identity or timing comparison is performed here. |
| BC-031 | REQ-BROWSER-CONTENT-031 | file: Use a separately authorized future downloaded sample with validated source identity and eligible audio/MIDI/device destination. Retain ordinary default and actual imported clip mode; native load/Warp owners remain authoritative and all file/audio outcomes stay null. |
| BC-032 | REQ-BROWSER-CONTENT-032 | protocol: Only with an independently authorized permitted future sample and known writable configured destination retain registration/library/location state through owner-supported insertion. No licensing decision, download, file write, token or account mutation occurs here. |
| BC-033 | REQ-BROWSER-CONTENT-033 | control: With independently valid authorized account/catalog and an owned test collection inspect offered Library and collection-edit controls. Future sharing/deletion requires separately authorized disposable state; this packet publishes nothing and proves no service persistence/privacy policy. |
| BC-034 | REQ-BROWSER-CONTENT-034 | control: Using independently available permitted service UI inspect named Settings entries in known account contexts. Do not activate downloads, plan changes, support messages, links requiring login or license generation; only control/information roles are proposed. |
| BC-035 | REQ-BROWSER-CONTENT-035 | protocol: Only in a separately authorized future known-compatible account/Move-or-Note configuration retain offered Sign In and synced catalog identities. No login, cloud synchronization or account write is performed here; a visible label alone proves neither support nor data availability. |
| BC-036 | REQ-BROWSER-CONTENT-036 | protocol: Future authorized known synced Set with independently valid assets and accessible User Library required. Retain source versus developed Set and asset location; test unavailable Library separately only after positive baseline. No sync, collection or file repair occurs here. |
| BC-037 | REQ-BROWSER-CONTENT-037 | protocol: Only in a separately authorized future genuine independently supported Push3 Standalone/firmware/network setup retain actual device identity and offered pairing stages. No hardware connection, code exchange, protocol emulator or controller-family completion is claimed here. |
| BC-038 | REQ-BROWSER-CONTENT-038 | control: Require independently valid actual paired Push3 capability/catalog before future observations. Inspect named folders and offered refresh/Disconnect routes without performing pairing/transfer here; absent hardware or stale list stays U. |
| BC-039 | REQ-BROWSER-CONTENT-039 | protocol: Future independently authorized supported Push3 plus owned validated Set/device/sample inventory required. Retain native versus plug-in/frozen/collected contexts under existing owners. No copy/transfer/freeze/remote service action is performed by this packet. |
| BC-040 | REQ-BROWSER-CONTENT-040 | control: Use an independently valid owned Library with known eligible saved content and configured location. Inspect applicable folders/Library entries only; source copy/default/clip/groove/template operations stay with their canonical owners, not retested by folder presence. |
| BC-041 | REQ-BROWSER-CONTENT-041 | control: With valid writable owned Library and saved Project inspect Manage User Library overview and Current Project reveal entry separately. File-manager diagnostics/repair, external shell behavior and actual missing-file resolution remain U. |
| BC-042 | REQ-BROWSER-CONTENT-042 | file: Future owned disposable unsaved then independently saved Project with retained before/after file inventory required. Inspect Browser backup listing under existing save owner; no save/restore/delete/trash operation occurs here and exact counts/metadata remain ungraded. |
| BC-043 | REQ-BROWSER-CONTENT-043 | control: Use an independently valid registered owned discrete folder and completed positive indexing, then an unavailable copy under the existing owner. Inspect scan/Locate/Remove entrypoints; do not infer data deletion or completion from a missing indicator. No whole-drive scan is initiated. |
| BC-044 | REQ-BROWSER-CONTENT-044 | control: With Browser focus and two known accessible populated folders, open A then B, reset, and repeat B with declared Ctrl/Cmd modifier. Inspect expansion only; global shortcut dispatch and unsupported focus remain unknown. |
| BC-045 | REQ-BROWSER-CONTENT-045 | signal: Use independently valid readable nonzero eligible sample and warped/unwarped clip with active nonmuted cue output. Establish positive preview, then retain Raw/scrub/transport settings separately. No render, onset, waveform or route-equivalence oracle is supplied. |
| BC-046 | REQ-BROWSER-CONTENT-046 | signal: With known eligible sample, Browser focus, declared keyboard preferences and independently audible preview baseline, turn Preview off and request each gesture separately. Retain input/state only; no actual Browser runtime or audio comparison occurs here. |
| BC-047 | REQ-BROWSER-CONTENT-047 | control: With independently valid compatible analyzed owned file and Browser focus inspect icon/context and platform chord separately. Record requested reference identity; generic shortcuts and unsupported file admission are not inferred from uninspected figures. |
| BC-048 | REQ-BROWSER-CONTENT-048 | similarity: Future valid owned nonzero analyzed reference/corpus and compatible target required. Retain reference/source identity, completed analysis and observed offered results in separate samples/preset contexts; no nearest-neighbor, ranking, similarity count or swap-output oracle is assigned. |
| BC-049 | REQ-BROWSER-CONTENT-049 | control: With separately retained known in-progress eligible analysis and independently completed positive corpus inspect Status Bar/Pause availability. Do not generate or require a scan here; absent status or source capability is inconclusive, not completed analysis. |
| BC-050 | REQ-BROWSER-CONTENT-050 | control: With an independently known productive valid reference/result list save a disposable label via the general entrypoint and revisit it. Inspect reference identity/top presentation only; later corpus changes, ranking and persistence remain U. |
| BC-U-QUERY | REQ-BROWSER-CONTENT-U-QUERY | boundary: Compare known positive tagged catalog with nonexistent terms, same/cross-group selections, parent/subtags, Unicode/case, empty/missing metadata and equal sort keys in reset copies. |
| BC-U-INDEX | REQ-BROWSER-CONTENT-U-QUERY | source-loss: After completed positive indexing rename/move/disconnect only owned content and restore it; retain tag/query/label states without inventing refresh or repair deadlines. |
| BC-U-ANALYSIS | REQ-BROWSER-CONTENT-U-ANALYSIS | similarity: Use independently validated nonzero owned samples below/at/above source duration context, ambiguous content and presets with known positive completed analysis; compare offered outcomes without assumed eligibility or classifier correctness. |
| BC-U-RANK | REQ-BROWSER-CONTENT-U-ANALYSIS | numeric: Use fixed owned reference/corpus including duplicates, silence only as a separate boundary, changed library membership and offered Splice Random sorting; retain actual rankings/counts without seed, threshold or expected-neighbor criteria. |
| BC-U-AUTH | REQ-BROWSER-CONTENT-U-SERVICE | protocol: Future separately authorized test account/capability only: compare logged-out/expired/unavailable contexts after known positive service baseline; inspect offered prompts, not credentials or invented authentication grammar. |
| BC-U-CATALOG | REQ-BROWSER-CONTENT-U-SERVICE | error: Future independently validated service catalog first, then unavailable network/server or denied sample/Pack capability in disposable contexts. Empty catalog is not a proof of no available content. |
| BC-U-RIGHTS | REQ-BROWSER-CONTENT-U-SERVICE | protocol: Inspect only offered license/subscription/information entrypoints in independently authorized service context. No legal permission, certified-license validity, quota or fixed sample count is inferred. |
| BC-U-PAIR | REQ-BROWSER-CONTENT-U-TRANSFER | protocol: Future genuine supported Push3 Standalone and positive pairing baseline only; wrong/unavailable code, multiple units, disconnect/reconnect and unknown firmware remain exploratory, not protocol or lockout tests performed here. |
| BC-U-TRANSFER | REQ-BROWSER-CONTENT-U-TRANSFER | file: Future authorized known valid Cloud/Push source and owned destination only: compare native/frozen plug-in/collected versus missing dependency cases under existing owners; retain identity/partial state without compatibility or copy-equality criteria. |
| BC-U-STORE | REQ-BROWSER-CONTENT-U-STORAGE | file: Known writable owned destinations and valid permitted downloaded source first in future tests; compare unavailable space/permissions, collisions and configured destination changes without installing or exhausting storage here. |
| BC-U-UNDO | REQ-BROWSER-CONTENT-U-STORAGE | undo-redo: Create/edit/delete one owned tag/label/collection and inspect offered Undo/Redo separately; no global transaction grouping, sidecar rewrite or server-state restoration is presumed. |
| BC-U-CANCEL | REQ-BROWSER-CONTENT-U-STORAGE | cancellation: Dismiss offered tag/label/range/menu and future authorized download/install/pairing dialogs before/after independently observed commit on reset copies; no rollback or cleanup guarantee. |
| BC-U-PERSIST | REQ-BROWSER-CONTENT-U-STORAGE | persistence: Save/reopen an owned Set and separately restart with explicit filters/labels/collection visibility/Library paths and permitted account state; retain Set/global/index/server ownership separately. |
| BC-U-INACTIVE | REQ-BROWSER-CONTENT-U-LIFECYCLE | negative: Establish independently usable active indexed content/capability and nonzero preview/cue output, then change only the tested tag/filter/service/input state; silence or absent account/hardware cannot prove no effect. |
| BC-U-MALFORMED | REQ-BROWSER-CONTENT-U-LIFECYCLE | malformed: After valid owned baseline use invalid tag/path/name text, unsupported/corrupt file or metadata only through offered controls/known owner formats. No invented schema/parser/clamp/repair law. |
| BC-U-FOCUS | REQ-BROWSER-CONTENT-U-LIFECYCLE | context: Repeat supported Browser-focused tag/number/preview/similarity gestures with text edit, modal/plugin focus, alternate layout/IME and explicit Computer MIDI Keyboard/navigation preferences as separate unknown trials. |
| BC-U-TRANSPORT | REQ-BROWSER-CONTENT-U-LIFECYCLE | transport: With positive nonzero preview and valid owner-supported playback compare stopped/running/seek/tempo/loop around selection or allowed preview-option changes; no scheduling or phase comparator. |
| BC-U-AUTOMATION | REQ-BROWSER-CONTENT-U-LIFECYCLE | automation: Only if actually offered, explore mapping/automation of a Browser/preview/service control after a known positive eligible target. No general mapping eligibility or ownership arbitration. |
| BC-U-RATE | REQ-BROWSER-CONTENT-U-LIFECYCLE | sample-rate: Future independently accepted44.1/48/96kHz and64/512-frame contexts with positive source/output baseline; no resampling, timing, similarity or rate-invariance comparator. |
| BC-U-LOSS | REQ-BROWSER-CONTENT-U-LIFECYCLE | source-loss: After independently working local/service/paired capability disconnect only owned media/output/source/network/hardware in separate future contexts, then restore; no fallback, deadline, duplicate or sync-conflict rule. |
| BC-U-TEARDOWN | REQ-BROWSER-CONTENT-U-LIFECYCLE | teardown: During positive preview/selection/edit or separately authorized pending service operation close the view/Set/app or remove source in reset copies; retain prompts/partial state without resource, silence, flush or completion guarantee. |

## Analysis-only evidence and freeze

[Source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/sources.json) pins exact reused captures: Browser334122bytes
SHA256 `4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3`,
UTC2026-10-19T19:56:28.639468+00:00; Concepts306807bytes
SHA256 `da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`,
UTC2026-10-19T19:53:41.813664+00:00. [Browser268 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/source-blocks.json)
and [Similarity6 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/similarity-blocks.json) retain exact anchors/HTML lines.
Only Concepts sound-similarity section was selected; no whole-Concepts contract.
[Owner/reuse pins](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/owner-pins.json), [counts](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/counts.json),
[manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/manifest-author-r1.json) and canonical snapshots freeze the partial
packet. Current website prose is not immutable12.4.3 evidence. Shared catalogs,
coverage/questions/log and independent review are integrated separately by root.
