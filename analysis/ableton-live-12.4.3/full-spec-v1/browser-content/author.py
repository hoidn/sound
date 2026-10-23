"""Author bounded Browser content documentation; never opens a service or application."""
from pathlib import Path
from collections import Counter
import hashlib
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert not (P / 'manifest-author-r1.json').exists(), 'Never rewrite a frozen revision'
dump = lambda name, value: (P / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
pin = lambda q: {'bytes': q.stat().st_size, 'sha256': hashlib.sha256(q.read_bytes()).hexdigest()}
captured = ['source.json', 'sources.json', 'manual-browser-2026-10-19.html', 'manual-concepts.html',
            'source-blocks.json', 'source-blocks.txt', 'similarity-blocks.json', 'similarity-blocks.txt']
dump('pre-author-inputs.json', {name: pin(P / name) for name in captured})
blocks = {b['id']: b for name in ('source-blocks.json', 'similarity-blocks.json') for b in json.loads((P / name).read_text())}
rows = []


def add(title, kind, claim, refs, action):
    rows.append(dict(title=title, kind=kind, contract=claim, source_blocks=refs.split(), action=action))


add('Browser sizing contexts', 'control',
    'Dragging Browser dividers resizes panels; dragging its bottom edge closes Info and the active Clip/Device View. Full-Height Browser instead expands while those views remain open. Geometry limits and focus restoration remain U.',
    'BC-B012 BC-B013', 'With Info and Clip View explicitly open, resize a divider/bottom edge, then restore and choose Full-Height Browser. Repeat Device View separately; inspect named visibility only, no pixel tolerance.')
add('Content columns and sorting entrypoints', 'control',
    'Name is always shown; Content Options offers extra columns and file-extension visibility. Headers can be reordered and clicked for ascending/descending sorting. Sort keys, Unicode comparison, missing values and ties remain U.',
    'BC-B016 BC-B017 BC-B018 BC-B019', 'Use owned entries with known distinct names/metadata; show an offered extra column, move its header, toggle sort direction and extensions. Inspect controls/order choice, without a new exact result-ranking comparator.')
add('Tag-query entry and suggestions', 'control',
    'Typing # followed by a tag name exposes tag auto-complete suggestions. Ordinary word matching/clear/global-find behavior stays with Browser Workflows001..004; tag parser, matching, suggestion ranking and boolean algebra remain U.',
    'BC-B023 BC-B024', 'With independently known assigned custom tags and completed indexing, type # plus a partial known tag and choose an offered suggestion. Retain query/selection and compare an unassigned tag only as an unknown result probe.')
add('Custom result-label editing', 'control',
    'Add Label saves a search/filter result label in Library. Its context menu removes a custom label; factory/custom labels offer rename and icon choice. Dynamic versus snapshot membership and durable storage are not established.',
    'BC-B033 BC-B034 BC-B035 BC-B036 BC-B037 BC-B053', 'After a productive known search/filter baseline, Add Label, revisit it, rename/change its offered icon and remove the owned custom label on separate copies. Inspect label identity only; membership refresh/save/restart remains U.')
add('Per-label filter presentation', 'control',
    'Filter View can be shown/hidden, with label-specific groups shown through its menu or hidden by group context. Enabled filter state is recalled between Library labels; Ctrl Windows/Cmd Mac permits multiple tags in a group. Reset Filter Groups to Default restores visible groups, not a new search algebra.',
    'BC-B007 BC-B046 BC-B048 BC-B049 BC-B050 BC-B051 BC-B052', 'Use two labels with known available groups and positive content; vary visible groups and Ctrl/Cmd-selected tags, switch labels/back, then reset group visibility. Retain result-bar count as display context; exact result sets/count arithmetic remain U.')
add('Factory tag edit restrictions', 'control',
    'The chapter distinguishes factory/default tags and groups from user additions: factory-item default tags and default groups/tags cannot be removed or edited, while added user tags are allowed. Exact permissions, error presentation and serialization stay U or with Browser Index.',
    'BC-B056 BC-B057 BC-B072 BC-B079', 'Use an independently identified unmodified factory item plus an owned custom tag; inspect offered edit/removal commands and add the custom tag separately. Compare custom-only item; do not infer write protection from a failed source/index baseline.')
add('Automatic analysis and plug-in metadata tags', 'analysis',
    'Current documentation describes periodic sound analysis assigning a best-matching tag to user samples up to60 seconds, and VST3 metadata tags when a subcategory maps to a Live category. Analysis timing, duration-boundary admission, classification/model, category mapping and accuracy remain U; native index fields provide no algorithm.',
    'BC-B058 BC-B060', 'Use independently valid owned nonzero samples of retained duration and a known metadata-bearing plug-in only if separately available. Establish completed positive analysis/indexing context before observing tags; no deadline, exact classification or subcategory transform is predicted.')
add('Auto Tags controls', 'control',
    'Enable Auto Tags is offered in Filter View. Tag Editor can remove auto tags or change them to user tags. Source provenance conversion, future rescans, durability and classification remain U.',
    'BC-B059', 'With an independently retained actual auto-tag assignment and active index, inspect Enable Auto Tags and the offered editor removal/user-conversion routes in reset copies. Missing analyzed tags remain an unmet prerequisite, not an empty-result pass.')
add('Tag Editor assignment and custom creation', 'control',
    'Filter View opens Tag Editor; it shows selected-item tags, foldable groups and assigned-group emphasis. Checkbox edits can tag one or Shift-selected multiple files; Add Tag and Add Group create custom entries, with a group exposed in Filter View after one of its tags is assigned.',
    'BC-B062 BC-B063 BC-B064 BC-B065 BC-B066 BC-B067 BC-B068 BC-B069', 'Use two owned indexed files with different known tags, open editor, fold/unfold, assign a tag to one then Shift-select both. Create an owned group/tag and assign it; inspect entries and group visibility, not sidecar bytes or transaction grouping.')
add('Nested and custom tag editing', 'control',
    'Add Subtag in creates a nested tag under a parent; Creator-group tags do not permit subtags. Parent tags fold/unfold; custom tags/groups offer rename/delete. Editor closes through X or its Filter View entry; default-item restrictions remain separate.',
    'BC-B070 BC-B071 BC-B072 BC-B073', 'Create an owned parent/subtag, fold it, rename/delete custom entries on reset copies and inspect a Creator tag without presuming a particular disabled/hidden presentation. Close/reopen editor; deletion cascade and cancellation remain U.')
add('Quick Tags creation', 'control',
    'Quick Tags Add offers existing-tag auto-complete or Create new tag followed by parent/group selection. An unrecognized parent/group name offers creation of a parent tag or group. No arbitrary nesting, collision or text grammar is specified.',
    'BC-B075 BC-B076 BC-B077 BC-B078', 'Select an owned tagged file, add an existing offered tag, then type a distinct new tag and choose a known parent. Separately use an unrecognized parent/group name and inspect the offered creation choice; invalid/collision outcomes remain U.')
add('Quick Tags selection presentation', 'control',
    'Quick Tags shows assigned tags, with additions described in alphabetical order. Multi-selection shows the union and marks nonshared tags with an asterisk; selecting a tag shows its group in Status Bar. X removes user assignments, and Filter View can hide the section. Exact collation and saved visibility remain U.',
    'BC-B076 BC-B079 BC-B080 BC-B081 BC-B082', 'Use two indexed owned items with shared tag A and distinct B/C; select one then both, inspect shared/nonshared marks, select a tag for group status, remove an owned assignment and toggle section visibility. No Unicode/tie order or serialization oracle.')
add('Collection assignment entrypoints', 'control',
    'Selected items, including mixed types/folders or multiple items, can receive Collections colors through context or keys1..7;0 resets assignments. This is Browser-focused UI assignment, not a global shortcut or new sidecar color encoding. Existing collection-membership and sidecar owners remain authoritative.',
    'BC-B084 BC-B085 BC-B086', 'With Browser focus, declared key/layout/preferences and two owned different-type entries, assign via context then an offered number key in reset copies; reset with0. Inspect assignment presentation; do not reinterpret released sidecar values or global dispatch.')
add('Collection item presentation', 'control',
    'Collection folders can unfold. Content-pane color icons represent assignments, with at most three displayed even when an item has more colors. Collection membership itself remains Browser Workflows006; no color palette or chosen-color truncation order is established.',
    'BC-B087 BC-B088', 'Use an owned collection folder and item with independently confirmed multiple assignments; unfold the folder and inspect assignment icons versus retained actual assignments. Do not infer omitted assignments from icon count or exact pixels.')
add('Collection label name and visibility', 'control',
    'Collection labels support context rename or Browser-focused Ctrl/Cmd-R, and header Edit exposes Show/Hide Label with Done. Assigning a hidden previously unassigned color reveals its label; removing all assignments does not automatically hide a visible label.',
    'BC-B089 BC-B090 BC-B091 BC-B092', 'On owned assignments rename a label, explicitly hide an unassigned color, assign it to an indexed item and inspect visibility; remove that assignment separately. Retain prior hidden/visible state and key focus; no factory-default inference.')
add('Library label presentation', 'control',
    'Library presents type-oriented labels and header Edit/Done visibility selection. Their described contents are discovery roles, not a new extension-kind, plug-in admission, ranking or index algorithm. Source-described default visibility is not exact-target observation.',
    'BC-B094 BC-B095 BC-B096 BC-B097 BC-B098 BC-B099 BC-B100 BC-B101 BC-B102 BC-B103 BC-B104 BC-B105 BC-B106 BC-B107 BC-B108 BC-B109 BC-B110', 'With an independently known positive local catalog, inspect offered Library labels, hide/show one via Edit/Done and revisit. Existing Browser Index and device/media owners determine content admission; missing unavailable products are not a negative compatibility result.')
add('Places content entry roles', 'control',
    'Places exposes configured Packs, Splice, Cloud, Push, User Library, Current Project and user-folder entrypoints. Its actual labels depend on configuration; settings-owned Show Splice/Cloud/Push controls do not prove available services or hardware.',
    'BC-B112 BC-B113 BC-B114 BC-B115 BC-B116 BC-B117 BC-B118 BC-B119 BC-B120 BC-B121', 'Retain actual configured local Library/Project/folders and independently available service/hardware capability. Inspect corresponding Places entries without enabling accounts or transferring files; label absence alone is not service failure.')
add('Installed Pack presentation', 'control',
    'Installed Packs appear as expandable folders under Packs, with their presets/samples/Live Clips also exposed in appropriate Library labels. This is a known installed-catalog view, not an ALP codec, install transaction or universal content-admission law.',
    'BC-B123 BC-B124', 'Use a separately retained valid installed test Pack/catalog and known eligible contents; expand its folder and inspect offered Library entries. No Pack is downloaded/installed here; existing import/format owners remain prerequisites.')
add('Pack updates and available catalog', 'control',
    'Packs Updates exposes available updates for installed Packs; Available Packs exposes owned uninstalled Packs. Ownership/catalog validity, refresh ordering, stale state and entitlement protocol remain U.',
    'BC-B125 BC-B126', 'Only with independently valid authorized account/catalog snapshots, inspect known installed-update and owned-uninstalled entries separately. An offline or unavailable account/catalog is inconclusive, not proof that no update/Pack exists.')
add('Pack download controls', 'protocol',
    'The source describes download/progress, pause/resume/cancel and corresponding context commands, including selected multiple Packs. These are workflow roles only; bytes, authentication, queue order, retry, progress scale, cancellation and partial-file outcomes remain U.',
    'BC-B127 BC-B128 BC-B129 BC-B130 BC-B131', 'For separately authorized future service tests only, require a known permitted Pack/catalog and working positive download baseline; retain offered start/pause/resume/cancel states for one then two selections. No service request or download is performed by this packet.')
add('Pack install and delete roles', 'file',
    'After download the source offers Install with a progress dialog. Installed Pack context/Delete removes it and makes it available again. This is distinct from project-Pack creation/restore under Project Media021; atomicity, dependencies, rights, deletion extent and service refresh remain U.',
    'BC-B130 BC-B132 BC-B133 BC-B135', 'Future authorized disposable Pack copy and separately validated completed download/install baseline required. Retain offered install/delete and catalog states without performing them here; project references, disk effects and cancellation are separate unknowns.')
add('Pack size and downloadable visibility', 'control',
    'Content Options can expose Pack size in Updates/Available Packs. Library settings Show Downloadable Packs hides/shows those sections. Size units/accuracy, capacity prediction and default visibility are not new numerical laws.',
    'BC-B134 BC-B136', 'With a valid known Pack catalog inspect the size-column option and Show Downloadable Packs on/off. Compare section/control presence only; no byte-size, required-space or installation-success comparator.')
add('Pack Info entrypoints', 'control',
    'Installed Packs can expose Show Pack Info, and Help Pack Overview opens installed Pack Info pages. Content may include creator/summary/tutorial; the Core Library is documented without a Pack Info page. No external tutorial or content decoder is specified.',
    'BC-B138 BC-B139', 'Use independently known installed Pack Info content and Core Library as separate contexts; inspect Help/context entrypoints and available content identity. Missing known info is not silently interpreted as download/format failure.')
add('Splice Home and connection prerequisite', 'control',
    'The Splice label Home exposes navigation/search, Search with Sound and category entrypoints, with login/signup entries. Viewing its content requires an active Internet connection. Settings-owned label visibility and account/service availability remain distinct.',
    'BC-B142 BC-B143 BC-B144 BC-B145', 'Use an independently authorized available catalog/connection fixture and known version capability before inspecting Home entries and internal back/forward navigation. This packet makes no connection; offline/unavailable content remains U.')
add('Splice device-confirmation login role', 'protocol',
    'Login/Try free opens an OS browser for Splice device confirmation and then account entry; the source describes matching confirmation codes in browser and Live. This supplies no credential, token, code-generation, security, entitlement or login-success law.',
    'BC-B147 BC-B148', 'Only in separately authorized future account/service investigation retain offered redirect/confirmation stages and independently valid account capability. No account/login/code/credential is acquired, submitted or simulated here; failure/cancel outcomes stay U.')
add('Splice account-dependent capabilities', 'protocol',
    'The source distinguishes unauthenticated browse/preview from logged-in Set insertion, library saving and Search with Sound. Logged-in Home exposes Library and rearranged browse/search areas. Free/paid catalog contents, counts, rights and subscription behavior remain unknown.',
    'BC-B147 BC-B149 BC-B155', 'Use independently authorized known logged-out/logged-in and account-tier contexts only in future tests. Inspect offered capabilities and catalog labels without asserting a fixed sample count, legal entitlement, accepted authentication or server response.')
add('Splice search and result controls', 'control',
    'Splice has its own category/query suggestions, Samples/Packs view, tag/filter expansion and sorting options including Random/shuffle. Selected category scopes subsequent text search. Exact result matching, ranking, RNG, counts and history retention remain U; native Browser matching is not borrowed.',
    'BC-B151 BC-B152 BC-B153 BC-B154 BC-B156 BC-B159 BC-B160', 'With independently valid account/catalog and known sample category, inspect suggestions, Samples/Packs, offered filters and sort choices, then category-scoped query. Record controls only; relevance, popularity, random ordering and returned sets are ungraded.')
add('Splice Search with Sound', 'similarity',
    'Logged-in Search with Sound accepts a dragged clip or captured time selection; the source describes compatible results and reference replay/replacement/removal. Its reported50-result list is source context, not a target count or quality oracle. Model, upload, scoring, rights and rendering remain U.',
    'BC-B147 BC-B157', 'Use separately authorized account/catalog plus independently owned valid nonzero clip/time selection and positive search capability. Retain reference identity and offered replay/replace/delete controls only in future investigation; no audio upload or ranking/count criterion here.')
add('Splice sample-row entrypoints', 'control',
    'Sample rows expose pack navigation, sample-type/name/tags and context actions for Likes/Collections or pack view. Hover/selection can expose Like and expanded pane shows Time/Key/BPM columns. Display metadata does not establish audio analysis, source type or stored service identity.',
    'BC-B161 BC-B165 BC-B166', 'With a separately known permitted sample/catalog inspect row/context, pack entry, Like control and expanded columns. No account write, published collection or metadata accuracy is established by icon/text presence.')
add('Splice preview settings', 'signal',
    'Splice preview has its own play/name entry, loop/timestretch/original-tempo, selected-key/Live-scale and loudness options. Source defaults and preview synchronization supply no waveform, gain, pitch, scale, render or timing law; native Browser Preview remains a separate owner.',
    'BC-B162 BC-B163 BC-B164', 'Future independently permitted nonzero preview source, active cue/monitor output and paired audible baseline required. Retain actually offered preview options separately; no audio/service request, sample identity or timing comparison is performed here.')
add('Splice import Warp context', 'file',
    'Splice samples have service-specific drag/double-click/Enter/device destinations. The source describes Complex Warp overriding the ordinary default for clips using Splice samples; this is unverified source context, not a new Warp algorithm, decode result or guaranteed preview identity.',
    'BC-B167 BC-B168', 'Use a separately authorized future downloaded sample with validated source identity and eligible audio/MIDI/device destination. Retain ordinary default and actual imported clip mode; native load/Warp owners remain authoritative and all file/audio outcomes stay null.')
add('Splice sample registration and location', 'protocol',
    'The source describes Set insertion as licensing/registering a sample in the Splice library and storing downloads under User Library/Samples/Splice, Current Project/Samples/Splice or Custom Folder. These are source workflow/location roles, not a legal-rights conclusion, default-build promise, file transaction or service codec.',
    'BC-B169 BC-B170 BC-B171 BC-B172 BC-B173', 'Only with an independently authorized permitted future sample and known writable configured destination retain registration/library/location state through owner-supported insertion. No licensing decision, download, file write, token or account mutation occurs here.')
add('Splice Library and Collections controls', 'control',
    'Splice Library presents Likes, Collections and previously loaded/downloaded samples. Its Collections page/menu offers creation, name/description edit, private/share-link and delete controls. This is separate from Browser color Collections; publication, privacy enforcement and saved server state remain U.',
    'BC-B175 BC-B176', 'With independently valid authorized account/catalog and an owned test collection inspect offered Library and collection-edit controls. Future sharing/deletion requires separately authorized disposable state; this packet publishes nothing and proves no service persistence/privacy policy.')
add('Splice Settings information routes', 'control',
    'Splice Settings offers subscription/display, usage-log download, certified-license information, Knowledge Base/feedback and logged-out Login entrypoints. No subscription, usage-log format, legal validity, support service or credential behavior is specified.',
    'BC-B178 BC-B179', 'Using independently available permitted service UI inspect named Settings entries in known account contexts. Do not activate downloads, plan changes, support messages, links requiring login or license generation; only control/information roles are proposed.')
add('Ableton Cloud authorization entry', 'protocol',
    'Cloud label offers a Sign In browser route to authorize Ableton Cloud, after which synced Move/Note Sets appear. The published up-to-eight Set description is source context, not an exact-target quota, sync protocol, account entitlement or version-compatibility promise.',
    'BC-B181 BC-B182 BC-B183', 'Only in a separately authorized future known-compatible account/Move-or-Note configuration retain offered Sign In and synced catalog identities. No login, cloud synchronization or account write is performed here; a visible label alone proves neither support nor data availability.')
add('Cloud assets and direction boundary', 'protocol',
    'Synced Set assets require an accessible User Library; ABL Assets stores Move/Note assets. The chapter describes Move/Note-to-Live sync rather than Live-to-source and recommends Collect All and Save for developed Sets. Existing project/media collection and missing-reference owners retain their laws.',
    'BC-B184 BC-B185 BC-B205', 'Future authorized known synced Set with independently valid assets and accessible User Library required. Retain source versus developed Set and asset location; test unavailable Library separately only after positive baseline. No sync, collection or file repair occurs here.')
add('Push3 standalone pairing entry', 'protocol',
    'Browser Push transfer requires Push3 Standalone and the same Wi-Fi network. Named-device selection/Connect precedes a code displayed on Push and entered in Live. The six-digit description is not a wire or pairing-code algorithm; Push1/2/controller mode cannot substitute.',
    'BC-B189 BC-B190', 'Only in a separately authorized future genuine independently supported Push3 Standalone/firmware/network setup retain actual device identity and offered pairing stages. No hardware connection, code exchange, protocol emulator or controller-family completion is claimed here.')
add('Paired Push file-view controls', 'control',
    'After successful pairing, saved Standalone Project folders and Push User Library appear. Switching away/back refreshes the list; Push-label Disconnect unpairs. These are Browser file-view entrypoints, not file-transfer integrity, discovery timing or Push3 standalone/controller compatibility.',
    'BC-B191 BC-B192 BC-B193', 'Require independently valid actual paired Push3 capability/catalog before future observations. Inspect named folders and offered refresh/Disconnect routes without performing pairing/transfer here; absent hardware or stale list stays U.')
add('Push continuity prerequisites', 'protocol',
    'The chapter describes Standalone Set transfer/open on computer and transfer back using native devices, frozen plug-in tracks and collected Project samples. These are prerequisites/guidance, not an arbitrary Set/device codec, plugin parity, successful transfer or full Push3 contract.',
    'BC-B188', 'Future independently authorized supported Push3 plus owned validated Set/device/sample inventory required. Retain native versus plug-in/frozen/collected contexts under existing owners. No copy/transfer/freeze/remote service action is performed by this packet.')
add('User Library folder entry roles', 'control',
    'User Library exposes user-saved content and custom folders; source folder roles include ABL Assets, Chord Banks, Clips, Defaults, Grooves, Presets, Samples and Templates. Existing owners retain save/default/Stacks/groove/media/template and dependent-copy semantics; folder names do not establish codecs or constructor contents.',
    'BC-B197 BC-B202 BC-B203 BC-B205 BC-B207 BC-B209 BC-B210 BC-B211 BC-B213 BC-B217 BC-B218 BC-B221 BC-B222 BC-B225 BC-B226 BC-B228', 'Use an independently valid owned Library with known eligible saved content and configured location. Inspect applicable folders/Library entries only; source copy/default/clip/groove/template operations stay with their canonical owners, not retested by folder presence.')
add('User Library manager and Project reveal', 'control',
    'File Manage Files then Manage User Library opens that Library overview; Current Project context Show in Explorer/Finder reveals its folder. Project Media retains Set file management and reference operations, and Settings retains location selection.',
    'BC-B231 BC-B239', 'With valid writable owned Library and saved Project inspect Manage User Library overview and Current Project reveal entry separately. File-manager diagnostics/repair, external shell behavior and actual missing-file resolution remain U.')
add('Current Project Backup presentation', 'file',
    'The chapter describes a Backup folder after repeated saves, timestamped prior Sets and bounded retention with old backups moved to trash; unsaved Sets use a temporary Project without Backup. Its twice-saved/last-ten wording remains source context, not a new recovery, retention-timing, filesystem or restore law.',
    'BC-B233 BC-B234 BC-B235 BC-B236 BC-B237 BC-B238', 'Future owned disposable unsaved then independently saved Project with retained before/after file inventory required. Inspect Browser backup listing under existing save owner; no save/restore/delete/trash operation occurs here and exact counts/metadata remain ungraded.')
add('Folder scan, locate and removal entrypoints', 'control',
    'A Places scan has a spinning progress indicator. For a registered folder, Locate Folder and Remove from Sidebar are offered; removal also applies to an available folder. Existing Browser Workflows007/008 owns nonrelocating registration and dimmed unavailable entries; retry/index timing and deletion effects remain U.',
    'BC-B243 BC-B244 BC-B245 BC-B246 BC-B247', 'Use an independently valid registered owned discrete folder and completed positive indexing, then an unavailable copy under the existing owner. Inspect scan/Locate/Remove entrypoints; do not infer data deletion or completion from a missing indicator. No whole-drive scan is initiated.')
add('Multi-folder expansion modifier', 'control',
    'Opening another folder normally closes previously open folders; Ctrl Windows/Cmd Mac while opening overrides that behavior. Generic arrows/focus remain Keyboard Navigation-owned; selection, layout/IME, hidden folders and persistence require their own contexts.',
    'BC-B252', 'With Browser focus and two known accessible populated folders, open A then B, reset, and repeat B with declared Ctrl/Cmd modifier. Inspect expansion only; global shortcut dispatch and unsupported focus remain unknown.')
add('Native preview Raw and scrubbing context', 'signal',
    'Beyond existing generic preview, the chapter describes waveform scrubbing except unwarped saved clips, Raw original-tempo/unlooped versus non-Raw next-bar/looped preview, and no scrubbing in Raw. Cue/routing owns output selection; all sound, loop, onset and tempo algorithms remain U.',
    'BC-B258 BC-B259 BC-B260 BC-B261 BC-B262', 'Use independently valid readable nonzero eligible sample and warped/unwarped clip with active nonmuted cue output. Establish positive preview, then retain Raw/scrub/transport settings separately. No render, onset, waveform or route-equivalence oracle is supplied.')
add('Explicit preview gesture without toggle', 'signal',
    'Shift-Enter or right arrow on a selected eligible Browser item can request preview even with Preview toggle off. Existing Browser Workflows009 owns generic preview; focus conflict, actual sound and cancellation/timing remain U.',
    'BC-B257', 'With known eligible sample, Browser focus, declared keyboard preferences and independently audible preview baseline, turn Preview off and request each gesture separately. Retain input/state only; no actual Browser runtime or audio comparison occurs here.')
add('Browser Similarity Search entry', 'control',
    'Compatible selected Browser files offer Show Similar Files icon/context and Ctrl-Shift-F Windows/Cmd-Shift-F Mac entry. This owns Browser entrypoints only; Clip View042 retains its corresponding entry and sample-file management.',
    'SIM-B003 SIM-B004', 'With independently valid compatible analyzed owned file and Browser focus inspect icon/context and platform chord separately. Record requested reference identity; generic shortcuts and unsupported file admission are not inferred from uninspected figures.')
add('Similarity source and ranking role', 'similarity',
    'Concepts describes comparing a reference against Core/User Library samples up to60 seconds, instrument/drum presets, then listing results from most to least similar. Similar Sample Swapping names Drum Rack, Simpler and Drum Sampler targets. No embedding/model, scoring, threshold, exact result/order, boundary admission or replacement algorithm is supplied.',
    'SIM-B002 SIM-B004', 'Future valid owned nonzero analyzed reference/corpus and compatible target required. Retain reference/source identity, completed analysis and observed offered results in separate samples/preset contexts; no nearest-neighbor, ranking, similarity count or swap-output oracle is assigned.')
add('Similarity background-analysis status', 'control',
    'The Concepts source says similarity needs analysis, with new-user-file background work reported in Status Bar and a Pause control; Core Library is described as pre-analyzed. This clause owns status/Pause affordances, not a scan trigger, completion deadline, resume law, index lifecycle or generated features.',
    'SIM-B006', 'With separately retained known in-progress eligible analysis and independently completed positive corpus inspect Status Bar/Pause availability. Do not generate or require a scan here; absent status or source capability is inconclusive, not completed analysis.')
add('Similarity custom-label reference presentation', 'control',
    'For a custom User Label saved from Similarity Search results, the reference sound is shown at the top. General custom-label editing stays above; reference identity is distinct from any numerical similarity rank or successful sample replacement.',
    'SIM-B005', 'With an independently known productive valid reference/result list save a disposable label via the general entrypoint and revisit it. Inspect reference identity/top presentation only; later corpus changes, ranking and persistence remain U.')

unknowns = [
('QUERY', 'Query, tags and result algebra', 'Tag/query grammar, boolean combination, collation/Unicode/IME, hierarchy/sort ties, filter counts, dynamic label refresh and index-to-UI result identity remain unknown.', [('QUERY','boundary','Compare known positive tagged catalog with nonexistent terms, same/cross-group selections, parent/subtags, Unicode/case, empty/missing metadata and equal sort keys in reset copies.'),('INDEX','source-loss','After completed positive indexing rename/move/disconnect only owned content and restore it; retain tag/query/label states without inventing refresh or repair deadlines.')]),
('ANALYSIS', 'Automatic classification and similarity algorithms', 'Sound-analysis eligibility,60-second boundaries, models/features/scoring, periodic scheduling, CPU behavior, rankings/thresholds/RNG and swap sound/state outcomes remain unknown.', [('ANALYSIS','similarity','Use independently validated nonzero owned samples below/at/above source duration context, ambiguous content and presets with known positive completed analysis; compare offered outcomes without assumed eligibility or classifier correctness.'),('RANK','numeric','Use fixed owned reference/corpus including duplicates, silence only as a separate boundary, changed library membership and offered Splice Random sorting; retain actual rankings/counts without seed, threshold or expected-neighbor criteria.')]),
('SERVICE', 'Accounts, catalogs and legal/service boundaries', 'Online capability, credentials/tokens/device confirmation, free/paid entitlements/catalogs/quotas, sample rights, logs/licenses, privacy/sharing, availability and server protocols remain unknown. No legal interpretation follows from marketing or registration prose.', [('AUTH','protocol','Future separately authorized test account/capability only: compare logged-out/expired/unavailable contexts after known positive service baseline; inspect offered prompts, not credentials or invented authentication grammar.'),('CATALOG','error','Future independently validated service catalog first, then unavailable network/server or denied sample/Pack capability in disposable contexts. Empty catalog is not a proof of no available content.'),('RIGHTS','protocol','Inspect only offered license/subscription/information entrypoints in independently authorized service context. No legal permission, certified-license validity, quota or fixed sample count is inferred.')]),
('TRANSFER', 'Cloud and Push file identity', 'Cloud/Push versions, pairing/discovery, permissions, codecs, dependency/device portability, synchronization/conflict order, partial copies and direction/capacity limits remain unknown; no Push3 standalone or controller profile is completed.', [('PAIR','protocol','Future genuine supported Push3 Standalone and positive pairing baseline only; wrong/unavailable code, multiple units, disconnect/reconnect and unknown firmware remain exploratory, not protocol or lockout tests performed here.'),('TRANSFER','file','Future authorized known valid Cloud/Push source and owned destination only: compare native/frozen plug-in/collected versus missing dependency cases under existing owners; retain identity/partial state without compatibility or copy-equality criteria.')]),
('STORAGE', 'Content transactions and saved state', 'Pack install/update/delete, Library reconfiguration, backup retention, downloads/paths/collisions, tagging side effects, Undo/cancel, saved browser state and migration remain unknown beyond existing finite owners.', [('STORE','file','Known writable owned destinations and valid permitted downloaded source first in future tests; compare unavailable space/permissions, collisions and configured destination changes without installing or exhausting storage here.'),('UNDO','undo-redo','Create/edit/delete one owned tag/label/collection and inspect offered Undo/Redo separately; no global transaction grouping, sidecar rewrite or server-state restoration is presumed.'),('CANCEL','cancellation','Dismiss offered tag/label/range/menu and future authorized download/install/pairing dialogs before/after independently observed commit on reset copies; no rollback or cleanup guarantee.'),('PERSIST','persistence','Save/reopen an owned Set and separately restart with explicit filters/labels/collection visibility/Library paths and permitted account state; retain Set/global/index/server ownership separately.')]),
('LIFECYCLE', 'Input admission and cross-cutting lifecycle', 'Malformed/unavailable content, focus/preferences, unsupported controls, transport/automation/rate changes, source loss, concurrency and teardown retain null outcomes; missing capability or positive input is never a negative pass.', [('INACTIVE','negative','Establish independently usable active indexed content/capability and nonzero preview/cue output, then change only the tested tag/filter/service/input state; silence or absent account/hardware cannot prove no effect.'),('MALFORMED','malformed','After valid owned baseline use invalid tag/path/name text, unsupported/corrupt file or metadata only through offered controls/known owner formats. No invented schema/parser/clamp/repair law.'),('FOCUS','context','Repeat supported Browser-focused tag/number/preview/similarity gestures with text edit, modal/plugin focus, alternate layout/IME and explicit Computer MIDI Keyboard/navigation preferences as separate unknown trials.'),('TRANSPORT','transport','With positive nonzero preview and valid owner-supported playback compare stopped/running/seek/tempo/loop around selection or allowed preview-option changes; no scheduling or phase comparator.'),('AUTOMATION','automation','Only if actually offered, explore mapping/automation of a Browser/preview/service control after a known positive eligible target. No general mapping eligibility or ownership arbitration.'),('RATE','sample-rate','Future independently accepted44.1/48/96kHz and64/512-frame contexts with positive source/output baseline; no resampling, timing, similarity or rate-invariance comparator.'),('LOSS','source-loss','After independently working local/service/paired capability disconnect only owned media/output/source/network/hardware in separate future contexts, then restore; no fallback, deadline, duplicate or sync-conflict rule.'),('TEARDOWN','teardown','During positive preview/selection/edit or separately authorized pending service operation close the view/Set/app or remove source in reset copies; retain prompts/partial state without resource, silence, flush or completion guarantee.')])]

requirements, cases = [], []
for i, row in enumerate(rows, 1):
    rid, cid = f'REQ-BROWSER-CONTENT-{i:03d}', f'BC-{i:03d}'
    evidence = [dict(block=x, anchor=blocks[x]['anchor'], html_line=blocks[x]['html_line'], source='D12-SOUND-SIMILARITY' if x.startswith('SIM-') else 'D12-BROWSER-CONTENT') for x in row['source_blocks']]
    requirements.append(dict(id=rid, title=row['title'], contract=row['contract'], provenance='D12', target_applicability='U', evidence=evidence))
    visible = row['kind'] == 'control'
    cases.append(dict(id=cid, requirements=[rid], kind=row['kind'], provenance='D12', fixture='fixtures.json#BC-OWNED', preconditions=['common','active-positive-guard'], setup_and_action=row['action'], source_claim=row['contract'], documentary_expected=row['contract'] if visible else None, documentary_comparator='Named text-supported visible controls, entrypoints, selection or membership roles only; no signal, similarity/ranking, timing, numeric, protocol, service or file-integrity proof.' if visible else None, expected=None, comparison=None, target_grade='U', executed=False, evidence=evidence))
for suffix, title, contract, probes in unknowns:
    rid='REQ-BROWSER-CONTENT-U-'+suffix
    requirements.append(dict(id=rid,title=title,contract=contract,provenance='U',target_applicability='U',evidence=[]))
    for cid,kind,action in probes:
        cases.append(dict(id='BC-U-'+cid,requirements=[rid],kind=kind,provenance='U',fixture='fixtures.json#BC-OWNED',preconditions=['common','active-positive-guard'],setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,unknown=contract,evidence=[]))
dump('requirements.json',requirements);dump('cases.json',cases)
dump('fixtures.json',dict(id='BC-OWNED',status='Future finite owned setups; no catalog/account/hardware/media/reference result provided',common='Retain exact build/platform/capabilities, readable valid owned files with bytes/format/duration/tags, independently completed indexing/analysis, current Library/Places paths and source identities, Browser query/filter/selection/focus/layout/IME/key preferences and Computer MIDI Keyboard, visible controls, transport/rate and actually accepted values. Reset per trial. Service contexts additionally require independently authorized genuine account/catalog/network and, for Push, genuine supported Push3 Standalone hardware/firmware. Neither a label nor tool availability supplies them.',
    setups={'local':'Two indexed readable owned items with shared/distinct tags and known positive search/label/collection paths; separate custom/factory metadata and supported preset/sample types.','service':'Independently valid permitted catalog/account/source and separately authorized future service investigation only; no account, credentials, confirmation, requests, install, download, upload, sharing or transfer provided/executed.','audio':'Valid nonzero owned preview/reference sample and eligible active instrument/device/cue path; nonzero gain/amount and nonmuted output/wet return, exact Warp/Raw/scale/loop settings.','push':'Independently accepted actual Push3 Standalone firmware/network/paired catalog; Push1/2 or a generic controller cannot substitute.'},
    **{'active-positive-guard':'Before any no-result/disabled/no-effect claim independently establish readable eligible nonempty owned content, completed positive indexing/analysis or usable authorized catalog/account/hardware capability, correct focus/path/selection/settings and an actual working paired positive response. Audible/reference paths require valid nonzero source, enabled eligible processing, nonzero gain/amount and nonmuted cue/return/output with matched positive baseline. Missing input/account/hardware/service/control or failed baseline leaves U, never pass.','not_provided':['No actual Browser/native/candidate/audio/MIDI/hardware runtime','No network login/account/Cloud/Splice request, Pack install/download or Push transfer','No embedding/scoring/ranking/RNG/protocol/credential/file algorithm or acceptance tolerance']},original_execution=False,candidate_comparison=False))
owner_paths=['wiki/specs/'+s+'.md' for s in ['browser-workflows','browser-index','project-media-workflows','media-file-workflows','clip-view-workflows','settings-learning-workflows','keyboard-navigation','device-racks','device-simpler','synthesis-instruments','plugin-discovery','tuning-systems','groove-workflows','midi-editing-tools','routing-monitoring-latency']]
owner_paths += ['wiki/research/browser-workflows.md','wiki/research/browser-index-static.md','analysis/ableton-live-12.4.3/full-spec-v1/reviews/governance-browser-review.json','analysis/ableton-live-12.4.3/full-spec-v1/browser/manual-browser-2026-10-19.html','analysis/ableton-live-12.4.3/full-spec-v1/browser/capture.json','analysis/ableton-live-12.4.3/full-spec-v1/browser/source-manifest.json','analysis/ableton-live-12.4.3/full-spec-v1/arrangement/manual-concepts.html','analysis/ableton-live-12.4.3/full-spec-v1/arrangement/concepts-source.json','analysis/ableton-live-12.4.3/full-spec-v1/session-workflows/capture.py']
owner_paths += ['handoff/browser-index-v1/'+n for n in ['README.md','spec.md','REVIEW.md','manifest.json']]
dump('owner-pins.json',[dict(path=n,**pin(ROOT/n)) for n in owner_paths])
release=ROOT/'handoff/browser-index-v1';rm=json.loads((release/'manifest.json').read_text());rf=rm['files']
entries=rf if isinstance(rf,list) else [dict(path=n,**v) for n,v in rf.items()]
for e in entries:
    q=release/e['path'];assert pin(q)==dict(bytes=e['bytes'],sha256=e['sha256'])
dump('release-boundary.json',dict(release='browser-index-v1',payload_hashes_checked=len(entries),finite_only=True,UI_analysis_or_service_parity_inferred=False))
counts=dict(requirements=len(requirements),requirement_provenance=dict(Counter(r['provenance'] for r in requirements)),cases=len(cases),case_provenance=dict(Counter(c['provenance'] for c in cases)),case_kinds=dict(Counter(c['kind'] for c in cases)),source_blocks={'Browser':268,'SoundSimilarity':6},documentary_visible_proposals=sum(c['documentary_expected'] is not None for c in cases),documentary_null_cases=sum(c['documentary_expected'] is None for c in cases),all_target_null_U_unexecuted=True)
dump('counts.json',counts)
base='../../analysis/ableton-live-12.4.3/full-spec-v1/browser-content/'
spec='''---
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

[Future fixtures](REPLACEfixtures.json) require independently valid owned eligible
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

'''.replace('REPLACE',base)
for r in requirements:
    spec+=f"### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
    if r['evidence']:spec+='Evidence: '+', '.join(f"`{e['block']}` (#{e['anchor']}, HTML{e['html_line']})" for e in r['evidence'])+'.\n\n'
spec+=f'''## Finite cases and open obligations

[{len(cases)} cases]({base}cases.json) cover{len(requirements)} requirements ({len(rows)} D12/{len(unknowns)} U).
No future recipe is a result or exhaustive feature/profile coverage.

| Case | Requirement | Kind / finite action |
| --- | --- | --- |
'''
for c in cases:spec+=f"| {c['id']} | {c['requirements'][0]} | {c['kind']}: {c['setup_and_action']} |\n"
spec+=f'''
## Analysis-only evidence and freeze

[Source ledger]({base}sources.json) pins exact reused captures: Browser334122bytes
SHA256 `4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3`,
UTC2026-10-19T19:56:28.639468+00:00; Concepts306807bytes
SHA256 `da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`,
UTC2026-10-19T19:53:41.813664+00:00. [Browser268 blocks]({base}source-blocks.json)
and [Similarity6 blocks]({base}similarity-blocks.json) retain exact anchors/HTML lines.
Only Concepts sound-similarity section was selected; no whole-Concepts contract.
[Owner/reuse pins]({base}owner-pins.json), [counts]({base}counts.json),
[manifest]({base}manifest-author-r1.json) and canonical snapshots freeze the partial
packet. Current website prose is not immutable12.4.3 evidence. Shared catalogs,
coverage/questions/log and independent review are integrated separately by root.
'''
research='''---
id: RESEARCH-BROWSER-CONTENT-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; current Version12 applicability U
---

# Browser content and service evidence

The [canonical draft](../specs/browser-content-workflows.md) follows the
[full coverage plan](full-live-specification-plan.md). Existing
[Browser workflow evidence](browser-workflows.md) and [index research](browser-index-static.md)
remain authoritative for their selected interactions and finite sidecar boundary.
All268 Browser text blocks/headings and six Concepts Sound Similarity blocks were
read. Figures and linked help/media were not inspected. No source fetch was needed.

## Exact retained identities

[Sources](REPLACEsources.json) keeps original UTC/URLs/bytes/hashes and reuse paths.
Browser chapter334122bytes SHA256
`4e34895d5d37d6579e29cb65156b83c53672e89bd01b3bd8233596fc5b17e8b3`
was captured2026-10-19T19:56:28.639468+00:00; Concepts306807bytes SHA256
`da51ae19eab185813aac3b4240b7fad6022885421a3794155ca1207fd6e2eed5`
was captured2026-10-19T19:53:41.813664+00:00. Local exact copies are not new captures.
The existing guarded Session chapter parser is reused only as pure text extraction.
Browser BC-B001..268 covers the complete chapter; SIM-B001..006 selects exactly
the Concepts #sound-similarity section with original line/heading context.
All pre-author source/derived bytes are pinned unchanged. Publication is Version12,
without immutable patch/build/firmware/account feature applicability.

## Interpretation and questions

- Q-BC-001: ordinary search/clear/history/membership/preview/import and folder
  nonrelocation/dimmed unavailable state stay with existing Browser Workflows.
  Tag query/selection suggests narrowing but supplies no complete tag boolean,
  parser/Unicode/collation/tie or result-ranking algebra. Per-label filter recall
  is not restart persistence; a saved result label may need dynamic/snapshot study.
- Q-BC-002: factory/custom/auto tags are distinct. BC-B058 periodic analysis and
  up-to60-second samples, VST3 subcategory mapping BC-B060 and SIM-B006 background
  status give no classifier/model, exact eligibility, scan cadence or file-format
  law. Exact index fields/precomputed features are not an embedding specification.
  Sidecar color/tag/binding bytes retain their released owner, not UI inference.
- Q-BC-003: local Similarity Search compares Core/User Library with compatible
  samples/presets and descriptive most-to-least ordering. This differs from
  Splice Search with Sound's clip/time-selection service and reported50 results.
  Neither yields scores, thresholds, exact order/neighbors, RNG or sound identity.
  Clip View042 retains its own Show Similar Files entry; device swaps stay owned.
- Q-BC-004: Packs installed/Updates/Available/download/install/delete are content
  workflow roles distinct from project-Pack create/restore. Positive known catalog,
  account/permission, bytes and capacity are prerequisites. No queue, progress,
  resume/retry, install/update/deletion transaction, rights or partial-file law.
  Pack Info source typically includes creator/tutorial but Core Library lacks it.
- Q-BC-005: Splice Home and logged-out versus logged-in controls do not establish
  protocol or account availability. Source royalty-free/automatically licensed/
  certified-license language is retained context without legal interpretation.
  Free-account catalog counts, Search with Sound50 and defaults are version/service
  dependent, not target outcomes. Browser Collections and Splice Collections are
  different scopes. No public share, account edit, signup/login or download ran.
- Q-BC-006: source says Cloud holds up to eight Move/Note Sets and syncs into Live,
  not back. These are current source contexts, not a quota or capability guarantee.
  User Library/ABL Assets access and Collect All and Save retain file/collection
  owners. Accessible labels do not establish usable assets or accepted Set versions.
- Q-BC-007: Push source is explicitly Push3 Standalone on same Wi-Fi, not Push1/2
  controller mode. Named device, six-digit pairing prose and refresh/Disconnect
  controls supply no packet/code codec or firmware/standalone completeness.
  Native/frozen-plugin/collected prerequisites do not prove arbitrary portability.
- Q-BC-008: Library folder names and current Project Backup descriptions give
  discovery locations, not new serialization, relocation, retention/trash/restore
  or dependent-copy rules. BC-B211 conditions copy on Collect Files on Export;
  BC-B222's unqualified preset-sample wording does not override Project Media019.
  Default paths/visibility/location controls stay Settings-owned. Missing files,
  Pack removal and copy/move/restart outcomes remain U under their owners.
- Q-BC-009: native Raw/scrub/explicit-preview gestures and Splice preview controls
  are separate. No source up-to-next-bar/loop/key/scale/loudness description provides
  sample identity, decode/gain/Warp/timing or reference-audio criteria. Preview tests
  need actual nonzero content, active cue path and a matched positive baseline.

Root owns canonical question-register integration; local U requirements preserve
all unresolved contexts. No user account, service request, Pack installation,
Cloud/Push transfer, native/browser/runtime/hardware/candidate execution, tooling
installation or private algorithm implementation occurred.

## Freeze and remaining evidence

Requirements/cases retain all target expected/comparison null, gradeU and unexecuted.
Visible controls/entry/selection proposals are separate from null signal/timing/
protocol/numeric/RNG/similarity/file/analysis outcomes. Source_claim is not an oracle.
Finite future fixtures require independently valid owned content, completed index/
analysis or genuine authorized service/hardware/catalog, accepted controls and
focus/preferences. Missing capability is U, never a negative pass. Audible paths
require active eligible processing, nonzero source/gain/amount and nonmuted cue/
return/output with paired positive baseline.

[Owner pins](REPLACEowner-pins.json), original source metadata, finite release pins
and [manifest](REPLACEmanifest-author-r1.json) are hash checked. Browser-index-v1
payloads remain unchanged; its finite laws are not broadened. Exact browser ID
equality includes U clauses. Read-only post-seal validation checks hashes/source
blocks, cases/nulls, owners/releases, snapshots, links and untracked whitespace.
Run `python3 -B analysis/ableton-live-12.4.3/full-spec-v1/browser-content/validate.py`.
Separate semantic review is required. Shared indexes/coverage/log remain root-owned.
No entire Browser/Cloud/Splice/Pack/Push/controller family is complete.
'''.replace('REPLACE',base)
for folder,name,text in [('specs','spec-r1.md',spec),('research','research-r1.md',research)]:
    path=ROOT/'wiki'/folder/'browser-content-workflows.md';assert not path.exists();path.write_text(text);(P/name).write_text(text)
print(json.dumps(counts,indent=2))
