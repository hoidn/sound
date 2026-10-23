"""Author finite documentary predicates and explicit unknown probes; never execute Live."""
from pathlib import Path
import json
root=Path(__file__).resolve().parent
rows=[]
def add(req,dev,kind,setup,action,oracle,lines,grade='D12'):
 rows.append({'id':f'NME-{len(rows)+1:03d}','requirement':f'REQ-NATIVE-MIDI-{req:03d}','device':dev,'kind':kind,'setup':setup,'action':action,'documentary_oracle':oracle,'grade':grade,'source':{'id':'SRC-NATIVE-MIDI-MANUAL-20261019','text_lines':lines} if lines else None,'exact_build_grade':'U','execution':'unexecuted','comparator':'Only the stated predicate; no timing/channel/note-off/rounding implication' if oracle else None})
add(1,'Pitch','positive','Use Current Scale off, current clip has C major','Enable Use Current Scale','Pitch control displays scale degrees rather than semitones',[3,4])
add(2,'Arpeggiator','positive','Chord Trigger, held C3 E3 G3; transposition disabled','Run several steps','Each repeated block contains C3 E3 G3; equal-time ordering and note-offs ungraded',[15,16])
add(2,'Arpeggiator','positive','Play Order, press C3 then G3 then E3; settled held set','Inspect pattern order','Ordering follows the input play order; phase ungraded',[15,15])
add(2,'Arpeggiator','positive','Random Other; distinct held C3 E3 G3','Inspect one complete traversal','No pitch reused before other input pitches used; seed and frequency ungraded',[19,19])
add(2,'Arpeggiator','positive','Random Once; distinct held C3 E3 G3; no input change','Inspect consecutive full patterns','One generated pattern repeats while incoming MIDI remains unchanged',[20,20])
add(2,'Arpeggiator','positive','A known stable multi-note pattern, offset0','Set Pattern Offset1','Second pattern position becomes first and former first becomes last',[26,26])
add(3,'Arpeggiator','positive','Single C3; Distance+12st Steps2; scale awareness off','Inspect first complete transposition cycle','Pitches at C3, C4, C5 in successive transposition passes',[22,22])
add(3,'Arpeggiator','boundary','Free Rate100ms Gate150%, one held pitch','Run sequence','Nominal duration150ms, greater than100ms interval; exact timestamps and same-key lifecycle U',[21,24])
add(3,'Arpeggiator','positive','Local Root/Scale choosers active; clip scale defined','Enable Use Current Scale','Root/Scale choosers disabled and determined by clip',[23,23])
add(4,'Arpeggiator','positive','Hold on; one C3 physically held','Release C3 without another key event','Pattern continues after release; eventual teardown not covered',[25,25])
add(4,'Arpeggiator','positive','Retrigger Note, running held pattern','Add a new note','Pattern retriggers and retrigger LED flashes; first new event phase U',[30,34])
add(4,'Arpeggiator','positive','Repeats infinite and a stable held set','Observe beyond two pattern passes','Pattern remains eligible to repeat indefinitely; stopping/reset U',[35,35])
add(5,'Arpeggiator','positive','Velocity toggle off','Enable Velocity','Target and Decay controls available; event velocity formula U',[36,36])
add(4,'Arpeggiator','cancellation','Hold on; initial keys released','Play another note then release it',None,[25,25],'U')
add(6,'CC Control','positive','Pitch Bend at neutral, external MIDI output monitor','Move Pitch Bend below then above neutral','Pitch bend messages with downward then upward meaning; byte values and recipient response U',[45,46])
add(6,'CC Control','positive','Pressure control and external MIDI monitor','Change Pressure','Channel pressure/aftertouch event family generated; numeric encoding U',[47,48])
add(6,'CC Control','positive','Custom A assigned CC64','Toggle Custom A on then off','Assigned on/off or maximum/minimum CC messages generated; exact values U',[49,49])
add(7,'CC Control','positive','Custom B named Brightness assigned CC74','Save preset then reload','Custom name and assignment saveable; actual round trip unexecuted, exact-build U',[50,50])
add(7,'CC Control','positive','First bank visible','Choose controls9–16 then1–8','Requested bank shown; switching emission U',[51,51])
add(7,'CC Control','positive','Distinct assigned CC values visible','Click Send','Current MIDI CC values are sent; ordering/count/non-CC handling U',[51,51])
add(7,'CC Control','positive','Selected customizable control, Learn enabled','Receive CC74 then move that controller','Incoming CC can assign the customizable control; exact selection/forwarding U',[51,51])
add(8,'Chord','positive','Shift1+4 Shift2+7 other additions inactive; Strum0; Chance100%; input C3','Play C3','Root pitch set contains C3 E3 G3; tie ordering and note-offs U',[56,57])
add(8,'Chord','negative','Shift2+8 active','Assign Shift3+8','Additional same-pitch assignment deactivated',[58,58])
add(9,'Chord','positive','Learn enabled, initially no held notes','Hold C3 then E3 then G3; disable Learn','First C3 defines root, E3 then G3 fill slots in order; Learn stops assigning after disabled',[59,59])
add(10,'Chord','boundary','Generated pitch+7 with Velocity100% and Chance100%; note-on velocity64','Play isolated C3','Generated G3 has velocity64 and occurs for this input; note-off velocity U',[61,62])
add(10,'Chord','boundary','Generated pitch+7; Chance0%','Play isolated C3','Configured generated pitch is absent; root and note-off lifecycle otherwise ungraded',[62,62])
add(11,'Chord','positive','Shift1+7 Shift2+4, other additions inactive; positive Strum; neutral Tension','Play C3','Onset order C3 then G3 then E3; exact deltas U',[64,64])
add(11,'Chord','positive','Same chord as NME-027 with negative Strum','Play C3','Onset order E3 then G3 then C3; exact deltas U',[64,64])
add(11,'Chord','positive','Chord title bar context menu','Enable Send Per Note Events to Generated Notes','Option permits MPE events on generated notes; numeric bends/allocation U',[71,73])
add(11,'Chord','boundary','Strum+400ms, Tension/Crescendo0, legal pitches','Play chord',None,[64,69],'U')
add(12,'Note Length','positive','Note On source, Latch off, Free Length200ms Gate100%','Send note-on C3','Nominal generated duration200ms; sample placement and early source off U',[78,78])
add(12,'Note Length','boundary','Note On source, Latch off, Free Length200ms Gate50%','Send note-on C3','Nominal generated duration100ms',[78,78])
add(12,'Note Length','boundary','Note On source, Latch off, Free Length200ms Gate200%','Send note-on C3','Nominal generated duration400ms',[78,78])
add(13,'Note Length','positive','Note Off source, Latch off, Length100ms Gate100%; C3 on at0ms','Release C3 at300ms','Generated note starts upon input release rather than at input onset; nominal duration100ms; sample placement U',[79,79])
add(14,'Note Length','positive','Note Off source; on velocity100 off velocity20; Balance50%; DecayTime1s','Release at500ms',None,[81,82],'U')
add(14,'Note Length','boundary','Note Off source, positive Key Scale; compare C2,C3,C4','Measure generated lengths',None,[83,83],'U')
add(15,'Note Length','positive','Note On source, Latch enabled','Play C3 then later E3','C3 is sustained until next input note-on; Gate and Length disabled; exact retirement ordering U',[84,84])
add(15,'Note Length','positive','Note Off source, Latch enabled','Inspect controls','Gate, Length, Release Velocity, Decay Time and Key Scale disabled',[84,84])
add(15,'Note Length','teardown','Note Off source Latch on; hold C3 E3 with sustain down','Release keys then pedal then send new note-off',None,[84,84],'U')
add(16,'Pitch','positive','Pitch+12st; permissive range, scale off; input C3','Send C3','Output pitch C4; event timing/off U',[88,89])
add(16,'Pitch','positive','Pitch0 StepWidth7st; scale off','Press Step Up then Step Down','Pitch becomes+7 then0',[90,92])
add(16,'Pitch','boundary','Pitch+128st input key127; separately Pitch-128st input key0','Send isolated notes',None,[88,88],'U')
add(17,'Pitch','negative','Pitch0 Block; Lowest C3; accepted positive Range value in UI (unit/upper endpoint U); input C1 safely below range','Send C1','Input pitch blocked; Range LED flashes; off ownership U',[93,95])
add(17,'Pitch','positive','Pitch0 Limit; Lowest C3; accepted positive Range value in UI (unit/upper endpoint U); input C1','Send C1','Output pitch at lower bound C3',[93,97])
add(17,'Pitch','boundary','Pitch0 Fold; Lowest C3; accepted positive Range value in UI (unit/upper endpoint U); input C1','Send C1',None,[93,96],'U')
add(18,'Random','positive','Random Add Chance50% Choices1 Interval12; scale off','Repeat isolated C3 32 times','Every output pitch belongs to {C3,C4}; no frequency/sequence oracle',[103,104])
add(18,'Random','positive','Random Add Chance50% Choices12 Interval1; scale off','Repeat isolated C3 32 times','Every output pitch belongs to C3 or C#3 through C4; finite proportions ungraded',[103,104])
add(18,'Random','negative','Random Sub; input midrange; no overflow','Repeat isolated C3','Altered outputs below C3; zero and minus LEDs correspond to unchanged/lower pitches; exact probabilities U',[107,114])
add(19,'Random','boundary','Alt Chance0%; Choices12 Interval1','Repeat isolated C3','Every output is incoming C3; internal cycle advance/reset U',[105,105])
add(19,'Random','boundary','Fresh Alt Chance100% Choices12 Interval1 scale off','Repeat isolated C3 28 times',None,[106,106],'U')
add(19,'Random','boundary','Fresh Alt Chance100% Choices2 Interval2 scale off','Repeat isolated C3 8 times',None,[106,106],'U')
add(20,'Random','positive','Current clip C major, Use Current Scale on; input C3 in scale','Repeat isolated C3','Generated pitches stay in clip scale; dry off-scale policy not exercised',[115,115])
add(21,'Scale','positive','User matrix maps input C to output D; Fold off, Transpose0, full range','Play C3','Output D3',[119,122])
add(21,'Scale','negative','User mapping for input C removed; full range','Play C3','No output note generated for removed mapping',[122,122])
add(22,'Scale','positive','User maps C3 to A3; Fold initially off','Enable Fold then play C3','Output A2 instead of A3',[124,124])
add(22,'Scale','boundary','User mapping exactly+6st; Fold enabled','Play C3',None,[124,124],'U')
add(23,'Scale','boundary','C-major scale Lowest C2 Range+36st Transpose+7; test below/above range','Play C1 and C5','Outside range pitches unaffected by mapping/transposition',[125,125])
add(23,'Scale','positive','C-major scale Lowest C2 Range+36st Transpose+7; input in scale','Play C2 and B4','Outputs G2 and F#5 by the documented selected-range transposition',[123,125])
add(21,'Scale','positive','Base/Scale Name initially active; clip root/scale defined','Enable Use Current Scale','Base and Scale Name disabled and owned by clip',[121,121])
add(24,'Velocity','positive','Operation Note On; OutLow80 OutHi127; Random0; legal nonzero input notes','Play velocities10,64,120','Output on velocities stay in80..127; exact curve values U',[129,132])
add(25,'Velocity','positive','Fixed mode OutHi100; Random0 Drive0 Compand0; Operation Note On','Play velocities1,64,127','Outgoing on velocity100 for each note; off velocity U',[136,136])
add(25,'Velocity','negative','Gate mode Lowest80 Range20; Operation Note On','Play velocity10','Out-of-range note blocked and gate LED flashes; subsequent off lifecycle U',[133,135])
add(24,'Velocity','positive','Operation Rel.Vel.; Fixed100 Random0 Drive0 Compand0','Play on velocity50 then off velocity20','Operation targets note-off velocity; numeric combined-mode behavior not inferred',[132,132])
add(26,'Velocity','boundary','OutLow60 OutHi127 Random50; legal input velocity100','Repeat isolated notes 32 times','Outputs remain60..127; modulation baseline, displacement, sequence and frequency U',[137,137])
add(26,'Velocity','positive','Drive+50 then-50; Compand0 Random0; input velocities32,64,96','Compare each output curve',None,[139,141],'U')
add(25,'Velocity','boundary','Clip mode Lowest80 Range20; Operation Both; input on velocity0 off velocity127','Send raw events',None,[133,136],'U')
assert len(rows)==66
profiles={
'ARP':('Arpeggiator','Rate','Hold on; C3/E3 held; pattern running'),
'CC':('CC Control','Custom B value','Custom A CC64 on; Custom B assigned CC74; downstream note held'),
'CH':('Chord','Shift1','C3 held, Shift1+7, Chance100%, Strum100ms'),
'NL':('Note Length','Length','Note On Latch on; C3 held'),
'PI':('Pitch','Pitch','Pitch+12st; C3 held'),
'RA':('Random','Chance','Alt Chance100% Choices3 Interval1; C3 held after two completed triggers'),
'SC':('Scale','Transpose','User C-to-D mapping; C3 held'),
'VE':('Velocity','Out Hi','Fixed100; Operation Both; C3 held')}
for short,(dev,param,setup) in profiles.items():
 probes=[
 ('positive',f'Automate {param} between two legal values while held, and exactly at next note-on','Event sampling, held-note changes, scheduling and forwarding'),
 ('boundary','After releasing test notes, send note0 then127; also overlapping same-key ons and offs','Boundary pitch, same-key ownership, output range and matching offs'),
 ('malformed','Submit unpaired note-off; separately incomplete CC message, invalid status/data bytes and nonfinite/out-of-range parameter input','Trust-boundary rejection/normalization/error surface; use bounded independent adapters; no crash oracle assumed'),
 ('cancellation','Cancel a partially edited parameter drag; for CC/Chord additionally enter Learn, receive one assignment, then leave Learn without a completed assignment sequence','Restored versus retained values, emitted events and learned-state cancellation'),
 ('undo',f'Edit {param}, invoke Undo then Redo with and without sounding notes','Undo grouping, restored parameter and output/held-state consequences'),
 ('positive','Disable device while note sounds, deliver its off while bypassed, re-enable, then send a fresh note','Bypass forwarding, retirement, reactivation and possible duplicate/stuck notes'),
 ('positive','Stop/continue transport; separately explicit reset path if exposed; repeat earlier input sequence','Pattern/cycle/held-state retention, pitch-bend/sustain reset and reset availability'),
 ('positive','Save and reopen after named settings/assignments, then repeat input; separately save while note held','Saved control/preset state versus transient held/random/pattern state; emission during reopening'),
 ('teardown','Delete device while note sounds/pending events; separately delete track, change preset and close Set','Scheduled-event cancellation, note-off/sustain/pitch-bend cleanup and output retirement'),
 ('negative','Inject unrelated CC11, channel pressure, pitch bend and per-note bend before/during held note; isolate each event family','Unchanged, consumed, transformed or fanned-out non-note events; channel/MPE association')]
 for i,(kind,action,unknown) in enumerate(probes,1):
  case_setup=('Note On source, Latch off; Free Length200ms Gate100%; Length enabled; C3 held and output still sounding before200ms' if short=='NL' and i in (1,5) else setup)
  rows.append({'id':f'NME-{short}-L{i:02d}','requirement':'REQ-NATIVE-MIDI-027','device':dev,'kind':kind,'setup':case_setup,'action':action,'documentary_oracle':None,'grade':'U','unknown_observable':unknown,'source':None,'exact_build_grade':'U','execution':'unexecuted','comparator':None})
(root/'cases.json').write_text(json.dumps({'revision':2,'target':'Ableton Live12 Suite12.4.3','source_applicability':'Current manual to exact build unresolved','cases':rows},indent=2)+'\n')
from collections import Counter
summary={'total':len(rows),'by_grade':dict(Counter(r['grade'] for r in rows)),'by_device':dict(Counter(r['device'] for r in rows)),'by_kind':dict(Counter(r['kind'] for r in rows)),'executed':0,'exact_build_U':len(rows)}
(root/'case-counts.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
