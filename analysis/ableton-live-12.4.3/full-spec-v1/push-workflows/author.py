"""Analyst documentary catalog; never executes Push, MIDI or Live."""
from pathlib import Path
from collections import Counter
import json
import hashlib

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
assert not (P / 'manifest-author-r1.json').exists(), 'Do not regenerate sealed bytes'
requirements, cases = [], []


def dump(name, data):
    (P / name).write_text(json.dumps(data, indent=2) + '\n')


def add(model, title, refs, claim, action, kind='control'):
    n = 1 + sum(r['model'] == model for r in requirements)
    rid, cid = f'REQ-PUSH{model}-WF-{n:03d}', f'P{model}-WF-{n:03d}'
    blocks = [f'P{model}-B{int(r):03d}' for r in refs.split()]
    requirements.append(dict(id=rid, model=model, title=title, provenance='D12', target_applicability='U', contract=claim, source_blocks=blocks))
    addcase(cid, rid, model, title, kind, action, claim, blocks)


def addcase(cid, rid, model, title, kind, action, claim, blocks):
    visible = kind == 'control' and '-U-' not in rid
    cases.append(dict(id=cid, requirements=[rid], model=model, title=title, kind=kind,
                      preconditions=['common', f'Push{model}', 'active-positive-guard'],
                      setup_and_action=action, source_blocks=blocks, source_claim=claim,
                      documentary_expected=claim if visible else None,
                      documentary_comparator='Compare only text-supported named controls, modes, display/selection or membership predicates; no pad-number, signal, timing, LED-palette, protocol or hardware parity oracle.' if visible else None,
                      expected=None, comparison=None, target_grade='U', executed=False))


# Separate records cite only their model's chapter; similar roles are not parity proof.
add(1, 'USB setup role', '7', 'Push 1 is described as automatically recognized when connected over USB while Live is running, without manual driver or Settings setup. Accepted platform, firmware, enumeration, recovery and latency remain unknown.', 'On an independently accepted Push 1/host/firmware/USB setup only, retain before/after connection and selected surface/ports. No device is acquired or connected by this packet.', 'protocol')
add(1, 'Browse navigation and load', '9 10 11 12 13 14', 'Browse opens a column browser; In/Out shifts hierarchy, Selection/State buttons navigate, encoders scroll and Shift up/down pages. Text distinguishes selected preset load from device default load and already-loaded next-entry behavior; no figure-derived button identity or exact light color is imposed.', 'F-BROWSE: actual available owned presets in two folders; enter Browse, navigate In/Out and page, load an offered preset/default then next entry. Grade display and loaded device identity only; preview audio stays U.')
add(1, 'Browse context filtering', '15', 'Push 1 browsing depends on selected instrument/effect context; an empty MIDI track shows available device families. Only currently loadable folders are visible, with sample-only locations described for an individual Drum Rack pad.', 'F-BROWSE: compare selected instrument, effect, empty MIDI track and selected individual rack pad using known available content. Inspect offered categories; absence is not a plug-in or format incompatibility law.')
add(1, 'Drum layout roles', '17 18 19 21 30 35 36 37', 'In Note Mode with Drum Rack, the chapter describes Loop Selector sections for play/sequence/length, a velocity layout and full-grid playing. Note-based switching/momentary access is described, but the separate Layout wording is unresolved; no physical pad map or complete transition table is adopted.', 'F-DRUM: retain actual offered layout/control identity, select known active Drum Rack and compare playing, step and loop roles. Capture layout transitions without inferring positions from figures or the disputed Layout label.', 'pad-role')
add(1, 'Drum pad bank and silent selection', '29 45', 'Touch strip and Octave controls navigate Drum Rack pads, with Shift finer movement; Select plus pad selects without playing. Exact pad indices, MIDI notes and pressure response remain unknown.', 'F-DRUM: independently audible populated pad plus an empty pad, navigate a bank then Select-tap known active pad. Retain actual selected identity and paired ordinary-tap response, no no-effect/silence threshold.', 'pad-role')
add(1, 'Individual drum browsing and copy', '39 40 41 43', 'Device selection can focus an individual Drum Rack pad for Browse replacement; other pad taps select further browse targets. Duplicate held from source pad to destination replaces destination devices while preserving already recorded destination notes.', 'F-DRUM/F-BROWSE: distinct source/destination devices and destination notes retained; browse a selected pad then copy on a disposable reset trial. Inspect devices and note membership, no voice/DSP or event-encoding law.')
add(1, 'Drum step gestures', '46 47 49 54', 'Step taps add notes and start clip playback; tapping occupied steps deletes them, Mute plus step deactivates without deletion, Solo plus pad solos a sound, and Delete plus pad removes its notes within the current loop. Triplet layout leaves some pads inactive; no grid/sample arithmetic follows.', 'F-DRUM/F-REC: active nonempty loop with notes inside/outside it; separately add/remove/mute/solo/delete and inspect triplet layout. Retain positive pad/output before inactive comparison; events and timing ungraded.', 'midi-output')
add(1, 'Record and overdub controls', '58 59 60', 'Metronome is available for real-time recording; successive Record actions record, stop recording while playback continues, then enable overdub. General count-in/record eligibility and actual recorded notes remain with recording owners.', 'F-REC: explicit eligible armed monitored instrument and positive pad response, choose count-in/metronome and actual transport; record, stop record and overdub on reset trials. Capture record/play states and output, no event/cadence oracle.', 'recording')
add(1, 'New and workflow modes', '61 217 219 220 223 224', 'Scene Workflow Duplicate captures playing clips into a new scene; New prepares selected-track material instead. Clip Workflow Duplicate/New operates on selected clip/track while other tracks continue, with Shift-Duplicate scene behavior. Seamless wording supplies no transition tolerance.', 'F-SESSION: two independently playing tracks, explicit Scene then Clip Workflow; use New and Duplicate separately and retain scene/clip membership. Timing, empty slots and conflicts remain ungraded.', 'timing')
add(1, 'Fixed Length controls', '63 64 65 66', 'Fixed Length selects predetermined new-clip length, holding it opens length choice; disabled recording runs until a documented stop action. Enabling during record stops writing and loops the preceding span according to setting, without a beat/sample endpoint law.', 'F-REC: known active recording and admitted nonzero length; compare Fixed Length off/on and enable during a separate pass. Retain selection, actual record/transport and resulting region; no rounding oracle.', 'timing')
add(1, 'Repeat and swing roles', '69 70 71 72', 'Repeat produces repeated held-pad notes, with rate via Scene/Grid and state/settings remembered per track. A short press latches while a hold is momentary; pressure and Swing influence output. No force curve, note rate or swing calculation is supplied.', 'F-DRUM/F-REC: accepted active pad and nonzero output, compare tap/hold Repeat and two admitted grid/rate settings, another track, then nonzero Swing. Capture output/pressure context without MIDI/latency metrics.', 'timing')
add(1, 'Quantize entry and scope', '74 75 76 77 78 79', 'Quantize applies selected clip note quantization; holding exposes Swing Amount, Quantize To/Amount and Record Quantize. Quantize plus drum pad narrows scope to that drum. Numeric quantization and record-grid enums retain existing owners.', 'F-EDIT: known off-grid notes for two drums, explicit accepted settings; inspect hold menu, invoke whole-clip then selected-drum route on reset copies. Note movement/output remains ungraded.', 'editing')
add(1, 'Pitched pad and scale layouts', '85 93 95 96 97 99 100 101 102 103 244', 'Instrument Note Mode offers pitched playing and loop controls; Scales selects key/scale and Fixed/In Key/Chromatic/layout options. Scale options are described as saved with Set. Scales is ineligible for Drum Rack or Session context; no note-number map, tuning or default key law is prescribed.', 'F-PITCH: active eligible instrument and nonzero note/output baseline; inspect Scales options and two admitted layouts, then Drum Rack/Session ineligibility. Save/reopen is a separate U branch; pad/tuning outputs null.', 'pad-role')
add(1, 'Melodic step and loop layout', '107 108 109 110 111 113', 'Note switches to melodic step layouts, rows represent chosen pitches and columns selected grid steps. Held Note exposes loop controls and Shift-Note locks them per track; Octave/touch strip changes range. Numeric mapping/phase and the 32-note layout remain ungraded.', 'F-PITCH/F-EDIT: known nonempty clip and distinct admitted pitches, select melodic layout, reveal/lock loop controls and change range; compare before/after visible clip and input identities without pad equations.', 'pad-role')
add(1, 'Loop page selection and copy', '116 117 123 124', 'Loop-length pads select loop span or viewed sequencer page. A locked view need not be the playing page; reselecting loop restores follow, whereas selecting outside loop sets that page as loop. Duplicate-page adds copied notes over existing destination notes; Delete-page clears first.', 'F-EDIT: longer positive loop with distinct page contents and destination notes; select in-loop page, restore follow and select out-of-loop page on separate copies, then duplicate. Capture membership and play/view separately; timing null.', 'timing')
add(1, 'Combined melodic playing and sequencing', '126 128 129 138 139 140', 'Melodic Sequencer plus Notes combines real-time pitch selection with steps. Select avoids playing; a step adds selected notes, holding it exposes contained pitches, and removing a selected pitch removes it from that step. Duplicate adds copied notes without clearing destination.', 'F-PITCH/F-EDIT: distinct notes and occupied destination step, select/hold/add/remove/duplicate on reset copies with positive instrument baseline. No pad index, stored-note merge or numeric output oracle.', 'pad-role')
add(1, 'Note navigation and arm context', '152 153 154 155', 'Left/right selects tracks and MIDI selection is described as auto-arming. Up/down moves scenes, with Scene versus Clip Workflow determining launched scope; source describes immediate Legato-like position continuation. No constructor arm default or timing law is established.', 'F-SESSION/F-PITCH: distinct active tracks/clips, explicit Workflow and arm/monitor states; change track then up/down in separate trials. Retain output/ownership and position, without extending launch or implicit-arm laws.', 'timing')
add(1, 'Device mode and banks', '157 158 159 161 162', 'Device enables parameter encoders; Selection buttons choose devices and State buttons enable/disable the selected device. In/Out reaches additional parameter banks or rack chains. Exact banks/targets, codecs and DSP remain device/rack owned.', 'F-DEVICE: two named eligible devices and a multichain rack, retain active nonzero processed baseline; select/enable/disable, then navigate offered bank/chain. Inspect control and selected identity only.')
add(1, 'Mix modes and split pan', '164 165 166 167 168 169 170 171', 'Volume, Pan/Send and Track modes select mix controls; Shift refines adjustment, Master selects Main and held group selection folds/unfolds. In split stereo pan, Pan/Send shows value but disables dial, while Track mode offers appropriate pan controls.', 'F-MIX: active sources/returns and known pan mode; inspect each control mode, select Main/group and compare split versus ordinary pan. Existing numeric mixer and routing laws are not retested.')
add(1, 'Automation entry and indicators', '173 174 175 176', 'Automation toggles Session Automation Arm; Delete plus encoder touch deletes recorded parameter automation or resets unautomated parameter to default. Recorded/overridden parameters have rectangle/bracket presentation; Shift-Automation re-enables overridden automation.', 'F-AUTO: independently active changing envelope and untouched eligible parameter, record off for override, explicit transport/arm/record for a separate pass. Inspect controls/indicators; audible return, default value, event production and persistence remain U.')
add(1, 'Held-step editing and automation', '178 179 181 183 184 185 186 187 188 189 190 192', 'Holding steps exposes note Nudge, coarse/fine Length and Velocity with multistep selection; empty-step edits can create notes and Duplicate copies note settings. Device/Volume modes permit per-step automation even without notes. Exact values/timebase remain unproven.', 'F-EDIT/F-AUTO: known occupied and empty steps plus active target with nonzero amount/output, hold individual/multiple steps and edit offered controls on reset copies; capture resulting notes/envelopes without formulas.', 'editing')
add(1, 'Session entry, clip and stop controls', '194 195 200 201 202 237 300', 'Session/Note hold gives momentary mode access. Session pad/Scene controls launch corresponding material and Select chooses without launch; Stop mode stops a track and Shift-Stop stops all clips. The selected-track new-record sentence lacks full slot prerequisites and stays context only.', 'F-SESSION: active populated distinct clips/scenes and an independently identified empty slot, explicit arm/monitor/record/launch settings. Use mode/select/launch/stop separately; empty-slot recording and all scheduling remain U.', 'pad-role')
add(1, 'Session navigation and overview', '203 204 205 207', 'Session arrows and modifiers move the controlled region; Shift exposes Session Overview where pads choose larger blocks and scene controls larger scene ranges. Region borders link software/hardware focus; no numeric pad-to-track/scene or viewport oracle is added.', 'F-SESSION: enough owned populated scenes/tracks for interior and boundary regions; navigate normal and Shift overview, choose a block, retain actual controlled identities. No figure position or block-index arithmetic is graded.', 'pad-role')
add(1, 'User preferences and alternate mode', '214 215 216 217 226 248', 'Held User opens pad/aftertouch response and Workflow preferences; User Mode disables built-in functionality for alternate mapping. Recommended relative-encoder mode and sensitivity/threshold examples supply no complete protocol, force curve or configuration-token equivalence.', 'On independently accepted Push 1 inspect User preferences, two admitted settings and alternate mode while keeping a working positive built-in baseline. Alternate mapping is attempted only through existing remote owner; physical response remains null.')
add(1, 'Touch strip contextual roles', '293 294', 'Instrument real-time touch strip controls pitch bend or mod wheel, toggled by Select-tap; melodic sequencing uses note-range navigation and Drum Rack uses bank selection. Real-time expression is not offered in melodic step-sequencer context.', 'F-PITCH/F-DRUM: active instrument and admitted nonzero bend/wheel target, establish paired positive output before context changes. Compare Select-tap real-time and sequencer/rack contexts; no MIDI bytes, range or pressure law.', 'signal')
add(1, 'Track/effect and common edit entrypoints', '81 82 83 84 240 241 281 282 284 289', 'Add Track/Add Effect and modifiers expose track-type and insertion-side entrypoints, with selected group context affecting placement. Undo/Shift-Undo invokes Live history, Delete is context-sensitive, Double extends loop material, and Record-New on armed MIDI triggers Capture. Generic history/record/rack semantics stay with their owners.', 'F-EDIT/F-DEVICE: fresh owned track/group/device/clip before-inventory; invoke each actually offered entrypoint separately with explicit mode/selection. Compare visible membership only; compound history, Capture notes and loop/event output remain U.')

add(2, 'Power/USB and firmware setup context', '6 7', 'Push 2 setup describes included power, USB and power-on followed by automatic Live recognition without manual driver/Settings setup. Live updates may prompt firmware update. No firmware bytes, supported version set, updater, deadline or recovery law is specified.', 'Only on independently accepted Push 2 hardware/firmware/host/ports retain detected state and any offered prompt. No update, power action, driver installation or hardware connection is performed by this packet.', 'protocol')
add(2, 'Browse columns, preview and load', '9 10 11 12 13 14 15 16', 'Browse exposes context-dependent columns/Collections, encoders/arrows navigate and upper controls move hierarchy. Preview toggles browser audition, Shift-Master adjusts preview level and Load loads selection. Instrument/effect/empty-track context filters available content.', 'F-BROWSE: known available owned content and positive preview output first; inspect categories, hierarchy, Preview and Load with instrument/effect/empty contexts. Numeric gain, preview timing and plug-in support remain U.')
add(2, 'Drum layouts and Layout hold', '18 19 20 22 30 31 33 34 36 37 38', 'With Drum Rack in Note Mode, Layout cycles Loop Selector, velocity and full-grid modes; held Layout exposes alternate controls and Shift-Layout locks them. Octave/touch strip changes drum banks without automatically changing the sequenced subset across layout changes.', 'F-DRUM: active populated rack and independently identified selected pad, compare Layout tap/hold/lock and bank changes with nonzero output. No numeric pad map or velocities are an oracle.', 'pad-role')
add(2, 'Individual pad browse and selection', '40 41 42 43 44 45', 'Device focus plus pad and second upper display button selects pad-level Browse. Load changes to Load Next with a previous-entry option; Select-pad avoids triggering, and expanded rack lower controls/arrows select pads without playing.', 'F-DRUM/F-BROWSE: two distinct available owned samples/presets and audible pad baseline; select pad, browse/next/previous and silent-selection routes separately. Grade selection/loaded identity only, no sound/timing criterion.')
add(2, 'Pad copy and local options', '47 48 49 50 51', 'Duplicate source-to-destination replaces destination pad devices but retains its recorded notes. Selected pad offers choke group/transposition; Shift-pad opens custom-color choice saved with Set and shown on Push, not Live. No LED palette, note number or choke/DSP law follows.', 'F-DRUM: owned source/destination devices and destination notes, actual offered controls; copy then inspect pad options/color gesture on reset trial. Record membership and choice presence only; hardware colors and save/reopen are U.')
add(2, 'Drum step editing', '53 54 56 58 63', 'Pad selection enables sequencing; steps add/delete notes, Mute deactivates without deletion and Solo solos the sound. Delete can clear pattern/pad notes; Delete on a pad without notes in current pattern removes its devices. Triplet layout has inactive pads; no event/grid equation is supplied.', 'F-DRUM/F-REC: positive audible rack, separate occupied/empty steps and a populated no-note pad with retained device identity. Invoke each deletion/mute/solo branch on separate copies, retaining context and paired positive output; all MIDI/pad numeric outputs null.', 'midi-output')
add(2, 'Record, Accent and overdub', '67 68 69 70 71 72 73', 'Record alternates record/playback/overdub, with metronome/count-in display context. Accent overrides velocity-sensitive playing/step entry and velocity-pad selection; tap latches and hold is momentary. No velocity byte/force curve, countdown or event timing oracle is added.', 'F-REC: explicit eligible arm/monitor/transport and active instrument/pad baseline; record then overdub, compare Accent off/tap/hold with accepted velocity mode. Retain actual events and display only as ungraded observations.', 'recording')
add(2, 'New and Workflow modes', '74 339 341 342 345 346', 'Scene Workflow Duplicate captures playing clips and New omits selected clip while preparing new material. Clip Workflow Duplicate/New narrows to selected track/clip while other clips continue; Shift-Duplicate captures a scene. Seamless language supplies no audio or scheduler metric.', 'F-SESSION: two positive playing tracks, explicit Scene/Clip Workflow; compare New/Duplicate/Shift-Duplicate in reset copies with before-inventory. Timing and empty-slot boundaries remain U.', 'timing')
add(2, 'Fixed Length and Phrase Sync roles', '76 77 78 79 80', 'Fixed Length and held length selector govern new recording span; enabling during record stops writing and loops preceding material. Phrase Sync relates recording start inside the chosen phrase to current song phase, unlike described beginning-of-clip start. No phrase modulo or quantization formula is adopted.', 'F-REC: positive eligible recording and nonzero length, explicit global quantization and running transport; compare Phrase Sync off/on at known different song positions, then enable Fixed Length during separate pass. Capture ranges/events ungraded.', 'timing')
add(2, 'Quantize controls and record-swing context', '87 88 89 90 91 92', 'Quantize and held settings expose note-grid, amount, swing and record quantization; pad modifier narrows to that drum. Record Quantize with Swing is described as not applying swing to automatically quantized notes. Algorithms and exact note positions stay with MIDI/groove/record owners or U.', 'F-EDIT/F-REC: two off-grid drum parts, explicit record quantization and admitted nonzero Swing with positive recording/output; compare pad/clip and live-record routes. No timing or grid formula is graded.', 'editing')
add(2, 'Focus-dependent Arrangement recording', '94 95', 'Record toggles Arrangement recording when Arrangement is focused; Shift-Record requests it from Session focus. In Arrangement focus Shift-Record instead toggles Session recording. Other selection/recording prerequisites and actual written events retain their owners.', 'F-REC: independently valid eligible Set and explicit software view focus/arm/monitor/transport; compare Record and Shift-Record in each view on separate copies. Capture actual recording owner without global dispatch or event oracle.', 'recording')
add(2, 'Pitched/Scale controls', '102 110 112 113 114 116 117 118 119 120 121 122', 'Instrument Note Mode offers pitched pads; Scale selects key/type, Layout/Direction, Fixed and In Key/Chromatic settings. Scale settings are described as Set-persistent and default-Set eligible; Delete-pad removes same-pitch notes in current loop. No pad-note/tuning/default/velocity equation follows.', 'F-PITCH: active instrument and nonzero notes/output, inspect Scale options and two admitted layouts, then same-pitch deletion with retained inside/outside-loop notes. Save/default-Set and actual pad outputs remain ungraded.', 'pad-role')
add(2, 'Melodic sequencer layout and range', '124 125 126 127 128 130', 'Layout selects melodic sequencers; held Layout exposes loop pads and Shift-Layout locks per track. Rows use selected scale pitches and columns chosen grid steps; Octave/touch strip and Shift alter range. No exact note-to-pad or step-time equation is supplied.', 'F-PITCH/F-EDIT: positive instrument/clip with distinct pitches, change Layout, hold/lock loop and change range using actual offered controls. Record identities/notes ungraded, without inferring figure labels.', 'pad-role')
add(2, 'Loop pages, follow and duplication', '133 134 135 142 143', 'Loop pads set span/view; viewed page may differ from sounding page. Reselecting loop or holding Page navigation restores follow, while out-of-loop page selection changes loop. Page Duplicate adds notes over destination and Delete-page clears first.', 'F-EDIT: positive multi-page loop with occupied destination; compare selected view/follow/page changes and duplicate on reset copies. Retain actual loop bounds/notes; no sample rounding or merge formula.', 'timing')
add(2, 'Track navigation and arm context', '215 216 217 218 219 220', 'Lower controls/arrows select tracks; MIDI selection is described as auto-arming and held track control or Record-plus-track manually arms. Up/down has Scene versus Clip Workflow scope and source describes immediate Legato-like continuation. No universal arm/default or timing law is supplied.', 'F-SESSION/F-REC: positive tracks with explicit arm/monitor/record/Workflow; compare selection versus manual arm and up/down under both modes in independent copies. Record host states/output with no ownership race oracle.', 'timing')
add(2, 'Device editing and pages', '222 223 224 225 226', 'Device mode selects current-track devices via upper display controls; pressing selected control enters Edit with lower parameter pages and navigation for further pages. Leftmost upper control returns to top level. Actual target banks/plug-in support remain separate.', 'F-DEVICE: two admitted active devices and one with offered extra pages, positive processed output; select/edit/page/return. Inspect selected identity/control presence only, not numeric conversion or full bank parity.')
add(2, 'Device insertion, mute, reorder and racks', '228 229 230 231 232 233 234 235 238 239 240', 'Add Device browses insertable types; instrument loading replaces existing instrument, effects have documented chain-side roles. Delete/Mute plus device and held-control encoder reorder are entrypoints. Rack device unfolding/macros/chain selection has distinct context, with Drum Rack fold state described as software-controlled here.', 'F-DEVICE: owned instrument/effect/multichain rack, positive enabled path and retained order; separately add, disable/re-enable, reorder and select rack chains. Grade membership and offered context only; rack semantics/DSP stay owned.')
add(2, 'Track/global Mix and split pan', '242 243 244 245 246 247 248 249 250 251', 'Mix alternates selected-track and visible-track global controls; Track Input/Output exposes routing. Extra return/track navigation, Shift refinement and Master previous-track return are provided. Split pan disables Global dial while Track mode offers corresponding pan controls.', 'F-MIX: independently active two-track/return paths and explicit ordinary/split pan; inspect Track/Global/Input-Output, navigation and Master return. Numeric routing/mixer effects remain with existing owners.')
add(2, 'Mix-context rack/group expansion', '253 254 255', 'In Mix context, group/rack tracks can be unfolded with their lower display control to expose contained tracks/chains; arrows reach additional contents and Select-pad jumps to its mixer. This is distinct from Device-context Drum Rack unfolding.', 'F-MIX: owned group and Drum Rack with distinct positive chains; unfold via track lower controls and Select-pad, compare device-context state separately. Grade display/selection only, no graph or sum law.')
add(2, 'Automation controls and status', '257 258 259 260', 'Automation toggles Session Automation Arm; Delete-touch encoder deletes automation or resets unautomated default. Display dots distinguish automated/overridden parameters; Shift-Automation re-enables overridden automation. Numeric default, events, persistence and return timing remain U.', 'F-AUTO: independently changing active envelope and untouched eligible parameter, explicit recording off before override and actual arm/record/running transport for a separate pass. Inspect control/status only; runtime audio and point production null.')
add(2, 'Held-step automation and notes', '262 263 264 265 294 296 297 298 299 300 301 302', 'Clip mode held steps expose note Nudge, coarse/fine Length and Velocity including multiple/empty steps; Device/Mix held steps edit per-step parameter automation even without notes. No note-time percentage conversion or generated event law is supplied.', 'F-EDIT/F-AUTO: separate occupied/empty/multiple steps and positive active target with nonzero base/amount/output; edit note versus device/Mix modes on reset copies. Retain notes/envelope output as ungraded.', 'editing')
add(2, 'Session entry, selection and stopping', '304 305 311 312 313 314 315 316 318 319 320 322', 'Held Session/Note offers momentary modes; Session pad/scene controls launch material, Select-pad selects without launch, Duplicate copies clip and Stop Clip/Mute/Solo have selected-track, held-track and locked contexts. Shift-Stop Clip stops all. New-record selected-track sentence lacks full slot context and stays U.', 'F-SESSION: populated and empty slots with explicit arm/record/monitor/launch context, independently positive clips and confirmed pending state if needed; compare select/launch/stop/copy routes separately. Scheduling and actual pad/event output null.', 'pad-role')
add(2, 'Session Overview access', '325 326', 'Held Layout opens Session Overview; Shift-Layout locks and Layout unlocks it. Pads select larger scene/track blocks and scene controls wider ranges. No figure-derived numeric pad/block mapping or LED palette is prescribed.', 'F-SESSION: sufficient populated scenes/tracks for interior navigation; hold and lock Overview then select a block. Retain actually controlled region without numeric row/column oracle.', 'pad-role')
add(2, 'Setup response and brightness controls', '332 333 334 335 336 337 338 339', 'Setup exposes Pad Sensitivity, Gain, Dynamics, Display Light, LED Brightness and Workflow. The source describes response curves and a linear-setting recipe, but these supply no force/velocity/LED calibration, numeric hardware output or default-build guarantee.', 'On independently accepted Push 2 inspect named Setup controls and two admitted settings, preserving positive pad/output baseline and model/firmware. Grade presence/selected setting only; no pressure, light or curve measurement oracle.')
add(2, 'Simpler sample display/control entry', '171 172 173 175 176 177 178 180 181 182 184 197 198 202 211 212 213', 'Push 2 sample workflow uses Simpler: empty state prompts sample browsing, loaded waveform/position/zoom controls and Classic/One-Shot/Slicing choices are exposed. Simpler Edit pages, crop/reverse and slice creation/nudge/split/delete are controller entrypoints only; all mode/voice/DSP/sample semantics remain with sample-instrument and conversion/media owners.', 'F-SAMPLE: independently readable nonzero sample and accepted Simpler, retain source bytes and known mode/markers; inspect empty versus loaded display and offered controls in each mode. Use only existing-owner operations; audio, slicing and marker numeric outputs remain U.')
add(2, 'Clip mode controls and display', '267 268 269 271 272 273 274 275 279 281 283 288 290 292', 'Clip opens selected-clip parameters with audio/no-selection prompt, loop/start/end controls, zoom and audio Warp/gain/transpose context. MIDI layouts have Crop and sequenceable-area display/range navigation. Clip View and MIDI owners retain region/edit algorithms; no pad/time or folded-view numeric law is added.', 'F-EDIT/F-SAMPLE: known audio and MIDI clips plus no-selection case, positive sources and explicit loop/layout; inspect Clip controls, offered Crop/range/zoom and sequenceable area. All timing, detune conversion, loop and sample outputs null.', 'editing')
add(2, 'Touch strip and User Mode roles', '371 378', 'Instrument real-time touch strip selects pitch bend/mod wheel with Select-tap; melodic sequencing changes range and Drum Rack changes bank. User Mode disables built-in roles for alternate mapping; recommended relative mode is not exact configuration-token/codec equivalence.', 'F-PITCH/F-DRUM: positive active eligible instrument expression target then rack/sequencer, admitted nonzero target/base and output; compare actual strip/User modes via existing mapping owner only. Signal/protocol outcomes remain null.', 'signal')

gaps = {
 'PROTOCOL': ('Hardware, firmware and protocol', 'Accepted hardware/firmware/platform/USB/ports, messages, LED palette/framebuffer, touch/pressure/velocity calibration, pedal polarity, latency and User Mode protocol remain unknown. Source presence and control names are not hardware capability proof.'),
 'CONTEXT': ('Model and ambiguous source contexts', 'Per-mode/track/layout defaults, unsupported/empty/selected-slot recording predicates, conflicting button/context wording, model note maps and same-label behavior require evidence. Push 1 source cannot establish Push 2/3 parity.'),
 'EDIT': ('Editing and boundary outcomes', 'Empty/end/overlap/range/duplicate/choke/note/step boundaries, arbitrary slice placement, quantization, note expression/tuning and admitted malformed controls have no new numerical, refusal or normalization law.'),
 'STATE': ('History and durable state', 'Undo grouping, cancel/rollback, saved override/arm/mode/selection/Workflow/scale/pad settings, defaults, device/clip transfers and reopen migration remain unknown beyond documentary roles.'),
 'CLOCK': ('Transport, recording and rates', 'Recording ownership, event generation, quantization/phase, repeat/swing/pressure response, automation return, engine/sample-rate/block/tempo/transport transitions and synchronization remain ungraded.'),
 'LOSS': ('Failure, source loss and teardown', 'Controller/port/media/device/track loss, disconnection/reconnect, engine restart, concurrent editing, close/replace Set and quit during held inputs/record/pending operations have no new recovery, cleanup or silence deadline.')
}
probes = [
 ('PROTOCOL', 'hardware', 'protocol', 'Independently accepted matching model/firmware/host/USB/input/output and positive pad/encoder/display response first. Retain actual events and feedback while changing one offered mode; no device is acquired or simulated, no packet/LED/touch codec or latency oracle.'),
 ('CONTEXT', 'inactive', 'negative', 'Start from independently active eligible instrument/pad/section and nonzero source/base/amount/gain with nonmuted output; compare another actually offered ineligible mode/track or disabled path against matched positive trial. Silence/absent controller cannot prove no-effect.'),
 ('CONTEXT', 'selected-slot', 'boundary', 'Compare populated selected/unselected and independently empty selected slots with arm/monitor/record/transport/Workflow declared. Inspect launch/record availability and effects without deriving empty-slot recording law from the broad selected-track sentence.'),
 ('EDIT', 'boundaries', 'boundary', 'On disposable copies compare valid interior step/page/sample/range with first/last/empty/occupied destination, equal/reversed numeric text and multi-selection. Use offered controls only; no clamp/refusal/pad-index/merge rule.'),
 ('EDIT', 'malformed', 'malformed', 'After valid positive edit, attempt abc/NaN/out-of-range text through actually offered Live companion control or independently understood saved-state owner. Hardware encoders have no invented text parser or hidden command; missing admission remains U.'),
 ('STATE', 'undo', 'undo', 'Retain complete note/clip/device/route before-inventory, then separately edit step, duplicate pad/page, load device and record automation. Invoke offered Undo/Redo; generic entrypoints do not guarantee transaction grouping or restored physical state.'),
 ('STATE', 'cancel', 'cancel', 'Begin offered browse/load, held layout/parameter gesture or length selection, then dismiss/release using available controls before and after actual commit in separate copies. No universal cancellation or rollback is assumed.'),
 ('STATE', 'reopen', 'persistence', 'Save/reopen disposable Set after scale/Workflow/layout/pad response/automation edits separately, keeping required source/controller then removing it in a copy. Record Set/global/controller state without broad persistence or firmware-default assumptions.'),
 ('CLOCK', 'record-and-automation', 'automation', 'Independent nonzero source, eligible armed/monitored target, explicit running transport and appropriate record/Automation Arm plus active nonzero envelope/base/depth first. Compare per-step versus live pass, manual override/re-enable and recorded playback without event/timebase or return comparator.'),
 ('CLOCK', 'transport-rate', 'sample-rate', 'After positive playback/record baseline compare stop/start/seek/loop/tempo/meter changes, then separately actually supported 44.1/48/96 kHz and 64/512-frame settings or engine restart. No repeat/latency/velocity/signal invariance or phase deadline.'),
 ('LOSS', 'disconnect', 'source-loss', 'After independently working source/target and accepted hardware input/output baseline, remove only available controller/port/media/device in separate copies during held pad/encoder or recording; reconnect through offered controls. No stuck-note prevention, silence or reconstruction oracle.'),
 ('LOSS', 'teardown', 'teardown', 'During positive held note, recording, step edit or pending browse operation separately close/replace Set, remove track or quit using offered controls. Retain prompts/physical and software state if available; no completion/cleanup/flush guarantee.')
]
for model in [1, 2]:
    for suffix, (title, contract) in gaps.items():
        requirements.append(dict(id=f'REQ-PUSH{model}-WF-U-{suffix}', model=model, title=title, provenance='U', target_applicability='U', contract=contract, source_blocks=[]))
    for suffix, label, kind, action in probes:
        addcase(f'P{model}-U-{label.upper()}', f'REQ-PUSH{model}-WF-U-{suffix}', model, label.replace('-', ' ').capitalize(), kind, action, None, [])

assert len({r['id'] for r in requirements}) == len(requirements)
assert len({c['id'] for c in cases}) == len(cases)
dump('requirements.json', requirements)
dump('cases.json', cases)
counts = dict(requirements=len(requirements), requirement_grades=dict(Counter(r['provenance'] for r in requirements)), cases=len(cases), case_kinds=dict(Counter(c['kind'] for c in cases)), documentary_oracles=sum(c['documentary_expected'] is not None for c in cases), null_documentary_oracles=sum(c['documentary_expected'] is None for c in cases), retained_blocks={'Push1':303,'Push2':403}, target_oracles=0, per_model={str(m):dict(requirements=sum(r['model']==m for r in requirements),D12=sum(r['model']==m and r['provenance']=='D12' for r in requirements),U=6,cases=sum(c['model']==m for c in cases)) for m in [1,2]})
dump('counts.json', counts)
owners = ['midi-editing-tools.md', 'recording-comping.md', 'session-view-workflows.md', 'clip-view-workflows.md', 'arrangement-editing.md', 'routing-monitoring-latency.md', 'mixer-values.md', 'automation-envelopes.md', 'automation-workflows.md', 'remote-control-workflows.md', 'device-racks.md', 'device-simpler.md', 'warp-markers.md', 'mpe-workflows.md', 'tuning-systems.md']
pins = []
for name in owners:
    path = ROOT / 'wiki/specs' / name
    data = path.read_bytes()
    pins.append(dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), purpose='Existing canonical boundary only; no model/firmware/runtime proof'))
dump('owner-pins.json', pins)
dump('fixtures.json', {
    'common': 'Future finite setups only: disposable valid owned editable Set and explicit exact Live build/platform, model and independently supported firmware/hardware/USB/power/input/output/permissions. Retain actual mode/layout/track/clip/device/rack selection, focus, arm/monitor/record/Automation Arm, transport/tempo/meter/quantization, Workflow, source/content references and accepted control values before every reset trial. Source text and availability of tools do not prove connected hardware.',
    'Push1': 'Open prerequisite: independently accepted genuine Push 1 with known firmware/host/USB/ports and positively working built-in mode, pad/encoder/button/input/display response. Push 2/3 or a generic control surface cannot substitute. No hardware, profile script, message bytes or firmware is supplied or executed.',
    'Push2': 'Open prerequisite: independently accepted genuine Push 2 with known firmware/host/USB/power/ports and positively working built-in mode, pad/encoder/button/input/display response. Push 1/3 cannot substitute. No hardware/firmware updater, profile script, message bytes or protocol emulator is supplied or executed.',
    'F-BROWSE': 'Two future owned available loadable presets/samples in known folders plus an active device and empty MIDI track. Establish independently positive preview path before audition probes, with nonzero preview gain and nonmuted output. Browser visibility/selection and loaded device identity are separate from preview audio and format compatibility.',
    'F-DRUM': 'Known loaded Drum Rack with distinct populated active pads, empty pad and retained pad/device/note identities. Correct track arm/monitor and independently positive nonzero excitation, active chain and output required. Retain notes both inside/outside known loop and occupied destination before deletion/copy; no exact pad index, note number, velocity or pressure conversion is supplied.',
    'F-PITCH': 'Actually offered active instrument with admitted nonzero output and a known playable note pair, scale/tuning mode and expression destinations. Nonzero bend/wheel/base/depth and separately positive response before context/no-effect probes. Actual pad-to-note correspondence is future evidence, not inferred from a figure, default key or another model.',
    'F-REC': 'Eligible nonempty source/instrument/audio path with accepted input, explicit arm/monitor/record/Automation Arm as relevant, actual running transport and independently nonzero source/output. Retain count-in, fixed length/Phrase Sync if offered, Workflow, launch/record quantization and admitted nonzero movement/notes. Positive recording pass required before disabled/ineligible trial.',
    'F-EDIT': 'Known valid nonempty clip with separated notes/steps/pages, editable target, actual loop/selection/grid and retained before-inventory. Establish productive device/chain/output first. Each gesture/platform/layout/action branch uses reset copies; MIDI numerical formats, timebase and merge law are not provided.',
    'F-SESSION': 'At least three distinct populated scenes/tracks with independently positive nonmuted clips, plus identified empty slot. Actual selected slot/track, arm/monitor, Workflow, active source ownership, transport and launch settings recorded. Independently confirm pending launch before cancellation; selection and playback are separate.',
    'F-DEVICE': 'Two independently admitted active devices, multichain rack and owned disposable instrument/effect chain with retained order/identity. Nonzero source, enabled eligible processing, nonzero gain/amount and positive processed output before mute/no-effect comparisons; no arbitrary plug-in bank parity.',
    'F-MIX': 'Two independently positive source tracks, nonzero sends and nonmuted wet returns/Main output with correct receiver Monitor/arm/clip state. Explicit ordinary/split-pan and selected Track/Global mode. Isolate controls only after matched positive output baseline; numerical gains/coefficients stay with mixer/routing owner.',
    'F-AUTO': 'Independently changing active eligible automation envelope with nonzero source/base/depth/amount and nonmuted output; untouched parameter retained as separate default-identity control. Explicit record off before manual override; accepted Automation Arm/record/running transport and positive movement for live automation record. Per-step edit has named selected steps and actual target.',
    'F-SAMPLE': 'Future owned readable distinguishable nonzero sample with retained exact bytes/hash/duration/rate and source reference. Accepted active Simpler/sample mode and positively audible pad/playback baseline first. Empty state is separate eligibility context. Markers/regions and original sample retained before crop/reverse/slicing operations routed to their owners.',
    'active-positive-guard': 'Require independently supported matching hardware/firmware/host/ports and known usable input plus active eligible track/device/pad/envelope, correct mode/selection, nonempty source, nonzero base/depth/amount/gain/send, correct arm/monitor/clip state and nonmuted positive source/wet return/output. Recording needs explicit appropriate record/Automation Arm and running transport, plus admitted nonzero notes/movement and paired positive pass. No-effect requires a matched active positive baseline before changing only tested state. Missing hardware/target, silent source, zero wet path or absent feedback leaves U, never pass. Visible controls do not prove input, output, physical calibration or timing.',
    'not_provided': ['No Push hardware/controller/firmware/driver acquisition or execution', 'No ALS/audio/MIDI/reference/candidate output or protocol bytes', 'No model/pad numeric map, LED palette, touch/pressure/velocity curve or USB codec', 'No runtime comparator, latency/rate/force tolerance or compatibility result']
})
base = '../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/'
spec = '''---
id: SPEC-PUSH-CONTROLLER-WORKFLOWS
type: spec
status: draft
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Push 1 and Push 2 documentary applicability U
---

# Separate Push 1 and Push 2 documentary workflows

## Scope and evidence boundary

This partial F-08 draft gives separate text-supported profiles for Push 1 and
Push 2: setup, browser, drum/pitched/step layouts, record controls, device/mix,
automation, Session and preferences, plus selected Push 2 sample/Clip entrypoints.
[Research](../research/push-controller-workflows.md) retains interpretations and
source questions. [Coverage design](../research/full-live-specification-design.md)
governs closure. Neither profile is complete or a released implementation input.

**D12** means the retained official Version 12 chapter for that named model,
captured 2026-10-19. Every new clause has **exact-12.4.3 applicability U**, including
controls, modes, availability, default and firmware contexts. All target expected
and comparison fields are null, all grades U and all cases unexecuted. Only named
textual controls/display/selection/membership roles have documentary proposals.
Signal, timing, recording, MIDI, pad-role/numeric/model and protocol cases also
have null documentary expectations/comparators with source_claim retained separately.
No case closes a compound signal or physical-hardware clause.

Push 1 text is not Push 2 or Push 3 evidence. Broader Push 3 standalone/firmware,
all 149 controller-directory protocols, complete control references, pedal/pressure
calibration, user profiles and device-bank compatibility remain open. Figures,
inline glyphs and linked videos/help are not inspected. No physical pad placement,
button label or color palette is inferred from an image. Public pad counts and
examples are documentary context, not numeric pad/MIDI oracles.

## Canonical owners and prerequisites

[MIDI editing/tools](midi-editing-tools.md) retains note edits/quantization;
[recording](recording-comping.md) retains record, count-in, punch and Capture;
[Session](session-view-workflows.md), [Clip View](clip-view-workflows.md),
[Arrangement](arrangement-editing.md) and [launch](clip-launch.md) retain ordinary
selection/clip/scene/loop and recording eligibility. These new controller gestures
do not supply their event storage, note merging or scheduler equations.

[Automation storage/evaluation](automation-envelopes.md), especially REQ013,
retains unknown editing/runtime. [Automation workflows](automation-workflows.md)
owns generic record/override/re-enable and clip-envelope roles; controller buttons
do not establish numerical interpolation, event generation or override persistence.
[Routing/monitoring](routing-monitoring-latency.md) and [mixer values](mixer-values.md)
retain controls/coefficient and admitted signal-path conditions. [Racks](device-racks.md),
[Simpler](device-simpler.md), [conversion](audio-to-midi.md),
[Warp markers](warp-markers.md), [MPE](mpe-workflows.md) and [tuning](tuning-systems.md)
retain device, slicing, Warp, expression and scale/tuning computation. A named
Nudge or Warp control does not supply those algorithms. [Remote control](remote-control-workflows.md)
and [MIDI mapping](midi-user-mapping.md) retain generic/manual mapping and finite
configuration codec boundaries; User Mode recommendations do not prove exact token
equivalence or complete protocol support. [Project/media](project-media-workflows.md)
owns shared save/history/media operations. Entry points do not imply transactions.

The [future fixtures](../../analysis/ableton-live-12.4.3/full-spec-v1/push-workflows/fixtures.json)
require independently accepted matching hardware/firmware/platform/ports and a
working positive response before each role investigation. Hardware is absent here.
Retain actual mode/layout, target/track/clip, focus/selection, arm/monitor/record,
Automation Arm, transport/Workflow, source references and accepted values. A source
paragraph cannot supply these capabilities. Missing control/hardware remains U.

Audio, recording and no-effect probes additionally require nonempty source,
enabled active eligible instrument/effect/envelope, nonzero base/depth/amount/gain/
send, correct receiver monitoring and nonmuted positive output/wet return. Confirm
admitted input and nonzero response independently. Recording needs explicit valid
record context and running transport plus paired working pass. Silent source,
inactive section, zero wet amount, muted return or absent hardware is not a pass.

No private USB/MIDI/LED/framebuffer format, pressure/force law, latency, numerical
scale/pad map, RNG, audio waveform, voice model, tolerance, rate invariance or
firmware updater is invented. Setup/update text authorizes no hardware action,
installation, original/native/runtime probe, emulator or independent implementation.

## Model requirements
'''
for model in [1, 2]:
    spec += f'\n## Push {model}\n'
    for r in requirements:
        if r['model'] != model:
            continue
        spec += f"\n### {r['id']} — {r['title']}\n\n**{r['provenance']}/target-U.** {r['contract']}\n\n"
        if r['source_blocks']:
            spec += 'Evidence: ' + ', '.join(f'[{ref}]({base}manual-push-{model}-blocks.json)' for ref in r['source_blocks']) + '.\n'
        else:
            spec += 'Evidence: unsupported outcome; ungraded investigation obligation for this model.\n'
spec += f'''
## Finite cases and remaining obligations

The [{len(cases)} proposed cases]({base}cases.json) map to {len(requirements)}
[requirements]({base}requirements.json): 53 D12 and 12 U. Push 1 has 26 D12/six U
and 38 cases; Push 2 has 27 D12/six U and 39 cases. Eighteen cases have only visible
documentary proposals; 59 have null documentary oracles. All 77 target oracles are
null/U and unexecuted. These counts do not close either model or any profile family.
Each named action branch/control mode requires its own later retained result.

| Case | Requirement | Kind | Action focus |
| --- | --- | --- | --- |
'''
for c in cases:
    spec += f"| {c['id']} | {c['requirements'][0]} | {c['kind']} | {c['title']} |\n"
spec += f'''
## Source-context questions

[Research local questions](../research/push-controller-workflows.md#source-context-questions)
retain Push 1 Note/Layout wording, selected-track/new-clip recording context and
mode-specific settings/labels. Ambiguous text is not silently repaired from Push 2
or source figures. Source Session/overview colors and pressure/velocity recipes
are retained but not adopted as LED or physical-calibration laws.

Per-model U probes retain inactive/unsupported paths, occupied/empty/boundary
targets, malformed admitted inputs, cancel, Undo/Redo, save/reopen/migration,
automation ownership, transport/rates, disconnection/source loss and teardown.
Pedals, every remaining reference control, profile bank/protocol and firmware
failure handling remain incomplete. No whole hardware family or compatibility is
claimed. [Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage)
retains publication/build applicability.

## Analyst evidence appendix

[Source ledger]({base}sources.json) pins both exact URLs/final URLs, UTC capture,
Version 12 identity, HTML size and SHA256. [Owner pins]({base}owner-pins.json)
retain 15 canonical boundaries unchanged. [Counts]({base}counts.json),
[frozen manifest]({base}manifest-author-r1.json), [parser]({base}source_parser.py)
and read-only [validator]({base}validate.py) identify the reviewable packet.

| Model | Retained chapter | Blocks | Text |
| --- | --- | --- | --- |
| Push 1 | §35/using-push-1; setup through control reference/footswitches |303| [Push 1 text]({base}manual-push-1.txt) |
| Push 2 | §36/using-push-2; setup through control reference/footswitches |403| [Push 2 text]({base}manual-push-2.txt) |

Original HTML lines, anchors, section and heading context accompany each derived
block. Figures/PDFs/videos and native/controller code were not inspected. Root
integrates shared indexes, coverage, questions and log after independent review.
'''
(ROOT / 'wiki/specs/push-controller-workflows.md').write_text(spec)
(P / 'spec-r1.md').write_text(spec)

research = f'''---
id: RESEARCH-PUSH-CONTROLLER-WORKFLOWS
type: research
status: current
updated: 2026-10-19
access: analysis
revision: 1
target: Ableton Live 12 Suite 12.4.3; Push 1/Push 2 documentary applicability U
specs: SPEC-PUSH-CONTROLLER-WORKFLOWS
---

# Push 1 and Push 2 documentary evidence

## Question and role

Which bounded observable controller workflows are described for each model?
The [canonical draft](../specs/push-controller-workflows.md) owns proposed clauses,
while the [coverage plan](full-live-specification-plan.md) and
[coverage design](full-live-specification-design.md) govern F-08 closure. This
analyst context has read original-reference documentation and cannot implement.
No original/native/application/controller/hardware/audio/MIDI/firmware/candidate
execution, installation, emulator or hardware acquisition was performed.

## Retained sources and extraction

The inventory [TOC](../../analysis/ableton-live-12.4.3/full-spec-v1/inventory/manual-toc.json)
identifies exact §35/§36 model URLs. No existing exact chapter capture was found
in retained source catalogs. Two official Version 12 HTML pages were captured
once; [sources]({base}sources.json) retains URL/final URL, UTC, edition, size/SHA.
Neither source identifies firmware/platform support or exact 12.4.3 applicability.
'''
for s in json.loads((P / 'sources.json').read_text()):
    research += f"\n- {s['id']}: [{s['path']}]({base}{s['path']}), {s['bytes']} bytes, SHA256 `{s['sha256']}`, captured `{s['captured_utc']}`; [official chapter]({s['url']}).\n"
research += f'''

The retained pure [parser]({base}source_parser.py) extracts numbered chapter
headings/paragraphs/lists only, excluding manual navigation. It is copied unchanged
from the pure automation packet parser; no original code is involved. Push 1 has
303 blocks, Push 2 has 403. Each retains HTML line, anchor/section and heading
context, plus a derived text view. Text controls are used only when explicitly
named; figures/inline glyphs/linked videos/tutorials/PDFs were not inspected.

## Interpretation and limits

Push1 setup P1-B007 and Push2 P2-B006/B007 are separate connection/power/firmware
contexts. Automatic/driver-free prose is not proof of a working route on this
host, USB packet specification or updater/recovery law. Browsing P1-B009–B015
and P2-B009–B016 uses different named hierarchy/load/preview controls; source
similarity is not generic controller/plug-in compatibility. Content availability
and positive preview output must be established independently.

Drum layouts/steps and melodic pages have model-specific Note versus Layout,
Select, copy/delete and momentary/lock contexts. All pad-number/velocity/MIDI
outputs and timing oracles are null. Textual note membership, active/inactive
pad roles and shape examples cannot provide a MIDI note map, pad calibration,
quantization or voice equation. Push1 P1-B049 limits pad-note deletion to loop;
Push2 P2-B058 adds a no-note pad device-deletion branch, kept distinct.

Record/Fixed Length/New/Workflow/Repeat/Quantize and navigation refer to generic
record/clip/scene owners but require this model's explicit gestures and context.
Push2 P2-B079 Phrase Sync and B094/B095 focused Arrangement/Shift recording have
no adopted modulo/clock or written-event comparator. Push1 P1-B069 and Push2
P2-B083 pressure descriptions supply no pressure-to-volume mapping. Numeric
settings/examples, swing and seamless adjectives are not timing/audio oracles.

Device/mixer/rack modes are scoped to corresponding display context. Push2
Device Rack unfolding P2-B238 and Mix track/rack expansion P2-B254 are different
controls/contexts; the draft does not collapse them into a contradiction or one
fold law. Split-pan mode exceptions remain explicit. Positive source, enabled
nonzero route and unmuted wet return/output are prerequisites, not observations.

Automation P1-B173–B176 and P2-B257–B260 supplies controller arm/delete/re-enable
entry and different presentation, preserving existing REQ-AUTOMATION-ENVELOPES-013
and [generic automation workflows](../specs/automation-workflows.md) unknowns.
Held-step roles do not settle event production, normalization, Nudge arithmetic
or runtime return. Push2 Simpler/Clip pages are entrypoints to existing owners,
not rewritten sample/Warp/slicing/loop kernels. User Mode recommended relative
names do not equal historical configuration tokens or prove host protocol.

## Source context questions

| Local ID | Retained context | Treatment |
| --- | --- | --- |
| Q-PUSH-001 | P1-B019/B030/B035/B037 describes Note transitions/holds, whereas P1-B032 calls for Layout to enter velocities. P2-B020/B031–B038 consistently uses Layout. | Preserve both Push1 texts and leave exact Push1 transition/control-label association U. Do not silently copy Push2 physical layout or infer a missing button from figures. |
| Q-PUSH-002 | P1-B195 and P2-B305 say a selected track pad press records a new clip while also describing pad launch, without stating all slot/arm/record preconditions. | Treat new-record sentence as incomplete source context; separate populated/empty, selected/unselected and actual arm/monitor/record trials. No selected-populated-slot unconditional recording law. |
| Q-PUSH-003 | P1-B147 labels a triplet color Light Red while saying columns unlit; other per-model color lists and numeric velocity/aftertouch examples are context-sensitive. | No LED palette/intensity, force law, packet or pad-index oracle adopted. No contradiction claim without matched model/mode/firmware and actual states. |

Push1 control-reference Clip Mode wording and examples remain in their exact
contexts; no uninspected icon or UI label association is inferred. Model defaults,
scale persistence, preferences and broad recording claims remain target U.
Root owns shared question integration, including broader
[Q-027](../questions.md#q-027-whole-product-specification-evidence-and-version-coverage).

## Future cases and guards

There are 65 requirements (Push1: 26 D12/six U; Push2: 27 D12/six U) and 77 cases
(38/39). Eighteen control/display/membership proposals have documentary predicates;
59 are null, including all signal/timing/pad/recording/protocol/wholly unknown
probes. All target outcomes/comparators are null/U/unexecuted; source_claim is
separate and never an audio/event oracle. Neither profile is complete. Remaining
reference controls/pedals, Push3 standalone/firmware and 149 controller protocols
remain product obligations rather than silently removed denominator entries.

[Fixtures]({base}fixtures.json) require accepted genuine matching model/firmware/
host/ports and independently working input/display/output. No hardware or media
is supplied. Each probe declares actual mode/target/source, active eligible
section/envelope, nonzero base/depth/amount/gain/send, correct arm/monitor and
nonmuted positive output/wet return with a matched positive trial. Recording also
requires admitted input, explicit appropriate record/Automation Arm and running
transport. A silent source, absent controller or unsupported path stays U.

Per-model finite unknown cases cover inactive contexts, selected/empty slots,
boundaries/malformed admitted controls, Undo, cancel, save/reopen, automation,
transport/rates, disconnection/source loss and teardown. No fake port/host,
firmware action, protocol/timing/pressure tolerance or cleanup law is invented.
Generic owners keep numerical controls and saved-state representation.

## Frozen review packet

[Owner pins]({base}owner-pins.json) retain 15 current canonical boundaries unchanged;
[manifest]({base}manifest-author-r1.json) seals source/derived bytes, fixtures,
requirements/cases, author/parser/validator and both canonical snapshots.
Read-only [validation]({base}validate.py) reproduces all 706 blocks, checks source/
owner hashes, permodel evidence/IDs/counts/oracles, exact browser ID equality,
snapshots, local links/anchors, complete payload inventory and untracked-aware
whitespace. It prints stdout only and never rewrites sealed results.

Separate semantic review is required. Root integrates shared catalogs, coverage,
questions and log. This packet provides no original-reference execution,
independent implementation, hardware compatibility or full-profile closure.
'''
research = research.replace('Push1', 'Push 1').replace('Push2', 'Push 2').replace('Push3', 'Push 3')
(ROOT / 'wiki/research/push-controller-workflows.md').write_text(research)
(P / 'research-r1.md').write_text(research)
print(json.dumps(counts, indent=2))
