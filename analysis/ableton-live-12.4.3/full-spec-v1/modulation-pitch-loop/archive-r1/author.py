"""Build analyst documentary views and finite unexecuted cases; no product execution."""
from pathlib import Path
import json, hashlib, collections
P=Path(__file__).resolve().parent
R=P.parents[3]
REQ=[];CASES=[];DEVS=[]
def write(name,obj):
 (P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def expand(text):
 out=[]
 for part in text.split(','):
  if '-' in part:
   a,b=map(int,part.split('-'));out.extend(range(a,b+1))
  else:out.append(int(part))
 return out
contexts={
'AP':('Wander waveform in Synced Panning, Amount nonzero, Phase Offset nonzero','Amount, Time mode and Phase Offset','sustained dual-mono tone'),
'AS':('MIDI On, Poly 8, source with held notes, Note Latch on, attack/release nonzero','MIDI On, correction strength, modulation depth and pitch range','monophonic pitched/unpitched phrase plus authored MIDI events'),
'CE':('Chorus with nonzero Feedback and Amount, then Vibrato with disabled Feedback/Dry-Wet','Mode, Rate, Amount and Feedback Invert','burst followed by sustained distinct-channel tone'),
'PF':('Doubler with nonzero Feedback, enabled Env Fol with nonzero amount and LFO2 Mix interior','Mode, Envelope Amount, LFO2 Mix and sync rate','amplitude steps and transient burst'),
'SH':('MIDI Pitch Mode with held source note, Pitch mode, Delay on and nonzero Feedback','Pitch Mode, Coarse, Delay sync and Wide/Spread','dual-mono tone plus authored MIDI notes'),
'SR':('MIDI Poly 16 with gate active, held notes, active tuning, nonzero resonance and Granular mode','Polyphony, Use Current Scale, Quantize and Decay','broadband finite excitation plus held notes'),
'ST':('Freezer On, Freeze active, Retrigger Envelope, overlapping freezes, Delay On and Frz > Dly','Freeze, processing order, interval units and Resolution','successive distinguishable tone bursts'),
'VO':('External carrier from existing track, L/R mode, nonzero Unvoiced and active band levels','Carrier source, channel mode, Sens and band attenuation','distinct-channel carrier and voiced/unvoiced modulator'),
'BR':('Repeat active with captured material, Gate output mode, nonzero Volume, Variation 0','Repeat, Interval/Offset, Chance and Variation mode','distinct successive transient bursts'),
'LP':('owned loop A, completed overdub B, active overdub C, monitoring Never and Follow song tempo','Feedback, Reverse, Song Control and Quantization','distinct base/overdub phrase identifiers A/B/C')}
for line in (P/'authored-contracts.txt').read_text().splitlines():
 if not line:continue
 if line.startswith('['):
  slug,prefix,name,cls=line[1:-1].split('|');dev={'slug':slug,'prefix':prefix,'name':name,'class':cls};DEVS.append(dev);number=0
  blocks={r['locator']:r for r in json.loads((P/f'manual-{slug}-blocks.json').read_text())}
  continue
 parts=line.split('|');assert len(parts)==5,parts
 loc,kind,claim,action,expected=parts;number+=1
 refs=[f'{slug}:B{n:03d}' for n in expand(loc)];assert all(x in blocks for x in refs)
 rid=f'REQ-MPL-{prefix}-{number:03d}'
 evidence=[{'id':'D12-AUDIO-EFFECTS','block':b,'html_line':blocks[b]['html_line']} for b in refs]
 REQ.append({'id':rid,'surface':'SURF-DEVICE-'+slug.upper(),'device':name,'kind':kind,'strength':'D12','exact_build':'U','contract':claim,'evidence':evidence})
 CASES.append({'id':f'MPL-{prefix}-{number:03d}','requirements':[rid],'device':name,'kind':'documented-control' if kind=='ui' else 'signal-obligation' if kind=='audio' else 'documented-state','preconditions':['common-setup','positive-signal-guard'] if kind=='audio' else ['common-setup'],'setup_and_action':action,'documentary_expected':expected,'documentary_comparator':None if kind=='audio' else 'Compare only named control labels/choices/units/endpoints or explicit visible state transitions; no audio, waveform, latency, tolerance or private-state assertion.','expected':None,'target_grade':'U','executed':False,'source_blocks':refs,'fixture':'stimulus-recipes.json#'+prefix})
for d in DEVS:
 slug,prefix,name=d['slug'],d['prefix'],d['name'];context,controls,stimulus=contexts[prefix]
 rid=f'REQ-MPL-{prefix}-LIFECYCLE'
 REQ.append({'id':rid,'surface':'SURF-DEVICE-'+slug.upper(),'device':name,'kind':'lifecycle','strength':'U','exact_build':'U','contract':f'The required boundary, automation, transport, persistence, undo, malformed, cancellation, teardown and sample-rate outcomes for {name} in the retained device-specific state are unknown. No behavior is borrowed from a similarly named device or generic storage field.','evidence':[]})
 actions=[
 ('boundary',f'Initialize {context}; test documented numeric endpoints where available, then adjacent inadmissible values and zero/nonzero modulation with {stimulus}; move tempo from 100 to 120 BPM at a repeat/voice/LFO boundary.','Clamping/rejection, endpoint restoration, tempo event order, clock/sample rounding and response at exact boundary are unknown.'),
 ('automation',f'Initialize {context}; automate {controls} across two nonzero interior values and a mode change while {stimulus} runs; compare manual/mapped/automated presentation without assuming identical scheduling.','Automation eligibility, smoothing, event partition, mapping ownership and audible transitions are unknown; existing envelope storage is not their oracle.'),
 ('transport',f'Initialize {context}; run 4/4 at 120 BPM with {stimulus}, stop then resume at a different song position, and perform a separate seek while running.','Tail/held-note/capture lifetime, LFO/freezer/repeat reset and transport synchronization are unknown beyond the documentary clauses.'),
 ('persistence',f'Initialize {context}; save an owned Set/preset where offered, close/reopen and remove/rename external source tracks or imported media in a disposable copy.','Which selected modes, latch/freeze/captured/buffer state and source bindings persist, and missing-source handling, are unknown; shipped preset fields prove storage presence only.'),
 ('undo',f'Initialize {context}; make two edits to {controls}, replace device/preset, then global Undo/Redo; test local Undo/Redo separately if offered.','Undo grouping, interaction with captured audio/notes and restoration after replacement are unknown; Looper local overdub Undo remains a separate documented operation.'),
 ('malformed',f'On disposable owned copies only, attempt empty/truncated preset or malformed saved state; enter empty text, NaN, inf and 1e309 in exposed numeric controls associated with {controls}.','Admission, validation, messages, recovery and retained prior state are unknown; no successful import or a particular dialog is assumed.'),
 ('cancel',f'Initialize {context}; begin a device/preset replacement or supported source/import gesture, cancel before commit, then inspect prior state and resume {stimulus}.','Availability of cancellation, commit point, partial changes and buffer/capture preservation are unknown; no speculative modal dialog is imposed.'),
 ('teardown',f'Initialize {context}; while {stimulus} and wet-output baseline are active, delete an external source where relevant, remove device, undo removal, then close the owned Set.','Source-loss response, note release, frozen/recorded-buffer disposal, resource cleanup and silent-tail policy are unknown; no real-time deadline is asserted.'),
 ('sample-rate',f'Initialize {context} at 48 kHz with {stimulus}; request 44.1 kHz and then 48 kHz in supported audio settings while stopped, and separately while running.','Supported rate changes, compensation, resampling, pitch/clock alignment, captured-buffer lifetime and failure/cancellation behavior are unknown; request does not presume success.')]
 for suffix,action,unknown in actions:
  CASES.append({'id':f'MPL-{prefix}-U-{suffix.upper()}','requirements':[rid],'device':name,'kind':suffix,'preconditions':['common-setup','positive-signal-guard'],'setup_and_action':action,'documentary_expected':None,'expected':None,'target_grade':'U','executed':False,'comparison':None,'unknown':unknown,'source_blocks':[],'fixture':'stimulus-recipes.json#'+prefix})
write('requirements.json',REQ);write('cases.json',CASES)
recipes={'common-setup':{'set':'valid, editable, test-owned Set; reset per independent trial','signal_path':'isolated enabled device in active track/chain; route named input/MIDI source into it, with monitoring active when needed; explicit 4/4, 120 BPM and 48 kHz chosen as authored setups, not product limits','neutralization':'disable unrelated automation, mapping, randomization and effects except when named; set gain and wet output nonzero/unmuted; all values used as interior controls must first be admitted by target UI','references':'use owned disposable copies for destructive/replacement/malformed cases; never change immutable source artifacts'},'positive-signal-guard':{'enabled':'tested control/section enabled, correct mode, active routing and explicit nonzero amount/depth/send/feedback when testing its influence','baseline':'first demonstrate the relevant wet path responds to the test stimulus in a paired positive case; no effect caused by disabled control, zero amount, silence, missing notes, muted channel or dry-only output is evidence','negative_cases':'documented zero/disabled exception uses separate nonzero/enabled positive baseline, changes only the targeted setting, and leaves expected signal/comparator null unless independently supplied','stereo':'use equal samples in both channels only when dual-mono is specified; LFO channel equality is never generalized to audio equality from distinct stereo inputs','random':'no seed, distribution, sequence matching or expectation of identical repeated output is asserted','safety':'test-owned bounded low-amplitude source; high-feedback stability is not a grade or a claim'},'authored_audio':{'dual_mono':'four seconds; left=right=0.125*sin(2*pi*440*t); 48000 frames/s; silence before/after; this formula defines analyst input only','distinct_stereo':'four seconds; left=0.125*sin(2*pi*220*t); right=0.125*sin(2*pi*660*t)','amplitude_steps':'440 Hz dual-mono tone, amplitude 0.03125 for first two seconds, 0.125 next two; separate silence/held-tone segments for onset tests','broadband':'owned deterministic multitone 60, 440, 880 and 2400 Hz, each amplitude 0.025; finite 200 ms bursts at 0,1,2,3 seconds; intended bands must be confirmed active in target','phrases':'distinct analyst-owned A/B/C segments of 440/660/880 Hz, one 4/4 bar each at 120 BPM; loop orientation/content identifiers, not a measured resampling oracle'},'authored_midi':{'events':'Use explicit note-on/off pairs with admitted channel/note/velocity in a valid editable source MIDI clip. Single-note A then overlapping B; for voice-boundary cases use distinct held notes up to named voice count then one extra. Release all notes between trials.','limitations':'No MIDI byte codec, pitch-frequency mapping, voice allocation, stealing or ordering is supplied by this recipe.'}}
for prefix,(context,controls,stimulus) in contexts.items():recipes[prefix]={'initial_device_state':context,'controls':controls,'stimulus':stimulus,'audio':'choose the matching explicit authored_audio recipe; unpitched/voiced carrier materials must be owned retained fixtures before any future signal execution','midi':'authored_midi where applicable','observations':'record control state separately from audio. These recipes are finite proposed inputs, not reference results.'}
write('stimulus-recipes.json',recipes)
assert len(DEVS)==10 and len(REQ)==106 and len(CASES)==186
assert len({r['id'] for r in REQ})==len(REQ) and len({c['id'] for c in CASES})==len(CASES)
assert all(c['expected'] is None and c['target_grade']=='U' and not c['executed'] for c in CASES)
assert all(c.get('documentary_comparator') is None for c in CASES if c['kind']=='signal-obligation')
print('requirements',len(REQ),collections.Counter(r['strength'] for r in REQ),'cases',len(CASES),collections.Counter(c['kind'] for c in CASES))
