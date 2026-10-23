"""Render finite analyst proposals and null-oracle obligations; run no product."""
from collections import Counter
from pathlib import Path
import json

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
devices = json.loads((P / 'authored-contracts.json').read_text())
requirements, cases = [], []


def write(name, value):
    (P / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


fixtures = {
    'common': 'Valid editable test-owned Set; one enabled device on a legal path. Explicitly select route, source, gain, unit and Delay Compensation state. Disable unrelated automation, mapping, solo/mute and effects unless named. Reset the Set/device between independent trials. Named values/rates are analyst input choices, never product domains; if not admitted or not representable in the chosen unit, leave that case unexecuted rather than infer clamping or a replacement value.',
    'positive-signal-guard': 'Before a signal, silence, no-effect or bypass trial, independently identify active physical output/input/MIDI ports or a qualifying internal plug-in route and retain a positive response baseline. Supply nonzero admitted send/return gain where applicable, active monitoring, the intended channel, enabled device/section and an unmuted nonzero return/output path. External Audio Effect needs nonzero wet contribution, with full wet only for isolating return and an interior mix for processed-versus-dry probes. External Instrument has no asserted device Dry/Wet control here. Missing hardware/notes/return, mute, dry-only output or zero gain cannot prove an active-path property. Preserve that positive setup and change only the named negative setting. The baseline is a prerequisite, not an output captured in this packet.',
    'hardware': 'Prerequisite only: independently known working external synth/effect and identified interface/MIDI ports; retain device/interface model, firmware, driver, port/channel identities, physical wiring, accepted audio configuration and existing calibration before future execution. No hardware acquisition, connection, calibration run or driver installation occurred here. Do not assume external gear is unity gain, transparent, memoryless, phase-neutral or constant latency.',
    'plugin': 'Prerequisite only: independently identified qualifying multitimbral plug-in on another owned track with separately known main and auxiliary outputs. Retain plug-in identity/version, program/state, offered channels/outputs and host-track monitoring. No arbitrary plug-in compatibility or installed fixture is supplied.',
    'audio': 'Authored input definitions only: 48 kHz, 4/4, 120 BPM; four-second PCM tones with left=0.0625*sin(2*pi*220*t), right=0.0625*sin(2*pi*660*t), and a separate amplitude-step source using 440 Hz at 0.03125 then 0.0625 for two seconds each. Include silence before/after. Distinct owned finite bursts may mark outgoing versus returning paths. Actual physical/plug-in transfer and measured samples must be retained separately; these formulas specify no returned audio.',
    'midi': 'Use a valid test-owned MIDI clip with explicit admitted notes, channels and paired releases; for held-note lifecycle tests retain one held note and release it after the trial. No note-frequency mapping, message bytes, MPE interpretation, channel domain, scheduling or release policy is supplied.',
    'rate-state': 'Use 128 samples or 2.5 ms only after the target admits and represents that selected-unit amount. Start at accepted 48 kHz, request 44.1 kHz then 48 kHz. A refused setting/rate leaves the relevant documentary case unexecuted; rate failure/recovery and unit conversion are separate U cases. Compare only selected-unit retained amount, not physical delay or time alignment.',
    'owned-state': 'Use disposable Set/preset copies for malformed, replacement, missing-source and recovery probes. Never alter immutable captured evidence. No private saved-state field names or byte format are presumed.'
}
write('fixtures.json', fixtures)
for prefix, device in devices.items():
    slug, name = device['slug'], device['name']
    blocks = {r['locator']: r for r in json.loads((P / f'manual-{slug}-blocks.json').read_text())}
    for row in device['requirements']:
        evidence = [{'source': device['source'], 'block': slug + ':' + block, 'html_line': blocks[slug + ':' + block]['html_line']} for block in row['blocks']]
        requirements.append({'id': row['id'], 'device': name, 'surface': 'SURF-DEVICE-' + slug.upper(), 'strength': 'D12', 'exact_target_applicability': 'unknown', 'contract': row['contract'], 'evidence': evidence})
        cases.append({'id': row['id'].replace('REQ-', '', 1), 'requirements': [row['id']], 'device': name, 'kind': 'documented-' + row['kind'], 'strength': 'D12', 'setup': 'common; hardware or plugin as required by the named route; rate-state for retained-unit cases', 'action': row['action'], 'documentary_expected': row['documentary_expected'], 'documentary_comparator': 'Only named selector roles, offered controls/units, enabled state and admitted selected-unit amount retention; no audio, MIDI bytes, physical timing or invented rounding/tolerance.', 'expected': None, 'exact_target_applicability': 'unknown', 'executed': False, 'comparison': None, 'evidence': evidence, 'fixture': 'fixtures.json'})
    for suffix, text in [
        ('SIGNAL', f'Required quantitative audio/MIDI, gain, phase, metering, conversion and latency outcomes for {name} remain unknown. The documentary role descriptions and stored class presence provide no numerical oracle or internal mechanism.'),
        ('LIFECYCLE', f'Required boundary, automation, transport, persistence, undo, malformed, cancellation, disconnect, sample-rate failure, bypass, ownership, recovery and teardown outcomes for {name} remain unknown. Existing common-device, export and finite mix contracts do not establish these external-route interactions.')
    ]:
        requirements.append({'id': f'REQ-EHW-{prefix}-{suffix}', 'device': name, 'surface': 'SURF-DEVICE-' + slug.upper(), 'strength': 'U', 'exact_target_applicability': 'unknown', 'contract': text, 'evidence': []})

signals = {
    'EA': [
        ('ROUTE', '001', 'Use independently known working physical send/return ports with a positive returned-audio baseline; send distinct owned bursts and select Audio To/From explicitly.', 'Port/channel signal membership, buffering, conversion and exact returned samples remain unknown; no transparent hardware is assumed.'),
        ('PEAK', '003', 'With independent active send and return baselines, apply amplitude steps, click each peak indicator separately, then apply another nonzero burst.', 'Peak convention, maximum window, send/return measurement points, reset value, smoothing and refresh timing are unknown.'),
        ('GAIN', '004', 'On a positive active physical loop, keep wet output audible and change only send Gain, reset, then only return Gain, between two admitted nonzero values.', 'Separate path roles are documented, but numeric gain law, external processor response, clipping and exact unaffected-branch samples are unknown.'),
        ('MIX', '005', 'Keep dry input and independently known distinct hardware return both active and unmuted; select 100% and two admitted interior Dry/Wet values in separate reset trials.', 'Mix law, dry/return alignment, dry contribution at exact endpoints and numerical output are unknown.'),
        ('INVERT', '006', 'With a known active nonzero return and distinct live dry source, use an admitted interior mix; compare Invert off/on, then repeat with an admitted full-wet setting.', 'Processed-return targeting is documented; phase convention, numeric sign/channel action, dry-path equality and cancellation depth remain ungraded.'),
        ('LATENCY', '007', 'With separately identified physical timing/calibration prerequisites and a positive return baseline, vary an admitted nonzero Hardware Latency in samples and milliseconds; compare Delay Compensation on/off separately.', 'Actual round-trip compensation, driver/gear latency, sample/ms conversion, rounding, drift, jitter and transitions are unknown; no successful alignment is asserted.')
    ],
    'EI': [
        ('MIDI-ROUTE', '001', 'Use an independently known working external synth/MIDI port and admitted channels, a valid owned note clip and positive audible return; select each physical destination/channel in separate reset trials.', 'Emitted MIDI bytes, delivery/ordering, channel isolation, external note response and resulting audio remain unknown.'),
        ('PLUGIN-OUTPUTS', '004', 'Use a separately known qualifying multitimbral plug-in with distinguishable main/auxiliary signals; keep the instrument-host track and External Instrument track monitored and unmuted, explicitly select an auxiliary return and MIDI channel.', 'The documented main-on-host and auxiliary-return roles have no supplied numerical routing/mix oracle, plug-in callback contract, duplicate suppression or channel matrix.'),
        ('GAIN', '005', 'For separately reset positive hardware and qualifying internal-plugin returns, vary only External Instrument Gain between admitted nonzero values while the owned note input and return remain active.', 'Return gain law, clipping, external/plug-in response and numerical output are unknown; no MIDI-send gain or limiter is inferred.'),
        ('LATENCY', '009', 'With Delay Compensation on, compare a positive qualifying internal-plugin return and a separately calibrated physical route with admitted nonzero Hardware Latency; request samples/ms only on the physical route.', 'Internal automatic compensation and external manual compensation are documented goals; measured accuracy, conversion, latency limits and scheduling are unknown. A disabled internal slider is not proof of compensated audio.')
    ]
}
contexts = {
    'EA': ('active physical send/return pair, nonzero separate Gains, admitted interior Dry/Wet, Invert on and 128 samples Hardware Latency with Delay Compensation on', 'Audio To/From, both Gains, Dry/Wet, Invert and latency units'),
    'EI': ('separately reset physical synth route and qualifying internal multitimbral plug-in/auxiliary route, nonzero Gain, owned held note, Delay Compensation on and 2.5 ms manual latency on the physical route', 'MIDI port/track/channel, Audio From, Gain, latency units and Delay Compensation')
}
for prefix, device in devices.items():
    name, slug = device['name'], device['slug']
    for suffix, role, action, unknown in signals[prefix]:
        rid = f'REQ-EHW-{prefix}-{role}'
        evidence = next(r['evidence'] for r in requirements if r['id'] == rid)
        cases.append({'id': f'EHW-{prefix}-SIGNAL-{suffix}', 'requirements': [rid, f'REQ-EHW-{prefix}-SIGNAL'], 'device': name, 'kind': 'signal', 'strength': 'U', 'setup': 'common; positive-signal-guard; hardware or plugin as explicitly named; audio/midi; owned-state', 'action': action, 'documentary_expected': None, 'documentary_comparator': None, 'expected': None, 'comparison': None, 'unknown': unknown, 'exact_target_applicability': 'unknown', 'executed': False, 'evidence': evidence, 'fixture': 'fixtures.json'})
    context, controls = contexts[prefix]
    for kind, action, unknown in [
        ('boundary', f'Initialize {context}; test two admitted nonzero interior settings, then adjacent endpoint/zero/negative entries for exposed numeric controls in {controls}; do not infer a legal range.', 'Clamp/reject policy, endpoint restoration, zero semantics, unit switching, numeric precision and event-boundary ordering are unknown.'),
        ('automation', f'Initialize {context}; attempt supported automation or mapping of exposed controls in {controls}; run manual and automated changes separately over a positive signal baseline.', 'Eligibility, mapping ownership, smoothing, port-change scheduling and equivalence of manual/mapped/automated changes are unknown.'),
        ('transport', f'Initialize {context}; play the owned audio/note source, stop, seek, resume and separately seek during playback at 4/4 120 BPM.', 'Held-note release, external/plug-in tails, port flushing, compensation restart and signal lifetime are unknown; no transport deadline is asserted.'),
        ('persistence', f'Initialize {context}; save an owned Set/preset where supported, close/reopen with the same configuration, then in a disposable copy reopen with missing or renamed ports/source tracks.', 'Saved routing/gain/unit identities, hardware reconnection matching, external/plug-in state ownership and missing-source handling are unknown.'),
        ('undo', f'Initialize {context}; edit two controls in {controls}, replace the device or preset, then use global Undo/Redo in separate reset trials.', 'Undo grouping, restoration of route/unit/held-note state, engine reconfiguration and captured external/plug-in state are unknown.'),
        ('malformed', f'On disposable owned copies only, attempt empty/truncated preset import and invalid numeric text including NaN, inf and 1e309 in exposed editable controls in {controls}.', 'Admission, parser/field validation, diagnostics, retained state and recovery are unknown; no private file encoding is assumed.'),
        ('cancel', f'Initialize {context}; open a routing chooser and dismiss before selection; separately begin a supported device/preset replacement and cancel where offered. For External Audio Effect also enter Audio Settings through Configure… and dismiss without committing edits.', 'Cancellation availability, commit point, port reconfiguration, partial updates and preservation of previous signal/state are unknown.'),
        ('disconnect', f'Initialize {context} with a positive baseline; in separately reset future trials disconnect the identified physical port/interface and remove or unload an internal source/plugin track where that route is applicable.', 'Hotplug/source-loss detection, stale selectors, diagnostics, note release, reconnection identity and returned audio are unknown; no hardware connection or disconnection occurred here.'),
        ('sample-rate', f'Initialize {context}; request 48 to 44.1 to 48 kHz while stopped and separately while active; test supported refusal/failure contexts separately and switch sample/ms units only in a distinct trial.', 'Successful selected-unit retention has the bounded D12 cases; unsupported-rate response, conversion rounding, discontinuities, clock drift, queued notes, failure and recovery remain unknown.'),
        ('bypass', f'Initialize {context}; on a positive nonzero source/return path toggle device/chain activation, then restore it while the external or plug-in source remains active.', 'Bypass routing, held notes, return/tail lifetime, residual hardware activity and reactivation are unknown; common device activation does not supply an external-route signal oracle.'),
        ('ownership', f'Initialize {context}; change selected/focused track and Session/Arrangement view, then separately change which owned clip supplies active input, retaining explicit source routing.', 'Focus/selection effects on monitoring/control ownership, active-clip changes and delivery to external/plugin destinations remain unknown beyond their linked finite owners.'),
        ('recovery', f'Initialize {context}; in a disposable supported configuration request a route whose audio-engine/port activation is refused or unavailable, then restore the previously functioning configuration.', 'Diagnostics, refused activation, permission/driver failure, rollback, retry and preservation of prior state are unknown; no fault injection or driver changes occurred here.'),
        ('teardown', f'Initialize {context} with a positive signal baseline; remove device, undo removal, close the owned Set and separately close the application while source/held note is active.', 'Port/resource release, outstanding MIDI, tails, compensation teardown, external hardware state and save/close prompts are unknown; no forced external reset or cleanup deadline is asserted.')
    ]:
        cases.append({'id': f'EHW-{prefix}-U-{kind.upper()}', 'requirements': [f'REQ-EHW-{prefix}-LIFECYCLE'], 'device': name, 'kind': kind, 'strength': 'U', 'setup': 'common; positive-signal-guard; hardware/plugin prerequisites where applicable; owned-state', 'action': action, 'documentary_expected': None, 'documentary_comparator': None, 'expected': None, 'comparison': None, 'unknown': unknown, 'exact_target_applicability': 'unknown', 'executed': False, 'evidence': [], 'fixture': 'fixtures.json'})
write('requirements.json', requirements)
write('cases.json', cases)
assert len(requirements) == 24 and Counter(r['strength'] for r in requirements) == {'D12': 20, 'U': 4}
assert len(cases) == 56 and Counter(c['strength'] for c in cases) == {'D12': 20, 'U': 36}
assert len({r['id'] for r in requirements}) == 24 and len({c['id'] for c in cases}) == 56
assert all(c['expected'] is None and not c['executed'] for c in cases)

rel = '../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/'
spec = '''---
id: SPEC-EXTERNAL-HARDWARE-DEVICES
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Live 12 documentary behavior with exact-build applicability unknown
---

# External Instrument and External Audio Effect

## Scope and authority

This partial F-06/F-09 draft owns the individual routing/control behavior of
`SURF-DEVICE-EXTERNAL-AUDIO-EFFECT` and `SURF-DEVICE-EXTERNAL-INSTRUMENT`.
The [full coverage design](../research/full-live-specification-design.md) governs
closure; [research](../research/external-hardware-devices.md) owns source
interpretation and installed-presence limits. Neither profile is complete or
released for implementation.

**D12** is prose in the retained official Version 12 manuals captured 2026-10-19.
All runtime clauses have **exact 12.4.3 applicability U**. **Dpkg** observations
prove schema/inventory presence only, not behavioral aliases or runtime fields.
All 56 case `expected` values are null and every case is unexecuted. Twenty
cases retain documentary control/state proposals; ten signal probes and 26
lifecycle probes have null documentary expectations and comparators. There is
no S/X execution, hardware experiment or original-versus-candidate result.

[Device chains/racks](device-racks.md) owns common insertion, bypass, presets and
chain composition; [plug-in hosting](plugin-hosting.md) owns its bounded host
workflows. A qualifying multitimbral plug-in and its auxiliary outputs are
prerequisites here, not a promise of arbitrary plug-in support. [Audio/video
export](audio-video-export.md), especially REQ-EXPORT-019–022, owns real-time
versus offline rendering, countdown, restart and render cancellation. Do not
classify a render solely from either device's presence or duplicate its laws here.

[Mix graph](mix-graph.md) explicitly excludes general routing/monitoring,
latency-reporting devices, real-time scheduling and the physical audio-device
stage. Its finite mixer laws are not evidence for these round trips or latency
compensation. [Automation](automation-envelopes.md), [MIDI configuration](midi-user-mapping.md),
[transport](transport-state.md), [clip launch](clip-launch.md) and
[recording/comping](recording-comping.md) retain their bounded owners; none
closes these devices' automation, MIDI delivery, active-clip or recording/render
interactions. Global audio preferences/driver lifecycle and general routing
remain separate open engine/control scope.

## Controlled inputs and observable state

Use a valid editable test-owned Set and explicitly admitted settings. The
[fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/fixtures.json)
separate physical hardware, qualifying internal plug-in, owned audio/MIDI and
selected-unit rate setups. Port identity, enabled channel, active monitoring,
source and nonmuted return/output must be independently established before any
signal claim. Hardware/plug-in availability is an unproven prerequisite on this
analyst host; a selected name or schema class is insufficient.

All signal/no-effect/silence probes need a paired positive baseline, active
device, admitted nonzero relevant send/return gain and appropriate source.
External Audio Effect also needs nonzero wet contribution; an interior mix is
needed to distinguish dry from processed-return behavior. External Instrument
does not inherit a Dry/Wet or separate send-Gain control from the effect.
Dry-only monitoring, absent carrier/note, muted return, zero gain or unavailable
hardware supplies no evidence about an active path. No baseline was captured.

The proposed 128 samples, 2.5 ms, 48/44.1 kHz and 120 BPM are authored finite
inputs, not product ranges or constructor defaults. If entry or rate change
is unavailable or not representable, the documentary case remains unexecuted.
Selected-unit retention is separate from physical alignment and cross-unit
conversion; no rounding law, tolerance, gain coefficient or MIDI byte codec is
established. All measurements of actual returned signals remain unknown.

## Individual requirements

Every D12 row below is target-U. Evidence names exact blocks in the packet,
including the retained HTML line and major-release source identity.

'''
schema = {r['class']: r for r in json.loads((P / 'schema-fields.json').read_text())}
for prefix, device in devices.items():
    spec += f"### {device['name']}\n\nSurface `SURF-DEVICE-{device['slug'].upper()}`; frozen discovery association `{device['schema_class']}` at schema line {schema[device['schema_class']]['line']} is inferred presence only, not a behavioral/runtime alias.\n\n| Requirement | Preconditions, documented result and limits | Evidence |\n| --- | --- | --- |\n"
    for row in requirements:
        if row['device'] == device['name']:
            refs = ', '.join(r['block'] for r in row['evidence']) or 'Required unknown; no supplied outcome'
            spec += f"| {row['id']} / {row['strength']} | {row['contract']} | {refs} |\n"
    spec += '\n'
spec += '''## Timing, lifecycle and boundary obligations

Sample-mode retention preserves a count; millisecond-mode retention preserves
the selected duration after a successful rate change. Neither establishes
physical round-trip compensation, an exact converted count, drift/jitter or a
sample/event ordering law. External Instrument's disabled internal-route slider
is a control predicate; it cannot demonstrate the documented automatic
compensation goal numerically. Delay Compensation off disables the slider in
both devices, without establishing bypassed audio or restoration on re-enable.

For each device thirteen distinct lifecycle probes cover numeric boundaries,
automation/mapping, transport, persistence/missing sources, undo, malformed
state, cancellation, disconnect, rate failure/change, bypass, selection/focus
ownership, recovery and teardown. All are required unknowns, with no lifecycle
kind marked inapplicable. A missing physical device or qualifying plug-in keeps
its probe unexecuted. The effect's Configure… route is documented; it is not
silently assigned to the instrument. Hardware side effects and third-party
state restoration are not assumed to be controlled by Set Undo or reload.

## Acceptance catalog

The [requirements](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/requirements.json)
and [cases](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/cases.json)
retain complete setup/action, source references and null unknowns. Documentary
comparators inspect only named controls, choices, disabled state and admitted
selected-unit retention. They do not grade gain, peak values, phase, MIDI, returned
audio or timing. Every exact-target expectation is null.

| Device | D12 / U requirements | Control / state cases | Signal / lifecycle U cases |
| --- | --- | --- | --- |
'''
for prefix, device in devices.items():
    counts = Counter(c['kind'] for c in cases if c['device'] == device['name'])
    spec += f"| {device['name']} | 10 / 2 | {counts['documented-control']} / {counts['documented-state']} | {counts['signal']} / 13 |\n"
spec += '\nTotal: **24 requirements (20 D12, four U); 56 unexecuted cases (20 documentary, 36 U)**.\n\n| Case | Requirements | Kind | Finite action / proposed observation or required unknown |\n| --- | --- | --- | --- |\n'
for case in cases:
    outcome = case['documentary_expected'] or case['unknown']
    spec += f"| {case['id']} | {', '.join(case['requirements'])} | {case['kind']} | {case['action']} {outcome} |\n"
spec += '''
## Unknowns and evidence appendix

[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
owns exact-build/whole-product coverage gaps. Required unknowns include port
domains and naming/grouping, configuration failure and restoration, hardware or
plug-in availability, MIDI delivery/codec/channel domain, main/auxiliary signal
composition, gain/mix/phase/peak laws, limits and rounding, compensation accuracy,
automation, undo, persistence, cancellation, hotplug, driver failures and teardown.
No source specifies an external-device protocol, private DSP mechanism or full
saved-state API. No figure, FAQ or linked routing chapter was independently
inspected for this packet.

The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/sources.json)
pins seven reused external sources, including original capture catalogs and the
frozen inventory/schema. D12-AUDIO-EFFECTS is the original audio-utilities source
identity: [HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/audio-utilities/manual-audio-effects-2026-10-19.html),
SHA-256 `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299`,
[official chapter](https://www.ableton.com/en/live-manual/12/live-audio-effect-reference/),
§29.18, heading HTML line 1144, paragraphs line 1154.
SAMPLE-INSTRUMENTS-MANUAL is the original sample-instruments identity:
[HTML](../../analysis/ableton-live-12.4.3/full-spec-v1/sample-instruments/manual-instruments-2026-10-19.html),
SHA-256 `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a`,
[official chapter](https://www.ableton.com/en/live-manual/12/live-instrument-reference/),
§31.6, heading HTML line 1016, paragraphs line 1026. Both were captured
2026-10-19 and identify Version 12, not exact patch behavior.

The two [manual block views](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-audio-effect-blocks.json)
and [instrument blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-instrument-blocks.json)
retain 18 paragraphs plus two headings. The
[schema view](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/schema-fields.json)
and [discovery associations](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/inventory-associations.json)
are Dpkg presence only. The latest schema hash is
`b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299`.
Both profiles have no matched preset example in the frozen inventory; fields
and inferred class associations prove no port serialization or runtime behavior.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manifest-author-r1.json)
freezes payloads and both canonical snapshots. The
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validate.py)
and [result](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validation-author-r1.json)
check packet integrity only. These analysis-only links require review and
sanitization before any handoff. No source bytes were rewritten and no original,
candidate, external device or plug-in was executed. Independent semantic review
is a separate gate; no release, installation or publication occurs here.
'''
(ROOT / 'wiki/specs/external-hardware-devices.md').write_text(spec)
research = '''---
id: RES-EXTERNAL-HARDWARE-DEVICES
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3
---

# External routing devices: retained documentary evidence

## Ownership and sources

The [individual-device contract](../specs/external-hardware-devices.md) owns the
documented External Audio Effect and External Instrument behavior. This page
owns source interpretation and limits under the
[coverage design](full-live-specification-design.md) and
[execution plan](full-live-specification-plan.md).

The [capture script](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/capture.py)
uses only retained HTML, frozen inventory/schema and Python standard-library
parsing/hashes. The [source ledger](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/sources.json)
pins seven external dependencies and original source identities/catalogs; the
manuals are reused captures, not newly downloaded or relabeled sources.

| Source identity | Version/capture and exact locator | SHA-256 |
| --- | --- | --- |
| D12-AUDIO-EFFECTS | Version 12, captured 2026-10-19; §29.18 external-audio-effect heading HTML 1144, nine paragraphs HTML 1154; audio-utilities original catalog | `9cb15cb3d80bda4771e5add2c2b74f5c57d73ee8850e198acf7cf8a51dfd1299` |
| SAMPLE-INSTRUMENTS-MANUAL | Version 12, captured 2026-10-19; §31.6 external-instrument heading HTML 1016, nine paragraphs HTML 1026; sample-instruments original catalog | `3975fec856ada335526b35504ab3ca058dbf8f2885169944e0a819d45990fd6a` |
| PKG-SCHEMA | Installed latest 12.0_12402 schema; BufferAudioDevice line 939, BufferInstrument line 963 | `b7c9d4c767d8ca9b346ce7d517265446bbacd6de366cc058e155613789d0f299` |

Observed D12: each bounded manual section has one heading and nine paragraphs.
The retained [effect blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-audio-effect-blocks.json)
and [instrument blocks](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manual-external-instrument-blocks.json)
preserve normalized text, paragraph/heading kind and original HTML line. Images,
the linked Driver Error Compensation FAQ and Routing and I/O chapter were not
inspected; this packet does not claim their contents.

## Presence and interpretation limits

Observed Dpkg: the frozen inventory associates External Audio Effect with
BufferAudioDevice and External Instrument with BufferInstrument using
`schema-and-product-directory; semantic alias inferred`. The
[retained entries](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/inventory-associations.json)
have `example: null`, `complete: false` and no matched preset. The
[class fields](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/schema-fields.json)
each contain the common device vocabulary and a Gain field. This is not an
observed runtime alias or sufficient evidence for routing serialization,
constructor defaults, numeric range, control exposure or hardware compatibility.

Interpretation notes below explain boundaries in the canonical clauses without
replacing their individual contracts:

- The effect explicitly supplies Configure… in both port choosers (§29.18,
  external-audio-effect:B003). The instrument's availability sentence references
  Audio Settings (§31.6, external-instrument:B005), but establishes no independent
  Configure… command there. Similar device roles do not justify copying a control.
- Instrument hardware-return inputs and plug-in auxiliary outputs belong to
  different route contexts. Its B006 main-output-on-host statement is a signal
  ownership goal, not a numeric mixing/downmix or arbitrary plug-in contract.
- Effect send/return Gains and instrument return Gain have different stated
  roles (effect B005, instrument B007). Neither description supplies a gain
  coefficient, clipping limiter or external hardware transfer function.
- Effect Peak indicators (B004) and processed-return Invert (B007) name
  observable controls/goals. Their sample conventions, reset values, phase
  matrix, update timing and quantitative signal comparisons remain U.
- Both B008 latency paragraphs separate sample-count retention from
  millisecond-duration retention across rate changes. Displayed selected-unit
  state can be proposed separately from physical alignment. Digital/analog
  setup and fine-tune advice do not specify cross-unit rounding or a conversion
  implementation. No physical latency was measured.
- Instrument B008 disables manual latency for internal routing and documents
  automatic compensation. B009 in each section disables the slider when Delay
  Compensation is unchecked. These disabled-state predicates do not prove
  compensation accuracy, bypassed audio or restoration of hidden values.

[Audio/video export](../specs/audio-video-export.md) already owns external-route
real-time/offline decisions and restart/cancel controls. Device names alone
cannot establish whether a particular render is affected. The finite
[mix graph](../specs/mix-graph.md) excludes general physical routing and
latency-reporting devices; its mixer arithmetic supplies no hardware oracle.
Hardware, qualifying plug-ins, active ports, driver permissions, supported audio
rates and calibration are explicit prerequisites for future observations, not
capabilities demonstrated on this analyst host.

## Authored probes and frozen evidence

The packet contains 24 requirements: 20 D12 documentary clauses and four U
signal/lifecycle obligations. Its 56 unexecuted cases comprise 16 control and
four selected-unit state proposals, ten ungraded signal probes and 26 U
lifecycle probes. All exact-target expected outcomes are null; signal/lifecycle
documentary expectations and comparators are also null. Both device profiles
remain partial. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains the major-release-to-exact-build evidence gap.

The [fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/fixtures.json)
require independently known active ports and a nonmuted nonzero return positive
baseline before any signal/no-effect proposal. They define owned input tones,
admitted-unit/rate choices and MIDI setup without claiming returned samples,
MIDI encoding, waveform equality, gain, jitter or timing tolerances. No hardware,
plug-in binary, baseline recording or executable product fixture is supplied.
Missing prerequisites keep cases unexecuted; they never become passes.

The [author manifest](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/manifest-author-r1.json)
pins the complete packet and canonical snapshots; the
[validator](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validate.py)
and [author result](../../analysis/ableton-live-12.4.3/full-spec-v1/external-hardware/validation-author-r1.json)
check source hashes/catalog identity, exact block reproduction, schema/inventory
derivations, requirement/case ownership, source locators, null outcomes,
lifecycle kinds, JSON, snapshots, links and untracked-aware whitespace. These
are integrity checks; independent semantic review remains separate.

No original application/function, candidate, emulator, plug-in or hardware was
run. No network capture, hardware acquisition, tooling installation, calibration,
release, publication or commit occurred. Shared catalog/coverage/question/log
integration is coordinated outside this packet.
'''
(ROOT / 'wiki/research/external-hardware-devices.md').write_text(research)
print(json.dumps({'requirements': len(requirements), 'requirement_strength': dict(Counter(r['strength'] for r in requirements)), 'cases': len(cases), 'case_kinds': dict(Counter(c['kind'] for c in cases))}, indent=2))
