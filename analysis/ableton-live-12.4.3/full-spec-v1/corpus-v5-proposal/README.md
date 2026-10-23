# Private v5 handoff delta design

This is a design/readiness proposal only. It creates no candidate handoff,
staging package, comparator implementation, adopted owner or release. Root must
separately authorize work after independent R7 owner review and adoption.

[proposal.json](proposal.json) specifies one prospective group027/evaluation
CORPUS-AUDIO-027-01, mapped only to DCO-033 and partial REQ-001/012. It preserves
all 26 old groups, 72 evaluation objects, 81 physical F32 fixtures, old comparator
branches/labels/errors and both existing reference hash guards. The proposed
package would have 27 groups, 73 evaluations and 82 physical F32 fixtures; these
are design counts, not an assembled inventory.

The initial 38-value/order fixture comes from the exact R7 case, matching old
006-01. On one fresh instance, process frames 0–8191 in 512-frame blocks, set only
ListeningXL index15 to 0.75 at boundary8192, then process frames8192–16383 without
resetting or restarting input. The existing input impulse is at4096. No events,
other parameter change, warm-up or transport movement is introduced. A single
additive `parameter_updates` field records that history; no scheduler framework
or general configuration is proposed.

The only measurement-code changes would be a fixed `pickup_step_waveform`
branch and its independent literal step-reference SHA guard. Four independent
checks cover pre/post L/R windows, with full-file length/finiteness and positive
reference/candidate energies on each axis. Each normalized RMS must be at most
0.01, inclusive without epsilon, fitting, alignment or transition exclusion.
The existing channel-major loop reports left-pre, left-post, right-pre,
right-post; the proposal explicitly maps these to the retained method's axis
records. No dependency or old metric changes are needed.

The budget is a new finite engineering choice, not calibrated uncertainty or a
tolerance transfer. Prefix0–4095 is finite-only. The retained concentrated-error
and prefix-corruption passes remain explicit limits. This does not establish
4,000-frame movement, eight-frame latency, general right-channel invariance,
A1, Live/arm64 behavior or a candidate grade. All 174 old modal omissions and
two note72 mode16 omissions remain unchanged.

[providers.json](providers.json) pins immutable/as-of inputs. The R7 owner
proposal is a pending dependency, distinct from the separately approved capture
and actual finite-method validation. No live canonical identity is made a
future gate. The complete v4 comparator/spec/metadata were read as data; old
case objects and fixture hashes were inspected without executing measurements.
Prior capture/method/R7 semantic reads are carried with their exact identities,
not renewed approval of the old 72 comparisons.

Planned checks cover old-object/fixture preservation, literal comparator inverse,
all four axes, trust guards, boundary and invalid controls, isolated export and
sanitization. A dispatch change makes an old72 regression a concrete future
dependency, subject to Root's separate execution selection. The old 4,795
measurements plus four new checks would total4,799 **if actually run**; this
proposal reports no such execution or result. No comparator/evaluator/model,
fit/FFT, original/native or candidate code was run, and no audio was decoded.

Public packaging must be self-contained, without private paths, internal code
or analyst links. New approval/adoption/reviewer metadata must remain pending
until established. The published v4 and all earlier sources stay immutable.
