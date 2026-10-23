"""Create bounded Settings case successor once; original sources and catalogs immutable."""
from pathlib import Path
import hashlib
import json
import shutil

P = Path(__file__).resolve().parent
R = P.parents[3]


def main():
    assert not (P / 'manifest-author-r2.json').exists(), 'Sealed successor; refuse author writes'
    read = lambda p: json.loads(p.read_text())
    info = lambda p: dict(bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    oldmanifest = read(P / 'manifest-author-r1.json')
    assert hashlib.sha256((P / 'manifest-author-r1.json').read_bytes()).hexdigest() == '0c4d506425f34a330e7f668563c63824be3746407ff00d358f5bf4df5fc4509c'
    originals = list(oldmanifest['files']) + ['manifest-author-r1.json']
    archive = P / 'archive-r1'
    archive.mkdir(exist_ok=True)
    for name in originals:
        if name in oldmanifest['files']:
            assert info(P / name) == oldmanifest['files'][name]
        destination = archive / name
        assert not destination.exists() or destination.read_bytes() == (P / name).read_bytes()
        shutil.copyfile(P / name, destination)
    old = read(P / 'cases.json')
    cases = json.loads(json.dumps(old))
    updates = {
        'SET-001': ('With independently available lesson content and working connection, inspect named modules/video/text on Learn home and each manual and Knowledge Base resource entry separately. Retain exact content/catalog and offered link identity; external destination, YouTube playlist and no-application-update content delivery remain ungraded source context.', ['modules/video/text', 'manual resource entry', 'Knowledge Base resource entry']),
        'SET-002': ('Visit an identified nonhome lesson, close Learn with its offered X, then reopen through Help and the exact platform shortcut in separate reset trials while Live stays open. Record Windows Ctrl+Alt+7 or macOS Cmd+Option+7 and ordinary focus. Inspect the returned page. First-open and application-restart histories are separate U observations, never supplied defaults.', ['Windows Help', 'Windows Ctrl+Alt+7', 'macOS Help', 'macOS Cmd+Option+7']),
        'SET-003': ('Use two independently available lessons. Retain separate all-lessons and topic-filtered home histories, mark one complete and inspect its home indication and related-link presentation. In reset nonhome histories invoke Learn View Home Page and < Lessons separately. Exact strings, catalog/progress persistence and linked destination behavior remain unknown.', ['all lessons', 'topic-filtered lessons', 'Complete Lesson/home indication', 'Learn View Home Page return', '< Lessons return']),
        'SET-004': ('With independently available video/content, inspect and operate play/pause, progress scrub, volume, subtitles and picture-in-picture in separate reset trials. Establish genuinely active playback and productive nonzero audio before pause/volume absence observations. Named controls only have documentary roles; actual video/audio/subtitle/seek outcomes remain ungraded.', ['play/pause', 'progress scrubbing', 'volume', 'subtitles', 'picture-in-picture']),
        'SET-005': ('From a known visible available lesson window, open picture-in-picture and inspect Learn closing, movement and resize roles. Explicitly hover PiP before using X. Separately use Learn View arrow while Live is focused and while over another owned application; retain focus, Learn/PiP visibility and exact OS. Geometry, fullscreen/monitor/privilege and playback consequences remain unknown.', ['PiP opens/Learn closes', 'move', 'resize', 'hover then X', 'Learn arrow with Live focused', 'Learn arrow over other application']),
        'SET-006': ('Establish genuine active lesson playback at an independently known interior landmark. Hover PiP controls and invoke each 15 seek separately. In separate histories close Learn during playback or close PiP during playback, leave Live open and return to the same lesson. Retain actual positions without inferred seek units, rounding, resumption deadline, decoder or timing comparator.', ['backward 15', 'forward 15', 'Learn closed during playback/Live stays open', 'PiP closed during playback/Live stays open']),
        'SET-015': ('On an independently supported identified OS choose each offered theme/appearance/tone and high-contrast control separately. Independently vary grid opacity, brightness, color intensity and hue one at a time. Retain offered controls/settings; OS-follow transition, numeric limits, rendered colors/pixels and persistence remain unknown.', ['theme', 'light', 'dark', 'follow OS', 'warm', 'cool', 'neutral', 'high contrast', 'grid opacity', 'brightness', 'color intensity', 'hue']),
        'SET-016': ('With explicit palette and owned new empty tracks, choose automatic/default/reduced color settings separately. Retain explicit track-color versus random Clip Color histories before creating new clips. Preserve Q031 and matched source/preference/version context; neither every random result differing nor a sequence/distribution/default/unconditional inheritance is assumed.', ['track auto colors on', 'track auto colors off', 'default color', 'Reduced Automatic Colors', 'new clip track-color mode', 'new clip random-color mode']),
        'SET-017': ('With independently supported productive interface/output, inspect offered device/rate/latency/testing controls. On a separately admitted macOS setup inspect Driver Type and Use System Device, then two known productive OS Sound outputs. On Windows separately inspect chosen driver and any offered driver-owned configuration entry. Existing installed supported choices only: no install, universal device support, ASIO-only, failover, audio/latency or transition result is presumed.', ['device/rate/latency/testing controls', 'macOS offered Driver Type', 'macOS Use System Device/two productive OS outputs', 'Windows chosen driver', 'Windows offered driver-owned configuration entry']),
        'SET-U-UNDO': ('From separately known reversible positive settings/lesson/Info Text baselines, inspect actually offered Undo and Redo independently for a setting, lesson completion and note edit. Record command availability, Set/global scope and retained state; no undo grouping, rollback or universal command support is presumed.', ['setting', 'lesson completion', 'track/device Info Text']),
        'SET-U-CANCEL': ('At an offered path/device/settings/content dialog before acceptance and while a genuine operation is pending where meaningful, inspect offered Cancel/close separately after a known successful positive baseline. Retain controls/resources/prompts; no cancellation availability, partial-output cleanup or rollback law.', ['before acceptance: offered Cancel', 'before acceptance: offered close', 'pending operation: offered Cancel if available', 'pending operation: offered close if available']),
        'SET-U-PERSISTENCE': ('After successful independently available controls/content/notes, use two owned Sets to distinguish Set-specific track/device Info Text from global settings, lesson progress/content and window state. Retain save/reopen, application restart and separately admitted profile histories independently; no persistence/default/account/cache law follows.', ['Set A save/reopen', 'Set B save/reopen', 'application restart', 'separately admitted profile history']),
        'SET-U-TEARDOWN': ('At visible idle, genuinely pending content load and pending offered settings-operation checkpoints, close Learn, PiP, Settings, Set and application separately where meaningful. Establish successful productive baselines first; retain prompts/playback/files without cleanup, leak, cancel, persistence or restore guarantees.', ['visible idle', 'pending content load', 'pending offered settings operation']),
    }
    for case in cases:
        case['fixture'] = 'fixtures-r2.json#SET-OWNED'
        if case['id'] in updates:
            action, contexts = updates[case['id']]
            case.update(setup_and_action=action, finite_contexts=contexts, refines_R1_case=case['id'])
    cases.append(dict(id='SET-U-AVAILABILITY', requirements=['REQ-SETTINGS-LEARNING-U-LIFECYCLE'], kind='availability', fixture='fixtures-r2.json#SET-OWNED', setup_and_action='Record independently known exact build/edition/platform and already available Learn/content/player/Info/settings/device controls. With a separately admitted and documented first-open history, inspect initial Learn visibility before manual opening. Retain profile/template/preferences/prior-session state; no reset/install/account/network operation is performed, no target constructor/default or failed-content outcome is predicted. Missing feature/history/positive baseline stays U.', source_claim=None, documentary_expected=None, documentary_comparator=None, expected=None, comparison=None, target_grade='U', executed=False, evidence=[], finite_contexts=['exact build/platform/edition', 'already available feature/content/control', 'separately admitted first-open history before manual opening']))
    assert len(cases) == 31 and len({c['id'] for c in cases}) == 31
    def save(name, data):
        assert not (P / name).exists(), name
        (P / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    save('cases-r2.json', cases)
    fixture = read(P / 'fixtures.json')
    fixture['positive_guard'] += ' Active input is not active operation. Before pause/volume/no-output observations retain genuine active lesson playback and productive nonzero audio; retain first-open histories separately from explicitly configured in-session tests.'
    save('fixtures-r2.json', fixture)
    delta = [dict(id=a['id'],old_pointer=f'/{i}/setup_and_action',new_pointer=f'/{i}/setup_and_action',old_action=a['setup_and_action'],new_action=b['setup_and_action'],finite_contexts=b.get('finite_contexts')) for i,(a,b) in enumerate(zip(old,cases)) if a['setup_and_action']!=b['setup_and_action']]
    save('delta-r2.json', dict(old_requirements_verbatim=21,shared_unchanged_requirement_catalog='requirements.json',old_cases_preserved=30,refined_actions=delta,new_case_ids=['SET-U-AVAILABILITY'],adopted_audit_groups=['G01','G02','G03','G04','G05','G06','G07','G08','G10','G11'],pending_external_owner_group='G09',actual_outcomes='all null/U/unexecuted'))
    pins = [dict(path=str((P/name).relative_to(R)),**info(P/name)) for name in originals]
    for name in ['settings-source-audit/manifest-r2.json','reviews/settings-source-audit-review.json']:
        q=P.parent/name;pins.append(dict(path=str(q.relative_to(R)),**info(q)))
    save('inputs-r2.json', pins)
    spec=(archive/'spec-r1.md').read_text().replace('revision: 1\n','revision: 2\n',1).replace('settings-learning/fixtures.json','settings-learning/fixtures-r2.json')
    oldaccept=spec[spec.index('[30 cases]'):spec.index('## Analysis-only evidence')]
    spec=spec.replace(oldaccept,'''[31 current cases](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r2.json)
refine the same21unchanged requirements (19D12/2U), preserving all30old IDs.
Explicit entry/return/player/PiP/resume/customization/driver/color and operational
contexts adopt ten reviewed retained-block audit groups. G09 exact cross-owner
reconciliation remains pending; owner links are not semantic coverage. Twelve
operational U cases include first-open/feature availability observations, with
no target default inferred. All31actual expected/comparison values remain null/U/
unexecuted; lesson timing and every operational U documentary oracle also stay
null. No movie/content/network/account/device/install operation was performed.
The unchanged requirements.json is shared by R1/R2; cases.json remains historical.

''')
    spec=spec.replace('and [author seal]', 'and [original author seal]')
    spec+='''
## Preserved source-audit successor

[Retained-block audit](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-source-audit/README-r2.md)
and [independent audit review](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-source-audit-review.json)
cover70old source blocks only; images, glyphs, captions outside that extraction
and linked destinations remain uninspected. [R2 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/delta-r2.json)
adds no normative law or ID. Original14files and exact archive copies remain
immutable. R4historical Settings pins resolve to original snapshots through the
[disclosed historical replay](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/r4-cohort-historical-replay.py).
No frozen old pin, review, catalog or output report is rewritten. The current
[R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r2.json)
awaits independent focused review; this remains a partial analyst draft.
'''
    research=(archive/'research-r1.md').read_text().replace('revision: 1\n','revision: 2\n',1)
    research=research.replace('## Review and remaining evidence\n', '## Original R1 review and remaining evidence\n\nThe following catalog counts and seal describe the preserved R1 partial review.\nCurrent case contexts are listed in the R2 section below.\n')
    research+='''
## R2 case-context adoption

The [independently reviewed70-block audit](../../analysis/ableton-live-12.4.3/full-spec-v1/reviews/settings-source-audit-review.json)
identifies scoped cases rather than whole-paragraph coverage. R2 retains every
one of the21original requirement records unchanged in requirements.json; current
[cases-r2](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/cases-r2.json)
retain30old IDs, refine13actions, and add one availability/first-open U action.
Ten groups adopt named local resource/entry/return/player/PiP/resume/display/driver/
color/operational contexts. G09 external-owner reconciliation remains pending,
including Sample Editor choice, hardware resync, plug-in folders and Max edition
conditions; those are not covered merely because the chapter routes to an owner.
Q031 color context remains open. First-open visibility is a documented source
claim with unknown target/history, never a constructor/default/restore guarantee.
Player pause/volume absence needs genuine running playback/nonzero output.

Eighteen named visible documentary roles and one null timing role remain only
source proposals; all12operational U and all31actual outcomes/comparators are
null/U/unexecuted. No figure/image/glyph, caption outside the70retained blocks,
linked destination, actual UI/content/player/device/file/service or lifecycle
result is supplied. R1 originally reviewed scope remains valid for its revision.
The [R2 delta](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/delta-r2.json)
and [R2 seal](../../analysis/ableton-live-12.4.3/full-spec-v1/settings-learning/manifest-author-r2.json)
retain original14files plus exact archive copies. Old checkers expecting live
R1wiki bytes are historical; R4 /pins/64 and /pins/68 read the exact original
research/spec snapshots via the separately disclosed historical replay. No old
pin or report is changed, and no historical mapping approves current extra cases.
'''
    for name, data, target in [('spec-r2.md',spec,R/'wiki/specs/settings-learning-workflows.md'),('research-r2.md',research,R/'wiki/research/settings-learning-workflows.md')]:
        assert not (P/name).exists();(P/name).write_text(data);target.write_text(data)


if __name__ == '__main__':
    main()
