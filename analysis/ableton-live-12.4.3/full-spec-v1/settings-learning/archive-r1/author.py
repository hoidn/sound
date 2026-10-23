"""Author bounded settings/Learn/Info proposals; no original program execution."""
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
ROOT=P.parents[3]
blocks={r['id']:r for r in json.loads((P/'source-blocks.json').read_text())}
DATA=[
('Learn content and resources','Learn View provides structured modules with video and explanatory text; modules can be added without a Live update. Its home page links to the manual and Knowledge Base. Available lesson catalog, delivery service, download/cache and authenticity protocol remain unknown.',[8],'With known available lesson content and working connection, open Learn home, inspect modules/text/resource entries, and record exact catalog/content identity.','control'),
('Learn entry and in-session page retention','Close Learn with its X and reopen from Help or Ctrl+Alt+7 Windows/Cmd+Option+7 macOS. Before Live closes, reopening returns to the last visited page. First-open default visibility is documentary only, not an observed target constructor default; application-restart restoration remains unknown.',[9],'Visit a nonhome lesson, close and reopen Learn using each documented entry separately without closing Live; use explicit platform/focus.','state'),
('Lesson filter, completion and navigation','Lessons can be filtered by topic and marked completed. Complete Lesson gives a home-page check mark. Lesson Home or < Lessons returns home; bottom related-lesson links are described only when home shows all lessons. Completion persistence across application/reinstall/account contexts is unknown.',[10,11,12],'With two distinct available lessons, explicitly choose all lessons, filter a topic, mark one complete and inspect the home indication; compare related links with home filtered versus all.','control'),
('Lesson player controls','The lesson player offers play/pause, progress scrubbing, volume, subtitles and picture-in-picture controls. This lists named public controls, not decoder support, actual video/audio output, subtitle languages or timing precision.',[13],'Open a known available lesson video; inspect and operate each offered control in separate reset trials. Independently confirm actual content/output before any future silence or playback assertion.','control'),
('Picture-in-picture window transitions','Opening lesson picture-in-picture closes Learn and allows window movement/resizing. Its X closes it; Learn View arrow reopens Learn and closes picture-in-picture. The source describes always above application windows, including other apps; the arrow then brings Live into focus. OS permissions, exclusive/fullscreen conflicts and geometry persistence remain unknown.',[14,16,17],'On an identified supported OS open lesson picture-in-picture, move/resize, switch to an owned second application and use Learn View arrow. Repeat X separately; record focus/windows without a pixel oracle.','control'),
('Lesson playback position and seek roles','Within picture-in-picture, hover exposes progress and backward/forward 15 controls. While Live remains open the lesson video resumes from the prior position, even after closing either view during playback. Exact seek interval units, endpoint rounding, transport ordering, audio/video timing and decoder output are not calibrated here.',[15],'Establish active positive lesson playback at a known interior landmark, hover controls, invoke each 15 seek separately, then close/reopen views while Live stays open and record source position.','timing'),
('Learn connectivity and reload','Learn View requires an Internet connection. Following loss and reconnection, Reload refreshes it. The text does not establish offline-cache behavior, authentication, network error text, retry policy or recovery deadline.',[18],'First confirm lesson content loads over a known usable connection, interrupt and restore only that connection in an owned future setup, then use Reload and record displayed state.','control'),
('Info View contextual help and visibility','Info View displays the hovered UI element name/function. Its bottom-left view toggle or ? key shows/hides it. Exact help strings, keyboard-layout/focus conflicts, hover delay and accessibility announcements are unknown; global key context remains with keyboard navigation.',[20,21],'Explicitly focus ordinary Live UI with no text editor or mapping mode active; inspect hover help for two known controls and toggle Info View by the view control and ? separately.','control'),
('Track and device Info Text entry points','Track/device context-menu Edit Info Text opens editable notes in Info View; the chapter describes notes saved/displayed with the Set. Clip Edit Info Text remains owned by REQ-CLIP-VIEW-004, not duplicated here. Text codec/limits, undo and exact persistence/error transactions remain unknown.',[22],'In an owned disposable Set, use a track and a device context menu separately, enter distinct safe notes in Info View, then save/reopen to propose inspecting their display. Use Clip View owner for clips.','state'),
('Platform Settings entry','Settings opens from Options on Windows or Live menu on macOS, or Ctrl+, Windows/Cmd+, macOS. Keyboard traversal/close/page shortcuts and preferred-language selection remain with keyboard-navigation; no crossplatform key equivalence is inferred.',[28,29],'Record OS and ordinary focus, then open Settings from the platform menu and documented shortcut in separately reset trials; inspect named window only.','control'),
('Window zoom roles','Display settings offer separate zoom for main window, second window if open, and Settings window. Mouse adjustment of Settings zoom updates after mouse-button release. Offered range, scale arithmetic, permonitor layout and persistence are unknown; preferred language belongs to keyboard-navigation.',[32],'Open a second window only where supported; adjust each offered zoom separately. For Settings zoom retain pointer-down/move/release sequence and inspect update point, without pixel or latency threshold.','control'),
('Display option roles','Display Options includes Outline View in Focus, scrollbar presentation, Arrangement/clip Follow and UI-label visibility. Enabling Outline draws a border around the selected view. Exact option enums and underlying Follow navigation/transport behavior remain with relevant view owners or unknown.',[33],'With identifiable selected views and explicit transport, inspect available display options, enable Outline and switch selection, then vary scrollbar/label options separately. Do not infer a Follow scrolling law.','control'),
('Mouse and pen settings','Mouse and Pen Input exposes Pen Tablet Mode, permanent scrub areas and pitch-locked MIDI drawing options. Actual pen protocol, gesture thresholds, scrubbing audio and note drawing remain with editing owners or unknown.',[35],'Inspect these offered settings with a known input device, toggle one at a time and record control state. Use Clip View/MIDI editor for actual drawing/scrub behavior.','control'),
('Suppressed warning restoration','Application Options can restore warning dialogs previously suppressed through Don\'t Show Again. The warning set, exact dialog text, perwarning/global scope, account and restart retention remain unknown.',[36],'Using an owned reversible action, first retain a known offered warning and suppress it, confirm its absence on repetition, then restore warnings and repeat that same action.','control'),
('Theme and appearance controls','Theme offers a color scheme, light/dark or OS-follow appearance, warm/cool/neutral palette tone and high contrast. Customization adjusts grid opacity, brightness, color intensity and hue. Numeric ranges, color values, assets and OS-change propagation timing remain unknown.',[39,40],'On an identified OS explicitly choose each offered appearance/tone mode separately and inspect control states; change OS theme only in a future owned setup, retaining settings and no pixel comparator.','control'),
('Track and clip color preferences','Track and Clip Colors controls automatic track colors, a default track color and Reduced Automatic Colors. Clip Color may choose random colors or track color for new clips. No palette enumeration, random distribution or color-sequence oracle follows. This preference context qualifies the Clip View new-clip inheritance wording; matched target resolution remains unknown.',[41],'With explicit safe palette and new empty tracks, choose automatic/default/reduced options separately. For new clips compare explicit track-color mode against random mode in separate histories; do not assume every random result differs or infer probability.','control'),
('Audio device and system-output settings','Audio settings expose input/output devices, sample rate/latency and calibration testing. The source describes macOS CoreAudio and Windows driver selection/driver-owned management, recommending ASIO without prohibiting other drivers. macOS Use System Device follows the OS Sound output choice. Accepted devices/drivers/rates, fallback and transition artifacts remain unknown.',[43,44,45],'With independently supported interface and active nonzero output, inspect offered device/rate/latency/testing controls. In a separate macOS setup select Use System Device and switch between two known working OS outputs; retain positive baselines and no latency/audio oracle.','control'),
('Library settings and Places labels','Library settings choose default Pack/User Library locations and dependent-file copying when moving clips/tracks/presets to Browser. They also show/hide Cloud, Push and Splice Places labels. General file-copy/project and Browser operations remain with existing owners. Visible labels do not establish service availability, credentials, cloud protocol or target feature presence.',[64],'Inspect offered Library locations/copy setting and explicitly show/hide each available Places label, retaining Browser presentation. Do not perform online login, Pack install or file movement as part of this documentary packet.','control'),
('Licenses and Updates settings category','The chapter identifies Licenses and Updates settings for authorization, automatic updates and usage data. It supplies no detailed command surface, default consent, telemetry payload, update protocol, rollback or entitlement rules; those remain required unknowns.',[70],'Inspect the named settings category on an identified authorized target, retaining offered controls only. Do not change license, consent, install or update anything as part of this packet.','control'),
]
GAPS={
 'DELIVERY':('Installation, authorization and update operations','Installation/authentication/license entitlement, online/offline authorization, usage-data consent and telemetry, update/download/install/rollback, OS permissions and recovery remain required unknowns. SET-B003 is a source pointer and publisher licensing prose, not a new independently interpreted license contract.',[
 ('INSTALL','In a future separately authorized disposable OS setup retain installer identity, supported platform, permissions, failure/cancel and resulting files; this packet installs nothing.'),
 ('AUTH','Use an independently authorized test account/entitlement only in a separately authorized future investigation; enumerate online/offline/deauthorization/unavailable-network state and error transitions without publishing credentials.'),
 ('UPDATE','Retain current and offered package versions, update/usage-data controls and explicit consent states; independently investigate cancel/restart/failure/rollback without assuming helper topology or applying an update.')]),
 'LIFECYCLE':('Settings, help and media lifecycle','Malformed/boundary input, unavailable content/device, cancel/undo/persistence/restart, focus/mapping conflicts, monitor/rate changes and teardown remain unknown.',[
 ('BOUNDARY','Use offered zoom/theme/name/path bounds and invalid or unavailable paths in separate owned setups, recording clamp/reject policy without presupposing it.'),
 ('UNDO','Change a setting, lesson completion or Info Text and invoke Undo/Redo only where offered; record actual command availability and state.'),
 ('CANCEL','Cancel an offered path/device/settings/content dialog separately and inspect retained settings and partial resources; no rollback policy is assumed.'),
 ('PERSISTENCE','Save/reopen two owned Sets, restart application and separately change user profile in an admitted setup; distinguish Set-specific Info Text from global preferences, content/progress and window state.'),
 ('LOSS','After positive available content/device/path baseline, remove only that dependency or connectivity and restore it; inspect reload/relink/fallback without a deadline.'),
 ('FOCUS','Use text-edit focus, map mode, alternate keyboard layout and OS-reserved shortcuts separately; record routing/conflicts and screen-reader access rather than assuming global handling.'),
 ('RATE','Change accepted audio rate, system output, window zoom and monitor scale separately while lesson playback and independently active Set audio are present; signal/glitch/latency comparator remains null.'),
 ('TEARDOWN','Close lesson/PiP/Settings, Set and application during pending content load or offered settings operation in separate trials; retain prompts, playback and files without leak/cleanup claims.')])}
reqs,cases=[],[]
for i,(title,contract,refs,action,kind) in enumerate(DATA,1):
 rid=f'REQ-SETTINGS-LEARNING-{i:03d}'
 evidence=[dict(block=f'SET-B{n:03d}',anchor=blocks[f'SET-B{n:03d}']['anchor'],html_line=blocks[f'SET-B{n:03d}']['html_line']) for n in refs]
 reqs.append(dict(id=rid,title=title,contract=contract,strength='D12',target_applicability='U',evidence=evidence))
 cases.append(dict(id=f'SET-{i:03d}',requirements=[rid],kind=kind,fixture='fixtures.json#SET-OWNED',setup_and_action=action,source_claim=contract,documentary_expected=contract if kind in {'control','state'} else None,documentary_comparator='Named visible controls/state relationship only; no pixel, audio, timing or service protocol result.' if kind in {'control','state'} else None,expected=None,comparison=None,target_grade='U',executed=False,evidence=evidence))
for group,(title,contract,probes) in GAPS.items():
 rid='REQ-SETTINGS-LEARNING-U-'+group;reqs.append(dict(id=rid,title=title,contract=contract,strength='U',target_applicability='U',evidence=[]))
 for suffix,action in probes:
  cases.append(dict(id='SET-U-'+suffix,requirements=[rid],kind=suffix.lower(),fixture='fixtures.json#SET-OWNED',setup_and_action=action,source_claim=None,documentary_expected=None,documentary_comparator=None,expected=None,comparison=None,target_grade='U',executed=False,evidence=[]))
assert len(reqs)==21 and len(cases)==30 and len({c['id'] for c in cases})==30
def save(name,value):
 raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode() if not isinstance(value,str) else value.encode();p=P/name
 assert not p.exists() or p.read_bytes()==raw,name
 p.write_bytes(raw)
save('requirements.json',reqs);save('cases.json',cases)
helper=P.parent/'session-workflows/capture.py'
save('dependencies.json',[dict(path=str(helper.relative_to(ROOT)),bytes=helper.stat().st_size,sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),role='existing analyst chapter_content parser, no original code')])
save('fixtures.json',dict(id='SET-OWNED',status='future owned setup; no content/media/hardware/account/UI results supplied',setup='Disposable editable Set with distinct track/device notes and safe owned media. Record exact OS/build, installed feature/lesson content availability, input devices/keyboard layout/focus, preferences and active transport/audio, network state and optional supported second monitor/output. Explicitly set preferences instead of relying on defaults. Distinguish authenticated online content from independently available local lesson entries.',positive_guard='Confirm the relevant control/content/device/dialog/output path works first; then vary only the named condition. A hidden view, missing lesson, silent input, zero gain, absent permission or unsupported option is not a passing negative test. No network/account/license/update/install/audio operation is performed by this packet.',scope='Window/control/source-role proposals only. Use separately authorized owned disposable contexts for any future install/account/OS-changing probe. Protect credentials and immutable evidence. All target12.4.3 outcomes remain unknown.'))
front='---\nid: {id}\ntype: {type}\nstatus: {status}\nupdated: 2026-10-19\naccess: analysis\nrevision: 1\ntarget: Ableton Live 12 Suite 12.4.3\n---\n\n'
spec=front.format(id='SPEC-SETTINGS-LEARNING-WORKFLOWS',type='spec',status='draft')+'''# Settings, Learn View and Info View workflows

This partial F-07/F-08 contract owns newly documented settings/help entry points,
appearance and Learn/Info View roles. The [coverage design](../research/full-live-specification-design.md)
governs closure; [research](../research/settings-learning-workflows.md) owns exact
evidence. It is not a complete preference, delivery or learning-content contract.

**D12/target-U:** the captured current Version12 chapter supports documentary
prose only. All exact12.4.3 outcomes/comparisons, including Learn View and newer
settings/Places availability, remain null/U/unexecuted. No figures, UI, content,
audio/video, network/account, installer/update, native code or candidate ran.
Named UI roles do not prove content availability or private service behavior.

## Canonical boundaries

[Keyboard navigation](keyboard-navigation.md) owns preferred language, focus,
Tab/Wrap/arrow options and settings traversal. [Clip View](clip-view-workflows.md)
REQ004 owns clip Info Text; REQ005's new-clip inheritance wording needs the explicit
Clip Color preference context below. [Session](session-view-workflows.md) retains
its particular entry points. This page adds only track/device notes and general
Info View presentation. No existing sealed owner is silently revised.

[Media](media-file-workflows.md) owns analysis files, destructive Sample Editor
and decoding cache; [recording](recording-comping.md) owns temporary recordings
and format defaults; [project/media](project-media-workflows.md) owns file/project
operations and library content. [Max host](max-for-live-hosting.md),
[plug-in hosting](plugin-hosting.md), [routing](routing-monitoring-latency.md),
[synchronization](synchronization-workflows.md), [clip launch](session-launch-workflows.md)
and [Warp](warp-markers.md) retain their settings behavior. The chapter's tab
summaries route to those owners rather than duplicate their contracts.

## Requirements

Use [future owned setups](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/fixtures.json)
with explicit feature availability/focus/preferences and paired positive baselines.
Compound clauses remain partial until each branch, state and required case kind
has evidence. Numeric/color/RNG/time/audio/codec comparisons remain unknown.

'''
for r in reqs:
 spec+=f"### {r['id']} — {r['title']}\n\n**{r['strength']}/target-U.** {r['contract']}\n\n"
 if r['evidence']:spec+='Evidence: '+', '.join('`'+e['block']+'`' for e in r['evidence'])+'; [exact routes](#analysis-only-evidence).\n\n'
spec+='''## Source-context question

**SET-U-CLIP-COLOR:** SET-B041 permits new-clip random color or track color;
REQ-CLIP-VIEW-005 describes track-color inheritance without that preference.
Retain both exact source contexts. Do not infer a contradiction, silently change
the sealed Clip View owner, or use a random-result inequality as an oracle.
Matched version/preference evidence and a separately reviewed successor are needed.

## Finite acceptance proposals

[30 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases.json)
cover19documentary source roles and11operational U probes for21requirements
(19D12/2U). The lesson timing case has null documentary output/comparator;
all30target expected/comparison fields are null/U/unexecuted. No future fixture
is supplied content or a result. Installation/authorization/update operations
remain U; licensing prose is not independently interpreted as a legal contract.

## Analysis-only evidence

'''
source=json.loads((P/'source.json').read_text())
spec+=f'''Official [Version12 First Steps]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/{source['file']}).
[70 blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json)
retain chapter anchors/HTML lines; figures uninspected, current-site revision
and exact12.4.3 applicability unknown. The existing analyst parser is pinned
in dependencies.json. [Requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements.json)
and [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r1.json)
freeze this partial analyst draft, not implementation inputs or a release expansion.
'''
research=front.format(id='RES-SETTINGS-LEARNING-WORKFLOWS',type='research',status='current')+f'''# Settings and learning evidence

The [canonical draft](../specs/settings-learning-workflows.md) follows the
[execution plan](full-live-specification-plan.md). No original application,
learning service/video, installer, account, update, hardware or candidate ran.

## Source identity

Official [Version12 First Steps]({source['url']}), captureUTC
{source['capture_utc']}, {source['bytes']}bytes, SHA-256 `{source['sha256']}`;
[exact retained HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/{source['file']}).
The current website names Version12, not an immutable publication revision or
the exact12.4.3 build. New Learn View/setting/Places availability remains U.
The separate web reading view is not this byte identity. Only chapter_content
was parsed with the existing pinned Session analyst parser. The
[70 retained blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/source-blocks.json)
preserve anchors/HTML lines; figures and glyph image labels were not inspected.

## Interpretation, questions and ownership

Learn is network-dependent and source-described in-session page/video retention
does not establish restart/cache/account-progress persistence. Player control
presence and picture-in-picture z-order/focus roles give no decoder, audio,
subtitle, image or timing oracle. The 15 seek labels are not calibrated interval
or boundary tests. New lessons without application update gives no service schema.

Info View hover/visibility is distinct from clip notes. Existing Clip View owns
clip Edit Info Text; this adds track/device entry points only. The source's
note-save prose does not establish encoding, limits, error handling or atomicity.
Keyboard focus/layout/navigation remain separate prerequisites and owners.

SET-U-CLIP-COLOR retains the new-clip random/track preference from SET-B041
alongside existing REQ-CLIP-VIEW-005 track-color wording. Both sources need
matched version/preference context before any correction. No random inequality,
probability distribution or default palette is inferred. Existing sealed bytes
are preserved. Other chapter tab summaries are routed to canonical owners.

Audio driver recommendations are not prohibitions or proof every CoreAudio/ASIO
device works. Use System Device is a named macOS output role, without a failover,
resampling, latency or hot-swap law. Library Places label visibility is not an
authenticated cloud/Push/Splice feature or supported-service matrix.

Installation/authentication/authorization/update/usage-data prose only identifies
public routes/categories. The publisher license summary is context, not a legal
interpretation or algorithm. No new installer, license, telemetry, update or
rollback contract follows; separate public-source/exact-platform evidence is needed.

## Review and remaining evidence

[21 requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/requirements.json)
cover19D12roles/2U obligations; [30 cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases.json)
retain19documentary proposals and11U probes. All target outcomes are null/U;
signal/time/numeric/codec/color/encoding and lifecycle outcomes remain unknown.
Future owned configurations/content are not retained stimuli or measured results.
The [author seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r1.json)
supports independent partial-scope review only. Full preferences/help/delivery,
settings serialization, accessibility, services and target applicability remain open.
'''
for name,text,canonical in [('spec-r1.md',spec,'wiki/specs/settings-learning-workflows.md'),('research-r1.md',research,'wiki/research/settings-learning-workflows.md')]:
 path=ROOT/canonical;assert not path.exists() or path.read_text()==text
 path.write_text(text);save(name,text)
print('21 requirements /30 cases authored; freeze/check separately')
